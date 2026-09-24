---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-authentication
fetch_date: 2026-09-21
product: AI Gateway
slug: consumer-authentication
body_sha256: 11cac8ddcf7d76e3aae7aaed9a3f9925d73555b0dd67de95db916076e9b305a4
body_bytes: 3379
migration_status: current
---

Model API消费者鉴权通过API key的认证方式验证调用者的身份，精准控制 API 访问权限，实现多租户细粒度管控，保障敏感数据隔离与合规调用，有效防止未授权访问和资源滥用。  

## **策略说明**
* 安全性：

  * 防止未授权访问：消费者鉴权通过验证请求者的身份（如API Key），可以有效防止未经授权的用户或系统访问敏感资源。

  * 防范恶意攻击：通过鉴权机制，可以防范爬虫攻击、接口滥用或 DDoS 攻击等恶意行为。

* 多租户数据隔离：在多租户系统中，消费者鉴权可以为不同租户分配独立的访问权限，确保每个租户只能访问自己的数据。

* 使用量控制：通过鉴权机制与限流策略的结合，可以对每个消费者账号配置基于Token消耗量的限流规则，确保其在配额范围内使用。

## 适用场景
* 多租户系统：在开放平台中，为不同租户分配独立的API访问权限，确保数据隔离和安全性。

* 开放平台：为第三方开发者提供受控的API访问权限，保障平台的安全性和稳定性。

* 内部系统调用：在微服务架构中，确保只有合法的服务能够调用特定的AI接口。

* 付费服务管理：根据用户的订阅级别或权限，控制其对高级功能或大模型的访问权限。

## 操作步骤
**说明**

启用消费者鉴权后，可针对每个消费者账号配置基于Token消耗量的限流规则。当预设的资源用量被突破时，将自动触发限流。

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**消费者认证** ，然后单击**配置信息** 右侧的**编辑** ，在弹出的**API 级消费者认证** 对话框中，打开**启用状态** 开关并选择**认证方式** 后，单击**确定** **。**

   **重要**

   开启消费者认证后，若没有配置授权关系，将无法访问当前API。
   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>启用状态</b></p></td> <td><p>开启或关闭消费者授权开关，默认关闭。</p></td> </tr> <tr> <td><p><b>认证方式</b></p></td> <td><p>消费者授权的认证方式目前支持两种：<b>API Key</b>、<b>JWT</b>。</p> <ul> <li><p>API Key是一种简单的认证方式，客户端访问时，需将凭证以指定的方式添加至请求中，网关收到请求后会验证API Key的合法性及权限。</p></li> <li><p>JSON Web Token (JWT) 用于在客户端和服务端之间以JSON对象的形式安全地传输信息。该信息可以被验证和信任，因为JWT使用HMAC算法、RSA或ECDSA的公钥/私钥对其进行签名。JWT认证可以在网关中验证身份并控制授权访问。</p></li> </ul></td> </tr> </tbody> </table>
4. 单击**授权** 并选择消费者，然后单击**添加**。

   若没有消费者，您可单击**消费者** 右侧的选择框，并在下拉列表中单击[创建消费者](https://help.aliyun.com/document_detail/2882031.html)进行创建。