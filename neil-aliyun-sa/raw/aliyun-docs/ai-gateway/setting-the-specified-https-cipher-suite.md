---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/setting-the-specified-https-cipher-suite
fetch_date: 2026-09-21
product: AI Gateway
slug: setting-the-specified-https-cipher-suite
body_sha256: c643047df963bda462ecc911b516f72e1288944624f54e6ab2280f22300ed072
body_bytes: 4253
migration_status: current
---

HTTPS（超文本传输安全协议）是HTTP协议的安全版本，它通过SSL/TLS协议为传输的数据提供加密保护。HTTPS加密套件（Cipher Suite）是一组加密算法和协议，用于在客户端（如浏览器）和服务器之间建立安全的通信连接。为了进一步满足您在使用网关时，对于安全性、兼容性、性能优化以及其他合法合规的要求，AI网关支持客户端选择指定的加密套件。  

## 概述
一个HTTPS加密套件通常包括以下几个组成部分：

1. 密钥交换算法：用于安全地交换加密通信的密钥。常见的密钥交换算法包括RSA、Diffie-Hellman（DH）和ECDHE（椭圆曲线Diffie-Hellman）。

2. 消息认证码（MAC）算法：用于确保数据的完整性和认证，常见的MAC算法包括HMAC-SHA256、HMAC-SHA384等。

3. 对称加密算法：用于加密数据本身性，常见的对称加密算法包括AES（高级加密标准）、ChaCha20等。

## 支持范围
AI网关支持的套件及对应支持TLS版本。
<table> <thead> <tr> <td> <p><b>套件名称</b></p> </td> <td> <p><b>支持的TLS版本列表</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>ECDHE-ECDSA-AES128-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-ECDSA-AES256-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-RSA-AES128-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-RSA-AES256-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>AES128-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>AES256-SHA</p> </td> <td> <p>TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-ECDSA-AES128-GCM-SHA256</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-ECDSA-CHACHA20-POLY1305</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-RSA-AES128-GCM-SHA256</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-RSA-CHACHA20-POLY1305</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>AES128-GCM-SHA256</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-ECDSA-AES256-GCM-SHA384</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>ECDHE-RSA-AES256-GCM-SHA384</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> <tr> <td> <p>AES256-GCM-SHA384</p> </td> <td> <p>TLS 1.2、TLS 1.3</p> </td> </tr> </tbody> </table>

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**域名**，并在顶部菜单栏选择地域。

3. 单击**添加域名** 或者在目标域名的**操作** 列下单击**编辑**。

4. 在**添加域名** 或者**编辑域名** 页面的**域名**下拉列表中选择HTTPS协议。

5. 单击**高级选项** ，在**加密算法套件** 单选框中选择**自定义** **。** 在可选算法列表中勾选需要设置的算法，单击**确定**。

## 结果验证
1. 设置HTTPS域名为指定加密套件，如本例将加密套件指定为：`ECDHE-ECDSA-AES128-GCM-SHA256`并设置成功。

2. 指定加密套件为`ECDHE-ECDSA-AES128-GCM-SHA256`访问。

   ```
   HELPCODEESCAPE-bash
   curl -iv --ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256' https://bantian.alijam.top/get --resolve "bantian.alijam.top:443:8.154.33.131"
   ```

3. 指定套件`ECDHE-ECDSA-AES128-GCM-SHA256`请求正常返回成功，双方协商使用加密套件 `ECDHE-ECDSA-AES128-GCM-SHA256`。

   ```
   HELPCODEESCAPE-bash
   ~ curl -iv --ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256' https://bantian.alijam.top/get --resolve "bantian.alijam.top:443:8.xxx.xxx"
   * Added bantian.alijam.top:443:8 xxx xxx to DNS cache
   * Hostname bantian.alijam.top was found in DNS cache
   *   Trying 8.154.33.131:443...
   * Connected to bantian.alijam.top (8.154.33.131) port 443 (#0)
   * ALPN, offering h2
   * ALPN, offering http/1.1
   * Cipher selection: ECDHE-ECDSA-AES128-GCM-SHA256
   * successfully set certificate verify locations:
   *  CAfile: /etc/ssl/cert.pem
   *  CApath: none
   ```