---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/basic-auth-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: basic-auth-plug-ins
body_sha256: d77ff20026713321f5f618ad17bf32b24aa5e2b81eb4c9460db1fd6610943d32
body_bytes: 5994
migration_status: current
---

basic-auth插件实现了基于HTTP Basic Auth标准进行认证鉴权的功能。本文介绍如何配置basic-auth插件。  

## **插件类型**
认证鉴权。

## 配置字段
### 认证配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>consumers</b></p></td> <td><p>array of object</p></td> <td><p>必填。</p></td> <td><p>-</p></td> <td><p>配置服务的调用者，用于对请求进行认证。</p></td> </tr> <tr> <td><p><b>global_auth</b></p></td> <td><p>array of string</p></td> <td><p>选填（\*\*仅实例级别配置\*\*）</p></td> <td><p>-</p></td> <td><p>只能在实例级别配置，若配置为true，则全局生效认证机制; 若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。</p></td> </tr> </tbody> </table>

子项`consumers`中每一项的配置字段说明如下。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>credential</b></p></td> <td><p>string</p></td> <td><p>必填。</p></td> <td><p>-</p></td> <td><p>配置该consumer的访问凭证。</p></td> </tr> <tr> <td><p><b>name</b></p></td> <td><p>string</p></td> <td><p>必填。</p></td> <td><p>-</p></td> <td><p>配置该consumer的名称。</p></td> </tr> </tbody> </table>

#### **鉴权配置（非必需）**

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>allow</b></p></td> <td><p>array of string</p></td> <td><p>选填（\*\*非实例级别配置\*\*）。</p></td> <td><p>-</p></td> <td><p>只能在路由或域名等细粒度规则上配置，对于符合匹配条件的请求，配置允许访问的 consumer，从而实现细粒度的权限控制。</p></td> </tr> </tbody> </table>  
**重要**

* 在一个规则里，鉴权配置和认证配置不可同时存在。

* 对于通过认证鉴权的请求，请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。

## 配置示例
### 全局配置认证和路由粒度进行鉴权

以下配置将对网关特定路由或域名开启Basic Auth认证和鉴权。  
**说明**

* 凭证信息中的用户名和密码之间使用":"分隔。

* `credential`字段不能重复。

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
global_auth: false
consumers:
- credential: 'admin:123456'
  name: consumer1
- credential: 'guest:abc'
  name: consumer2
```

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

* 此例指定的`route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将允许`name`为`consumer1`的调用者访问，其他调用者不允许访问。

* 此例指定的`*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将允许`name`为`consumer2`的调用者访问，其他调用者不被允许访问。

根据该配置，下列请求可以允许访问。
请求指定用户名密码。

```
HELPCODEESCAPE-plaintext
# 假设以下请求将会匹配到route-a路由
# 使用 curl 的 -u 参数指定
curl -u admin:123456  http://xxx.hello.com/test
# 或者直接指定 Authorization 请求头，用户名密码使用 base64 编码
curl -H 'Authorization: Basic YWRtaW46MTIzNDU2'  http://xxx.hello.com/test
```

认证鉴权通过后，请求的Header中会被添加一个`X-Mse-Consumer`字段，在此例中其值为`consumer1`，用以标识调用方的名称。

下列请求将拒绝访问。
* 请求未提供用户名密码，返回401。

  ```
  HELPCODEESCAPE-plaintext
  curl  http://xxx.hello.com/test
  ```

* 请求提供的用户名密码错误，返回401。

  ```
  HELPCODEESCAPE-plaintext
  curl -u admin:abc  http://xxx.hello.com/test
  ```

* 根据请求的用户名和密码匹配到的调用者无访问权限，返回403。

  ```
  HELPCODEESCAPE-plaintext
  # consumer2不在route-a的allow列表里
  curl -u guest:abc  http://xxx.hello.com/test
  ```

### 网关实例级别开启

以下配置将对网关实例级别开启 Basic Auth 认证，所有请求均需要经过认证后才能访问。

```
HELPCODEESCAPE-yaml
global_auth: true
consumers:
- credential: 'admin:123456'
  name: consumer1
- credential: 'guest:abc'
  name: consumer2
```

## 相关错误码
<table> <thead> <tr> <td><p><b>HTTP状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>Request denied by Basic Auth check. No Basic Authentication information found.</p></td> <td><p>请求未提供凭证。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Request denied by Basic Auth check. Invalid username and/or password.</p></td> <td><p>请求凭证无效。</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Request denied by Basic Auth check. Unauthorized consumer.</p></td> <td><p>请求的调用方无访问权限。</p></td> </tr> </tbody> </table>