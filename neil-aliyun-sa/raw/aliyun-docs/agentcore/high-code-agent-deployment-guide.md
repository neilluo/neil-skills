---
source_url: https://help.aliyun.com/zh/agentcore/high-code-agent-deployment-guide
fetch_date: 2026-09-20
product: AgentCore
slug: high-code-agent-deployment-guide
body_sha256: e9f36b6ac3593578b3f06e67ba29274ca8459ce407c6a5688305914bd6ecfbb2
body_bytes: 16039
migration_status: current   # 见 FETCH-CONTRACT §3
---

高代码 Agent 支持将自行开发的 Agent 应用以容器镜像部署到 AgentCore。您可以保留已有的开发框架和 HTTP 服务，在控制台配置运行环境、调试对话并获取调用地址。  
本文介绍控制台操作。应用开发、SDK 安装及框架接入，请参见[开发参考](https://help.aliyun.com/document_detail/3061297.html)；首次体验可参见[使用 Python SDK 快速创建高代码 Agent](https://help.aliyun.com/document_detail/3061880.html)。

## 前提条件
* 已开通 AgentCore，并创建 Workspace。具体操作，请参见[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)。

* 已准备可运行的 Agent 容器镜像，并推送至企业版容器镜像服务 ACR。

* 已明确应用的启动命令、监听端口、健康检查路径及对话协议。

* 如应用使用平台模型、MCP、Skill 等资源，已在目标 Workspace 中完成相应资源配置，并准备具备所需权限的执行角色。

**说明** ：本文介绍将自建代码部署到 AgentCore 托管运行，不是将本地运行的 Agent 纳管到平台。自建 HTTP 服务无需替换为 `AgentCoreServer`，但其实际接口必须与控制台填写的协议和路径一致。

## 步骤一：检查镜像与应用配置
创建前，确认镜像满足以下要求。
<table> <thead> <tr> <td> <p>检查项</p> </td> <td> <p>要求</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>镜像架构</p> </td> <td> <p>支持 <code>linux/amd64</code>（x86_64），不能仅支持 ARM64。</p> </td> </tr> <tr> <td> <p>Shell 环境</p> </td> <td> <p>镜像中同时提供可执行的 <code>/bin/bash</code> 和 <code>/bin/sh</code>。</p> </td> </tr> <tr> <td> <p>镜像仓库</p> </td> <td> <p>当前仅支持企业版 ACR。按当前创建页要求，实例需开启公开匿名拉取，镜像仓库需设为公开。不要将密钥或业务数据打入公开镜像。</p> </td> </tr> <tr> <td> <p>服务监听</p> </td> <td> <p>应用监听 <code>0.0.0.0</code>，服务端口与控制台配置一致。仅监听 <code>127.0.0.1</code> 的服务无法正常接收平台转发的请求。</p> </td> </tr> <tr> <td> <p>健康检查</p> </td> <td> <p>应用提供可访问的健康检查接口。路径和端口以应用实际实现为准。</p> </td> </tr> <tr> <td> <p>依赖与配置</p> </td> <td> <p>镜像包含启动所需的程序、依赖和文件；业务环境变量在部署时按需填写。</p> </td> </tr> </tbody> </table>

镜像仓库还需从 Agent 运行环境网络可达。本地能够推送或拉取镜像，不代表云端可以拉取。网络设置见后文"配置网络和日志"。镜像构建示例，请参见[使用 Python SDK 快速创建高代码 Agent](https://help.aliyun.com/document_detail/3061880.html)。

## 步骤二：创建高代码 Agent
### 1. 进入创建页面

1. 登录 [AgentCore 控制台](https://agentcore.console.aliyun.com/)。

2. 在顶部选择目标地域，并切换至目标 Workspace。

3. 在左侧导航栏单击 **Agent** ，单击 **创建 Agent**。

4. 在 **选择创建方式** 中选择 **自定义代码 / 镜像**。

### 2. 配置基本信息和容器镜像

在 **基本信息** 区域填写以下内容。
<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>操作说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Agent 名称</p> </td> <td> <p>设置便于识别的名称，例如 <code>my-code-agent</code>。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>可选。填写应用用途或职责。</p> </td> </tr> <tr> <td> <p>容器镜像实例</p> </td> <td> <p>选择已准备的企业版 ACR 实例。新建实例后可单击刷新按钮重新加载。</p> </td> </tr> <tr> <td> <p>镜像仓库</p> </td> <td> <p>选择镜像所在的仓库。</p> </td> </tr> <tr> <td> <p>镜像版本</p> </td> <td> <p>在版本列表中选择要部署的版本，可通过 Digest、镜像大小和最近推送时间核对。</p> </td> </tr> </tbody> </table>

建议为每次发布使用明确的版本标签，便于后续确认部署内容和定位问题。

### 3. 配置启动方式和执行角色

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>操作说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>启动命令</p> </td> <td> <p>填写镜像内可执行的应用启动命令。不要直接照抄与自身目录、入口文件不一致的示例。</p> </td> </tr> <tr> <td> <p>服务端口</p> </td> <td> <p>填写应用实际监听端口。创建页默认显示 <code>8080</code>；若应用监听 <code>9000</code>，需改为 <code>9000</code>。</p> </td> </tr> <tr> <td> <p>执行角色</p> </td> <td> <p>选择授予 Agent 运行时所需云资源访问权限的角色。可通过 <b>查看策略</b> 核对权限，通过刷新按钮更新角色列表。</p> </td> </tr> <tr> <td> <p>环境变量</p> </td> <td> <p>按应用要求添加名称和值，支持表单模式和 JSON 模式。应用无需额外环境变量时可不填。</p> </td> </tr> </tbody> </table>

执行角色用于 Agent 访问云资源，不是外部调用 Agent 的 API Key。角色要求请参见页面上的 **授权说明**。

所选角色的状态决定页面上可用的授权入口：

* 角色显示 **未创建** 时，单击 **一键创建并授权**，由平台创建角色并附加所需策略。

* 角色已存在但缺少所需权限时，页面会列出缺失的权限，可单击 **一键授权** 补齐，或单击 **前往 RAM 控制台授权** 自行处理。

* 授权完成后提示 **授权成功，权限已生效**。若提示授权未完成或权限尚未生效，请重试。

**说明**：授权窗口被浏览器拦截时，需允许弹出窗口后重试。当前账号缺少相应权限时，页面无法列出角色，需联系主账号或权限管理员授权。

使用平台模型、MCP 或 Skill 时，由代码引用相应资源。高代码创建页不会像托管 Harness 一样替应用生成提示词、选择模型或注册工具，具体接入方法请参见对应语言的 SDK 使用指南。

### 4. 声明对话协议

在 **协议配置** 中单击 **配置**，勾选应用实际支持的协议，填写 Path，并按需添加 Header。可同时声明两种协议。
<table> <thead> <tr> <td> <p>页面选项</p> </td> <td> <p>适用场景</p> </td> <td> <p>页面预填 Path</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Chat Completions</p> </td> <td> <p>使用 OpenAI Chat Completions 格式调用 Agent。</p> </td> <td> <p><code>/openai/v1/chat/completions</code></p> </td> </tr> <tr> <td> <p>AGUI</p> </td> <td> <p>使用 AG-UI 格式进行流式对话，展示应用返回的执行过程和工具事件。</p> </td> <td> <p><code>/ag-ui/agent</code></p> </td> </tr> </tbody> </table>

* **Path** ：填写应用的实际接口路径，以 `/` 开头，不填写完整域名。例如自建服务使用 `/v1/chat/completions`，应修改为该路径。

* **Header**：填写调用该协议接口时需要携带的固定请求头。没有额外要求时留空；不要将下游模型的 API Key 误填为 Agent 接口的鉴权信息。

填写后单击弹窗内的 **保存**。

**说明**：协议声明不会为应用自动生成对应接口，也不会自动增加工具事件。未声明协议时，控制台调试面板无法按协议发起对话；如果声明与实际接口不一致，可能出现 404 或响应解析失败。

### 5. 配置运行资源和健康检查

在 **高级配置** 中按需调整以下参数。
<table> <thead> <tr> <td> <p>配置项</p> </td> <td> <p>操作说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>规格</p> </td> <td> <p>选择应用所需的 CPU 和内存。</p> </td> </tr> <tr> <td> <p>实例数</p> </td> <td> <p>设置运行实例数量。</p> </td> </tr> <tr> <td> <p>实例最大 Session 数</p> </td> <td> <p>设置单个实例承载的 Session 数量上限，并结合应用并发能力调整。</p> </td> </tr> <tr> <td> <p>Session TTL（秒）</p> </td> <td> <p>设置平台 Session 的存活时间参数；这不是模型单次生成的超时时间。</p> </td> </tr> <tr> <td> <p>会话隔离方式</p> </td> <td> <p>根据业务选择 <b>不启用</b>、<b>会话亲和</b> 或 <b>Header 隔离</b>，并完成所选方式要求的配置。</p> </td> </tr> <tr> <td> <p>健康检查</p> </td> <td> <p>填写检查路径、检查端口、检查间隔、超时时间和不健康阈值。</p> </td> </tr> </tbody> </table>

平台会按配置进行健康检查。连续检查失败会影响实例接收流量，并可能触发实例重启。因此，不能只修改服务端口而保留不匹配的检查端口。

以下为官网 Python 快速入门示例的部署值，**仅适用于该示例，其他应用按实际实现填写**。
<table> <thead> <tr> <td> <p>配置项</p> </td> <td> <p>示例值</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>启动命令</p> </td> <td> <p><code>uvicorn app:server --host 0.0.0.0 --port 9000</code></p> </td> </tr> <tr> <td> <p>服务端口</p> </td> <td> <p><code>9000</code></p> </td> </tr> <tr> <td> <p>对话协议与路径</p> </td> <td> <p>AGUI，<code>/ag-ui/agent</code></p> </td> </tr> <tr> <td> <p>健康检查路径</p> </td> <td> <p><code>/readyz</code></p> </td> </tr> <tr> <td> <p>健康检查端口</p> </td> <td> <p><code>9000</code></p> </td> </tr> </tbody> </table>

**说明** ：当前创建页的健康检查默认路径为 `/healthz`。使用 `/readyz` 或其他路径的应用，需要手动修改，不应直接保留页面默认值。

### 6. 配置网络和日志

**网络配置**

* 应用需要访问公网模型服务或其他公网接口时，按需开启 **允许默认网卡访问公网**。

* 应用需要访问 Workspace 的 VPC 资源时，按需开启 **允许访问 VPC**。开启后使用当前 Workspace 的 VPC 配置。

* 未开启 VPC 访问时，镜像通过公网拉取。如 ACR 配置了公网访问白名单，将页面显示的 **当前 Workspace 公网出口 IP** 加入白名单；开启 VPC 访问后，平台会尝试经 VPC 拉取镜像，需同时确认 ACR 允许对应 VPC 访问。

**日志配置**

建议开启 **启用日志** ，选择 **日志项目** 和 **日志库**，以便在部署或调用异常时查看运行日志。应用也需要输出有助于排障的启动信息和错误日志，避免打印密钥及敏感业务内容。

### 7. 提交创建

核对镜像版本、启动命令、服务端口、协议路径和健康检查配置，单击页面右上角的 **立即创建**。

创建后返回 Agent 列表，等待状态变为 **运行中** 。将鼠标移至对应卡片，单击 **详情** ，可在 **概览与配置** 中查看已保存的镜像版本、启动配置和协议声明。

## 步骤三：在控制台调试
1. 打开 Agent 详情，单击 **调试**。

2. 在协议下拉框中选择已声明的协议，确认 **调试端点** 显示就绪。

3. 输入一条简单消息，例如"你好，请用一句话介绍你能做什么"，单击发送。

4. 检查 Agent 是否返回预期回答。随后再测试需要调用工具或访问业务资源的请求。

需要重新开始对话时，单击 **创建会话** 。排障时可复制页面上的会话 ID，并通过 **运行日志** 查看对应时间段的记录。

**说明**：能否展示执行过程和工具调用，取决于应用返回的协议事件。仅在控制台勾选 AGUI，不会自动补齐代码未输出的事件。

## 步骤四：从业务应用调用
1. 在 Agent 详情中单击 **外部渠道配置**。

2. 单击 **直接访问**，查看 Endpoint 状态和调用地址。

3. 在 **鉴权方式** 中单击 **获取鉴权信息**，按页面显示的 Header 名称和 API Key 配置调用方。

4. 参考页面的 **API 调用说明** 和调用示例发起请求，使用与协议声明一致的路径及请求格式。

Endpoint 是 Agent 应用的访问地址，不是下游模型供应商地址。API Key 应保存在可信的服务端配置中，不要写入公开前端代码或文档。

请求体和流式响应的开发示例，请参见 [Python SDK 使用指南](https://help.aliyun.com/document_detail/3061225.html)或 [Node.js SDK 使用指南](https://help.aliyun.com/document_detail/3061224.html)中的"调用 Agent 服务"。自建 Server 使用其实际实现的协议。

## 更新 Agent
1. 将新版本镜像推送到 ACR。

2. 打开 Agent 详情，在 **概览与配置** 中单击 **编辑配置** ；也可从列表卡片进入 **编辑**。

3. 刷新镜像版本列表并选择新版本。若应用入口、端口或协议发生变化，同步修改启动命令、服务端口、健康检查和协议配置。

4. 单击 **保存**，等待更新完成，并重新进行控制台调试和业务调用验证。

更新可能影响正在处理的请求，建议在合适的业务时间窗口操作。不要仅根据 ACR 中出现新镜像，就判断 Agent 已使用新版本，应在 Agent 配置中核对。

## 查看运行状态和排查异常
<table> <thead> <tr> <td> <p>入口</p> </td> <td> <p>用途</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>概览与配置</p> </td> <td> <p>核对当前镜像版本、启动命令、端口、环境变量和协议声明。</p> </td> </tr> <tr> <td> <p>实例与 Session</p> </td> <td> <p>查看实例状态、Session 数量，并按实例 ID 或 Session ID 定位。</p> </td> </tr> <tr> <td> <p>可观测 → 基础监控</p> </td> <td> <p>查看所选时间范围的运行数据。</p> </td> </tr> <tr> <td> <p>可观测 → 运行日志</p> </td> <td> <p>查看已配置采集的应用日志。</p> </td> </tr> </tbody> </table> <table> <thead> <tr> <td> <p>现象</p> </td> <td> <p>优先检查</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>找不到镜像或拉取失败</p> </td> <td> <p>地域、ACR 实例及仓库、镜像版本、公开匿名拉取配置，以及公网白名单或 VPC 访问配置。</p> </td> </tr> <tr> <td> <p>实例未就绪或反复重启</p> </td> <td> <p>镜像架构、Shell、启动命令、依赖、资源规格；核对应用监听地址、服务端口和健康检查路径、端口。</p> </td> </tr> <tr> <td> <p>调试页没有可选协议</p> </td> <td> <p>在 <b>编辑配置 → 协议配置</b> 中声明应用支持的协议并保存。</p> </td> </tr> <tr> <td> <p>调用返回 404</p> </td> <td> <p>协议 Path 是否与应用路由一致，是否误把示例路径用于自建服务。</p> </td> </tr> <tr> <td> <p>调用返回鉴权错误</p> </td> <td> <p>区分外部调用的 Endpoint API Key 与应用访问云资源的执行角色；按失败环节核对。</p> </td> </tr> <tr> <td> <p>普通对话正常，但模型或工具调用失败</p> </td> <td> <p>代码引用的资源名称、所属 Workspace、执行角色权限，以及下游服务是否可达。</p> </td> </tr> <tr> <td> <p>看不到运行日志</p> </td> <td> <p>是否已启用日志并选择正确的日志项目、日志库；应用是否输出日志，查询时间是否覆盖失败时刻。</p> </td> </tr> </tbody> </table>

向技术支持反馈时，提供地域、Workspace ID、Agent ID、失败时间和错误信息；如有会话 ID 或请求 ID，一并提供。不要附带 API Key 或完整敏感请求头。

## 开发参考
* [开发参考](https://help.aliyun.com/document_detail/3061297.html)

* [使用 Python SDK 快速创建高代码 Agent](https://help.aliyun.com/document_detail/3061880.html)

* [AgentCore Python SDK 使用指南](https://help.aliyun.com/document_detail/3061225.html)

* [AgentCore Node.js SDK 使用指南](https://help.aliyun.com/document_detail/3061224.html)