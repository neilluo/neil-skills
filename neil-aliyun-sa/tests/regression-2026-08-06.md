# 自动化回归报告 — 2026-08-06 09:32 

> **测试器**：scripts/run-regression.py
> **用例库**：tests/regression-cases.yaml (v1.3)
> **覆盖文件**：14 个 markdown / 共 231160 字符
> **PASS 阈值**：命中率 ≥ 85%

## 总览

- **整体命中率**：100.0%
- **PASS 数**：36/36
- **FAIL 数**：0/36

## 用例结果矩阵

| ID | 模式 | 场景 | 命中 / 总数 | 命中率 | 状态 |
| --- | --- | --- | --- | --- | --- |
| T01 | F | Tair vs 自建 Redis 30 秒判断 | 4/4 | 100% | ✅ PASS |
| T02 | C | Qwen-Plus vs Qwen-Turbo 选型 | 4/4 | 100% | ✅ PASS |
| T03 | C | 视频点播平台存储+分发选型 | 8/8 | 100% | ✅ PASS |
| T04 | B | 零售连锁全渠道数据中台 | 8/8 | 100% | ✅ PASS |
| T05 | B | SaaS 多租户架构 | 7/7 | 100% | ✅ PASS |
| T06 | E | 阿里云 vs 火山引擎 AI MaaS | 7/7 | 100% | ✅ PASS |
| T07 | D | 教育行业上云特征 | 6/6 | 100% | ✅ PASS |
| T08 | B | 车联网 5000 万设备接入 | 7/7 | 100% | ✅ PASS |
| T09 | C | MaxCompute vs EMR Spark 选型 | 5/5 | 100% | ✅ PASS |
| T10 | F | ALB vs MSE 网关 vs API Gateway | 5/5 | 100% | ✅ PASS |
| BD01 | B | 自建 Hadoop/Hive 500节点迁 MaxCompute+EMR | 7/7 | 100% | ✅ PASS |
| BD02 | C | HDFS 500TB 迁 OSS 选型 | 5/5 | 100% | ✅ PASS |
| BD03 | B | 自建 Kafka 迁云 + Flink 实时链路 | 5/5 | 100% | ✅ PASS |
| BD04 | F | 30秒 EMR vs MaxCompute vs Hologres | 6/6 | 100% | ✅ PASS |
| BD05 | B | Oracle 数仓 50TB 迁 MaxCompute | 5/5 | 100% | ✅ PASS |
| BD06 | B | CDH/HDP EOL 迁 EMR | 6/6 | 100% | ✅ PASS |
| BD07 | C | DataWorks vs Airflow/DolphinScheduler | 5/5 | 100% | ✅ PASS |
| BD08 | B | Spark Streaming→Flink+Paimon+Hologres 实时升级 | 6/6 | 100% | ✅ PASS |
| S01 | C | WAF 3.0 版本选型（基础/高级/企业/旗舰） | 6/6 | 100% | ✅ PASS |
| S02 | B | 企业安全合规方案（等保/DDoS/WAF/云安全中心） | 5/5 | 100% | ✅ PASS |
| LZ01 | B | Landing Zone 多账号管理架构 | 5/5 | 100% | ✅ PASS |
| MG01 | B | IDC 迁云 6R 决策 + 数据迁移工具链 | 5/5 | 100% | ✅ PASS |
| MG02 | C | 迁移方法论四阶段选型 | 5/5 | 100% | ✅ PASS |
| AI01 | B | 企业 AI Agent 平台方案（百炼+RAG+多Agent） | 6/6 | 100% | ✅ PASS |
| AI02 | C | AIGC 内容生产选型（万相/HappyHorse/CosyVoice） | 5/5 | 100% | ✅ PASS |
| AI03 | F | 百炼 vs PAI-EAS 成本交叉点 30秒判断 | 5/5 | 100% | ✅ PASS |
| PP01 | C | PolarDB 家族购买路径核验完整性 | 6/6 | 100% | ✅ PASS |
| PP02 | C | RDS 家族购买路径核验完整性 + Serverless 下线 | 6/6 | 100% | ✅ PASS |
| PP03 | C | ADB / MaxCompute / Hologres 购买路径核验 | 7/7 | 100% | ✅ PASS |
| PP04 | C | ClickHouse 双版本购买路径核验 | 6/6 | 100% | ✅ PASS |
| PP05 | C | Lindorm 购买路径 + Serverless 无法新购 | 6/6 | 100% | ✅ PASS |
| PP06 | C | EMR 家族购买路径核验 + HA Master 3 起步 | 6/6 | 100% | ✅ PASS |
| PP07 | C | Flink 全托管无作业级 Serverless | 5/5 | 100% | ✅ PASS |
| PP08 | C | DataWorks 资源组购买路径核验 | 5/5 | 100% | ✅ PASS |
| PP09 | C | Tair / OSS / PAI / 百炼 购买路径核验 | 6/6 | 100% | ✅ PASS |
| PP10 | C | 采购路径核验清单结构完整性（红色预警清单 + 匿名核验边界） | 9/9 | 100% | ✅ PASS |

