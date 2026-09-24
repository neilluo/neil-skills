---
source_url: https://help.aliyun.com/zh/agentcore/guidelines-for-the-use-of-local-nanoagent
fetch_date: 2026-09-20
product: AgentCore
slug: guidelines-for-the-use-of-local-nanoagent
body_sha256: 730c3990f85f3f097f2226aa2a76da4facdc0ba30a76b4e659df7a4cc69a175d
body_bytes: 28362
migration_status: current   # 见 FETCH-CONTRACT §3
---

需要将团队已有的本地开发环境接入 AgentCore Team 统一协作时，可以使用本地纳管 Agent：Agent 进程运行在自有的电脑或服务器上，由 LoongSuite Pilot 完成本地进程管理，并作为 Team Worker 加入 AgentCore Team 参与协作。本文说明本地纳管 Agent 的创建、接入、使用、运维和故障处理方法，适用于 Claude Code、Codex、OpenClaw 和 Qoder CLI。  
**警告**

启动命令包含连接凭据和云监控配置，属于敏感信息。不得将完整启动命令、bootstrap token 或云监控配置保存到代码仓库、文档、工单、日志系统或即时通信记录中。

## 接入准备
### 控制台条件

接入前确认以下条件：

1. 工作空间已开启 **Team 协作**。本地纳管 Agent 只能作为 Team Worker 使用，不支持设置为 Leader，且每个纳管 Agent 仅可加入一个 Team。

2. 已创建目标 Team。

3. 当前账号具备 Agent 创建和 Team 管理权限。

4. 已在控制台准备需要分配的模型连接、Skill 和 MCP。

未开启 Team 协作时，控制台不允许创建纳管 Agent。

### 本地环境条件

运行机器需满足以下要求：
<table> <thead> <tr> <td><p><b>项目</b></p></td> <td><p><b>要求</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>操作系统</p></td> <td><p>启动命令页面支持的 Linux/macOS 或 Windows</p></td> </tr> <tr> <td><p>本地运行时</p></td> <td><p>已安装 Claude Code、Codex、OpenClaw 或 Qoder CLI，并满足第 1.4 节版本要求</p></td> </tr> <tr> <td><p>本地模型</p></td> <td><p>选择本地模型时，运行时已完成登录、凭据和模型配置</p></td> </tr> <tr> <td><p>项目目录</p></td> <td><p>已确定 Agent 需要访问的目录，并具备必要的读写权限</p></td> </tr> <tr> <td><p>网络</p></td> <td><p>能够访问所选网络对应的 AgentCore、模型和 MCP 服务</p></td> </tr> </tbody> </table>

无需预先安装 LoongSuite Pilot。控制台生成的完整启动命令会自动完成 Pilot 的安装或升级。

### 本地运行时验证

选择本地模型前，先在目标机器终端验证运行时能够正常启动并调用模型。运行时命令不在默认 PATH 中时，记录其绝对路径，供后续接入时配置。

### 版本要求

<table> <thead> <tr> <td><p><b>组件</b></p></td> <td><p><b>最低版本要求</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>LoongSuite Pilot</p></td> <td><p>使用当前启动命令安装或升级的版本</p></td> <td><p>版本以控制台当前启动命令的安装或升级结果为准；已有安装仍需完整执行 LoongSuite Pilot 步骤</p></td> </tr> <tr> <td><p>Claude Code</p></td> <td><p>2.1.141 或以上</p></td> <td><p>低版本不支持纳管所需的配置参数</p></td> </tr> <tr> <td><p>Codex</p></td> <td><p>0.103 或以上</p></td> <td><p>需支持稳定的运行和 Trace 能力</p></td> </tr> <tr> <td><p>OpenClaw（Linux/macOS）</p></td> <td><p>2026.5.12 或以上</p></td> <td><p>需满足 OpenClaw 运行和 Trace 能力要求</p></td> </tr> <tr> <td><p>OpenClaw（Windows）</p></td> <td><p>2026.6.11 或以上</p></td> <td><p>Windows 需要支持对应的消息文件能力</p></td> </tr> <tr> <td><p>Qoder CLI</p></td> <td><p>1.0.33 或以上</p></td> <td><p>低版本与当前运行方式不兼容</p></td> </tr> </tbody> </table>

