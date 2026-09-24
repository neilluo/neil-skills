---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-product-overview
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-product-overview
body_sha256: e6c8a6f1381832090809d0c404af94fc99b63e722402d751aefa7e10940a12ba
body_bytes: 5407
migration_status: current
---

[AgentCore](https://agentcore.console.aliyun.com/)是阿里云提供的智能体构建和治理平台。以构建与运行、协作与治理、观测与评估三大能力，覆盖 Agent 全生命周期；通过多模式构建入口、统一身份鉴权与 Team 协作编排，将自研、开源 Harness、商业 SaaS Agent 多来源统管于一个平台，让智能体建得快、管得住、协作好。本文介绍 AgentCore 的产品定位、核心功能、应用场景和支持地域，帮助开发者快速了解平台能力。  

## 什么是 AgentCore
AgentCore 是一款智能体构建和治理平台，支持在统一的控制台中创建和管理 Agent 。通过 AgentCore，用户可以接入多个 AI 模型供应商、集成外部工具（MCP 服务），并对 Agent 的运行状态进行实时监控。

AgentCore 支持多成员、多角色的团队协作和权限管理，满足企业级安全和合规要求。

## 核心功能
<table> <thead> <tr> <td><p><b>功能</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Agent 管理</p></td> <td><p>创建和管理Agent，支持多种运行模式，满足不同业务场景的智能体配置需求。</p></td> </tr> <tr> <td><p>Agent 模板</p></td> <td><p>创建可复用的 Agent 配置模板，快速批量部署同类型智能体，降低重复配置成本。</p></td> </tr> <tr> <td><p>模型连接</p></td> <td><p>统一管理模型配置，支持在不同 Agent 间灵活切换模型。</p></td> </tr> <tr> <td><p>Skill 管理</p></td> <td><p>创建、发布和管理 Skill，支持从 Skill 广场导入三方skill，为 Agent 扩展可复用的专业能力。</p></td> </tr> <tr> <td><p>工具管理</p></td> <td><p>基于 Model Context Protocol（MCP）集成和管理外部工具，为 AI Agent 提供扩展工具调用能力。</p></td> </tr> <tr> <td><p>凭证管理</p></td> <td><p>集中管理用户访问外部系统用到的AK/SK等敏感信息，避免密钥明文散落在各处配置中。</p></td> </tr> <tr> <td><p>Team 协作</p></td> <td><p>创建团队、管理成员权限，支持多角色协作，满足企业级权限管控需求。</p></td> </tr> <tr> <td><p>账号集成</p></td> <td><p>配置钉钉、微信、飞书等平台的账号集成，将 Agent 接入企业日常沟通渠道，实现对话式调用。</p></td> </tr> </tbody> </table>

## 应用场景
* **数字员工：**面向企业内部事务的岗位型智能体，通过 Harness 配置化创建即可上线，经 IM 渠道直连办公场景，依托记忆库与知识库积累业务上下文，承接入职办理、单据审核、工单值守等工作。

* **智能客服：**以单一 Agent 服务承接对外咨询与业务办理，基于沙箱运行时按需弹性伸缩以应对流量高峰，由身份与权限体系约束数据访问范围，可观测与评估能力支撑全链路追溯与效果调优。

* **智能问数：**通过自然语言提出业务问题，由 Agent Team 拆解任务，多个 Agent 经 MCP 工具接入数据源分别完成取数、建模与归因，输出可直接支撑决策的分析结论。

* **AI 编程助手：**将企业多种存量编程 Agent 原样纳管，按需组队，统一协作完成研发任务；研发任务全链路可观测、可干预；Token 消耗可归因、可管控、可审计。

## 支持地域
AgentCore 当前支持以下地域：
<table> <thead> <tr> <td><p><b>地域名称</b></p></td> <td><p><b>地域 ID</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>华东 1（杭州）</p></td> <td><p>cn-hangzhou</p></td> </tr> <tr> <td><p>华东 2（上海）</p></td> <td><p>cn-shanghai</p></td> </tr> <tr> <td><p>华南 1（深圳）</p></td> <td><p>cn-shenzhen</p></td> </tr> <tr> <td><p>华北 2（北京）</p></td> <td><p>cn-beijing</p></td> </tr> <tr> <td><p>新加坡</p></td> <td><p>ap-southeast-1</p></td> </tr> </tbody> </table>

## 依赖产品
<table> <thead> <tr> <td><p><b>产品</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>开通方式</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>CMS（</b><a href="https://help.aliyun.com/zh/cms/cloudmonitor-2-0/product-overview/product-introduction/"><b>云监控</b></a><b>）</b></p></td> <td><p>用于写入 Tracing 数据</p></td> <td><p>跳转<a href="https://cloudmonitornext.console.aliyun.com/?spm=5176.2ef5001f.console-base_search-panel.dtab-product_cms.4efe316dIz4rRe">云监控控制台</a>开通</p></td> </tr> <tr> <td><p><b>PrivateLink（私网连接）</b></p></td> <td><p>提供私网访问能力</p></td> <td><p>点击后自动开通</p></td> </tr> <tr> <td><p><a href="https://help.aliyun.com/document_detail/3031320.html"><b>SchedulerX3</b></a></p></td> <td><p>提供分布式任务调度能力</p></td> <td><p>跳转<a href="https://mse.console.aliyun.com/#/schedulerx-version/">售卖页</a>购买</p></td> </tr> </tbody> </table>

## 相关文档
了解更多 AgentCore 功能：

* [AgentCore 基本概念](https://help.aliyun.com/document_detail/3052315.html)

* [AgentCore 计费说明](https://help.aliyun.com/document_detail/3057998.html)

* [AgentTeams 迁移至 AgentCore](https://help.aliyun.com/document_detail/3052611.html)

* [管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)