---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/proxy-comfyui-service-via-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: proxy-comfyui-service-via-ai-gateway
body_sha256: 7e229a0c7a7fd9842d936b6dae05d429fd165067f8eb5c1d3b8fc51d698b3748
body_bytes: 1142
migration_status: current
---

本文介绍如何使用AI网关代理ComfyUI服务。  

## **前提条件**
**创建AI网关**  
若当前无可用AI网关，请参考[创建AI网关实例](https://help.aliyun.com/document_detail/2881527.html)。

### 操作步骤

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，选择**服务** ，单击**创建服务**，服务来源根据已创建的ComfyUI服务选择并完成配置。

   **说明**

   可选：进行[设置安全组规则](https://help.aliyun.com/document_detail/2882561.html)，确保网关至目标服务网络链路畅通。
5. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

6. 在创建Model API页面中，选择图片生成，单击**创建** ，协议选择**ComfyUI**，并选择所需路由。在大模型服务的服务列表中，选择步骤4创建的服务。

7. 配置完成后，可通过AI网关接入点或配置的自定义域名，对接ComfyUI服务。