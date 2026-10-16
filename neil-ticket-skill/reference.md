# reference — neil-ticket-skill 实测档案

台账单一事实源是 [config/customers.json](config/customers.json)；本文件只记机制、报文解剖与陷阱，不重复台账数据。

## 工单事件报文解剖（2026-10-14 实测）

触发链：客户在主群 `@阿里云服务台 <关键词>` → 机器人「阿里云服务台」秒回卡片。卡片是**纯 text/markdown 消息，非结构化 card**，字段全部正则可提。

建单卡片骨架：

```
@<建单人> 已为您创建新企业工单
企业工单标题：<font color=#096DD9><标题></font>
企业工单ID：E<yymmdd><随机>
企业工单状态：处理中
当前小二：<姓名>
请[点击此处](dingtalk://...url=...joinSubgroup%3FtaskId%3D<taskId>%26departmentId%3D<deptId>%26openconversitionid%3D<主群cid编码>) 进入企业工单专项群。
Tips：...点击[催单](dingtalk://...urge%3Ftid%3D<taskId>...%26openconversitionid%3D<★子群cid编码★>)...
```

- **子群 cid 藏在「催单」链接的 openconversitionid 里**（URL-decode 两次）；joinSubgroup 链接里的 openconversitionid 是主群 cid，别拿错。
- taskId 是子群唯一键；工单 ID `E<yymmdd>...` 自带日期，可按天过滤。
- 完结卡片：`企业工单已完结` + 【问题描述】【解决方案】全文 + chatRecord 链接（亦含子群 cid）。这是未入群客户的降级信息源。
- 子群群名不出现在卡片里；子群 3 天不续自动解散 → 补跑老日期时子群可能已不存在，降级路径天然兜底。
- 群内其他发言方：客户真人、AI小钉（入群欢迎）、云通知（故障公告）——均非工单事件，采集时过滤。

## 实测陷阱清单

1. `+chat-search` 搜不到客户服务群；可靠通道是原子 `dws chat search --query "<群名片段>"` 与 `dws aisearch enterprise --queries "<群名>" --types im`（后者 meta 直接给 cid+chat_type）。
2. `+conversation-list --page-all` 只回 100 条且谎报 complete=true。
3. 跨组织读消息需 `dws chat data-auth cross-org --all --grant-type timed --ttl 24h --yes`，24h 过期 → 脚本每轮幂等续期。
4. asc + start 窗口读消息会漏读（返回 0 但 desc 有消息）→ 固定 desc/older 方向单页窗口翻页。
5. `+chat-messages --page-all` 在此类群 pagination_error（hasMore 不可靠）→ 单页窗口自翻。
6. `doc info` / `wiki node list` 偶发只回 `{"success":true}` 无数据 → 重试 3 次退避。
7. dws **无进群/接受邀请能力**；`chat group members add` 需群管理权限，对非成员子群预期被拒。自动入群只能走服务侧配置（组织动作）。
8. `conversation-info` 对服务群报 FORBIDDEN「无权访问该内部群」，但 `+chat-messages` 可读 → 不要用 conversation-info 做可读性探针。
9. 子群探读报 `130003 OpendId is not in conversation` = 不在群内 = 降级信号；这是唯一可信的入群判定。
10. 2026-10-14 实测：海底捞子群可读（自动入群生效）；合思、千里马子群均 130003（千里马自动入群当时尚未配置，用户当日 19:43 仍在问 TAM）。
11. 卡片链接里 `openconversitionid` 后跟的是 `%3D` 不是 `=`（等号在 url= 参数里被再编码一层）→ 正则必须 `openconversitionid(?:%3D|=)`，值再双 decode。回归哨兵 tests/run-regression.py 含此 bug 类负控。
12. 模板占位符是双花括号 `{{token}}`，与 `str.format` 的转义语义冲突（format 会把 `{{` 渲染成字面 `{`）→ 脚本用逐 token `replace`，禁用 format。
13. `doc read` 正文字段名 = `markdown`；空文档 = `markdown:""`（publish 的「空才写」判据）。首调偶发只回 `{"success":true}`（trap#6），require 谓词已覆盖。
14. 🔴 `+chat-messages` 偶发返回**空 messages 列表**（envelope 正常、count=0）：空页会被误判成「窗口无消息」或「子群可读但无内容」（2026-10-14 实测同时造成海底捞 0 张假阴性与合思假 readable）。fetch_page 对空页重试 3 次后才接受为空；翻页中段空页耗尽重试会写 warnings「窗口老侧可能漏读」。
15. 🔴 130003 判定必须结构化（JSON errorCode/errorMsg 字段 + stderr），禁全文子串：消息正文/回读文档正文可能含 "130003" 数字串，子串匹配会造成假降级或整批崩溃（GLM-5.3 评审 P0，2026-10-14 修）。

