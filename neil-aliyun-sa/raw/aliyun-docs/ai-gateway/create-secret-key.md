---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-secret-key
fetch_date: 2026-09-21
product: AI Gateway
slug: create-secret-key
body_sha256: 4bbe0202c2b7b3eaeff5312ddb3c387aabaf858653f920c26b47ddd3800d18c5
body_bytes: 1900
migration_status: current
---

AI 网关提供密钥管理能力，支持密钥的创建、存储与管理。所有密钥统一托管在密钥管理服务 KMS 中，确保凭证信息的安全存储与使用。本文介绍如何在 AI 网关控制台创建密钥。  

## **前提条件**
* 已创建 KMS 实例，具体操作参考：[购买和启用 KMS 实例](https://help.aliyun.com/document_detail/480156.html)。

* 已配置 KMS 加密主密钥，具体操作参考：[管理密钥](https://help.aliyun.com/document_detail/480160.html)。

## 创建密钥
1. 前往 [AI 网关控制台](https://apig.console.aliyun.com/#/overview)。

2. 在左侧导航栏，选择**密钥**。

3. 在页面左上角，单击**创建密钥**，在创建密钥页面，配置密钥相关的参数。

   **说明**

   如果服务关联角色未授权，单击**授权** ，为 AI 网关授权服务关联角色`AliyunServiceRoleForNativeApiGwInvokeKms`，参考：[服务关联角色](https://help.aliyun.com/document_detail/2881275.html)。
   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>密钥名称</p></td> <td><p>密钥的名称。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>密钥名称不能重复，支持英文、数字、下划线 "_"，不超过 64 个字符。</p> </div> </div></td> </tr> <tr> <td><p>凭证来源</p></td> <td><p>指定密钥的存储位置，默认为 KMS。</p></td> </tr> <tr> <td><p>选择实例</p></td> <td><p>选择用于存储密钥的 KMS 实例。</p></td> </tr> <tr> <td><p>主密钥</p></td> <td><p>选择 KMS 中用于加密的主密钥。</p></td> </tr> <tr> <td><p>密钥内容</p></td> <td><p>需要加密存储的凭证信息，将被同步至 KMS 并作为凭据资源。</p></td> </tr> </tbody> </table>
4. 单击**确定**，完成密钥创建。