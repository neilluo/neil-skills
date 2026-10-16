# AGENTS.md — neil-ticket-skill 工程规范（单一事实源）

沉淀自多轮多模型评审与机械度量：第一轮 GLM-5.3（tests/review-2026-10-14-glm53.md）；第二轮 Ultimate + Kimi-K3（tests/review-2026-10-14-ultimate-a.md / ultimate-b.md / kimi-k3.md）；第三轮 DeepSeek-V4-Pro + Qwen3.8-Max 七项专项（tests/review-2026-10-14-deepseek-v4-pro.md / qwen38-max.md，提示词 tests/review-prompt-v3.md）；第四轮 MiniMax-M3（tests/review-2026-10-15-minimax-m3.md，包结构落地）；第五轮两个不同 focus 的 review subagent 交叉评审（2026-10-17，关注等级功能，修复记录见 reference.md「开放项与取舍记录·第五轮」）；机械度量 scripts/analyze-metrics.py。改 scripts/neil_ticket/（含兼容 shim scripts/ticket.py）、templates/、config/、tests/ 前必须通读本文件；本文件与 SKILL.md/reference.md 冲突时以本文件为准。

## A. dws 调用一律经 run_dws
- 所有 dws 调用必须走 scripts/neil_ticket/transport.py 的 `run_dws`（subprocess argv 列表形式，全包唯一 dws 出口）。禁止在 shell 里拼 dws 命令：重定向（`>`）、shell 变量、`for`/`while` 循环、管道包裹一律禁止。
- `require` 谓词只做信封形状校验（如 `"messages" in d`、`isinstance(d.get("nodes"), list)`）；业务判定（如 `success is True`）放在调用方，不进 require。`lambda d: True` 恒真谓词视同缺失 require，禁止。
- require 谓词合规化已于 2026-10-15 落地（第四轮拆包同批）：collect.py/publish.py 三处——cmd_collect 的 data-auth（collect.py:154-158）、create_doc_idempotent 的 doc create（publish.py:75-83）、_update_doc 的 doc update（publish.py:162-167），require 只留形状校验，success/nodeId 判定全部移到调用方。
- 来源：第三轮 DeepSeek-V4-Pro §3（require 谓词形状/业务标志/恒真三类混用）、Qwen3.8-Max §7；SKILL.md Anti-Patterns（第一轮起实测约束）。

## B. 重试与退避集中在 run_dws 与常量表
- 重试与指数退避（`2**attempt`）只允许存在于 `run_dws` 内部，次数由常量表统一声明：`RETRY_TRANSPORT=3`（传输/空回默认）、`RETRY_EMPTY_PAGE=2`（空页）、`RETRY_AUTH=2`（data-auth 跨组织授权）、`RETRY_CREATE=1`（doc create，配合规则 I 外层查重）。
- 业务函数禁止自建第二层无退避重试循环。空页重试（fetch_page，trap#14）是 run_dws 之外唯一允许的第二层循环，且必须有上限与退避。doc create 外层循环属幂等查重流程（规则 I），每轮先查重再决定，不算盲重试。
- 来源：第三轮 Qwen3.8-Max §3（重试三套并存；fetch_page 外层×run_dws 内层＝单页最多 9 次子进程＋双层退避；create 外层零 sleep）、DeepSeek-V4-Pro §3（retries 3/2/1 无说明漂移）、§7-5。

## C. 130003 只按结构化判定
- 130003（OpendId not in conversation，降级信号）只按两处判定：① JSON 结构化错误字段（`errorCode`/`errorMsg`/`error`/`errMsg`，含 `data`/`result` 一层嵌套信封）；② stderr 文本。两处均用数字边界正则 `(?<!\d)130003(?!\d)`，防 1300030 等长码误伤。
- 禁止对消息正文、文档正文或 stdout 全文做子串扫描判 130003。
- 来源：第一轮 GLM-5.3 P0（全文子串造成整批崩溃/假降级，trap#15）；第二轮 Kimi-K3 P2-f（数字边界）、P2-g（一层嵌套信封）、Ultimate-a P2（嵌套漏判与 stderr 误伤）。

