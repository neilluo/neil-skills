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
- **突发/增速限流**（区别于上表稳态限额）：除稳态 RPM/TPM 限额外，另有用户维度**静态增速限流**（突发时 token 增速 ≤ max(前 5min token×30%, 增速配置值)）+ 客户维度重试随机指数退避（1-5 次最长 6/15/36/63/114s）——完整机制见 [aliyun-products.md](aliyun-products.md) 百炼卡「增速限流 / 突发限流机制」
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
- **Meoo（秒悟）**（2026.4 起持续迭代，主体：通义云启杭州）：**云端 AI Vibe Coding 全栈应用工厂**，一句话生成前端+后端+DB+部署上线的完整应用（网页/H5/微信小程序），内置 Supabase 化 BaaS + 多模型选择器（Qwen3.7-Max/Plus、Qwen3.6-Plus、Kimi2.5、GLM-5/5.1/5.2、MiniMax、DeepSeek-v3.2、Qwen3-VL、通义万相/Wan2.7）。产品形态：网页端 + Meoo CLI（让 Claude Code/Codex/Cursor/Qoder 等外部 Agent 接管云端资源）+ 微信小程序代提审。四种 Agent 模式（Agent/Swarms 蜂群/Plan/Design）+ 技能市场 + 团队版席位制积分共享（¥698/月起 5 席位）。对标海外 Vercel v0/Bolt.new/Lovable/Replit Agent，国内 Trae/秒哒。**与 Qoder 的分工：Qoder 面向开发者/IDE，Meoo 面向业务/无代码/端到端全栈**。仅中国大陆部署，服务器无海外节点。官网 meoo.com / 文档 docs.meoo.com
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

### 10. 企业级 AI 战略与落地路径（2026 共识）[ATA实战+第三方报告]

> 来源：2026-08-10 ATA 60 关键词检索（501 篇去重）+ 云知道 GTM/市场洞察全量元数据（5000 篇）。核心 6 篇已逐句回源核查。

**10.1 架构选型的三条硬阈值**（面客选型时可直接引用）

- 单 Agent 任务成功率达 **45%** 以上后，单纯增加 Agent 数量收益边际递减甚至为负（Google DeepMind 论文，ATA 11020589335 转引）
- 纯独立多 Agent 架构错误放大 **17.2 倍**，引入中心化机制后可控在 **4.4 倍**（同上）
- 多 Agent 对复杂任务性能高出单 Agent **90.2%**，但 Token 消耗是 **10–15 倍**（Anthropic 内部研究，ATA 11020602957 转引；该解读带"仅为个人理解"免责）
- 单 Agent 适用三条件（需同时成立）：场景复杂度低、检索召回质量有保障、核心指令 + 背景知识 ≤ **2 万 Token**
- 选型顺序 P0→P3：单 Agent → Agent Skills → Multi-Agent → Agent Teams

**10.2 收敛趋势：复杂编排回退成「单编排器 + Skills」** [实战]

云小二 Aivis 把 Planner-Reasoner-Executor 三层多 Agent 收敛为单 Orchestrator + Skills（ATA 11020582433，五条理由：路由张冠李戴 / 多轮连贯性差 / 机械性回复 / 重复模块执行 / 通信耗时累积）。高德智能问数是 9 个并列 Skill → 统一 Skill + 四层确定性路由（ATA 11020633211），**注意它 V1 本就不是 Multi-Agent，不能与前者混为一谈**。两者唯一真正共振的结论：**路由准确率是整个系统的天花板**。

**10.3 上下文与工具的成本杠杆** [实战，ATA 11020600930]

5 个 MCP Server ≈ 55,000 tokens 工具定义开销（200K 上下文里先吃掉近三成）；Prompt Caching 稳定前缀读取折扣可达 90%；Cursor 改按需查询后总 Token 降 46.9%；每工具附 1–5 个调用示例可使准确率 72%→90%。
**边界条件（原文自划，勿漏）**：「工程杠杆 > 模型杠杆」在代码编写这类高可验证任务上最成立；开放式研究、多轮协商等弱验证任务里模型上限仍更关键 —— 制造业的工艺决策/异常研判属弱验证，报方案时必须说明。

**10.4 评测是最容易被跳过、最不该跳过的一环** [实战]

每步 90% 准确率，第十步只剩 0.9^10（ATA 11020698840）。开发期用 Pass@k、上线回归用 Pass^k，两把尺子不能混用。启动评测只需 **20–50 个真实失败案例**；在线按 10%–20% 采样 Trace，负反馈 100% 入队，模型/Prompt 变更后头 48 小时全量审查。行业现状：传统 ML 指标仅占 16.9%，近四分之一团队尚未开始评测。
**工程纪律：先修评测，再改 Agent** —— 评测环境资源不足会把基础设施错误记成模型失败。

**10.5 度量体系（可直接给客户当模板）** [实战，ATA 11020644822 三层模型]

- L1 AI 效能层（领先/工具侧）：AI 代码行占比、AI 有效交互频次、Agent loop 效率
- L2 工程质量层（约束/质量侧）：AI 千行代码缺陷率、AI 代码生存率（N 天内未被回滚重写）
- L3 价值交付层（结果/业务侧）：需求端到端交付周期、交付频率、变更失败率
- 目标基线设定法：集团月均 17 万+ 需求、传统中位数 30+ 天 → 10 倍提效 ≈ < 3 天

