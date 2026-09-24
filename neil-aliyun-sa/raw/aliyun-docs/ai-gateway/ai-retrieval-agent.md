---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-retrieval-agent
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-retrieval-agent
body_sha256: e262264d0053103ac3cbd1bc268acc5cac96bda5f9a6dcb818049a5f03ab6589
body_bytes: 13994
migration_status: current
---

本文介绍AI RAG 检索代理插件功能以及如何通过该插件实现AI应用与外部RAG引擎连接。  

## **功能说明**
AI RAG 检索代理插件通过检索协议转化和检索结果转换, 实现Dify等AI应用连接并检索[RAGFlow](#r12nx)和[百炼知识库](#Ua8Pb)等外部RAG引擎。

## 运行属性
* 插件执行阶段：`默认阶段`。

* 插件执行优先级：`150`。

## 配置说明
### 基本配置

<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>rag_proxy.provider.name</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>被调用的外部知识库的类型,支持的枚举类型目前包括：ragflow、bailian。</p></td> </tr> <tr> <td><p><code>rag_proxy.source.name</code></p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>dify</p></td> <td><p>外部知识库调用方引擎类型,支持的枚举类型目前包括: dify。</p></td> </tr> <tr> <td><p><code>rag_proxy.source.enable_to_proxy_api_key</code></p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>false</p></td> <td><p>是否开启AI网关与外部知识库调用方之间API Key校验，不填写默认为false，开启后AI网关与外部知识库调用方之间API Key必须一致，否则无法正常使用。</p></td> </tr> <tr> <td><p><code>rag_proxy.source.to_proxy_api_key</code></p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>外部知识库调用方引擎的创建外部知识库API时，填写的API Key, 填写后，AI网关会校验此处填入的参数是否与外部知识库创建API时填写的API Key相同，否则不进行校验。</p></td> </tr> </tbody> </table>

### RAGFlow配置

当选择RAGFlow作为被调用的外部知识库时（`rag_proxy.provider.name="ragflow"`），请参考以下说明进行配置。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>rag_proxy.provider.api_key</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>调用RAGFlow API的API Key, 可在RAGFlow控制台右上角头像-API-RAGFlow API处获取。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.dataset_ids</code></p></td> <td><p>list\[string\]</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>检索RAGFlow的DataSet ID，如这里不填，请在Dify配置外部知识库时填写，优先以Dify配置的外部知识库ID为准。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.document_ids</code></p></td> <td><p>list\[string\]</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>检索RAGFlow的Document ID，可以只在指定的Document下检索。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.similarity_threshold</code></p></td> <td><p>float</p></td> <td><p>选填</p></td> <td><p>0.0</p></td> <td><p>相似度阈值, 低于阈值的分块会被过滤，可以在Dify的召回界面配置该参数。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.top_n</code></p></td> <td><p>integer</p></td> <td><p>选填</p></td> <td><p>30</p></td> <td><p>返回相似度最高的top_n个分块, 其他分块会被过滤，可以在Dify的召回界面配置该参数。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.vector_similarity_weight</code></p></td> <td><p>float</p></td> <td><p>选填</p></td> <td><p>0.3</p></td> <td><p>向量余弦相似度权重, 如果x表示向量余弦相似度, 则<code>(1-x)</code>表示语义相似度权重。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.keyword</code></p></td> <td><p>boolean</p></td> <td><p>选填</p></td> <td><p>false</p></td> <td><p>表示是否启用基于关键字的匹配：true：启用基于关键字的匹配。false：禁用基于关键字的匹配（默认）。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.rerank_id</code></p></td> <td><p>integer</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>RAG引擎中配置的Rerank模型的ID，配置后使用该模型开启Rerank功能，具体选型请参照ragflow支持的rerank模型，默认不开启该功能。</p></td> </tr> </tbody> </table>

关于RAGFlow的知识库使用操作指引，请参见：[Configure knowledge base](https://ragflow.io/docs/dev/configure_knowledge_base)。

关于RAGFlow的检索更详细参数说明，请参见：[Retrieve chunks](https://ragflow.io/docs/dev/http_api_reference#retrieve-chunks)。

基础配置示例如下所示：

```
HELPCODEESCAPE-yaml
rag_proxy:
  provider:
    name: 'ragflow'
    api_key: "xxxxxxxx"
```

### 百炼知识库配置

当选择百炼知识库作为被调用的外部知识库时（`rag_proxy.provider.name="bailian"`）， 请参考以下说明进行配置。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>rag_proxy.provider.api_key</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>百炼平台API Key，获取地址<a href="https://bailian.console.aliyun.com/?tab=model#/api-key">百炼API-KEY</a>。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.index_id</code></p></td> <td><p>string</p></td> <td><p>选填</p></td> <td><p>-</p></td> <td><p>阿里云百炼知识库ID，获取方式参考: <a href="https://help.aliyun.com/document_detail/2852772.html">知识库API指南</a>。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.enable_reranking</code></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>true</p></td> <td><p>是否开启Rerank功能。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.rerank_min_score</code></p></td> <td><p>float</p></td> <td><p>选填</p></td> <td><p>当前知识库配置的相似度阈值</p></td> <td><p>仅开启Rerank时生效, Rerank后的相似度阈值, 低于该阈值的分块会被过滤, 取值范围<code>\[0.01-1.00\]</code>。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.rerank_top_n</code></p></td> <td><p>integer</p></td> <td><p>选填</p></td> <td><p>5</p></td> <td><p>仅开启Rerank时生效, Rerank后的top_n返回分块, 取值范围<code>\[1-20\]</code>。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.save_retriever_history</code></p></td> <td><p>bool</p></td> <td><p>选填</p></td> <td><p>false</p></td> <td><p>是否保存历史检索召回数据。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.dense_similarity_top_k</code></p></td> <td><p>integer</p></td> <td><p>选填</p></td> <td><p>100</p></td> <td><p>向量检索TopK, 通过生成输入文本的向量并在知识库中检索与其向量表示最相似的K个文本切片, 取值范围<code>\[0-100\]</code>。 dense_similarity_top_k和sparse_similarity_top_k二者之和小于等于200。</p></td> </tr> <tr> <td><p><code>rag_proxy.provider.sparse_similarity_top_k</code></p></td> <td><p>integer</p></td> <td><p>选填</p></td> <td><p>100</p></td> <td><p>关键词检索TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果, 取值范围<code>\[0-100\]</code>。 dense_similarity_top_k和sparse_similarity_top_k二者之和小于等于200。</p></td> </tr> </tbody> </table>

关于百炼平台的知识库使用操作指引，请参见：[百炼知识库操作和使用指引](https://bailian.console.aliyun.com/?tab=doc#/doc/?type=app&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2807740.html&renderType=iframe)。

关于百炼的检索更详细参数说明，请参见：[检索知识库](https://help.aliyun.com/document_detail/2834091.html)。

基础配置示例如下所示：

```
HELPCODEESCAPE-yaml
rag_proxy:
  provider:
    name: 'bailian'
    api_key: 'sk-xxxxxx'
```

## 操作步骤
以Dify外部知识库连接RAGFlow与百炼知识库为例，对插件的操作和配置步骤进行说明。

### 通过AI RAG 检索代理插件实现Dify连接RAGFlow

1. 在AI网关中创建RAGFlow检索服务。

   1. 前往[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

   2. 在左侧导航栏，选择**服务** ，然后单击**创建服务**。

   3. 以固定地址来源的RAGFlow为例，创建服务来源为固定地址的ragflow检索服务，如下图所示，端口设置为80。如果是同VPC内容器部署的RAGFlow实例，也可以采用容器服务作为服务来源创建服务。

2. 创建Agent API路由。

   1. 创建自定义Agent API。

      在对应网关实例控制台，选择**Agent API** ，然后单击**创建Agent API**，协议选择自定义。
   2. 创建Agent API路由。

      进入已经创建的Agent API，单击**创建路由**，注意需要确保路径后缀为/retrieval，服务选择步骤1创建的RAGFlow检索服务。
3. 获取API KEY并在AI网关中配置插件。

   1. 进入RAGFlow，点击右上角用户头像-\>左侧选择-\>API-\>API KEY，获取API KEY。

   2. 在对应网关实例控制台，选择**插件市场** ，然后单击**安装插件** ，插件类型选择**AI** ，然后选择AI RAG代理插件，单击**安装并配置** 进入规则配置，相关配置如下图所示。设置启用并点击**保存**后，插件生效。

4. 在Dify中创建外部知识库API。

   前往Dify控制台，点击知识库-\>外部知识库API-\>添加外部知识库API，API Endpoint使用上述网关接入点与Agent API路由路径组合（`http(s)://{endpoint}/{agent api path}`），注意需要去除/retrieval后缀，API Key可自行定义。  
   **重要**

   如果在插件中配置了rag_proxy.source.enable_to_proxy_api_key和rag_proxy.source.to_proxy_api_key，需保证API Key和rag_proxy.source.to_proxy_api_key保持一致，否则Dify访问AI网关会鉴权失败，无法执行后续路由。
5. 在Dify中连接外部知识库。

   1. 获取知识库命名空间ID。

      前往RAGFlow知识库页面，选择待检索的知识库，页面URL路径中对应部分为外部知识库ID，如下图所示。
   2. 配置知识库信息。

      前往Dify控制台，点击知识库-\>连接外部知识库，知识库名称和描述可自定义，外部知识库API选择上述步骤4创建的API，如下图所示，点击连接后完成配置。
6. 验证检索连通性。

   前往Dify知识库页面，选择上述步骤创建的知识库，在召回测试输入源文本进行验证，能够根据召回设置返回文本分块，即说明实现连通。

### 通过AI RAG 检索代理插件实现Dify连接百炼知识库

1. 在AI网关中创建百炼检索服务。

   1. 前往[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

   2. 在左侧导航栏，选择**服务** ，然后单击**创建服务**，服务来源选择DNS域名，相关配置如下图所示。

2. 在AI网关中创建自定义Agent API路由。

   1. 创建自定义Agent API。

      在左侧导航栏，选择**Agent API** ，然后单击**创建Agent API**，相关配置如下图所示，其中域名和Base Path可按需自定义，协议选择自定义。
   2. 创建Agent API路由。

      进入已创建的Agent API，单击**创建路由**，注意需要确保路径后缀为/retrieval，服务选择步骤1创建的百炼检索服务。
3. 获取API KEY并在AI网关中配置插件。

   1. 登录阿里云百炼平台[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)并获取API Key。

   2. 在对应网关实例控制台，选择**插件市场** ，然后单击**安装插件** ，插件类型选择**AI** ，然后选择AI RAG代理插件，单击**安装并配置** 进入规则配置，相关配置如下图所示。设置启用并点击**保存**后，插件生效。

4. 在Dify中连接外部知识库。

   前往Dify控制台，点击知识库-\>外部知识库API-\>添加外部知识库API，API Endpoint使用上述网关接入点与Agent API路由路径组合（`http(s)://{endpoint}/{agent api path}`），注意需要去除/retrieval后缀，API Key可自行定义。  
   **重要**

   如果在插件中配置了rag_proxy.source.enable_to_proxy_api_key和rag_proxy.source.to_proxy_api_key，需保证API Key和rag_proxy.source.to_proxy_api_key保持一致，否则Dify访问AI网关会鉴权失败，无法执行后续路由。
5. 在Dify中创建外部知识库。

   1. 获取百炼知识库ID。

      前往阿里云百炼平台[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)，选择待检索的知识库，如下图所示，获取知识库ID。
   2. 配置知识库信息。

      前往Dify控制台，点击知识库-\>连接外部知识库，知识库名称和描述可自定义，外部知识库API选择上述步骤4创建的API，外部知识库ID的格式为：{知识库ID}，如下图所示，点击连接后完成创建。
6. 验证检索连通性。

   前往Dify知识库页面，选择上述步骤创建的知识库，在召回测试输入源文本进行验证，能够根据召回设置返回文本分块，即说明实现连通。

<br />