## D. 消息分页固定 desc/older 单页自翻
- 读群消息一律 `--direction older` 单页窗口自翻（LIMIT=100、MAX_PAGES=60）。禁止 asc 方向（实测漏读，trap#4）；禁止 `+chat-messages --page-all`（此类群 pagination_error、hasMore 不可靠，trap#2/#5）。
- 翻页 boundary 不前进（min_ct == boundary）与 MAX_PAGES 耗尽必须写 warnings 上抛告警；翻页中段空页重试耗尽必须告警「窗口老侧可能漏读」。禁止静默截断。
- 来源：reference trap#2/#4/#5（2026-10-14 实测）；第一轮 GLM-5.3 P1（空页静默漏读）；第二轮 Ultimate-a P2（边界等值/同时间戳满页、页数耗尽反而无告警）、Kimi-K3 P2-c（probe flaky 标志被丢弃）。

## E. sanitize 三重门禁不可绕
- effective_status 走「LLM 提议、脚本门禁」：`sanitize_summary` 必须校验 ① 取值 ∈ EFFECTIVE_ENUM；② `effective_evidence.message_id` 存在于本工单 allowed 集合（建单/完结卡 id + 本工单 subgroup_msg_ids），allowed 按工单隔离，禁跨工单引用；③ `quote` 是所指消息原文归一化后的子串。任一失败 → 回退 `default_effective` 并写 `effective_status_invalid_evidence` 留痕。
- 「已解决待关单」必须有本工单有效引证（message_id+quote）；禁止证据整体缺省或空 quote 绕过。除「无法判定(无子群)」外的状态不得无引证裸奔。
- 来源：第一轮 GLM-5.3 业务#3；第二轮 Ultimate-a P1（allowed 跨工单共享即可伪造）、Kimi-K3 P2-a（卡片 id 免 quote 校验、evidence 缺省绕过）。

## F. 回归 fixture 禁 slice 级伪造
- tests/run-regression.py 手搭的 slice 形状必须与 `cmd_collect` 实际产物逐键同形：键名与层级（哪些键在 ticket 级、哪些在 slice 级）以 cmd_collect 落盘的 collect JSON 为准。禁止按消费方读法伪造 slice 形状。
- 来源：第三轮 Qwen3.8-Max §2——cmd_collect 把 `subgroup_msg_times` 写在 ticket 级（ticket.py:447-448），render 却从 slice 级读（ticket.py:520），生产环境「（窗口外）」标注永不触发；回归 slice6（run-regression.py:163-168）用 slice 级伪造掩盖了该 bug。

## G. 模板占位符与转义
- 模板占位符一律双花括号 `{{token}}`，渲染用逐 token `str.replace`；禁用 `str.format`（format 会把 `{{` 渲染成字面 `{`，trap#12）。
- 一切写入 Markdown 的文本先转义：表格单元走 `esc_cell`（转义 `|`、压缩换行），正文走 `esc_prose`。禁止未转义拼接。
- 来源：reference trap#12（实测）；第一轮 GLM-5.3 P2（标题/描述含 `|` 或换行破坏表格版面）。

## H. 单客户失败隔离
- collect 与 publish 都必须 per-future try/except：单客户异常（含 transcripts 落盘、slice 组装、create/update、回读校验失败）写入 `collect["errors"]` 或汇报行后继续处理其余客户。禁止任一 future 异常中断全批遍历或报废已完成客户的产物。
- 来源：第一轮 GLM-5.3 P1（collect 全批报废）；第二轮 Ultimate-a P1（publish 完全未隔离；落盘/组装不在隔离范围）、Kimi-K3 P1-a。

## I. doc create 重试前先查重
- `create_doc_idempotent`：create 抛异常或未拿到 nodeId 时，必须先 `list_nodes` 按文档名查重，命中即复用 nodeId；查重未命中才允许再次 create，上限 3 轮。禁止盲重试非幂等 create。
- 来源：第一轮 GLM-5.3 P1（盲重试最多建 3 个同名重复文档）；第二轮 Ultimate-a P1（服务端已建但 CLI 非零 rc 时直接抛错，重跑重复建文档）。

## J. config 键必须被消费
- config/customers.json 每个键必须有代码消费方；无消费方的键删除或同批接线。新增配置键必须同批落地消费代码与回归断言，禁止只写文档承诺不实现。
- 来源：第三轮 DeepSeek-V4-Pro §2（doc_title_pattern/customer_folder_node/subgroup_policy/auto_join_expected 四字段零读取；SKILL.md 承诺的 auto_join_expected「预期 vs 实测」提醒未实现）、§7-2。消费现状表见 reference.md「配置键消费表」。

