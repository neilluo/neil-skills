---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-an-api-product-of-the-model-api-type
fetch_date: 2026-09-21
product: AI Gateway
slug: create-an-api-product-of-the-model-api-type
body_sha256: 282b0755bd57dc5876f78a1c16c8e1e1e9001316c7c9ea466cad904c8eb0c2c0
body_bytes: 3196
migration_status: current
---

Model API 提供大语言模型的调用能力。本文介绍如何将 Model API 封装为 API 产品，发布到开发者门户，供开发者浏览和订阅。  

## 前提条件
已创建 Model API，详见[管理Model API](https://help.aliyun.com/document_detail/2859333.html)

已创建开发者门户。详见[创建门户](https://help.aliyun.com/document_detail/3030781.html)。

## 创建 API 产品
1. 登录开放平台控制台。

2. 在左侧导航栏，选择 **API 产品**。

3. 单击 **创建 API 产品**。

4. 在创建面板，填写产品基本信息。

   <table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>产品名称</p></td> <td><p>产品的唯一标识，例如 <code>model-api-product</code>。必填。</p></td> </tr> <tr> <td><p>产品描述</p></td> <td><p>简要描述产品的功能和用途。必填。</p></td> </tr> <tr> <td><p>产品类型</p></td> <td><p>选择 <b>Model API</b>。必填。</p></td> </tr> <tr> <td><p>产品类别</p></td> <td><p>选择产品类别，支持自定义。选填。</p></td> </tr> <tr> <td><p>自动订阅审批</p></td> <td><p>开启后，开发者的订阅申请将自动通过。门户和 API 产品均可配置此选项，API 产品的配置优先级更高。</p></td> </tr> <tr> <td><p>产品图标</p></td> <td><p>可使用 URL 链接或上传本地文件。选填。</p></td> </tr> </tbody> </table>
5. 配置模型参数。

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Model</p></td> <td><p>模型名称，例如 <code>qwen-turbo</code>。</p></td> </tr> <tr> <td><p>Max Tokens</p></td> <td><p>最大生成令牌数，控制返回内容的长度。</p></td> </tr> <tr> <td><p>Temperature</p></td> <td><p>采样温度，控制生成内容的随机性，取值范围 0～2。</p></td> </tr> <tr> <td><p>支持联网搜索</p></td> <td><p>是否启用 Web Search 能力。</p></td> </tr> </tbody> </table>  
   **说明**

   模型参数用于 HiMarket 前台调试模型时使用，参数缺失可能导致模型调用失败，请确保配置完整。
6. 单击 **确定**，完成创建。

## 关联 API
API 产品必须关联具体的 AI API 后才能发布到门户。

1. 在 API 产品详情页，单击 **关联 API**。

2. 选择网关实例和 Model API。

3. 单击 **关联**。

关联成功后，产品状态变为 **待发布**，页面会显示 Model API 的路由信息。

## 编写使用指南
使用指南帮助开发者快速了解和使用 API 产品。一份完善的指南应包含产品介绍、接口说明、调用示例等内容，能有效降低开发者的上手成本。

1. 在 API 产品详情页，单击 **使用指南** 页签。

2. 使用 Markdown 编辑器编写文档，或上传已有的 Markdown 文件。

3. 单击 **保存**。

## 发布到门户
1. 确认产品状态为 **待发布**。

2. 单击 **发布到门户**。

3. 选择目标门户。

4. 单击 **发布**。

发布后，开发者即可在门户中浏览和订阅该产品。