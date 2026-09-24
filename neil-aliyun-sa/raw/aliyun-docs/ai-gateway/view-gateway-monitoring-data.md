---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/view-gateway-monitoring-data
fetch_date: 2026-09-21
product: AI Gateway
slug: view-gateway-monitoring-data
body_sha256: c1d528b9f1273da0afa9693199a77c910b07a3e0df4499814a94bd948905760d
body_bytes: 3186
migration_status: current
---

AI 网关支持查看网关监控数据，包括业务监控及资源监控。  

## 前提条件
* [创建网关实例](https://help.aliyun.com/document_detail/2881527.html)

* [开启网关日志投递](https://help.aliyun.com/document_detail/2882057.html)

* [开通云监控](https://help.aliyun.com/document_detail/35170.html)

## 查看网关监控分析
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**观测分析** \> **业务监控**。

5. 在**业务监控**页面可以查看以下信息：

   * **全局看板** ：**PV** 、**UV** 、**网关入流量** 、**网关出流量** 、**Method分布** 、**网关状态码分布** 、**后端服务状态码分布** 、**QPS** 、**请求成功率** 、**请求RT/ms** 、**请求分布**。

   * **灰度对比看板** ：在灰度发布场景下，可以通过选择线上服务与灰度服务进行对比，查看**QPS** 、**请求成功率** 、**请求RT/ms** 、**请求分布**对比情况。

   **说明**
   * 默认显示最近1小时数据，您可以在左上方设置时间进行筛选。

   * 开启页面右上方**自动刷新**，将自动刷新监控数据。

   * AI 网关利用日志服务进行业务监控，开启网关日志投递后可能会产生相关费用，关于日志服务的计费请参见[计费概述](https://help.aliyun.com/document_detail/259690.html)。

## 查看网关资源监控
**说明**

Serverless实例不支持资源监控。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**观测分析** \> **资源监控**。

   在**资源监控** 页面，您可以查看**网关CPU使用率(%)** 、**内存负载(B)** 、**网关内存使用率(%)** 、**网络入方向IO负载(B/s)** 、**网络出方向IO负载(B/s)** 、**磁盘Read负载(B/s)** 和**磁盘Write负载(B/s)**。

   网关 CPU 使用率为多核聚合计算值。双核场景下，一个 CPU 使用率 100%、另一个 50%，综合显示 75%。多核实例压测时 CPU 监控值不会达到 100%，属正常行为。  
   **说明**
   * 默认显示最近1小时数据，您可以在左上方设置时间进行筛选。

   * 开启页面右上方**自动刷新**，将自动刷新监控数据。

   * AI 网关免费支持查看业务监控大盘，若需监控企业大盘或导出监控数据，需开通云监控企业版。云监控企业版将根据您的使用量收费，关于云监控的计费方式，请参见[计费概述](https://help.aliyun.com/document_detail/450483.html)。

5. （可选）如需配置告警，您可以单击看板右上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3358742571/p985439.png)图标，或单击AI 网关控制台的左侧导航栏中的**告警** \> **创建报警规则**配置告警进行设置。