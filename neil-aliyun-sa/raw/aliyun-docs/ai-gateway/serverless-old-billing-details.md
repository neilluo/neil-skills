---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/serverless-old-billing-details
fetch_date: 2026-09-21
product: AI Gateway
slug: serverless-old-billing-details
body_sha256: 94e0ebc30898c4d5ca62f5fec0e4aaa9f027ecfbfe94facd6218f493d7ca4539
body_bytes: 3164
migration_status: legacy
---

AI 网关 Serverless（旧）采用按量付费模式，计费项包括请求 CU 费用和公网流量费用，按小时结算。  

## 版本说明
新版 Serverless 包含 Serverless 标准版和 Serverless 企业版，采用多租户架构，支持更低接入门槛和更完整的生产级能力，并持续迭代演进。Serverless（旧）为原 Serverless 版本，主要面向已有实例客户，已有实例可继续管理和使用。新客户建议优先选择新版 Serverless 标准版或企业版。

## 计费方式
AI 网关 Serverless（旧）支持按量付费（后付费）：计费以小时为单位，不足 1 小时按 1 小时计算。每小时结算一次，每 24 小时出一次账单，费用自动从阿里云账户余额中扣除。具体出账时间以实际为准。

## 计费项
Serverless（旧）计费项由请求 CU 费用和公网流量费用组成。

### 请求 CU 费用

网关请求单位 CU（Capacity Unit）是用来衡量 Serverless 实例资源消耗的最小计量单位。

CU 费用按小时收取，计费周期为 1 小时。最小计费粒度为 1000 CU，不满 1000 CU 会向上取整。在一个计费周期内，如果使用时长不足 1 小时，按 1 小时计算；如果 CU 数不足 10 万，按 10 万计算。计算公式如下：

每小时 CU 费用 = max{向上取整至 1000（该小时实际 CU 数），100000} × CU 单价

计费示例：

* 某一小时内实际 CU 数为 50200，因低于 10 万 CU，则该小时计费 CU 数为 10 万。

* 某一小时内实际 CU 数为 150200，高于 10 万 CU，因最小计费粒度为 1000 CU，向上取整后该小时计费 CU 数为 151000。

#### 不同 API 的 CU 衡量规则

单个 API 的 CU 由该 API 类型的 CU 系数和 payload 数据大小决定。计算公式如下：

单个 API CU = CU 系数 × 向上取整{（该 API 请求 payload + 该 API 响应 payload）/ 512 KB}

各类 API 的 CU 系数如下：

* Model API：10

* MCP Server：5

* Agent API：2

计费示例：

* 某 Model API 请求，请求 payload 为 100 KB，响应为 800 KB，则该次请求的 CU 为 10 × 向上取整{(100+800)/512} = 20。

* 某 MCP Server 请求，请求 payload 为 50 KB，响应为 300 KB，则该次请求的 CU 为 5 × 向上取整{(50+300)/512} = 5。

#### CU 单价

<table> <thead> <tr> <td><p><b>区域</b></p></td> <td><p><b>单价（元/1000CU）</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>中国内地（不含中国香港、中国澳门、中国台湾）</p></td> <td><p>0.005</p></td> </tr> <tr> <td><p>中国香港、日本（东京）</p></td> <td><p>0.0075</p></td> </tr> <tr> <td><p>新加坡、印度尼西亚（雅加达）、德国（法兰克福）</p></td> <td><p>0.007</p></td> </tr> <tr> <td><p>美国（弗吉尼亚）、美国（硅谷）</p></td> <td><p>0.006</p></td> </tr> </tbody> </table>

### 公网流量费用

公网流量将基于[云数据传输CDT](https://help.aliyun.com/document_detail/2357716.html)进行统一计费和出账。详细信息，请参见[CDT公网流量定价](https://help.aliyun.com/document_detail/410942.html)。