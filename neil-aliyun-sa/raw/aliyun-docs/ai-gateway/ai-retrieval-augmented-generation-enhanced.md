---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-retrieval-augmented-generation-enhanced
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-retrieval-augmented-generation-enhanced
body_sha256: 03c899db23c0d7240eb98b5d822fc6417f2f1a7d3cd1bf4574ef32bdac0bc3c4
body_bytes: 16066
migration_status: current
---

本文介绍AI检索增强生成（加强版）及其使用方法。  

## 功能说明
通过对接主流RAG引擎实现LLM调用前的自动检索增强生成，支持RARFlow和百炼知识库。

## 运行属性
* 插件执行阶段：`默认阶段`。

* 插件执行优先级：`400`。

## 配置说明
### 基本配置

<table> <thead> <tr> <td> <p><b>名称</b></p> </td> <td> <p><b>数据类型</b></p> </td> <td> <p><b>填写要求</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>rag.rag_engine_type</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>RAG引擎类型，支持的枚举类型包括: ragflow、bailian。</p> </td> </tr> <tr> <td> <p><code>result_placement_type</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>append</p> </td> <td> <p>支持用户模板替换占位符，如果选择replace，则System提示词模板中的占位符<code>{{higressRagResultReplacementKey}}</code>会被替换为RAG生成的内容，如果选择append，则RAG生成的内容会被追加到用户模板中，支持的枚举类型包括: append、replace。</p> </td> </tr> </tbody> </table>

### RAGFlow配置

当选择RAGFlow作为RAG引擎时（`rag.rag_engine_type=ragflow`），请参考以下说明进行配置。
<table> <thead> <tr> <td> <p><b>名称</b></p> </td> <td> <p><b>数据类型</b></p> </td> <td> <p><b>填写要求</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>rag.ragflow.api_key</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>调用RAGFlow API的API Key，可在RAGFlow控制台右上角头像-API-RAGFlow API处获取。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.serviceFQDN</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>RAGFlow在AI网关的服务名。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.servicePort</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>RAGFlow在AI网关的服务端口。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.dataset_ids</code></p> </td> <td> <p>list\[string\]</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>检索RAGFlow的DataSet ID。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.serviceHost</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>-</p> </td> <td> <p>AI网关访问RAGFlow时域名。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.document_ids</code></p> </td> <td> <p>list\[string\]</p> </td> <td> <p>选填</p> </td> <td> <p>-</p> </td> <td> <p>检索RAGFlow的Document ID。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.similarity_threshold</code></p> </td> <td> <p>float</p> </td> <td> <p>选填</p> </td> <td> <p>0.2</p> </td> <td> <p>相似度阈值, 低于阈值的分块会被过滤。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.top_n</code></p> </td> <td> <p>integer</p> </td> <td> <p>选填</p> </td> <td> <p>30</p> </td> <td> <p>返回相似度最高的top_n个分块，其他分块会被过滤。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.vector_similarity_weight</code></p> </td> <td> <p>float</p> </td> <td> <p>选填</p> </td> <td> <p>0.3</p> </td> <td> <p>向量余弦相似度权重，如果x表示向量余弦相似度，则<code>(1-x)</code>表示语义相似度权重。</p> </td> </tr> <tr> <td> <p><code>rag.ragflow.rerank_id</code></p> </td> <td> <p>integer</p> </td> <td> <p>选填</p> </td> <td> <p>-</p> </td> <td> <p>RAG引擎中配置的Rerank模型的ID。</p> </td> </tr> </tbody> </table>

