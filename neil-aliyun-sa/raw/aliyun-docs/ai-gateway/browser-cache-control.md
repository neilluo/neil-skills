---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/browser-cache-control
fetch_date: 2026-09-21
product: AI Gateway
slug: browser-cache-control
body_sha256: 65f047340512998ff8ea7008cc63540680b1f3a934442213a8de0cac8272a7de
body_bytes: 2034
migration_status: current
---

`cache-control`插件实现了基于 URL 文件后缀来为请求的响应头部添加 `Expires` 和 `Cache-Control` 头部，从而方便浏览器对特定后缀的文件进行缓存，例如 `jpg`、`png` 等图片文件。  

## **运行属性**
插件执行阶段：`认证阶段` 插件执行优先级：`420`

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>suffix</p></td> <td><p>string</p></td> <td><p>选填，表示匹配的文件后缀名，例如\&nbsp;<code>jpg</code>、<code>png</code>\&nbsp;等。</p><p>如果需要匹配多种后缀，需要用\&nbsp;<code>\|</code>\&nbsp;进行分割，例如\&nbsp;<code>png\|jpg</code>。</p><p>如果不填写，表示匹配所有后缀</p></td> <td><p>-</p></td> <td><p>配置用于匹配的请求文件后缀</p></td> </tr> <tr> <td><p>expires</p></td> <td><p>string</p></td> <td><p>必填，表示缓存的最长时间。</p><p>当填入的字符串为数字时，单位为秒，例如需要缓存1小时，需填写 3600。</p><p>另外，还可以填写 epoch 或 max</p><p>，与 nginx 中语义相同。</p></td> <td><p>-</p></td> <td><p>配置缓存的最大时间</p></td> </tr> </tbody> </table>

## 配置示例
1. 缓存后缀为 `jpg`, `png`, `jpeg` 的文件，缓存时间为一小时。

   ```
   HELPCODEESCAPE-yaml
   suffix: jpg|png|jpeg
   expires: 3600
   ```

   根据该配置，下列请求在访问时，将会在响应头中添加 `Expires` 和 `Cache-Control` 字段，且过期时间为 1 小时后。

   ```
   HELPCODEESCAPE-yaml
   curl http://example.com/test.png
   curl http://exmaple.com/test.jpg
   ```

2. 缓存所有文件，且缓存至最大时间 `"Thu, 31 Dec 2037 23:55:55 GMT"`

   ```
   HELPCODEESCAPE-yaml
   expires: max
   ```