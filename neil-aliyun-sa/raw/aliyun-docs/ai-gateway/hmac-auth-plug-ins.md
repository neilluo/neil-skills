---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/hmac-auth-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: hmac-auth-plug-ins
body_sha256: 22a895f41b7f83d769a56c9a73e925f01ac0bd1dd7dfab7e99d9d60d1b47ed7d
body_bytes: 13117
migration_status: current
---

hmac-auth插件实现了基于HMAC算法为HTTP请求生成不可伪造的签名，并基于签名实现身份认证和鉴权。本文介绍如何配置hmac-auth插件。  

## **插件类型**
认证鉴权。

## 配置字段
### 认证配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>consumers</b></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置服务的调用者，用于对请求进行认证。</p></td> </tr> <tr> <td><p><b>date_offset</b></p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>配置允许的客户端最大时间偏移，单位为秒。根据请求头<code>Date</code>解析客户端UTC时间，可用于避免请求重放。未配置时，不做校验。</p></td> </tr> <tr> <td><p><b>global_auth</b></p></td> <td><p>array of string</p></td> <td><p>选填（仅实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在实例级别配置，若配置为true，则全局生效认证机制；若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。</p></td> </tr> </tbody> </table>

子项`consumers`中每一项的配置字段说明如下。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>key</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置该consumer的访问凭证。</p></td> </tr> <tr> <td><p><b>secret</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置用于生成签名的secret。</p></td> </tr> <tr> <td><p><b>name</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置该consumer的名称。</p></td> </tr> </tbody> </table>

#### **鉴权配置（非必需）**

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>allow</b></p></td> <td><p>array of string</p></td> <td><p>选填（非实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在路由或域名等细粒度规则上配置，对于符合匹配条件的请求，配置允许访问的 consumer，从而实现细粒度的权限控制。</p></td> </tr> </tbody> </table>  
**重要**

* 在一个规则里，鉴权配置和认证配置不可同时存在。

* 对于通过认证鉴权的请求，请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。

## 配置示例
### 全局配置认证和路由粒度进行鉴权

以下配置将对网关特定路由或域名开启 Hmac Auth 认证和鉴权。注意`key`字段不能重复。

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
global_auth: false
consumers: 
- key: appKey-example-1
  secret: appSecret-example-1
  name: consumer-1
- key: appKey-example-2
  secret: appSecret-example-2
  name: consumer-2
```

`route-a`和`route-b`两个路由做如下插件配置：

```
HELPCODEESCAPE-yaml
allow:
- consumer1
```

在`*.example.com`和`test.com`两个域名做如下插件配置：

```
HELPCODEESCAPE-yaml
allow:
- consumer2
```

**说明**

* 此例指定的`route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将允许`name`为`consumer1`的调用者访问，其他调用者不允许访问。

* 此例指定的`*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将允许`name`为`consumer2`的调用者访问，其他调用者不被允许访问。

## 网关实例级别开启
```
HELPCODEESCAPE-yaml
global_auth: true
consumers: 
- key: appKey-example-1
  secret: appSecret-example-1
  name: consumer-1
- key: appKey-example-2
  secret: appSecret-example-2
  name: consumer-2