版本检查命令：

```
HELPCODEESCAPE-bash
loongsuite-pilot info
claude --version
codex --version
openclaw --version
qodercli --version
```

仅需检查实际使用的运行时。本地版本低于最低要求时，先升级运行时，再执行控制台最新生成的完整启动命令。

本地 Skill/MCP 继承功能要求使用控制台当前启动命令安装或升级的 LoongSuite Pilot 和运行时组件。该能力不能仅根据 Pilot 的版本号判断；已有安装未执行过当前启动命令时，重新执行完整的 Pilot 安装配置步骤。核对或提交排障信息时，使用以下命令获取实际版本：

```
HELPCODEESCAPE-bash
loongsuite-pilot info
```

版本要求可能随产品升级调整。重新接入时，以本文档和控制台生成的启动命令为准。

## 创建纳管 Agent
### 创建步骤

1. 在左侧导航栏单击 **Team 协作**，确认功能已开启。

2. 进入 **Agent** 页面。

3. 单击右上角的 **纳管 Agent**。

4. 配置 Agent 名称、描述和系统提示词。

5. 选择模型来源和模型配置。

6. 选择所属 Team。

7. 根据需要分配 Skill 和 MCP。

8. 保存配置，等待 Agent 状态变为运行中。

### 模型来源

<table> <thead> <tr> <td><p><b>模型来源</b></p></td> <td><p><b>适用场景</b></p></td> <td><p><b>使用前确认</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>平台模型</b></p></td> <td><p>使用控制台统一管理的模型连接</p></td> <td><p>模型连接可用，Agent 已选择正确模型</p></td> </tr> <tr> <td><p><b>本地模型</b></p></td> <td><p>使用运行时已有的账号、模型配置或原生模型路由</p></td> <td><p>运行时已在本机完成登录并能够调用模型</p></td> </tr> </tbody> </table>

**本地模型**表示模型配置由本地运行时管理，不表示模型服务部署在本机。控制台无法检查本地账号登录状态、模型额度和本地凭据是否有效。

### 运行时与模型支持

<table> <thead> <tr> <td><p><b>运行时</b></p></td> <td><p><b>平台模型</b></p></td> <td><p><b>本地模型</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Claude Code</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>根据 Agent 模型来源使用平台配置或本地配置</p></td> </tr> <tr> <td><p>OpenClaw</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>根据 Agent 模型来源使用平台配置或本地配置</p></td> </tr> <tr> <td><p>Codex</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>根据 Agent 模型来源使用平台配置或本地配置</p></td> </tr> <tr> <td><p>Qoder CLI</p></td> <td><p>不支持</p></td> <td><p>支持</p></td> <td><p>使用 Qoder CLI 本地模型配置；可通过 <code>--qoder-model</code> 指定模型</p></td> </tr> </tbody> </table>

### 系统提示词、Skill 和 MCP

以下配置项已在创建步骤（第 2.1 节）完成初始设置；创建完成后，在 Agent 详情页查看和调整：

* 通过 **系统提示词**配置 Agent 的职责、工作范围和输出要求。

* 通过 **管理 Skills** 分配平台 Skill。

* 通过 **管理 MCP** 分配平台 MCP。

* 通过 Team 配置确认 Agent 的协作关系。

配置更新后需等待系统生效。运行中的 Agent 未获取最新配置时，先确认连接和心跳状态，再重新连接。

## 生成启动命令
### 进入启动命令页面

Agent 状态变为运行中后，进入 Agent 详情页，在**启动命令** 区域生成命令。需要重新接入、迁移机器或轮换凭据时，单击**重新生成启动命令**。每次生成的令牌明文仅在当前页面展示，关闭页面后无法再次查看，需要重新签发。

### 选择访问网络

第一步选择运行机器访问 AgentCore 的网络：
<table> <thead> <tr> <td><p><b>访问网络</b></p></td> <td><p><b>适用条件</b></p></td> <td><p><b>选择依据</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>内网访问</p></td> <td><p>运行机器与 AgentCore 位于同一 VPC，或已通过专线、VPN 等方式实现内网互通</p></td> <td><p>运行机器可访问页面提供的内网地址</p></td> </tr> <tr> <td><p>公网访问</p></td> <td><p>运行机器与 AgentCore 位于不同网络环境</p></td> <td><p>办公电脑、个人电脑或跨网络服务器通常选择公网访问</p></td> </tr> </tbody> </table>