**红线：不要考核 AI 生码率或任何单一指标。** 阿里云 CIO 线（ATA 11020606541）与支付宝（ATA 12020627239）分别独立点名，后者直接引用霍桑效应。

**10.6 关键反直觉结论：编码提效 ≠ 交付提效** [三源互证]

纯编码 10 倍 vs 端到端交付仅 2–3 倍（ATA 11020628090）；集团初步度量显示有 AI 参与的需求交付周期仍接近 30 天、测试阶段 AI 参与反而更耗时（ATA 11020644822）；某团队真实整体提升约 10%（ATA 11020606541）。**面客承诺时禁止把工具侧数字等同业务侧收益。**

**10.7 组织设计的两个可复用模板** [实战]

- 岗位合并（阿里云 CIO 线 ATA 11020606541）：PDFE = 产品经理 + 交互设计 + 前端；ABE = 架构 + 后端 + Agent 开发；取消独立运维/测试岗。成效：前端人均有效代码量约 3 倍、后端约 2 倍，千行缺陷率前端 -30%、后端 -55%
- 双层三柱（ATA 11020628090）：Harness 层（AI 主导，越结构化越好）+ Hive Mind 层（人主导，越松散越好）；三柱 = Agent 平台组 + 3–5 人垂直领域组 + 风险监督组（定位免疫系统非官僚刹车）。**最被低估的红利**：以「任务+上下文+权限+工具」为最小单元的执行图，可把组织重组成本从 6–12 个月压到周级
- **新瓶颈不是模型**：内部大规模调研中提及最多的期待是"系统打通与数据整合"（167 条原声，断崖式第一），员工在做"人肉中间件"

**10.8 面客避坑清单（8 条，均有出处）**

① 用向量检索做业务口径路由会翻车（高德：收入/供给/DAU/补贴在不同域 embedding 几乎一样但口径完全不同）② 大而全提示词很容易让模型跳步遗漏（云小二）③ 先上多 Agent 再想收益（Anthropic 解读）④ 没评测就改 Agent（11020600930）⑤ 知识库把每个函数都写一遍，低价值文档反噬注意力（11020705611）⑥ 单一指标考核必被灌水 ⑦ 引入 Agent 后时延可能涨 10 倍不做治理直接毁体验（淘小蜜 11020591712）⑧ 内部 MCP 市场 348 个 Server 中 89.7% 使用量低于 10k（11020603381，2026-03-25 快照）

**10.9 云知道市场洞察报告区 = 面客 PPT 的第三方背书弹药库**

`https://yunzhidao.alibaba-inc.com/doc/detail/{id}`，2026 年高价值：亿欧-中国工业大模型发展洞察 218410、赛迪智库-工业智能体 216118、IDC-企业级 AGI 商业价值评估与选型白皮书（提出「Token 效能」）219467、券商-AI ROI 分析 223650、信通院-智能原生研究 218206、腾讯研究院-AI 时代组织变革 220921、艾瑞-企业级 AI Agent 发展洞察 226831、亚信-智能体 Token 计费与运营白皮书 223905、沙利文-企业级大模型调用全景 216329（2025H2 中国企业级日均 37 万亿 Tokens，千问 32.1% 第一）、Omdia 中国 AI 云市场份额 221476（2025 全年 567 亿元，阿里云 38.1% 超 2-4 名总和）。
**检索技巧**：该区无关键词过滤接口，`DocumentLibraryService.queryDocuments` 只能全量拉后本地筛（试过 keyword/searchKey/name/title/docName 五种字段名均被忽略）；全量 5000 篇仅覆盖近 4 个月；站点全 SSO 登录墙，匿名 curl 302。

---

### 11. 商业化 Agent 工作台形态参考：Accio Work（阿里国际站 / AIDC）[官方][2026-08-10]

> **为什么进这个知识库**：Accio Work **不是阿里云产品**（属阿里国际数字商业集团，面向外贸/跨境商家），但它是阿里体系内少有的**完整商业化 Agent 工作台**——把 Credits 计价、企业级治理、Agent/Skill/Plugin 资产化、双币种结算全部跑通并公开文档化。SA 做「企业 Agent 平台」方案设计、报价结构与治理清单时，这是**可直接对标抄作业的参照系**。
> 来源：公开语雀 `acciowork.yuque.com/rfmg8t/ieb85b` 全 28 篇，raw 归档于 [../raw/aliyun-docs/accio/](../raw/aliyun-docs/accio/)（含 SHA256SUMS）。

**① 定位与形态**：先厘清**产品家族**（2026-08-10 官网实抓校正）——**Accio（`www.accio.com`）= 买家侧 AI 采购引擎**（AI sourcing engine，能力为 Find products / Find suppliers / Hot-selling analysis / New product design / AI-assisted inquiries / Business research；官网宣称 **200 万+ 企业用户、150 万+ 认证供应商、10 亿+ 认证商品、25 年 B2B 电商积累、7,600+ 商品类目**）；**Accio Work = 卖家/中小企业主侧的 Agent 工作台**（本节主体）。两者**账号与积分互通**（网页版与客户端积分同一套），但**不是同一个产品**，对客介绍时勿混为一谈。
Accio Work 面向全球中小企业主/创业者，定位「生意大脑」。Agent 有独立"大脑"（`agent-core`），**能操作本机电脑与浏览器**，非纯对话机器人。形态 = 桌面客户端（macOS 11+ / Windows 10+ 64 位）+ 网页版 + 移动 APP + Chrome 插件 `accio browser relay`。登录仅支持邮箱 / 国际站账号。安全叙事为**沙箱 + 支付类操作强制显式授权**。⚠️ 网页端与桌面端**数据未完全同步**，本地训练数据不跨设备同步。