## 详细命中明细

### T01 — Tair vs 自建 Redis 30 秒判断  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Tair` | ✅ |
| `持久内存` | ✅ |
| `ElastiCache` | ✅ |
| `三种形态` | ✅ |

### T02 — Qwen-Plus vs Qwen-Turbo 选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Qwen-Plus` | ✅ |
| `Qwen-Turbo` | ✅ |
| `百炼` | ✅ |
| `限流` | ✅ |

### T03 — 视频点播平台存储+分发选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `VoD` | ✅ |
| `视频点播` | ✅ |
| `MPS` | ✅ |
| `Live` | ✅ |
| `RTC` | ✅ |
| `S6` | ✅ |
| `DRM` | ✅ |
| `HLS` | ✅ |

### T04 — 零售连锁全渠道数据中台  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `零售` | ✅ |
| `全渠道` | ✅ |
| `S8` | ✅ |
| `Quick BI` | ✅ |
| `SAG` | ✅ |
| `CDP` | ✅ |
| `RFM` | ✅ |
| `门店` | ✅ |

### T05 — SaaS 多租户架构  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `SaaS` | ✅ |
| `多租户` | ✅ |
| `S9` | ✅ |
| `Serverless` | ✅ |
| `6R` | ✅ |
| `Rehost` | ✅ |
| `Shared-DB` | ✅ |

### T06 — 阿里云 vs 火山引擎 AI MaaS  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `火山引擎` | ✅ |
| `Coze` | ✅ |
| `扣子` | ✅ |
| `Doubao` | ✅ |
| `Ark` | ✅ |
| `百炼 Agent` | ✅ |
| `Winback` | ✅ |

### T07 — 教育行业上云特征  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `教育` | ✅ |
| `在线教育` | ✅ |
| `K12` | ✅ |
| `未成年人保护` | ✅ |
| `RTC` | ✅ |
| `口语评测` | ✅ |

### T08 — 车联网 5000 万设备接入  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `车联网` | ✅ |
| `IoT Platform` | ✅ |
| `S7` | ✅ |
| `MQTT` | ✅ |
| `Lindorm` | ✅ |
| `汽车数据安全` | ✅ |
| `T-Box` | ✅ |

### T09 — MaxCompute vs EMR Spark 选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `MaxCompute` | ✅ |
| `EMR` | ✅ |
| `Paimon` | ✅ |
| `Serverless Spark` | ✅ |
| `Hudi` | ✅ |

### T10 — ALB vs MSE 网关 vs API Gateway  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `API Gateway` | ✅ |
| `MSE` | ✅ |
| `ALB` | ✅ |
| `云原生网关` | ✅ |
| `API 网关` | ✅ |

### BD01 — 自建 Hadoop/Hive 500节点迁 MaxCompute+EMR  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `MaxCompute` | ✅ |
| `EMR` | ✅ |
| `DataWorks` | ✅ |
| `DLF` | ✅ |
| `6R` | ✅ |
| `Replatform` | ✅ |
| `波次` | ✅ |