## alidocs 落位

workspace `nb9XJrQQ3D0RPXyA`（个人空间 mine space）。树：`2025`(真 folder) > `客户`(adoc) > 客户文件夹(adoc) > `XX每日工单`(adoc) > `YYYYMMDD工单`(adoc)。整条链除顶层 2025 外全是「挂子文档的 adoc」，不是文件夹。「客户」层下另有燕京啤酒/威科/雍和植发等 16 个其他客户节点 → 按名字精确匹配防误挂。

建文档：`dws doc create --name "YYYYMMDD工单" --folder <每日工单nodeId> --content-file <md路径>`（--folder 收 adoc nodeId，勿传 drive dentryId）。

## 开放项与取舍记录（GLM-5.3 评审 2026-10-14）

- **催单事件未建模**：主群里催单事件的报文样式尚无逐字样本，不臆造解析器；SKILL.md 契约已撤下「催单」宣称。拿到样本后补 parse_cards 分支 + 日报催单计数（客户不满信号）。
- **规范单一事实源与催单采样路径已在列**：各轮评审/度量沉淀的工程规范以 [AGENTS.md](AGENTS.md) 为单一事实源（新规律同批回写，AGENTS.md 规则 M）；催单建模的采样路径已在列——先把主群内含「催单」关键词的消息原样落盘采样，攒够逐字样本再补 parse_cards 分支，不臆造（Kimi-K3 第二轮业务#2）。
- **probe 边界=now 是刻意取舍**：子群读入窗口后消息（次日客户确认、工程师补总结）正是「实质状态」的证据链；评审建议的「边界改窗口末」省 30-50% 子群调用但砍掉该证据，否决。子群消息已按 messageId 去重、300 条封顶。
- **补跑 >3 天**：子群可能已解散。诚实口径（Kimi-K3 冲突#1 裁决）：130003 本身**不能区分**未入群与已解散，「已解散」标签只在错误文本显式含解散/disband 时才打；文档「未入群(降级)」列可能实际含已解散case，补跑老日期时勿据此催 TAM。probe_error 三值：未入群/已解散/不可读，渲染三分支。
- **第二轮交叉评审（Ultimate + Kimi-K3，2026-10-14）**已修：publish 失败隔离、跟进节按客户隔离+回看 7 天、sanitize 按工单隔离 allowed+强制引证+卡片原文入 texts、130003 数字边界+一层嵌套信封、probe 空页告警上抛、不可读三分支渲染、create 非零 rc 先查重、collect 落盘进隔离、最早建单卡改比较式、完结卡缺标题 guard、翻页 boundary 不前进/ MAX_PAGES 耗尽告警、解析哨兵（卡片缺工单ID/未配置服务台发送者）、窗口外引证标注、总结缺失文档水印。报告：[tests/review-2026-10-14-ultimate-a.md](tests/review-2026-10-14-ultimate-a.md)、[tests/review-2026-10-14-ultimate-b.md](tests/review-2026-10-14-ultimate-b.md)、[tests/review-2026-10-14-kimi-k3.md](tests/review-2026-10-14-kimi-k3.md)。
- **自动入群不追溯历史子群**（2026-10-15 实测）：用户确认服务侧配置生效后，10-13 的合思/千里马子群仍 130003；配置只对生效后新建的子群起作用。`_auto_join_gap` 告警因此带日期门：仅工单日 ≥ 昨日 的跑批才告警「预期自动入群但实测全降级」，补跑老日期静默。新配置的首次活体证明＝合思/千里马配置生效后第一张新工单的子群 probe 转「读」。
- **登记未做（价值排序）**：①跨日报工单状态台账（持续未结/重开/跨多日完结）；②关单滞后 >24h 标记驱动小二关单；③首响/解决耗时与催单计数指标（待催单样本落盘采样后一起做）；④LIMIT 100→200 待 dws 支持验证。均不阻塞每日跑批。
- 评审报告全文：[tests/review-2026-10-14-glm53.md](tests/review-2026-10-14-glm53.md)；P0/P1/P2 与业务#1-4、#6、#7 已修，性能#1 否决（见上），业务#5 以标签方式部分落地。
- **第四轮：包结构落地（2026-10-15）**：单文件 scripts/ticket.py（52 函数）拆为九模块包 scripts/neil_ticket/（config/transport/parse/gate/render/collect/publish/cli/__init__），依赖方向 config←transport←parse←gate←render←collect/publish←cli、只准向左依赖、零循环；原 ticket.py 保留为兼容 shim（星号重导出 + monkeypatch 写入转发），`python3 scripts/ticket.py collect/publish` 与 `import ticket as T` 契约不变。触发点：用户批评「单文件谈不上扩展」；分层渗漏证据在第三轮 Qwen3.8-Max §4（run_dws 内嵌门禁、render 反依赖、followup_section 磁盘 IO 等）与 DeepSeek-V4-Pro（换输出目标需先拆 publish/alidocs 耦合）。度量复测（scripts/analyze-metrics.py 已改全包扫描）：跨模块重复行占比 0.00%（红线 <5%）、死代码 0 个、>40 行函数 0 个（最长 render/parse_cards 35 行）。工程契约沉淀为 AGENTS.md 规则 P；四个死配置键消费与规则 A require 合规化同批落地（见「配置键消费表」与 AGENTS.md 规则 A/K）。
- **零工单结转（用户 2026-10-15 指令「如果没有工单的话，可以复用一下昨天的」）**：某客户当日窗口零新工单时，回看 ≤7 天历史 collect（复用 `publish._load_prev_collects`），取该客户最近一个有工单的日期 D0，结转 D0 中官方未完结（`completed_at` 为空）的工单——「三、零工单说明」节替换为「三、零工单说明与昨日结转」，先一句「窗口内无新工单；以下工单结转自 <D0>，官方状态仍未完结」，再对每张结转工单渲染与正常详情同形的块（复用 `render._ticket_section`，块首加「- 结转自：<D0> 日报，当日无新工单」行）。内容复用 D0 的 `outputs/summary-<D0>-<key>.json`，缺失则回退 D0 collect 的 `desc_card/sol_card` 与规则默认；`effective_status` 复用 D0 summary 值并经 `sanitize_summary` **以 D0 slice 校验**（allowed 用 D0 slice 的建单/完结卡 id + subgroup_msg_ids），失败回退规则值并留痕（复用既有门禁，不新造）。概览表保持零行占位、不重复列结转工单（避免与「当日事件」口径混淆）。取舍：D0 存在但全完结或无任何历史 → 维持纯零工单说明节，**不再回看更早日**（只认最近一个有工单的日）；有新工单的日结转节不出现。装配在 `publish._carryover_data`（IO+门禁），纯渲染在 `render.carryover_section`（经 render 的 `carryover` 参数注入替换零工单节），符合分层依赖方向。回归 tests/run-regression.py 含正控（结转自/tid/D0 日期出现、旧文案被替换、概览零行占位、引证经 D0 slice 校验保留）、失败分支（非法引证回退留痕）与负控（prev 全完结→纯零工单说明）。
- **云端（QCA）可行性调研（2026-10-15，只读调研未建资源）**：结论＝**部分可跑通但不采用**。四问证据摘要：① dws CLI 有 linux 包（v1.0.64，GitHub release），云端环境可安装；② 云端网络 unrestricted，可达 api.dingtalk.com / alidocs.dingtalk.com；③ 登录态：`dws auth export/import` 设计上跨机可用，但 QCA vault 不可载入、且无文件上传类 MCP 工具，认证包只能经 env var base64（≤64KB）或 REST 投递；④ 调度：`create_forward_schedule` 支持 cron+timezone，但云端内置工具无 Task/subagent 能力、单 Turn 30 分钟上限、存储 24h 临时。不采用理由：总结 subagent 步（每客户一并发子代理，AGENTS.md 规则 N）无法原生并发 + 认证包上云泄漏面扩大（dws refresh 有效期至 2026-11-14、滚动 30 天；若未来上云建议：最小 scope、单组织 profile、到期不续、异常即 `dws auth reset` + 钉钉侧吊销）。本地 qoder_cron（每日 09:00 跑批 + 每 30 分钟完成标记巡检补偿，见 SKILL.md 维护操作；完成判据＝publish 收尾写的 `outputs/run-<工单日>.json`）为当前零改造路径。

