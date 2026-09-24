---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/throttle-based-on-cluster-keys
fetch_date: 2026-09-21
product: AI Gateway
slug: throttle-based-on-cluster-keys
body_sha256: 3af72be5acaedf59504e45e1e6a8283b27fd197a5265ff7597c6ff786d9e1b4d
body_bytes: 13186
migration_status: current
---

`cluster-key-rate-limit` 插件基于 Redis 实现集群限流，适用于需要跨多个 Higress Gateway 实例实现全局一致速率限制的场景。 限流所使用的 Key 可以来源于 URL 参数、HTTP 请求头、客户端 IP 地址、消费者名称或 Cookie 中的 Key。  

## **运行属性**
插件执行阶段：`默认阶段` 插件执行优先级：`20`

## 配置说明
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>必填</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>rule_name</p> </td> <td> <p>string</p> </td> <td> <p>是</p> </td> <td> <p>-</p> </td> <td> <p>限流规则名称，根据限流规则名称 + 限流类型 + 限流 key 名称 + 限流 key 对应的实际值来拼装 redis key</p> </td> </tr> <tr> <td> <p>rule_items</p> </td> <td> <p>array of object</p> </td> <td> <p>是</p> </td> <td> <p>-</p> </td> <td> <p>限流规则项，按照 rule_items 下的排列顺序，匹配第一个 rule_item 后命中限流规则，后续规则将被忽略</p> </td> </tr> <tr> <td> <p>show_limit_quota_header</p> </td> <td> <p>bool</p> </td> <td> <p>否</p> </td> <td> <p>false</p> </td> <td> <p>响应头中是否显示\&nbsp;<code>X-RateLimit-Limit</code>（限制的总请求数）和\&nbsp;<code>X-RateLimit-Remaining</code>（剩余还可以发送的请求数）</p> </td> </tr> <tr> <td> <p>rejected_code</p> </td> <td> <p>int</p> </td> <td> <p>否</p> </td> <td> <p>429</p> </td> <td> <p>请求被限流时，返回的 HTTP 状态码</p> </td> </tr> <tr> <td> <p>rejected_msg</p> </td> <td> <p>string</p> </td> <td> <p>否</p> </td> <td> <p>Too many requests</p> </td> <td> <p>请求被限流时，返回的响应体</p> </td> </tr> <tr> <td> <p>redis</p> </td> <td> <p>object</p> </td> <td> <p>是</p> </td> <td> <p>-</p> </td> <td> <p>redis 相关配置</p> </td> </tr> </tbody> </table>

`rule_items` 中每一项的配置字段说明。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>必填</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>limit_by_header</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>配置获取限流键值的来源 HTTP 请求头名称</p> </td> </tr> <tr> <td> <p>limit_by_param</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>配置获取限流键值的来源 URL 参数名称</p> </td> </tr> <tr> <td> <p>limit_by_consumer</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>根据 consumer 名称进行限流，无需添加实际值</p> </td> </tr> <tr> <td> <p>limit_by_cookie</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>配置获取限流键值的来源 Cookie中 key 名称</p> </td> </tr> <tr> <td> <p>limit_by_per_header</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>按规则匹配特定 HTTP 请求头，并对每个请求头分别计算限流，配置获取限流键值的来源 HTTP 请求头名称，配置\&nbsp;<code>limit_keys</code>\&nbsp;时支持正则表达式或\&nbsp;<code>\*</code></p> </td> </tr> <tr> <td> <p>limit_by_per_param</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>按规则匹配特定 URL 参数，并对每个参数分别计算限流，配置获取限流键值的来源 URL 参数名称，配置\&nbsp;<code>limit_keys</code>\&nbsp;时支持正则表达式或\&nbsp;<code>\*</code></p> </td> </tr> <tr> <td> <p>limit_by_per_consumer</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>按规则匹配特定 consumer，并对每个 consumer 分别计算限流，根据 consumer 名称进行限流，无需添加实际值，配置\&nbsp;<code>limit_keys</code>\&nbsp;时支持正则表达式或\&nbsp;<code>\*</code></p> </td> </tr> <tr> <td> <p>limit_by_per_cookie</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>按规则匹配特定 Cookie，并对每个 Cookie 分别计算限流，配置获取限流键值的来源 Cookie中 key 名称，配置\&nbsp;<code>limit_keys</code>\&nbsp;时支持正则表达式或\&nbsp;<code>\*</code></p> </td> </tr> <tr> <td> <p>limit_by_per_ip</p> </td> <td> <p>string</p> </td> <td> <p>否，<code>limit_by_\*</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>按规则匹配特定 IP，并对每个 IP 分别计算限流，配置获取限流键值的来源 IP 参数名称，从请求头获取，以\&nbsp;<code>from-header-对应的header名</code>，示例：<code>from-header-x-forwarded-for</code>，直接获取对端 socket ip，配置为\&nbsp;<code>from-remote-addr</code></p> </td> </tr> <tr> <td> <p>limit_keys</p> </td> <td> <p>array of object</p> </td> <td> <p>是</p> </td> <td> <p>-</p> </td> <td> <p>配置匹配键值后的限流次数</p> </td> </tr> </tbody> </table>

