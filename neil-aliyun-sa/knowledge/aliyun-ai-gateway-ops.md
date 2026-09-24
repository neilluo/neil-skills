# AI 网关 · §10 可观测与运维 / §11 开发者门户与开放平台 / §12 实践教程与集成配方 / §13 OpenAPI 与 RAM 元信息

> **所属**：[[aliyun-ai-gateway]] 专题页家族（7 文件）｜**主页与导航**：[aliyun-ai-gateway.md](aliyun-ai-gateway.md)
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（186 个快照 = 149 个有正文页 + 37 个 TOC 容器页；另有 SLA 协议全文外部源 1 页）
> **事实标注体系**：`[官方｜slug]` raw 快照有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方原文错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕见 `tests/ai-gateway-rulings-2026-09-21.md`
>
> 🔖 正文中的 `W1`~`W7` 是**本次蒸馏批次的分工代号**（7 路并行 worker），不是产品术语；对照表见 [主页 §0.6](aliyun-ai-gateway.md)。

🔴 **对客纪律**：9 类资源配额在错误码页全是 `%s` 占位符 → 容量规划必须走配额中心/工单。140 个 Action 中 66 个（47.1%）无法资源级授权，MCP / AI 模型元信息 / 消费者组 / 插件四类对象**在 RAM 层面根本没有 ARN 定义** → 多租户只能分账号或分实例。`access-vertex-ai-through-ai-gateway` **不含**跨境网络要求（只有「VPC 须绑公网 NAT」），**不得据该页承诺跨境网络方案**。

## 本章导读

> 蒸馏员：W7 ｜ 快照抓取日期：2026-09-21 ｜ 覆盖 25 页（全部读完）
> 事实标注体系见 `tests/ai-gateway-distill-contract-2026-09-21.md` §2。

## §10 可观测与运维

### 10.1 可观测能力全景：谁看什么、在哪看、要不要另外付钱

| 能力 | 控制台入口 | 数据底座 | 是否另外计费 | 来源 slug |
|---|---|---|---|---|
| Model API 可观测（AI 大盘） | 实例 → Model API → 目标 API → **统计** 页签（大盘名 `apig-ai-api-dashboard`） | 日志服务 SLS（**必须先开启网关日志投递**，否则页面提示「立即开通日志投递」） | AI 产品不收日志费用，SLS 按使用量收费 | `ai-observable`｜`enable-gateway-log-delivery` |
| Model API 日志（SQL 分析） | 同上 → **日志** 页签 | SLS | 同上 | `ai-observable` |
| 网关业务监控 | 实例 → **观测分析 > 业务监控** | SLS（依赖网关日志投递） | 「AI 网关免费支持查看业务监控大盘，若需监控企业大盘或导出监控数据，需开通云监控企业版」，云监控企业版按使用量收费 | `view-gateway-monitoring-data` |
| 网关资源监控 | 实例 → **观测分析 > 资源监控** | 云监控 | 同上（企业大盘/导出需云监控企业版） | `view-gateway-monitoring-data` |
| 网关链路追踪 | 实例 → **观测分析 > 链路追踪**；或 **参数配置 > 可观测性参数 > 链路追踪** | 阿里云链路追踪 Tracing Analysis 或 Skywalking | 「AI 网关本身不收取链路追踪费用，但如果您使用了链路追踪 Tracing Analysis 服务，链路追踪 Tracing Analysis 产品将根据您的使用量进行收费」，具体以 Tracing Analysis 价格说明为准 | `enable-gateway-link-tracing` |
| 网关访问日志投递 | **观测分析 > 日志中心**；或 **参数配置 > 可观测性参数 > 访问日志投递配置** | SLS | AI 产品不收取日志费用，SLS 按使用量收费 | `enable-gateway-log-delivery` |
| MCP 服务日志 | 实例 → **MCP管理** → 目标服务卡片 → **日志** 页签 | SLS | 同上（原文写作「按使用功能计费」，链接同为 SLS 48220） | `enable-mcp-service-log-delivery` |
| 请求/响应采集（Header/Body） | 实例 → **参数配置 > 访问日志投递配置 > 请求/响应采集** | 随访问日志进 SLS | 「开启该功能会显著增加日志量和日志成本，建议仅在调试时开启，问题定位完成后及时关闭」 | `request-response-capture-1` |
| AI 请求日志字段策略 | Model API → **策略与插件** → 预置策略与插件 → **AI 请求日志** | 写入 `ai_log` 字段随访问日志投递 | 功能本身不单独标价；定位为「控制日志记录范围、降低存储成本」 | `configure-ai-log-policy` |
| 告警 | 看板右上角图标；或左侧导航 **告警 > 创建报警规则** | 云监控 | 文档未说明 | `view-gateway-monitoring-data` |

🟠 **SA 对客要点**：AI 网关侧的**全部**可观测能力都建立在「网关日志投递到 SLS」这一前提上。未开日志投递 → 统计页签、业务监控都不可用。因此「AI 网关账单 ≠ 全成本」：**SLS 按量 + 云监控企业版（可选）+ Tracing Analysis 按量（可选）** 是三笔连带费用。[官方｜ai-observable｜enable-gateway-log-delivery｜view-gateway-monitoring-data｜enable-gateway-link-tracing]

🟠 **`ai-observable` 页附带说明**：「限流、缓存、联网搜索策略在处理异常时会透出异常日志，并提供完整策略日志的查看能力」——即策略类问题排查也走同一条日志链路。[官方｜ai-observable]

### 10.2 Model API 可观测指标（`ai-observable`）

大盘 `apig-ai-api-dashboard` 的关键指标（逐条照抄，含粒度限定）：

| 指标 | 官方定义（含粒度/拆分维度） |
|---|---|
| QPS | 每秒 AI 请求和响应的数量统计，分为 AI 请求的 QPS、流式响应的 QPS 和非流式响应的 QPS |
| 请求成功率 | 即 AI 请求的成功率，**可按秒、15 秒、分钟进行统计** |
| token消耗数/s | 每秒消耗的 token 数量，分为输入 token、输出 token 和总计 token |
| 请求平均RT/ms | 一段时间内（**秒、15 秒、分钟**）AI 请求的平均响应时间（ms），分为非流式 RT、流式 RT（流式响应的整体时间）、流式首包 RT（流式响应的首包时间） |
| 缓存命中情况/s | 一段时间内缓存的命中数和 miss 数统计 |
| 限流请求数/s | 一段时间内被限流的请求和正常请求的统计 |
| 模型token使用统计 | 一段时间内不同模型的 token 消耗统计 |
| 消费者token使用统计 | 一段时间内不同消费者的 token 消耗统计 |
| 风险类型统计 | 被内容安全检测出来的风险，按照风险类型、消费者等维度的统计 |
| 风险消费者统计 | 被消费者鉴权检测出来的消费者风险统计 |
| 限流消费者统计 | 被限流检测出来的消费者风险 |

[官方｜ai-observable]

🟠 **指标粒度结论**：AI 维度的时间粒度是**秒 / 15 秒 / 分钟**三档，且 token、RT、成功率都能按**模型**和**消费者**两个维度切分——这是 FinOps 分账与「哪个客户在烧钱」类问题的直接答案来源。[官方｜ai-observable]

**Agent API 可观测 / MCP 服务可观测**：不在 W7 指派页内，归 W5（`agent-api-observable`、`mcp-observable`、`agent-management-access-and-observation`）。W7 侧仅能确认 MCP 服务的日志入口与 Logstore 归属（见 10.5）。[文档未说明 — 本章查无]

### 10.3 网关监控数据（`view-gateway-monitoring-data`）

**前提条件（三项全部）**：创建网关实例 + **开启网关日志投递** + **开通云监控**。[官方｜view-gateway-monitoring-data]

| 看板 | 可见指标 |
|---|---|
| 全局看板 | PV、UV、网关入流量、网关出流量、Method分布、网关状态码分布、后端服务状态码分布、QPS、请求成功率、请求RT/ms、请求分布 |
| 灰度对比看板 | 在灰度发布场景下，通过选择线上服务与灰度服务进行对比，查看 QPS、请求成功率、请求RT/ms、请求分布 对比情况 |

- 默认显示**最近 1 小时**数据，可在左上方设置时间筛选；右上方可开启**自动刷新**。[官方｜view-gateway-monitoring-data]
- 🔴 **资源监控不支持 Serverless 实例**：「Serverless实例不支持资源监控。」[官方原文｜view-gateway-monitoring-data]
- 资源监控指标：网关CPU使用率(%)、内存负载(B)、网关内存使用率(%)、网络入方向IO负载(B/s)、网络出方向IO负载(B/s)、磁盘Read负载(B/s)、磁盘Write负载(B/s)。[官方｜view-gateway-monitoring-data]

🔴 **压测/容量类高频争点（逐字照抄）**：
> 网关 CPU 使用率为多核聚合计算值。双核场景下，一个 CPU 使用率 100%、另一个 50%，综合显示 75%。多核实例压测时 CPU 监控值不会达到 100%，属正常行为。
> [官方原文｜view-gateway-monitoring-data]

[推断] 由「多核聚合 + 压测不会到 100% 属正常行为」可推出：客户以「CPU 没打满所以还不必升配」为结论是不可靠的，SA 做容量判断时应结合 RT/成功率而非只看聚合 CPU 百分比。推理链仅为上述原文；raw 未给出替代判据 → 判据本身[文档未说明]。

### 10.4 网关日志投递（`enable-gateway-log-delivery`）

- 目标存储：**日志服务 SLS**（「日志投递功能是 AI 网关结合阿里云日志服务 SLS 提供的服务」）。[官方｜enable-gateway-log-delivery]
- 计费：「AI产品不收取日志费用，但日志服务SLS将根据您的使用量收费」，指向 SLS **按量付费**。[官方原文｜enable-gateway-log-delivery]
- 两条开启路径：**观测分析 > 日志中心 > 立即开启日志投递功能**；或 **参数配置 > 可观测性参数 > 访问日志投递配置**（打开「网关访问日志 (AccessLog)」）。[官方｜enable-gateway-log-delivery]
- Project 选择：**使用默认** 或 **使用已有**。
- 🔴 **默认 Project 命名格式（对客定位日志库时必用）**：`aliyun-product-data-{阿里云主账号UID}-{地域}`
  - 示例（中国站）：`aliyun-product-data-1069xxxxx28319-cn-shanghai`
  - `aliyun-product-data` 为固定前缀；`{地域}` 为实例所在地域 ID，**因站点而异**（中国站为 `cn-*`，如 `cn-shanghai`、`cn-hangzhou`；国际站为国际地域 ID，如 `ap-southeast-1`、`us-east-1`）
  - 该命名说明同样适用于「通过日志中心」选择**使用默认**的场景
  [官方｜enable-gateway-log-delivery]
- 🟠 **跨系统兼容开关**：可打开「**输出日志兼容 Nginx Ingress 格式**」，「使输出日志与 Nginx Ingress 的格式保持一致，以便于统一日志分析和提高跨系统兼容性」。→ 客户从 Nginx Ingress 迁移到 AI 网关时，日志解析规则可复用的官方抓手。[官方｜enable-gateway-log-delivery]

### 10.5 MCP 服务日志投递（`enable-mcp-service-log-delivery`）

| 项目 | 官方口径 |
|---|---|
| 目标存储 | SLS（与网关日志投递同一产品） |
| 开启状态粒度 | 「**日志投递的开启状态是网关实例级别的**」 |
| 两类日志 | **网关请求日志** 与 **MCP服务日志** |
| 🔴 MCP服务日志的限制 | 「**MCP服务日志仅支持带有 `HTTP转MCP` 标签可以查询分析日志**」→ 其他形态的 MCP 服务无此类日志 |
| Project / Logstore 关系 | 「**网关请求日志** 和 **MCP服务日志**如果都使用默认开启日志投递服务，日志服务创建的 Project 是同一个，只是 Logstore 不同」 |
| 网关请求日志的开启方式 | 方式一：创建实例时选择使用日志服务（SLS）；方式二：日志页签单击**立即开启日志投递功能**，选**使用默认**或**使用已有** Project |
| MCP服务日志的开启方式 | 仅方式二（单击**立即开启日志投递功能**，选默认或已有 Project） |
| 计费 | 「AI产品不收取日志费用，但日志服务SLS将根据您的使用量收费」，指向 SLS「按使用功能计费」 |
| 常用查询 | 提供「网关请求日志常用查询条件」/「MCP服务日志常用查询条件」的**查看**按钮，可复制查询语句到 SLS 搜索栏 |

[官方｜enable-mcp-service-log-delivery]

**字段差异**：`enable-mcp-service-log-delivery` 与 `enable-gateway-log-delivery` 的**日志字段表 SHA256 完全相同**，**请求失败原因（Response_Flag）章节也完全相同**（W7 实测比对）。→ 两页字段无差异，只写一份（见 10.6）。两页正文整体不同（MCP 页多了开启粒度、`HTTP转MCP` 标签限制等说明），**不算重复页**。[官方｜enable-gateway-log-delivery｜enable-mcp-service-log-delivery]

### 10.6 访问日志字段字典（27 个字段，两页共用）

| 字段名 | 类型 | 含义 |
|---|---|---|
| __time__ | long | 日志产生的时间。 |
| cluster_id | string | 购买的网关实例。 |
| ai_log | json | 针对 Model API/Agent API/MCP API 设计的日志字段，字段格式为 json。**其他类型的 API 此字段为空**（子字段见下表）。 |
| authority | string | 请求报文中的 Host Header。 |
| bytes_received | long | 请求的 Body 大小（不包含 Header）。 |
| bytes_sent | long | 响应的 Body 大小（不包含 Header）。 |
| downstream_local_address | string | 网关 Pod 地址。 |
| downstream_remote_address | string | 连接到网关的 Client 端地址。 |
| duration | long | 请求的整体耗时。包含从网关收到来自下游的第一个字节开始，到发送出最后一个响应字节为止的时间段。单位毫秒。 |
| method | string | HTTP 方法。 |
| path | string | HTTP 请求中的 Path。 |
| protocol | string | HTTP 的协议版本。 |
| request_duration | long | 从网关收到来自下游的第一个字节开始，到收到来自下游的最后一个字节为止的时间段。单位毫秒。 |
| request_id | string | 网关会为每次请求产生一个 ID，并放在 Header 的 `x-request-id` 中，后端可以根据这个字段记录并进行排查。 |
| requested_server_name | string | SSL 连接时使用的 Server Name。 |
| response_code_details | string | 提供与响应码相关的额外信息。例如 `via_upstream` 表示响应码是由后端服务返回的，`route_not_found` 表示请求没有匹配的路由。 |
| response_tx_duration | long | 从网关收到来自上游的第一个字节开始，到给下游发送出最后一个字节为止的时间段。单位毫秒。 |
| route_name | string | 路由名。 |
| start_time | string | 请求开始时间。格式：UTC。 |
| trace_id | string | Trace ID。 |
| upstream_cluster | string | 上游集群。 |
| upstream_host | string | 上游 IP。 |
| upstream_local_address | string | 本地连接上游的地址。 |
| upstream_service_time | long | 上游服务处理请求的耗时（毫秒），包括网关访问上游服务的网络耗时和上游服务自身处理耗时两部分。 |
| upstream_transport_failure_reason | string | 上游链接失败的原因。 |
| user_agent | string | HTTP Header 中的 UserAgent。 |
| x_forwarded_for | string | HTTP Header 中的 `x-forwarded-for`，通常用来表示 HTTP 请求端真实 IP。 |

[官方｜enable-gateway-log-delivery｜enable-mcp-service-log-delivery]

**`ai_log` 的 12 个子字段**：

| 子字段 | 官方含义 |
|---|---|
| api | ai api 的名称 |
| cache_status | Model API 中开启内容缓存时该字段会反映请求是否命中缓存 |
| consumer | 开启消费者鉴权后，此字段会记录当前请求的消费者身份 |
| fallback_from | Model API 中开启 fallback 策略时，此字段记录请求从哪一条路由 fallback 过来 |
| input_token | LLM 请求输入 token 数 |
| llm_first_token_duration | LLM 请求首包 RT |
| llm_service_duration | LLM 请求整体 RT |
| model | LLM 请求的模型名称 |
| output_token | LLM 请求输出 token 数 |
| response_type | LLM 请求流式/非流式 |
| safechack_status | LLM 请求内容安全检测状态 **[原文如此，疑为 safecheck 拼写错误]** |
| token_ratelimit_status | LLM 请求是否被限流拦截 |

[官方原文｜enable-gateway-log-delivery｜enable-mcp-service-log-delivery]

🟠 **耗时字段三层拆解（排障主抓手）**：`duration`（整体）包含 `request_duration`（下游首字节→下游末字节）、`response_tx_duration`（上游首字节→给下游发送完最后一个字节）、`upstream_service_time`（含网关到上游的网络耗时 + 上游自身处理耗时）。`llm_first_token_duration` / `llm_service_duration` 则是 AI 专属的首包 RT / 整体 RT。[官方｜enable-gateway-log-delivery]

### 10.7 `Response_Flag` 请求失败原因码（23 个，两页共用）

原文说明：「请求失败的原因主要通过日志中 `Response_Flag` 的值判断」；「**下游指客户端，上游指后端服务**」。

| Flag | 含义（照抄） |
|---|---|
| UH | 上游集群中，没有健康的上游主机 |
| UF | 上游连接失败 |
| NR | 给定请求未配置路由 |
| URX | 请求被拒绝，因为达到了上游重试限制（HTTP）或最大连接尝试次数（TCP） |
| NC | 无法找到上游集群（排查步骤见下） |
| DT | 请求或连接超过了 `max_connection_duration` 或 `max_downstream_connection_duration` |
| DC | 下游连接终止 |
| LH | 本地服务未通过健康检查请求 |
| UT | 上游请求超时 |
| LR | 连接本地重置 |
| UR | 上游远程重置 |
| UC | 上游连接终止 |
| DI | 请求处理被延迟一段时间，该延迟时间由故障注入指定 |
| FI | 请求被故障注入指定的响应码中止 |
| RL | 请求在本地被 HTTP 速率限制过滤器限制，**除了 429 响应码之外** |
| UAEX | 请求被外部授权服务拒绝 |
| RLSE | 请求被拒绝，因为速率限制服务出现错误 |
| IH | 请求被拒绝，因为在严格检查的标头中设置了无效值 |
| SI | Stream 流空闲超时 |
| DPE | 下游请求存在 HTTP 协议错误 |
| UPE | 上游响应存在 HTTP 协议错误 |
| UMSDR | 上游请求达到了最大流程持续时间 |
| OM | 超负荷管理器终止了请求 |

[官方｜enable-gateway-log-delivery｜enable-mcp-service-log-delivery]

🔴 **`NC` / `cluster_not_found` 官方四步排查**（「网关访问不到后端」类工单的标准答案，第 3 步是网络设计硬约束）：
1. 确认路由关联的 AI 服务中，模型提供商及后端服务地址配置正确且可用。
2. 确认 AI 服务已绑定到网关实例，且后端服务的健康检查状态正常。
3. **确认网关所在 VPC 的网络可访问后端服务地址。若后端服务为公网域名，需在该 VPC 中配置 NAT 网关和 SNAT 条目，否则网关无法访问公网地址。**
4. 确认上述配置变更已发布并生效。
[官方原文｜enable-gateway-log-delivery｜enable-mcp-service-log-delivery]

### 10.8 AI 日志策略：采集什么字段、怎么裁（`configure-ai-log-policy`）

**定位**：「AI 网关在处理模型请求时会产生大量日志数据。AI 日志策略支持按需选择日志字段、使用内置模板批量添加字段、自定义日志字段及 JSON PATH 配置，从而**控制日志记录范围、降低存储成本**。此功能对已兼容协议（如 OpenAI、百炼）和自定义 HTTP 协议均适用，但两者的配置能力有所差异。」[官方原文｜configure-ai-log-policy]

**前提条件**：已开通阿里云 API 网关服务 + 已创建 AI 网关实例 + **已配置至少一个 Model API 或 Agent API**。[官方｜configure-ai-log-policy]

#### 10.8.1 协议类型决定配置能力（选型判据）

| 能力 | 已兼容协议（如 OpenAI、百炼） | 自定义 HTTP 协议 |
|---|---|---|
| 预定义基础字段 | 支持 | **不支持** |
| 内置模板批量添加 | 支持 | 支持 |
| 自定义 JSON PATH 字段 | 支持 | 支持 |
| 字段独立启用/禁用 | 支持 | 支持 |

[官方｜configure-ai-log-policy]

- **预定义基础字段的适用面（有边界）**：「已兼容协议中支持预定义基础字段能力的协议与场景：Model API：**OpenAI 和百炼下的文本生成、图片生成场景**；Agent API：**百炼应用**。」→ 其他场景/其他供应商协议**不在**预定义基础字段覆盖范围内。[官方原文｜configure-ai-log-policy]
- **配置粒度**：「每条 Model API 的路径（Path）拥有独立的字段配置」；「在后端服务模型为多服务时，一个 Path 可能对应多条路由，**同 Path 的多条路由对应使用同一份配置**」；「修改某个路径下的字段配置不会影响其他路径」。[官方｜configure-ai-log-policy]
- 自定义 HTTP 协议的实操口径：不提供带预定义 JSON Path 的基础字段，需自行配置；「也可以使用模板导入**相近协议**的模板作为基础，再根据实际协议结构调整 JSON PATH」。[官方｜configure-ai-log-policy]

#### 10.8.2 基础字段（4 个分类）

| 分类 | 字段示例 | 说明 |
|---|---|---|
| 对话 | question、answer | 用户提问和模型响应内容 |
| 元信息 | request_model、model、chat_id | 请求模型名称、响应模型名称、会话 ID |
| 用量 | input_token、output_token、total_token、input_token_details、output_token_details、input_tokens_details.cached_tokens、output_tokens_details.reasoning_tokens | 请求和响应的 Token 消耗量及明细 |
| 工具 | tool_use | 工具调用信息 |

[官方｜configure-ai-log-policy]

🔴 **字段落盘位置（写 SLS 查询语句必须知道）**：
> 基础字段统一以固定的 Key（字段名称）写入日志。其中，**除 answer、question 外，其余基础字段均作为一级字段存放在 `ai_log` 字段下，answer 与 question 已从 `ai_log` 中单独抽取，作为独立字段存放。**
> [官方原文｜configure-ai-log-policy]

🔴 **系统内置字段（默认开启）**：`model`、`chat_id`、`input_token`、`input_token_details`、`output_token`、`output_token_details`、`total_token`。「系统内置字段默认开启，字段提取时优先按已配置的 JSON PATH 进行提取，未配置时按系统内置规则进行默认提取。」[官方｜configure-ai-log-policy]

🟠 **默认开启/关闭的实操含义**：官方配置示例表中 `question` 与 `answer` 的「默认启用」列为**否**，而 `input_token`/`output_token`/`total_token` 为**是**。→ **默认配置下日志里不含对话正文**，客户要做内容审计/合规留痕必须显式开启 question/answer；反过来，这也是控制 SLS 存储成本的最大杠杆。[官方｜configure-ai-log-policy]

**流式与非流式是两套 JSON PATH**：「多数响应字段同时支持非流式响应和流式响应两种提取方式，对应不同的 JSON PATH 配置。以 answer 字段为例，在 `/v1/chat/completions` 路径下，非流式响应的提取路径为 `choices.0.message.content`，流式响应的提取路径为 `choices.0.delta.content`。」[官方｜configure-ai-log-policy]

#### 10.8.3 JSON PATH 语法与三条路径的差异

- 语法：**GJSON**。`.` 访问对象字段；数组下标从 `0` 开始；支持多层嵌套。示例 `choices.0.message.content`。[官方｜configure-ai-log-policy]
- 官方示例响应中的映射：`answer` ← `choices.0.message.content`（值 `我是阿里云开发的一款超大规模语言模型，我叫千问。`）；`model` ← `model`（值 `qwen-plus`）；`input_token` ← `usage.prompt_tokens`（值 `3019`）。该示例响应还含 `usage.total_tokens: 3123`、`usage.completion_tokens: 104`、`usage.prompt_tokens_details.cached_tokens: 2048`、`id: chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a`。[官方｜configure-ai-log-policy]

| 字段 | 来源 | `/v1/chat/completions` | `/v1/completions` | `/v1/responses` |
|---|---|---|---|---|
| question | 请求 | `messages.@reverse.#(role=="user").content` | `prompt` | `input` |
| answer | 非流式响应 | `choices.0.message.content` | `choices.0.text` | `output.#(type=="message").content.#(type=="output_text").text` |
| answer | 流式响应 | `choices.0.delta.content` | `choices.0.text` | `delta` |
| input_token | 非流式响应 | `usage.prompt_tokens` | `usage.prompt_tokens` | `usage.input_tokens` |
| input_token | 流式响应 | `usage.prompt_tokens` | `usage.prompt_tokens` | `response.usage.input_tokens` |

[官方｜configure-ai-log-policy]

🟠 切换 Path 时基础字段 JSON PATH **会自动更新**；单字段可在行操作列**编辑**改 JSON PATH。[官方｜configure-ai-log-policy]

#### 10.8.4 内置模板：15 个（OpenAI 6 + 百炼 9）

**OpenAI 模板（6 个）**

| 场景 | 路径 |
|---|---|
| 文本生成 | `/v1/chat/completions` |
| 文本生成 | `/v1/completions` |
| 文本生成 | `/v1/responses` |
| 图片生成 | `/v1/images/generations` |
| 图片生成 | `/v1/images/edits` |
| 图片生成 | `/v1/images/variations` |

**百炼模板（9 个）**

| 场景 | 路径 |
|---|---|
| 文本生成 | `/api/v1/services/aigc/text-generation/generation` |
| 图片生成 | `/api/v1/services/aigc/text2image/image-synthesis` |
| 图片生成 | `/api/v1/services/aigc/image2image/image-synthesis` |
| 图片生成 | `/api/v1/services/aigc/image2image/out-painting` |
| 图片生成 | `/api/v1/services/aigc/virtualmodel/generation` |
| 图片生成 | `/api/v1/services/aigc/background-generation/generation` |
| 图片生成 | `/api/v1/services/aigc/multimodal-generation/generation` |
| 图片生成 | `/api/v1/tasks` |
| Agent应用 | `/api/v1/apps/{app_id}/completion` |

[官方｜configure-ai-log-policy]

