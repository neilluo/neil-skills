<!-- source_url: https://help.aliyun.com/zh/api-gateway/llms.txt -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 未在 .md 通道提供（fetched 2026-09-21） -->
<!-- summary: API 网关产品线 llms.txt 全文索引（补归档：三形态谱系第 3 行逐字原文、原 API 网关 EOL 时间线第 41 行、AI 网关定位与能力清单第 40 行的出处）。 -->

# API 网关

> API 网关（API Gateway）提供云原生 API 网关、AI 网关和原 API 网关三种形态，涵盖路由转发、流量治理、协议转换、鉴权认证等核心能力。云原生 API 网关支持 Ingress/微服务/安全三合一部署与可观测；AI 网关面向大模型调用场景提供 Token 限流、内容审核、多模型路由与缓存加速；原 API 网关兼容传统 RESTful/SOAP 接口托管与 SDK 自动生成。

本文档内容仅适用于「阿里云中国站」，阿里云国际站文档请参考 https://www.alibabacloud.com/help/llms.txt

## 产品概述

- [产品概述](https://help.aliyun.com/zh/api-gateway/product-overview.md): API网关是统一的API托管服务，能安全、高效地管理您的所有API。本文深度解析云原生与AI网关的核心差异及适用场景，助您做出精准的架构选型。

## 快速入门

- [快速入门](https://help.aliyun.com/zh/api-gateway/quick-start.md): 快速入门索引,分别提供云原生 API 网关(微服务场景:HTTP API 访问容器服务、REST API 生命周期)与 AI 网关(Model API、MCP 服务管理)的核心入门文档。

## 操作指南

- [操作指南](https://help.aliyun.com/zh/api-gateway/user-guide.md): 汇总 API 网关与云原生 API 网关控制台操作入口,涵盖 API 生命周期管理、版本与发布历史、路由与策略、网关实例、域名、黑白名单/认证鉴权及监控诊断的功能矩阵与对应文档链接。

## 安全合规

- [安全合规](https://help.aliyun.com/zh/api-gateway/security-and-compliance.md): 推荐使用 RAM 用户与 RAM 角色而非主账号访问 API 网关或云原生 API 网关,索引两套产品各自的「使用 RAM 进行访问控制」实操文档。

## 实践教程

- [实践教程](https://help.aliyun.com/zh/api-gateway/use-cases.md): 索引 API 网关与云原生 API 网关的最佳实践教程入口,两套产品分别维护独立的场景化实践文档。

## 开发参考

- [开发参考](https://help.aliyun.com/zh/api-gateway/developer-reference.md): API 网关提供 API 参考、CLI 参考、SDK 参考、Terraform 与资源编排五种开发对接方式;云原生 API 网关目前提供 API 参考文档。

## 服务支持

- [服务支持](https://help.aliyun.com/zh/api-gateway/support.md): 汇总 API 网关与云原生 API 网关两套产品的常见问题(FAQ)入口与各自的服务等级协议(SLA)/相关协议文档链接。

## 子产品

> 以下子产品拥有独立文档，请前往对应文档获取详细信息。

- [云原生API网关](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/llms.txt): 云原生API网关基于 Envoy 内核和开源 Higress，将流量网关、微服务网关、K8s Ingress 三合一，提供 REST API/HTTP API/WebSocket API 全生命周期管理、Nginx Ingress 兼容与迁移、限流降级、JWT/OIDC/mTLS 认证鉴权、插件市场（含消费者认证、IP 黑白名单、WAF 集成）、日志投递与链路追踪，支持专享实例和 Serverless 实例，SLA 99.99%。
- [AI 网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/llms.txt): AI 网关是云原生 API 网关面向 AI 原生应用的托管入口，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，兼容 OpenAI 协议；支持 Model API/Agent API/MCP Server 三类接入，覆盖多模型路由、按比例灰度、HTTP to MCP 转换、A2A 协议转换、消费者 API-Key/JWT/HMAC 鉴权、KMS 凭证托管、Token 限流、Fallback、语义缓存、AI 安全护栏（内容合规/提示词攻击/敏感数据/恶意文件/水印）与全链路可观测；提供专享实例与 Serverless 实例，按实例规格或 AI Credits 计费。
- [原API网关](https://help.aliyun.com/zh/api-gateway/traditional-api-gateway/llms.txt): 原 API 网关（传统版）是覆盖 API 设计、发布、调用、鉴权、限流、监控和下线等全生命周期的 API 托管服务，支持对接 ECS、函数计算 FC、K8s、PAI、DataWorks 等后端，提供专享实例和 Serverless 实例两种规格。产品将于 2026 年 8 月 23 日停止新购、2027 年 9 月 21 日全面下线，存量实例请迁移至云原生 API 网关。
