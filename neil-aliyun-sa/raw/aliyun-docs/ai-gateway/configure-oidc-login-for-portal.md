---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-oidc-login-for-portal
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-oidc-login-for-portal
body_sha256: 3c19a637eeea9c7a43d0deb18fa5575cca6edc1f11b91b8d45337bd57b31fb5d
body_bytes: 4869
migration_status: current
---

企业用户使用内部统一账号体系直接登录开发者门户。通过配置 OIDC（OpenID Connect）协议对接企业身份提供商，可实现企业级单点登录，用户无需额外注册。  

## OIDC 概述
OIDC（OpenID Connect）是一种基于 OAuth 2.0 协议的身份认证标准。开放平台通过标准的 OIDC 授权码流程与企业身份提供商对接，企业员工可使用内部统一账号直接登录开发者门户，无需单独注册。

目前支持的登录特性包括：

* **授权码模式**：采用标准的 OAuth2 Authorization Code 授权流程，安全可靠。

* **自动用户创建**：企业用户首次登录时，系统会自动创建对应的开发者账号，无需手动注册。

* **身份映射**：支持从 ID Token 中灵活映射用户标识、显示名称、邮箱等用户属性。

## 配置 OIDC 登录
### 进入安全设置

1. 登录开放平台控制台。

2. 在左侧导航栏进入 **门户管理** 菜单，查看门户列表。

3. 在列表中找到要配置的目标门户，点击该门户卡片进入详情页。

4. 在门户详情页中切换到 **安全设置** 标签页。

### 启用 OIDC 登录

1. 在安全设置页面的 **第三方认证** 区域中，添加 OIDC 登录配置。

2. 按照下表填写 OIDC 配置信息：

   <table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>提供商标识</p></td> <td><p>身份提供商的唯一标识，用于区分不同的 IdP（例如 <code>aliyun</code>）。</p></td> </tr> <tr> <td><p>显示名称</p></td> <td><p>在开发者门户登录页面上展示的登录按钮名称（例如 <code>阿里云账号登录</code>）。</p></td> </tr> <tr> <td><p>启用状态</p></td> <td><p>控制该登录方式是否在当前门户启用。</p></td> </tr> <tr> <td><p>Client ID</p></td> <td><p>在 IdP 注册应用后获取的客户端标识。</p></td> </tr> <tr> <td><p>Client Secret</p></td> <td><p>在 IdP 注册应用后获取的客户端密钥。</p></td> </tr> <tr> <td><p>授权范围</p></td> <td><p>OIDC 授权请求的范围，例如 <code>openid profile email</code>。</p></td> </tr> <tr> <td><p>Issuer</p></td> <td><p>IdP 的 Issuer URL（例如 <code>https://idp.example.com</code>），用于自动发现端点。</p></td> </tr> <tr> <td><p>授权端点（authorization 端点）</p></td> <td><p>IdP 的授权端点地址。</p></td> </tr> <tr> <td><p>令牌端点（token 端点）</p></td> <td><p>用于换取访问令牌和 ID Token 的端点地址。</p></td> </tr> <tr> <td><p>用户信息端点（userinfo 端点）</p></td> <td><p>用于获取用户详细信息的端点地址。</p></td> </tr> <tr> <td><p>公钥端点（jwks 端点）</p></td> <td><p>IdP 的公钥集地址，用于验证 ID Token 的签名。</p></td> </tr> </tbody> </table>

**说明**

如果已填写 **Issuer** 地址，系统会自动请求 `{issuer}/.well-known/openid-configuration` 端点获取 IdP 的元数据信息，并自动填充授权端点、令牌端点和用户信息端点。如果 IdP 不支持自动发现协议，或需要手动指定端点地址，则需手动填写上述各端点。

### 配置身份映射

身份映射用于定义从 IdP 返回的 Claims 到开放平台用户属性的映射关系，系统会根据映射规则提取用户信息并创建开发者账号。
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>用户标识</p></td> <td><p><code>sub</code></p></td> <td><p>用户的唯一标识字段，用于关联外部身份。</p></td> </tr> <tr> <td><p>显示名称</p></td> <td><p><code>name</code></p></td> <td><p>用户的显示名称字段，作为开发者名称展示。</p></td> </tr> <tr> <td><p>邮箱</p></td> <td><p><code>email</code></p></td> <td><p>用户的邮箱地址字段，用于联系和通知。</p></td> </tr> </tbody> </table>  
**说明**

OIDC 配置确定后，系统会自动校验配置的有效性，如有问题会给出相应提示。

## IdP 配置
在身份提供商侧，将 **回调地址** 配置为：`{portal-address}/oidc/callback`，其中 `{portal-address}` 是访问门户的地址。

## 验证配置
完成配置后，可按以下步骤验证 OIDC 登录是否正常：

1. 打开开发者门户登录页面，确认已显示配置的 OIDC 登录按钮（显示名称与配置一致）。

2. 点击 OIDC 登录按钮，系统应跳转至 IdP 的授权页面。

3. 使用企业账号完成身份验证，系统应自动跳转回门户并完成登录。

4. 首次登录时，系统会自动创建对应的开发者账号，可查看账号信息确认身份映射是否正确。