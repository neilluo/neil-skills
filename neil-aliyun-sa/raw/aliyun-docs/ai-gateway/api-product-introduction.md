---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/api-product-introduction
fetch_date: 2026-09-21
product: AI Gateway
slug: api-product-introduction
body_sha256: 0f2df82afdf66f1be350164a1bfee7803165a73803645d8c250a16ea6cf32389
body_bytes: 1697
migration_status: current
---

将底层 AI API 能力封装为标准化产品，管理员可以将 MCP Server、Model API、Agent API 打包后发布到门户，供开发者浏览和订阅。  

## 什么是 API 产品
API 产品是 AI 网关开放平台的核心概念，用于将底层的 AI API 能力封装为标准化产品，供开发者订阅和使用。

管理员可以将已有的 MCP Server、Model API、Agent API 等打包成 API 产品，搭配产品使用文档后发布到门户。登录门户的开发者即可浏览并订阅所需的 API 产品。

## API 产品类型
目前开放平台支持以下三种 API 产品类型：
<table> <thead> <tr> <td><p><b>产品类型</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>MCP Server</p></td> <td><p>将 MCP Server 封装为标准化 API 产品，供开发者订阅调用。</p></td> </tr> <tr> <td><p>Model API</p></td> <td><p>将模型 API 封装为标准化 API 产品，提供统一的调用入口。</p></td> </tr> <tr> <td><p>Agent API</p></td> <td><p>将 Agent API 封装为标准化 API 产品，便于开发者集成到业务场景中。</p></td> </tr> </tbody> </table>

## 产品生命周期
API 产品的生命周期包含以下状态：
<table> <thead> <tr> <td><p><b>状态</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>待配置</p></td> <td><p>刚创建，需要关联 API。</p></td> </tr> <tr> <td><p>待发布</p></td> <td><p>已关联 API，可以发布到门户。</p></td> </tr> <tr> <td><p>已发布</p></td> <td><p>已发布到门户，开发者可订阅。</p></td> </tr> </tbody> </table>