## 实质状态（effective_status）

用户观察（2026-10-14）：很多工单实际已解决，但官方状态仍挂「处理中」（工程师发完总结/客户已确认，关单动作滞后或缺失）。日报因此加派生列「实质状态」：

- 取值枚举单一事实源＝scripts/neil_ticket/gate.py 的 `EFFECTIVE_ENUM` 常量（shim 可达）；本节只引用不复制枚举（改取值须改常量并按 AGENTS.md 规则 L 同步 SKILL/reference/tests）。各值语义（仅注释，非枚举定义）：已完结＝有官方完结卡；已解决待关单＝无完结卡但实质已解决；处理中＝子群可读但无解决信号；无法判定(无子群)＝子群不可读降级。
- 确定性信号（脚本 compute_signals）：子群内含【解决方案】且 >80 字的消息＝工程师总结块；命中确认语正则（没有了/谢谢/解决了/好的 收到/没问题/可以关单/恢复了/正常了）且 <120 字＝客户确认。
- 判定分工：子代理给 effective_status + effective_evidence{message_id, quote}；publish 用 sanitize_summary 机械校验 message_id 存在于子群原文/卡片 id 集合，失败回退 default_effective（规则默认）并在文档标注「引证校验失败回退规则」——LLM 提议、脚本门禁。

