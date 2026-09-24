---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-a-modelapi-throttling-policy
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-a-modelapi-throttling-policy
body_sha256: 883e5bbc324b6e940a688f46f764b574b120b1f1c23c2842d6e45e7872729756
body_bytes: 22633
migration_status: current
---

通过调用 `UpdateHttpApi` 接口，在 Model API 的 `deployConfigs` 中配置和更新 `aiTokenRateLimitConfig`（AI Token 限流策略），实现基于 Token 消耗量的多维度限流控制。

## 使用场景
AI Token 限流策略以 Token 消耗量为核心指标进行流量管控，与传统请求数限流不同，能够精准匹配大模型计算资源的实际消耗。支持按消费者、请求 Header、Query 参数、Cookie、客户端 IP、模型名称等多维度配置限流规则，并提供全局（API 级别）限流能力。

* **高并发场景**: 电商大促期间，按用户单位时间调用 Token 总量限流，防止恶意高频调用。

* **AI 服务调用**: 对大模型 API 的调用进行限流，避免因突发流量导致服务质量下降。

* **多租户系统**: 为不同租户分配独立的限流配额，确保公平性和资源隔离。

* **模型级精细管控**: 针对不同模型设置差异化的限流阈值，保护高成本模型资源。

## 接口信息
* **请求方法** : `PUT`

* **Action** : `UpdateHttpApi`

## 请求参数结构
AI Token 限流配置位于 `UpdateHttpApiRequest` 的 `deployConfigs[ ].policyConfigs[ ]` 中，通过 `PolicyConfig` 结构传递。

### PolicyConfig 结构

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>类型</p> </td> <td> <p>是否必填</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>type</p> </td> <td> <p>String</p> </td> <td> <p>是</p> </td> <td> <p>策略类型，固定为 <code>"AiTokenRateLimit"</code></p> </td> </tr> <tr> <td> <p>enable</p> </td> <td> <p>Boolean</p> </td> <td> <p>是</p> </td> <td> <p>是否启用限流策略。<code>true</code> 表示开启,<code>false</code> 表示关闭</p> </td> </tr> <tr> <td> <p>aiTokenRateLimitConfig</p> </td> <td> <p>Object</p> </td> <td> <p>是（enable 为 true 时）</p> </td> <td> <p>AI Token 限流配置详情</p> </td> </tr> </tbody> </table>

### AiTokenRateLimitConfig 结构

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>类型</p> </td> <td> <p>是否必填</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>rules</p> </td> <td> <p>Array\&lt;AiTokenRateLimitRule\&gt;</p> </td> <td> <p>条件必填</p> </td> <td> <p>普通限流规则列表（包含按维度限流和模型限流）。<code>rules</code> 和 <code>globalRules</code> 至少配置一项</p> </td> </tr> <tr> <td> <p>enableGlobalRules</p> </td> <td> <p>Boolean</p> </td> <td> <p>否</p> </td> <td> <p>是否开启全局（API 级别）限流规则，默认 <code>false</code></p> </td> </tr> <tr> <td> <p>globalRules</p> </td> <td> <p>Array\&lt;AiTokenRateLimitRule\&gt;</p> </td> <td> <p>条件必填</p> </td> <td> <p>全局限流规则列表,仅当 <code>enableGlobalRules</code> 为 <code>true</code> 时生效。规则的 <code>limitType</code> 必须为 <code>"Global"</code></p> </td> </tr> <tr> <td> <p>redisConfig</p> </td> <td> <p>Object</p> </td> <td> <p>否</p> </td> <td> <p>Redis 配置信息。</p> <ul> <li> <p>AI网关实例默认使用内置KVStore，无需配置<code>redisConfig</code></p> </li> <li> <p>仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置<code>redisConfig</code>。</p> </li> </ul> </td> </tr> </tbody> </table>