页面会标识当前可用的访问方式，无法确认 VPC 关系时，由环境管理员确认网络条件。网络选项不仅影响 Agent 连接，也影响运行数据上报；连接状态正常但运行数据缺失时，同时检查网络选择和目标地址连通性。

### 选择操作系统和运行时

第二步选择操作系统和运行时：

* 操作系统：**Linux/macOS** 或 **Windows**。

* 运行时：**Claude Code** 、**OpenClaw** 、**Qoder CLI** 或 **Codex**。

操作系统必须与实际执行启动命令的机器一致，运行时必须与本机已安装的命令一致。页面同时展示以下信息：

* 本地 Agent 由 LoongSuite Pilot 管理。

* Trace 将上报至当前账号下的云监控 2.0 工作空间，用于运行数据分析。

* 启动命令包含连接凭据和云监控配置。

* 令牌明文仅在当前页面展示。

### 执行完整命令

生成的启动命令包括两个连续步骤：

1. **安装并配置 LoongSuite Pilot**。

2. **连接并纳管 Agent**。

单击**复制全部**，在目标机器上按顺序执行全部命令。不得跳过第 1 步，也不得仅复制第 2 步。

执行要求：

* 以页面生成的命令为准，不手工修改连接凭据和云监控参数。

* Linux/macOS 与 Windows 的命令不可混用。

* 页面关闭后需要重新执行时，重新生成启动命令。

* 启动命令疑似泄露时，立即重新生成，旧命令停止使用。

### 设置工作目录

工作目录决定 Agent 默认访问和修改的本地文件范围：

* 启动命令包含 `--work-dir` 时，使用该参数指定的目录。

* 未指定 `--work-dir` 时，使用执行连接命令时所在的当前目录。

* 建议使用绝对路径，避免 Pilot 服务启动位置变化导致目录不一致。

* 目录应仅授予完成任务所需的权限。

以下示例适用于本地实例已存在、通过重新连接修改工作目录的场景（见第 8.3 节）：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID \
  --work-dir /absolute/path/to/project
```

命令中的 `INSTANCE_ID` 为本地实例 ID，可通过 `loongsuite-pilot worker list` 获取。

## 首次接入验证
启动命令执行完成后，按以下顺序验证。

### 验证 Pilot

```
HELPCODEESCAPE-bash
# 查看服务状态
loongsuite-pilot status

# 查看版本和配置信息
loongsuite-pilot info
```

`status` 应显示服务正在运行，版本信息以 `info` 输出为准。

### 验证本地实例

```
HELPCODEESCAPE-bash
# 查看全部实例
loongsuite-pilot worker list

# 查看指定实例
loongsuite-pilot worker status INSTANCE_ID
```

`worker list` 应包含新接入的实例；`worker status` 应能查看运行时、状态、工作目录、Agent、Team、心跳和日志位置。

### 验证控制台状态

返回 Agent 详情页，确认：

* 部署方式显示为本地纳管。

* 连接状态显示**已连接**。

* 所属 Team、模型、Skill 和 MCP 与预期一致。

* 最近纳管时间和配置状态正常。

### 验证 Team 协作

在目标 Team @ 该 Agent，执行只读验证任务：

1. 返回当前工作目录。

2. 列出项目顶层文件。

3. 说明当前可用的 Skill 和 MCP。

4. 不修改文件。

工作目录、Team 或资源配置不符合预期时，先修正接入配置，再执行实际任务。

## 使用纳管 Agent
### 发起任务

<table> <thead> <tr> <td><p><b>会话类型</b></p></td> <td><p><b>使用方式</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Team 群聊或任务会话</p></td> <td><p>@ 目标 Agent 后发送任务</p></td> </tr> <tr> <td><p>Agent 直接会话</p></td> <td><p>直接发送任务</p></td> </tr> </tbody> </table>

任务描述应明确目标、允许修改的目录、交付物和验收标准。涉及写操作时，先确认工作目录正确。  
**重要**

Agent 在本地生成的文件不会自动上传到 Team。需要交付文件时，任务描述应明确要求以附件形式提交；如果回复中仅包含本地路径，文件仍保存在运行机器上。

### 会话控制

<table> <thead> <tr> <td><p><b>命令</b></p></td> <td><p><b>作用</b></p></td> <td><p><b>是否清空上下文</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>/stop</code></p></td> <td><p>终止当前执行</p></td> <td><p>否</p></td> </tr> <tr> <td><p><code>/clear</code></p></td> <td><p>终止当前执行并清空会话上下文</p></td> <td><p>是</p></td> </tr> </tbody> </table>

通过 Team 群聊或任务会话发送控制命令时，同时 @ 目标 Agent。控制命令单独发送，不与普通任务内容合并。

### 任务并发

默认并发数为 2，支持设置为 1～8：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID -- \
  --max-concurrent-tasks 3
```