**② 架构四件套（Agent / Skill / Plugin / 定时任务）**——这套抽象值得直接复用：

| 组件 | 角色 | 关键机制 |
| --- | --- | --- |
| **Agent** | 执行者（数字员工） | 每个 Agent **独立记忆空间、互相隔离**；删聊天≠删长期记忆；官方**建议按职责拆多个 Agent**（选品/发品/采购各一），因为**积分只与模型调用次数和任务复杂度相关，与 Agent 数量无关** |
| **Skill** | 结构化文档形式的领域知识 | 🔴 **双开关才生效**：Skills 页 `Enabled` **且** Agent 配置里 `Selected`；装太多不相关技能会导致**调用不准**；Agent 可把重复任务**自动固化为新技能** |
| **Plugin** | 工具包 = 连接器 + 技能 + 指令 | 一键安装 + 账号授权；对话框内一键唤醒 |
| **定时任务** | 时间触发器 | 延迟/定时/循环三种；**失败主因是缺授权**（官方建议先手动跑一遍再自动化）；重启后一次性任务补跑、周期任务从当前时间恢复 → **依赖客户端在线，非纯云端调度**[推断] |

- **默认模型 ≠ 实际执行模型**：默认模型只负责对话理解与调度，执行时系统按任务类型自动切换（如生图切图像模型）。用量记录里看到"换模型"是预期行为。
- **权限模型**（可直接抄的四×三矩阵）：策略 `allow` / `ask` / `ask_once` / `deny`；有效期 `once` / `session` / `persistent`。默认**文件读取与网络放行，文件写入 / Shell / 浏览器需确认**。工作区隔离靠**路径白名单 + 符号链接保护 + 边界检查**；另有命令白名单、敏感目录 deny 规则、**审计日志**。

**③ Credits 商业化设计（个人版）**——⚠️ **以下为 2026-08-10 官网 `/pricing` 中文站实抓，与语雀文档口径有出入，以官网为准**：

| 档位（官网中文名）| 价格 | 每日登录积分 | 会员积分/月 | 高质量模型上限 |
| --- | --- | --- | --- | --- |
| 免费版（体验）| ¥0 | 20 | — （另有 7 天试用积分）| 见下方冲突说明 |
| **标准版（轻享）** | **¥69/月** | 20 | **2,000** | 50 次 / 3 小时 |
| 专业版（热门，即 Pro）| **¥139/月** | **30** | 4,000 | 50 次 / 3 小时 |
| 精英版（进阶，即 Elite）| **¥699/月** | **50** | 20,000 | 150 次 / 3 小时 |
| 尊享版（旗舰，即 Ultra）| **¥1,399/月** | **100** | 40,000 | 无限制 |

- 🔴 **官网比语雀多一个「标准版 ¥69/月 = 2,000 积分」档位**，语雀文档完全未提及 → 语雀的三档表述（Pro/Elite/Ultra）**已过时**。
- 🔴 **每日登录积分按档位递增（20/20/30/50/100）**，并非语雀所述的"所有档位统一 20"。
- 🔴 **口径冲突（未解决）**：官网 FAQ 写「免费套餐…可每 3 小时最多使用 **20 次**高质量模型」，语雀《积分与额度》则写 Free **不可用**高质量模型。两处矛盾，**对客前需实测确认**。
- 限时活动（2026-08 在架）：**每月赠送 2,000 积分（每日 100，8/31 截止）**；连续包年「立省两月」。
- **企业版（Business）官网无公开价格，入口是"联系我们"** → 语雀里"四档套餐价格仅图片"的缺口**官网也没填上**，企业版仍是 Sales-led 报价。
- 新用户赠 **500 试用积分 / 7 天**。
- **模型成本只给档位不给单价**：低（DeepSeek V4 Pro/Flash、MiniMax M2.5）｜中（Auto、标准、Qwen 3.7 Plus）｜高（专业、Qwen 3.7 Max、GLM-5、Kimi K2.5）｜极高（极致）。**0.15.0+ 版本 Auto 能力升级导致积分消耗变快**。
- 升级当天调额度、**降级下周期生效**；**支付宝扫码支付不支持退款**（仅能取消自动续费），Stripe 退款扣手续费；**2026-04-19 起国内新用户统一支付宝渠道**，此前为 Stripe。

**④ 企业版治理模型（最有复用价值的部分）**：

