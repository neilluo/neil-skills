---
source_url: https://help.aliyun.com/zh/agentcore/model-management
fetch_date: 2026-09-20
product: AgentCore
slug: model-management
body_sha256: 479519ca2f7fd54455a7770887f36a7c49720725e786bb81a8b63a2c3c379be9
body_bytes: 5022
migration_status: current   # 见 FETCH-CONTRACT §3
---

Agent 运行依赖模型配置。模型管理功能支持接入多个 AI 模型供应商，统一管理 API 端点和认证信息，并在正式使用前验证模型可用性。  

## **添加模型连接**
1. 登录 AgentCore [控制台](https://agentcore.console.aliyun.com/)。

2. 在详情页左侧导航栏，点击**模型连接**。

3. 点击**模型列表**标签页。

4. 点击**添加模型连接**。

5. 配置模型基本信息。

   1. 选择预制模型供应商或自定义模型供应商。

   2. 输入模型连接名称。

   3. 若选择自定义模型供应商，请配置API端点。

   4. 输入访问凭证，目前仅支持手动输入API Key。

6. 在**模型配置**下选择需要的模型。

7. 点击**确定**完成模型添加。

## 管理模型
### 查看模型详情

点击**详情**可查看模型基本信息。

#### **基本信息**

<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>模型名称</p> </td> <td> <p>模型的名称，例如 qwen3.8-max。</p> </td> </tr> <tr> <td> <p>模型 ID</p> </td> <td> <p>系统为模型分配的唯一标识。</p> </td> </tr> <tr> <td> <p>所属模型连接</p> </td> <td> <p>模型所属的模型连接 ID。</p> </td> </tr> <tr> <td> <p>模型供应商</p> </td> <td> <p>模型的供应商，例如阿里云百炼。</p> </td> </tr> <tr> <td> <p>协议</p> </td> <td> <p>模型调用使用的接口协议，例如 OpenAI/v1。</p> </td> </tr> <tr> <td> <p>创建时间</p> </td> <td> <p>模型接入的时间。</p> </td> </tr> </tbody> </table>

#### **模型能力**

展示该模型支持的能力，各项标注为支持或不支持。
<table> <thead> <tr> <td> <p>能力</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>工具调用</p> </td> <td> <p>模型是否支持调用工具。</p> </td> </tr> <tr> <td> <p>多工具调用</p> </td> <td> <p>模型是否支持在一次请求中调用多个工具。</p> </td> </tr> <tr> <td> <p>流式工具调用</p> </td> <td> <p>模型是否支持以流式方式调用工具。</p> </td> </tr> <tr> <td> <p>视觉</p> </td> <td> <p>模型是否支持图片输入。</p> </td> </tr> <tr> <td> <p>音频</p> </td> <td> <p>模型是否支持音频输入。</p> </td> </tr> <tr> <td> <p>视频</p> </td> <td> <p>模型是否支持视频输入。</p> </td> </tr> <tr> <td> <p>文档</p> </td> <td> <p>模型是否支持文档输入。</p> </td> </tr> <tr> <td> <p>推理</p> </td> <td> <p>模型是否支持推理。</p> </td> </tr> </tbody> </table>

#### **调用参数**

<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>上下文长度</p> </td> <td> <p>模型单次请求可处理的最大 Token 数。</p> </td> </tr> <tr> <td> <p>单次最大输出</p> </td> <td> <p>模型单次响应可输出的最大 Token 数。</p> </td> </tr> <tr> <td> <p>流式输出</p> </td> <td> <p>模型是否支持流式返回结果。</p> </td> </tr> </tbody> </table>

### 调试模型

点击**调试**可测试模型输出。

### 删除模型

点击**删除**来删除模型，

## 管理模型连接
### 查看模型详情

点击**详情**可查看模型基本信息。

## 基本信息
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>模型供应商</p> </td> <td> <p>模型连接对接的供应商，例如阿里云百炼。</p> </td> </tr> <tr> <td> <p>API 端点</p> </td> <td> <p>供应商提供的模型调用地址，例如\&nbsp;v1 · dashscope.aliyuncs.com。</p> </td> </tr> <tr> <td> <p>协议</p> </td> <td> <p>模型调用使用的接口协议，例如 OpenAI/v1。</p> </td> </tr> </tbody> </table>

## 模型配置
模型配置区域展示该连接下已接入的模型，按模型类型分组，分组标签后的数字为该类型下的模型数量。区域右上角可切换卡片视图与列表视图。

每个模型展示以下信息：
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>模型名称</p> </td> <td> <p>模型的名称，例如 qwen3.8-max。</p> </td> </tr> <tr> <td> <p>上下文长度</p> </td> <td> <p>模型单次请求可处理的最大 Token 数，例如 1 m 表示 100 万 Tokens。</p> </td> </tr> <tr> <td> <p>模型能力</p> </td> <td> <p>该模型支持的能力标签，例如工具调用、多工具调用、流式工具调用、视觉、视频、推理；不支持的能力不展示标签。</p> </td> </tr> </tbody> </table>

单击模型名称可进入模型详情页，查看模型 ID、创建时间与完整的能力与调用参数。

### 调试模型

点击**调试**可测试模型连接输出。

### 删除模型

点击**删除**来删除模型连接。