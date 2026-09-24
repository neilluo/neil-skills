---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/current-limiting
fetch_date: 2026-09-21
product: AI Gateway
slug: current-limiting
body_sha256: 1a213773d185bc563a3aae028ed75254b6c1dc9a14826f5980a51343ab15a524
body_bytes: 22270
migration_status: current
---

API 限流策略专为大模型服务及高并发调用场景设计，支持基于 Token 消耗量、请求数和并发数的多维度动态控制机制。该策略可针对消费者身份、请求 Header 参数、Query 参数、Cookie、客户端 IP、模型名称等多维度配置限流规则，并提供 API 级别的全局限流能力。这种多维度限流模式能精准匹配大模型计算资源消耗特性，有效防止系统过载、接口滥用及恶意调用，同时保障核心业务在复杂场景下的稳定运行。

## 策略说明
* 防止资源过载：通过设置灵活的限流策略（如按消费者、Header、Query 参数、Cookie、客户端 IP 或模型名称），可以有效限制高频调用或恶意请求，避免因资源过载导致系统崩溃或性能下降。同时，建议配合[缓存](https://help.aliyun.com/document_detail/2873942.html)策略以提升系统性能。

* 动态调整流量：支持多种限流范围（如每秒、每分钟、每小时、每天），可以根据业务需求灵活调整限流规则，确保系统在高并发场景下仍能稳定运行。

* 多种匹配规则支持：限流策略支持多种匹配规则（精确匹配、前缀匹配、正则匹配、任意匹配），能够满足高优先级的复杂业务场景需求。

* 多种限流模式：支持按 Token 消耗量限流、按请求数限流和按并发数限流三种模式，满足不同粒度的流量管控需求。

* 模型级精细管控：支持针对不同模型名称设置差异化的限流阈值，保护高成本模型资源。

* 全局限流能力：支持 API 级别的全局限流（按 API 限流），作为普通规则之外的兜底策略，从整体上控制 API 的 Token 消耗、请求数和并发数。

* 防止恶意攻击：通过对特定消费者、Header、Query 参数、Cookie 或客户端 IP 进行限流，可以有效限制爬虫或自动化工具的访问频率，保护数据安全。

## 适用场景
* 高并发场景：电商大促期间，按用户单位时间调用 Token 总量限流，防止恶意高频调用，保障服务稳定及活动公平。

* AI 服务调用：对大模型 API 的调用进行限流，避免因突发流量导致服务质量下降或系统崩溃。

* 多租户系统：在开放平台或多租户架构中，为不同租户分配独立的限流配额，确保公平性和资源隔离。

* 模型级精细管控：针对不同模型（如 qwen-max、qwen-plus）设置差异化的 Token 限额和请求数限额，保护高成本模型资源。

* 全局流量保护：通过 API 级别的全局限流，从整体上控制 Token 消耗总量、请求总数和最大并发数，防止 API 被过度调用。

* 恶意攻击防护：防范针对 AI 接口的爬虫攻击、DDoS 攻击或接口滥用行为，保护系统安全。

## 操作步骤
1. 打开[AI 网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例 ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API 名称** 进入**API 详情**页面。

3. 单击**策略与插件** ，然后打开**限流**开关并配置相关参数。

> **说明** 最多只支持同时命中 10 条规则。

### 限流策略

**限流策略** 区域用于配置具体的限流规则。每条规则由三部分组成：**判断条件** 、**限流规则** （匹配方式）和**限流范围** （限流模式 + 限流值 + 限流单位）。规则支持拖拽排序，可通过**添加**按钮新增规则行。
<table> <thead> <tr> <td> <p>配置项</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>限流</b><b></b></p> </td> <td> <p>开启或关闭限流策略，默认关闭。</p> </td> </tr> <tr> <td> <p><b>判断条件</b><b></b></p> </td> <td> <p>选择限流维度，支持 6 种：按消费者、按请求 Header、按请求 Query 参数、按请求 Cookie、按客户端 IP、按模型。</p> </td> </tr> <tr> <td> <p><b>限流规则</b><b></b></p> </td> <td> <p>根据判断条件的不同，需要填写不同的匹配信息（匹配规则、参数名称、匹配内容等），详见下方各维度说明。</p> </td> </tr> <tr> <td> <p><b>限流范围</b><b></b></p> </td> <td> <p>选择限流的时间窗口：每秒、每分钟、每小时、每天。</p> </td> </tr> <tr> <td> <p><b>限流值</b></p> </td> <td> <p>填写限流阈值。</p> </td> </tr> <tr> <td> <p><b>限流单位</b></p> </td> <td> <p>选择限流的计量单位：<b>Token</b>、<b>请求数</b>或<b>并发数</b>。</p> </td> </tr> </tbody> </table>

#### 按消费者

根据消费者身份进行限流，适用于多租户场景。

* **表单项**：判断条件（按消费者）→ 匹配规则（精确匹配/前缀匹配/正则匹配/任意匹配）→ 消费者选择 → 限流范围 → 限流值 + 限流单位

* **消费者选择** ：从已有消费者列表中选择，也可点击**创建消费者** 快速新建。选择`任意匹配`时无需选择具体消费者。

* **示例**：任意消费者每分钟限流 1000 Token。

> **重要** 配置按消费者限流，需要先开启 [消费者认证](https://help.aliyun.com/document_detail/2873943.html)。

#### 按请求 Header

根据请求 Header 中的指定字段进行限流。

* **表单项**：判断条件（按请求 Header）→ 参数名称（Header 字段名）→ 匹配规则（精确匹配/前缀匹配/正则匹配/任意匹配）→ 匹配内容 → 限流范围 → 限流值 + 限流单位

* **参数名称**：必填，输入需要匹配的 Header 字段名。

* **匹配内容** ：选择`任意匹配`时无需填写。

* **示例** ：限制 Header 中 `x-user-level` 值为 `beta` 的请求，每分钟限流 100 Token。

#### 按请求 Query 参数

根据请求 URL 中的 Query 参数进行限流。

* **表单项**：判断条件（按请求 Query 参数）→ 参数名称（Query 参数名）→ 匹配规则（精确匹配/前缀匹配/正则匹配/任意匹配）→ 匹配内容 → 限流范围 → 限流值 + 限流单位

* **参数名称**：必填，输入需要匹配的 Query 参数名。

* **匹配内容** ：选择`任意匹配`时无需填写。

* **示例** ：限制 Query 参数中 `user_id=1` 的请求，每分钟限流 100 Token。

#### 按请求 Cookie

根据请求 Cookie 中的指定字段进行限流。

* **表单项**：判断条件（按请求 Cookie）→ 参数名称（Cookie 字段名）→ 匹配规则（精确匹配/前缀匹配/正则匹配/任意匹配）→ 匹配内容 → 限流范围 → 限流值 + 限流单位

* **参数名称**：必填，输入需要匹配的 Cookie 字段名。

* **匹配内容** ：选择`任意匹配`时无需填写。

* **示例**：限制 Cookie 中带有目标标识的请求，每分钟限流 100 Token。

#### 按客户端 IP

根据客户端 IP 地址进行限流，支持单个 IP 和 IP 段。

* **表单项**：判断条件（按客户端 IP）→ IP 地址 → 限流值 + 限流单位

* **IP 地址** ：输入需要限流的 IP 地址（如 `192.168.1.1`）或 IP 段（如 `192.168.1.0/24`）。填写 `0.0.0.0/0` 表示匹配所有客户端 IP。

* **示例**：限制每个客户端 IP 最大并发数为 50。

> **说明** 按客户端 IP 限流无需选择匹配规则和限流范围，系统会自动处理。

#### 按模型

针对特定模型名称设置独立的限流阈值，适用于多模型服务场景。

* **表单项**：判断条件（按模型）→ 匹配规则（精确匹配，固定不可更改）→ 模型名称 → 限流值 + 限流单位

* **模型名称**：必填，输入需要限流的目标模型名称。

* **限流单位** ：支持 **Token** 、**请求数** 和**并发数**三种。

* **示例** ：`qwen-max` 每分钟限流 500 Token，同时限制最大并发数为 10。

> **说明** 按模型限流固定使用精确匹配。如果需要更灵活的模型匹配（如前缀匹配、正则匹配），可以使用"按请求 Header"并手动指定参数名称为 `x-higress-llm-model`。

### 按 API 限流（全局限流）

按 API 限流是独立于上述限流策略之外的**兜底策略**，对整个 API 进行全局限流，不区分具体的判断条件。

* **启用方式** ：勾选**按 API 限流** 区域的**开启**复选框。

* **表单项**：限流范围（每秒/每分钟/每小时/每天）→ 限流值 + 限流单位（Token/请求数/并发数）

* **支持添加多条** ：可通过**添加**按钮新增多条全局限流规则，分别设置不同的限流模式。

* **示例**：整个 API 每分钟最多消耗 10000 Token，每分钟最多 100 次请求，最大并发数为 20。

> **说明** 按 API 限流为上述策略之外的兜底策略。全局限流和普通规则可以同时使用，两者叠加生效，命中任一规则即触发限流。

4. 确认配置信息并单击**保存**。

## 匹配规则
按消费者、按请求 Header、按请求 Query 参数、按请求 Cookie 四种判断条件支持以下四种**匹配规则**，优先级：精确匹配 \> 前缀匹配 \> 正则匹配 \> 任意匹配。
<table> <thead> <tr> <td> <p>匹配规则</p> </td> <td> <p>说明</p> </td> <td> <p>示例</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>精确匹配</b></p> </td> <td> <p>匹配值与目标值完全相同</p> </td> <td> <p>Header <code>x-user-level</code> 精确等于 <code>beta</code></p> </td> </tr> <tr> <td> <p><b>前缀匹配</b></p> </td> <td> <p>匹配值以指定前缀开头</p> </td> <td> <p>Header <code>x-user-level</code> 以 <code>vip</code> 开头</p> </td> </tr> <tr> <td> <p><b>正则匹配</b></p> </td> <td> <p>匹配值符合指定正则表达式</p> </td> <td> <p>Header <code>x-user-level</code> 匹配 <code>\`\^(gold</code></p> </td> </tr> <tr> <td> <p><b>任意匹配</b></p> </td> <td> <p>匹配该维度下的所有值，无需填写匹配内容</p> </td> <td> <p>任意消费者均适用</p> </td> </tr> </tbody> </table> **说明** 如果配置了多条规则，则命中任一规则即被拦截。按客户端 IP 和按模型有各自固定的匹配方式，无需手动选择匹配规则。

## 限流单位与限流模式
每条限流规则的限流值后面可以选择**限流单位**，不同的限流单位对应不同的计量方式：
<table> <thead> <tr> <td> <p>限流单位</p> </td> <td> <p>说明</p> </td> <td> <p>适用的判断条件</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Token</b></p> </td> <td> <p>按大模型的传入传出 Token 消耗量计算</p> </td> <td> <p>所有判断条件</p> </td> </tr> <tr> <td> <p><b>请求数</b></p> </td> <td> <p>按请求次数计算</p> </td> <td> <p>所有判断条件</p> </td> </tr> <tr> <td> <p><b>并发数</b></p> </td> <td> <p>按同时处理的请求数量计算</p> </td> <td> <p>所有判断条件</p> </td> </tr> </tbody> </table>

限流策略支持以下**限流范围**（时间窗口），与限流单位组合使用：
<table> <thead> <tr> <td> <p>限流范围</p> </td> <td> <p>Token 限流</p> </td> <td> <p>请求数限流</p> </td> <td> <p>并发数限流</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>每秒</b></p> </td> <td> <p>每秒允许消耗的最大 Token 数</p> </td> <td> <p>每秒允许的最大请求次数</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p><b>每分钟</b></p> </td> <td> <p>每分钟允许消耗的最大 Token 数</p> </td> <td> <p>每分钟允许的最大请求次数</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p><b>每小时</b></p> </td> <td> <p>每小时允许消耗的最大 Token 数</p> </td> <td> <p>每小时允许的最大请求次数</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p><b>每天</b></p> </td> <td> <p>每天允许消耗的最大 Token 数</p> </td> <td> <p>每天允许的最大请求次数</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p><b>（无时间窗口）</b></p> </td> <td> <p>---</p> </td> <td> <p>---</p> </td> <td> <p>允许同时处理的最大请求数</p> </td> </tr> </tbody> </table>  
**说明**

带时间窗口的限流范围采用固定 TTL 时间窗口统计。同一限流维度和匹配值对应一个独立限流 Key，窗口从该 Key 首次写入有效统计数据时开始计时，不按自然时间边界（例如 1:00 到 2:00）切分，也不是滑动窗口。窗口到期后自动重置，后续请求不会刷新当前窗口的到期时间。例如，某 Key 在 01:23:10 首次写入统计且配置每小时限流，则该窗口到 02:23:10 左右重置，而不是在 02:00:00 重置。
> **说明** 并发数限流不需要选择限流范围（时间窗口），直接设置最大并发数即可。

## 配置示例
### 示例一：按消费者 Token 限流 + 按客户端 IP 并发限流

配置两条规则：任意消费者每分钟限流 1000 Token，每个客户端 IP 最大并发数 50。
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>判断条件</p> </td> <td> <p>匹配规则</p> </td> <td> <p>参数名称/匹配内容</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>按消费者</p> </td> <td> <p>任意匹配</p> </td> <td> <p>---</p> </td> <td> <p>每分钟</p> </td> <td> <p>1000</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>2</p> </td> <td> <p>按客户端 IP</p> </td> <td> <p>---</p> </td> <td> <p>0.0.0.0/0</p> </td> <td> <p>---</p> </td> <td> <p>50</p> </td> <td> <p>并发数</p> </td> </tr> </tbody> </table>

### 示例二：按请求 Header 限流（多种匹配规则）

针对不同 Header 值设置差异化限流规则：
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>判断条件</p> </td> <td> <p>参数名称</p> </td> <td> <p>匹配规则</p> </td> <td> <p>匹配内容</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>按请求 Header</p> </td> <td> <p>x-user-level</p> </td> <td> <p>精确匹配</p> </td> <td> <p>beta</p> </td> <td> <p>每分钟</p> </td> <td> <p>100</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>2</p> </td> <td> <p>按请求 Header</p> </td> <td> <p>x-user-level</p> </td> <td> <p>前缀匹配</p> </td> <td> <p>vip</p> </td> <td> <p>每小时</p> </td> <td> <p>5000</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>3</p> </td> <td> <p>按请求 Header</p> </td> <td> <p>x-app-id</p> </td> <td> <p>任意匹配</p> </td> <td> <p>---</p> </td> <td> <p>每分钟</p> </td> <td> <p>50</p> </td> <td> <p>请求数</p> </td> </tr> </tbody> </table>

### 示例三：按模型名称差异化限流

针对不同模型设置差异化限流：`qwen-max` 每分钟限流 500 Token 且最大并发 10，`qwen-plus` 每分钟限流 2000 Token。
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>判断条件</p> </td> <td> <p>匹配规则</p> </td> <td> <p>模型名称</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>按模型</p> </td> <td> <p>精确匹配</p> </td> <td> <p>qwen-max</p> </td> <td> <p>每分钟</p> </td> <td> <p>500</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>2</p> </td> <td> <p>按模型</p> </td> <td> <p>精确匹配</p> </td> <td> <p>qwen-plus</p> </td> <td> <p>每分钟</p> </td> <td> <p>2000</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>3</p> </td> <td> <p>按模型</p> </td> <td> <p>精确匹配</p> </td> <td> <p>qwen-max</p> </td> <td> <p>---</p> </td> <td> <p>10</p> </td> <td> <p>并发数</p> </td> </tr> </tbody> </table>

### 示例四：按 API 限流（全局限流）+ 消费者限流组合

在消费者限流基础上，开启按 API 限流作为兜底策略：

**限流策略（普通规则）**：
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>判断条件</p> </td> <td> <p>匹配规则</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>按消费者</p> </td> <td> <p>任意匹配</p> </td> <td> <p>每分钟</p> </td> <td> <p>1000</p> </td> <td> <p>Token</p> </td> </tr> </tbody> </table>

**按 API 限流（全局规则，勾选"开启"）**：
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>每分钟</p> </td> <td> <p>10000</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>2</p> </td> <td> <p>每分钟</p> </td> <td> <p>100</p> </td> <td> <p>请求数</p> </td> </tr> <tr> <td> <p>3</p> </td> <td> <p>---</p> </td> <td> <p>20</p> </td> <td> <p>并发数</p> </td> </tr> </tbody> </table> **说明** 按 API 限流为上述策略之外的兜底策略，需要单独勾选"开启"，与普通规则独立配置。

### 示例五：混合多维度限流

同时配置多种判断条件的限流规则：
<table> <thead> <tr> <td> <p>序号</p> </td> <td> <p>判断条件</p> </td> <td> <p>参数名称</p> </td> <td> <p>匹配规则</p> </td> <td> <p>匹配内容/IP/模型名称</p> </td> <td> <p>限流范围</p> </td> <td> <p>限流值</p> </td> <td> <p>限流单位</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1</p> </td> <td> <p>按消费者</p> </td> <td> <p>---</p> </td> <td> <p>精确匹配</p> </td> <td> <p>consumer-001</p> </td> <td> <p>每分钟</p> </td> <td> <p>500</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>2</p> </td> <td> <p>按请求 Header</p> </td> <td> <p>x-user-level</p> </td> <td> <p>前缀匹配</p> </td> <td> <p>vip</p> </td> <td> <p>每小时</p> </td> <td> <p>10000</p> </td> <td> <p>Token</p> </td> </tr> <tr> <td> <p>3</p> </td> <td> <p>按请求 Query 参数</p> </td> <td> <p>user_id</p> </td> <td> <p>正则匹配</p> </td> <td> <p>\^\[0-9\]+$</p> </td> <td> <p>每分钟</p> </td> <td> <p>200</p> </td> <td> <p>请求数</p> </td> </tr> <tr> <td> <p>4</p> </td> <td> <p>按请求 Cookie</p> </td> <td> <p>session</p> </td> <td> <p>任意匹配</p> </td> <td> <p>---</p> </td> <td> <p>每分钟</p> </td> <td> <p>100</p> </td> <td> <p>请求数</p> </td> </tr> <tr> <td> <p>5</p> </td> <td> <p>按客户端 IP</p> </td> <td> <p>---</p> </td> <td> <p>---</p> </td> <td> <p>192.168.1.0/24</p> </td> <td> <p>---</p> </td> <td> <p>30</p> </td> <td> <p>并发数</p> </td> </tr> <tr> <td> <p>6</p> </td> <td> <p>按模型</p> </td> <td> <p>---</p> </td> <td> <p>精确匹配</p> </td> <td> <p>qwen-max</p> </td> <td> <p>每分钟</p> </td> <td> <p>1000</p> </td> <td> <p>Token</p> </td> </tr> </tbody> </table>

## 常见问题
**Q：最多可以配置多少条限流规则？**

A：最多只支持同时命中 10 条规则。您可以根据业务需求灵活组合不同维度的规则，但建议控制规则数量以确保性能。

**Q：多条规则之间的关系是什么？**

A：多条规则之间的关系为`或`，即命中任一规则即触发限流。相同限流维度（相同判断条件 + 匹配键）的规则会被合并到同一个规则组中执行。

**Q：按 API 限流和普通限流规则可以同时使用吗？**

A：可以。按 API 限流（全局规则）作为普通规则之外的兜底策略，作用于整个 API 级别，不区分具体的 key；普通规则按维度细分限流。两者可以叠加使用，任一规则触发即执行限流。

**Q：按模型限流和按请求 Header 限流有什么区别？**

A：按模型限流时，系统会自动将其转换为基于 `x-higress-llm-model` Header 的精确匹配限流。如果需要更灵活的模型匹配（如前缀匹配、正则匹配），可以使用按请求 Header 限流并手动指定参数名称为 `x-higress-llm-model`。

**Q：Token、请求数和并发数三种限流单位可以组合使用吗？**

A：可以。同一个判断条件下可以添加多条规则，分别选择不同的限流单位。例如，针对同一个模型既可以设置每分钟 Token 限额，也可以设置最大并发数限额，两者独立计数，命中任一即触发限流。

**Q：按客户端 IP 限流为什么没有匹配规则和限流范围选项？**

A：按客户端 IP 限流的表单经过简化设计，只需输入 IP 地址或 IP 段即可。系统会自动处理匹配逻辑。如果需要对所有客户端 IP 进行限流，可以输入 `0.0.0.0/0`。

**Q：规则的顺序是否影响限流效果？**

A：规则支持拖拽排序，但多条规则之间的关系为`或`，命中任一规则即触发限流，因此规则顺序不影响最终的限流效果。

**Q：更新限流配置后多久生效？**

A：更新配置后，系统会自动将新的限流规则推送到网关数据面，通常在几秒内生效。

**Q：限流在分布式架构下的准确性如何？**

A：由于分布式架构的特性，限流计数可能存在轻微偏差。实际允许的请求数与配置数会因请求量、速率、后端延迟等因素产生差异。