## K. 函数长度上限 40 行
- 单函数不超过 40 行（含 def 行）。超线必须抽 `_helper`（既有方向：`_paginate`/`_build_slice`/`_overview_row`/`_ticket_section`/`_load_json_optional`）。
- 40 行上限口径为全包扫描：2026-10-15 起 scripts/analyze-metrics.py 已改为扫描 scripts/neil_ticket 全包九模块（func_lengths_pkg，「>40 行函数」红线覆盖包内全部 FunctionDef；shim ticket.py 仅纳入重复率/死代码对照，不参与函数长度统计）。
- 裁决记录（第四轮）：MiniMax-M3 建议内联 render 层 `_evidence_text`（仅单点调用），裁决拒绝——内联后 render 超 40 行红线（render 现 35 行 + `_evidence_text` 正文 7 行），保留 helper 符合规则 K。来源：tests/review-2026-10-15-minimax-m3.md P1-1。
- 来源：第三轮 DeepSeek-V4-Pro §6、Qwen3.8-Max §6（render 65 / publish_one 59 / parse_cards 58 / cmd_collect 50 行超线，附重构目标行数）；机械度量 scripts/analyze-metrics.py 的 func_lengths（「>40 行函数」即红线统计口径）。

## L. 变更影响面契约（同批清单）
- 加客户：仅改 config/customers.json（建节点 → 加 entry），代码零改动。
- 加卡片事件类型（如催单）：parse_cards 分支 + templates/daily-report.md + tests/fixtures 与回归断言 + reference.md「工单事件报文解剖」节，四处同批落地。
- 改日报列：templates/daily-report.md 表头 + render 行格式，两处同批（表头在模板、数据行在代码，一表拆两文件，改一处必改另一处）+ 回归断言。
- 改门禁/枚举：只改 scripts/neil_ticket/gate.py 常量（EFFECTIVE_ENUM 等）；reference.md 引用代码常量名，文档不复制枚举值。
- 改零工单口径（含昨日结转）＝ render/publish 结转逻辑（render.carryover_section + render() 的 carryover 参数替换零工单节 + publish._carryover_data 装配）+ SKILL.md 日期口径节 + reference.md「开放项与取舍记录」结转条目，同批落地 + 回归断言（正控/失败分支/负控）。
- 改关注等级硬信号词表/阈值＝parse.py 常量（`SAFETY_KEYWORDS`/`PRODUCTION_KEYWORDS`，及 compute_attention 内的档位阈值如「存活≥2 天」「>24h 无活动」）+ reference.md「硬信号风险词表」/「关注等级判定」节 + tests/run-regression.py 回归断言，三处同批落地。词表放代码常量便于审计，reference.md 复制其实际值（与门禁枚举「文档只引用常量名不复制值」相反，词表属可审计业务口径须逐字列出），改一处必改其余两处。
- 来源：第三轮 DeepSeek-V4-Pro §4/§5（加客户已验证零代码；模板表头↔render 行隐式耦合；effective_status 枚举存在四处代码外拷贝应下沉）、Qwen3.8-Max §4/§5；第二轮 Ultimate-b（催单能力虚标教训：契约未落地不得写入宣称）；零工单结转（用户 2026-10-15 指令「如果没有工单的话，可以复用一下昨天的」）；关注等级词表同批（用户 2026-10-16 指令，见规则 R）。

## M. 评审发现必须回写规范
- 每轮评审（多模型评审或 analyze-metrics.py 度量）发现的新规律、新陷阱、新契约，必须同批回写本 AGENTS.md 与 reference.md，禁止留「只在评审报告里」的知识；回写条目须标注来源报告。
- 来源：第三轮 review-prompt-v3 §7（规范沉淀专项，本 skill 此前无 AGENTS.md）；用户 2026-10-14 决策。

