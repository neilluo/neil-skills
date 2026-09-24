<!-- source_url: https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/billing-overview -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-06-18 -->
<!-- summary: 云原生API网关「计费概述」官方全文：按量付费（小时）与包年包月（首购 6 折）两种模式；计费项 = 网关实例费 + 数据处理费 + 公网流量费（走 CDT）；含各地域各规格（apigw.dev.x1 / small.x1-x4 / medium.x1-x3 / large.x1-x2 等）单价表。 -->

本文介绍云原生API网关专享实例的计费项和计费价格。其中，首次购买包年包月（预付费）可享6折优惠。  

## 计费方式
云原生API网关支持以下计费方式。

* 按量付费（后付费）：在后付费模式下，计费以小时为单位，不足1小时按照1小时计算。每小时进行一次结算，每24小时出一次账单，费用自动从阿里云账户余额中扣除。具体出账时间以实际为准。

* 包年包月（预付费）：在预付费模式下，计费以月为单位，包年按照12个月计算。费用自动从您的阿里云账户余额中扣除。具体出账时间以实际为准。

## 计费项
**重要**

本文中提供的价格信息仅供参考，产品实际价格请以产品购买页为准。

云原生API网关的计费项由网关实例费用、数据处理费用、公网流量费用组成。
![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1288671871/CAEQThiBgIDwvfO7ihkiIGMzOWFhODVmYWQyNTRlOGRiODY0NmFiMjQxMzQ0OGYx4591256_20240813203946.019.svg)

### 网关实例费用

网关实例支持按量付费和包年包月两种计费模式，网关内置了阿里云网络型负载均衡SLB，您无需再单独购买负载均衡。  
**说明**