并发数用于控制不同会话的同时执行数量，同一会话内的消息仍按顺序处理。并发数会影响 CPU、内存和模型额度消耗，应根据运行机器资源配置。`--max-concurrent-tasks` 等运行时参数应写在 `--` 分隔符之后。  
**重要**

重连时，在 `--` 后传入的运行时参数会整体替换原有参数。修改任一参数时，应同时传入仍需保留的其他运行时参数。

## 使用平台和本地 Skill/MCP
### 默认资源范围

默认情况下，纳管 Agent 可使用：

* 控制台分配的平台 Skill 和 MCP。

* 项目目录中随项目提供的 Skill。

本地个人目录中的 Skill 和本地 MCP 默认不继承，以避免未经确认的个人资源被 Team 任务调用。

### 继承本地资源

版本前置条件：

1. 执行 `loongsuite-pilot info` 查看当前 Pilot 版本和安装信息。

2. 确认本机已执行控制台当前生成的完整启动命令。

3. 旧安装、来源不明的安装或无法识别继承参数时，重新执行 安装并配置 LoongSuite Pilot 步骤，并重新连接 Agent。

启用前确认：

* Skill 和 MCP 来源可信。

* 本地命令及依赖在目标机器可用。

* MCP 权限符合 Team 任务范围。

* Skill、启动参数和项目文件中不包含个人密钥。

确认本地资源可信且符合 Team 使用要求后，启用本地资源继承：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID -- \
  --inherit-local-resources true
```

启用后，Agent 按所选运行时的标准配置读取本地个人 Skill 和 MCP。平台 MCP 与本地 MCP 同名时，平台配置优先。停用本地资源继承：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID -- \
  --inherit-local-resources false
```

**重要**

重连时，在 `--` 后传入的运行时参数会整体替换原有参数，规则详见第 5.3 节。

## 查看状态和日志
### 状态说明

<table> <thead> <tr> <td><p><b>状态</b></p></td> <td><p><b>含义</b></p></td> <td><p><b>处理建议</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>pending</code></p></td> <td><p>实例正在准备</p></td> <td><p>等待后重新查看</p></td> </tr> <tr> <td><p><code>running</code></p></td> <td><p>实例正常运行</p></td> <td><p>无需处理</p></td> </tr> <tr> <td><p><code>waiting</code></p></td> <td><p>实例正在等待运行时满足启动条件</p></td> <td><p>检查运行时命令和本地配置</p></td> </tr> <tr> <td><p><code>degraded</code></p></td> <td><p>实例已运行，但连接、心跳或部分能力异常</p></td> <td><p>查看 Reason、Message 和日志</p></td> </tr> <tr> <td><p><code>failed</code></p></td> <td><p>实例启动失败</p></td> <td><p>根据错误信息和日志处理</p></td> </tr> <tr> <td><p><code>stopping</code></p></td> <td><p>已请求断开，进程正在停止</p></td> <td><p>等待状态变为 <code>disabled</code></p></td> </tr> <tr> <td><p><code>disabled</code></p></td> <td><p>实例已断开</p></td> <td><p>需要恢复时重新连接</p></td> </tr> <tr> <td><p><code>stale</code></p></td> <td><p>记录的进程已不再活动</p></td> <td><p>查看日志后重新连接</p></td> </tr> </tbody> </table>

### 查看日志

`worker status INSTANCE_ID` 输出中包含日志路径。执行以下命令时，将 `LOG_PATH` 替换为实际日志路径。

