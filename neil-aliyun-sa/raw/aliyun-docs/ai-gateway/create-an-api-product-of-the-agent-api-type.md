---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-an-api-product-of-the-agent-api-type
fetch_date: 2026-09-21
product: AI Gateway
slug: create-an-api-product-of-the-agent-api-type
body_sha256: 078a3f60dbf2882d7d4e7a8ac9327761fc4b05954a78805ef0b226e8642abfef
body_bytes: 2676
migration_status: current
---

Agent API 提供智能体应用的调用能力。通过开放平台的 API 产品管理功能，可以将 Agent API 封装为 API 产品，关联到 AI API 后发布到开发者门户，供订阅者浏览和使用。  

## 适用范围
创建 Agent API 类型的 API 产品前，需满足以下硬性条件：

1. 已创建 Agent API，详见[管理 Agent API](https://help.aliyun.com/document_detail/2937089.html)。

2. 已创建开发者门户，详见[创建门户](https://help.aliyun.com/document_detail/3030781.html)。

## 创建 Agent API 产品
按以下流程完成 API 产品的创建、API 关联、使用指南编写和门户发布。

### 创建 API 产品

1. 登录开放平台控制台。

2. 在左侧导航栏选择 **API 产品**。

3. 单击 **创建 API 产品**。

4. 填写产品信息，参数说明如下：

   <table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>产品名称</p></td> <td><p>产品的唯一标识，例如 <code>agent-api-product</code>。必填。</p></td> </tr> <tr> <td><p>产品描述</p></td> <td><p>简要描述产品的功能和用途。必填。</p></td> </tr> <tr> <td><p>产品类型</p></td> <td><p>选择 <b>Agent API</b>。必填。</p></td> </tr> <tr> <td><p>产品类别</p></td> <td><p>选择产品类别，支持自定义。选填。</p></td> </tr> <tr> <td><p>自动订阅审批</p></td> <td><p>开启后，开发者的订阅申请将自动通过。门户和 API 产品均可配置此选项，API 产品的配置优先级更高。</p></td> </tr> <tr> <td><p>产品图标</p></td> <td><p>可使用 URL 链接或上传本地文件。选填。</p></td> </tr> </tbody> </table>
5. 单击 **确定**，完成 API 产品创建。

### 关联 API

API 产品必须关联具体的 AI API 后才能发布到门户。

1. 在 API 产品列表中单击 **关联 API**。

2. 选择网关实例和 Agent API。

3. 单击 **关联**。

关联成功后，产品状态变为 **待发布**，页面会显示 Agent API 的路由信息。

### 编写使用指南

使用指南帮助开发者快速了解和使用 API 产品。一份完善的指南应包含产品介绍、接口说明、调用示例等内容，能有效降低开发者的上手门槛。

1. 单击 **使用指南** 标签。

2. 使用 Markdown 编辑器编写文档，或上传已有的 Markdown 文件。

3. 单击 **保存**。

### 发布到门户

1. 确认产品状态为 **待发布**。

2. 单击 **发布到门户**。

3. 选择目标门户。

4. 单击 **发布**。

发布后，开发者即可在门户中浏览和订阅该 API 产品。