- 🔴 **字段量级**：「内置模板提供的可选字段数量显著多于基础字段。以 OpenAI `/v1/chat/completions` 模板为例，**可选字段超过 200 个**，并按照对话、配置、工具、用量、元信息、候选、标识、缓存、多模态、概率等类别进行组织。」[官方原文｜configure-ai-log-policy]
- 🔴 **官方免责声明（照抄）**：「内置模板中的字段配置**可作为参考**，实际字段定义及含义**请以对应协议的 API 文档为准**。」→ 字段语义被推给上游协议文档，SA 对客承诺字段含义时不能只引 AI 网关文档，**这是文档级空白**。[官方原文｜configure-ai-log-policy]
- 界面提示「基础字段 (14/24)」是**已启用数/总数**的示例展示形式（原文用「如」引出），不是配额上限；可单击「仅展示开启的字段」过滤。[官方｜configure-ai-log-policy]

#### 10.8.5 自定义字段参数

| 参数 | 说明 |
|---|---|
| 字段名称 | 自定义的字段名称，作为日志中 `ai_log` 字段下的 Key |
| 来源 | 可选：**请求、非流式响应、流式响应** |
| Json Path | 从对应来源数据中提取字段值的 JSON Path 路径 |
| 描述 | 字段的用途说明 |

[官方｜configure-ai-log-policy]

自定义字段添加后显示在**自定义字段**标签页，可通过操作列的**编辑**和**删除**管理。[官方｜configure-ai-log-policy]

### 10.9 🔴 请求/响应采集（Body 采集）：硬限制逐字照抄（`request-response-capture-1`）

**定位与作用域**：「请求/响应采集是网关的一项**日志增强能力**，可将经过网关的请求和响应内容记录到访问日志中，随访问日志投递到日志服务（SLS），便于问题排查、接口审计和流量分析。采集内容分为**请求头、请求体、响应头和响应体四项，每项可独立开启或关闭**。该功能在**网关级别生效，作用于该网关下的所有流量**。」[官方原文｜request-response-capture-1]

🔴 **成本告警（原文「重要」）**：
> 开启该功能会显著增加日志量和日志成本，建议仅在调试时开启，问题定位完成后及时关闭。
> [官方原文｜request-response-capture-1]

#### 10.9.1 版本要求（硬门槛）

| 网关类型 | 最低引擎版本 |
|---|---|
| 云原生 API 网关 | **2.1.18 及以上** |
| AI 网关 | **2.1.20 及以上** |

- 🔴 **「Serverless版不支持该功能。」**[官方原文｜request-response-capture-1]
- 「开启时系统会**自动校验引擎版本**，不满足要求时会**拒绝并提示升级**。**关闭操作不受版本限制，任何版本都可随时关闭**。」[官方｜request-response-capture-1]
- 「若版本过低，请先升级网关引擎版本后再开启。」[官方｜request-response-capture-1]

#### 10.9.2 配置项与默认值

| 配置项 | 说明 | 默认值 |
|---|---|---|
| 记录请求 Headers | 是否采集请求头 | **关闭** |
| 记录请求 Body | 是否采集请求体 | **关闭** |
| 请求 Body 最大采集大小（Bytes） | 请求体最大采集字节数 | **5120（5 KB）** |
| 记录响应 Headers | 是否采集响应头 | **关闭** |
| 记录响应 Body | 是否采集响应体 | **关闭** |
| 响应 Body 最大采集大小（Bytes） | 响应体最大采集字节数 | **5120（5 KB）** |

[官方｜request-response-capture-1]

#### 10.9.3 Body 最大采集大小规则（4 条，逐字）

1. 单位为字节（Bytes），**仅在对应 Body 采集开启时生效**。
2. **不填或填 0 及以下：按默认 5 KB 采集**。
3. 「单个 Body 的最大采集大小上限取决于网关实例的部署形态，**请以控制台配置页给出的上限提示为准**；当前为**全托管实例 5 KB（5120 字节）**、**非全托管实例 200 KB（204800 字节）**。」
4. **超出该大小的 Body 内容会被截断，只保留前面部分。**

[官方原文｜request-response-capture-1]

🔴 **这是契约 §3.6 定义的「用『以…为准』把数字推走」的情形**：官方一面给出 5 KB / 200 KB 的当前值，一面声明以控制台配置页上限提示为准。**SA 做合规/审计承诺时必须以控制台实测为准，此处属文档级空白**。同时 raw 未定义「全托管实例」「非全托管实例」分别对应哪种售卖形态（专享 / Serverless）→ 术语映射[文档未说明]。

#### 10.9.4 开启前置与采集内容落盘字段

- 🔴 **前置**：「采集内容随访问日志投递到日志服务（SLS）。**开启前，确保已配置访问日志投递**。」[官方原文｜request-response-capture-1]
- 入口：网关详情页 → **参数配置** → **访问日志投递配置** 区域 → **请求/响应采集** 右侧状态链接 → 弹窗配置 → 保存。保存成功后状态链接变为「已开启」；四项全部关闭即等同关闭整个功能，状态链接变为「未开启」，相关内容不再写入访问日志。[官方｜request-response-capture-1]

| 采集内容 | 访问日志字段 | 控制开关 |
|---|---|---|
| 请求头 | `request_headers` 对象下的 `envoy.all_request_headers` 子字段 | 记录请求 Headers |
| 请求体 | 顶层字段 `request_body` | 记录请求 Body |
| 响应头 | `response_headers` 对象下的 `envoy.all_response_headers` 子字段 | 记录响应 Headers |
| 响应体 | 顶层字段 `response_body` | 记录响应 Body |

[官方｜request-response-capture-1]

- 头字段共存机制：「`request_headers` / `response_headers` 对象也承载访问日志的自定义 Header 采集能力，因此采集到的完整头信息**以子字段形式与其共存，不会互相覆盖**」。[官方｜request-response-capture-1]
- **字段按需出现**：「只有对应采集项开启时，相关字段才会写入访问日志；未开启的采集项对应的字段不会出现。」[官方｜request-response-capture-1]
- 截断在字段层的体现：「当请求体/响应体超过配置的最大采集大小时，对应字段中只保留截断后的前面部分内容。」[官方｜request-response-capture-1]

#### 10.9.5 数据安全与采集范围限制

> **敏感数据**：请求/响应的头和正文中可能包含令牌、密码、个人信息等敏感数据。开启前请评估合规与脱敏要求，仅开启必要的采集项，并合理设置 Body 大小。
> **Body 采集范围**：**并非所有类型的正文都会被记录（受内容类型限制）**，且超过设置大小的部分会被截断。
> [官方原文｜request-response-capture-1]

🔴 「受内容类型限制」但**具体哪些 Content-Type 会被采集/跳过，raw 未列出** → 客户问「SSE 流式响应体能采到吗」「multipart 文件上传能采到吗」时[文档未说明]。

### 10.10 网关链路追踪（`enable-gateway-link-tracing`）

| 项目 | 官方口径 |
|---|---|
| 依赖产品 | 「AI 网关支持集成**阿里云链路追踪 Tracing Analysis 服务**和 **Skywalking 服务**」，用途为「帮助您定位性能瓶颈，提升微服务开发诊断效率」 |
| 前提条件 | 已创建 AI 网关实例；**已开通阿里云链路追踪**（未开通需用阿里云账号登录链路追踪控制台开通） |
| 开启方式 | 两种入口：① **观测分析 > 链路追踪 > 开启链路追踪**；② **参数配置 > 可观测性参数 > 链路追踪** 右侧图标 |
| 配置项 | 在「链路追踪配置」对话框开启**链路追踪状态**，选择**链路追踪协议**和**采样率**，然后单击确定 |
| 查看位置 | 开启后在网关实例 **观测分析 > 链路追踪** 中查看网关链路追踪数据 |
| 计费 | 「AI 网关本身不收取链路追踪费用，但如果您使用了链路追踪 Tracing Analysis 服务，链路追踪 Tracing Analysis 产品将根据您的使用量进行收费。具体收费详情**以链路追踪 Tracing Analysis 价格说明为准**」 |

[官方｜enable-gateway-link-tracing]

- **采样率取值范围与默认值**：[文档未说明]（页面只说「选择采样率」，未给区间/步长/默认值）。
- **开启链路追踪的性能开销**：[文档未说明]。
- **「链路追踪协议」的可选值枚举**：[文档未说明]（页面未列出具体协议名，仅在开头提到 Tracing Analysis 与 Skywalking 两类服务）。
- 与访问日志的关联：访问日志字段中有 `trace_id`（见 10.6）。[推断] 由 `enable-gateway-log-delivery` 的 `trace_id` 字段 + `enable-gateway-link-tracing` 的链路数据在同实例「观测分析」下可见，推出可用 trace_id 做日志↔链路串联；raw 未明文写出该用法。
- 相关 OpenAPI：`GetTraceConfig`（获取链路追踪配置），流控配额 `60/1(s)`。[官方｜api-apig-2024-03-27-overview-ai-gateway｜api-apig-2024-03-27-quota-ai-gateway]

### 10.11 实例标签管理（`label`）

- 结构：产品标签、设备标签和分组标签的结构为 **标签键：标签值**。[官方｜label]
- 🔴 **配额**：「**每个 AI 网关实例最多可设置 20 个标签。**」[官方原文｜label]
- 🔴 **保留前缀**：「**ACS 开头的标签为系统预留标签，请勿使用此值作为标签的标签键。**」[官方原文｜label]
- 用途（官方表述）：「帮助您从不同维度对具有相同特征的云资源进行分类、搜索和聚合，提高资源管理效率」。[官方｜label]
- 编辑入口两处：实例页面**标签**列悬停图标 → 编辑；或实例 **基本信息** 页签 → **标签** 单元格图标。编辑页可增加、删除和修改标签。
- 过滤：实例页面单击**标签筛选**选择标签键，或在搜索框输入标签键搜索。
- **对权限的影响**：[文档未说明]（`label` 页未提标签鉴权 / 标签条件键；RAM 页的产品级条件关键字只有 `apig:GatewayId`、`apig:NetworkType`，**没有标签类条件键**，见 13.4）。
- **对账单/分账的影响**：[文档未说明]（`label` 页未提分账标签、成本分摊）。
- 相关 OpenAPI：`TagResources`（资源打标）、`UntagResources`（去除资源标签）、`ListTagResources`（获取资源标签列表），均在概览页「其他」分组；三者均**无流控配额条目**（见 13.3）。[官方｜api-apig-2024-03-27-overview-ai-gateway｜api-apig-2024-03-27-quota-ai-gateway]

### 10.12 资源组管理（`resource-group`）

| 项目 | 官方口径 |
|---|---|
| 定义 | 「资源组对您拥有的云资源从**用途、权限、归属**等维度上进行分组，实现企业内部多用户、多项目的资源分级管理」 |
| 归属唯一性 | 「**一个云资源只能属于一个资源组**，云资源之间的关联关系不会因加入资源组而发生变化」 |
| 跨地域 | 「一个资源组可以包含不同地域的云资源。例如，资源组 A 中可以同时包含华北2（北京）地域和华东1（杭州）地域的实例」 |
| 🔴 对权限的影响 | 「**资源组会继承 RAM 用户（子账号）的全局权限。即如果您授权 RAM 用户管理所有的阿里云资源，那么阿里云账号（主账号）下所有的资源组也会出现在该 RAM 用户中。**」 |
| 默认归属 | 「如果您没有选择资源组，系统会自动将该资源归属到**默认资源组**」 |
| 可设置的资源 | 创建**实例**时（在产品购买页面选择资源组）、创建**域名**时（添加域名面板）、创建 **Model API** 时、创建 **Agent API** 时 |
| 管理入口 | 增加/删除/修改/查看资源组参见 RAM 侧「管理资源组」文档 |

[官方｜resource-group]

- 🟠 **权限设计要点**：资源组是分组视图而非权限边界——**全局授权的 RAM 用户能看到所有资源组**。[推断] 由「资源组会继承 RAM 用户的全局权限」推出「资源组本身不构成隔离边界，多项目隔离需在 RAM 策略侧做限制」；raw 未给出对应的资源组级 RAM 策略示例 → 示例[文档未说明]。
- **对账单的影响**：[文档未说明]（`resource-group` 页未提账单按资源组拆分）。
- 原文瑕疵：「创建 Agent API 时设置」的步骤 3 写作「在**创建Model API**面板中，选择该API归属**资源组**」——面板名与上文操作（创建 Agent API）不一致。[原文如此｜resource-group]
- 相关 OpenAPI：`ChangeResourceGroup`（资源转组），流控配额 `30/1(s)`，RAM 资源类型为「全部资源」（不支持资源级授权）。[官方｜api-apig-2024-03-27-overview-ai-gateway｜api-apig-2024-03-27-quota-ai-gateway｜api-apig-2024-03-27-ram-ai-gateway]

### §10 溯源

- `ai-observable` — Model API 可观测（2572 B）：10.1 全景表、10.2 全部 11 项指标定义与秒/15秒/分钟粒度、大盘名 `apig-ai-api-dashboard`、统计与日志页签位置、SLS 依赖关系、限流/缓存/联网搜索策略异常日志说明。
- `configure-ai-log-policy` — 配置 AI 日志策略（16380 B）：10.8 全节——协议类型能力矩阵、预定义基础字段的协议/场景边界、Path 级配置粒度、4 类基础字段与 7 个默认开启的系统内置字段、`ai_log` 落盘位置与 answer/question 抽取规则、GJSON 语法、三条路径 × 流式/非流式的 JSON PATH 差异表、15 个内置模板清单、单模板 >200 可选字段、自定义字段 4 参数。
- `enable-gateway-log-delivery` — 开启网关日志投递（10210 B）：10.1 计费口径、10.4 全部（SLS、两种入口、默认 Project 命名格式与站点差异、Nginx Ingress 兼容格式开关）、10.6 的 27 字段字典 + 12 个 `ai_log` 子字段、10.7 的 23 个 `Response_Flag` 与 `NC` 四步排查（含 NAT/SNAT 硬约束）。
- `enable-mcp-service-log-delivery` — 开启 MCP 服务日志投递（9425 B）：10.5 全节（实例级开启状态、`HTTP转MCP` 标签限制、同 Project 不同 Logstore、两种日志的开启方式差异）；10.6/10.7 的字段表与 Response_Flag 章节经 SHA256 比对与网关页完全相同，故只写一份并双标 slug。
- `enable-gateway-link-tracing` — 开启网关链路追踪（2045 B）：10.10 全节（Tracing Analysis + Skywalking、前提需先开通、两种开启入口、三个配置项、AI 网关自身不收费但 Tracing Analysis 按量收费）。
- `view-gateway-monitoring-data` — 查看网关监控数据（3186 B）：10.1 全景、10.3 全节（三项前提、全局看板 11 项指标、灰度对比看板 4 项指标、默认最近 1 小时、Serverless 不支持资源监控、7 项资源指标、多核 CPU 聚合与「压测不到 100% 属正常行为」、业务监控大盘免费 vs 云监控企业版收费边界、告警入口）。
- `request-response-capture-1` — API网关请求/响应采集（Body最大5KB/日志字段与版本要求）（5690 B）：10.9 全节的所有硬限制（网关级生效、四项独立开关、云原生 API 网关 ≥2.1.18 / AI 网关 ≥2.1.20、Serverless 不支持、开启校验版本而关闭不校验、6 项默认值、5 KB 默认与 0/负值兜底、全托管 5 KB / 非全托管 200 KB、截断行为、需先配访问日志投递、4 个落盘字段、按需出现、敏感数据与内容类型限制）。
- `label` — 实例标签管理（1975 B）：10.11 全节（20 个标签上限、ACS 前缀保留、标签键值结构、两处编辑入口、标签筛选）。
- `resource-group` — 资源组管理（2818 B）：10.12 全节（一资源一资源组、跨地域、继承 RAM 全局权限、默认资源组、四类资源的设置时机）。

**本章查无**（翻过但 raw 确实没写的高价值问题）：
1. **SLS 侧的具体计费单价与量级估算**——多处只说「SLS 按使用量收费」并外链 SLS 计费文档，raw 内无任何单价，SA 无法据此估日志成本。
2. **日志/监控数据的保留时长**——SLS Logstore 默认保存天数、是否可调、AI 网关侧是否有默认 TTL：全部[文档未说明]。
3. **Body 采集的 Content-Type 范围**——只说「受内容类型限制」，未列具体类型；SSE 流式响应体、multipart、已压缩响应能否采集均无答案。
4. **「全托管实例」与「非全托管实例」的定义及与售卖形态（专享/Serverless）的映射**——200 KB 上限到底适用哪种形态，无法从 raw 判定。
5. **链路追踪采样率的取值范围、默认值、步长，以及开启后的性能开销**——全部[文档未说明]。
6. **链路追踪协议可选值枚举**（是否支持 Jaeger/Zipkin/OpenTelemetry）——[文档未说明]。
7. **标签是否可用于 RAM 条件鉴权与分账**——`label` 页与 RAM 页均未提供标签类条件关键字。
8. **资源组级最小权限策略示例**——`resource-group` 页只给 RAM 通用文档外链。
9. **AI 请求日志的字段数量上限 / 自定义字段个数上限 / 单条日志大小上限**——`configure-ai-log-policy` 未给任何上限数字（「超过 200 个」是模板可选字段数，不是配额）。
10. **Agent API 可观测、MCP 服务可观测的指标清单**——不在 W7 指派页；W7 只能确认 MCP 日志入口与 Logstore 归属。
11. **`apig-ai-api-dashboard` 是否可自定义/导出，以及能否用 OpenAPI 拉指标**——仅知有 `GetDashboard`（获取监控日志大盘接口）与 `GetTraceConfig` 两个监控管理 Action，其入参/返回结构在 raw 内[文档未说明]。
12. **告警规则的可选指标项与阈值建议**——`view-gateway-monitoring-data` 只给了创建入口。
13. **云监控企业版的价格**——只说「根据您的使用量收费」并外链计费概述。
14. **`observation-analysis` 页未被任何 worker 认领**（W7 在 raw 目录发现该文件，但 7 个 shard TSV 中均无此行）；按契约 §0.1「只读指派快照」，W7 未读取该页，因此「观测分析」总览级内容存在覆盖缺口，请主控裁决归属。

---

## §11 开发者门户与开放平台

### 11.1 门户是什么、给谁用（`create-portal`）

> 门户（Portal）是**开放平台中面向外部开发者的自助服务站点**。管理员可以在控制台创建和配置门户，将 API 产品发布到门户；开发者访问门户后注册账号，即可浏览和订阅已发布的 API 产品。**每个门户拥有独立的配置和 API 产品集合。**
> [官方原文｜create-portal]

官方一句话定位（`create-portal` 开头）：「面向外部开发者搭建 API 自助服务站点，集中展示和管理 API 产品、审批开发者注册、管理订阅关系。」[官方原文｜create-portal]

**角色划分**：管理员（在开放平台管理页面创建/配置门户、发布 API 产品、审批注册与订阅）↔ 外部开发者（在门户注册、浏览、订阅、拿 API Key）。[官方｜create-portal｜developer-guide]

**门户能实现的三个目标（照抄）**：
1. 展示已发布的 API 产品，供开发者浏览和检索。
2. 管理开发者注册和订阅，支持自动审批或手动审批。
3. **提供 AI API 使用入口（HiChat），方便开发者快速调用 AI 能力。**
[官方｜create-portal]

（HiChat 本体归 W5；W7 只记录门户把它作为使用入口这一事实。）

**创建门户的参数极少**：只有 **名称**（「门户的唯一标识，用于区分不同的门户。例如 `ai-platform`」）与 **描述**（「简要描述门户的用途和定位，以便管理员快速识别」）。→ 创建时不涉及域名、规格、地域。[官方｜create-portal]

**门户详情页四个配置模块**：

| 模块 | 能做什么 |
|---|---|
| 门户概览 | 查看门户的基础信息，包括名称、描述和相关统计数据 |
| 已发布的 API 产品 | 管理当前门户中已发布的 API 产品，包括发布新产品到门户和从门户下架已有产品 |
| 开发者管理 | 查看在该门户注册的开发者列表；审批开发者的注册申请；查看开发者的 API 产品订阅情况 |
| 安全设置 | 配置审批策略：**开发者自动审批**（开启后开发者注册账号时审批自动通过；关闭后需管理员在开发者管理页面手动审批）、**订阅自动审批**（开启后开发者订阅 API 产品时审批自动通过；关闭后需管理员手动审批） |

[官方｜create-portal]

🔴 **删除门户的后果（原文「警告」）**：
> 门户删除后，该门户上注册的开发者账号将被删除，已发布的 API 产品均会下架。请谨慎操作。
> [官方原文｜create-portal]

**后续操作**：创建门户后需 ① 将 API 产品发布到门户；② 在开发者管理中处理注册申请和审批订阅请求。[官方｜create-portal]

### 11.2 门户部署形态（`deployment-portal`）

门户是**自部署**的：官方给出镜像，客户自己跑在 SAE / ACK / 本地 Docker 上，不是 AI 网关的内置托管组件。官方定位：「开放平台面向外部开发者的自助服务站点。本文介绍如何在阿里云 SAE、ACK 以及本地 Docker 环境中部署门户服务，快速搭建**生产就绪或开发测试用**的开发者门户。」[官方｜deployment-portal]

| 部署方式 | 适用场景 | 说明 |
|---|---|---|
| 阿里云 SAE | **生产环境推荐** | Serverless 应用引擎，免运维、自动弹性伸缩 |
| 阿里云 ACK | 大规模生产环境 | 容器服务 Kubernetes 版，适合复杂编排需求 |
| 本地 Docker | 开发测试 | 本地快速验证，**不适用于生产** |

[官方｜deployment-portal]

**SAE 部署前提**：① 已开通阿里云 SAE 服务，并创建命名空间；② 已在开放平台控制台创建门户实例，并获取**门户 ID**。「门户服务的镜像地址为固定地址，部署时直接填写即可。」SAE 方式的官方优势表述：「具备免服务器运维、自动弹性伸缩、按需付费等优势。」[官方｜deployment-portal]

**镜像地址**：`opensource-registry.cn-hangzhou.cr.aliyuncs.com/higress-group/himarket-portal:latest`（SAE 章节）[官方｜deployment-portal]

🔴 **[官方矛盾] 同一页给出两个不同的门户镜像地址**：
- SAE 章节（且前文明称镜像地址为「**固定地址**」）：「**镜像地址**：填写 `opensource-registry.cn-hangzhou.cr.aliyuncs.com/higress-group/himarket-portal:latest`」
- 本地 Docker 章节的 `docker run` 命令末行：「`registry.cn-hangzhou.aliyuncs.com/acs/alibaba-cloud-portal:latest`」

两者仓库路径完全不同（`opensource-registry…/higress-group/himarket-portal` vs `registry…/acs/alibaba-cloud-portal`），页面未说明二者关系、是否为同一镜像的不同别名、生产应使用哪个。**不裁决，交主控。**

**实例规格建议（SAE，「按需设置」）**：

| 参数 | 官方建议值 |
|---|---|
| vCPU | 建议 **0.5 核或以上** |
| 内存 | 建议 **1 GiB 或以上** |
| 实例数 | 根据实际访问量配置，**最小 1 实例** |

[官方｜deployment-portal]

**必需环境变量（核心配置）**：

| 环境变量 | 说明 | 示例值 |
|---|---|---|
| `POP_GATEWAY_URL` | 门户服务访问 APIG OpenAPI 的 Endpoint。<br>公网：`https://apig.{regionId}.aliyuncs.com`<br>内网：`https://apig-vpc.{regionId}.aliyuncs.com` | `https://apig.cn-hangzhou.aliyuncs.com` |
| `POP_REGION_ID` | 门户服务所在的地域 ID | `cn-hangzhou` |
| `PORTAL_ID` | 在开放平台控制台创建的门户 ID | `portal-xxx` |

[官方｜deployment-portal]

🟠 `POP_GATEWAY_URL` 的公网/内网两种格式与 §13.2 服务接入点表的域名格式**完全一致**，可与「25 个地域中 19 个有 VPC 接入点」的覆盖结论直接对照。[推断] 由 `deployment-portal` 的 Endpoint 说明 + `api-apig-2024-03-27-endpoint-ai-gateway` 的地域表推出「门户若走内网 Endpoint 需确认所在地域有 `apig-vpc.{regionId}.aliyuncs.com`」；raw 未明文提示这一交叉约束。

**ACK 部署要点**：① 准备含 Deployment、Service 等资源的 K8s YAML；② 用 **ConfigMap** 存环境变量（`POP_GATEWAY_URL`、`POP_REGION_ID`、`PORTAL_ID` 等）；③ 用 **Secret** 存 `ALIYUN_ACCESS_KEY_ID` 和 `ALIYUN_ACCESS_KEY_SECRET`；④ 配置接入方式，推荐 API 网关，也可 Ingress 或 SLB 直接暴露。ACK 接入建议与 SAE 相同：「同样推荐使用阿里云 API 网关作为统一接入层」，创建**容器类型的服务** + HTTP API + 路由规则。[官方｜deployment-portal]

**本地 Docker 运行命令**（代码块语言标记已从 `HELPCODEESCAPE-bash` 修复为 bash）：

```bash
docker run -d \
  --name portal \
  -p 8000:8000 \
  -e POP_GATEWAY_URL=https://apig.cn-hangzhou.aliyuncs.com \
  -e POP_REGION_ID=cn-hangzhou \
  -e PORTAL_ID=portal-xxx \
  -e ALIYUN_ACCESS_KEY_ID=LTAxxx \
  -e ALIYUN_ACCESS_KEY_SECRET=3f98xxx \
  registry.cn-hangzhou.aliyuncs.com/acs/alibaba-cloud-portal:latest
```
运行后访问 `http://localhost:8000` 即可访问门户，端口可按需修改。[官方｜deployment-portal]

### 11.3 门户服务的认证与 RAM 最小权限（`deployment-portal`）

「门户服务需要访问阿里云 OpenAPI，需配置认证凭证。SAE 支持 **RRSA OIDC** 和 **AccessKey** 两种方式，**推荐优先使用 RRSA OIDC，安全性更高**。」[官方｜deployment-portal]

| 方式 | 适用部署形态 | 关键点 |
|---|---|---|
| **方式一：RRSA OIDC（推荐）** | **仅 SAE 支持** | 在配置应用时启用 RRSA OIDC 功能。「此方式无需在环境变量中配置 AK/SK，通过 OIDC 令牌自动获取临时凭证，安全性更高。」配置参考 SAE「设置身份认证服务功能（**邀测**）」。🔴「**RRSA OIDC 为 SAE 特有功能，ACK 环境不支持此方式。**」 |
| **方式二：AccessKey** | SAE（暂无法用 RRSA OIDC 时）/ ACK / 本地 Docker | 环境变量 `ALIYUN_ACCESS_KEY_ID`（示例 `LTAxxx`）、`ALIYUN_ACCESS_KEY_SECRET`（示例 `3f98xxx`）。原文「重要」：**使用子账号 AK/SK，避免使用主账号**；该子账号需具备下述 RAM 权限策略 |

