---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-a-consumer
fetch_date: 2026-09-21
product: AI Gateway
slug: creating-a-consumer
body_sha256: 20594c597f4d69b6e14f0a4cb0f207372128c353afa155718a7c8901f15b7b12
body_bytes: 4132
migration_status: current
---

AI 网关通过消费者来为路由、API开启认证能力，本文介绍AI网关控制台如何管理消费者。  

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**消费者**，并在顶部菜单栏选择地域。

3. 在**消费者** 页面左上角，单击**创建消费者**。

4. 在**创建消费者** 页面，填写消费者名称，选择如下认证方式并单击**创建**。

   ## JWT认证
   --------

   配置参数说明如下：
   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>消费者名称</b></p> </td> <td> <p>自定义消费者的名称。</p> </td> </tr> <tr> <td> <p><b>状态</b></p> </td> <td> <p>消费者状态为<b>已启用</b>或<b>已停用</b>。创建完成消费者后您可以手动<b>启用</b>或<b>停用</b>。</p> </td> </tr> <tr> <td> <p><b>描述</b></p> </td> <td> <p>对消费者进行描述。</p> </td> </tr> <tr> <td> <p><b>认证方式</b></p> </td> <td> <p>当前消费者支持的认证方式，目前主要支持JWT和API Key两种认证方式。</p> </td> </tr> <tr> <td> <p><b>密钥类型</b></p> </td> <td> <ul> <li> <p><b>对称密钥</b>：生成一份默认的JWKS配置（每个消费者不同），包含加密或者解密Token时使用的密钥。</p> </li> <li> <p><b>非对称密钥</b>：需要您自己填写完整的JWKS配置，使用私钥加密Token。网关根据JWKS中配置的公钥进行解密。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>JWKS</b></p> </td> <td> <p>JWKS规范说明请参考<a href="https://datatracker.ietf.org/doc/html/rfc7517">JSON Web Key (JWK)</a>。</p> </td> </tr> <tr> <td> <p><b>JWKS Token 配置</b></p> </td> <td> <ul> <li> <p><b>类型</b>：Token参数类型，默认Header。</p> </li> <li> <p><b>Key</b>：Token参数名称。</p> </li> <li> <p><b>前缀</b>：Token参数名的前缀。设置需要校验的Token参数信息，默认是以<b>Bearer</b>为前缀放在<b>Authorization Header</b>中，例如<b>Authorization: Bearer token</b>。</p> </li> <li> <p><b>是否透传</b>：选中Token参数透传，表示透传此Token参数到后端服务。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>JWKS Payload 内消费者标识</b></p> </td> <td> <p>指定从JWKS Payload中的Key以及对应Value来识别为当前消费者。默认提供一对标识，Key为uid，Value为随机字符串，可自行修改。</p> <p>Payload配置示例如下所示：</p><pre>HELPCODEESCAPE-json<br>{<br> "uid": "11215ac069234abcb8944232b79ae711"<br>}</pre> </td> </tr> </tbody> </table>

   ## API Key认证
   ------------

   配置参数说明如下：
   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>消费者名称</b></p> </td> <td> <p>自定义消费者的名称。</p> </td> </tr> <tr> <td> <p><b>状态</b></p> </td> <td> <p>消费者状态为<b>已启用</b>或<b>已停用</b>。创建完成消费者后您可以手动<b>启用</b>或<b>停用</b>。</p> </td> </tr> <tr> <td> <p><b>描述</b></p> </td> <td> <p>对消费者进行描述。</p> </td> </tr> <tr> <td> <p><b>认证方式</b></p> </td> <td> <p>当前消费者支持的认证方式，目前主要支持JWT和API Key两种认证方式。</p> </td> </tr> <tr> <td> <p><b>生成方式</b></p> </td> <td> <ul> <li> <p><b>系统生成</b>：系统为您自动生成API Key凭证。</p> </li> <li> <p><b>自定义</b>：自定义API Key凭证及凭证来源。</p> </li> </ul> </td> </tr> <tr> <td> <p><b>凭证</b></p> </td> <td> <p>自定义API Key凭证。</p> </td> </tr> <tr> <td> <p><b>凭证来源</b></p> </td> <td> <p>凭证来源用于网关从请求的提取参数的位置和名称，支持如下：</p> <ul> <li> <p><b>Authorization: Bearer \&lt;token\&gt;</b></p> </li> <li> <p><b>自定义 HTTP Header</b></p> </li> <li> <p><b>自定义Query参数</b></p> </li> </ul> </td> </tr> </tbody> </table>