`limit_keys` 中每一项的配置字段说明。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>必填</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>key</p> </td> <td> <p>string</p> </td> <td> <p>是</p> </td> <td> <p>-</p> </td> <td> <p>匹配的键值，<code>limit_by_per_header</code>,<code>limit_by_per_param</code>,<code>limit_by_per_consumer</code>,<code>limit_by_per_cookie</code>\&nbsp;类型支持配置正则表达式（以regexp：开头后面跟正则表达式）或者\*（代表所有），正则表达式示例：<code>regexp:\^d.\*</code>（以d开头的所有字符串）；<code>limit_by_per_ip</code>支持配置 IP 地址或 IP 段</p> </td> </tr> <tr> <td> <p>query_per_second</p> </td> <td> <p>int</p> </td> <td> <p>否，<code>query_per_second</code>,<code>query_per_minute</code>,<code>query_per_hour</code>,<code>query_per_day</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>允许每秒请求次数</p> </td> </tr> <tr> <td> <p>query_per_minute</p> </td> <td> <p>int</p> </td> <td> <p>否，<code>query_per_second</code>,<code>query_per_minute</code>,<code>query_per_hour</code>,<code>query_per_day</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>允许每分钟请求次数</p> </td> </tr> <tr> <td> <p>query_per_hour</p> </td> <td> <p>int</p> </td> <td> <p>否，<code>query_per_second</code>,<code>query_per_minute</code>,<code>query_per_hour</code>,<code>query_per_day</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>允许每小时请求次数</p> </td> </tr> <tr> <td> <p>query_per_day</p> </td> <td> <p>int</p> </td> <td> <p>否，<code>query_per_second</code>,<code>query_per_minute</code>,<code>query_per_hour</code>,<code>query_per_day</code>\&nbsp;中选填一项</p> </td> <td> <p>-</p> </td> <td> <p>允许每天请求次数</p> </td> </tr> </tbody> </table>

`redis` 中每一项的配置字段说明。
<table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>类型</b></p> </td> <td> <p><b>必填</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>service_name</p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>redis 服务名称，带服务类型的完整 FQDN 名称，例如 my-redis.dns、redis.my-ns.svc.cluster.local</p> </td> </tr> <tr> <td> <p>service_port</p> </td> <td> <p>int</p> </td> <td> <p>否</p> </td> <td> <p>服务类型为固定地址（static service）默认值为80，其他为6379</p> </td> <td> <p>输入Redis服务的服务端口</p> </td> </tr> <tr> <td> <p>username</p> </td> <td> <p>string</p> </td> <td> <p>否</p> </td> <td> <p>-</p> </td> <td> <p>redis 用户名</p> </td> </tr> <tr> <td> <p>password</p> </td> <td> <p>string</p> </td> <td> <p>否</p> </td> <td> <p>-</p> </td> <td> <p>redis 密码</p> </td> </tr> <tr> <td> <p>timeout</p> </td> <td> <p>int</p> </td> <td> <p>否</p> </td> <td> <p>1000</p> </td> <td> <p>redis 连接超时时间，单位毫秒</p> </td> </tr> </tbody> </table>

## 配置示例
### 识别请求参数 apikey，进行区别限流

