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
        assert carry, "应产生结转节"
        md_c = T.render(customer, cur_a, empty_slice, {}, carryover=carry)
        assert "三、零工单说明与昨日结转" in md_c, md_c[:400]
        assert "结转自" in md_c and ctid in md_c and d0 in md_c, md_c[:400]
        assert "当日无新工单" in md_c and "窗口内无新工单" in md_c
        assert "窗口内无工单事件（无建单/完结卡片" not in md_c, "旧零工单文案未被结转节替换"
        assert "{{" not in md_c
        # 概览表保持零行占位（结转工单不入概览表，避免与「当日事件」口径混淆）
        assert "| — | — | — | — | — | — | — |" in md_c
        # 需求4：effective_status 复用 D0 summary 且经 D0 slice 校验通过 → 保留、无回退留痕
        assert "引证校验失败回退规则" not in md_c
        assert "实质状态：处理中" in md_c and "子群原文片段" in md_c

        # A2) 需求4 失败分支：D0 summary 引证非法 → 回退规则值并留痕（复用既有门禁）
        _wj(p_summary, sum_bad)
        carry_fb = T._carryover_data("haidilao", T._load_prev_collects(cur_a, days=7), "+08:00")
        assert "引证校验失败回退规则" in carry_fb, carry_fb[:400]
        assert "已解决待关单" not in carry_fb

        # B) 负控：最近日 D0 全完结 → 纯零工单说明，不结转、不再回看更早日
        carry2 = T._carryover_data("haidilao", T._load_prev_collects(cur_b, days=7), "+08:00")
        assert carry2 == "", carry2
        md_z = T.render(customer, cur_b, empty_slice, {}, carryover=carry2)
        assert "窗口内无工单事件（无建单/完结卡片" in md_z
        assert "结转自" not in md_z and "三、零工单说明与昨日结转" not in md_z
    finally:
        for p in tmp_paths:
            if os.path.exists(p):
                os.unlink(p)

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

    print("REGRESSION OK")


if __name__ == "__main__":
    main()
