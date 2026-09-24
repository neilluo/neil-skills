---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/enable-llm-api-compression-to-save-bandwidth-costs
fetch_date: 2026-09-21
product: AI Gateway
slug: enable-llm-api-compression-to-save-bandwidth-costs
body_sha256: 48fa37ed2e25ef2738278d05006770aab93b806b195275dcaad8239d24e270a2
body_bytes: 9932
migration_status: current
---

随着大语言模型（LLM）的快速发展，LLM API 已成为 AI 原生应用的核心基础设施。本文基于阿里云 AI 网关在 LLM API 场景下的实际压测数据，评估了多种压缩算法（ZSTD、GZIP、Brotli、QATZip）在流式与非流式响应场景中的性能表现。测试结果显示，启用响应压缩功能可显著降低网络带宽消耗，在流式响应场景下最高可减少 90% 以上的出方向带宽成本。  

## **LLM API 特点**
LLM API 通常具备以下特征：

* **以流式传输为主**：为提升响应实时性，多数 LLM API 采用 Server-Sent Events（SSE）或流式数据传输机制。

* **响应数据量显著大于请求数据量**：典型场景中，请求通常仅包含简短的提示词（Prompt），而响应则包含完整的生成文本，部分情况下还包括推理过程、置信度信息等附加内容，导致响应数据规模远超请求。因此，网络带宽消耗主要集中于出方向，即响应数据的传输阶段。

* **响应数据高度结构化**：LLM API 的响应通常以 JSON 格式组织，具有明确的字段结构和较高的数据冗余度。结构化数据因存在重复模式与固定语法元素，更易于通过通用压缩算法实现高效压缩。在流式传输场景下，连续的数据帧常包含相似的结构信息，进一步提升了可压缩性。

综上，针对 LLM API 的响应数据，尤其是在流式传输场景下实施压缩，可显著降低传输带宽占用，提升整体传输效率。

## 核心优势与适用场景
### 解决的核心问题

* **高带宽成本**：LLM 应用的响应通常为大量文本，在调用量较大时会产生较高的公网流出带宽费用。

* **弱网体验不佳**：在移动或网络不佳的环境下，未经压缩的大体积响应会导致客户端卡顿，影响流式体验。

### 量化收益

启用响应压缩，特别是针对流式 API，能节约成本并提升体验。

* **成本节约**：

  * 在 **流式响应** 场景下，带宽节省率可达 **92% - 97%**。

  * 在 **非流式响应** 场景下，带宽节省率约为 **28% - 40%**。

* **体验提升**：降低传输数据量，加快响应在客户端的加载速度，在弱网环境下效果明显。

### 适用场景与决策建议

<table> <thead> <tr> <td><p><b>场景</b></p></td> <td><p><b>推荐策略</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>LLM 流式 API</b></p></td> <td><p><b>推荐</b></p></td> <td><p>例如基于 SSE 的对话接口。流式传输的协议和数据结构存在冗余，压缩效果好，可节省最高 97% 的带宽。</p></td> </tr> <tr> <td><p><b>返回大量文本/JSON 的普通 API</b></p></td> <td><p><b>推荐</b></p></td> <td><p>例如返回长文章、大列表的 API。当响应体大于 100KB 时，压缩能带来带宽节约。</p></td> </tr> <tr> <td><p><b>API 响应体已是压缩格式</b></p></td> <td><p><b>不推荐</b></p></td> <td><p>例如图片（JPEG/PNG）、视频、二进制文件等。对已压缩数据再次压缩，效果不佳，且会增加 CPU 开销。</p></td> </tr> <tr> <td><p><b>API 响应体极小</b></p></td> <td><p><b>不推荐</b></p></td> <td><p>例如小于 1KB 的响应。压缩带来的开销（CPU、延迟）可能超过其收益。</p></td> </tr> </tbody> </table>

## 性能评测
### 测试环境

<table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>配置</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>网关节点</p></td> <td><p>1 核 2GB 内存，单节点部署</p></td> </tr> <tr> <td><p>压测 QPS</p></td> <td><p>固定 30 QPS</p></td> </tr> <tr> <td><p>测试场景</p></td> <td><p>LLM API 实际调用场景</p></td> </tr> <tr> <td><p>压缩算法</p></td> <td><p>ZSTD、GZIP、Brotli、QATZip</p></td> </tr> </tbody> </table>

### 压缩算法

本次测试对比四种压缩算法：
<table> <thead> <tr> <td><p><b>算法</b></p></td> <td><p><b>技术特点</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>GZIP</b></p></td> <td><p>经典的 DEFLATE 压缩算法，兼容性优秀。</p></td> </tr> <tr> <td><p><b>ZSTD</b></p></td> <td><p>Facebook 开源，压缩比和速度平衡优秀。</p></td> </tr> <tr> <td><p><b>Brotli</b></p></td> <td><p>Google 开源，压缩比高但 CPU 消耗较大。</p></td> </tr> <tr> <td><p><b>QATZip</b></p></td> <td><p>基于 Intel QAT 技术的硬件加速 GZIP，适用于高并发、低延迟、低 CPU 消耗场景。</p></td> </tr> </tbody> </table>

**QATZip 技术详解**：

QATZip 是基于 Intel QuickAssist Technology（QAT）硬件加速技术实现的 GZIP 压缩方案。QAT 是 Intel 提供的专用硬件加速平台，通过在独立的加速卡上执行压缩与解压缩操作，将原本由 CPU 承担的计算密集型任务卸载至专用硬件处理，从而显著提升系统性能。

