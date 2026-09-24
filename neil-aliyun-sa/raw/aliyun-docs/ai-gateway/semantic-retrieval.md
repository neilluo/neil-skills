---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/semantic-retrieval
fetch_date: 2026-09-21
product: AI Gateway
slug: semantic-retrieval
body_sha256: a375c272c9c7dc5029b505d52626ecfa5996725c933866d49b3ab2fceef00131
body_bytes: 11015
migration_status: current
---

语义检索可基于用户请求，通过分析理解用户意图，智能选择合适的MCP工具，从而降低上下文Token，提升检索效率。本文介绍如何开启语义检索及相关配置。  

## **背景信息**
当用户开发的智能体需要调用大量MCP工具时，可能面临管理困难、工具选择不合适、Tokens消耗增加以及检索效率降低等问题。为解决相关问题，AI网关推出MCP语义检索功能，通过以下方式优化MCP工具调用过程。

* **统一入口管理**：通过AI网关构建统一的MCP服务接入点，所有Agent可通过单一端点访问网关实例中注册的全部MCP工具，实现集中化接入，降低多MCP Server分散部署带来的运维复杂度。

* **智能工具检索**：集成x_higress_tool_search语义搜索功能，基于AD向量数据库与Qwen系列大模型，提供高精度的工具推荐能力。Agent可通过自然语言描述需求，系统自动匹配并返回最相关的工具，无需预先了解具体工具名称。

* **双阶段检索机制**：采用"向量召回 + 重排序"两阶段检索架构。首先利用Qwen Embedding模型进行向量化相似度计算，获取初步候选工具集，然后可选择性地使用Qwen Rerank模型对候选结果进行精细化排序，提升最终工具推荐的准确性与相关性。

* **实时元数据同步**：建立完整的MCP工具生命周期管理流程。当用户在控制台执行MCP Server的增、删、改操作时，系统自动触发工具元信息的采集、向量化处理及持久化存储，确保向量数据库与实际部署的服务实例保持一致。

* **控制台集成化配置**：在控制台启用"语义搜索"功能后，系统将自动完成ADB集合初始化、模型参数配置、路由规则下发及数据同步等全部配置流程，实现语义搜索能力的一站式开通与管理，提供即开即用的服务体验。

