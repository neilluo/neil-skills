---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/new-feature-release-notes-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: new-feature-release-notes-ai-gateway
body_sha256: 57ba67c154fdeb28ccd7e4bfa2d34811741d88cfd5fe2ec6335be41997c42846
body_bytes: 14419
migration_status: current
---

本文介绍 AI 网关的版本变更信息，包括发布时间、功能说明以及相关文档等信息。  

## 2026 年
### 2026-07

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>多租 Serverless 正式开启公测，提供企业版与标准版，最低 0 起步，公测期间免费试用。</p></li> <li><p>支持模型资产管理，提供模型元信息与供应商管理，可对模型进行 Credits 配额管控。</p></li> <li><p>FinOps 支持自定义周期配额，支持 Credits 管控。</p></li> <li><p>自定义 Model/Agent API 支持 HTTP 重写。</p></li> <li><p>支持与全球加速 GA 的集成。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td> <ul> <li><p>安全护栏支持并行检测配置。</p></li> <li><p>网关接入点支持移除。</p></li> </ul></td> </tr> </tbody> </table>

### 2026-06

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>上线FinOps能力，支持消费者级别的Token配额限制</p></li> <li><p>支持消费者组，可对消费者按组划分，实现消费者组级别的API授权</p></li> <li><p>支持千问云以及百炼Token Plan的对接</p></li> <li><p>支持接入KlingAI等类型的文生图、文生视频模型</p></li> <li><p>支持VertexAI Claude模型的OpenAI与Anthropic访问协议</p></li> <li><p>支持AI服务多API Key场景下的Failover，提升模型调用的稳定性与成功率</p></li> </ul></td> </tr> </tbody> </table>

### 2026-05

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td><p>AWS Bedrock 服务支持 Anthropic 协议调用。</p></td> </tr> <tr> <td><p>新功能</p></td> <td><p>支持对接安全护栏自定义 Agent 规则，支持返回拦截信息及对应 RequestID。</p></td> </tr> <tr> <td><p>新功能</p></td> <td><p>支持对连接数、自动扩容 Unit 数的监控。</p></td> </tr> <tr> <td><p>新功能</p></td> <td><p>AI 网关新增 FinOps 消费者配额能力，支持消费者在实例级别设置 Token 配额，支持按自然日/月/年设置配额周期，支持配额规则时区设置、配额重置及配额使用水位监控。</p><p>新增 Credits 配额维度。创建配额规则时，在<b>规则类型</b>中可选择 Token 配额或 Credits 配额。Credits 为统一计量单位，跨模型归一化成本。两种配额类型的设置方式相同，均支持按自然日/周/月设置重置周期、时区设置、配额重置及用量监控。</p></td> </tr> </tbody> </table>

### 2026-04

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>集成 HiMarket，支持通过控制台搭建 AI 开放平台，进行 API 产品管理、门户管理与产品分类管理。</p></li> <li><p>支持 AI 安全护栏脱敏能力，包括文本脱敏和图片脱敏。</p></li> <li><p>支持自定义配置 AI 安全护栏的返回信息。</p></li> <li><p>支持开通公网后关闭公网。</p></li> <li><p>支持配置第三方代理 Base URL。</p></li> </ul></td> </tr> </tbody> </table>

