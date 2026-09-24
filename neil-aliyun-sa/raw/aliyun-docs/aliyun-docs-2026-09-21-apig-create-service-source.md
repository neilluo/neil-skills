<!-- source_url: https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service-source -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-09-20 -->
<!-- summary: 云原生API网关「服务来源管理」官方全文：添加 ACK/ACS/ACK Serverless 集群或 MSE Nacos 作为服务来源的步骤、版本要求（ACK 1.18+，建议 1.28+）、同 VPC 与安全组授权要求。若客户认证服务在 K8s/Nacos 中，这是必须先做的服务来源步骤。 -->

云原生API网关支持容器服务（包括ACK/ACS/ACK Serverless 集群）和MSE Nacos这两种服务来源。本文将介绍如何将部署了后端服务的ACK集群或注册有后端服务的MSE Nacos注册中心添加至网关服务来源中并进行管理。  

## **前提条件**
* 已[创建网关实例](https://help.aliyun.com/document_detail/2796788.html)。

* 已[创建ACK托管集群](https://help.aliyun.com/document_detail/95108.html)或者[创建MSE Nacos集群](https://help.aliyun.com/document_detail/2852403.html)。

## 配置说明
* 当配置的服务来源失效时，请手动清理此处配置，否则可能会引发稳定性问题，例如无法及时同步其他来源的服务信息。

* 您无需配置服务来源即可添加DNS域名或固定地址服务。具体操作，请参见[创建服务](https://help.aliyun.com/document_detail/2796820.html)。

* 添加ACK容器服务时，网关需要监听ACK集群的Service和Endpoints来获取服务与端点信息。如果通过K8s Ingress配置网关的HTTPS请求时，网关还需要监听集群的Secret来获取HTTPS的证书信息。

## 创建服务来源
1. 登录[云原生API网关控制台](https://apigw.console.aliyun.com/#/) 。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例**页面，单击目标网关实例ID。

4. 在左侧导航栏，选择**服务** ，并单击**来源**页签。

5. 单击**创建来源** ，在**创建来源** 面板，配置相关参数，然后单击**确定**。

   ## 来源类型为容器服务时
   -------------

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b></b><b>ACK/ACK Serverless 集群</b></p> </td> <td> <p>选择后端服务所在的集群。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <ul> <li> <p>如当前VPC下不存在 ACK/ACS/ACK Serverless 集群，则需要<a href="https://help.aliyun.com/document_detail/95108.html">创建ACK托管集群</a>，再选择该集群。</p> </li> <li> <p>如果需要添加其他VPC下的服务来源，请重新<a href="https://help.aliyun.com/document_detail/2796788.html">创建指定VPC下的网关实例</a>后，再选择该集群。</p> </li> <li> <p>关联的 ACK 集群版本不得低于 1.18。如果集群版本低于 1.18，请先升级集群版本后再关联来源。建议使用 1.28 及以上版本。</p> </li> </ul> </div> </div> </td> </tr> <tr> <td> <p><b>安全组授权</b></p> </td> <td> <p>容器集群的节点池上配置有安全组。通常情况下，集群外的组件要想访问到集群内的服务，就必须在安全组上开放服务所需的全部端口。</p> <p>您可以对网关实例安全组进行修改。具体操作，请参见<a href="https://help.aliyun.com/document_detail/2796806.html">设置安全组规则</a>。</p> </td> </tr> </tbody> </table>

   ## 来源类型为MSE Nacos时
   ------------------

   <table> <thead> <tr> <td> <p><b>配置项</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Nacos 集群</b></p> </td> <td> <p>选择Nacos 集群。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <ul> <li> <p>如果当前VPC下不存在MSE Nacos集群，则需要先<a href="https://help.aliyun.com/document_detail/2852403.html">创建MSE Nacos集群</a>，再选择该Nacos集群。</p> </li> <li> <p>如果需要添加其他VPC下的服务来源，请重新<a href="https://help.aliyun.com/document_detail/2796788.html">创建指定VPC下的网关实例</a>，再选择该Nacos集群。</p> </li> <li> <p>集群列表仅展示<code>MCPEnabled = true</code>的MSE Nacos实例，可在MSE Nacos参数设置中更改。</p> </li> </ul> </div> </div> </td> </tr> </tbody> </table>
6. 查看服务来源信息。如果已包含新建的服务来源信息，则说明服务来源新建成功。

## 删除服务来源
1. 登录[云原生API网关控制台](https://apigw.console.aliyun.com/#/) 。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例**页面，单击目标网关实例ID。

4. 在左侧导航栏，选择**服务** ，并单击**来源**页签。

5. 单击目标服务来源**操作** 列下的**删除**。

6. 在确认**删除** 对话框，单击**确定**。

## 相关文档
* [如何创建网关实例](https://help.aliyun.com/document_detail/2796788.html)

* [API管理](https://help.aliyun.com/document_detail/2796782.html)

* [服务管理](https://help.aliyun.com/document_detail/2796812.html)

* [消费者管理](https://help.aliyun.com/document_detail/2857976.html)

* [常见问题](https://help.aliyun.com/document_detail/2807681.html)