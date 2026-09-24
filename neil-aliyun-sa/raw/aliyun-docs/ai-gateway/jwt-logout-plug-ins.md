---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/jwt-logout-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: jwt-logout-plug-ins
body_sha256: d3d437b8702fabb67b22bbfde19bc83652dd74075c1fc02f31c54128ec47ecda
body_bytes: 17636
migration_status: current
---

jwt-logout插件利用Redis实现了对JWT的弱状态管理机制，解决了JWT本身无法主动登出的问题，并可用于实现唯一登录控制，例如在支持多设备登录场景下实现用户互踢功能。  

## 插件类型
认证鉴权。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>jwks</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>指定JSON字符串，用于验证JWT。当此插件搭配jwt-auth插件使用时，无需配置此项。更多信息，请参见<a href="https://www.rfc-editor.org/rfc/rfc7517">详情</a>。</p></td> </tr> <tr> <td><p>clock_skew</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>60</p></td> <td><p>校验JWT的exp和iat字段时，允许的时钟偏移量。单位为秒。</p></td> </tr> <tr> <td><p>token_header</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>Authorization</p></td> <td><p>抽取JWT的请求Header。</p></td> </tr> <tr> <td><p>token_prefix</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>"Bearer"</p></td> <td><p>将请求Header中Value值的指定前缀去除后，剩余部分将被用作JWT的内容。</p></td> </tr> <tr> <td><p>redis</p></td> <td><p>Redis</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>Redis服务配置信息。</p></td> </tr> <tr> <td><p>logout</p></td> <td><p>Logout</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>用于实现JWT登出功能的配置。不配置此字段时，该功能关闭。</p></td> </tr> <tr> <td><p>login</p></td> <td><p>Login</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>用于实现JWT唯一登录的配置。不配置此字段时，该功能关闭。</p></td> </tr> </tbody> </table>

Redis类型的配置字段说明如下：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>service</p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>Redis服务名称。例如：</p> <ul> <li><p>固定地址服务：my-redis.static。</p></li> <li><p>DNS域名服务：my-redis.dns。</p></li> <li><p>K8s容器服务：my-redis.default.svc.cluster.local。</p></li> </ul></td> </tr> <tr> <td><p>port</p></td> <td><p>number</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>Redis服务端口。</p></td> </tr> <tr> <td><p>username</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>Redis <a href="https://redis.io/commands/auth/">AUTH</a>命令使用的username。</p></td> </tr> <tr> <td><p>password</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>Redis <a href="https://redis.io/commands/auth/">AUTH</a>命令使用的password。</p></td> </tr> <tr> <td><p>timeout</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>1000</p></td> <td><p>Redis命令的超时时间。单位为毫秒。</p></td> </tr> </tbody> </table>

Logout类型的配置字段说明如下：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>key_prefix</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>higress_jwt_logout_</p></td> <td><p>Redis中存储Key的前缀。</p></td> </tr> <tr> <td><p>key</p></td> <td><p>array of string</p></td> <td><p>选填</p></td> <td><p>\["jti"\]</p></td> <td><p>指定JWT Payload中的字段标识JWT，携带相同字段的会被认作同一个JWT；若JWT Payload中不存在相应字段，将返回401 invalid token。</p></td> </tr> <tr> <td><p>path</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>/jwt_logout</p></td> <td><p>URL路径后缀匹配此字符串时，登出当前请求携带的JWT，该JWT此后将无法使用。</p></td> </tr> <tr> <td><p>error_status</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>401</p></td> <td><p>登出状态时的错误状态码。</p></td> </tr> <tr> <td><p>error_body</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>'{"message":"invalid token"}'</p></td> <td><p>登出状态时的响应Body。</p></td> </tr> <tr> <td><p>ttl</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>在Redis中，存储Key的ttl，以秒为单位。此配置确定了登出的JWT在多长时间内无法使用。若未填写此配置，将根据Payload中的exp减去当前时间来计算生存时间；若Payload中没有exp字段，则默认的ttl为86400秒（24小时）。</p></td> </tr> </tbody> </table>