### AiTokenRateLimitRule 结构

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>类型</p> </td> <td> <p>是否必填</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>limitType</p> </td> <td> <p>String</p> </td> <td> <p>是</p> </td> <td> <p>限流维度类型</p> </td> </tr> <tr> <td> <p>matchKey</p> </td> <td> <p>String</p> </td> <td> <p>条件必填</p> </td> <td> <p>匹配键名。</p> <ul> <li> <p><code>Consumer</code> 类型允许为空</p> </li> <li> <p><code>IP</code> 类型自动设置为 <code>from-remote-addr</code></p> </li> <li> <p><code>Model</code> 类型自动设置为 <code>x-higress-llm-model</code></p> </li> <li> <p><code>Global</code> 类型自动置空</p> </li> </ul> </td> </tr> <tr> <td> <p>matchType</p> </td> <td> <p>String</p> </td> <td> <p>条件必填</p> </td> <td> <p>匹配模式。</p> <ul> <li> <p><code>IP</code> 类型自动设置为 <code>IP</code></p> </li> <li> <p><code>Model</code> 类型自动设置为 <code>Exact</code></p> </li> <li> <p><code>Global</code> 类型自动置空</p> </li> </ul> </td> </tr> <tr> <td> <p>matchValue</p> </td> <td> <p>String</p> </td> <td> <p>条件必填</p> </td> <td> <p>匹配值。</p> <ul> <li> <p><code>All</code> 模式下自动设置为 <code>\*</code></p> </li> <li> <p><code>IP</code> 类型需为合法 IP 或 IP 段</p> </li> <li> <p><code>Model</code> 类型为模型名称</p> </li> <li> <p><code>Global</code> 类型自动置空</p> </li> </ul> </td> </tr> <tr> <td> <p>limitMode</p> </td> <td> <p>String</p> </td> <td> <p>是</p> </td> <td> <p>限流模式。</p> </td> </tr> <tr> <td> <p>limitValue</p> </td> <td> <p>Integer</p> </td> <td> <p>是</p> </td> <td> <p>限流阈值,必须大于 0</p> </td> </tr> </tbody> </table>

### limitType 枚举值

<table> <thead> <tr> <td> <p>取值</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Header</p> </td> <td> <p>按请求 Header 限流</p> </td> </tr> <tr> <td> <p>Parameter</p> </td> <td> <p>按请求 Query 参数限流</p> </td> </tr> <tr> <td> <p>Consumer</p> </td> <td> <p>按消费者限流（需先开启消费者认证）</p> </td> </tr> <tr> <td> <p>Cookie</p> </td> <td> <p>按请求 Cookie 限流</p> </td> </tr> <tr> <td> <p>IP</p> </td> <td> <p>按客户端 IP 限流</p> </td> </tr> <tr> <td> <p>Model</p> </td> <td> <p>按模型名称限流（针对特定模型设置独立限额）</p> </td> </tr> <tr> <td> <p>Request</p> </td> <td> <p>按请求数限流（针对特定 key 的请求数限流）</p> </td> </tr> <tr> <td> <p>Concurrency</p> </td> <td> <p>按并发数限流（针对特定 key 的并发数限流）</p> </td> </tr> <tr> <td> <p>Global</p> </td> <td> <p>全局限流（API 级别，不区分 key，仅用于 <code>globalRules</code>）</p> </td> </tr> </tbody> </table>

### matchType 枚举值

<table> <thead> <tr> <td> <p>取值</p> </td> <td> <p>说明</p> </td> <td> <p>适用 limitType</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Exact</p> </td> <td> <p>精确匹配</p> </td> <td> <p>Header / Parameter / Consumer / Cookie / Request / Concurrency</p> </td> </tr> <tr> <td> <p>Prefix</p> </td> <td> <p>前缀匹配</p> </td> <td> <p>Header / Parameter / Consumer / Cookie / Request / Concurrency</p> </td> </tr> <tr> <td> <p>Regex</p> </td> <td> <p>正则匹配</p> </td> <td> <p>Header / Parameter / Consumer / Cookie / Request / Concurrency</p> </td> </tr> <tr> <td> <p>All</p> </td> <td> <p>任意匹配（matchValue 自动设为 <code>\*</code>）</p> </td> <td> <p>Header / Parameter / Consumer / Cookie / Request / Concurrency</p> </td> </tr> <tr> <td> <p>IP</p> </td> <td> <p>IP 匹配（自动设置，无需手动指定）</p> </td> <td> <p>IP</p> </td> </tr> </tbody> </table>  
**说明**

