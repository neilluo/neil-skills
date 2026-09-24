---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/ai-gateway-capacity-description
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-gateway-capacity-description
body_sha256: 1ab29872180d144c1aa8bb0182c21dd8d24443be6a57ac564cec59f52b14af7b
body_bytes: 15992
migration_status: current
---

AI 网关提供多种实例类型，适用于从快速试用、开发测试到生产业务和核心系统的不同场景。本文介绍各实例类型的定位、能力差异和推荐选择方式，帮助您选择适合的实例类型。具体可购买的实例类型、功能范围、计费项、价格、服务等级和可用地域，请以产品控制台、价格页和服务等级协议页面展示为准。  

## **实例类型概览**
<table> <thead> <tr> <td><p><b>实例类型</b></p></td> <td><p><b>产品定位</b></p></td> <td><p><b>适用场景</b></p></td> <td><p><b>主要特点</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Serverless 标准版</b></p></td> <td><p>低门槛 AI 网关实例</p></td> <td><p>快速试用、PoC、开发测试、低流量业务</p></td> <td><p>0 元起步，按量付费，使用平台分配入口</p></td> </tr> <tr> <td><p><b>Serverless 企业版</b></p></td> <td><p>生产级 Serverless AI 网关实例</p></td> <td><p>正式生产业务、需要独立入口或自定义域名的业务</p></td> <td><p>提供独立入口能力，支持自定义域名和传输加密配置</p></td> </tr> <tr> <td><p><b>Serverless（旧）</b></p></td> <td><p>原 Serverless 版本</p></td> <td><p>已有存量实例继续使用、平滑过渡</p></td> <td><p>已有实例可继续管理和使用，能力以原版本为准</p></td> </tr> <tr> <td><p><b>实例型独享版</b></p></td> <td><p>高规格独享实例</p></td> <td><p>核心生产、高并发、高隔离或完整治理能力要求较高的业务</p></td> <td><p>提供更高规格、更强隔离和更完整的网关能力</p></td> </tr> </tbody> </table>

## 如何选择
<table> <thead> <tr> <td><p><b>如果您需要</b></p></td> <td><p><b>推荐选择</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>低成本快速体验 AI 网关核心能力</p></td> <td><p>Serverless 标准版</p></td> </tr> <tr> <td><p>企业采购前 PoC 或开发测试环境</p></td> <td><p>Serverless 标准版</p></td> </tr> <tr> <td><p>正式生产业务，需要更高服务等级</p></td> <td><p>Serverless 企业版</p></td> </tr> <tr> <td><p>需要自定义域名、证书、TLS policy 或 HTTP/2 配置</p></td> <td><p>Serverless 企业版</p></td> </tr> <tr> <td><p>已有 Serverless（旧）实例，短期内不调整业务链路</p></td> <td><p>Serverless（旧）继续使用</p></td> </tr> <tr> <td><p>高并发、强隔离、高合规或完整高级治理能力</p></td> <td><p>实例型独享版</p></td> </tr> </tbody> </table>

## Serverless 新旧版本说明
新版 Serverless 包含 **Serverless 标准版** 和 **Serverless 企业版**，采用新架构，面向低门槛接入、生产级 Serverless 场景和后续能力持续演进设计。Serverless（旧）为原 Serverless 版本，主要面向已有实例客户和过渡场景，已有实例可继续管理和使用。

相比 Serverless（旧），新版 Serverless 在架构和能力演进上具备以下优势：

* **资源使用更高效**：新版 Serverless 采用多租资源池化架构，可提升整体资源利用效率，降低低流量和弹性波动场景下的使用门槛。

* **开通和扩展更灵活**：新版 Serverless 更适合快速创建、按需使用和弹性增长的业务场景，标准版支持 0 元起步，企业版提供生产级入口能力。

* **版本分层更清晰**：新版 Serverless 区分标准版和企业版，分别面向低成本试用、开发测试和生产业务，便于用户按业务阶段选择合适实例类型。

* **能力演进更统一**：新版 Serverless 统一承载 LLM API、Agent API、MCP Server、智能路由、观测分析等 AI 网关核心能力，后续新增能力会优先围绕新版 Serverless 演进。