Login类型的配置字段说明如下：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>key_prefix</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>higress_jwt_logout_</p></td> <td><p>Redis中存储key的前缀。</p></td> </tr> <tr> <td><p>key</p></td> <td><p>array of string</p></td> <td><p>选填</p></td> <td><p>\["iss","aud","sub"\]</p></td> <td><p>指定JWT Payload中的字段作为唯一登录标识。若携带相同字段但与已登录的JWT不完全相同，将被判断为重复登录并拒绝访问，直到已登录的JWT对应的key在Redis中过期；若JWT Payload中不存在相应字段，将返回401 invalid token。</p></td> </tr> <tr> <td><p>path</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>/jwt_login</p></td> <td><p>URL路径后缀匹配此字符串时，强制登录当前请求携带的JWT，已登录的相同Payload特征的JWT将被登出。</p></td> </tr> <tr> <td><p>error_status</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>403</p></td> <td><p>重复登录时的错误状态码。</p></td> </tr> <tr> <td><p>error_body</p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>'{"message":"already login on other device"}'</p></td> <td><p>重复登录时的响应Body。</p></td> </tr> <tr> <td><p>ttl</p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>在Redis中存储key的ttl，单位为秒，决定唯一登录的JWT在多久时间内有效。若未填写此配置，则基于Payload中的exp减去当前时间计算。若Payload中未包含exp字段，则默认ttl为86400秒（24小时）。</p></td> </tr> </tbody> </table>

<br />

## 配置示例
### 使用阿里云Redis

