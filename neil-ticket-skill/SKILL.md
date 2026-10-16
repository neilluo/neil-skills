---
name: neil-ticket-skill
description: 重点客户工单每日巡检。把客户钉钉服务群里昨天的工单事件（建单/完结卡片）抽出来，顺卡片链接进工单专项子群读处理细节（未入群自动降级为完结卡片全文总结），渲染成日报写入该客户 alidocs 的「YYYYMMDD工单」文档（缺失自动建、写完回读校验）。当用户提到 工单巡检 / 每日工单 / 工单日报 / 重点客户工单 / 服务群巡检 / 跑工单 / 补跑某天生成的工单记录，或提到海底捞、合思、千里马的工单时使用。
---

# neil-ticket-skill

> 工程规范单一事实源：[AGENTS.md](AGENTS.md)（三轮多模型评审+机械度量沉淀，改代码/模板/配置/测试前必读）。

每天把重点客户服务群里的工单情况走一遍，产出 alidocs 日报文档。采集/发布全脚本化（`scripts/ticket.py`），总结步由每客户一个 subagent 按契约执行（只有「把子群聊天记录整理成要点」这一步需要 LLM，并发完成；契约见 AGENTS.md 规则 N 与 reference.md few-shot）。

## 配置驱动（加客户只改配置）

单一事实源：[config/customers.json](config/customers.json)。每个客户一条 entry：

| 字段 | 含义 |
|---|---|
| key / name | 客户标识 / 显示名（文档标题与日报抬头用 name） |
| service_group_name / service_group_cid | 服务群群名与 cid；cid 留空时脚本按群名原子搜索解析（不回填配置，报告里提醒固化） |
| daily_doc_parent_node | 「XX每日工单」节点 id（每日文档的父节点） |
| customer_folder_node | 客户文件夹节点 id（仅用于报告与校验） |
| subgroup_policy | 固定 `probe_then_fallback`：先探读子群，130003 则降级完结总结 |
| auto_join_expected | 该客户子群是否已配自动入群；仅用于报告标注「预期 vs 实测」不一致 |

加客户三步：在 alidocs「2025 > 客户」树下建客户文件夹与「XX每日工单」adoc 拿 nodeId → 在 customers 数组加一条 entry → 完成，代码零改动。群 cid 可先留空。

## 日期口径

D 日跑批记 **D-1（工单日）** 的工单，文档名 = 工单日（`YYYYMMDD工单`）。`--date` 一律传工单日。窗口 = 工单日 00:00–24:00（配置 timezone）。当日文档记录窗口内全部工单事件（建单/完结；**催单事件尚未建模，见 reference 开放项**）；前一日建单、当日窗口内完结的工单在当日文档加「四、前日工单完结跟进」节（跨天对账）。**零工单结转口径**：某客户当日窗口零新工单时，回看 ≤7 天历史 collect，取该客户最近一个有工单的日期 D0，结转 D0 中官方未完结（`completed_at` 为空）的工单，把「三、零工单说明」节替换为「三、零工单说明与昨日结转」（每块加「结转自：<D0> 日报」行，内容复用 D0 的 summary，缺失则回退 D0 collect 的 desc_card/sol_card；`effective_status` 复用 D0 summary 值并经 `sanitize_summary` 以 D0 slice 校验，失败回退规则值并留痕）；概览表不重复列结转工单（保持零行占位）；D0 全完结或无任何历史 → 维持纯零工单说明节；有新工单的日不受影响。

## 跑批流程

1. 采集（脚本，客户间并发，单客户失败隔离进 collect["errors"]）：
   `python3 scripts/ticket.py collect --date <工单日>`
   自动续期跨组织读授权（24h TTL）→ 每客户 desc/older 单页窗口拉主群消息（空页重试、翻页漏读告警）→ 正则抽卡片事件与子群 cid → 探读子群 → 产出 `outputs/collect-<date>.json` 与每客户 `outputs/transcripts-<date>-<key>.json`。