匹配优先级：精确匹配 \> 前缀匹配 \> 正则匹配 \> 任意匹配。命中任一规则即触发限流。

### limitMode 枚举值

<table> <thead> <tr> <td> <p>取值</p> </td> <td> <p>说明</p> </td> <td> <p>适用 limitType</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>TokenPerSecond</p> </td> <td> <p>每秒 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>TokenPerMinute</p> </td> <td> <p>每分钟 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>TokenPerHour</p> </td> <td> <p>每小时 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>TokenPerDay</p> </td> <td> <p>每天 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>TokenPerWeek</p> </td> <td> <p>每周 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>TokenPerMonth</p> </td> <td> <p>每月 Token 限流</p> </td> <td> <p>所有类型</p> </td> </tr> <tr> <td> <p>RequestPerSecond</p> </td> <td> <p>每秒请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>RequestPerMinute</p> </td> <td> <p>每分钟请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>RequestPerHour</p> </td> <td> <p>每小时请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>RequestPerDay</p> </td> <td> <p>每天请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>RequestPerWeek</p> </td> <td> <p>每周请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>RequestPerMonth</p> </td> <td> <p>每月请求数限流</p> </td> <td> <p>Model / Global / Request</p> </td> </tr> <tr> <td> <p>ConcurrencyLimit</p> </td> <td> <p>并发数限流</p> </td> <td> <p>Model / Global / Concurrency</p> </td> </tr> </tbody> </table>  
**说明**

带时间窗口的限流范围采用固定 TTL 时间窗口统计。同一限流维度和匹配值对应一个独立限流 Key，窗口从该 Key 首次写入有效统计数据时开始计时，不按自然时间边界（例如 1:00 到 2:00）切分，也不是滑动窗口。窗口到期后自动重置，后续请求不会刷新当前窗口的到期时间。例如，某 Key 在 01:23:10 首次写入统计且配置每小时限流，则该窗口到 02:23:10 左右重置，而不是在 02:00:00 重置。

### redisConfig 结构

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>类型</p> </td> <td> <p>是否必填</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>host</p> </td> <td> <p>String</p> </td> <td> <p>是</p> </td> <td> <p>Redis 服务地址</p> </td> </tr> <tr> <td> <p>port</p> </td> <td> <p>Integer</p> </td> <td> <p>是</p> </td> <td> <p>Redis 服务端口</p> </td> </tr> <tr> <td> <p>username</p> </td> <td> <p>String</p> </td> <td> <p>否</p> </td> <td> <p>Redis 用户名</p> </td> </tr> <tr> <td> <p>password</p> </td> <td> <p>String</p> </td> <td> <p>否</p> </td> <td> <p>Redis 密码</p> </td> </tr> <tr> <td> <p>timeout</p> </td> <td> <p>Integer</p> </td> <td> <p>否</p> </td> <td> <p>连接超时时间</p> </td> </tr> <tr> <td> <p>databaseNumber</p> </td> <td> <p>Integer</p> </td> <td> <p>否</p> </td> <td> <p>Redis 数据库编号</p> </td> </tr> </tbody> </table>  
**重要**

* AI网关实例默认使用内置KVStore，无需配置`redisConfig`

* 仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置`redisConfig`

## 配置示例
### 示例一：按消费者和 IP 限流

* 为 Model API 配置消费者限流：任意消费者每分钟限流 1000 Token。

