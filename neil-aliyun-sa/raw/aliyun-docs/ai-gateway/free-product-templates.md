---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/free-product-templates
fetch_date: 2026-09-21
product: AI Gateway
slug: free-product-templates
body_sha256: 083c603775369cd6f5f9ea026f487f9de767d098650bbab611fe98d521b3fb17
body_bytes: 7573
migration_status: current
---

AI 网关专享实例采用独占物理资源的部署形态，适合对性能和隔离性有较高要求的场景。本文介绍专享实例的计费项及定价，便于评估使用成本。  

## 计费方式
AI 网关专享实例支持以下计费方式：

* 按量付费（后付费）：计费以小时为单位，不足 1 小时按照 1 小时计算。每小时结算一次，每 24 小时出一次账单，费用自动从阿里云账户余额中扣除。

* 包年包月（预付费）：计费以月为单位，包年按照 12 个月计算。费用自动从阿里云账户余额中扣除。

## 计费项
专享实例的计费项由以下三部分组成：
<table> <thead> <tr> <td><p><b>计费项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>实例费用</p></td> <td><p>根据所选实例规格和地域，按小时或按月收取</p></td> </tr> <tr> <td><p>数据处理量费用</p></td> <td><p>根据请求和响应的数据量，按 GB 收取</p></td> </tr> <tr> <td><p>公网流量费用</p></td> <td><p>通过云数据传输 CDT 统一计费</p></td> </tr> </tbody> </table>

## 实例费用
实例费用根据所选地域和实例规格确定。
<table> <thead> <tr> <td><p><b>地域</b></p></td> <td><p><b>实例规格</b></p></td> <td><p><b>按量付费单价（元/小时）</b></p></td> <td><p><b>包年包月单价（元/月）</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>中国内地（不含中国香港、中国澳门、中国台湾）</p></td> <td><p>aigw.small.x1</p></td> <td><p>7.9335</p></td> <td><p>3,997.5</p></td> </tr> <tr> <td><p>aigw.small.x2</p></td> <td><p>15.1782</p></td> <td><p>7,650.6</p></td> </tr> <tr> <td><p>aigw.small.x4</p></td> <td><p>28.7287</p></td> <td><p>14,477.1</p></td> </tr> <tr> <td><p>aigw.medium.x1</p></td> <td><p>56.1</p></td> <td><p>28,276</p></td> </tr> <tr> <td><p>aigw.medium.x2</p></td> <td><p>110.484</p></td> <td><p>55,684</p></td> </tr> <tr> <td><p>aigw.medium.x3</p></td> <td><p>164.864</p></td> <td><p>83,092</p></td> </tr> <tr> <td><p>aigw.large.x1</p></td> <td><p>213.7668</p></td> <td><p>107,737.5</p></td> </tr> <tr> <td><p>aigw.large.x2</p></td> <td><p>425.8527</p></td> <td><p>214,628.7</p></td> </tr> <tr> <td><p>aigw.large.x3</p></td> <td><p>637.9425</p></td> <td><p>321,523.8</p></td> </tr> <tr> <td><p>金融云</p></td> <td><p>aigw.small.x1</p></td> <td><p>15.07365</p></td> <td><p>7,595.25</p></td> </tr> <tr> <td><p>aigw.small.x2</p></td> <td><p>28.83858</p></td> <td><p>14,536.14</p></td> </tr> <tr> <td><p>aigw.small.x4</p></td> <td><p>54.58453</p></td> <td><p>27,506.49</p></td> </tr> <tr> <td><p>aigw.medium.x1</p></td> <td><p>106.59</p></td> <td><p>53,724.4</p></td> </tr> <tr> <td><p>aigw.medium.x2</p></td> <td><p>209.9196</p></td> <td><p>105,799.6</p></td> </tr> <tr> <td><p>aigw.medium.x3</p></td> <td><p>313.2416</p></td> <td><p>157,874.8</p></td> </tr> <tr> <td><p>aigw.large.x1</p></td> <td><p>406.15692</p></td> <td><p>204,701.25</p></td> </tr> <tr> <td><p>aigw.large.x2</p></td> <td><p>809.12013</p></td> <td><p>407,794.53</p></td> </tr> <tr> <td><p>aigw.large.x3</p></td> <td><p>1,212.09075</p></td> <td><p>610,895.22</p></td> </tr> <tr> <td><p>中国香港、日本（东京）</p></td> <td><p>aigw.small.x1</p></td> <td><p>11.9023</p></td> <td><p>5,996.25</p></td> </tr> <tr> <td><p>aigw.small.x2</p></td> <td><p>22.7673</p></td> <td><p>11,475.9</p></td> </tr> <tr> <td><p>aigw.small.x4</p></td> <td><p>43.0951</p></td> <td><p>21,715.65</p></td> </tr> <tr> <td><p>aigw.medium.x1</p></td> <td><p>84.152</p></td> <td><p>42,414</p></td> </tr> <tr> <td><p>aigw.medium.x2</p></td> <td><p>165.728</p></td> <td><p>83,526</p></td> </tr> <tr> <td><p>aigw.medium.x3</p></td> <td><p>247.296</p></td> <td><p>124,638</p></td> </tr> <tr> <td><p>aigw.large.x1</p></td> <td><p>320.6502</p></td> <td><p>161,606.25</p></td> </tr> <tr> <td><p>aigw.large.x2</p></td> <td><p>638.7771</p></td> <td><p>321,943.05</p></td> </tr> <tr> <td><p>aigw.large.x3</p></td> <td><p>956.9157</p></td> <td><p>482,285.7</p></td> </tr> <tr> <td><p>新加坡、印度尼西亚（雅加达）、德国（法兰克福）</p></td> <td><p>aigw.small.x1</p></td> <td><p>10.947</p></td> <td><p>5,516.55</p></td> </tr> <tr> <td><p>aigw.small.x2</p></td> <td><p>20.9469</p></td> <td><p>10,557.828</p></td> </tr> <tr> <td><p>aigw.small.x4</p></td> <td><p>39.647</p></td> <td><p>19,978.398</p></td> </tr> <tr> <td><p>aigw.medium.x1</p></td> <td><p>77.42</p></td> <td><p>39,020.88</p></td> </tr> <tr> <td><p>aigw.medium.x2</p></td> <td><p>152.468</p></td> <td><p>76,843.92</p></td> </tr> <tr> <td><p>aigw.medium.x3</p></td> <td><p>227.512</p></td> <td><p>114,666.96</p></td> </tr> <tr> <td><p>aigw.large.x1</p></td> <td><p>294.9999</p></td> <td><p>148,677.75</p></td> </tr> <tr> <td><p>aigw.large.x2</p></td> <td><p>587.6754</p></td> <td><p>296,187.606</p></td> </tr> <tr> <td><p>aigw.large.x3</p></td> <td><p>880.3626</p></td> <td><p>443,702.844</p></td> </tr> <tr> <td><p>美国（弗吉尼亚）、美国（硅谷）</p></td> <td><p>aigw.small.x1</p></td> <td><p>9.5202</p></td> <td><p>4,797</p></td> </tr> <tr> <td><p>aigw.small.x2</p></td> <td><p>18.2122</p></td> <td><p>9,180.72</p></td> </tr> <tr> <td><p>aigw.small.x4</p></td> <td><p>34.4728</p></td> <td><p>17,372.52</p></td> </tr> <tr> <td><p>aigw.medium.x1</p></td> <td><p>67.32</p></td> <td><p>33,931.2</p></td> </tr> <tr> <td><p>aigw.medium.x2</p></td> <td><p>132.58</p></td> <td><p>66,820.8</p></td> </tr> <tr> <td><p>aigw.medium.x3</p></td> <td><p>197.836</p></td> <td><p>99,710.4</p></td> </tr> <tr> <td><p>aigw.large.x1</p></td> <td><p>256.5186</p></td> <td><p>129,285</p></td> </tr> <tr> <td><p>aigw.large.x2</p></td> <td><p>511.0248</p></td> <td><p>257,554.44</p></td> </tr> <tr> <td><p>aigw.large.x3</p></td> <td><p>765.531</p></td> <td><p>385,828.56</p></td> </tr> </tbody> </table>

