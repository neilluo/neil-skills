---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-dns-server
fetch_date: 2026-09-21
product: AI Gateway
slug: configure-dns-server
body_sha256: 39df29e83d1e7edd11f98f54e3708bb31e83330fcf64a5f8a4187a0eaaa38344
body_bytes: 1597
migration_status: current
---

为服务配置DNS服务器可以实现高效、安全的内部域名解析，确保内部服务的访问稳定性和可靠性。通过合理配置DNS服务器，可以实现对内部服务域名的集中管理，避免因外部DNS故障或网络波动导致的服务不可用问题。  

## 使用场景
* 自定义DNS需求：满足用户对内网DNS的自定义配置需求。

* 内部服务解析：后端服务位于VPC内时，AI网关使用内网DNS正确路由请求。

* 混合云环境：统一管理内部和外部服务的DNS解析。

## 使用限制
DNS服务器列表最大限制5个。

## 操作入口
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**服务**页签。

5. 根据不同场景的需求，提供以下两种操作入口：

   * 单击**创建服务**。

   * 单击需要变更的服务**操作** 列下的**编辑**。

## 配置DNS服务器
1. 单击**更多设置** ，单击**一键填充内网DNS解析服务地址**。

   当您[开通内网DNS服务解析](https://dnsnext.console.aliyun.com/privateDNS/introduce)时，阿里云会自动为您的VPC分配内网DNS解析服务地址。系统自动填充内网DNS解析服务地址。最多可配置5个DNS服务器，也可单击 **+ 添加** 手动添加。
2. 单击**添加**，您也可以输入DNS服务器地址。

   手动输入地址的格式为 `IP:端口`。