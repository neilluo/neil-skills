---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/route-list
fetch_date: 2026-09-21
product: AI Gateway
slug: route-list
body_sha256: 68b648784d6f5649795152f6ef9866ba58a90e3ff6ab4c2b754bbef053322b20
body_bytes: 4293
migration_status: current
---

Model API 支持自定义路由，您可以按请求特征进行精细化路由的能力。本文介绍Model API的自定义路由管理。  

## **创建路由**
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**路由列表** ，然后单击**创建路由** ，并在**创建路由**面板配置相关参数：

   <table> <thead> <tr> <td> <ul> <li><p><b>路由名称</b>：自定义路由名称。</p></li> <li><p><b>路径</b>：Model\&nbsp;API的自定义路由路径支持<code>/v1/chat/completions</code>、<code>/v1/completions</code>、<code>/v1/embeddings</code>和<code>/v1/fine-tuning</code>四种方式。</p></li> <li><p><b>更多匹配规则</b>：如需创建多个相同路径的路由，需要对<b>方法（Method）</b>、<b>请求头（Header）</b>和<b>请求参数（Query）</b>进行配置，以区分不同路由。</p></li> <li><p><b>服务模型</b>：支持<b>单模型服务</b>和<b>多模型服务（按比例）</b>两种类型。</p> <ul> <li><p><b>单模型服务</b>：在同一个服务实例中只部署和运行一个模型，适用于需要专注于单一任务或模型的应用场景。</p></li> <li><p><b>多模型服务（比例）</b>：在同一个服务实例中部署和运行多个模型，并根据设定的比例分配资源和请求，适用于需要同时处理多种任务或模型的应用场景。</p></li> </ul></li> <li><p><b>服务列表</b>：在服务列表中选择服务。</p></li> <li><p><b>Fallback</b>：开启后可添加<a href="https://help.aliyun.com/document_detail/2880076.html">Fallback 服务</a>，按照降序执行。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>Fallback服务支持重复使用同一个服务组建多条策略。</p> </div> </div></li> </ul></td> </tr> </thead> <colgroup></colgroup> <tbody></tbody> </table>
4. 确认配置信息并单击**添加**。

## 编辑路由
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**路由列表**，并在路由列表中选择目标自定义路由。

4. 单击**编辑路由** ，并修改相关参数配置。更多参数说明，请参见[创建路由](#f777b0d9e9pag)。

5. 确认配置信息并单击**确定**。

## 发布路由
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**路由列表**，并在路由列表中选择目标自定义路由。

4. 单击**发布路由** ，并在确认弹框中单击**确定**。

## 下线路由
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**路由列表**，并在路由列表中选择目标自定义路由。

4. 选择**更多操作** \> **下线**，并在确认下线弹框中单击**下线**。

## 删除路由
**说明**

删除操作仅支持删除未发布或已下线的路由，如需删除已发布路由，请先完成[下线路由](#1ad200c606idf)操作。

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**路由列表**，并在路由列表中选择目标自定义路由。

4. 选择**更多操作** \> **删除**，并在确认删除的弹框中单击**删除**。