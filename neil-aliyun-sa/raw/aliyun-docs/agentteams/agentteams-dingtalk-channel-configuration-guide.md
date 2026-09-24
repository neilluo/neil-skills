---
source_url: https://help.aliyun.com/zh/agentteams/agentteams-dingtalk-channel-configuration-guide
fetch_date: 2026-09-20
product: AgentTeams
slug: agentteams-dingtalk-channel-configuration-guide
body_sha256: 2ec427eb0d9036121caf09c08dd04f163cb06463dc0a6a207dbeee6230d93b97
body_bytes: 3791
migration_status: migrated-legacy
---

通过配置钉钉渠道，可将 AgentTeams 的 Worker 接入钉钉机器人。配置完成后，用户通过钉钉单聊或群聊向机器人发送消息，机器人将消息转发给对应的 Worker，并将 Worker 的回复返回到当前会话。配置流程包含以下五个步骤：  

## 一、创建钉钉应用
1. 登录[钉钉开发者平台](https://open.dingtalk.com/)，进入**开发者后台**。

2. 创建一个企业内部应用，用于接入 AgentTeams Worker。

<br />

## 二、添加和配置机器人
为已创建的钉钉应用添加机器人能力，并完成以下基础配置：

1. 申请添加机器人。申请成功后，在 **基础信息** \> **基础信息** \> **App Key \& Secret** 中，获取 `app_key（钉应用、机器人）` 和 `app_secret`，后续需要在 AgentTeams 控制台填写。

2. 在 **机器人** \> **基础信息** \> **消息接收模式** 中，选择 **Stream 模式**。

3. 在 **机器人** \> **可见性管理** \>**机器人当前可见性** 中，设置允许访问机器人的部门范围。

4. 在 **开发配置** \> **权限管理** \> **更多权限** 中，搜索并添加以下权限：

   * **互动卡片实例写权限**

   * **AI 卡片流式更新权限**

5. 在 **开发配置** \> **安全设置** \> **IP 白名单**，添加服务器出口 IP。

   **说明**

   服务器出口 IP 可以通过与 Worker 对话"告诉我你的公网IP"获取。

<br />

## 三、配置流式输出卡片（可选）
如果希望 Worker 的回复通过钉钉以流式方式逐步展示，需要额外完成流式输出卡片配置。不需要流式输出时，可跳过此步骤，直接进入 AgentTeams 控制台配置。

1. 在 **开发工具** \> **卡片搭建** 中，选择 **新建卡片**。

2. 卡片类型选择 **AI 卡片**。

3. 进入编辑界面后，先点击 **保存** 、再点击 **发布**。

   <br />

4. 发布完成后，从卡片列表获取 `TemplateId`，后续作为卡片 ID 填入 AgentTeams 控制台。

   <br />

## 四、在 AgentTeams 控制台启用钉钉渠道
完成钉钉侧的应用和机器人配置后，通过 AgentTeams 控制台为目标 Worker 启用钉钉渠道。

1. 登录 AgentTeams [控制台](https://mse.console.aliyun.com/#/magic-console/instances)。

2. 在左侧导航栏点击 **Worker 管理**，找到目标 Worker 并进入其详情页。

3. 进入 **Worker 访问设置**。

   <br />

   填写前序步骤获取到的配置：
   * `app_key（钉应用、机器人）`

   * `app_secret`

   * 如果启用流式输出，还需要填写卡片 ID `TemplateId`。

   如果页面中单独展示 Robot Code，可使用 `app_key（钉应用、机器人）` 作为 Robot Code。

## 五、验证配置
配置保存后，通过以下方式验证钉钉渠道是否配置成功：

* **单聊**：打开钉钉，搜索已配置的机器人名称，直接发起对话。

* **群聊** ：打开目标群聊，进入 **群设置** \> **群管理** \> **机器人** \> **添加机器人**，搜索并添加机器人后发起对话。

发送任意消息后，机器人应将 Worker 的回复返回到当前会话。如果未收到回复，检查以下配置：

* IP 白名单是否已添加正确的服务器出口 IP。

* `app_key` 和 `app_secret` 是否填写正确。

* 是否已添加 **互动卡片实例写权限** 和 **AI 卡片流式更新权限**。

## 安全注意事项
* `app_secret` 是应用密钥，仅通过 AgentTeams 控制台配置页填写，请勿写入文档、代码仓库或聊天记录。

* 群聊场景下，机器人被加入群后，群内所有成员均可能触发 Worker。建议仅向可信群开放机器人。

* 建议将机器人的可见范围设置为最小化，避免无关人员搜索到机器人。