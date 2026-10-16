#!/usr/bin/env python3
"""regex 与渲染回归哨兵：python3 tests/run-regression.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
import ticket as T  # noqa: E402

FIX = os.path.join(HERE, "fixtures", "cards-2026-10-13.json")


def _patch_fetch(seq):
    """monkeypatch T.fetch_page 按 seq 逐次返回 (page, flaky)，并记录 boundary 调用序列。"""
    calls = []
    real = T.fetch_page

    def fake(cid, boundary, limit):
        calls.append(boundary)
        return seq[len(calls) - 1]
    T.fetch_page = fake
    return real, calls


def main():
    with open(FIX, encoding="utf-8") as fh:
        fix = json.load(fh)
    tickets, order, pw = T.parse_cards(fix["messages"], fix["main_cid"])
    assert pw == [], pw
    exp = fix["expected"]
    assert order == [exp["tid"]], order
    t = tickets[exp["tid"]]
    assert t["title"] == exp["title"], t["title"]
    assert t["creator"] == exp["creator"], t["creator"]
    assert t["xiaoer"] == exp["xiaoer"], t["xiaoer"]
    assert t["status"] == exp["status"], t["status"]
    assert t["subgroup_cid"] == exp["subgroup_cid"], t["subgroup_cid"]
    assert t["desc_card"].startswith(exp["desc_prefix"]), t["desc_card"]
    assert t["sol_card"].startswith(exp["sol_prefix"]), t["sol_card"]
    assert t["chatrecord_url"].startswith("dingtalk://"), t["chatrecord_url"]
    assert t["created_at"] == "2026-10-13 16:11:40", t["created_at"]
    assert t["completed_at"] == "2026-10-14 10:09:09", t["completed_at"]

    cfg = T.load_config()
    customer = [c for c in cfg["customers"] if c["key"] == "haidilao"][0]
    empty_slice = {"ticket_order": [], "tickets": {}, "subgroup_readable": {}}
    md = T.render(customer, "2026-10-12", empty_slice, {})
    assert "零工单" in md, md[:200]
    assert "{{" not in md, "模板占位符未替换"
    assert "海底捞" in md and "20261012" in md

    full_slice = {
        "ticket_order": [exp["tid"]], "tickets": {exp["tid"]: t},
        "subgroup_readable": {exp["tid"]: False},
        "probe_errors": {exp["tid"]: "未入群"},
    }
    md2 = T.render(customer, "2026-10-13", full_slice, {})
    assert exp["tid"] in md2 and "未入群(降级)" in md2 and "{{" not in md2
    assert "实质状态" in md2 and "已完结" in md2

    # 实质状态：无完结卡 + 工程师总结 + 客户确认语 → 已解决待关单
    sub_msgs = [
        {"messageId": "msgSUM==", "sender": "史月函",
         "text": "工单总结如下 【问题描述】SLS project quota达到上限150，客户请求扩容。 【解决方案】1、确认UID信息后，后台调整SLS project quota上限至300，客户验证通过。"},
        {"messageId": "msgCFM==", "sender": "左明", "text": "没有了，谢谢。"},
    ]
    t2 = dict(t)
    t2["completed_at"] = ""
    sig = T.compute_signals(t2, sub_msgs)
    assert len(sig["engineer_summary_msgs"]) == 1, sig
    assert len(sig["customer_confirm_msgs"]) == 1, sig
    assert T.default_effective(t2, sig, True) == "已解决待关单"
    assert T.default_effective(t2, {"engineer_summary_msgs": [], "customer_confirm_msgs": []}, True) == "处理中"
    assert T.default_effective(t2, {"engineer_summary_msgs": [], "customer_confirm_msgs": []}, False) == "无法判定(无子群)"

    # 门禁：子代理引证 messageId 不存在 → 回退规则默认并留痕
    slice3 = {
        "ticket_order": [exp["tid"]],
        "tickets": {exp["tid"]: {**t2, "subgroup_msg_ids": ["msgSUM==", "msgCFM=="]}},
        "subgroup_readable": {exp["tid"]: True},
        "signals": {exp["tid"]: sig},
    }
    bad = {exp["tid"]: {"problem": "p", "process_bullets": [], "solution": "s",
                        "effective_status": "已完结",
                        "effective_evidence": {"message_id": "msgFAKE==", "quote": "x"}}}
    fixed = T.sanitize_summary(bad, slice3)
    assert fixed[exp["tid"]]["effective_status"] == "已解决待关单", fixed
    assert fixed[exp["tid"]]["effective_status_invalid_evidence"] == "msgFAKE=="
    good = {exp["tid"]: dict(bad[exp["tid"]], effective_status="已解决待关单",
                             effective_evidence={"message_id": "msgCFM==", "quote": "没有了，谢谢。"})}
    kept = T.sanitize_summary(good, slice3)
    assert kept[exp["tid"]]["effective_status"] == "已解决待关单"
    assert "effective_status_invalid_evidence" not in kept[exp["tid"]]

    # quote 与所指消息原文不符 → 回退（引文不可编造）
    lying = {exp["tid"]: dict(good[exp["tid"]],
                              effective_evidence={"message_id": "msgCFM==", "quote": "客户承诺加钱"})}
    fixed2 = T.sanitize_summary(lying, slice3, {"E2610138P570LF": {"msgCFM==": "没有了，谢谢。"}})
    assert fixed2[exp["tid"]]["effective_status"] == "已解决待关单"
    assert fixed2[exp["tid"]]["effective_status_invalid_evidence"] == "msgCFM=="
    # 枚举外状态 → 回退
    rogue = {exp["tid"]: dict(good[exp["tid"]], effective_status="已关闭吧大概")}
    fixed3 = T.sanitize_summary(rogue, slice3, {"E2610138P570LF": {"msgCFM==": "没有了，谢谢。"}})
    assert fixed3[exp["tid"]]["effective_status"] == "已解决待关单"

    # 小二本人说「没问题」不算客户确认
    sig_x = T.compute_signals(t2, [{"messageId": "m1", "sender": "邱成相", "text": "没问题，已处理。"}])
    assert sig_x["customer_confirm_msgs"] == [], sig_x
    sig_c = T.compute_signals(t2, [{"messageId": "m2", "sender": "聂伟", "text": "没问题，谢谢！"}])
    assert len(sig_c["customer_confirm_msgs"]) == 1

    # process_bullets 精简合成观察哨 lint_process_bullets（AGENTS.md 规则 N，只报不改）
    assert T.MAX_BULLETS == 8, T.MAX_BULLETS
    # 正控：精简主线（4 条、无时间戳）→ 无告警
    good_b = ["建单与首响：客户报数据源连通失败", "定位白名单争议：工程师澄清 192 网段",
              "找到真因：数据库名称填错", "解决与关单：修正后连通成功并结单"]
    assert T.lint_process_bullets(good_b) == [], T.lint_process_bullets(good_b)
    # 正控：>MAX_BULLETS 条 → 命中条数超限签名
    many = [f"要点{i}" for i in range(9)]
    w_many = T.lint_process_bullets(many)
    assert any("超上限" in w for w in w_many), w_many
    # 正控：过半 bullet 以时间戳开头 → 命中逐条摘录签名（不足 3 条不触发占比判定）
    ts_b = ["16:28 播报建单", "16:29 客户首述", "16:30 工程师响应", "结论"]
    w_ts = T.lint_process_bullets(ts_b)
    assert any("时间戳开头" in w for w in w_ts), w_ts
    # 日期+时间前缀同样识别
    assert T.lint_process_bullets(["2026-10-15 09:22 推送", "09:52 完结", "其他"])
    # 负控：2 条时间戳开头（<3）不触发占比签名，避免小样本误报
    assert "时间戳开头" not in "".join(T.lint_process_bullets(["16:28 建单", "16:30 响应"]))
    # 负控：空/非列表安全返回空
    assert T.lint_process_bullets([]) == []
    assert T.lint_process_bullets(None) == []
    assert T.lint_process_bullets("不是列表") == []
    # 只报不改：lint 不得修改入参
    probe = list(ts_b)
    T.lint_process_bullets(probe)
    assert probe == ts_b, "lint 疑似改动了入参（违反只报不改）"
    # publish._bullets_note 逐工单聚合签名（命中→非空含 tid；无命中→空串）
    slice_bul = {"ticket_order": ["TA", "TB"],
                 "tickets": {"TA": {}, "TB": {}}, "subgroup_readable": {}}
    sum_bul = {"TA": {"process_bullets": many}, "TB": {"process_bullets": good_b}}
    note = T._bullets_note(sum_bul, slice_bul)
    assert "TA" in note and "疑似流水账" in note and "TB" not in note, note
    assert T._bullets_note({"TA": {"process_bullets": good_b}},
                           {"ticket_order": ["TA"]}) == ""

    # 机器人重发建单卡：created_at 不被后到的重发卡覆盖（生产消息升序入 parse）
    dup = list(fix["messages"])
    later = dict(dup[0], createTime="2026-10-13 17:00:00", messageId="msgDUP==")
    tk, od, _ = T.parse_cards(dup + [later], fix["main_cid"])
    assert tk[exp["tid"]]["created_at"] == "2026-10-13 16:11:40", tk[exp["tid"]]["created_at"]
    assert tk[exp["tid"]]["create_msg_id"] == "msg/3vRFCnAV5rVQ0AyYeBHhw=="

    # 表格转义：标题含管道与换行不破坏版面
    t_pipe = dict(t, title="a|b\nc")
    slice4 = {"ticket_order": [exp["tid"]], "tickets": {exp["tid"]: t_pipe},
              "subgroup_readable": {exp["tid"]: True}, "signals": {}, "probe_errors": {}}
    md4 = T.render(customer, "2026-10-13", slice4, {}, followup="## 四、前日工单完结跟进\n\n| 工单ID | 标题 | 建单日 | 完结时间 |\n|---|---|---|---|\n| X | y | z | w |")
    assert "a\\|b c" in md4 and "前日工单完结跟进" in md4 and "{{" not in md4

    # 跟进节纯函数化：prev_collects 由调用方传入，按客户隔离（合思的行不得进海底捞日报）
    prev_data = {"date": "2026-10-12", "customers": {
        "haidilao": {"ticket_order": ["TX"], "tickets": {"TX": {"completed_at": ""}}},
        "hesi": {"ticket_order": ["TY"], "tickets": {"TY": {"completed_at": ""}}}}}
    cur = {"customers": {
        "haidilao": {"tickets": {"TX": {"title": "x", "completed_at": "2026-10-13 10:00:00"}}},
        "hesi": {"tickets": {"TY": {"title": "y", "completed_at": "2026-10-13 11:00:00"}}}}}
    fu = T.followup_section("2026-10-13", cur, [("2026-10-12", prev_data)], "haidilao")
    assert "TX" in fu and "TY" not in fu, fu
    assert T.followup_section("2026-10-13", cur, [], "haidilao") == ""

    # 读盘循环归 _load_prev_collects（cmd_publish 调用）：仅读存在的历史 collect 文件
    prev_path = os.path.join(T.OUT_DIR, "collect-2026-10-12.json")
    with open(prev_path, "w", encoding="utf-8") as fh:
        json.dump(prev_data, fh)
    try:
        loaded = T._load_prev_collects("2026-10-13", days=1)
        assert [d for d, _ in loaded] == ["2026-10-12"], loaded
        fu2 = T.followup_section("2026-10-13", cur, loaded, "haidilao")
        assert "TX" in fu2 and "TY" not in fu2, fu2
    finally:
        os.unlink(prev_path)

    # 跨工单引证隔离 + 缺引证门禁
    slice5 = {
        "ticket_order": ["T1", "T2"],
        "tickets": {
            "T1": {"completed_at": "", "subgroup_msg_ids": ["mA=="]},
            "T2": {"completed_at": "", "subgroup_msg_ids": ["mB=="]}},
        "subgroup_readable": {"T1": True, "T2": True},
        "signals": {"T1": {"engineer_summary_msgs": [{"messageId": "mA=="}],
                           "customer_confirm_msgs": []},
                    "T2": {"engineer_summary_msgs": [{"messageId": "mB=="}],
                           "customer_confirm_msgs": []}},
    }
    cross = {"T1": {"effective_status": "已解决待关单",
                    "effective_evidence": {"message_id": "mB==", "quote": ""}}}
    fx = T.sanitize_summary(cross, slice5, {"T1": {"mA==": "原文甲"}, "T2": {"mB==": "原文乙"}})
    assert fx["T1"]["effective_status"] == "已解决待关单"
    assert fx["T1"]["effective_status_invalid_evidence"] == "mB=="
    noev = {"T1": {"effective_status": "已解决待关单", "effective_evidence": {}}}
    fn = T.sanitize_summary(noev, slice5, {})
    assert fn["T1"]["effective_status_invalid_evidence"] == "<缺引证>"

    # 完结卡缺标题不崩
    done_notitle = [dict(fix["messages"][1], text="@聂伟   企业工单已完结 \n\n 企业工单ID：E2610138P570LF \n\n 企业工单总结：【问题描述】x 【解决方案】y")]
    tk2, _, _ = T.parse_cards(done_notitle, fix["main_cid"])
    assert tk2["E2610138P570LF"]["title"] == ""

    # 乱序输入下最早建单卡（比较式而非顺序式）
    tk3, _, _ = T.parse_cards([dict(fix["messages"][0], createTime="2026-10-13 17:00:00",
                                    messageId="msgLATE==")] + fix["messages"], fix["main_cid"])
    assert tk3[exp["tid"]]["created_at"] == "2026-10-13 16:11:40"

    # 解析哨兵归 parse_cards：卡片缺工单ID / 陌生服务台发送者 → warnings
    no_tid = [dict(fix["messages"][0], text="已为您创建新企业工单（无ID卡）", messageId="msgNT==")]
    _, _, w1 = T.parse_cards(no_tid, fix["main_cid"])
    assert any("缺工单ID" in w for w in w1), w1
    odd = [dict(fix["messages"][0], sender="阿里云服务台2号")]
    _, _, w2 = T.parse_cards(odd, fix["main_cid"])
    assert any("未配置的服务台" in w for w in w2), w2

    # _paginate 统一翻页（monkeypatch fetch_page，不跑 dws）
    # a) 内容页后连续空页 → flaky 告警；boundary 按 min(createTime) 前进
    real, calls = _patch_fetch([
        ([{"messageId": "mA==", "createTime": "2026-10-13 10:00:00"}], False),
        ([], True),
    ])
    try:
        msgs, warns = T.read_messages("cidT", "2026-10-13 00:00:00", "2026-10-14 00:00:00")
    finally:
        T.fetch_page = real
    assert [m["messageId"] for m in msgs] == ["mA=="], msgs
    assert calls == ["2026-10-14 00:00:00", "2026-10-13 10:00:00"], calls
    assert any("连续空页" in w for w in warns), warns

    # b) min(createTime)==boundary → 不前进防死循环告警
    real, _ = _patch_fetch([([{"messageId": "mB==", "createTime": "2026-10-14 00:00:00"}], False)])
    try:
        msgs2, warns2 = T.read_messages("cidT", "2026-10-13 00:00:00", "2026-10-14 00:00:00")
    finally:
        T.fetch_page = real
    assert msgs2 == [] and any("不前进" in w for w in warns2), (msgs2, warns2)

    # c) max_pages 耗尽告警
    real, _ = _patch_fetch([([{"messageId": f"m{i}==", "createTime": f"2026-10-13 0{5 - i}:00:00"}], False)
                            for i in range(5)])
    real_max = T.MAX_PAGES
    T.MAX_PAGES = 2
    try:
        msgs3, warns3 = T.read_messages("cidT", "2026-10-13 00:00:00", "2026-10-14 00:00:00")
    finally:
        T.fetch_page = real
        T.MAX_PAGES = real_max
    assert len(msgs3) == 2 and any("max_pages=2" in w for w in warns3), (msgs3, warns3)

    # d) probe：短页即停（stop_on_short_page）、字段投影、去重
    real, _ = _patch_fetch([
        ([{"messageId": "mS==", "createTime": "2026-10-13 09:00:00", "sender": "s",
           "senderId": "sid", "text": "t", "extra": 1}], False),
    ])
    try:
        sub, w3 = T.probe_subgroup("cidS", lower_bound="2026-10-13 00:00:00")
    finally:
        T.fetch_page = real
    assert sub == [{"createTime": "2026-10-13 09:00:00", "sender": "s", "senderId": "sid",
                    "text": "t", "messageId": "mS=="}], sub
    assert w3 == [], w3

    # select_customers：过滤 / 缺省全量 / 无匹配 sys.exit（collect+publish 共用）
    assert [c["key"] for c in T.select_customers(cfg, "haidilao,hesi")] == ["haidilao", "hesi"]
    assert len(T.select_customers(cfg, None)) == len(cfg["customers"])
    try:
        T.select_customers(cfg, "nope")
        assert False, "无匹配应 sys.exit"
    except SystemExit as se:
        assert "无匹配" in str(se), se

    # doc_title_pattern / verification_markers / 重试常量表
    assert T.doc_title(cfg, "2026-10-13") == cfg["doc_title_pattern"].format(yyyymmdd="20261013")
    assert T.doc_title({}, "2026-10-13") == "20261013工单"
    assert T.verification_markers(customer, full_slice) == [(f"工单日报（{customer['name']}）", "<标题行>")]
    assert ("零工单", "<零工单说明>") in T.verification_markers(customer, empty_slice)
    assert (T.RETRY_TRANSPORT, T.RETRY_EMPTY_PAGE, T.RETRY_AUTH, T.RETRY_CREATE) == (3, 2, 2, 1)

    # 不可读标签三分支 + 窗口外引证标注 + 水印。
    # subgroup_msg_times 与 cmd_collect 产物同形：写在 tickets[tid] 内部（ticket 级）
    slice6 = {"ticket_order": [exp["tid"]],
              "tickets": {exp["tid"]: {**t, "subgroup_msg_ids": ["msgOUT=="],
                                       "subgroup_msg_times": {"msgOUT==": "2026-10-15 09:00:00"}}},
              "subgroup_readable": {exp["tid"]: False},
              "probe_errors": {exp["tid"]: "不可读"},
              "signals": {}}
    sum6 = {exp["tid"]: {"effective_status": "已解决待关单",
                         "effective_evidence": {"message_id": "msgOUT==", "quote": "q"}}}
    md6 = T.render(customer, "2026-10-13", slice6, sum6, watermark="> 注：总结子代理缺失，本篇为规则回退渲染。\n")
    assert "不可读(降级)" in md6 and "（窗口外）" in md6 and "规则回退渲染" in md6 and "{{" not in md6

    # 负控：slice 级 subgroup_msg_times（生产不存在的伪造形状）不再被 render 读取 → 不产生标注
    slice6_neg = {"ticket_order": [exp["tid"]],
                  "tickets": {exp["tid"]: {**t, "subgroup_msg_ids": ["msgOUT=="]}},
                  "subgroup_readable": {exp["tid"]: False},
                  "probe_errors": {exp["tid"]: "不可读"},
                  "signals": {},
                  "subgroup_msg_times": {exp["tid"]: {"msgOUT==": "2026-10-15 09:00:00"}}}
    md6n = T.render(customer, "2026-10-13", slice6_neg, sum6)
    assert "（窗口外）" not in md6n, "slice 级伪造形状仍被读取，render 未走 ticket 级真路径"

    # _doc_folder_id 三层信封容错单测（第四轮 MiniMax-M3 P1-2）：
    # 顶层 folderId / data.folderId / result.folderId 各返回正确值
    assert T._doc_folder_id({"folderId": "F-top"}) == "F-top"
    assert T._doc_folder_id({"data": {"folderId": "F-data"}}) == "F-data"
    assert T._doc_folder_id({"result": {"folderId": "F-result"}}) == "F-result"
    # 全缺 → 代码实际返回空串 ""（publish.py:_doc_folder_id 兜底 return ""）
    assert T._doc_folder_id({"data": {}, "result": {}}) == ""
    assert T._doc_folder_id({}) == ""
    # 负控：folderId 在 messages 正文层（非错误/元数据层）不得被误取
    assert T._doc_folder_id({"data": {"messages": [{"folderId": "F-body"}]}}) == ""
    assert T._doc_folder_id({"messages": [{"folderId": "F-body"}],
                             "data": {"folderId": "F-data"}}) == "F-data"

    # ===== 零工单结转（当日零新工单 → 回看 ≤7 天结转 D0 官方未完结工单）=====
    # 用临时 outputs 文件（不与既有产物碰撞的日期），finally 清理
    def _wj(path, obj):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, ensure_ascii=False)

    d0, d0_done = "2026-10-19", "2026-10-20"   # A 结转源 / B 全完结负控源
    cur_a, cur_b = "2026-10-20", "2026-10-21"  # 两个「当日零新工单」跑批日
    ctid, dtid = "TCARRY01", "TDONE01"
    p_collect = os.path.join(T.OUT_DIR, f"collect-{d0}.json")
    p_summary = os.path.join(T.OUT_DIR, f"summary-{d0}-haidilao.json")
    p_trans = os.path.join(T.OUT_DIR, f"transcripts-{d0}-haidilao.json")
    p_done = os.path.join(T.OUT_DIR, f"collect-{d0_done}.json")
    tmp_paths = [p_collect, p_summary, p_trans, p_done]
    # D0 slice 与 cmd_collect 产物逐键同形（规则 F）：subgroup_msg_times/ids 在 ticket 级
    d0_slice = {
        "name": "海底捞", "cid": "cidMAIN", "ticket_order": [ctid], "warnings": [],
        "tickets": {ctid: {
            "tid": ctid, "title": "结转测试工单", "status": "处理中",
            "creator": "张三", "xiaoer": "李四", "created_at": "2026-10-19 09:00:00",
            "completed_at": "", "subgroup_cid": "cidSUB", "create_msg_id": "msgCREATE==",
            "done_msg_id": "", "desc_card": "建单卡问题描述", "sol_card": "",
            "chatrecord_url": "", "create_card_text": "建单卡原文", "done_card_text": "",
            "subgroup_msg_ids": ["msgSUB1=="],
            "subgroup_msg_times": {"msgSUB1==": "2026-10-19 09:30:00"}}},
        "probe_errors": {ctid: ""},
        "signals": {ctid: {"engineer_summary_msgs": [], "customer_confirm_msgs": []}},
        "subgroup_readable": {ctid: True},
    }
    d0_trans = {"customer_key": "haidilao", "customer_name": "海底捞", "date": d0,
                "window": ["2026-10-19 00:00:00", "2026-10-20 00:00:00"],
                "tickets": {ctid: {
                    "subgroup_messages": [{"messageId": "msgSUB1==",
                                           "text": "这是子群原文片段用于引证",
                                           "createTime": "2026-10-19 09:30:00",
                                           "sender": "李四", "senderId": "sid"}],
                    "create_msg_id": "msgCREATE==", "create_card_text": "建单卡原文",
                    "done_msg_id": "", "done_card_text": ""}}}
    sum_ok = {ctid: {"problem": "结转问题描述", "process_bullets": ["处理步骤一"],
                     "solution": "结转解决方案", "effective_status": "处理中",
                     "effective_evidence": {"message_id": "msgSUB1==", "quote": "子群原文片段"}}}
    sum_bad = {ctid: {"problem": "p", "process_bullets": [], "solution": "s",
                      "effective_status": "已解决待关单",
                      "effective_evidence": {"message_id": "msgFAKE==", "quote": "x"}}}
    done_slice = {
        "name": "海底捞", "cid": "cidMAIN", "ticket_order": [dtid], "warnings": [],
        "tickets": {dtid: {
            "tid": dtid, "title": "已完结工单", "status": "已完结", "creator": "王五",
            "xiaoer": "赵六", "created_at": "2026-10-20 09:00:00",
            "completed_at": "2026-10-20 18:00:00", "subgroup_cid": "",
            "create_msg_id": "msgC2==", "done_msg_id": "msgD2==", "desc_card": "",
            "sol_card": "", "chatrecord_url": "", "create_card_text": "",
            "done_card_text": "", "subgroup_msg_ids": [], "subgroup_msg_times": {}}},
        "probe_errors": {dtid: ""}, "signals": {dtid: {}},
        "subgroup_readable": {dtid: None},
    }
    try:
        _wj(p_collect, {"date": d0, "customers": {"haidilao": d0_slice}, "errors": {}})
        _wj(p_trans, d0_trans)
        _wj(p_done, {"date": d0_done, "customers": {"haidilao": done_slice}, "errors": {}})

        # A) 正控：D0 有未完结工单 → 结转节含「结转自」/tid/D0 日期，旧零工单文案被替换
        _wj(p_summary, sum_ok)
        carry = T._carryover_data("haidilao", T._load_prev_collects(cur_a, days=7), "+08:00")
        assert isinstance(carry, tuple) and carry[0], "应产生结转节 (md, rows) 二元组"
        md_c = T.render(customer, cur_a, empty_slice, {}, carryover=carry)
        assert "三、零工单说明与昨日结转" in md_c, md_c[:400]
        assert "结转自" in md_c and ctid in md_c and d0 in md_c, md_c[:400]
        assert "当日无新工单" in md_c and "窗口内无新工单" in md_c
        assert "窗口内无工单事件（无建单/完结卡片" not in md_c, "旧零工单文案未被结转节替换"
        assert "{{" not in md_c
        # 概览表保持 9 列零行占位（结转工单不入当日概览表，避免与「当日事件」口径混淆）
        assert "| — | — | — | — | — | — | — | — | — |" in md_c, md_c
        # 需求4：effective_status 复用 D0 summary 且经 D0 slice 校验通过 → 保留、无回退留痕
        assert "引证校验失败回退规则" not in md_c
        assert "实质状态：处理中" in md_c and "子群原文片段" in md_c

        # A2) 需求4 失败分支：D0 summary 引证非法 → 回退规则值并留痕（复用既有门禁）
        _wj(p_summary, sum_bad)
        carry_fb_md = T._carryover_data("haidilao", T._load_prev_collects(cur_a, days=7), "+08:00")[0]
        assert "引证校验失败回退规则" in carry_fb_md, carry_fb_md[:400]
        assert "已解决待关单" not in carry_fb_md

        # B) 负控：最近日 D0 全完结 → 纯零工单说明，不结转、不再回看更早日
        carry2 = T._carryover_data("haidilao", T._load_prev_collects(cur_b, days=7), "+08:00")
        assert carry2 == ("", []), carry2
        md_z = T.render(customer, cur_b, empty_slice, {}, carryover=carry2)
        assert "窗口内无工单事件（无建单/完结卡片" in md_z
        assert "结转自" not in md_z and "三、零工单说明与昨日结转" not in md_z
    finally:
        for p in tmp_paths:
            if os.path.exists(p):
                os.unlink(p)

    # ---- publish._reage_urgency（结转单按报告日重新锚定，2026-10-16 修复）----
    # D0 slice 的 urgency 锚在 D0；结转单在报告日仍未完结，须重算 days_span/stalled
    # 并按 title 重算 safety/production_hit（D0 可能是无 urgency 的旧格式 collect）。
    pslice_re = {
        "ticket_order": ["TRE"],
        "tickets": {"TRE": {"tid": "E261013TRE", "title": "es不可用导致生产环境异常",
                            "status": "处理中", "creator": "熊高鹏", "xiaoer": "王震",
                            "created_at": "2026-10-13 14:59:47", "completed_at": "",
                            "subgroup_cid": "", "create_msg_id": "", "done_msg_id": "",
                            "desc_card": "", "sol_card": "", "subgroup_msg_ids": [],
                            "subgroup_msg_times": {}}},
        "signals": {"TRE": {}},  # 旧格式：无 urgency
        "subgroup_readable": {"TRE": False},
        "probe_errors": {"TRE": "未入群"},
    }
    reaged = T._reage_urgency(pslice_re, ["TRE"], "2026-10-15")
    urg = reaged["signals"]["TRE"]["urgency"]
    assert urg["days_span"] == 2, urg          # 10-13 → 10-15
    assert urg["completed"] is False, urg
    assert urg["production_hit"] != "", urg     # 标题「生产/不可用/异常」命中，重算而非信旧值
    assert pslice_re["signals"]["TRE"] == {}, "不得原地改动入参 pslice"
    # re-aged 后 compute_attention 应升 🟡（跨天未完结 + 生产故障标题），不再是 ⚪
    e_re, lv_re, _ = T.compute_attention(pslice_re["tickets"]["TRE"], urg, "无法判定")
    assert (e_re, lv_re) == ("🟡", "留意"), (e_re, lv_re)
    # 第五轮评审 P2-6：复用 D0 非空 last_active（子群可读）→ 按报告日重算 stalled
    pslice_la = {**pslice_re,
                 "tickets": {"TRE": {**pslice_re["tickets"]["TRE"], "title": "普通咨询"}},
                 "signals": {"TRE": {"urgency": {"last_active": "2026-10-13 10:00:00",
                                                 "readable": True}}},
                 "subgroup_readable": {"TRE": True}}
    urg_la = T._reage_urgency(pslice_la, ["TRE"], "2026-10-15")["signals"]["TRE"]["urgency"]
    assert urg_la["last_active"] == "2026-10-13 10:00:00", urg_la  # 复用 D0 原值
    assert urg_la["stalled"] is True, urg_la   # 报告日 10-15 距最后活动 >24h → 僵单
    # 第五轮评审 P2-5：report_date 畸形 → 原样返回 pslice，不崩溃
    assert T._reage_urgency(pslice_re, ["TRE"], "不是日期") is pslice_re

    # 集成：_carryover_data 带 report_date → 结转单 re-age 后升 🟡，(md, rows) 的 rows
    # 非空，供 render 顶部「零、重点关注」合并（修复顶部漏列结转跨天单的口径不一致）。
    # 用不与既有产物碰撞的丢弃日期（D0=10-27、报告日=10-29，跨度 2 天），finally 清理。
    d0_re, rep_re = "2026-10-27", "2026-10-29"
    p_col_re = os.path.join(T.OUT_DIR, f"collect-{d0_re}.json")
    p_tr_re = os.path.join(T.OUT_DIR, f"transcripts-{d0_re}-hesi.json")
    _wj(p_col_re, {"date": d0_re, "customers": {"hesi": pslice_re}, "errors": {}})
    _wj(p_tr_re, {"customer_key": "hesi", "date": d0_re, "tickets": {}})
    try:
        carry_md, carry_rows = T._carryover_data(
            "hesi", T._load_prev_collects(rep_re, days=7), "+08:00", report_date=rep_re)
        assert carry_rows and carry_rows[0][0] == "🟡", carry_rows
        assert "🟡" in carry_md, carry_md[:200]
        # 顶部合并渲染：结转 🟡 出现在「零、重点关注」节
        md_top = T.render({"name": "合思", "service_group_name": "g"}, rep_re,
                          empty_slice, {}, carryover=(carry_md, carry_rows))
        top_sec = md_top.split("## 一、概览")[0]
        assert "TRE" in top_sec and "🟡" in top_sec, top_sec
        assert "今日无重点关注工单" not in top_sec, "结转跨天单未进顶部重点关注节"
    finally:
        for fp in [p_col_re, p_tr_re]:
            if os.path.exists(fp):
                os.unlink(fp)

    # 自动入群告警日期门：补跑老日期不告警（入群配置不追溯历史子群），昨日跑批仍告警
    from neil_ticket import collect as C
    from datetime import datetime as _dt, timedelta as _td
    gap_slice = {"ticket_order": ["T1"],
                 "tickets": {"T1": {"subgroup_cid": "cidX=="}},
                 "subgroup_readable": {"T1": False}}
    cust_exp = {"auto_join_expected": True}
    yesterday = (_dt.now(T.cfg_tz()) - _td(days=1)).strftime("%Y-%m-%d")
    assert C._auto_join_gap(cust_exp, gap_slice, "2026-10-13") is False
    assert C._auto_join_gap(cust_exp, gap_slice, yesterday) is True
    assert C._auto_join_gap({"auto_join_expected": False}, gap_slice, yesterday) is False

    # ===== 机械完成判定 check_status（qoder_cron 巡检补偿依据，check 子命令纯函数）=====
    # 临时写 outputs/run-<某日>.json（不与既有产物碰撞的日期），finally 清理
    run_date = "2026-10-22"
    p_run = os.path.join(T.OUT_DIR, f"run-{run_date}.json")
    now_tz = _dt.now(T.cfg_tz())
    today_iso = now_tz.isoformat(timespec="seconds")
    yesterday_iso = (now_tz - _td(days=1)).isoformat(timespec="seconds")
    try:
        # a) 标记不存在 → (False, "marker_absent")
        assert not os.path.exists(p_run), "回归前提：临时 run 标记不得已存在"
        ok, reason = T.check_status(run_date)
        assert ok is False and reason == "marker_absent", (ok, reason)
        # b) finished_at=今天（配置时区）→ (True, finished_at 原值)
        _wj(p_run, {"date": run_date, "finished_at": today_iso,
                    "results": [], "errors": {}})
        ok, reason = T.check_status(run_date)
        assert ok is True and reason == today_iso, (ok, reason)
        # c) finished_at=昨天 → (False, "stale:finished_at")
        _wj(p_run, {"date": run_date, "finished_at": yesterday_iso,
                    "results": [], "errors": {}})
        ok, reason = T.check_status(run_date)
        assert ok is False and reason == "stale:finished_at", (ok, reason)
        # d) 标记损坏（缺 finished_at 键）→ 抛异常（cmd_check 归 exit 1）
        _wj(p_run, {"date": run_date})
        try:
            T.check_status(run_date)
            assert False, "缺 finished_at 应抛异常"
        except KeyError:
            pass
    finally:
        if os.path.exists(p_run):
            os.unlink(p_run)

    # publish 机械幂等门负控：当日标记存在且无 --force 时 cmd_publish 必须早退；
    # 门禁若失效会因缺 collect-2099-01-01.json 抛 FileNotFoundError 暴露
    import argparse as _ap
    gate_marker = os.path.join(T.OUT_DIR, "run-2099-01-01.json")
    with open(gate_marker, "w", encoding="utf-8") as fh:
        json.dump({"date": "2099-01-01",
                   "finished_at": _dt.now(T.cfg_tz()).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
                   "results": [], "errors": {}}, fh)
    try:
        T.cmd_publish(_ap.Namespace(date="2099-01-01", customers=None, force=False))
    finally:
        os.unlink(gate_marker)

    # =====================================================================
    # 新功能：工单连续性 + 负面情绪 + 关注等级三档（AGENTS.md 规则 Q/R）
    # =====================================================================
    from datetime import date as _date

    # ---- parse.compute_urgency_signals（today 传 date 对象；纯事实抽取）----
    # 催单命中路径①（子群独立机器人消息，真实生产路径）：催单事件是「阿里云服务台」在
    # 子群发的独立消息，正文含「催单信息：<font >业务阻塞</font>」，不在建单卡里。
    # 这是 2026-10-16 修复的真 bug（原来只扫 create/done_card_text，催单永不触发）。
    tk_u = {"tid": "E2610143Y5HYZP", "title": "数据库查询突然变慢超时",
            "created_at": "", "completed_at": "2026-10-15 09:52:10"}
    sub_urge = [{"messageId": "mU1", "createTime": "2026-10-15 09:00:00",
                 "text": "#### 您好，钉群服务已经收到您的催单。\n ****** \n "
                         ">###### 催单信息：<font >业务阻塞</font> \n >###### 企业工单ID：E2610143Y5HYZP"}]
    sig_urge_sub = T.compute_urgency_signals(tk_u, sub_urge, _date(2026, 10, 15))
    assert sig_urge_sub["urge_reason"] == "业务阻塞", sig_urge_sub
    assert T._detect_urge(sub_urge, "", "") == "业务阻塞"
    # 催单命中路径②（建单/完结卡文本，向后兼容）：create_card_text 含「催单信息：」→ urge_reason
    card_urge = " ****** \n >###### 催单信息：<font color=#F00>业务阻塞</font> \n >###### 企业工单ID：E2610143Y5HYZP"
    sig_urge = T.compute_urgency_signals(tk_u, [], _date(2026, 10, 15),
                                         create_card_text=card_urge)
    assert sig_urge["urge_reason"] == "业务阻塞", sig_urge
    # 负控（防误报）：普通建单卡 Tips 里有「催单」按钮链接但无「催单信息：」→ urge_reason 为空
    card_plain = ("已为您创建新企业工单 企业工单标题：<font color=#096DD9>x</font> "
                  "企业工单ID：E2610143Y5HYZP Tips：可以点击[催单]"
                  "(dingtalk://dingtalkclient/page/link?url=task%2Furge%3Ftid%3D1)为您加急处理。")
    sig_plain = T.compute_urgency_signals(tk_u, [], _date(2026, 10, 15),
                                          create_card_text=card_plain)
    assert sig_plain["urge_reason"] == "", sig_plain
    # 负控：子群普通消息（含「催单」二字但非「催单信息：」事件）不误报
    assert T._detect_urge([{"text": "您可以点击催单按钮加急"}], "", "") == ""
    # 安全词 / 生产词命中（标题词表）
    assert T.compute_urgency_signals({"tid": "T", "title": "waf注入漏洞"}, [],
                                     _date(2026, 10, 16))["safety_hit"] != ""
    assert T.compute_urgency_signals({"tid": "T", "title": "es不可用导致生产环境异常"}, [],
                                     _date(2026, 10, 16))["production_hit"] != ""
    # 存活天数：created_at 为空时靠 tid 前缀 E26MMDD 仍能算跨度
    # E26 10 14 → date(2026,10,14)；completed_at 2026-10-15 → span==1
    assert sig_urge["days_span"] == 1, sig_urge
    assert T._ticket_open_date("E2610143Y5HYZP", "") == _date(2026, 10, 14)
    # 僵单三分支
    # a) 子群可读 + 未完结 + 最近活动距今 >24h → stalled True
    tk_st = {"tid": "E2610143Y5HYZP", "created_at": "", "completed_at": ""}
    sig_st = T.compute_urgency_signals(
        tk_st, [{"createTime": "2026-10-14 10:00:00", "messageId": "m1"}],
        _date(2026, 10, 16))
    assert sig_st["readable"] is True and sig_st["stalled"] is True, sig_st
    # b) 子群不可读（readable=False 且 sub_messages 空）+ 未完结 → stalled False（降级单不判僵单）
    sig_nost = T.compute_urgency_signals(
        {**tk_st, "subgroup_readable": False}, [], _date(2026, 10, 16))
    assert sig_nost["readable"] is False and sig_nost["stalled"] is False, sig_nost
    # c) 已完结 → stalled False
    sig_done = T.compute_urgency_signals(
        {"tid": "E2610143Y5HYZP", "created_at": "", "completed_at": "2026-10-16 09:00:00"},
        [{"createTime": "2026-10-14 10:00:00", "messageId": "m1"}], _date(2026, 10, 16))
    assert sig_done["completed"] is True and sig_done["stalled"] is False, sig_done
    assert T._is_stalled(2, "", "", False, _date(2026, 10, 16)) is False, "不可读降级单不应判僵单"

    # ---- parse.compute_attention → (emoji, level_name, reasons) 三档 ----
    # 🔴重点
    e, lv, rs = T.compute_attention({}, {"urge_reason": "业务阻塞"}, "无")
    assert (e, lv) == ("🔴", "重点") and any("催单" in r for r in rs), (e, lv, rs)
    e, lv, _ = T.compute_attention({}, {"safety_hit": "漏洞"}, "无")
    assert (e, lv) == ("🔴", "重点"), (e, lv)
    e, lv, rs = T.compute_attention({}, {"completed": False, "days_span": 1}, "明显")
    assert (e, lv) == ("🔴", "重点") and any("未完结且客户明显负面情绪" in r for r in rs), (e, lv, rs)
    # span=0 当天建单未完结 + 明显负面：措辞不得谎称「跨天」（第五轮评审 P2-3）
    e, lv, rs = T.compute_attention({}, {"completed": False, "days_span": 0}, "明显")
    assert (e, lv) == ("🔴", "重点") and any("未完结" in r for r in rs) and not any("跨天" in r for r in rs), (e, lv, rs)
    e, lv, rs = T.compute_attention({}, {"completed": True}, "明显")
    assert (e, lv) == ("🔴", "重点") and any("明显负面情绪" in r for r in rs), (e, lv, rs)
    # 🟡留意
    e, lv, rs = T.compute_attention({}, {"completed": False, "days_span": 2}, "无")
    assert e == "🟡" and lv == "留意" and any("存活 2 天" in r for r in rs), (e, lv, rs)
    e, lv, _ = T.compute_attention({}, {}, "轻微")
    assert e == "🟡", (e, lv)
    e, lv, _ = T.compute_attention({}, {"production_hit": "生产"}, "无")
    assert e == "🟡", (e, lv)
    e, lv, _ = T.compute_attention({}, {"stalled": True}, "无")
    assert e == "🟡", (e, lv)
    # 跨天已完结（耗时≥2天）→ 🟡留意（关注服务时效，用户规则 a：仅当天完结算常规）
    e, lv, rs = T.compute_attention({}, {"completed": True, "days_span": 2}, "无")
    assert (e, lv) == ("🟡", "留意") and any("跨天已完结" in r for r in rs), (e, lv, rs)
    # ⚪常规：已完结 + 当天(span=0) + sentiment 无
    e, lv, rs = T.compute_attention({}, {"completed": True, "days_span": 0}, "无")
    assert (e, lv) == ("⚪", "常规") and rs == ["当天完结普通问答"], (e, lv, rs)
    # 优先级：同时满足🔴（催单）和🟡（跨天未完结）→ 🔴 重点
    e, lv, rs = T.compute_attention({}, {"urge_reason": "业务阻塞", "completed": False,
                                         "days_span": 3}, "无")
    assert (e, lv) == ("🔴", "重点") and any("催单" in r for r in rs), (e, lv, rs)

    # ---- gate.sanitize_sentiment（与 sanitize_summary 同构，规则 Q）----
    assert T.SENTIMENT_ENUM == {"无", "轻微", "明显", "无法判定"}, T.SENTIMENT_ENUM
    assert T.SENTIMENT_NEEDS_EVIDENCE == {"轻微", "明显"}, T.SENTIMENT_NEEDS_EVIDENCE
    assert T._allowed_ids({"create_msg_id": "c1", "done_msg_id": "",
                           "subgroup_msg_ids": ["s1", "s2"]}) == {"c1", "s1", "s2"}
    sl_slice = {"tickets": {"TS": {"create_msg_id": "msgC==", "done_msg_id": "",
                                   "subgroup_msg_ids": ["msgS==", "msgX=="]}}}
    sl_texts = {"TS": {"msgS==": "这个方案根本不行，太让人失望了", "msgX==": "好的收到"}}
    # 正控：level=明显 + 合法引证（message_id 在本工单、quote 是原文子串）→ 保留、无留痕
    good_sent = {"TS": {"sentiment": {"level": "明显",
                                      "evidence": {"message_id": "msgS==", "quote": "根本不行"},
                                      "reason": "客户明确表达不满"}}}
    g_out = T.sanitize_sentiment(good_sent, sl_slice, sl_texts)
    assert g_out["TS"]["sentiment"]["level"] == "明显", g_out
    assert "sentiment_invalid_evidence" not in g_out["TS"], g_out
    # 负控：伪造 quote（非原文子串）→ 回退无法判定 + 留痕该 message_id
    fake_q = {"TS": {"sentiment": {"level": "明显",
                                   "evidence": {"message_id": "msgS==", "quote": "客户承诺加钱"},
                                   "reason": "编造"}}}
    fq_out = T.sanitize_sentiment(fake_q, sl_slice, sl_texts)
    assert fq_out["TS"]["sentiment"]["level"] == "无法判定", fq_out
    assert fq_out["TS"]["sentiment_invalid_evidence"] == "msgS==", fq_out
    # 负控：缺引证（level=轻微 但 evidence={}）→ 回退 + <缺引证>
    no_ev = {"TS": {"sentiment": {"level": "轻微", "evidence": {}, "reason": "r"}}}
    ne_out = T.sanitize_sentiment(no_ev, sl_slice, sl_texts)
    assert ne_out["TS"]["sentiment"]["level"] == "无法判定", ne_out
    assert ne_out["TS"]["sentiment_invalid_evidence"] == "<缺引证>", ne_out
    # 负控：跨工单（message_id 不在本工单 allowed）→ 回退 + 留痕
    cross = {"TS": {"sentiment": {"level": "明显",
                                  "evidence": {"message_id": "msgOTHER==", "quote": "q"},
                                  "reason": "r"}}}
    cr_out = T.sanitize_sentiment(cross, sl_slice, sl_texts)
    assert cr_out["TS"]["sentiment"]["level"] == "无法判定", cr_out
    assert cr_out["TS"]["sentiment_invalid_evidence"] == "msgOTHER==", cr_out
    # 负控：枚举外 level → 回退无法判定
    rogue_lv = {"TS": {"sentiment": {"level": "气死了",
                                     "evidence": {"message_id": "msgS==", "quote": "根本不行"},
                                     "reason": "r"}}}
    rl_out = T.sanitize_sentiment(rogue_lv, sl_slice, sl_texts)
    assert rl_out["TS"]["sentiment"]["level"] == "无法判定", rl_out
    # 缺字段：summary 某工单无 sentiment 键 → level 无法判定 + sentiment_missing
    miss = {"TS": {"problem": "p"}}
    ms_out = T.sanitize_sentiment(miss, sl_slice, sl_texts)
    assert ms_out["TS"]["sentiment"]["level"] == "无法判定", ms_out
    assert ms_out["TS"].get("sentiment_missing") is True, ms_out
    # level=无 无引证 → 保留「无」，无留痕（默认安全值不需引证）
    none_sent = {"TS": {"sentiment": {"level": "无", "evidence": {}, "reason": ""}}}
    nn_out = T.sanitize_sentiment(none_sent, sl_slice, sl_texts)
    assert nn_out["TS"]["sentiment"]["level"] == "无", nn_out
    assert "sentiment_invalid_evidence" not in nn_out["TS"], nn_out
    # 第五轮评审 P1-1：evidence 非 dict（LLM 结构异常）不得崩溃，需引证档回退留痕
    bad_ev = {"TS": {"sentiment": {"level": "明显", "evidence": "msgS==", "reason": "r"}}}
    be_out = T.sanitize_sentiment(bad_ev, sl_slice, sl_texts)
    assert be_out["TS"]["sentiment"]["level"] == "无法判定", be_out
    assert be_out["TS"]["sentiment_invalid_evidence"] == "<evidence结构异常>", be_out
    # 非 dict evidence + 宽容档（无）→ 放行不崩溃
    bad_ev2 = {"TS": {"sentiment": {"level": "无", "evidence": ["x"], "reason": ""}}}
    assert T.sanitize_sentiment(bad_ev2, sl_slice, sl_texts)["TS"]["sentiment"]["level"] == "无"
    # 第五轮评审 P1-2：空 quote + 真实 message_id 不得绕过（规则 E 明令禁止空 quote 绕过）
    empty_q = {"TS": {"sentiment": {"level": "明显",
                                    "evidence": {"message_id": "msgS==", "quote": ""},
                                    "reason": "r"}}}
    eq_out = T.sanitize_sentiment(empty_q, sl_slice, sl_texts)
    assert eq_out["TS"]["sentiment"]["level"] == "无法判定", eq_out
    assert eq_out["TS"]["sentiment_invalid_evidence"] == "<空quote>", eq_out
    # _evidence_bad 共用核心：sanitize_summary 同源，空 quote 也拦（effective_status 侧）
    sum_empty_q = {"TS": {"effective_status": "已解决待关单",
                          "effective_evidence": {"message_id": "msgS==", "quote": ""}}}
    sl_slice_sig = {"tickets": sl_slice["tickets"], "signals": {"TS": {}},
                    "subgroup_readable": {"TS": True}}
    seq_out = T.sanitize_summary(sum_empty_q, sl_slice_sig, sl_texts)
    assert seq_out["TS"]["effective_status_invalid_evidence"] == "<空quote>", seq_out
    # 词表逐字 pin（规则 L：改词表须同步回归断言，删词会被此断言拦下）
    assert T.SAFETY_KEYWORDS == ("漏洞", "注入", "绕过", "泄露", "越权", "攻击", "安全风险", "waf"), T.SAFETY_KEYWORDS
    assert T.PRODUCTION_KEYWORDS == ("生产", "不可用", "宕机", "故障", "挂了", "影响业务",
                                     "业务阻塞", "无法访问", "报错", "异常", "中断", "超时"), T.PRODUCTION_KEYWORDS
    # RE_URGE 兼容半角冒号变体（第五轮评审 P2-7）
    assert T.RE_URGE.search("催单信息:业务阻塞 ").group(1) == "业务阻塞"
    assert T.RE_URGE.search("催单信息：<font >业务阻塞</font> ").group(1) == "业务阻塞"

    # ---- render._attention_rows + _attention_section（rows 解耦，支持当日+结转合并）----
    at_slice = {"ticket_order": ["TY", "TR"],  # 🟡 在前、🔴 在后：验证红前黄后靠 emoji 排序
                "tickets": {"TY": {"title": "跨天未结单"}, "TR": {"title": "催单业务阻塞"}}}
    at_map = {"TY": ("🟡", "留意", ["跨天未完结（存活 2 天）"]),
              "TR": ("🔴", "重点", ["催单事件：业务阻塞"])}
    at_rows = T._attention_rows(at_slice, at_map)
    # _attention_rows 只收 🔴/🟡，⚪不入表
    assert all(r[0] in ("🔴", "🟡") for r in at_rows) and len(at_rows) == 2, at_rows
    sec = T._attention_section(at_rows)
    assert "## 零、重点关注" in sec, sec
    assert sec.index("TR") < sec.index("TY"), "🔴行应在🟡行之前：" + sec
    assert "催单事件：业务阻塞" in sec and "🔴" in sec and "🟡" in sec, sec
    # 合并：当日行 + 结转行一起渲染（结转跨多日未完结单也要在顶部列出）
    carry_rows = [("🔴", "TCARRY", "结转生产故障", "重点", ["催单事件：业务阻塞"])]
    sec_merge = T._attention_section(at_rows + carry_rows)
    assert "TCARRY" in sec_merge and "TR" in sec_merge and "TY" in sec_merge, sec_merge
    # 全⚪ → 今日无重点关注工单
    all_norm = {"T1": ("⚪", "常规", ["当天完结普通问答"])}
    sec0 = T._attention_section(T._attention_rows(
        {"ticket_order": ["T1"], "tickets": {"T1": {"title": "x"}}}, all_norm))
    assert "今日无重点关注工单" in sec0 and "🔴" not in sec0, sec0

    # ---- render._sentiment_line ----
    ln = T._sentiment_line({"sentiment": {"level": "明显", "reason": "客户明显不满",
                                          "evidence": {"quote": "根本不行"}}})
    assert "⚠️ 情绪信号（明显）" in ln and "根本不行" in ln, ln
    ln2 = T._sentiment_line({"sentiment": {"level": "无法判定", "reason": "", "evidence": {}}})
    assert "无法判定" in ln2, ln2
    # 第五轮评审 P1-2：引证校验失败回退必须可观测（与 effective_status 对齐，非虚标死码）
    ln_inv = T._sentiment_line({"sentiment": {"level": "无法判定", "evidence": {}},
                                "sentiment_invalid_evidence": "msgFAKE=="})
    assert "引证校验失败回退" in ln_inv and "msgFAKE==" in ln_inv, ln_inv
    # 无留痕的无法判定 → 通用文案，不含「引证校验失败」
    assert "引证校验失败回退" not in ln2, ln2
    # evidence 非 dict 不崩溃
    assert "无法判定" in T._sentiment_line({"sentiment": {"level": "无法判定", "evidence": "x"}})
    assert T._sentiment_line({"sentiment_missing": True,
                              "sentiment": {"level": "无法判定"}}) == ""
    assert T._sentiment_line({"sentiment": {"level": "无"}}) == ""

    # ---- render._overview_row（新签名带 span/emoji；9 列）----
    row_t = {"title": "标题", "status": "处理中", "creator": "甲", "xiaoer": "乙"}
    row = T._overview_row("TR", row_t, "处理中", True, "", 2, "🔴")
    assert "2天" in row and "🔴" in row, row
    assert row.count("|") == 10, f"概览行应为 9 列（10 个 |）：{row}"

    # ---- render 端到端（含 signals[tid].urgency + summary.sentiment）----
    e2e_tid = "E2610143Y5HYZP"
    e2e_t = {**T._blank_ticket(e2e_tid), "title": "数据库查询突然变慢超时",
             "status": "处理中", "creator": "张腾龙", "xiaoer": "楚成龙",
             "created_at": "2026-10-14 09:12:33",
             "subgroup_msg_ids": ["msgS=="], "subgroup_msg_times": {}}
    e2e_slice = {"ticket_order": [e2e_tid], "tickets": {e2e_tid: e2e_t},
                 "subgroup_readable": {e2e_tid: True},
                 "probe_errors": {e2e_tid: ""},
                 "signals": {e2e_tid: {"urgency": {"days_span": 2, "completed": False,
                                                   "urge_reason": "业务阻塞",
                                                   "safety_hit": "", "production_hit": "",
                                                   "readable": True, "stalled": False,
                                                   "last_active": ""}}}}
    e2e_sum = {e2e_tid: {"problem": "p", "process_bullets": ["定位慢查询"], "solution": "s",
                         "effective_status": "处理中",
                         "effective_evidence": {"message_id": "msgS==", "quote": "q"},
                         "sentiment": {"level": "明显", "reason": "客户催促不满",
                                       "evidence": {"message_id": "msgS==", "quote": "太慢"}}}}
    md_e = T.render(customer, "2026-10-16", e2e_slice, e2e_sum)
    assert "零、重点关注" in md_e, md_e[:400]
    assert "🔴" in md_e and "存活" in md_e and "关注" in md_e, md_e[:600]
    assert "⚠️ 情绪信号（明显）" in md_e, md_e
    assert "{{" not in md_e, "模板占位符未替换"

    # ---- collect._merged_signals（合并 compute_signals + compute_urgency_signals）----
    m_ticket = {"tid": "E2610164MG01", "title": "扩容", "xiaoer": "史月函",
                "created_at": "2026-10-16 09:00:00", "completed_at": "",
                "create_card_text": "建单卡", "done_card_text": ""}
    m_submsgs = [
        {"messageId": "mS==", "sender": "史月函", "createTime": "2026-10-16 10:00:00",
         "text": "工单总结如下 【问题描述】SLS project 配额达到上限 150，客户请求扩容以支撑新业务写入。 【解决方案】1、确认 UID 信息后，后台调整 SLS project 配额上限至 300；2、客户验证读写恢复正常，确认可以关单，本次处理完毕。"},
        {"messageId": "mC==", "sender": "聂伟", "createTime": "2026-10-16 11:00:00",
         "text": "没有了，谢谢。"},
    ]
    m_entry = {"subgroup_messages": m_submsgs,
               "signals": T.compute_signals(m_ticket, m_submsgs)}
    merged = T._merged_signals(m_ticket, m_entry, _date(2026, 10, 16))
    assert "engineer_summary_msgs" in merged and "customer_confirm_msgs" in merged, merged
    assert len(merged["engineer_summary_msgs"]) == 1, merged
    assert len(merged["customer_confirm_msgs"]) == 1, merged
    assert isinstance(merged.get("urgency"), dict), merged
    assert merged["urgency"]["days_span"] == 0, merged

    # ---- publish._watermark ----
    assert "总结子代理缺失" in T._watermark(True, {}), T._watermark(True, {})
    assert "未产出情绪判定" in T._watermark(False, {"T1": {"sentiment_missing": True}})
    assert T._watermark(False, {"T1": {"sentiment": {"level": "无"}}}) == ""

    # ---- 新 fixture：cards-2026-10-16-attention.json（催单/安全/普通完结三张卡）----
    fix_attn_path = os.path.join(HERE, "fixtures", "cards-2026-10-16-attention.json")
    with open(fix_attn_path, encoding="utf-8") as fh:
        fix_attn = json.load(fh)
    tk_a, order_a, w_a = T.parse_cards(fix_attn["messages"], fix_attn["main_cid"])
    assert w_a == [], w_a
    exp_a = fix_attn["expected"]
    assert order_a == exp_a["order"], order_a
    for tid_a, fields in exp_a["tickets"].items():
        for k_a, v_a in fields.items():
            assert tk_a[tid_a][k_a] == v_a, f"{tid_a}.{k_a}: {tk_a[tid_a][k_a]!r} != {v_a!r}"
    # 催单信号走子群消息路径（真实生产形态，2026-10-16 修复的 bug）：建单卡本身不含催单信息，
    # 催单事件是子群里阿里云服务台的独立机器人消息（fixture 的 subgroup_messages 段）。
    sub_a = fix_attn["subgroup_messages"]
    urge_t = tk_a["E2610144URGE01"]
    # 负控：建单卡（仅 Tips 有催单按钮链接）不触发催单信息
    assert not T.RE_URGE.search(urge_t["create_card_text"]), "建单卡不应含催单信息（那是按钮链接）"
    assert T._detect_urge([], urge_t["create_card_text"], urge_t["done_card_text"]) == ""
    # 正控：子群消息命中「催单信息：<font >业务阻塞</font>」
    urge_sig = T.compute_urgency_signals(
        urge_t, sub_a["E2610144URGE01"], _date(2026, 10, 16),
        create_card_text=urge_t["create_card_text"], done_card_text=urge_t["done_card_text"])
    assert urge_sig["urge_reason"] == exp_a["urge_reason"], urge_sig
    assert urge_sig["days_span"] == 2, urge_sig  # E261014 建单 → 工单日 2026-10-16
    # 安全卡：标题含 waf/注入/漏洞 → safety_hit 非空
    safe_sig = T.compute_urgency_signals(tk_a["E2610164SAFE01"], sub_a["E2610164SAFE01"],
                                         _date(2026, 10, 16))
    assert safe_sig["safety_hit"] != "", safe_sig
    # 普通当天完结卡：completed True + span 0 + 无 sentiment → ⚪常规
    done_a = tk_a["E2610164DONE01"]
    done_sig = T.compute_urgency_signals(done_a, sub_a["E2610164DONE01"], _date(2026, 10, 16),
                                         create_card_text=done_a["create_card_text"],
                                         done_card_text=done_a["done_card_text"])
    assert T.compute_attention(done_a, done_sig, "无")[0] == "⚪", done_sig
    # 催单卡跨天+催单 → 🔴（优先级验证）
    assert T.compute_attention(urge_t, urge_sig, "无")[:2] == ("🔴", "重点")

    print("REGRESSION OK")


if __name__ == "__main__":
    main()