## N. 总结子代理契约
- 每客户一个总结 subagent 并发执行：只允许整理卡片/子群原文，禁止补充事实；effective_evidence 必须引真实 messageId + 原文子串 quote；publish 由 sanitize_summary 脚本门禁兜底（规则 E）。契约全文与 few-shot 样例以 reference.md 为唯一出处。
- **process_bullets 必须精简合成、禁止逐条摘录群聊原文**（用户 2026-10-16 指令「几乎没有总结、原封不动把群里的聊天内容直接摘录下来这种是不对的」）：每单目标 3–6 条主线要点（客户核心诉求 → 工程师关键判断/方案 → 最终结果），合并同话题往返追问，去掉逐条时间戳流水账，不透服务人员与客户人名（用「客户」「工程师」「值班小二」等角色词——人名已在概览表的建单人/当前小二列呈现）。合成＝压缩与归类，不是编造：「只整理原文、不补充事实」同样约束 bullets。
- **机械观察哨（只报不改，对齐规则 E「LLM 提议、脚本门禁」与用户「长度约束只报观察、拒截断式 normalize」）**：gate.py `lint_process_bullets` 识别「疑似流水账」签名——bullet 数 > `MAX_BULLETS`(8)，或以时间戳（`HH:MM` / `YYYY-MM-DD HH:MM`）开头的 bullet 占比 ≥50%（≥3 条时）；publish._bullets_note 逐工单跑 lint，命中则在发布行追加「总结疑似流水账[tid:签名]」，随 run-<date>.json results 投递到「问问」供人工/巡检复核。**只报不改**：绝不截断/重写 bullets（截断会伤事实、重写需 LLM），质量好坏由总结 subagent 依本契约负责，lint 仅暴露违规信号。合成质量本身无机械判据（无法用正则区分「好总结」与「坏总结」），故 lint 只抓最强的流水账签名，其余靠契约 + few-shot + 发布行人工复核兜底。
- 人名脱敏为何停在契约层不做机械：`lint_process_bullets` 无法可靠机器识别所有客户/工程师人名（如某工单 creator 为空、人名散落在长句中），机械脱敏会漏判或误伤正文，故只写进契约由 subagent 遵守，不谎称有机械保证（对齐用户「契约未落地不得写入宣称」）。
- 来源：SKILL.md 跑批流程第 2 步；第一轮 GLM-5.3（子代理编造事实风险）；第二轮 Ultimate-b（few-shot 曾缺 effective_status/effective_evidence 字段，已补）；用户 2026-10-16（process_bullets 逐条摘录群聊、透人名）。

## O. 评审工具链坑
- 用 qodercli 跑评审子代理（如 Ultimate）：评审材料必须用 `--attachment` 注入，并在提示词中禁止工具调用——`-p` 模式不执行工具调用，让模型「自己读文件」会静默早退，产出空报告。
- 调用前缀必带 `env -u QODER_AGENT_SDK_ENTRYPOINT`，避免 SDK 入口环境变量干扰子进程。
- 来源：第二轮评审执行实测——首次 Ultimate 评审静默早退，tests/review-2026-10-14-ultimate.md 仅一行空输出；改 `--attachment` 注入后重跑才得到 ultimate-a/b 两份完整报告。

## P. 物理分层与依赖方向
- scripts/neil_ticket/ 九模块职责一句话清单：config＝路径常量/台账读取/时区/时间窗/--customers 过滤/doc_title 配置消费（依赖链最底层，不 import 包内其他层）；transport＝run_dws 唯一 dws 出口 + RETRY_* 重试预算表 + 130003 结构化判定 + _paginate 通用翻页；parse＝卡片正则与工单结构化 + compute_signals 确定性信号抽取 + compute_urgency_signals/compute_attention 关注等级确定性信号与三档合成（纯函数，无 I/O）；gate＝EFFECTIVE_ENUM/SENTIMENT_ENUM 与 sanitize_summary/sanitize_sentiment 三重门禁 + _evidence_bad 共用引证校验（纯函数）；render＝模板渲染与转义纯函数 + verification_markers 回读校验标记 + 关注等级注入（_attention_map/_attention_section 经 compute_attention）；collect＝主群窗口读取/子群探读/slice 组装/collect 子命令编排；publish＝幂等建文档/覆盖更新/回读校验/跨天跟进节/结转 re-age（_reage_urgency）/publish 子命令编排；cli＝argparse 装配，唯一对外执行入口，不写业务逻辑；__init__＝公共名重导出与 __all__（包公共 API 单一出处）。
- 依赖方向：config←transport←parse←gate←render←collect/publish←cli，只准向左（下层）依赖，禁止循环依赖；scripts/ticket.py 仅为兼容 shim（星号重导出 + monkeypatch 写入转发），禁止新增业务逻辑。当前实际包内 import：render→{config,gate,parse}（parse 的 compute_attention 供关注等级合成，向左合规）；collect→{config,parse,transport}；publish→{config,gate,parse,render,transport}（parse 的 _days_span/_is_stalled/词表供结转 re-age，向左合规）；cli→{collect,publish}；config/transport/parse/gate 包内零依赖。
- 扩展契约：加客户＝仅改 config/customers.json，代码零改动；加卡片事件类型＝parse 分支 + templates/daily-report.md + tests/fixtures 回归断言 + reference.md「工单事件报文解剖」节，四处同批（与规则 L 一致）；加输出目标＝仅 publish 层新增 target 函数 + cli 接线，其余层不动；换传输通道（dws 替代）＝仅改 transport 层。
- 来源：用户 2026-10-15 批评「单文件谈不上扩展」（第四轮包结构落地触发点）；第三轮 Qwen3.8-Max §4（六层可辨但边界渗漏：run_dws 内嵌 130003 门禁、probe_subgroup 采集里做解析投影、render 反依赖门禁与配置、followup_section 归渲染却做磁盘 IO、publish_one 一函数跨发布/门禁/渲染/IO）、DeepSeek-V4-Pro（新输出目标与 alidocs 强耦合需先拆）。落地态与度量复测（跨模块重复 0.00%、死代码 0、函数 ≤40 行）见 reference.md「开放项与取舍记录·第四轮」。

