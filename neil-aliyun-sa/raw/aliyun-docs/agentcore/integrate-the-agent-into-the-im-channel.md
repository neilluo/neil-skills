---
source_url: https://help.aliyun.com/zh/agentcore/integrate-the-agent-into-the-im-channel
fetch_date: 2026-09-20
product: AgentCore
slug: integrate-the-agent-into-the-im-channel
body_sha256: bb3298f78cdb61691e28838dd32c0db552382aff808668d982307cda399e9145
body_bytes: 9844
migration_status: current
---

通过配置 IM 渠道，可以将 AgentCore 中的 Agent 接入钉钉、飞书或企业微信机器人。配置完成后，用户通过单聊或群聊向机器人发送消息，机器人将消息转发给对应的 Agent，并把 Agent 的回复返回到当前会话。配置流程包含以下三个步骤：  
1. 在对应 IM 平台创建机器人并获取凭证。

2. 在 AgentCore 控制台配置 IM 渠道。

3. 通过 IM 会话验证机器人是否可以正常调用 Agent。

## 适用范围
* 已在 AgentCore 创建一个托管 Agent（Worker），且 Agent 已进入可运行状态。创建托管 Agent 时，系统会自动创建默认 ServiceEndpoint，无需手动开启 **直接访问** 或单独创建 Endpoint。

* Agent 的默认 ServiceEndpoint 处于 **READY** 状态，并支持公网访问。

* 当前 Workspace 处于可操作状态。Workspace 正在创建、更新或删除时，只能查看渠道，不能保存配置。

* 拥有对应 IM 平台的应用或机器人创建权限。

**说明**

IM 渠道目前用于接入托管 Agent。通过注册或本地纳管方式接入的 Agent，不展示 **外部渠道配置** 入口。

## 步骤一：在 IM 平台创建机器人并获取凭证
不同 IM 平台使用的机器人类型和凭证名称不同。请在对应平台完成应用或机器人创建，并妥善保存凭证，后续需要填写到 AgentCore 控制台。
<table> <thead> <tr> <td><p><b>IM 平台</b></p></td> <td><p><b>创建入口</b></p></td> <td><p><b>需要获取的凭证</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>钉钉</p></td> <td><p><a href="https://open-dev.dingtalk.com/">钉钉开放平台</a></p></td> <td><p>Client ID、Client Secret</p></td> </tr> <tr> <td><p>飞书</p></td> <td><p><a href="https://open.feishu.cn/page/launcher?from=backend_oneclick">飞书开放平台·一键创建智能体应用</a></p></td> <td><p>App ID、App Secret</p></td> </tr> <tr> <td><p>企业微信</p></td> <td><p><a href="https://work.weixin.qq.com/">企业微信管理后台</a></p></td> <td><p>Bot ID、Secret</p></td> </tr> </tbody> </table>

每个 Agent 在每个 IM 平台最多配置一个机器人渠道，可以分别为其配置钉钉、飞书和企业微信渠道。

配置机器人时，请开通卡片读写权限。如果启用了 IP 白名单，还需将以下 IP 地址加入白名单：

```
HELPCODEESCAPE-plaintext
121.40.82.220
47.97.73.42
47.98.226.113
47.96.151.112
118.178.89.160
120.27.202.100
```

**重要**

不建议将同一组机器人凭证同时绑定到多个 Agent。如果提示凭证已被占用，请先将该渠道从原 Agent 解绑，再重新配置。

### 钉钉

推荐使用钉钉开放平台提供的一键创建入口。使用一键创建时，平台会预置机器人所需的基础配置；如果页面没有一键创建入口，也可以手动创建钉钉应用。

1. 登录钉钉开放平台，进入 **开发者后台**。

2. 选择 **应用开发** \> **钉钉应用**。

3. 在应用创建页面单击 **一键创建** ；如需手动创建，单击 **立即创建**。

4. 填写智能体应用名称，完成应用创建。

5. 在应用凭证页面复制 **Client ID** 和 **Client Secret**。

6. 按钉钉开放平台提示设置机器人的可见范围，并完成应用发布。

### 飞书

推荐使用飞书开放平台提供的智能体应用一键创建入口。使用一键创建时，平台会预置机器人所需的基础能力。

1. 登录飞书开放平台，使用智能体应用一键创建入口；也可以在开发者后台手动创建企业自建应用。

2. 填写智能体应用名称，完成应用创建。

3. 在 **凭证与基础信息** 页面复制 **App ID** 和 **App Secret**。

4. 按飞书开放平台提示配置机器人的可用范围，并发布应用版本。

### 企业微信

1. 登录企业微信管理后台。

2. 选择 **安全与管理** \> **管理与工具** \> **智能机器人** ，单击 **创建机器人**。

3. 选择 **手动创建** ，并使用 **API 模式** 创建。

4. 设置机器人的可见范围，将连接方式设置为 **长连接**。

5. 按页面提示获取 Secret、完成授权并保存机器人。

6. 从机器人配置详情复制 **Bot ID** 和 **Secret**。

## 步骤二：在 AgentCore 控制台配置 IM 渠道
完成机器人创建后，将机器人凭证配置到目标 Agent。

1. 登录 AgentCore 控制台。

2. 进入目标 Workspace，在 **我的 Agent** 找到目标 Agent，并进入其详情页。

3. 选择 **外部渠道配置** 页签。

