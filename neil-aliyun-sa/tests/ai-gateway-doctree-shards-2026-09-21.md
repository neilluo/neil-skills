# ai-gateway 文档树 · 分片清单与范围裁决

生成：2026-09-21 ｜ 生成器：`scripts/build-doc-inventory.py`（确定性解析，非 LLM 归纳）｜ 源：`tests/ai-gateway-llms-2026-09-21.txt`

llms.txt 链接总数 **438** = core **188** + deferred **250**

## 一、按栏目分类计数

| 栏目 | core（本次蒸馏） | deferred（延后） | external |
|---|---|---|---|
| 产品概述 | 19 | 0 | 0 |
| 快速入门 | 3 | 0 | 0 |
| 操作指南 | 139 | 0 | 0 |
| 安全合规 | 7 | 0 | 0 |
| 实践教程 | 9 | 0 | 0 |
| 开发参考 | 8 | 250 | 0 |
| 服务支持 | 3 | 0 | 0 |
| **合计** | **188** | **250** | **0** |

分类判据（**精确 slug 允许表，非关键词子串**）：`/developer-reference/` 下 slug 形如 `api-apig-2024-03-27-*` → deferred（逐 Action / 逐数据结构参考页），除非其 tail 精确等于 {overview-ai-gateway, endpoint-ai-gateway, ram-ai-gateway, quota-ai-gateway, changeset-ai-gateway, errorcodes}，或 slug 精确等于 {developer-reference, api-reference, sdk-reference, cli-reference} → core。其余栏目一律 core。**不做语义猜测**，判据可复算。

> 🔴 首版曾用关键词子串白名单（overview/quota/ram/...），实测误纳 11 页逐 Action 页：`getresourceoverview`（含 overview）、10 个 `*gatewayquotarule*`（含 quota）、`struct-httpapiparameter-ai-gateway`（pa**ram**eter 含 ram）。已改为精确允许表。

## 二、core 分片（蒸馏 worker 指派单位）

### SHARD-1（19 页 ｜ 栏目：产品概述）

- `product-overview.md` — 产品概述 📁容器
- `what-is-an-ai-gateway.md` — AI 网关产品概述
- `new-feature-release-notes-ai-gateway.md` — 新功能发布记录
- `dynamics-and-announcements.md` — AI网关-动态与公告
- `ai-gateway-commercialization-announcement.md` — AI 网关 Serverless 新版商业化公告（2026年9月起计费）
- `announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta.md` — AI网关Serverless新版公测公告
- `engine-version-description.md` — AI 网关引擎版本说明
- `supported-regions.md` — AI 网关开服地域
- `product-comparison.md` — AI 网关与 Higress 开源版对比
- `product-billing.md` — 产品计费 📁容器
- `free-product-templates.md` — AI网关-专享实例计费说明
- `overview-of-billing-during-the-serverless-public-preview-of-the.md` — AI网关Serverless新版公测计费说明
- `serverless-old-billing-details.md` — AI网关Serverless旧版计费说明
- `ai-credits-billing-details.md` — AI Credits 计费说明
- `ai-gateway-capacity-description.md` — 网关类型
- `capacity-description.md` — AI网关-容量规格与资源配额
- `query-bills.md` — 查看 AI 网关账单
- `description-of-arrears.md` — AI 网关欠费与到期处理
- `refund.md` — AI 网关退款说明

### SHARD-2（26 页 ｜ 栏目：快速入门、操作指南）

