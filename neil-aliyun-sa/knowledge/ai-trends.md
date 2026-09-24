# AI 趋势 — ai-trends.md

> **定位**：阿里云在 AI 维度的产品演进、行业落地、客户实践。
> **更新方式**：百炼/PAI/通义新动态、ATA AI 实践文章、行业 AI 案例蒸馏后回灌。
> **分级**：区分"已规模化生产" / "早期落地" / "概念阶段"。

**↔️ Cross-references**：
- AI 产品能力 → [aliyun-products.md](aliyun-products.md)(百炼/PAI/通义各产品卡)
- AI 方案 → [cloud-solutions.md](cloud-solutions.md)(S3 AI Agent 方案等)
- AI 竞品 → [competitor-cloud.md](competitor-cloud.md)(模型竞品矩阵/火山引擎对比)
- 客户 AI 实践 → [company-profiles.md](company-profiles.md)(客户 AI 落地案例)

## 关键追踪线

### 1. 百炼（Model Studio）[官方]
- 模型 / 路由 / 工具 / 工作流 / Agent / RAG 能力演进
- 与 PAI / 通义 的边界：**百炼 = MaaS 应用层**（API 直调、Agent 编排、RAG 知识库）；**PAI = 训练与推理基础设施**（DLC 训练、EAS 推理部署、GPU 资源管理）
- 客户接入模式（应用直调 / Agent 编排 / 私有部署）
- 模型矩阵（2026-06更新）：**Qwen3.7-Max**（最新旗舰，视觉+文本）/ Qwen3.7-Plus（多模态智能体）/ Qwen-Plus（日常平衡1M）/ Qwen-Turbo（轻量1M）/ Qwen-VL（视觉）/ Qwen-Audio / Qwen-Coder
- 旗舰模型演进：Qwen-Max → Qwen3-Max-Thinking(1月,1T+参数) → Qwen3.5系列(3-4月) → **Qwen3.7-Max**(5月20日云峰会,当前最强)
- 竞品定价对标：Qwen3.7-Max 12元/百万input vs GPT-4o ~$5/M → 价格相近；Qwen-Plus 0.8元/百万 vs GPT-4o-mini → 极致性价比

**百炼 API 限流表 [官方]**：

| 模型 | RPM(请求/分钟) | TPM(Token/分钟) | 等效 QPS |
| --- | --- | --- | --- |
| qwen-max | 1,200 | 1,000,000 | ~20 |
| qwen-plus | 30,000 | 5,000,000 | ~500 |
| qwen-turbo | 1,200 | 5,000,000 | ~20 |
| deepseek-v4-pro | 15,000 | 1,200,000 | ~250 |

- 限额按**主账号**维度（所有 RAM 子账号/工作空间/APIKey 共享）
- 可临时提升配额（控制台申请，北京/新加坡即时生效，最长30天）
- PTU（专属吞吐单元）：大客户预留容量，绕过共享限流
- Batch API：非实时异步批处理，50%折扣，更高吞吐允许
- **SLA**：可用性 ≥ 99.9%（赔偿阶梯：99.0-99.9%→10%代金券；95-99%→25%；<95%→50%）
- **无延迟 SLA**：无官方 TTFT/P99 延迟承诺

**百炼 vs PAI-EAS 成本交叉点 [推断]**：
- 月调用量低（<300万token/天）→ 百炼 MaaS（Token 计费更划算）
- 月调用量高（>3000万token/天）或 QPS 长期 >100 → PAI-EAS 私有部署（GPU 时长摊薄）
- 数据不出域 → 只能 PAI-EAS 或自建

### 2. PAI 全栈 [官方]
- DSW（开发） / DLC（训练） / EAS（推理） / Designer（低代码）
- GPU 资源池化、PD 分离（Prefill-Decode 分离部署，训练推理混合调度）、推理加速（vLLM / TensorRT / ACC）
- 大规模训练实践：千卡级 DLC 训练集群 + CPFS 共享数据 + OSS Checkpoint
- EAS 核心能力：自动扩缩 / A/B Test / 蓝绿发布 / 模型版本管理 / 流量镜像
- 选型边界：需要全流程 ML 工程能力时用 PAI；只需 API 调模型时用百炼

**PAI-EAS GPU 定价表 [官方]**：

| GPU 型号 | 实例规格 | 显存 | vCPU | 内存 | 按量(CNY/时) | 月估(CNY) |
| --- | --- | --- | --- | --- | --- | --- |
| NVIDIA T4 | gn6i | 16GB | 16 | 62GB | ~14.82 | ~10,670 |
| NVIDIA A10 (GU30) | gn7i / ml.gu7i | 24GB | 16 | 60GB | ~12.71 | ~9,151 |
| NVIDIA V100 | gn6v | 32GB | 8 | 32GB | ~26.46 | ~19,051 |
| NVIDIA A100 | gn7e / ml.gu8xf | 80GB | 16 | 125GB | ~34.74 | ~25,013 |
| NVIDIA H800/H100 | 灵骏智算 | 80GB | - | - | 未公开（需销售，仅包年） | - |

- 资源抵扣包：59 CNY = 200 CNY 额度（约 3 折）
- A10 是最优性价比选择（24GB 够跑 7B/14B 模型，价格最低）
- H800/H100 仅灵骏智算程序提供，包年包月，需销售介入

**GPU 推理 Capacity Planning 参考 [实战+推断]**：

| 模型 | GPU 配置 | 输出吞吐(tokens/s) | 并发支撑 | 场景 |
| --- | --- | --- | --- | --- |
| Qwen2.5-7B | 1×A10 (24GB) | ~30-45 (短上下文) | ~50-80 并发 | 轻量客服/摘要 |
| Qwen2.5-7B | 1×A100 (80GB) | ~40 (短) / ~19 (长) | ~100 并发 | 标准推理 |
| Qwen2.5-14B | 2×A10 (48GB) | ~20-30 | ~30-50 并发 | 复杂对话/Agent |
| Qwen2.5-72B | 4×A100 (320GB) | ~155 总 / ~39/卡 | ~20-40 并发 | 企业级推理 |
| DeepSeek-R1-671B | 8×H800 (FP8) | ~620 总 | ~100 并发 | 超大模型 |