- **与个人版是两个独立产品**：同一客户端（**0.7.6+** 可见）左下角切换，但**不可从个人版升级**、**积分不互通**；新用户赠送积分只落个人空间。
- **三角色权限矩阵**：Owner 独占「修改成员角色 / 查看账单历史 / 进入订阅页」；Admin 可进控制台、管资产、**仅可分配 Member 积分**；Member 无控制台。**Admin 数量无限制，但暂不支持自定义 Admin 权限范围**。
- **配额**：子账号上限 **入门版 5 / 标准版 15 / 旗舰版 50**（含 Owner+Admin+Member 全部角色）。
- **资产化三条路径**：Agent **推荐制**、Skill **上传即自动上架**、Plugin **分享制**；Owner/Admin 统一控「全员可见」，客户端内标【团队默认】置顶。🔴 **AI 帮助创建的智能体无法共享，仅手动创建的可以**。
- **企业知识库**（**0.20.0+**，仅入门版及以上）：四状态（待解析/解析中/解析成功/内容违规）；**解析成功后企业内全员可见——无文件级权限**；仅 Owner/Admin 可上传；**智能体生效范围由成员各自管理，Owner/Admin 无法干涉**；改生效范围**仅对新对话生效**；重命名必须带后缀。
- **计费结构**：套餐（体验/入门/标准/旗舰，**主价格表仅图片未文字化**）+ 积分加油包 **¥1,099/2 万、¥2,499/5 万、¥6,999/15 万（均 6 个月有效）** + 席位加油包 **¥4,000/年/席位 = 6,000 积分/月/席位（不跨月累计，仅标准版/旗舰版可增购）**。**消耗顺序：套餐内积分 → 加油包**。
- **双币种**：i 豆（生意助手存量货币）+ 积分（AI 新货币），默认 **i 豆优先、不足扣积分**；⚠️ **仅主账号可改消耗偏好，子账号不可**。
- **审计**：Owner/Admin 可看全员消耗明细并下钻任务；成员移除后**记录保留但无法下钻会话**，团队数据归团队、支持资产转移。
- 🔴 **Owner 邮箱不可更改**：企业版权益绑定购买时国际站主账号邮箱，私自在 MA 后台改邮箱导致无法登录**官方不支持处理**。

**⑤ 生态接入**：**生意助手**（国际站官方，需 **0.12.0+**，已预装，内置 20+ B2B 垂类 Skill；CGS 商家已购生意助手则 **Free 版即可唤起、不额外收插件费**）｜**OKKI**（B2B 客户经营，三模块 CRM/AiReach/Shops，需已购 OKKI 并绑定授权账号，**仅国内版**，**目前单向调用**——OKKI 内反向调起 AW 未开放）｜**1688 采购助手**（选品比价/找源头工厂/采购询盘，打通「1688 拿货 → 国际站转卖」，**仅国内版**）。
> 判断国内版 vs 国外版：**国内版不外显模型名**（只标自动/标准/专业/极致），国外版外显。装不上 OKKI/1688 插件多半是装了国外版 → 关 VPN 重下。

**⑥ 两个垂直 Agent（两条不同技术路线）**：

- **全域电商管家 = RPA + 多平台账号托管**：覆盖淘宝/京东/拼多多/抖店/1688/AE，12 项技能横跨店铺诊断、竞品监控、发品（文档另一处写"16 项技能"，**与技能表 12 行自相矛盾**）。靠**本地加密密码本**（不上云）实现自动登录切店。🔴 硬红线：Excel 中「商品名称」必须与素材目录下**商品文件夹完全同名**，空格/大小写/序号不同即关联失败。
- **设计专家 = 多模态生成 + 沉浸式画布**：内置 **11 个平台图片规范**（国际站/Amazon/eBay/Walmart/Shopify/Etsy/AliExpress/TikTok Shop/Shopee/Lazada/1688）**生成前自动校验**；一次出整套主副图；多分镜视频最长 **32 秒**；宣称"锁定产品形态/颜色/材质/Logo 不变、不虚构认证与参数"。成本优化前后：简单 104→**11** 积分、中等 144→**25**、复杂 184→**50**（auto 模型，官方注明非固定值）。
- 官方 Skill 的 i 豆价目（可作 Agent 功能定价参考）：URL 发品 **10–40 i 豆/品**（支持 1688/淘宝/天猫/AE/Amazon，单次最多 100 条、建议 5–10 条），素材包发品 **62 / 101 / 168 i 豆**（快速版/经济基础版/全能精装版，单次最多 15 商品 15 图）；店铺装修 获取账号信息 **≥80 i 豆**、生成预览/完整页 **10–20**、编辑 **10**。⚠️ **进入实际发品流程后即使部分失败，已处理部分照常计费**。

**⑦ 对 SA 的可复用洞察**[推断]：

- **① Credits 抽象已成 Agent 产品定价事实标准**：与[[百炼]] Token Plan 同构——「统一 Credits 计量 + 模型成本分档 + 高质量模型滚动窗口限流 + 加油包兜底」这四件套可直接搬进客户的 Agent 平台计费设计。差别在受众：Token Plan 面向开发者工具链，Accio 面向业务终端用户。
- **② 企业版治理清单可当需求模板**：团队积分池 + 子账号配额分配 / 三角色权限矩阵 / 资产可见性管控 / 成员级用量审计与离职留痕 / 知识库全员可见但生效范围自治——客户提「我们要个企业 Agent 平台」时，这就是问需求的提纲。
- **③ 双币种是存量企业上 Agent 的必经形态**：老业务货币（i 豆）与新 AI 货币（积分）并存 + 消耗优先级 + 偏好开关。凡是已有计费体系的客户都会遇到，注意"仅主账号可改偏好"这类权限坑。
- **④ 印证「路由准确率 = 系统天花板」**（见本文件第 10 节）：Skill 双开关设计与"装太多技能反而调不准"、官方明确建议拆多 Agent 而非堆一个大 Agent——与集团内多 Agent 回退到「单编排器 + Skills」的共识同向。
- **⑤ 客户端型 Agent 的自动化天花板**：定时任务依赖客户端在线，天然弱于云端调度。客户若要 7×24 无人值守，应走云端 Agent（百炼/PAI）而非客户端产品——这是对比时的关键分野。
- **⑥ 社媒自动化的风控红线**：OKKI 文档**明确建议初期不要用品牌官方大号**做自动化发布（第三方海外社媒自动化普遍面临平台风控），建议先用测试号。对客承诺自动化运营时必须带上这条。

