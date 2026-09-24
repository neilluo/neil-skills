---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/mcp-server-product
fetch_date: 2026-09-21
product: AI Gateway
slug: mcp-server-product
body_sha256: 2378494af37783dfb1d3bcb31351ef7195c4d39d6702e69610f93c43dc107144
body_bytes: 2624
migration_status: current
---

通过开放平台，可以将已创建的 MCP Server 封装为 API 产品并发布到开发者门户，供开发者浏览和订阅。本文介绍创建 MCP Server 类型 API 产品的完整流程。  

## 创建 API 产品
开始创建前，需已完成以下操作：

* 创建 MCP Server，详见[管理 MCP](https://help.aliyun.com/document_detail/2930330.html)。

* 创建开发者门户，详见[创建门户](https://help.aliyun.com/document_detail/3030781.html)。

登录[开放平台控制台](https://apig.console.aliyun.com/cn-hangzhou/open-platform#/cn-hangzhou/open-platform/api-product)，在左侧导航栏选择 **API 产品** ，然后单击 **创建 API 产品**。

在创建面板中填写产品信息。
<table> <thead> <tr> <td><p><b>字段</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>产品名称</p></td> <td><p>产品的唯一标识，例如 <code>api-product</code>。必填。</p></td> </tr> <tr> <td><p>产品描述</p></td> <td><p>简要描述产品功能和用途。必填。</p></td> </tr> <tr> <td><p>产品类型</p></td> <td><p>选择 <b>MCP Server</b>。必填。</p></td> </tr> <tr> <td><p>产品分类</p></td> <td><p>选择产品类别，支持自定义。选填。</p></td> </tr> <tr> <td><p>自动审批订阅</p></td> <td><p>开启后，开发者的订阅申请将自动通过。门户和 API 产品均可配置此选项，API 产品的配置优先级更高。</p></td> </tr> <tr> <td><p>产品图标</p></td> <td><p>选择产品图标，可使用 URL 链接或上传本地文件。选填。</p></td> </tr> </tbody> </table>

填写完成后，单击 **确定** 完成创建。

## 关联 API
API 产品必须关联具体的 API 后才能发布到门户。

1. 在 API 产品详情页，单击 **关联 API**。

2. 选择目标网关实例和 MCP Server。

3. 单击 **关联**。

关联成功后，产品状态变更为 **待发布**，页面将显示 MCP Server 的连接点信息。

## 编写使用指南
使用指南帮助开发者快速了解和使用 API 产品。一份完善的使用指南应包含产品介绍、接口说明、调用示例等内容，能有效降低开发者的上手门槛。

1. 在 API 产品详情页，单击 **使用指南** 页签。

2. 使用 Markdown 编辑器编写文档，或上传已有的 Markdown 文件。

3. 单击 **保存**。

## 发布到门户
1. 确认产品状态为 **待发布**。

2. 单击 **发布到门户**。

3. 选择目标门户。

4. 单击 **发布**。

发布完成后，开发者即可在门户中浏览和订阅该 API 产品。