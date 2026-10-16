MCP issues detected. Run /mcp list for status.
回归全绿。以下为第二轮交叉评审结论（全程只读，未执行任何 dws 写操作）。

## 第一轮修复核验表

| 条目 | 结论 | 证据 |
|---|---|---|
| P0 130003 结构化判定 | 修正确，有残留 | `_access_denied` 只查 4 个错误字段+stderr(ticket.py:67-73)，不再扫正文；但字段值/stderr 仍是子串匹配，见残留 P2-f |
| P1 单客户失败隔离 | collect 修好，publish 漏修 | collect per-future try/except(383-388)✅；`cmd_publish`(612-615）无隔离→残留 P1-a |
| P1 create 查重 | 正确 | `create_doc_idempotent`(509-523）先取 nodeId、失败按名 list_nodes 查重，幂等 ✅ |
| P1 空页漏读告警 | 修好一半 | read_messages 有 warnings(144-145)✅；probe_subgroup 丢弃 flaky 标志→残留 P2-c |
| P2 timezone/workers=0/timeout/bot 名 | 全部正确 | cfg_tz(57)、判空（375/611)、TimeoutExpired 入重试（83)、service_bot_name(345) |
| P2 小二确认语 | 部分 | 排除 xiaoer+TAM(244)✅，其他工程师/机器人仍误报→P2-b |
| P2 probe 去重/校验留 node/表格转义/最早建单卡 | 正确 | seen 去重（303)、node_id 输出（598)、esc_cell/esc_prose、`if not created_at`(195)，回归均有断言 |
| P2 summary 缺失告警 | 轻微 under-fix | 仅汇报行 note(579)，文档本体无降级水印 |
| 业务#2 跨天跟进 | **over-fix 引入新 bug** | `followup_section` 不过滤客户（526-547)，调用于 570→残留 P1-b；只回看 1 天→P2-d |
| 业务#3 sanitize 三重门禁 | 实现但有绕过面 | 枚举+存在+quote(265-297)✅；卡片 id 免 quote 校验、证据可整体缺省→P2-a |
| 业务#5 解散标签 | 部分 | label 分类（40-48)✅；render 二分支把「不可读」渲成「未入群（降级）」(468)→P2-e |

## 残留缺陷表

| 级 | 位置 | 触发条件 | 后果 | 修法 |
|---|---|---|---|---|
| P1-a | ticket.py:612-615 | 任一 publish_one 抛异常（summary JSON 损坏/create 三次失败/update 失败） | `fut.result()` 中断遍历，后续客户结果丢失、无汇报、退出码非零 | 与 collect 同款 per-future try/except，错误进汇报行 |
| P1-b | ticket.py:526-547 + 570 | 多客户配置下任一前日未完结工单当日完结 | **跨客户串档**：海底捞日报的「四、前日工单完结跟进」含合思/千里马行 | followup_section 传 customer key，只取本客户行 |
| P2-a | ticket.py:265-297 + 567 | ①引证用 create/done_msg_id（卡片 id 在 allowed 但不在 texts)②evidence 整体缺省 | ①卡片引证 quote 可编造过门禁②枚举内状态无证据裸奔，门禁形同虚设 | texts 并入 desc_card/sol_card/title；「已解决待关单」强制有效证据，缺失回退 |
| P2-b | ticket.py:244 | 非卡片小二（值班工程师、AI小钉/服务台自动消息）说「谢谢/没问题」<120 字 | 假客户确认→假「已解决待关单」 | 排除 engineer_summary_msgs 同 sender 与已知机器人名 |
| P2-c | ticket.py:306 | 子群翻页中段连续空页（trap#14 持续抖动） | `_flaky` 被丢弃，静默截断无告警 | 与 read_messages 同款 warnings 上抛 |
| P2-d | ticket.py:528 | 建单 D-3、当日完结 | 只回看 1 天→跟进漏报 | 以 E-ID 日期前缀为权威建单日，回看 N 天 collect 或标「历史工单当日完结」 |
| P2-e | ticket.py:468 | probe_error=「不可读」（非解散非未入群） | 误渲为「未入群（降级）」，误导催 TAM | 三分支渲染 |
| P2-f | ticket.py:71-73 | 错误字段/stderr 含「1300030」等长码 | 子串误伤→假 AccessDenied→假降级 | 错误字段精确匹配，stderr 加 `\b130003\b` |
| P2-g | ticket.py:76-88 + 300 | 主群权限类 130003 或被解散群 probe | collect 隔离兜底 ✅；但 probe 对嵌套 envelope(errorCode 在 data 内层）不判 AccessDenied→重试耗尽→整客户失败而非降级 | 递归扫一层嵌套错误字段（需 dws 报文样本确认） |

无新 P0。

## 性能建议（≤4，稳定性优先）

1. probe_subgroup 加下界 `ticket.created_at`：补跑老日期时从 now 翻到建单日即停；窗口后证据链在上方页已拿到，不受损——老工单补跑省页最多。
2. LIMIT 100→200（GLM#2 未落地，待验证 dws 支持）：主群+子群页数减半，无行为变更。
3. 零工单客户每日固定付 3 次空页重试+约 3s：首页即空且重试 1 次即可接受，省 2 次调用/客户/天。
4. 工单级 probe 并发仍不建议：dws 并发限流行为未验证，维持客户级并发。

## 业务改进（≤5，按价值）

1. **解析哨兵防静默漏报**：窗口内有消息但 0 卡片、且存在含「企业工单ID」却未命中正则的消息→warning。机器人改名/卡片改版从「静默 0 工单假阴性」变显式告警，这是当前最大漏报残余。
2. **催单建模落地路径**（开放项）：先把主群含「催单」关键词的非卡片消息原样落盘采样，攒够样本再写解析器，不臆造。
3. **跨天口径补强**：概览加「建单日」列（E-ID 前缀解析），跟进节按 P2-d 扩展回看；长工单不再永久「未完结」。
4. **关单滞后提醒**：「已解决待关单」超 24h 无完结卡→日报加滞后标记，驱动小二关单动作（用户核心痛点即官方状态失真）。
5. **总结缺失文档水印**：summary 缺失时文档内加「（总结缺失，规则渲染）」行，不只控制台 note。

## 口径冲突

1. **「已解散」标签可能永不触发**：子群被解散后，不在群成员的读取大概率仍报 `OpendId is not in conversation`→被 `AccessDenied.__init__`(40-48）标成「未入群」。reference 宣称「probe_error 标签区分未入群/已解散」名存实亡，补跑 >3 天仍会误催 TAM。裁决需一个**已解散子群的真实 130003 报文样本**；拿到前建议把「未入群」标签文案改为「未入群或已解散」。
2. **probe 边界=now 取舍本身成立，但否决理由不完整**：作者只算了「边界改窗口末会砍证据链」的账；存在第三条路——保留边界=now，同时在文档标注引证消息时间戳是否落在窗口外，证据链与口径自洽兼得，成本仅一个渲染字段。不需新证据，属方案空间遗漏，建议以「引证（窗口外）」标注落地。

核验结论：第一轮 15 项修复中 11 项正确、2 项引入新 bug(P1-a 为漏修、P1-b 为 over-fix)、2 项部分到位。无新 P0；P1-b 跨客户串档建议优先修。回归哨兵当前全绿，但 fixture 未覆盖多客户 followup 与 publish 异常路径，建议补这两条负控。