> **Capacity Planning 公式（估算）**：所需 GPU 卡数 ≈ (目标并发 × 平均output长度) / (单卡tokens/s × 可接受延迟秒数)
> 例：2000并发 × 200 token/响应 / (30 tokens/s/卡 × 5s 可接受延迟) = ~2667/150 ≈ **27 张 A10**（跑14B模型）

### 3. 通义系列 [官方+推断]
- **千问 Qwen**：语言模型，开源生态（Qwen2.5 系列 72B/14B/7B/1.5B 全开源）；长文本（128K+）；多模态（VL/Audio）
- **万相**：图像/视频生成（文生图/图生图/视频生成），对标 Midjourney/DALL-E
- **Qoder CN 系列**（原灵码 Lingma，2026.5.20 更名）：从 AI 代码助手升级为 Agentic Coding Platform。产品线含 Qoder CN（IDE 插件/Quest 自主开发）、QoderWork CN（桌面办公助手）、CLI、Cloud Agents。对标 GitHub Copilot/Cursor/Windsurf。全球版 qoder.com / 中国版 qoder.com.cn
- **听悟**：语音识别/会议纪要/音频理解
- 与百炼的关系：通义模型 = 底层能力；百炼 = 调用/编排/管理平台；DashScope = API 网关通道

### 4. AI Infra（推理服务架构）[实战-ATA]

**PD 分离（Prefill-Decode 分离部署）**— 来源：ATA SA动手系列2 (11020600554)
- 核心思想：Prefill = 计算密集(TP8)，Decode = 显存密集(DP8+EP16)，资源配比完全不同
- 实测数据(DeepSeek-R1-671B FP8)：
  - Prefill GPU 利用率 95%+；Decode 受限于 KV Cache 显存
  - 1K 上下文：204 tokens/s 解码，441 并发
  - 64K 上下文：34 tokens/s 单卡，TTFT 2569ms
  - MTP 推测解码：TPOT 58ms→52ms (-10.3%)，接受率 ~68%
- KV Cache 传输：GPUDirect RDMA（200Gbps，微秒延迟，零 CPU 开销）
- Chunked Prefill：64K 序列不 Chunk 会 OOM，Chunk 后延迟仅 +7.8%
- P/D 比例公式：Ratio = (InputLen × PrefillTime/Token) / (OutputLen × DecodeTime/Token)
  - 1P3D（平衡）、2P1D（RAG/长输入）、1P8D（代码生成/长输出）
- 监控关键指标：prefill_queue_length / decode_queue_length / ttft_p99 / tpot_p99 / GPU 利用率
- 客户实践：中国移动智算推理池 PD 分离测试
- 产品组合：PAI + ACS/ACK GPU 集群 + IB 网络(RDMA) + SGLang 推理引擎