**工作原理**：

QAT 硬件加速卡集成专用压缩/解压缩引擎，针对数据压缩计算任务进行优化，通过 PCIe 总线与主机连接，支持与CPU并行运行及异步操作模式。CPU 可将压缩任务提交至加速卡后立即返回处理其他任务，实现高效的任务卸载。

阿里云 AI 网关与云原生 API 网关支持 QATZip 技术，可通过硬件加速 Gzip 压缩，有效降低CPU利用率并减少网络带宽消耗。

## 测试方法
本次测试对比四种压缩算法在两种响应模式下的表现：

* **非流式响应**：一次性返回完整的 JSON 响应。

* **流式响应**：采用流式传输模式（SSE/Chunked Transfer Encoding）。

测试指标：

**压缩比**：压缩后数据大小与原数据大小的比例（越小越好）。

**CPU 消耗**：网关节点在处理压缩时的 CPU 使用率。

## 测试结果
<table> <thead> <tr> <td><p><b>压缩算法</b></p></td> <td><p><b>响应模式</b></p></td> <td><p><b>压缩比</b></p></td> <td><p><b>CPU 消耗</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>ZSTD</b></p></td> <td><p>非流式</p></td> <td><p><b>72%</b></p></td> <td><p>6%</p></td> </tr> <tr> <td><p></p></td> <td><p>流式</p></td> <td><p><b>2.8%</b></p></td> <td><p>23.6%</p></td> </tr> <tr> <td><p><b>GZIP</b></p></td> <td><p>非流式</p></td> <td><p><b>68.8%</b></p></td> <td><p>6%</p></td> </tr> <tr> <td><p></p></td> <td><p>流式</p></td> <td><p><b>7.2%</b></p></td> <td><p>30%</p></td> </tr> <tr> <td><p><b>Brotli</b></p></td> <td><p>非流式</p></td> <td><p><b>60.8%</b></p></td> <td><p>6.2%</p></td> </tr> <tr> <td><p></p></td> <td><p>流式</p></td> <td><p><b>7.2%</b></p></td> <td><p>34.5%</p></td> </tr> <tr> <td><p><b>QATZip</b></p></td> <td><p>非流式</p></td> <td><p><b>67%</b></p></td> <td><p>4.8%</p></td> </tr> <tr> <td><p></p></td> <td><p>流式</p></td> <td><p><b>2.9%</b></p></td> <td><p>20.9%</p></td> </tr> </tbody> </table>

**注：压缩比 = 压缩后大小 / 原始大小**，压缩比越小表示压缩效果越好。例如，2.8% 表示压缩后数据仅为原始数据的 2.8%，节省了 97.2% 的带宽。

## 结果分析
### 流式响应压缩优势明显

流式响应的压缩效果显著优于非流式响应，两者压缩比可相差 **10 倍以上**。

**非流式场景**：压缩比在 60%-72% 区间，带宽节省约 28%-40%。

**流式场景** ：压缩比可低至 2.8%-7.2%，带宽节省高达 **92%-97%**

流式响应采用分块传输机制，数据按 token 逐步返回。每个返回的 chunk 中包含重复性较高的数据结构（如 JSON 字段名、格式字符等），导致冗余信息较多，此类重复模式更易被压缩算法识别并高效压缩。针对 LLM API 的流式响应进行压缩，可显著降低出方向网络带宽消耗。

### CPU 消耗权衡

流式响应在实现更高压缩率的同时，会带来相应的 CPU 开销增加。

在非流式场景下，CPU使用率稳定在4.8%至6.2%之间，资源消耗较低。而在流式场景下，CPU使用率上升至20.9%至34.5%，需要消耗更多的计算资源。

由于流式压缩需对连续数据进行实时分块处理，算法复杂度和数据处理量均显著增加，同时更高的压缩率通常伴随更多的计算操作，因此 CPU 使用率上升属于预期现象。

### QATZip 综合性能更好

根据压缩算法的测试结果，QATZip 在综合性能上表现更优。

在流式场景下，ZSTD/QATZip的压缩比为2.8%～2.9%，显著优于 Gzip/Brotli 的7.2%。

在相近压缩比条件下，QATZip 的 CPU 消耗为20.9%，低于 ZSTD 的23.6%。得益于专用硬件加速支持，QATZip 在压缩效率和资源占用方面均具备优势。

## 实施步骤
### 创建支持硬件加速的 AI 网关实例

1. 登录[**AI 网关控制台**](https://apig.console.aliyun.com/#/overview)，在顶部菜单栏选择**地域**。

2. 在左侧导航栏，选择 **AI网关** \> **实例**。

3. 单击**创建实例**，在配置页面完成以下配置：

   * **商品类型** 选择**专享实例**。

   * **网关规格** 选择`aigw.medium.x1`及以上规格。

   * 勾选**分配Gzip硬件压缩资源**。

     **说明**

     Serverless 实例不支持硬件加速。

     仅`aigw.medium.x1`及以上规格实例支持开启硬件加速。
4. 单击**立即购买**。

### 在网关参数中开启压缩

1. 返回**实例**页面，单击目标实例 ID 进入详情页。

2. 在左侧导航栏，选择**参数配置**。

3. 在**网关引擎参数** 配置区，单击**EnableGzipHardwareAccelerate** 参数右侧编辑，开启**参数值**开关。

开启后，需要客户端能够处理Gzip压缩的数据，对于支持的客户端需要在请求头中添加`Accept-Encoding:gzip`。