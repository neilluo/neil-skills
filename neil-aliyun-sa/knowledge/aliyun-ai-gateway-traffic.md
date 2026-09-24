# AI 网关 · §4 核心对象模型 / §5 流量治理与成本控制

> **所属**：[[aliyun-ai-gateway]] 专题页家族（7 文件）｜**主页与导航**：[aliyun-ai-gateway.md](aliyun-ai-gateway.md)
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（186 个快照 = 149 个有正文页 + 37 个 TOC 容器页；另有 SLA 协议全文外部源 1 页）
> **事实标注体系**：`[官方｜slug]` raw 快照有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方原文错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕见 `tests/ai-gateway-rulings-2026-09-21.md`
>
> 🔖 正文中的 `W1`~`W7` 是**本次蒸馏批次的分工代号**（7 路并行 worker），不是产品术语；对照表见 [主页 §0.6](aliyun-ai-gateway.md)。

🔴 **对客纪律**：限流超限的返回码 —— **限流专页确实未写，但 `custom-response-plugin` 页明文「触发网关限流时一般会返回429状态码」并给了自定义应答样例** → 对客可答 429（须说明出处与「是否对全部限流单位一律成立」官方未说明）；**FinOps 配额超限的返回码仍查无，不可把 429 类推过去**；Token 计量口径的 7 个子问题全部空白；语义缓存无 TTL 配置项。客户问「限流了返回什么」「Token 怎么算」时，先答空白再给实测建议，不要拿邻近机制类推。

## §4 核心对象模型

### 4.1 对象层级与依赖顺序（必须先有什么才能建什么）

AI 网关的资源对象是**实例内的分层引用关系**：实例 →（域名 / 供应商 → 模型元信息 / 服务来源 → 服务）→ Model API →（默认路由 + 自定义路由）→ API 产品 → 产品分类。

| 序号 | 对象 | 硬前提（官方明文） | 来源 slug |
|---|---|---|---|
| 1 | **实例** | 一切对象的容器；跨 VPC 的服务来源必须「重新创建指定VPC下的网关实例」 | creating-services |
| 2 | **服务来源**（ACK / MSE Nacos） | 「您在创建网关时需要选择和后端集群相同的VPC，那么服务来源添加时会自动获取该VPC下的集群」；「云原生API网关只能添加同VPC内的Nacos或者ACK，不支持跨VPC添加服务来源」[原文如此，本页为 AI 网关文档] | create-a-service-source、creating-services |
| 3 | **服务**（8 类来源） | DNS 域名与固定地址服务「无需配置服务来源即可添加」；ACK / Nacos / SAE 类服务必须先有对应服务来源 | create-a-service-source、creating-services |
| 4 | **供应商 Provider** | 「已创建网关实例」；「除上述条件外，管理供应商无需额外的 RAM 权限、实例规格或地域限制」 | manage-providers |
| 5 | **模型元信息** | 「已创建网关实例」+「当前实例下至少有一个可用供应商（预置供应商或自定义供应商）。如没有，请先管理供应商」；「如当前实例内无可用供应商，无法创建模型，需先创建供应商或启用预置供应商」 | model-metadata |
| 6 | **域名** | Model API 必填项之一；「域名与基本路径 `BasePath` 的组合必须唯一」；「如果还没有域名，请单击右侧 **添加域名** 按钮完成创建」 | managing-the-model-api、manage-the-ai-api |
| 7 | **Model API** | 建议（非强制）先注册供应商、添加模型：「创建 Model API 不强制绑定供应商下的模型资源。如未提前添加模型，创建时可直接输入模型名称字符串」；「确认已拥有可用的 AI 网关实例」 | manage-the-ai-api |
| 8 | **自定义路由** | 挂在 Model API 详情页「路由列表」下；「删除操作仅支持删除未发布或已下线的路由，如需删除已发布路由，请先完成下线路由操作」 | route-list |
| 9 | **API 产品** | 「已创建 Model API」+「已创建开发者门户」；「API 产品必须关联具体的 AI API 后才能发布到门户」 | create-an-api-product-of-the-model-api-type |
| 10 | **产品分类** | 与 API 产品多对多关联；在开放平台管理控制台创建 | product-category-management |

**跨对象的连带前提（避坑重点）**

| 能力 | 官方明文前提 | 来源 slug |
|---|---|---|
| AI Fallback | 「已创建网关实例」+「已创建服务」 | ai-fallback |
| 智能路由 | 「已创建 AI 网关实例，并具备该实例的 Model API、AI 服务和模型元信息配置权限」；「智能路由需要单独开通……功能未开通时，无法完成智能路由配置」；「已为自定义模型创建可用的 AI 服务」；「已维护模型元信息」；「智能路由 Model API 默认启用消费者鉴权，且在服务类型为智能路由时不能关闭」 | configure-smart-routing |
| 多服务（按观测指标）/ 多模型服务（智能路由） | 「需要将AI网关版本升级至`2.1.15`及以上」 | managing-the-model-api、manage-the-ai-api |
| 按消费者限流 | 「配置按消费者限流，需要先开启消费者认证」；OpenAPI 侧：「需要先为该 Model API 开启消费者认证。否则限流策略无法识别消费者身份，规则不会生效」 | current-limiting、configure-a-modelapi-throttling-policy |
| 消费者配额（FinOps） | 「引擎版本为2.1.19及以上，如需使用 Credits 配额能力，请升级至2.1.20及以上」；「网关实例的版型不能是旧版本 Serverless 规格」；「已创建消费者」；「已开通 SLS 日志服务并开启日志投递（用于查看用量统计）」 | consumer-quotas-management |
| 被动健康检查 | 「需将引擎版本提升至2.1.10及以上版本」 | configure-service-health-checks |
| AI 请求观测（Logging / Tracing） | 「Logging 与 Tracing 依赖 SLS 日志投递服务」 | managing-the-model-api、manage-the-ai-api |
| 语义缓存 | 需已开通向量检索服务 DashVector；「创建Collection时距离度量方式选择`Cosine`，向量维度要与文本向量化模型的维度对应」 | ai-cache-1 |
| 精确缓存 | 「请前往Redis控制台添加白名单。在Redis控制台中，您需要将网关实例的VPC网段添加至白名单」 | ai-cache-1 |
| 联网搜索 | 需开通阿里云信息查询服务；「首次使用夸克联网搜索时，默认**服务状态**为**未开通**状态」 | networked-search |
| 公网后端（如百炼 DashScope） | 「AI 网关部署在 VPC 内，默认不具备公网出访能力。若后端服务为公网地址（如百炼 DashScope），需在网关所在 VPC 创建公网 NAT 网关，创建 VPC 粒度的 SNAT 条目并绑定弹性公网 IP」；「云企业网（CEN）用于 VPC 间互联，无法替代公网出访。百炼等公网 API 服务不在 VPC 内，不能通过 CEN 访问」 | configure-service-health-checks、creating-services |

### 4.2 Model API：创建参数与取值范围

> 「Model API适用于面向人工智能应用开发的团队，提供了更加灵活和智能的AI网关配置和调试能力。它可以用于各种AI代理、AI观测、消费者鉴权、内容安全防护等插件的预置。」[官方原文｜managing-the-model-api]

**使用场景（7 种，决定协议可选项与系统自动创建的默认路由）**

| 场景 | 官方标注 | 来源 slug |
|---|---|---|
| 文本生成（Text） | 「支持 OpenAI 兼容协议和 Anthropic 协议」 | managing-the-model-api、manage-the-ai-api |
| 图片生成（Image） | — | 同上 |
| 视频生成（Video） | — | 同上 |
| 语音合成（Audio） | — | 同上 |
| 向量化（Embedding） | — | 同上 |
| 文本排序（Rerank） | — | 同上 |
| 其他（Others） | — | 同上 |

**基本信息配置项**

| 配置项 | 取值范围 / 默认值 / 约束 | 来源 slug |
|---|---|---|
| 协议 | 「不同协议对应该场景下的一组内置默认路由，用于快速生成常用的 OpenAI/DashScope/vLLM 等兼容接口」 | managing-the-model-api、manage-the-ai-api |
| API 名称 | 「名称必须全局唯一（同一账号下不可重复），支持英文、数字、下划线"_"、"-"，且不超过64个字符」 | 同上 |
| 域名 | 「支持选择多个。域名与基本路径 `BasePath` 的组合必须唯一」 | 同上 |
| Base Path | 「配置API的基本请求路径，默认为 `/`」；可选启用「转发至后端服务时移除」 | 同上 |
| AI 请求观测 | 「开启后可查看 Metrics、Logging、Tracing 信息」；可勾选「记录请求内容」与「记录响应内容」 | 同上 |
| 大模型服务 | 5 种服务类型，见下表 | 同上 |
| Fallback | 「可**开启**并按顺序配置多条 Fallback 策略（可复用同一服务）」 | 同上 |
| 首包超时 | 「单位为毫秒，设为0时表示不启用」 | 同上 |
| 资源组 | 「支持选择默认或已有资源组，也可新建。资源组用于对账户资源分组管理、授权与监控」 | 同上 |

**BasePath 移除语义（原文示例）**：「BasePath设置为 /api」+「原始请求路径 /api/users」→「实际转发到后端的路径变为 /users」[官方原文｜managing-the-model-api]

**⚠️ 协议影响 Token 统计口径（对客高频，与限流/配额计量直接相关）**

> 「协议转换可能会改变 Token 的统计结构。例如，阿里云百炼协议的 input token 统计会包含缓存 token（cache token），而 Anthropic 协议的 input token 统计不包含缓存 token。请在查看可观测指标时留意不同协议的统计口径差异。」[官方原文｜managing-the-model-api、manage-the-ai-api]

**大模型服务类型（5 种）**

| 服务类型 | 行为 | 版本/开通要求 | 来源 slug |
|---|---|---|---|
| 单模型服务 | 「选择 1 个 AI 服务，并可设置**模型名称**（可透传或改写）」；模型名称字段支持下拉选择模型资源或自定义输入 | — | managing-the-model-api、manage-the-ai-api |
| 多模型服务（按模型名称） | 「根据请求体中的模型名按规则匹配到不同服务；匹配规则支持通配符 `?` 与 `*`，例如 `qwen-*` 可匹配 `qwen-max`、`qwen-long`」 | — | 同上 |
| 多模型服务（按权重） | 「选择多个 AI 服务并设置权重，支持透传或改写模型名」 | — | 同上 |
| 多服务（按观测指标） | 「系统将根据各服务的响应时间、成功率等观测指标自动选择最优服务进行请求路由，无需手动配置权重」 | 「需要将AI网关版本升级至`2.1.15`及以上」 | 同上 |
| 多模型服务（智能路由） | 「系统将根据模型特征为请求自动选择最合适的模型」 | 「需要将AI网关版本升级至`2.1.15`及以上」；另「需要单独开通」（见 §5.2） | 同上、configure-smart-routing |

**模型资源 vs 模型名称字符串（弱绑定，重要选型事实）**

> 「选择模型资源仅用于提示用户当前实例内有哪些模型可选，并帮助快速填写模型名称。Model API 不强制绑定模型资源，最终以用户提交的模型名称字符串为准。用户直接输入一个不在模型资源列表中的模型名称时，允许保存。」[官方原文｜manage-the-ai-api]

配套事实：「编辑模型名称时，会影响 Model API 和路由中的模型名称候选展示」；「删除模型后从列表中移除，但不影响已保存的 Model API 和路由中的模型名称字符串（Model API 中以字符串方式存储的模型名称不会因模型资源删除而失效）」[官方原文｜model-metadata]

**调试 Model API（仅一条路径可用）**

| 项目 | 数值 / 范围 | 来源 slug |
|---|---|---|
| 可调试范围 | 「当前只支持文本生成的`/v1/chat/completions`调试」 | managing-the-model-api、manage-the-ai-api |
| System Prompt | 「系统提示词，上限 100 字符」 | 同上 |
| max_tokens | 「范围 0--8192，默认 1024」[原文如此，双连字符] | 同上 |
| top_p | 「范围 0--1，默认 0.95」 | 同上 |
| temperature | 「范围 0--2，默认 1，对结果影响较大，请谨慎调整」 | 同上 |
| 其他 | 可开启「流式请求」开关、自定义参数；右侧页签：模型返回 / CURL命令 / 原始输出 | 同上 |

**编辑 / 删除**：编辑入口为 Model API 列表操作列「编辑」；删除「在确认删除的弹框中输入API名称，然后单击**删除**」[官方｜managing-the-model-api]

**数据安全提示（原文）**：「启用后系统会记录所有 AI 请求内容（包括请求体 body）到访问日志，请妥善配置 SLS 并做好数据安全防护。」[官方原文｜managing-the-model-api、manage-the-ai-api]

### 4.3 默认路由（场景 × 协议 → 系统自动创建）

> 「在不同**使用场景**下选择不同**协议**时，系统将自动创建**默认路由**。」[官方原文｜managing-the-model-api]

| 场景 | 协议 | 路由名称 | 路径 | 方法 |
|---|---|---|---|---|
| 文本生成 | OpenAI 兼容（OpenAI/v1） | `create-chat-completion` | `/v1/chat/completions` | POST |
| 文本生成 | OpenAI 兼容（OpenAI/v1） | `create-completion` | `/v1/completions` | POST |
| 文本生成 | Anthropic（Anthropic） | `create-message` | `/v1/messages` | POST |
| 图片生成 | 阿里云百炼图片生成 | `dashscope-text-to-image-synthesis` | `/api/v1/services/aigc/text2image/image-synthesis` | POST |
| 图片生成 | 阿里云百炼图片生成 | `dashscope-image-to-image-synthesis` | `/api/v1/services/aigc/image2image/image-synthesis` | POST |
| 图片生成 | 阿里云百炼图片生成 | `dashscope-image-to-image-outpainting` | `/api/v1/services/aigc/image2image/out-painting` | POST |
| 图片生成 | 阿里云百炼图片生成 | `dashscope-virtual-model-generation` | `/api/v1/services/aigc/virtualmodel/generation` | POST |
| 图片生成 | 阿里云百炼图片生成 | `dashscope-background-generation` | `/api/v1/services/aigc/background-generation/generation` | POST |
| 图片生成 | 阿里云百炼图片生成 | `tasks` | `/api/v1/tasks` | GET/POST/PUT/PATCH/DELETE |
| 图片生成 | OpenAI 兼容 | `openai-image-generation` | `/api/v1/images/generations` | POST |
| 图片生成 | OpenAI 兼容 | `openai-image-edit` | `/api/v1/images/edits` | POST |
| 图片生成 | OpenAI 兼容 | `openai-image-variation` | `/api/v1/images/variations` | POST |
| 视频生成 | 阿里云百炼视频生成 | `dashscope-video-generation-synthesis` | `/api/v1/services/aigc/video-generation/video-synthesis` | POST |
| 视频生成 | 阿里云百炼视频生成 | `dashscope-image-to-video-synthesis` | `/api/v1/services/aigc/image2video/video-synthesis` | POST |
| 视频生成 | 阿里云百炼视频生成 | `tasks` | `/api/v1/tasks` | GET/POST/PUT/PATCH/DELETE |
| 语音合成 | 阿里云百炼语音合成 | `dashscope-text-to-audio-synthesis` | `/api-ws/v1/inference` | GET |
| 语音合成 | OpenAI 兼容（OpenAI/v1） | `openai-audio-speech` | `/api/v1/audio/speech` | POST |
| 向量化（Embedding） | OpenAI 兼容（OpenAI/v1） | `create-embedding` | `/v1/embeddings` | POST |
| 文本排序（Rerank） | 阿里云百炼文本排序 | `rerank` | `/api/v1/services/rerank/text-rerank/text-rerank` | POST |
| 文本排序（Rerank） | vLLM（vLLM） | `rerank` | `/v1/rerank` | POST |
| 其他（Others） | OpenAI 兼容（OpenAI/v1） | `models` | `/v1/models` | GET/POST/PUT/PATCH/DELETE |
| 其他（Others） | OpenAI 兼容（OpenAI/v1） | `files` | `/v1/files` | GET/POST/PUT/PATCH/DELETE |
| 其他（Others） | OpenAI 兼容（OpenAI/v1） | `batches` | `/v1/batches` | GET/POST/PUT/PATCH/DELETE |
| 其他（Others） | OpenAI 兼容（OpenAI/v1） | `fine-tuning` | `/v1/fine_tuning` | GET/POST/PUT/PATCH/DELETE |

全部来源：managing-the-model-api（默认路由章节，HTML `<table>` 逐格重排）

**ComfyUI 协议（图片生成场景）默认路由 25 条**（来源同上，逐格转录）

| 路由名称 | 路径 | 方法 |
|---|---|---|
| `comfyui-websocket` | `/ws` | GET |
| `comfyui-embeddings` | `/embeddings` | GET |
| `comfyui-extensions` | `/extensions` | GET |
| `comfyui-features` | `/features` | GET |
| `comfyui-models` | `/models` | GET |
| `comfyui-models-folder` | `/models/{folder}` | GET |
| `comfyui-workflow-templates` | `/workflow_templates` | GET |
| `comfyui-upload-image` | `/upload/image` | POST |
| `comfyui-upload-mask` | `/upload/mask` | POST |
| `comfyui-view` | `/view` | GET |
| `comfyui-view-metadata` | `/view_metadata/` | GET |
| `comfyui-system-stats` | `/system_stats` | GET |
| `comfyui-prompt` | `/prompt` | GET/POST |
| `comfyui-object-info` | `/object_info` | GET |
| `comfyui-object-info-class` | `/object_info/{node_class}` | GET |
| `comfyui-history` | `/history` | GET/POST |
| `comfyui-history-prompt-id` | `/history/{prompt_id}` | GET |
| `comfyui-queue` | `/queue` | GET/POST |
| `comfyui-interrupt` | `/interrupt` | POST |
| `comfyui-free` | `/free` | POST |
| `comfyui-userdata` | `/userdata` | GET |
| `comfyui-userdata-v2` | `/v2/userdata` | GET |
| `comfyui-userdata-file` | `/userdata/{file}` | GET/POST/DELETE |
| `comfyui-userdata-file-move` | `/userdata/{file}/move/{dest}` | POST |
| `comfyui-users` | `/users` | GET/POST |

**Anthropic 协议供应商范围（原文）**

> 「支持该协议的大模型供应商包括：阿里云百炼（Qwen）、Claude、月之暗面（Moonshot）、智谱 AI（ZhipuAI）等。以上供应商AI服务自动支持Anthropic协议，无需额外配置。」[官方原文｜managing-the-model-api]

> 「兼容性说明：对于支持Anthropic协议的大模型供应商（阿里云百炼、Claude、月之暗面、智谱 AI等），创建AI服务时会自动支持多种协议，包括OpenAI兼容协议和Anthropic协议，用户可根据需要选择合适的协议创建Model API。」[官方原文｜managing-the-model-api]

**[官方矛盾] fine-tuning 路径拼写**
- managing-the-model-api 默认路由表：「`fine-tuning` ｜ `/v1/fine_tuning` ｜ GET/POST/PUT/PATCH/DELETE ｜ Manage fine-tuning jobs。」（**下划线**）
- route-list 自定义路由：「Model API的自定义路由路径支持`/v1/chat/completions`、`/v1/completions`、`/v1/embeddings`和`/v1/fine-tuning`四种方式。」（**连字符**）
- 不裁决，交主控核。SA 抄路径给客户时极易踩错。

**[观察｜官方原文事实]** 文本生成 / 向量化 / 其他的 OpenAI 兼容默认路由前缀为 `/v1/...`，而图片生成、语音合成的 OpenAI 兼容默认路由前缀为 `/api/v1/...`（来源 managing-the-model-api 默认路由表）。两页均未解释该前缀差异。

### 4.4 自定义路由管理

> 「Model API 支持自定义路由，您可以按请求特征进行精细化路由的能力。」[官方原文｜route-list]

| 配置项 | 取值 / 约束 |
|---|---|
| 路由名称 | 自定义 |
| 路径 | 「支持`/v1/chat/completions`、`/v1/completions`、`/v1/embeddings`和`/v1/fine-tuning`四种方式」（仅 4 种） |
| 更多匹配规则 | 「如需创建多个相同路径的路由，需要对**方法（Method）**、**请求头（Header）**和**请求参数（Query）**进行配置，以区分不同路由」 |
| 服务模型 | 仅 2 种：「**单模型服务**：在同一个服务实例中只部署和运行一个模型」；「**多模型服务（比例）**：在同一个服务实例中部署和运行多个模型，并根据设定的比例分配资源和请求」 |
| 服务列表 | 「在服务列表中选择服务」 |
| Fallback | 「开启后可添加Fallback 服务，按照降序执行」；「Fallback服务支持重复使用同一个服务组建多条策略」 |

