---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-sdk-overview
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-sdk-overview
body_sha256: 0b1ead9ec00def21c03e6235499778ac155009791ff1fb59c699a0b9f4c6eedb
body_bytes: 6472
migration_status: current
---

基于 AgentCore 开发 Agent 应用时，模型、MCP 工具、Skill、记忆和凭证都由平台托管。逐个拼接资源访问地址和访问密钥会使应用随运行环境变化而失效，凭证也容易写进代码或日志。AgentCore SDK 让业务代码按名称调用这些托管资源，把资源接入已有的 Agent 框架，并通过 AG-UI 或 OpenAI Chat Completions 协议对外提供 Agent 服务。  
本文是 AgentCore SDK 文档入口，用于确认 SDK 的能力边界、选择开发语言、准备所需资源并选定对外服务协议；安装命令、代码示例和框架集成方法由两篇使用指南按开发语言分别介绍。

## 功能介绍
<table> <thead> <tr> <td> <p><b>功能</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>模型</p> </td> <td> <p>按模型连接名称调用云端模型，支持普通调用和流式输出；也可接入自有模型服务。</p> </td> </tr> <tr> <td> <p>MCP</p> </td> <td> <p>获取工具列表、调用工具，并将工具接入 Agent 框架；支持平台托管的 MCP 服务和自有服务。</p> </td> </tr> <tr> <td> <p>Skill</p> </td> <td> <p>加载平台已发布的 Skill，或加载随应用分发的 Skill 文件。</p> </td> </tr> <tr> <td> <p>记忆</p> </td> <td> <p>写入、检索、查询、更新和删除记忆，并通过框架适配器接入 Agent 执行流程。</p> </td> </tr> <tr> <td> <p>凭证</p> </td> <td> <p>按名称获取托管凭证，或为 MCP 显式绑定 MCP Header 凭证。</p> </td> </tr> <tr> <td> <p>框架适配</p> </td> <td> <p>转换模型、工具和执行事件。</p> </td> </tr> <tr> <td> <p>对外服务协议</p> </td> <td> <p>使用 AgentCoreServer 提供 AG-UI、OpenAI Chat Completions 或自定义协议服务，也可以继续使用现有 Web 服务。</p> </td> </tr> </tbody> </table>

本文介绍的 `alibabacloud-agentcore-sdk` 是用于开发 Agent 应用的 SDK，与调用平台管理 API 的 OpenAPI SDK 不是同一个包。SDK 不负责创建 Workspace、上传代码、构建镜像或部署应用。云端资源示例由 AgentCore 托管的应用运行环境执行，SDK 从运行环境获取访问配置，业务代码无需填写平台访问密钥。自有模型、自有 MCP 服务和随应用分发的 Skill 无需注册为平台资源，其连接方式见对应使用指南的"接入自定义资源"。

## 选择开发语言
<table> <thead> <tr> <td> <p><b>开发语言</b></p> </td> <td> <p><b>使用指南</b></p> </td> <td> <p><b>基础运行环境</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Python</p> </td> <td> <p>AgentCore Python SDK 使用指南</p> </td> <td> <p>Python 3.10 及以上。部分框架需要更高版本，详见对应使用指南。</p> </td> </tr> <tr> <td> <p>JavaScript / TypeScript</p> </td> <td> <p>AgentCore Node.js SDK 使用指南</p> </td> <td> <p>Node.js 20.3 及以上。部分框架需要更高版本，详见对应使用指南。</p> </td> </tr> </tbody> </table>

两篇使用指南都包含托管资源与自定义资源的调用方法、完整的 LangChain Agent 服务示例、协议调用示例和常见问题，只需阅读所用语言的那一篇，无需对照另一种语言的参数和代码。各语言支持的框架与记忆适配范围详见对应使用指南。

## 使用前准备
1. 开通 AgentCore，并按[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)创建 Agent 所属的 Workspace。

2. 根据应用需要的能力准备资源，并确认 Agent 对这些资源具有相应访问权限。

   各能力需要准备的资源如下：

<table> <thead> <tr> <td> <p><b>需要的能力</b></p> </td> <td> <p><b>需要准备的资源</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>调用云端模型</p> </td> <td> <p>模型连接，以及该连接中已配置的模型。创建方式见<a href="https://help.aliyun.com/document_detail/3052299.html">管理模型</a>。</p> </td> </tr> <tr> <td> <p>使用 MCP</p> </td> <td> <p>MCP 服务。创建方式见<a href="https://help.aliyun.com/document_detail/3052308.html">管理 MCP 工具</a>。</p> </td> </tr> <tr> <td> <p>使用 Skill</p> </td> <td> <p>已启用且有已发布版本的 Skill。创建与发布流程见<a href="https://help.aliyun.com/document_detail/3052296.html">管理 Skill</a>。</p> </td> </tr> <tr> <td> <p>使用记忆</p> </td> <td> <p>MemoryStore。</p> </td> </tr> <tr> <td> <p>使用托管凭证</p> </td> <td> <p>按需创建 API Key 凭证或 MCP Header 凭证。创建与授权方式见<a href="https://help.aliyun.com/document_detail/3052318.html">管理凭证</a>。</p> </td> </tr> </tbody> </table>

只调用模型时，无需创建 MCP、Skill、MemoryStore 或额外凭证。完成准备后，打开所用语言的使用指南，安装 SDK 及所需框架依赖，然后编写并部署 Agent 应用。

## 选择对外服务协议
<table> <thead> <tr> <td> <p><b>需求</b></p> </td> <td> <p><b>协议</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>展示 Agent 多步执行过程、消息边界、工具调用和结果</p> </td> <td> <p>AG-UI</p> </td> </tr> <tr> <td> <p>接入使用 Chat Completions 格式的客户端</p> </td> <td> <p>OpenAI Chat Completions</p> </td> </tr> </tbody> </table>

AG-UI 与 OpenAI Chat Completions 的表达范围不同：AG-UI 保留独立的工具结果事件，OpenAI Chat Completions 不提供独立的工具结果响应事件。具体请求示例、事件说明和限制见对应使用指南的"调用 Agent 服务"。此外，AgentCoreServer 也支持以自定义协议对外提供服务，还可以继续使用现有 Web 服务。

AgentCoreServer 只负责协议接入，不会自动持久化对话历史。会话状态由应用或框架维护，长期记忆不能替代完整的会话历史。

## 相关文档
* [AgentCore Python SDK 使用指南](https://help.aliyun.com/document_detail/3061225.html)

* [AgentCore Node.js SDK 使用指南](https://help.aliyun.com/document_detail/3061224.html)

* [Python SDK 安装包](https://pypi.org/project/alibabacloud-agentcore-sdk/)：查看 SDK 在 PyPI 上的已发布版本。

* [Node.js SDK 安装包](https://www.npmjs.com/package/alibabacloud-agentcore-sdk)：查看 SDK 在 npm 上的已发布版本。