## 性能表现
在Salesforce的原始数据集[xlam-function-calling-60k](https://huggingface.co/datasets/Salesforce/xlam-function-calling-60k)上，使用以下18个维度进行对比：

* **纯向量检索**：3种相似度算法（cosine、L2、IP）。

* **RRF混合搜索双路召回**：5个k值参数（10、30、60、100、200）。

  **说明**

  倒数排序融合(Reciprocal rank fusion)，有一个参数 k 控制融合效果，指定计算分数的算法的**1/(k+rank_i)**中的 k 常数，范围大于 1 的正整数。
* **Weight混合搜索**：5个α值参数（0.0、0.2、0.5、0.8、1.0）。

  **说明**

  比重排序，采用一个参数 alpha 控制向量和全文的分数比重，然后再排序，计算公式**alpha * vector_score + (1-alpha) * text_score**，参数 alpha 表示向量和全文的检索分数比重，范围为 0～1，其中 0 表示仅全文，1 表示仅向量。
* **Cascaded混合搜索**：无参数算法。

  **说明**

  先全文检索再在其基础上进行向量检索。
* **最优配置对比**：4种最优配置的综合对比。

**结果表明：**

* **Weight算法优势**：Weight混合搜索在精确测量下表现出微幅优势，α=0.8时Top-1准确率最高（80.6873%），α=0.5时Top-10准确率最高（98.3119%）

* **纯向量算法等效性**：cosine和L2算法完全一致（80.6471%），IP算法略低（80.6270%），推荐使用cosine（业界标准）

* **混合搜索价值验证**：Weight算法相比纯向量提升0.04个百分点，虽然幅度微小但在大规模应用中具有统计学意义

* **RRF算法局限**：RRF算法在所有k值下Top-1准确率显著低于纯向量（57-59% vs 80.6%），存在系统性性能瓶颈

* **全文搜索局限性**：Weight(α=0.2)准确率显著下降至76.19%，证明过度依赖全文搜索的风险

* **Cascaded表现**：Cascaded算法Top-10准确率97.6%，略低于其他算法但仍保持较高水准

* **性能一致性**：所有算法搜索时间均在0.32-0.35秒范围内，性能差异微小

### 评测结果

#### **工具检索准确性**

<table> <thead> <tr> <td><p><b>算法类型</b></p></td> <td><p><b>配置</b></p></td> <td><p><b>Top-1准确率</b></p></td> <td><p><b>Top-10准确率</b></p></td> <td><p><b>平均搜索时间</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Weight混合</p></td> <td><p>α=0.8</p></td> <td><p><b>80.687%</b></p></td> <td><p>98.292%</p></td> <td><p>0.3498s</p></td> </tr> <tr> <td><p>纯向量</p></td> <td><p>Cosine</p></td> <td><p>80.647%</p></td> <td><p>98.272%</p></td> <td><p>0.3194s</p></td> </tr> <tr> <td><p>纯向量</p></td> <td><p>L2</p></td> <td><p>80.647%</p></td> <td><p>98.272%</p></td> <td><p>0.3187s</p></td> </tr> <tr> <td><p>Weight混合</p></td> <td><p>α=1.0</p></td> <td><p>80.647%</p></td> <td><p>98.272%</p></td> <td><p>0.3177s</p></td> </tr> <tr> <td><p>纯向量</p></td> <td><p>IP</p></td> <td><p>80.627%</p></td> <td><p>98.252%</p></td> <td><p>0.3237s</p></td> </tr> <tr> <td><p>Weight混合</p></td> <td><p>α=0.5</p></td> <td><p>80.527%</p></td> <td><p><b>98.312%</b></p></td> <td><p>0.3503s</p></td> </tr> <tr> <td><p>Weight混合</p></td> <td><p>α=0.2</p></td> <td><p>76.186%</p></td> <td><p>98.292%</p></td> <td><p>0.3464s</p></td> </tr> <tr> <td><p>RRF混合</p></td> <td><p>k=10</p></td> <td><p>59.043%</p></td> <td><p>96.805%</p></td> <td><p>0.3519s</p></td> </tr> <tr> <td><p>RRF混合</p></td> <td><p>k=60</p></td> <td><p>57.918%</p></td> <td><p>96.744%</p></td> <td><p>0.3508s</p></td> </tr> </tbody> </table>

**关键发现**：

* **Weight算法微幅领先**：Weight(α=0.8)在Top-1准确率上比纯向量高0.0402个百分点，Weight(α=0.5)在Top-10准确率上比纯向量高0.0402个百分点

* **算法精确排序**：cosine=L2 \> IP，Weight(α=1.0)等同于纯向量cosine，证明α=1.0时完全退化为纯向量搜索

* **RRF算法系统性劣势**：所有k值配置下Top-1准确率均低于80%，与纯向量存在20+个百分点差距，不适合精确匹配场景

#### **Top-K准确率分析**

**纯向量算法梯度表现**：

* Top-1: 80.647%

* Top-3: 92.785%

* Top-5: 95.96%

* Top-10: 98.272%

* Top-15: 98.995%

* Top-20: 99.297%

**检索召回率**：99.3%的查询能够在Top-20结果中找到正确工具，表明向量搜索具有优秀的召回能力。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1153551671/p1019939.png)

#### **混合搜索算法深度分析**

##### **Weight算法参数优化**

