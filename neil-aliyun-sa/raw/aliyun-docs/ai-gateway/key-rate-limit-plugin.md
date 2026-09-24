---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/key-rate-limit-plugin
fetch_date: 2026-09-21
product: AI Gateway
slug: key-rate-limit-plugin
body_sha256: 58def42d3d54a81c7ba706727e9cc3873e05585a75317cadbdbbedb4f9ff416f
body_bytes: 4070
migration_status: current
---

key-rate-limit插件实现了基于特定键值的限流，键值来源可以是URL参数、HTTP请求头。本文介绍如何配置key-rate-limit插件。  

## **插件类型**
流量管控。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>limit_by_header</b></p></td> <td><p>string</p></td> <td><p>选填。limit_by_header、limit_by_param中选填一项。</p></td> <td><p>-</p></td> <td><p>配置获取限流键值的来源HTTP请求头名称。</p></td> </tr> <tr> <td><p><b>limit_by_param</b></p></td> <td><p>string</p></td> <td><p>选填。limit_by_header、limit_by_param中选填一项。</p></td> <td><p>-</p></td> <td><p>配置获取限流键值的来源URL参数名称。</p></td> </tr> <tr> <td><p><b>limit_keys</b></p></td> <td><p>array of object</p></td> <td><p>必填。</p></td> <td><p>-</p></td> <td><p>配置匹配键值后的限流次数。</p></td> </tr> </tbody> </table>

子项`limit_keys`中每一项的配置字段说明。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>key</b></p></td> <td><p>string</p></td> <td><p>必填。</p></td> <td><p>-</p></td> <td><p>匹配的键值。</p></td> </tr> <tr> <td><p><b>query_per_second</b></p></td> <td><p>number</p></td> <td><p>选填。query_per_second、query_per_minute、query_per_hour或query_per_day中选填一项。</p></td> <td><p>-</p></td> <td><p>允许每秒请求次数。</p></td> </tr> <tr> <td><p><b>query_per_minute</b></p></td> <td><p>number</p></td> <td><p>选填。query_per_second、query_per_minute、query_per_hour或query_per_day中选填一项。</p></td> <td><p>-</p></td> <td><p>允许每分钟请求次数。</p></td> </tr> <tr> <td><p><b>query_per_hour</b></p></td> <td><p>number</p></td> <td><p>选填。query_per_second、query_per_minute、query_per_hour或query_per_day中选填一项。</p></td> <td><p>-</p></td> <td><p>允许每小时请求次数。</p></td> </tr> <tr> <td><p><b>query_per_day</b></p></td> <td><p>number</p></td> <td><p>选填。query_per_second、query_per_minute、query_per_hour或query_per_day中选填一项。</p></td> <td><p>-</p></td> <td><p>允许每天请求次数。</p></td> </tr> </tbody> </table>

## 配置示例
* 识别请求头x-ca-key，进行区别限流。

  ```
  HELPCODEESCAPE-yaml
  limit_by_header: x-ca-key
  limit_keys:
  - key: 102234
    query_per_second: 10
  - key: 308239
    query_per_hour: 10
  ```

* 识别请求参数apikey，进行区别限流。

  ```
  HELPCODEESCAPE-yaml
  limit_by_param: apikey
  limit_keys:
  - key: 9a342114-ba8a-11ec-b1bf-00163e1250b5
    query_per_second: 10
  - key: a6a6d7f2-ba8a-11ec-bec2-00163e1250b5
    query_per_minute: 100
  ```

* 对特定路由或域名开启。

  在`route-a`和`route-b`两个路由做如下插件配置：

  ```
  HELPCODEESCAPE-yaml
    limit_by_header: x-ca-key
    limit_keys:
    - key: 102234
      query_per_second: 10
  ```

  在`*.example.com`和`test.com`两个域名做如下插件配置：

  ```
  HELPCODEESCAPE-yaml
    limit_by_header: x-ca-key
    limit_keys:
    - key: 102234
      query_per_second: 100
  ```

  **说明**
  * 此例中的`route-a`和`route-b`即在创建网关路由时填写的路由名称，当匹配到这两个路由时，将使用此段配置。

  * 此例中的`*.example.com`和`test.com`用于匹配请求的域名，当发现域名匹配时，将使用此段配置。

  * 配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。