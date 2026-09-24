---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-fallback
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-fallback
body_sha256: e1b61d2c7127fe04394e03d3ba240907312662b2cb7d162503fd26f08e9b7b01
body_bytes: 3414
migration_status: current
---

当Model API的模型服务因异常、故障或高负载而无法正常响应时，通过配置Fallback切换到备用模型，有效避免因模型服务中断导致的响应失败问题。本文将介绍如何为Model API开启和配置Fallback。  

## **什么是AI Fallback**
AI Fallback 是指Model API在主模型服务不可用时Fallback到备用模型，从而提升Model API的可用性，避免因为某个模型服务的异常或者高负载造成的请求不可用。

Model API 支持多级Fallback，启用并合理的配置Fallback， 可有效提升AI请求的成功率。典型场景示例如下：

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8958334471/p940026.jpeg)

AI 网关支持配置一到多个Fallback模型，当主模型服务不可用时，网关将会按顺序调用Fallback模型服务，如果调用成功，则会立即返回。

Fallback 模型包含如下配置项：

* [服务名称](#8f11299f6edij)：备用模型服务的名称，从该实例下的服务列表中选择。

* [模型名称](#0c436a29c63bn)：支持透传和指定具体模型的名称，如 Qwen-plus。

## 触发条件
当调用模型服务，返回任意 HTTP 4xx、5xx 错误状态码时，均会触发 AI Fallback。

## 前提条件
* 已[创建网关实例](https://help.aliyun.com/document_detail/2796788.html)。

* 已[创建服务](https://help.aliyun.com/document_detail/2796820.html)。

## 配置AI Fallback
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API**。可在创建或者编辑Model API时开启Fallback。

   * [创建Model API](https://help.aliyun.com/document_detail/2859333.html#9d7f312e31snz)：单击**创建API** ，在Model API 的配置页面，开启**Fallback**。

   * [编辑Model API](https://help.aliyun.com/document_detail/2859333.html#709a9c0ec6ihh)：单击目标API**操作** 列的**编辑** ，在Model API 的配置页面，开启**Fallback**。

   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Fallback</b></p></td> <td><p>开启后可添加Fallback服务，按照降序执行。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>Fallback服务支持重复使用同一个服务组建多条策略。</p> </div> </div></td> </tr> <tr> <td><p><b>仅Fallback后端服务错误</b></p></td> <td><p>开启后，仅当后端服务返回错误时才会触发Fallback机制。</p><p>如果不开启，则当请求被网关限流或者其它形式拦截时同样会触发Fallback。</p></td> </tr> <tr> <td><p><b>Fallback列表</b></p></td> <td><p><b>服务名称</b></p></td> <td><p>选择Fallback服务名称。</p></td> </tr> <tr> <td><p><b>模型名称</b></p></td> <td><p>默认为透传。将请求中的模型名称直接传递给Fallback模型服务。</p></td> </tr> <tr> <td><p><b>首包超时</b></p></td> <td><p>流式传输中首个响应包的超时时间，单位为毫秒。首包超时仅对流式响应生效，设为0时代表不启用，当设置首包超时为非0时，对于首包响应过慢的请求网关将会fallback至兜底服务。</p></td> </tr> </tbody> </table>