---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/authorization-management
fetch_date: 2026-09-21
product: AI Gateway
slug: authorization-management
body_sha256: 4a06d6f6bc48266904b359d8c1984e74f3888286414527ccfa9023ef3d64342d
body_bytes: 2999
migration_status: current
---

本文介绍如何通过对API消费者进行授权管理，确保只有经过身份验证和权限校验的请求才能访问服务资源。  

## 授权消费者
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**消费者**，并在顶部菜单栏选择地域。

3. 在**消费者** 页面，单击目标消费者进入详情页，选择消**费者授权**页签。

4. 支持Model API授权和MCP授权两种。

   ## 授权Model API
   --------------

   1. 选择**Model API** 页签，单击**授权**。

   2. 在授权面板中，配置相关参数，单击**确定**。

      <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>生效网关实例</b></p></td> <td><p>选择生效的云原生网关实例。</p></td> </tr> <tr> <td><p><b>选择API</b></p></td> <td><p>选择需要授权的Model API。</p></td> </tr> <tr> <td><p><b>可选API</b></p></td> <td><p>展示发布至此网关的可选API。</p></td> </tr> <tr> <td><p><b>已选API</b></p></td> <td><p>已勾选的API列表。单击目标API右侧的<b>查看</b>，查看详情信息。</p></td> </tr> </tbody> </table>

   ## 授权MCP
   --------

   1. 选择**MCP** 页签，单击**授权**。

   2. 在授权面板中，配置相关参数，单击**确定**。

      <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>生效网关实例</b></p></td> <td><p>选择生效的云原生网关实例。</p></td> </tr> <tr> <td><p><b>选择MCP服务</b></p></td> <td><p>选择需要授权MCP服务。</p></td> </tr> <tr> <td><p><b>可选MCP服务</b></p></td> <td><p>展示发布至此网关的可选MCP服务。</p></td> </tr> <tr> <td><p><b>已选MCP服务</b></p></td> <td><p>已勾选的MCP服务。单击目标MCP服务右侧的<b>查看</b>，查看详情信息。</p></td> </tr> </tbody> </table>

## 解除授权
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**消费者**，并在顶部菜单栏选择地域。

3. 在**消费者** 页面，单击目标消费者进入详情页，单击**消费者授权**。

4. 支持Model API解除授权和MCP解除授权两种。

   ## Model API解除授权
   ----------------

   1. 选择**Model API**页签。

   2. 单击目标API右侧**操作** 列下的**解除授权** ，然后在确认解除对话框中单击**解除**。

   ## MCP解除授权
   ----------

   1. 选择**MCP**页签。

   2. 单击目标服务右侧**操作** 列下的**解除授权** ，然后在确认解除对话框中单击**解除**。

## 相关文档
消费者如何通过认证和鉴权实现安全访问。具体详情，请参见[消费者认证鉴权](https://help.aliyun.com/document_detail/2882285.html)。