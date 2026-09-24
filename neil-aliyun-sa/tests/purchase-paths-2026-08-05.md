# Purchase Paths Sentinel — 2026-08-05

## 一、产品家族覆盖度

| 家族 | 状态 | 命中关键词 | 缺失关键词 |
|------|------|-----------|-----------|
| PolarDB MySQL 集群版 | ✅ | PolarDB MySQL 集群版, polardb-buy.aliyun.com | — |
| PolarDB MySQL Serverless | ✅ | PolarDB MySQL Serverless, 不支持转包月 | — |
| PolarDB-X | ✅ | PolarDB-X, drds_polarxpre_public_cn | — |
| RDS MySQL 高可用版 | ✅ | RDS MySQL 高可用版 | — |
| RDS MySQL Serverless | ✅ | RDS MySQL Serverless | — |
| RDS PostgreSQL Serverless | ✅ | RDS PostgreSQL Serverless | — |
| RDS SQL Server Serverless (已下线) | ✅ | RDS SQL Server Serverless, 已停售 | — |
| ADB MySQL 企业版 | ✅ | ADB MySQL 企业版, 节点 ≥ 3，步长 3 | — |
| ADB PostgreSQL 弹性模式 | ✅ | ADB PostgreSQL, GreenplumPre | — |
| MaxCompute | ✅ | MaxCompute, odpsplus | — |
| Hologres 计算组 | ✅ | Hologres 计算组, 网关 ≥ 2 | — |
| ClickHouse 企业版 | ✅ | ClickHouse 企业版, 0.49987 | — |
| ClickHouse 社区兼容版 | ✅ | ClickHouse 社区兼容版, clickhouse_pre_public_cn | — |
| Lindorm 宽表 | ✅ | Lindorm 宽表引擎, hitsdb_lindormnextpre_public_cn | — |
| Lindorm Serverless (无法新购) | ✅ | Lindorm Serverless, 无法新购 | — |
| EMR on ECS | ✅ | EMR on ECS, Master ≥ 3 | — |
| EMR Serverless Spark | ✅ | EMR Serverless Spark | — |
| EMR Serverless StarRocks | ✅ | EMR Serverless StarRocks | — |
| Flink 全托管 | ✅ | Flink 全托管, 管控资源固定 2 CU | — |
| Flink 作业级 Serverless (不存在) | ✅ | 作业级 Serverless | — |
| DataWorks Serverless 资源组 | ✅ | DataWorks Serverless 资源组 | — |
| Tair 内存型 | ✅ | Tair 内存型, kvstore_pretair_public_cn | — |
| Tair Serverless | ✅ | Tair Serverless | — |
| 百炼 Token Plan 个人版 | ✅ | 百炼 Token Plan 个人版 | — |
| 百炼 Token Plan 团队版 | ✅ | 百炼 Token Plan 团队版 | — |
| PAI-EAS 独享 | ✅ | PAI-EAS 独享, learn_EasDedicatedPrepay_public_cn | — |
| PAI-EAS Serverless (仅 SDWebUI) | ✅ | PAI-EAS Serverless, SDWebUI | — |
| PAI-DSW | ✅ | PAI-DSW | — |
| OSS 资源包 | ✅ | OSS, 存储包 | — |

**覆盖度**: 29/29 = 100.0%

## 二、清单结构完整性

| 结构关键词 | 状态 |
|-----------|------|
| 全域速查表 v2 | ✅ |
| 红色预警 | ✅ |
| 匿名核验的边界 | ✅ |
| 登录复验 | ✅ |
| C11 版本可售性时效 | ✅ |
| C12 Serverless 语义粒度 | ✅ |

**通过**: 6/6

## 三、4 字段完整性抽样

| 字段类别 | 关键词命中数 |
|---------|-------------|
| 购买路径 (commodityCode) | 2/2 ✅ |
| 最低起步约束 | 4/4 ✅ |
| 规格页可用性 | 5/5 ✅ |
| 采购流程兼容性 | 2/5 ✅ |

**通过**: 4/4

---

## 结论: ✅ PASS — 采购路径核验清单结构完整

**执行时机**: 每次修改 `references/pricing-verification-checklist.md` 或新增 DB/大数据/AI 产品家族后必跑；每月 Lint 时抽跑一次