### 2026-03

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>开服</p></td> <td><p>新增亚特兰大地域。</p></td> </tr> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>支持百炼语言识别 Fun-ASR 及 Qwen3-vl-embedding 模型。</p></li> <li><p>Token 限流支持 7 天、30 天限制，支持更灵活的用量控制场景。</p></li> <li><p>支持模型日志字段参数映射，将模型返回的字段与网关的日志字段映射，统一解决各类模型的可观测适配问题。</p></li> <li><p>Bedrock 服务支持 Prompt Caching 配置，可降低推理成本和响应延迟。</p></li> <li><p>Claude 服务支持 ClaudeCodeMode 配置，解决 Claude Code 对接时的鉴权冲突问题。</p></li> <li><p>AI 安全护栏防护维度新增自定义 Agent（CustomLabel），可针对自定义 Agent 服务进行安全防护。</p></li> <li><p>AI 网关与普通网关支持区分默认告警规则类型，AI 网关使用专属告警指标（AIGatewayEnvoyCpuUsageRate、AIGatewayEnvoyMemoryUsageRate、AIGatewayEnvoyPluginCrash）。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td> <ul> <li><p>创建 AI 服务时，Base URL 支持配置 Claude、Gemini 等模型的第三方代理平台地址。</p></li> <li><p>解决用户同时配置健康检测和大模型负载均衡导致的配置推送失败问题，产品侧增加互斥校验。</p></li> <li><p>资源配额扩大，适配用户的更大使用规模。</p></li> <li><p>Token 限流策略支持依据引擎版本过滤限流模式，每周/每月限流（TokenPerWeek/TokenPerMonth/RequestPerWeek/RequestPerMonth）需引擎版本 ≥ 2.1.15。</p></li> <li><p>创建 AI 服务时，Bedrock 供应商支持选择端点模式（Mantle 或 Runtime），Mantle 模式下自动使用 Anthropic 协议且不支持 Prompt Caching。</p></li> </ul></td> </tr> </tbody> </table>

### 2026-02

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>支持百炼 Embedding 原生协议。</p></li> <li><p>Agent API 支持 AI 可观测。</p></li> <li><p>Agent API 支持调试能力。</p></li> <li><p>新增 API 创建模板，快速创建简单文本模型代理与高可用模型代理。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td> <ul> <li><p>Agent 服务支持配置内网 DNS 解析。</p></li> <li><p>更新百炼 Anthropic 兼容接口标准。</p></li> <li><p>新增快速开始，优化 AI 网关操作链路信息展示。</p></li> </ul></td> </tr> </tbody> </table>

### 2026-01

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>Model API 支持 Vertex AI 的原生 Gemini 协议，覆盖 Gemini、Nano Banana、Veo3 等模型。</p></li> <li><p>在 Dify 的模型供应商中提供官方 Higress 插件，方便用户接入 AI 网关代理模型。</p></li> <li><p>百炼 Agent API 支持接入 AI 安全护栏。</p></li> <li><p>MCP Server 支持 JWT 认证。</p></li> </ul></td> </tr> </tbody> </table>

## 2025 年
### 2025-12

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><a href="https://help.aliyun.com/document_detail/2883382.html">开服</a></p></td> <td><p>新增马来西亚地域。</p></td> </tr> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>新增风险管理能力。</p></li> <li><p>自定义协议的 Model API 支持配置路由级 fallback。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td> <ul> <li><p>对于非安全的鉴权插件进行风险提示。</p></li> <li><p>同步自 Nacos 的 MCP Server 支持移除和编辑域名。</p></li> <li><p>支持代理 vertex AI 上的 gemini3 模型。</p></li> <li><p>代理的 Azure openAI 服务支持不包含 deployment-id 的 endpoint 格式。</p></li> </ul></td> </tr> </tbody> </table>

### 2025-11

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>Model API 支持服务节点的负载感知路由，可基于推理框架的监控数据智能调度服务节点。</p></li> <li><p>直接代理的 MCP Server 支持展示工具粒度的消费者授权、工具组装和语义检索。</p></li> <li><p>服务支持 Cloudflow。</p></li> <li><p>AI 安全防护支持图片防护。</p></li> </ul></td> </tr> </tbody> </table>

### 2025-10

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>AI 安全防护支持按消费者配置拦截策略和 service。</p></li> <li><p>Model API 限流策略新增请求数和并发数维度，且支持在 embedding、rerank 和多模态场景开启。</p></li> <li><p>Embedding 场景的 Model API 支持按模型名称路由到多个服务提供商。</p></li> <li><p>多模态、Embedding 和 Rerank 场景的 Model API 支持设置策略和插件。</p></li> <li><p>Agent API 新增可观测大盘。</p></li> <li><p>自定义协议的 Agent API 支持按请求权重路由到多个后端服务。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td><p>openAI 兼容协议下 AI 观测支持记录 responses API 的 question 和 answer。</p></td> </tr> <tr> <td><p>修复</p></td> <td><p>修复停止状态的实例不支持续费的问题。</p></td> </tr> </tbody> </table>