全部来源：route-list

**路由生命周期状态机（有决策含义）**：创建 → 编辑 → **发布路由** → **下线路由**（更多操作 > 下线）→ 删除。约束原文：「删除操作仅支持删除未发布或已下线的路由，如需删除已发布路由，请先完成下线路由操作。」[官方原文｜route-list]

**[对照事实]** 自定义路由的「服务模型」只有单模型 / 多模型（按比例）2 种，而 Model API 级别的「大模型服务」有 5 种（含按观测指标、智能路由）。route-list 未说明自定义路由能否使用智能路由或按观测指标 → [文档未说明]。

### 4.5 供应商（Provider）

> 「AI 网关通过供应商（Provider）资源标识和管理模型服务的提供方」[官方原文｜manage-providers]

| 类型 | 可编辑 | 可删除 | 引用关系 |
|---|---|---|---|
| 预置供应商 | 「系统内置，不可编辑和删除」 | 否 | 「可被模型和服务引用」 |
| 自定义供应商 | 「可编辑名称」 | 「可删除（需无引用）」 | 同上 |

| 项目 | 官方口径 |
|---|---|
| 入口 | 左侧导航「**模型元信息管理**」→「**供应商**」页签 |
| 创建参数 | 「名称｜必填。供应商的展示名称，**支持重名**」；「标识｜必填。由系统自动生成，**创建后不可编辑**，页面中为禁用态」 |
| 列表列 | 名称 / 标识（系统自动生成的唯一标识）/ 关联模型数（当前供应商绑定的模型数量）/ 更新时间 / 操作（查看、编辑、删除） |
| 删除拦截 | 「若供应商已被模型或服务引用，则禁止删除。弹窗将显示关联的模型或服务列表，请先前往对应页面解除引用后再执行删除」 |
| 与服务的关系 | 「创建或编辑服务时，可在**高级设置**中关联供应商」；「**高级设置**中的**供应商**字段与**供应商配置模版**为两个独立概念，不互相筛选、不互相继承配置」 |
| 权限 / 规格 / 地域限制 | 「除上述条件外，管理供应商无需额外的 RAM 权限、实例规格或地域限制」 |

全部来源：manage-providers

**[原文如此]** 「系统支持预置供应商，也可以创建自定义供应商，也可创建自定义供应商。」（原句重复，逐字保留）[manage-providers]

**智能路由视角下的供应商作用（原文）**：「在**模型元信息**的**供应商**页签中，找到该模型所属供应商，并使用**管理关联服务**将对应 AI 服务关联到该供应商」；「候选模型由"模型元信息 + 模型供应商 + 已关联的 AI 服务"共同确定。智能路由不会把名称相同但未关联服务、协议不匹配或元信息缺失的模型作为可用候选。」[官方原文｜configure-smart-routing]

### 4.6 模型元信息（Model Metadata）

> 「AI 网关使用模型元信息资源管理隶属于供应商的具体 AI 模型。您可以在 AI 网关实例中创建、编辑和删除模型，配置其 Credits 消耗、Token 上限、能力特性和可用路径等信息，使模型可用于 Model API 和路由配置。」[官方原文｜model-metadata]

**四组信息构成（原文）**：基础信息（「所属供应商、名称、信息来源 URL」）｜Credits 信息（「输入/输出/缓存 Token 消耗的 Credits 单价」）｜能力与性能（「最大输入/输出/总 Token 上限，输入/输出模态，能力特性」）｜可用路径（「模型支持的 API 路径和协议类型」）

**参数与取值范围**

| 分组 | 参数 | 必填 | 取值范围 / 默认值 |
|---|---|---|---|
| 基础信息 | 供应商 | 必填 | 「下拉展示当前实例内所有可用供应商（预置 + 自定义）。如无可用的供应商，无法创建模型并提示先创建供应商或启用预置供应商」 |
| 基础信息 | 模型名称 | 必填 | 「模型的展示名称」（长度限制 [文档未说明]） |
| Credits 信息 | 输入 Token 消耗 | 选填 | 「单位 Credits/1M tokens，如填写必须为大于等于 0 的数字，最多两位小数。**默认值为 0**」 |
| Credits 信息 | 输出 Token 消耗 | 选填 | 同上，「**默认值为 0**」 |
| Credits 信息 | 缓存 Token 消耗 | 选填 | 同上，「**默认值为 0**」 |
| 能力与性能 | 最大输入 Token | 选填 | 「如填写必须为大于等于 0 的整数」 |
| 能力与性能 | 最大输出 Token | 选填 | 「如填写必须为大于等于 0 的整数」 |
| 能力与性能 | 总 Token 上限 | 选填 | 「如填写必须为大于等于 0 的整数」 |
| 能力与性能 | 输入模态 | 选填 | 「多选，可选值：text、image、audio、video」 |
| 能力与性能 | 输出模态 | 选填 | 「多选，可选值：text、image、audio、video」 |
| 可用路径 | 路径 | 必填 | 「必须以 `/` 开头。例如 `/v1/chat/completions`。同一模型内可用路径不建议重复」；可「添加路径」多条 |
| 可用路径 | 协议类型 | 必填 | 「可选：OpenAI Compatible、Anthropic Compatible、Custom」 |

全部来源：model-metadata

**使用限制（原文逐条）**：「路径必须以 `/` 开头」｜「同一模型内的可用路径不建议重复」｜「Credits 消耗参数如填写，必须为大于等于 0 的数字，最多两位小数」｜「如当前实例内无可用供应商，无法创建模型，需先创建供应商或启用预置供应商」[model-metadata]

**能力特性 15 项（完整枚举，列表页「能力」列即以 15 为分母）**

| # | 能力特性 | 官方释义 | # | 能力特性 | 官方释义 |
|---|---|---|---|---|---|
| 1 | 系统消息 | 支持 System Prompt | 9 | 视觉理解 | 支持 Vision |
| 2 | 结构化输出 | 支持 Structured Output | 10 | 图像 Embedding | 支持 Image Embedding |
| 3 | 函数调用 | 支持 Function Calling | 11 | 流式输出 | 支持 Streaming Output |
| 4 | 工具选择 | 支持 Tool Choice | 12 | 并行函数调用 | 支持 Parallel Function Calling |
| 5 | 前缀补全 | 支持 Prefix Completion | 13 | 联网搜索 | 支持 Web Search |
| 6 | Prompt 缓存 | 支持 Prompt Cache | 14 | 推理模式 | 支持 Reasoning |
| 7 | 计算机操作 | 支持 Computer Use | 15 | URL 上下文 | 支持 URL Context |
| 8 | PDF 输入 | 支持 PDF Input | | | |

来源：model-metadata（「能力特性」表 + 列表列说明「模型已启用的能力特性数量与全部可选能力特性数量（15 项）的比值，如 5/15」，两处 15 项一致）

**列表页列**：模型名称 / 单价（「输入、输出、缓存 Credits 单价（Credits/1M tokens）」）/ 总 Token 上限 / 能力（如 5/15）/ 供应商 / 更新时间 / 操作（查看、编辑、删除）[model-metadata]

**智能路由对元信息的依赖（原文，选型必读）**

> 「模型元信息不是静态备注。若上游模型的名称、上下文长度、支持的协议、工具调用能力或价格发生变化，但实例内元信息没有同步更新，可能导致模型不能进入候选池，或影响自动选择结果。」[官方原文｜configure-smart-routing]

| 元信息项 | 官方「维护要求和作用」 |
|---|---|
| 模型名称和模型供应商 | 「名称应与 AI 服务实际调用的模型一致；供应商应与模型所属供应商一致，用于将模型与正确的服务关联」 |
| Credits 单价 | 「维护输入、输出和缓存 Token 的价格信息，使成本相关的优化目标具备准确的成本依据」 |
| 输入、输出和总 Token 上限 | 「应与上游模型的实际限制一致，避免长上下文或大输出请求被错误地视为可执行」 |
| 输入输出模态和能力 | 「例如文本、图片、音视频输入，以及工具调用等能力。只有满足本次请求所需能力的模型才适合作为候选」 |
| 可用路径和兼容协议 | 「应标记模型可处理的请求路径和协议，例如 OpenAI 兼容或 Anthropic 兼容的路径。Model API 选择的协议和路径必须与候选一致」 |

来源：configure-smart-routing

### 4.7 后端服务与服务来源

> 「您需要将已有的服务添加到网关中，登记为路由备选服务，以便网关获取服务地址。AI 网关支持以容器服务、固定地址、DNS域名和FC函数计算等几种形式添加服务。」[官方原文｜creating-services]
> 「网关通过服务动态感知后端资源变化，实现流量路由、治理和安全防护的统一管理。」[官方原文｜creating-services]

**服务来源 8 类（完整枚举）**

| 服务来源 | 关键配置 / 硬约束 | 来源 slug |
|---|---|---|
| **AI 服务** | 大模型供应商（18 个，见下表）+ 模型协议（OpenAI/v1 或 原生协议）+ 服务接入点（BaseURL）+ API-KEY | creating-services |
| **Agent 服务** | 服务供应商：「**千问云 / 阿里云百炼**、**Dify**、**自定义**」；百炼默认 API 地址 `https://dashscope.aliyuncs.com/api/v1`，需 APP ID + API KEY；Dify 默认 `https://api.dify.ai/v1`，应用类型「**Agent** 或 **Workflow**」 | creating-services |
| **DNS 域名** | 服务地址格式「`<DNS域名>:<服务端口>`，支持填写多个，以英文`,`分隔」；TLS 模式默认关闭（关闭 / 单向TLS / 双向TLS(mTLS)）；「如果指定的是外网地址，需要配置NAT网关」 | creating-services |
| **固定地址** | 服务地址格式「`<IP>:<服务端口>`，支持填写多个，以英文`,`分隔」；「如果该服务没有服务发现机制，需要手动添加服务的后端节点地址」；TLS 模式同上 | creating-services |
| **容器服务**（ACK / ACS / ACK Serverless） | 需先「创建来源」再「创建服务」；「单个网关实例最多只能关联3个ACK容器服务」；「不支持跨VPC添加服务来源」；「网关会从ACK/ACK Serverless集群获取服务列表」 | creating-services、create-a-service-source |
| **SAE Kubernetes服务** | 「SAE应用需要开启K8s Service服务注册发现」；选命名空间 + 服务列表 | creating-services |
| **函数计算 FC** | 「支持函数计算3.0，**暂不支持函数计算2.0**的服务来源」；选函数 + 版本或别名 | creating-services |
| **MSE Nacos** | 「单个网关实例最多只能关联1个Nacos实例」；「集群列表仅展示`MCPEnabled = true`的MSE Nacos实例，可在MSE Nacos参数设置中更改」 | creating-services |

**服务来源（来源页签）通用规则**

| 规则 | 官方原文 | 来源 slug |
|---|---|---|
| ACK 集群版本 | 「关联的 ACK 集群版本不得低于 1.18。如果集群版本低于 1.18，请先升级集群版本后再关联来源。建议使用 1.28 及以上版本。」 | create-a-service-source |
| VPC 一致性 | 「您在创建网关时需要选择和后端集群相同的VPC，那么服务来源添加时会自动获取该VPC下的集群」；「如果需要添加其他VPC下的服务来源，请重新创建指定VPC下的网关实例后，再选择该集群」 | create-a-service-source、creating-services |
| 安全组授权 | 「容器集群的节点池上配置有安全组。通常情况下，集群外的组件要想访问到集群内的服务，就必须在安全组上开放服务所需的全部端口。」 | create-a-service-source |
| 监听对象 | 「网关需要监听ACK集群的Service和Endpoints来获取服务与端点信息。如果通过K8s Ingress配置网关的HTTPS请求时，网关还需要监听集群的Secret来获取HTTPS的证书信息。」 | create-a-service-source |
| 失效来源必须清理 | 「当配置的服务来源失效时，请手动清理此处配置，否则可能会引发稳定性问题，例如无法及时同步其他来源的服务信息。」 | create-a-service-source |
| 命名空间过滤 | 「默认不展示arms-prom、kube-system和mse-pilot命名空间的服务」（容器服务 / SAE / MSE Nacos 三处一致） | creating-services |
| 服务名过滤 | 容器服务段：「默认不展示以consumers开头的服务」；SAE / Nacos 段：「默认不展示以`consumers:`开头的服务」（**两处写法不一致**：`consumers` vs `consumers:`） | creating-services |
| 修改来源限制 | 「目前仅支持对含有Ingress监听配置的ACK容器服务进行修改操作」 | manage-service-sources |
| 不支持的注册中心 | 「网关不支持通过Nacos、ZooKeeper注册的本地服务」（健康检查异常排查段） | configure-service-health-checks |

**AI 服务：大模型供应商清单（18 个，原文顺序）**

「**千问云 / 阿里云百炼**、PAI-EAS、**Deepseek**、**OpenAI兼容（OpenAI Compatible）**、**OpenAI**、**Azure**、**Gemini**、**Bedrock**、**Claude**、**月之暗面**、**百川智能**、**零一万物**、**智谱AI**、**混元**、**阶跃星辰**、**星火**、**豆包**、**MiniMax**」[官方原文｜creating-services]

**模型协议（2 种）**：「**OpenAI/v1**：使用 OpenAI 兼容协议，适用于大多数供应商」；「**原生协议**：使用供应商原生 API 协议。选择原生协议时，服务地址将切换为对应的原生协议地址（如阿里云百炼为 `https://dashscope.aliyuncs.com`）」；「选择供应商后系统会填充默认值，可根据需要修改」[官方原文｜creating-services]

**⚠️ Bedrock Mantle 模式限制（原文）**：「Bedrock **端点模式**为 Mantle 时，仅支持 Anthropic 兼容协议（/v1/messages），不支持 OpenAI/v1 协议，且无法启用 Prompt Caching 功能。」[官方原文｜creating-services]

**各供应商服务地址与可用模型（逐格转录）**

| 供应商 | 服务地址（base_url） | 可用模型 | 特殊配置说明 |
|---|---|---|---|
| 阿里云百炼 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | qwen-max、qwen-plus、qwen-turbo、qwen-long、qwen-vl-max、qwen-vl-plus、qwen-vl-ocr、deepseek-r1、deepseek-v3 | 需选择**地域**，支持多地域切换 |
| Bedrock | `https://bedrock-runtime.{awsRegion}.amazonaws.com` | 无预设（用户自行输入模型名） | 需配置 awsRegion、**端点模式**（Runtime 或 Mantle）和认证方式（API Key 或 AK/SK）；Mantle 模式仅支持 Anthropic 兼容协议 |
| Vertex AI | 用户手动输入 | 无预设 | 需配置**鉴权方式**（GCP Service Account 或 Vertex AI Express Mode）；GCP 模式需填写 JSON 格式的 GCP Service Account KEY，自动解析 vertexProjectId |
| Azure | `https://{endpoint}?api-version={api-version}` | gpt-3、gpt-35-turbo、gpt-4、gpt-4o、gpt-4o-mini | endpoint 为 Azure OpenAI 资源的接入点地址 |
| OpenAI | `https://api.openai.com/v1` | gpt-3、gpt-35-turbo、gpt-4、gpt-4o、gpt-4o-mini | --- |
| OpenAI兼容（OpenAI Compatible） | `http://{endpoint}/v1` | 无预设（用户自行输入模型名） | 仅支持满足 OpenAI 接口标准的 AI 服务 |
| DeepSeek | `https://api.deepseek.com/v1` | deepseek-chat、deepseek-reasoner | --- |
| 豆包 | `https://ark.cn-beijing.volces.com/api/v3` | doubao-seed-1-6-250615、doubao-seed-1-6-flash-250715、doubao-seed-1-6-thinking-250715、doubao-1-5-thinking-vision-pro-250428 | --- |
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai` | gemini-1.5-flash、gemini-1.5-pro | --- |
| MiniMax | `https://api.minimaxi.com/v1` | abab6.5s、abab6.5g、abab6.5t、abab5.5s | --- |
| 月之暗面 | `https://api.moonshot.cn/v1` | moonshot-v1-8k、moonshot-v1-32k、moonshot-v1-128k | --- |
| 智谱AI | `https://open.bigmodel.cn/api/paas/v4` | GLM-4-Plus、GLM-4-0520、GLM-4-Long、GLM-4-AirX、GLM-4-Air、GLM-4-FlashX、GLM-4-Flash、GLM-4-AllTools、GLM-4 | --- |
| PAI-EAS | 通过**工作空间**和**EAS服务**选择自动获取 | 无预设（动态获取） | 需依次选择**工作空间**、**EAS服务**和**连接类型**（私网或公网）；API-KEY 自动获取，无需手动配置 |
| Claude | `https://api.anthropic.com` | claude-3-5-sonnet-latest、claude-3-5-haiku-latest、claude-3-opus-latest | 可选开启**使用 Claude Code OAuth Token**以兼容 Claude Code 客户端调用 |
| 百川智能 | `https://api.baichuan-ai.com/v1` | Baichuan4-Turbo、Baichuan4-Air、Baichuan4、Baichuan3-Turbo、Baichuan3-Turbo-128k、Baichuan2-Turbo | --- |
| 零一万物 | `https://api.lingyiwanwu.com/v1` | yi-lightning、yi-large、yi-medium、yi-medium-200k、yi-spark、yi-large-rag、yi-large-fc、yi-large-turbo | --- |
| 混元 | `https://hunyuan.tencentcloudapi.com` | hunyuan-turbo-latest、hunyuan-turbo、hunyuan-large、hunyuan-pro、hunyuan-standard-256K、hunyuan-standard、hunyuan-lite | --- |
| 阶跃星辰 | `https://api.stepfun.com` | step-1-8k、step-1-32k、step-1-128k、step-1-256k、step-2-16k、step-1-flash | --- |
| 星火 | `https://spark-api-open.xf-yun.com` | lite、generalv3、pro-128k、generalv3.5、max-32k、4.0Ultra | --- |

来源：creating-services（HTML `<table>` 逐格重排）

**[官方矛盾 1] 供应商清单 vs 配置示例表**
- 正文枚举「大模型供应商」共 18 个，**不含 Vertex AI**：「支持**千问云 / 阿里云百炼**、PAI-EAS、**Deepseek**、**OpenAI兼容（OpenAI Compatible）**、**OpenAI**、**Azure**、**Gemini**、**Bedrock**、**Claude**、**月之暗面**、**百川智能**、**零一万物**、**智谱AI**、**混元**、**阶跃星辰**、**星火**、**豆包**、**MiniMax**。」
- 同页「各供应商配置示例」表格中却有完整的 **Vertex AI** 行（含鉴权方式、GCP Service Account KEY、vertexProjectId 解析）。
- 同一 slug（creating-services）内两处不一致，不裁决。

**[官方矛盾 2] Azure 服务地址格式**
- 同页正文引用块：「Azure 服务提供商服务地址格式： `https://{endpoint}/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}`」
- 同页配置示例表 Azure 行：「`https://{endpoint}?api-version={api-version}`」
- 两条格式不同，不裁决。SA 配 Azure OpenAI 时须以控制台实际填充值为准。

**API-KEY 获取方式（原文）**：阿里云百炼「前往阿里云百炼控制台获取」；PAI-EAS「选择**工作空间**和**EAS服务**后自动获取，无需手动配置」；Bedrock「使用 API Key 模式时，支持引用 KMS 密钥或手动输入；使用 AK/SK 模式时，需填写 awsAccessKey 和 awsSecretKey」；其他供应商「请前往对应供应商平台获取 API-KEY，或咨询服务提供商」[creating-services]

**免责声明（原文，两段措辞不同）**
- AI 服务段：「本AI服务所提供的大模型能力并非由AI网关直接提供。在使用前，请您自行评估该服务的适用性和可靠性……对于因违反上述规定而产生的一切后果，我们将不承担任何责任。」
- Agent 服务段：「请注意，本Agent服务所提供的智能体相关能力并非由**云原生API网关**直接提供……」[原文如此，AI 网关文档中出现「云原生API网关」]
- 来源：creating-services

**查看 / 编辑 / 删除服务**