关于RAGFlow的知识库使用操作指引，请参见：[Configure knowledge base](https://ragflow.io/docs/dev/configure_knowledge_base)。

关于RAGFlow的检索更详细参数说明，请参见：[Retrieve chunks](https://ragflow.io/docs/dev/http_api_reference#retrieve-chunks)。

基础配置实例如下所示。

```
HELPCODEESCAPE-yaml
rag:
  rag_engine_type: "ragflow"
  ragflow:
    api_key: "xxxxxxxx"
    serviceFQDN: "xxxxxxxx"
    servicePort: 80
    dataset_ids:
      - "xxxxxxxx"
    document_ids:
      - "xxxxxxxx"
    similarity_threshold: 0.2
    top_n: 5
    vector_similarity_weight: 0.3
    rerank_id: "gte-rerank"
```

### 百炼知识库配置

当选择百炼知识库作为RAG引擎时（`rag.rag_engine_type=bailian`）, 请参考以下说明进行配置。
<table> <thead> <tr> <td> <p><b>名称</b></p> </td> <td> <p><b>数据类型</b></p> </td> <td> <p><b>填写要求</b></p> </td> <td> <p><b>默认值</b></p> </td> <td> <p><b>描述</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>rag.bailian.ak</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>调用百炼的access key，获取方式参考：<a href="https://help.aliyun.com/document_detail/2713037.html">业务空间成员管理</a>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.sk</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>调用百炼的secret key，获取方式参考：<a href="https://help.aliyun.com/document_detail/2713037.html">业务空间成员管理</a>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.serviceFQDN</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>百炼服务在AI网关的服务名。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.workspace_id</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>阿里云百炼业务空间ID，获取方式参考：<a href="https://help.aliyun.com/document_detail/2713037.html">业务空间成员管理</a>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.index_id</code></p> </td> <td> <p>string</p> </td> <td> <p>必填</p> </td> <td> <p>-</p> </td> <td> <p>阿里云百炼知识库ID，获取方式参考：<a href="https://help.aliyun.com/document_detail/2852772.html">知识库API指南</a>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.servicePort</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>443</p> </td> <td> <p>百炼在AI网关的服务端口。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.serviceHost</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>bailian.cn-beijing.aliyuncs.com</p> </td> <td> <p>AI网关访问百炼时域名。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.enable_reranking</code></p> </td> <td> <p>bool</p> </td> <td> <p>选填</p> </td> <td> <p>false</p> </td> <td> <p>是否开启Rerank。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.rerank_min_score</code></p> </td> <td> <p>float</p> </td> <td> <p>选填</p> </td> <td> <p>当前知识库配置的相似度阈值</p> </td> <td> <p>仅开启Rerank时生效，Rerank后的相似度阈值，低于该阈值的分块会被过滤，取值范围：<code>\[0.01 - 1.00\]</code>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.rerank_top_n</code></p> </td> <td> <p>integer</p> </td> <td> <p>选填</p> </td> <td> <p>5</p> </td> <td> <p>仅开启Rerank时生效，Rerank后的top_n返回分块, 取值范围：<code>\[1 - 20\]</code>。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.rerank_model</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>gte-rerank-hybrid</p> </td> <td> <p>仅开启Rerank时生效，Rerank模型，支持的模型包括：gte-rerank-hybrid、gte-rerank。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.enable_rewrite</code></p> </td> <td> <p>bool</p> </td> <td> <p>选填</p> </td> <td> <p>false</p> </td> <td> <p>是否开启会话改写。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.rewrite_model</code></p> </td> <td> <p>string</p> </td> <td> <p>选填</p> </td> <td> <p>conv-rewrite-qwen-1.8b</p> </td> <td> <p>仅开启会话改写时生效，会话改写模型名称，会基于会话上下文自动调整原始用户问题以提升检索效果，支持的模型包括：conv-rewrite-qwen-1.8b。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.save_retriever_history</code></p> </td> <td> <p>bool</p> </td> <td> <p>选填</p> </td> <td> <p>false</p> </td> <td> <p>是否保存历史检索召回数据。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.dense_similarity_top_k</code></p> </td> <td> <p>integer</p> </td> <td> <p>选填</p> </td> <td> <p>100</p> </td> <td> <p>向量检索TopK，通过生成输入文本的向量并在知识库中检索与其向量表示最相似的K个文本切片，取值范围：<code>\[0 - 100\]</code>。</p> <p>dense_similarity_top_k和sparse_similarity_top_k二者之和小于等于200。</p> </td> </tr> <tr> <td> <p><code>rag.bailian.sparse_similarity_top_k</code></p> </td> <td> <p>integer</p> </td> <td> <p>选填</p> </td> <td> <p>100</p> </td> <td> <p>关键词检索TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果，取值范围：<code>\[0 - 100\]</code>。</p> <p>dense_similarity_top_k和sparse_similarity_top_k二者之和小于等于200。</p> </td> </tr> </tbody> </table>

关于百炼平台的知识库使用操作指引，请参见：[百炼知识库操作和使用指引](https://bailian.console.aliyun.com/?tab=doc#/doc/?type=app&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2807740.html&renderType=iframe)。

关于百炼的检索更详细参数说明，请参见：[检索知识库](https://help.aliyun.com/document_detail/2834091.html)。

基础配置示例如下所示。

```
HELPCODEESCAPE-yaml
rag:
  rag_engine_type: bailian
  bailian:
    ak: xxxxxxxx
    sk: xxxxxxxx
    workspace_id: xxxxxxxx
    index_id: xxxxxxxx
    serviceFQDN: xxxxxxxx.dns
    enable_reranking: true
    rerank_min_score: 0.3
    rerank_top_n: 5
    save_retriever_history: false
```

## 操作指引
### RAGFlow

1. [创建Model API](https://help.aliyun.com/document_detail/2859333.html#9d7f312e31snz)。在AI网关创建AI服务和文本生成场景Model API，确保可以通过Model API访问模型进行文本对话。

   创建完成后，在 **Model API** 列表中可看到已创建的 API **bailian-llm** ，类型为文本生成，域名为 `*.example.com`（HTTP），模型服务为 **bailian.ai** 。可在操作列对该 API 进行**编辑** 、**调试** 或**删除**。
2. 创建服务来源为固定地址的ragflow检索服务。在对应网关实例控制台的左侧导航栏，单击**服务** ，并单击**创建服务**。

   > 如果是同VPC内容器部署的Ragflow的实例，也可以采用容器服务来源创建服务。
   * **服务来源**：选择固定地址。

   * **服务名称** ：自定义服务名称，例如`ragflow`。

   * **服务地址** ：格式为`IP:端口`，此处端口设置为80。

   * **TLS模式**：保持默认关闭。

3. 获取Ragflow服务FQDN和Port。

   单击上述步骤创建的RagFlow服务，获取FQDN。RagFlow Port默认为80，用户可根据需要自行获取和设置。
4. 获取待访问的RAGFlow信息。

   1. **获取API Key**。进入RAGFlow控制台，单击右上角用户头像-\>左侧选择API-\>API KEY，获取API Key。

   2. **获取Dataset ID**。前往RAGFlow的知识库页面，单击需要被检索的知识库，网页url中的id即为Dataset ID。

   3. （可选）**获取Document ID**。前往RAGFlow的知识库页面，单击需要被检索的知识库，单击需要被检索的文档名，网页url中的doc_id即为Document ID。

5. 在AI网关配置插件。在对应网关实例控制台，选择**插件** \>**安装插件** \>**AI** \>**AI检索增强生成（加强版）** ，单击**安装并配置**，配置到对应的生效范围。填入前序步骤获取的必需参数（api_key、serviceFQDN、dataset_ids、servicePort），可选参数可按需添加，单击启用后，配置即可生效。

   配置格式为 YAML，顶层字段 `rag_engine_type` 设为 `ragflow`，其余参数嵌套在 `ragflow` 节点下。可选参数包括 `document_ids`、`similarity_threshold`（示例值 0.2）、`top_n`（示例值 5）、`vector_similarity_weight`（示例值 0.3）、`rerank_id`（示例值 gte-rerank）。生效范围选择**实例级别** ，开启启用状态开关后单击**保存**。
6. 调试并验证效果。在对应网关实例控制台，单击**Model API** ，选择插件作用生效的API，并单击**调试**，验证添加RAG检索能力之后的模型返回结果。

### 百炼知识库

1. [创建Model API](https://help.aliyun.com/document_detail/2859333.html#9d7f312e31snz)。在AI网关创建AI服务和文本生成场景Model API，确保可以通过Model API访问模型进行文本对话。

   创建完成后，在 **Model API** 列表中可看到已创建的 API **bailian-llm** ，类型为文本生成，域名为 `*.example.com`（HTTP），模型服务为 **bailian.ai** 。可在操作列对该 API 进行**编辑** 、**调试** 或**删除**。
2. 创建服务来源为DNS域名的百炼检索服务。在对应网关实例控制台，选择**服务** \> **创建服务**，配置表单信息。

   * **服务来源**：选择DNS域名。

   * **服务名称** ：自定义服务名称，例如`bailian-rag`。

   * **服务地址** ：格式为`DNS域名:端口`，此处端口设置为443。

   * **TLS模式**：选择单向TLS。

3. 获取百炼检索服务FQDN。单击上述步骤创建百炼检索服务，获取FQDN。

   在服务详情页的**概览** \> **基本信息** 区域，查看**FQDN** 字段的值，例如 `bailian-rag.dns`。
4. 获取待访问的百炼知识库信息

   1. 获取AK/SK。登录阿里云[RAM访问控制台](https://ram.console.aliyun.com/overview)，参考[创建AccessKey](https://help.aliyun.com/document_detail/116401.html)获取AccessKey和AccessKey Secret。

      **说明**

      为了您的数据安全，强烈建议您创建子账号并使用子账号AK/SK。需要保证您的子账号：
      * 具有AliyunBailianDataFullAccess或sfm:Retrieve的操作权限，参考[管理RAM用户的权限](https://help.aliyun.com/document_detail/116146.html)为子账号授权。

      * 子账号已经被授权加入到百炼业务空间权限，参考[业务空间成员管理](https://help.aliyun.com/document_detail/2713037.html)。

   2. 获取知识库命名空间ID。前往百炼应用页面，单击左下角查看知识库所在账号空间详情，获取业务空间ID。

   3. 获取知识库ID。单击数据-知识库，选择待外挂检索的知识库，获取知识库ID。

5. 在AI网关配置插件。在对应网关实例控制台，选择**插件** \>**安装插件** \>**AI** \>**AI检索增强生成（加强版）** ，单击**安装并配置**，配置到对应的生效范围。填入前序步骤获取的必需参数（ak、sk、serviceFQDN、workspace_id、index_id），可选参数可按需添加，单击启用后，配置即可生效。

   配置生效范围选择 **Model API级插件规则** ，在插件规则 YAML 编辑区中，`rag` 节点下设置 `rag_engine_type` 为 `bailian`，在 `bailian` 子节点中填入各必需参数，其中 `serviceFQDN` 示例值为 `bailian-rag.dns`。同时在上方 API 选择面板中勾选需要绑定的目标 API。

   配置完成后，在**Model API级插件规则** 列表中可看到关联 **bailian-llm** 的规则条目，此时生效状态为未启用。
6. 调试并验证效果。在对应网关实例控制台，单击**Model API** ，选择插件作用生效的API，并单击**调试**，验证添加RAG检索能力之后的模型返回结果。