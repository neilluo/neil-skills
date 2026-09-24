---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/jwt-auth-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: jwt-auth-plug-ins
body_sha256: 4f2aa5f9d4bb4ac5f83c1a7152a875f9a8b81a9339e853942fc2991b318c17b6
body_bytes: 16630
migration_status: current
---

jwt-auth插件实现了基于JWT（JSON Web Tokens）进行认证鉴权的功能，支持从HTTP请求的URL参数、请求头、Cookie字段解析JWT，同时验证该Token是否有权限访问。相较于[配置JWT认证鉴权](https://help.aliyun.com/document_detail/2807798.html)，jwt-auth插件额外提供了调用方身份识别的能力，支持对不同调用方配置不同的JWT凭证。本文介绍如何配置jwt-auth插件。  

## **配置字段**
### 认证配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>consumers</b></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置服务的调用者，用于对请求进行认证。</p></td> </tr> <tr> <td><p><b>global_auth</b></p></td> <td><p>array of string</p></td> <td><p>选填（仅实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在实例级别配置，若配置为true，则全局生效认证机制; 若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。</p></td> </tr> </tbody> </table>

子项`consumers`中的每一项配置字段说明如下。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>name</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置该consumer的名称。</p></td> </tr> <tr> <td><p><b>jwks</b></p></td> <td><p>string</p></td> <td><p>选填。jwks和remote_jwks必填一个。</p></td> <td><p>-</p></td> <td><p><a href="https://www.rfc-editor.org/rfc/rfc7517">JSON Web Key (JWK)</a>指定的JSON格式字符串，是由验证JWT中签名的公钥（或对称密钥）组成的JSON Web Key Set。</p></td> </tr> <tr> <td><p><b>remote_jwks</b></p></td> <td><p>object</p></td> <td><p>选填。jwks和remote_jwks二选一。</p></td> <td><p>{"uri":"http://127.0.0.1/keys","service":"test.static","port":"80","ttl":30000,"timeout":3000}</p></td> <td><p>用于从指定服务的指定URI定时拉取JWKS，和JWKS字段同时配置时，以此字段配置拉取的JWKS优先。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>建议remote_jwks返回的jwks大小控制在1Mb以内。如果超过之后报错，欢迎您加入钉群"88010006189"交流，或通过<span><a href="https://smartservice.console.aliyun.com/service/create-ticket">提工单</a></span>联系支持同学。</p> </div> </div></td> </tr> <tr> <td><p><b>issuer</b></p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>JWT的签发者，需要和payload中的iss字段保持一致。</p></td> </tr> <tr> <td><p><b>claims</b></p></td> <td><p>object </p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>key/value分别对应payload中的key/value，可以用于校验多个字段是否和payload中一致，例如配置aud: mobile-site，则要求payload中的aud必须是mobile-site。</p></td> </tr> <tr> <td><p><b>claims_to_headers</b></p></td> <td><p>array of object</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>抽取JWT的payload中指定字段，设置到指定的请求头中，然后转发给后端。</p></td> </tr> <tr> <td><p><b>from_headers</b></p></td> <td><p>array of object</p></td> <td><p>选填</p></td> <td><p>\[{"name":"Authorization","value_prefix":"Bearer"}\]</p></td> <td><p>从指定的请求头中抽取JWT。</p></td> </tr> <tr> <td><p><b>from_params</b></p></td> <td><p>array of string</p></td> <td><p>选填</p></td> <td><p>access_token</p></td> <td><p>从指定的URL参数中抽取JWT。</p></td> </tr> <tr> <td><p><b>from_cookies</b></p></td> <td><p>array of string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>从指定的cookie中抽取JWT。</p></td> </tr> <tr> <td><p><b>clock_skew_seconds</b></p></td> <td><p>number</p></td> <td><p>选填</p></td> <td><p>60</p></td> <td><p>校验JWT的exp和iat字段时允许的时钟偏移量，单位为秒。</p></td> </tr> <tr> <td><p><b>keep_token</b></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>true</p></td> <td><p>转发给后端时是否保留JWT。</p></td> </tr> </tbody> </table>  
**说明**

只有当`from_headers`，`from_params`，`from_cookies`均未配置时，才会使用默认值。

* `from_headers`中每一项的配置字段说明如下。

  <table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>name</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>抽取JWT的请求Header。</p></td> </tr> <tr> <td><p><b>value_prefix</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>对请求Header的value去除此前缀，剩余部分作为JWT。</p></td> </tr> </tbody> </table>
* `claims_to_headers`中每一项的配置字段说明如下。

  <table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>claim</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>JWT payload中的指定字段，要求必须是字符串或无符号整数类型。</p></td> </tr> <tr> <td><p><b>header</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>从payload取出字段的值设置到这个请求头中，转发给后端。</p></td> </tr> <tr> <td><p><b>override</b></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>true</p></td> <td> <ul> <li><p>true时，存在同名请求头会进行覆盖。</p></li> <li><p>false时，追加同名请求头。</p></li> </ul></td> </tr> </tbody> </table>
* `remote_jwks`中每一项的配置字段说明如下。

  <table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>uri</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>请求URL。</p></td> </tr> <tr> <td><p><b>service</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td> <ul> <li><p>K8s服务填写示例：foo.default.svc.cluster.local。</p></li> <li><p>Nacos服务填写示例：foo.DEFAULT-GROUP.public.nacos。</p></li> <li><p>如果是名为test的DNS服务，则填写test.dns。</p></li> <li><p>如果是名为test的静态IP服务，则填写test.static。</p></li> </ul></td> </tr> <tr> <td><p><b>port</b></p></td> <td><p>bool</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>服务端口</p></td> </tr> <tr> <td><p><b>timeout</b></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>3000</p></td> <td><p>服务请求超时时间，单位是毫秒</p></td> </tr> <tr> <td><p><b>ttl</b></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>30000</p></td> <td><p>缓存时间，单位是毫秒。</p></td> </tr> </tbody> </table>

### 鉴权配置（非必需）

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>allow</b></p></td> <td><p>array of string</p></td> <td><p>选填（非实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在路由或域名等细粒度规则上配置，对于符合匹配条件的请求，配置允许访问的 consumer，从而实现细粒度的权限控制。</p></td> </tr> </tbody> </table>  
**重要**

* 在一个规则里，鉴权配置和认证配置不可同时存在。

* 对于通过认证鉴权的请求，请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。

## 配置示例
### 全局配置认证和路由粒度进行鉴权

以下配置将对网关特定路由或域名开启JWT Auth认证和鉴权。  
**说明**

如果一个JWT能匹配多个jwks，则按照配置顺序命中第一个匹配的consumer。

#### 插件配置

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
consumers:
- name: consumer1
  issuer: abcd
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
- name: consumer2
  issuer: abc
  jwks: |
    {
      "keys": [
        {
          "kty": "RSA",
          "e": "AQAB",
          "use": "sig",
          "kid": "123",
          "alg": "RS256",
          "n": "i0B67f1jggT9QJlZ_8QL9QQ56LfurrqDhpuu8BxtVcfxrYmaXaCtqTn7OfCuca7cGHdrJIjq99rz890NmYFZuvhaZ-LMt2iyiSb9LZJAeJmHf7ecguXS_-4x3hvbsrgUDi9tlg7xxbqGYcrco3anmalAFxsbswtu2PAXLtTnUo6aYwZsWA6ksq4FL3-anPNL5oZUgIp3HGyhhLTLdlQcC83jzxbguOim-0OEz-N4fniTYRivK7MlibHKrJfO3xa_6whBS07HW4Ydc37ZN3Rx9Ov3ZyV0idFblU519nUdqp_inXj1eEpynlxH60Ys_aTU2POGZh_25KXGdF_ZC_MSRw"
        }
      ]
    }
```

#### 路由和域名配置

在`route-a`和`route-b`两个路由做如下插件配置：

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

* 此例指定的`route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将允许`name`为`consumer1`的调用者访问，其他调用者不被允许访问。

* 此例指定的`*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将允许`name`为`consumer2`的调用者访问，其他调用者不被允许访问。

#### 请求示例

根据该配置，允许访问以下请求。假设以下请求会匹配到route-a这条路由。
* 将JWT设置在URL参数中。

  ```
  HELPCODEESCAPE-bash
  curl  'http://xxx.hello.com/test?access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEy****.eyJpc3MiOiJhYmNkIiwic3ViIjoidGVzdCIsImlhdCI6MTY2NTY2MDUyNywiZXhwIjoxODY1NjczODE5fQ.-vBSV0bKeDwQcuS6eeSZN9dLTUnSnZVk8eVCXdooCQ4'
  ```

* 将JWT设置在HTTP请求头中。

  ```
  HELPCODEESCAPE-bash
  curl  http://xxx.hello.com/test -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEyMyJ9.eyJpc3MiOiJhYmNkIiwic3ViIjoidGVzdCIsImlhdCI6MTY2NTY2MDUyNywiZXhwIjoxODY1NjczODE5fQ.-vBSV0bKeDwQcuS6eeSZN9dLTUnSnZVk8eVCXdooCQ4'
  ```

#### 结果验证

认证通过后，请求Header会添加`X-Mse-Consumer`字段，在此例中其值为`consumer1`，用于标识调用方名称。

下列请求将拒绝访问。
* 请求未提供JWT，返回401。

* 根据请求提供的JWT匹配到的调用者无访问权限，返回403。

### 网关实例级别开启，但特定路由关闭

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
global_auth: true
consumers:
- name: consumer1
  issuer: abcd
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
- name: consumer2
  issuer: abc
  jwks: |
    {
      "keys": [
        {
          "kty": "RSA",
          "e": "AQAB",
          "use": "sig",
          "kid": "123",
          "alg": "RS256",
          "n": "i0B67f1jggT9QJlZ_8QL9QQ56LfurrqDhpuu8BxtVcfxrYmaXaCtqTn7OfCuca7cGHdrJIjq99rz890NmYFZuvhaZ-LMt2iyiSb9LZJAeJmHf7ecguXS_-4x3hvbsrgUDi9tlg7xxbqGYcrco3anmalAFxsbswtu2PAXLtTnUo6aYwZsWA6ksq4FL3-anPNL5oZUgIp3HGyhhLTLdlQcC83jzxbguOim-0OEz-N4fniTYRivK7MlibHKrJfO3xa_6whBS07HW4Ydc37ZN3Rx9Ov3ZyV0idFblU519nUdqp_inXj1eEpynlxH60Ys_aTU2POGZh_25KXGdF_ZC_MSRw"
        }
      ]
    }
```

在`route-b`路由做如下插件配置：

```
HELPCODEESCAPE-yaml
_disable_: true
```

此例`route-b`即在创建网关路由时填写的路由名称。因为`_disable_`设置为`true`，当匹配到这个路由时，将关闭此插件功能，不进行JWT认证，所有人均可访问。

当没有匹配到`route-b`路由时，因为全局配置中`global_auth`设置为了`true`，表明对所有请求开启认证，所以将进行JWT认证，并且允许`consumer1`和`consumer2`都能访问。

### 域名级别开启，但特定路由关闭

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
consumers:
- name: consumer1
  issuer: abcd
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
- name: consumer2
  issuer: abc
  jwks: |
    {
      "keys": [
        {
          "kty": "RSA",
          "e": "AQAB",
          "use": "sig",
          "kid": "123",
          "alg": "RS256",
          "n": "i0B67f1jggT9QJlZ_8QL9QQ56LfurrqDhpuu8BxtVcfxrYmaXaCtqTn7OfCuca7cGHdrJIjq99rz890NmYFZuvhaZ-LMt2iyiSb9LZJAeJmHf7ecguXS_-4x3hvbsrgUDi9tlg7xxbqGYcrco3anmalAFxsbswtu2PAXLtTnUo6aYwZsWA6ksq4FL3-anPNL5oZUgIp3HGyhhLTLdlQcC83jzxbguOim-0OEz-N4fniTYRivK7MlibHKrJfO3xa_6whBS07HW4Ydc37ZN3Rx9Ov3ZyV0idFblU519nUdqp_inXj1eEpynlxH60Ys_aTU2POGZh_25KXGdF_ZC_MSRw"
        }
      ]
    }
```

在`route-b`路由做如下插件配置：

```
HELPCODEESCAPE-yaml
_disable_: true
```

在`*.example.com`域名做如下插件配置：

```
HELPCODEESCAPE-yaml
allow:
- consumer1
- consumer2
```

此例中`route-b`即在创建网关路由时填写的路由名称。因为`_disable_`设置为`true`，当匹配到这个路由时，将关闭此插件功能，不进行JWT认证，所有人均可访问。

此例中指定的`*.example.com`用于匹配请求的域名。当发现域名匹配时，将允许`name`为`consumer1`或`consumer2`的调用者访问，其他调用者不允许访问。

配置规则顺序会依次执行匹配，有任一规则匹配到，就会执行对应配置，不再匹配其他规则。因为这里配置路由匹配优先级高于域名，即对当前配置的域名生效，而对域名下的特定路由关闭。

## 相关错误码
<table> <thead> <tr> <td><p><b>HTTP状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>Jwt missing</p></td> <td><p>请求头未提供JWT。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Jwt expired</p></td> <td><p>JWT已经过期。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Jwt verification fails</p></td> <td><p>JWT payload校验失败，如iss不匹配。</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Access Denied</p></td> <td><p>无权限访问当前路由。</p></td> </tr> </tbody> </table>