[官方原文｜deployment-portal]

🔴 **门户服务的最小 RAM 权限（官方给出的组合）**：
- 系统权限策略：`AliyunAPIGReadOnlyAccess`——「阿里云云原生 API 网关资源的只读权限」
- 自定义权限策略（「由于门户服务需要管理消费者（Consumer），需要额外添加以下自定义策略」）：

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apig:*Consumer*"
      ],
      "Resource": "*"
    }
  ]
}
```
[官方原文｜deployment-portal]

🟠 **SA 可直接引用的最小权限样板**：门户 = 「APIG 全量只读 + Consumer 通配写」。[推断] 由 `deployment-portal` 的策略 JSON + `api-apig-2024-03-27-ram-ai-gateway` 的 140 个 Action 名推出：`apig:*Consumer*` 可覆盖消费者管理类 Action（`CreateConsumer`/`UpdateConsumer`/`DeleteConsumer`/`GetConsumer`/`ListConsumers`/`Create|Update|Delete|Get|Query|Remove|BatchDelete ConsumerAuthorizationRule(s)`/`ListConsumerAuthorizationRules`/`Create|Get|Update|Delete ConsumerGroup`/`ListConsumerGroups`/`ListConsumerGroupConsumers`/`BatchAdd|BatchRemoveConsumerGroupConsumers`/`ListConsumerQuotaRules`）；raw 未明文说明该通配符的匹配范围。

🔴 **`RRSA OIDC` 依赖的 SAE「设置身份认证服务功能」处于「邀测」状态**——按契约 §8 的时效性要求记录：截至快照抓取日（2026-09-21），该 SAE 功能在官方链接文字中标注为**邀测**，raw 未说明邀测何时结束、GA 时间、以及邀测期间是否有名额/地域限制。生产选型时若客户不在邀测范围，只能退回 AccessKey 方式。[官方｜deployment-portal]

🔴 **交叉说明（按主控指派注明）**：本页的 RRSA OIDC 是**门户服务自身访问阿里云 OpenAPI 的云资源身份认证**，与「开发者用企业 SSO 登录门户」的 **门户 OIDC 登录**是两件不同的事。后者的详细配置页 `configure-oidc-login-for-portal` 归 **W4**，W7 未读取该页，因此 §11 只写门户侧的部署与定位。W7 侧能从 `developer-guide` 确认的门户 OIDC 登录**行为**见 11.5.1。[官方｜deployment-portal｜developer-guide]

### 11.4 门户的访问接入（`deployment-portal`）

| 方式 | 官方定位 | 关键配置 |
|---|---|---|
| **方式一：通过 API 网关访问（推荐）** | 「推荐使用阿里云 API 网关作为门户服务的统一接入层，可获得**流量控制、安全防护、监控告警、日志审计**等能力」 | ① 登录 API 网关控制台，开通 API 网关服务；② 创建 **SAE 类型的服务**，选择已部署的门户应用作为后端；③ 创建 **HTTP API**，配置路由规则（例如将路径 `/*` 转发到门户服务的 **`8000` 端口**）；④ 通过 API 网关生成的接入点地址访问门户 |
| **方式二：通过负载均衡访问** | 「如暂不需要 API 网关的高级功能，也可通过负载均衡直接暴露服务」 | SAE 应用详情页 → **添加访问方式** → 负载均衡类型 **NLB 或 CLB 均可** → 监听配置：**协议 TCP**、**容器端口 `8000`（门户服务默认端口）** → 保存后系统分配访问地址 |

[官方｜deployment-portal]

- 🔴 **`8000` 是门户服务的默认监听端口**（三处一致：API 网关路由示例、SLB 容器端口、Docker `-p 8000:8000`）。[官方｜deployment-portal]
- **验证部署三步**：① 在 SAE 控制台查看应用实例状态，确保运行正常；② 通过配置的访问地址访问门户首页，确认页面加载正常；③ 测试开发者注册、登录、浏览 API 产品等核心功能。[官方｜deployment-portal]

🟠 **连带开通/计费清单（门户方案的「账单 ≠ 全成本」）**：门户本身在 raw 中未标价，但落地必然连带 SAE（或 ACK）应用资源、API 网关或 NLB/CLB 接入层，以及门户调用的 APIG OpenAPI。这些各自的计费口径[文档未说明]（`deployment-portal` 全页无任何价格或计费数字）。

### 11.5 开放平台开发者操作指南（`developer-guide`）

**开放平台是什么、面向谁、能做什么**：「通过开放平台，开发者可以**浏览和订阅 API 产品进行接口调用**。本文介绍如何注册开发者账号、浏览和订阅 API 产品，以及创建和管理消费者凭证的完整操作流程。」→ 面向**外部开发者**（API 消费方），能力链 = 注册 → 浏览 → 订阅 → 拿凭证 → 调用。[官方原文｜developer-guide]

#### 11.5.1 注册：两种方式与审批差异

| 注册方式 | 流程 | 审批行为 |
|---|---|---|
| **账号密码注册** | 门户首页登录区点击**注册** → 填写注册信息（用户名和密码）→ 确认无误后点击**注册**提交申请 | 取决于门户审批配置：**自动审批模式**——注册申请提交后立即生效，可直接使用账号登录门户；**手动审批模式**——注册申请需等待管理员在后台审批通过后方可登录使用 |
| **OIDC 登录注册**（如企业 SSO） | 门户首页登录区点击 OIDC 登录按钮（如**阿里云账号登录**）→ 跳转至企业身份提供商（IdP）的登录页面 → 在企业 IdP 中完成身份验证 → 授权完成后自动跳转回开放平台，**系统自动创建开发者账号并完成登录** | 🔴「使用 OIDC 方式登录的开发者**无需设置密码，首次登录后账号状态即为已审批，可直接使用**」；「使用 OIDC 登录的用户**默认自动完成审批，无需等待管理员审核**」 |

[官方｜developer-guide]

前提：「若管理员已配置 OIDC 登录（如企业 SSO），可直接使用企业账号登录」——即 OIDC 登录方式需管理员侧先配置。[官方｜developer-guide]

🟠 **门户 OIDC 登录的实质安全含义**：一旦管理员配好 OIDC，**门户的「开发者自动审批」开关对 OIDC 用户不再起作用**——IdP 侧放进来的人首次登录即为已审批状态。SA 做方案时必须提示客户：门户的准入控制点会前移到企业 IdP。[推断] 由「OIDC 首次登录后账号状态即为已审批」+「安全设置中的开发者自动审批开关」两条官方事实推出；raw 未明文讨论二者叠加时的优先级。OIDC 的具体配置（IdP、client_id、回调地址等）见 W4 `configure-oidc-login-for-portal`。

#### 11.5.2 浏览与订阅

- 浏览：① 用注册的开发者账号登录开发者门户；② 在导航栏进入 **模型**、**MCP**、**智能体** 等产品页面；③ 浏览产品列表，查看产品名称、功能描述和所属类别，通过筛选和搜索快速定位目标产品；④ 点击产品卡片进入详情页，查看产品功能介绍、使用指南和调用示例等信息。[官方｜developer-guide]
  🟠 门户的一级产品分类是**模型 / MCP / 智能体**三类，与 AI 网关的 Model API / MCP / Agent API 三条产品线对应。
- 🔴 **订阅前置**：「在订阅 API 产品前，**需先创建消费者并获取对应的调用凭证**。」[官方原文｜developer-guide]
- 订阅流程：① 产品详情页点击**订阅**发起订阅申请；② **从消费者列表中选择要用于该产品调用的消费者身份**（「每个开发者注册成功后，系统会自动创建一个默认消费者。如需创建更多消费者，请参见本文档**管理消费者凭证**章节」）；③ 点击**确定订阅**提交申请。[官方｜developer-guide]
- 订阅生效同样受审批配置影响：**自动审批**——订阅申请立即生效，可通过消费者凭证访问 API 产品；**手动审批**——需等待管理员审批通过后方可调用。[官方｜developer-guide]

#### 11.5.3 消费者凭证管理

| 事实 | 官方原文/口径 |
|---|---|
| 凭证形态 | 「开放平台使用**消费者**作为 API 调用的身份凭证」；消费者创建成功后「系统会**自动生成 API Key** 作为调用凭证」 |
| 🔴 默认消费者 | 「**每个开发者注册成功后，系统会自动为其创建一个默认消费者**」 |
| 新增消费者 | 登录门户 → 右上角头像展开菜单 → **消费者管理** → **新增消费者**；字段：**消费者名称**（「用于标识该消费者的名称，建议按照用途命名（例如 `my-app-prod`），**必填**」）、**描述**（「简要说明该消费者的用途（例如用于生产环境调用），**选填**」） |
| 查看/使用 | 消费者列表 → **查看凭证** → 复制 API Key，「在 API 调用时将其**添加到请求头中**进行身份认证」 |
| 🔴 吊销 | 「如需废弃该凭证，可点击**删除**按钮进行删除，**删除后该凭证立即失效**」 |

[官方｜developer-guide]

🟠 **与 AI 网关消费者体系的关系**：[推断] 由 `developer-guide` 的消费者凭证机制 + `deployment-portal` 要求的 `apig:*Consumer*` 写权限推出「门户是通过 APIG OpenAPI 在网关侧创建/管理 Consumer 的」；raw 未明文说明门户消费者与网关 Consumer 是同一实体还是门户侧独立对象 → [文档未说明]，消费者全生命周期归 W4。

### §11 溯源

- `create-portal` — 创建开发者门户（2971 B）：11.1 全节（门户定义与「每个门户拥有独立的配置和 API 产品集合」、管理员/开发者双角色、三个目标含 HiChat 入口、创建参数仅名称+描述、四个配置模块、两个自动审批开关、删除门户的警告级后果、后续操作）。
- `deployment-portal` — 部署开发者门户服务（8008 B）：11.2 全节（三种部署方式对比表、SAE 两项前提、固定镜像地址、0.5 核/1 GiB/最小 1 实例建议、三个核心环境变量含公网与内网 Endpoint 格式、ACK 的 ConfigMap/Secret 分工与接入建议、Docker 完整命令）；11.3 全节（RRSA OIDC vs AccessKey 二选一、RRSA 仅 SAE 且 ACK 不支持、SAE 身份认证服务功能处于邀测、`AliyunAPIGReadOnlyAccess` + `apig:*Consumer*` 最小权限样板、子账号 AK/SK 要求）；11.4 全节（API 网关接入的四项能力与四步配置、NLB/CLB 接入、TCP 协议与 8000 默认端口、`/*` 路由示例、验证三步）；11.3 末尾的 OIDC 概念区分。
- `developer-guide` — 开放平台开发者操作指南（4399 B）：11.5 全节（开放平台定位与面向对象、账号密码 vs OIDC 两种注册流程、OIDC 免密且首次登录即已审批、自动/手动审批对注册与订阅的双重作用、模型/MCP/智能体三类产品导航、订阅前必须先有消费者、默认消费者自动创建、消费者名称必填与命名建议、API Key 自动生成与放请求头、删除凭证立即失效）。

**本章查无**：
1. **门户自身的计费**——门户是否收费、SAE/ACK/NLB/CLB/API 网关各接入层的单价与量级：`deployment-portal` 与 `create-portal` 全页无任何价格数字，SA 报门户方案时无法给出量级。
2. **门户 OIDC 登录的配置方法**（IdP 类型、client_id/secret、回调地址、支持的 scope、是否支持阿里云账号以外的 IdP）——归 W4 `configure-oidc-login-for-portal`，W7 未读；本章仅有开发者侧的行为描述。
3. **`apig:*Consumer*` 之外门户是否还需要其他 Action**——例如发布/查询 API 产品是否需要 `apig:*HttpApi*` 权限；页面只用 `AliyunAPIGReadOnlyAccess` 兜底，未拆解到 Action 级。
4. **RRSA OIDC「邀测」的时间边界**——何时结束邀测、GA 时间、地域/名额限制、邀测结束后 AccessKey 方式是否保留：全部[文档未说明]。
5. **两个镜像地址的关系**（见 11.2 [官方矛盾]）以及镜像版本策略——`latest` 标签是否有版本固定方式、是否有 changelog：[文档未说明]。
6. **门户的规格容量**——0.5 核/1 GiB 能支撑多少开发者并发/多少 API 产品：无任何压测数据。
7. **门户的高可用与多副本**——只说「实例数根据实际访问量配置，最小 1 实例」，未给多可用区、健康检查、滚动升级建议。
8. **门户自定义域名与 HTTPS 证书**——门户对外暴露时的域名/证书/备案要求：[文档未说明]（只给接入方式，未提证书；API 网关路由示例甚至是路径转发，未涉 HTTPS）。
9. **门户与 API 产品的绑定关系**——「将 API 产品发布到门户」的具体字段、一个 API 产品能否发布到多个门户、下架对已订阅开发者的影响：[文档未说明]（API 产品与分类归 W3）。
10. **开发者账号的生命周期**——能否禁用/删除单个开发者、密码重置、账号数量上限：[文档未说明]（只写了删除整个门户会连带删除开发者账号）。
11. **门户侧 API Key 的轮转机制**——`proxy-dify…` 页提到 AI 网关有「API-KEY 自动轮转」能力，但门户生成的 API Key 是否支持轮转、轮转周期：[文档未说明]。
12. **门户的审计日志**——管理员审批操作、开发者订阅操作是否有审计留痕：[文档未说明]。
13. **门户的地域属性**——创建门户只有名称+描述，门户是否有地域、跨地域门户如何工作：[文档未说明]。

---
## §12 实践教程与集成配方（7 张配方卡）

统一结构：**目标场景 ｜ 前置条件 ｜ 关键配置步骤（只留有决策含义的）｜ 涉及的能力/插件 ｜ 踩坑点与限制 ｜ 对 SA 的可复用价值 ｜ 来源 slug**

### 配方 1 — 接入 Google Vertex AI

| 维度 | 内容 |
|---|---|
| **目标场景** | 「通过阿里云 AI 网关快速接入 Google Vertex AI，实现对 Gemini 等模型的统一管理和调用」。官方给出 **6 个场景**：① GCP Service Account 模式接入；② Vertex AI Express Mode 接入；③ Vertex AI REST API 接入（原生协议，「适用于 Imagen、Veo 等非 Gemini 系列模型」）；④ Google GenAI SDK 模式接入（**官方标注不推荐**）；⑤ 多模态理解场景（图片/视频）；⑥ 图片生成场景（生成/编辑/变体）。四项收益（照抄）：**统一接入**（通过 OpenAI 兼容协议访问 Vertex AI，无需适配原生 API）、**灵活鉴权**（支持 GCP Service Account 和 Vertex AI Express Mode 两种鉴权方式）、**协议转换**（支持 AI 网关自动协议转换或使用 Vertex AI 原生兼容端点）、**高可用保障**（结合 AI 网关的 Fallback 能力实现跨供应商容灾） |
| **前置条件** | ① **已创建专有网络 VPC 并绑定公网 NAT 网关**；② 已创建 AI 网关实例；③ 已获取 Google Cloud 项目的访问凭证（**Service Account Key 或 Vertex AI Express Mode API Key**）。场景一另需：在 Google Cloud Console 创建 Service Account 并下载 JSON 密钥，为其分配 **Vertex AI User 角色（或更高权限）** |
| **关键配置步骤（只留有决策含义的）** | **AI 服务（场景一 SA 模式）**：服务来源=**AI 服务**；服务名称如 `vertex-ai`；大模型供应商=**Vertex AI**；鉴权方式=**GCP Service Account**；**GCP Service Account KEY**=粘贴完整的 SA JSON 密钥内容；**`vertexLocation`**=Vertex AI 服务区域，**默认值为 `global`**，可选择其他区域如 `us-central1`、`europe-west4` 等；**`vertexProjectId`**=GCP 项目 ID（**只读**，「系统会自动从 JSON 密钥中解析 `project_id` 字段」）。<br>**OpenAI 协议兼容方式（二选一，决策核心）**：**AI 网关转换**——「通过 AI 网关在请求和响应阶段进行协议转换。网关会将 OpenAI 格式的请求转换为 Vertex AI 原生格式，并将响应转换回 OpenAI 格式」，适用「需要使用 Vertex AI 原生功能（如特定安全设置）的场景」；**Vertex AI 原生兼容端点**——「使用 Vertex AI 提供的 OpenAI 兼容 Chat Completions 端点，直接接收 OpenAI 格式请求」，适用「如需要获取 Vertex AI 独有的 `extra_content` 等字段，选用此模式」。<br>**Model API（场景一/二）**：域名建议配置自定义域名（**使用默认环境域名存在限流**）；Base Path 如 `/gemini`；模型类型=**文本生成**；协议=**OpenAI 兼容**；路由配置**需勾选 `/v1/chat/completions`**；**AI 请求观测=开启**；服务模型=单模型服务；服务列表选上一步的 Vertex AI 服务，模型名称选**透传**或指定具体模型（如 `gemini-2.0-flash`）。<br>**场景二 Express Mode**：AI 服务鉴权方式=**Vertex AI Express Mode**，只需填 **API-KEY**（从 Google AI Studio 获取）；「Express Mode 配置方式与其他大模型供应商（如 OpenAI、Claude）类似，只需填写 API Key 即可」。<br>**场景三 REST API**：AI 服务的**模型协议必须选「原生协议」**（「选择「原生协议」后，将不会显示「OpenAI 协议兼容方式」选项，因为此模式不进行协议转换」）；Model API 的**协议选 `VertexAI`**，网关自动配置两条内置路由：`/{api-version}/publishers/{publisher}/models/{model}:{action}`（**Express Mode 使用的路径格式**）、`/{api-version}/projects/{project}/locations/{location}/publishers/{publisher}/models/{model}:{action}`（**Service Account 模式使用的路径格式**）；使用场景可选文本生成/图片生成/视频生成，官方注明「此处仅是控制台的分类辅助，**混用也不会有问题**」。<br>**场景四 SDK 模式**：因 SDK 自行完成鉴权，需创建 **DNS 域名**类型服务直连 Vertex AI；服务地址二选一——`aiplatform.googleapis.com:443`（**全局端点，适用于 Express Mode**）或 `{location}-aiplatform.googleapis.com:443`（**区域端点，适用于 Service Account 模式**，如 `us-central1-aiplatform.googleapis.com:443`，需根据 GCP 项目所在区域填写）；**TLS 模式选「单向」**；**SNI 默认与填入的域名一致，无需手动修改**；SDK 侧 `vertexai=True`（「目前仅支持 vertexai=True」）、`api_key`（Express Mode 的 Key，或留空使用默认 Service Account 凭证）、`base_url` = `https://{域名}{Base Path}`；SA 模式可用环境变量 `GOOGLE_APPLICATION_CREDENTIALS` 指向密钥文件 |
| **涉及的能力/插件** | AI 服务（Vertex AI 供应商 + 两种鉴权）、协议转换（AI 网关转换 / Vertex AI 原生兼容端点）、Model API 单模型服务与**多模型服务（按模型名称）**、Fallback（跨供应商容灾）、AI 请求观测、DNS 域名服务、单向 TLS/SNI、**引用凭据（KMS）**、IP 白名单、限流、观测分析 > 日志中心 |
| **踩坑点与限制** | 🔴 **原生兼容端点模式下模型名必须加 Provider 前缀 `google/`**：「**使用「Vertex AI 原生兼容端点」模式时**，请求体中的 `model` 参数需要添加 Provider 前缀 `google/`。例如：原本使用 `gemini-3-flash-preview` 需要改为 `google/gemini-3-flash-preview`」。<br>🔴 **图片生成/编辑/变体在 GCP SA 模式下必须选「AI 网关转换」**：「在 GCP Service Account 模式下进行图片生成/编辑/变体时，**OpenAI 协议兼容方式必须选择「AI 网关转换」**。这是因为 Vertex AI 原生兼容端点**目前仅支持文本对话接口（Chat Completions）**，而 AI 网关的协议转换支持图片相关接口的转换」。<br>🔴 **OpenAI SDK 对 `/v1/images/edits`、`/v1/images/variations` 的 `image_url` 写法不支持**：「OpenAI SDK 对 `image_url` 写法不支持；如需 `image_url` 请使用 HTTP JSON 请求（**SDK 的 multipart 文件上传可正常使用**）」；`/v1/images/generations`「不涉及（该接口通常无需传 `image_url`）」。SDK 推荐调用方式分别为 `client.images.generate()`（JSON）、`client.images.edit(image=<file>)`（multipart）、`client.images.create_variation(image=<file>)`（multipart）。<br>🔴 **场景四官方标注不推荐**：「**不推荐使用**：此模式下网关仅作为透明代理，**无法使用 AI 服务中配置的鉴权信息**，功能受限」；原因是「GenAI SDK 的鉴权方式是客户端先向 Google 认证服务器发起 OAuth 2.0 认证请求，再进行模型推理 API 调用」；「由于鉴权在客户端完成，网关无法进行鉴权配置代理」。仅能获得请求观测与计量（日志中心可见请求路径、响应状态码、响应时间、Token 用量——「如果响应中包含」）。<br>🔴 **视频理解复用 `image_url` 类型**：「由于 OpenAI 的接口规范仅定义了 `image_url` 类型，但这不妨碍我们传入视频内容。**AI 网关会自动完成兼容性转换**，将视频内容正确传递给 Vertex AI」。<br>🔴 **调试面板只打 `/v1/chat/completions`**：「在模型返回页签下，使用的是 `/v1/chat/completions` 对话接口，如需使用其他接口，您可选择 **CURL 命令** 或 **原始输出** 的方式通过 curl、SDK 调试」。<br>🔴 **默认环境域名存在限流**（全页 4 处重复「建议配置自定义域名（使用默认环境域名存在限流）」），但**限流阈值 raw 未给任何数字**。<br>**其他提示**：「如果 JSON 密钥格式不正确或缺少必要字段，系统会显示相应的错误提示」；「`vertexProjectId` 为只读字段，前端会自动解析 JSON 密钥中的 `project_id`」；「Express Mode API Key 可能有使用限制，详情请参考 Google 官方文档」；密钥文件「包含敏感信息，请妥善保管」。<br>**支持的媒体格式（照抄）**：图片 `image/png, image/jpeg, image/webp, image/heic, image/heif`；视频 `video/x-flv, video/quicktime, video/mpeg, video/mpegs, video/mpg, video/mp4, video/webm, video/wmv, video/3gpp`；「不同模型的支持能力详见 Google 官方文档」。<br>**官方 FAQ 四类**：**401/403 鉴权失败**——检查 SA JSON 密钥完整性（确保包含 `private_key`、`client_email`、`token_uri` 等必要字段）、确认 SA 具有 **Vertex AI User 或更高权限**、Express Mode 确认 API Key 有效且未过期；**404 模型不存在**——确认模型名称正确、检查所选区域是否支持该模型；**JSON 解析失败**——确保粘贴完整（勿漏开头 `{` 或结尾 `}`）、可用在线 JSON 验证工具检查；**请求超时**——「检查 VPC 是否正确配置公网 NAT 网关」、「确认目标区域的网络连通性」 |
| **对 SA 的可复用价值** | ① 回答「阿里云上怎么统一管 Gemini / Imagen / Veo」——给出四种接入形态的选型判据（企业级完整功能 → SA + AI 网关转换；快速验证/轻量 → Express Mode；非 Gemini 系列 → 原生协议 REST；只想观测计量 → SDK 透明代理但功能受限且官方不推荐）。② 回答「Vertex 的图片生成能不能用 OpenAI SDK」——multipart 可以、`image_url` 只能裸 HTTP JSON。③ 回答「OpenAI 的 size 参数怎么映射到 Vertex」——14 行官方映射表（见下）。④ 回答「跨境访问 Vertex 的网络怎么准备」——**raw 只给出「VPC + 公网 NAT 网关」这一条**，详见下方🔴专门说明。⑤ 跨供应商容灾样板：Vertex AI（`gemini*`）+ 阿里云百炼（`qwen*`）多模型服务 + Fallback。⑥ 安全交付清单：KMS 引用凭据 + IP 白名单 + 限流保护（官方明示目的是「避免意外的高额费用」） |
| **来源 slug** | `access-vertex-ai-through-ai-gateway`（42868 B，924 行全读） |

🔴 **关于「跨地域/跨境网络要求」的如实说明（重要）**：主控指派中提示本页含「跨地域/跨境网络要求」的高价值弹药，但 **W7 通读全文（924 行 / 42868 B）并做了关键词检索（跨境/跨地域/海外/国际站/NAT/公网）后确认：该页没有任何关于跨境、跨地域、专线、GA/CEN、数据出境合规或链路质量/延迟的表述**。全页涉及网络的只有两处，且都是同一件事：
> 前提条件：「已创建专有网络 VPC 并绑定**公网 NAT 网关**，具体操作请参见专有网络与交换机和公网访问。」
> 常见问题-请求超时：「检查 VPC 是否正确配置**公网 NAT 网关**。」「确认目标区域的网络连通性。」
> [官方原文｜access-vertex-ai-through-ai-gateway]

因此可照抄的网络硬要求只有一条：**AI 网关所在 VPC 必须能通过公网 NAT 网关出网访问 Google 端点**（另参见 §10.7 `NC`/`cluster_not_found` 排查第 3 步「若后端服务为公网域名，需在该 VPC 中配置 NAT 网关和 SNAT 条目，否则网关无法访问公网地址」——两处口径一致，可互相印证）。至于跨境专线、GA/CEN、数据出境合规、Google 侧区域与阿里云地域的对应关系、跨境延迟量级——raw 全部[文档未说明]。**SA 对客时不得基于本页承诺跨境网络方案。**

**Vertex AI 图片尺寸参数映射表（14 行，OpenAI size → Vertex aspectRatio + imageSize，逐行照抄）**

官方说明：「由于 OpenAI 接口使用分辨率（如 `1024x1024`）而 Vertex AI 使用宽高比（aspectRatio）+ 分辨率等级（imageSize）的方式，**AI 网关会自动进行参数转换**。」
- Vertex AI 支持的宽高比（10 个）：`1:1`、`3:2`、`2:3`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`
- Vertex AI 支持的分辨率等级（3 个）：`1k`、`2k`、`4k`

| OpenAI size 参数 | Vertex AI aspectRatio | Vertex AI imageSize |
|---|---|---|
| `256x256` | 1:1 | 1k |
| `512x512` | 1:1 | 1k |
| `1024x1024` | 1:1 | 1k |
| `1792x1024` | 16:9 | 2k |
| `1024x1792` | 9:16 | 2k |
| `2048x2048` | 1:1 | 2k |
| `4096x4096` | 1:1 | 4k |
| `1536x1024` | 3:2 | 2k |
| `1024x1536` | 2:3 | 2k |
| `1024x768` | 4:3 | 1k |
| `768x1024` | 3:4 | 1k |
| `1280x1024` | 5:4 | 1k |
| `1024x1280` | 4:5 | 1k |
| `2560x1080` | 21:9 | 2k |

[官方｜access-vertex-ai-through-ai-gateway]

**Vertex AI 页出现的模型清单（raw 内明文）**

| 类别 | 模型名称 | 模型 ID | Publisher | 官方描述 |
|---|---|---|---|---|
| 图片生成 | Gemini Nano Banana Pro | `gemini-3-pro-image-preview` | google | Google 最新的图片生成模型，支持高质量图片生成 |
| 图片生成 | Gemini Nano Banana | `gemini-2.5-flash-image` | google | Google 上一代图片生成模型，支持高质量图片生成 |
| 图片生成（REST 场景示例） | Imagen 4 | `imagen-4.0-generate-preview-06-06` | google | — |
| 视频生成（REST 场景示例） | Veo 3 | `veo-3.0-generate-preview` | google | — |
| 文本生成（REST 场景示例） | Llama 4 | `llama-4-maverick-17b-128e-instruct-maas` | **meta** | — |
| 文本生成/多模态（代码示例中出现） | — | `gemini-3-flash-preview`、`gemini-2.0-flash`、`gemini-3-pro-preview` | google | — |

页面三处声明「具体支持的模型列表请参考 Google 官方文档」，即**模型清单以 Google 侧为准**，raw 未给权威全量列表。「总结」节补充：REST API 模式「代理 Vertex AI 原生 REST API，**适用于所有模型**，常见用于 **Imagen、Veo、Claude** 等非 Gemini 系列模型」。多模态理解支持的模型表述为「支持多模态理解的 Gemini 模型，如 `gemini-3-flash-preview`、`gemini-2.0-flash` 等」。[官方｜access-vertex-ai-through-ai-gateway]

**Vertex AI 服务 JSON 密钥需含字段（官方示例）**：`type`（`service_account`）、`project_id`、`private_key_id`、`private_key`、`client_email`、`token_uri`（示例值 `https://oauth2.googleapis.com/token`）。[官方｜access-vertex-ai-through-ai-gateway]

**高级配置与安全建议（照抄）**：
- 多供应商高可用：① 创建多个 AI 服务（如 Vertex AI + 阿里云百炼）；② 创建 Model API 时选择 **多模型服务（按模型名称）**；③ 配置路由规则——服务名称 `vertex-ai` 配模型名称匹配规则 `gemini*`，服务名称 `bailian` 配 `qwen*`；④ 开启 **Fallback**，选择备用服务。
- 安全配置建议三条：**凭证管理**——「建议通过引用凭据方式将 Service Account Key 或 API Key 存储在阿里云 KMS 中，避免凭证泄露风险」；**访问控制**——「配置 IP 白名单或其他访问控制策略，限制 API 访问来源」；**限流保护**——「设置合理的限流规则，**避免意外的高额费用**」。
[官方｜access-vertex-ai-through-ai-gateway]

### 配方 2 — 接入 DeepSeek 模型

| 维度 | 内容 |
|---|---|
| **目标场景** | 「基于三种 AI 模型接入场景，介绍如何通过 AI 网关快速实现第三方 DeepSeek 模型的统一接入」：① **集成模型接入 AI 网关**——「支持通过选择已集成的部分大模型供应商及配置 API-KEY 的方式直接接入使用」；② **通用模型方式接入 AI 网关**——「支持通过配置自定义 AI 服务地址且满足 OpenAI 接入标准的 AI 服务」；③ **AI 网关多模型代理**——「支持通过网关已集成的部分大模型供应商和配置自定义 AI 服务地址接入使用」 |
| **前置条件** | ① **创建专有网络 VPC 并绑定公网 NAT 网关**；② **基于上述 VPC 创建 AI 网关实例** |
| **关键配置步骤** | **场景一（集成模型）**：服务 → 创建服务 → 服务来源=**AI服务**；服务名称如 `aliyun-deepseek`；大模型供应商选对应供应商（示例为**阿里云百炼**）；**服务接入点使用阿里云百炼默认配置，如 `https://dashscope.aliyuncs.com/compatible-model/v1`**；填 **API-KEY**（「如果使用阿里云百炼，请在阿里云百炼 API-KEY 获取。其他大模型供应商，请咨询对应的服务供应商」）。Model API：域名建议配置（**使用默认环境域名下存在限流**）、Base Path、**AI请求观测=开启**、服务模型=**单模型服务**、模型名称=**透传**。调试：模型选 `deepseek-r1`。<br>**场景二（通用模型）**：适用于两类情况——「对于 AI 网关中**未集成大模型供应商**，且该模型支持 OpenAI 协议」、「对于通过在阿里云**人工智能平台 PAI** 或者**函数计算 FC** 等方式部署的 DeepSeek 服务」；官方直接指向「通过 AI 网关接入 PAI 部署模型」页（即配方 3），本页无独立步骤。<br>**场景三（多模型代理）**：先按场景一/二分别完成 **3 个** AI 服务（阿里云百炼、火山引擎、PAI）。**火山引擎服务配置（照抄）**：服务来源=**AI服务**；服务名称=`bytedance-deepseek`；大模型供应商=**豆包**；**服务地址（base_url）=`https://ark.cn-beijing.volces.com`**；在**大模型配置**区域填写对应 API-KEY；**并开启健康检查**。Model API：服务模型=**多模型服务（按模型名称）**；服务列表添加两个服务——百炼 DeepSeek 服务匹配规则 `deepseek-*`、火山引擎 DeepSeek 服务匹配规则 `ep-*`；**Fallback=开启**；**Fallback 列表**选 PAI DeepSeek 服务，模型名称配置为 `DeepSeek-R1-Distill-Qwen-1.5B` |
| **涉及的能力/插件** | AI 服务（已集成供应商 + 自定义 base_url）、服务接入点、健康检查、Model API 单模型服务与**多模型服务（按模型名称）**、模型名称**通配符匹配规则**、**Fallback**（多 Fallback 按顺序）、AI 请求观测、路由调试 |
| **踩坑点与限制** | 🔴 **路由规则语义（官方给出的执行规则，照抄）**：「模型为 `deepseek-*` 时调用阿里云 DeepSeek。模型为 `ep-*` 时调用火山引擎 DeepSeek。**在其他模型出错或限流场景下调用 PAI DeepSeek-R1-Distill-Qwen-1.5B（如配置多个 Fallback，则按顺序调用）**」。<br>🔴 **Fallback 触发条件的官方验证法**：「当配置一个**匹配上述模型前缀但错误**的名称，如 `deepseek-abc`，此时阿里云百炼不存在该模型。因此会触发 **Fallback**，调用到 PAI DeepSeek」；「在调试页面将模型设置为 `deepseek-abc` 并发送消息『你是谁?』，模型回复自我介绍为深度求索（DeepSeek）公司开发的 DeepSeek-R1 智能助手，确认 Fallback 已生效」→ **「模型不存在」也算 Fallback 触发条件**，不只是超时/5xx。<br>🔴 **火山引擎模型名以客户实际获取为准**：调试示例 `ep-20250219155230-28l6f`（原文注明「以火山引擎侧实际获取的模型为准」）；`deepseek-v3` 走阿里云百炼。<br>🔴 **默认环境域名下存在限流**（阈值 raw 未给数字）。<br>🔴 调试面板「模型返回」页签固定使用 `/v1/chat/completions` 对话接口，其他接口需选 **CURL命令** 或 **原始输出** 方式。<br>**限制**：场景二本页无独立内容，完全复用 PAI 配方；场景三需先备齐三个服务（含 PAI 自建兜底），对无 PAI 的客户不直接可用 |
| **对 SA 的可复用价值** | ① **回答「AI 网关开箱支持哪些模型供应商」的清单（15 家）**——见下表，选型答疑高频问题。② 回答「自部署/第三方 DeepSeek（PAI、FC、火山方舟）怎么统一入口」——通用模型 + OpenAI 协议。③ 回答「多供应商容灾怎么配、怎么验证」——多模型服务按名称匹配 + Fallback 顺序 + 故意写错模型名触发 Fallback 的可复现验证手法（可直接作为交付验收用例）。④ 回答「火山方舟（豆包）怎么接」——base_url `https://ark.cn-beijing.volces.com` + 供应商选豆包 + 开健康检查。⑤ 回答「百炼兼容端点地址是什么」——`https://dashscope.aliyuncs.com/compatible-model/v1` |
| **来源 slug** | `deepseek-integration-through-ai-gateway`（7855 B） |

**AI 网关已集成的 15 家大模型供应商（照抄清单，原文标题为「展开集成的大模型」）**：阿里云百炼、DeepSeek、OpenAI、Azure、Claude、月之暗面、百川智能、零一万物、智谱AI、混元、阶跃星辰、星火、豆包（火山引擎）、MiniMax、Gemini。[官方原文｜deepseek-integration-through-ai-gateway]

🟠 注意：这是**实践教程页**给出的清单且未标注时点；`access-vertex-ai-through-ai-gateway` 另把 **Vertex AI** 作为独立的大模型供应商选项、`pai-deployment-model-access-ai-gateway` 另有 **PAI-EAS**，二者均不在该 15 项内，说明该清单**不是供应商全集**。权威全量供应商清单[文档未说明]（应归 W3「供应商与模型元信息」）。

### 配方 3 — 接入 PAI-EAS 部署的模型

| 维度 | 内容 |
|---|---|
| **目标场景** | 「主要介绍如何通过 AI 网关访问部署在**人工智能平台 PAI** 的模型」。同时是配方 2 场景二（通用模型接入）的官方落地路径 |
| **前置条件** | ① **已通过 PAI 部署模型**（参见「一键部署模型」）；② 已创建 AI 网关实例 |
| **关键配置步骤** | **步骤一 创建 AI 服务**（7 个配置项）：服务来源=**AI服务**；服务名称如 `pai`；**大模型供应商=PAI-EAS**；**工作空间**=人工智能平台 PAI 工作空间（例如 `pai_xqrj0u0t******`）；**EAS服务**=选择通过 PAI 部署模型的名称（例如 `Qwen3-32B`）；**连接类型**=「选择与 PAI 部署模型的连接类型，**包含公网和私网两种**。本示例选择**私网**」；**API-KEY**=「**已自动获取**通过 PAI 部署模型的 API-KEY」；**健康检查**=「是否开启服务健康状态检查」。<br>**步骤二 创建 Model API**：配置 **Base Path**（API 的基本路径）+ **服务列表**选择步骤一新建的 AI 服务。<br>**步骤三 调试**：调试面板中**模型选择**在 PAI 中部署的模型，在**模型返回**页签对话；或用 **CURL命令** 页签复制 AI 网关提供的代码示例 → 把示例中的 `url` 接口替换为 `/v1/completions` → 把 `data(body)` 部分修改为 `/v1/completions` 需要的格式 |
| **涉及的能力/插件** | AI 服务（**PAI-EAS** 供应商）、工作空间/EAS服务选择器、**公网与私网两种连接类型**、**API-KEY 自动获取**、健康检查、Model API、`/v1/chat/completions` 与 `/v1/completions` 两种接口、路由调试 |
| **踩坑点与限制** | 🔴 **私网必须同 VPC（原文「重要」）**：「**当使用私网地址访问模型时，请确保 AI 网关实例与人工智能平台 PAI 部署的模型处于同一 VPC。**」→ 跨 VPC 场景本页未给方案。<br>🔴 **API-KEY 由网关自动获取**：「该 API-KEY 用于在 **AI 网关与 PAI-EAS 服务之间**进行身份验证，**AI 网关将自动获取 API-KEY 并与 PAI-EAS 服务建立通信**」→ 客户无需手工粘贴 EAS Token；密钥的生命周期由 PAI 侧驱动。<br>🔴 **调试面板「模型返回」页签固定走 `/v1/chat/completions`**，要用 `completions` 必须走 CURL/原始输出并自行改 URL 与 body 格式。<br>官方 CURL 示例的域名形态：`http://env-cxxx-cn-wulanchabu.alicloudapi.com/v1/completions`（**HTTP 非 HTTPS**，且为环境默认域名）；示例模型 `DeepSeek-R1-Distill-Qwen-1.5B`，示例响应 `usage` 为 `prompt_tokens:6, total_tokens:22, completion_tokens:16`，`finish_reason:"length"`，`object:"text_completion"`。<br>**限制**：本页未说明 PAI-EAS 供应商下是否支持多模型服务/Fallback/Token 限流等治理能力（只在配方 2 场景三中间接把 PAI 服务用作 Fallback 兜底）→ [文档未说明] |
| **对 SA 的可复用价值** | ① **回答「PAI-EAS 自部署模型怎么统一入口 + 统一观测 + 统一鉴权」**——标准三步。② **回答「私网打通要求」**——同 VPC 硬约束，跨 VPC 需另做网络设计。③ 回答「EAS 的 Token 要不要自己管」——网关自动获取。④ 该配方是配方 2 场景三的 Fallback 兜底服务来源（PAI `DeepSeek-R1-Distill-Qwen-1.5B`），可与配方 2 组合成「三方模型 + 自建兜底」的完整容灾方案，也可与配方 5 的高级负载均衡（自建模型集群 + 前缀匹配/GPU 感知）组合成「自建模型性能优化」方案 |
| **来源 slug** | `pai-deployment-model-access-ai-gateway`（4661 B） |

### 配方 4 — 代理 ComfyUI 服务

| 维度 | 内容 |
|---|---|
| **目标场景** | 「本文介绍如何使用 AI 网关代理 ComfyUI 服务」（**这是本页全部的背景说明，仅一句**） |
| **前置条件** | **创建 AI 网关**：「若当前无可用 AI 网关，请参考创建 AI 网关实例」（本页前提条件仅此一项，未提 VPC/NAT/ComfyUI 部署形态） |
| **关键配置步骤** | ① 实例 → 左侧导航 **服务** → **创建服务**，「**服务来源根据已创建的 ComfyUI 服务选择并完成配置**」；② （**说明中标注为「可选」**）进行**设置安全组规则**，「确保网关至目标服务网络链路畅通」；③ 左侧导航 **Model API** → **创建 Model API** → 在创建页面中**选择「图片生成」**，单击**创建** → **协议选择 `ComfyUI`** → **并选择所需路由**；④ 在**大模型服务的服务列表**中，选择步骤①创建的服务；⑤ 「配置完成后，可通过 **AI 网关接入点或配置的自定义域名**，对接 ComfyUI 服务」 |
| **涉及的能力/插件** | 服务（服务来源类型待客户自行判断）、**安全组规则**（可选）、Model API（**图片生成**类型）、**`ComfyUI` 协议**（与 OpenAI 兼容、百炼、VertexAI、Dify 并列的一种 Model API 协议选项）、路由、网关接入点/自定义域名 |
| **踩坑点与限制** | 🔴 **本页信息量严重不足（1142 B，为 W7 全部 25 页中最小的一页，正文仅 7 个步骤 + 1 条前提 + 1 条可选说明）**。逐条列出 raw 缺失项：ComfyUI 服务应选哪种**服务来源**（页面只写「根据已创建的 ComfyUI 服务选择」，未给枚举，也未说是否支持 DNS/固定地址/容器/SAE）；`ComfyUI` 协议下**可选哪些路由/接口**（只写「选择所需路由」，未列路径）；ComfyUI 的部署形态要求（ECS/ACK/SAE/自建 IDC）；鉴权方式；**Body 大小限制**（ComfyUI 工作流 JSON 与图片 Base64 通常远超 §10.9 的 5 KB 采集上限，二者关系未说明）；是否需要 VPC 打通或公网 NAT；健康检查；是否为公测能力；有无版本要求。**以上全部[文档未说明]。**<br>唯一可提取的硬性提示：**安全组规则是「可选」步骤，目的是「确保网关至目标服务网络链路畅通」**——即 ComfyUI 场景存在安全组阻断风险，交付时应主动核查 |
| **对 SA 的可复用价值** | 有限但有两点可用：① **确认 AI 网关把 ComfyUI 作为一等协议支持**（Model API 创建时「协议」下拉含 `ComfyUI`，且归类在「图片生成」场景下）——可用于回答「AI 网关能不能代理绘图工作流服务」这类能力有无问题。② 提示客户 ComfyUI 接入需额外检查安全组连通性。**除此之外的方案设计、容量评估、协议细节均无法基于本页完成，必须回控制台实测或提工单**；对客时应主动说明官方教程此页内容单薄，避免客户按本页做生产设计 |
| **来源 slug** | `proxy-comfyui-service-via-ai-gateway`（1142 B，全文照读，无省略） |

### 配方 5 — 代理 Dify 出入流量

| 维度 | 内容 |
|---|---|
| **目标场景** | 「为提升 Dify 应用的高可用性与安全性，用户可通过 AI 网关代理 Dify 的**入站与出站流量**」。**架构变更（照抄）**：「在原有架构中，Dify 内置 Nginx 作为反向代理处理入口流量，Dify 直接调用大模型、RAG 服务、Mcp Server 等后端服务。在新架构中，**AI 网关替代 Dify 内置 Nginx，统一代理 Dify 应用的所有入站和出站流量**」 |
| **前置条件** | 已部署 Dify，页面覆盖两种部署来源：**SAE**（「通过 SAE 或计算巢 Dify 社区版-Serverless 部署」）、**ACK**（「通过 ACK Helm 或计算巢 Dify 社区版-高可用版部署」）；已创建 AI 网关实例（页面未单列前提条件章节，此为步骤隐含要求）；**集群限流与前缀匹配负载均衡场景需 Redis 实例** |
| **关键配置步骤** | **入流量-服务来源（SAE）**：创建服务 → **服务来源选「SAE Kubernetes服务」** → **命名空间**选 Dify 应用所属命名空间 → **服务列表**选 **`dify-api-{namespace}`** 应用 → 确定。<br>**入流量-服务来源（ACK）**：「在服务-来源-创建来源处创建**容器来源**后，在服务-服务-创建服务处添加对应容器服务中 **`dify-system` 命名空间下的 `ack-dify-api`**」（服务来源选**容器服务**，命名空间选 Dify 应用所属命名空间）。<br>**入流量-路由（用 Agent API，不是 Model API）**：左侧导航 **Agent API** → **创建 Agent API** →「**域名** 和 **Base Path** 可以根据实际情况配置，用于通过域名访问 Dify 并且避免和其他服务的路径冲突」→ **勾选「转发至后端服务时移除」** → **协议选择 `Dify`** → 创建后进入该 Agent API 单击**创建路由**，按使用场景配置**路径（Path）**，**Agent 服务**选择上一步创建的服务。<br>**路径取值（决策关键）**：「如果 Dify 存在 **workflow 应用**，路径选择 **`/v1/workflows/run`**」；「如果 Dify 存在 **agent 应用**，路径选择 **`/v1/chat-messages`**」。<br>**一条路由对应一个 Dify 应用**：「可在**更多匹配规则**中配置请求头或请求参数匹配条件，例如设置 `header-key=app-id`。**需要注意通过 AI 网关访问 Dify 应用时，需自行在请求中携带对应的匹配字段**」。<br>验证：「路由发布后，可通过配置的域名和路径（Path）访问 Dify 应用以进行验证。若请求能够正常调用，则表明入流量代理配置成功」。<br>**出流量-模型代理（5 步）**：① 在 AI 网关控制台创建 **Model API**（用于访问自建或第三方大模型）；② **前往 Dify 应用市场，安装 higress 插件**；③ Dify 控制台右上角 **设置 > 模型供应商** → 为 higress 添加模型（以 LLM 为例）：**模型类型**选 **LLM**、**模型名称**和**凭据名称**可自定义、根据 AI 网关 Model API 实际场景和协议选择**使用场景**和**模型协议**（如文本生成、图片生成场景，OpenAI兼容协议、百炼协议等）、**「Higress AI 网关路由」填写在 AI 网关创建的 Model API 的域名+前缀**、**消费者鉴权策略/函数调用类型/思考模式支持**等其他参数按需配置；④ 在应用中需要选择模型的节点选择上述步骤创建的模型；⑤ 在 Dify 中运行 Workflow 或 Agent，验证通过 AI 网关代理访问 LLM 可以正常返回结果。<br>**出流量-外部知识库代理**：「部分 Dify 用户在利用 Dify 的高效构建与编排能力的同时，期望能够连接并访问**百炼、RAGFlow** 等外部知识库，以提升 RAG 效果。AI 网关提供**专为 Dify 设计的 RAG 代理插件**，支持 Dify 便捷、高效地对接外部知识库，降低用户自行实现的技术难度与开发成本」，具体见「AI RAG 检索代理」 |
| **涉及的能力/插件** | **Agent API（协议 `Dify`）**、Base Path「**转发至后端服务时移除**」、**更多匹配规则**（请求头/请求参数）、**SAE Kubernetes 服务来源**、**容器服务来源**、Model API、**Dify higress 插件**、**AI RAG 检索代理插件**、**cluster-key-rate-limit 插件（基于 Key 集群限流，从插件市场启用）**、Token 限流、**AI Fallback**（含「**仅Fallback后端服务错误**」选项）、**高级负载均衡**（全局最小请求数 / 前缀匹配 / GPU 感知）、**Redis**（集群限流计数 + prefix_cache 负载均衡）、AI 缓存、API-KEY 自动轮转、JWT 身份认证、敏感内容实时检测与拦截、Token 级度量指标监控与请求全链路追踪 |
| **踩坑点与限制** | 🔴 **为什么必须替代 Nginx 而不是串在 Nginx 前面（官方三条理由，可直接作对客话术）**：<br>1. **能力全覆盖**：「AI 网关已全面覆盖 Nginx 的反向代理功能，并提供**超过 20 项面向 AI 服务的专用治理策略**。**Nginx 默认启用的缓冲机制会中断 SSE 流式响应**，需手动调优多项参数以支持流式传输，配置复杂且缺乏深度可观测性支持。」<br>2. **架构精简化**：「由 AI 网关直接代理流量至 Dify 服务，可消除额外的代理层级。若采用**双网关架构（AI网关>Nginx>Dify）**，将引入不必要的网络跳转，增加延迟并影响性能；同时故障排查需覆盖 Nginx 层，延长问题定位周期，降低运维效率。」<br>3. **运维成本优化**：「Nginx 需独立部署并消耗额外计算与内存资源，扩缩容依赖人工干预。流量路由变更需在两套系统间同步配置，易引发配置不一致风险。相比之下，AI 网关采用**托管部署模式，提供企业级 SLA 保障**，原生集成监控、日志与告警能力。」<br>🔴 **集群限流必须引入 Redis**：「为支持全局级与应用级限流，**需引入 Redis 实例用于计数**。由于 **Redis 是 Dify 系统存储架构中的必要组件，可直接复用现有 Dify 系统的 Redis 实例**」→ 不产生新增组件成本，这是重要的方案卖点。<br>🔴 **前缀匹配负载均衡也依赖 Redis**（插件配置含 `serviceFQDN`、`servicePort: 6379`、`username`、`password`、`redisKeyTTL: 60`）。<br>🔴 **匹配规则需客户端配合**：走 `header-key=app-id` 一类路由匹配时，「需自行在请求中携带对应的匹配字段」，否则路由不命中。<br>🔴 **Fallback 官方验证用「不可达地址」作主服务**：主服务名 `wrong-service`、**使用指定模型名称=是**且模型名称为**透传**；开启 **Fallback** 开关并勾选**「仅Fallback后端服务错误」**，Fallback 服务名 `bailian`、**使用指定模型名称=否**。「通过网关日志可以发现 AI 网关在访问主模型服务时发生了 **503** 异常，于是自动 Fallback 至百炼模型进行调用，并返回正常调用结果」。<br>🔴 **限流的施加位置有区别**：出流量限流「配置方法与效果与前述内容一致，**仅限流策略施加位置不同**」。<br>🔴 **原文错字（逐字保留，客户照抄可能失败）**：「以**前提取**匹配负载均衡为例」出现两次，按上下文应为「前缀匹配」；负载均衡插件 YAML 中键名写作 **`Ib_config`**（大写 I），按上下文应为 `lb_config`。**建议客户实测确认后再落地。**[原文如此] |
| **对 SA 的可复用价值** | ① **回答「Dify 上生产怎么保证高可用」**——完整的入流量（替代 Nginx）+ 出流量（模型/RAG）双侧代理方案，含三条可背诵的反 Nginx 论据（尤其「Nginx 默认缓冲机制会中断 SSE 流式响应」极具说服力）。② **回答「多个 Dify 应用怎么共用一个网关」**——一 Agent API + 多路由 + header/param 匹配。③ **回答「Dify 怎么做应用级限流和 Token 限流」**——cluster-key-rate-limit（复用 Dify 的 Redis）+ 按消费者 Token 限流，均有可抄配置。④ **回答「自建模型集群怎么在不加硬件的前提下提升吞吐」**——前缀匹配负载均衡的官方压测数据（下表），可直接用于 GPU 成本优化论证。⑤ **回答「Dify 怎么接百炼/RAGFlow 等外部知识库」**——AI RAG 检索代理插件。⑥ 页面开头给出的 AI 网关四类核心特性与五项高可用机制，可作 §1/§5 的补充话术 |
| **来源 slug** | `proxy-dify-inbound-and-outbound-traffic-through-ai-gateway`（14578 B） |

**官方限流/负载均衡示例配置（照抄，代码块语言标记已从 `HELPCODEESCAPE-yaml` 修复为 yaml）**

集群限流（示例语义：「对某 Dify 应用设置 **1 分钟只允许通过一次的请求**」）：
```yaml
rule_name: dify_higress_demo_rule
rule_items:
- Limit_by_header: x-app-id
  limit_keys:
  - key: 9a342******************3e1250b5
    query_per_minute: 1
redis:
  service_name: dify-redis.dns
show_limit_quota_header: true
```
效果（照抄）：「插件启用后，对该应用发起调用时，若在一分钟内发送第 2 次请求，将触发 AI 网关的限流规则，导致请求失败。而**其他未配置流控规则的应用仍可被无限制地调用**。」

Token 限流（示例语义：「设置 Model API **每分钟限流 500 Token**」）：「开启**限流**开关，在限流策略中将判断条件设为**按消费者**，限流规则设为**任意匹配**，每分钟 Token 限额设为 **500**」；「配置生效后，当模型服务整体在 1 分钟时间范围内超出 500 Token 消耗后，访问模型的请求将会被 AI 网关直接拒绝。」

前缀匹配负载均衡：
```yaml
lb_policy: prefix_cache
Ib_config:            # [原文如此] 疑为 lb_config
  serviceFQDN: redis.dns
  servicePort: 6379
  username: default
  password: xxxxxxxxxxxx
  redisKeyTTL: 60
```
「插件生效后，Dify 应用通过 AI 网关对 LLM 服务发起调用，即可实现对自建 LLM 服务实例的负载均衡。」
[官方原文｜proxy-dify-inbound-and-outbound-traffic-through-ai-gateway]

🔴 **高级负载均衡压测数据（连表头逐行照抄）**

压测条件（照抄）：「针对 Dify 访问自建模型（例如在阿里云 PAI 上部署的模型）的场景，AI 网关提供面向 LLM 服务的多种负载均衡策略，包括**全局最小请求数负载均衡、前缀匹配负载均衡和 GPU 感知负载均衡**。这些策略可在**不增加硬件成本**的前提下，提升系统吞吐量、降低响应延迟，并实现更公平、高效的任务调度。」「使用 **NVIDIA GenAI-Perf** 作为压测工具，配置**每轮输入平均 200 token、输出平均 800 token，并发数为 20，每个会话包含 5 轮对话，共执行 60 个会话**。性能测试结果显示，启用该负载均衡策略后，**首Token延迟有明显降低**。」

| 指标 | 无负载均衡 | 前缀匹配负载均衡 |
|---|---|---|
| TTFT（首Token延迟） | **240 ms** | **120 ms** |
| 平均 RT | **14934.85 ms** | **14402.36 ms** |
| P99 RT | **35345.65 ms** | **30215.01 ms** |
| Token 吞吐 | **367.48 (token/s)** | **418.96 (token/s)** |
| Prefix Cache 命中率 | **40 %+** | **80 %+** |

[官方｜proxy-dify-inbound-and-outbound-traffic-through-ai-gateway]

🟠 [推断] TTFT 减半（240 ms → 120 ms）、Token 吞吐提升（367.48 → 418.96 token/s）、Prefix Cache 命中率翻倍（40 %+ → 80 %+），而平均 RT 仅从 14934.85 ms 降到 14402.36 ms、P99 RT 从 35345.65 ms 降到 30215.01 ms。推理链：在本压测的长输出配置下（输出平均 800 token vs 输入平均 200 token），前缀缓存主要压缩 prefill 阶段耗时，因此对 TTFT 收益最大，对整体 RT 的收益被 decode 时间稀释。**这是「不增加硬件投入」前提下最直接的性能论据**；但这是**单场景单轮压测**，raw 未给测试模型、GPU 型号、网关实例规格、模型副本数，故不可外推为客户环境的承诺值。

**该页给出的 AI 网关能力总述（可作 §1/§5 交叉引用，照抄要点）**
- 定位：「AI 网关作为**外部环境与企业 AI 应用之间、以及企业 AI 应用与大语言模型服务、MCP 服务之间的桥梁**，致力于解决模型集成复杂性、安全合规要求高、管理效率不足等问题，提供统一的流量治理与管控入口。」
- 核心特性四项：**协议标准化**（将不同模型的异构 API 统一转换为 OpenAI 兼容的标准化接口格式）、**可观测体系**（支持 **Token 级度量指标监控**，如 QPS、成功率、响应耗时，及请求全链路追踪能力）、**安全防护层**（提供 **API-KEY 自动轮转**、JWT 身份认证、敏感内容实时检测与拦截机制）、**稳定性引擎**（集成多级 Fallback 策略、AI 缓存加速、Token 粒度限流等流量治理功能）。
- 高可用机制五项：**多维度请求限流**（支持按应用、模型等维度，基于**秒级、分钟级、小时级**等时间粒度）、**Token 级资源流控**（「避免个别高消耗请求导致资源池耗尽」）、**模型 Fallback 机制**（「自动且透明地将请求路由至预配置的备用模型……实现**秒级故障切换与容灾恢复**」）、**模型负载均衡**（「面向自建模型集群，支持 **GPU 感知、前缀匹配**等智能负载均衡策略，在不增加硬件投入的前提下……最大化 GPU 资源利用效率」）、**AI 缓存机制**（「由网关直接返回缓存内容，显著减少对底层大模型的调用次数」）。
[官方｜proxy-dify-inbound-and-outbound-traffic-through-ai-gateway]

### 配方 6 — 把官方 Claude Code 迁移到任意模型

| 维度 | 内容 |
|---|---|
| **目标场景** | 「当用户使用 Claude Code 进行开发辅助，但**无法使用官方模型**时，可通过 AI 网关将 Claude Code 使用的模型从官方模型迁移到其他模型服务」。四项收益（照抄）：**统一接入**（统一入口屏蔽各家模型协议差异）、**避免锁定**（避免被特定供应商锁定）、**高可用性**（支持供应商 A 失败后兜底到供应商 B）、**按需路由**（根据模型名称智能路由到不同供应商） |
| **前置条件** | ① 已创建专有网络 VPC 并绑定**公网 NAT 网关**；② 已创建 AI 网关实例；③ **已安装 Claude Code 客户端**；④ 已获取目标大模型供应商 API Key |
| **关键配置步骤** | **步骤1 创建 AI 服务**：实例 → **服务** → **创建服务** → 服务来源选 **AI服务** → 在**大模型供应商**处选择对应模型提供商 → 在**大模型配置**中填写 API-KEY → 确定。「**可根据实际需要创建多个不同供应商的服务，实现多模型支持和高可用保障**」。<br>**步骤2 创建并调试 Model API**：**Model API** → **创建 Model API** →（以文本生成为例）单击文本生成选项框中的**创建** → 完成基本信息配置 → 在**大模型服务**中服务模型选**单模型服务**、**服务名称**选已创建的 AI 服务 → 确定。创建后单击右上角**调试** → 在**路由调试**页输入 Prompt → 单击**发送请求** → 「模型返回正确，则验证 Model API 已正确路由至指定大模型服务」。<br>**取访问入口**：「调试完成后，返回 Model API 列表，**单击所选 Model API「实例访问入口」列下的复制按钮**，用以设置 Claude Code 环境变量」。<br>**步骤3 在 Claude Code 中使用指定模型**：设置 `ANTHROPIC_BASE_URL` 与 `ANTHROPIC_AUTH_TOKEN` 两个环境变量（语义见「踩坑点」），再以 `--model` 指定模型启动，示例 `claude --model qwen3-coder-plus`（「以 qwen3 模型为例」）。<br>**步骤4 验证迁移效果**：执行 4 项测试（见下） |
| **涉及的能力/插件** | AI 服务（多供应商并存）、Model API 单模型服务/**多模型服务**、模型名称**通配符匹配**（「路由规则支持通配符匹配，如 `qwen*` 匹配所有以 qwen 开头的模型名称」）、**Fallback**（「开启 Fallback 后，当主要服务出错或限流时会自动切换到备用服务」「可以配置多个 Fallback 服务，按顺序进行故障转移」）、路由调试、**引用凭据（KMS）**、Model API 实例访问入口、消费者认证（API Key） |
| **踩坑点与限制** | 🔴 **两个环境变量的确切语义（照抄）**：<br>• `ANTHROPIC_BASE_URL`：「设置为步骤2中复制的 **Model API 实例访问入口**」。<br>• `ANTHROPIC_AUTH_TOKEN`：「如果 Model API **已开启认证**，并配置独立的 API Key，填写对应的 API Key。**如果没有开启认证，需填写一个任意值，不能填空。**」<br>→ **「不能填空」是本配方最容易踩的坑**：客户端强制要求该变量非空，与网关侧是否鉴权无关。<br>官方示例（bash）：<br>`export ANTHROPIC_BASE_URL=http://env-xxxxxx-cn-hangzhou.alicloudapi.com`<br>`export ANTHROPIC_AUTH_TOKEN=xxxx`<br>🔴 **示例 Base URL 为 `http://` 而非 `https://`**，且是**环境默认域名**（`env-xxxxxx-cn-hangzhou.alicloudapi.com`）。本页未像 Vertex/DeepSeek 页那样提示「默认环境域名存在限流」，也未讨论研发流量走 HTTP 明文的安全风险 → 生产落地建议改自定义域名 + HTTPS，但该建议属 [推断]（推理链：配方 1/2 明示默认域名存在限流 + 本页示例为 http 明文），raw 本页未明文提示。<br>🔴 **API Key 安全（原文「重要」）**：「API Key 建议通过**引用凭据**方式存储在 **KMS** 中，以避免 API Key 泄露风险。具体操作参见**钥**引用密钥」——原文「钥引用密钥」有衍字。[原文如此]<br>🔴 **切换模型完全靠客户端 `--model` 参数**：多模型切换测试即「通过 `--model` 参数切换不同模型，验证路由功能」。<br>**限制（raw 未覆盖）**：本页未说明 Claude Code 的哪些高级能力（如 Anthropic 专有的 tool use 格式、prompt caching、thinking 块、子命令）在非 Anthropic 后端下能否完整工作；未说明是否支持 Claude Code 的所有版本；未说明流式（SSE）兼容性 → 全部[文档未说明]。「工具调用测试」一条仅表述为「如果使用 MCP 工具，可验证工具调用功能是否正常」，未给结论 |
| **对 SA 的可复用价值** | ① **回答「Claude Code 不能用官方模型了怎么办 / 想用通义千问跑 Claude Code」**——研发工具链迁移的高频诉求，四步可交付。② 回答「研发工具怎么统一治理与避免供应商锁定」——网关侧统一入口 + 按需路由 + Fallback。③ **`ANTHROPIC_AUTH_TOKEN` 不能填空**这一条可直接省掉客户一轮排障工单。④ 官方给出的 4 项验证清单可直接作为交付验收用例。⑤ 与配方 2/3 组合：把 Claude Code 的后端指向「多模型服务 + PAI 自建兜底」，即得到研发场景的容灾方案 |
| **来源 slug** | `migrate-the-official-claude-code-model-to-any-model-using-ai-gateway`（4112 B） |

**官方 4 项验证测试（照抄）**：1. **基础对话测试**：输入简单问题，验证模型响应正常；2. **代码生成测试**：要求生成特定功能的代码，测试编程能力；3. **工具调用测试**：如果使用 MCP 工具，可验证工具调用功能是否正常；4. **多模型切换测试**：通过 `--model` 参数切换不同模型，验证路由功能。[官方｜migrate-the-official-claude-code-model-to-any-model-using-ai-gateway]

**步骤2 的补充说明（照抄）**：「若已创建多个大模型服务，在创建 Model API 时可选择**多模型服务**，并配置多个 AI 服务」；「路由规则支持通配符匹配，如 `qwen*` 匹配所有以 qwen 开头的模型名称」；「开启 Fallback 后，当主要服务**出错或限流**时会自动切换到备用服务」；「可以配置多个 Fallback 服务，按顺序进行故障转移」。[官方｜migrate-the-official-claude-code-model-to-any-model-using-ai-gateway]

### 配方 7 — 开启 LLM API 响应压缩节省带宽

| 维度 | 内容 |
|---|---|
| **目标场景** | 「基于阿里云 AI 网关在 LLM API 场景下的**实际压测数据**，评估了多种压缩算法（**ZSTD、GZIP、Brotli、QATZip**）在**流式与非流式**响应场景中的性能表现。测试结果显示，启用响应压缩功能可显著降低网络带宽消耗，**在流式响应场景下最高可减少 90% 以上的出方向带宽成本**」。解决两个核心问题：**高带宽成本**——「LLM 应用的响应通常为大量文本，在调用量较大时会产生较高的**公网流出带宽费用**」；**弱网体验不佳**——「在移动或网络不佳的环境下，未经压缩的大体积响应会导致客户端卡顿，影响流式体验」 |
| **前置条件** | 🔴 **实例形态与规格硬门槛（创建实例时的三项配置）**：**商品类型选「专享实例」**；**网关规格选 `aigw.medium.x1` 及以上规格**；勾选 **「分配Gzip硬件压缩资源」**。两条限制原文：「**Serverless 实例不支持硬件加速**」、「**仅 `aigw.medium.x1` 及以上规格实例支持开启硬件加速**」 |
| **关键配置步骤** | ① 创建支持硬件加速的 AI 网关实例（配置见前置条件）→ 单击**立即购买**；② 返回**实例**页面 → 单击目标实例 ID 进入详情页 → 左侧导航 **参数配置** → 在**网关引擎参数**配置区单击 **`EnableGzipHardwareAccelerate`** 参数右侧编辑 → **开启参数值开关**；③ **客户端侧要求（照抄）**：「开启后，需要客户端能够处理 Gzip 压缩的数据，**对于支持的客户端需要在请求头中添加 `Accept-Encoding:gzip`**」 |
| **涉及的能力/插件** | 网关引擎参数 **`EnableGzipHardwareAccelerate`**、**QATZip**（基于 Intel QuickAssist Technology 的硬件加速 GZIP）、专享实例购买页的「**分配Gzip硬件压缩资源**」选项 |
| **踩坑点与限制** | 🔴 **只有 Gzip 一个开关**：性能评测对比了 ZSTD/GZIP/Brotli/QATZip 四种算法，但**实施步骤只提供 `EnableGzipHardwareAccelerate` 一个参数**。如何启用 ZSTD/Brotli、是否有软件压缩（非硬件加速）路径、低于 `aigw.medium.x1` 的规格能否用软件压缩 → **全部[文档未说明]**。<br>🔴 **Serverless 实例完全不支持硬件加速**，即 Serverless 形态客户无法用本配方（与 §10.9 的「Serverless 版不支持请求/响应采集」构成 Serverless 形态在可观测/优化能力上的第二处缺失）。<br>🔴 **客户端必须显式声明 `Accept-Encoding:gzip`**，否则不生效——这是「开了压缩但账单没降」的头号原因。<br>🔴 **不推荐场景（官方决策表，见下）**：响应体已是压缩格式（图片 JPEG/PNG、视频、二进制文件）——「对已压缩数据再次压缩，效果不佳，且会增加 CPU 开销」；响应体极小（小于 1KB）——「压缩带来的开销（CPU、延迟）可能超过其收益」。<br>🔴 **流式压缩的 CPU 代价**：「在非流式场景下，CPU 使用率稳定在 **4.8% 至 6.2%** 之间，资源消耗较低。而在流式场景下，CPU 使用率上升至 **20.9% 至 34.5%**，需要消耗更多的计算资源」；官方解释「由于流式压缩需对连续数据进行实时分块处理，算法复杂度和数据处理量均显著增加，同时更高的压缩率通常伴随更多的计算操作，因此 **CPU 使用率上升属于预期现象**」。<br>🔴 **QATZip 依赖专用硬件**：「QAT 硬件加速卡集成专用压缩/解压缩引擎……**通过 PCIe 总线与主机连接**，支持与 CPU 并行运行及异步操作模式。CPU 可将压缩任务提交至加速卡后立即返回处理其他任务」→ 是否所有可用区/所有 `aigw.medium.x1` 以上规格都具备 QAT 硬件，raw 未说明。<br>[推断] 由「测试节点为 1 核 2GB 单节点」+「流式最高 34.5% CPU」推出：规格偏小的实例开流式压缩有 CPU 打满风险，SA 应建议客户在开启后观察资源监控（见 §10.3）；raw 未给出规格与 CPU 开销的推荐对应关系 → 推荐值[文档未说明] |
| **对 SA 的可复用价值** | 🔴 **这是全知识库最高价值的「省钱数字」之一，可直接进报价与优化建议**：流式响应带宽节省率 **92% - 97%**、非流式 **28% - 40%**。配合公网流出带宽单价即可算出客户 LLM 应用的可节省金额量级（单价归 W2/W1，本页无价格）。同时给出**四象限决策表**（流式 LLM API 推荐 / 大文本 JSON 推荐 / 已压缩内容不推荐 / 极小响应不推荐）与两个明确阈值（**1KB**、**100KB**），可直接用于方案评审。另可回答「压缩会不会拖慢网关」——用 CPU 消耗数据（非流式 4.8%-6.2%、流式 20.9%-34.5%）与 QATZip 选型结论作答 |
| **来源 slug** | `enable-llm-api-compression-to-save-bandwidth-costs`（9932 B） |

🔴 **带宽节省比例（逐字照抄，主控指派的高价值弹药）**
> **量化收益**：启用响应压缩，特别是针对流式 API，能节约成本并提升体验。
> * **成本节约**：
>   * 在 **流式响应** 场景下，带宽节省率可达 **92% - 97%**。
>   * 在 **非流式响应** 场景下，带宽节省率约为 **28% - 40%**。
> * **体验提升**：降低传输数据量，加快响应在客户端的加载速度，在弱网环境下效果明显。
> [官方原文｜enable-llm-api-compression-to-save-bandwidth-costs]

同页另有三处相关表述（一并照抄，注意口径差异）：
- 开篇：「启用响应压缩功能可显著降低网络带宽消耗，在流式响应场景下**最高可减少 90% 以上**的出方向带宽成本」。
- 结果分析：「流式响应的压缩效果显著优于非流式响应，两者压缩比可相差 **10 倍以上**」；「**非流式场景**：压缩比在 **60%-72%** 区间，带宽节省约 **28%-40%**」；「**流式场景**：压缩比可低至 **2.8%-7.2%**，带宽节省高达 **92%-97%**」。
- 决策表内：「LLM 流式 API……流式传输的协议和数据结构存在冗余，压缩效果好，**可节省最高 97% 的带宽**」；「返回大量文本/JSON 的普通 API……**当响应体大于 100KB 时，压缩能带来带宽节约**」。
[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

🔴 **压缩比定义（原文「注」，照抄）**
> **注：压缩比 = 压缩后大小 / 原始大小**，压缩比越小表示压缩效果越好。例如，**2.8% 表示压缩后数据仅为原始数据的 2.8%，节省了 97.2% 的带宽**。
> [官方原文｜enable-llm-api-compression-to-save-bandwidth-costs]

🟠 **注意「压缩比」与「节省率」是互补关系而非同一数字**：压缩比 2.8% ⇔ 节省 97.2%；非流式压缩比 72% ⇔ 节省 28%。SA 对客时若把「压缩比 72%」说成「节省 72%」即为报错数字。[推断] 由官方定义式与 2.8%↔97.2% 示例推出，二者互补关系在原文示例中已明示。

**测试环境（照抄）**

| 参数 | 配置 |
|---|---|
| 网关节点 | **1 核 2GB 内存，单节点部署** |
| 压测 QPS | **固定 30 QPS** |
| 测试场景 | LLM API 实际调用场景 |
| 压缩算法 | ZSTD、GZIP、Brotli、QATZip |

测试指标定义：**压缩比**——「压缩后数据大小与原数据大小的比例（越小越好）」；**CPU 消耗**——「网关节点在处理压缩时的 CPU 使用率」。
两种响应模式：**非流式响应**——「一次性返回完整的 JSON 响应」；**流式响应**——「采用流式传输模式（SSE/Chunked Transfer Encoding）」。
[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

🔴 **测试结果（连表头逐行照抄；原表用空单元格表示同一算法的第二行，此处补出算法名以免丢维度）**

| 压缩算法 | 响应模式 | 压缩比 | CPU 消耗 |
|---|---|---|---|
| **ZSTD** | 非流式 | **72%** | 6% |
| **ZSTD** | 流式 | **2.8%** | 23.6% |
| **GZIP** | 非流式 | **68.8%** | 6% |
| **GZIP** | 流式 | **7.2%** | 30% |
| **Brotli** | 非流式 | **60.8%** | 6.2% |
| **Brotli** | 流式 | **7.2%** | 34.5% |
| **QATZip** | 非流式 | **67%** | 4.8% |
| **QATZip** | 流式 | **2.9%** | 20.9% |

[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

**四种算法的技术特点（照抄）**：**GZIP**——「经典的 DEFLATE 压缩算法，兼容性优秀」；**ZSTD**——「Facebook 开源，压缩比和速度平衡优秀」；**Brotli**——「Google 开源，压缩比高但 CPU 消耗较大」；**QATZip**——「基于 Intel QAT 技术的硬件加速 GZIP，适用于高并发、低延迟、低 CPU 消耗场景」。[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

**官方选型结论（照抄）**：「根据压缩算法的测试结果，**QATZip 在综合性能上表现更优**。在流式场景下，**ZSTD/QATZip 的压缩比为 2.8%～2.9%，显著优于 Gzip/Brotli 的 7.2%**。在相近压缩比条件下，**QATZip 的 CPU 消耗为 20.9%，低于 ZSTD 的 23.6%**。得益于专用硬件加速支持，QATZip 在压缩效率和资源占用方面均具备优势。」另：「**阿里云 AI 网关与云原生 API 网关支持 QATZip 技术**，可通过硬件加速 Gzip 压缩，有效降低 CPU 利用率并减少网络带宽消耗。」[官方原文｜enable-llm-api-compression-to-save-bandwidth-costs]

🔴 **为什么流式压缩比这么高（官方机理，可作对客解释）**：「流式响应采用分块传输机制，数据按 token 逐步返回。**每个返回的 chunk 中包含重复性较高的数据结构（如 JSON 字段名、格式字符等），导致冗余信息较多**，此类重复模式更易被压缩算法识别并高效压缩。针对 LLM API 的流式响应进行压缩，可显著降低出方向网络带宽消耗。」[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

**「LLM API 特点」三条前提（照抄，解释为何压缩收益集中在出方向）**：
- **以流式传输为主**：「为提升响应实时性，多数 LLM API 采用 Server-Sent Events（SSE）或流式数据传输机制」。
- **响应数据量显著大于请求数据量**：「典型场景中，请求通常仅包含简短的提示词（Prompt），而响应则包含完整的生成文本，部分情况下还包括推理过程、置信度信息等附加内容，导致响应数据规模远超请求。因此，**网络带宽消耗主要集中于出方向**，即响应数据的传输阶段」。
- **响应数据高度结构化**：「LLM API 的响应通常以 JSON 格式组织，具有明确的字段结构和较高的数据冗余度……在流式传输场景下，连续的数据帧常包含相似的结构信息，进一步提升了可压缩性」。
[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

🟠 **适用场景与决策建议（官方四象限表，照抄）**

| 场景 | 推荐策略 | 说明 |
|---|---|---|
| **LLM 流式 API** | **推荐** | 例如基于 SSE 的对话接口。流式传输的协议和数据结构存在冗余，压缩效果好，**可节省最高 97% 的带宽** |
| **返回大量文本/JSON 的普通 API** | **推荐** | 例如返回长文章、大列表的 API。**当响应体大于 100KB 时，压缩能带来带宽节约** |
| **API 响应体已是压缩格式** | **不推荐** | 例如图片（JPEG/PNG）、视频、二进制文件等。对已压缩数据再次压缩，效果不佳，且会增加 CPU 开销 |
| **API 响应体极小** | **不推荐** | 例如**小于 1KB** 的响应。压缩带来的开销（CPU、延迟）可能超过其收益 |

[官方｜enable-llm-api-compression-to-save-bandwidth-costs]

🟠 [推断] 由「小于 1KB 不推荐」+「大于 100KB 时压缩能带来带宽节约」可推出：官方隐含的收益甜区在 1KB 以上、100KB 以上最明显；**1KB～100KB 区间官方未给结论** → 该中间区间收益[文档未说明]。另由「响应体已是压缩格式不推荐」可推出：**图片生成/视频生成类 Model API（如配方 1 场景六的 Imagen/Nano Banana、配方 4 的 ComfyUI）不适合开启响应压缩**——其响应为 base64 图片或二进制。推理链仅为上述两条官方判定 + 配方 1/4 的响应形态；raw 未明文针对图片生成场景给出压缩建议。

### §12 溯源

- `access-vertex-ai-through-ai-gateway` — AI 网关接入 Vertex AI（42868 B，924 行全读，含关键词检索复核）：配方 1 全部内容——6 场景划分与四项收益、两种鉴权方式、`vertexLocation` 默认 `global`、`vertexProjectId` 只读与自动解析、两种 OpenAI 协议兼容方式及各自适用场景、`google/` 前缀要求、原生协议模式与两条内置路由（Express / SA 两种路径格式）、DNS 服务的全局与区域端点选择及单向 TLS/SNI、GenAI SDK 不推荐的原因与可观测范围、多模态图片/视频格式清单与「AI 网关自动完成兼容性转换」、图片生成必须「AI 网关转换」的原因、SDK 对 `image_url` 的三接口支持矩阵、14 行尺寸映射表 + 10 个宽高比 + 3 个分辨率等级、模型清单（含 Publisher meta 的 Llama 4）、四类 FAQ、多供应商 Fallback 高级配置、三条安全建议、SA JSON 密钥字段与 Vertex AI User 角色要求；以及「本页无跨境网络要求」的否定性结论。
- `deepseek-integration-through-ai-gateway` — AI 网关接入 DeepSeek 模型（7855 B）：配方 2 全部内容——三场景划分与官方描述、15 家已集成供应商清单、百炼默认服务接入点 `https://dashscope.aliyuncs.com/compatible-model/v1`、场景二的两类适用情况与指向 PAI 页、火山引擎豆包 base_url `https://ark.cn-beijing.volces.com` 与健康检查、`deepseek-*`/`ep-*` 匹配规则、PAI Fallback 与「按顺序调用」、`deepseek-abc` 触发 Fallback 的官方验证法、默认环境域名限流提示、调试面板接口限制。
- `pai-deployment-model-access-ai-gateway` — AI 网关接入 PAI-EAS 部署模型（4661 B）：配方 3 全部内容——PAI 部署与网关实例两项前提、7 个 AI 服务配置项（PAI-EAS 供应商、工作空间示例、EAS服务示例、公网/私网连接类型、API-KEY 自动获取与其用途、健康检查）、同 VPC 硬约束、`/v1/completions` 的 CURL 改写三步与示例响应字段。
- `proxy-comfyui-service-via-ai-gateway` — AI 网关代理 ComfyUI 服务（1142 B）：配方 4 全部内容；信息量不足已在卡内逐条列明 9 项缺失，可提取事实仅为「协议选 ComfyUI」「场景归类图片生成」「可选设置安全组规则以确保网络链路畅通」「通过网关接入点或自定义域名对接」。
- `proxy-dify-inbound-and-outbound-traffic-through-ai-gateway` — AI 网关代理 Dify 出入流量（14578 B）：配方 5 全部内容——替代 Nginx 的架构决策与三条理由（含「超过 20 项专用治理策略」「Nginx 默认缓冲机制会中断 SSE 流式响应」「托管部署 + 企业级 SLA」）、SAE/ACK 两种服务来源与具体服务名（`dify-api-{namespace}`、`dify-system` 下 `ack-dify-api`）、Agent API 协议 `Dify` 与「转发至后端服务时移除」、workflow `/v1/workflows/run` 与 agent `/v1/chat-messages` 两条路径、header 匹配需客户端携带、Dify higress 插件安装与模型供应商各字段（含「Higress AI 网关路由 = Model API 域名+前缀」）、AI RAG 检索代理插件与百炼/RAGFlow、cluster-key-rate-limit 完整 YAML 与「1 分钟 1 次」效果、Redis 复用 Dify 现有实例、Token 限流 500/分钟配置、Fallback `wrong-service`→`bailian` 与 503 日志现象、前缀匹配负载均衡 YAML 与 5 项压测指标、GenAI-Perf 压测参数（200/800 token、并发 20、5 轮/会话、60 会话）、三种负载均衡策略、AI 网关四特性五机制总述、两处原文错字。
- `migrate-the-official-claude-code-model-to-any-model-using-ai-gateway` — Claude Code 迁移至任意模型（4112 B）：配方 6 全部内容——四项收益、四条前提、四步迁移（含「实例访问入口」复制按钮）、`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` 语义与「不能填空」、`claude --model qwen3-coder-plus`、http 明文示例域名、通配符路由与多 Fallback 顺序、KMS 引用凭据建议（含原文衍字）、4 项验证测试、步骤2 的四条补充说明。
- `enable-llm-api-compression-to-save-bandwidth-costs` — LLM API 响应压缩节省带宽（9932 B）：配方 7 全部内容——92%-97% / 28%-40% 节省率、90% 以上出方向带宽成本、压缩比定义与 2.8%↔97.2% 示例、60%-72% 与 2.8%-7.2% 两个压缩比区间、10 倍以上差距、测试环境（1 核 2GB 单节点 / 固定 30 QPS）、8 行测试结果（4 算法 × 2 模式，压缩比 + CPU 消耗双维度）、CPU 区间 4.8%-6.2% 与 20.9%-34.5% 及其机理解释、四算法技术特点、QATZip 选型结论与 Intel QAT/PCIe 原理、四象限决策表（1KB / 100KB 两个阈值）、LLM API 三条特点、专享实例 + `aigw.medium.x1` 及以上 + 分配Gzip硬件压缩资源、Serverless 不支持硬件加速、`EnableGzipHardwareAccelerate`、`Accept-Encoding:gzip` 客户端要求。

**本章查无**：
1. 🔴 **Vertex AI 的跨境/跨地域网络要求**——主控指派提示本页含此弹药，但通读 924 行 + 关键词检索后确认全页仅有「VPC + 公网 NAT 网关」与「确认目标区域的网络连通性」两处网络表述，**无跨境专线、GA/CEN、数据出境合规、地域对应关系、延迟量级任何内容**。详见配方 1 内的专门说明。
2. **默认环境域名的限流阈值**——Vertex AI 页 4 处、DeepSeek 页 1 处提示「使用默认环境域名存在限流」，但**没有任何数字**（QPS/并发/带宽均无）。SA 无法量化「为什么必须买自定义域名」。
3. **各配方的性能基线**——除配方 5（负载均衡压测）与配方 7（压缩压测）外，配方 1/2/3/4/6 均无任何 RT、吞吐、并发数据。
4. **网关引入的额外延迟**——7 个配方均未给出「经过 AI 网关 vs 直连后端」的延迟对比，客户问「加一层网关慢多少」无答案。
5. **配方 4（ComfyUI）的绝大部分技术细节**——服务来源类型、可选路由/接口、部署形态、鉴权、Body 大小限制、网络要求、是否公测：全部[文档未说明]（页面仅 1142 B）。
6. **压缩算法的选择方式**——如何在 ZSTD/GZIP/Brotli/QATZip 之间选择、是否有对应参数、无 QAT 硬件时如何启用软件压缩：[文档未说明]。
7. **`aigw.medium.x1` 的规格定义与 QAT 硬件可用性**——本页只给规格名（规格含义归 W1）；QAT 加速卡在哪些地域/可用区/规格可用：[文档未说明]。
8. **压缩对首包时延（TTFT）的影响**——开启压缩后 TTFT 是否变差、客户端是否需支持增量解压：[文档未说明]（配方 7 只给了压缩比与 CPU 两个维度）。
9. **Dify higress 插件的版本要求与 Dify 版本兼容性**——只说「前往 Dify 应用市场安装 higress 插件」，未给版本号、最低 Dify 版本、插件参数全集。
10. **配方 6 中 Claude Code 的功能完整性**——非 Anthropic 后端下 tool use / prompt caching / thinking / 各子命令是否降级：[文档未说明]。
11. **15 家已集成供应商清单是否为全集**——Vertex AI、PAI-EAS 在其他页作为独立供应商出现但不在该 15 项内；权威清单[文档未说明]（归 W3）。
12. **各配方涉及能力的连带计费**——7 个配方页均无价格信息；例如配方 1/2/6 需 NAT 网关、配方 5 复用 Redis、配方 7 需专享实例特定规格、配方 3 需 PAI-EAS 资源，这些连带成本在本章 raw 内全部[文档未说明]（归 W2）。
13. **配方 5 中「超过 20 项面向 AI 服务的专用治理策略」的具体清单**——只给数量，未列项目（归 W6 插件体系）。
14. **配方 3/5 中自建模型的 GPU 感知负载均衡实测数据**——官方只给了前缀匹配一种策略的压测结果，GPU 感知与全局最小请求数两种策略无数据。

---
## §13 OpenAPI 与 RAM 元信息

> 本章是给 SA 做**自动化脚本设计**与**权限方案**用的速查。按主控要求：归纳 + 保留关键数字，不照搬长表。

### 13.1 OpenAPI 概览（`api-apig-2024-03-27-overview-ai-gateway`）

| 项目 | 官方口径 |
|---|---|
| 产品与版本 | **APIG / 2024-03-27** |
| 🔴 签名风格 | 「本产品（APIG/2024-03-27）的 OpenAPI 采用 **ROA** 签名风格」 |
| SDK | 「我们已经为开发者封装了**常见编程语言**的 SDK，开发者可通过下载 SDK 直接调用本产品 OpenAPI 而无需关心技术细节」——🔴 **具体支持哪些语言、各语言版本，raw 未列出**，只给下载入口外链 → [文档未说明] |
| 🔴 自签名成本 | 「如果现有 SDK 不能满足使用需求，可通过签名机制进行自签名对接。**由于自签名细节非常复杂，需花费 5个工作日左右**。因此建议加入我们的服务钉钉群（**147535001692**），在专家指导下进行签名对接」 |
| 账号准备 | 「在使用 API 前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI 等）访问 API」 |
| 🔴 安全基线（照抄） | 「阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，**建议创建一个仅具备 API 访问权限的 RAM 用户并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略**。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号」 |

[官方原文｜api-apig-2024-03-27-overview-ai-gateway]

🟠 「**5 个工作日左右** + **钉钉群 147535001692**」是排期与升级路径的直接弹药：客户提出自签名对接需求时，SA 应先给这个工期预期并引导入群，而不是承诺 SDK 之外的快速交付。

#### Action 分组与数量（W7 逐组计数：合计 **140 个 Action，无重名**）

| 分组 | Action 数 | 全部/典型 Action |
|---|---|---|
| API管理（HTTP API） | **9** | `CreateHttpApi`、`UpdateHttpApi`、`GetHttpApi`、`ListHttpApis`、`DeleteHttpApi`、`DeployHttpApi`、`UndeployHttpApi`、`ImportHttpApi`、`ExportHttpApi` |
| 接口管理 | **5** | `CreateHttpApiOperation`、`GetHttpApiOperation`、`UpdateHttpApiOperation`、`ListHttpApiOperations`、`DeleteHttpApiOperation` |
| 模型元信息管理 | **10** | 供应商 5 个（`CreateAiModelProvider`/`GetAiModelProvider`/`ListAiModelProviders`/`UpdateAiModelProvider`/`DeleteAiModelProvider`）+ 模型卡片 5 个（`CreateAiModelCard`/`GetAiModelCard`/`ListAiModelCards`/`UpdateAiModelCard`/`DeleteAiModelCard`） |
| MCP管理 | **8** | `CreateMcpServer`、`UpdateMcpServer`、`GetMcpServer`、`ListMcpServers`、`DeleteMcpServer`、`DeployMcpServer`、`UnDeployMcpServer`、`SyncMCPServers`（同步 Nacos MCP 到网关） |
| 路由管理 | **5** | `CreateHttpApiRoute`、`UpdateHttpApiRoute`、`GetHttpApiRoute`、`DeleteHttpApiRoute`、`ListHttpApiRoutes` |
| 服务管理 | **3** | `CreateServiceVersion`、`UpdateServiceVersion`、`DeleteServiceVersion`（**仅服务版本**；服务本体 CRUD 在「其他」分组） |
| 网关管理 | **12** | `CreateGateway`、`UpdateGatewayName`、`UpdateGatewayFeature`、`UpgradeGateway`、`GetGateway`、`ListGateways`、`AddGatewaySecurityGroupRule`、`DeleteGateway`、`DeleteGatewaySecurityGroupRule`、`ListZones`、`RestartGateway`、`ListGatewayFeatures` |
| 消费者组管理 | **8** | `CreateConsumerGroup`、`GetConsumerGroup`、`ListConsumerGroups`、`ListConsumerGroupConsumers`、`UpdateConsumerGroup`、`DeleteConsumerGroup`、`BatchAddConsumerGroupConsumers`、`BatchRemoveConsumerGroupConsumers` |
| 消费者管理 | **13** | `CreateConsumer`、`UpdateConsumer`、`GetConsumer`、`ListConsumers`、`DeleteConsumer` + 授权规则 8 个（`CreateConsumerAuthorizationRule`、`CreateConsumerAuthorizationRules`、`UpdateConsumerAuthorizationRule`、`GetConsumerAuthorizationRule`、`QueryConsumerAuthorizationRules`、`DeleteConsumerAuthorizationRule`、`RemoveConsumerAuthorizationRule`、`BatchDeleteConsumerAuthorizationRule`） |
| 策略管理 | **5** | `ListPolicyClasses`、`UpdatePolicy`、`CreatePolicyAttachment`、`GetPolicyAttachment`、`DeletePolicyAttachment` |
| 插件管理 | **8** | `ListPlugins`、`CreatePluginAttachment`、`GetPluginAttachment`、`ListPluginAttachments`、`UpdatePluginAttachment`、`DeletePluginAttachment`、`InstallPlugin`、`UninstallPlugin` |
| 域名管理 | **6** | `ListSslCerts`、`GetDomain`、`CreateDomain`、`ListDomains`、`DeleteDomain`、`UpdateDomain` |
| 监控管理 | **2** | `GetTraceConfig`（获取链路追踪配置）、`GetDashboard`（获取监控日志大盘接口） |
| 资源管理 | **1** | `GetResourceOverview`（获取资源概览信息） |
| 历史接口 | **3** | `GetEnvironment`、`CreateAndAttachPolicy`、`UpdateAndAttachPolicy`（页面另有一行「环境管理」为分组标题占位，无对应 Action） |
| 其他 | **42** | 见下方拆解 |
| **合计** | **140** | — |

[官方｜api-apig-2024-03-27-overview-ai-gateway]

**「其他」分组 42 个 Action 的按主题拆解（W7 归纳，非官方分组）**：

| 子主题 | 数量 | Action |
|---|---|---|
| **FinOps 配额规则** | **9** | `AddGatewayQuotaRule`、`UpdateGatewayQuotaRule`、`UpdateGatewayQuotaRuleStatus`（启/停用）、`ResetGatewayQuotaRule`、`GetGatewayQuotaRule`、`ListGatewayQuotaRules`、`DeleteGatewayQuotaRule`、`GetGatewayQuotaRuleSubjectUsage`（获取配额规则下某个消费主体用量详情，「包括已用配额、总配额、是否超限、用量详情及消费记录等」）、`ListConsumerQuotaRules` |
| **密钥/凭据** | **7** | `CreateSecret`（生成密钥）、`UpdateSecret`、`GetSecret`、`GetSecretValue`（获取密钥值）、`ListSecrets`、`DeleteSecret`（删除密钥值）、`ListSecretReferences`（列出密钥引用） |
| **服务与服务来源** | **9** | `CreateService`、`UpdateService`（「支持更新服务健康检查配置，DNS 域名和固定地址的地址配置信息」）、`GetService`、`ListServices`、`DeleteService`、`CreateSource`、`GetSource`、`DeleteSource`、`ListExternalServices`（获取网关的外部服务信息） |
| **环境** | **4** | `CreateEnvironment`、`UpdateEnvironment`、`ListEnvironments`、`DeleteEnvironment` |
| **策略与插件类** | **7** | `CreatePolicy`、`GetPolicy`、`ListPolicies`、`DeletePolicy`、`CreatePluginClass`（创建自定义插件类）、`GetPluginClass`、`ListPluginClasses` |
| **标签与资源组** | **4** | `TagResources`（资源打标）、`UntagResources`、`ListTagResources`、`ChangeResourceGroup`（资源转组） |
| **地域** | **1** | `DescribeRegions`（「查询当前账号可见的云原生 API 网关开服地域」） |
| **消费者授权规则** | **1** | `ListConsumerAuthorizationRules` |

[官方｜api-apig-2024-03-27-overview-ai-gateway]

🟠 **对 SA 的三个结论**：
1. **概览页的分组不可靠**——42 个 Action（占总数 30%）被塞进「其他」，其中包括整套 **FinOps 配额规则**（成本控制自动化的核心）、**密钥管理**、**服务与服务来源 CRUD**。写自动化脚本时不能按分组名找 Action。[推断] 由上表计数推出；raw 未说明「其他」分组的归类依据。
2. **服务本体与网关本体的 CRUD 分散在两处**：`CreateService`/`UpdateService`/`GetService`/`ListServices`/`DeleteService` 在「其他」，而「服务管理」分组只有服务版本三个 Action。
3. **`ImportHttpApi` 的能力边界（官方概述）**：「导入 HTTP API，**支持将 OpenAPI 2.0 和 OpenAPI 3.0.x 版本的定义文件导入为 REST 类型的 API**」→ 只导入为 REST 类型，不支持导入为其他 API 类型。[官方原文｜api-apig-2024-03-27-overview-ai-gateway]

### 13.2 服务接入点（`api-apig-2024-03-27-endpoint-ai-gateway`）

**域名格式**：公网 `apig.{regionId}.aliyuncs.com`；VPC `apig-vpc.{regionId}.aliyuncs.com`。[官方｜api-apig-2024-03-27-endpoint-ai-gateway]（该格式与 §11.2 门户环境变量 `POP_GATEWAY_URL` 的公网/内网写法一致）

**地域覆盖（W7 逐行计数）**：全页分三张表，共 **25 个地域**，其中 **19 个有 VPC 接入地址，6 个没有**。

| 分区 | 地域数 | 有 VPC 接入地址 | 无 VPC 接入地址 |
|---|---|---|---|
| 亚太 | **19** | 14 | 5 |
| 欧洲与美洲 | **4** | 4 | 0 |
| 中东 | **2** | 1 | 1 |
| **合计** | **25** | **19** | **6** |

[官方｜api-apig-2024-03-27-endpoint-ai-gateway]

🔴 **6 个无 VPC 接入地址的地域（完整列出）**：

| 地域名称 | 地域ID | 备注 |
|---|---|---|
| **澳大利亚（悉尼）已关停** | `ap-southeast-2` | 🔴 官方在地域名称中直接标注「**已关停**」 |
| 菲律宾（马尼拉） | `ap-southeast-6` | — |
| 泰国（曼谷） | `ap-southeast-7` | — |
| 华南3（广州） | `cn-guangzhou` | — |
| 华南2（河源） | `cn-heyuan` | — |
| 沙特（利雅得） | `me-central-1` | — |

[官方｜api-apig-2024-03-27-endpoint-ai-gateway]

🟠 **对 SA 的结论**：客户若要把门户/自动化脚本部署在**广州、河源、马尼拉、曼谷、利雅得**并要求走内网 Endpoint，**做不到**——这 5 个地域只有公网接入地址，必须走公网（连带公网带宽费用与出网链路）。`ap-southeast-2`（悉尼）已关停，不应再出现在任何方案里。[推断] 由上表 VPC 列空值推出；raw 未说明这些地域为何无 VPC 接入点、是否有替代方案（如 PrivateLink）。

**19 个有 VPC 接入地址的地域（regionId）**：`cn-shenzhen`、`cn-wulanchabu`、`cn-beijing`、`ap-northeast-2`、`ap-northeast-1`、`cn-chengdu`、`cn-qingdao`、`cn-shanghai`、`cn-hongkong`、`ap-southeast-1`、`ap-southeast-3`、`ap-southeast-5`、`cn-zhangjiakou`、`cn-hangzhou`、`us-west-1`、`us-east-1`、`eu-central-1`、`eu-west-1`、`me-east-1`。[官方｜api-apig-2024-03-27-endpoint-ai-gateway]

🟠 **注意与「AI 网关实例可开通地域」不是同一份清单**：本页是 **OpenAPI 接入点**的地域覆盖（APIG 产品级），不等于 AI 网关实例的售卖地域。后者归 W1；raw 本页未声明二者关系 → 交叉核验[文档未说明]。

### 13.3 🔴 OpenAPI 流控配额（`api-apig-2024-03-27-quota-ai-gateway`）

**表结构**：4 列——API名称 / API版本 / 配额 / 配额维度。**共 105 行**（W7 逐行解析）。

**三个「全表统一」的事实（无例外）**：
- **API版本**：105 行全部为 `2024-03-27`。
- **地域**：105 行全部为 `*`（即不区分地域，全地域同一配额）。
- 🔴 **API限速维度**：105 行全部为 **`regionId,API,ParentUid`**。

[官方｜api-apig-2024-03-27-quota-ai-gateway]

🟠 **限速维度的实操含义**：三元组 `regionId + API + ParentUid`。[推断] 由该维度组合推出「限流是按**主账号（ParentUid）**在**单个地域**内**按单个 API** 分别计数的」，因此：① 同一主账号下多个 RAM 子账号**共享**同一份配额（维度里没有子账号标识）；② 不同地域各自独立计数，多地域并行调用不会互相挤占；③ 不同 Action 各自独立计数。raw 未解释该维度语义 → 语义解释[文档未说明]，此为按维度字段的推断。

**配额记法**：原文格式为 `N/M(s)`（如 `30/1(s)`、`60/60(s)`、`60/3000(s)`）。**页面未给出该记法的单位说明** → [文档未说明]。[推断] 按阿里云通用流控记法，`N/M(s)` 表示「M 秒内最多 N 次」，故 `30/1(s)` = 每秒 30 次、`60/60(s)` = 每 60 秒 60 次（即平均每秒 1 次）、`60/3000(s)` = 每 3000 秒 60 次（即平均每分钟 1.2 次）。此推断未经 raw 证实，SA 对客报数时应同时给出原文记法。

#### 配额分布（按读/写拆分，W7 按 Action 动词前缀归类）

| 类别 | Action 数 | 配额分布（照抄原文记法） |
|---|---|---|
| **写操作**（Create/Update/Delete/Deploy/Undeploy/UnDeploy/Install/Uninstall/Import/Add/Remove/Batch*/Change/Reset/Restart/Upgrade/Sync） | **64** | `30/1(s)` × **46**；`50/1(s)` × **17**；`60/60(s)` × **1**（`UpdatePluginAttachment`） |
| **读操作**（Get/List/Query/Export） | **41** | `60/1(s)` × **32**；`50/1(s)` × **8**；`60/3000(s)` × **1**（`GetPluginAttachment`） |
| **合计** | **105** | `30/1(s)` × 46；`50/1(s)` × 25；`60/1(s)` × 32；`60/60(s)` × 1；`60/3000(s)` × 1 |

