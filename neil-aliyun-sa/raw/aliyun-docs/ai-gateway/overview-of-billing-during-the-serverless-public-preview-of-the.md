---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/overview-of-billing-during-the-serverless-public-preview-of-the
fetch_date: 2026-09-21
product: AI Gateway
slug: overview-of-billing-during-the-serverless-public-preview-of-the
body_sha256: bd8e371519fc588887da02659628b6ed5244081699edbac6440f57507339c4c3
body_bytes: 6768
migration_status: current
---

AI 网关 Serverless 按照实例类型和实际使用量计费，费用由实例费和按量计费项组成。具体可购买的实例类型、价格、折扣、出账周期和可用地域，请以**产品控制台** 、官网价格页和**费用与成本**页面展示为准。  

## 适用范围
本文适用于 AI 网关 Serverless 新版（Serverless 标准版和 Serverless 企业版）商业化后的计费说明，不适用于 Serverless（旧）实例和实例型独享版。

模型服务、日志服务、云监控等其他云产品的费用，由对应云产品单独计费。

## 实例类型计费差异
AI 网关 Serverless 新版包含标准版和企业版。两种实例类型的计费方式不同：
<table> <thead> <tr> <td><p><b>对比项</b></p></td> <td><p><b>Serverless 标准版</b></p></td> <td><p><b>Serverless 企业版</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>起步成本</p></td> <td><p>0 元起步，无实例费</p></td> <td><p>有实例费</p></td> </tr> <tr> <td><p>计费方式</p></td> <td><p>按实际用量计费</p></td> <td><p>实例费 + 按实际用量计费</p></td> </tr> <tr> <td><p>入口能力</p></td> <td><p>使用平台分配入口</p></td> <td><p>提供独立入口能力</p></td> </tr> <tr> <td><p>自定义域名和传输加密配置</p></td> <td><p>不支持用户自定义配置</p></td> <td><p>支持自定义域名、证书、TLS policy 和 HTTP/2 配置</p></td> </tr> <tr> <td><p>公网流量</p></td> <td><p>出网、入网均由网关侧计费，0.8 元/GB</p></td> <td><p>出网、入网均由网关侧计费，0.8 元/GB</p></td> </tr> <tr> <td><p>默认 QPS 限制</p></td> <td><p>默认 50 QPS</p></td> <td><p>500 QPS</p></td> </tr> <tr> <td><p>服务等级</p></td> <td><p>99.9%</p></td> <td><p>99.95%</p></td> </tr> </tbody> </table>

如果希望低成本试用、开发测试或承载低流量业务，可以选择 Serverless 标准版。如果业务已经进入生产阶段，或需要独立入口、自定义域名和更高服务等级，建议选择 Serverless 企业版。

## 计费项说明
AI 网关 Serverless 按照实例和实际使用情况计费，包含以下计费项：
<table> <thead> <tr> <td><p><b>计费项</b></p></td> <td><p><b>计费维度</b></p></td> <td><p><b>计费方式</b></p></td> <td><p><b>参考单价</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>实例费</p></td> <td><p>实例运行时长</p></td> <td><p>仅 Serverless 企业版按实例运行时长收取，标准版无实例费</p></td> <td><p>0.245 元/小时</p></td> </tr> <tr> <td><p>请求调用次数</p></td> <td><p>请求次数（万次）</p></td> <td><p>按经过网关的请求调用次数阶梯计费，用量越大单价越低（阶梯见下表）；长连接按连接保持时长折算请求次数，计量方式见下文</p></td> <td><p>0.008--0.015 元/万次</p></td> </tr> <tr> <td><p>数据处理量</p></td> <td><p>数据量（GB）</p></td> <td><p>按请求体和响应体的数据量之和，按小时计费，不区分公网/私网</p></td> <td><p>0.037 元/GB/小时</p></td> </tr> <tr> <td><p>消费者规则扩容数</p></td> <td><p>规则数量</p></td> <td><p>当消费者相关规则数量超过基础规格时，按扩容规则数量计费</p></td> <td><p>0.02 元/100 个/小时</p></td> </tr> <tr> <td><p>公网出网流量</p></td> <td><p>公网出方向流量</p></td> <td><p>由网关侧计费；自行配置 NAT 网关的出网流量不在网关侧计费</p></td> <td><p>0.8 元/GB</p></td> </tr> <tr> <td><p>公网入网流量</p></td> <td><p>公网入方向流量</p></td> <td><p>由网关侧计费</p></td> <td><p>0.8 元/GB</p></td> </tr> </tbody> </table>

标准版和企业版的请求调用次数、数据处理量、规则扩容数适用相同的计费方式和单价。不同地域和账号优惠可能影响最终费用，以上单价为参考值，实际单价请以官网价格页和账单为准。

### 公网流量说明

公网出网和入网流量均由网关侧计费，单价为 0.8 元/GB：

* 公网出网流量：网关访问公网服务时产生的流量。如果自行配置了 NAT 网关，公网出网流量走该 NAT 网关，则网关侧不产生此部分费用。

* 公网入网流量：网关对外提供的公网接入点被访问时产生的流量。

通过私网访问不产生公网流量费用。

### 请求调用次数阶梯单价

请求调用次数按小时用量分档计价，用量越大单价越低：
<table> <thead> <tr> <td><p><b>每小时调用量</b></p></td> <td><p><b>参考单价</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>0 -- 50 万次</p></td> <td><p>0.015 元/万次</p></td> </tr> <tr> <td><p>50 -- 100 万次</p></td> <td><p>0.012 元/万次</p></td> </tr> <tr> <td><p>100 万次以上</p></td> <td><p>0.008 元/万次</p></td> </tr> </tbody> </table>

### 请求调用次数的计量规则

请求调用次数按经过网关的请求个数计费。对于长连接（如流式响应、MCP 长连接、Agent 长会话），因其在连接保持期间持续占用网关资源，会按连接保持时长折算为请求次数：
<table> <thead> <tr> <td><p><b>计量规则</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>短连接请求</p></td> <td><p>普通请求-响应请求按 1 次请求调用计量</p></td> </tr> <tr> <td><p>长连接按时长折算</p></td> <td><p>长连接按连接保持时长，每 30 秒计为 1 次请求调用</p></td> </tr> </tbody> </table>

计量示例：
<table> <thead> <tr> <td><p><b>请求特征</b></p></td> <td><p><b>计量请求次数</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>普通 AI 对话请求（数秒内完成）</p></td> <td><p>1 次</p></td> </tr> <tr> <td><p>保持 2 分钟的长连接</p></td> <td><p>4 次</p></td> </tr> <tr> <td><p>保持 10 分钟的长连接</p></td> <td><p>20 次</p></td> </tr> </tbody> </table>

请求体和响应体的数据量单独按"数据处理量"计费，不影响请求调用次数。具体计量规则、单价请以官网价格页、**产品控制台**和账单展示为准。

## 费用计算方式
```
HELPCODEESCAPE-plaintext
网关费用 = 实例费 + 请求调用费用 + 数据处理量费用 + 规则扩容费用 + 公网流量费用
```

公网出入网流量按 0.8 元/GB 在网关账单中计费；智能路由等 AI 增强能力和模型 Token 费用单独计费。

## 查看账单
可以在**费用与成本**相关页面查看 AI 网关 Serverless 的用量和账单明细。