| 操作 | 官方约束 | 来源 slug |
|---|---|---|
| 查看 | 「可以通过服务名称的关键字或**服务来源**的类别进行筛选」 | manage-services |
| 编辑 | 「您可以编辑由您自己创建的**静态IP服务和DNS服务**。**其他类型的服务不允许编辑**，例如从ACK导入的服务。」 | manage-services |
| 删除 | 服务列表操作列 > 删除 > 确认对话框 | manage-services |
| 变更动机（原文） | 「在AI 网关中添加固定地址来源的服务的后端节点地址可能发生变更，而该服务没有注册到网关服务来源，网关无法动态获取该服务的后端节点地址。需要通过变更服务手动调整服务的后端节点地址」 | manage-services |

### 4.8 服务健康检查

> 「为服务配置健康检查，可检测后端服务运行状态。若服务实例节点发生异常，可下线或隔离异常的节点，以保障路由到该服务的接口可用性。同时可进行恐慌阈值配置，以保障系统在极端情况下的基本服务能力。」[官方原文｜configure-service-health-checks]

**默认值（关键）**：「创建服务时默认开启TCP健康检查。」[官方原文｜configure-service-health-checks]

| 类型 | 机制（原文） | 版本要求 |
|---|---|---|
| 主动健康检查 | 「实现服务中个别实例节点异常时自动下线（**主动发送请求，如TCP链接/HTTP GET、探测服务节点是否存活以及直接判断节点是否可用）**），并在节点恢复正常后自动上线。该功能可在后端服务存在多副本部署时，提高路由到该服务的接口的可用性。」 | [文档未说明] |
| 被动健康检查 | 「实现**基于实际流量请求**失败率动态分析节点健康状态，若某节点表现异常（如失败率过高），将临时隔离该节点，待恢复后自动重启用。」 | 「需将引擎版本提升至2.1.10及以上版本」 |
| 恐慌阈值 | 「用于防止在系统负载升高或部分节点故障时，故障扩散至整个集群，从而避免服务系统性失效」 | [文档未说明] |

**主动健康检查配置项（官方给的是「示例值」，非默认值）**

| 配置项 | 示例值 | 描述（原文） |
|---|---|---|
| 健康检查协议 | HTTP | 「TCP协议健康检查通过发送SYN握手报文来检测服务器端口是否存活」；「HTTP协议健康检查通过发送请求模拟浏览器的访问行为来检查服务器应用是否健康」 |
| 健康检查路径 | `/` | 「用于健康检查页面文件的URI，建议对静态页面进行检查」 |
| 正常状态码 | `http_2xx` | 「用于判断健康检查正常的HTTP状态码」 |
| 健康检查响应超时时间 | 2 | 「每次健康检查响应的最大超时时间，超时视同不健康」（单位 [文档未说明]） |
| 健康检查间隔时间 | 2 | 「相邻两次健康检查的时间间隔」（单位 [文档未说明]） |
| 健康检查健康阈值 | 2 | 「云服务器从失败到成功的连续健康检查成功次数」 |
| 健康检查不健康阈值 | 2 | 「云服务器从成功到失败的连续健康检查失败次数」 |

**被动健康检查配置项（同为「示例值」）**

| 配置项 | 示例值 | 描述（原文） |
|---|---|---|
| 失败率阈值 | 80 | 「当某节点失败请求占比达到此阈值，系统将触发该节点的弹出机制」 |
| 检测间隔时间 | 30 | 「每隔指定时间（如 30 秒）计算节点在这段时间内的请求失败率」 |
| 初始隔离时长 | 30 | 「节点被弹出后的初始隔离时长（如 30 秒）。隔离时间计算公式：k \* base_ejection_time（k 初始值为1），每次弹出会延长隔离时间（k 加一），若连续检测正常则逐步缩短隔离时间（k 减一）」 |

**被动健康检查副作用（原文）**：「当更新被动健康配置时，被动健康检测状态将会重置，隔离的节点将全部重新启用。」[官方原文｜configure-service-health-checks]

**恐慌阈值行为（默认值 1%，逐字）**

> 「为在极端场景下最大限度保障服务可用性，系统将恐慌阈值默认设为 1%。当健康节点占比降至该阈值及以下时，系统将切换至恐慌模式，对所有节点转发请求。」[官方原文｜configure-service-health-checks]

| 健康节点比例 | 系统行为（原文） |
|---|---|
| **高于**恐慌阈值 | 「健康检查机制正常生效，请求仅路由至被标记为健康的节点，已失效或被弹出的节点将不再接收流量」 |
| **小于或等于**恐慌阈值 | 「系统进入"恐慌模式"，健康检查机制将被临时绕过，请求会均匀转发至所有节点（包括已被标记为不健康或被弹出的节点）」 |

设计意图原文：「此配置旨在避免出现大量节点异常时，剩余少量健康节点因承载全部流量而过载，进而导致级联故障」；「建议根据实际业务场景和容灾能力合理调整该阈值，以取得稳定性与服务正确性之间的最佳平衡」[configure-service-health-checks]

**初次添加服务健康检查异常排查（4 步，含决策含义）**：① VPC 是否一致或已通过云企业网/专线打通（「若VPC不一致且未做VPC连通，网关将无法访问到实例IP」；「网关不支持通过Nacos、ZooKeeper注册的本地服务」）② 再次确认 VPC 一致性 ③「确认是否进行了安全组授权，若服务来源为ACK服务，需授权容器集群的安全组」④「AI 网关部署在 VPC 内，默认不具备公网出访能力……需在网关所在 VPC 创建公网 NAT 网关，创建 VPC 粒度的 SNAT 条目并绑定弹性公网 IP」[configure-service-health-checks]

### 4.9 域名（对象边界说明）

本分片内域名只作为 Model API 的**引用项**出现，可确认的事实：

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 作用 | 「访问该 API 的域名，支持选择多个」 | managing-the-model-api、manage-the-ai-api |
| 唯一性约束 | 「域名与基本路径 `BasePath` 的组合必须唯一」 | 同上 |
| 未创建时 | 「如果还没有域名，请单击右侧 **添加域名** 按钮完成创建」 | 同上 |
| 调试时 | 调试面板需「选择域名和模型」 | 同上 |
| 全局认证授权 | 授权信息需填「**请求域名**、**请求Path** 和 **匹配方式**」 | manage-global-authentication |

域名对象本身的创建、协议与证书更换、删除规则页（`create-a-domain-name`、`change-the-protocol-and-certificate-of-the-domain-name`、`delete-a-domain-name`）**不在本分片**，归 W1 → 域名的证书/协议/加密套件细节在本章为 [文档未说明]。

### 4.10 API 产品与产品分类

**API 产品（Model API 类型）**

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 目的 | 「本文介绍如何将 Model API 封装为 API 产品，发布到开发者门户，供开发者浏览和订阅」 | create-an-api-product-of-the-model-api-type |
| 前提 | 「已创建 Model API」+「已创建开发者门户」 | 同上 |
| 入口 | 「登录开放平台控制台」→ 左侧导航「**API 产品**」→「**创建 API 产品**」 | 同上 |
| 发布硬约束 | 「API 产品必须关联具体的 AI API 后才能发布到门户」；「关联成功后，产品状态变为 **待发布**，页面会显示 Model API 的路由信息」 | 同上 |

**产品基本信息字段**

| 字段 | 必填 | 说明（原文） |
|---|---|---|
| 产品名称 | 必填 | 「产品的唯一标识，例如 `model-api-product`」 |
| 产品描述 | 必填 | 「简要描述产品的功能和用途」 |
| 产品类型 | 必填 | 「选择 **Model API**」 |
| 产品类别 | 选填 | 「选择产品类别，支持自定义」 |
| 自动订阅审批 | — | 「开启后，开发者的订阅申请将自动通过。**门户和 API 产品均可配置此选项，API 产品的配置优先级更高**」 |
| 产品图标 | 选填 | 「可使用 URL 链接或上传本地文件」 |

**模型参数字段（用途有明确限定）**

| 参数 | 说明（原文） |
|---|---|
| Model | 「模型名称，例如 `qwen-turbo`」 |
| Max Tokens | 「最大生成令牌数，控制返回内容的长度」（取值范围 [文档未说明]） |
| Temperature | 「采样温度，控制生成内容的随机性，取值范围 0～2」 |
| 支持联网搜索 | 「是否启用 Web Search 能力」 |

> 「模型参数用于 **HiMarket 前台调试模型时使用**，参数缺失可能导致模型调用失败，请确保配置完整。」[官方原文｜create-an-api-product-of-the-model-api-type]

**使用指南与发布**：「使用 Markdown 编辑器编写文档，或上传已有的 Markdown 文件」；发布流程为「确认产品状态为 **待发布**」→「**发布到门户**」→「选择目标门户」→「**发布**」；「发布后，开发者即可在门户中浏览和订阅该产品」[create-an-api-product-of-the-model-api-type]

**产品分类**

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 作用 | 「API 产品分类用于对开放平台中的 API 产品进行归类与打标，便于在管理侧检索、筛选，以及在开发者门户中按分类浏览与展示」 | product-category-management |
| 关系 | 「产品分类与 API 产品之间通过关联表建立**多对多**关系」：「同一 API 产品可以绑定多个产品分类」；「同一产品分类下可以包含多个 API 产品」 | 同上 |
| 绑定方式 | ①「创建或更新 API 产品时，指定产品所属的分类」②「在分类详情页中，将指定产品添加到当前分类」 | 同上 |
| 名称 | 「必填。长度为 **2～64 个字符**，须以**英文字母开头**，仅允许字母、数字、下划线（_）与连字符（-）」 | 同上 |
| 描述 | 「选填。长度**不超过 500 个字符**」 | 同上 |
| 图标 | 「选填。与 API 产品图标结构一致，可用于开发者门户展示」 | 同上 |
| 入口 | 「登录开放平台管理控制台」→「产品分类管理页面」→「新增产品分类」 | 同上 |
| 编辑 | 「可修改分类的名称、描述和图标」；「分类名称的命名规则与创建时一致」 | 同上 |
| 移除 | 分类详情页产品列表中「点击移除，确认操作」 | 同上 |

### 4.11 全局认证鉴权管理（仅入口位置，详细鉴权归 W4）

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| **入口位置** | AI 网关控制台 →「**实例**」→ 顶部菜单栏选地域 → 单击目标「**实例ID**」→ 左侧导航「**安全管理** > **全局认证鉴权**」 | manage-global-authentication |
| 生效层级 | **实例级**（从实例左侧导航进入，非 Model API 详情页的「策略与插件」） | manage-global-authentication |
| 可执行操作 | 「配置鉴权后，您可以查看鉴权详情，并对其执行编辑和删除操作」 | 同上 |
| 详情页三块内容 | 「可查看当前服务的**基本信息**和**认证配置**，也可查看并管理**授权信息**」 | 同上 |
| 授权信息字段 | 「单击**创建授权信息**，在对话框中输入**请求域名**、**请求Path** 和 **匹配方式**，新增授权规则」 | 同上 |
| 匹配方式取值 | [文档未说明] | 同上 |
| 支持的鉴权类型（API-Key/JWT/OIDC/自建） | 本页 [文档未说明]；对应页 `configure-jwt-authentication`、`configure-oidc-authentication`、`configure-self-built-authentication` 归 W4 | — |
| 与 Model API 消费者鉴权的关系 | 本页 [文档未说明]；`consumer-authentication`（Model API 消费者鉴权）归 W4 | — |

**[对照事实]** Model API 级鉴权开关散落在多处：按消费者限流「需要先开启消费者认证」[current-limiting]；智能路由「默认启用消费者鉴权，且在服务类型为智能路由时不能关闭」[configure-smart-routing]；API 级插件挂载列表中「**入站处理**区域显示 **jwt-auth**（未开启）和 **key-auth**（已启用）」[more-policies-and-plugins]。三处均为不同层级入口。

### §4 溯源

- `managing-the-model-api` — 管理 Model API（23549）：Model API 7 种使用场景、协议与默认路由的对应关系、API 名称 64 字符与全局唯一约束、域名+BasePath 唯一性、BasePath 默认 `/` 与移除语义、AI 请求观测依赖 SLS、5 种大模型服务类型与 2.1.15 版本门槛、首包超时毫秒/0=不启用、调试参数上限（System Prompt 100 字符、max_tokens 0--8192 默认 1024、top_p 0--1 默认 0.95、temperature 0--2 默认 1）、删除需输入 API 名称、协议转换改变 Token 统计结构、默认路由全表（含 ComfyUI 25 条）、Anthropic 协议供应商范围、智能路由 IntentCode 五分类（与 §5.2 交叉）
- `manage-the-ai-api` — Model API 管理快速入门（7403）：创建 Model API 的前提条件（供应商注册、可选添加模型、可用实例）、「不强制绑定模型资源，最终以模型名称字符串为准」、模型资源下拉来源、与 managing-the-model-api 的场景/参数/调试口径一致性交叉验证
- `route-list` — Model API 自定义路由管理（4293）：自定义路由仅支持 4 种路径、更多匹配规则（Method/Header/Query）、服务模型仅 2 种（单模型 / 多模型按比例）、路由级 Fallback 降序执行、发布/下线/删除状态机与「仅支持删除未发布或已下线的路由」
- `model-metadata` — 管理模型元信息（8625）：模型元信息四组构成、前提（实例 + 至少一个可用供应商）、使用限制 4 条、Credits 单位 Credits/1M tokens 与默认 0、最多两位小数、Token 上限为 ≥0 整数、输入输出模态 4 值、能力特性 15 项完整枚举、可用路径必填与 3 种协议类型、编辑名称影响候选展示、删除不影响已保存的模型名称字符串
- `manage-providers` — 管理供应商（3552）：预置 vs 自定义供应商的可编辑/可删除差异、入口在「模型元信息管理 > 供应商」、名称支持重名、标识系统生成不可编辑、被引用时禁止删除、「供应商」与「供应商配置模版」为独立概念、无额外 RAM/规格/地域限制
- `creating-services` — 添加后端服务（18183）：服务来源 8 类枚举、18 个大模型供应商清单、模型协议 2 种与原生协议地址切换、Bedrock Mantle 模式仅 Anthropic 且不支持 Prompt Caching、各供应商 base_url 与可用模型全表、单实例最多 3 个 ACK / 1 个 Nacos、不支持跨 VPC、FC 仅支持 3.0、SAE 需开启 K8s Service 注册发现、命名空间与服务名过滤规则、MSE Nacos 仅展示 MCPEnabled=true、免责声明
- `manage-services` — 查看、编辑与删除服务（2003）：仅自建的静态 IP 服务与 DNS 服务可编辑，ACK 导入等其他类型不允许编辑；按服务名关键字或服务来源类别筛选
- `manage-service-sources` — 管理服务来源（1070）：修改服务来源「仅支持对含有Ingress监听配置的ACK容器服务」；删除来源入口
- `create-a-service-source` — 添加 ACK 容器服务来源（2612）：ACK 集群版本 ≥1.18（建议 ≥1.28）、VPC 必须与网关一致、安全组需开放全部服务端口、需监听 Service/Endpoints（HTTPS 还需 Secret）、失效来源须手动清理否则引发稳定性问题、DNS/固定地址无需服务来源
- `configure-service-health-checks` — 配置服务健康检查（7494）：创建服务默认开启 TCP 健康检查、主动/被动/恐慌阈值三类机制、主动 7 个配置项与被动 3 个配置项（均为「示例值」）、被动健康检查需引擎 2.1.10+、更新被动配置会重置状态并重启全部隔离节点、恐慌阈值默认 1% 及两侧行为、隔离时长公式 k * base_ejection_time、不支持 Nacos/ZooKeeper 注册的本地服务、VPC/安全组/NAT+CEN 排查四步
- `create-an-api-product-of-the-model-api-type` — 创建 Model API 类型产品（3196）：API 产品前提（Model API + 开发者门户）、开放平台控制台入口、6 个基本信息字段与「API 产品的配置优先级更高」、4 个模型参数与「用于 HiMarket 前台调试模型时使用」、「必须关联具体的 AI API 后才能发布到门户」、待发布状态、Markdown 使用指南、发布到门户
- `product-category-management` — API 产品分类管理（2370）：分类与产品多对多、两种绑定方式、名称 2～64 字符且须英文字母开头、描述 ≤500 字符、图标结构、开放平台管理控制台入口、编辑与移除
- `manage-global-authentication` — 全局认证鉴权管理（1713）：仅用于确认入口位置（安全管理 > 全局认证鉴权，实例级）、可查看的三块内容、授权信息三字段（请求域名/请求Path/匹配方式）、支持编辑与删除
- `configure-smart-routing` — 配置智能路由（13423）：本章用于候选模型三要素（元信息+供应商+已关联 AI 服务）、模型元信息五项维护要求原文、「模型元信息不是静态备注」告警、最多 5 个自定义候选且系统内置模型不占名额、单独开通要求、默认启用且不可关闭的消费者鉴权（详细机制见 §5.2）
- `current-limiting`、`configure-a-modelapi-throttling-policy`、`ai-fallback`、`ai-cache-1`、`networked-search`、`more-policies-and-plugins`、`consumer-quotas-management` — 主体内容归 §5，本章仅引用其与对象依赖相关的约束（按消费者限流需先开启消费者认证、Fallback 需先创建服务、语义缓存需 DashVector + AI 服务、精确缓存需 Redis 白名单加网关 VPC 网段、FinOps 需引擎 2.1.19+/2.1.20+ 且非旧版 Serverless 版型、策略挂载分入站/出站处理）

- **本章查无**（翻过但本分片文档确实没写的高价值问题）：
  1. 单个 AI 网关实例可创建的 **Model API 数量上限**、**自定义路由数量上限**、**服务数量上限**、**域名数量上限**、**模型元信息条目上限**、**供应商数量上限** —— 全部 [文档未说明]（仅有「单个网关实例最多只能关联3个ACK容器服务」「单个网关实例最多只能关联1个Nacos实例」「一个智能路由 Model API 最多可配置五个自定义候选」三条零散上限）
  2. Model API 名称的**唯一性作用域**表述为「全局唯一（同一账号下不可重复）」，是否含跨地域、跨实例 [文档未说明]
  3. BasePath 的**字符集、层级深度、通配符支持**（除「默认为 `/`」外）[文档未说明]
  4. 单个 Model API 可**关联的域名个数上限**、域名+BasePath 冲突时的报错行为 [文档未说明]
  5. 「语音合成（Audio）」与「其他（Others）」场景**是否支持 Anthropic 协议 / 智能路由**（configure-smart-routing 明确「当前智能路由支持**OpenAI 兼容**和**Anthropic 兼容**的文本生成 Model API」，其他场景 [文档未说明]）
  6. **默认路由能否删除或改路径**、自定义路由与默认路由路径重复时的优先级 [文档未说明]
  7. 自定义路由**是否支持智能路由 / 按观测指标 / 按模型名称匹配**（route-list 仅列 2 种服务模型）[文档未说明]
  8. 主动健康检查各配置项的**取值范围与单位**（官方只给「示例值」2、80、30 等，未标单位与区间）[文档未说明]
  9. 主动健康检查的**引擎版本要求**、是否所有服务来源类型都支持健康检查 [文档未说明]
  10. 恐慌阈值是否**可在控制台修改**、修改入口与取值范围（仅说「默认设为 1%」「建议……合理调整」）[文档未说明]
  11. 模型元信息的**预置模型清单**（哪些供应商下系统自带哪些模型、其默认 Credits 单价与 Token 上限）[文档未说明]
  12. 模型元信息「信息来源 URL」字段的**填写规范与是否必填** [文档未说明]
  13. Credits 单价的**上限**（仅「大于等于 0」「最多两位小数」）[文档未说明]
  14. 供应商**被引用判定**是否包含「已被 Model API 以字符串引用的模型名」 [文档未说明]
  15. AI 服务的 **API-KEY 是否支持引用 KMS 密钥**（仅 Bedrock 明确「支持引用 KMS 密钥或手动输入」，其他供应商 [文档未说明]）
  16. 服务级 **TLS 单向/双向的证书来源、TLS 版本与加密套件** [文档未说明]（域名证书页归 W1）
  17. **超时/重试/并发数在服务级的默认值**（more-policies-and-plugins 只给 API 级策略，服务级 [文档未说明]）
  18. API 产品的**订阅计费、配额下发、与消费者体系的打通方式**（仅提到「自动订阅审批」与「开发者可浏览和订阅」）[文档未说明]
  19. API 产品「关联 API」时**可否关联多个 Model API**、可否跨实例 [文档未说明]
  20. 产品分类的**数量上限、层级（是否支持父子分类）** [文档未说明]
  21. 全局认证鉴权的**匹配方式取值**、授权信息与 Model API 域名/Path 的匹配优先级、与 API 级 key-auth/jwt-auth 插件的**叠加关系** [文档未说明]
  22. 「多服务（按观测指标）」的**指标采集窗口、判定算法与权重公式**（仅「根据各服务的响应时间、成功率等观测指标自动选择最优服务」）[文档未说明]
  23. Agent 服务、函数计算 FC、SAE Kubernetes 服务**能否作为 Model API 的大模型服务后端** [文档未说明]

