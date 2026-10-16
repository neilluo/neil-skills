MCP issues detected. Run /mcp list for status.
评审完成。以下为第三轮专项结论（只读，未改任何文件、未执行 dws）。

# neil-ticket-skill 第三轮专项评审

## 1 重复度（~4.9%，红线内但临界）
自动统计：精确重复冗余行 35/713 ≈ **4.9%**（双份计 ~9%）。主要块：
- **分页循环** `read_messages` 156-176 vs `probe_subgroup` 337-353：seen 去重/flaky 告警/min_ct/boundary 停滞/推进五段近乎逐行复制，仅上限·limit·bound 变量·文案不同。→ 抽 `_paginate(fetch, boundary, *, max_pages, limit, stop_before)` 生成器，两处各留 ~10 行。
- `time.sleep(2 ** attempt)` ×5（101/112/116/120/146）：run_dws 四处错误尾巴重复 → 收敛为 `_fail()` 闭包。
- customers 过滤块 `cmd_collect` 426-429 == `cmd_publish` 682-685 逐字相同 → `_select_customers()`。
- parse_cards 230-233 与 247-250（subgroup_cid+order append）重复 → `_note()`。
- tests↔脚本：run-regression 反复手搭 slice（65-70/109-110/132-142/163-168）结构雷同且形状与生产不符（见 §2）→ 提供 `make_slice()` 工厂，去重兼防漂移。

## 2 死代码 / 死数据
- 🔴 **`subgroup_msg_times` 形状错配（半死功能）**：cmd_collect 写 **ticket 级** 447-448，render 520 从 **slice 级** `slice_.get("subgroup_msg_times")` 读。实测 outputs/collect-2026-10-13/14 slice 无此键（ticket 有）→ 生产 `ev_time` 恒 None，「（窗口外）」标注 521-522 **永不触发**；回归 slice6 163-168 用 slice 级伪造掩盖了它。
- **`chatrecord_url`**：解析存 212/246，render 溯源行 547 只输出 create/done_msg_id·subgroup_cid，从不渲染；SKILL.md:47/reference 却宣称「保留 chatRecord 链接」→ 死字段或文档失真。
- **`senderId`**：probe_subgroup 357 收集，compute_signals/sanitize/render 全不消费 → 死数据。
- `create_doc_idempotent` `require=lambda d: True` 575 恒真 → run_dws 118 永不触发，死参数（应传 None）。
- probe_subgroup 341 `len(page)<100 or not page` 的 `or not page` 被 `<100` 蕴含 → 死分支。
- parse_cards 251-253 status 兜底与 228-229 重叠 → 冗余分支。

## 3 命令风格不一致
- **重试三套**：run_dws 默认 3；data-auth 2（423）；create_doc_idempotent 1 + 外层 for3 且**无退避**（571-586）。fetch_page 又在 run_dws(3) 外套 for3（137-146）→ 单页最多 **9 次子进程 + 双层退避**。
- **退避不统一**：run_dws `2**attempt`；create 外层零 sleep 立即重试。
- **信封取值不一致**：messages/nodes/markdown 取顶层（143/480/491）；groups 取 `data["result"]`（369）；nodeId 三层兜底（578-579）；success 判 `is True`（425/664）。
- **require 形态混杂**：`in d` / `isinstance(...,dict)` / `isinstance(...,list)` / `is True` / `lambda d:True`。

## 4 架构分层
六层可辨，但边界渗漏：run_dws（传输）内嵌 130003 门禁 108+AccessDenied；probe_subgroup 采集里做投影 355-359（解析职责）；render 反依赖门禁 515+配置 555-556；followup_section 归渲染却做磁盘 IO 598-602；cmd_collect 命令层塞切片序列化 441-455；publish_one 一函数跨发布+门禁 641+渲染 643+IO 624-640。
三扩展各动层数：
- **加客户**：仅 config（配置层，零代码）— 良好。
- **加卡片事件类型（催单）**：解析 208-213/257 + 渲染 530-548 + 模板 + fixture/回归 + SKILL/reference ≈ **5-6 处**（ticket schema 硬编码、render 点名字段所致）。
- **加输出目标**：发布层被 alidocs 硬绑（create_doc_idempotent/list_nodes/doc_markdown 回读 666-671/cmd_publish），**无 OutputTarget 抽象** → 须重构发布层为接口+新实现+配置选择，改动最大。

## 5 内聚（改一功能需改多处）
- 改日报列：模板表头 8-9 + render 行 530-533（**表头在模板、数据行在代码，一表拆两文件**）+ 回归断言 → 内聚缺陷。
- 改 ticket 字段名：setdefault 208-213 + 投影 444-452 + render 543/546/547 + sanitize 305-306 + texts 634-640 ≈ 6 处（schema 无 dataclass）→ 缺陷。
- 改重试/退避：run_dws/fetch_page/create/probe/read_messages 五处各自为政 → 缺陷。
- 改日期口径：window_of 126 + collect_one 382 + render 505 + followup 自行 strptime 592 → 缺陷。
- 加客户仅改 config；effective_status 分散于枚举/信号/门禁/渲染 → **合理分层，非缺陷**。

## 6 冗长方法 top5
- `render` 502-566（65→~25）：抽 `_overview_row()`(~8)+`_ticket_section()`(~12)。
- `cmd_collect` 420-469（50→~28）：抽 `_build_slice()`(~12) 收拢 441-455 巨型推导。
- `parse_cards` 197-254（58→~35）：抽 `_note_subgroup()` 消 230-233/247-250。
- `publish_one` 617-675（59→~30）：抽 `_load_texts()`(~10)+`_verify()`(~8)。
- `read_messages`/`probe_subgroup`（各 ~25/30→各 ~10）：共用 `_paginate()`，兼解 §1 最大重复。

## 7 应沉淀进 AGENTS.md（现无）
可直接粘贴：
- dws 一律经 `run_dws` subprocess argv；禁 shell 重定向/变量/for。
- 读消息固定 `--direction older` 单页窗口自翻；禁 asc+start、禁 `--page-all`。
- 130003 只按结构化字段(errorCode/errorMsg/error/errMsg)+stderr，数字须边界防 1300030；禁全文子串。
- 每个 `run_dws` 必带有效 `require` 谓词；`lambda d:True` 视为缺失。
- 空 messages 页重试 3 次后才接受为空（trap#14）。
- 重试退避集中在 run_dws；业务函数禁自建第二层 for 重试或无退避重试。
- 模板 `{{token}}` 用逐 token `replace`，禁 `str.format`。
- effective_status 走「LLM 提议、脚本门禁」：枚举+messageId 存在性（按工单隔离，禁跨工单）+quote 子串；失败回退 default_effective 并留痕。
- publish 默认只写缺失/空文档，非空跳过；`--force` 才 overwrite。
- doc create 重试前先 list_nodes 查重。
- 单客户失败隔离：per-future try/except 进 collect["errors"]。
- 台账单一事实源 config/customers.json；加客户零代码；cid 不回填，仅报告提醒固化。
- 时区从配置读禁硬编码；日期统一走 window_of，禁各函数自行 strptime。
- **回归 fixture 的 slice 形状必须与 cmd_collect 实际产物一致**（禁 slice-level 伪造，见 §2）。
- 改正则/模板/字段 schema 后必跑 `python3 tests/run-regression.py`。

---
最高优先：§2 `subgroup_msg_times` 形状错配致「窗口外」标注生产环境失效，且被回归 fixture 掩盖。
