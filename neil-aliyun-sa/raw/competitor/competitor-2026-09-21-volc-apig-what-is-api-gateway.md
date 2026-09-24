<!-- source_url: https://www.volcengine.com/docs/6569/82992 -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-05-14 -->
<!-- summary: 火山引擎「什么是 API 网关」官方全文（getDocDetail API）。关键取证点：流量网关「采用 Envoy 内核，兼容 Kubernetes Ingress 标准」→ 与阿里云（Higress/Envoy 系）技术底座同源，外部认证差异是实现选择而非平台代差。 -->

> 文档标题：什么是 API 网关｜DocumentCode: WhatisAPIG｜FirstPublishedTime: 2022-01-07T11:21:45Z｜UpdatedTime: 2026-05-14T03:57:14Z

API 网关（API Gateway，APIG）是一款高扩展、高可用的云上网关托管服务。提供智能路由、多协议支持和 AI 模型代理。结合弹性伸缩、认证鉴权及灰度发布，保障 AI 服务高效稳定运行。

<span id="sL2kAFRX"></span>
## 为什么选择 API 网关

API 网关是托管在火山引擎云上的云原生网关服务，支持对接容器服务集群、云服务器、函数服务、微服务引擎等云上基础资源，为用户的云上应用提供南北向流量和东西向流量管理。同时支持对接部署在云端的 AI 框架和服务。API 网关根据后端对接的云产品，主要包含以下网关类型：


|网关类型 |说明 |
|---|---|
|流量网关 |采用 Envoy 内核，兼容 Kubernetes Ingress 标准，支持对接容器服务（VKE）集群、ECS 实例和 veFaaS 函数实例。负责为集群、ECS 或函数实例提供入口流量管理，包括：路由策略、安全认证、协议转发、监控告警等功能。为您提供高性能、高可扩展的云原生流量入口。 |
|微服务网关 |对接微服务引擎（MSE）注册中心， 为注册的应用提供云原生网关功能，自动发现和管理后端服务。您可以通过网关轻松实现全链路灰度、服务治理等高级功能，显著提升微服务架构的稳定性和迭代效率。 |
|AI 网关 |为大语言模型应用提供统一的应用程序代理入口。通过协议转换，将客户端的标准化请求适配到多个不同模型厂商，降低多模型接入的适配成本。支持基于业务规则的请求分发与模型降级（Fallback），并为流式长连接提供稳定性保障。内置精细化的的 token 用量统计、成本预算与访问限流能力，结合身份认证与全链路可观测性，确保模型服务兼具成本效益和安全合规。 |


<span id="6Y2ehBwO"></span>
## 产品架构

API 网关在传统流量网关的基础上，集成丰富的服务发现和服务治理能力，打通微服务架构的内外部网络，快速实现各服务之间、服务与客户端之间的安全通信。

<span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_b9adfc82ad6101f42d4e3f97c95689f2.png) </span>

<span id="67ueowGv"></span>
## 学习资源


* [成长地图](https://www.volcengine.com/docs/6569)

* [快速入门](https://www.volcengine.com/docs/6569/82995)

* [最佳实践](https://www.volcengine.com/docs/6569/605024)

* [AI 网关](https://www.volcengine.com/docs/6569/1356167)

* [常见问题](https://www.volcengine.com/docs/6569/105069)
