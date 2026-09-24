---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/change-the-protocol-and-certificate-of-the-domain-name
fetch_date: 2026-09-21
product: AI Gateway
slug: change-the-protocol-and-certificate-of-the-domain-name
body_sha256: 4a1ec7888cb03e35c6c733aa9536fc0dc2c0f1527f4c6c24cb10eadc83d71c01
body_bytes: 1079
migration_status: current
---

当SSL证书到期、域名所有者发生变更、或者需要将网站的协议从HTTP升级到HTTPS时，通常需要变更域名的证书和协议，以确保网站的安全性和合规性。这些变更对于保护数据、建立信任，并遵守最新的网络安全标准至关重要。  

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**域名**，并在顶部菜单栏选择地域。

3. 在**域名**页面，单击需要变更的域名名称。

4. 在域名详情页面单击**编辑**，您可以选择更换协议或证书。

   * 更换协议：单击**域名** 右侧的下拉列表选择协议，然后单击**确定**。

     **说明**

     目前云原生API网关支持**HTTP** 协议和**HTTPS** 协议，且**HTTPS**协议必须关联SSL证书。不同协议支持的端口号如下：
     * **HTTP**：支持80端口。

     * **HTTPS**：支持443端口。

   * 更换证书：单击**证书** 右侧的下拉列表选择证书，然后单击**确定**。