**⑧ 已知文档缺口**（对客前必须另行确认）：**企业版四档套餐价格与权益——语雀仅图片、官网入口是"联系我们"，两边都拿不到，确认为 Sales-led 报价**；企业知识库容量配额未给；**数据存储地域、是否用于模型训练、隐私条款、合规认证全部未涉及**；私有化/专有云部署未涉及；SLA、速率与并发限制未涉及；各模型单次积分数值未公开。
**⑨ 来源与鲜度**：主体来自语雀 28 篇（2026-08-10 归档）；第 ①③ 条的产品家族界定、个人版五档价格、每日登录积分梯度、限时活动与企业版无公开价，来自 **`www.accio.com` `/pricing` + `/about-us` 2026-08-10 浏览器实抓**（SPA 客户端渲染，curl 取不到正文）。**定价属高频变动项，已纳入月度价格抽样复核池候补**。未纳入：`/help`（robots.txt Disallow 且与语雀高度重叠）、`/blog/`（消费选品趋势内容）、PLP/PDP/supplier SEO 商品页。

---

### 12. Agent 工程问答速查（研发大讲堂 90 期观众问答，2026-08-25）[实战+推断]

> 来源：中国研发大讲堂第九十期《AI Coding 实践与大模型前沿趋势分析》观众聊天区 8 问。完整问答稿见当次会话 outputs。与第 9/10/11 节互为印证。

- **Skill 治理**：三类角色（平台管理员/Skill Owner/贡献消费者）+ 三层分级（官方/团队/个人，类 npm scope）+ 使用频率遥测驱动生命周期（高频晋官方、低频归档）；「在别人 skill 上微调」优先组合（base+团队 overlay）而非 fork；每 skill 附回归哨兵防腐烂；「装太多技能反而调不准」→ 收敛单编排器+分层 Skills+确定性路由（与 §10.2、§11④ 共振）。
- **Harness 落地**：DeepSeek=引擎、OpenClaw/Claude Code=身体（harness=工具+沙箱+权限+记忆+重试编排层）；SAP/ERP 接入=RFC/BAPI/IDoc 封 MCP，只读先行再审批式写；生产力公式=模型×harness×工具工程×SOP 嵌入；MCP 市场 89.7% Server 使用量<1 万 → 接入≠生产力。
- **3/5 年趋势**：1 年内 harness 协议标准化（MCP/A2A=agent 时代 HTTP）+「RAG 底座+编译层」双层；3 年模型商品化、资产（skill/评测/连接器库）升值、组织岗位合并；5 年 spec 驱动开发主流、程序性知识=企业核心资产；不变=责任在人、编码提效≠交付提效。一句：模型层贬值、系统层升值。
- **RAG vs 本体**：不从零重建（经典 KG 坑），增量演化——RAG 先跑通→LLM 编译高频知识进本体/wiki 层双层并存；强结构域（法规/科目/主数据）才并行建本体。
- **上下文与记忆**：热/温/冷三层；显式文件记忆 > 纯向量（可审计可改可删）；中规模 index.md 即可、大规模 BM25+向量；框架对位 MemGPT/Letta（OS 分页）vs LangGraph（状态图）vs 文件化（工程主流）。
- **协议 vs 记忆**：协议=HTTP（互通）、共享记忆=DB（状态）；中心编排+共享工件层 > 对等协商（错误放大 17.2× vs 4.4×，呼应 §10.1）。
- **闭环自增强**：闭环落在资产不落在权重（日志→memory→审核晋升 skill→回归验证）；先修评测再改 Agent（呼应 §10.4）。
- **MiniMax vs DeepSeek**：DS=推理/代码/开源/私有化/极致性价比，弱多模态生成与 API 稳定性；MiniMax=语音/视频多模态+C 端陪伴+Agent M 系列；落地调用量比例≈轻量模型走量 70–80% / 旗舰走难 15–25% / 多模态走场景其余。

## 13. 长上下文 / 思考模型的超长输出延迟治理（GLM-5.2 实战）

> 来源：2026-07-15 百炼业务网关 glm-5.2 高延迟工单排查（Query 回写）+ Google/GitHub 交叉验证。