[官方｜api-apig-2024-03-27-quota-ai-gateway]

🔴 **典型 QPS 配额结论（SA 速记）**：
- **写操作典型配额 = `30/1(s)`**（64 个写 Action 中 46 个，占 72%）——`CreateGateway`、`CreateHttpApi`、`CreateHttpApiRoute`、`CreateService`、`CreateConsumer`、`CreateDomain`、`DeployHttpApi`、`RestartGateway`、`UpgradeGateway`、`InstallPlugin`、`DeleteGateway` 等全部是 `30/1(s)`。
- **读操作典型配额 = `60/1(s)`**（41 个读 Action 中 32 个，占 78%）——`GetGateway`、`ListGateways`、`GetHttpApi`、`ListHttpApis`、`ListHttpApiRoutes`、`GetConsumer`、`ListConsumers`、`ListServices`、`ListDomains`、`GetDashboard`、`GetTraceConfig`、`ListPlugins` 等全部是 `60/1(s)`。
- **`50/1(s)` 是中间档**（25 个）——集中在 **MCP 管理**（`CreateMcpServer`/`UpdateMcpServer`/`GetMcpServer`/`ListMcpServers`/`DeleteMcpServer`/`DeployMcpServer`/`UnDeployMcpServer`/`SyncMCPServers` 全部为 `50/1(s)`）、**密钥管理**（`CreateSecret`/`UpdateSecret`/`GetSecret`/`GetSecretValue`/`ListSecrets`/`DeleteSecret`/`ListSecretReferences` 全部为 `50/1(s)`）、**策略**（`CreatePolicy`/`UpdatePolicy`/`DeletePolicy`/`GetPolicyAttachment`/`CreatePolicyAttachment`/`DeletePolicyAttachment`）、以及消费者授权规则的批量类（`CreateConsumerAuthorizationRules`/`RemoveConsumerAuthorizationRule`/`BatchDeleteConsumerAuthorizationRule`/`QueryConsumerAuthorizationRules`）。

