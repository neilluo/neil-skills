# Inbox — Raw 层注册入口

> **Karpathy LLM Wiki 角色**：本文件是 Raw Sources 层的**索引与状态机**，跟踪每个来源的生命周期。
> 实体存储位于 `raw/` 目录（不可变副本）。
>
> **写入优先红线**：收到任何投喂资料的第一个动作就是在这里登记一条 pending 记录，再做分析。
> 状态机：`pending`（已登记，未处理） → `processing`（蒸馏中） → `done`（已落盘到 knowledge/）。
> 格式：`- [状态] 日期 | 类型 | 标题 | URL | raw/归档路径 | 落地文件`
>
> **与 raw/ 的关系**：
> - inbox.md = 索引（知道有什么、什么状态）
> - raw/ = 实体（原始内容的不可变副本）
> - knowledge/ = 编译产物（蒸馏后的结构化知识）

## Pending（待处理）

> **[raw-pending] 标记说明**：官方文档（help.aliyun.com）按 AGENTS.md 策略仅存 URL+摘要，无需全文归档；
> ATA 文章已全部存入 raw/ata/ 目录（含 SHA256）。以下官方文档条目标记 `[done]` 表示已按策略完成归档。

> 以下为种子语料 —— 等待逐篇蒸馏。每篇蒸馏前先移到 Processing，蒸馏后再移到 Done 并指明落地文件。

### Coding Agent 工程化专项（2026-08-08，六路并行调研）— 已蒸馏

> ⚠️ **本次违反了写入优先红线**：先做调研后登记 inbox，而非收到任务第一动作就登记。已在 changelog 标注。原始资料全部落盘在项目 `research/raw/`（不在本 skill 的 raw/ 下，因体量 1.4MB+ 且属项目资产），本条为索引指针。

- [done] 2026-08-08 | ATA×56 | Loop Engineering / Graph Engineering / 常驻 Coding Agent 地毯式调研（122 关键词 → 640 篇去重 → 归档 56 篇全文） | 核心 6 篇：飞樰《Loop Engineering 概念解析》https://ata.atatech.org/articles/11020674841 、飞樰《从 Loop 到 Graph Engineering》https://ata.atatech.org/articles/11020728011 、也达《线上错误自主发现修复发布》https://ata.atatech.org/articles/11020683205 、风弦《业务流如何提升 Coding Agent》https://ata.atatech.org/articles/12020607628 、《OpenClaw 集群已在内网上线》https://ata.atatech.org/articles/11020588930 、《权限，身份，云沙箱》https://ata.atatech.org/articles/12020707208 | `loop_engineering_practice/research/raw/ata/`（56 篇，带 metadata 头） | knowledge/ai-trends.md 第11节
- [done] 2026-08-08 | Web/一手×29 | Anthropic harness/context 官方系列、Thoughtworks Radar Vol.34、Stripe minions、Devin machine setup、Cursor Cloud Agents、METR time-horizon 1.1、Sourcegraph 80% problem、Cognition don't-build-multi-agents | 官方文档按策略仅存 URL+摘要，正文已归档 | `research/raw/web/`（32 篇，二手明确标 SECONDARY） | knowledge/ai-trends.md 第11节
- [done] 2026-08-08 | GitHub×33 | 循环骨架（goose/aider/SWE-agent）+ 常驻服务（omnara/vibe-kanban/Sculptor）+ 沙箱（OpenSandbox/E2B/codex-rs）+ 评测（SWE-bench harness），star 与最近 commit 全部 `gh api` 实测 | — | `research/raw/github/`（24 文件覆盖 33 项目） | knowledge/ai-trends.md 第11.7/11.9节
- [done] 2026-08-08 | 论文/官方×24 | Graph 专项：SCIP/Kythe/Glean/CodeQL/Joern/Stack Graphs/RepoGraph(ICLR2025)/CodexGraph/cAST/LazyGraphRAG/CodePlan(arXiv 2309.12499) + 六家编排框架官方立场 | — | `research/raw/graph/` | knowledge/ai-trends.md 第11.8节
- [done] 2026-08-08 | grow 内网课程×5 | 釋心《Loop Engineering 实践：从 Harness 团队到 Loop 团队》https://grow.alibaba-inc.com/course/4810000000010637 、釋心《理论与实战》/4810000000010695 、覇天《1688 数据研发的 Loop Engineering 实践》/4810000000010723 、颜律《2 小时实战：用 Harness 搭 AI 研发管理体系》/4810000000010521 、式夏《Agent 框架落幕，Agent 工程起航？》/4810000000003454 | `research/raw/grow/`（6.6 万字，页面自带通义听悟文稿，**免 ASR**） | knowledge/ai-trends.md 第11.1/11.6节
- [done] 2026-08-08 | 源码测绘 | Multica（`~/Desktop/neilcodebase/multica`，HEAD `002ea0d87` / 2026-07-17 / v0.2.0）13 问架构测绘 + 3 处交叉核验修正（task 状态机 8 态 / LICENSE 改动版 Apache 2.0 / repocache 1288 行成熟实现） | — | `research/findings/multica.md` | 未入 skill 知识库（属项目资产）

