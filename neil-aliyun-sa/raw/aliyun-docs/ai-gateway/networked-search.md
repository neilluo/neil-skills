---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/networked-search
fetch_date: 2026-09-21
product: AI Gateway
slug: networked-search
body_sha256: dfb88bef18bf0c83db12623a2e726ea434eaf1094b4907a5d1bde503cb9f3e5f
body_bytes: 7606
migration_status: current
---

联网搜索策略能够扩展大语言模型的知识范围，通过实时检索互联网数据（支持夸克搜索引擎），提升生成内容的准确性与时效性。本文将为您介绍Model API 联网搜索策略的功能优势，以及开启步骤。  

## **策略说明**
* 搜索引擎支持：夸克搜索引擎（阿里云信息查询服务），扩展大模型的知识范围。

  1. 搜索重写：将模型生成的多种结果，在搜索引擎中检索后的优化和重构，生成高质量、高相关性的上下文信息。

  2. 意图识别：快速分析大模型输入，判断是否需要调用联网搜索。

* 灵活配置选项：联网搜索配置，支持自定义返回结果数量、超时时间、查询时间范围及行业筛选等参数，提升生成内容的准确性和时效性。

* 结果渲染：支持中英文双语输出、展示引用来源，并提供引用格式自定义配置，满足多样化的展示需求。

## 操作步骤
1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击目标**API名称** 进入**API详情**页面。