```

## 签名机制说明
### 配置准备

如上指引，在插件配置中配置生成和验证签名所需的凭证配置。

* key: 用于请求头`x-ca-key`中设置。

* secret: 用于生成请求签名。

### 客户端签名生成方式

#### 流程简介

客户端生成签名共分三步处理。

1. 从原始请求中提取关键数据，得到一个用来签名的字符串。

2. 使用加密算法和配置的`secret`对关键数据签名串进行加密处理，得到签名。

3. 将签名所相关的所有头加入到原始HTTP请求中，得到最终HTTP请求。

#### 签名串提取流程

客户端需要从HTTP请求中提取出关键数据，组合成一个签名串，生成的签名串的格式如下。

```
HELPCODEESCAPE-properties
HTTPMethod
Accept
Content-MD5
Content-Type
Date
Headers
PathAndParameters
```

以上7个字段构成整个签名串，字段之间使用\\n间隔，如果Headers为空，则不需要加\\n，其他字段如果为空都需要保留\\n。签名大小写敏感。

每个字段的提取规则如下。

* HTTPMethod：HTTP的方法，全部大写，比如POST。

* Accept：请求中的Accept头的值，可为空。建议显式设置 Accept Header。当 Accept 为空时，部分HTTP客户端会给Accept设置默认值为`*/*`，导致签名校验失败。

* Content-MD5：请求中的Content-MD5头的值可为空，只有在请求存在Body且Body为非Form形式时才计算Content-MD5头，下面是Java的Content-MD5值的参考计算方式。

  ```
  HELPCODEESCAPE-java
  String content-MD5 = Base64.encodeBase64(MD5(bodyStream.getbytes("UTF-8")));
  ```

* Content-Type：请求中的Content-Type头的值，可为空。

* Date：请求中的Date头的值，当未开启`date_offset`配置时，可为空，否则将用于时间偏移校验。

* Headers：您可以选取指定的Header参与签名，关于Header的签名串拼接方式有以下规则。

  * 参与签名计算的Header的Key按照字典排序后使用如下方式拼接。

    ```
    HELPCODEESCAPE-properties
    HeaderKey1 + ":" + HeaderValue1 + "\n"\+
    HeaderKey2 + ":" + HeaderValue2 + "\n"\+
    ...
    HeaderKeyN + ":" + HeaderValueN + "\n"
    ```

  * 某个Header的Value为空，则使用HeaderKey+":"+"\\n"参与签名，需要保留Key和英文冒号。

  * 所有参与签名的Header的Key的集合使用英文逗号分割放到Key为`X-Ca-Signature-Headers`的Header中。

  * 以下Header不参与Header签名计算：X-Ca-Signature、X-Ca-Signature-Headers、Accept、Content-MD5、Content-Type、Date。

* PathAndParameters: 这个字段包含Path、Query和Form中的所有参数，具体组织形式如下。

  ```
  HELPCODEESCAPE-properties
  Path + "?" + Key1 + "=" + Value1 + "&" + Key2 + "=" + Value2 + ... "&" + KeyN + "=" + ValueN
  ```

**说明**

* Query和Form参数对的Key按照字典排序后使用上面的方式拼接。

* Query和Form参数为空时，则直接使用Path，不需要添加。

* Query和Form存在数组参数时（Key相同，Value不同的参数） ，取第一个Value参与签名计算。

#### 签名串提取示例

初始的HTTP请求。

```
HELPCODEESCAPE-properties
POST /http2test/test?param1=test HTTP/1.1
host:api.aliyun.com
accept:application/json; charset=utf-8
ca_version:1
content-type:application/x-www-form-urlencoded; charset=utf-8
x-ca-timestamp:1525872629832
date:Wed, 09 May 2018 13:30:29 GMT+00:00
user-agent:ALIYUN-ANDROID-DEMO
x-ca-nonce:c9f15cbf-f4ac-4a6c-b54d-f51abf4b5b44
content-length:33
username=xiaoming&password=123456789
```

生成的正确签名串。

```
HELPCODEESCAPE-properties
POST
application/json; charset=utf-8
application/x-www-form-urlencoded; charset=utf-8
Wed, 09 May 2018 13:30:29 GMT+00:00
x-ca-key:203753385
x-ca-nonce:c9f15cbf-f4ac-4a6c-b54d-f51abf4b5b44
x-ca-signature-method:HmacSHA256
x-ca-timestamp:1525872629832
/http2test/test?param1=test&password=123456789&username=xiaoming
```

#### 签名计算流程

客户端从HTTP请求中提取出关键数据组装成签名串后，需要对签名串进行加密及编码处理，形成最终的签名。

具体的加密形式如下，其中`stringToSign`是提取出来的签名串，`secret`是插件配置中填写的，`sign`是最终生成的签名。

```
HELPCODEESCAPE-java
Mac hmacSha256 = Mac.getInstance("HmacSHA256");
byte[] secretBytes = secret.getBytes("UTF-8");
hmacSha256.init(new SecretKeySpec(secretBytes, 0, secretBytes.length, "HmacSHA256"));
byte[] result = hmacSha256.doFinal(stringToSign.getBytes("UTF-8"));
String sign = Base64.encodeBase64String(result);
```

将`stringToSign`使用UTF-8解码后得到Byte数组，然后使用加密算法对Byte数组进行加密，然后使用Base64算法进行编码，形成最终的签名。

#### 添加签名流程

客户端需要将以下四个Header放在HTTP请求中传输给云原生API网关，进行签名校验。

* x-ca-key：取值APP Key。必选。

* x-ca-signature-method：签名算法。取值HmacSHA256或者HmacSHA1，可选，默认值为HmacSHA256。

* x-ca-signature-headers：所有签名头的Key的集合。使用英文逗号分隔，可选。

* x-ca-signature：签名。必选。

下面是携带签名的整个HTTP请求的示例。

```
HELPCODEESCAPE-properties
POST /http2test/test?param1=test HTTP/1.1
host:api.aliyun.com
accept:application/json; charset=utf-8
ca_version:1
content-type:application/x-www-form-urlencoded; charset=utf-8
x-ca-timestamp:1525872629832
date:Wed, 09 May 2018 13:30:29 GMT+00:00
user-agent:ALIYUN-ANDROID-DEMO
x-ca-nonce:c9f15cbf-f4ac-4a6c-b54d-f51abf4b5b44
x-ca-key:203753385
x-ca-signature-method:HmacSHA256
x-ca-signature-headers:x-ca-timestamp,x-ca-key,x-ca-nonce,x-ca-signature-method
x-ca-signature:xfX+bZxY2yl7EB/qdoDy9v/uscw3Nnj1pgoU+Bm6xdM=
content-length:33
username=xiaoming&password=123456789
```

### 服务端签名验证方式

#### 流程简介

服务器验证客户端签名一共分四步处理。

1. 从接收到的请求中提取关键数据，得到一个用来签名的字符串。

2. 从接收到的请求中读取`key`，通过`key`查询到对应的`secret`。

3. 使用加密算法和`secret`对关键数据签名串进行加密处理，得到签名。

4. 从接收到的请求中读取客户端签名，对比服务器端签名和客户端签名的一致性。

#### **签名排错方法**

网关签名校验失败时，会将服务端的签名串（StringToSign）放到HTTP Response的Header中返回到客户端，Key为：X-Ca-Error-Message，您只需要将本地计算的签名串（StringToSign）与服务端返回的签名串进行对比即可找到问题。

如果服务端与客户端的StringToSign一致请检查用于签名计算的APP Secret是否正确。

因为HTTP Header中无法表示换行，因此StringToSign中的换行符都被替换成`#`，如下所示。

```
HELPCODEESCAPE-properties
X-Ca-Error-Message:  Server StringToSign:`GET#application/json##application/json##X-Ca-Key:200000#X-Ca-Timestamp:1589458000000#/app/v1/config/keys?keys=TEST`
```

## 相关错误码
<table> <thead> <tr> <td><p><b>HTTP状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>400</p></td> <td><p>Invalid Signature.</p></td> <td><p>请求头x-ca-signature签名串，与服务端计算得到签名不一致。</p></td> </tr> <tr> <td><p>400</p></td> <td><p>Invalid Content-MD5.</p></td> <td><p>请求头content-md5不正确。</p></td> </tr> <tr> <td><p>400</p></td> <td><p>Invalid Date.</p></td> <td><p>根据请求头date计算时间偏移超过配置的date_offset。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Invalid Key.</p></td> <td><p>请求头未提供x-ca-key，或者x-ca-key无效。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Empty Signature.</p></td> <td><p>请求头未提供x-ca-signature签名串。</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Unauthorized Consumer.</p></td> <td><p>请求的调用方无访问权限。</p></td> </tr> <tr> <td><p>413</p></td> <td><p>Request Body Too Large.</p></td> <td><p>请求Body超过限制大小：32MB。</p></td> </tr> <tr> <td><p>413</p></td> <td><p>Payload Too Large.</p></td> <td><p>请求Body超过全局配置DownstreamConnectionBufferLimits，请在参数配置页调高此项。</p></td> </tr> </tbody> </table>  
**说明**

注意谨慎调高`DownstreamConnectionBufferLimits`此参数配置，调高后网关内存使用将有显著增加。