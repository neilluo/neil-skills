# 自动化回归报告 — 2026-06-18 15:23 

> **测试器**：scripts/run-regression.py
> **用例库**：tests/regression-cases.yaml (v1.1)
> **覆盖文件**：13 个 markdown / 共 176249 字符
> **PASS 阈值**：命中率 ≥ 85%

## 总览

- **整体命中率**：100.0%
- **PASS 数**：18/18
- **FAIL 数**：0/18

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

## 文件覆盖

| 文件 | 字符数 |
| --- | --- |
| `knowledge/aliyun-products.md` | 41,683 |
| `knowledge/cloud-solutions.md` | 39,536 |
| `knowledge/industry-landscape.md` | 14,210 |
| `knowledge/ai-trends.md` | 6,313 |
| `knowledge/competitor-cloud.md` | 18,501 |
| `knowledge/company-profiles.md` | 6,896 |
| `references/architecture-templates.md` | 9,458 |
| `references/migration-methodology.md` | 8,897 |
| `references/bigdata-migration.md` | 17,483 |
| `references/well-architected.md` | 3,597 |
| `references/caf-landing-zone.md` | 4,646 |
| `references/cloud-product-mapping.md` | 3,098 |
| `references/customer-playbook.md` | 1,931 |