Linux/macOS：

```
HELPCODEESCAPE-bash
# 查看最近 200 行
tail -n 200 LOG_PATH

# 持续查看
tail -f LOG_PATH
```

Windows PowerShell：

```
HELPCODEESCAPE-powershell
# 查看最近 200 行
Get-Content -Path "LOG_PATH" -Tail 200

# 持续查看
Get-Content -Path "LOG_PATH" -Tail 200 -Wait
```

日志和排障反馈中不得包含 token 或完整启动命令。

## 断开、重连、迁移和删除
### 断开实例连接

```
HELPCODEESCAPE-bash
loongsuite-pilot worker disconnect INSTANCE_ID
```

执行后，实例停止运行，本机实例配置保留。通过 `worker status` 确认状态变为 `disabled`。

### 重新连接

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID
```

凭据失效或控制台已重新签发启动命令时，执行新命令更新连接。

### 修改工作目录

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID \
  --work-dir /new/absolute/path
```

修改后通过 `worker status` 核对 WorkDir，并在 Team 重新执行只读验证任务。重连时如需同时传入 `--` 后的运行时参数，整体替换规则见第 5.3 节。

### 删除本地实例

```
HELPCODEESCAPE-bash
loongsuite-pilot worker disconnect INSTANCE_ID
loongsuite-pilot worker delete INSTANCE_ID
```

删除前需等待实例停止。若提示进程仍在运行，再次查看状态，确认变为 `disabled` 后再删除。

删除本地实例不会删除控制台中的纳管 Agent。不再使用时，还需在控制台删除对应 Agent。

## 分步排障流程
### 检查 Pilot 服务

```
HELPCODEESCAPE-bash
loongsuite-pilot status
loongsuite-pilot info
```

* 服务未运行：执行 `loongsuite-pilot start`。

* 服务状态异常：确认没有正在执行的重要任务后，再执行 `loongsuite-pilot restart`。

* 版本或配置异常：重新执行控制台生成的 安装并配置 LoongSuite Pilot 命令。

重启 Pilot 会影响该机器上的全部本地纳管实例。

### 检查实例是否存在

```
HELPCODEESCAPE-bash
loongsuite-pilot worker list
```

未显示目标实例时，重新生成并完整执行启动命令。

### 检查实例状态

```
HELPCODEESCAPE-bash
loongsuite-pilot worker status INSTANCE_ID
```

重点检查：

* `State`：当前状态。

* `Reason` 和 `Message`：失败原因。

* `WorkDir`：工作目录。

* `Worker` 和 `Team`：Agent 与 Team。

* `Heartbeat`：最近心跳。

* `Log`：日志路径。

### 检查运行时

在目标机器终端直接执行所选运行时命令，确认：

* 命令可被找到。

* 账号登录有效。

* 本地模型配置可用。

* 当前账号能够访问工作目录。

运行时命令不在 PATH 中时，按第 9.7 节查找命令，并按第 9.8 节使用命令路径参数指定绝对路径。

### 检查网络

* 确认启动命令选择的内网或公网方式与运行机器网络一致。

* 确认运行机器可访问 AgentCore、模型和 MCP 服务。

* 控制台显示已连接但 Trace 缺失时，重新执行控制台最新生成的完整安装配置命令，并检查对应网络连通性。

### 检查 Team 使用方式

* 确认 Agent 已加入目标 Team。

* Team 群聊或任务会话中已 @ 目标 Agent。

* 使用 `/stop` 或 `/clear` 时，控制命令单独发送。

* 任务长时间无进展时，先发送 `/stop`，再根据需要重新发起任务。

### 查找运行时命令

Pilot 提示运行时命令不存在时，先在目标机器上查找命令路径。

Linux/macOS：

```
HELPCODEESCAPE-bash
command -v claude
command -v codex
command -v openclaw
command -v qodercli
```

Windows PowerShell：

```
HELPCODEESCAPE-powershell
(Get-Command claude -ErrorAction SilentlyContinue).Source
(Get-Command codex -ErrorAction SilentlyContinue).Source
(Get-Command openclaw -ErrorAction SilentlyContinue).Source
(Get-Command qodercli -ErrorAction SilentlyContinue).Source
```

