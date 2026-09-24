---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/reference-secret-key
fetch_date: 2026-09-21
product: AI Gateway
slug: reference-secret-key
body_sha256: 68624b3fe4f6d9bbdbbc098079c50569b2902956d7b545713c70f5a8a12b708c
body_bytes: 3303
migration_status: current
---

密钥可被应用于消费者、AI 服务、Agent 服务、MCP 服务以及插件等多种资源，用于替代原有的明文凭证信息，防止凭证泄露。本文介绍如何在相关资源中引用密钥。  

## **前提条件**
已创建密钥，如尚未创建密钥，参考[创建密钥](https://help.aliyun.com/document_detail/2978735.html#ced3de0cb2sd2)。  
**重要**

支持在 AI 网关`2.1.11`及以上版本中引用密钥。

## 在消费者中引用密钥
1. 前往 [AI 网关控制台](https://apig.console.aliyun.com/)，在左侧导航栏选择**消费者**，在顶部菜单栏选择地域。

2. 单击**创建消费者**，在创建消费者页面，配置消费者名称，认证方式选择 API Key，生成方式选择引用密钥，在绑定密钥选项中选择已有密钥。

   **说明**

   消费者凭证信息中仅 API key 认证方式支持引用密钥。

## 在 AI 服务中引用密钥
1. 前往 [AI 网关控制台](https://apig.console.aliyun.com/)，在左侧导航栏选择**实例**，在顶部菜单栏选择地域。

2. 单击目标实例 ID，选择左侧导航栏**服务** ，然后单击**创建服务**。

3. 在**创建服务** 面板中，服务来源选择AI服务，在**大模型配置**中，生成方式选择引用密钥，API Key 选择已有密钥。

## 在 Agent 服务中引用密钥
1. 前往 [AI 网关控制台](https://apig.console.aliyun.com/)，在左侧导航栏选择**实例**，在顶部菜单栏选择地域。

2. 单击目标实例 ID，选择左侧导航栏的**服务** ，然后单击**创建服务**。

3. 在**创建服务**面板中，服务来源选择Agent 服务，生成方式选择引用密钥，API Key 选择已有密钥名称。

## 在 MCP 服务中引用密钥
AI 网关直接代理的 MCP 服务支持开启后端认证，在认证配置中，可将凭证直接指定为已有密钥。

1. 登录 [AI 网关控制台](https://apig.console.aliyun.com/)，在左侧导航栏选择**实例**，在顶部菜单栏选择地域。

2. 单击目标实例 ID，创建使用场景为MCP服务直接代理的 MCP 服务，参考：[创建网关托管MCP服务](https://help.aliyun.com/document_detail/2930330.html#2ff4f3006620f)。

3. 进入 MCP 服务详情页，在基本信息页单击**配置后端服务凭证**开启认证状态，参考以下内容完成相关配置。

   1. **认证方式** ：选择 **API Key**。

   2. **凭证来源**：自定义 HTTP Header。

   3. **Header**：携带凭证的 Header 名称。

   4. **生成方式** ：选择**引用密钥**。

   5. **凭证**：选择已有的密钥名称。

## 在插件中引用密钥
在插件配置中，可以使用`$ref{secretName}`语法引用已创建的密钥，其中`secretName`为密钥名称，下面是 Key-Auth 插件的配置示例：

```
HELPCODEESCAPE-yaml
credentials: 
# 引用名为secretName的密钥
- $ref{secretName}
keys:
- apikey
- x-api-key
```

通过上述配置，可直接使用`secretName`密钥访问 AI 网关，官方插件与自定义插件均支持引用密钥。

## 查看密钥的引用详情
前往 [AI 网关控制台](https://apig.console.aliyun.com/)，在左侧导航栏选择**密钥** ，在**被引用**列点击密钥的引用次数，可查看当前密钥被哪些资源引用。