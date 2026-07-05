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
- 核心模式：AI Gateway(Higress) 多模型容灾 → 0.5 秒自动切换
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
