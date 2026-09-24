---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-jwt-authentication
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-jwt-authentication
body_sha256: 9aeb294ad3cba7d575bd2f5a13173625bb53842b34cda2878e6d7ee9376fb99e
body_bytes: 4407
migration_status: current
---

JSON Web Token (JWT) 用于在客户端和服务端之间以JSON对象的形式安全地传输信息。该信息可以被验证和信任，因为JWT可以使用HMAC算法、RSA或ECDSA的公钥/私钥对其进行签名。JWT认证可以在网关中验证身份并控制授权访问。  

## 前提条件
* 了解JWT基本标准。

* 了解AI 网关支持的集成方式：自主颁发Token（安全性有保障）和网关配置公钥对请求验签。

* 准备用于生成与验证Token的私钥与公钥。私钥用于授权服务的签发JWT；公钥配置在AI网关中，用于对请求验签。

## 背景信息
AI 网关致力于为云上用户提供体系化的安全解决方案，其中JWT认证能力是在Json Web Token这种结构化令牌的基础上实现了一套基于用户体系对用户的API（服务）进行授权访问的机制，满足用户个性化安全设置的需求。

**基于Token的认证**

AI 网关对外开放的API需要识别请求者的身份，并据此判断所请求的资源是否可以返回给请求者。Token就是一种用于身份验证的机制，基于这种机制，应用不需要在服务端保留用户的认证信息或者会话信息，可实现无状态、分布式的Web应用授权，为应用的扩展提供了便利。

**支持的接入集成方式**
![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9877627771/CAEQVRiBgMCIxZeXtBkiIDU0YmJlMjE3NDJmZDQyN2I5NTFlMzMyNDI0M2Q4MTRm5076932_20250427113032.403.svg)

## 创建鉴权
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**安全管理** \> **全局认证鉴权**。

5. 在**全局认证鉴权** 页面左上角，单击**创建鉴权** ，然后配置网关鉴权相关参数，最后单击**确定**。

   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>开启</b></p></td> <td><p>是否开启AI 网关鉴权。</p></td> </tr> <tr> <td><p><b>鉴权名称</b></p></td> <td><p>自定义AI 网关鉴权的名称。</p></td> </tr> <tr> <td><p><b>鉴权类型</b></p></td> <td><p>默认支持JWT认证方式。</p></td> </tr> <tr> <td><p><b>Issuer</b></p></td> <td><p>设置JWT Claims的Issuer，即签发人。</p></td> </tr> <tr> <td><p><b>Sub</b></p></td> <td><p>设置JWT claims的sub(subject)，即主体。</p></td> </tr> <tr> <td><p><b>JWKS</b></p></td> <td><p>设置JWT公钥，参考格式如下：</p><pre>HELPCODEESCAPE-plaintext<br>{<br> "keys":\[<br> {<br> "e":"AQAB",<br> "kid":"DHFbpoIUqrY8t2zpA2qXfCmr5VO5ZEr4RzHU_-envvQ",<br> "kty":"RSA",<br> "n":"xAE7eB6qugXyCAG3yhh7pkDkT65pHymX-<br>P7KfIupjf59vsdo91bSP9C8H07pSAGQO1MV_xFj9VswgsCg4R6otmg5PV2<br>He95lZdHtOcU5DXIg_pbhLdKXbi66Gl<br>VeK6ABZOUW3WYtnNHD-91gVuoeJT_DwtGGcp4ignkgXfkiEm4sw-<br>4sfb4qdt5oLbyVpmW6x9cfa7vs2WTfURiCrBoUqgBo_-4WTiULmmHSG<br>ZHOjzwa8WtrtOQGsAFjIbno85jp6MnGGGZ<br>PYZbDAa_b3y5u-YpW7ypZrvD8BgtKVjgtQgZhLAGezMt0ua3D<br>RrWnKqTZ0BJ_EyxOGuHJrLsn00fnMQ"<br> }<br> \]<br>}</pre></td> </tr> <tr> <td><p><b>JWT Token配置</b></p></td> <td><p>设置JWT Token配置信息。</p> <ul> <li><p><b>类型</b>：Token参数类型，默认Header。</p></li> <li><p><b>Key</b>：Token参数名称。</p></li> <li><p><b>前缀</b>：Token参数名的前缀。设置需要校验的Token参数信息，默认是以Bearer为前缀放在Authorization Header中，例如：<span><code>Authorization: Bearer token</code></span>。</p></li> <li><p><b>是否透传</b>：选中Token参数透传，表示透传此Token参数到后端服务。</p></li> </ul></td> </tr> <tr> <td><p><b>授权</b></p></td> <td><p>授权模式支持<b>白名单模式</b>和<b>黑名单模式</b>。</p> <ul> <li><p>白名单模式：白名单中的hosts+paths不需要校验即可访问，其余都需要校验。</p></li> <li><p>黑名单模式：黑名单中的hosts+paths需要校验，其余可直接访问。</p></li> </ul> <div> <p>单击<b>规则条件</b>，设置请求<b>域名</b>和<b>路径</b>。</p> <ul> <li><p>域名：请求访问的域名，即hosts。</p></li> <li><p>路径（Path）：请求访问的接口Path，即paths。</p></li> </ul> </div></td> </tr> </tbody> </table>