* **支持插件体系**：新版 Serverless 支持平台提供的插件体系，不支持自定义插件。用户可根据实例类型和功能开放范围使用插件能力，便于扩展认证鉴权、安全防护、流量治理、观测分析等网关能力。

* **迁移路径更明确**：已有 Serverless（旧）实例可继续使用；新客户建议优先选择新版 Serverless 标准版或企业版。已有客户可根据业务阶段、入口能力、服务等级和治理能力需求，逐步评估迁移到新版 Serverless 或实例型独享版。

## 能力对比
<table> <thead> <tr> <td><p><b>对比项</b></p></td> <td><p><b>Serverless 标准版</b></p></td> <td><p><b>Serverless 企业版</b></p></td> <td><p><b>Serverless（旧）</b></p></td> <td><p><b>实例型独享版</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>推荐业务阶段</p></td> <td><p>试用、评估、开发测试、低流量业务</p></td> <td><p>正式生产、规模化业务</p></td> <td><p>正式生产、规模化业务</p></td> <td><p>核心生产、高并发、高合规业务</p></td> </tr> <tr> <td><p>起步成本</p></td> <td><p>0 元起步</p></td> <td><p>有实例费</p></td> <td><p>有起步费用</p></td> <td><p>按独享规格计费</p></td> </tr> <tr> <td><p>计费方式</p></td> <td><p>按实际用量付费</p></td> <td><p>实例费 + 按实际用量付费</p></td> <td><p>起步费 + 按实际用量付费</p></td> <td><p>按实例规格和实际用量计费</p></td> </tr> <tr> <td><p>访问入口</p></td> <td><p>平台分配入口</p></td> <td><p>独立入口能力</p></td> <td><p>独立实例入口</p></td> <td><p>独享入口能力</p></td> </tr> <tr> <td><p>架构形态</p></td> <td><p>新架构，平台分配入口</p></td> <td><p>新架构，独立入口能力</p></td> <td><p>原 Serverless 旧架构</p></td> <td><p>独享实例架构</p></td> </tr> <tr> <td><p>插件体系</p></td> <td><p>支持平台提供的插件体系，不支持自定义插件；具体可用插件以产品控制台展示为准</p></td> <td><p>支持平台提供的插件体系，不支持自定义插件；具体可用插件以产品控制台展示为准</p></td> <td><p>不支持插件体系</p></td> <td><p>支持完整插件和高级治理能力</p></td> </tr> <tr> <td><p>自定义域名</p></td> <td><p>不支持关联到标准版实例</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>支持</p></td> </tr> <tr> <td><p>证书/TLS/HTTP/2</p></td> <td><p>不支持用户自定义配置，平台默认 HTTPS 入口保持可用</p></td> <td><p>支持用户配置</p></td> <td><p>支持用户配置</p></td> <td><p>支持</p></td> </tr> <tr> <td><p>默认 QPS 限制</p></td> <td><p>50 QPS</p></td> <td><p>500 QPS</p></td> <td><p>以原版本规格为准</p></td> <td><p>以实例规格为准</p></td> </tr> <tr> <td><p>服务等级</p></td> <td><p>99.9%</p></td> <td><p>99.95%</p></td> <td><p>99.95%</p></td> <td><p>99.99%</p></td> </tr> <tr> <td><p>AI 核心能力</p></td> <td><p>支持 LLM API、Agent API、MCP Server、智能路由、AI 安全、Token 用量看板等核心能力</p></td> <td><p>支持标准版核心能力，并提供更完整的生产级配置能力</p></td> <td><p>支持 LLM API、Agent API、MCP Server、智能路由、AI 安全、Token 用量看板等核心能力</p></td> <td><p>支持完整网关能力</p></td> </tr> <tr> <td><p>高级治理能力</p></td> <td><p>部分高级能力不开放</p></td> <td><p>支持更多企业级能力</p></td> <td><p>支持原版本治理能力</p></td> <td><p>支持完整高级治理能力</p></td> </tr> </tbody> </table>

