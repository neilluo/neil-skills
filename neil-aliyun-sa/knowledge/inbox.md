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

## Processing（蒸馏中）

<!-- 正在分析的资料移到这里 -->

## Done（已落盘）

- [done] 2026-06-17 | meta | neil-aliyun-sa skill 骨架建立 | (无外部 URL) | SKILL.md / README.md / changelog.md / knowledge × 6 / references × 5
- [done] 2026-06-17 | 元方法论 | 修炼之路 11 天版 —— 自我演进知识库的协议设计原则（写入优先 / 跨源验证 / 知识与参考分离 / 6 种工作模式） | https://ata.atatech.org/articles/11020643601 | SKILL.md（六种模式 + 写入优先 + 跨源验证）+ README.md（设计说明）
