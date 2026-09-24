---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-certification
fetch_date: 2026-09-21
product: AI Gateway
slug: consumer-certification
body_sha256: 8004271da85dc4310a73372a051875f9e3339dbb96d660adb1eaf318cfa7a836
body_bytes: 3208
migration_status: current
---

AI 网关支持为MCP服务和MCP工具配置消费者认证。通过API key的认证方式验证调用者的身份，精准控制 API 访问权限，实现多租户细粒度管控，保障敏感数据隔离与合规调用，有效防止未授权访问和资源滥用。本文为您介绍如何配置消费者认证。  

## **配置说明**
* 消费者认证支持以下场景：

  * 网关自建HTTP转MCP。

  * 网关自建MCP服务直接代理。

  * Nacos 托管HTTP转MCP。

  * Nacos托管代理MCP 服务。

* **MCP服务级别消费者认证权限高于MCP工具级别**。

## 配置MCP服务级别消费者认证
1. 打开[AI网关控制台实例页面](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择实例所在的地域，并单击目标实例ID。

2. 单击左侧导航栏的**MCP管理** 。然后单击目标服务卡片，然后单击**消费者认证**页签。

3. 单击**配置信息** 右侧的**编辑** ，然后在弹出的**MCP 服务消费者认证** 菜单中打开**启用状态** ，并单击**确定** **。**

   **重要**
   * 开启消费者认证后，若没有配置授权关系，将无法访问当前API。

   * 认证方式目前仅支持**API Key**认证。

     > API Key是一种简单的认证方式，客户端访问时，需将凭证以指定的方式添加至请求中，网关收到请求后会验证API Key的合法性及权限。API Key常用于不涉及敏感操作的简单场景，安全性相比JWT、AK/SK较低，请注意凭证的管理与保护。
4. 在**MCP** 页签单击**授权** ，并在**添加消费者授权** 面板中选择消费者。完成后单击**添加**。

   **说明**

   若没有消费者，您可在此页面单击**消费者** 右侧的输入框，并在下拉菜单中单击[创建消费者](https://help.aliyun.com/document_detail/2882031.html)进行创建。

## 配置MCP工具级别消费者认证
1. 打开[AI网关控制台实例页面](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择实例所在的地域，并单击目标实例ID。

2. 单击左侧导航栏的**MCP管理** 。然后单击目标服务卡片，然后单击**消费者认证**页签。

3. 单击**配置信息** 右侧的**编辑** ，然后在弹出的**MCP 服务消费者认证** 菜单中打开**启用状态** ，并单击**确定** **。**

   **重要**
   * 开启消费者认证后，若没有配置授权关系，将无法访问当前API。

   * 认证方式目前仅支持**API Key**认证。

     > API Key是一种简单的认证方式，客户端访问时，需将凭证以指定的方式添加至请求中，网关收到请求后会验证API Key的合法性及权限。API Key常用于不涉及敏感操作的简单场景，安全性相比JWT、AK/SK较低，请注意凭证的管理与保护。
4. 单击**MCP工具** ，然后在**MCP工具** 页签单击**授权** ，并在**添加消费者授权** 面板中选择消费者和工具。完成后单击**添加**。

   **说明**

   若没有消费者，您可在此页面单击**消费者** 右侧的输入框，并在下拉菜单中单击[创建消费者](https://help.aliyun.com/document_detail/2882031.html)进行创建。