* 为 Model API 配置 IP 限流：每个客户端 IP 每分钟限流 500 Token。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Consumer",
                "matchKey": "",
                "matchType": "All",
                "matchValue": "*",
                "limitMode": "TokenPerMinute",
                "limitValue": 1000
              },
              {
                "limitType": "IP",
                "matchValue": "0.0.0.0/0",
                "limitMode": "TokenPerMinute",
                "limitValue": 500
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**说明**

* `IP` 类型的 `matchKey` 和 `matchType` 由系统自动设置，无需手动指定。

* `matchValue` 设为 `0.0.0.0/0` 表示匹配所有客户端 IP。

### 示例二：按请求 Header 精确匹配限流

限制 Header 中 `x-user-level` 值为 `beta` 的请求，每分钟限流 100 Token。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Header",
                "matchKey": "x-user-level",
                "matchType": "Exact",
                "matchValue": "beta",
                "limitMode": "TokenPerMinute",
                "limitValue": 100
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### 示例三：按模型名称限流

针对不同模型设置差异化限流：

* `qwen-max` 每分钟限流 500 Token。

* `qwen-plus` 每分钟限流 2000 Token。

* `qwen-max` 每分钟最多 10 次请求。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Model",
                "matchValue": "qwen-max",
                "limitMode": "TokenPerMinute",
                "limitValue": 500
              },
              {
                "limitType": "Model",
                "matchValue": "qwen-plus",
                "limitMode": "TokenPerMinute",
                "limitValue": 2000
              },
              {
                "limitType": "Model",
                "matchValue": "qwen-max",
                "limitMode": "RequestPerMinute",
                "limitValue": 10
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**说明**

* `Model` 类型的 `matchKey` 和 `matchType` 由系统自动设置（分别为 `x-higress-llm-model` 和 `Exact`），无需手动指定。

* `matchValue` 填写目标模型名称。

### 示例四：开启全局限流

开启 API 级别的全局限流：整个 API 每分钟最多消耗 10000 Token，每分钟最多 100 次请求，最大并发数为 20。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Consumer",
                "matchKey": "",
                "matchType": "All",
                "matchValue": "*",
                "limitMode": "TokenPerMinute",
                "limitValue": 1000
              }
            ],
            "enableGlobalRules": true,
            "globalRules": [
              {
                "limitType": "Global",
                "limitMode": "TokenPerMinute",
                "limitValue": 10000
              },
              {
                "limitType": "Global",
                "limitMode": "RequestPerMinute",
                "limitValue": 100
              },
              {
                "limitType": "Global",
                "limitMode": "ConcurrencyLimit",
                "limitValue": 20
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**说明**

* 全局规则的 `limitType` 必须为 `"Global"`，不需要指定 `matchKey`、`matchType`、`matchValue`（系统会自动置空）。

* 全局限流支持 Token、Request、Concurrency 三种限流模式。

### 示例五：配置外部 Redis

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "gatewayType": "API",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Consumer",
                "matchKey": "",
                "matchType": "All",
                "matchValue": "*",
                "limitMode": "TokenPerMinute",
                "limitValue": 1000
              }
            ],
            "redisConfig": {
              "host": "r-bp1xxxxxxxxxxxxx.redis.rds.aliyuncs.com",
              "port": 6379,
              "username": "",
              "password": "your-redis-password",
              "databaseNumber": 0
            }
          }
        }
      ]
    }
  ]
}
```

### 示例六：关闭 Token 限流

将 `enable` 设置为 `false` 即可关闭限流策略。关闭后，已配置的规则不会生效，但配置信息会保留。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": false,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Consumer",
                "matchKey": "",
                "matchType": "All",
                "matchValue": "*",
                "limitMode": "TokenPerMinute",
                "limitValue": 1000
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### 示例七：更新限流规则

更新已有的限流规则，需在请求中传入完整的 `policyConfigs` 配置。以下示例将消费者限流阈值从 1000 调整为 2000。

```
HELPCODEESCAPE-json
PUT /v1/http-apis/{httpApiId}

