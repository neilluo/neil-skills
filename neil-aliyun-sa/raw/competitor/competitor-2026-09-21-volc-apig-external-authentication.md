<!-- source_url: https://www.volcengine.com/docs/6569/1798159 -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-08-10 -->
<!-- summary: 火山引擎 API 网关「外部认证鉴权」插件官方全文（getDocDetail API）。关键取证点：生效级别仅实例级；认证位置可配 header（例 Authorization）；认证地址自由路径（例 /）；认证方法可选 GET 或 POST；后端类型 容器/ECS/函数/固定 IP；匹配规则黑/白名单、路径前缀匹配或精确匹配；客户端 Host/Method/Path/Content-Length 请求头默认添加至鉴权请求报文（原始 Path 走 header 传递）；两条硬约束——「自建认证鉴权当前仅支持在实例级别生效」「自建认证鉴权服务所在的云资源（VKE/ECS 等）必须与 API 网关实例在相同私有网络」。 -->

> 文档标题：外部认证鉴权｜DocumentCode: Externalauthenticationandauthorization｜FirstPublishedTime: 2025-08-25T11:47:26Z｜UpdatedTime: 2026-08-10T09:59:43Z

API 网关支持对接用户外部自建的认证鉴权服务，方便用户统一认证鉴权方式。本文介绍如何在 API 网关中配置外部认证鉴权。

<span id="ddeDwTYn"></span>
## 背景信息

部署在云端的业务通常根据客户端请求携带的凭证信息（即 Token）来保护对外暴露接口的通信安全。当 Token 形式为用户自定义格式时，则业务的服务端收到请求后，必须额外访问的鉴权服务来完成鉴权操作，以保证客户端访问的合法性。为满足此场景，API 网关支持基于用户自建认证鉴权服务的认证。具体的认证流程如下所示。

<span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_ae29b82d359843ad663042ff06fce41d.png) </span>


1. 客户端向网关发起认证请求。

2. 网关将认证请求直接转发给自建认证服务。认证服务支持搭建在容器服务集群、ECS 实例、函数服务中，或指定固定的 IP 地址。

3. 认证服务读取请求中的验证信息进行验证，验证通过后返回凭证信息（Token）给网关，由网关返回给客户端。

4. 客户端向网关发起业务请求，请求中携带上一步中身份认证成功后颁发的 Token。

5. 网关通过截取原始业务请求的 Path（包含 Query Parameters）、HTTP 方法（GET、POST 等）和 Token 来形成一个新的请求报文，向接入的自建鉴权服务发起鉴权请求。您可以在 API 网关控制台中配置认证 Token 的 HTTP Header 位置（Authorization、Cookie 或自定义），也可以根据需要指定鉴权携带的请求头和鉴权返回的响应头。

6. 认证服务收到鉴权请求后，根据 Token 完成合法性校验，并返回`2xx`或异常状态码。

   * 如果认证服务返回的 HTTP 状态码为`2xx`，则表明 Token 合法且 Token 有权限访问指定的后端资源。网关继续将原始业务请求转发给受保护的后端服务，收到业务响应后再次转发给客户端，完成受保护的业务访问。

   * 如果认证服务返回的 HTTP 状态码为其他异常状态码，则表明 Token 不合法或 Token 无权限访问指定的后端资源。网关直接返回鉴权服务的响应给客户端，业务访问失败。


<span id="ddeDwTYn"></span>
## 前提条件


