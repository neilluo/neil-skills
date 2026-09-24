---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/hsts-plug-in
fetch_date: 2026-09-21
product: AI Gateway
slug: hsts-plug-in
body_sha256: 99739133cfc45ac72341e82558da070df49fa58ceeb0c206dc547de5e834e7d6
body_bytes: 1860
migration_status: current
---

HSTS是HTTP Strict Transport Security的缩写，它是一种安全协议， 旨在增强Web应用程序的安全性。本文介绍如何配置HSTS插件。  

## **插件类型**
流量管控。

## 功能说明
HSTS插件的作用是通知浏览器在未来的一段时间内，它应该只使用HTTPS与该服务器进行通信。HSTS与HTTPS强跳转的不同地方在于，HSTS对于HTTP请求可以直接在浏览器通过307内部跳转完成HTTPS转换，无需执行额外的网络请求。

## 插件原理
HSTS插件会对所有的HTTPS响应中添加`strict-transport-security`头部，关于值的部分，其中：

* `max_age`：强制使用HTTPS访问网站的最大持续时间（以秒为单位）。

* `include_sub_domains`：当前域名以及子域名强制使用HTTPS访问网站。

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>max_age</b></p></td> <td><p>number</p></td> <td><p>选填。</p></td> <td><p>15724800</p></td> <td><p>强制使用HTTPS访问网站的最大持续时间（以秒为单位）。</p></td> </tr> <tr> <td><p><b>include_sub_domains</b></p></td> <td><p>bool</p></td> <td><p>选填。</p></td> <td><p>false</p></td> <td><p>当前域名以及子域名强制使用HTTPS访问网站。</p></td> </tr> </tbody> </table>  
**说明**

当开启`include_sub_domains`时，当前域名以及子域名强制使用HTTPS访问网站，必须确保所有子域名都支持HTTPS，否则用户将无法访问这些子域名。 建议您在启用`include_sub_domains`之前先确保所有子域名都配置为支持HTTPS。