---

## §5 流量治理与成本控制

### 5.1 四套「限制类」机制对照总表（限流 ≠ 配额 ≠ 流控 ≠ 熔断）

⚠️ 本分片文档中存在**四套彼此独立**的限制机制，客户与 SA 极易混淆。下表每一格均可回指 slug。

| 维度 | ① Model API 限流策略（控制台） | ② Model API Token 限流策略（OpenAPI） | ③ 消费者配额（FinOps） | ④ API 级 流量控制 / 并发控制 / 熔断 |
|---|---|---|---|---|
| 来源 slug | current-limiting | configure-a-modelapi-throttling-policy | consumer-quotas-management | more-policies-and-plugins |
| 配置入口 | Model API 详情 → **策略与插件** → **限流**开关 | `PUT /v1/http-apis/{httpApiId}`，`deployConfigs[].policyConfigs[]`，`type` 固定为 `"AiTokenRateLimit"` | 实例左侧导航 **FinOps** → **消费者配额** | Model API 详情 → **策略与插件** → **更多策略与插件** → 入站处理/出站处理 → 启用策略/插件 |
| 生效层级 | **API 级**（单个 Model API）；普通规则可细分到消费者/Header/Query/Cookie/IP/模型；另有「按 API 限流」全局兜底 | 同①（同一 `httpApiId` 下） | **实例级**：「支持在实例级别对消费者设置配额规则」 | **API 级** |
| 计量单位 | Token / 请求数 / 并发数 | Token（TokenPer*）/ 请求数（RequestPer*）/ 并发数（ConcurrencyLimit） | **Token 配额 或 Credits 配额**（二选一，「Token 配额按大模型 token 数计量；Credits 配额按统一积分制计量」） | 流量控制＝**QPS**（「总体QPS阈值」）；并发控制＝**并发数**（「总体并发数阈值」）；熔断＝慢调用比例(%) 或 异常比例(%) |
| 时间窗口 | 每秒 / 每分钟 / 每小时 / 每天（并发数无时间窗口） | 每秒 / 每分钟 / 每小时 / 每天 / **每周 / 每月**（Token 与 Request 各 6 档）；ConcurrencyLimit 无窗口 | **自然日 / 自然周 / 自然月**（「创建后不可修改」） | 流量控制/并发控制无窗口（瞬时阈值）；熔断有「统计窗口时长，取值范围为1秒~120分钟」 |
| 窗口语义 | 「固定 TTL 时间窗口统计……不按自然时间边界（例如 1:00 到 2:00）切分，也不是滑动窗口」 | 同①（原文逐字一致） | **自然周期**（自然日/周/月）+ 时区 | [文档未说明] |
| 主体（限谁） | 消费者 / Header / Query / Cookie / 客户端 IP / 模型 / 整个 API | limitType 9 值：Header / Parameter / Consumer / Cookie / IP / Model / Request / Concurrency / Global | **消费者**（穿梭框选择） | 整个 API（无主体维度） |
| 超限行为 | 「命中任一规则即触发限流」（返回的 HTTP 状态码与响应体 **[文档未说明]**） | 「当任意一条规则的配额耗尽时，即触发限流」（返回码 **[文档未说明]**） | 「配额达到限额后，消费者将无法继续调用模型，直到下一个周期重置」（返回码 **[文档未说明]**） | **有明确 fallback 配置**：Web fallback 行为＝「返回指定内容」（Http状态码「默认为429」、content-type「普通文本」或「JSON」、HTTP 返回文本）或「跳转地址」/「跳转到指定页面」 |
| 默认状态 | 「开启或关闭限流策略，**默认关闭**」 | `enable` 必填；`enableGlobalRules`「默认 `false`」 | 需手动创建规则；可「生效中」/「停用」，「启用后……立即生效」「停用后……立即失效」 | 各策略均有「是否开启」/「开启」开关（默认值 [文档未说明]） |
| 规则数量约束 | 「最多只支持同时命中 10 条规则」 | 「一个请求可以同时命中多条规则（最多同时命中 10 条）」 | 「单次创建或编辑配额规则操作，最多可选择 **1000** 个消费者」；「同一消费者对应一个重置周期，**只能存在一条配额规则**」 | [文档未说明] |
| 规则间关系 | 「多条规则之间的关系为`或`，即命中任一规则即触发限流」；「相同限流维度（相同判断条件 + 匹配键）的规则会被合并到同一个规则组中执行」 | 「所有命中的规则均会独立扣减各自的配额」；「相同限流维度（即相同 `limitType` + `matchKey`）的规则会被合并到同一个规则组中执行」 | 「支持按自然日、自然周、自然月设置配额周期，且**支持多个维度配额规则并存同时扣减**」 | 各策略独立生效 |
| 存储介质 | [文档未说明]（控制台页未提 Redis） | 「AI网关实例默认使用**内置KVStore**，无需配置`redisConfig`」；「仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置」 | [文档未说明] | [文档未说明] |
| 生效延迟 | 「更新配置后，系统会自动将新的限流规则推送到网关数据面，通常在**几秒内**生效」 | 同①（原文一致） | 「立即生效」/「立即失效」 | 「策略配置修改后**即时生效，无需重新发布**」 |
| 准确性声明 | 「由于分布式架构的特性，限流计数可能存在**轻微偏差**。实际允许的请求数与配置数会因请求量、速率、后端延迟等因素产生差异」 | 同①（原文一致） | [文档未说明] | [文档未说明] |
| 版本/版型门槛 | [文档未说明] | [文档未说明] | 「引擎版本为**2.1.19及以上**，如需使用 Credits 配额能力，请升级至**2.1.20及以上**」；「网关实例的版型**不能是旧版本 Serverless 规格**」；「已开通 SLS 日志服务并开启日志投递」 | [文档未说明] |
| 是否消耗额外 Token/Credits | [文档未说明] | [文档未说明] | [文档未说明] | [文档未说明] |

**官方对「配额 vs 限流」的定性（唯一一句原文，务必逐字引用）**

> 「注意：消费者配额与消费者限流互补。**配额是 FinOps 维度，控制周期内总使用量；限流是 QPS/并发维度，控制瞬时使用量。**」[官方原文｜consumer-quotas-management]

**[推断]** ①与②是**同一个策略的两个配置面**（控制台 vs OpenAPI）。推理链：② 的 `PolicyConfig.type` 固定为 `"AiTokenRateLimit"`；① 的 6 种判断条件与 ② 的 limitType（Header/Parameter/Consumer/Cookie/IP/Model）一一对应；① 的三种限流单位与 ② 的三类 limitMode（TokenPer*/RequestPer*/ConcurrencyLimit）一一对应；两页的「固定 TTL 时间窗口」说明段、「更新配置后……通常在几秒内生效」、「分布式架构……轻微偏差」三段文字**逐字相同**；① 的「按模型限流……系统会自动将其转换为基于 `x-higress-llm-model` Header 的精确匹配限流」与 ② 的「`Model` 类型自动设置为 `x-higress-llm-model`／`Exact`」一致。两页均**未明文声明二者为同一策略** → 该等同关系标 [推断]。

**[官方矛盾 1] 限流单位适用的判断条件范围**
- current-limiting「限流单位与限流模式」表：**Token / 请求数 / 并发数** 三种单位的「适用的判断条件」列**均写「所有判断条件」**。
- configure-a-modelapi-throttling-policy「limitMode 枚举值」表：`RequestPerSecond`～`RequestPerMonth` 的「适用 limitType」为「**Model / Global / Request**」；`ConcurrencyLimit` 的「适用 limitType」为「**Model / Global / Concurrency**」；仅 `TokenPerSecond`～`TokenPerMonth` 写「**所有类型**」。
- 即：按 OpenAPI 表，消费者/Header/Query/Cookie/IP 维度**不能**用请求数或并发数限流；按控制台表，**可以**。current-limiting 示例一本身就给了「按客户端 IP …… 50 并发数」的配置。不裁决，交主控核。

**[官方矛盾 2] 时间窗口档位数量**
- current-limiting：「**限流范围**｜选择限流的时间窗口：**每秒、每分钟、每小时、每天**」（4 档）；「限流策略支持以下**限流范围**（时间窗口）」表同样只有 4 行 +「（无时间窗口）」。
- configure-a-modelapi-throttling-policy limitMode 表：Token 有 `TokenPerSecond/TokenPerMinute/TokenPerHour/TokenPerDay/`**`TokenPerWeek`/`TokenPerMonth`**；Request 有 `RequestPerSecond/…/RequestPerDay/`**`RequestPerWeek`/`RequestPerMonth`**（各 6 档）。
- 即 OpenAPI 多出「每周」「每月」两档，控制台页未列。不裁决。SA 若客户要「按月 Token 限额」，需确认是走 OpenAPI 还是走 FinOps 自然月配额。

**[官方矛盾 3] 按客户端 IP 是否需要选限流范围**
- current-limiting：「按客户端 IP 限流**无需选择匹配规则和限流范围**，系统会自动处理」；「按客户端 IP 限流的表单经过简化设计，只需输入 IP 地址或 IP 段即可」；示例一中「按客户端 IP」行的限流范围为「---」。
- configure-a-modelapi-throttling-policy 示例一：「为 Model API 配置 IP 限流：每个客户端 IP **每分钟**限流 500 Token」，JSON 为 `{"limitType": "IP", "matchValue": "0.0.0.0/0", "limitMode": "TokenPerMinute", "limitValue": 500}` —— IP 维度明确带时间窗口。
- 不裁决。

**[歧义｜不裁决] 「10 条」是配置上限还是命中上限**
- current-limiting 常见问题：「**Q：最多可以配置多少条限流规则？** A：最多只支持**同时命中** 10 条规则。」（问的是「配置」，答的是「同时命中」）
- configure-a-modelapi-throttling-policy：「一个请求可以**同时命中**多条规则（最多同时命中 10 条）」。
- 因此「单个 Model API 最多可**配置**多少条限流规则」在两页均为 [文档未说明]。

### 5.2 智能路由

**两套并存的官方描述（同一功能名，请求侧模型不同）**

`managing-the-model-api` 的智能路由章节按**意图分类**描述：「AI网关设计实现模型语义智能路由功能，通过语义分析自动将用户请求路由到最合适的模型服务，支持以下意图分类」

| IntentCode | 描述 | 典型场景 |
|---|---|---|
| `Coder` | 代码编写与调试 | 编程问题、代码生成、Bug修复 |
| `Math` | 数学计算与推理 | 数学证明、公式推导、统计分析 |
| `Translation` | 多语言翻译 | 文档翻译、实时翻译、本地化 |
| `Flash` | 快速简单响应 | 简单问答、信息查询、日常对话 |
| `Complex` | 复杂逻辑推理 | 深度分析、复杂决策、长文本理解 |

并给出模型优势映射：「**代码生成**：Qwen-Coder系列在代码理解和生成方面表现优异」「**数学推理**：Qwen-Math系列擅长复杂数学问题的求解」「**翻译任务**：Qwen-MT系列针对多语言翻译进行了专项优化」「**快速响应**：Qwen-Flash系列在延迟敏感场景下提供极速响应」「**复杂推理**：Qwen-Max、DeepSeek-R1等模型在复杂逻辑推理上更胜一筹」；同时列出 4 项挑战：「用户体验割裂」「资源利用不均」「开发复杂度高」「缺乏统一入口」[managing-the-model-api]

`configure-smart-routing` 则按**优化目标**描述，请求模型名必须是 `auto/<目标>`：

| 请求模型名 | 目标 | 适用说明（原文） |
|---|---|---|
| `auto/balanced` | 综合均衡 | 「生产环境的默认目标，兼顾质量与成本。建议作为没有明确单一优先级时的常用选择。」 |
| `auto/cheap` | 成本优先 | 「在满足当前请求要求的前提下，优先选择成本更低的候选模型。」 |
| `auto/quality` | 质量优先 | 「优先选择能力更强、与本次任务更匹配的候选模型。」 |
| `auto/fast` | 速度优先 | 「优先选择低延迟、响应更快的候选模型。」 |

**[官方矛盾 4] 智能路由的请求侧模型：意图分类 vs `auto/<目标>`**
- managing-the-model-api：「AI网关设计实现模型语义智能路由功能，通过语义分析自动将用户请求路由到最合适的模型服务，**支持以下意图分类**」+ IntentCode 表（Coder/Math/Translation/Flash/Complex），且「多模型服务（智能路由）：系统将根据**模型特征**为请求自动选择最合适的模型」。
- configure-smart-routing：「智能路由的请求模型名**必须显式使用 `auto/<目标>`**，例如 `auto/balanced`。**单独填写 `auto` 不会作为默认目标使用**」；「智能路由**只识别** `auto/balanced`、`auto/cheap`、`auto/quality` 或 `auto/fast` 这类请求模型名」；「优化目标表达的是业务偏好，**而不是固定模型名称或强制规则**」。
- 两页对「调用方如何在请求里表达路由意图」给出不相容口径（5 个 IntentCode vs 4 个 `auto/*` 目标），且 managing-the-model-api 全篇未出现 `auto/` 前缀。不裁决，交主控核（疑为两代能力，但两页均未标注版本切换或废弃时间）。

**按什么维度路由（configure-smart-routing 原文）**

> 「网关只会在满足当前协议、请求路径、输入输出类型、Token 上限和能力要求的候选模型中进行选择。」[官方原文｜configure-smart-routing]

即路由维度 = **协议 + 请求路径 + 输入输出类型（模态）+ Token 上限 + 能力特性**，再叠加调用方声明的**优化目标**（成本/质量/速度/均衡）。其中「成本」维度的依据来自模型元信息中的 Credits 单价：「维护输入、输出和缓存 Token 的价格信息，使**成本相关的优化目标具备准确的成本依据**」[configure-smart-routing]

**适用范围与关键约束**

| 项目 | 官方口径 |
|---|---|
| 支持协议 | 「当前智能路由支持**OpenAI 兼容**和**Anthropic 兼容**的文本生成 Model API」；「应用仍使用原有协议和对应路径调用，例如 OpenAI 兼容的 Chat Completions 或 Responses 路径，以及 Anthropic 兼容的 Messages 路径；**无需为智能路由接入新的应用协议**」 |
| 适用业务 | 「适合简单问答、内容生成、代码辅助和 Agent 等请求类型混合的业务」；「您可以在不修改应用中具体模型名称的前提下，集中调整候选模型池，并按成本、质量或响应速度选择不同的优化目标」 |
| 执行链路 | 「选中的模型通过其关联的 AI 服务执行请求，响应仍按照您选择的 OpenAI 兼容或 Anthropic 兼容协议返回」 |
| 非承诺（原文） | 「`auto/cheap` 会在可用候选中优先考虑成本更低的模型，但**不会绕过协议、能力或输入限制**；它也**不承诺每次都调用同一具体模型或绝对价格最低的模型**」 |
| 同目标结果不稳定 | 「候选池、模型元信息、请求内容和能力要求发生变化时，实际处理模型也可能不同。**若必须固定模型，请使用非智能路由的 Model API**」 |
| API 名称不参与路由 | 「智能路由不使用 API 名称作为请求模型名……即使您的 Model API 名称为 `my-router`，请求模型名仍应为 `auto/balanced`」；「API 名称仅用于管理和标识接口，不决定请求中的智能路由模型名」 |
| 具体模型名不触发（原文） | 「在服务类型为**智能路由**的 Model API 中，`model` 字段**不能用于指定候选池中的具体模型名称**。填写 `qwen3.7-flash`、`claude-*` 等具体模型名不会触发智能路由。若业务必须固定使用某一模型，请新建或调用非智能路由的 Model API，例如单服务或按模型名称路由的 Model API」 |
| 鉴权强绑定（原文） | 「智能路由 Model API **默认启用消费者鉴权，且在服务类型为智能路由时不能关闭**」；「已为调用方创建消费者、配置认证凭据，并向该消费者授予目标 Model API 的调用权限」 |
| 开通方式 | 「智能路由需要**单独开通**。在创建 Model API 时选择**智能路由**后，如果页面显示**请开通智能路由**，请单击**前往开通**并按页面指引完成开通。**功能未开通时，无法完成智能路由配置**」 |
| 版本要求 | managing-the-model-api / manage-the-ai-api：「多模型服务（智能路由）需要将AI网关版本升级至`2.1.15`及以上」；configure-smart-routing **未提版本要求**（该页 [文档未说明]） |

**候选来源与名额上限**

| 候选来源 | 适用场景（原文） | 配置要求（原文） |
|---|---|---|
| 系统内置模型 | 「希望直接将平台提供的模型加入候选池。」 | 「在智能路由配置中启用系统内置模型。**系统负责维护其基础模型信息**；此来源可以单独使用，也可以与自定义候选混合使用。」 |
| 自定义模型（包括 BYOK） | 「希望将您接入的第三方、专有或自带凭据模型加入候选池。」 | 「先维护模型元信息，再将 AI 服务关联到模型供应商，最后选择对应服务和模型。**一个智能路由 Model API 最多可配置五个自定义候选；系统内置模型不占用该名额。**」 |

补充原文：「系统内置模型、自定义模型或二者混合均可作为候选来源。对于自定义模型，**模型元信息、供应商和服务关联缺少任一项时，配置无法形成可用候选**」；「同一 AI 服务可以配置多个不同模型，但**重复的服务与模型组合不能重复添加**」；「确认服务、供应商和模型元信息处于**同一实例**，且服务能够按模型元信息声明的协议路径正常调用」；「对于 BYOK 模型，请在该 AI 服务中配置您自己的访问凭据和服务地址」[configure-smart-routing]

**💰 AI 增强能力是否消耗 Credits / Token（计费强相关，逐字引用）**