{
  "deployConfigs": [
    {
      "gatewayId": "gw-xxxxxxxxxxxxx",
      "policyConfigs": [
        {
          "type": "AiTokenRateLimit",
          "enable": true,
          "aiTokenRateLimitConfig": {
            "rules": [
              {
                "limitType": "Consumer",
                "matchKey": "",
                "matchType": "All",
                "matchValue": "*",
                "limitMode": "TokenPerMinute",
                "limitValue": 2000
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## 配置更新规则
通过 `UpdateHttpApi` 更新策略配置时，系统按以下规则处理 `deployConfigs` 和 `policyConfigs`:

1. **PolicyConfigs 整体替换** : 当 `policyConfigs` 字段非空时，会整体替换该 `gatewayId` 下的所有策略配置。更新限流规则时，需要同时传入其他策略（如 AiFallback、AiStatistics 等）的配置，否则其他策略配置会被清空。

2. **限流规则全量更新** : `aiTokenRateLimitConfig.rules` 和 `aiTokenRateLimitConfig.globalRules` 均为全量更新，每次请求需传入完整的规则列表。

**重要**

更新限流配置前，建议先通过 `GetHttpApi` 获取当前完整的 `deployConfigs` 和 `policyConfigs`，在此基础上修改限流相关配置后再提交更新，以避免误覆盖其他策略配置。

## 配置验证规则
提交配置时，系统会对 `aiTokenRateLimitConfig` 进行以下验证：
<table> <thead> <tr> <td> <p>验证项</p> </td> <td> <p>规则</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>规则数量</p> </td> <td> <p><code>rules</code> 和 <code>globalRules</code> 至少需要配置一项</p> </td> </tr> <tr> <td> <p>limitType 与 matchType 组合</p> </td> <td> <ul> <li> <p>Header / Parameter / Consumer / Cookie / Request / Concurrency 支持 Exact / Prefix / Regex / All</p> </li> <li> <p>IP 仅支持 IP 模式</p> </li> <li> <p>Model 自动设为 Exact</p> </li> <li> <p>Global 不需要 matchType</p> </li> </ul> </td> </tr> <tr> <td> <p>matchKey</p> </td> <td> <ul> <li> <p>Header / Parameter / Cookie / Request / Concurrency 类型必填</p> </li> <li> <p>Consumer 类型允许为空</p> </li> <li> <p>IP / Model / Global 类型由系统自动设置</p> </li> </ul> </td> </tr> <tr> <td> <p>matchValue</p> </td> <td> <ul> <li> <p>Exact / Prefix / Regex 模式下必填</p> </li> <li> <p>All 模式自动设为 <code>\*</code></p> </li> <li> <p>IP 类型需为合法 IP 或 IP 段格式</p> </li> </ul> </td> </tr> <tr> <td> <p>limitValue</p> </td> <td> <ul> <li> <p>必须大于 0</p> </li> <li> <p>Model 类型的 <code>limitValue</code> 不能超过 Int32 最大值</p> </li> </ul> </td> </tr> <tr> <td> <p>globalRules 中的 limitType</p> </td> <td> <p>必须为 <code>"Global"</code></p> </td> </tr> <tr> <td> <p>rules 中的 limitType</p> </td> <td> <p>不能为 <code>"Global"</code>（Global 类型仅允许出现在 globalRules 中）</p> </td> </tr> <tr> <td> <p>redisConfig</p> </td> <td> <ul> <li> <p>AI网关实例默认使用内置KVStore，无需配置<code>redisConfig</code></p> </li> <li> <p>仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置<code>redisConfig</code></p> </li> </ul> </td> </tr> </tbody> </table>

## 常见问题
**Q：AI 网关实例是否需要配置 redisConfig？**

A：不需要。AI网关实例默认使用内置KVStore，无需配置`redisConfig`。仅在需要指定外部 Redis 实例进行流控key存储时，才需要配置`redisConfig`。

**Q：配置按消费者限流时，需要注意什么？**

A：配置按消费者（`Consumer`）限流前，需要先为该 Model API 开启消费者认证。否则限流策略无法识别消费者身份，规则不会生效。

**Q：多条规则之间的关系是什么？**

A：一个请求可以同时命中多条规则（最多同时命中 10 条），所有命中的规则均会独立扣减各自的配额。当任意一条规则的配额耗尽时，即触发限流。相同限流维度（即相同 `limitType` + `matchKey`）的规则会被合并到同一个规则组中执行。

**Q：全局限流和普通规则可以同时使用吗？**

A：可以。全局限流（`globalRules`）作用于整个 API 级别，不区分具体的 key；普通规则（`rules`）按维度细分限流。两者可以叠加使用，任一规则触发即执行限流。

**Q：更新限流配置后多久生效？**

A：更新配置后，系统会自动将新的限流规则推送到网关数据面。通常在几秒内生效。

**Q：限流在分布式架构下的准确性如何？**

A：由于分布式架构的特性，限流计数可能存在轻微偏差。实际允许的请求数与配置数会因请求量、速率、后端延迟等因素产生差异。