4. 单击需要配置的渠道卡片：**钉钉** 、**飞书** 或**企业微信**。

5. 在 **应用配置** 区域完成以下配置：

   * 打开 **启用渠道** 开关。

   * **ServiceEndpoint**：选择系统为当前 Agent 自动创建的默认 Endpoint。

6. 在 **渠道凭证** 区域填写机器人凭证。

   <table> <thead> <tr> <td><p><b>渠道</b></p></td> <td><p><b>AgentCore 表单字段</b></p></td> <td><p><b>填写内容</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>钉钉</p></td> <td><p>Client ID、Client Secret</p></td> <td><p>钉钉应用凭证页面获取的 Client ID 和 Client Secret</p></td> </tr> <tr> <td><p>飞书</p></td> <td><p>App ID、App Secret</p></td> <td><p>飞书应用 <b>凭证与基础信息</b> 页面获取的 App ID 和 App Secret</p></td> </tr> <tr> <td><p>企业微信</p></td> <td><p>Bot ID、Secret</p></td> <td><p>企业微信智能机器人配置详情中获取的 Bot ID 和 Secret</p></td> </tr> </tbody> </table>
7. 在 **显示配置** 区域按需设置以下选项：

   * **显示思考过程**：渠道回复中展示 Agent 的思考内容。默认关闭。

   * **显示工具调用**：渠道回复中展示工具调用信息。默认关闭。

8. 单击 **保存** ，等待渠道状态变为 **已开启**。

**重要**

保存后，渠道可能短暂显示 **创建中** 或**更新中**。此时请等待状态自动刷新，不要重复提交。

## 步骤三：验证配置
渠道状态变为 **已开启** 后，可以通过以下方式验证：

1. 将机器人添加到一个测试群，并确认测试账号处于机器人的可见范围内。

2. 群聊中 `@机器人`，发送一条不依赖外部工具的测试消息，例如：

   ```
   HELPCODEESCAPE-plaintext
   请只回复：AgentCore IM 渠道连接成功
   ```

3. 机器人应将 Agent 的回复返回到当前群聊。

4. 如果对应 IM 平台支持机器人单聊，也可以搜索机器人名称并发起单聊测试。

如果机器人没有回复，请依次检查：

* Agent 是否处于可运行状态。

* 渠道状态是否为 **已开启** ，而不是 **已停用** 、**创建中** 或**配置失败**。

* 绑定的 ServiceEndpoint 是否仍为 **READY**，并支持公网访问。

* 机器人应用是否已发布，测试账号或测试群是否在可见范围内。

* 群聊中是否已正确 `@机器人`。

* 填写的 ID 和 Secret 是否来自同一个机器人应用。

## 管理已有渠道
### 停用和重新启用渠道

关闭 **启用渠道** 开关并保存后，渠道状态变为 **已停用**。停用不会删除已有配置，后续可以重新打开开关并保存。

### 修改机器人凭证

* Secret 不会在控制台回显。编辑已有渠道时，Secret 留空表示保留当前值。

* 修改 Client ID、App ID 或 Bot ID 时，必须同时重新输入对应的 Secret。

### 解绑渠道

单击 **解绑** 并确认后，系统会彻底删除当前渠道配置并释放机器人凭证。解绑与停用不同：

* **停用**：保留配置，可以随时重新启用。

* **解绑**：删除配置；再次使用时需要重新选择默认 Endpoint 并填写完整凭证。

渠道处于 **创建中** 、**更新中** 或**删除中** 时，不能执行解绑。如果渠道显示 **配置失败**，请解绑后重新配置。

## 渠道状态说明
<table> <thead> <tr> <td><p><b>状态</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>建议操作</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>未配置</b></p></td> <td><p>当前 Agent 尚未创建该类型的渠道</p></td> <td><p>进入渠道页面完成配置</p></td> </tr> <tr> <td><p><b>已开启</b></p></td> <td><p>渠道配置完成且已启用</p></td> <td><p>通过 IM 验证机器人</p></td> </tr> <tr> <td><p><b>已停用</b></p></td> <td><p>配置仍保留，但机器人不会转发消息</p></td> <td><p>按需重新启用</p></td> </tr> <tr> <td><p><b>创建中</b>、<b>更新中</b>或<b>删除中</b></p></td> <td><p>系统正在处理渠道配置</p></td> <td><p>等待状态自动刷新，不要重复操作</p></td> </tr> <tr> <td><p><b>配置失败</b></p></td> <td><p>渠道创建或更新未完成</p></td> <td><p>查看页面提示，解绑后重新配置</p></td> </tr> <tr> <td><p><b>删除失败</b></p></td> <td><p>上次解绑未完成</p></td> <td><p>刷新状态后重新解绑</p></td> </tr> </tbody> </table>

## 安全注意事项
* Client Secret、App Secret 和 Secret 均属于敏感凭证。仅在 AgentCore 控制台配置页填写，不要写入文档、代码仓库或聊天记录。

* 机器人加入群聊后，群内可以 `@机器人` 的成员都可能调用该 Agent。请将机器人可见范围和群成员范围控制在最小必要范围内。

* IM 用户可以使用该 Agent 已配置的模型、Skill、MCP 工具和凭证能力。请按照最小权限原则配置 Agent，并仅将机器人加入可信群。

* **显示思考过程** 和 **显示工具调用** 可能暴露业务上下文或工具参数。非调试场景建议保持关闭。