- `getting-started.md` — 快速入门 📁容器
- `manage-the-ai-api.md` — Model API 管理快速入门
- `mcp-service-management.md` — MCP 服务管理快速入门
- `user-guide.md` — 操作指南 📁容器
- `model-metadata-and-provider-management.md` — 模型元信息与供应商管理 📁容器
- `model-metadata.md` — 管理模型元信息
- `manage-providers.md` — 管理供应商
- `gateway-management.md` — 网关管理 📁容器
- `create-a-gateway-instance.md` — 创建 AI 网关实例
- `view-gateway-instance-details.md` — 查看网关实例详情
- `modifying-gateway-parameter-configurations.md` — 修改网关引擎参数
- `set-security-group-rules.md` — 配置安全组授权规则
- `model-api-management.md` — Model API管理 📁容器
- `managing-the-model-api.md` — 管理 Model API
- `add-policies-and-plug-ins.md` — 策略与插件 📁容器
- `current-limiting.md` — Model API 限流策略
- `ai-cache-1.md` — AI 缓存策略
- `content-security-protection.md` — AI 安全防护
- `networked-search.md` — 联网搜索策略
- `more-policies-and-plugins.md` — API 级策略与插件配置
- `tool-selection.md` — 工具精选策略
- `consumer-authentication.md` — Model API 消费者鉴权
- `ai-observable.md` — Model API 可观测
- `route-list.md` — Model API 自定义路由管理
- `ai-fallback.md` — Model API AI Fallback
- `configure-smart-routing.md` — 配置智能路由

### SHARD-3（26 页 ｜ 栏目：操作指南）

- `agent-api-management.md` — Agent API管理 📁容器
- `manage-agent-apis.md` — 管理 Agent API
- `routing-management.md` — Agent API 自定义路由管理
- `consumer-certification-1.md` — Agent API 消费者认证
- `configure-policies-and-plug-ins.md` — Agent API 策略与插件配置
- `agent-api-observable.md` — Agent API 可观测
- `mcp-service-management-1.md` — MCP服务管理 📁容器
- `mcp-gateway-management.md` — 创建网关托管 MCP 服务
- `synchronizing-nacos-mcp-services.md` — 同步 Nacos MCP 服务
- `consumer-certification.md` — MCP 消费者认证
- `enable-mcp-service-log-delivery.md` — 开启 MCP 服务日志投递
- `debug-mcp-services.md` — AI 网关-调试MCP服务（控制台与MCP Inspector）
- `http-to-mcp-field-configurations.md` — HTTP to MCP 配置字段参考（YAML/认证/模板语法）
- `configure-policies-and-plugins-1.md` — MCP Server 策略与插件配置
- `mcp-observable.md` — MCP 服务可观测
- `mcp-tool-assembly.md` — MCP Tool 组装
- `semantic-retrieval.md` — MCP 语义检索
- `mcp-grayscale-release.md` — MCP 服务灰度发布
- `agent-management-access-and-observation.md` — Agent 管理
- `service-management.md` — 服务管理 📁容器
- `service.md` — 服务 📁容器
- `creating-services.md` — 添加后端服务
- `manage-services.md` — 查看、编辑与删除服务
- `configure-service-health-checks.md` — 配置服务健康检查
- `configure-dns-server.md` — 配置 DNS 服务器
- `service-source.md` — 服务来源 📁容器

### SHARD-4（26 页 ｜ 栏目：操作指南）

- `create-a-service-source.md` — 添加 ACK 容器服务来源
- `manage-service-sources.md` — 管理服务来源
- `domain-name-management-1.md` — 域名管理 📁容器
- `create-a-domain-name.md` — 创建域名
- `delete-a-domain-name.md` — 编辑或删除域名
- `change-the-protocol-and-certificate-of-the-domain-name.md` — 更换域名协议和证书
- `setting-the-specified-https-cipher-suite.md` — 设置 HTTPS 加密套件
- `secret-key-management.md` — 密钥管理 📁容器
- `create-secret-key.md` — 创建密钥
- `reference-secret-key.md` — 引用密钥
- `edit-and-delete-secret-key.md` — 编辑与删除密钥
- `tags-and-resources.md` — 标签与资源 📁容器
- `label.md` — 实例标签管理
- `resource-group.md` — 资源组管理
- `consumer-management.md` — 消费者管理 📁容器
- `creating-a-consumer.md` — 创建消费者
- `authorization-management.md` — 消费者授权管理
- `consumer-quotas-management.md` — AI网关-管理消费者配额
- `deactivate-or-delete-a-consumer.md` — 停用或删除消费者
- `observation-analysis.md` — 观测分析 📁容器
- `request-response-capture-1.md` — API网关请求/响应采集（Body最大5KB/日志字段与版本要求）
- `view-gateway-monitoring-data.md` — 查看网关监控数据
- `enable-gateway-log-delivery.md` — 开启网关日志投递
- `enable-gateway-link-tracing.md` — 开启网关链路追踪
- `security-capability-management.md` — 安全能力管理 📁容器
- `set-the-gateway-ip-whitelist-and-whitelist.md` — 设置网关 IP 黑白名单

