---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta
fetch_date: 2026-09-21
product: AI Gateway
slug: announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta
body_sha256: d66577f88ef2f4037f3320520779c8b31a6952dc070071b1e29b1ae7fa8efe70
body_bytes: 3969
migration_status: current
---

AI 网关 Serverless 新版将开启公测。新版提供更低门槛的 AI 网关接入方式，适用于模型路由、Agent API、MCP（Model Context Protocol）Server、AI 安全防护、Token 用量分析等场景，便于构建和管理 AI 应用流量入口。  

## 公测时间
AI 网关 Serverless 新版公测时间为 **7 月 31 日至 8 月 31 日**。公测期间，可在支持的地域创建和试用 AI 网关 Serverless 新版实例。

## 公测地域
本次公测支持的地域包括：北京、上海、杭州、深圳、香港。

上述公测地域会随测试完成后逐步放开，请以产品控制台展示为准。

## 公测版本
本次公测面向 AI 网关 Serverless 新版，包含以下实例类型：
<table> <thead> <tr> <td><p><b>实例类型</b></p></td> <td><p><b>适用场景</b></p></td> <td><p><b>关键差异</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Serverless 标准版</p></td> <td><p>快速试用、PoC、开发测试、低流量业务</p></td> <td><p>---</p></td> </tr> <tr> <td><p>Serverless 企业版</p></td> <td><p>正式生产业务</p></td> <td><p>支持独立入口、自定义域名</p></td> </tr> </tbody> </table>

如已在使用 Serverless（旧）实例，已有实例可继续使用。

## 公测期间计费说明
公测期间，AI 网关 Serverless 新版的**网关自身费用不收费** ，仅**公网入网流量按照 CDT（Cloud Data Transfer，云数据传输）计费**。
<table> <thead> <tr> <td><p><b>费用类型</b></p></td> <td><p><b>公测期间计费规则</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>AI 网关 Serverless 新版网关自身费用</p></td> <td><p>不收费</p></td> </tr> <tr> <td><p>公网入网流量</p></td> <td><p>按照 CDT 计费</p></td> </tr> <tr> <td><p>其他云产品费用</p></td> <td><p>按对应云产品计费规则收取</p></td> </tr> </tbody> </table>  
**说明**

模型服务、日志服务、云监控、CDT 等其他云产品费用不属于 AI 网关 Serverless 新版公测免费范围。实际费用以账单和对应产品计费规则为准。

## 主要能力
公测期间，您可以通过 AI 网关 Serverless 新版体验以下能力：

* LLM API 管理：统一管理模型 API 的创建、发布、下线和删除。

* Agent API 管理：面向 Agent 访问场景提供统一入口和治理能力。

* MCP Server：支持 MCP 相关接入和代理场景。

* AI 安全防护：为 AI 流量提供内容安全相关防护能力。

* 观测分析：查看 Token 用量、访问日志和 AI 访问统计等信息。

* 流量治理：支持超时、重试、QPS 限流、并发数限流、跨域、Header 修改等网关策略。

具体可用功能、功能限制和地域支持情况，请以产品控制台展示为准。

## 如何参与公测
公测期间，登录产品控制台，选择公测支持的地域创建 AI 网关 Serverless 新版实例，并按照页面指引完成配置。试用前建议确认以下信息：

* 当前账号所在地域是否在公测地域范围内。

* 业务是否需要公网访问，以及是否可能产生公网入网流量。

* 是否需要自定义域名、证书、TLS policy 或 HTTP/2 等生产级配置能力。

* 是否同时使用模型服务、日志服务、云监控或其他云产品。

## 注意事项
* 公测期间的功能范围、地域范围和计费优惠可能根据产品发布节奏调整，请以产品控制台、官网公告和价格页展示为准。

* 公测期间网关自身计费项不收费，但公网入网流量仍按照 CDT 计费。

* 公测期间产生的其他云产品费用，按照对应云产品的计费规则收取。

* 公测结束后，AI 网关 Serverless 新版可能进入商业化计费阶段。商业化后的收费项目、价格和优惠政策，请以正式公告、产品控制台和官网价格页为准。