仅需执行实际使用的运行时命令。命令返回绝对路径表示已找到；无输出表示运行时未安装或未加入 PATH。

找到命令后，执行对应的版本命令确认其可正常启动：

```
HELPCODEESCAPE-bash
claude --version
codex --version
openclaw --version
qodercli --version
```

若命令存在但 Pilot 仍无法识别，将查询结果中的绝对路径配置到第 9.8 节对应的 `--*-command` 参数中。

### 指定运行时命令路径

Pilot 无法找到运行时命令时，可通过运行时参数指定绝对路径：
<table> <thead> <tr> <td><p><b>运行时</b></p></td> <td><p><b>参数</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Claude Code</p></td> <td><p><code>--claude-command /absolute/path/to/claude</code></p></td> </tr> <tr> <td><p>Codex</p></td> <td><p><code>--codex-command /absolute/path/to/codex</code></p></td> </tr> <tr> <td><p>OpenClaw</p></td> <td><p><code>--openclaw-command /absolute/path/to/openclaw</code></p></td> </tr> <tr> <td><p>Qoder CLI</p></td> <td><p><code>--qodercli-command /absolute/path/to/qodercli</code></p></td> </tr> </tbody> </table>

运行时参数应写在 `--` 分隔符之后。例如：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect INSTANCE_ID -- \
  --codex-command /absolute/path/to/codex
