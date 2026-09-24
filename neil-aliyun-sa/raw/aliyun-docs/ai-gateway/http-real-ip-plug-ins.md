---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/http-real-ip-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: http-real-ip-plug-ins
body_sha256: ba8674c8b1df06987a122ba003310c08ea9f2717caab1c7491f3be6890852434
body_bytes: 384
migration_status: current
---

http-real-ip插件是[nginx real-ip 模块](http://nginx.org/en/docs/http/ngx_http_realip_module.html)的wasm实现。  

## **插件类型**
流量管控。

## 参数描述
* `real_ip_from`：定义已知发送客户端请求的可信地址。

* `real_ip_header`：定义包含客户端地址的请求Header，其值将用于替换客户端地址，默认使用`x-forwarded-for`。