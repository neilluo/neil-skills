---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/synchronizing-nacos-mcp-services
fetch_date: 2026-09-21
product: AI Gateway
slug: synchronizing-nacos-mcp-services
body_sha256: 50c95c2787093a17c7cad5dc92fd023f6b884c9ffc0f5562965dd29c10a7b01b
body_bytes: 1933
migration_status: current
---

本文档介绍如何通过 MCP 协议将 Nacos 服务信息同步至 AI 网关，实现服务注册、发现与治理能力的扩展，提升多平台环境下服务管理的统一性与效率。  

## **前提条件**
* 目前只支持注册在MSE Nacos企业版3.0及以上版本中的MCP服务同步到AI网关。

  * 升级网关引擎版本至2.1.6及以上。  
  1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

  2. 进入目标实例页面，在**基本信息** 页签的**运行信息** 区域，查看网关**引擎版本**。

  3. （可选）如果不是最新版，可单击**升级至新版本**，升级到最新版。

  > 网关升级过程大约需要持续 5\~10 分钟。升级过程对短连接无损，对长连接可能会有重建过程。建议在业务低峰期执行此操作。

## 操作步骤
Nacos企业版创建的服务类型为HTTP转化MCP的MCP服务和标准MCP服务的同步操作相同，具体操作如下所示：

1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**MCP管理**。

3. 单击**同步 Nacos MCP 服务** ，选择您创建的MSE Nacos类型的[服务来源](https://help.aliyun.com/document_detail/2881570.html)。

4. 选择MCP服务所在的**Nacos 命名空间**，然后选择访问MCP 服务使用的域名，支持选择多个域名。

5. 在选择需要同步的**Nacos MCP 服务** 时，您可以通过**协议类型**区分它的后端类型。

   * mcp-sse：后端是SSE类型mcp server。

   * mcp-streamable：后端是streamable类型的mcp server。

   * http：Nacos上HTTP服务转MCP类型。

6. 同步成功后，MCP服务卡片上除了有直接代理或者HTTP转MCP的标识外，还会新增Nacos托管标识。