### Web 蒸馏（长上下文 / 思考模型延迟）— 已蒸馏

- [done] 2026-07-15 | Web/Google+GitHub | RULER(NVIDIA arXiv 2404.06654) + Context Rot(Chroma) + morphllm 2026 对比 + THUDM/LongBench | 官方/公开文献，仅存 URL+摘要 | knowledge/ai-trends.md 第10节
- [done] 2026-07-15 | Query回写 | 百炼 glm-5.2 高延迟工单排查结论（10条请求分析）| 内部工单/latency_analysis 项目 | knowledge/ai-trends.md 第10节

### ATA 高价值文章（共 12 篇候选种子）— 9/12 已蒸馏

- [done] 2026-06-17 | ATA | 一个广告行业 AI 顾问的修炼之路（11 天版） | https://ata.atatech.org/articles/11020643601 | raw/ata/ata-2026-06-17-ai-consultant-11day.md | SKILL.md（元方法论）+ knowledge/ai-trends.md
- [done] 2026-06-17 | ATA | ADR 与 SDD：从架构决策到代码落地的闭环 | https://ata.atatech.org/articles/11020634808 | raw/ata/ata-2026-06-17-adr-sdd.md | references/architecture-templates.md（ADR方法论）
- [done] 2026-06-17 | ATA | 宝马落地阿里云Landing Zone Accelerator | https://ata.atatech.org/articles/11020552831 | raw/ata/ata-2026-06-17-bmw-landing-zone.md | references/caf-landing-zone.md + knowledge/company-profiles.md
- [not-found] 2026-06-17 | ATA | 可口可乐云原生变革 | (ATA搜索未找到，可能标题不同或限制访问) | -
- [not-found] 2026-06-17 | ATA | 莉莉丝 AWS Winback | (ATA搜索未找到，仅找到重保/广告分析相关) | -
- [done] 2026-06-17 | ATA | 网商银行智能化业务定位决策系统 | https://ata.atatech.org/articles/12020553615 | raw/ata/ata-2026-06-17-mybank-ai.md | knowledge/ai-trends.md（Agent案例）
- [done] 2026-06-17 | ATA | 构建高可用AI系统 | https://ata.atatech.org/articles/11020604053 | raw/ata/ata-2026-06-17-high-availability-ai.md | knowledge/ai-trends.md（AI Infra）+ cloud-solutions.md（S3高可用模式）
- [done] 2026-06-17 | ATA | Taobao Bonus：淘海外跨境支付资产体系 | https://ata.atatech.org/articles/11020594402 | raw/ata/ata-2026-06-17-taobao-bonus.md | knowledge/cloud-solutions.md（S2跨境参考）
- [not-found] 2026-06-17 | ATA | Aegis AI 数字分身 | (ATA搜索仅返回旧安全产品，未找到AI数字分身文章) | -
- [done] 2026-06-17 | ATA | Serverless跨云迁移：从 AWS Lambda到阿里云FC | https://ata.atatech.org/articles/11020645626 | raw/ata/ata-2026-06-17-lambda-to-fc.md | knowledge/aliyun-products.md（FC卡片补充）
- [done] 2026-06-17 | ATA | SA动手系列2-PD分离技术深度实践 | https://ata.atatech.org/articles/11020600554 | raw/ata/ata-2026-06-17-pd-separation.md | knowledge/ai-trends.md（PD分离实战数据）
- [done] 2026-06-17 | ATA | Java程序员转型AI开发者：四月学习路线 | https://ata.atatech.org/articles/12020603721 | raw/ata/ata-2026-06-17-java-to-ai.md | knowledge/ai-trends.md（Agent三层次）