### SHARD-5（26 页 ｜ 栏目：操作指南）

- `consumer-authentication-authentication.md` — 消费者认证鉴权
- `global-authentication.md` — 全局认证鉴权 📁容器
- `configure-jwt-authentication.md` — 全局 JWT 认证鉴权配置
- `configure-oidc-authentication.md` — 全局 OIDC 认证鉴权配置
- `configure-self-built-authentication.md` — 全局自建认证鉴权配置
- `manage-global-authentication.md` — 全局认证鉴权管理
- `plug-in-market.md` — 插件市场 📁容器
- `manage-plug-ins.md` — 插件安装启用与卸载
- `develop-plug-ins-1.md` — 开发插件 📁容器
- `develop-gateway-plug-ins-using-the-go-language.md` — Go 语言开发网关插件
- `developing-gateway-plug-ins-using-rust-and-c-languages.md` — Rust 与 C++ 开发网关插件
- `upload-plug-in.md` — 发布自定义插件
- `plug-in-performance-reference.md` — 插件性能参考
- `platform-plug-ins.md` — 平台插件 📁容器
- `authentication.md` — 认证鉴权 📁容器
- `key-auth-plug-ins.md` — key-auth 插件
- `basic-auth-plug-ins.md` — basic-auth 插件
- `hmac-auth-plug-ins.md` — hmac-auth 插件
- `jwt-auth-plug-ins.md` — jwt-auth 插件
- `jwt-logout-plug-ins.md` — jwt-logout 插件
- `oauth-plugin.md` — oauth 插件
- `flow-control.md` — 流量管控 📁容器
- `key-rate-limit-plugin.md` — key-rate-limit 插件
- `http-real-ip-plug-ins.md` — http-real-ip 插件
- `hsts-plug-in.md` — hsts 插件
- `canary-header-plugin.md` — canary-header 插件

### SHARD-6（26 页 ｜ 栏目：操作指南）

- `the-traffic-tag-plugin.md` — traffic-tag 插件
- `throttle-based-on-cluster-keys.md` — cluster-key-rate-limit 插件
- `transport-protocol.md` — 传输协议 📁容器
- `degraphql-plugin.md` — DeGraphQL 插件
- `front-end-grayscale-plug-in.md` — frontend-gray 前端灰度插件
- `browser-cache-control.md` — cache-control 浏览器缓存插件
- `geographic-location-of-ip.md` — geo-ip 插件
- `custom-response-plugin.md` — custom-response 插件
- `safety-protection.md` — 安全防护 📁容器
- `request-block-plugin.md` — request-block 插件
- `bot-detect-plug-ins.md` — bot-detect 插件
- `waf-plugin.md` — waf 插件
- `parameter-access-control.md` — param-access-control 参数访问控制
- `ai-plug-in.md` — AI插件 📁容器
- `ai-retrieval-augmented-generation-enhanced.md` — AI 检索增强生成加强版
- `ai-retrieval-agent.md` — AI RAG 检索代理
- `ai-rag.md` — AI RAG 插件
- `ai-cue-template.md` — AI 提示词插件
- `ai-cue-decorator.md` — AI 提示词模板插件
- `ai-request-response-intelligent-transformation.md` — AI 请求响应转换插件
- `ai-auxiliary-plug-in-development.md` — AI 辅助插件开发
- `webide-writing-plug-ins.md` — WebIDE 编写插件
- `policy-management.md` — 策略管理 📁容器
- `configure-a-modelapi-throttling-policy.md` — 配置 Model API Token 限流策略
- `configure-ai-log-policy.md` — 配置 AI 日志策略
- `open-platform.md` — 开放平台 📁容器