## subgroup_policy 语义

`probe_then_fallback`：先探读子群消息；成功 → 详情含处理过程要点；130003 → 降级为完结卡片【问题描述】【解决方案】逐字 + 标注「子群未入群」。客户配好自动入群后 probe 自然成功，**配置与代码零改动**。`auto_join_expected` 仅用于报告标注预期 vs 实测不一致。

## 配置键消费表（AGENTS.md 规则 J：每键必须被代码消费）

2026-10-15 落地态（第三轮 DeepSeek-V4-Pro §2 点名的四键零读取已全部由 scripts/neil_ticket/ 包消费，「消费代码由并行重构落地中」的承诺已兑现；行号以当日代码为准）：

| 配置键 | 消费模块.函数（行号） | 行为 |
|---|---|---|
| doc_title_pattern | `config.doc_title`（config.py:54-57），由 `publish.publish_one` 调用（publish.py:191） | 文档标题按 pattern 生成（`{yyyymmdd}` 占位），缺省 `"{yyyymmdd}工单"` 与原硬编码等价；标题用于 publish 查重命中与 doc create 命名 |
| subgroup_policy | `collect.collect_one` 读取（collect.py:101），`collect._probe_ticket` 分支消费（collect.py:75-87） | 探读策略：`probe_then_fallback`（默认）先探读子群、AccessDenied(130003) 才降级为不可读；`fallback_only` 跳过探读直接降级（probe_error=「策略fallback_only跳过探读」） |
| customer_folder_node | `publish._folder_warning`（publish.py:51-67），由 `publish_one` 拼入汇报行（publish.py:199） | 父节点校验：doc info 取 daily_doc_parent_node 的所属 folderId（`_doc_folder_id` publish.py:41-48 容错提取）与配置值比对；不一致或校验失败只在该客户汇报行追加警告，不阻断发布 |
| auto_join_expected | `collect._auto_join_gap`（collect.py:129-137），由 `_report_collect` 消费（collect.py:146-147） | 汇报行「预期 vs 实测」不一致标注：预期自动入群且本批有子群链接的工单实测全部降级 → 追加「（警告：预期自动入群但实测全降级）」 |

已被消费的键（对照）：timezone（cfg_tz）、doc_workspace（list_nodes）、customers[].key/name/service_group_name/service_group_cid/daily_doc_parent_node（collect_one/publish_one）、service_bot_name（可选，parse_cards 哨兵，缺省「阿里云服务台」）。

## 总结子代理契约 few-shot 样例（2026-10-14 真实数据验证）

输入：海底捞 2026-10-13 工单 E261013EN4RBWM（PolarDB），子群 cid 由建单卡「催单」链接两次 URL-decode 得 `cidaRKQP6jRenmtQmIyfFQFqA==`，与完结卡 chatRecord 链接一致；子群 32 条原文可读。输出（字段名严格 problem / process_bullets / solution；**process_bullets 精简合成为主线要点，不透人名**，用「客户」「值班小二」「ADB 官方支持」等角色词）：