### help.aliyun.com 官方框架文档（共 4 篇）— ✅ 已全部蒸馏

- [done] 2026-06-17 | 官方文档 | 阿里云 Cloud Adoption Framework (CAF) | https://help.aliyun.com/zh/caf/ | references/caf-landing-zone.md
- [done] 2026-06-17 | 官方文档 | 阿里云 Well-Architected Framework | https://help.aliyun.com/zh/product/2362200.html | references/well-architected.md
- [done] 2026-06-17 | 官方文档 | Cloud Network Well-Architected Design | https://help.aliyun.com/zh/cloud-network-well-architected-design/ | references/well-architected.md (网络章节)
- [done] 2026-06-17 | 官方文档 | 阿里云安全建设指南 ACSG | https://help.aliyun.com/zh/acsg/ | references/well-architected.md (安全章节)

### help.aliyun.com 产品文档全域蒸馏（66+ 产品）— ✅ 已全部蒸馏

- [done] 2026-06-17 | 官方文档 | 计算域 7 产品（ECS/ACK/ACS/ECI/SAE/FC/ESS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 存储域 5 产品（OSS/NAS/CPFS/EBS/Tablestore） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 网络域 11 产品（VPC/CEN/GA/CLB/ALB/NLB/NAT/VPN/高速通道/PrivateLink/Anycast EIP） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 数据库域 11 产品（RDS/PolarDB/Lindorm/Tair/AnalyticDB/Hologres/MaxCompute/DataWorks/Flink/DTS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | AI 域 7 产品（百炼/PAI/千问/万相/灵码/DashScope） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 安全域 9 产品（WAF/DDoS/Cloud Firewall/云安全中心/KMS/堡垒机/RAM/ActionTrail/Config） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 中间件+监控域 12 产品（MSE/RocketMQ/Kafka/RabbitMQ/EventBridge/ARMS/SLS/CloudMonitor/ROS/ACR/CDN/DCDN） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 混合云/边缘 2 产品（专有云/ENS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md

### help.aliyun.com / aliyun.com 客户案例首批蒸馏（共 8 个旗舰 + 索引若干）— ✅ 已蒸馏

- [done] 2026-06-17 | 官方案例 | 南京银行 SOFAStack + OceanBase 金融分布式 | https://help.aliyun.com/zh/document_detail/194962.html | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 哈啰出行 SLS 日志统一 + 百炼 Agent | https://help.aliyun.com/zh/sls/hellobike + developer.aliyun.com/article/1647416 | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 中国一汽 红旗云妹 AI 智能体 | https://www.aliyun.com/customer-stories/automotive-2025-faw | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | bilibili 游戏迁移上云 | https://www.aliyun.com/lowcode/common/case-studies/internet-2023-bilibili | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 启迪公交 PolarDB-X + AnalyticDB | https://help.aliyun.com/zh/polardb/polardb-for-xscale/bus-traveling-tuspass | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 51Talk 智能客服 Agent | https://developer.aliyun.com/article/1647416 | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 菜鸟 PolarDB for AI | https://help.aliyun.com/zh/polardb/polardb-for-mysql/case-studies/ | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 国际客户群索引（Garuda/GCash/Lazada/周大福/老虎/恒生/众安/鹰角/KLab 等 200+） | https://www.alibabacloud.com/zh/customers | knowledge/company-profiles.md（行业映射快查）

### 2026-06-23 MSE Nacos 深度蒸馏 + 全产品 Lint

- [done] 2026-06-23 | 官方文档 | MSE Nacos 实例版本选型指南 | https://help.aliyun.com/zh/mse/product-overview/select-an-edition | knowledge/aliyun-products.md（MSE 卡刷新）
- [done] 2026-06-23 | 官方文档 | MSE Nacos 引擎版本特性 | https://help.aliyun.com/zh/mse/product-overview/edition-features | knowledge/aliyun-products.md
- [done] 2026-06-23 | 官方文档 | MSE 开发版+专业版计费 | https://help.aliyun.com/zh/mse/product-overview/billing-description-of-developer-edition-instances-and-professional-edition-instances | knowledge/aliyun-products.md
- [done] 2026-06-23 | 官方文档 | MSE 企业版计费指南 | https://help.aliyun.com/zh/mse/product-overview/nacos-platinum-edition-billing-description | knowledge/aliyun-products.md
- [done] 2026-06-23 | meta | 全产品 Lint（健康检查 + 报价量级版本维度审查） | (内部触发) | tests/lint-2026-06-23.md（14 个条目，1 个 P0 已修，6 个 P1 待办）