## Serverless 标准版
Serverless 标准版适合希望低成本快速体验 AI 网关能力的用户。您可以通过标准版快速验证 LLM API、Agent API、MCP Server、智能路由、AI 安全、Token 用量看板等核心能力。

### 适用场景

* 个人开发者体验 AI 网关能力。

* 企业进行采购前 PoC 或技术验证。

* AI 应用初创团队在低流量阶段接入 AI 网关。

* ISV 或 SaaS 厂商用于开发、测试环境。

### 主要优势

* **0 元起步**：无实例费，按实际用量付费。

* **快速开通**：使用平台分配入口，降低接入门槛。

* **核心 AI 能力可用**：支持 LLM API、Agent API、MCP Server、智能路由等核心能力。

### 使用限制

* 默认实例级 QPS 上限为 50。

* 不支持关联用户自定义域名。

* 不支持用户自定义证书、TLS policy 或 HTTP/2 配置。

* 不提供独立公网入口。

* 标准版后续规划支持一键升级为企业版，无需资源迁移；具体支持时间和操作入口请以产品控制台展示为准。

## Serverless 企业版
Serverless 企业版适合正式生产业务。相比标准版，企业版提供独立入口能力、更高服务等级，并支持自定义域名和传输加密配置。

### 适用场景

* 已经承载正式生产流量的 AI API、Agent API 或 MCP Server。

* 需要稳定独立访问入口的企业业务。

* SaaS 或 ISV 需要向下游客户提供稳定 API 入口。

* 需要自定义域名、证书、TLS policy 或 HTTP/2 配置的业务。

### 主要优势

* **生产级实例形态**：适合正式生产业务。

* **独立入口能力**：满足生产业务对稳定访问入口的要求。

* **更高服务等级**：服务等级为 99.95%。

* **自定义域名能力**：支持关联自定义域名。

* **传输加密配置**：支持用户配置证书、TLS policy 和 HTTP/2。

### 使用建议

如果您的业务已经进入生产阶段，或需要自定义域名、独立访问入口、更高服务等级、超过标准版默认 QPS 上限的能力，建议选择 Serverless 企业版。

## Serverless（旧）
Serverless（旧）是原 Serverless 版本，采用旧架构，主要面向已有实例客户和过渡场景。已有 Serverless（旧）实例可以继续管理和使用，具体能力以已购实例规格和控制台展示为准。

新客户建议优先选择新版 Serverless 标准版或企业版。新版 Serverless 采用新架构，在资源效率、开通灵活性、版本分层、能力演进和插件体系支持方面更适合后续 AI 网关能力持续升级。

### 适用场景

* 已经拥有 Serverless（旧）实例，短期内不调整业务链路。

* 当前业务仍依赖原版本能力，迁移需要更多验证时间。

* 需要在业务窗口内逐步评估迁移到新版 Serverless 或实例型独享版。

### 使用建议

新客户建议优先选择新版 Serverless 标准版或企业版。已有 Serverless（旧）实例的客户，可根据业务需求逐步评估迁移到新版 Serverless 或实例型独享版。

如需新购 Serverless（旧），请以控制台可购买范围和产品规则为准。

## 实例型独享版
实例型独享版适合对资源隔离、服务等级、性能规格或完整治理能力有更高要求的核心业务。

### 适用场景

* 大型企业核心生产系统。

* 需要 99.99% 服务等级的业务。

* 长期高并发或突发流量较高的业务。

* 需要更完整的插件、安全、观测、治理能力。

* 对资源隔离、合规、审计或网络控制有更高要求的业务。

### 主要优势

* **更强资源隔离能力**：适合核心生产和高合规场景。

* **最高服务等级**：服务等级为 99.99%。

* **完整网关能力**：适合复杂插件、安全、观测和治理需求。

* **更稳定的性能预期**：适合高吞吐、强隔离和大型客户场景。

