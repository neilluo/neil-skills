---
source_url: https://help.aliyun.com/zh/api-gateway/request-response-capture-1
fetch_date: 2026-09-21
product: AI Gateway
slug: request-response-capture-1
body_sha256: 6712f66b31a0793c66a1baf4c36e83e3f08322ea114ca5a60fd8ada2b920dfd5
body_bytes: 5690
migration_status: current
---

请求/响应采集是网关的一项日志增强能力，可将经过网关的请求和响应内容记录到访问日志中，随访问日志投递到日志服务（SLS），便于问题排查、接口审计和流量分析。  
采集内容分为请求头、请求体、响应头和响应体四项，每项可独立开启或关闭。该功能在网关级别生效，作用于该网关下的所有流量。  
**重要**

开启该功能会显著增加日志量和日志成本，建议仅在调试时开启，问题定位完成后及时关闭。

## 网关版本要求
该功能需要较新的网关引擎版本。Serverless版不支持该功能。

开启时系统会自动校验引擎版本，不满足要求时会拒绝并提示升级。关闭操作不受版本限制，任何版本都可随时关闭。
<table> <thead> <tr> <td><p><b>网关类型</b></p></td> <td><p><b>最低引擎版本</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>云原生 API 网关</p></td> <td><p>2.1.18 及以上</p></td> </tr> <tr> <td><p>AI 网关</p></td> <td><p>2.1.20 及以上</p></td> </tr> </tbody> </table>

若版本过低，请先升级网关引擎版本后再开启。

## 配置说明
功能包含以下配置项：
<table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>默认值</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>记录请求 Headers</p></td> <td><p>是否采集请求头</p></td> <td><p>关闭</p></td> </tr> <tr> <td><p>记录请求 Body</p></td> <td><p>是否采集请求体</p></td> <td><p>关闭</p></td> </tr> <tr> <td><p>请求 Body 最大采集大小（Bytes）</p></td> <td><p>请求体最大采集字节数</p></td> <td><p>5120（5 KB）</p></td> </tr> <tr> <td><p>记录响应 Headers</p></td> <td><p>是否采集响应头</p></td> <td><p>关闭</p></td> </tr> <tr> <td><p>记录响应 Body</p></td> <td><p>是否采集响应体</p></td> <td><p>关闭</p></td> </tr> <tr> <td><p>响应 Body 最大采集大小（Bytes）</p></td> <td><p>响应体最大采集字节数</p></td> <td><p>5120（5 KB）</p></td> </tr> </tbody> </table>

### Body 最大采集大小规则

* 单位为字节（Bytes），仅在对应 Body 采集开启时生效。

* 不填或填 0 及以下：按默认 5 KB 采集。

* 单个 Body 的最大采集大小上限取决于网关实例的部署形态，请以控制台配置页给出的上限提示为准；当前为全托管实例 5 KB（5120 字节）、非全托管实例 200 KB（204800 字节）。

* 超出该大小的 Body 内容会被截断，只保留前面部分。

## 开启与关闭
### 开启

**重要**

采集内容随访问日志投递到日志服务（SLS）。开启前，确保已配置访问日志投递。

1. 进入网关详情页，打开**参数配置** ，找到**访问日志投递配置**区域。

2. 找到**请求/响应采集**，单击其右侧的状态链接打开配置弹窗。

3. 按需开启**记录请求 Headers** 、**记录请求 Body** 、**记录响应 Headers** 、**记录响应 Body**，并设置 Body 最大采集大小。

4. 单击**保存**。保存成功后，状态链接变为"已开启"。

### 关闭

打开配置弹窗，关闭对应开关并单击**保存**。四项全部关闭即等同关闭整个功能，保存后状态链接变为"未开启"，相关内容不再写入访问日志。

## 查看采集到的日志
采集到的内容会作为附加字段写入网关访问日志，随访问日志一起进入日志服务（SLS）。采集内容对应以下日志字段：
<table> <thead> <tr> <td><p><b>采集内容</b></p></td> <td><p><b>访问日志字段</b></p></td> <td><p><b>控制开关</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>请求头</p></td> <td><p><code>request_headers</code> 对象下的 <code>envoy.all_request_headers</code> 子字段</p></td> <td><p>记录请求 Headers</p></td> </tr> <tr> <td><p>请求体</p></td> <td><p>顶层字段 <code>request_body</code></p></td> <td><p>记录请求 Body</p></td> </tr> <tr> <td><p>响应头</p></td> <td><p><code>response_headers</code> 对象下的 <code>envoy.all_response_headers</code> 子字段</p></td> <td><p>记录响应 Headers</p></td> </tr> <tr> <td><p>响应体</p></td> <td><p>顶层字段 <code>response_body</code></p></td> <td><p>记录响应 Body</p></td> </tr> </tbody> </table>

### 字段说明

* **请求体/响应体** ：直接写入顶层字段 `request_body` / `response_body`。

* **请求头/响应头** ：写入 `request_headers` / `response_headers` 对象内的 `envoy.all_request_headers` / `envoy.all_response_headers` 子字段。这两个对象也承载访问日志的自定义 Header 采集能力，因此采集到的完整头信息以子字段形式与其共存，不会互相覆盖。

### 字段出现规则

* 字段**按需出现**：只有对应采集项开启时，相关字段才会写入访问日志；未开启的采集项对应的字段不会出现。

* 通过日志服务（SLS）可按上述字段进行查询、过滤和分析。

* 当请求体/响应体超过配置的最大采集大小时，对应字段中只保留截断后的前面部分内容。

## 数据安全与采集限制
* **敏感数据**：请求/响应的头和正文中可能包含令牌、密码、个人信息等敏感数据。开启前请评估合规与脱敏要求，仅开启必要的采集项，并合理设置 Body 大小。

* **Body 采集范围**：并非所有类型的正文都会被记录（受内容类型限制），且超过设置大小的部分会被截断。