<table> <thead> <tr> <td><p><b>α值</b></p></td> <td><p><b>语义含义</b></p></td> <td><p><b>Top-1准确率</b></p></td> <td><p><b>Top-10准确率</b></p></td> <td><p><b>推荐场景</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>0.0</p></td> <td><p>纯全文搜索</p></td> <td><p>54.7%</p></td> <td><p>95.5%</p></td> <td><p>关键词匹配</p></td> </tr> <tr> <td><p>0.2</p></td> <td><p>主要全文+少量向量</p></td> <td><p>76.2%</p></td> <td><p>98.3%</p></td> <td><p>文本相关性优先</p></td> </tr> <tr> <td><p>0.5</p></td> <td><p>平衡混合</p></td> <td><p><b>80.5%</b></p></td> <td><p><b>98.3%</b></p></td> <td><p><b>推荐配置</b></p></td> </tr> <tr> <td><p>0.8</p></td> <td><p>主要向量+少量全文</p></td> <td><p><b>80.7%</b></p></td> <td><p><b>98.3%</b></p></td> <td><p>语义理解优先</p></td> </tr> <tr> <td><p>1.0</p></td> <td><p>纯向量搜索</p></td> <td><p>80.6%</p></td> <td><p>98.3%</p></td> <td><p>等同纯向量</p></td> </tr> </tbody> </table>

**优化建议**：α=0.5-0.8区间为最优选择，能够充分利用向量语义理解和全文检索的优势。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1153551671/p1019938.png)

##### **RRF算法性能分析**

<table> <thead> <tr> <td><p><b>k值</b></p></td> <td><p><b>Top-1准确率</b></p></td> <td><p><b>Top-10准确率</b></p></td> <td><p><b>性能特点</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>10</p></td> <td><p>59.0%</p></td> <td><p>96.8%</p></td> <td><p>偏向排名靠前结果</p></td> </tr> <tr> <td><p>30</p></td> <td><p>57.4%</p></td> <td><p>96.7%</p></td> <td><p>中等平衡</p></td> </tr> <tr> <td><p>60</p></td> <td><p>57.9%</p></td> <td><p>96.7%</p></td> <td><p>经验推荐值</p></td> </tr> <tr> <td><p>100</p></td> <td><p>57.6%</p></td> <td><p>96.7%</p></td> <td><p>更平衡的融合</p></td> </tr> <tr> <td><p>200</p></td> <td><p>57.6%</p></td> <td><p>96.7%</p></td> <td><p>接近线性组合</p></td> </tr> </tbody> </table>

**性能瓶颈**：RRF算法在所有k值配置下均表现出Top-1准确率的系统性劣势，建议在对精确匹配要求较高的场景中谨慎使用。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1153551671/p1019937.png)

#### **搜索性能分析**

##### **响应时间对比**

* **纯向量搜索**：0.319-0.324秒

* **Weight混合搜索**：0.318-0.350秒

* **RRF混合搜索**：0.351-0.352秒

* **Cascaded搜索**：0.320秒

**性能结论**：所有算法的搜索时间均控制在350毫秒以内，满足实时检索需求。混合搜索相比纯向量搜索仅增加约30毫秒延迟。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1153551671/p1019940.png)

##### **错误案例分析**

总错误案例：4,214个（占总查询的4.7%）。

**错误分布**：

* Weight(α=0.0)：2,255个错误（纯全文搜索局限性）。

* RRF系列：平均161个错误/配置。

* 纯向量系列：平均85个错误/配置。

* Weight(α=0.2-1.0)：83-85个错误/配置。

**错误模式**：主要集中在语义相似但功能不同的工具混淆，以及多工具场景下的优先级判断。

## 操作步骤
### 启用语义检索

1. 在AI 网关控制台的[实例](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)页面，在顶部菜单栏选择目标实例所在地域。

2. 在**实例**页面，单击目标网关实例ID。

3. 在左侧导航栏选择**MCP 管理** ，单击**语义检索**页签。

4. 单击**编辑** ，开启**启用语义检索** ，选择**检索工具接入点** ，单击**确定**发布语义检索。

### 配置消费者认证

语义检索支持配置认证鉴权，开启后仅授权的消费者可通过API Key访问，无认证或认证异常的请求将被拒绝。

1. 在语义检索页签，选择**消费者认证**。

2. 单击**配置信息** 功能编辑按钮，在MCP 服务消费者认证开启**启用状态**。认证方式默认选择API KEY。

3. 单击**授权** ，在**添加消费者授权**页面选择消费者。

   **说明**

   消费者认证方式需使用API Key，不支持JWT认证方式的消费者使用语义检索。
4. 单击**添加**完成授权。

<br />