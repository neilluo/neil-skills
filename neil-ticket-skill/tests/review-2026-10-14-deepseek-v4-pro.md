MCP issues detected. Run /mcp list for status.
七项核查完成，全部结论附 file:line 如下。

# 第三轮专项评审（neil-ticket-skill）

## 1 重复度 ≈3.8%（27/713 行），达标
- 精确重复：parse_cards 的 subgroup_cid/order 注册块两现（ticket.py:230-233 vs 247-250，4 行）；`bot=` 表达式两现（386-387）。
- 骨架重复：翻页边界推进 read_messages:165-171 vs probe_subgroup:345-351（4 行）；cursor 翻页 resolve_cid_by_name:363-377 vs list_nodes:473-486（8 行）；esc_cell/esc_prose:494-499（2 行）；publish_one 两次 exists+load:623-640（3 行）；run_dws 错误构造+退避三现:111-120（6 行）。
- 与 tests：slice_ 形状在 run-regression.py:40-43、65-70 手抄（约 10 行，属测试契约，可接受）。
- 合并方案：抽 `_register(ticket,cids)`、`paginate()` 骨架、`_load_json_optional()`、`_abort()`。

## 2 死代码（函数级 AST 全查无死函数）
1. config 四字段零读取：doc_title_pattern（customers.json:5）、customer_folder_node（:13,24,35）、subgroup_policy（:14,25,36）、auto_join_expected（:15,26,37）；SKILL.md:38 承诺的 auto_join 提醒未实现（cmd_collect:464-467 无比对）。
2. `require=lambda d: True` 恒真谓词：create_doc_idempotent:575（run_dws 已拦 parsed None）。
3. 双重 300 封顶：probe_subgroup:352 已 break，:359 `[:300]` 冗余。
4. tests/run-regression.py:115 `import os as _os` 冗余（模块级 os:4 已用于 :7）。

## 3 dws 调用风格不一致
- require 谓词两类混用：形状校验（:141,:367,:479,:490）vs 业务标志（:425,:664 success is True）vs 恒真（:575）。
- retries 无说明地漂移：默认 3，auth=2（:424），create=1（:574）。
- 输出取值双重标准：create 三重信封回退 nodeId/data.nodeId/result.nodeId（:578-579），其余单形状。
- 初始 cursor 不一：resolve "0"（:363）vs list_nodes ""（:474）。
- 字面重复：`' '.join(args[:4])` 三现（:111,115,119）、`2**attempt` 五现（:101,112,116,120,146）。
- 一致面（良好）：argv 全 list、无 shell、AccessDenied 统一 raise、130003 判定集中（:85-89）。

## 4 六层边界：三处越界
- 配置层被散读 5 次：render:555、publish_one:647、create_doc_idempotent:582、cmd_*:421,679 —— 应入口读一次下传。
- 采集层内嵌解析哨兵：collect_one:388-396。
- 渲染层跨层读盘：followup_section:596-602 直读 collect-*.json；门禁消费采集产物形状（sanitize:294-327）。
- 扩展影响：加客户=仅 config（已验证零代码）；新卡片类型=解析+采集哨兵+渲染+模板+门禁枚举+测试+双文档（5-6 层）；新输出目标=发布层五函数+配置，但 publish_one:666-672 回读校验与 alidocs 强耦合需先拆。

## 5 内聚缺陷清单（改一功能动多文件）
- 加列/改版式：template 表头（templates/daily-report.md:8）↔ render 行格式（ticket.py:530-533）隐式耦合——缺陷。
- 改 effective_status 枚举：EFFECTIVE_ENUM:33、default_effective:279、SKILL.md:34、reference.md:64、tests——四处代码外拷贝，应下沉常量/config——缺陷。
- slice_ 形状无 schema：cmd_collect:441-455 生产，sanitize/render/publish_one 消费，tests 手抄——单文件内可接受，建议加 dataclass。
- 换输出目标：单文件内集中——合理。
- 加客户：仅 config——优秀。

## 6 冗长 top5（现→目标行）
1. parse_cards 57→42：抽 `_register` 消 4 行块。
2. publish_one 58→44：`_load_json_optional` 吸收 623-640。
3. cmd_collect 49→38：441-455 五连推导改单循环。
4. run_dws 31→22：`_abort(msg)` 助手。
5. render 64→50：抽 `_row/_section`；配合共享 `paginate()`。

## 7 应沉淀进 AGENTS.md 的规则
1. dws 一律经 run_dws argv 调用，禁 shell 拼接；require 只做形状校验，success/业务标志放调用侧。
2. 新增 config 字段必须先有读取方；任何字段不得只写文档不接线（现状反例：auto_join_expected）。
3. effective_status 枚举改动必须同步 EFFECTIVE_ENUM、default_effective、SKILL.md、reference.md 四处。
4. 新增卡片事件类型必须同步 parse_cards、collect_one 哨兵、模板、fixtures、回归五处。
5. 翻页必须复用 paginate 骨架（空页重试+boundary 不前进告警）；新增翻页代码禁止再抄。
6. 渲染/门禁层禁止直接 load_config 或读 outputs 盘；配置入口读一次下传。
7. 任何正则/模板改动必须跑 tests/run-regression.py。