**高可用 AI 系统**— 来源：ATA "构建高可用AI系统" (11020604053)
- 核心模式：AI Gateway(Higress) 多模型容灾 → 0.5 秒自动切换（口径说明 2026-09-21：「AI Gateway(Higress)」= 阿里云 **AI 网关**，云原生 API 网关面向 AI 原生应用的实例形态，Envoy/Higress 内核；产品谱系/计费/外部认证 → [aliyun-products.md 云原生API网关/AI网关深度卡](aliyun-products.md#云原生-api-网关apig--ai-网关深度卡)。以下既有结论不变）
- Prompt 热更新：MSE 配置中心管理 Prompt 版本 + 灰度发布，无需重启
- Agent 沙箱：AgentRun 隔离执行，动态加载+权限控制+行为审计
- 弹性实例：ACK + ECI，10 → 200 实例自动扩缩
- 向量库优化：跨地域向量库部署，延迟降低 70%
- 设计原则：HA 架构必须匹配业务重要性，避免过度设计
- 核心公式：生产级 = 高可用模型 × 高可用应用 × 全景可观测

**通用推理架构选型**：
- ACS / ECI / GPU ECS 选型 → 参见 cloud-solutions.md 升级阈值表
- PD 分离适用场景：模型 >100B 参数 + 长上下文 + 高并发 + 多卡集群

### 5. AI Agent 与智能体 [官方+实战]

**百炼 Agent 2.0 架构**— 来源：help.aliyun.com + ATA 多篇
- Zero-code 可视化编排 + Full-code ADK 开发套件 + ADP 生产部署
- MCP 协议（Model Context Protocol）：标准化工具互操作
- Multi-Agent 编排：专家 Agent 协作处理子任务
- Workflow：DAG 编排，条件分支/循环/人工审批/异步等待

**Agent 落地三层次**— 来源：ATA "Java程序员转型AI" (12020603721)
- L1 Prompt User（高可替代性）→ L2 AI 应用集成者（中等）→ L3 AI-Native 架构师（极低可替代性）
- Java 开发者转型优势：OOP→nn.Module 映射、分布式经验、CI/CD/监控工程力
- Spring AI 框架：Java 原生 AI 集成路径（ChatClient Builder / 流式响应）
- RAG 四阶项目训练：API 调用(1-2周) → RAG系统(3-6周) → Multi-Agent(7-10周) → 企业AI应用(11-12周)

**企业级 Agent 案例**：
- 一汽红旗"云妹"：BI 报告 7天→5秒，人员减半 [官方]
- 哈啰出行：运维成本-30%，GMV+5%，纠纷准确率87% [官方]
- 51Talk：响应-30%，成本-20~30%，事件驱动+主动外呼 [官方]
- 网商银行：决策树+FaaS+Agent 诊断系统，故障恢复3分钟内，准确率93.5% [实战-ATA]

### 6. RAG 与向量检索 [官方+实战]

**百炼知识库规格**：
- 标准版：100GB 存储，1 QPS 固定（开发测试）
- 旗舰版：9999GB，1-200 RCU（1 RCU ≈ 50 QPS），0.2 CNY/RCU/hr
- 单次检索最多 20 分片，每分片 ≤ 6000 token

**向量库选型矩阵**：
- **百炼内置知识库**：零代码 RAG，全托管，最快上手
- **Hologres 向量**：OLAP + 向量统一，SQL 友好，AI Function 自动生成 embedding
- **AnalyticDB 向量**：AI + 数据分析融合，内置向量搜索引擎
- **Lindorm 向量**：十亿级向量，宽表+向量一站式，最低成本高写入
- **OpenSearch 向量版**：托管搜索+向量，电商/内容搜索型 RAG

**RAG 工程化**：
- 文档解析 / 切片策略（chunk_size ≤ 6000 token + overlap + 语义切片）
- 召回策略：混合检索 BM25+向量 / Rerank 重排
- 知识库工程化：文档更新频率 / 索引刷新 / 评测指标（Recall@K, MRR）
- 混合检索（关键词+向量+Re-ranking）为生产推荐模式 [实战-ATA]

### 7. AIGC 内容生产 [官方+推断]

**通义万相（Wanx）**—— 来源：help.aliyun.com + 百炼控制台
- 产品定位：图像/视频生成 API，对标 Midjourney/DALL-E/Sora
- 能力矩阵：
  - wan2.7-image-pro：文生图，高质量多风格
  - qwen-image-2.0-pro：图像编辑/参考图生成
  - happyhorse-1.1-t2v：文生视频（Text-to-Video）
  - happyhorse-1.1-i2v：图生视频（首帧驱动）
  - happyhorse-1.1-r2v：参考图生视频（最多 9 张参考图）
  - happyhorse-1.0-video-edit：视频编辑
- 调用方式：通过百炼 API 统一调用，按次/时长计费
- 输出规格：图像最高 2048×2048；视频 720p/1080p，时长 5-30s
- 行业落地：广告素材批量生产、电商产品图、教育课件视觉、娱乐短视频、零售营销素材
- 竞品对标：Midjourney（图像）/ Runway Gen-3（视频）/ 可灵 Kling（快手）/ Pika

**数字人与虚拟人** [推断]:
- CosyVoice（语音克隆/合成）：cosyvoice-v3.5-plus，支持零样本声音克隆
- 数字人技术栈：音频生成 + 图像/视频生成 + 口型同步
- 落地场景：直播带货数字人、客服虚拟形象、知识视频主播
- 成4成熟度：图像生成已规模化生产；视频生成早期落地；数字人尚在探索期

**3D 模型生成** [官方-新]:
- Tripo-H3.1 / Tripo-P1.0：文生 3D / 图生 3D，通过百炼 API 调用
- 场景：游戏资产、电商 3D 展示、建筑可视化

**音乐生成** [官方-新]:
- fun-music-v1：根据提示词/歌词生成音乐
- 场景：短视频 BGM、广告配乐、教育内容

### 8. 模型即服务 (MaaS) 商业模式 [官方+推断]

**百炼平台商业模式**：
- 核心收入：Token 消费费（按量）+ PTU 专属吐量单元（大客户预留）+ 微调/训练费
- 定价策略：“极致性价比”路线——Qwen-Plus 0.8元/百万 vs GPT-4o-mini ~$0.15/M（约 1元）
- 客户分层：
  - 开发者/初创：免费额度 + 按量付费
  - 中型企业：资源包抵扣（打折）
  - 大客户：PTU 专属容量 + 商务制定价
  - 生态合作伙伴：ISV/SI 分成模式

**市场竞争格局** [2026-06 推断]:
- 国内 MaaS 竞争激烈：百炼 vs 火山引擎 Ark vs 智谱 BigModel vs 月之暗面 vs 小米
- 竞争维度：模型能力 × 定价 × 生态工具链 × 开源影响力
- 阿里云差异化：
  - Qwen 开源生态（全球 #1 开源模型下载量）
  - 百炼“一站式”（模型+编排+RAG+微调+部署）
  - 三方模型聚合（DeepSeek/GLM/Kimi/MiniMax/小米 均已接入百炼）
  - 与阿里云 IaaS 深度绑定（PAI GPU + VPC + SLS 监控）

**关键趋势信号** [2026-06 推断]:
- 价格战持续：各厂商密集降价，百炼多次调整定价（Flash 系列最新 1.2元/百万）
- 多模态融合：从纯文本向全模态（omni）演进，语音+视觉+文本统一
- Agent 平台化：从API 调用向 Agent 编排平台转型
- 私有化部署需求增长：金融/政企数据不出域，PAI-EAS 私有部署量上升
- 3D/音乐生成新赛道：Tripo 接入百炼，扩展 AIGC 边界

### 9. Agent 知识工程（Knowledge Engineering for Agents）[ATA实战+官方]

> 来源：飞樰《从 LLM Wiki / Obsidian-Wiki / GBrain 来看 Agent时代知识的“自组织”与“自进化”》(2026-04-27, 9423览) + 晴可《别让你的知识腐烂——Karpathy LLM Wiki 在 KBase 的实践》(2026-04-24, 3861览)

**核心论断：RAG → LLM Wiki 的范式转移** [ATA实战]

| 维度 | RAG（检索模式） | LLM Wiki（编译模式） |
|------|------|------|
| 知识装配时机 | 查询时临时拼凑 | 提前编译好，随时可用 |
| 状态性 | 无状态，每次从零推导 | 有状态，知识持续累积 |
| 文档处理 | 片段化切割，语义割裂 | 全文理解，重构知识网络 |
| 增量更新 | 追加入库，无知识关联 | 增量编译，自动更新交叉引用 |
| 类比 | “每次拆快递箱找东西的仓库” | “分类收纳好贴好标签的柜子” |

**补充关系**：RAG 和 LLM Wiki 互补而非替代——海量文档高并发用 RAG，中等规模深度理解用 LLM Wiki，大规模+概念理解用“RAG底座+Wiki上层”。

**Karpathy LLM Wiki 三层架构** [ATA实战]

```
Schema 层（AGENTS.md/SKILL.md）—— 告诉 Agent 如何维护 wiki
Wiki 层（knowledge/ + index.md）—— Agent 编译产出的结构化知识
Raw 层（raw/）—— 不可变原始资料，唯一事实来源
```

三个核心操作：
- **Ingest**：新源进入 raw/，触发 Agent 读取→提取→整合到 wiki（一篇源可能触及 10-15 个 wiki 页面）
- **Query**：先读 index 定位相关页面，综合回答（好答案可回写 wiki）
- **Lint**：定期健康检查（矛盾/过时/孤立/缺页/交叉引用/数据空白）

**渐进式披露（Progressive Disclosure）** [ATA实战]
- Agent 先读 index.md 定位→按需加载 1-2 个相关页面→不够再扩大范围
- 中等规模（~100 源/百页）无需 embedding-based RAG 基础设施，index.md 即可胜任
- 大规模时可引入 qmd（BM25+向量混合搜索）或 MCP 工具

**Skillify 概念** [ATA实战]
- Skill 不再局限于固定格式的 SKILL.md，而是泛化为一种知识组织形态
- 任何 Markdown 文件通过定义清晰的 Metadata/Schema，描述“什么场景下调用哪些文件”，即可实现知识的渐进式披露
- GBrain (Garry Tan) 称之为 "Skillify"——“像 Skill 一样去组织和加载知识”

**多对一编译（核心价值）** [ATA实战]
- 最有价值的能力不是“1篇文档⥹1篇wiki”，而是**多篇原始文档编译为同一篇主题页**
- 从“情景记忆”到“语义记忆”的映射——5篇关于认证的散落文档编译为1篇《认证模块总览》
- KBase QCon 案例：72篇分享文档 → 14个主题 Wiki 页 + 知识图谱

**KBase 平台工程实践** [ATA实战]
- **远端 KBase Wiki 层**：Wiki文章和用户原始文档共存同一知识库，复用版本管理和权限控制
- **本地 KBase Mind 客户端**：内置 Claude Code + 浏览器插件 + 多格式支持 + 与平台双向同步
- **工具链**：a1 kbase CLI → 全流程编译/查询/健康检查
- 对标 Obsidian 差异化：内置编译流程（raw→wiki→索引）+ Agent 集成 + KBase 双向同步

**对方案设计的启示**：
1. 客户的“知识管理”需求可用 Karpathy 架构设计，而不是只卖 RAG
2. 中等规模知识库（<500文档）可不用向量数据库，index.md+全文读取即可
3. “编译思维”可纳入方案设计——为客户建设“越用越厚”的知识体，而非“每次现查”的检索服务
4. [[百炼]] RAG 功能可与 LLM Wiki 互补：百炼做海量文档级检索，Wiki 做概念级导航

---

## 10. 长上下文 / 思考模型的超长输出延迟治理（GLM-5.2 实战）

> 来源：2026-07-15 百炼业务网关 glm-5.2 高延迟工单排查（Query 回写）+ Google/GitHub 交叉验证。

### 10.1 事实：GLM-5.2 是智谱模型，可通过百炼网关调用 [官方]
- **GLM-5.2 = 智谱 AI（Zhipu / THUDM）的模型，不是通义/阿里自研**；发布约 2026-06-13。内部业务网关（dashscope-admin）可以代理/接入该模型。
- 规格（智谱官方多源交叉）：**上下文 1M（100万）token / 最大输出 128K（131072）token**；属**深度思考（reasoning）模型**（双思考模式）。
- **含义**：一个模型的「默认/最大输出长度」由其**模型 spec（此处是智谱）**决定，与“走哪个网关”无关；不要把它当成百炼/Qwen 的默认。

### 10.2 百炼 thinking 模型的截断参数语义 [官方]
> 百炼 OpenAI 兼容接口（help.aliyun.com/zh/model-studio）对思考模型有关键区分：
- **`max_tokens`：只限制“回答”部分**（不含思维链）——对思考模型**挡不住思考跑飞**。
- **`max_completion_tokens`：限制“思维链 + 回答”的完整输出**——想兜住总时长/总生成量要用它。
- 默认值与最大值通常 = 模型最大输出长度（特定模型可不同，以其 API 文档为准）。
- 思考开关：Zhipu 系 `thinking:{type:"enabled"|"disabled"}`；Qwen 系 `enable_thinking` + `thinking_budget`；**glm-5.2 在百炼的确切字段以其模型 API 文档为准**。

### 10.3 “支持 128K 但过 64K 断崖”——事实核查 [官方+实战]
**方向属实，但是「渐进/非均匀下降」而非普适的 64K 硬悬崖；且要区分输入侧 vs 输出侧。**

| 证据源 | 结论 |
|---|---|
| RULER（NVIDIA, arXiv 2404.06654; github.com/NVIDIA/RULER） | 号称 ≥32K 的模型只有一半能在 32K 维持满意表现；输入越长全线退化 |
| RULER 2026 解读 | 多数前沿模型可靠可用仅标称的 **50–65%** → 128K 模型可靠区≈64–83K |
| Context Rot（Chroma 2025.7） | 18 模型，输入越长性能一致下降且非均匀；NIAH 会掩盖问题 |
| morphllm 2026 | 每个被测模型有效上下文都低于标称；output cap 常先触顶 |
| THUDM/LongBench | 智谱自己也专门做长文本评测 |

- 真正陡降拐点在「原生训练长度 / RoPE-YaRN 外推边界」附近，**模型相关**。
- **输出侧变差**另有两因：（a）KV cache 随序列增长→解码越往后越慢；（b）超长思维链发散/不收敛→撞上限截断。

### 10.4 实战案例：glm-5.2 over-thinking 导致 ~20min 延迟 [实战]
- 10 条高延迟请求均 http_code=200、SSE、prod；总耗时 ~20–25 分钟（cost 118万–150万 ms）。
- **8/10 条 output_tokens=65537（=64K+1）且 reasoning_tokens=65536、回答仅 1 token** → 思考打满 64K 输出预算被截断，**没产出答案**（finish_reason≈length）。
- TTFT（first_output_duration）仅 0.5–28s，占总耗时 <3%；解码吞吐 ~44–56 tok/s。
- **根因 = decode-bound + 思考失控**，非排队/网络/首包。注意 64K 仅模型上限 128K 的一半，说明是 max_tokens/网关默认而非模型上限。
- 注：**业务网关“用户请求查询”报表不记录请求入参**（无 max_tokens/prompt/temperature 字段），只有 usage 用量。要看入参需客户端日志/请求级 trace。

### 10.5 客户端延迟治理 Playbook（可直接给客户）[实战]
1. **用对截断参数**：`max_completion_tokens` 压到 8K–16K（`max_tokens` 只限回答、挡不住思考）。
2. **控制/关闭深度思考**：简单任务关思考或降 thinking_budget（治本）。
3. **压输入**：RAG 只喂相关片段，输入尽量 <32K（留在有效区）。
4. **Prompt 约束**：“简要思考/答案≤N 字/停止条件/结构化输出”；Agent 限步数+收敛判据。
5. **长输出拆分**：大纲→分段 map-reduce。
6. **流式+超时熔断**：客户端 60–120s 超时 + “N 秒无有效回答即中止”看门狗。
7. **处理 finish_reason=length**；**快慢分流**（简单任务路非思考/更快模型）；**客户端自记入参**。
8. **上下文缓存降 TTFT（输入侧杠杆）**：固定长前缀（system prompt/长文档/代码仓库/工具定义）用 [[百炼]] 显式缓存（`cache_control:{type:ephemeral}`，命中按输入价 10% 计费、5min 有效）或隐式缓存（自动/命中 20%）复用 prefill，砍首包延迟。**注意仅解输入侧**：本案例瓶颈在 decode+思考打满 64K 被截断（输出侧），缓存救不了，仍需第 1-2 条兜住。

**对方案设计的启示**：
1. 向客户推荐思考模型时，必须同步给出**输出上限 + 思考预算 + 超时熔断**的工程防护，否则单请求可能 20 分钟。
2. 长上下文卖点要说清「标称 vs 有效」：官方 128K/1M 不等于全程可靠，建议客户按有效区（≈一半）设计。
3. [[百炼]] 接入三方模型（如 GLM）时，参数语义走百炼兼容层，但**模型能力边界（上下文/输出/思考）看模型本尊（智谱）**。

---

## 11. Coding Agent 工程化：Loop Engineering / Graph Engineering [ATA实战+grow实战+官方]

> 来源：2026-08-08 六路并行调研（ATA 56 篇全文 / 29 篇一手英文源 / 33 个 GitHub 项目实测 / Graph 专项 24 篇 / Multica 源码测绘 / grow 5 门课 6.6 万字听悟文稿）。
> 完整报告：`~/Desktop/neilcodebase/loop_engineering_practice/research/`（00-master-report.md + 01-spec）

### 11.1 术语定谱：外部无共识，内部有两套定义 [官方+实战]

**外部（写方案不能当权威概念引用）**：
- Anthropic 只在 verification-loops 博文**结尾随口用过一次** "loop engineering"，全文从未定义；官方用词是 `verification loop` / `the agentic loop`
- Thoughtworks Radar Vol.34 **官方警告语义扩散**：spec-driven development 与 harness engineering *"sometimes used inconsistently or overlap in meaning"*
- **真正被正式定义的相邻词**：`harness engineering`（Böckeler：`Agent = Model + Harness`，用户可控部分叫 outer harness）、`context engineering`（Anthropic 专文，底层概念 `context rot` + `attention budget`）、`agentic loop`（官方三段式 **gathering context → taking action → verifying results**）

**内部（阿里）有两套并行定义，不冲突**：

| 框架 | 出处 | 内容 |
|---|---|---|
| **六大核心框架** | ATA 飞樰《Loop Engineering 概念解析》17337 览 | Automations / Worktrees / Skills / Connectors / Sub Agents / State；原则 **"不能既当运动员又当裁判员"** |
| **Graph Engineering** | ATA 飞樰《从 Loop 到 Graph Engineering》6026 览 | **= "Loops watching loops"**，多个不同速度的循环互相监督。与 Workflow 明确划界（Workflow 是预定义单向确定性序列） |
| **五要素最小闭环** | grow 釋心《从 Harness 团队到 Loop 团队》 | **Go / Drive / Harness / Tracker / Gate**（听悟文稿把 Harness 转写成 Honors/honest，已核实修正）。金句：**"先写怎么停，再写怎么跑"** |
| **Harness 五层** | grow 颜律（4332 浏览） | Agent MD / Skill / Ruler / Command / Agent；哲学"人主导、AI 执行；文档先行" |
| **KST 三层** | grow 覇天（1688 数据研发） | Knowledge / Spec / Task；AI 逆向解析历史代码可自动清洗 **80% 通用知识** |

**Graph Engineering 三大护栏（最该抄的设计）**：
- **Anchors** — 由外部系统验证的铁事实，**不由 Agent 自己产生**（CI 结果、线上 error 计数、官方评测分）
- **Frozen Nodes** — **测试集不可被优化器篡改**
- **External Judgment** — 人定价值方向

对应单 Loop 四大结构性缺陷：Goodhart's Law / Blindness Upward / Conflict / Measurement Decay。

### 11.2 量化效果：门禁 > 图谱（优先级判据）[实战]

| 措施 | 效果 | 性质 | 来源 |
|---|---|---|---|
| 加门禁/约束 | **编译通过率 35% → 91%**；环境适配失败率 15%→3%；误判新增率 20%→5% | **可行性前提** | ATA 051 高德测试 AgentLoop（prompt 1600+ 行中 **60% 以上是约束而非指令**） |
| review 子代理 | 成本仅编码的 **10-20%**，总成本降 60-70% | 可行性前提 | ATA 005 Qoder 官方 |
| 注入代码图谱 | 时间 −44%、Token −56%、工具调用 −71% | **效率优化** | ATA 050 蚂蚁 BizFlow（同链路同 prompt 唯一变量对照） |
| 完整生产闭环 | 一周 ERROR **1210→47（↓96%）**；修复 48min→15min；人工介入 每次→**0**；多 Agent 冲突率 30%→<5% | — | ATA 003（诚实标注：**工具链建设占总工作量 30%**） |
| 经验自进化 | SWE-bench Verified **67.2%→74.4%（+7.2pp）**；工具调用 −25.1%；有害事件 −27.8% | — | ATA 052（轨迹清洗到原始 Trace 的 4-6%） |

**结论**：图谱优化"跑得快不快"，门禁决定"能不能自主跑起来"，**量级差一档**。

### 11.3 自主度分级：内部矩阵 vs 外部权限档 [实战+官方]

| 体系 | 出处 | 用途 |
|---|---|---|
| **A1-A5 × T1-T5 正交矩阵** | ATA 039 AgentLoop | **成熟度门槛**。人注意力档 5%/15%/30%/50%/80%；晋级阈值 **A2 覆盖率≥60% / A3 历史成功率≥90% / A4 ≥99%+自动回滚** |
| **`permission_mode` 六档** | Claude Agent SDK [官方] | **权限档位**。`default`/`acceptEdits`/`plan`/`dontAsk`/`auto`(classifier 逐动作)/`bypassPermissions`(**仅隔离环境、不能 root**) |

`auto` 档官方数据：classifier *"caught more dangerous actions than developers did"*，且 ***"Claude works 9x longer between interruptions"***。

三个具名客户的共同结构 = **默认高自治 + 一张很短的硬 deny 清单 + 按操作域降档**：Nuro 硬 deny recursive delete；Gusto 碰 Terraform/AWS 降 `acceptEdits`；Garner Health 禁"与他人通信"类动作。

### 11.4 门禁的成本平衡（唯一一手答案）[官方]

Thoughtworks 已把 backpressure 升为 **Trial 级 blip**，规则原文：门禁 *"should run **during the coding session** and report clean results **before a commit is made**, rather than relying on post-commit checks."*

**Stripe 的两级设计（可直接抄）**：

| 级别 | 轮数 | 实现 |
|---|---|---|
| 本地确定性 lint | **无限 loop** | pre-push hook + 后台 daemon 预计算缓存，**1 秒内出结果** |
| 完整 CI | **硬限 1 轮 + 1 次修复** | 之后转人工。理由：*"diminishing marginal returns..."* |

规模验证：**每周 1300+ 个纯 agent 产出的 PR 合并**。

**两类闸门必须分开**（[推断]，但混用是常见设计错误）：质量门禁 **fail-closed**，资源门禁 **fail-open-to-human**（超预算是升级不是失败）。

### 11.5 失败模式与 reward hacking [官方]

Anthropic 官方三分类：**agentic laziness**（50 项审查做 35 项就宣布完工）/ **self-preferential bias** / **goal drift**（compaction 后目标漂移）。

Ralph 作者最直白：*"the reward function is compiling code"*。四条对策：做者/判者分离、判者单独调 skeptical、能确定性就别用推断、**要证据不要断言**（*"show evidence rather than asserting success"*）。反向警告同为官方：过度 review 导致 over-engineering，reviewer prompt 要限定"只报影响正确性的问题"。

> **四源同述（本轮置信度最高的设计原则）**：飞樰"不能既当运动员又当裁判员" = 釋心"maker/checker 拆分" = Anthropic 做者判者分离 = 釋心金马奖"自家回归 + 官方评测平台**双 tracker 交叉验证**"。

### 11.6 状态持久化：官方四件套 + event sourcing [官方+实战]

Anthropic 对问题的定义：*"engineers working in shifts, where each new engineer arrives with **no memory**"*，并**明确说 compaction 不够**。官方解法 = **initializer agent + coding agent 两套 prompt**，initializer 首轮产出 `init.sh` + `claude-progress.txt` + **一个初始 git commit** + **200+ 条初始全标 failing 的 feature list**。

- context 管理三件套（官方原词）：`compaction` / `structured note-taking` / `multi-agent architectures`
- 最实操的官方警告：**compaction 会吃掉早期规则** → *"Persistent rules belong in CLAUDE.md ... **re-injected on every request**"*
- 官方提供 `session_store` adapter，**支持无状态容器跨主机 resume**

**三方独立收敛到 event sourcing 而非 state snapshot**：Temporal *"records a full Event History... you never have to think about checkpoints"* + ATA 044 AgentRun "Session 是活在上下文窗口之外的追加式事件日志"（TTFT p50 −60% / p95 −90%）+ ATA 022 如意"无状态容器 + Session 持久化事件轨迹"。

**内部更主动的操作手法**（grow 颜律）：每轮问 agent "列出本轮主题 + 健康度"（红/橙/黄/绿），**对话超 10~15 轮或主题超 3~4 个就新开会话并让 agent 整理上下文接过去**。

### 11.7 六方一致：不要默认上图编排框架 [官方]

| 来源 | 立场 |
|---|---|
| **Anthropic** | 点名警告 LangGraph 类抽象层"掩盖底层 prompt"；编码场景推荐 **orchestrator-workers**，理由是子任务数量**无法预先确定**（静态 DAG 做不到） |
| **Cognition** | *"in 2025... only results in fragile systems"*，点名 swarm 与 autogen |
| **Microsoft AG2** | 官方顶部 *"Warning: GraphFlow is an experimental feature"* |
| **Google ADK** | 图只是四选一；`/agents/multi-agents/` 已 **301 重定向**到 `/workflows/` |
| **OpenAI Agents SDK** | **里面没有图**；handoff = 工具 `transfer_to_<agent>`；默认共享完整历史 |
| **Temporal** | *"it's just regular code... no new language or DSL... no abstractions to get in your way"* |

内部印证：ATA 024《蚁窝》（10293 览）原话 *"随着模型能力快速增强，我逐渐发现身边的 AI 实践**收束到了 Claude Code + Skills + CLI 这种形式**"*。

LangGraph 的真实运维成本（四个官方 Troubleshooting）：`thread_id` 须 <255 字符 / `InMemorySaver` 重启全丢 / **"Checkpoints growing unboundedly"（官方建议加 cron 删）** / **subgraph 独立 checkpoint namespace 导致父图看不到子图状态**。→ **多一张要自己清的表 + 一个调试陷阱，换零新增能力。**

### 11.8 代码图谱：只有轻量档成立 [论文+官方]

**四条独立证据打掉重量档**：

| 证据 | 内容 |
|---|---|
| **cAST 打平 RepoGraph** | cAST **不建图不建库**只改 chunking 用 AST 边界，SWE-bench **+2.67**；RepoGraph 建整套行级图 **+2.34** |
| **RepoGraph 自己的 ablation** | **1-hop flatten 29.67（最佳）> 基线 27.33 > 2-hop flatten 26.00（低于基线，有害）**；1-hop+LLM摘要 28.33（比 flatten 差） |
| **LazyGraphRAG 1000 倍成本差** | 索引期零 LLM 调用（换 NLP 名词短语共现）；索引成本 = full GraphRAG 的 **0.1%**；全局查询成本降至 **1/700**；用 **4%** 查询成本反超 |
| **CodexGraph 三重代价** | GPT-4o 下 SWE-bench Lite **22.96 = AutoCodeRover 22.96（打平）**；Qwen2 下 **1.95 vs BM25 9.34（大输）**；**43 个 Sympy 样本 OOM** |

**⚠️ 必须带限定的数字**：流传的 "RepoGraph 提升 32.8%" 是**相对提升平均值被极弱 RAG 基线（2.67→5.33）拉高**，四组**绝对提升全部落在 +2.00~+2.66 点**。

**两条时点性事实（2026-08）**：
- **Kùzu 已被官方归档**（README 顶部 *"We are archiving the KuzuDB project here"*）→ 2024-2025 年所有"推荐 Kùzu 替代 Neo4j"的选型文章已过期
- **工业级系统无一用通用图数据库做主存储**：Meta Glean = RocksDB；CodeQL = **关系表**（"a table for every language construct"）；Joern 自研 OverflowDB；Aider = SQLite + NetworkX 内存图。用 Neo4j/Memgraph 的全是研究原型

**"agentic grep 打败 embedding" 的精确边界**：Anthropic 官方措辞是 **"get to the same accuracy level"** + "much cleaner **deployment** story"，放弃理由绝大多数是运维/安全/部署（需持续 re-index、多分支 stale、代码要送第三方 embedding 服务），**且官方推荐工具清单里含 `ast-grep`**。→ **被否定的是「稠密向量索引这个基础设施」，不是「结构感知搜索」。** 反证：Cursor 官方称语义检索 *"improved response accuracy by 12.5% on average"*，time-to-first-query 中位 **7.87s→525ms**、P99 **4.03h→21s**。**差异根因是产品形态（本地 CLI vs 云端集中索引），不是技术优劣。**

**最反直觉的一条（CodePlan，唯一控制了 context 变量的干净对照）**：CodePlan 通过 validity checks **5/6 仓库 vs baseline 0/6**，官方明说 baseline 拥有 *"the same type of contextual information as CodePlan"* → **唯一变量是有没有 planning**。对照 RepoGraph（图当检索索引）只 +2.34：

> **图的收益不来自"把图给 LLM 看"，而来自"用图算出待办清单"。图的输出应该是任务队列，不是 context blob。→ 接 `plan` 阶段做影响面展开器，不接 `implement` 阶段做检索后端。**
> 限定：CodePlan 仅 6 仓库 2 语言、任务是机械性可判定的批量改造、**无 SWE-bench 数字**。

**若要做，技术栈**：tree-sitter tags + `ast-grep` → **file-incremental 内容哈希增量**（GitHub Stack Graphs：*"purely syntactic analysis... without any per-package configuration, and without having to invoke an arbitrary, untrusted, package-specific build process"*，且支持 *"within and across repositories"* 不合并大图）→ **已有 PostgreSQL 加两张表** → **只做 1-hop** → 喂 LLM 是**代码骨架文本**。ATA 050 实测渐进式披露必要性：原始 graph.json 1703 节点 ≈ **74K token**，压缩到 **10-14K** 才可用；Tree-sitter 建图 50 万行**冷启动 <10s、增量 <2s**。

### 11.9 常驻服务化：三种形态 + 一条合规红线 [实战]

| 形态 | 代表 | 算力位置 | 特征 |
|---|---|---|---|
| 本地 Daemon + 云端编排 | **Multica**（ATA 040，929 览） | 用户本地 | LLM 账单归用户、**代码不出本地**；定位"**调度器而非大脑**"（全仓库无 LLM SDK，prompt 模板 <200 行） |
| 办公网单机托管 | 蚁窝（ATA 024，一台 Mac Studio） | 办公网 | 受网络边界约束 |
| 云端 Managed Agent | 如意（022）/ AgentRun（044）/ Qoder Cloud Agents | 云端 MicroVM | 强隔离可弹性 |

**🔴 合规红线（ATA 025《OpenClaw 集群已在内网上线》13033 览）**：
> `2026/03/06` 接到安全团队沟通：**生产网、测试网禁止部署此 Agent。这类 Agent 只能在沙箱环境内部署（强隔离）。** `2026/04/09` 已按合规要求全部迁移到沙箱环境。

**Stripe 讲透了沙箱与自治的因果**：因为 devbox 是隔离 QA 环境（**无真实用户数据、无生产服务、无任意网络出口**），所以 *"the agent doesn't need confirmation prompts"*。→ **沙箱够硬才有资格谈高自治常驻。**

**凭据正解 = egress proxy**（ATA 045，589 览，点名 Multica *"执行层还是你本地的 runtime，从权限的视角其实就还是你"*）：拆开**触发人 / Agent 身份 / 执行身份**三件事；agent 在容器里发**不带 token** 的请求，出网时 proxy 按身份注入短期 token → **真实凭证不进沙箱**。反模式：token 塞进容器 env（"Agent 一执行 `env`、读配置、打印日志就可能泄漏"）。现成组件：**`alibaba/OpenSandbox`**（Aone Sandbox 开源版，12399★）的 Credential Vault，是**唯一可 `go get` 的沙箱 Go SDK**。

### 11.10 多仓库服务化：Devin 的官方架构最贴合 [官方]

**Devin**：*"this snapshot should include **all the repositories you want Devin to work on** ... You can think of this as **setting up Devin's laptop on the first day of work**."* 机制 = 组织级 VM snapshot + **per-repo 的 Secrets/Lint/Test/Run 命令** + direnv/nvm per-repo 环境隔离 + **Machine Version History 快照回滚**。

**Cursor Cloud Agents** 支持 multi-repo：`.cursor/environment.json`（环境即代码）+ Builds 预备 + restrict outbound domains + OIDC。

**反面参照**：GitHub Copilot cloud agent 是**单仓单分支单 PR + 59 分钟硬上限** —— 最有条件做多仓的厂商选了最保守模型，说明**跨仓 PR 的原子性/权限/review 归属复杂度被刻意规避**。

**Stripe 三层样板**：预热多仓 devbox 池（**10 秒 SLO**）+ blueprint 状态机（确定性节点混 agent 节点）+ 中心 MCP 层 Toolshed（近 **500 tools** 但**按任务只下发子集**）。

**Sourcegraph 的 "80% problem"（多仓场景最强论证）**：agent 可靠完成可见的 80%，漏掉的 20% **每次都是同几类** —— auth middleware / 另一层 API DTO / audit log / **sibling repo 里的集成测试** / 前端 guard / migration script。

### 11.11 可靠性数据与成本量级 [论文+实战]

**METR（唯一权威曲线）**：人类耗时 **<4 分钟**的任务成功率接近 100%；**>4 小时**的任务 **<10%**。TH1.1 修订后 ≥2024 doubling time **108.9→88.6 天**；Opus 4.5 的 50% time horizon = **320 分钟 [170, 729]**。
> ⚠️ 必须一起引用：*"These confidence intervals are still very wide"* —— **320 分钟 ≠ 能可靠工作 5 小时**，它只是 50% 成功率的插值点。

**成本量级**：单 Agent 任务 ≈ 普通 chat 的 **4 倍** token；多 Agent 系统 ≈ **15 倍**（ATA 046）。反面案例：CSS 小改跑 2 天烧 **~$100**，根因是模型 CRLF 换行导致改动根本没写盘（grow 颜律）。

**行业分歧（真实未收敛，须诚实呈现）**：Cognition 主张 single-threaded linear agent，Anthropic 多 agent 研究系统却比单 agent 高 **90.2%**。→ [推断] 领域不同不是真矛盾：code editing 的并行动作产生**冲突的隐含决策**，read-only research 的广度**可无冲突并行**。**规则应定为：并行度由「是否写共享状态」决定，而非由任务大小决定。**

### 11.12 六条踩坑（全部有出处）[实战]

1. **ATA 001**："用 Loop 的时候，你的需求和验证标准必须比原来写得**更加明确**"；不要每天现开 Loop（费 token + 结果漂移不可复现）
2. **ATA 033**（7587 览）原文直书：**"不要在一个会话里跑完全部流程"**
3. **ATA 043**（1792 览）：**"agent 的失败模式是 infra 设计缺陷的放大器"** —— "Agent 每次都会忠实地撞上去，频率极高"
4. **ATA 047**："每次命令失败都销毁重建…**试错无法收敛**"；要求**原样透传退出码**、区分"依赖仍在初始化"与"初始化已失败"
5. **grow 颜律**：朋友团队完全 vibe coding，**一个月后代码重复率 90%**
6. **claude-code-action 源码注释**：`exempt_head_branches: []` 因为 *"branch names are attacker-controlled, so this is not a safe place to encode trust"*；且**配置只从默认分支读** → 自建时把 verify 命令放仓库内配置，**必须只从默认分支读**，否则提个 PR 就能提权

### 11.13 对方案设计的启示

1. **给客户设计 coding agent 平台时，先卖门禁不卖图谱** —— 35%→91% 的编译通过率是可行性前提，图谱的 −44% 时间是效率优化，量级差一档。
2. **"常驻 agent" 要区分云端与常驻两件事** —— ATA 045 自我怀疑成立：Claude Code 公开数据**平均任务时长 45s**，"真正需要的是调度能力和权限边界，不一定需要一个云端 Agent 长时间占着机器自己思考"。价值在长尾（定时巡检、错误自愈、跨仓批量改造），不在平均值。
3. **上云端 Agent 方案必带沙箱与凭据设计** —— ATA 025 合规红线 + ATA 045 egress proxy，这两条是内网/生产场景的准入条件，不是加分项。
4. **不要给客户推荐图编排框架做 coding agent 编排** —— 六方一致反对，且有官方运维成本清单可举证。

---

## 待蒸馏种子

- [x] ATA：高可用 AI 系统 (11020604053) — 已蒸馏到上方第4节
- [x] ATA：SA 动手系列 PD 分离部署 (11020600554) — 已蒸馏到上方第4节
- [x] ATA：Java 程序员转型 AI (12020603721) — 已蒸馏到上方第5节
- [x] ATA：网商银行智能化定位 (12020553615) — 已蒸馏到上方第5节
- [x] ATA：从 LLM Wiki/Obsidian-Wiki/GBrain 看 Agent知识自进化 (11020627647) — 已蒸馏到上方第9节
- [x] ATA：Karpathy LLM Wiki 在 KBase 的实践 (11020627230) — 已蒸馏到上方第9节
- [ ] ATA：Aegis AI 数字分身 — 未找到原文，待确认标题
- [ ] ATA：AIGC 证券投教视频 — 视频 AIGC
- [ ] help.aliyun.com 百炼最新文档 — 部分已融入第5/6节
- [ ] help.aliyun.com PAI EAS 推理服务最佳实践