## 典型场景推荐
<table> <thead> <tr> <td><p><b>客户场景</b></p></td> <td><p><b>推荐实例类型</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>快速体验智能路由、Agent API 或 MCP Server</p></td> <td><p>Serverless 标准版</p></td> <td><p>低成本试用，适合低频调用和功能验证</p></td> </tr> <tr> <td><p>企业采购前 PoC</p></td> <td><p>Serverless 标准版</p></td> <td><p>快速创建、低成本验证，后续可迁移到企业版</p></td> </tr> <tr> <td><p>开发或测试环境长期保留网关实例</p></td> <td><p>Serverless 标准版</p></td> <td><p>无实例费，适合非生产环境</p></td> </tr> <tr> <td><p>正式生产业务上线</p></td> <td><p>Serverless 企业版</p></td> <td><p>提供独立入口、更高服务等级、自定义域名和证书能力</p></td> </tr> <tr> <td><p>SaaS 服务对外提供稳定 API 入口</p></td> <td><p>Serverless 企业版</p></td> <td><p>独立访问入口和自定义域名更符合对外服务诉求</p></td> </tr> <tr> <td><p>已有 Serverless（旧）生产实例</p></td> <td><p>Serverless（旧）继续使用，并评估迁移</p></td> <td><p>已有实例管理操作保持不变，迁移可按业务窗口规划</p></td> </tr> <tr> <td><p>大客户核心系统或高合规业务</p></td> <td><p>实例型独享版</p></td> <td><p>提供更高服务等级、更强隔离和完整能力</p></td> </tr> <tr> <td><p>高并发或需要完整高级治理能力</p></td> <td><p>实例型独享版</p></td> <td><p>适合重载和复杂治理场景</p></td> </tr> </tbody> </table>

## 迁移建议
### 从标准版迁移到企业版

标准版后续规划支持一键升级为企业版，无需资源迁移。升级后可获得企业版的独立入口、自定义域名、传输加密配置、更高 QPS 和更高服务等级等能力；具体支持时间、升级条件和操作入口请以产品控制台展示为准。

### 从 Serverless（旧）迁移到新版 Serverless

如果您希望降低使用门槛并快速体验新版 AI 能力，可以评估 Serverless 标准版。如果您希望获得生产级入口、自定义域名和更高服务等级，可以评估 Serverless 企业版。如果原实例承载核心高流量业务或依赖完整高级治理能力，可以评估实例型独享版。

### 从企业版迁移到实例型独享版

当业务需要更高服务等级、更强资源隔离、高并发、完整高级治理能力或更高合规要求时，建议评估实例型独享版。

## 常见问题
### Serverless 标准版是否适合生产业务？

Serverless 标准版适合低流量、低成本、可接受平台分配入口的轻量业务。如果需要自定义域名、独立访问入口、更高服务等级或超过默认 QPS 上限，建议选择 Serverless 企业版。

### Serverless 标准版是否支持 HTTPS？

支持平台默认 HTTPS 入口。标准版不支持用户自定义证书、TLS policy 或 HTTP/2 配置。

### Serverless 企业版和实例型独享版有什么区别？

Serverless 企业版适合生产级 Serverless 场景，提供独立入口能力、自定义域名和传输加密配置。实例型独享版适合对资源隔离、服务等级、性能规格或完整治理能力有更高要求的核心业务。

### 新客户是否应该选择 Serverless（旧）？

新客户建议优先选择新版 Serverless 标准版或企业版。Serverless（旧）主要面向已有实例客户和特定过渡场景，具体可购买范围以控制台展示和产品规则为准。

## 注意事项
* 新版统一称为 **Serverless** ，包含 **标准版** 和 **企业版** ；原版本称为 **Serverless（旧）**。

* Serverless 标准版是低门槛轻量入口，不等同于完整生产规格。如需自定义域名、证书、TLS、HTTP/2、独立入口或更高服务等级，请选择 Serverless 企业版或实例型独享版。

* Serverless 企业版适合生产级 Serverless 场景。如需更强资源隔离、完整独享规格或最高服务等级，请选择实例型独享版。

* Serverless（旧）主要面向已有实例客户和特定过渡场景，新客户建议优先选择新版 Serverless。

* 具体功能、规格、计费项、价格、服务等级和可购买范围，请以产品控制台、官网价格页和服务等级协议页面为准。