🔴 **两个例外项（必须单独记住，是全表最严的两条）**：

| Action | 配额 | 换算（[推断]） | 影响 |
|---|---|---|---|
| **`UpdatePluginAttachment`**（更新插件挂载） | **`60/60(s)`** | 每 60 秒最多 60 次 ≈ 平均 1 次/秒 | 比常规写操作 `30/1(s)` 严 **30 倍**。批量刷插件配置（如给上百条路由批量改插件参数）会被限流 |
| **`GetPluginAttachment`**（查询插件挂载） | **`60/3000(s)`** | 每 3000 秒（50 分钟）最多 60 次 ≈ 平均 **1.2 次/分钟** | 🔴 **比常规读操作 `60/1(s)` 严 3000 倍**，是全表最紧的一条。**任何轮询 `GetPluginAttachment` 的自动化脚本都会立刻撞墙**；同类查询应改用 `ListPluginAttachments`（`60/1(s)`） |

[官方｜api-apig-2024-03-27-quota-ai-gateway]

🟠 [推断] 由「`GetPluginAttachment` 为 `60/3000(s)` 而 `ListPluginAttachments` 为 `60/1(s)`」推出：官方有意把单条查询压到极低以引导使用列表接口。做插件配置巡检/同步的自动化，**必须走 List 而非 Get 逐条查**。此为推断，raw 未说明设计意图。