* 已创建实例，详情请参见 [创建实例](https://www.volcengine.com/docs/6569/85693)。

* 已自建认证鉴权服务器，并在 API 网关中将认证服务器配置为 Upstream。详情请参见 [Upstream 管理](https://www.volcengine.com/docs/6569/163236)。


<span id="AyamhzTh"></span>
## 使用限制


* 自建认证鉴权当前仅支持在实例级别生效。

* 自建认证鉴权服务所在的云资源（例如 VKE 集群、ECS 实例等），必须与 API 网关实例在相同私有网络。


<span id="hFSwy7SA"></span>
## 操作步骤


1. 登录 [API 网关控制台](https://console.volcengine.com/veapig)。

2. 在顶部导航栏，选择目标地域。

3. 在左侧导航栏 **实例管理**  下拉框中选择目标实例后，单击 **插件中心 \> 认证鉴权 \>**  **外部认证插件。** 

4. 单击 **创建插件**，配置认证鉴权信息。

   <span>![图片](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_c66b2b4abd048a83c8bbd5aea5047950.png) </span>

   
   |配置项 |说明 |
   |---|---|
   |生效级别 |选择外部认证插件的生效级别，当前仅支持 **实例级别**。 |
   |所属实例 |选择外部认证功能生效的 API 网关实例。 |
   |备注 |支持根据业务需要选择是否编辑备注内容，例如插件的用途，便于后期识别。 |
   |认证位置 |配置认证信息所在的请求头，例如`Authorization`。 |
   |认证服务地址 |配置认证服务器的地址和认证鉴权方式，包括：<br><br><br>* **后端类型**：选择认证服务器的后端类型，支持 **容器服务**、**云服务器**、**函数服务** 和 **固定 IP**。<br><br>* **Upstream**：选择认证服务器所在的具体 Upstream。<br><br>* **认证地址**：配置认证使用的路径，例如`/`。<br><br>* **认证方法**：配置认证使用的 HTTP Method，支持 **GET** 或 **POST**。<br><br>* **超时时间**：配置等待鉴权服务返回结果的最大等待时间，单位：秒。如果超过该时间，鉴权服务仍没有返回，则鉴权失败。<br><br>* **认证鉴权**：配置认证鉴权方式，包括：<br><br>   * **不启用**：不启用认证鉴权。<br><br>   * **API Key**：使用 API Key 进行认证鉴权。当选择该选项时，需要指定 API Key 的位置（**请求头** 或 **请求参数**）和  API Key 的值。<br><br>   * **签名**：使用签名进行认证鉴权。当选择该选项时，需要配置签名的 **Service**、**Access Key** 和 **Secret Key**。 |
   |转发请求头 |配置在鉴权请求报文中，额外携带的客户端请求头。鉴权请求报文会携带该头部，发送至鉴权服务。<br><br><div data-tips="true" data-tips-type="default" data-tips-is-title="true">说明</div><br><br><br><div data-tips="true" data-tips-type="default">客户端的<code>Host</code>、<code>Method</code>、<code>Path</code>和<code>Content-Length</code>请求头会默认添加至鉴权请求报文中，无需您额外手动添加。</div><br> |
   |添加请求头 |配置从认证服务返回的响应头中，需要提取并转发给 Upstream 的请求头。 |
   |忽略预检请求 |配置是否忽略预检请求（Options）。<br><br><br>* **开启**：网关将忽略预检请求（Options），不对其进行认证鉴权，直接放行。<br><br>* **未开启**：网关不忽略预检请求，将按照正常流程进行外部认证鉴权。 |
   |允许匿名访问 |配置是否允许匿名访问，即是否放行不包含认证信息的请求。<br><br><br>* **开启**：允许匿名访问。网关将直接放行无认证信息的请求。<br><br>* **未开启**：禁止匿名访问。网关将拦截并阻断无认证信息的请求。 |
   |隐藏凭证 |配置网关在向后端服务（Upstream）转发请求时，是否隐藏前端传入的认证信息。<br><br><br>* **开启**：对后端隐藏凭证。网关将在转发请求前，移除相关的认证信息（如 Authorization 头）。<br><br>* **未开启**：不隐藏凭证。网关将把原始的认证信息直接透传给后端服务。 |
   |重新路由 |是否根据客户端请求中添加的鉴权响应头，进行重新路由。<br><br><br>* **开启**：根据客户端原始请求中的 Method、Path、请求头、请求参数、以及添加的鉴权响应头，对请求进行重新路由。<br><br>* **未开启**：仅会基于客户端原始请求中的 Method、Path、请求头和请求参数进行路由。 |
   |降级模式 |是否采用鉴权降级模式。<br><br><br>* **开启**：当认证鉴权服务服务器不可用时，系统会自动跳过鉴权流程。此时，客户端可以在未鉴权的前提下访问后端业务。<br><br>* **未开启**：当认证鉴权服务服务器不可用时，系统不会跳过鉴权流程。此时，由于无法完成鉴权，客户端无法访问对应的后端业务。 |
   |匹配规则 |配置鉴权匹配规则，包括：<br><br><br>* **黑名单**：黑名单中匹配的域名和路径，无需进行认证鉴权。其余域名或路径，均需要进行认证鉴权。<br><br>* **白名单**：白名单中匹配中的域名和路径，需要进行认证鉴权。其余域名或路径，均无需进行认证鉴权。<br><br><br><div data-tips="true" data-tips-type="default" data-tips-is-title="true">说明</div><br><br><br><div data-tips="true" data-tips-type="default">单击 <strong>添加</strong>，允许配置多条匹配规则。</div><br><br><br><br>* **域名**：配置匹配规则中的域名信息。<br><br>* **路径**：配置匹配规则中的路径信息，支持 **前缀匹配** 或 **精确匹配**。 |
   

5. 单击 **确定**，完成配置。


<span id="crEZAagP"></span>
## 结果验证

<span id="a3YqrwlK"></span>
### 查看配置

配置完成后，在外部认证插件列表将生成一条新的插件记录。插件状态为 **已启用**，表示插件功能生效。

<span id="5zCWNWus"></span>
### 认证测试

在 API 网关实例中配置外部认证插件，当访问请求命中配置的域名和路径时，仅携带该认证信息的访问请求，能够通过 API 网关访问到后端 Upstream。


1. 使用 API 网关实例中配置的域名访问服务，当未携带认证信息时。

   ```Bash
   curl -H "Host: apig-example.com" http://14.xxx.xxx.xxx
   ```
   

   预期结果如下，表示认证失败，无法通过 API 网关访问到后端的服务。

   ```Bash
   ext_auth:missing_credential
   ```
   

2. 使用 API 网关实例中配置的域名访问服务，当携带认证信息时。

   ```Bash
   curl -H "Host: apig-example.com" http://14.xxx.xxx.xxx -H "Authorization: Bearer e8cc8b4f-***"
   ```
   

   预期结果如下，表示能够通过 API 网关访问到后端的服务。

   ```HTML
   <!DOCTYPE html>
   <html>
   <head>
   <title>Welcome to nginx!</title>
   <style>
   html { color-scheme: light dark; }
   body { width: 35em; margin: 0 auto;
   font-family: Tahoma, Verdana, Arial, sans-serif; }
   </style>
   </head>
   <body>
   <h1>Welcome to nginx!</h1>
   <p>If you see this page, the nginx web server is successfully installed and
   working. Further configuration is required.</p>
   
   <p>For online documentation and support please refer to
   <a href="http://nginx.org/">nginx.org</a>.<br/>
   Commercial support is available at
   <a href="http://nginx.com/">nginx.com</a>.</p>
   
   <p><em>Thank you for using nginx.</em></p>
   </body>
   </html>
   ```