1. 创建Redis实例。具体操作，请参见[Redis 快速入门](https://help.aliyun.com/document_detail/54592.html)。

2. 开启logout和login配置。插件将处理1次请求，导致产生3次Redis读请求（1次logout检查，2次login检查）。在少量情况下（如登出或首次登录），将额外产生2次Redis写请求。为评估Redis容量，可以简单地按插件处理的请求吞吐量乘以2进行计算。

3. 配置好Redis后，获取其在VPC内的地址。例如：r-xxxxxxx.redis.rds.aliyuncs.com。

4. 添加服务。服务来源选择**DNS 域名** ，服务端口填写Redis端口（一般为6379），域名列表中填写获取的VPC地址，**TLS模式** 选择关闭。具体操作，请参见[创建服务](https://help.aliyun.com/document_detail/2796820.html)。

5. 在插件配置中添加如下内容即可连接到该Redis：

   ```
   HELPCODEESCAPE-yaml
   redis:
     service: redis.dns
     port: 6379
   ```

   如果给Redis服务设置了密码，则配置如下：

   ```
   HELPCODEESCAPE-yaml
   redis:
     service: redis.dns
     port: 6379
     password: ****** # 这里填写您设置的密码
   ```

### 实现JWT登出

#### **场景介绍**

由于JWT是面向无状态设计的，一旦签发就会一直有效，直到JWT过期。基于这一插件的能力，可以实现对指定JWT的强制登出。

#### **实现原理**

* 若请求路径的后缀与插件配置中的Path匹配，则会触发登出机制，通过Redis记录需要登出的JWT。Redis中存储的Key由配置的前缀以及从当前JWT Payload中提取出的Key和Value构成。

* 若请求中携带的JWT的Payload与Redis中存储的Key特征相匹配，则会被视为当前JWT已经登出，并将拒绝访问。

* Redis中键的过期时间默认值是基于JWT Payload的`exp`字段计算的，即默认存储到该JWT过期。

**说明**

* 插件默认推荐的登出键是\["jti"\]，`jti`是用于唯一标识一个JWT的Payload字段。按照JWT标准要求，当`jti`相同时，整个JWT也是完全相同的，因此可用来标记JWT的登出状态。

* Redis中存储键的拼接规则为：`<key_prefix><PayloadKey>##<PayloadValue>`，其中PayloadKey由多个键用#间隔拼接，PayloadValue由相应键对应的值用#间隔拼接。例如：`higress_jwt_logout_jti#iss##xxxxx#abcde`。

* 本插件只能登出当前请求携带的Token，您也可以手动操作Redis来登出指定的Token，按照上述键拼接规则即可。当网关查询Redis发现该键存在时，即会拒绝相应JWT的访问。

#### **示例**

插件配置：

```
HELPCODEESCAPE-yaml
redis:
  service: redis.dns
  port: 6379
jwks: |
  {
    "keys": [
      {
        "kty": "oct",
        "kid": "123",
        "k": "hM0k3AbXBPpKOGg__Ql2Obcq7s60myWDpbHXzgKUQdYo7YCRp0gUqkCnbGSvZ2rGEl4YFkKqIqW7mTHdj-bcqXpNr-NOznEyMpVPOIlqG_NWVC3dydBgcsIZIdD-MR2AQceEaxriPA_VmiUCwfwL2Bhs6_i7eolXoY11EapLQtutz0BV6ZxQQ4dYUmct--7PLNb4BWJyQeWu0QfbIthnvhYllyl2dgeLTEJT58wzFz5HeNMNz8ohY5K0XaKAe5cepryqoXLhA-V-O1OjSG8lCNdKS09OY6O0fkyweKEtuDfien5tHHSsHXoAxYEHPFcSRL4bFPLZ0orTt1_4zpyfew",
        "alg": "HS256"
      }
    ]
  }
logout:
  path: "/jwt_logout"
  key: ["jti"]
  error_status: 401
  error_body: |
    {"message":"invalid token"}
```

1. 触发登出。

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/jwt_logout -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJ4eHh4IiwiaXNzIjoiYWJjZCIsInN1YiI6InRlc3QiLCJhdWQiOiJ3d3cudGVzdC5jb20iLCJpYXQiOjE2NjU2NjA1MjcsImV4cCI6MTg2NTY3MzgxOX0.tmKF6qc1mOWNyCCzBOT2XKNoEGeEgr3EbhTKAQfq1io'

   # 将返回以下应答：
   {"message": "logout success"}
   ```

   该Token的Payload为：

   ```
   HELPCODEESCAPE-javascript
   {
       "jti": "xxxx",
       "iss": "abcd",
       "sub": "test",
       "aud": "www.test.com",
       "iat": 1665660527,
       "exp": 1865673819
   }
   ```

   此时Redis中将存在一个Key：`higress_jwt_logout_jti##xxxx`。
2. 登出后，再使用该JWT，将无法访问。

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/abc -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJ4eHh4IiwiaXNzIjoiYWJjZCIsInN1YiI6InRlc3QiLCJhdWQiOiJ3d3cudGVzdC5jb20iLCJpYXQiOjE2NjU2NjA1MjcsImV4cCI6MTg2NTY3MzgxOX0.tmKF6qc1mOWNyCCzBOT2XKNoEGeEgr3EbhTKAQfq1io'

   # 将返回以下应答：
   {"message":"invalid token"}
   ```

### 实现JWT登录互踢

#### **场景介绍**

当用户在多个设备上登录，并使用JWT进行登录认证时，可能会在不同的设备上签发不同的JWT。通过此插件，可以实现用户只能在同一时间在一个设备上登录。

#### **实现原理**

* 在请求时，提取当前请求的JWT，并根据配置的前缀以及从当前JWT Payload中提取出的Key和Value拼接出Redis Key。接着，在Redis中查询该Key所对应的Value，若该Value与当前JWT不一致，则拒绝访问。

* 若该Value不存在，则将当前JWT写入该Redis Key。Redis中Key的过期时间默认值是基于JWT Payload的`exp`字段计算的，即默认存储到该JWT过期。在此期间，具备相同Payload特征的其他JWT均将无法访问。

* 若请求的后缀匹配插件配置中的`path`，则触发强制登录机制，会将当前JWT写入对应的Redis Key的Value。这意味着之前已经登录的具有相同Payload特征的JWT将被登出，实现了登录时互踢的效果。

**说明**

* 插件默认推荐的login key是\["iss","aud","sub"\]，其中`iss`代表JWT的签发者，`aud`代表JWT的使用场景，`sub`代表JWT的签发对象。通常情况下，这三者的组合可以满足登录时互踢的场景。

* Redis中存储Key的拼接规则为：`<key_prefix><PayloadKey>##<PayloadValue>`，其中PayloadKey由多个Key用#间隔拼接，PayloadValue由Key对应的Value用#间隔拼接。举例：`higress_jwt_login_iss#aud#sub##xxxxx#abcde#fffff`。

* 在相同Payload特征的情况下，首个JWT会随业务请求自动写入Redis，从而实现插件的唯一登录功能。因此，不需要调用强制登录接口。只有在登录时需要进行互踢的情况下，才需要使用该接口。

* 就像同时开启了JWT logout功能一样，当触发logout逻辑时，也会清理Redis中当前JWT的login key。

#### **示例**

插件配置：

```
HELPCODEESCAPE-yaml
redis:
  service: redis.dns
  port: 6379
jwks: |
  {
    "keys": [
      {
        "kty": "oct",
        "kid": "123",
        "k": "hM0k3AbXBPpKOGg__Ql2Obcq7s60myWDpbHXzgKUQdYo7YCRp0gUqkCnbGSvZ2rGEl4YFkKqIqW7mTHdj-bcqXpNr-NOznEyMpVPOIlqG_NWVC3dydBgcsIZIdD-MR2AQceEaxriPA_VmiUCwfwL2Bhs6_i7eolXoY11EapLQtutz0BV6ZxQQ4dYUmct--7PLNb4BWJyQeWu0QfbIthnvhYllyl2dgeLTEJT58wzFz5HeNMNz8ohY5K0XaKAe5cepryqoXLhA-V-O1OjSG8lCNdKS09OY6O0fkyweKEtuDfien5tHHSsHXoAxYEHPFcSRL4bFPLZ0orTt1_4zpyfew",
        "alg": "HS256"
      }
    ]
  }
login:
  path: "/jwt_login"
  key: ["iss","aud","sub"]
  error_status: 403
  error_body: |
    {"message":"already login on other device"}
```

1. 成功登入。

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/abc -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJ6enp6IiwiaXNzIjoiYWJjZCIsImF1ZCI6Ind3dy5leGFtcGxlLmNvbSIsInN1YiI6InRlc3QiLCJpYXQiOjE2NjU2NjA1MjcsImV4cCI6MTg2NTY3MzgxOX0.WljMr5ucxfLF8SmeaaL25c0QG3IX04HoD0als9gglYg'
   ```

   该Token的Payload为：

   ```
   HELPCODEESCAPE-javascript
   {
       "jti": "zzzz",
       "iss": "abcd",
       "aud": "www.example.com",
       "sub": "test",
       "iat": 1665660527,
       "exp": 1865673819
   }
   ```

   此时Redis中将存在一个Key：`higress_jwt_login_iss#aud#sub##abcd#www.example.com#abcd`，Value为当前JWT。
2. 相同Payload特征拒绝访问。

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/abc -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJqdGkiOiJ5eXl5eSIsImlzcyI6ImFiY2QiLCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjY1NjYwNTI5LCJleHAiOjE4NjU2NzM4MTl9.6vi6eKPWSKHQxfzBPrj3-SWI4Q5zGtWhqp38JIN3FEo'

   # 将返回以下应答：
   {"message":"already login on other device"}
   ```

   该Token的Payload为：

   ```
   HELPCODEESCAPE-javascript
   {
       "jti": "yyyyy",
       "iss": "abcd",
       "aud": "www.example.com",
       "sub": "test",
       "iat": 1665660527,
       "exp": 1865673819
   }
   ```

   和第一步中的JWT的Payload特征一致，但非特征字段`jti`不同，因此该JWT会被拒绝访问。
3. 强制登录。

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/jwt_login -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJqdGkiOiJ5eXl5eSIsImlzcyI6ImFiY2QiLCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjY1NjYwNTI5LCJleHAiOjE4NjU2NzM4MTl9.6vi6eKPWSKHQxfzBPrj3-SWI4Q5zGtWhqp38JIN3FEo'

   # 将返回以下应答：
   {"message":"login success"}
   ```

   此时Redis中已有的Key：`higress_jwt_login_iss#aud#sub##abcd#www.example.com#abcd`，其Value会被替换为当前JWT。

   使用当前JWT可以访问成功：

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/abc -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJqdGkiOiJ5eXl5eSIsImlzcyI6ImFiY2QiLCJhdWQiOiJ3d3cuZXhhbXBsZS5jb20iLCJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjY1NjYwNTI5LCJleHAiOjE4NjU2NzM4MTl9.6vi6eKPWSKHQxfzBPrj3-SWI4Q5zGtWhqp38JIN3FEo'
   ```

   使用第一步的JWT访问，将返回失败：

   ```
   HELPCODEESCAPE-bash
   curl  http://xxx.hello.com/test/abc -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJqdGkiOiJ4eHh4IiwiaXNzIjoiYWJjZCIsImF1ZCI6Ind3dy5leGFtcGxlLmNvbSIsInN1YiI6InRlc3QiLCJpYXQiOjE2NjU2NjA1MjcsImV4cCI6MTg2NTY3MzgxOX0.P0WtBTHJzUJvklu9q8XSRszfPbgojrZHg7t4ZaYfKGo'

   # 将返回以下应答：
   {"message":"already login on other device"}
   ```

## 相关错误码
<table> <thead> <tr> <td><p><b>HTTP 状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>invalid token</p></td> <td><p>请求头未提供JWT、JWT格式错误或过期等原因。</p></td> </tr> <tr> <td><p>500</p></td> <td><p>redis server error</p></td> <td><p>访问Redis超时或失败等原因。</p></td> </tr> </tbody> </table>

<br />