#### 🔴 配额覆盖缺口（对写自动化脚本的客户是坑）

概览页列出 **140** 个 Action，配额页只有 **105** 行，且「配额页的 105 个 Action 全部包含在概览页的 140 个之内」（W7 做双向差集，反向差集为 0）。→ **35 个 Action 在配额页查无流控条目**：

| 缺口主题 | 数量 | Action |
|---|---|---|
| **AI 模型元信息（整套全缺）** | **10** | `CreateAiModelProvider`、`GetAiModelProvider`、`ListAiModelProviders`、`UpdateAiModelProvider`、`DeleteAiModelProvider`、`CreateAiModelCard`、`GetAiModelCard`、`ListAiModelCards`、`UpdateAiModelCard`、`DeleteAiModelCard` |
| **FinOps 配额规则（整套全缺）** | **9** | `AddGatewayQuotaRule`、`UpdateGatewayQuotaRule`、`UpdateGatewayQuotaRuleStatus`、`ResetGatewayQuotaRule`、`GetGatewayQuotaRule`、`ListGatewayQuotaRules`、`DeleteGatewayQuotaRule`、`GetGatewayQuotaRuleSubjectUsage`、`ListConsumerQuotaRules` |
| **消费者组（整套全缺）** | **8** | `CreateConsumerGroup`、`GetConsumerGroup`、`ListConsumerGroups`、`ListConsumerGroupConsumers`、`UpdateConsumerGroup`、`DeleteConsumerGroup`、`BatchAddConsumerGroupConsumers`、`BatchRemoveConsumerGroupConsumers` |
| **插件类与环境/外部服务** | **5** | `CreatePluginClass`、`GetPluginClass`、`CreateEnvironment`、`ListExternalServices`、`DescribeRegions` |
| **标签三件套** | **3** | `TagResources`、`UntagResources`、`ListTagResources`（注：`ChangeResourceGroup` 在配额页**有**条目，为 `30/1(s)`） |
| **合计** | **35** | — |

[官方｜api-apig-2024-03-27-overview-ai-gateway｜api-apig-2024-03-27-quota-ai-gateway]

🔴 **这是文档级空白**：FinOps 配额规则、AI 模型元信息、消费者组这三类**较新的能力**（正好是 AI 网关区别于云原生 API 网关的差异化 Action）在流控配额页**完全没有条目**，客户无法预知这些接口的调用频率上限。**SA 在为客户设计成本控制/模型元信息批量同步的自动化方案时，必须提工单确认配额，不能引用本页。**

### 13.4 🔴 RAM 授权信息（`api-apig-2024-03-27-ram-ai-gateway`）

**产品级元信息**：

| 项目 | 官方口径 |
|---|---|
| RAM 代码（RamCode） | **`apig`** |
| 🔴 支持的授权粒度 | 「**资源级**」 |
| Action 总数 | **140 个**（W7 逐行解析 Action 表 141 行含表头 → 140 个 Action） |
| 与概览页的一致性 | **完全一致**——W7 做双向差集，RAM 页与概览页的 140 个 Action **无任何差集**（互为子集） |
| 权限策略格式 | JSON，`Version` 为 `"1"`；`Statement` 内含 `Effect`（**Allow / Deny**）、`Action`、`Resource`（用资源 ARN 描述）、`Condition`（**可选字段**，含 `Condition_operator` / `Condition_key` / `Condition_value`） |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