### 2026-06-26 EMR Serverless StarRocks 深度蒸馏

- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 产品概述 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/product-overview/what-is-emr-serverless-starrocks | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 规格规划建议 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/instance-specification-planning-and-suggestions | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 计费方式 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/product-overview/billable-items/ | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档（StarRocks 社区） | 主键表设计指南 | https://docs.starrocks.io/zh/docs/table_design/table_types/primary_key_table/ | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档（StarRocks 社区） | 导入概览 | https://docs.starrocks.io/zh/docs/loading/Loading_intro/ | knowledge/aliyun-products.md

### 2026-06-28 ATA LLM Wiki 知识工程专项

- [done] 2026-06-28 | ATA | 从 LLM Wiki / Obsidian-Wiki / GBrain 来看 Agent时代知识的"自组织"与"自进化" | https://ata.atatech.org/articles/11020627647 | raw/ata/ata-2026-06-28-llm-wiki-self-evolution.md | knowledge/ai-trends.md
- [done] 2026-06-28 | ATA | 别让你的知识腐烂——Karpathy LLM Wiki 在 KBase 的实践 | https://ata.atatech.org/articles/11020627230 | raw/ata/ata-2026-06-28-kbase-llm-wiki.md | knowledge/ai-trends.md

### help.aliyun.com / aliyun.com 客户案例后续待蒸馏（深度档案）

- [done] 2026-06-28 | 官方案例 | PolarDB 客户案例深度蒸馏（心动网络/真有趣/雅迪科技） | https://help.aliyun.com/zh/polardb/polardb-for-mysql/case-studies/ | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | 三一重工工业互联网架构 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | 完美日记/逸仙电商上云路径 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | SHEIN 出海架构 | (公开报道汇总，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | Lazada 全栈电商架构 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [cancelled-merged] 2026-06-17 | 官方案例 | 网商银行金融分布式 | 已由 ATA 文章 ata-2026-06-17-mybank-ai.md 蒸馏到 knowledge/ai-trends.md，不再单独补充

### 2026-09-21 云原生API网关 / AI网关 深度蒸馏（外部认证专项）

> 16 篇已全文归档 raw/aliyun-docs/（每篇头部含 source_url / fetched_date / page_last_modified / summary 四行元信息）。落地：knowledge/aliyun-products.md 新增「云原生 API 网关（APIG）/ AI 网关【深度卡】」+ 三处产品名消歧（MSE 卡/原API Gateway 卡/选型速查表）；knowledge/cloud-solutions.md 新增 S10 + S3 口径订正；index.md / ai-trends.md / architecture-templates.md 交叉引用同步。

