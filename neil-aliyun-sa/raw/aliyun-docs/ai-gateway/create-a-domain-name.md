---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/create-a-domain-name
fetch_date: 2026-09-21
product: AI Gateway
slug: create-a-domain-name
body_sha256: be5cc23545d8b0d5387c5a94c206686848d1f1e9e7547f66834c27bc1af4023f
body_bytes: 6438
migration_status: current
---

AI网关提供多域名管理能力，便于您管理不同域名下的协议、证书及路由配置。同时也支持泛域名匹配，例如绑定了`*.hello.com`这个泛域名之后，可以通过`1.hello.com`、`2.hello.com`等域名同时访问。  

## 前提条件
完成相关域名的备案。  
**说明**

中国地域独立域名需要在阿里云备案或者在阿里云备案接入，海外地域不需要域名备案。

## 操作步骤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**域名**，并在顶部菜单栏选择地域。

3. 单击**添加域名** ，在**添加域名** 面板中配置相关参数，然后单击**确定**。

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>域名</b></p></td> <td><p>输入完整域名（例如：<code>hello.com</code>）或泛域名（例如：<code>\*.hello.com</code>）。在这个域名下，您可以独立管理该域名的协议及证书，路由配置可以通过域名实现相互隔离。</p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p><code>\*.hello.com</code>可以匹配<code>a.hello.com</code>、<code>b.hello.com</code>和<code>a.b.hello.com</code>等类型的域名，但是如果申请的证书域名是<code>\*.hello.com</code>，则证书只能用于<code>a.hello.com</code>、<code>b.hello.com</code>，不能用于<code>a.b.hello.com</code>。</p> </div> </div></td> </tr> <tr> <td><p>选择<b>HTTP</b>协议或<b>HTTPS</b>协议。不同协议支持的端口号如下：</p> <ul> <li><p><b>HTTP</b>：支持80端口。</p></li> <li><p><b>HTTPS</b>：支持443端口。</p></li> </ul></td> </tr> <tr> <td><p>选择协议为<b>HTTPS</b>协议</p></td> </tr> <tr> <td><p><b>证书</b></p></td> <td><p>选择HTTPS协议所关联的阿里云SSL证书服务上的证书。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>如果您还未购买或者上传相关SSL证书，可以单击<b>购买/上传证书</b>跳转至<b>数字证书管理服务</b>控制台进行操作。具体操作，请参见<span><a href="https://www.aliyun.com/product/cas">选购SSL证书</a></span>。</p> </div> </div></td> </tr> <tr> <td><p><b>强制HTTPS</b></p></td> <td><p>开启强制HTTPS，表示只生效HTTPS端口，正常HTTP端口将被拒绝访问，请求将被重定向至HTTPS。</p></td> </tr> <tr> <td><p><b>是否启用 HTTP/2</b></p></td> <td><p>通过ALPN协议在TLS握手阶段决定是否采用HTTP/2。</p> <ul> <li><p>使用网关实例配置：根据参数配置中<code>EnableHttp2</code>的值决定当前域名是否使用HTTP/2，并跟随参数配置中<code>EnableHttp2</code>的值动态变化。</p></li> <li><p>开启：当前域名在TLS握手成功后使用HTTP/2协议通信。</p></li> <li><p>关闭：当前域名在TLS握手成功后不使用HTTP/2协议通信。</p></li> </ul> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>当协议配置为HTTP协议时，网关会利用HTTP Upgrade协议根据客户端要求自动升级为HTTP/2。因此，您只有在使用了HTTPS协议时才需要按需配置HTTP/2开关。</p> </div> </div></td> </tr> <tr> <td><p><b>TLS版本</b></p></td> <td><p>配置当前域名允许TLS通信时所选择的版本。</p> <ul> <li><p><b>最小TLS版本</b>：配置当前域名允许TLS通信时所选择的最小版本，默认为1.0。</p></li> <li><p><b>最大TLS版本</b>：配置当前域名允许TLS通信时所选择的最大版本，默认为1.3。</p></li> </ul></td> </tr> <tr> <td><p><b>加密算法套件</b></p></td> <td><p>选择<b>默认</b>或者<b>自定义</b>加密算法套件。</p> <ul> <li><p><b>默认</b>：选择默认加密算法套件。</p> <div> <p><b>默认加密算法套件：</b></p> <div> <ul> <li><p>ECDHE-ECDSA-AES128-GCM-SHA256(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-RSA-AES128-GCM-SHA256(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-ECDSA-AES256-GCM-SHA384(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-RSA-AES256-GCM-SHA384(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-ECDSA-CHACHA20-POLY1305(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-RSA-CHACHA20-POLY1305(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-ECDSA-AES128-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-RSA-AES128-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-ECDSA-AES256-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> <li><p>ECDHE-RSA-AES256-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> <li><p>AES128-GCM-SHA256(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>AES256-GCM-SHA384(支持版本：TLS 1.2, TLS 1.3)</p></li> <li><p>AES128-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> <li><p>AES256-SHA(支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3)</p></li> </ul> </div> </div></li> <li><p><b>自定义</b>：选择加密算法至已选算法框中。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>指定加密套件只会在协商结果为TLS 1.0-1.2时有效，协商结果为TLS1.3时不生效。</p> </div> </div></li> </ul></td> </tr> <tr> <td><p><b>客户端双向认证 mTLS</b></p></td> <td><p>开启或者关闭<b>客户端双向认证 mTLS</b>，默认关闭。</p></td> </tr> <tr> <td><p><b>客户端双向认证 CA 证书</b></p></td> <td><p>开启<b>客户端双向认证 mTLS</b>后，需要配置<b>客户端双向认证 CA 证书</b>，用于验证客户端身份。</p></td> </tr> <tr> <td><p><b>资源组</b></p></td> <td><p>选择目标资源组。您可单击右侧的<b>创建资源组</b>。</p></td> </tr> </tbody> </table>

## 结果验证
当前域名的路径下已配置可访问的路由。

* 如果您的域名公网解析已生效，可以直接通过浏览器访问验证。

* 如果您的域名还未配置DNS解析，可以通过以下方式进行验证。例如域名配置为`hello.com`，将下面URL中的{公网IP}替换为您的实际公网IP。

  * 验证HTTP

    ```
    HELPCODEESCAPE-bash
    curl http://hello.com --resolve "hello.com:80:{公网IP}"
    ```

  * 验证HTTPS

    ```
    HELPCODEESCAPE-bash
    curl -v -k https://hello.com --resolve "hello.com:443:{公网IP}" --cacert my-cert.pem
    ```