2. 总结（每客户一个 subagent，并发）：读自己的 transcripts 文件与 collect 切片，按工单写 `outputs/summary-<date>-<key>.json`，字段 `{ "<工单ID>": {"problem": str, "process_bullets": [str], "solution": str, "effective_status": str, "effective_evidence": {"message_id": str, "quote": str}} }`。契约：只允许整理原文，不允许补充事实；problem 取材＝完结卡【问题描述】逐字 > 建单卡标题+客户首条原话；solution 取材＝完结卡【解决方案】逐字 > 子群内技术工程师总结原文 > 字面量「截至生成时无完结总结」；子群不可读时 `process_bullets=["子群未入群，无过程细节"]`。**process_bullets 必须精简合成、禁止逐条摘录群聊原文**（用户 2026-10-16 指令）：每单目标 3–6 条主线要点（客户核心诉求 → 工程师关键判断/方案 → 最终结果），合并同话题的往返追问，去掉逐条时间戳流水账，不透出服务人员与客户人名（用「客户」「工程师」「值班小二」等角色词；人名已在概览表的建单人/当前小二中呈现）。只整理原文不补充事实的要求同样适用于 bullets——合成＝压缩与归类，不是编造。publish 的 `lint_process_bullets`（gate.py，AGENTS.md 规则 N）机械识别「疑似流水账」签名（条数 > MAX_BULLETS 或过半 bullet 以时间戳开头）并在发布行提示，只报不改。effective_status 取值＝已完结/已解决待关单/处理中/无法判定(无子群)，判定「实质已解决但官方未关单」看子群工程师总结块与客户确认语（脚本已抽好 signals 供参考，确认语已排除小二本人发言）；effective_evidence.message_id 必须是子群原文或卡片的真实 messageId，quote 必须是该消息原文子串，publish 用 sanitize_summary 机械校验（枚举+存在性+quote 子串），校验失败回退规则默认值并在文档留痕。few-shot 样例与溯源要求见 reference.md。
3. 发布（脚本，客户间并发，含回读校验）：
   `python3 scripts/ticket.py publish --date <工单日>`
   合并 collect+summary → 按 [templates/daily-report.md](templates/daily-report.md) 渲染 → 文档缺失自动建（`dws doc create --folder <daily_doc_parent_node>`）→ 已存在且空才写，**非空默认跳过并报告**（`--force` 才覆盖）→ 写完 `doc read` 回读校验关键行。
4. 汇报：每客户一行——工单数、子群探读成功/降级、文档链接或跳过原因、校验结果；auto_join_expected 与实测不一致时显式提醒。

## Anti-Patterns

- 在 shell 里手拼 dws 循环：重定向/变量/for 包裹 dws 全禁；一律走 ticket.py（subprocess argv 调用）。
- 假设子群可读：必须先 probe，130003 即降级；海底捞已生效、合思/千里马配置中（2026-10-14 实测）。补跑 >3 天时 130003 可能是「子群已解散」而非「未入群」，文档按 probe_error 标签区分。
- 用全文子串匹配判 130003：消息正文/文档正文可能含该数字串 → 只按结构化错误字段与 stderr 判定（trap#15）。
- asc 方向分页读消息（实测漏读）；脚本固定 desc/older。
- 覆盖非空文档：publish 默认跳过非空文档，防冲掉手工内容。
- 总结 subagent 编造事实：只能整理卡片/子群原文，溯源字段保留 messageId 与 chatRecord 链接。
- process_bullets 逐条摘录群聊原文：必须是精简合成的主线要点（3–6 条，合并往返、去逐条时间戳、不透人名）；违反时 `lint_process_bullets` 在发布行提示「疑似流水账」（只报不改，见跑批流程第 2 步）。

## 维护操作

| 动作 | 命令 |
|---|---|
| 每日跑批（工单日=昨天） | collect → subagents → publish |
| 补跑指定工单日 | 同上，`--date YYYY-MM-DD` |
| 只看采集不写文档 | `collect --date ...` 后检查 outputs/ |
| 回归哨兵 | `python3 tests/run-regression.py`（改正则/模板后必跑） |
| 完成判定（巡检补偿依据） | `python3 scripts/ticket.py check --date <工单日>`（exit 0=今日已完成，stdout `DONE finished_at=…`；exit 3=缺失/过期，stdout `MISSING reason=marker_absent\|stale:finished_at`；exit 1=其他异常。纯读判定，无网络/写；巡检任务据退出码机械补偿，不靠 prompt 推理） |
| 规范回写 | 每轮评审后更新 [AGENTS.md](AGENTS.md)（评审/度量发现的新规律同批回写，见 AGENTS.md 规则 M） |
| 每日 10:00 跑批 | qoder_cron job（name: `neil-ticket 每日跑批 10:00`，cron `0 10 * * *` Asia/Shanghai），触发本流程（工单日=昨天），结果发「问问」 |
| 巡检补偿（10:30 / 11:30 / 12:30） | qoder_cron job（name: `neil-ticket 巡检补偿 10:30/11:30/12:30`，cron `30 10-12 * * *` Asia/Shanghai，即 10:30、11:30、12:30 三次），完成判据＝当日 `outputs/run-<工单日>.json`（publish 收尾落盘，`finished_at`＝本次 publish 完成时刻），机械判定走上表「完成判定」check 子命令，exit 3 则补偿跑批。**双层止跑**：① 调度层——12:30 后当日不再触发；② 会话层——check exit 0 秒退（不发消息），publish 另有机械幂等门（当日标记存在且无 `--force` 即 no-op），双重防重复跑。顺利日实测目标＝10:00 跑批 1 会话 + 0 个补偿会话 |

互斥约定：跑批会话用 `outputs/.lock`（mtime<2h 视为进行中）+ `pgrep -f "ticket.py collect"` 双重检测，禁止两个跑批并发。

细节与实测陷阱见 [reference.md](reference.md)。