官方对表列的定义（决定了怎么读这张表，照抄要点）：
- **访问级别**：「指每个操作的访问级别，取值为**写入（Write）、读取（Read）或列出（List）**」
- **资源类型**：「对于**必选资源类型，用前面加 `*` 表示**」；「对于**不支持资源级授权的操作，用`全部资源`表示**」
- **条件关键字**：「指云产品自身定义的条件关键字。**该列不体现适用于任何操作的通用条件关键字**」
- **关联操作**：「指成功执行操作所需要的其他权限。**操作者必须同时具备关联操作的权限，操作才能成功**」
[官方原文｜api-apig-2024-03-27-ram-ai-gateway]

#### 13.4.1 按资源级/操作级授权的分布（🔴 权限设计的核心数据）

| 资源类型（Action 表「资源类型」列的取值） | Action 数 | 占比 | 典型 Action |
|---|---|---|---|
| **`全部资源`**（= **不支持资源级授权**，只能操作级授权） | **66** | 47.1% | 见下方清单 |
| **Gateway** | **22** | 15.7% | `CreateGateway`、`GetGateway`、`ListGateways`、`DeleteGateway`、`UpgradeGateway`、`RestartGateway`、`UpdateGatewayFeature`、`UpdateGatewayName`、`ListGatewayFeatures`、`Add/DeleteGatewaySecurityGroupRule`、`ListExternalServices`、`TagResources`、`UntagResources`、以及 **FinOps 配额规则 7 个**（`Add/Update/Delete/Reset/Get/List GatewayQuotaRule(s)`、`UpdateGatewayQuotaRuleStatus`、`GetGatewayQuotaRuleSubjectUsage`） |
| **HttpApi** | **18** | 12.9% | `CreateHttpApi`、`GetHttpApi`、`ListHttpApis`、`UpdateHttpApi`、`DeleteHttpApi`、`DeployHttpApi`、`UndeployHttpApi`、`ExportHttpApi`、`Create/Get/Update/Delete HttpApiRoute`、`ListHttpApiRoutes`、`Create/Get/Update/Delete HttpApiOperation`、`ListHttpApiOperations` |
| **Domain** | **18** | 12.9% | 🔴 **该标签是个「大杂烩」**，W7 按 ARN 实测拆为三块：真正的**域名类 5 个**（`CreateDomain`、`GetDomain`、`ListDomains`、`UpdateDomain`、`DeleteDomain`）+ **消费者类 9 个**（`GetConsumer`、`UpdateConsumer`、`DeleteConsumer`、`CreateConsumerAuthorizationRule`、`GetConsumerAuthorizationRule`、`UpdateConsumerAuthorizationRule`、`DeleteConsumerAuthorizationRule`、`ListConsumerAuthorizationRules`、`ListConsumerQuotaRules`）+ **密钥类 4 个**（`GetSecret`、`UpdateSecret`、`DeleteSecret`、`ListSecretReferences`）。（注意 `CreateConsumer` **不在此组**，它标为「全部资源」，见下方硬结论 4） |
| **Service** | **7** | 5.0% | `CreateService`、`GetService`、`ListServices`、`UpdateService`、`DeleteService`、`UpdateServiceVersion`、`DeleteServiceVersion` |
| **Environment** | **5** | 3.6% | `CreateEnvironment`、`GetEnvironment`、`ListEnvironments`、`UpdateEnvironment`、`DeleteEnvironment` |
| **Policy** | **3** | 2.1% | `GetPolicy`、`CreateAndAttachPolicy`、`UpdateAndAttachPolicy` |
| **Source** | **1** | 0.7% | `DeleteSource` |
| **合计** | **140** | 100% | — |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

🔴 **结论：140 个 Action 中只有 74 个支持资源级授权，66 个（47.1%）标为「全部资源」即不支持资源级授权**——按官方自己的定义，这 66 个只能做操作级（Action 级）授权，无法限定到具体资源实例。**近一半的 Action 无法做细粒度隔离，这是权限方案设计的硬约束。**

**66 个标为「全部资源」的 Action（完整清单，W7 按能力重排归类；各组数量之和经脚本校验 = 66）**：

| 能力 | 数量 | Action |
|---|---|---|
| **AI 模型元信息（整套）** | **10** | `CreateAiModelProvider`、`GetAiModelProvider`、`ListAiModelProviders`、`UpdateAiModelProvider`、`DeleteAiModelProvider`、`CreateAiModelCard`、`GetAiModelCard`、`ListAiModelCards`、`UpdateAiModelCard`、`DeleteAiModelCard` |
| **MCP（整套）** | **8** | `CreateMcpServer`、`UpdateMcpServer`、`GetMcpServer`、`ListMcpServers`、`DeleteMcpServer`、`DeployMcpServer`、`UnDeployMcpServer`、`SyncMCPServers` |
| **消费者组（整套）** | **8** | `CreateConsumerGroup`、`GetConsumerGroup`、`ListConsumerGroups`、`ListConsumerGroupConsumers`、`UpdateConsumerGroup`、`DeleteConsumerGroup`、`BatchAddConsumerGroupConsumers`、`BatchRemoveConsumerGroupConsumers` |
| **插件与插件类（整套）** | **11** | `ListPlugins`、`ListPluginClasses`、`CreatePluginClass`、`GetPluginClass`、`InstallPlugin`、`UninstallPlugin`、`CreatePluginAttachment`、`GetPluginAttachment`、`ListPluginAttachments`、`UpdatePluginAttachment`、`DeletePluginAttachment` |
| **策略与策略挂载（整套）** | **8** | `CreatePolicy`、`UpdatePolicy`、`DeletePolicy`、`ListPolicies`、`ListPolicyClasses`、`CreatePolicyAttachment`、`GetPolicyAttachment`、`DeletePolicyAttachment` |
| **消费者与授权规则（部分）** | **6** | `CreateConsumer`、`ListConsumers`、`QueryConsumerAuthorizationRules`、`CreateConsumerAuthorizationRules`、`RemoveConsumerAuthorizationRule`、`BatchDeleteConsumerAuthorizationRule` |
| **密钥与服务来源（部分）** | **6** | `CreateSecret`、`GetSecretValue`、`ListSecrets`、`CreateSource`、`GetSource`、`CreateServiceVersion` |
| **监控与资源（整套）** | **5** | `GetDashboard`、`GetTraceConfig`、`GetResourceOverview`、`ListZones`、`ListSslCerts` |
| **其他** | **4** | `ImportHttpApi`、`ChangeResourceGroup`、`DescribeRegions`、`ListTagResources` |
| **合计** | **66** | — |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

🔴 **权限设计的四条硬结论**：
1. **MCP、AI 模型元信息、消费者组三类能力完全无法做资源级授权**（整套均为「全部资源」）→ 多租户/多项目隔离场景下，**不能靠 RAM 资源级策略把 A 项目的 MCP Server 与 B 项目隔开**，只能靠分账号或分网关实例。[推断] 由三类能力 100% 标为「全部资源」+ 官方对「全部资源」的定义推出。
2. **插件相关 Action 全部无法资源级授权**（含 `InstallPlugin`/`UninstallPlugin`/`CreatePluginAttachment`/`UpdatePluginAttachment`）→ 授予插件管理权即等于授予该账号在**所有**网关上的插件管理权。
3. **FinOps 配额规则反而支持资源级授权**（7 个 Action 的资源类型是 **Gateway**）→ 可以按网关实例隔离成本控制权限，这是三类新能力中唯一能细粒度授权的。
4. **`CreateConsumer` 标为「全部资源」，但 `GetConsumer`/`UpdateConsumer`/`DeleteConsumer` 标为「Domain」** → 创建消费者无法限定资源，读改删可以。做「只能管理自己项目消费者」的策略时，创建环节无法收窄。

#### 13.4.2 访问级别分布

| 访问级别（原文取值） | Action 数 |
|---|---|
| **none** | **96** |
| get | 12 |
| list | 9 |
| create | 9 |
| delete | 8 |
| update | 6 |
| **合计** | **140** |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

🔴 **注意口径冲突**：官方在表列说明中写「访问级别……取值为**写入（Write）、读取（Read）或列出（List）**」，但表内实际出现的取值是 **`none` / `get` / `list` / `create` / `delete` / `update`**——**没有任何一行的取值是 Write 或 Read**，且 **96 个 Action（68.6%）的访问级别为 `none`**（未标注）。[官方矛盾]（同页两处口径不一致：说明文字 vs 表格实际取值）
- 说明文字原文：「访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。」
- 表格实际取值：`none`(96)、`get`(12)、`list`(9)、`create`(9)、`delete`(8)、`update`(6)。
→ **不裁决，交主控**。实操影响：SA 无法用「访问级别」列可靠地区分读写 Action（近 7 成为 `none`），设计只读角色时应改用 Action 动词前缀（Get/List/Query/Describe/Export）判断，参见 13.3 的读/写拆分。

#### 13.4.3 条件关键字（Condition Key）

**产品级条件关键字只有 2 个**：

| 条件关键字 | 描述 | 类型 |
|---|---|---|
| `apig:GatewayId` | 网关ID | **Array** |
| `apig:NetworkType` | 网络类型 | **Array** |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

- 官方说明：「以下仅列举**产品级**的条件关键字，阿里云定义的**通用条件关键字**也同样适用 API 网关」；「数据类型决定了您可以使用哪些条件运算符……**您必须使用与数据类型匹配的条件运算符，否则无法匹配策略语句，授权行为无效**」。两个键的类型都是 **Array**。[官方｜api-apig-2024-03-27-ram-ai-gateway]
- 🔴 **实际使用情况（W7 逐行统计 Action 表的「条件关键字」列）**：`无` × **138**；`apig:GatewayId` × **2**。**只有 `apig:GetService` 与 `apig:GetSource` 两个 Action 标注了 `apig:GatewayId`**。
- 🔴 **`apig:NetworkType` 未被任何 Action 标注**（140 行中 0 次）——它出现在条件关键字表里，但 Action 表的「条件关键字」列从未引用它。是否可用、用在哪些 Action 上：[文档未说明]。
- 🔴 **没有标签类条件关键字**（如 `acs:ResourceTag/...` 的产品级变体）→ 结合 §10.11「标签对权限的影响[文档未说明]」，**无法在 AI 网关侧用标签做 ABAC 授权**（阿里云通用条件关键字是否覆盖标签场景，raw 只说「通用条件关键字也同样适用」，未列举）。

🟠 [推断] 由「仅 2 个 Action 支持 `apig:GatewayId` 条件键」推出：**条件键在 AI 网关上几乎不可用**，按网关实例做权限收窄只能依赖资源级 ARN（`acs:apig:{#regionId}:{#accountId}:gateway/{#GatewayId}`），不能依赖 Condition。推理链为上述两项统计；raw 未说明为何只有这两个 Action 支持条件键。

#### 13.4.4 资源（Resource）ARN 表（8 类，照抄）

| 资源类型 | 资源 ARN |
|---|---|
| **Environment** | `acs:apig:{#regionId}:{#accountId}:environment/{#EnvironmentId}`<br>`acs:apig:{#regionId}:{#accountId}:environment/*` |
| **HttpApi** | `acs:apig:{#regionId}:{#accountId}:httpapi/{#HttpApiId}`<br>`acs:apig:{#regionId}:{#accountId}:httpapi/*` |
| **Policy** | `acs:apig:{#regionId}:{#accountId}:policy/{#PolicyId}`<br>`acs:apig:{#regionId}:{#accountId}:policy/*` |
| **Gateway** | `acs:apig:{#regionId}:{#accountId}:gateway/{#GatewayId}`<br>`acs:apig:{#regionId}:{#accountId}:gateway/*` |
| **Domain** | `acs:apig:{#regionId}:{#accountId}:secret/{#SecretId}`<br>`acs:apig:{#regionId}:{#accountId}:consumer/*`<br>`acs:apig:{#regionId}:{#accountId}:consumer/{#ConsumerId}`<br>`acs:apig:{#regionId}:{#accountId}:secret/*`<br>`acs:apig:{#regionId}:{#accountId}:domain/*`<br>`acs:apig:{#regionId}:{#accountId}:domain/{#DomainId}` |
| **Service** | `acs:apig:{#regionId}:{#accountId}:service/*`<br>`acs:apig:{#regionId}:{#accountId}:service/{#ServiceId}` |
| **Source** | `acs:apig:{#regionId}:{#accountId}:source/{#SourceId}`<br>`acs:apig:{#regionId}:{#accountId}:source/{SourceId]` **[原文如此：第二条的花括号与方括号不匹配]** |
| **ConsumerAuthorizationRule** | `acs:apig:{#regionId}:{#accountId}:consumerauthorizationrule/*` |

[官方｜api-apig-2024-03-27-ram-ai-gateway]

ARN 变量说明（照抄）：「`{#}` 为变量标识，需要您替换为实际值。例如 `{#ramcode}` 需要您替换为实际的云服务 RAM 代码」；「`*` 表示全部。例如：`{#resourceType}` 为 `*` 时表示全部资源；`{#regionId}` 为 `*` 时表示全部地域；`{#accountId}` 为 `*` 时表示全部阿里云账号」。[官方原文｜api-apig-2024-03-27-ram-ai-gateway]

🔴 **RAM 页的四处官方文档缺陷（逐条列出，供主控裁决/反馈官方）**：
1. **「Domain」资源类型的 ARN 列混入了 6 种 ARN**（secret、consumer、domain 三类），资源类型名与实际 ARN 不符。W7 统计 Action 表中标为 `Domain` 的 18 个 Action，其 ARN 实际分布为：`consumer/{#ConsumerId}` × 9、`secret/{#SecretId}` × 4、`domain/{#DomainId}` × 3、`domain/*` × 2。→ **Consumer、Secret、Domain 三种资源在 RAM 元信息里被合并成一个叫「Domain」的资源类型**，写策略时容易误判。
2. **`Source` 的第二条 ARN 括号不匹配**：`acs:apig:{#regionId}:{#accountId}:source/{SourceId]`（`{SourceId]`）。[原文如此]
3. **`ConsumerAuthorizationRule` 资源类型在 ARN 表中定义（`consumerauthorizationrule/*`），但在 Action 表的「资源类型」列中从未出现**（140 个 Action 的资源类型只有 8 种取值：`全部资源`/Gateway/HttpApi/Domain/Service/Environment/Policy/Source）。→ 该资源类型无法用于任何 Action 的授权。
4. **`CreateConsumerAuthorizationRule` 的资源类型标为 `Domain`，但 ARN 是 `consumer/{#ConsumerId}`**（与缺陷 1 同源）。

🔴 **缺失的资源类型**：ARN 表中**没有** `mcpserver`、`plugin`/`pluginattachment`、`aimodelprovider`、`aimodelcard`、`consumergroup`、`serviceversion` 的 ARN 定义——与 13.4.1 中这些 Action 全部标为「全部资源」相互印证。**即 MCP / 插件 / AI 模型元信息 / 消费者组四类对象在 RAM 层面根本没有资源标识**。[推断] 由 ARN 表 8 类 + Action 表资源类型 8 种取值均不含上述对象推出。

#### 13.4.5 关联操作与最小权限策略

- 🔴 **关联操作**：140 个 Action 的「关联操作」列**全部为「无」**（W7 逐行统计）。→ **不存在「必须同时具备另一个权限才能成功」的隐含依赖**，这对最小权限设计是好消息：不需要为某个 Action 追加隐藏的伴生权限。[官方｜api-apig-2024-03-27-ram-ai-gateway]
- 官方给出的后续操作路径：创建自定义权限策略 → 为 RAM 用户 / RAM 用户组 / RAM 角色授权（均为 RAM 侧通用文档外链）。[官方｜api-apig-2024-03-27-ram-ai-gateway]
- 🔴 **本页没有给出任何最小权限策略示例**——没有「只读角色」「运维角色」「网关管理员」等样板。raw 内唯一可直接引用的最小权限样板来自 **§11.3 门户服务**（`AliyunAPIGReadOnlyAccess` + `apig:*Consumer*`，见 `deployment-portal`）。→ **RAM 页只有元数据表，没有策略模板，这是文档级空白**。
- 🟠 [推断] 基于 13.3 的读/写拆分与 13.4.1 的资源类型分布，可构造只读角色：Action 取全部 `Get*`/`List*`/`Query*`/`Describe*`/`Export*`（41 个有配额条目的读 Action，参见 13.3 清单），Resource 取 `acs:apig:*:*:*`。推理链为 13.3 读操作清单 + ARN 变量说明中「`*` 表示全部」；**该策略非官方给出，SA 使用前需实测**。

### 13.5 公共错误码（`api-apig-2024-03-27-errorcodes`）

**总量与分布（W7 逐行解析，表共 5 列：HTTP status code / 错误码 / 错误信息 / 描述 / 操作）**：**111 行**，其中 `DatabaseError.RecordNotFound` 出现 **2 次**（描述不同）→ **去重后 110 个错误码**。每行都带一个「诊断」外链（`https://api.aliyun.com/troubleshoot?q=<错误码>`）。

| HTTP status code | 条数 | 占比 |
|---|---|---|
| **409** | **67** | 60.4% |
| **400** | **23** | 20.7% |
| **404** | **13** | 11.7% |
| **500** | **5** | 4.5% |
| **403** | **3** | 2.7% |
| **合计** | **111** | 100% |

| 错误码前缀 | 条数 |
|---|---|
| `Conflict.*` | **66** |
| `InvalidParameter.*` | **22** |
| `NotFound.*` | **10** |
| `ServiceInternalError.*` | 3 |
| `APIG.ErrorCode.*` | 2 |
| `DatabaseError.*` | 2 |
| `CloudProductInactive.*` | 1 |
| `InternalError` | 1 |
| `ApiReplaced.*` | 1 |
| `GatewayIsDeleted.*` | 1 |
| `CodeupService.*` | 1 |
| `Forbidden.*` | 1 |

[官方｜api-apig-2024-03-27-errorcodes]

🟠 **总体判断**：**六成错误是 409 冲突类**，即 AI 网关 OpenAPI 的失败绝大多数是**状态/命名/配额冲突**，而不是权限或参数格式问题。写自动化脚本时，**409 必须做重试与幂等处理**，而不是简单抛异常。[推断] 由 409 占 60.4% 且其中大量为「已存在」「正在变更中」「状态不允许」类语义推出。

#### 13.5.1 🔴 409 冲突类（客户最可能遇到，按子类归纳；共 67 条）

**A. 名称/版本重复（幂等与命名规范问题）**

| 错误码 | 错误信息 | 描述（照抄） |
|---|---|---|
| `Conflict.ApiNameDuplicated` | `API name %s duplicated.` | API%s已存在，请修改名称 |
| `Conflict.ApiVersionDuplicated` | `API version %s duplicated.` | API版本%s，已存在，请更换版本号 |
| `Conflict.OperationNameDuplicated` | `Operation name %s duplicated.` | 接口%s已存在，请修改名称 |
| `Conflict.RouteNameDuplicated` | `Route name %s is duplicated.` | 路由%s已存在，请修改名称 |
| `Conflict.DomainExisted` | `Domain %s is existed.` | 域名%s已存在 |
| `Conflict.EnvironmentExisted` | `Environment %s is existed.` | 已经存在名称为%s的环境，请更换环境名称 |
| `Conflict.ServiceExisted` | `the service %s is existed.` | 已存在名为%s的服务，请修改服务名称 |
| `Conflict.ServiceVersionExisted` | `Service version %s already exists, please change the service version name.` | 服务版本 %s 已存在，请更换服务版本名称 |
| `Conflict.K8sServiceSourceExisted` | `The k8s service source of %s is existed.` | 网关已存在%s集群的K8s服务来源 |
| `Conflict.PluginNameExisted` | `Plugin name %s existed.` | 插件%s已存在，请修改名称 |
| `InvalidParameter.PluginNameExist`（**400**） | `The plugin name already exists.` | 已存在同名的插件 |
| `Conflict.PolicyExisted` | `Policy %s is existed.` | 策略%s已存在，无法重复启用 |

🔴 **注意「插件重名」有两个错误码、两个状态码**：`Conflict.PluginNameExisted`（409）与 `InvalidParameter.PluginNameExist`（400），描述都是「已存在同名的插件」。**脚本做重名判断时必须同时匹配这两个码。**[官方｜api-apig-2024-03-27-errorcodes]

**B. 路径/发布冲突（🔴 主控点名的重点）**

| 错误码 | 错误信息 | 描述（照抄） |
|---|---|---|
| `Conflict.ApiPublishDuplicatedPathFound` | `Duplicated path found, key: %s, apiId: %s ,operationId: %s, environmentId: %s, conflict domains: %s.` | **API路径冲突**，冲突键为%s，冲突的API ID为%s，接口 ID为%s，环境 ID为%s，冲突的域名为%s |
| `Conflict.ApiPublished` | `API %s is published in %s.` | API：%s**已经被发布到环境**：%s，**请先取消发布** |
| `Conflict.ApiVersionMustEnabled` | `API has more than one version, can not disable version.` | API已存在多个版本，**不能关闭版本管理功能** |
| `Conflict.ApiDebugProtocolMismatch` | `Domain %s protocol mismatch, got: %s, want: %s.` | 域名%s支持的协议与调试请求的协议不匹配，调试协议为%s，域名支持的协议为%s |
| `Conflict.ApiPublishServiceTypeNotSupported` | `Service type %s is not supported.` | 不支持的服务类型：%s，请检查您的配置 |
| `Conflict.HttpApiTypeNotSupportedForRoute` | `Only APIs of type Http, HttpIngress, and Websocket support route.` | **只有类型为 Http, HttpIngress, Websocket 的 API 支持路由** |
| `Conflict.PluginPublishSameVersion` | `Plugin %s version %s has been published.` | 插件%s的%s版本**已发布，请勿重复发布** |
| `Conflict.PluginPublishVersionOnlyIncrement` | `Plugin %s version %s must be larger than history version.` | 插件%s的版本%s不合法，**版本只能向上递增，并超过所有历史版本** |
| `Conflict.DomainIsProcessing` | `The domain %s is currently being deployed. Please try again later.` | 目标环境域名正在部署中 |

**C. 授权冲突（🔴 主控点名的重点）**

| 错误码 | 错误信息 | 描述（照抄） |
|---|---|---|
| `Conflict.ConsumerAuthorizationForbidden` | `Consumer has authorized to resource %s.` | **消费者已授权资源%s，请勿重复授权** |
| `Conflict.PolicyAttachExceedLimit` | `Resource can not attach 2 same class policy.` | **一个资源上不能挂两个相同类型的策略** |
| `Conflict.WafAttachConditionNotMatch` | `WAF should be enabled on gateway instance first.` | 您必须**先在网关实例启用 WAF** 后才能配置 WAF 策略 |
| `Conflict.GatewayNotSupportedWAF` | `The gateway %s does not support enabling WAF protection. Please upgrade to a version of the gateway that supports it.` | 网关%s不支持开启WAF防护，**请升级到支持的网关版本** |
| `CodeupService.NotAuthorized`（**403**） | `The caller has not authorized APIG to access Codeup, or no Codeup organization exists...` | 调用方**未授权 APIG 访问云效 Codeup**，或账号下不存在 Codeup 组织 |

🟠 **`Conflict.PolicyAttachExceedLimit` 的硬约束**：「一个资源上不能挂两个相同类型的策略」——这是策略设计的强限制，客户想「同一 API 上叠两条限流策略」会直接失败。[官方原文｜api-apig-2024-03-27-errorcodes]

**D. 状态机冲突（需重试）**

| 错误码 | 描述（照抄） |
|---|---|
| `Conflict.AppClusterIsAlreadyInChanging` | 网关实例正在变更中，**请稍后重试操作**（`App cluster is already in changing. Retry after some minutes.`） |
| `Conflict.GatewayStatusInvalidForbidden` | 网关当前不支持操作，**请等网关正常运行时再做操作** |
| `Conflict.GatewayStatusNotExpected` | 网关的状态%s不是期望的状态%s |
| `Conflict.GatewayIsDeleted` | 网关%s已删除 |
| `Conflict.EnvironmentGatewayNotReady` | 环境 %s 里的网关 %s **未就绪**，请等网关就绪后再操作 |
| `Conflict.EnvironmentPublishing` | 环境%s正处于**发布中**，请稍后重试 |
| `Conflict.PluginInstallGatewayNotReady` | 网关实例%s状态未就绪，请稍后再安装插件 |
| `Conflict.PluginClassNotReady` | 插件%s尚未就绪，请稍后重试安装 |
| `Conflict.SdkGenerating` | SDK 生成中，请稍后重试 |
| `Conflict.DeleteRouteForbidden` / `Conflict.DeployRouteForbidden` / `Conflict.UndeployRouteForbidden` / `Conflict.UpdateRouteForbidden` | 路由%s 状态为%s，不允许**删除 / 部署 / 取消部署 / 更新**（`UndeployRouteForbidden` 的错误信息原文为 `Route %s cannot be updeployed when its status is %s.`，**`updeployed` 疑为 `undeployed` 拼写错误**，[原文如此]） |
| `Conflict.UpdateRouteEnvironmentForbidden` | 当前路由%s状态为%s不允许更改环境。**如需修改，可以先将路由部署，待完成后再更换环境** |

**E. 删除保护（引用/依赖检查）**

| 错误码 | 描述（照抄） |
|---|---|
| `Conflict.DeleteHttpApiForbidden` | 当前API %s 存在已经%s个部署的路由，不能删除（错误信息：`The current API %s has already deployments of routes and cannot be deleted.`） |
| `Conflict.DomainCannotDelete` | 域名%s还存在关联的**已发布 API 或路由**，无法删除，**请下线相关资源后再执行操作** |
| `Conflict.EnvironmentCannotDelete` | 环境%s存在关联的已发布的 API 或路由，无法删除，请下线相关资源后再执行操作 |
| `Conflict.ServiceIsReferencedWhenDelete` | 存在其他资源引用此服务，**请先解绑后再删除服务**，关联的资源为%s |
| `Conflict.ServicesExistedWhenDeleteSource` | 服务来源还存在服务，请先删除对应服务后再删除服务来源，关联的服务ID为%s |
| `Conflict.HttpIngressApiExistedWhenDeleteSource` | 存在 http ingress api 使用该来源，请先删除对应 http ingress api 后再删除服务来源，关联的 http ingress api ID 为%s |
| `Conflict.SourceExistedWhenCreateIngressApi` | 该服务来源 %s 已经被其他 HTTP Ingress API 使用，请使用其他的服务来源来创建 HTTP Ingress API |
| `Conflict.PluginHasAttachedRule` | 插件%s 可能在 **API/接口、路由、域名或网关实例**上开启，无法卸载，**请检查并停用对应资源上的插件规则再试** |
| `Conflict.PluginInstalled` | 插件%s已安装到网关实例，请先卸载相关网关实例的插件再进行删除 |
| `Conflict.PluginOtherVersionInstalled` | 插件%s的%s版本已经安装，**请先卸载后再重试** |