- [done] 2026-09-21 | 官方文档 | 云原生API网关「配置自建认证鉴权」（页面更新 2026-09-20，A 路全文） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/configure-self-built-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-configure-self-built-authentication.md | knowledge/aliyun-products.md（深度卡 A 路）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | AI网关「配置自建认证鉴权」（2026-06-02，与 apig 版配置表逐字一致，diff 复核） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-self-built-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-configure-self-built-authentication.md | knowledge/aliyun-products.md（深度卡 A 路）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「Go语言开发网关插件」（2026-04-28，第 462/467 行 = 服务 FQDN 命名规则与 .static 逻辑端口 80 原文出处） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/develop-plug-ins-in-go | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-develop-plug-ins-in-go-service-fqdn.md | knowledge/aliyun-products.md（FQDN 对照表）
- [done] 2026-09-21 | 官方文档 | AI网关「Go语言开发网关插件」（2026-04-23，第 462 行注释与 apig 版逐字相同） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/develop-gateway-plug-ins-using-the-go-language | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-develop-plug-ins-go-service-fqdn.md | knowledge/aliyun-products.md（FQDN 对照表）
- [done] 2026-09-21 | 开源文档 | Higress ext-auth 插件 README（B 路完整字段表 / service_name 定义第 47 行 / envoy vs forward_auth / 全部示例 YAML） | https://raw.githubusercontent.com/alibaba/higress/main/plugins/wasm-go/extensions/ext-auth/README.md | raw/aliyun-docs/aliyun-docs-2026-09-21-higress-ext-auth-plugin-readme.md | knowledge/aliyun-products.md（深度卡 B 路）+ cloud-solutions.md（S10 配置骨架）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「创建服务」（七种服务来源参数表 / TLS 三档） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-create-service.md | knowledge/aliyun-products.md（前置步骤）
- [done] 2026-09-21 | 官方文档 | AI网关「创建服务」（八类来源；DNS 域名 `<DNS域名>:<服务端口>` / 外网地址需 NAT 网关原文出处） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-services | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-creating-services.md | knowledge/aliyun-products.md（前置步骤）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「服务来源管理」（ACK 1.18+/建议 1.28+、同 VPC、安全组授权、Nacos MCPEnabled=true） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service-source | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-create-service-source.md | knowledge/aliyun-products.md（前置步骤）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「插件安装启用卸载」（官方插件=Higress官方/社区插件=Higress社区；三级作用域） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/enable-plugin | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-enable-plugin.md | knowledge/aliyun-products.md（B 路安装启用）
- [done] 2026-09-21 | 官方文档 | AI网关「插件安装启用卸载」（第 31 行：仅专享实例型AI网关支持安装与启用插件，Serverless版不支持） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-plug-ins | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-manage-plug-ins.md | knowledge/aliyun-products.md（避坑 🔴）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「认证鉴权插件清单」（6 插件，无 ext-auth） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-authentication-plugin-index.md | knowledge/aliyun-products.md（B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | AI网关「认证鉴权插件清单」（同 6 插件，无 ext-auth） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-authentication-plugin-index.md | knowledge/aliyun-products.md（B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | MSE 云原生网关「认证鉴权插件清单」（7 插件含 edas-service-auth，无 ext-auth） | https://help.aliyun.com/zh/mse/user-guide/authentication-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-mse-authentication-plugin-index.md | knowledge/aliyun-products.md（MSE 卡消歧 + B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「全局认证鉴权」机制对比（JWT/OIDC/自建三种方式） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/global-authentication-1 | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-global-authentication.md | knowledge/aliyun-products.md（A 路定位）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「计费概述」（专享实例 apigw 全规格单价表 + 数据处理费 0.037/0.049 + CDT，页面更新 2026-06-18） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/billing-overview | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-billing-overview.md | knowledge/aliyun-products.md（计费）+ cloud-solutions.md（S10 成本）
- [done] 2026-09-21 | 官方文档 | AI网关「专享实例计费说明」（aigw 全规格单价表，页面更新 2026-07-29） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/free-product-templates | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-billing-dedicated-instance.md | knowledge/aliyun-products.md（计费）+ cloud-solutions.md（S3 成本订正 + S10）

> 补充口径（2026-09-21 收口已补归档 raw，原「未单独归档」备注作废）：三形态谱系/EOL 时间线/AI 网关能力清单出自 https://help.aliyun.com/zh/api-gateway/llms.txt → raw/aliyun-docs/aliyun-docs-2026-09-21-apig-llms-index.md ；AI Credits（0.01 元/Credit、开通后不支持退订）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md ；Serverless 旧版 CU 系数（10/5/2、0.005 元/千CU、最小 1000 CU 不足 10 万按 10 万计）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md ；Serverless 新版商业化公告（公测 2026-08-31 结束）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-commercialization-announcement.md 。

### 2026-09-21 收口补充（MCP 鉴权维度 + 火山引擎对标 + 合思画像 + forward_auth 源码取证）

> 本轮为上一轮网关蒸馏的收口：MCP 维度与竞品对标两路取证在上一轮开跑后才回来，本次补入并修正引用限定。新增 raw 20 个文件（aliyun-docs ×9、standards ×4【新目录】、competitor ×4、misc ×1、ata ×2）。ATA 内网站点被 SSO 拦截，两篇 ATA 仅能归档**逐字摘录**（头部已注明「摘录而非全文」）；客户现场记录含敏感信息不落 raw（脱敏红线）。