> 「智能路由会对请求进行语义分析，**可能产生额外 Token 消耗**。请在成本评估中一并考虑，具体计费以[AI Credits 计费说明](https://help.aliyun.com/document_detail/3048572.html)为准。」[官方原文｜configure-smart-routing]

- 结论（本分片可确证的部分）：**智能路由会产生额外 Token 消耗**（官方明文），但**具体 Credits 单价、是否计入 AI Credits、计量口径**在本分片内 = [文档未说明]。官方用「以……为准」把数字**推给了「AI Credits 计费说明」页**（slug `ai-credits-billing-details`，**不在 W3 分片，归 W2**）。
- **这是文档级空白 + 数字被推走**：SA 报价智能路由时必须另走 `ai-credits-billing-details` 与购买页核验，本章不能给出任何单价。
- 「系统内置模型」由「系统负责维护其基础模型信息」，其 Credits 单价是否平台预置、客户能否修改 → [文档未说明]。
- 其他 AI 增强能力的消耗口径见 §5.11 汇总表。

**排障（原文）**：「请求没有可用候选模型时，应该检查什么？依次检查请求中的 `model` 是否为 `auto/<目标>`、候选模型是否支持当前协议和路径、模型元信息中的 Token 与能力信息是否准确，以及自定义模型的 AI 服务是否已关联到正确的模型供应商并可正常访问。」[configure-smart-routing]

**验证与维护（原文 4 步）**：①「使用控制台调试功能，分别以 `auto/balanced` 和业务需要的其他目标发送测试请求」②「验证 OpenAI 兼容或 Anthropic 兼容的实际调用路径、消费者认证凭据和请求格式与应用保持一致」③「新增模型、调整候选模型、修改 AI 服务或服务关联后，**按控制台提示保存并发布配置**，再通过业务请求验证」④「当上游模型升级、下线、变更协议能力、调整上下文长度或修改价格时，同步更新模型元信息和候选配置」[configure-smart-routing]

**调用示例（OpenAI 兼容，逐字保留）**

```shell
curl https://<your-domain>/<base-path>/v1/chat/completions \
  -H "Authorization: Bearer <API-KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/balanced",
    "messages": [
      {"role": "user", "content": "请帮我总结这段内容。"}
    ]
  }'
```

Anthropic 兼容：`POST /v1/messages`，body 中 `"model": "auto/quality"`、`"max_tokens": 1024`；「除协议所需的请求头外，调用方还必须按智能路由 Model API 的消费者鉴权配置携带网关认证凭据；**凭据字段以实际选择的认证方式为准**」；「如果您为 OpenAI 兼容 Model API 配置了 Responses 路径，也可以继续使用对应的 Responses 请求格式，并将 `model` 改为 `auto/<目标>`」[configure-smart-routing]

### 5.3 Model API Fallback

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 定义 | 「AI Fallback 是指Model API在主模型服务不可用时Fallback到备用模型，从而提升Model API的可用性，避免因为某个模型服务的异常或者高负载造成的请求不可用」 | ai-fallback |
| **触发条件（逐字）** | 「当调用模型服务，返回**任意 HTTP 4xx、5xx 错误状态码**时，均会触发 AI Fallback。」 | ai-fallback |
| 回退顺序 | 「AI 网关支持配置一到多个Fallback模型，当主模型服务不可用时，网关将会**按顺序**调用Fallback模型服务，如果调用成功，则会**立即返回**」；配置表：「开启后可添加Fallback服务，**按照降序执行**」 | ai-fallback |
| 级数 | 「Model API 支持**多级Fallback**，启用并合理的配置Fallback，可有效提升AI请求的成功率」；条数上限 [文档未说明] | ai-fallback |
| 服务复用 | 「Fallback服务支持重复使用同一个服务组建多条策略」 | ai-fallback、route-list |
| **失败判定收窄开关** | 「**仅Fallback后端服务错误**｜开启后，仅当后端服务返回错误时才会触发Fallback机制。如果不开启，则当请求被**网关限流或者其它形式拦截**时同样会触发Fallback。」 | ai-fallback |
| 服务名称 | 「备用模型服务的名称，从该实例下的服务列表中选择」 | ai-fallback |
| 模型名称 | 「支持透传和指定具体模型的名称，如 Qwen-plus」；「**默认为透传**。将请求中的模型名称直接传递给Fallback模型服务」 | ai-fallback |
| 首包超时 | 「流式传输中首个响应包的超时时间，单位为毫秒。**首包超时仅对流式响应生效，设为0时代表不启用**，当设置首包超时为非0时，对于首包响应过慢的请求网关将会fallback至兜底服务。」 | ai-fallback |
| 配置位置 | 「可在创建或者编辑Model API时开启Fallback」（Model API 级）；自定义路由的创建/编辑面板同样有 Fallback 项（路由级，「按照降序执行」） | ai-fallback、route-list |
| 前提 | 「已创建网关实例」+「已创建服务」 | ai-fallback |

**⚠️ 与限流的连带关系（避坑，原文级）**：默认（未开启「仅Fallback后端服务错误」）情况下，**网关限流拦截也会触发 Fallback**。即 §5.1 的限流命中后流量会被打到 Fallback 备用模型 —— 这会绕开客户预期的「限流即拒绝」语义，并产生备用模型的额外调用量。该连带影响在 ai-fallback 页未量化 → [文档未说明]。

**Fallback 相关空白**：是否消耗额外 Credits / 是否重复计费 → [文档未说明]（ai-fallback 全页无 Credits 或计费字样）｜全部 Fallback 均失败时返回什么状态码 → [文档未说明]｜是否对非文本生成场景（图片/视频/Embedding/Rerank）生效 → [文档未说明]｜首包超时的取值范围与推荐值 → [文档未说明]（仅「单位为毫秒，设为0时表示不启用」）｜Fallback 是否有独立超时/重试次数 → [文档未说明]｜「降序执行」与「按顺序调用」是否为同一语义 → 两页措辞不同，[文档未说明]。

### 5.4 Model API 限流策略（控制台面）

**策略定位（原文）**：「API 限流策略专为大模型服务及高并发调用场景设计，支持基于 Token 消耗量、请求数和并发数的多维度动态控制机制。该策略可针对消费者身份、请求 Header 参数、Query 参数、Cookie、客户端 IP、模型名称等多维度配置限流规则，并提供 API 级别的全局限流能力。」[current-limiting]

**7 项策略说明（原文要点）**：防止资源过载（「建议配合缓存策略以提升系统性能」）｜动态调整流量（「支持多种限流范围（如每秒、每分钟、每小时、每天）」）｜多种匹配规则支持（「精确匹配、前缀匹配、正则匹配、任意匹配」）｜多种限流模式（「支持按 Token 消耗量限流、按请求数限流和按并发数限流三种模式」）｜模型级精细管控（「支持针对不同模型名称设置差异化的限流阈值，**保护高成本模型资源**」）｜全局限流能力（「支持 API 级别的全局限流（按 API 限流），作为普通规则之外的**兜底策略**」）｜防止恶意攻击（「有效限制爬虫或自动化工具的访问频率」）[current-limiting]

**6 项适用场景（原文）**：高并发场景（「电商大促期间，按用户单位时间调用 Token 总量限流，防止恶意高频调用，保障服务稳定及活动公平」）｜AI 服务调用｜多租户系统（「为不同租户分配独立的限流配额，确保公平性和资源隔离」）｜模型级精细管控（「针对不同模型（如 qwen-max、qwen-plus）设置差异化的 Token 限额和请求数限额」）｜全局流量保护（「从整体上控制 Token 消耗总量、请求总数和最大并发数」）｜恶意攻击防护（「防范针对 AI 接口的爬虫攻击、DDoS 攻击或接口滥用行为」）[current-limiting]

**规则三段式构成（原文）**：「每条规则由三部分组成：**判断条件**、**限流规则**（匹配方式）和**限流范围**（限流模式 + 限流值 + 限流单位）。规则支持**拖拽排序**，可通过**添加**按钮新增规则行。」[current-limiting]

| 配置项 | 说明（原文） |
|---|---|
| 限流 | 「开启或关闭限流策略，**默认关闭**」 |
| 判断条件 | 「选择限流维度，支持 **6 种**：按消费者、按请求 Header、按请求 Query 参数、按请求 Cookie、按客户端 IP、按模型」 |
| 限流规则 | 「根据判断条件的不同，需要填写不同的匹配信息（匹配规则、参数名称、匹配内容等）」 |
| 限流范围 | 「选择限流的时间窗口：每秒、每分钟、每小时、每天」 |
| 限流值 | 「填写限流阈值」（取值范围 [文档未说明]） |
| 限流单位 | 「选择限流的计量单位：**Token**、**请求数**或**并发数**」 |

**6 种判断条件的表单项差异（逐个转录）**

| 判断条件 | 表单项顺序 | 参数名称 | 匹配规则 | 匹配内容 / 值 | 官方示例 |
|---|---|---|---|---|---|
| 按消费者 | 判断条件 → 匹配规则 → 消费者选择 → 限流范围 → 限流值 + 限流单位 | — | 精确/前缀/正则/任意 | 「从已有消费者列表中选择，也可点击**创建消费者**快速新建。选择`任意匹配`时无需选择具体消费者」 | 「任意消费者每分钟限流 1000 Token」 |
| 按请求 Header | 判断条件 → 参数名称 → 匹配规则 → 匹配内容 → 限流范围 → 限流值 + 限流单位 | 「必填，输入需要匹配的 Header 字段名」 | 精确/前缀/正则/任意 | 「选择`任意匹配`时无需填写」 | 「限制 Header 中 `x-user-level` 值为 `beta` 的请求，每分钟限流 100 Token」 |
| 按请求 Query 参数 | 同上（参数名称为 Query 参数名） | 「必填，输入需要匹配的 Query 参数名」 | 精确/前缀/正则/任意 | 「选择`任意匹配`时无需填写」 | 「限制 Query 参数中 `user_id=1` 的请求，每分钟限流 100 Token」 |
| 按请求 Cookie | 同上（参数名称为 Cookie 字段名） | 「必填，输入需要匹配的 Cookie 字段名」 | 精确/前缀/正则/任意 | 「选择`任意匹配`时无需填写」 | 「限制 Cookie 中带有目标标识的请求，每分钟限流 100 Token」 |
| 按客户端 IP | 判断条件 → IP 地址 → 限流值 + 限流单位 | — | 「无需选择匹配规则和限流范围，系统会自动处理」 | 「输入需要限流的 IP 地址（如 `192.168.1.1`）或 IP 段（如 `192.168.1.0/24`）。**填写 `0.0.0.0/0` 表示匹配所有客户端 IP**」 | 「限制每个客户端 IP 最大并发数为 50」 |
| 按模型 | 判断条件 → 匹配规则（**精确匹配，固定不可更改**）→ 模型名称 → 限流值 + 限流单位 | — | 固定精确匹配 | 「必填，输入需要限流的目标模型名称」；「**限流单位**：支持 **Token**、**请求数** 和**并发数**三种」 | 「`qwen-max` 每分钟限流 500 Token，同时限制最大并发数为 10」 |

全部来源：current-limiting

**按模型的实现细节（原文）**：「按模型限流固定使用精确匹配。如果需要更灵活的模型匹配（如前缀匹配、正则匹配），可以使用"按请求 Header"并手动指定参数名称为 `x-higress-llm-model`」；「按模型限流时，系统会自动将其转换为基于 `x-higress-llm-model` Header 的精确匹配限流」[current-limiting]

**按消费者限流的硬前提（原文）**：「配置按消费者限流，需要先开启消费者认证。」[current-limiting]

**4 种匹配规则与优先级**

> 「按消费者、按请求 Header、按请求 Query 参数、按请求 Cookie 四种判断条件支持以下四种**匹配规则**，优先级：**精确匹配 > 前缀匹配 > 正则匹配 > 任意匹配**。」[官方原文｜current-limiting]

| 匹配规则 | 说明（原文） | 示例（原文，含渲染残留） |
|---|---|---|
| 精确匹配 | 「匹配值与目标值完全相同」 | 「Header `x-user-level` 精确等于 `beta`」 |
| 前缀匹配 | 「匹配值以指定前缀开头」 | 「Header `x-user-level` 以 `vip` 开头」 |
| 正则匹配 | 「匹配值符合指定正则表达式」 | 「Header `x-user-level` 匹配 `` \`\^(gold ``」[原文如此，示例被截断且含转义残留] |
| 任意匹配 | 「匹配该维度下的所有值，无需填写匹配内容」 | 「任意消费者均适用」 |

补充原文：「如果配置了多条规则，则命中任一规则即被拦截。**按客户端 IP 和按模型有各自固定的匹配方式，无需手动选择匹配规则**。」[current-limiting]

**3 种限流单位 × 4+1 种限流范围（原文两张表逐格转录）**

| 限流单位 | 说明（原文） | 适用的判断条件（原文） |
|---|---|---|
| **Token** | 「按大模型的**传入传出 Token 消耗量**计算」 | 「所有判断条件」 |
| **请求数** | 「按请求次数计算」 | 「所有判断条件」 |
| **并发数** | 「按同时处理的请求数量计算」 | 「所有判断条件」 |

| 限流范围 | Token 限流 | 请求数限流 | 并发数限流 |
|---|---|---|---|
| 每秒 | 每秒允许消耗的最大 Token 数 | 每秒允许的最大请求次数 | --- |
| 每分钟 | 每分钟允许消耗的最大 Token 数 | 每分钟允许的最大请求次数 | --- |
| 每小时 | 每小时允许消耗的最大 Token 数 | 每小时允许的最大请求次数 | --- |
| 每天 | 每天允许消耗的最大 Token 数 | 每天允许的最大请求次数 | --- |
| （无时间窗口） | --- | --- | 允许同时处理的最大请求数 |

补充原文：「并发数限流不需要选择限流范围（时间窗口），直接设置最大并发数即可。」[current-limiting]

**🔴 窗口语义（客户高频误解，逐字引用）**

> 「带时间窗口的限流范围采用**固定 TTL 时间窗口**统计。同一限流维度和匹配值对应一个独立限流 Key，窗口从该 Key **首次写入有效统计数据时**开始计时，**不按自然时间边界（例如 1:00 到 2:00）切分，也不是滑动窗口**。窗口到期后自动重置，**后续请求不会刷新当前窗口的到期时间**。例如，某 Key 在 01:23:10 首次写入统计且配置每小时限流，则该窗口到 02:23:10 左右重置，而不是在 02:00:00 重置。」[官方原文｜current-limiting；configure-a-modelapi-throttling-policy 逐字相同]

**按 API 限流（全局兜底）**

| 项目 | 官方口径 |
|---|---|
| 定位 | 「按 API 限流是独立于上述限流策略之外的**兜底策略**，对整个 API 进行全局限流，**不区分具体的判断条件**」 |
| 启用方式 | 「勾选**按 API 限流**区域的**开启**复选框」；「需要单独勾选"开启"，与普通规则独立配置」 |
| 表单项 | 「限流范围（每秒/每分钟/每小时/每天）→ 限流值 + 限流单位（Token/请求数/并发数）」 |
| 多条 | 「可通过**添加**按钮新增多条全局限流规则，分别设置不同的限流模式」 |
| 叠加语义（原文） | 「全局限流和普通规则可以同时使用，**两者叠加生效，命中任一规则即触发限流**」；「按 API 限流（全局规则）作为普通规则之外的兜底策略，作用于整个 API 级别，不区分具体的 key；普通规则按维度细分限流」 |
| 官方示例 | 「整个 API 每分钟最多消耗 10000 Token，每分钟最多 100 次请求，最大并发数为 20」 |

来源：current-limiting

**5 个官方配置示例（逐格转录，可直接引用给客户）**

示例一：按消费者 Token 限流 + 按客户端 IP 并发限流

| 序号 | 判断条件 | 匹配规则 | 参数名称/匹配内容 | 限流范围 | 限流值 | 限流单位 |
|---|---|---|---|---|---|---|
| 1 | 按消费者 | 任意匹配 | --- | 每分钟 | 1000 | Token |
| 2 | 按客户端 IP | --- | 0.0.0.0/0 | --- | 50 | 并发数 |

示例二：按请求 Header 限流（多种匹配规则）

| 序号 | 判断条件 | 参数名称 | 匹配规则 | 匹配内容 | 限流范围 | 限流值 | 限流单位 |
|---|---|---|---|---|---|---|---|
| 1 | 按请求 Header | x-user-level | 精确匹配 | beta | 每分钟 | 100 | Token |
| 2 | 按请求 Header | x-user-level | 前缀匹配 | vip | 每小时 | 5000 | Token |
| 3 | 按请求 Header | x-app-id | 任意匹配 | --- | 每分钟 | 50 | 请求数 |

示例三：按模型名称差异化限流（原文：「`qwen-max` 每分钟限流 500 Token 且最大并发 10，`qwen-plus` 每分钟限流 2000 Token」）

| 序号 | 判断条件 | 匹配规则 | 模型名称 | 限流范围 | 限流值 | 限流单位 |
|---|---|---|---|---|---|---|
| 1 | 按模型 | 精确匹配 | qwen-max | 每分钟 | 500 | Token |
| 2 | 按模型 | 精确匹配 | qwen-plus | 每分钟 | 2000 | Token |
| 3 | 按模型 | 精确匹配 | qwen-max | --- | 10 | 并发数 |

示例四：按 API 限流（全局）+ 消费者限流组合

| 层 | 序号 | 判断条件 | 匹配规则 | 限流范围 | 限流值 | 限流单位 |
|---|---|---|---|---|---|---|
| 普通规则 | 1 | 按消费者 | 任意匹配 | 每分钟 | 1000 | Token |
| 全局规则（勾选「开启」） | 1 | （按 API） | — | 每分钟 | 10000 | Token |
| 全局规则 | 2 | （按 API） | — | 每分钟 | 100 | 请求数 |
| 全局规则 | 3 | （按 API） | — | --- | 20 | 并发数 |

示例五：混合多维度限流

| 序号 | 判断条件 | 参数名称 | 匹配规则 | 匹配内容/IP/模型名称 | 限流范围 | 限流值 | 限流单位 |
|---|---|---|---|---|---|---|---|
| 1 | 按消费者 | --- | 精确匹配 | consumer-001 | 每分钟 | 500 | Token |
| 2 | 按请求 Header | x-user-level | 前缀匹配 | vip | 每小时 | 10000 | Token |
| 3 | 按请求 Query 参数 | user_id | 正则匹配 | `^\[0-9\]+$` | 每分钟 | 200 | 请求数 |
| 4 | 按请求 Cookie | session | 任意匹配 | --- | 每分钟 | 100 | 请求数 |
| 5 | 按客户端 IP | --- | --- | 192.168.1.0/24 | --- | 30 | 并发数 |
| 6 | 按模型 | --- | 精确匹配 | qwen-max | 每分钟 | 1000 | Token |

全部来源：current-limiting（HTML `<table>` 逐格重排，`---` 为原文占位）

**10 条常见问题（官方 Q&A 要点）**

| 问题 | 官方答复要点 |
|---|---|
| 最多可以配置多少条限流规则？ | 「最多只支持同时命中 10 条规则。您可以根据业务需求灵活组合不同维度的规则，但**建议控制规则数量以确保性能**」 |
| 多条规则之间的关系？ | 「为`或`，即命中任一规则即触发限流。相同限流维度（相同判断条件 + 匹配键）的规则会被合并到同一个规则组中执行」 |
| 按 API 限流和普通限流规则可同时使用？ | 「可以……两者可以叠加使用，任一规则触发即执行限流」 |
| 按模型限流 vs 按请求 Header 限流的区别？ | 「按模型限流时，系统会自动将其转换为基于 `x-higress-llm-model` Header 的精确匹配限流。如果需要更灵活的模型匹配（如前缀匹配、正则匹配），可以使用按请求 Header 限流并手动指定参数名称为 `x-higress-llm-model`」 |
| Token、请求数、并发数三种单位可组合？ | 「可以。同一个判断条件下可以添加多条规则，分别选择不同的限流单位……**两者独立计数，命中任一即触发限流**」 |
| 按客户端 IP 为何没有匹配规则和限流范围选项？ | 「表单经过简化设计，只需输入 IP 地址或 IP 段即可。系统会自动处理匹配逻辑。如果需要对所有客户端 IP 进行限流，可以输入 `0.0.0.0/0`」 |
| 规则顺序是否影响限流效果？ | 「规则支持拖拽排序，但多条规则之间的关系为`或`……因此**规则顺序不影响最终的限流效果**」 |
| 更新限流配置后多久生效？ | 「系统会自动将新的限流规则推送到网关数据面，通常在**几秒内**生效」 |
| 分布式架构下的准确性？ | 「限流计数可能存在**轻微偏差**。实际允许的请求数与配置数会因请求量、速率、后端延迟等因素产生差异」 |

来源：current-limiting

### 5.5 Model API Token 限流策略（OpenAPI 面：`UpdateHttpApi` + `aiTokenRateLimitConfig`）

**接口信息**：「**请求方法**：`PUT`」；「**Action**：`UpdateHttpApi`」；路径 `PUT /v1/http-apis/{httpApiId}`；配置位置「`UpdateHttpApiRequest` 的 `deployConfigs[ ].policyConfigs[ ]` 中，通过 `PolicyConfig` 结构传递」[configure-a-modelapi-throttling-policy]

**定位（原文）**：「AI Token 限流策略以 Token 消耗量为核心指标进行流量管控，**与传统请求数限流不同，能够精准匹配大模型计算资源的实际消耗**。」；4 项使用场景（高并发场景 / AI 服务调用 / 多租户系统 / 模型级精细管控）与 current-limiting 高度重合[configure-a-modelapi-throttling-policy]

**PolicyConfig 结构**

| 参数 | 类型 | 是否必填 | 说明（原文） |
|---|---|---|---|
| type | String | 是 | 「策略类型，**固定为 `"AiTokenRateLimit"`**」 |
| enable | Boolean | 是 | 「是否启用限流策略。`true` 表示开启,`false` 表示关闭」 |
| aiTokenRateLimitConfig | Object | 「是（enable 为 true 时）」 | 「AI Token 限流配置详情」 |

**AiTokenRateLimitConfig 结构**

| 参数 | 类型 | 是否必填 | 说明（原文） |
|---|---|---|---|
| rules | Array\<AiTokenRateLimitRule\> | 条件必填 | 「普通限流规则列表（包含按维度限流和模型限流）。**`rules` 和 `globalRules` 至少配置一项**」 |
| enableGlobalRules | Boolean | 否 | 「是否开启全局（API 级别）限流规则，**默认 `false`**」 |
| globalRules | Array\<AiTokenRateLimitRule\> | 条件必填 | 「全局限流规则列表,**仅当 `enableGlobalRules` 为 `true` 时生效**。规则的 `limitType` **必须为 `"Global"`**」 |
| redisConfig | Object | 否 | 「**AI网关实例默认使用内置KVStore，无需配置`redisConfig`**」；「仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置」 |

**AiTokenRateLimitRule 结构与自动填充规则**

| 参数 | 类型 | 必填 | 说明（原文） |
|---|---|---|---|
| limitType | String | 是 | 「限流维度类型」 |
| matchKey | String | 条件必填 | 「`Consumer` 类型允许为空」；「`IP` 类型自动设置为 `from-remote-addr`」；「`Model` 类型自动设置为 `x-higress-llm-model`」；「`Global` 类型自动置空」 |
| matchType | String | 条件必填 | 「`IP` 类型自动设置为 `IP`」；「`Model` 类型自动设置为 `Exact`」；「`Global` 类型自动置空」 |
| matchValue | String | 条件必填 | 「`All` 模式下自动设置为 `*`」；「`IP` 类型需为合法 IP 或 IP 段」；「`Model` 类型为模型名称」；「`Global` 类型自动置空」 |
| limitMode | String | 是 | 「限流模式」 |
| limitValue | Integer | 是 | 「限流阈值,**必须大于 0**」 |

**limitType 9 个枚举值**

| 取值 | 说明（原文） |
|---|---|
| Header | 按请求 Header 限流 |
| Parameter | 按请求 Query 参数限流 |
| Consumer | 「按消费者限流（**需先开启消费者认证**）」 |
| Cookie | 按请求 Cookie 限流 |
| IP | 按客户端 IP 限流 |
| Model | 「按模型名称限流（针对特定模型设置独立限额）」 |
| Request | 「按请求数限流（针对特定 key 的请求数限流）」 |
| Concurrency | 「按并发数限流（针对特定 key 的并发数限流）」 |
| Global | 「全局限流（API 级别，不区分 key，**仅用于 `globalRules`**）」 |

**matchType 5 个枚举值与适用范围**

| 取值 | 说明 | 适用 limitType（原文） |
|---|---|---|
| Exact | 精确匹配 | Header / Parameter / Consumer / Cookie / Request / Concurrency |
| Prefix | 前缀匹配 | Header / Parameter / Consumer / Cookie / Request / Concurrency |
| Regex | 正则匹配 | Header / Parameter / Consumer / Cookie / Request / Concurrency |
| All | 「任意匹配（matchValue 自动设为 `*`）」 | Header / Parameter / Consumer / Cookie / Request / Concurrency |
| IP | 「IP 匹配（自动设置，无需手动指定）」 | IP |

原文补充：「匹配优先级：精确匹配 > 前缀匹配 > 正则匹配 > 任意匹配。**命中任一规则即触发限流**。」

**limitMode 13 个枚举值（Token 6 档 + Request 6 档 + Concurrency 1 档）**

| 取值 | 说明 | 适用 limitType（原文） |
|---|---|---|
| TokenPerSecond | 每秒 Token 限流 | 所有类型 |
| TokenPerMinute | 每分钟 Token 限流 | 所有类型 |
| TokenPerHour | 每小时 Token 限流 | 所有类型 |
| TokenPerDay | 每天 Token 限流 | 所有类型 |
| **TokenPerWeek** | 每周 Token 限流 | 所有类型 |
| **TokenPerMonth** | 每月 Token 限流 | 所有类型 |
| RequestPerSecond | 每秒请求数限流 | Model / Global / Request |
| RequestPerMinute | 每分钟请求数限流 | Model / Global / Request |
| RequestPerHour | 每小时请求数限流 | Model / Global / Request |
| RequestPerDay | 每天请求数限流 | Model / Global / Request |
| **RequestPerWeek** | 每周请求数限流 | Model / Global / Request |
| **RequestPerMonth** | 每月请求数限流 | Model / Global / Request |
| ConcurrencyLimit | 并发数限流 | Model / Global / Concurrency |

**redisConfig 结构（仅外部 Redis 时需要）**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| host | String | 是 | Redis 服务地址（示例 `r-bp1xxxxxxxxxxxxx.redis.rds.aliyuncs.com`） |
| port | Integer | 是 | Redis 服务端口（示例 6379） |
| username | String | 否 | Redis 用户名 |
| password | String | 否 | Redis 密码 |
| timeout | Integer | 否 | 连接超时时间（单位 [文档未说明]） |
| databaseNumber | Integer | 否 | Redis 数据库编号（示例 0） |

**🔴 配置更新规则（最高危避坑点，逐字引用）**

> 「**PolicyConfigs 整体替换**：当 `policyConfigs` 字段非空时，会**整体替换**该 `gatewayId` 下的所有策略配置。更新限流规则时，**需要同时传入其他策略（如 AiFallback、AiStatistics 等）的配置，否则其他策略配置会被清空**。」[官方原文｜configure-a-modelapi-throttling-policy]

> 「**限流规则全量更新**：`aiTokenRateLimitConfig.rules` 和 `aiTokenRateLimitConfig.globalRules` 均为**全量更新**，每次请求需传入完整的规则列表。」[官方原文｜configure-a-modelapi-throttling-policy]

> 「更新限流配置前，**建议先通过 `GetHttpApi` 获取当前完整的 `deployConfigs` 和 `policyConfigs`**，在此基础上修改限流相关配置后再提交更新，以避免误覆盖其他策略配置。」[官方原文｜configure-a-modelapi-throttling-policy]

即：用 OpenAPI 改限流，若不带全量 policyConfigs，会**静默清空 Fallback / 统计等其他策略**。`gatewayType` 字段仅在示例五中出现为 `"API"`（其余示例未带该字段）[configure-a-modelapi-throttling-policy]。

**配置验证规则（提交时校验，逐项转录）**

| 验证项 | 规则（原文） |
|---|---|
| 规则数量 | 「`rules` 和 `globalRules` 至少需要配置一项」 |
| limitType 与 matchType 组合 | 「Header / Parameter / Consumer / Cookie / Request / Concurrency 支持 Exact / Prefix / Regex / All」；「IP 仅支持 IP 模式」；「Model 自动设为 Exact」；「Global 不需要 matchType」 |
| matchKey | 「Header / Parameter / Cookie / Request / Concurrency 类型**必填**」；「Consumer 类型允许为空」；「IP / Model / Global 类型由系统自动设置」 |
| matchValue | 「Exact / Prefix / Regex 模式下必填」；「All 模式自动设为 `*`」；「IP 类型需为合法 IP 或 IP 段格式」 |
| limitValue | 「必须大于 0」；「**Model 类型的 `limitValue` 不能超过 Int32 最大值**」 |
| globalRules 中的 limitType | 「必须为 `"Global"`」 |
| rules 中的 limitType | 「不能为 `"Global"`（Global 类型仅允许出现在 globalRules 中）」 |
| redisConfig | 「AI网关实例默认使用内置KVStore，无需配置`redisConfig`」；「仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置」 |

**关闭语义（原文）**：「将 `enable` 设置为 `false` 即可关闭限流策略。**关闭后，已配置的规则不会生效，但配置信息会保留**。」[configure-a-modelapi-throttling-policy]

**7 个官方 JSON 示例覆盖的场景**：①按消费者 + IP（Consumer/All/TokenPerMinute/1000 + IP/`0.0.0.0/0`/TokenPerMinute/500）②按 Header 精确匹配（x-user-level=beta，TokenPerMinute，100）③按模型（qwen-max TokenPerMinute 500、qwen-plus TokenPerMinute 2000、qwen-max RequestPerMinute 10）④开启全局限流（rules: Consumer TokenPerMinute 1000；globalRules: Global TokenPerMinute 10000 + Global RequestPerMinute 100 + Global ConcurrencyLimit 20）⑤配置外部 Redis ⑥关闭 Token 限流（enable=false）⑦更新限流规则（消费者阈值 1000 → 2000）[configure-a-modelapi-throttling-policy]

原文补充：「全局限流支持 **Token、Request、Concurrency 三种限流模式**」；「全局规则的 `limitType` 必须为 `"Global"`，不需要指定 `matchKey`、`matchType`、`matchValue`（系统会自动置空）」；「`IP` 类型的 `matchKey` 和 `matchType` 由系统自动设置，无需手动指定」；「`matchValue` 设为 `0.0.0.0/0` 表示匹配所有客户端 IP」[configure-a-modelapi-throttling-policy]

**本页 5 条常见问题**：AI 网关实例是否需要配置 redisConfig（「不需要……默认使用内置KVStore」）｜按消费者限流注意事项（「需要先为该 Model API 开启消费者认证。否则限流策略无法识别消费者身份，**规则不会生效**」）｜多条规则关系（「最多同时命中 10 条，所有命中的规则均会独立扣减各自的配额」）｜全局限流与普通规则可叠加｜生效时间（「通常在几秒内生效」）｜分布式准确性（「可能存在轻微偏差」）[configure-a-modelapi-throttling-policy]

### 5.6 🔴 Token 限流的计量口径（客户高频问题，文档写了多少抄多少）

| 问题 | 官方口径 | 来源 slug |
|---|---|---|
| 算输入还是输出还是两者？ | 「按大模型的**传入传出 Token 消耗量**计算」→ 明文为**输入 + 输出两者** | current-limiting |
| 如何统计（窗口）？ | 「固定 TTL 时间窗口统计……窗口从该 Key **首次写入有效统计数据时**开始计时，不按自然时间边界切分，也不是滑动窗口。窗口到期后自动重置，后续请求不会刷新当前窗口的到期时间」 | current-limiting、configure-a-modelapi-throttling-policy |
| 统计 Key 粒度 | 「同一限流维度和匹配值对应一个**独立限流 Key**」；「相同限流维度（即相同 `limitType` + `matchKey`）的规则会被合并到**同一个规则组**中执行」 | 同上 |
| 何时扣减 | 「一个请求可以同时命中多条规则（最多同时命中 10 条），**所有命中的规则均会独立扣减各自的配额**。当任意一条规则的配额耗尽时，即触发限流」 | configure-a-modelapi-throttling-policy |
| **超限返回什么？** | 🔴 **2026-09-21 主控修正（R1 判定 D3）**：限流两页本身**确实未写**状态码，但**别页有明文答案** —— `custom-response-plugin`「**触发网关限流时一般会返回429状态码**，这时请求将返回自定义应答如下」`[官方原文｜custom-response-plugin]`，并给了完整自定义应答样例（该插件可对 429 等状态码自定义响应体）。<br>**对客口径**：限流命中一般返回 **429**，且可用 custom-response 插件自定义应答内容；<br>**但仍有一层真空白**：这条 429 出自**自定义应答插件**页而非限流专页，官方**未说明**它是否对 AiTokenRateLimit 的所有限流单位（Token/请求数/并发数）与全部判断条件一律成立，也未说明未装 custom-response 时的默认响应体长什么样。（另对照：`more-policies-and-plugins` 的流量控制/并发控制/熔断策略明确「Http状态码……默认为429」，那是**另一套策略**，不可直接套用） | current-limiting、configure-a-modelapi-throttling-policy（未写）／**custom-response-plugin（写了 429）** |
| 是否含缓存 Token（cache token）？ | **[文档未说明]**。仅 managing-the-model-api / manage-the-ai-api 提到协议会改变 Token 统计结构：「阿里云百炼协议的 input token 统计**会包含**缓存 token（cache token），而 Anthropic 协议的 input token 统计**不包含**缓存 token」→ 该口径差是否传导到限流计数，两页均未说明 | — |
| 是否含推理 Token（reasoning tokens）？ | **[文档未说明]** | — |
| 流式响应如何计数（首包前扣还是结束后扣）？ | **[文档未说明]** | — |
| 命中 AI 缓存（tokens 为 0）时是否计入限流？ | **[文档未说明]**。（ai-cache-1 明确「命中精确缓存（from-cache），则输入 tokens 和输出 tokens 均为 0」「语义缓存命中时……输入和输出 tokens 均为 0，不消耗模型推理资源」，但未说明限流侧如何计） | ai-cache-1 |
| 联网搜索/意图识别消耗的 Token 是否计入限流？ | **[文档未说明]**。（networked-search 明确「**意图识别**能力也会消耗Token，并且**不会在模型调用监控中被统计**」，但未说明是否计入限流） | networked-search |
| 智能路由语义分析消耗的 Token 是否计入限流？ | **[文档未说明]**。（configure-smart-routing 仅「可能产生额外 Token 消耗」） | configure-smart-routing |
| 请求失败 / Fallback 重试是否重复计数？ | **[文档未说明]** | — |
| 限流值的取值上限？ | 「`limitValue`｜必须大于 0」+「Model 类型的 `limitValue` 不能超过 **Int32 最大值**」；非 Model 类型上限 **[文档未说明]**；控制台侧「限流值｜填写限流阈值」无范围 | configure-a-modelapi-throttling-policy、current-limiting |
| 精度是否精确？ | 「由于分布式架构的特性，限流计数可能存在**轻微偏差**。实际允许的请求数与配置数会因请求量、速率、后端延迟等因素产生差异」（未给偏差百分比） | current-limiting、configure-a-modelapi-throttling-policy |
| Token 分词口径（用哪个 tokenizer 计数）？ | **[文档未说明]** | — |

### 5.7 消费者配额管理（FinOps）

**功能定位（原文）**：「通过配额规则控制 AI 网关消费者在指定周期的大模型调用总量，实现精细化的成本管控。**支持 Token 和 Credits 两种计量维度，可按自然日、周、月自动重置**」；「AI 网关实例新增 **FinOps** 功能，支持在**实例级别**对消费者设置配额规则。配额规则通过设定配额类型（Token 配额或 Credits 配额）、配额限额、重置周期和时区，限制绑定消费者的调用量」[consumer-quotas-management]

**5 项能力（原文逐条）**：「支持消费者在实例级别设置 Token 配额」｜「支持按自然日、自然周、自然月设置配额周期，且**支持多个维度配额规则并存同时扣减**」｜「支持配额规则时区设置」｜「支持手动重置配额规则」｜「支持配额使用水位监控大盘」[consumer-quotas-management]

**超限行为（原文）**：「配额达到限额后，**消费者将无法继续调用模型，直到下一个周期重置**。」[consumer-quotas-management]（返回的 HTTP 状态码/错误体 [文档未说明]）

**基本配置（步骤一）**

| 配置项 | 必填 | 取值范围 / 默认值（原文） |
|---|---|---|
| 规则名称 | 必填 | 「支持字母、数字、下划线（_）和短划线（-），长度 **1~64 个字符**」 |
| 规则类型 | 必填 | 「选择 **Token 配额** 或 **Credits 配额**。Token 配额按大模型 token 数计量；Credits 配额按统一积分制计量」 |
| 限额 | 必填 | 「**最小值为 1，默认值为 60000**。单位根据所选配额类型动态切换为 Tokens 或 Credits」（最大值 [文档未说明]） |
| 重置周期 | 必填 | 「选择 **自然日**、**自然周** 或 **自然月**。**创建后不可修改**」 |
| 时区 | 必填 | 「默认为 **UTC+8（北京/上海/新加坡/香港）**。支持以下 **9 个时区**……**创建后不可修改**」 |

**9 个可选时区（逐字，原文顺序）**：「UTC+9（东京）、UTC+8（北京/上海/新加坡/香港）、UTC+7（曼谷）、UTC+5:30（新德里）、UTC+3（莫斯科）、UTC+1（柏林/巴黎）、UTC+0（伦敦）、UTC-5（纽约）、UTC-8（洛杉矶）」[consumer-quotas-management]

**主体选择（步骤二）**：「在 **选择消费者** 区域，通过穿梭框选择需要应用此配额规则的消费者」；「左侧列表为可用消费者，右侧列表为已选消费者」；「支持搜索消费者名称进行快速筛选」；「**单次创建或编辑配额规则操作，最多可选择 1000 个消费者**」；「已选消费者右侧提供 **查看** 链接，可跳转至该消费者的详情页面」；「如需了解配额与鉴权的配合使用方式，请参见 Model API 消费者鉴权」[consumer-quotas-management]

**冲突规则与处理（步骤三）**

> 「提交前，系统会自动检测是否存在冲突。**同一消费者对应一个重置周期，只能存在一条配额规则**。」[官方原文｜consumer-quotas-management]

| 情况 | 系统行为（原文） |
|---|---|
| 无冲突 | 「直接创建成功。操作成功后页面返回配额规则列表页，顶部显示"创建成功"提示，新规则出现在列表」 |
| 有冲突 | 「弹出 **配额规则冲突** 对话框，展示冲突消费者列表及其已有的配额类型。可选择：**覆盖已有规则**（以当前规则覆盖已有配额规则）／**退回重新选择**（返回消费者选择步骤，调整消费者列表）」 |

**编辑 / 启停 / 重置 / 删除**

| 操作 | 官方约束（原文） |
|---|---|
| 编辑 | 「编辑态下，**重置周期** 和 **时区** 不可修改」；「编辑时可**增量调整**消费者列表，直接通过穿梭框添加或移除消费者即可」；「编辑后同样会进行冲突检测，流程与创建时一致」 |
| 启用 / 停用 | 「在操作列选择 **生效中** 或 **停用**」；「启用后，配额规则**立即生效**」；「停用后，配额规则**立即失效**」；列表状态标识为绿色「启用」/ 灰色「停用」 |
| **配额重置** | 「单击操作列的 **配额重置** 按钮」；「重置操作会将**历史配额用量清零，但不会清除日志用量信息记录**。重置后同样会进行冲突检测，如有冲突需按提示处理」 |
| 删除 | 「单击操作列的 **删除** 按钮，**输入规则名称进行确认**后删除」 |

**用量查询（规则详情页，默认展示「用量统计」）**

| 区域 | 可查看内容（原文） |
|---|---|
| 左侧：消费者列表 | 「展示已绑定到此配额规则的消费者列表，支持按消费者名称搜索」；「每个消费者展示名称/ID、所属实例 ID/名称，以及**用量进度条（已用量/总限额）**」；「用量超过限额时标记为 **已超限**，未超过时标记为 **未超限**」 |
| 右侧：用量详情 | 「支持查看 **Token 和 Credits** 统计数据」：**Token 用量 / Credits用量**（已用量/总限额）｜**输入Token / 输入Credits**（「当前周期内输入方向的消耗」）｜**输出Token / 输出Credits**｜**缓存Token / 缓存Credits**（「当前周期内缓存的消耗」）｜**消费记录**表格（「包含模型名称、输入、输出、用量、消费时间等列，展示当前周期的消费明细」） |
| 分页 | 「每页可展示 **5 条或 10 条**记录」 |
| 依赖 | 「已开通 SLS 日志服务并开启日志投递（用于查看用量统计）」 |

**[文档未说明]**：「Token 用量」是否 = 输入 + 输出 + 缓存 Token 三者之和；缓存 Token 是否计入 Token 配额扣减；Credits 配额与模型元信息中 Credits 单价（Credits/1M tokens）的换算公式；配额扣减是实时还是有延迟。

**🔴 FinOps 风险通知（短信）—— 官方明文的运维风险，SA 必须知道**

| 项目 | 官方口径（原文） |
|---|---|
| 短信含义 | 「AI 网关实例在当前版本下，**FinOps** 相关功能的使用**可能影响日志计量准确性或触发异常限流**，存在潜在风险」 |
| 触发原因 | 「实例**未规范配置日志字段**或**未设置消费者配额规则**」 |
| 消除步骤 1 | 「进入对应实例的 **Model API > 策略与插件 > AI 请求日志**，启用日志策略，并**仅保留必要字段（如 `input_token`、`output_token` 等），禁用非必需字段，以降低计量成本**」 |
| 消除步骤 2 | 「在 **FinOps > 消费者配额** 中为消费者设置 **Token 配额** 或 **Credits 配额** 的周期配额」 |
| 结果 | 「完成上述两步调整后，该风险即可消除」 |
| **大额配额规避策略（原文）** | 「如果不希望配额真正限制业务调用，可以将 **配额限额** 设置为远大于实际用量的数值。这样既满足"已设置消费者配额"的要求以消除风险告警，又不会影响生产环境的正常调用」 |

来源：consumer-quotas-management

**⚠️ 连带计费信号**：消除步骤 1 把「日志字段」与「计量成本」直接挂钩（「禁用非必需字段，以**降低计量成本**」），说明 AI 请求日志字段数量本身影响成本；具体单价 [文档未说明]，AI 请求日志策略详情归 W7。

**⚠️ 时效性说明**：本页含「AI 网关实例**新增** FinOps 功能」的表述，但未给功能上线日期与灰度范围 → 上线时间 [文档未说明]。可确证的时间边界只有引擎版本门槛（2.1.19+ / Credits 需 2.1.20+）与「版型不能是旧版本 Serverless 规格」。

### 5.8 AI 缓存策略

**双引擎定位（原文）**：「在重复性强的 AI 请求场景，AI网关现已全面升级缓存能力，通过**Redis精确缓存**与**DashVector语义缓存**的双引擎协同，实现对大语言模型（LLM）调用的降本增效」[ai-cache-1]

**两种缓存类型对照（官方「策略对比」表，逐格转录）**

| 对比维度 | 传统精确缓存 | 语义化缓存 |
|---|---|---|
| 匹配方式 | 「字符串完全一致。」 | 「向量空间距离判定（余弦相似度）。」 |
| 容错能力 | 「不识别同义/近义表达。」 | 「支持同义词、句式变体等模糊匹配。」 |
| 响应速度 | 「毫秒级（本地Key-Value查询）。」 | 「毫秒级（向量数据库近邻搜索）。」 |
| 典型场景 | 「标准FAQ、固定参数接口调用。」 | 「自然语言指令、多轮对话、模糊查询。」 |
| 成本效益 | 「适合高频重复请求。」 | 「适合语义多样性高、意图相近的场景。」 |

**命中判定**

| 缓存类型 | 命中判定口径（原文） |
|---|---|
| 精确缓存 | 「基于Redis的Key-Value存储架构，对**完全相同**的请求实现毫秒级响应」；「在缓存时长内，如果API接收到**相同的AI请求**，则会**跳过LLM请求，直接返回缓存的响应数据**」 |
| 语义缓存 | 「系统会通过**余弦相似度**算法计算新请求与历史缓存的向量夹角。**当相似度达到预设阈值（建议0.8~0.9，可按需调整），就会触发缓存响应**」；向量库「通过**分层聚类算法（HNSW）**实现百万级向量的毫秒级检索，同时具备动态更新能力」；「语义缓存不仅支持无限语义变体的匹配，还能通过共享相似语义的存储空间提升资源利用率」 |

**缓存键生成策略（两类型共用）**：「选择控制台默认的**只取最新提问**，或根据需要选择**整合历史提问**」[ai-cache-1]

**🔴 绕过缓存的请求头（原文，两种缓存均适用）**

> 「携带请求头`x-higress-skip-ai-cache: on`时，当前请求将不会使用缓存中的内容，而是直接转发给后端服务，**同时也不会缓存该请求返回响应的内容**。」[官方原文｜ai-cache-1，语义化缓存段与精确缓存段各出现一次]

**配置项与默认值**

| 缓存类型 | 配置组 | 配置项 | 默认值 / 取值范围（原文） |
|---|---|---|---|
| 语义化 | 缓存键生成策略 | 只取最新提问 / 整合历史提问 | 「控制台默认的**只取最新提问**」 |
| 语义化 | 文本向量化配置 | AI 服务 | 「选择您创建好的AI 服务。若没有AI 服务，单击创建服务，创建一个新的AI 服务」 |
| 语义化 | 文本向量化配置 | 模型名称 | 「选择您计划使用的模型名称」 |
| 语义化 | 文本向量化配置 | 超时时间 | 「**默认5000ms**」 |
| 语义化 | 向量数据库配置 | 服务提供者类型 | DashVector；「若之前没有开通向量检索服务Dashvector，单击前往控制台……跳转至向量检索服务的服务开通页面进行开通」；「创建Collection时**距离度量方式选择`Cosine`**，**向量维度要与文本向量化模型的维度对应**」；「[文本与多模态向量化]可以查看到百炼平台文本向量化模型的输出向量维度」 |
| 语义化 | 向量数据库配置 | 服务地址 / Collection名称 / API Key | 「输入您的Dashvector服务地址」／「输入您创建好的Collection的名称」／「访问凭证」 |
| 语义化 | 向量数据库配置 | **向量相似度阈值** | 「该值决定系统对查询和缓存内容的匹配的严格程度。取值范围为**（0,1）**，建议您取值为**0.8或者0.9**，较大的值表示更大的语义相似性」 |
| 语义化 | 向量数据库配置 | 超时时间 | 「**默认3000ms**」 |
| 精确 | 缓存键生成策略 | 只取最新提问 / 整合历史提问 | 「控制台默认的**只取最新提问**」 |
| 精确 | Redis缓存配置 | Redis服务地址 / 端口号 | 「输入您的Redis服务地址」／「输入您的端口号」 |
| 精确 | Redis缓存配置 | 访问方式 | 「支持**账号+密码登录**、**密码登录**、**免密登录**三种方式」 |
| 精确 | Redis缓存配置 | 数据库账号 / 数据库密码 | 「若选择账号+密码登录的访问方式，需要您输入数据库账号」／「若选择账号+密码登录或密码登录的访问方式，需要您输入数据库密码」 |
| 精确 | Redis缓存配置 | 数据库编号 | 「指定的数据库编号」 |
| 精确 | Redis缓存配置 | **缓存时长（秒）= TTL** | 「缓存时长**默认为1800秒**，在缓存时长内，如果API接收到相同的AI请求，则会跳过LLM请求，直接返回缓存的响应数据」 |

**⚠️ 语义缓存的 TTL [文档未说明]** —— ai-cache-1 只给精确缓存的「缓存时长（秒）默认为1800秒」，**语义化缓存段没有任何 TTL / 缓存时长 / 过期配置项**。语义缓存条目何时过期、能否配置过期，属文档级空白（客户高频问题）。

**精确缓存网络前提（原文）**：「请前往Redis控制台添加白名单。在Redis控制台中，您需要将**网关实例的VPC网段**添加至白名单。」[ai-cache-1]

**向量相似度阈值调优指南**

| 项目 | 官方口径（原文） |
|---|---|
| 取值范围 | 「介于**0.0（完全不相似）到1.0（完全相似）**之间」 |
| 建议范围 | 「**0.8 ~ 0.9**（根据业务需求调整），**不建议低于0.8**」 |
| 阈值越低（如0.75） | 「即使用户表述方式不同，只要语义相近就会返回缓存结果」 |
| 阈值越高（如0.99） | 「仅当用户使用几乎完全相同的表述才返回缓存结果」 |
| 为何不建议低于 0.8 | 「当阈值低于0.8时，系统可能将**不相关的查询误判为匹配**。这会引发 **"假阳性" 问题**（系统错误地返回不相关结果），影响用户体验或业务准确性」 |
| 基准测试 | 「您可以从**默认值0.8**开始，逐步降低或升高阈值观察缓存命中情况变化」 |
| 场景适配 | 「对时效性敏感的查询（如实时物流跟踪）：建议相似度阈值**高**些」；「对标准化回答要求高的场景（如常见问题应答）：建议相似度阈值**低**些」 |
| 性能平衡 | 「**降低阈值，将增加LLM调用次数**」 |
| 最优阈值判定 | A/B 测试：「计算缓存命中率 vs LLM调用成本」「收集用户对重复内容的投诉率（如"为什么我的新问题返回了旧答案？"）」「监控关键查询的响应时间波动」；「建议定期（**如每月**）根据最新业务数据重新评估阈值设置，特别是在高峰期，可适当降低阈值以应对激增的查询量」 |

**官方效果对比示例（配置：「百炼文本向量化模型text-embedding-v4 (1024维)」+「缓存键生成策略：只取最新提问」+「向量相似度阈值0.85」）**

| 相似度 | 查询示例 | 特征说明（原文） |
|---|---|---|
| 1.0 | 「我的快递什么时候到？」 | 「以此条目作为比较基准。」 |
| 0.89 | 「我的快递预计送达时间是什么时候？」 | 「匹配"我的快递什么时候到？"，**命中**。」 |
| 0.86 | 「我的快递今天能不能送到？」 | 「匹配"我的快递什么时候到？"，**命中**。」 |
| 0.83 | 「我的快递今天能送到哪里？」 | 「**不能命中**。」 |

[官方原文如此] 该表把 0.83 与 0.86 都列在「阈值 0.85」的配置下，0.86 > 0.85 判定命中可自洽，但 0.83 < 0.85 判定「不能命中」也与阈值语义自洽；两行均在同一「示例配置」单元格下（原表首列为跨行合并的示例配置说明）。逐格保留，不做解释。

**缓存命中率查询（有明确前置条件与粒度限制）**

| 项目 | 官方口径（原文） |
|---|---|
| 前置条件 | 「请确保在查询之前**已经开通了日志服务**，**只能查到开通日志服务之后**的缓存命中率信息」 |
| 查询粒度 | 「目前支持的查询粒度为**网关级别**」（即不支持按 Model API / 消费者维度查命中率） |
| 日志源 | 「日志源为 `apig-plugin-log`」；「在**监控（AI 缓存）**页面中，单击**查看日志**进入日志查询界面」 |
| 查询语句前缀 | 「`cluster_id:{your-gatewayId} and inner-ai-cache-{your-gatewayId} \| SELECT …`」；「`{your-gatewayId}`替换为您的网关实例ID，注意**前一处替换需要保留`gw-`前缀，后一处替换不用保留**」 |
| 命中/未命中判定关键字 | 命中：`content LIKE '%cache hit for key%'` 或 `'%key accepted%'`；未命中：`'%cache miss for key%'` 或 `'%score not meet the threshold%'` |
| 官方示例结果 | 「`hit_count`（缓存命中次数）为 **7**，`miss_count`（缓存未命中次数）为 **6**，`hit_rate`（命中率）约为 **53.85%**」 |

**降本效果（原文量化示例）**

> 「当**开启精确缓存**时，只匹配完全相同的查询：在策略对比中，当用户发送相同语义的查询（如"你是谁"）时，若未命中缓存，模型正常消耗 token（**输入 tokens: 127，输出 tokens: 40**）；若命中精确缓存（from-cache），则**输入 tokens 和输出 tokens 均为 0**，直接返回缓存结果，有效降低 token 消耗。」[官方原文｜ai-cache-1]

> 「当**开启语义化缓存**时，语义相似的查询也可以匹配，语义相似度低于阈值则不匹配：语义缓存命中时，相似问题直接复用缓存中的回复，**输入和输出 tokens 均为 0，不消耗模型推理资源**。例如，用户提问`我的快递今天能送到哪里？`时，该问题与已缓存的问题语义差异较大，缓存未命中，模型 `qwen-max` 正常生成回复并消耗 tokens。」[官方原文｜ai-cache-1]

**功能优势（原文 5 条）**：双模缓存体系（「根据业务需求灵活选择两种缓存并动态调整匹配阈值」）｜减少重复计算（「避免重复调用大语言模型」）｜性能提升维度（「显著降低响应时间以及后端服务器的负载压力」）｜场景覆盖扩展（「适配客服系统、知识库查询等标准场景」）｜日志监控（「提供缓存命中率指标分析」）[ai-cache-1]

**⚠️ 连带开通/计费（P1）**：语义缓存需另开通**向量检索服务 DashVector**（「跳转至向量检索服务的服务开通页面进行开通」）+ 一个用于文本向量化的 **AI 服务与模型**（该模型调用本身会产生 Token 消耗）；精确缓存需自备 **Redis 实例**并加白名单。三者的独立计费单价在本页均为 [文档未说明] → 属「账单 ≠ 全成本」的典型场景。

### 5.9 联网搜索策略

> 「联网搜索策略能够扩展大语言模型的知识范围，通过实时检索互联网数据（**支持夸克搜索引擎**），提升生成内容的准确性与时效性。」[官方原文｜networked-search]

**3 项策略说明（原文）**：搜索引擎支持（「夸克搜索引擎（阿里云信息查询服务）」，含「**搜索重写**：将模型生成的多种结果，在搜索引擎中检索后的优化和重构，生成高质量、高相关性的上下文信息」与「**意图识别**：快速分析大模型输入，判断是否需要调用联网搜索」）｜灵活配置选项（「支持自定义返回结果数量、超时时间、查询时间范围及行业筛选等参数」）｜结果渲染（「支持中英文双语输出、展示引用来源，并提供引用格式自定义配置」）[networked-search]

**配置项与取值范围（逐格转录）**

| 配置组 | 配置项 | 官方口径（原文） |
|---|---|---|
| 总开关 | 联网搜索 | 「开启或关闭联网搜索开关，**默认关闭**」 |
| 总开关 | 搜索引擎 | 「目前**仅支持夸克**（阿里云信息查询服务）」 |
| 总开关 | 服务状态 | 「首次使用夸克联网搜索时，默认**服务状态**为**未开通**状态。单击**前往开通**，跳转至信息查询服务的服务开通页面进行开通」；「开通后，单击**开通校验**，控制台的**服务状态**会更新为**试用中**」 |
| 搜索配置 | API Key | 「访问凭证……在访问信息查询服务凭证管理控制台进行获取」 |
| 搜索配置 | **返回结果数量** | 「范围 **1-10**，最大值为 **10**，即最多返回 10 篇结果」 |
| 搜索配置 | **超时时间** | 「**默认 3000ms**」 |
| 搜索配置 | 查询时间范围 | 「1天内／1周内／1月内／1年内／无限制」 |
| 搜索配置 | 行业（可选） | 「金融／法律／医疗／互联网／税务／新闻省级／新闻中央」 |
| 结果渲染 | 默认语言 | 「支持中、英文」 |
| 结果渲染 | 输出引用来源 | 「是/否，**默认为否**，不展示引用来源」 |
| 结果渲染 | 引用来源位置 | 「首部/尾部，**默认位置为首部**」 |
| 结果渲染 | 内容类型 | 「**摘要（默认）**：只返回搜索条目的摘要信息，满足大模型的基础推理需求，覆盖常规问答任务的信息检索需求」／「**正文**：返回搜索条目的正文信息，信息量较大但内容详细，适合需要信息细节的场景」 |
| 结果渲染 | 引用格式 | 「`%s`为引用条目的渲染占位符，可以按需修改引用条目的展示格式」 |
| 自动启用 | 是否开启 | 「**开启**：调用时进行联网搜索，若已配置意图识别，则根据意图识别的结果进行处理」／「**关闭**：调用时默认不进行联网搜索，可通过调用参数手动控制是否要进行联网搜索」 |
| 意图识别 | 是否开启 | 「判断是否需要进行联网搜索」+「对联网搜索的搜索语句进行改写、拓展，增强搜索能力」 |
| 意图识别 | AI 服务 / 模型名称 | 「选择AI 服务」／「选择模型名称」 |
| 意图识别 | **超时时间** | 「设置超时时间，**默认 5000ms**」 |
| 意图识别 | **搜索重新生成的最大查询次数** | 「重新生成搜索查询的最大次数，**默认1次**。若配置为大于1次，改写将会产生多个搜索语句进行**并发搜索**，并最终聚合个多个搜索的结果」[原文如此，「聚合个多个」] |

**🔴 免费试用额度（时效性 + 数量，逐字）**

> 「阿里云信息查询服务提供**15天的免费试用**，用量为**1000次/天**，性能限制**5 QPS**。您可以进行正式接口的申请，具体步骤详情，请参见正式开通流程说明。」[官方原文｜networked-search]

⚠️ 试用**结束后的正式接口价格**在本页 = [文档未说明]，官方把定价推给了「正式开通流程说明」（doc 2869993，不在本分片）→ SA 报价须另核。

**🔴 意图识别的 Token 消耗（计费强相关，逐字）**

> 「**意图识别**能力也会消耗Token，并且**不会在模型调用监控中被统计**。」[官方原文｜networked-search]

即：联网搜索的意图识别是**额外的、监控不可见的 Token 消耗**。这部分 Token 是否计入 §5.4/§5.5 的 Token 限流、是否计入 §5.7 的 Token/Credits 配额 → [文档未说明]。

**手动控制参数（`web_search_options`）**

| 项目 | 官方口径（原文） |
|---|---|
| 激活方式 | 「当请求中包含`web_search_options`字段时，联网搜索会被激活」；示例 `("web_search_options": {})` [原文如此，圆括号] |
| `search_context_size` | 「若已经配置意图识别，`web_search_options`参数还具备控制搜索改写数量的能力，通过`search_context_size`字段控制」 |
| low | 「生成**1个**搜索查询（适合简单问题）」 |
| medium | 「生成**3个**搜索查询（**默认值**）」 |
| high | 「生成**5个**搜索查询（适合复杂问题）」 |

curl 完整样例（逐字）：

```shell
curl --location 'http://your-domain/v1/chat/completions' \
   --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen-max",
    "stream": true,
    "web_search_options": {
        "search_context_size": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "介绍下通义千问"
        }
    ]
}'
```

来源：networked-search

**[交叉事实]** 模型元信息的 15 项能力特性中含「联网搜索｜支持 Web Search」[model-metadata]；API 产品的模型参数中含「支持联网搜索｜是否启用 Web Search 能力」[create-an-api-product-of-the-model-api-type]。三处为不同层级：模型能力标记 / API 级策略开关 / 产品调试参数。三者之间是否需要同时开启才生效 → [文档未说明]。

### 5.10 API 级策略与插件配置（入口 + 非限流类策略）

**总入口与生效方式**

> 「AI 网关支持对API级进行添加策略和配置插件，提高API的安全性、性能和可维护性。」
> 「**策略配置修改后即时生效，无需重新发布。**」[官方原文｜more-policies-and-plugins]

入口路径：Model API 详情 →「**策略与插件**」页签 →「**更多策略与插件**」区域 →「选择需要配置策略或插件的位置（**入站处理**/**出站处理**）」→「**启用策略/插件**」[more-policies-and-plugins]

**请求流向（原文）**：「后端服务地址为 **test.static**，请求流向为**前端API → 入站处理 → 后端服务 → 出站处理**」；挂载列表示例：「**入站处理**区域显示 **jwt-auth**（未开启）和 **key-auth**（已启用），**出站处理**区域显示 **key-auth**（已启用）和 **jwt-auth**（未开启）」[more-policies-and-plugins]

**插件安装流程（原文 3 步）**：「单击**添加插件**页签」→「在**快捷导航**处，选择要安装的插件类型或者搜索插件名称，单击插件卡片：如果插件未安装，在安装插件的弹出框中单击**安装并配置**，在启用插件的弹框中配置插件规则，并选择启用状态；如果插件已安装，在启用插件的弹框中，配置插件规则，并选择启用状态」→「单击**确定**，返回API的挂载列表」[more-policies-and-plugins]（插件逐个参数与适用场景归 **W6**）

**6 类 API 级策略参数**

| 策略 | 原理（原文摘要） | 关键参数与取值范围 |
|---|---|---|
| **并发控制** | 「统计当前网关处理中的请求数之和，当指标达到设定的阈值时立即拦截流量，可配置为后端服务的最大并发处理请求数，实现在高并发下的后端服务可用性保护」 | 是否开启；**总体并发数阈值**；Web fallback 行为＝「返回指定内容」（**Http状态码「默认为429」**、返回 content-type「**普通文本**或**JSON**」、HTTP 返回文本）或「**跳转地址**」 |
| **流量控制** | 「监控API的**QPS**指标，当指标达到设定的阈值时立即拦截流量，避免后端服务被瞬时的流量高峰冲垮」 | 是否开启；**总体QPS阈值**；Web fallback 行为＝「返回指定内容」（Http状态码「默认为429」、content-type 普通文本/JSON、HTTP 返回文本）或「**跳转到指定页面**」（跳转地址） |
| **熔断策略** | 「监控API的响应时间或异常比例，当达到指定的阈值时立即降低依赖优先级。在指定的时间内，系统不会调用该不稳定的资源……当指定时间过后，再重新恢复对该资源的调用」 | 是否开启；**统计窗口时长「取值范围为1秒~120分钟」**；**最小请求数目**（「若当前统计窗口内的请求数小于此值，即使达到熔断条件规则也不会触发」）；**阈值类型**＝「慢调用比例（%）」或「异常比例（%）」；**慢调用RT**（「即最大的响应时间」）；**熔断比例阈值「取值范围 0-100（代表 0%-100%）」**；**熔断时长（s）**；Web fallback（Http状态码默认429 / content-type / HTTP 返回文本 / 跳转到指定页面） |
| **IP黑白名单** | 「通过预先配置允许或拒绝访问的 IP 地址列表，控制客户端对服务的访问权限」 | 开启；名称（「自定义标识名称，用于在多个策略中进行区分和管理」）；备注；**类型**＝「**白名单**：仅允许指定的 IP 地址访问服务，**其余默认拒绝**」／「**黑名单**：阻止特定 IP 地址访问服务，**其余默认允许**」；**IP地址/地址段**「支持多个条目，格式如`192.168.1.1/24`」[原文如此，该示例的网络位写法非常规] |
| **超时策略** | 「AI 网关提供API级别的超时设置……如果网关在设定的时间内未收到后端服务的响应，将向客户端返回一个 **HTTP 状态码为 504（Gateway Timeout）** 的响应结果」 | 开启（「开启：网关API超时策略生效」／「关闭：网关API超时策略失效」）；**超时时间「单位为秒」**；「**当设置为0或者关闭超时策略时，表示网关会一直等待请求的响应结果**」；「超时策略配置完成且开启后，请根据实际业务验证服务超时规则是否生效」 |
| **重试策略** | 「AI 网关提供API级别的重试设置，可以对出错的请求进行自动重试」；「当后端服务返回`5xx`错误时，AI 网关按照设置的重试次数对出错的请求自动进行重试」 | 开启；**重试次数「支持设置0~10次，建议不超过2次」**，「重试次数设置为0，表示取消重试」；重试条件（多选）；重试状态码（「**重试条件**指定`retriable-status-codes`，才能配置**重试状态码**」） |
| **Header修改策略** | 「在将请求转发至目标后端服务之前，或在后端服务的响应返回给客户端之前，Header设置功能允许修改原始请求中的头信息」 | 开启；**Header类型**＝请求/响应；**操作类型**＝新增/修改/删除；Header Key；Header Value。新增：「如果新增的Header已存在，那么Header Value将会**拼接在已有的Header值后面，并通过英文逗号（,）分隔**」；修改：「如果指定的Header不存在，将会按照Header Key和Header Value进行**新增**操作；如果指定的Header存在，将会进行**覆盖修改**操作」 |

全部来源：more-policies-and-plugins

**🔴 关闭重试策略后的网关内置默认值（易被误认为「关掉就不重试」，逐字引用）**

> 「关闭重试后，网关内部有**默认重试配置**，重试次数**默认为2次**，重试条件默认为 `connect-failure`、`refused-stream`、`unavailable`、`cancelled`、`non_idempotent`和 `retriable-status-codes`。」[官方原文｜more-policies-and-plugins]

**重试条件枚举**

| 协议 | 重试条件（原文） |
|---|---|
| HTTP | `5xx`（「如果后端服务返回任何`5xx`响应，或者发生连接断开、重置、读取超时事件……」；「`5xx`包含`connect-failure`和`refused-stream`的条件」）｜`reset`（「如果发生连接断开、重置、读取超时事件」）｜`connect-failure`（「如果请求是由连接断开导致的出错」）｜`refused-stream`（「如果后端服务以`REFUSED_STREAM`错误代码来重置流」）｜`retriable-status-codes`（「如果后端服务响应结果的HTTP状态码匹配上指定的重试状态码」；「只有在重试条件中指定了`retriable-status-codes`，才能使用重试状态码」） |
| gRPC | `cancelled`｜`deadline-exceeded`｜`internal`｜`resource-exhausted`｜`unavailable`（均为「如果后端gRPC服务的响应头部中的gRPC状态码为 X，AI 网关将尝试对该请求进行重试」） |

来源：more-policies-and-plugins

**⚠️ 与限流的边界（重要区分）**：`more-policies-and-plugins` 的「流量控制」（QPS 阈值）与「并发控制」（并发数阈值）是**独立于** §5.4/§5.5 AiTokenRateLimit 的另一套策略，且**只有这两者与熔断明确给出 429 兜底状态码**；AiTokenRateLimit 的超限返回码在两页限流文档中均未写。四者的关系与叠加顺序 → [文档未说明]。

**⚠️ IP 黑白名单的两处入口**：本页为 **API 级**「IP黑白名单」策略；另有 **网关级** IP 黑白名单页 `set-the-gateway-ip-whitelist-and-whitelist`（归 **W4**）。两者的优先级与叠加关系在本分片内 [文档未说明]。

### 5.11 AI 增强能力的 Token / Credits 消耗汇总（计费强相关）

| 能力 | 是否产生额外 Token / Credits | 官方原文 | 来源 slug |
|---|---|---|---|
| **智能路由** | **会产生额外 Token 消耗**（明文）；具体 Credits 口径推给「AI Credits 计费说明」 | 「智能路由会对请求进行语义分析，**可能产生额外 Token 消耗**。请在成本评估中一并考虑，具体计费以 AI Credits 计费说明为准。」 | configure-smart-routing |
| **联网搜索 - 意图识别** | **会消耗 Token，且监控不统计**（明文） | 「**意图识别**能力也会消耗Token，并且**不会在模型调用监控中被统计**。」 | networked-search |
| **联网搜索 - 搜索重写 / 多查询并发改写** | 会产生多次搜索（「生成多个搜索语句进行并发搜索」），单次搜索的计费口径 [文档未说明]；免费试用额度为「15天的免费试用，用量为1000次/天，性能限制5 QPS」 | 「若配置为大于1次，改写将会产生多个搜索语句进行并发搜索，并最终聚合个多个搜索的结果」 | networked-search |
| **AI 缓存 - 命中** | **输入 tokens 和输出 tokens 均为 0**（明文，降本） | 「若命中精确缓存（from-cache），则输入 tokens 和输出 tokens 均为 0」；「语义缓存命中时……输入和输出 tokens 均为 0，不消耗模型推理资源」 | ai-cache-1 |
| **AI 缓存 - 语义缓存的向量化调用** | 需配「AI 服务 + 模型名称」做文本向量化，该调用本身的 Token/Credits 消耗 [文档未说明] | 「**文本向量化配置**：**AI 服务**……**模型名称**：选择您计划使用的模型名称」 | ai-cache-1 |
| **模型元信息 Credits 单价** | 输入 / 输出 / 缓存三项，单位 **Credits/1M tokens**，「默认值为 0」 | 「输入 Token 消耗｜选填。单位 Credits/1M tokens，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0」 | model-metadata |
| **Fallback** | 是否额外计费 [文档未说明]（全页无 Credits/计费字样） | — | ai-fallback |
| **限流 / 配额 / 流控 / 熔断策略本身** | 是否消耗 Credits [文档未说明] | — | current-limiting、configure-a-modelapi-throttling-policy、consumer-quotas-management、more-policies-and-plugins |
| **AI 请求观测（记录请求/响应内容）** | 无 Credits 口径；但 FinOps 风险通知明文将日志字段与「计量成本」挂钩 | 「仅保留必要字段（如 `input_token`、`output_token` 等），禁用非必需字段，以**降低计量成本**」 | consumer-quotas-management、managing-the-model-api |

**🔴 文档级空白（务必告知主控）**：本分片 21 页中**没有任何一页给出「哪些 AI 增强能力消耗 AI Credits、哪些不消耗」的完整清单或单价**。`configure-smart-routing` 明确把口径推给「AI Credits 计费说明」（doc 3048572 → slug `ai-credits-billing-details`），该页**不在 W3 分片，归 W2**。按契约 §3.6，此处照实记录「以……为准」这句话本身，并标注为**文档级空白**：SA 报价智能路由 / 联网搜索 / 语义缓存时必须另走 `ai-credits-billing-details` + 购买页核验。

### §5 溯源

- `configure-smart-routing` — 配置智能路由（13423）：智能路由定义与适用范围（仅 OpenAI 兼容 / Anthropic 兼容的文本生成 Model API）、`auto/<目标>` 4 个优化目标表、「必须显式使用 `auto/<目标>`，单独填写 `auto` 不会作为默认目标使用」、路由维度（协议+路径+输入输出类型+Token上限+能力）、候选模型三要素与「缺少任一项时配置无法形成可用候选」、最多 5 个自定义候选且系统内置模型不占名额、需单独开通、默认启用且不可关闭消费者鉴权、「可能产生额外 Token 消耗……以 AI Credits 计费说明为准」、模型元信息五项维护要求、「模型元信息不是静态备注」告警、排障四查、OpenAI/Anthropic 调用示例
- `managing-the-model-api` — 管理 Model API（23549）：智能路由 IntentCode 五分类表（Coder/Math/Translation/Flash/Complex）与 Qwen 系列优势映射（与 configure-smart-routing 的 `auto/*` 口径构成 [官方矛盾 4]）、「多服务（按观测指标）和多模型服务（智能路由）需要将AI网关版本升级至`2.1.15`及以上」、Fallback 可开启并按顺序配置多条、首包超时毫秒且 0=不启用、协议转换改变 Token 统计结构（百炼 input token 含 cache token，Anthropic 不含）
- `ai-fallback` — Model API AI Fallback（3414）：触发条件「返回任意 HTTP 4xx、5xx 错误状态码」、按顺序/降序执行且成功即立即返回、支持多级 Fallback、可复用同一服务、「仅Fallback后端服务错误」开关（不开启则网关限流或其它拦截也会触发 Fallback）、模型名称默认透传、首包超时仅对流式响应生效且 0=不启用
- `current-limiting` — Model API 限流策略（22270）：控制台面限流全部事实——默认关闭、6 种判断条件、4 种匹配规则及优先级、3 种限流单位（Token「按大模型的传入传出 Token 消耗量计算」/请求数/并发数）、4 档时间窗口 + 并发数无窗口、固定 TTL 窗口语义与 01:23:10→02:23:10 示例、按 API 限流兜底与叠加生效、按模型自动转 `x-higress-llm-model` 精确匹配、`0.0.0.0/0` 匹配所有 IP、按消费者限流需先开启消费者认证、最多同时命中 10 条、规则关系为「或」、相同维度合并到同一规则组、几秒内生效、分布式轻微偏差、5 个配置示例全表、9 条常见问题
- `configure-a-modelapi-throttling-policy` — 配置 Model API Token 限流策略（22633）：OpenAPI 面全部事实——`PUT` + `UpdateHttpApi`、`deployConfigs[].policyConfigs[]`、`type` 固定 `"AiTokenRateLimit"`、AiTokenRateLimitConfig 四字段（rules/enableGlobalRules 默认 false/globalRules/redisConfig）、AiTokenRateLimitRule 六字段与自动填充规则、limitType 9 值、matchType 5 值及适用类型、limitMode 13 值（Token 6 档 + Request 6 档 + ConcurrencyLimit）及各档适用 limitType、redisConfig 6 字段与「默认使用内置KVStore」、limitValue > 0 且 Model 类型不超 Int32 最大值、8 项配置验证规则、**PolicyConfigs 整体替换会清空 AiFallback/AiStatistics 等其他策略**、rules/globalRules 全量更新、建议先 GetHttpApi、7 个 JSON 示例、6 条常见问题
- `consumer-quotas-management` — AI网关-管理消费者配额（8274）：FinOps 实例级配额全部事实——Token/Credits 两种规则类型、限额最小 1 默认 60000、重置周期自然日/周/月且创建后不可改、9 个时区清单与默认 UTC+8 且创建后不可改、规则名称 1~64 字符、单次最多 1000 个消费者、「同一消费者对应一个重置周期只能存在一条配额规则」与冲突覆盖/退回、多维度并存同时扣减、编辑不可改周期与时区、启停立即生效/失效、配额重置清零用量但不清日志记录、删除需输入规则名称、用量统计左右两栏字段与 5/10 条分页、超限后「无法继续调用模型，直到下一个周期重置」、前提（引擎 2.1.19+/Credits 需 2.1.20+/非旧版 Serverless 版型/已创建消费者/已开通 SLS 并开启日志投递）、**「配额是 FinOps 维度……限流是 QPS/并发维度」定性原文**、FinOps 风险短信含义+触发原因+两步消除+大额配额规避策略
- `ai-cache-1` — AI 缓存策略（13592）：Redis 精确缓存 + DashVector 语义缓存双引擎、策略对比表 5 维、命中判定（字符串完全一致 / 余弦相似度达阈值）、HNSW 与百万级毫秒检索、缓存键生成策略两选项、`x-higress-skip-ai-cache: on` 绕过语义、语义缓存 8 项配置（向量化超时默认 5000ms、向量库超时默认 3000ms、Collection 距离度量须 Cosine、维度须与向量化模型对应）、相似度阈值取值 (0,1) 建议 0.8~0.9 且不建议低于 0.8、精确缓存 7 项配置（三种访问方式、**缓存时长默认 1800 秒**）、Redis 白名单须加网关 VPC 网段、阈值调优与 A/B 测试建议、text-embedding-v4(1024维)+阈值0.85 的 4 行效果对比表、缓存命中率查询（须先开通日志服务、粒度为网关级别、日志源 apig-plugin-log、`gw-` 前缀一处保留一处不保留、示例 7/6/53.85%）、命中时输入输出 tokens 均为 0 与未命中示例 127/40
- `networked-search` — 联网搜索策略（7606）：默认关闭、仅支持夸克（阿里云信息查询服务）、服务状态未开通→前往开通→开通校验→试用中、**15 天免费试用/1000 次每天/5 QPS**、返回结果数量 1-10、搜索超时默认 3000ms、查询时间范围 5 档、行业 7 项、默认语言中英、输出引用来源默认否、引用来源位置默认首部、内容类型摘要（默认）/正文、引用格式 `%s`、自动启用开关语义、**意图识别消耗 Token 且不在模型调用监控中统计**、意图识别超时默认 5000ms、搜索重新生成最大查询次数默认 1、`web_search_options` 激活、`search_context_size` low=1/medium=3（默认）/high=5、curl 样例
- `more-policies-and-plugins` — API 级策略与插件配置（16275）：入口（策略与插件 > 更多策略与插件 > 入站处理/出站处理）、「策略配置修改后即时生效，无需重新发布」、请求流向「前端API → 入站处理 → 后端服务 → 出站处理」、并发控制（总体并发数阈值 + Web fallback Http状态码默认429）、流量控制（总体QPS阈值 + 429）、熔断策略（统计窗口 1秒~120分钟、最小请求数目、慢调用比例/异常比例、慢调用RT、熔断比例阈值 0-100、熔断时长）、IP黑白名单（白名单其余默认拒绝/黑名单其余默认允许）、超时策略（单位秒、超时返回 504、设为 0 或关闭则一直等待）、重试策略（0~10 次建议不超过 2 次、0=取消重试、**关闭后网关内置默认重试 2 次及 6 个默认重试条件**、retriable-status-codes 前置条件）、HTTP 5 条与 gRPC 5 条重试条件、Header修改策略（新增拼接逗号/修改不存在则新增存在则覆盖）、插件安装 3 步流程
- `manage-the-ai-api` — Model API 管理快速入门（7403）：与 managing-the-model-api 交叉验证协议转换影响 Token 统计结构的同一原文；智能路由/按观测指标的 2.1.15 版本门槛
- `model-metadata` — 管理模型元信息（8625）：Credits 三项单价单位 Credits/1M tokens 且默认 0、最多两位小数、能力特性 15 项含「联网搜索｜支持 Web Search」、可用路径与 3 种协议类型（智能路由候选适配依据）
- `route-list` — Model API 自定义路由管理（4293）：路由级 Fallback「按照降序执行」且「支持重复使用同一个服务组建多条策略」
- `manage-global-authentication`、`manage-providers`、`manage-services`、`manage-service-sources`、`create-a-service-source`、`creating-services`、`configure-service-health-checks`、`create-an-api-product-of-the-model-api-type`、`product-category-management` — 本章仅用于交叉引用（API 级策略与全局认证鉴权分属不同入口；API 产品模型参数含「支持联网搜索」；健康检查/被动隔离与限流、熔断共同构成后端保护链）

- **本章查无**（翻过但本分片文档确实没写的高价值问题）：
  1. **限流触发后返回的 HTTP 状态码、响应体、错误码** —— 🔴 **2026-09-21 主控修正（R1 DEF-4 + R2a P0-5）**：current-limiting 与 configure-a-modelapi-throttling-policy 两页均 [文档未说明]，**但 `custom-response-plugin` 页有明文「触发网关限流时一般会返回429状态码」+ 完整自定义应答样例**（见 §5 对照表「超限返回什么？」行）。仍成立的空白：该 429 是否对全部限流单位（Token/请求数/并发数）与全部判断条件一律成立、未装 custom-response 时的默认响应体（只有 more-policies-and-plugins 的流量控制/并发控制/熔断给了「默认为429」，属另一套策略）
  2. **配额超限后返回的 HTTP 状态码与错误体** —— consumer-quotas-management 只写「消费者将无法继续调用模型」，[文档未说明]。⚠️ 注意与**限流**超限区分：限流侧有 `custom-response-plugin`「触发网关限流时一般会返回429状态码」的明文（见 §5 对照表），但**配额（FinOps）侧无任何等价明文**，不可把 429 类推到配额超限
  3. **Token 限流是否计入缓存 Token / 推理 Token / 联网搜索意图识别 Token / 智能路由语义分析 Token** —— 全部 [文档未说明]
  4. **Token 计数使用哪个 tokenizer、按哪个协议口径** —— [文档未说明]（仅知协议转换会改变 input token 是否含 cache token）
  5. **限流计数的偏差上限（百分比或绝对值）** —— 仅「可能存在轻微偏差」，[文档未说明]
  6. **单个 Model API 可配置的限流规则条数上限**（区别于「最多同时命中 10 条」）—— [文档未说明]
  7. **限流规则是否支持按域名 / 按路由（自定义路由）维度** —— 6 种判断条件中无此二者，[文档未说明]
  8. **控制台能否配置「每周 / 每月」Token 限流**（OpenAPI 有 TokenPerWeek/TokenPerMonth，控制台只列 4 档）—— [文档未说明]，且已作为 [官方矛盾 2] 上报
  9. **限流/配额是否支持预扣（请求前按 max_tokens 预估扣减）** —— [文档未说明]
  10. **AI Credits 单价与「哪些 AI 增强能力消耗 Credits」的完整清单** —— 本分片 [文档未说明]，官方推给 `ai-credits-billing-details`（归 W2）
  11. **智能路由的开通是否有单独收费、是否仅企业版/特定版型支持** —— configure-smart-routing 仅「需要单独开通……单击前往开通」，费用与版型限制 [文档未说明]
  12. **智能路由语义分析用的模型是哪个、能否自定义、其 Token 消耗量级** —— [文档未说明]
  13. **智能路由 `auto/*` 四个目标的实际选路算法与权重** —— 仅「先排除不适配当前请求的候选，再在其余候选中按目标进行选择」，[文档未说明]
  14. **IntentCode（Coder/Math/Translation/Flash/Complex）是否仍可用、如何调用** —— managing-the-model-api 未给请求格式，[文档未说明]（已作为 [官方矛盾 4] 上报）
  15. **Fallback 的最大条数、每级超时、全部失败后的返回码、是否跨供应商/跨协议 Fallback** —— [文档未说明]
  16. **Fallback 与重试策略（more-policies-and-plugins）的先后顺序与是否叠加** —— [文档未说明]
  17. **语义缓存的 TTL / 过期策略 / 容量上限 / 条目数上限** —— [文档未说明]（精确缓存有「缓存时长默认1800秒」，语义缓存无对应项）
  18. **语义缓存的向量维度上限、DashVector Collection 规格要求、是否支持多 Collection** —— [文档未说明]
  19. **AI 缓存能否两种模式同时开启、优先级如何** —— 「您需要根据策略对比选择适合的缓存方式」，是否互斥 [文档未说明]
  20. **缓存命中率是否支持按 API / 按消费者维度查询** —— 明文「目前支持的查询粒度为**网关级别**」，更细粒度 [文档未说明]
  21. **联网搜索免费试用 15 天到期后的正式接口单价** —— [文档未说明]，官方推给「正式开通流程说明」（doc 2869993，不在本分片）
  22. **联网搜索的调用次数如何计量（每次请求算 1 次还是每个搜索查询算 1 次）** —— 「搜索重新生成的最大查询次数」默认 1、`search_context_size` 可生成 1/3/5 个查询，但计费按哪个口径 [文档未说明]
  23. **联网搜索是否支持非文本生成场景（图片/视频/Embedding/Rerank）** —— [文档未说明]
  24. **并发控制 / 流量控制 / 熔断三者的默认开关状态与阈值取值范围**（仅熔断的统计窗口 1秒~120分钟、熔断比例阈值 0-100 有范围）—— [文档未说明]
  25. **超时策略的默认超时时间** —— 仅「单位为秒」「设置为0或者关闭……一直等待」，默认值 [文档未说明]
  26. **API 级策略与 AiTokenRateLimit 限流的执行顺序（哪个先拦）** —— [文档未说明]
  27. **入站处理 / 出站处理各支持哪些策略与插件、是否有顺序控制** —— 仅给出挂载列表示例，[文档未说明]
  28. **FinOps 配额是否支持按 Model API / 按模型维度设置**（当前仅「实例级别对消费者」）—— [文档未说明]
  29. **Credits 配额与模型元信息 Credits 单价（Credits/1M tokens）的换算公式** —— [文档未说明]
  30. **配额用量的统计延迟（实时 or T+N）** —— [文档未说明]
  31. **FinOps 功能的上线日期与灰度地域** —— 仅「新增 FinOps 功能」+ 引擎版本门槛 2.1.19/2.1.20，[文档未说明]