**F. 🔴 配额超限类（9 条，全部用 `%s` 占位，官方未给数值）**

| 错误码 | 描述（照抄） | 配额数值 |
|---|---|---|
| `Conflict.ApiOperationQuotaExceed` | 每个 API 的 Operation 数量不能超过 %s 个，当前数量为 %s，**请提升您的配额** | 🔴 `%s` 占位 |
| `Conflict.OperationQuotaExceed` | 接口总数量不能超过%s，当前数量为%s，请提升您的配额（错误信息注明维度为 **per region**） | 🔴 `%s` 占位 |
| `Conflict.OnlineOperationQuotaPerGatewayExceed` | 单个网关**在线接口**数量不能超过%s，当前数量为%s | 🔴 `%s` 占位 |
| `Conflict.RouteQuotaPerGatewayExceed` | 单个网关的**路由**数量不能超过%s，当前数量为%s | 🔴 `%s` 占位 |
| `Conflict.ServiceQuotaPerGatewayExceed` | 单个网关的**服务**数量不能超过%s，当前数量为%s | 🔴 `%s` 占位 |
| `Conflict.DomainQuotaPerGatewayExceed` | 单个网关关联**域名**数量不能超过%s，当前数量为%s | 🔴 `%s` 占位 |
| `Conflict.GatewayEnvironmentLimitExceeded` | 每个网关关联的**环境**不应超过%s个，当前为%s个 | 🔴 `%s` 占位 |
| `Conflict.K8sServiceSourceLimitExceeded` | 单个网关的 **K8s 服务来源**数量不能超过%s，当前数量为%s | 🔴 `%s` 占位 |
| `Conflict.PluginCountExceed` | 插件数量超过配额，当前插件数量为%s个 | 🔴 `%s` 占位 |

🔴 **这是本章最重要的文档级空白**：9 类配额全部是 `%s` 占位符，**错误码页不给数值，只告诉客户「请提升您的配额」**。这些正是容量规划的核心数字（每网关多少路由/服务/域名/环境/接口、每 API 多少 Operation、每地域多少接口、每网关多少插件）。SA 做规模评估时**必须去配额中心或提工单核验，不能引用本页**。（配额数值可能在 W1 的规格与配额页，本章 raw 内确实没有。）

**G. 其他 409（硬编码数值，可直接引用）**

| 错误码 | 描述（照抄） | 🔴 硬数值 |
|---|---|---|
| `Conflict.SecurityGroupRulesLimitExceeded` | 网关的安全组规则数量不能超过 5 条（错误信息：`The security group rule ports count cannot be greater than 5.`） | **5 条** |
| `Conflict.ServiceSourceUpdateIsDisabled` | **仅允许修改 K8s 类型的服务来源** | — |
| `Conflict.ServiceUpdateIsDisabled` | **仅允许修改 DNS 和固定地址类的服务** | — |
| `Conflict.RouteBackServiceProtocolNotSupported` | 路由暂时不支持服务协议%s | — |
| `Conflict.PluginWasmFileIllegal` | 插件 WASM 文件非法，文件名为%s | — |
| `Conflict.Fc2NotSupported` | **FC 集成方案已升级，请重新创建 FC 服务后再发布 API/路由** | — |
| `Conflict.OssRequestError` | 访问 OSS 失败，请检查参数配置或您的账户 RAM 权限 | — |
| `Conflict.DebugRequestFailed` | 创建调试请求失败，请检查您的配置，请求URL为：%s | — |
| `Conflict.GatewayNotSupportAutoMaintenance` | 该网关不支持自动维护时间窗口配置 | — |
| `InvalidParameter.EnvironmentAliasLengthExceedUpLimit` | 当前环境别名长度为%s，**至多应不超过 50 个字符** | **50 字符** |

🔴 **`Conflict.ServiceSourceUpdateIsDisabled` / `Conflict.ServiceUpdateIsDisabled` 是设计行为而非 bug**：服务来源只有 K8s 类型可改，服务只有 DNS 和固定地址类可改。客户报「为什么我的服务改不了」时，这是标准答案。[官方｜api-apig-2024-03-27-errorcodes]

🔴 **状态码归类异常**：`InvalidParameter.EnvironmentAliasLengthExceedUpLimit` 被归在 **409**，而其余 22 个 `InvalidParameter.*` 全部归在 **400**。**按前缀判断状态码会误判这一条。**[官方｜api-apig-2024-03-27-errorcodes]

#### 13.5.2 400 参数类（23 条，含 4 个硬编码长度上限）

🔴 **可直接引用的硬编码数值**：

| 错误码 | 描述（照抄） | 硬数值 |
|---|---|---|
| `InvalidParameter.ConsumerNameExceedLimit` | 消费者名称长度不能超过 **64 个字符**，现在 %s（错误信息：`Consumer name length can not exceed 64 characters, now %s.`） | **64 字符** |
| `InvalidParameter.DomainNameExceedLimit` | 域名长度为%s，超过长度限制，**最大允许的域名长度为 128 位** | **128** |
| `InvalidParameter.EnvironmentAliasLengthExceedUpLimit`（**归 409**） | 当前环境别名长度为%s，至多应不超过 **50 个字符** | **50 字符** |
| `Conflict.SecurityGroupRulesLimitExceed`（409，见上） | 网关的安全组规则数量不能超过 **5 条** | **5 条** |

**其余 400 类错误码（按主题归纳）**：

| 主题 | 错误码 | 描述要点（照抄） |
|---|---|---|
| 消费者凭证长度 | `InvalidParameter.ConsumerAkLengthExceed`、`InvalidParameter.ConsumerSkLengthExceed`、`InvalidParameter.ConsumerApiKeyLengthExceed` | 消费者 AK / SK / ApiKey 长度超限，「不能超过%s，当前%s」——🔴 **三个上限值全是 `%s` 占位，未给数值** |
| 命名格式 | `InvalidParameter.ConsumerNameStartOrEndFormatIllegal` | 消费者名称**必须以字母或者数字开头或者结尾** |
| 命名格式 | `InvalidParameter.EnvironmentFormatIllegal` | 环境名称「应当**仅包含字母，数字，点号与中划线**」 |
| 命名格式 | `InvalidParameter.EnvironmentNameStartOrEndFormatIllegal` | 环境名称「应当以**字母和数字**作为环境名称的开头与结尾」 |
| 命名格式 | `InvalidParameter.EnvironmentAliasStartOrEndFormatIllegal` | 环境别名「应当以**字母或汉字**作为环境别名的开头」（错误信息：`must start with an alphanumeric or Chinese character`） |
| 必填/参数解析 | `InvalidParameter.IsEmpty` | 必填参数为空（`Required parameter should not be empty.`） |
| 必填/参数解析 | `InvalidParameter.FailToBindBody` | 解析请求内容失败，请检查参数数据类型是否有误 |
| 必填/参数解析 | `InvalidParameter.WithDetail` | 无效的请求参数 |
| 必填/参数解析 | `InvalidParameter.BothEmpty` | **ResourceId 和 Tag 均未提供**（错误信息：`Parameter ResourceId and Tag should not both be empty. At least one must be provided.`）→ 对应 `TagResources`/`UntagResources`/`ListTagResources` |
| API 类型 | `InvalidParameter.HttpApiTypeNotSupported` | HTTP API 类型%s不支持 |
| API 类型 | `InvalidParameter.RouteConfigHostnamesIsEmpty` | 参数不合法，**域名列表不能为空** |
| API 定义导入 | `InvalidParameter.OasSpecParseFailed` | OpenAPI 定义解析失败，失败原因为：%s |
| API 定义导入 | `InvalidParameter.SwaggerSpecParseFailed` | Swagger 定义解析失败，失败原因为：%s |
| 后端服务 | `InvalidParameter.HttpTriggerRequired` | 函数%s/%s **没有配置 HTTP 触发器**，无法作为 API 和路由的后端服务，请为函数添加 HTTP 触发器 |
| 规格变更 | `InvalidParameter.InvalidGatewaySpecification` | **升配或降配的配置不合法**，请重新选择 |
| 策略类型 | `InvalidParameter.PolicyNotSupportedType` | %s 不是被支持的**全局策略**类型 |
| 日志投递 | `CloudProductInactive.LogDeliveryNotEnabled` | **网关未开启 SLS 日志投递功能**（`SLS log delivery configuration is not enabled.`） |
| 兜底 | `InternalError` | 🔴 见下方矛盾说明 |

🔴 **[官方矛盾] `InternalError`（HTTP 400）的错误信息与描述互相矛盾**：
- 错误信息：`The request processing has failed due to some unknown error.`（请求处理因未知错误失败）
- 描述：**「参数值大小写不匹配」**
两者语义完全不对应；且该码名为 `InternalError` 却归在 **400**（客户端错误），与 `APIG.ErrorCode.InternalError`（**500**，描述「系统内部错误」）命名撞车。**不裁决，交主控。**实操影响：客户拿到 400 + `InternalError` 时，按错误信息会以为是服务端问题，按描述应检查参数大小写。[官方｜api-apig-2024-03-27-errorcodes]

🟠 **`CloudProductInactive.LogDeliveryNotEnabled` 与 §10 强关联**：这是「调用某个 OpenAPI 时报未开日志投递」的错误码，正好印证 §10.1「所有可观测能力都建立在开启 SLS 日志投递之上」。[推断] 由本错误码描述 + `view-gateway-monitoring-data`/`ai-observable` 的前提条件推出；raw 未说明具体哪些 Action 会返回该码。

#### 13.5.3 403 权限类（3 条，全部列出）

| 错误码 | 错误信息 | 描述（照抄） |
|---|---|---|
| `APIG.ErrorCode.Forbidden` | `Not allowed to perform the operation.` | 操作禁止，**无操作权限** |
| `Forbidden.AccessDenied` | `Not allowed to perform the operation.` | **没有权限执行该操作** |
| `CodeupService.NotAuthorized` | `The caller has not authorized APIG to access Codeup, or no Codeup organization exists. Please authorize APIG to access your Codeup account and ensure at least one Codeup organization is created before calling this API.` | 调用方**未授权 APIG 访问云效 Codeup**，或账号下**不存在 Codeup 组织** |

[官方｜api-apig-2024-03-27-errorcodes]

🔴 **`APIG.ErrorCode.Forbidden` 与 `Forbidden.AccessDenied` 的错误信息完全相同**（都是 `Not allowed to perform the operation.`），描述也几乎相同。→ **脚本无法靠 message 区分这两个码，只能靠 code**；且官方未说明二者的触发条件差异（例如一个是 RAM 策略拒绝、一个是资源级条件不匹配）→ [文档未说明]。
🟠 `CodeupService.NotAuthorized` 揭示了一条隐含依赖：**AI 网关有对接云效 Codeup 的能力，且需要单独授权 + 账号下至少存在一个 Codeup 组织**。该能力在本章 raw 内无其他说明（疑与 W6 插件开发/WebIDE 相关）。[官方｜api-apig-2024-03-27-errorcodes]

#### 13.5.4 404 未找到类（13 条）

| 错误码 | 描述（照抄） |
|---|---|
| `NotFound.GatewayNotFound` | 您所查询的网关实例不存在，实例ID：%s |
| `NotFound.GatewayVersionNotConfig` | 未找到网关版本的配置 |
| `NotFound.EnvironmentNotFound` | 环境%s不存在，请检查请求参数 |
| `NotFound.ServiceNotFound` | 未找到指定的服务，ID为%s |
| `NotFound.ServiceSourceNotFound` | 未找到指定的服务来源，ID为%s |
| `NotFound.ServiceVersionNotFound` | 服务版本 %s 未找到，请确认服务版本名称正确 |
| `NotFound.CsClusterNotFound` | 容器服务集群%s不存在，请检查配置 |
| `NotFound.SAEK8SServiceNotFound` | SAE K8S Service %s不存在，命名空间为%s |
| `NotFound.ConsumerAuthorizationRule` | 查询的消费者授权规则不存在（`The ConsumerAuthorizationRule '%s' does not exist under Consumer '%s'.`） |
| `NotFound.ExternalResponseNotFound` | **创建 MSE_NACOS 服务来源时，指定的 Nacos 实例不存在或当前地域不可访问**（错误信息：`The request to the external API failed`） |
| `DatabaseError.RecordNotFound`（第 1 处） | **配额规则 ID 不存在或已被删除**（错误信息：`The specified QuotaRule '%s' does not exist.`） |
| `DatabaseError.RecordNotFound`（第 2 处） | 请求引用的记录不存在：**迁移任务关联的后端记录不可用，请先确认任务与集群状态**（错误信息：`Record not found.`） |
| `ApiReplaced.UseUpdateAuthorizationRule` | 🔴 见下方矛盾说明 |

🔴 **`DatabaseError.RecordNotFound` 是「一码多义」**：同一错误码在表中出现两次，错误信息与描述都不同（一次指配额规则 ID 不存在，一次指迁移任务后端记录不可用）。**脚本无法靠该码定位具体资源类型，必须同时解析 message。**[官方｜api-apig-2024-03-27-errorcodes]

🔴 **[官方矛盾] `ApiReplaced.UseUpdateAuthorizationRule`（404）指向一个概览页不存在的 Action**：
- 错误码页描述：「该 API 已废弃并被替代，请改用 **UpdateAuthorizationRule**（`PUT /v1/authorization-rules/{consumerAuthorizationRuleId}`）」
- 错误信息原文：`This API has been deprecated and replaced. Please use UpdateAuthorizationRule at /v1/authorization-rules/{customerAuthorizationRuleId} instead.` **[原文如此：错误信息中为 `customerAuthorizationRuleId`，描述中为 `consumerAuthorizationRuleId`，两处拼写不一致]**
- 但 W7 在 `api-apig-2024-03-27-overview-ai-gateway` 全文检索 **`UpdateAuthorizationRule` = 0 次命中**；概览页 140 个 Action 中只有 **`UpdateConsumerAuthorizationRule`**（消费者管理分组）。
→ **官方让客户改用的 Action 名在 OpenAPI 概览页查不到**，且路径参数名两处拼写不一致。**不裁决，交主控。**实操影响：客户按错误提示调用 `UpdateAuthorizationRule` 可能直接失败，应改用 `UpdateConsumerAuthorizationRule`（此为 W7 推断，需实测确认）。

#### 13.5.5 500 服务端类（5 条，全部列出）

| 错误码 | 错误信息 | 描述（照抄） |
|---|---|---|
| `APIG.ErrorCode.InternalError` | `Internal error.` | 系统内部错误 |
| `ServiceInternalError.UnknownError` | `An unknown error occurred. Please submit a ticket to contact an engineer for processing.` | **未分类的服务端内部错误兜底码，响应不区分具体失败原因** |
| `ServiceInternalError.FailToRequestCs` | `Request to cs failed` | 请求容器服务集群失败，**网关无法访问指定的 K8s 集群** |
| `ServiceInternalError.CreateMigrationTaskFailed` | `api type not match` | 创建迁移任务时指定的 httpApiId **不是 HttpIngress 类型的 API** |
| `GatewayIsDeleted.GetMigrationNamespacedServicesFailed` | `The gateway associated with migration task has been deleted. Please create a new migration task with an active gateway.` | **迁移任务关联的网关已被删除**，请使用处于正常状态的网关重新创建迁移任务 |

[官方｜api-apig-2024-03-27-errorcodes]

🟠 **对 SA 的结论**：500 类里有 **2 条与「迁移任务」相关**（`CreateMigrationTaskFailed`、`GetMigrationNamespacedServicesFailed`），且都限定 HttpIngress 类型 → 说明存在一条**从 Nginx Ingress 迁移到 AI 网关的 OpenAPI 迁移任务能力**，但**这 3 个迁移相关 Action 在概览页 140 个 Action 中均未出现**。[推断] 由两条 500 错误码描述提到「迁移任务」+ W7 对概览页的 Action 全量检索无 `*Migration*` 推出。→ **迁移任务能力有错误码但无 OpenAPI 文档**，属文档级空白，客户问「怎么用 API 做 Ingress 迁移」时无法回答。

### 13.6 OpenAPI 变更集（`api-apig-2024-03-27-changeset-ai-gateway`）

**共 7 条变更记录，时间跨度 2026-01-23 ~ 2026-03-25**（快照抓取日 2026-09-21，即最近一条变更距抓取日约 6 个月）。表结构：OpenAPI 名称 / 变更内容概要 / 操作（两个外链：「查看变更详情」带 `updateTime` 参数、「查看API文档」）。

| 变更时间 | OpenAPI 名称 | 变更内容概要（照抄） | 🔴 对自动化脚本的破坏性 |
|---|---|---|---|
| **2026-03-25** | `ImportHttpApi` | **OpenAPI 返回结构发生变更** | 🔴 **高**——解析返回体的脚本可能崩 |
| **2026-03-16** | `ListPluginAttachments` | API 内部配置变更，**不影响调用** | 低 |
| **2026-02-11** | `CreateHttpApi` | API 内部配置变更，**不影响调用** | 低 |
| **2026-02-09** | `DeployHttpApi` | API 内部配置变更，**不影响调用** | 低 |
| **2026-01-30** | `CreateService` | **OpenAPI 入参发生变更** | 🔴 **高**——请求体构造可能失败 |
| **2026-01-30** | `CreateHttpApiRoute` | API 内部配置变更，**不影响调用** | 低 |
| **2026-01-23** | `GetConsumer` | **OpenAPI 返回结构发生变更** | 🔴 **高**——解析返回体的脚本可能崩 |

[官方｜api-apig-2024-03-27-changeset-ai-gateway]

🔴 **对写自动化脚本的客户，3 条是硬坑（照抄原文口径）**：
1. **返回结构变更 × 2**：`ImportHttpApi`（2026-03-25）、`GetConsumer`（2026-01-23）。
2. **入参变更 × 1**：`CreateService`（2026-01-30）。
3. 其余 4 条官方明确标注「**API 内部配置变更，不影响调用**」，可忽略。

🟠 **变更集中在两条主线上**：① **消费者体系**（`GetConsumer` 返回结构变更，且 §11 门户服务正好依赖 `apig:*Consumer*`）；② **服务与 API 创建链路**（`CreateService` 入参、`CreateHttpApi`、`CreateHttpApiRoute`、`DeployHttpApi`）。[推断] 由上表 7 条的 Action 归类推出；raw 未说明变更主题。

🔴 **变更集的信息粒度不足（文档级空白）**：本页只给「返回结构发生变更」「入参发生变更」这类**概要**，**不列出具体新增/删除/改名的字段**，具体差异必须点进 `api.aliyun.com` 的「查看变更详情」外链（URL 带 `updateTime=2026-03-25` 一类参数）。→ **SA 无法从 raw 判断某次变更是否会破坏客户现有脚本**，只能引导客户自查变更详情页。
🔴 **另需注意**：`GetConsumer` 在 2026-01-23 发生返回结构变更，而 §11.3 的门户服务恰好依赖 `apig:*Consumer*` 权限调用消费者类接口——**门户镜像若固定用 `latest` 标签（见 §11.2），其 SDK 版本与 OpenAPI 返回结构的兼容性无从验证**。此为 [推断]，raw 未讨论二者的版本耦合。

### §13 溯源

- `api-apig-2024-03-27-overview-ai-gateway` — AI网关OpenAPI概览（35490 B，全文读取并脚本化逐组计数）：13.1 全节——ROA 签名风格、SDK「常见编程语言」口径、自签名 5 个工作日与钉钉群 147535001692、AccessKey 与最小权限原则（PoLP）基线、**16 个分组共 140 个 Action 的逐组计数与全量 Action 名**、「其他」分组 42 个 Action 的 8 类主题拆解、`ImportHttpApi` 仅导入为 REST 类型的边界、`UpdateService` 的可更新范围、`GetGatewayQuotaRuleSubjectUsage` 的返回内容、`DescribeRegions` 的语义。
- `api-apig-2024-03-27-endpoint-ai-gateway` — APIG 服务接入点（5841 B，逐行解析）：13.2 全节——公网/VPC 域名格式、三张分区表合计 25 个地域、19 个有 VPC 接入地址、6 个无（含 `ap-southeast-2` 悉尼「已关停」标注）、19 个有 VPC 接入点的 regionId 清单。
- `api-apig-2024-03-27-quota-ai-gateway` — APIG OpenAPI 流控配额（34173 B，逐行解析 105 行）：13.3 全节——105 个 Action 有配额条目、API版本全为 2024-03-27、地域全为 `*`、限速维度全为 `regionId,API,ParentUid`、配额分布（`30/1(s)`×46、`50/1(s)`×25、`60/1(s)`×32）、读/写拆分（写 64 / 读 41）、两个例外项 `UpdatePluginAttachment` `60/60(s)` 与 `GetPluginAttachment` `60/3000(s)`、MCP 与密钥类统一 `50/1(s)`、**35 个 Action 无配额条目的缺口清单**。
- `api-apig-2024-03-27-ram-ai-gateway` — AI网关-RAM授权信息（56328 B，全文读取并脚本化逐行解析三张表）：13.4 全节——RamCode `apig`、授权粒度「资源级」、**Action 表 140 行**（与概览页双向差集为 0）、访问级别分布（none 96 / get 12 / list 9 / create 9 / delete 8 / update 6）、**资源类型分布（全部资源 66 / Gateway 22 / HttpApi 18 / Domain 18 / Service 7 / Environment 5 / Policy 3 / Source 1）**、66 个「全部资源」Action 清单、Domain 组内 ARN 实际分布（consumer 9 / secret 4 / domain 5）、条件关键字仅 2 个（`apig:GatewayId`、`apig:NetworkType`，均 Array）且仅 2 个 Action 引用 `apig:GatewayId`、`apig:NetworkType` 零引用、关联操作 140 行全为「无」、资源 ARN 表 8 类全文、ARN 变量与 `*` 语义、四处官方文档缺陷、访问级别说明文字与表格取值的口径冲突。
- `api-apig-2024-03-27-errorcodes` — AI 网关公共错误码（43253 B，全文读取并脚本化逐行解析 111 行）：13.5 全节——按状态码分布（409×67 / 400×23 / 404×13 / 500×5 / 403×3）与前缀分布（Conflict 66 / InvalidParameter 22 / NotFound 10 / 其余 9 类）、409 的七个子类归纳（名称版本重复 / 路径发布冲突 / 授权冲突 / 状态机 / 删除保护 / 配额超限 / 硬编码数值）、9 类配额全为 `%s` 占位、4 个硬编码上限（消费者名 64 字符、域名 128、环境别名 50 字符、安全组规则 5 条）、`InternalError` 的信息与描述矛盾、`InvalidParameter.EnvironmentAliasLengthExceedUpLimit` 归 409 的异常、两个 403 码 message 完全相同、`DatabaseError.RecordNotFound` 一码两义、`ApiReplaced.UseUpdateAuthorizationRule` 指向概览页不存在的 Action、500 类中两条迁移任务错误码。
- `api-apig-2024-03-27-changeset-ai-gateway` — APIG OpenAPI 变更集（4794 B，全文读取）：13.6 全节——7 条变更的完整时间表与概要原文、3 条破坏性变更（`ImportHttpApi` 与 `GetConsumer` 返回结构变更、`CreateService` 入参变更）、4 条「不影响调用」、变更集不给字段级差异。

**本章查无**：
1. 🔴 **9 类资源配额的具体数值**（每网关的路由/服务/域名/环境/接口/在线接口/K8s服务来源/插件数量上限、每 API 的 Operation 上限、每地域的接口总量上限）——错误码页全部用 `%s` 占位；配额数值可能在 W1 的规格与配额页，本章 raw 内确实没有。
2. 🔴 **消费者 AK / SK / ApiKey 的长度上限**——三个错误码全是 `%s` 占位。
3. **SDK 支持的具体编程语言与版本**——概览页只说「常见编程语言」并给下载外链。
4. **配额记法 `N/M(s)` 的官方定义**——页面未解释，本章按阿里云通用记法做了 [推断] 并标注。
5. **35 个无流控配额条目的 Action 的实际限流值**——尤其 FinOps 配额规则、AI 模型元信息、消费者组三类新能力，客户无法预知频率上限。
6. **RAM 最小权限策略模板**——RAM 页只有元数据表，无只读/运维/管理员等角色样板（raw 内唯一样板来自 §11.3 门户服务）。
7. **`apig:NetworkType` 条件关键字的可用范围与取值枚举**——定义了但零 Action 引用，「网络类型」具体指什么（公网/私网？入站/出站？）[文档未说明]。
8. **访问级别为 `none` 的 96 个 Action 究竟是读还是写**——官方说明称取值为 Write/Read/List，但表内 68.6% 为 `none`（见 13.4.2 [官方矛盾]）。
9. **`UpdateAuthorizationRule` 这个 Action 是否存在**——错误码页让客户改用它，概览页 140 个 Action 中查无（见 13.5.4 [官方矛盾]）。
10. **迁移任务（Migration Task）相关的 OpenAPI**——500 类错误码提到「创建迁移任务」「迁移任务关联的网关」，但概览页无任何 `*Migration*` Action，能力入口[文档未说明]。
11. **`Forbidden.AccessDenied` 与 `APIG.ErrorCode.Forbidden` 的触发条件差异**——两者 message 完全相同，官方未区分。
12. **变更集的字段级差异**——只有「返回结构发生变更」「入参发生变更」概要，具体增删改字段需点外链，raw 内无内容。
13. **OpenAPI 的地域可用性差异**——接入点表列了 25 个地域，但**哪些 Action 在哪些地域可用**（例如 AI 网关专属 Action 是否全地域开放）：[文档未说明]。
14. **`DescribeRegions` 的返回结构**——它是判断地域可用性的唯一 Action，但入参/返回在 raw 内[文档未说明]。
15. **云效 Codeup 集成能力**——`CodeupService.NotAuthorized` 揭示存在该集成（疑与 W6 插件开发相关），本章 raw 内无任何功能说明。
16. **OpenAPI 是否支持 AI 网关专属对象**——概览页 140 个 Action 中**没有 Model API / Agent API / AI 服务 / AI 日志策略 / 链路追踪配置**的专属 Action（只有通用的 HttpApi/Service/Policy/Plugin 抽象）；「用 OpenAPI 管理 Model API」的映射关系[文档未说明]（W5 有「OpenAPI 管理 MCP」页，可交叉）。
