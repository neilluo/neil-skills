---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-basic-concepts
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-basic-concepts
body_sha256: 6d7ba4a08df6b5088a6f4cf1e5d47c75e2bc43fa6bff951aa2ee374588ba62b1
body_bytes: 6796
migration_status: current
---

本文介绍 AgentCore 的核心概念，帮助您理解 Workspace、Agent、模型、模型连接、Team、Skill 与 MCP 之间的关系。
[AgentCore](https://agentcore.console.aliyun.com/)中的资源以 Workspace 为边界组织。Workspace 内独立维护模型配置、Agent、Team 和 MCP 工具。Agent 是执行 AI 任务的单元，运行时关联一个模型，并可绑定 Skill 与 MCP；多个 Agent 可组成 Team。

## 概念总览
<table> <thead> <tr> <td><p><b>概念</b></p></td> <td><p></p></td> <td><p><b>定义</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>AgentCore</b></p></td> <td><p>阿里云的 AI 智能体构建与管理平台。</p></td> </tr> <tr> <td><p><b>Workspace</b></p></td> <td><p>资源隔离和管理的基本单元；独立维护模型、Agent、Team、MCP 工具等，互不干扰。</p></td> </tr> <tr> <td><p><b>Agent</b></p></td> <td><p>AI 智能体的执行单元，在 Workspace 内创建，接收任务后调用模型完成推理并给出结果；自身能力由绑定的资产决定，通过绑定 Skill 获得专业技能、绑定 MCP 工具获得外部工具调用能力，模型与凭证则提供推理能力和访问外部服务所需的密钥。</p></td> </tr> <tr> <td><p><b>Agent 模板</b></p></td> <td><p>可复用的 Agent 配置模板，用于快速创建同类型 Agent，减少重复配置。</p></td> </tr> <tr> <td><p><b>Agent 资产</b></p></td> <td><p><b>Skill</b></p></td> <td><p>Agent 调用的专业技能，支持ZIP 上传/Nacos CLI/预置模板三种导入方式。</p></td> </tr> <tr> <td><p><b>MCP</b></p></td> <td><p>Model Context Protocol；在 AgentCore 中为 Agent 扩展标准化工具集成，HTTP TO MCP 与直接代理两类，均要求网络可达。</p></td> </tr> <tr> <td><p><b>模型连接</b></p></td> <td><p>模型连接是接入模型供应商的通道，连接侧配置模型供应商、API 端点、协议与访问凭证。</p></td> </tr> <tr> <td><p><b>模型</b></p></td> <td><p>模型是连接下可供 Agent 选择的推理模型，模型侧记录上下文长度、单次最大输出、流式输出，以及工具调用、视觉、音频等能力项。</p></td> </tr> <tr> <td><p><b>凭证</b></p></td> <td><p>访问外部服务所需的密钥，以 Key-Value 形式集中保存；Key 为环境变量名（如 GITHUB_ACCESS_TOKEN），Value 创建后默认隐藏，供模型连接与工具的认证配置引用。</p></td> </tr> </tbody> </table>

## 概念详述
### AgentCore

[AgentCore](https://agentcore.console.aliyun.com/)是阿里云的 AI 智能体（Agent）构建与管理平台，能力分为四组：Agent 构建、资产管理、Agent 协作、身份与权限。AgentCore 的资源以 Workspace 为边界组织，每个 Workspace 独立维护模型配置、Agent、Team 和 MCP 工具，确保不同业务场景之间相互隔离。

### Workspace

Workspace 是 AgentCore 资源隔离和管理的基本单元，支持按项目或业务线独立分配资源。

具体操作，请参见[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)。

### Agent

Agent 是 AgentCore 中 AI 智能体的执行单元，关联模型并执行特定的 AI 任务。
<table> <thead> <tr> <td><p>Agent 类型</p></td> <td><p>说明</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Harness Agent</b></p></td> <td><p>由 AgentCore 提供运行框架的 Agent，在控制台完成配置即可创建并运行，无需自行开发或部署。配置项包括 Agent 名称、模型、所属 Team、SOUL.MD 与 AGENT.MD 文件、技能绑定与 MCP 工具绑定。</p></td> </tr> <tr> <td><p><b>高代码 Agent（待上线）</b></p></td> <td><p>以编写代码的方式开发的 Agent，适用于需要自定义业务逻辑、对运行过程有精细控制要求的场景。</p></td> </tr> <tr> <td><p><b>纳管 Agent</b></p></td> <td><p>将已部署在客户本地的 Agent 纳管到 AgentCore 统一管理，无需改造即可参与团队编排与协作。</p></td> </tr> <tr> <td><p><b>注册 Agent（待上线）</b></p></td> <td><p>将部署在 AgentCore 之外的 Agent 注册到平台，由平台统一调度。</p></td> </tr> </tbody> </table>

创建 Harness Agent 时需配置以下内容：
<table> <thead> <tr> <td><p>配置项</p></td> <td><p>说明</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Agent 名称</b></p></td> <td><p>Agent 的名称，用于在 Agent 列表中标识该 Agent。</p></td> </tr> <tr> <td><p><b>选择模型</b></p></td> <td><p>指定 Agent 执行任务时调用的模型，从 Workspace 内已配置的模型中选择。</p></td> </tr> <tr> <td><p><b>系统提示词</b></p></td> <td><p>定义 Agent 的角色设定与行为准则，内容分别写入 SOUL.MD 与 AGENT.MD。</p></td> </tr> <tr> <td><p><b>SubAgent</b></p></td> <td><p>为 Agent 添加 SubAgent，把复杂任务拆分给子 Agent 分别处理，由当前 Agent 负责调度。</p></td> </tr> <tr> <td><p><b>资源配置</b></p></td> <td><p>设置 Agent 运行时使用的资源规格。</p></td> </tr> <tr> <td><p><b>技能绑定</b></p></td> <td><p>绑定 Skill，为 Agent 补充特定领域的专业能力。</p></td> </tr> <tr> <td><p><b>MCP 绑定</b></p></td> <td><p>绑定 MCP 工具，为 Agent 扩展调用外部服务与工具的能力。</p></td> </tr> </tbody> </table>

具体操作，请参见[管理 Agent](https://help.aliyun.com/document_detail/3052293.html)。

### Agent 模板

Agent 模板是可复用的 Agent 配置，用于快速创建相同配置的 Agent，减少逐项重复配置。

具体操作，请参见[管理 Agent 模板](https://help.aliyun.com/document_detail/3052301.html)。

### Skill

Skill 是 Agent 调用的专业技能，例如发送通知、查询数据或触发工作流。Skill 的内容以 SKILL.md 定义，其 name 与 description 字段分别对应控制台中的 Skill 名称与描述。

Skill 支持三种导入方式：上传本地已打包为 ZIP 格式的 Skill、使用 Nacos CLI 导入本地 Skill 文件夹、导入预置 Skill 模板。

具体操作，请参见[管理 Skill](https://help.aliyun.com/document_detail/3052296.html)。

### MCP

MCP（Model Context Protocol）是用于将 Agent 与外部工具、数据源连接的协议。在 AgentCore 中，MCP 为 Agent 扩展标准化的工具集成能力，用于对接外部工具或第三方数据源。

具体操作，请参见[管理 MCP 工具](https://help.aliyun.com/document_detail/3052308.html)。

### Team

Team 是多个 Agent 组成的组织形式，在 Agent 之上再加一层组织。

具体操作，请参见[设置 Team 协作](https://help.aliyun.com/document_detail/3052302.html)。