关于网关实例规格选型，具体可参见[容量说明](https://help.aliyun.com/document_detail/2796770.html)。
<table> <thead> <tr> <td><p><b>地域</b></p></td> <td><p><b>实例规格</b></p></td> <td><p><b>按量付费单价（元/小时）</b></p></td> <td><p><b>包年包月单价（元/月）</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>中国内地（不含中国香港、中国澳门、中国台湾）</p></td> <td><p>apigw.dev.x1</p></td> <td><p>0.826</p></td> <td><p>416</p></td> </tr> <tr> <td><p>apigw.small.x1</p></td> <td><p>1.935</p></td> <td><p>975</p></td> </tr> <tr> <td><p>apigw.small.x2</p></td> <td><p>3.702</p></td> <td><p>1,866</p></td> </tr> <tr> <td><p>apigw.small.x4</p></td> <td><p>7.007</p></td> <td><p>3,531</p></td> </tr> <tr> <td><p>apigw.medium.x1</p></td> <td><p>14.025</p></td> <td><p>7,069</p></td> </tr> <tr> <td><p>apigw.medium.x2</p></td> <td><p>27.621</p></td> <td><p>13,921</p></td> </tr> <tr> <td><p>apigw.medium.x3</p></td> <td><p>41.216</p></td> <td><p>20,773</p></td> </tr> <tr> <td><p>apigw.large.x1</p></td> <td><p>54.812</p></td> <td><p>27,625</p></td> </tr> <tr> <td><p>apigw.large.x2</p></td> <td><p>109.193</p></td> <td><p>55,033</p></td> </tr> <tr> <td><p>apigw.large.x3</p></td> <td><p>163.575</p></td> <td><p>82,442</p></td> </tr> <tr> <td><p>apigw.large.x4</p></td> <td><p>217.956</p></td> <td><p>109,850</p></td> </tr> <tr> <td><p>金融云</p></td> <td><p>apigw.dev.x1</p></td> <td><p>1.57</p></td> <td><p>790.4</p></td> </tr> <tr> <td><p>apigw.small.x1</p></td> <td><p>3.677</p></td> <td><p>1,852.5</p></td> </tr> <tr> <td><p>apigw.small.x2</p></td> <td><p>7.034</p></td> <td><p>3,545.4</p></td> </tr> <tr> <td><p>apigw.small.x4</p></td> <td><p>13.313</p></td> <td><p>6,708.9</p></td> </tr> <tr> <td><p>apigw.medium.x1</p></td> <td><p>26.648</p></td> <td><p>13,431.1</p></td> </tr> <tr> <td><p>apigw.medium.x2</p></td> <td><p>52.48</p></td> <td><p>26,449.9</p></td> </tr> <tr> <td><p>apigw.medium.x3</p></td> <td><p>78.31</p></td> <td><p>39,468.7</p></td> </tr> <tr> <td><p>apigw.large.x1</p></td> <td><p>104.143</p></td> <td><p>52,487.5</p></td> </tr> <tr> <td><p>apigw.large.x2</p></td> <td><p>207.467</p></td> <td><p>104,562.7</p></td> </tr> <tr> <td><p>apigw.large.x3</p></td> <td><p>310.793</p></td> <td><p>156,639.8</p></td> </tr> <tr> <td><p>apigw.large.x4</p></td> <td><p>414.116</p></td> <td><p>208,715</p></td> </tr> <tr> <td><p>中国香港、日本（东京）</p></td> <td><p>apigw.dev.x1</p></td> <td><p>1.239</p></td> <td><p>624</p></td> </tr> <tr> <td><p>apigw.small.x1</p></td> <td><p>2.903</p></td> <td><p>1,462.5</p></td> </tr> <tr> <td><p>apigw.small.x2</p></td> <td><p>5.553</p></td> <td><p>2,799</p></td> </tr> <tr> <td><p>apigw.small.x4</p></td> <td><p>10.511</p></td> <td><p>5,296.5</p></td> </tr> <tr> <td><p>apigw.medium.x1</p></td> <td><p>21.038</p></td> <td><p>10,603.5</p></td> </tr> <tr> <td><p>apigw.medium.x2</p></td> <td><p>41.432</p></td> <td><p>20,881.5</p></td> </tr> <tr> <td><p>apigw.medium.x3</p></td> <td><p>61.824</p></td> <td><p>31,159.5</p></td> </tr> <tr> <td><p>apigw.large.x1</p></td> <td><p>82.218</p></td> <td><p>41,437.5</p></td> </tr> <tr> <td><p>apigw.large.x2</p></td> <td><p>163.789</p></td> <td><p>82,549.5</p></td> </tr> <tr> <td><p>apigw.large.x3</p></td> <td><p>245.363</p></td> <td><p>123,663</p></td> </tr> <tr> <td><p>apigw.large.x4</p></td> <td><p>326.934</p></td> <td><p>164,775</p></td> </tr> <tr> <td><p>新加坡、印度尼西亚（雅加达）、德国（法兰克福）</p></td> <td><p>apigw.dev.x1</p></td> <td><p>1.14</p></td> <td><p>574.08</p></td> </tr> <tr> <td><p>apigw.small.x1</p></td> <td><p>2.67</p></td> <td><p>1,345.5</p></td> </tr> <tr> <td><p>apigw.small.x2</p></td> <td><p>5.109</p></td> <td><p>2,575.08</p></td> </tr> <tr> <td><p>apigw.small.x4</p></td> <td><p>9.67</p></td> <td><p>4,872.78</p></td> </tr> <tr> <td><p>apigw.medium.x1</p></td> <td><p>19.355</p></td> <td><p>9,755.22</p></td> </tr> <tr> <td><p>apigw.medium.x2</p></td> <td><p>38.117</p></td> <td><p>19,210.98</p></td> </tr> <tr> <td><p>apigw.medium.x3</p></td> <td><p>56.878</p></td> <td><p>28,666.74</p></td> </tr> <tr> <td><p>apigw.large.x1</p></td> <td><p>75.641</p></td> <td><p>38,122.5</p></td> </tr> <tr> <td><p>apigw.large.x2</p></td> <td><p>150.686</p></td> <td><p>75,945.54</p></td> </tr> <tr> <td><p>apigw.large.x3</p></td> <td><p>225.734</p></td> <td><p>113,769.96</p></td> </tr> <tr> <td><p>apigw.large.x4</p></td> <td><p>300.779</p></td> <td><p>151,593</p></td> </tr> <tr> <td><p>美国（弗吉尼亚）、美国（硅谷）</p></td> <td><p>apigw.dev.x1</p></td> <td><p>0.991</p></td> <td><p>499.2</p></td> </tr> <tr> <td><p>apigw.small.x1</p></td> <td><p>2.322</p></td> <td><p>1,170</p></td> </tr> <tr> <td><p>apigw.small.x2</p></td> <td><p>4.442</p></td> <td><p>2,239.2</p></td> </tr> <tr> <td><p>apigw.small.x4</p></td> <td><p>8.408</p></td> <td><p>4,237.2</p></td> </tr> <tr> <td><p>apigw.medium.x1</p></td> <td><p>16.83</p></td> <td><p>8,482.8</p></td> </tr> <tr> <td><p>apigw.medium.x2</p></td> <td><p>33.145</p></td> <td><p>16,705.2</p></td> </tr> <tr> <td><p>apigw.medium.x3</p></td> <td><p>49.459</p></td> <td><p>24,927.6</p></td> </tr> <tr> <td><p>apigw.large.x1</p></td> <td><p>65.774</p></td> <td><p>33,150</p></td> </tr> <tr> <td><p>apigw.large.x2</p></td> <td><p>131.032</p></td> <td><p>66,039.6</p></td> </tr> <tr> <td><p>apigw.large.x3</p></td> <td><p>196.29</p></td> <td><p>98,930.4</p></td> </tr> <tr> <td><p>apigw.large.x4</p></td> <td><p>261.547</p></td> <td><p>131,820</p></td> </tr> </tbody> </table>

#### **计费公式：**

* 按量付费（后付费）：单实例费用=实例规格单价\*小时。

  例如您选择的地域为中国内地，实例规格选择了apigw.small.x1，实例运行时间为5小时，那么该实例的费用为 1.935\*5=9.675 元。
* 包年包月（预付费）：单实例费用=实例规格单价\*月数。

  例如您选择的地域为中国内地，实例规格选择了apigw.small.x1，实例运行时间为1年，那么该实例的费用为 975\*12=11700 元。

### 数据处理量费用

在创建网关实例时，您可以选择的网络类型有：公网、私网、公网+私网，不同网络类型的数据处理量将单独计费。在一个计费周期内，数据处理量为请求和响应的数据量之和。
<table> <thead> <tr> <td><p><b>地域</b></p></td> <td><p><b>网络类型</b></p></td> <td><p><span><b>单价（元/GB/小时）</b></span></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>公共云</p></td> <td><p>公网</p></td> <td><p><span>0.037</span></p></td> </tr> <tr> <td><p>私网</p></td> <td><p><span>0.049</span></p></td> </tr> <tr> <td><p>金融云</p></td> <td><p>公网</p></td> <td><p><span>0.07</span></p></td> </tr> <tr> <td><p>私网</p></td> <td><p><span>0.093</span></p></td> </tr> </tbody> </table>

#### **计费公式**

* 公网：单位小时费用=数据处理量\*单价。

  例如您使用网关实例2小时，第一个小时产生了5GB数据量，第二个小时产生了10GB数据量，那么2小时的数据处理量总费用为 0.037\*5+0.037\*10=0.555 元。
* 私网：单位小时费用=数据处理量\*单价。

  例如您使用网关实例2小时，第一个小时产生了5GB数据量，第二个小时产生了10GB数据量，那么2小时的数据处理量总费用为 0.049\*5+0.049\*10=0.735 元。

### 公网流量费用

公网流量将基于[云数据传输CDT](https://help.aliyun.com/document_detail/2357716.html)进行统一计费和出账。详细信息，请参见[CDT公网流量定价](https://help.aliyun.com/document_detail/410942.html)。