### SHARD-7（19 页 ｜ 栏目：安全合规、操作指南）

- `portal-management.md` — 门户管理 📁容器
- `create-portal.md` — 创建开发者门户
- `deployment-portal.md` — 部署开发者门户服务
- `developer-guide.md` — 开放平台开发者操作指南
- `configure-oidc-login-for-portal.md` — 门户 OIDC 单点登录配置
- `hichat-ai-interaction-center.md` — HiChat AI 交互中心
- `api-product-management.md` — API 产品管理 📁容器
- `api-product-introduction.md` — API 产品概念介绍
- `create-an-api-product-of-the-model-api-type.md` — 创建 Model API 类型产品
- `mcp-server-product.md` — 创建 MCP Server 类型产品
- `create-an-api-product-of-the-agent-api-type.md` — 创建 Agent API 类型产品
- `product-category-management.md` — API 产品分类管理
- `security-and-compliance.md` — 安全合规 📁容器
- `identity-management-and-access-control.md` — 使用RAM进行访问控制 📁容器
- `identity-management.md` — AI 网关 RAM 身份管理
- `identity-based-policies.md` — 基于身份的策略 📁容器
- `ai-gateway-system-permission-policy-reference.md` — AI 网关系统权限策略参考
- `custom-permission-policy-reference-for-ai-gateway.md` — AI 网关自定义权限策略参考
- `service-association-role-provided-only-when-involved-otherwise-no-need.md` — AI 网关服务关联角色

### SHARD-8（17 页 ｜ 栏目：实践教程、开发参考）

- `use-cases.md` — 实践教程 📁容器
- `deepseek-integration-through-ai-gateway.md` — AI 网关接入 DeepSeek 模型
- `pai-deployment-model-access-ai-gateway.md` — AI 网关接入 PAI-EAS 部署模型
- `manage-ai-gateway-mcp-services-via-openapi.md` — OpenAPI 管理 MCP 服务
- `proxy-comfyui-service-via-ai-gateway.md` — AI 网关代理 ComfyUI 服务
- `migrate-the-official-claude-code-model-to-any-model-using-ai-gateway.md` — Claude Code 迁移至任意模型
- `enable-llm-api-compression-to-save-bandwidth-costs.md` — LLM API 响应压缩节省带宽
- `proxy-dify-inbound-and-outbound-traffic-through-ai-gateway.md` — AI 网关代理 Dify 出入流量
- `access-vertex-ai-through-ai-gateway.md` — AI 网关接入 Vertex AI
- `developer-reference.md` — 开发参考 📁容器
- `api-reference.md` — API参考 📁容器
- `api-apig-2024-03-27-overview-ai-gateway.md` — AI网关OpenAPI概览（HTTP API/接口/模型供应商管理）
- `api-apig-2024-03-27-endpoint-ai-gateway.md` — APIG 服务接入点
- `api-apig-2024-03-27-ram-ai-gateway.md` — AI网关-RAM授权信息 Action/Resource/Condition定义
- `api-apig-2024-03-27-quota-ai-gateway.md` — APIG OpenAPI 流控配额
- `api-apig-2024-03-27-changeset-ai-gateway.md` — APIG OpenAPI 变更集
- `api-apig-2024-03-27-errorcodes.md` — AI 网关公共错误码（403/409/500 与 APIG.ErrorCode 排查）

### SHARD-9（3 页 ｜ 栏目：服务支持）

- `support.md` — 服务支持 📁容器
- `related-agreements.md` — 相关协议 📁容器
- `service-level-agreement.md` — AI 网关服务等级协议

## 三、纳入 core 的开发参考元页（白名单破例，逐条列出以便复核）

- `api-reference.md` — API参考
- `api-apig-2024-03-27-overview-ai-gateway.md` — AI网关OpenAPI概览（HTTP API/接口/模型供应商管理）
  - 摘要：AI网关(APIG 2024-03-27) OpenAPI目录：HTTP API创建/导入/发布/下线、接口管理、AI模型供应商管理。ROA签名，提供多语言SDK，支持自签名接入。