### 13.1 事实：GLM-5.2 是智谱模型，可通过百炼网关调用 [官方]
- **GLM-5.2 = 智谱 AI（Zhipu / THUDM）的模型，不是通义/阿里自研**；发布约 2026-06-13。内部业务网关（dashscope-admin）可以代理/接入该模型。
- 规格（智谱官方多源交叉）：**上下文 1M（100万）token / 最大输出 128K（131072）token**；属**深度思考（reasoning）模型**（双思考模式）。
- **含义**：一个模型的「默认/最大输出长度」由其**模型 spec（此处是智谱）**决定，与“走哪个网关”无关；不要把它当成百炼/Qwen 的默认。

### 13.2 百炼 thinking 模型的截断参数语义 [官方]
> 百炼 OpenAI 兼容接口（help.aliyun.com/zh/model-studio）对思考模型有关键区分：
- **`max_tokens`：只限制“回答”部分**（不含思维链）——对思考模型**挡不住思考跑飞**。
- **`max_completion_tokens`：限制“思维链 + 回答”的完整输出**——想兜住总时长/总生成量要用它。
- 默认值与最大值通常 = 模型最大输出长度（特定模型可不同，以其 API 文档为准）。
- 思考开关：Zhipu 系 `thinking:{type:"enabled"|"disabled"}`；Qwen 系 `enable_thinking` + `thinking_budget`；**glm-5.2 在百炼的确切字段以其模型 API 文档为准**。

### 13.3 “支持 128K 但过 64K 断崖”——事实核查 [官方+实战]
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

### 13.4 实战案例：glm-5.2 over-thinking 导致 ~20min 延迟 [实战]
- 10 条高延迟请求均 http_code=200、SSE、prod；总耗时 ~20–25 分钟（cost 118万–150万 ms）。
- **8/10 条 output_tokens=65537（=64K+1）且 reasoning_tokens=65536、回答仅 1 token** → 思考打满 64K 输出预算被截断，**没产出答案**（finish_reason≈length）。
- TTFT（first_output_duration）仅 0.5–28s，占总耗时 <3%；解码吞吐 ~44–56 tok/s。
- **根因 = decode-bound + 思考失控**，非排队/网络/首包。注意 64K 仅模型上限 128K 的一半，说明是 max_tokens/网关默认而非模型上限。
- 注：**业务网关“用户请求查询”报表不记录请求入参**（无 max_tokens/prompt/temperature 字段），只有 usage 用量。要看入参需客户端日志/请求级 trace。

### 13.5 客户端延迟治理 Playbook（可直接给客户）[实战]
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

## 14. Coding Agent 工程化：Loop Engineering / Graph Engineering [ATA实战+grow实战+官方]

> 来源：2026-08-08 六路并行调研（ATA 56 篇全文 / 29 篇一手英文源 / 33 个 GitHub 项目实测 / Graph 专项 24 篇 / Multica 源码测绘 / grow 5 门课 6.6 万字听悟文稿）。
> 完整报告：`~/Desktop/neilcodebase/loop_engineering_practice/research/`（00-master-report.md + 01-spec）

### 14.1 术语定谱：外部无共识，内部有两套定义 [官方+实战]

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

### 14.2 量化效果：门禁 > 图谱（优先级判据）[实战]

| 措施 | 效果 | 性质 | 来源 |
|---|---|---|---|
| 加门禁/约束 | **编译通过率 35% → 91%**；环境适配失败率 15%→3%；误判新增率 20%→5% | **可行性前提** | ATA 051 高德测试 AgentLoop（prompt 1600+ 行中 **60% 以上是约束而非指令**） |
| review 子代理 | 成本仅编码的 **10-20%**，总成本降 60-70% | 可行性前提 | ATA 005 Qoder 官方 |
| 注入代码图谱 | 时间 −44%、Token −56%、工具调用 −71% | **效率优化** | ATA 050 蚂蚁 BizFlow（同链路同 prompt 唯一变量对照） |
| 完整生产闭环 | 一周 ERROR **1210→47（↓96%）**；修复 48min→15min；人工介入 每次→**0**；多 Agent 冲突率 30%→<5% | — | ATA 003（诚实标注：**工具链建设占总工作量 30%**） |
| 经验自进化 | SWE-bench Verified **67.2%→74.4%（+7.2pp）**；工具调用 −25.1%；有害事件 −27.8% | — | ATA 052（轨迹清洗到原始 Trace 的 4-6%） |

**结论**：图谱优化"跑得快不快"，门禁决定"能不能自主跑起来"，**量级差一档**。

### 14.3 自主度分级：内部矩阵 vs 外部权限档 [实战+官方]

| 体系 | 出处 | 用途 |
|---|---|---|
| **A1-A5 × T1-T5 正交矩阵** | ATA 039 AgentLoop | **成熟度门槛**。人注意力档 5%/15%/30%/50%/80%；晋级阈值 **A2 覆盖率≥60% / A3 历史成功率≥90% / A4 ≥99%+自动回滚** |
| **`permission_mode` 六档** | Claude Agent SDK [官方] | **权限档位**。`default`/`acceptEdits`/`plan`/`dontAsk`/`auto`(classifier 逐动作)/`bypassPermissions`(**仅隔离环境、不能 root**) |

`auto` 档官方数据：classifier *"caught more dangerous actions than developers did"*，且 ***"Claude works 9x longer between interruptions"***。

三个具名客户的共同结构 = **默认高自治 + 一张很短的硬 deny 清单 + 按操作域降档**：Nuro 硬 deny recursive delete；Gusto 碰 Terraform/AWS 降 `acceptEdits`；Garner Health 禁"与他人通信"类动作。