```json
{
  "problem": "客户反馈“这都是 PolarDB 的数据库，怎么页面的配置差异这么大”，想知道如何根据数据库连接地址识别真实的实例类型（PolarDB、RDS、ADB）及具体配置（CPU、内存、节点数）。",
  "process_bullets": [
    "值班小二说明：根据连接地址判断第一个是 RDS MySQL、第二个是 PolarDB MySQL，并非同一产品，故页面配置差异大。",
    "按连接地址定位实例规格：rm-2ze9kictsgpfiu7bt 为 mysql.n4.xlarge.2c（8核32GB）高可用实例；pc-2ze285905v39np1f8 为 polar.mysql.g4.4xlarge（32核128GB）含一个只读节点。",
    "客户追问另一 ADB 数据库 amv-2zevyxl9b47km8f4，值班小二查到资源组 serverless 计算最大 64ACU、user_default 计算最大 48ACU、计算预留 48ACU。",
    "客户询问节点数，值班小二邀请 ADB 官方入群确认为 6 个 8ACU 节点，并补充控制台页面可查看集群配置。",
    "客户确认“没有了，多谢”，工程师给出总结并结单，工单状态变更为已完成。"
  ],
  "solution": "根据连接地址中的实例ID到控制台定位对应实例查询类型与规格：rm-2ze9kictsgpfiu7bt 为 RDS MySQL 高可用实例（mysql.n4.xlarge.2c，8核32GB）；pc-2ze285905v39np1f8 为 PolarDB MySQL 实例（polar.mysql.g4.4xlarge，32核128GB），含一个只读节点；amv-2zevyxl9b47km8f4 为 ADB Serverless 集群（资源组计算最大 64ACU、用户默认计算最大 48ACU、计算预留 48ACU，6 个 8ACU 节点）。页面配置差异的原因是三个连接地址分属不同云产品，无法直接从 URL 解析，需按实例ID在控制台查询。",
  "effective_status": "已完结",
  "effective_evidence": {"message_id": "msgkmS2FOt0Mk422JJGAZ5uCg==", "quote": "企业工单已完结"}
}
```

溯源要求：summary JSON 之外，子代理须在汇报里列支撑句的 messageId/时间戳（problem 2 条、process 逐 bullet、solution 指向工程师总结与完结卡）。

### process_bullets 反例：逐条摘录 vs 精简合成（2026-10-15 真实工单 E2610143Y5HYZP）

用户 2026-10-16 指令：process_bullets 把群聊原文几乎原封不动摘录下来是不对的。以下是同一张工单（DataWorks 独享资源组测试 MySQL 数据源连通失败）的错误写法与正确写法对照，`lint_process_bullets` 会把错误写法在发布行标为「疑似流水账」：

**反例（16 条逐条时间戳流水账，会被 lint 命中）**——每条以时间戳开头、把客户与工程师的每一句往返原样搬进来、透出真实人名：

```
"2026-10-14 16:28 阿里云服务台播报：胡凯隆提出的“数据源连接问题”已创建企业工单 E2610143Y5HYZP…当前值班小二曹咪…",
"16:29 胡凯隆在专项群发出两张截图并首述：“问题描述： 网段加了白名单，数据源还是无法测试通过”。",
"16:30 TAM-曹咪首次响应：…建议先确认资源组是否已添加指向数据源所在VPC或交换机的路由…",
"16:51 胡凯隆引用“…”追问…；16:52 曹咪答复…",
"16:53 胡凯隆贴出报错…",
"16:54 曹咪反问…；胡凯隆答复…",
"16:59 … 17:01 … 17:03 … 17:06 … 17:07 … 17:18 … 17:22 … 17:23 … 17:24 … 17:26 … 17:28 … 17:40 … 17:45 …"（逐条流水，共 16 条）
```

**正例（4 条主线要点，合并往返、去时间戳、不透人名）**：

```json
{
  "process_bullets": [
    "建单与首响：客户报 DataWorks 独享资源组测试 MySQL 数据源连通失败（connect timed out），称“网段已加白名单仍无法测试通过”；值班小二首次响应，判断需排查资源组到数据源 VPC 的路由、端口及白名单网段是否一致。",
    "定位白名单争议：反复围绕报错中的 192.168 网段——值班小二澄清那是资源组主网卡 IP（阿里云统一分配，非客户配的 172 交换机网段），内网连通须加入 RDS 白名单；客户因生产隔离库无法添加，工程师给出替代方案（改走公网 NAT 网关 + EIP 加白）。",
    "找到真因：客户提到同环境其他 MySQL 数据源可连通，值班小二判断卡在配置，引导核对数据源连接串，最终发现数据库名称填错（jdbc:mysql://…/hdl_data_insight）。",
    "解决与关单：客户修正数据库名后连通成功并确认“解决了哈就是数据库不对”；次日推送解决方案并结单，工单已完结。"
  ]
}
```

要点：正例保留全部关键事实（报错、网段争议、真因、结果）但把十几句往返压成 4 条主线；人名一律换角色词（客户/值班小二/工程师）；时间戳只在确有必要时保留极少数关键节点，不做逐句标注。

## 卡片逐字样本

逐字建单/完结卡片 fixture 在 [tests/fixtures/cards-2026-10-13.json](tests/fixtures/cards-2026-10-13.json)（含期望抽取值），回归跑 `python3 tests/run-regression.py`（含零工单渲染与占位符替换断言；负控：修复前的 `openconversitionid=` 旧正则在该 fixture 上 0 命中）。