- `api-apig-2024-03-27-endpoint-ai-gateway.md` — APIG 服务接入点
  - 摘要：亚太/欧洲/美洲/中东各地域 OpenAPI 公网及 VPC 接入地址列表,域名格式 apig.{regionId}.aliyuncs.com
- `api-apig-2024-03-27-ram-ai-gateway.md` — AI网关-RAM授权信息 Action/Resource/Condition定义
  - 摘要：API网关AI网关(apig)的RAM权限策略参考,资源级授权粒度,列出DeleteEnvironment/CreateAiModelCard/GetMcpServer等操作的Action、资源ARN、访问级别及条件关键字,用于配置最小权限策略
- `api-apig-2024-03-27-quota-ai-gateway.md` — APIG OpenAPI 流控配额
  - 摘要：各 OpenAPI 的 QPS 配额表,写操作多为 30/s、读操作多为 60/s,限速维度 regionId+API+ParentUid
- `api-apig-2024-03-27-changeset-ai-gateway.md` — APIG OpenAPI 变更集
  - 摘要：按时间倒序列出 APIG 2024-03-27 各 OpenAPI 的变更记录,含 ImportHttpApi、ListPluginAttachments、CreateHttpApi、CreateService 返回结构/入参变更
- `api-apig-2024-03-27-errorcodes.md` — AI 网关公共错误码（403/409/500 与 APIG.ErrorCode 排查）
  - 摘要：AI 网关 APIG 公共错误码：403 Forbidden 权限禁止、409 Conflict（API 名称/版本/路径重复、已发布、授权冲突）、500 InternalError。

## 四、deferred 清单（登记不蒸馏）

共 **250** 条，明细见同批生成的 TSV。前 20 条示例：

- `api-apig-2024-03-27-dir-ai-gateway` — API目录 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-dir-api-management-ai-gateway` — API管理 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-exporthttpapi` — ExportHttpApi - 导出HTTP API ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-importhttpapi` — API网关-ImportHttpApi 导入HTTP API（OpenAPI 2.0/3.0） ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-deployhttpapi` — API网关-DeployHttpApi 发布HTTP API ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-createhttpapi` — API网关-CreateHttpApi 创建HTTP API ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-updatehttpapi` — API网关-UpdateHttpApi 更新HTTP API配置 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-gethttpapi` — AI网关-GetHttpApi 获取HTTP API信息 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-listhttpapis` — API网关-ListHttpApis 获取HTTP API列表 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-undeployhttpapi` — API网关-UndeployHttpApi 下线HTTP API ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-deletehttpapi` — AI网关-DeleteHttpApi 删除HTTP API ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-dir-interface-management-ai-gateway` — 接口管理 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-createhttpapioperation` — API网关-CreateHttpApiOperation 创建HTTP API接口 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-gethttpapioperation` — API网关-GetHttpApiOperation 获取HTTP API接口信息 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-updatehttpapioperation` — API网关-UpdateHttpApiOperation 更新HTTP API接口定义 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-listhttpapioperations` — API网关-ListHttpApiOperations 获取HTTP API接口列表 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-deletehttpapioperation` — DeleteHttpApiOperation - 删除接口 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-dir-model-meta-information-management` — 模型元信息管理 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-createaimodelprovider` — API网关-CreateAiModelProvider 创建AI模型供应商 ｜ OpenAPI 逐 Action / 逐数据结构参考页
- `api-apig-2024-03-27-getaimodelprovider` — GetAiModelProvider - 查询AI模型供应商详情 ｜ OpenAPI 逐 Action / 逐数据结构参考页

## 五、可复算性

- llms.txt 快照：`tests/ai-gateway-llms-2026-09-21.txt`，124210 字节，SHA256 `076b5cd17da58491d58379b1c097175eee1e0af79239576bd3e0c6d8eb54df47`
- core TSV：`/tmp/aigw_core_v3.tsv`（188 行）
- deferred TSV：`/tmp/aigw_deferred_urls.tsv`（250 行）
- 重跑本脚本应产出逐字节相同的 MD 与 TSV（除时间戳行外）。