### 2025-09

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新商品</p></td> <td><p>AI 网关发布 Serverless 版本，最高节省 90%成本。</p></td> </tr> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>MCP 工具支持<a href="https://help.aliyun.com/document_detail/2983780.html">语义检索</a>。</p></li> <li><p>MCP Server 支持 <a href="https://help.aliyun.com/document_detail/2978406.html">Tool 组装</a>。</p></li> <li><p>MCP Server 支持 <a href="https://help.aliyun.com/document_detail/2983795.html">按比例灰度服务</a>。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2937089.html">Agent API</a> 支持策略与插件。</p></li> <li><p>AI 网关支持在日志中开关 question 和 answer 的写入。</p></li> <li><p>AI 安全防护支持按多个防护维度分别设置拦截策略。</p></li> </ul></td> </tr> </tbody> </table>

### 2025-08

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>支持<a href="https://help.aliyun.com/document_detail/2978735.html">密钥管理</a>，通过对接 KMS，实现消费者凭证、API-KEY、插件配置中的敏感信息等的安全管理。</p></li> <li><p>新增虚拟 MCP Server，可自由<a href="https://help.aliyun.com/document_detail/2978406.html">组装已有 MCP Server 的工具</a>，形成新的 MCP Server。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2859333.html">Model API</a> 支持 <a href="https://help.aliyun.com/document_detail/2978432.html">ComfyUI 服务</a>。</p></li> </ul></td> </tr> <tr> <td><p><a href="https://help.aliyun.com/document_detail/2883382.html">开服</a></p></td> <td><p>新增韩国地域。</p></td> </tr> </tbody> </table>

### 2025-07

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p><a href="https://help.aliyun.com/document_detail/2859333.html">Model API</a>支持代理万相、cosyvoice 等多模态模型。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2859333.html">Model API</a>支持代理 rerank 模型。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2859333.html">Model API</a>支持为 openAI 兼容协议添加 responses 接口。</p></li> <li><p>MCP Server 支持包括 tool 调用在内的可观测。</p></li> <li><p>MCP Server 支持<a href="https://help.aliyun.com/document_detail/2930333.html#4e9068601f0vw">MCP 工具级别消费者认证</a>。</p></li> </ul></td> </tr> <tr> <td><p>优化</p></td> <td> <ul> <li><p>MCP 配置格式错误时透出详细错误信息。</p></li> <li><p>MCP Server 配置保存时增加预检。</p></li> </ul></td> </tr> <tr> <td><p><a href="https://help.aliyun.com/document_detail/2883382.html">开服</a></p></td> <td><p>新增青岛地域。</p></td> </tr> </tbody> </table>

### 2025-06

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>新增<a href="https://help.aliyun.com/document_detail/2937089.html">Agent API</a>，支持代理百炼应用和 Dify。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2873942.html">AI 缓存</a>支持语义化缓存策略。</p></li> <li><p>Model API 支持 <a href="https://help.aliyun.com/document_detail/2925740.html">fine_tuning 接口</a>。</p></li> </ul></td> </tr> </tbody> </table>

### 2025-05

<table> <thead> <tr> <td><p><b>变更类型</b></p></td> <td><p><b>功能说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>新功能</p></td> <td> <ul> <li><p>支持<a href="https://help.aliyun.com/document_detail/2930331.html">从 Nacos MCP Registry 导入 MCP Server</a>。</p></li> <li><p>LLM API 支持<a href="https://help.aliyun.com/document_detail/2925740.html">自定义路由</a>，满足按请求特征进行精细化路由的能力。</p></li> <li><p>AI 服务支持直接<a href="https://help.aliyun.com/document_detail/2870215.html">对接 PAI EAS</a>并在运行时自动获取 API-KEY。</p></li> <li><p>支持直接添加<a href="https://help.aliyun.com/document_detail/2870215.html">PAI-EAS 服务</a>作为 AI 服务后端。</p></li> <li><p><a href="https://help.aliyun.com/document_detail/2873940.html">内容安全</a>升级为 AI 安全围栏。</p></li> <li><p>支持将<a href="https://help.aliyun.com/document_detail/2873944.html">搜索</a>设置为默认关闭，通过客户端参数手动启用搜索。</p></li> </ul></td> </tr> </tbody> </table>