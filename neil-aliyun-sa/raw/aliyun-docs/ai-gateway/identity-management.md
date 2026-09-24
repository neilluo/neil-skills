---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/security-and-compliance/identity-management
fetch_date: 2026-09-21
product: AI Gateway
slug: identity-management
body_sha256: d7e328e84192e76fb07d499109510c41604248803fb50abc8ef7cbc06eedb368
body_bytes: 4956
migration_status: current
---

为确保您的阿里云账号及云资源使用安全，如非必要都应避免直接使用阿里云账号（即主账号）来访问AI 网关。推荐的做法是使用RAM身份（即RAM用户和RAM角色）来访问AI 网关。  

## **RAM用户**
RAM用户需要由阿里云账号（即主账号）或拥有管理员权限的RAM用户、RAM角色来创建，且必须在获得授权后才能登录控制台或使用API访问阿里云账号下的资源。

对于RAM用户的使用，建议您：

* 使用阿里云账号创建一个RAM用户，并为RAM用户授予管理员权限，后续使用有管理员权限的RAM用户创建并管理其他RAM用户。

* 将人员用户和程序用户分离。

  创建RAM用户时，支持设置**控制台访问** 和**使用永久AccessKey访问**两种访问方式。

  控制台用户使用**账号和密码** 访问云产品控制台，API用户使用**访问密钥AK（AccessKey）**调用API访问云资源。建议您将两个不同的使用场景分离，避免误操作导致服务受到影响。对于通过控制台访问的用户，推荐为其开启MFA多因素认证。
* 按需为RAM用户分配最小权限。

  最小权限是指授予用户执行某项任务所需的权限，不授予其他无需用到的权限。最小授权可以避免用户操作权限过大，提高数据安全性，减少因权限滥用导致的安全风险。
* 不要把RAM用户的AccessKey ID和AccessKey Secret保存在工程代码中，否则可能导致AK泄露，威胁您账号下所有资源的安全。建议您使用STS或环境变量等方式获取访问授权。

* 满足条件时对RAM用户设置SSO单点登录功能，实现直接使用企业自有的身份登录并访问阿里云资源。

### RAM用户相关操作

* [RAM用户管理](https://help.aliyun.com/document_detail/122148.html)

* [AK安全方案](https://help.aliyun.com/document_detail/2391595.html)

* [RAM用户SSO管理](https://help.aliyun.com/document_detail/110499.html)

## RAM用户组
当您的阿里云账号下有多个RAM用户时，可以通过创建用户组对职责相同的RAM用户进行分组管理和批量授权，高效地管理RAM用户及其权限。

对于RAM用户组的使用，建议您：

* 在对RAM用户组授权时遵循最小权限策略原则。

* 在RAM用户职责发生变化时将其从不再归属的用户组中移除，避免权限滥用。

* 在某个用户组不再需要某些权限时移除用户组对应的权限。

### RAM用户组相关操作

* [RAM用户组](https://help.aliyun.com/document_detail/122150.html)

## RAM角色
RAM角色是一种RAM身份类型，可以被授予一组权限策略。与RAM用户不同，RAM角色没有长期身份凭证（登录密码或访问密钥），需要被一个可信实体扮演后才能使用。扮演成功后，可信实体将获得RAM角色的临时身份凭证，即安全令牌（STS Token），使用该安全令牌就能以RAM角色身份访问被授权的资源。

以下是使用RAM角色的安全建议：

* 创建RAM角色后，请勿随意变更RAM角色的可信实体。修改RAM角色信任策略中的可信实体，可能会导致原受信对象权限缺失，影响业务正常运行。也可能会因增加受信对象，带来过度授权的风险。特殊情况必须修改时请务必在测试账号充分测试，确保功能正常使用后，再应用到正式生产账号。

* 可信实体的RAM用户获得相关授权后即可以调用[AssumeRole - 获取扮演角色的临时身份凭证](https://help.aliyun.com/document_detail/371864.html)接口获取RAM角色的STS Token。STS Token自颁发后将在一段时间内有效，建议您设置合理的Token有效期，避免有效期过长带来安全风险。

  **说明**

  STS Token有效期的最大值为角色的最大会话时间。从安全的角度考虑，应将角色最大会话时间也设置在合理范围。
* 满足条件时对RAM角色设置SSO单点登录功能，实现直接使用企业自有的身份登录并访问阿里云资源。

### RAM角色相关操作

* [RAM角色管理](https://help.aliyun.com/document_detail/93689.html)

* [扮演RAM角色](https://help.aliyun.com/document_detail/116820.html)

* [设置RAM角色最大会话时间](https://help.aliyun.com/document_detail/166256.html)

* [角色SSO管理](https://help.aliyun.com/document_detail/110153.html)

## 身份管理相关文档
* [阿里云身份与权限](https://help.aliyun.com/document_detail/469087.html)

* [RAM基本概念](https://help.aliyun.com/document_detail/28628.html)

* [RAM相关使用限制](https://help.aliyun.com/document_detail/28753.html)

* [基于身份的策略](https://help.aliyun.com/document_detail/2796692.html)

* [AI网关系统权限策略参考](https://help.aliyun.com/document_detail/2883444.html)

* [AI网关自定义权限策略参考](https://help.aliyun.com/document_detail/2881273.html)

<br />

<br />