## Q. 情绪判定门禁（与规则 E 同构）
- 客户负面情绪走「LLM 提议、脚本门禁」，与规则 E 的 effective_status 完全同构：总结 subagent 提议 `sentiment`，publish 用 gate.py `sanitize_sentiment` 机械校验兜底。三重校验（共用核心抽为 gate.py `_evidence_bad`，sanitize_summary/sanitize_sentiment 共享，避免两套引证校验漂移）：① `sentiment.level ∈ SENTIMENT_ENUM`（枚举单一事实源＝gate.py `SENTIMENT_ENUM`，本文档与 reference.md 均只引用常量名不复制值，规则 L）；② `SENTIMENT_NEEDS_EVIDENCE`（gate.py 常量，即「轻微/明显」两档）必须有 `sentiment.evidence.message_id` 落在本工单 allowed 集合（`_allowed_ids`，与 sanitize_summary 共用，按工单隔离禁跨工单引用）且 `quote` 非空；③ `evidence.quote` 是所指消息原文归一化子串。任一失败 → level 回退「无法判定」并写 `sentiment_invalid_evidence` 留痕（不可静默）。evidence 非 dict（LLM 结构异常）→ 需引证档判失败、宽容档放行，`_evidence_bad` 不崩溃于畸形结构（第五轮评审 P1：原实现 `ev.get` 会 AttributeError）。空 quote + 真实 message_id 曾可绕过子串校验（第五轮 P1），现由 `_evidence_bad` 的 `<空quote>` 分支拦截。
- **绝不把「没评估」臆断成「没情绪」**：summary 整体缺 `sentiment` 字段（旧总结/流水线未产出）→ level 置「无法判定」+ `sentiment_missing` 标记，由 publish `_watermark` 出文档级水印「本篇未产出情绪判定（sentiment 缺失），关注等级仅按确定性信号合成，负面情绪可能漏标」，而非逐单渲染成「无」。render `_sentiment_line` 对 `sentiment_missing` 返回空串（避免逐单噪声），仅对 LLM 显式判定的「轻微/明显/无法判定」渲染引证行。
- **情绪与人名脱敏为何都停在「LLM 提议+脚本门禁」而非纯正则**：纯正则无法可靠区分语义——实测会误伤友好用语（如「好的谢谢[捂脸哭]」的 `[捂脸哭]` 是客气表情不是负面），也会漏掉无负面词的质疑（如「应该不是这个原因」「这个是线上任务，不能随意重启」——无脏词但表达不认同/受阻）。故情绪由 subagent 依契约判、脚本只校验引证真实性（防编造），语义判断本身不做机械保证，与人名脱敏停在契约层（规则 N）同一取舍逻辑。
- 来源：用户 2026-10-16 指令（负面情绪要标红、走 LLM+门禁）；研究 subagent 2026-10-16 于三天真实 transcripts 实测纯正则误伤/漏判（E2610143Y5HYZP「好的，谢谢[捂脸哭]」误伤、E2610134H5HYPU「应该不是这个原因」漏判）；设计取舍记录见 reference.md「开放项与取舍记录」。

