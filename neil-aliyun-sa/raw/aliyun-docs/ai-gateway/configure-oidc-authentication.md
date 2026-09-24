---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-oidc-authentication
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-oidc-authentication
body_sha256: 77558ba3455917295d4dfe41eae4f6d66fc87f0ce3f84863838065b579630df9
body_bytes: 6367
migration_status: current
---

通过OIDC协议与企业的认证鉴权系统整合，可以实现对内部服务的统一认证和授权管理，避免了重复的对接工作，同时简化了认证流程。AI 网关提供了统一认证鉴权，加强了系统的安全性，并提供了更加灵活的安全策略配置。整合OIDC协议还能实现单点登录，您只需一次登录即可访问多个服务。  

## 前提条件
已创建统一的认证鉴权服务，且支持标准的OIDC（OpenID Connect）协议。

## 背景信息
网关作为外界访问内部服务的一个控制点，需要对外部的请求进行认证鉴权，确保内部服务的安全性。企业内一般会自建一套统一的认证鉴权体系，AI网关支持通过OIDC协议与自建的认证鉴权体系打通，支持对接入的内部服务做统一认证鉴权，避免每个服务都需要对接认证鉴权体系。

#### **基于OIDC认证**

OIDC（OpenID Connect）是一种安全认证机制，第三方应用连接到身份认证提供商（Identify Provider）获取用户信息，并把这些信息以安全可靠的方式返回给第三方应用。OIDC对OAuth2.0协议进行了扩展，通过扩展的ID Token字段，提供用户基础身份信息，ID Token使用JWT（JSON Web Token）格式进行封装，提供自包含性、防篡改机制，可以安全地传递给第三方应用程序并容易被验证。

假设有以下四个角色：

* 客户端：直接为用户提供服务。

* 认证服务：OpenID提供方，通常是指OpenID认证服务器，为第三方颁发用于认证的ID Token。

* 业务服务：提供业务服务。

* 用户：指资源持有者。

业务流程如下：

1. 客户端发送认证请求给认证服务。

2. 用户在认证页面进行授权确认（通过用户名和密码登录）。

3. 认证服务对认证请求进行验证，并返回Code给客户端。

4. 客户端向业务服务请求回调接口，请求中携带Code。

5. 业务服务请求认证服务颁发Token，请求中携带Code、Client ID、Client Secret。

6. 认证服务验证合法性，并返回ID Token。

7. 认证成功，业务服务返回ID Token给客户端。

8. 客户端向业务请求，请求中携带ID Token。

9. 业务服务验证ID Token是否合法，然后返回业务应答。

#### **AI网关OIDC认证流程**

在上述OIDC认证流程中，如果有不同的业务服务，例如用户服务、订单服务等，则每个业务服务都需要实现认证鉴权逻辑，包括校验请求是否合法、对接认证服务等。通过AI 网关的OIDC认证功能，可以实现在网关统一认证鉴权。

<br />

业务流程如下：

1. 客户端向网关申请认证。

2. 网关向认证服务申请认证。

3. 认证服务返回 Code 给网关。

4. 网关返回 Code 给客户端。

5. 客户端携带 Code 回调网关。

6. 网关向认证服务交换 Token。

7. 认证服务返回 ID Token 给网关。

8. 网关向客户端返回认证成功响应，并设置 Cookie。

9. 客户端携带 Cookie 发起业务请求，网关验证 Token。

10. 网关携带 ID Token 转发业务请求给业务服务。

11. 业务服务应答经网关返回客户端。

在整个认证鉴权过程中，AI 网关会验证请求是否合法。如果请求不合法，AI网关会重定向到用户登录页面，并能代理请求认证服务实现用户登录认证，实现业务服务对认证服务无感知。

## 创建认证鉴权规则
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**安全管理** \> **全局认证鉴权**。

5. 在页面左上角，单击**创建鉴权** 配置网关鉴权相关参数，然后单击**确定**。

   AI 网关OIDC认证鉴权参数说明如下。
   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>开启</b></p></td> <td><p>是否开启AI 网关鉴权。</p></td> </tr> <tr> <td><p><b>鉴权名称</b></p></td> <td><p>自定义AI 网关鉴权的名称。</p></td> </tr> <tr> <td><p><b>鉴权类型</b></p></td> <td><p>选择<b>OIDC</b>认证方式。</p></td> </tr> <tr> <td><p><b>域名</b></p></td> <td><p>鉴权规则生效的域名。</p></td> </tr> <tr> <td><p><b>Issuer</b></p></td> <td><p>设置认证服务的Issuer，即签发人。</p></td> </tr> <tr> <td><p><b>重定向URL</b></p></td> <td><p>输入授权成功后的重定向地址，需要与OIDC中配置的重定向地址保持一致。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p>格式为<code>http(s)://yourdomain/path</code>（地址中的path必须为 <code>/oauth2/callback</code>）</p> </div> </div></td> </tr> <tr> <td><p><b>Client ID</b></p></td> <td><p>输入服务注册的应用ID。</p></td> </tr> <tr> <td><p><b>Client Secret</b></p></td> <td><p>输入服务注册的应用Secret。</p></td> </tr> <tr> <td><p><b>Cookie Domain</b></p></td> <td><p>输入Cookie的域名，认证通过后会将Cookie发送到指定的域名，保持登录状态。例如：设置<code>Cookie-domain=a.example.com</code>，则Cookie会发送到域名a.example.com；设置<code>Cookie-domain=.example.com</code>，则Cookie会发送到example.com的所有子域名。</p></td> </tr> <tr> <td><p><b>Cookie Secret</b></p></td> <td><p>用于在创建Cookie时添加数字签名，确保其不会被非法篡改。</p></td> </tr> <tr> <td><p><b>Scope</b></p></td> <td><p>输入授权作用域，多个域值用英文分号（;）分隔。</p></td> </tr> <tr> <td><p><b>授权</b></p></td> <td><p>授权模式支持<b>白名单模式</b>和<b>黑名单模式</b>。</p> <ul> <li><p>白名单模式：白名单中的hosts+paths不需要校验即可访问，其余的都需要校验。</p></li> <li><p>黑名单模式：黑名单中的hosts+paths需要校验，其余可直接访问。</p></li> </ul> <div> <p>单击<b>规则条件</b>，设置请求域名和路径。</p> <ul> <li><p><b>域名</b>：请求访问的域名，即hosts。</p></li> <li><p><b>路径（Path）</b>：请求访问的接口路径，即paths。</p></li> </ul> </div></td> </tr> </tbody> </table>