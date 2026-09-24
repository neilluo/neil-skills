---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/enable-gateway-link-tracing
fetch_date: 2026-09-21
product: AI Gateway
slug: enable-gateway-link-tracing
body_sha256: fe545d01f9ae6715549747bce704c39adf01d74092426fedd6a88615965a41cf
body_bytes: 2045
migration_status: current
---

AI 网关支持集成阿里云链路追踪Tracing Analysis服务和Skywalking服务，帮助您定位性能瓶颈，提升微服务开发诊断效率。本文介绍如何开启链路追踪以实现可观测性。  

## 前提条件
* [已创建AI 网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 已开通阿里云链路追踪，若未开通，请使用阿里云账号登录[阿里云链路追踪服务](https://tracing-analysis.console.aliyun.com/#/overview)控制台进行开通。

## 开启链路追踪
**说明**

AI 网关本身不收取链路追踪费用，但如果您使用了链路追踪Tracing Analysis服务，链路追踪Tracing Analysis产品将根据您的使用量进行收费。具体收费详情请以[链路追踪Tracing Analysis价格说明](https://www.aliyun.com/price/product?spm=5176.24342065.commonbuy2container.14.1758778bQ6qjsS#/xtrace/detail/xtrace)为准。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. AI 网关提供了两种开启链路追踪方式。

   ##### **方式一：通过链路追踪**

   1. 在左侧导航栏，单击**观测分析** \> **链路追踪**。

   2. 单击**开启链路追踪** ，在**链路追踪配置** 对话框，开启**链路追踪状态** ，选择**链路追踪协议** 和**采样率** ，然后单击**确定**。

   ##### **方式二：通过参数配置**

   1. 在左侧导航栏，单击**参数配置**。

   2. 在**可观测性参数** 区域，单击**链路追踪** 右侧的![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7494848561/p469718.png)图标，在**链路追踪配置** 对话框，开启**链路追踪状态** ，选择**链路追踪协议** 和**采样率** ，然后单击**确定**。

      开启链路追踪后，可以在网关实例中的**观测分析** \> **链路追踪**中查看网关链路追踪数据。