- [done] 2026-09-21 | 官方文档 | AI网关「调试MCP服务」（第 29 行工具级鉴权过滤 tools/list 反证 + 第 60 行 Bearer Token 调试配置） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/debug-mcp-services | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-debug-mcp-services.md | knowledge/aliyun-products.md（MCP 维度）+ cloud-solutions.md（S10 实战案例）
- [done] 2026-09-21 | 官方文档 | AI网关「消费者认证」（MCP服务级/工具级、服务级权限高于工具级、仅支持 API Key、ApiKeyIdentityConfig apikeySource=Header/QueryString） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-certification | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-consumer-certification.md | knowledge/aliyun-products.md（三种鉴权能力对照表）
- [done] 2026-09-21 | 官方文档 | AI网关「HTTP转MCP 配置字段说明」（工具 YAML 存放网关侧、tools/list 不回调后端） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/http-to-mcp-field-configurations | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-http-to-mcp-field-configurations.md | knowledge/aliyun-products.md（HTTP转MCP 鉴权语义）
- [done] 2026-09-21 | 官方文档 | AI网关「新功能发布记录」（2026-01 MCP Server 支持 JWT 认证 → 与 consumer-certification「仅支持 API Key」矛盾，文档口径滞后） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/new-feature-release-notes-ai-gateway | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-new-feature-release-notes.md | knowledge/aliyun-products.md（🔴 官方文档自相矛盾记录）
- [done] 2026-09-21 | 官方文档 | AI网关「引擎版本说明」（最新公开引擎版本 2.1.23 / 2026-09-03） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/engine-version-description | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-engine-version-description.md | knowledge/aliyun-products.md（产品缺口存疑项）
- [done] 2026-09-21 | 官方文档 | AI Credits 计费详情（补归档，上一轮仅在线复核） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/ai-credits-billing-details | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md | knowledge/aliyun-products.md（计费备注已改为已归档路径）
- [done] 2026-09-21 | 官方文档 | Serverless（旧）计费详情（CU 系数 10/5/2，补归档） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/serverless-old-billing-details | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md | knowledge/aliyun-products.md（计费备注已改为已归档路径）
- [done] 2026-09-21 | 官方文档 | AI网关 Serverless 商业化公告（补归档） | https://help.aliyun.com/zh/api-gateway/ai-gateway-commercialization-announcement | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-commercialization-announcement.md | knowledge/aliyun-products.md（计费）
- [done] 2026-09-21 | 官方文档 | API 网关产品线 llms.txt 全文索引（三形态谱系/EOL/AI 网关定位出处，补归档） | https://help.aliyun.com/zh/api-gateway/llms.txt | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-llms-index.md | knowledge/aliyun-products.md（产品谱系）
- [done] 2026-09-21 | 标准规范 | MCP 官方规范 Authorization 章（2026-07-28 版 + 2025-11-25 版，四版关键结论一致；无 per-method 免鉴权白名单） | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization ；https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization | raw/standards/standards-2026-09-21-mcp-spec-2026-07-28-authorization.md + standards-2026-09-21-mcp-spec-2025-11-25-authorization.md | knowledge/aliyun-products.md（MCP 协议层事实 [规范]）
- [done] 2026-09-21 | 标准规范 | MCP 官方规范 Streamable HTTP 传输章（2026-07-28 版，单一 MCP endpoint / 每条 JSON-RPC 消息一个 POST / 网关中介预设 / Security Warning 第 3 条）+ Transports 总览页 | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | raw/standards/standards-2026-09-21-mcp-spec-2026-07-28-transports-streamable-http.md + standards-2026-09-21-mcp-spec-2026-07-28-transports.md | knowledge/aliyun-products.md（MCP 协议层事实）
- [done] 2026-09-21 | 竞品文档 | 火山引擎 API 网关「MCP 服务」（HTTP转MCP 仅支持 Streamable HTTP；身份认证=Key Auth 插件） | https://www.volcengine.com/docs/6569/1816086 （经 getDocDetail API 取 MDContent，绕开 SPA JS 壳陷阱） | raw/competitor/competitor-2026-09-21-volc-apig-mcp-service.md | knowledge/competitor-cloud.md（火山 API 网关/AI 网关对标）
- [done] 2026-09-21 | 竞品文档 | 火山引擎「外部认证鉴权」插件（仅实例级、同私有网络硬约束、认证地址自由路径、认证方法可选 GET/POST、前缀或精确匹配、Host/Method/Path/Content-Length 默认走 header） | https://www.volcengine.com/docs/6569/1798159 | raw/competitor/competitor-2026-09-21-volc-apig-external-authentication.md | knowledge/competitor-cloud.md（外部认证对标核心表）
- [done] 2026-09-21 | 竞品文档 | 火山引擎「安全与认证概述」（外部认证=自定义 Token/实例级别/适用已有自建认证体系） | https://www.volcengine.com/docs/6569/2502428 | raw/competitor/competitor-2026-09-21-volc-apig-security-certification-overview.md | knowledge/competitor-cloud.md
- [done] 2026-09-21 | 竞品文档 | 火山引擎「什么是 API 网关」（采用 Envoy 内核，兼容 Kubernetes Ingress 标准 → 技术底座同源结论） | https://www.volcengine.com/docs/6569/82992 | raw/competitor/competitor-2026-09-21-volc-apig-what-is-api-gateway.md | knowledge/competitor-cloud.md
- [done] 2026-09-21 | 开源源码 | Higress ext-auth main.go/config.go 关键片段（endpoint_mode 分支、Authorization 无条件透传、with_request_body×GET 校验、DefaultStatusOnError=403、failure_mode_allow 仅 ≥500、GetRequestPathWithoutQuery）⚠️ 摘录而非全文 | https://github.com/alibaba/higress/tree/main/plugins/wasm-go/extensions/ext-auth | raw/misc/misc-2026-09-21-higress-ext-auth-source-excerpts.md | knowledge/aliyun-products.md（forward_auth 源码级细节）
- [done] 2026-09-21 | ATA | 陈思亮(玄斧)《AI网关-Restful API转换MCP的桥梁》11020495607（唯一 HTTP转MCP+消费者鉴权端到端实操）⚠️ SSO 拦截，仅归档逐字摘录 | https://ata.atatech.org/articles/11020495607 | raw/ata/ata-2026-09-21-http-to-mcp-consumer-auth-excerpts.md | knowledge/aliyun-products.md（MCP 维度 [实战]）
- [done] 2026-09-21 | ATA | 骁霆/王炳松《基于阿里云 AI 网关的万镜一刻 API 接入方案》11020742807 §5.5 五句引文（逐字复核准确）+ 🔴 引用限定（限自定义 HTTP 类型 Model API 链路，非 MCP；不可外推）⚠️ SSO 拦截，仅归档摘录 | https://ata.atatech.org/articles/11020742807 | raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md | knowledge/aliyun-products.md（引用限定 + 避坑「优先域名级」）
- [done] 2026-09-21 | ATA（未归档，登记限定） | 鹤渡/章丹鹰 11020591207（aigw 定位引文准确但无插件生效维度内容，`生效` 0 命中）；筱奥 11020729615《MCP Server 与 Client 之间的鉴权》（**内部 Aone MCP 网关 Normandy，非阿里云产品**，只可当模式参考） | https://ata.atatech.org/articles/11020591207 ；https://ata.atatech.org/articles/11020729615 | （SSO 拦截未归档，限定已写入 raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md 尾注） | knowledge/aliyun-products.md（引用限定节）
- [done] 2026-09-21 | 客户现场记录 | 合思信息（原易快报）：2026-09-16 现场会议（千问办公生态 MCP 上架诉求）+ 内部记录 2026-04-23（华为云 300 万+ 存量无搬迁计划）+ SA 归属链变更（罗勤/傲罗 2026-09-15 生效）+ S10 网关鉴权 case（A 路 404 → forward_auth 解法）⚠️ 敏感：token/PAT 与客户测试域名**不落盘**（脱敏红线），故不归档 raw | （内部记录，无公开 URL） | - | knowledge/company-profiles.md（合思画像）+ cloud-solutions.md（S10 实战案例）

## Processing（蒸馏中）

<!-- 正在分析的资料移到这里 -->

## Done（已落盘）

- [done] 2026-06-17 | meta | neil-aliyun-sa skill 骨架建立 | (无外部 URL) | SKILL.md / README.md / changelog.md / knowledge × 6 / references × 5
- [done] 2026-06-17 | 元方法论 | 修炼之路 11 天版 —— 自我演进知识库的协议设计原则（写入优先 / 跨源验证 / 知识与参考分离 / 6 种工作模式） | https://ata.atatech.org/articles/11020643601 | SKILL.md（六种模式 + 写入优先 + 跨源验证）+ README.md（设计说明）
