---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-authentication-authentication
fetch_date: 2026-09-21
product: AI Gateway
slug: consumer-authentication-authentication
body_sha256: 4f14872bee1dde3dbbbc9cee54db785827dffdf60f30d99803a1263db41aa47b
body_bytes: 14876
migration_status: current
---

AI 网关支持全局认证和消费者鉴权，确保只有授权请求才能访问服务。本文介绍消费者在AI 网关中如何通过认证和鉴权确保安全访问资源。  

## 背景信息
相比全局认证鉴权适用于统一登录认证等ToC场景，API开启消费者认证，适用于授权API给合作伙伴等ToB场景。
<table> <thead> <tr> <td><p><b>对比项</b></p></td> <td><p><b>全局认证鉴权</b></p></td> <td><p><b>消费者鉴权</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>适用场景</b></p></td> <td><p>统一登录认证等ToC场景。</p></td> <td><p>授权API给合作伙伴等ToB场景。</p></td> </tr> <tr> <td><p><b>核心差异</b></p></td> <td><p>开启认证的同时也开启鉴权。</p></td> <td><p>开启认证后，需要额外做鉴权配置。</p></td> </tr> <tr> <td><p><b>配置入口</b></p></td> <td><p><span><b>实例</b> \&gt; <b>安全管理</b> \&gt; <b>全局认证鉴权</b></span>。</p></td> <td> <ol> <li><p><b>实例</b>\&gt;<b>Model API</b>\&gt;<b>消费者认证</b>。</p></li> <li><p><b>实例</b>\&gt;<b>MCP 管理</b>\&gt;<b>消费者认证</b></p></li> <li><p><b>消费者</b>\&gt;<b>消费者详情</b>\&gt;<b>消费者鉴权</b>。</p></li> </ol></td> </tr> <tr> <td><p><b>认证方式配置（以JWT认证为例）</b></p></td> <td> <ol> <li><p>创建配置时填写全局的<b>JWKS</b>配置。</p></li> <li><p>填写<code>issue</code>和<code>sub</code>字段作为识别JWT是否合法的依据。</p></li> </ol></td> <td> <ol> <li><p>创建消费者配置时填写该消费者对应的<b>JWKS</b>配置。</p></li> <li><p>填写消费者标识用于识别<b>JWT</b>是否为对应的消费者。默认为<code>payload</code>中的<code>uid</code>字段，可以自定义。</p></li> </ol></td> </tr> <tr> <td><p><b>鉴权方式配置</b></p></td> <td><p>创建配置时填写黑名单或白名单的<b>域名</b>和<b>路径（Path）</b>列表。</p> <ul> <li><p><b>黑名单模式</b>：名单中的<b>域名</b>和<b>路径（Path）</b>需要进行认证，其余无需认证可直接访问。</p></li> <li><p><b>白名单模式</b>：名单中的域名和<b>路径（Path）</b>不需要认证即可访问，其余需要进行认证。</p></li> </ul></td> <td> <ol> <li><p>在Model API和MCP管理中开启<b>认证</b>。</p></li> <li><p>在<b>消费者鉴权</b>中授权开启了认证的API，完成授权。</p></li> </ol></td> </tr> </tbody> </table>

## 注意事项
当用户在消费者认证中开启认证后，认证策略会即时生效，如果此时API已发布，但是又未给API配置消费者和授权规则，则默认会拒绝所有访问请求。

## 使用消费者认证鉴权
## JWT认证
### JWT认证流程概览：

1. 客户端向AI 网关发起认证请求，请求中一般会携带终端用户的用户名和密码。

2. 网关将请求直接转发给后端服务。

3. 后端服务读取请求中的验证信息（比如用户名、密码）进行验证，验证通过后使用私钥生成标准的Token，返回给网关。

4. 网关将携带Token的应答返回给客户端，客户端需要将这个Token缓存到本地。

5. 客户端向AI 网关发送业务请求，请求中携带Token。

6. 网关使用用户设定的公钥对请求中的Token进行验证，验证通过后，将请求透传给后端服务。

7. 后端服务进行业务处理后应答。

8. 网关将业务应答返回给客户端。

下文主要介绍生成Token、客户端向网关发送请求、网关使用设定的公钥进行Token验证的过程。

### 认证服务生成Token

下文将通过Java示例来说明Token的生成方式，其他语言您也可使用相关的工具生成密钥对。

1. 新建Maven项目并注入依赖。

   首先，新建一个Maven项目，注入如下依赖项：

   ```
   HELPCODEESCAPE-xml
   <dependency>
       <groupId>org.bitbucket.b_c</groupId>
       <artifactId>jose4j</artifactId>
       <version>0.7.0</version>
   </dependency>
   ```

