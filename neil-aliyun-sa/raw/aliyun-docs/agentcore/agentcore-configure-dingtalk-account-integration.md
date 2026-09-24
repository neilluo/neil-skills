---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-configure-dingtalk-account-integration
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-configure-dingtalk-account-integration
body_sha256: 53b23af2ab8c56a870788d22e15799086bea5c9896cc6002d84f6d728071b7f1
body_bytes: 6648
migration_status: current
---

通过钉钉账号集成，企业成员可以使用钉钉扫码登录 AgentCore，用户信息从钉钉通讯录自动同步。配置钉钉账号集成后，无需手动创建用户，即可实现成员统一认证和自动化用户管理。  

## 前提条件
* 已创建钉钉开放平台应用。后续钉钉侧操作（权限开通、安全设置、事件订阅、版本发布）都在该应用完成。

* 权限开通可能需要企业管理员审批。如需审批，请等待审批通过后再继续后续配置。

## 配置钉钉应用权限
在[钉钉](https://open.dingtalk.com/)应用配置权限，并且发布钉钉应用版本。**此步骤需要在 AgentCore 控制台上配置钉钉集成前完成。**

根据要启用的能力开通对应权限，权限缺失会导致登录失败或同步不生效：  
**重要**

目前，同步仅支持导入 30 人以内的成员。

* 仅使用钉钉登录：开通 `open_app_api_base` 和 `Contact.User.Read`。

* 需要通讯录同步：再开通 `qyapi_get_department_member`、`qyapi_get_department_list` 和 `qyapi_get_member`。

* 需要同步成员手机号：再开通 `qyapi_get_member_by_mobile` 和 `fieldMobile`。该项为可选，不开通时其余字段仍可正常同步。

<table> <thead> <tr> <td><p><b>权限信息</b></p></td> <td><p><b>权限点 code</b></p></td> <td><p><b>对应功能</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>获取钉钉开放接口用户访问凭证的基础权限</p></td> <td><p><code>open_app_api_base</code></p></td> <td><p>登录</p></td> </tr> <tr> <td><p>通讯录个人信息读权限</p></td> <td><p><code>Contact.User.Read</code></p></td> <td><p>登录</p></td> </tr> <tr> <td><p>通讯录部门成员读权限</p></td> <td><p><code>qyapi_get_department_member</code></p></td> <td><p>通讯录同步</p></td> </tr> <tr> <td><p>通讯录部门信息读权限</p></td> <td><p><code>qyapi_get_department_list</code></p></td> <td><p>通讯录同步</p></td> </tr> <tr> <td><p>成员信息读权限</p></td> <td><p><code>qyapi_get_member</code></p></td> <td><p>通讯录同步</p></td> </tr> <tr> <td><p>根据手机号获取成员基本信息权限</p></td> <td><p><code>qyapi_get_member_by_mobile</code></p></td> <td><p>通讯录同步（可选）</p></td> </tr> <tr> <td><p>企业员工手机号信息</p></td> <td><p><code>fieldMobile</code></p></td> <td><p>通讯录同步（可选）</p></td> </tr> </tbody> </table>

权限开通方法：

1. 在钉钉开放平台应用的左侧导航栏，选择**开发配置** \> **权限管理**。

2. 按上表逐项搜索权限名称或权限点 code 并开通。

3. 确认所开通权限的**状态** 列均显示为**已开通**。若某项权限显示需要审批，请等待企业管理员审批通过后再继续。

## 配置钉钉登录
1. 从钉钉应用中获取 CorpId、Client ID（原 AppKey）和 Client Secret（原 AppSecret）。

   * 在钉钉开放平台，进入已创建应用的配置页面，在应用的左侧导航栏选择**基础信息** \> **凭证与基础信息** ，记录 **Client ID** 和 **Client Secret**。

   * 获取企业 **CorpId** ：单击页面右上角的企业头像，在展开的企业信息卡片，单击 **CorpId** 将其复制。CorpId 是企业在钉钉的唯一标识，配置时不可省略。

2. 在 [AgentCore 控制台](https://agentcore.console.aliyun.com/) AgentCore 控制台 左侧，选择**账号集成** \> **钉钉**。

3. 将获取的 CorpId、Client ID 和 Client Secret 配置到 AgentCore 的**钉钉集成**页面。

4. 将 AgentCore 提供的**钉钉登录回调地址**配置到钉钉应用安全设置的重定向 URL 中。

   在应用的左侧导航栏，选择**开发配置** \> **安全设置** ，将**钉钉登录回调地址** 粘贴到**重定向 URL（回调域名）** 输入框，然后单击**保存**。若输入框已有其他地址，请勿覆盖，按输入框下方提示的分隔符追加。
5. 发布应用版本。钉钉开放平台中对权限、安全设置等的修改，需发布版本后才能生效。

   在应用的左侧导航栏，选择**应用发布** \> **版本管理与发布** ，创建并发布新版本。发布版本时，可用范围需要设置为**全体员工**。当前账号集成的钉钉应用最多支持 30 个用户，超出后账号集成将失败。

完成配置后，AgentCore 会在用户通过钉钉扫码登录时，自动从钉钉拉取用户信息并创建对应的账号。

## 配置钉钉通讯录同步
钉钉登录配置实现了用户登录时的账号自动创建。若需在组织架构变动时自动同步用户变更至 AgentCore（如成员增加、删除或展示名变更），需额外配置通讯录增量同步。

### 配置钉钉增量同步

增量同步依赖钉钉的事件订阅能力，配置需要在钉钉开放平台和 AgentCore 控制台之间交替完成。请严格遵循以下顺序：先在钉钉侧生成加密 aes_key 和签名 token 并复制，此时不要保存；将其填入 AgentCore 并保存后，再回到钉钉保存事件订阅配置。

1. 在钉钉开放平台应用的左侧导航栏，选择**开发配置** \> **事件订阅** ，进入钉钉应用的事件订阅配置。推送方式选择 **HTTP 推送**。钉钉页面默认推荐 Stream 模式，此处请勿选择。

2. 分别单击**加密 aes_key** 和**签名 token** 输入框右侧的**刷新** 按钮生成，单击眼睛图标显示后复制备用。此时先不要单击**保存**。

3. 勾选以下三种通讯录事件：

   * **通讯录用户增加**

   * **通讯录用户更改**

   * **通讯录用户离职**

4. 在 AgentCore 控制台左侧的**账号集成**页面，填写上一步获取的加密 aes_key 和签名 token，并保存。

5. 在**钉钉集成** 页面获取事件订阅回调地址，将该地址填写到钉钉事件订阅的**请求网址**，保存配置。

6. 发布钉钉应用版本。发布时，可用范围需要设置为**全体员工**，以免因应用可读取的通讯录范围不足导致成员同步不全。

## 验证钉钉登录与通讯录同步
1. 打开 AgentCore 的登录入口，选择 **Continue with dingtalk**。

2. 使用钉钉 App 扫描页面上的二维码完成认证。

3. 授权后登录成功并返回 AgentCore，进入 Web 聊天页面，表示钉钉登录配置已生效。

4. 如果已启用通讯录同步，在用户列表确认钉钉成员已同步。后续组织架构发生变化（成员增加、删除或展示名变更）时，用户变更会自动同步至 AgentCore。

<br />