```

重连时，在 `--` 后传入的运行时参数会整体替换原有参数，规则详见第 5.3 节。

## 常见报错
<table> <thead> <tr> <td><p><b>报错或现象</b></p></td> <td><p><b>原因</b></p></td> <td><p><b>处理方法</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>--runtime is required</code></p></td> <td><p>首次连接命令缺少运行时</p></td> <td><p>重新生成并完整执行启动命令</p></td> </tr> <tr> <td><p><code>--bootstrap-token is required</code></p></td> <td><p>首次连接命令缺少凭据</p></td> <td><p>重新生成并完整执行启动命令</p></td> </tr> <tr> <td><p><code>invalid bootstrap token</code></p></td> <td><p>token 错误、过期或已失效</p></td> <td><p>重新生成启动命令，旧命令停止使用</p></td> </tr> <tr> <td><p><code>local worker not found</code></p></td> <td><p>实例 ID 不存在或本机未连接过该 Agent</p></td> <td><p>执行 <code>loongsuite-pilot worker list</code> 获取正确 ID；迁移机器时重新生成启动命令</p></td> </tr> <tr> <td><p><code>missing local worker runtime template</code></p></td> <td><p>Pilot 缺少所选运行时支持</p></td> <td><p>重新执行完整安装配置命令</p></td> </tr> <tr> <td><p>运行时命令未找到</p></td> <td><p>运行时未安装或不在 PATH</p></td> <td><p>按第 9.7 节查找命令；未安装时先安装运行时，已找到时按第 9.8 节指定绝对路径</p></td> </tr> <tr> <td><p>运行时版本低于最低要求</p></td> <td><p>本地运行时版本不兼容</p></td> <td><p>按第 1.4 节升级运行时，再重新连接</p></td> </tr> <tr> <td><p>控制台持续显示未连接</p></td> <td><p>Pilot、实例或网络异常</p></td> <td><p>按第 9 章依次检查服务、实例、状态、日志和网络</p></td> </tr> <tr> <td><p>Agent 启动后退出</p></td> <td><p>运行时启动失败或本地配置无效</p></td> <td><p>查看 Reason、Message 和日志，直接验证运行时命令</p></td> </tr> <tr> <td><p>平台模型调用失败</p></td> <td><p>模型连接配置不完整或不可用</p></td> <td><p>检查 Agent 模型配置，或切换为本地模型</p></td> </tr> <tr> <td><p>Qoder CLI 模型不符合预期</p></td> <td><p>本地模型配置或模型选择不正确</p></td> <td><p>检查 Qoder CLI 配置，或使用 <code>--qoder-model</code> 指定模型</p></td> </tr> <tr> <td><p>平台 Skill/MCP 不可用</p></td> <td><p>资源未分配或配置尚未生效</p></td> <td><p>检查 Agent 详情页配置并重新连接</p></td> </tr> <tr> <td><p>本地 Skill/MCP 不可用</p></td> <td><p>Pilot 或运行时组件过旧、未启用继承，或本地配置不可用</p></td> <td><p>执行 <code>loongsuite-pilot info</code>；重新执行当前启动命令后启用 <code>--inherit-local-resources true</code>，并检查本地配置和权限</p></td> </tr> <tr> <td><p>修改参数后其他参数失效</p></td> <td><p>重连时运行时参数被整体替换</p></td> <td><p>在 <code>--</code> 后完整传入所有需要保留的参数</p></td> </tr> <tr> <td><p><code>local worker must be disconnected before delete</code></p></td> <td><p>删除前未断开实例</p></td> <td><p>先执行 <code>loongsuite-pilot worker disconnect INSTANCE_ID</code>，状态变为 <code>disabled</code> 后再删除</p></td> </tr> <tr> <td><p><code>local worker is still running</code></p></td> <td><p>断开后进程尚未停止</p></td> <td><p>等待后重新查看状态，再执行删除</p></td> </tr> </tbody> </table>

## 使用与安全注意事项
* 同一纳管 Agent 不应同时启动多个本地副本。

* 迁移机器前必须先断开旧机器实例。

* 完整启动命令不得持久化或转发。

* 工作目录应遵循最小权限原则，不应直接设置为用户主目录或包含无关敏感文件的上级目录。

* 使用本地模型时，模型可用性、账号状态和额度由本地运行时负责。

* 使用平台模型时，应确认控制台模型连接和配额可用。

* 控制台配置更新需要一定生效时间；长时间未生效时，检查心跳和日志后重新连接。

* 本地 Skill/MCP 继承仅在业务需要且完成安全确认后启用。

* 删除本地实例前应保留仍需使用的任务文件和日志。

* **文件交付**：Agent 在本地生成的文件不会自动上传到 Team，交付方式见第 5.1 节。

## 命令速查
<table> <thead> <tr> <td><p><b>目标</b></p></td> <td><p><b>命令</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>查看 Pilot 服务状态</p></td> <td><p><code>loongsuite-pilot status</code></p></td> </tr> <tr> <td><p>查看 Pilot 版本和配置</p></td> <td><p><code>loongsuite-pilot info</code></p></td> </tr> <tr> <td><p>启动 Pilot</p></td> <td><p><code>loongsuite-pilot start</code></p></td> </tr> <tr> <td><p>重启 Pilot</p></td> <td><p><code>loongsuite-pilot restart</code></p></td> </tr> <tr> <td><p>查看实例列表</p></td> <td><p><code>loongsuite-pilot worker list</code></p></td> </tr> <tr> <td><p>查看实例详情</p></td> <td><p><code>loongsuite-pilot worker status INSTANCE_ID</code></p></td> </tr> <tr> <td><p>断开实例</p></td> <td><p><code>loongsuite-pilot worker disconnect INSTANCE_ID</code></p></td> </tr> <tr> <td><p>重新连接实例</p></td> <td><p><code>loongsuite-pilot worker connect INSTANCE_ID</code></p></td> </tr> <tr> <td><p>删除本地实例</p></td> <td><p><code>loongsuite-pilot worker delete INSTANCE_ID</code></p></td> </tr> <tr> <td><p>启用本地 Skill/MCP</p></td> <td><p><code>loongsuite-pilot worker connect INSTANCE_ID -- --inherit-local-resources true</code></p></td> </tr> <tr> <td><p>设置并发数</p></td> <td><p><code>loongsuite-pilot worker connect INSTANCE_ID -- --max-concurrent-tasks 3</code></p></td> </tr> </tbody> </table>

重连时，在 `--` 后传入的运行时参数会整体替换原有参数，规则详见第 5.3 节。

## 接入验收清单
* Team 协作已开启。

* Agent 已加入目标 Team。

* 模型来源和运行时选择正确。

* LoongSuite Pilot 和本地运行时满足第 1.4 节版本要求。

* 操作系统和访问网络选择正确。

* 已完整执行 Pilot 安装配置和 Agent 连接命令。

* Pilot 服务状态正常。

* 本地实例状态为 `running`。

* 控制台连接状态为 **已连接**。

* 工作目录符合任务范围。

* Team 会话中可以正常 @ Agent。

* Skill、MCP 和系统提示词符合预期。