2. 选择Token生成方式。

   您可以选择使用默认对称密钥示例生成Token和非对称密钥示例生成Token两种方式来生成Token。根据您的需求进行选择：

   ## 使用默认对称密钥示例生成Token
   --------------------

   代码示例：

   ```
   HELPCODEESCAPE-java
   package org.example;

   import java.io.UnsupportedEncodingException;
   import java.security.PrivateKey;

   import org.jose4j.base64url.Base64;
   import org.jose4j.json.JsonUtil;
   import org.jose4j.jwk.OctJwkGenerator;
   import org.jose4j.jwk.OctetSequenceJsonWebKey;
   import org.jose4j.jws.AlgorithmIdentifiers;
   import org.jose4j.jws.JsonWebSignature;
   import org.jose4j.jwt.JwtClaims;
   import org.jose4j.jwt.NumericDate;
   import org.jose4j.keys.HmacKey;
   import org.jose4j.lang.JoseException;
   import sun.lwawt.macosx.CSystemTray;

   public class Main {
       public static void main(String[] args) throws JoseException, UnsupportedEncodingException {
           //使用本文上述示例
           String privateKeyJson = "{\n"
                   + "    \"k\": \"VoBG-oyqVoyCr9G56ozmq8n_rlDDyYMQOd_DO4GOkEY\",\n"
                   + "    \"kty\": \"oct\",\n"
                   + "    \"alg\": \"HS256\",\n"
                   + "}";
           JwtClaims claims = new JwtClaims();
           claims.setGeneratedJwtId();
           claims.setIssuedAtToNow();
           //设置过期时间，并且小于7天
           NumericDate date = NumericDate.now();
           date.addSeconds(120*60);
           claims.setExpirationTime(date);
           claims.setNotBeforeMinutesInThePast(1);
           //添加自定义参数，所有值请都使用String类型
           //设置消费者标识
           claims.setClaim("uid", "11215ac069234abcb8944232b79ae711");
           JsonWebSignature jws = new JsonWebSignature();
           //设置加密算法
           jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.HMAC_SHA256);
           jws.setKey(new HmacKey(Base64.decode(JsonUtil.parseJson(privateKeyJson).get("k").toString())));
           jws.setPayload(claims.toJson());
           String jwtResult = jws.getCompactSerialization();
           System.out.println("Generate Json Web token , result is \n " + jwtResult);
       }
   }
   ```

   代码相关设置说明：
   * `privateKeyJson`：即在创建消费者时使用的JWKS，可以在创建消费者时记录下自己使用的JWKS，也可以在创建消费者后，在消费者基础配置页获取JWKS。

   * 设置消费者标识。即`claims.setClaim("uid", "11215ac069234abcb8944232b79ae711")`，该消费者标识为创建消费者时控制台默认生成，也可以根据自身逻辑进行修改。您也可以在创建消费者后，在消费者基础配置页获取消费者标识。

   * 设置加密算法。即`jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.HMAC_SHA256)`，该加密算法要和JWKS保持一致。

     **说明**

     目前支持的加密算法有ES256、ES384、ES512、RS256、RS384、RS512、PS256、PS384、PS512、HS256、HS384、HS512和EdDSA。

     使用对称加密的时，需要对"k"进行解码。

     ```
     HELPCODEESCAPE-java
     jws.setKey(new HmacKey(Base64.decode(JsonUtil.parseJson(privateKeyJson).get("k").toString())));
     ```

   <!-- -->

   * 设置过期时间。过期时间需要小于7天，超出过期时间后，请重新生成Token，以保证Token的安全性。

     ```
     HELPCODEESCAPE-java
     ...
         NumericDate date = NumericDate.now();
         date.addSeconds(120*60);
         claims.setExpirationTime(date);
         claims.setNotBeforeMinutesInThePast(1);
     ...
     ```

   * 根据自身业务需要，可以在JWKS的PAYLOAD中添加自定义参数。

   ## 使用非对称密钥示例生成Token
   -------------------

   代码示例：

   ```
   HELPCODEESCAPE-java
   package org.example;

   import java.io.UnsupportedEncodingException;
   import java.security.PrivateKey;

   import org.jose4j.base64url.Base64;
   import org.jose4j.json.JsonUtil;
   import org.jose4j.jwk.OctJwkGenerator;
   import org.jose4j.jwk.OctetSequenceJsonWebKey;
   import org.jose4j.jws.AlgorithmIdentifiers;
   import org.jose4j.jws.JsonWebSignature;
   import org.jose4j.jwt.JwtClaims;
   import org.jose4j.jwt.NumericDate;
   import org.jose4j.keys.HmacKey;
   import org.jose4j.lang.JoseException;
   import sun.lwawt.macosx.CSystemTray;

   public class Main {
       public static void main(String[] args) throws JoseException, UnsupportedEncodingException {
           //使用本文上述示例
           String privateKeyJson = "{\n"
                   + "    \"k\": \"VoBG-oyqVoyCr9G56ozmq8n_rlDDyYMQOd_DO4GOkEY\",\n"
                   + "    \"kty\": \"oct\",\n"
                   + "    \"alg\": \"HS256\",\n"
                   + "}";
           JwtClaims claims = new JwtClaims();
           claims.setGeneratedJwtId();
           claims.setIssuedAtToNow();
           //设置过期时间，并且小于7天
           NumericDate date = NumericDate.now();
           date.addSeconds(120*60);
           claims.setExpirationTime(date);
           claims.setNotBeforeMinutesInThePast(1);
           //添加自定义参数，所有值请都使用String类型
           //设置消费者标识
           claims.setClaim("uid", "11215ac069234abcb8944232b79ae711");
           JsonWebSignature jws = new JsonWebSignature();
           //设置加密算法
           jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.HMAC_SHA256);
           jws.setKey(new HmacKey(Base64.decode(JsonUtil.parseJson(privateKeyJson).get("k").toString())));
           jws.setPayload(claims.toJson());
           String jwtResult = jws.getCompactSerialization();
           System.out.println("Generate Json Web token , result is \n " + jwtResult);
       }
   }
   ```

   代码相关设置说明：
   * 设置`privateKeyJson`、消费者标识、过期时间，同对称加密算法。

     设置加密算法，即`jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256)`。该加密算法和JWKS保持一致。

     对于非对称加密算法，要用其私钥进行加密。

     ```
     HELPCODEESCAPE-java
     ...
         jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256);
         PrivateKey privateKey = new RsaJsonWebKey(JsonUtil.parseJson(privateKeyJson)).getPrivateKey();
         jws.setKey(privateKey);
     ...
     ```

   * 根据自身业务需要，可以在JWKS的`PAYLOAD`中添加自定义参数。

