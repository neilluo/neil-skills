---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-a-service-source
fetch_date: 2026-09-21
product: AI Gateway
slug: create-a-service-source
body_sha256: 9ea0f77bb4e616a06acb2ff2147b4f197807037a5d36f2f8afa0ad0443e98405
body_bytes: 2612
migration_status: current
---

AI网关支持添加容器服务（包括ACK与ACK Serverless集群）的服务来源。本文介绍如何将容器服务添加到AI网关服务来源中，以便网关能够动态获取您的后端服务。  

## **配置说明**
* 当配置的服务来源失效时，请手动清理此处配置，否则可能会引发稳定性问题，例如无法及时同步其他来源的服务信息。

* 您无需配置服务来源即可添加DNS域名或固定地址服务。具体操作，请参见[创建服务](https://help.aliyun.com/document_detail/2881570.html)。

* 添加ACK容器服务时，网关需要监听ACK集群的Service和Endpoints来获取服务与端点信息。如果通过K8s Ingress配置网关的HTTPS请求时，网关还需要监听集群的Secret来获取HTTPS的证书信息。

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**来源**页签。

5. 单击**创建来源** ，在**创建来源** 面板，配置相关参数，然后单击**确定**。

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>ACK/ACS/ACK Serverless 集群</p> </td> <td> <p>选择后端服务所在的集群。若当前 VPC下不存在ACK/ACS/ACK Serverless集群，您可以单击<b>创建集群</b>进行创建。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>您在创建网关时需要选择和后端集群相同的VPC，那么服务来源添加时会自动获取该VPC下的集群。</p> </div> </div> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p>关联的 ACK 集群版本不得低于 1.18。如果集群版本低于 1.18，请先升级集群版本后再关联来源。建议使用 1.28 及以上版本。</p> </div> </div> </td> </tr> <tr> <td> <p>安全组授权</p> </td> <td> <p>容器集群的节点池上配置有安全组。通常情况下，集群外的组件要想访问到集群内的服务，就必须在安全组上开放服务所需的全部端口。</p> <p>您可以对安全组进行修改。具体操作，请参见<a href="https://help.aliyun.com/document_detail/2882561.html">设置安全组规则</a>。</p> </td> </tr> </tbody> </table>

## 结果验证
在**来源**页签查看服务来源信息。如果已包含新建的服务来源信息，则说明服务来源新建成功。