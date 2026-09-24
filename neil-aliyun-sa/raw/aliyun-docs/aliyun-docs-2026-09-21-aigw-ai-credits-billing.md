<!-- source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/ai-credits-billing-details -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 未在 .md 通道提供（fetched 2026-09-21） -->
<!-- summary: AI Credits 计费详情官方全文（补归档：上一轮仅 llms.txt 在线复核）。关键取证点：Credit 单价 0.01 元/Credit；仅智能路由等 AI 增强能力消耗，普通 LLM API 代理透传与自定义模型服务调用不消耗；需先创建 AI 网关实例再单独开通，开通后不支持退订，未使用不产生费用。 -->

AI Credits 是 AI 网关中 AI 增强能力的计费单位，适用于 AI 网关 Serverless（标准版/企业版）和实例型独享版。当您使用智能路由等 AI 增强能力时，系统按实际使用量折算为 Credits 消耗并计费。

Credit 单价为 0.01 元/Credit。

按实际消耗的 Credits 数量按量计费。具体价格、优惠和出账周期请以官网价格页、产品控制台和账单展示为准。

## **开通方式**
AI Credits 是独立的按量付费开通型商品，与网关实例的基础计费相互独立：

* 您需要先创建 AI 网关实例，再单独开通 AI Credits 按量付费商品，才能使用对应的 AI 增强能力。

* 未开通时，AI 增强能力不可用，不会产生 Credits 费用。

* 开通后不支持退订和关闭。只要您不使用对应的 AI 增强能力，就不会产生 Credits 费用。

## 计费范围
目前 AI 增强能力仅先支持智能路由，后续能力将陆续支持，具体可用能力以产品控制台展示为准。
<table> <thead> <tr> <td><p><b>能力</b></p></td> <td><p><b>是否消耗 Credits</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>智能路由</p></td> <td><p>是</p></td> </tr> <tr> <td><p>普通 LLM API 代理透传</p></td> <td><p>否</p></td> </tr> <tr> <td><p>自定义模型服务调用</p></td> <td><p>否，由对应模型服务或模型提供方收取</p></td> </tr> </tbody> </table>

只有当请求实际触发 AI 增强能力时才产生 Credits 消耗。普通代理转发请求不消耗 Credits，模型 Token 费用不计入 AI Credits。

## 计费方式
```
HELPCODEESCAPE-plaintext
AI Credits 费用 = 实际消耗的 Credits 数量 × 0.01 元/Credit
```

Credits 消耗量与实际使用的 AI 增强能力类型和用量相关，不设置包量，各实例类型的 Credits 计费规则一致。

您可以在费用与成本相关页面查看 AI Credits 的消耗量、对应的 AI 增强能力类型和账单金额。

## 注意事项
* 公测期间的计费优惠请以公测公告和产品控制台展示为准。

* 实际计费项、价格和账单口径以官网价格页、产品控制台和账单展示为准。