### 14.4 门禁的成本平衡（唯一一手答案）[官方]

Thoughtworks 已把 backpressure 升为 **Trial 级 blip**，规则原文：门禁 *"should run **during the coding session** and report clean results **before a commit is made**, rather than relying on post-commit checks."*

**Stripe 的两级设计（可直接抄）**：

| 级别 | 轮数 | 实现 |
|---|---|---|
| 本地确定性 lint | **无限 loop** | pre-push hook + 后台 daemon 预计算缓存，**1 秒内出结果** |
| 完整 CI | **硬限 1 轮 + 1 次修复** | 之后转人工。理由：*"diminishing marginal returns..."* |

规模验证：**每周 1300+ 个纯 agent 产出的 PR 合并**。

**两类闸门必须分开**（[推断]，但混用是常见设计错误）：质量门禁 **fail-closed**，资源门禁 **fail-open-to-human**（超预算是升级不是失败）。

### 14.5 失败模式与 reward hacking [官方]

Anthropic 官方三分类：**agentic laziness**（50 项审查做 35 项就宣布完工）/ **self-preferential bias** / **goal drift**（compaction 后目标漂移）。

Ralph 作者最直白：*"the reward function is compiling code"*。四条对策：做者/判者分离、判者单独调 skeptical、能确定性就别用推断、**要证据不要断言**（*"show evidence rather than asserting success"*）。反向警告同为官方：过度 review 导致 over-engineering，reviewer prompt 要限定"只报影响正确性的问题"。

> **四源同述（本轮置信度最高的设计原则）**：飞樰"不能既当运动员又当裁判员" = 釋心"maker/checker 拆分" = Anthropic 做者判者分离 = 釋心金马奖"自家回归 + 官方评测平台**双 tracker 交叉验证**"。

### 14.6 状态持久化：官方四件套 + event sourcing [官方+实战]

Anthropic 对问题的定义：*"engineers working in shifts, where each new engineer arrives with **no memory**"*，并**明确说 compaction 不够**。官方解法 = **initializer agent + coding agent 两套 prompt**，initializer 首轮产出 `init.sh` + `claude-progress.txt` + **一个初始 git commit** + **200+ 条初始全标 failing 的 feature list**。

- context 管理三件套（官方原词）：`compaction` / `structured note-taking` / `multi-agent architectures`
- 最实操的官方警告：**compaction 会吃掉早期规则** → *"Persistent rules belong in CLAUDE.md ... **re-injected on every request**"*
- 官方提供 `session_store` adapter，**支持无状态容器跨主机 resume**

**三方独立收敛到 event sourcing 而非 state snapshot**：Temporal *"records a full Event History... you never have to think about checkpoints"* + ATA 044 AgentRun "Session 是活在上下文窗口之外的追加式事件日志"（TTFT p50 −60% / p95 −90%）+ ATA 022 如意"无状态容器 + Session 持久化事件轨迹"。

**内部更主动的操作手法**（grow 颜律）：每轮问 agent "列出本轮主题 + 健康度"（红/橙/黄/绿），**对话超 10~15 轮或主题超 3~4 个就新开会话并让 agent 整理上下文接过去**。

### 14.7 六方一致：不要默认上图编排框架 [官方]

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

### 14.8 代码图谱：只有轻量档成立 [论文+官方]

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

### 14.9 常驻服务化：三种形态 + 一条合规红线 [实战]

| 形态 | 代表 | 算力位置 | 特征 |
|---|---|---|---|
| 本地 Daemon + 云端编排 | **Multica**（ATA 040，929 览） | 用户本地 | LLM 账单归用户、**代码不出本地**；定位"**调度器而非大脑**"（全仓库无 LLM SDK，prompt 模板 <200 行） |
| 办公网单机托管 | 蚁窝（ATA 024，一台 Mac Studio） | 办公网 | 受网络边界约束 |
| 云端 Managed Agent | 如意（022）/ AgentRun（044）/ Qoder Cloud Agents | 云端 MicroVM | 强隔离可弹性 |

**🔴 合规红线（ATA 025《OpenClaw 集群已在内网上线》13033 览）**：
> `2026/03/06` 接到安全团队沟通：**生产网、测试网禁止部署此 Agent。这类 Agent 只能在沙箱环境内部署（强隔离）。** `2026/04/09` 已按合规要求全部迁移到沙箱环境。

**Stripe 讲透了沙箱与自治的因果**：因为 devbox 是隔离 QA 环境（**无真实用户数据、无生产服务、无任意网络出口**），所以 *"the agent doesn't need confirmation prompts"*。→ **沙箱够硬才有资格谈高自治常驻。**

**凭据正解 = egress proxy**（ATA 045，589 览，点名 Multica *"执行层还是你本地的 runtime，从权限的视角其实就还是你"*）：拆开**触发人 / Agent 身份 / 执行身份**三件事；agent 在容器里发**不带 token** 的请求，出网时 proxy 按身份注入短期 token → **真实凭证不进沙箱**。反模式：token 塞进容器 env（"Agent 一执行 `env`、读配置、打印日志就可能泄漏"）。现成组件：**`alibaba/OpenSandbox`**（Aone Sandbox 开源版，12399★）的 Credential Vault，是**唯一可 `go get` 的沙箱 Go SDK**。