### 客户端向网关发送业务请求

目前AI 网关支持Header的模式传递Token，客户可以自定义请求Header的名字和Token的前缀，请求验证时必须与消费者认证方式配对的key和前缀保持一致。

* **请求不携带提供JWT，返回401。**

  ```
  HELPCODEESCAPE-plaintext
  curl  http://xxx.hello.com/test
  ```

* **请求携带错误JWT，返回401。**

  ```
  HELPCODEESCAPE-plaintext
  curl  http://xxx.hello.com/test -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJpc3MiOiJhYmNkIiwic3ViIjoidGVzdCIsImlhdCI6MTY2NTY2MDUyNywiZXhwIjoxODY1NjczODE5fQ.-vBSV0bKeDwQcuS6eeSZN9dLTUnSnZVk8eVCXdooCQ1'
  ```

* **请求携带JWT，但JWT代表的消费者无权访问API时，返回403。**

  ```
  HELPCODEESCAPE-plaintext
  # consumer1没有授权给下列路径指定api

  curl  'http://xxx.example.com/test' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJpc3MiOiJhYmNkIiwic3ViIjoidGVzdCIsImlhdCI6MTY2NTY2MDUyNywiZXhwIjoxODY1NjczODE5fQ.-vBSV0bKeDwQcuS6eeSZN9dLTUnSnZVk8eVCXdooCQ4'
  ```

### 服务端验证Token请求

服务端验证Token主要分为以下三步：

1. 服务端收到用户请求时，先检查是否携带Token，未携带Token的请求，直接拒绝，返回401。

2. 携带Token的请求，使用用户jwks中配置的私钥验证Token是否合法且有效，不合法或者失效，直接拒绝，返回401。

3. 如果Token合法且有效后，再校验其代表的消费者是否授权给正在访问的API。

### 常见错误码说明

<table> <thead> <tr> <td><p><b>HTTP 状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>Jwt missing</p></td> <td><p>请求头未提供JWT</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Jwt expired</p></td> <td><p>JWT已经过期</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Jwt verification fails</p></td> <td><p>JWT payload校验失败，如iss不匹配</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Access Denied</p></td> <td><p>无权限访问当前API</p></td> </tr> </tbody> </table>

## API Key认证
**说明**

* 如果Model API未开启消费者认证鉴权策略，可直接访问。

* 如果Model API已开启消费者认证鉴权策略，但未授权，则提示401。

调试和调用类似，本文以调试Model API为例。

API Key的凭证来源主要有三类：

1. 默认凭证来源：Authorization: \<Bearer\> Token。

2. 自定义Header，填写Header参数名。

3. 自定义Query参数，填写query参数名。

### 默认凭证来源

在调试Model API时，您可以通过在调试页面的HTTP请求头中设置API Key，以确保请求的身份验证。具体步骤如下：

1. 在Authorization字段中，将Bearer作为前缀。

2. 确保在Bearer和API Key之间留一个空格。

### 自定义Header

除了标准的请求头，您还可以定义自定义HTTP请求头来传递特定信息。

### 自定义Query参数

在请求URL中，您还可以通过增加自定义Query参数来传递额外的信息或配置。

### 相关错误码

<table> <thead> <tr> <td><p><b>HTTP 状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>Request denied by Key Auth check. Muti API key found in request.</p></td> <td><p>请求提供多个 API Key。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Request denied by Key Auth check. No API key found in request.</p></td> <td><p>请求未提供 API Key。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Request denied by Key Auth check. Invalid API key.</p></td> <td><p>不允许当前 API Key 访问。</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Request denied by Key Auth check. Unauthorized consumer.</p></td> <td><p>请求的调用方无访问权限。</p></td> </tr> </tbody> </table>

## 相关文档
您可以对API进行授权和管理，具体操作，请参见[授权管理](https://help.aliyun.com/document_detail/2880008.html)。