## R. 关注等级合成契约（🔴重点/🟡留意/⚪常规）
- 三档由 parse.py `compute_attention(ticket, urgency, sentiment_level)` 纯函数合成，返回 `(emoji, level_name, [触发原因])`。两类输入分工明确：**确定性信号由脚本算**（`compute_urgency_signals`，无 I/O 纯函数，collect 阶段写入 `slice.signals[tid].urgency`），**情绪由 LLM 提议**（`sentiment.level`，经规则 Q 门禁校验后传入）。合成规则（任一命中即升该档，红优先于黄）：
  - 🔴重点：催单事件 `urge_reason` 非空 ｜ 安全类标题命中 `safety_hit` ｜ 未完结且「明显」负面 ｜「明显」负面情绪。
  - 🟡留意：跨天未完结（`days_span≥2` 且未完结）｜ 跨天已完结（`days_span≥2` 且 `completed`，关注服务时效；用户规则 a 只把当天完结算常规）｜「轻微」负面 ｜ 生产故障标题命中 `production_hit` ｜ 疑似僵单 `stalled`。
  - ⚪常规：其余（当天完结普通问答／建单无应答但子群不可读）。
- **硬信号词表放代码常量**：`SAFETY_KEYWORDS`（安全类标题，命中升🔴）与 `PRODUCTION_KEYWORDS`（生产故障类标题，命中升🟡）定义在 parse.py 顶部常量，便于统一审计；改词表/阈值按规则 L 三处同批（parse.py 常量 + reference.md 词表/判定节 + 回归断言）。催单信号由 `_detect_urge` 探测：真实催单事件是**子群里「阿里云服务台」发的独立机器人消息**（正文含「催单信息：<font >业务阻塞</font>」），**不在建单/完结卡里**——建单卡 Tips 的「催单」只是每张卡都有的按钮跳转链接（`RE_URGE` 只匹配「催单信息：」前缀，天然排除按钮，命中按钮会造成全量假升级）。故 `_detect_urge` 按序扫「子群消息文本 → 建单卡 → 完结卡」。⚠️修复记录（2026-10-16）：初版 `compute_urgency_signals` 只扫建单/完结卡文本，催单在生产永不触发；改为经 `_detect_urge` 同扫子群消息，回归补真实子群路径正控 + 建单卡按钮负控。实测样本见 reference.md「硬信号风险词表」节。
- **僵单判定只对可读子群生效**：`_is_stalled` 仅当子群可读（`readable`）且未完结且最近活动距今 >24h（或存活≥2 天但无任何子群消息活动）才判疑似僵单；子群不可读的降级单一律不判僵单——用户 2026-10-16 明确「合思那种未自动入群的降级单先不看，别把配置问题当业务问题预警」，避免把入群配置缺失误报成业务停滞。
- **存活天数以工单日锚点保补跑可复现**：`_ticket_open_date` 优先用 tid 前缀 `E26MMDD` 解码建单日（比 `created_at` 可靠——完结日 collect 的 `created_at` 为空），失败回退 `created_at` 日期部分；`_days_span` = 完结日或 today − 建单日。collect `_merged_signals` 传入的 `today`（work_day）取 `transcripts["date"]`（工单日）而非跑批当日，使补跑老日期时存活天数按工单日锚定、结果可复现。
- 分层：确定性信号抽取在 parse（纯函数），情绪门禁在 gate（规则 Q），合成 `_attention_map` 与「零、重点关注」节渲染在 render（`_attention_section` 只列🔴🟡、红前黄后），信号合并入 slice 在 collect（`_merged_signals`），水印在 publish（`_watermark`）——符合规则 P 依赖方向。
- 来源：用户 2026-10-16 指令（工单连续性要重点关注跨天单、负面情绪要标红、催单/安全/生产硬信号升级、子群不可读的降级单不做僵单判定）；实测催单卡样式「催单信息：<font >业务阻塞</font>」见 outputs/transcripts-2026-10-13-haidilao.json 工单 E2610134H5HZYU（`RE_URGE` 抽取「业务阻塞」验证通过）。三档判定表与词表实际值见 reference.md「关注等级判定」「硬信号风险词表」「工单连续性」节。