### 14.10 多仓库服务化：Devin 的官方架构最贴合 [官方]

**Devin**：*"this snapshot should include **all the repositories you want Devin to work on** ... You can think of this as **setting up Devin's laptop on the first day of work**."* 机制 = 组织级 VM snapshot + **per-repo 的 Secrets/Lint/Test/Run 命令** + direnv/nvm per-repo 环境隔离 + **Machine Version History 快照回滚**。

**Cursor Cloud Agents** 支持 multi-repo：`.cursor/environment.json`（环境即代码）+ Builds 预备 + restrict outbound domains + OIDC。

**反面参照**：GitHub Copilot cloud agent 是**单仓单分支单 PR + 59 分钟硬上限** —— 最有条件做多仓的厂商选了最保守模型，说明**跨仓 PR 的原子性/权限/review 归属复杂度被刻意规避**。

**Stripe 三层样板**：预热多仓 devbox 池（**10 秒 SLO**）+ blueprint 状态机（确定性节点混 agent 节点）+ 中心 MCP 层 Toolshed（近 **500 tools** 但**按任务只下发子集**）。

**Sourcegraph 的 "80% problem"（多仓场景最强论证）**：agent 可靠完成可见的 80%，漏掉的 20% **每次都是同几类** —— auth middleware / 另一层 API DTO / audit log / **sibling repo 里的集成测试** / 前端 guard / migration script。

### 14.11 可靠性数据与成本量级 [论文+实战]

**METR（唯一权威曲线）**：人类耗时 **<4 分钟**的任务成功率接近 100%；**>4 小时**的任务 **<10%**。TH1.1 修订后 ≥2024 doubling time **108.9→88.6 天**；Opus 4.5 的 50% time horizon = **320 分钟 [170, 729]**。
> ⚠️ 必须一起引用：*"These confidence intervals are still very wide"* —— **320 分钟 ≠ 能可靠工作 5 小时**，它只是 50% 成功率的插值点。

**成本量级**：单 Agent 任务 ≈ 普通 chat 的 **4 倍** token；多 Agent 系统 ≈ **15 倍**（ATA 046）。反面案例：CSS 小改跑 2 天烧 **~$100**，根因是模型 CRLF 换行导致改动根本没写盘（grow 颜律）。

**行业分歧（真实未收敛，须诚实呈现）**：Cognition 主张 single-threaded linear agent，Anthropic 多 agent 研究系统却比单 agent 高 **90.2%**。→ [推断] 领域不同不是真矛盾：code editing 的并行动作产生**冲突的隐含决策**，read-only research 的广度**可无冲突并行**。**规则应定为：并行度由「是否写共享状态」决定，而非由任务大小决定。**

### 14.12 六条踩坑（全部有出处）[实战]

1. **ATA 001**："用 Loop 的时候，你的需求和验证标准必须比原来写得**更加明确**"；不要每天现开 Loop（费 token + 结果漂移不可复现）
2. **ATA 033**（7587 览）原文直书：**"不要在一个会话里跑完全部流程"**
3. **ATA 043**（1792 览）：**"agent 的失败模式是 infra 设计缺陷的放大器"** —— "Agent 每次都会忠实地撞上去，频率极高"
4. **ATA 047**："每次命令失败都销毁重建…**试错无法收敛**"；要求**原样透传退出码**、区分"依赖仍在初始化"与"初始化已失败"
5. **grow 颜律**：朋友团队完全 vibe coding，**一个月后代码重复率 90%**
6. **claude-code-action 源码注释**：`exempt_head_branches: []` 因为 *"branch names are attacker-controlled, so this is not a safe place to encode trust"*；且**配置只从默认分支读** → 自建时把 verify 命令放仓库内配置，**必须只从默认分支读**，否则提个 PR 就能提权

### 14.13 对方案设计的启示

1. **给客户设计 coding agent 平台时，先卖门禁不卖图谱** —— 35%→91% 的编译通过率是可行性前提，图谱的 −44% 时间是效率优化，量级差一档。
2. **"常驻 agent" 要区分云端与常驻两件事** —— ATA 045 自我怀疑成立：Claude Code 公开数据**平均任务时长 45s**，"真正需要的是调度能力和权限边界，不一定需要一个云端 Agent 长时间占着机器自己思考"。价值在长尾（定时巡检、错误自愈、跨仓批量改造），不在平均值。
3. **上云端 Agent 方案必带沙箱与凭据设计** —— ATA 025 合规红线 + ATA 045 egress proxy，这两条是内网/生产场景的准入条件，不是加分项。
4. **不要给客户推荐图编排框架做 coding agent 编排** —— 六方一致反对，且有官方运维成本清单可举证。
> 🔀 **编号说明（2026-09-24 合并）**：本节在统一仓库 neil-skills 侧原编号「## 10. / ## 11.」；并入后与上方「关键追踪线」内的 `### 10./### 11./### 12.`（独立仓库侧新增）撞号，
> 故顺延为 **第13节（长上下文延迟治理）/ 第14节（Coding Agent 工程化）**，子编号 10.x→13.x、11.x→14.x 同步。历史 changelog / inbox 中的「第10节/第11节/11.7」等旧称指本节。


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