### BD02 — HDFS 500TB 迁 OSS 选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `闪电立方` | ✅ |
| `ossutil` | ✅ |
| `OSS Migration` | ✅ |
| `生命周期` | ✅ |
| `OSS-HDFS` | ✅ |

### BD03 — 自建 Kafka 迁云 + Flink 实时链路  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Kafka` | ✅ |
| `Flink` | ✅ |
| `Paimon` | ✅ |
| `Hologres` | ✅ |
| `Connector` | ✅ |

### BD04 — 30秒 EMR vs MaxCompute vs Hologres  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `EMR` | ✅ |
| `MaxCompute` | ✅ |
| `Hologres` | ✅ |
| `离线` | ✅ |
| `实时` | ✅ |
| `开源` | ✅ |

### BD05 — Oracle 数仓 50TB 迁 MaxCompute  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Oracle` | ✅ |
| `ADAM` | ✅ |
| `MaxCompute` | ✅ |
| `DTS` | ✅ |
| `PL/SQL` | ✅ |

### BD06 — CDH/HDP EOL 迁 EMR  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `CDH` | ✅ |
| `EMR` | ✅ |
| `Hadoop` | ✅ |
| `Spark` | ✅ |
| `Hive` | ✅ |
| `StarRocks` | ✅ |

### BD07 — DataWorks vs Airflow/DolphinScheduler  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `DataWorks` | ✅ |
| `调度` | ✅ |
| `DAG` | ✅ |
| `血缘` | ✅ |
| `数据质量` | ✅ |

### BD08 — Spark Streaming→Flink+Paimon+Hologres 实时升级  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Flink CDC` | ✅ |
| `Paimon` | ✅ |
| `Hologres` | ✅ |
| `Dynamic Table` | ✅ |
| `ODS` | ✅ |
| `DWD` | ✅ |

### S01 — WAF 3.0 版本选型（基础/高级/企业/旗舰）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `WAF` | ✅ |
| `3,880` | ✅ |
| `9,800` | ✅ |
| `Bot` | ✅ |
| `QPS` | ✅ |
| `按量付费` | ✅ |

### S02 — 企业安全合规方案（等保/DDoS/WAF/云安全中心）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `WAF` | ✅ |
| `Anti-DDoS` | ✅ |
| `云安全中心` | ✅ |
| `等保` | ✅ |
| `纵深防御` | ✅ |

### LZ01 — Landing Zone 多账号管理架构  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Landing Zone` | ✅ |
| `CAF` | ✅ |
| `资源目录` | ✅ |
| `管理账号` | ✅ |
| `Control Policy` | ✅ |

### MG01 — IDC 迁云 6R 决策 + 数据迁移工具链  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `6R` | ✅ |
| `Rehost` | ✅ |
| `Replatform` | ✅ |
| `DTS` | ✅ |
| `闪电立方` | ✅ |

### MG02 — 迁移方法论四阶段选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Assess` | ✅ |
| `Plan` | ✅ |
| `Migrate` | ✅ |
| `Optimize` | ✅ |
| `TCO` | ✅ |

### AI01 — 企业 AI Agent 平台方案（百炼+RAG+多Agent）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `百炼` | ✅ |
| `Agent` | ✅ |
| `RAG` | ✅ |
| `MCP` | ✅ |
| `Multi-Agent` | ✅ |
| `Workflow` | ✅ |

### AI02 — AIGC 内容生产选型（万相/HappyHorse/CosyVoice）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `万相` | ✅ |
| `happyhorse` | ✅ |
| `CosyVoice` | ✅ |
| `文生图` | ✅ |
| `文生视频` | ✅ |

### AI03 — 百炼 vs PAI-EAS 成本交叉点 30秒判断  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `百炼` | ✅ |
| `PAI-EAS` | ✅ |
| `Token` | ✅ |
| `GPU` | ✅ |
| `私有部署` | ✅ |

### PP01 — PolarDB 家族购买路径核验完整性  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `PolarDB MySQL 集群版` | ✅ |
| `PolarDB MySQL Serverless` | ✅ |
| `PolarDB-X` | ✅ |
| `polardb-buy.aliyun.com` | ✅ |
| `drds_polarxpre_public_cn` | ✅ |
| `不支持转包月` | ✅ |

