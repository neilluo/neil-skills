<!-- source_url: https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-09-20 -->
<!-- summary: 云原生API网关「创建后端服务」官方全文：容器服务/MSE Nacos/FC 函数计算/SAE Kubernetes/固定地址/DNS 域名/云工作流 CloudFlow 七种服务来源的创建步骤与参数表（服务名称、服务地址 <IP>:<端口>、TLS 模式）。这是让客户自有认证接口能被网关调用的前置步骤。 -->

您可以将服务添加到网关中，以便网关获取服务地址。云原生API网关支持多种添加方式，包括通过容器服务、MSE Nacos、固定地址、DNS域名以及FC函数计算等。  

## 操作步骤
1. 登录[云原生API网关控制台](https://apigw.console.aliyun.com/#/) 。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例**页面，单击目标网关实例ID。

4. 在左侧导航栏，选择**服务** ，并单击**创建服务** ，在**创建服务** 面板，选择**服务来源** 并[配置相关参数](#848d5a94a41l5)，完成后单击**确定**。

**说明**

云原生API网关不会修改您的请求，当请求转发到后端域名服务时，并不会将Host重写为您配置的域名。如果您需要配置域名，请参见[配置HTTP重写策略](https://help.aliyun.com/document_detail/2796832.html)。

## 服务相关参数
<table> <thead> <tr> <td><p><b>服务来源</b></p></td> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>容器服务</b></p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>如果在网关中添加了容器服务作为服务来源，网关会从ACK/<span>ACK Serverless集群</span>获取服务列表，将服务列表中的服务及其后端节点地址添加到网关中。</p> </div> </div></td> <td><p><b>命名空间</b></p></td> <td><p>选中集群的命名空间。默认不展示arms-prom、kube-system和mse-pilot命名空间的服务。</p></td> </tr> <tr> <td><p><b>服务列表</b></p></td> <td><p>在服务列表中选择服务。默认不展示以consumers开头的服务。</p></td> </tr> <tr> <td><p><b>MSE Nacos</b></p></td> <td><p><b>命名空间</b></p></td> <td><p>选中集群的命名空间。默认不展示arms-prom、kube-system和mse-pilot命名空间的服务。</p></td> </tr> <tr> <td><p><b>服务列表</b></p></td> <td><p>在服务列表中选择服务。默认不展示以consumers开头的服务。</p></td> </tr> <tr> <td><p><b>FC 函数计算</b></p></td> <td><p><b>后端服务</b></p></td> </tr> <tr> <td><p>函数列表</p></td> <td><p>在函数列表中选择函数。</p></td> </tr> <tr> <td><p>版本或别名</p></td> <td><p>选择函数的版本或别名。</p></td> </tr> <tr> <td><p><b>SAE Kubernetes 服务</b></p></td> <td><p><b>命名空间</b></p></td> <td><p>选中集群的命名空间。</p></td> </tr> <tr> <td><p><b>服务列表</b></p></td> <td><p>在服务列表中选择服务。</p></td> </tr> <tr> <td><p><b>固定地址</b></p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>如果该服务没有服务发现机制，需要手动添加服务的后端节点地址。</p> </div> </div></td> <td><p><b>服务名称</b></p></td> <td><p>自定义服务名称。</p></td> </tr> <tr> <td><p><b>服务地址</b></p></td> <td><p>服务的后端节点地址，不同来源的服务的后端节点有所不同，但格式均为<code>\&lt;后端节点IP\&gt;:\&lt;服务端口\&gt;</code>，多个节点通过换行分隔。</p></td> </tr> <tr> <td><p><b>TLS模式</b></p></td> <td><p>通过下拉框选择TLS模式。默认选择关闭TLS模式。</p> <ul> <li><p><b>关闭</b>：访问服务时，无需开启TLS。</p></li> <li><p><b>单向TLS</b>：需要使用HTTPS访问服务时开启单向TLS。</p></li> <li><p><b>双向TLS（mTLS）</b>：需要做双向认证时开启mTLS。</p></li> </ul></td> </tr> <tr> <td><p><b>DNS 域名</b></p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>云原生API网关支持根据DNS解析的结果作为后端服务地址。</p> </div> </div></td> <td><p><b>服务名称</b></p></td> <td><p>自定义服务名称。</p></td> </tr> <tr> <td><p><b>服务地址</b></p></td> <td><p>服务的后端节点地址，不同来源的服务的后端节点有所不同，但格式均为<code>\&lt;后端节点IP\&gt;:\&lt;服务端口\&gt;</code>，多个节点通过换行分隔。</p></td> </tr> <tr> <td><p><b>TLS模式</b></p></td> <td><p>通过下拉框选择TLS模式。默认选择关闭TLS模式。</p> <ul> <li><p><b>关闭</b>：访问服务时，无需开启TLS。</p></li> <li><p><b>单向TLS</b>：需要使用HTTPS访问服务时开启单向TLS。</p></li> <li><p><b>双向TLS（mTLS）</b>：需要做双向认证时开启mTLS。</p></li> </ul></td> </tr> <tr> <td><p><b>云工作流CloudFlow</b></p> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <ul> <li><p>云工作流CloudFlow服务要求网关版本大于等于2.1.8，如果网关实例版本过低，请升级网关版本。</p></li> <li><p>创建之后，系统将在API的入站处理策略中添加一条HTTP重写策略，重定向到<code>/</code>，且不支持修改或删除。</p></li> <li><p>云工作流CloudFlow服务仅支持单服务场景。</p></li> </ul> </div> </div></td> <td><p><b>工作流程</b></p></td> <td><p>选择已创建的<a href="https://help.aliyun.com/document_detail/2507664.html">CloudFlow</a><b>。</b></p></td> </tr> <tr> <td><p><b>调用方式</b></p></td> <td><p>支持异步调用与同步调用：</p> <ul> <li><p>StartExecution（异步调用 ）：标准模式（Standard）工作流仅支持异步调用模式</p></li> <li><p>StartSyncExecution（同步调用）：快速模式（Express）工作流仅支持同步调用模式</p></li> </ul></td> </tr> </tbody> </table>

## 结果验证
在**服务** 页签查看服务信息。如果包含新建服务的**服务名称** 、**服务地址** 和**服务来源**等信息，则表明服务新建成功。

## 相关文档
服务创建成功后，您还可以对服务进行管理。具体操作，请参见[管理服务](https://help.aliyun.com/document_detail/2796825.html)。