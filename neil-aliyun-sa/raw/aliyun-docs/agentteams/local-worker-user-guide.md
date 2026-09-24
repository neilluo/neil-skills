---
source_url: https://help.aliyun.com/zh/agentteams/local-worker-user-guide
fetch_date: 2026-09-20
product: AgentTeams
slug: local-worker-user-guide
body_sha256: f9cd226f515c1b8d846a77b7daf7520d6c7f27537aa731a5326bb178fe656341
body_bytes: 22855
migration_status: migrated-legacy
---

本文介绍如何在 [AgentTeams 控制台](https://agentteams.console.aliyun.com)创建并启动本地 Worker，如何选择模型和运行时，如何配置 LoongSuite Pilot，以及本地 Worker 启动失败时如何排查问题。  
本地 Worker 适合希望把 Agent 运行在自己机器或自有服务器上的场景。Worker 的配置由 AgentTeams 控制台统一管理，Worker 进程由本地的 LoongSuite Pilot 启动和守护。  
**重要**

安全提示：控制台生成的启动命令包含连接凭证和云监控 2.0 配置，属于敏感信息。请勿将启动命令、bootstrap token、云监控 license key 发送到公共群、代码仓库、Issue、日志系统或其他不可信位置。

## 前提条件
创建本地 Worker 前，确认已满足以下条件。
<table> <thead> <tr> <td><p><b>项目</b></p></td> <td><p><b>要求</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>AgentTeams 实例</p></td> <td><p>实例已创建完成，且已开通本地 Worker 能力。</p></td> </tr> <tr> <td><p>网络</p></td> <td><p>本地机器能够访问所选网络档位对应的云端服务。公网环境选择<b>公网访问</b>，同 VPC 或内网互通环境可选择<b>内网访问</b>。</p></td> </tr> <tr> <td><p>LoongSuite Pilot</p></td> <td><p>需使用 1.1.13 或以上版本。控制台生成的启动命令会自动安装和配置 LoongSuite Pilot；已有安装时，命令会复用或更新本地配置。可通过 <code>loongsuite-pilot status</code> 查看当前版本。</p></td> </tr> <tr> <td><p>本地运行时</p></td> <td><p>选择的运行时对应 CLI 需要在本机可用，例如 Claude Code、OpenClaw、Qoder CLI 或 Codex。</p></td> </tr> <tr> <td><p>本地模型配置</p></td> <td><p>如果选择<b>使用本地模型</b>，需要提前在对应运行时配置好可用模型和凭证。</p></td> </tr> </tbody> </table>

## 创建本地 Worker
### 进入 Worker 创建页

1. 登录 AgentTeams 控制台。

2. 进入目标实例。

3. 在左侧导航进入 **Worker 管理**。

4. 单击 **创建 Worker**。

5. 在创建方式中选择 **本地（模板创建）** 或 **本地（自定义）**。

两种方式的区别如下。
<table> <thead> <tr> <td><p><b>创建方式</b></p></td> <td><p><b>适用场景</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>本地（模板创建）</p></td> <td><p>复用已有 Worker 模板</p></td> <td><p>模板中的提示词、技能、上下文等配置由模板维护。模板创建的 Worker 不建议在详情页直接修改模板内容。</p></td> </tr> <tr> <td><p>本地（自定义）</p></td> <td><p>从零配置 Worker</p></td> <td><p>可以在控制台填写 Worker 的 Soul、Agents、技能等配置。</p></td> </tr> </tbody> </table>

如果从 Team 页面创建 Worker，可以选择绑定到当前 Team。绑定后，Worker 会加入对应 Team，并按 Team 成员身份工作。关于 Team 管理的详细说明，请参见[管理 Worker 和 Worker 团队](https://help.aliyun.com/document_detail/3040386.html)。

### 填写基本信息

创建本地 Worker 时，需要填写 Worker 名称，并根据创建方式选择模板或填写自定义配置。

本地 Worker 的运行进程在用户本地环境中启动，但 Worker 的配置仍由控制台下发。配置保存后，本地 Worker 通常会在约 1 分钟内感知并生效，具体时间取决于本地网络和进程状态。

### 选择模型配置

本地 Worker 支持两种模型配置方式。
<table> <thead> <tr> <td><p><b>模型配置</b></p></td> <td><p><b>含义</b></p></td> <td><p><b>适用场景</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>使用本地模型</p></td> <td><p>不在控制台选择云端模型，Worker 依赖本机运行时已有模型配置。</p></td> <td><p>本机已经配置好 Claude Code、OpenClaw、Qoder CLI 或 Codex 的模型。</p></td> </tr> <tr> <td><p>配置云端模型</p></td> <td><p>在控制台选择 AgentTeams 上的模型，本地 Worker 自动使用该模型配置。</p></td> <td><p>希望统一使用控制台管理的模型和 Token 配额。如需了解模型配置，请参见<a href="https://help.aliyun.com/document_detail/3040384.html">管理模型与供应商</a>。</p></td> </tr> </tbody> </table>

各运行时对模型配置方式的支持情况如下。
<table> <thead> <tr> <td><p><b>运行时</b></p></td> <td><p><b>使用本地模型</b></p></td> <td><p><b>配置云端模型</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Claude Code</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>云端模型模式下会自动应用控制台选择的模型配置。</p></td> </tr> <tr> <td><p>OpenClaw</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>可使用本地 OpenClaw 配置，也可使用控制台选择的云端模型。</p></td> </tr> <tr> <td><p>Codex</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>可使用本地 Codex 配置，也可使用控制台选择的云端模型。</p></td> </tr> <tr> <td><p>Qoder CLI</p></td> <td><p>支持</p></td> <td><p>暂不支持</p></td> <td><p>Qoder CLI 当前只能依赖本地 Qoder CLI 的模型配置。</p></td> </tr> </tbody> </table>

如果选择"使用本地模型"，控制台不会展示模型下拉框，也不会展示 Token 配额配置。请确保本地运行时本身可以正常调用模型。

## 生成并执行启动命令
创建本地 Worker 后，在 Worker 详情页打开**启动命令**，按页面指引生成启动命令。

### 选择网络访问方式

控制台会展示可用网络档位。
<table> <thead> <tr> <td><p><b>网络档位</b></p></td> <td><p><b>使用场景</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>公网访问</p></td> <td><p>本地机器不在实例 VPC 内，或需要通过公网访问 AgentTeams 服务。</p></td> </tr> <tr> <td><p>内网访问</p></td> <td><p>本地机器与实例在同一 VPC，或通过专线、VPN 等方式可访问实例内网地址。</p></td> </tr> </tbody> </table>

选择网络档位后，本地 Worker 通信和 Trace 数据上报都会使用对应网络路径。根据本地机器与实例之间的网络连通情况选择合适的档位。

### 选择运行时

启动命令阶段需要选择本地 Worker 使用的运行时。
<table> <thead> <tr> <td><p><b>运行时选项</b></p></td> <td><p><b>命令值</b></p></td> <td><p><b>本机依赖</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Claude Code</p></td> <td><p><code>claude-code</code></p></td> <td><p>本机已安装并可执行 Claude Code CLI。</p></td> </tr> <tr> <td><p>OpenClaw</p></td> <td><p><code>openclaw</code></p></td> <td><p>本机已安装并可执行 OpenClaw CLI。</p></td> </tr> <tr> <td><p>Qoder CLI</p></td> <td><p><code>qodercli</code></p></td> <td><p>本机已安装并可执行 Qoder CLI，且已配置本地模型。</p></td> </tr> <tr> <td><p>Codex</p></td> <td><p><code>codex</code></p></td> <td><p>本机已安装并可执行 Codex CLI。</p></td> </tr> </tbody> </table>

如果运行时命令不在常规 PATH 内，可以通过连接命令末尾的运行时参数指定命令路径。运行时参数需要放在 `--` 后面，例如：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect <id> -- --openclaw-command /path/to/openclaw
```

首次连接时也可以追加到控制台生成的 `worker connect` 命令后：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect \
  --runtime openclaw \
  --bootstrap-token '<bootstrap-token>' \
  -- --openclaw-command /path/to/openclaw
```

### 执行启动命令

控制台生成的启动命令通常分为两段。

第一段用于安装并配置 LoongSuite Pilot：

```
HELPCODEESCAPE-bash
curl -fsSL https://aliyun-observability-release-cn-shanghai.oss-cn-shanghai.aliyuncs.com/loongsuite-pilot/installer.sh -o /tmp/loongsuite-pilot-installer.sh && \
bash /tmp/loongsuite-pilot-installer.sh install \
  --collect-trace "true" \
  --cms-license-key '<license-key>' \
  --cms-endpoint '<cms-endpoint>' \
  --cms-workspace '<cms-workspace>' \
  --service-name-prefix 'agentteams-<instance-id>-worker'
```

第二段用于连接本地 Worker：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect \
  --runtime claude-code \
  --bootstrap-token '<bootstrap-token>'
```

通常情况下，直接复制控制台生成的完整命令执行即可。不要手动拆分或修改 token、云监控 2.0 endpoint、license key 等参数。

## LoongSuite Pilot 参数说明
控制台生成命令中的主要参数如下。
<table> <thead> <tr> <td><p>参数</p></td> <td><p>说明</p></td> <td><p>是否建议手动修改</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>--collect-trace</code></p></td> <td><p>是否开启 Trace 上报。控制台默认生成 <code>true</code>。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--cms-license-key</code></p></td> <td><p>控制台生成的云监控 2.0 Trace 上报 license key。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--cms-endpoint</code></p></td> <td><p>控制台生成的云监控 2.0 Trace 上报地址。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--cms-workspace</code></p></td> <td><p>AgentTeams 实例对应的云监控 2.0 工作空间。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--service-name-prefix</code></p></td> <td><p>Trace 上报使用的服务名前缀，由控制台按实例生成，用于仪表盘聚合展示。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--runtime</code></p></td> <td><p>本地 Worker 运行时，例如 <code>claude-code</code>、<code>openclaw</code>、<code>qodercli</code>、<code>codex</code>。</p></td> <td><p>可在控制台选择。</p></td> </tr> <tr> <td><p><code>--bootstrap-token</code></p></td> <td><p>本地 Worker 连接 AgentTeams 的启动凭证。</p></td> <td><p>不建议。</p></td> </tr> <tr> <td><p><code>--work-dir</code></p></td> <td><p>Worker 的本地工作目录。不传时使用执行命令时所在目录。</p></td> <td><p>可按需指定。</p></td> </tr> </tbody> </table>

其中，`--cms-license-key`、`--cms-endpoint`、`--cms-workspace` 和 `--service-name-prefix` 都由控制台生成，对应 AgentTeams 实例创建时为用户准备的云监控 2.0 工作空间。只有将 Trace 数据上报到该工作空间，AgentTeams 才能统计用户的 Trace 数据和 token 消耗，并在仪表盘中展示。

如果希望指定工作目录，可以执行：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect \
  --runtime claude-code \
  --bootstrap-token '<bootstrap-token>' \
  --work-dir /path/to/workdir
```

## 故障排查
本地 Worker 无法启动或无法回复消息时，按以下顺序排查。

### 确认 LoongSuite Pilot 运行状态

运行 `loongsuite-pilot status` 确认 LoongSuite Pilot 正在运行且版本为 1.1.13 或以上。如需查看更多信息，运行 `loongsuite-pilot info`。如果 LoongSuite Pilot 没有运行，执行以下命令重启：

```
HELPCODEESCAPE-bash
loongsuite-pilot restart
```

### 确认本地 Worker 连接状态

运行 `loongsuite-pilot worker list` 查看本地 Worker 列表。如果列表为空，说明连接命令可能没有执行成功，回到控制台重新复制启动命令执行。

对于列表中的目标 Worker，运行 `loongsuite-pilot worker status <id>` 查看详情，重点关注 `State`、`Worker`、`Team`、`Heartbeat` 和 `Log` 字段。

### 查看 Worker 日志

从 `worker status <id>` 输出中获取 `Log` 路径，查看日志：

```
HELPCODEESCAPE-bash
tail -n 200 <Log 路径>
```

持续观察日志：

```
HELPCODEESCAPE-bash
tail -f <Log 路径>
```

### 查看 Trace 上报情况

如果 Worker 可以回复消息，但云监控 2.0 中看不到 Trace，优先确认以下内容：

1. 是否使用控制台最新生成的启动命令。

2. 启动命令中 `--collect-trace` 是否为 `true`。

3. 启动命令中的云监控 2.0 参数是否完整。

4. 本地机器是否能够访问所选网络档位下的 Trace 上报地址。

排查时可以先查看 `worker status <id>` 输出中的日志路径，再通过日志确认是否存在 Trace 上报失败信息。

## 常见报错和处理方法
<table> <thead> <tr> <td><p><b>报错或现象</b></p></td> <td><p><b>可能原因</b></p></td> <td><p><b>处理方法</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>--runtime is required</code></p></td> <td><p>首次连接时没有指定运行时。</p></td> <td><p>使用控制台生成的完整命令，或补充 <code>--runtime claude-code/openclaw/qodercli/codex</code>。</p></td> </tr> <tr> <td><p><code>--bootstrap-token is required</code></p></td> <td><p>首次连接时没有传启动凭证。</p></td> <td><p>回到控制台重新生成启动命令。</p></td> </tr> <tr> <td><p><code>invalid bootstrap token</code> / <code>InvalidBootstrapToken</code></p></td> <td><p>token 被截断、复制错误、过期，或不是当前 Worker 的 token。</p></td> <td><p>在 Worker 详情页重新生成启动命令并执行。</p></td> </tr> <tr> <td><p><code>local worker not found: \&lt;id\&gt;</code></p></td> <td><p>指定的本地 Worker ID 不存在，或当前机器没有连接过该 Worker。</p></td> <td><p>执行 <code>loongsuite-pilot worker list</code> 获取正确 ID；如已迁移机器，使用控制台重新生成的启动命令连接。</p></td> </tr> <tr> <td><p><code>missing local worker runtime template</code></p></td> <td><p>本地 LoongSuite Pilot 缺少对应运行时支持，或版本过旧。</p></td> <td><p>重新执行控制台生成的安装命令，或更新 LoongSuite Pilot。</p></td> </tr> <tr> <td><p><code>Claude Code command not found</code></p></td> <td><p>本机找不到 Claude Code CLI。</p></td> <td><p>安装 Claude Code，确认命令已加入 PATH，或通过运行时参数指定命令路径。</p></td> </tr> <tr> <td><p><code>OpenClaw command not found</code></p></td> <td><p>本机找不到 OpenClaw CLI。</p></td> <td><p>安装 OpenClaw，确认命令已加入 PATH，或通过 <code>-- --openclaw-command /path/to/openclaw</code> 指定路径。</p></td> </tr> <tr> <td><p><code>QoderCLI command not found</code></p></td> <td><p>本机找不到 Qoder CLI。</p></td> <td><p>安装 Qoder CLI，确认命令已加入 PATH，或通过 <code>-- --qodercli-command /path/to/qodercli</code> 指定路径。</p></td> </tr> <tr> <td><p><code>Codex CLI command not found</code> / <code>CodexSpawnFailed</code></p></td> <td><p>本机找不到 Codex CLI，或 Codex CLI 无法启动。</p></td> <td><p>安装 Codex CLI，确认可在终端执行，或通过 <code>-- --codex-command /path/to/codex</code> 指定路径。</p></td> </tr> <tr> <td><p><code>ManagedRuntimeModelConfigMissing</code></p></td> <td><p>选择了云端模型，但模型配置不完整。</p></td> <td><p>回到控制台重新选择云端模型，或切换为<b>使用本地模型</b>。</p></td> </tr> <tr> <td><p><code>UnsupportedModelConfigMode</code></p></td> <td><p>当前运行时不支持所选模型模式。常见于 Qoder CLI 配置云端模型。</p></td> <td><p>Qoder CLI 选择<b>使用本地模型</b>；其他运行时确认控制台模型配置完整。</p></td> </tr> <tr> <td><p>日志提示消息通信凭证缺失</p></td> <td><p>Worker 未获取到云端通信凭证，或凭证已失效。</p></td> <td><p>重新生成启动命令并执行；如果仍失败，检查 Worker 是否已被删除。</p></td> </tr> <tr> <td><p>日志提示消息通信失败</p></td> <td><p>本地 Worker 与云端通信失败。</p></td> <td><p>检查网络档位选择是否正确；公网环境选择<b>公网访问</b>，内网环境确认网络连通。</p></td> </tr> <tr> <td><p>日志提示心跳或配置刷新失败</p></td> <td><p>本地 Worker 与云端控制服务通信失败。</p></td> <td><p>检查网络连通性；必要时重新生成启动命令。</p></td> </tr> <tr> <td><p><code>local worker must be disconnected before delete</code></p></td> <td><p>删除本地 Worker 前未停止连接。</p></td> <td><p>先执行 <code>loongsuite-pilot worker disconnect \&lt;id\&gt;</code>，待进程停止后再 delete。</p></td> </tr> <tr> <td><p><code>local worker is still running</code></p></td> <td><p>已请求停止，但 Worker 进程还未退出。</p></td> <td><p>等待几秒后再次执行 <code>worker status</code>；确认停止后再 delete。</p></td> </tr> </tbody> </table>

## 控制当前会话
本地 Worker 支持通过聊天窗口发送控制命令，用于处理任务卡住或需要清空上下文的场景。
<table> <thead> <tr> <td><p><b>命令</b></p></td> <td><p><b>效果</b></p></td> <td><p><b>是否清空上下文</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>/stop</code></p></td> <td><p>停止当前正在执行的任务，保留当前会话上下文。</p></td> <td><p>否</p></td> </tr> <tr> <td><p><code>/clear</code></p></td> <td><p>停止当前正在执行的任务，并清空当前会话上下文。下一条消息会开启新会话。</p></td> <td><p>是</p></td> </tr> </tbody> </table>

使用方式：

* Worker 个人会话内，直接发送 `/stop` 或 `/clear`。

* Team 会话内，需要 mention 对应 Worker，例如 `@worker-01 /stop` 或 `@worker-01 /clear`。

* 命令消息必须只包含控制命令，不要和普通任务内容混写。

如果只需要暂停当前卡住的执行，使用 `/stop`。如果希望丢弃历史上下文、重新开始一轮任务，使用 `/clear`。

## 配置任务并发度
本地 Worker 支持同时处理多个会话中的任务。默认并发度为 2，允许配置范围为 1 到 8。首次连接时，可以在控制台生成的 `worker connect` 命令末尾追加运行时参数：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect \
  --runtime claude-code \
  --bootstrap-token '<bootstrap-token>' \
  -- --max-concurrent-tasks 3
```

如果本地 Worker 已经创建，可以更新已有本地实例的运行时参数：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect <id> -- --max-concurrent-tasks 3
```

并发度只控制同一个本地 Worker 同时处理多少个会话中的任务。单个会话内的消息仍会按顺序处理。

## 停止、重连和清理本地 Worker
### 暂停连接

如果暂时不需要本地 Worker 工作，执行以下命令：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker disconnect <id>
```

执行后，本地 Worker 会停止运行，本地连接配置仍会保留。

### 重新连接

如果需要恢复同一个本地 Worker：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect <id>
```

如果控制台重新生成了启动命令，也可以用新 token 更新本地保存的凭证：

```
HELPCODEESCAPE-bash
loongsuite-pilot worker connect <id> --bootstrap-token '<new-bootstrap-token>'
```

### 删除本地数据

不再使用本地 Worker 时，可以删除本地连接数据。

```
HELPCODEESCAPE-bash
loongsuite-pilot worker disconnect <id>
loongsuite-pilot worker delete <id>
```

删除前确认不再需要该本地 Worker 的本地状态和运行日志。删除本地数据不会删除控制台上的 Worker；如果也不再需要云端 Worker 资源，在控制台删除 Worker。建议优先使用 `loongsuite-pilot worker delete <id>` 清理本地数据，不建议手动删除 LoongSuite Pilot 管理的数据。

## 使用注意事项
* 不要同时启动同一个 Worker 的两个副本。同一个 Worker 被多个本地进程同时连接，可能导致重复消费消息、重复回复或状态异常。

* 如果需要迁移到另一台机器，先在旧机器执行 `loongsuite-pilot worker disconnect <id>`，再在新机器执行控制台生成的启动命令。

* 不要把启动命令写入代码仓库、CI 日志、公开文档或聊天记录。命令中的 bootstrap token 和云监控 2.0 参数都属于敏感信息。

* 本地工作目录由用户自行管理。Worker 可能读写工作目录下的任务文件，选择合适的目录并做好权限控制。

* 选择**使用本地模型**时，模型可用性由本机运行时配置决定。控制台无法感知本机 API Key、模型额度或运行时登录状态。

* 选择**配置云端模型**时，模型调用会使用控制台配置的云端模型，适合统一审计、配额和模型管理。

* 模板创建的本地 Worker 会按模板内容工作。若需要大幅调整 Soul、Agents 或技能，修改模板或新建自定义 Worker。

* 修改控制台配置后，本地 Worker 需要一定时间拉取和应用新配置。若长时间未生效，可查看 `worker status` 的心跳时间和日志。

## 相关命令速查
<table> <thead> <tr> <td><p><b>目标</b></p></td> <td><p><b>命令</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>查看 Pilot 状态和版本</p></td> <td><p><code>loongsuite-pilot status</code></p></td> </tr> <tr> <td><p>查看 Pilot 信息</p></td> <td><p><code>loongsuite-pilot info</code></p></td> </tr> <tr> <td><p>重启 Pilot</p></td> <td><p><code>loongsuite-pilot restart</code></p></td> </tr> <tr> <td><p>查看本地 Worker 列表</p></td> <td><p><code>loongsuite-pilot worker list</code></p></td> </tr> <tr> <td><p>查看本地 Worker 详情</p></td> <td><p><code>loongsuite-pilot worker status \&lt;id\&gt;</code></p></td> </tr> <tr> <td><p>暂停本地 Worker</p></td> <td><p><code>loongsuite-pilot worker disconnect \&lt;id\&gt;</code></p></td> </tr> <tr> <td><p>重连本地 Worker</p></td> <td><p><code>loongsuite-pilot worker connect \&lt;id\&gt;</code></p></td> </tr> <tr> <td><p>删除本地 Worker 数据</p></td> <td><p><code>loongsuite-pilot worker delete \&lt;id\&gt;</code></p></td> </tr> <tr> <td><p>查看 Worker 日志</p></td> <td><p><code>tail -n 200 \&lt;worker status 输出中的 Log 路径\&gt;</code></p></td> </tr> <tr> <td><p>设置并发度</p></td> <td><p><code>loongsuite-pilot worker connect \&lt;id\&gt; -- --max-concurrent-tasks 3</code></p></td> </tr> </tbody> </table>

## 相关文档
* [管理 Worker 和 Worker 团队](https://help.aliyun.com/document_detail/3040386.html)：了解云端 Worker 的创建和管理，以及 Worker Team 的配置。