### PP02 — RDS 家族购买路径核验完整性 + Serverless 下线  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `RDS MySQL 高可用版` | ✅ |
| `RDS MySQL Serverless` | ✅ |
| `RDS PostgreSQL Serverless` | ✅ |
| `RDS SQL Server Serverless` | ✅ |
| `已停售` | ✅ |
| `无法转化为包年包月` | ✅ |

### PP03 — ADB / MaxCompute / Hologres 购买路径核验  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `ADB MySQL 企业版` | ✅ |
| `ADB PostgreSQL` | ✅ |
| `GreenplumPre` | ✅ |
| `MaxCompute` | ✅ |
| `odpsplus` | ✅ |
| `Hologres 计算组` | ✅ |
| `网关` | ✅ |

### PP04 — ClickHouse 双版本购买路径核验  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `ClickHouse 企业版` | ✅ |
| `ClickHouse 社区兼容版` | ✅ |
| `clickhouse_pre_public_cn` | ✅ |
| `clickhouse_go_public_cn` | ✅ |
| `无独立规格页` | ✅ |
| `0.49987` | ✅ |

### PP05 — Lindorm 购买路径 + Serverless 无法新购  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Lindorm 宽表引擎` | ✅ |
| `Lindorm 时序引擎` | ✅ |
| `hitsdb_lindormnextpre_public_cn` | ✅ |
| `无法新购` | ✅ |
| `4C16G` | ✅ |
| `≥ 3 节点` | ✅ |

### PP06 — EMR 家族购买路径核验 + HA Master 3 起步  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `EMR on ECS` | ✅ |
| `EMR Serverless Spark` | ✅ |
| `EMR Serverless StarRocks` | ✅ |
| `Master ≥ 3` | ✅ |
| `存算一体` | ✅ |
| `存算分离` | ✅ |

### PP07 — Flink 全托管无作业级 Serverless  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Flink 全托管` | ✅ |
| `管控资源固定 2 CU` | ✅ |
| `作业级 Serverless` | ✅ |
| `释放整个工作空间` | ✅ |
| `跨可用区` | ✅ |

### PP08 — DataWorks 资源组购买路径核验  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `DataWorks Serverless 资源组` | ✅ |
| `最低 2 CU` | ✅ |
| `包月不能转按量` | ✅ |
| `独享资源组` | ✅ |
| `不推荐` | ✅ |

### PP09 — Tair / OSS / PAI / 百炼 购买路径核验  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `kvstore_pretair_public_cn` | ✅ |
| `Tair Serverless` | ✅ |
| `learn_EasDedicatedPrepay_public_cn` | ✅ |
| `PAI-DSW` | ✅ |
| `百炼 Token Plan` | ✅ |
| `存储包` | ✅ |

### PP10 — 采购路径核验清单结构完整性（红色预警清单 + 匿名核验边界）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `红色预警` | ✅ |
| `采购走不通` | ✅ |
| `已下线` | ✅ |
| `无法新购` | ✅ |
| `不支持转包月` | ✅ |
| `匿名核验的边界` | ✅ |
| `登录复验` | ✅ |
| `C11 版本可售性时效` | ✅ |
| `C12 Serverless 语义粒度` | ✅ |

## 文件覆盖

| 文件 | 字符数 |
| --- | --- |
| `knowledge/aliyun-products.md` | 69,668 |
| `knowledge/cloud-solutions.md` | 40,054 |
| `knowledge/industry-landscape.md` | 14,480 |
| `knowledge/ai-trends.md` | 10,864 |
| `knowledge/competitor-cloud.md` | 18,893 |
| `knowledge/company-profiles.md` | 9,920 |
| `references/architecture-templates.md` | 9,458 |
| `references/migration-methodology.md` | 8,897 |
| `references/bigdata-migration.md` | 17,483 |
| `references/well-architected.md` | 3,597 |
| `references/caf-landing-zone.md` | 4,646 |
| `references/cloud-product-mapping.md` | 3,098 |
| `references/customer-playbook.md` | 1,931 |
| `references/pricing-verification-checklist.md` | 18,171 |