3. 单击**策略与插件** ，打开**联网搜索**开关并配置相关参数。

   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>联网搜索</b></p></td> <td><p>开启或关闭联网搜索开关，默认关闭。</p></td> </tr> <tr> <td><p><b>搜索引擎</b></p></td> <td><p>目前仅支持<b>夸克</b>（阿里云信息查询服务）。</p></td> </tr> <tr> <td><p><b>服务状态</b></p></td> <td><p>首次使用夸克联网搜索时，默认<b>服务状态</b>为<b>未开通</b>状态。单击<b>前往开通</b>，跳转至信息查询服务的服务开通页面进行开通。</p><p><img></p><p>开通后，单击<b>开通校验</b>，控制台的<b>服务状态</b>会更新为<b>试用中</b>。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>阿里云信息查询服务提供15天的免费试用，用量为1000次/天，性能限制5 QPS。<span>您可以进行正式接口的申请，具体步骤详情，请参见<a href="https://help.aliyun.com/document_detail/2869993.html">正式开通流程说明</a>。</span></p> </div> </div></td> </tr> <tr> <td><p><b>搜索配置</b></p></td> <td><p><b>API Key</b></p></td> <td><p>访问凭证。<span>您可以参考<a href="https://help.aliyun.com/document_detail/2872258.html">创建并查看凭证</a>，</span>在访问信息查询服务<a href="https://ipaas.console.aliyun.com/api-key">凭证管理控制台</a>进行获取。</p></td> </tr> <tr> <td><p><b>返回结果数量</b></p></td> <td><p>范围1-10，最大值为10，即最多返回10篇结果。</p></td> </tr> <tr> <td><p><b>超时时间</b></p></td> <td><p>默认3000ms。</p></td> </tr> <tr> <td><p><b>查询时间范围</b></p></td> <td> <ul> <li><p>1天内</p></li> <li><p>1周内</p></li> <li><p>1月内</p></li> <li><p>1年内</p></li> <li><p>无限制</p></li> </ul></td> </tr> <tr> <td><p><b>行业（可选）</b></p></td> <td> <ul> <li><p>金融</p></li> <li><p>法律</p></li> <li><p>医疗</p></li> <li><p>互联网</p></li> <li><p>税务</p></li> <li><p>新闻省级</p></li> <li><p>新闻中央</p></li> </ul></td> </tr> <tr> <td><p><b>结果渲染</b></p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>结果渲染用于配置搜索结果的展示格式与丰富度。</p> </div> </div></td> <td><p><b>默认语言</b></p></td> <td><p>支持中、英文。</p></td> </tr> <tr> <td><p><b>输出引用来源</b></p></td> <td><p>是/否，默认为否，不展示引用来源。</p></td> </tr> <tr> <td><p><b>引用来源位置</b></p></td> <td><p>首部/尾部，默认位置为首部。</p></td> </tr> <tr> <td><p><b>内容类型</b></p></td> <td> <ul> <li><p>摘要（默认）：只返回搜索条目的摘要信息，满足大模型的基础推理需求，覆盖常规问答任务的信息检索需求。</p></li> <li><p>正文：返回搜索条目的正文信息，信息量较大但内容详细，适合需要信息细节的场景。</p></li> </ul></td> </tr> <tr> <td><p><b>引用格式</b></p></td> <td><p><code>%s</code>为引用条目的渲染占位符，可以按需修改引用条目的展示格式。可以单击右侧<b>填写示例</b>查看引用格式示例。</p></td> </tr> <tr> <td><p><b>自动启用</b></p></td> <td><p><b>是否开启</b></p></td> <td><p>是否开启自动启用联网搜索。</p> <ul> <li><p>开启：调用时进行联网搜索，若已配置意图识别，则根据意图识别的结果进行处理。</p></li> <li><p>关闭：调用时默认不进行联网搜索，可通过调用参数手动控制是否要进行联网搜索。详细信息和使用示例，请参见<a href="#00ea5a7ba2oq4">手动控制参数说明</a>。</p></li> </ul></td> </tr> <tr> <td><p></p><p><b>意图识别</b></p></td> <td><p><b>是否开启</b></p></td> <td><p>是否开启<b>意图识别</b>配置。意图识别：</p> <ul> <li><p>判断是否需要进行联网搜索。</p></li> <li><p>对联网搜索的搜索语句进行改写、拓展，增强搜索能力。</p></li> </ul> <div> <div> <i></i> </div> <div> <strong>重要 </strong> <p><b>意图识别</b>能力也会消耗Token，并且不会在模型调用监控中被统计。</p> </div> </div></td> </tr> <tr> <td><p><b>AI 服务</b></p></td> <td><p>选择AI 服务。</p></td> </tr> <tr> <td><p><b>模型名称</b></p></td> <td><p>选择模型名称。</p></td> </tr> <tr> <td><p><b>超时时间</b></p></td> <td><p>设置超时时间，默认5000ms。</p></td> </tr> <tr> <td><p><b>搜索重新生成的最大查询次数</b></p></td> <td><p>重新生成搜索查询的最大次数，默认1次。若配置为大于1次，改写将会产生多个搜索语句进行并发搜索，并最终聚合个多个搜索的结果。</p></td> </tr> </tbody> </table>
4. 确认配置信息并单击**保存** **。**

### 手动控制参数说明

当请求中包含`web_search_options`字段时，联网搜索会被激活。

使用示例：

```
HELPCODEESCAPE-json
（"web_search_options": {}）
```

若已经配置意图识别，`web_search_options`参数还具备控制搜索改写数量的能力，通过`search_context_size`字段控制。

`search_context_size`支持三个级别：

* low：生成1个搜索查询（适合简单问题）。

* medium：生成3个搜索查询（默认值）。

* high：生成5个搜索查询（适合复杂问题）。

使用示例：

```
HELPCODEESCAPE-json
{
  "web_search_options": {
    "search_context_size": "medium"
  }
}
```

在curl中完整的请求样例：

```
HELPCODEESCAPE-shell
curl --location 'http://your-domain/v1/chat/completions' \
   --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen-max",
    "stream": true,
    "web_search_options": {
        "search_context_size": "medium"
    },
    "messages": [
        {
            "role": "user",
            "content": "介绍下通义千问"
        }
    ]
}'
```

### 效果展示

* 当选择**输出引用来源** 为`是`时：

  ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3656331471/p925375.png)
* 当选择**输出引用来源** 为`否`时，效果为：

  ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3656331471/p925373.png)