## 数据处理量费用
创建 AI 网关专享实例时，可选择的网络类型包括公网、私网、公网+私网。不同网络类型的数据处理量单独计费。在一个计费周期内，数据处理量为请求和响应的数据量之和。

### 数据处理量单价

<table> <thead> <tr> <td><p><b>地域</b></p></td> <td><p><b>网络类型</b></p></td> <td><p><b>单价（元/GB/小时）</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>公共云</p></td> <td><p>公网</p></td> <td><p>0.037</p></td> </tr> <tr> <td><p>私网</p></td> <td><p>0.049</p></td> </tr> <tr> <td><p>金融云</p></td> <td><p>公网</p></td> <td><p>0.07</p></td> </tr> <tr> <td><p>私网</p></td> <td><p>0.093</p></td> </tr> </tbody> </table>

### 计费公式

* 公网：单位小时费用 = 数据处理量 × 单价。

  例如：使用网关实例 2 小时，第一个小时产生了 5 GB 数据量，第二个小时产生了 10 GB 数据量，那么 2 小时的数据处理量总费用为 0.037×5 + 0.037×10 = 0.555 元。
* 私网：单位小时费用 = 数据处理量 × 单价。

  例如：使用网关实例 2 小时，第一个小时产生了 5 GB 数据量，第二个小时产生了 10 GB 数据量，那么 2 小时的数据处理量总费用为 0.049×5 + 0.049×10 = 0.735 元。

## 公网流量费用
公网流量通过[云数据传输CDT](https://help.aliyun.com/document_detail/2357716.html)统一计费和出账，定价详情参见[CDT公网流量定价](https://help.aliyun.com/document_detail/410942.html)。