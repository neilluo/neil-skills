---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/key-auth-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: key-auth-plug-ins
body_sha256: c26c36718466ea34980d35fb476b428ae9d7b7afbcdc68af705e1ed0ce4af657
body_bytes: 6839
migration_status: current
---

key-auth插件实现了基于API Key进行认证鉴权的功能，支持从HTTP请求的URL参数或者请求头解析API Key，同时验证该API Key是否有权限访问。本文介绍如何配置key-auth插件。  

## **插件类型**
认证鉴权。

## 配置字段
### 认证配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>consumers</b></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置服务的调用者，用于对请求进行认证。</p></td> </tr> <tr> <td><p><b>keys</b></p></td> <td><p>array of string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>API Key的来源字段名称，可以是URL参数或者HTTP请求头名称。</p></td> </tr> <tr> <td><p><b>in_query</b></p></td> <td><p>bool</p></td> <td><p><code>in_query</code>和<code>in_header</code>至少有一个为 true</p></td> <td><p>true</p></td> <td><p>配置为<code>true</code>时，网关会尝试从URL参数中解析API Key。</p></td> </tr> <tr> <td><p><b>in_header</b></p></td> <td><p>bool</p></td> <td><p><code>in_query</code>和<code>in_header</code>至少有一个为 true</p></td> <td><p>true</p></td> <td><p>配置为<code>true</code>时，网关会尝试从HTTP请求头中解析API Key。</p></td> </tr> <tr> <td><p><b>global_auth</b></p></td> <td><p>array of string</p></td> <td><p>选填（仅实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在实例级别配置，若配置为true，则全局生效认证机制；若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。</p></td> </tr> </tbody> </table>

子项`consumers`中每一项的配置字段说明如下。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>credential</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置该consumer的访问凭证。</p></td> </tr> <tr> <td><p><b>name</b></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>配置该consumer的名称。</p></td> </tr> </tbody> </table>

#### **鉴权配置（非必需）**

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>allow</b></p></td> <td><p>array of string</p></td> <td><p>选填（非实例级别配置）</p></td> <td><p>-</p></td> <td><p>只能在路由或域名等细粒度规则上配置，对于符合匹配条件的请求，配置允许访问的 consumer，从而实现细粒度的权限控制。</p></td> </tr> </tbody> </table>  
**重要**

* 在一个规则里，鉴权配置和认证配置不可同时存在。

* 对于通过认证鉴权的请求，请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。

## 配置示例
### 全局配置认证和路由粒度进行鉴权

以下配置将对网关特定路由或域名开启Key Auth认证和鉴权。`credential`字段不能重复。

在实例级别做如下插件配置：

```
HELPCODEESCAPE-yaml
global_auth: false
consumers:
- credential: 2bda943c-ba2b-11ec-ba07-00163e125***
  name: consumer1
- credential: c8c8e9ca-558e-4a2d-bb62-e700dcc40***
  name: consumer2
keys:
- apikey
- x-api-key
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

根据该配置，下列请求可以允许访问。假设以下请求会匹配到route-a这条路由。
* 将API Key设置在URL参数中。

  ```
  HELPCODEESCAPE-bash
  curl  http://xxx.hello.com/test?apikey=2bda943c-ba2b-11ec-ba07-00163e1***
  ```

* 将API Key设置在HTTP请求头中。

  ```
  HELPCODEESCAPE-bash
  curl  http://xxx.hello.com/test -H 'x-api-key: 2bda943c-ba2b-11ec-ba07-00163e1***'
  ```

认证鉴权通过后，请求的Header中会被添加一个`X-Mse-Consumer`字段，在此例中其值为`consumer1`，用以标识调用方的名称。

下列请求将拒绝访问。
* 请求未提供API Key，返回401。

  ```
  HELPCODEESCAPE-bash
  curl  http://xxx.hello.com/test
  ```

* 请求提供的API Key无权访问，返回401。

  ```
  HELPCODEESCAPE-bash
  curl  http://xxx.hello.com/test?apikey=926d90ac-ba2e-11ec-ab68-00163e1***
  ```

* 根据请求提供的API Key匹配到的调用者无访问权限，返回403。

  ```
  HELPCODEESCAPE-bash
  # consumer2不在route-a的allow列表里
  curl  http://xxx.hello.com/test?apikey=c8c8e9ca-558e-4a2d-bb62-e700dcc***
  ```

### 网关实例级别开启

以下配置将对网关实例级别开启 Basic Auth 认证，所有请求均需要经过认证后才能访问。

```
HELPCODEESCAPE-yaml
global_auth: true
consumers:
- credential: 2bda943c-ba2b-11ec-ba07-00163e1***
  name: consumer1
- credential: c8c8e9ca-558e-4a2d-bb62-e700dcc***
  name: consumer2
keys:
- apikey
- x-api-key
```

## 相关错误码
<table> <thead> <tr> <td><p><b>HTTP状态码</b></p></td> <td><p><b>出错信息</b></p></td> <td><p><b>原因说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>401</p></td> <td><p>No API key found in request.</p></td> <td><p>请求未提供API Key。</p></td> </tr> <tr> <td><p>401</p></td> <td><p>Request denied by Key Auth check. Invalid API key.</p></td> <td><p>不允许当前API Key访问。</p></td> </tr> <tr> <td><p>403</p></td> <td><p>Request denied by Basic Auth check. Unauthorized consumer.</p></td> <td><p>请求的调用方无访问权限。</p></td> </tr> </tbody> </table>