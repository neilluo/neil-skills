---
source_url: https://help.aliyun.com/zh/agentteams/magic-console-product-overview
fetch_date: 2026-09-20
product: AgentTeams
slug: magic-console-product-overview
body_sha256: 222fe8de6e22544903527255bd3884422c0aa1185f65351584b9f93457f04b8c
body_bytes: 4195
migration_status: migrated-legacy
---

[AgentTeams](https://mse.console.aliyun.com/#/magic-console/instances)是阿里云提供的企业级多智能体治理与协作平台，帮助企业统一创建、调度和监控 AI Worker（智能体），集中管理模型配置和团队权限。本文介绍 AgentTeams 的产品定位、核心功能、应用场景和支持地域，帮助开发者快速了解平台能力。  

## 什么是 AgentTeams
AgentTeams 是面向企业的多智能体治理与协作平台，支持在统一的控制台中创建和管理 AI Worker。通过 AgentTeams，可以接入多个 AI 模型供应商、集成外部工具（MCP 服务），并对 AI Worker 的运行状态进行实时监控。

AgentTeams 支持多成员、多角色的团队协作和权限管理，满足企业级安全和合规要求。

## 核心功能
<table> <thead> <tr> <td><p><b>功能</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>实例管理</p></td> <td><p>创建和管理 AgentTeams 实例，作为资源的隔离边界，支持按项目或业务线独立分配资源。</p></td> </tr> <tr> <td><p>Worker 管理</p></td> <td><p>创建和管理AI Worker，支持多种运行模式，满足不同业务场景的智能体配置需求。</p></td> </tr> <tr> <td><p>模型管理</p></td> <td><p>接入多个 AI 模型供应商，统一管理模型配置，支持在不同 Worker 间灵活切换模型。</p></td> </tr> <tr> <td><p>团队协作</p></td> <td><p>创建团队、管理成员权限，支持多角色协作，满足企业级权限管控需求。</p></td> </tr> <tr> <td><p>MCP 服务</p></td> <td><p>基于 Model Context Protocol（MCP）集成和管理外部工具，为 AI Worker 提供扩展工具调用能力。</p></td> </tr> <tr> <td><p>监控仪表盘</p></td> <td><p>实时查看 Worker 用量、模型调用量和 Token 消耗趋势，支持用量分析和异常识别。</p></td> </tr> <tr> <td><p>Worker 模板</p></td> <td><p>创建可复用的 Worker 配置模板，快速批量部署同类型智能体，降低重复配置成本。</p></td> </tr> </tbody> </table>

## 应用场景
* **企业数字员工**：员工通过企业 IM（钉钉、飞书、企业微信）发起任务，AgentTeams 按部门调度 Agent Team，Agent 通过 MCP/Skills 访问 CRM、OA、ERP 等企业系统执行操作，全程具备 IDP 认证、审计日志与成本归属能力。

* **Agent Team 服务化**：平台管理员按角色创建 Team 池（研发、运维、数据、安全等），业务团队通过 RBAC 按需申请接入对应 Team，实现权限隔离、独立配额计费与平台统一运维。

* **SaaS Agent Team 赋能**：SaaS 厂商为每个租户路由至独立 Agent Team，通过权限隔离与访问控制引擎按客户授权策略分配可调用的 Skills/MCP 组合，实现多租户数据隔离与用量独立计量。

* **存量 Agent 纳管**：企业通过 AgentTeams 统一治理平台将已部署的异构 Agent（OpenClaw、QwenPaw、Claude Code、自研 Agent 等）混编进同一 Team，无需改造即可纳管，并实现 Agent 资产（Skills、MCP、Prompt、知识库）的统一沉淀与跨 Team 复用。

## 支持地域
AgentTeams 当前支持以下地域：
<table> <thead> <tr> <td><p><b>地域名称</b></p></td> <td><p><b>地域 ID</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>华东 1（杭州）</p></td> <td><p>cn-hangzhou</p></td> </tr> <tr> <td><p>华北 2（北京）</p></td> <td><p>cn-beijing</p></td> </tr> <tr> <td><p><span>新加坡</span></p></td> <td><p><span>ap-southeast-1</span></p></td> </tr> </tbody> </table>

## 相关文档
* [AgentTeams 快速入门](https://help.aliyun.com/document_detail/3040378.html)：了解如何快速创建第一个 AI Worker，完成初始环境配置。

* [管理实例](https://help.aliyun.com/document_detail/3040381.html)：了解如何创建和配置 AgentTeams 实例，管理实例内的资源隔离边界。

* [管理 Worker 和 Worker 团队](https://help.aliyun.com/document_detail/3040386.html)：了解如何创建、编辑和删除 AI Worker，配置运行参数和模型绑定。

<br />