```
HELPCODEESCAPE-yaml
rule_name: default_rule
rule_items:
- limit_by_param: apikey
  limit_keys:
  - key: 9a342114-ba8a-11ec-b1bf-00163e1250b5
    query_per_minute: 10
  - key: a6a6d7f2-ba8a-11ec-bec2-00163e1250b5
    query_per_hour: 100
- limit_by_per_param: apikey
  limit_keys:
  # 正则表达式，匹配以 a 开头的所有字符串，每个 apikey 对应的请求 10qds
  - key: "regexp:^a.*"
    query_per_second: 10
  # 正则表达式，匹配以 b 开头的所有字符串，每个 apikey 对应的请求 100qd
  - key: "regexp:^b.*"
    query_per_minute: 100
  # 兜底用，匹配所有请求，每个 apikey 对应的请求 1000qdh
  - key: "*"
    query_per_hour: 1000
redis:
  service_name: redis.static
show_limit_quota_header: true
```

### 识别请求头 x-ca-key，进行区别限流

```
HELPCODEESCAPE-yaml
rule_name: default_rule
rule_items:
- limit_by_header: x-ca-key
  limit_keys:
  - key: 102234
    query_per_minute: 10
  - key: 308239
    query_per_hour: 10
- limit_by_per_header: x-ca-key
  limit_keys:
  # 正则表达式，匹配以 a 开头的所有字符串，每个 apikey 对应的请求 10qds
  - key: "regexp:^a.*"
    query_per_second: 10
  # 正则表达式，匹配以b开头的所有字符串，每个 apikey 对应的请求 100qd
  - key: "regexp:^b.*"
    query_per_minute: 100
  # 兜底用，匹配所有请求，每个 apikey 对应的请求 1000qdh
  - key: "*"
    query_per_hour: 1000
redis:
  service_name: redis.static
show_limit_quota_header: true
```

### 根据请求头 x-forwarded-for 获取对端 IP，进行区别限流

```
HELPCODEESCAPE-yaml
rule_name: default_rule
rule_items:
- limit_by_per_ip: from-header-x-forwarded-for
  limit_keys:
  # 精确 IP
  - key: 1.1.1.1
    query_per_day: 10
  # IP 段，符合这个 IP 段的 IP，每个 IP 100qpd
  - key: 1.1.1.0/24
    query_per_day: 100
  # 兜底用，即默认每个 IP 1000 qpd
  - key: 0.0.0.0/0
    query_per_day: 1000
redis:
  service_name: redis.static
show_limit_quota_header: true
```

### 识别 consumer，进行区别限流

```
HELPCODEESCAPE-yaml
rule_name: default_rule
rule_items:
- limit_by_consumer: ''
  limit_keys:
  - key: consumer1
    query_per_second: 10
  - key: consumer2
    query_per_hour: 100
- limit_by_per_consumer: ''
  limit_keys:
  # 正则表达式，匹配以 a 开头的所有字符串，每个 consumer 对应的请求 10qds
  - key: "regexp:^a.*"
    query_per_second: 10
  # 正则表达式，匹配以 b 开头的所有字符串，每个 consumer 对应的请求 100qd
  - key: "regexp:^b.*"
    query_per_minute: 100
  # 兜底用，匹配所有请求，每个 consumer 对应的请求 1000qdh
  - key: "*"
    query_per_hour: 1000
redis:
  service_name: redis.static
show_limit_quota_header: true
```

### 识别 Cookie 中的键值对，进行区别限流

```
HELPCODEESCAPE-yaml
rule_name: default_rule
rule_items:
  - limit_by_cookie: key1
    limit_keys:
      - key: value1
        query_per_minute: 10
      - key: value2
        query_per_hour: 100
  - limit_by_per_cookie: key1
    limit_keys:
      # 正则表达式，匹配以 a 开头的所有字符串，每个 cookie 中的 value 对应的请求 10qds
      - key: "regexp:^a.*"
        query_per_second: 10
      # 正则表达式，匹配以 b 开头的所有字符串，每个 cookie 中的 value 对应的请求 100qd
      - key: "regexp:^b.*"
        query_per_minute: 100
      # 兜底用，匹配所有请求，每个 cookie 中的 value 对应的请求 1000qdh
      - key: "*"
        query_per_hour: 1000
rejected_code: 200
rejected_msg: '{"code":-1,"msg":"Too many requests"}'
redis:
  service_name: redis.static
show_limit_quota_header: true
```

## 常见问题
### cluster-key-rate-limit插件配置后限流不生效？

检查 `redis.service_name` 字段，应填写带服务类型的完整 FQDN 名称（如 `redis.dns`、`redis.my-ns.svc.cluster.local`），而非直接填写 Redis 连接地址。需先将 Redis 通过 DNS 域名方式添加到网关服务中，再填入服务名称。