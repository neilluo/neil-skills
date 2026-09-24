<!-- source_url: https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/global-authentication-1 -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2024-12-27 -->
<!-- summary: 云原生API网关「全局认证鉴权」机制对比页全文：官方明确网关全局认证鉴权只有 JWT、OIDC、自建认证鉴权三种方式，并给出各自适用场景说明。用于给客户做选型定位（客户场景=自建认证鉴权，而非插件）。 -->

本文介绍云原生API网关不同认证鉴权机制的差异。  
在微服务的架构中，会有多个服务接收来自外部用户（客户端）的请求，通常不会直接将服务暴露给外部用户，而是在中间加一层网关作为外部用户访问内部服务的控制点。对于外部用户访问的请求，我们通常希望在网关中进行身份验证，知道用户是谁，并能定义访问控制策略。

## 网关认证鉴权类型
云原生API网关目前支持JWT、OIDC以及自建认证鉴权等方式：

* **JWT（JSON Web Tokens）**

  JWT（JSON Web Tokens）是一套基于用户体系对用户的API（服务）进行授权访问的机制，满足用户个性化安全设置的需求。云原生API网关对外开放的API需要识别请求者的身份，并据此判断所请求的资源是否可以返回给请求者。Token就是一种用于身份验证的机制，基于这种机制，应用不需要在服务端保留用户的认证信息或者会话信息，可实现无状态、分布式的Web应用授权，为应用的扩展提供了便利。

  关于云原生API网关JWT认证鉴权的具体操作，请参见[配置JWT认证鉴权](https://help.aliyun.com/document_detail/2807798.html)。
* **OIDC（OpenID Connect）**

  OIDC（OpenID Connect）是一种安全认证机制，第三方应用连接到身份认证提供商（Identify Provider）获取用户信息，并把这些信息以安全可靠的方式返回给第三方应用。OIDC对OAuth2.0协议进行了扩展，通过扩展的ID Token字段，提供用户基础身份信息，ID Token使用JWT（JSON Web Token）格式进行封装，提供自包含性、防篡改机制，可以安全地传递给第三方应用程序并容易被验证。

  关于云原生API网关OIDC认证鉴权的具体操作，请参见[配置OIDC认证鉴权](https://help.aliyun.com/document_detail/2807800.html)。
* **自建认证鉴权**

  如果客户端请求携带的凭证信息（即Token）的形式是业务方自定义的格式，则服务端收到请求后，必须额外访问中心化的鉴权服务来完成鉴权操作。云原生API网关支持自定义鉴权，方便在网关入口处完成鉴权，避免每个后端服务都接入鉴权服务。

  关于云原生API网关自建认证鉴权的具体操作，请参见[配置自建认证鉴权](https://help.aliyun.com/document_detail/2807799.html)。