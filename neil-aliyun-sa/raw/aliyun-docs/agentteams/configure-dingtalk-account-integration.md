---
source_url: https://help.aliyun.com/zh/agentteams/configure-dingtalk-account-integration
fetch_date: 2026-09-20
product: AgentTeams
slug: configure-dingtalk-account-integration
body_sha256: ecf6e1a82451023909dd658f46561b2d9cca4894fccac71272741fc35bd8aec4
body_bytes: 3245
migration_status: migrated-legacy
---

AgentTeams 支持通过钉钉账号集成实现企业成员使用钉钉扫码登录，并自动同步钉钉通讯录中的用户信息。配置钉钉账号集成后，可免去手动创建用户的操作，实现成员统一认证和自动化用户管理。  

## 配置钉钉应用权限
在[钉钉](https://open.dingtalk.com/)的应用中配置权限，并且发布钉钉应用版本。**此步骤需要在AgentTeams控制台上配置钉钉集成前完成。**
<table> <thead> <tr> <td><p><b>权限信息</b></p></td> <td><p><b>权限点 code</b></p></td> <td><p><b>对应功能</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>获取钉钉开放接口用户访问凭证的基础权限</p></td> <td><p>open_app_api_base</p></td> <td><p>登录</p></td> </tr> <tr> <td><p>通讯录个人信息读权限</p></td> <td><p>Contact.User.Read</p></td> <td><p>登录</p></td> </tr> <tr> <td><p>通讯录部门成员读权限</p></td> <td><p>qyapi_get_department_member</p></td> <td><p>同步用户信息</p></td> </tr> <tr> <td><p>通讯录部门信息读权限</p></td> <td><p>qyapi_get_department_list</p></td> <td><p>同步用户信息</p></td> </tr> <tr> <td><p>成员信息读权限</p></td> <td><p>qyapi_get_member</p></td> <td><p>同步用户信息</p></td> </tr> <tr> <td><p>根据手机号获取成员基本信息权限</p></td> <td><p>qyapi_get_member_by_mobile</p></td> <td><p>同步用户信息</p></td> </tr> <tr> <td><p>企业员工手机号信息</p></td> <td><p>fieldMobile</p></td> <td><p>同步用户信息</p></td> </tr> </tbody> </table>

## 配置钉钉登录
1. 从钉钉应用中获取 CorpId、AppKey 和 AppSecret。

2. 在[Agent Teams控制台](https://agentteams.console.aliyun.com/)中，选择左侧的**账号集成** \> **钉钉**。

3. 将获取的 CorpId、AppKey 和 AppSecret 配置在 AgentTeams 的**钉钉集成**页面中。

4. 将 AgentTeams 提供的**钉钉登录回调地址**配置到钉钉应用安全设置的重定向 URL 中。

5. 发布应用版本。

完成配置后，AgentTeams 会在用户通过钉钉扫码登录时，自动从钉钉拉取用户信息并创建对应的账号。

## 使用钉钉扫码登录 AgentTeams
1. AgentTeams会从钉钉拉取钉钉用户信息，并在AgentTeams创建对应的用户。

2. 选择**Continue with dingtalk**，使用钉钉扫码登录。授权后进入web聊天页面。

## 配置钉钉通讯录同步
钉钉登录配置实现了用户登录时的账号自动创建。若需在组织架构变动时自动同步用户变更至 AgentTeams（如成员增加、删除或展示名变更），需额外配置通讯录增量同步。

## 配置钉钉增量同步
1. 进入钉钉应用的事件订阅配置，选择 HTTP 推送。

2. 单击**刷新**按钮，生成 aes_key 和签名 token。

3. 勾选以下三种通讯录事件：

   * **通讯录用户增加**

   * **通讯录用户更改**

   * **通讯录用户离职**

4. 在 AgentTeams控制台左侧的**账号集成**页面填写对应的钉钉配置并保存。

5. 在钉钉集成页面获取事件订阅回调地址，将该地址填写在钉钉事件订阅的请求网址中并保存配置。

6. 发布钉钉应用版本。