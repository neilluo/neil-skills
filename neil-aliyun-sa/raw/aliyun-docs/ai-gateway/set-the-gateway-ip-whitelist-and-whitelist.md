---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/set-the-gateway-ip-whitelist-and-whitelist
fetch_date: 2026-09-21
product: AI Gateway
slug: set-the-gateway-ip-whitelist-and-whitelist
body_sha256: 6fd460ae6e33992ca462e496875cad2d8fb08c097a8cc89d6821d0a0b5eaa908
body_bytes: 2746
migration_status: current
---

网关IP黑名单和白名单是AI 网关提供的安全防护能力之一。您可以通过配置黑、白名单来拒绝或允许特定IP的访问请求。AI 网关支持在网关全局、域名和路由级别配置IP黑名单和白名单，满足精细化的访问控制诉求。本文介绍如何为AI 网关设置黑名单和白名单。  

## **操作步骤**
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**安全管理** \> **黑/白名单**。

5. 在页面左上角，单击**创建** ，在**创建** 页面，配置相关参数，然后单击**保存**。

   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>开启</b></p></td> <td><p>是否开启黑/白名单配置。</p></td> </tr> <tr> <td><p><b>名称</b></p></td> <td><p>自定义IP访问控制的名称。</p></td> </tr> <tr> <td><p><b>备注</b></p></td> <td><p>对IP访问控制做备注。</p></td> </tr> <tr> <td><p><b>类型</b></p></td> <td><p>按需选择IP访问控制的类型。</p> <ul> <li><p><b>白名单（允许特定IP访问）</b>：在网关场景只开放受信任来源IP访问。</p></li> <li><p><b>黑名单（禁止特定IP访问）</b>：在网关场景针对不友好访问执行来源IP封禁。</p></li> </ul></td> </tr> <tr> <td><p><b>生效层级</b></p></td> <td><p>用于指定访问控制策略在网关中作用的网络层次。该字段支持两个选项：<b>应用层（HTTP/HTTPS）</b>和<b>传输层（TCP/UDP）</b>。</p> <ul> <li><p><b>应用层（HTTP/HTTPS）</b>：<b>默认是应用层</b>。网关会允许客户端建立连接，并根据请求中的IP信息判断是否放行或屏蔽流量。</p></li> <li><p><b>传输层（TCP/UDP）</b>：网关将在TCP连接建立阶段就对客户端IP进行检查，<b>直接拒绝非法IP的连接请求</b>，不再继续后续的应用层处理流程。</p></li> </ul></td> </tr> <tr> <td><p><b>生效粒度</b></p></td> <td><p>IP访问控制的作用域。</p> <ul> <li><p><b>网关全局</b>：作用于网关实例。</p></li> <li><p><b>域名</b>：作用于指定域名。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>对于白名单，生效粒度为白名单配置交集。</p> <p>对于黑名单，生效粒度为黑名单配置并集。</p> </div> </div></li> </ul></td> </tr> <tr> <td><p><b>IP地址/地址段</b></p></td> <td><p>输入IP访问控制的来源IP地址或地址段。</p></td> </tr> </tbody> </table>

<br />