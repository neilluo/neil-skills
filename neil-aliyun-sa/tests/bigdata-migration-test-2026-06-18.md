# 大数据迁云专项 Mock Test — 2026-06-18

> **测试人**：QoderWork（外部视角，模拟真实企业大数据迁云场景）
> **被测对象**：neil-aliyun-sa skill v0.4（完成 P0/P1 修复后）
> **覆盖**：Hadoop/Hive/Spark 迁移、Kafka 迁移、自建数仓→湖仓、Oracle 数据库迁云、大数据ETL平移、实时计算升级、HDFS→OSS、数据质量/治理迁移
> **测试时间**：2026-06-18 CST

---

## 测试矩阵

| # | 模式 | 场景 | 难度 | 知识库支撑度 | 结论 |
| --- | --- | --- | --- | --- | --- |
| BD01 | B | 自建 Hadoop/Hive 500 节点迁 MaxCompute+EMR | 高 | 78% | ⚠️ 骨架完整但迁移路径细节不足 |
| BD02 | C | HDFS 500TB 迁 OSS 选型 | 中 | 85% | ✅ 通过 |
| BD03 | B | 自建 Kafka 集群迁云 Kafka + Flink 实时链路 | 高 | 72% | ⚠️ Kafka 迁移路径缺失 |
| BD04 | F | 30 秒判断：EMR vs MaxCompute vs Hologres | 低 | 95% | ✅ 通过 |
| BD05 | B | Oracle 数仓 50TB 迁 MaxCompute | 高 | 65% | ⚠️ ADAM 工具链描述薄 |
| BD06 | B | CDH/HDP 集群 EOL 迁 EMR | 高 | 55% | ❌ CDH 专项迁移路径缺失 |
| BD07 | C | DataWorks vs 自建 Airflow/DolphinScheduler | 中 | 70% | ⚠️ 调度迁移方法论缺 |
| BD08 | B | 实时数仓升级：Spark Streaming→Flink+Paimon+Hologres | 中 | 88% | ✅ 通过 |

---

## BD01（模式 B — 方案设计）

**Query**：我们有一个自建 Hadoop 集群（CDH 6.3），500 个节点，Hive 数仓 2PB 数据，日增 5TB，每天跑 8000 个 Hive/Spark ETL Job。想迁到阿里云，给方案。

### 作答（基于知识库）

**整体迁移策略**（命中 migration-methodology.md 6R + 四阶段框架）：

- **迁移模式**：Replatform（R2）— Hive → MaxCompute（托管化替代）+ 部分 Spark 任务 → EMR Spark（开源兼容）
- **四阶段**：Assess 3-4 周 → Plan 4 周 → Migrate 12-16 周（分波次）→ Optimize 持续

**目标架构**：

```
数据源                  接入层              湖存储           计算层              服务层
─────────             ─────────          ────────         ────────           ────────
业务DB ──DTS/CDC──┐                    OSS(Paimon/      MaxCompute         Hologres
                  ├→ Flink CDC ──→    Iceberg格式)     (替代 Hive SQL)   (实时OLAP)
日志 ────SLS投递──┤                       │                │                  │
                  │                    DLF Catalog      EMR Spark          Quick BI
Kafka ────────────┘                  (元数据治理)      (保留 Spark 生态)   DataV
                                          │                │
                                    DataWorks          ─→  PAI(AI训练)
                                   (替代 Oozie/Azkaban)
```

**可复用知识**：
- ✅ S5 数据湖仓一体方案 — 产品组合、湖格式选型、成本对比
- ✅ EMR 产品卡 — EMR on ECS/ACK/Serverless Spark 全形态
- ✅ MaxCompute 产品卡 — CU 模式 vs 按量，150 CNY/CU/月
- ✅ DataWorks 产品卡 — DAG 调度 + 数据质量 + 血缘
- ✅ DLF Catalog — 统一元数据管理
- ✅ migration-methodology.md — 四阶段框架 + 6R 决策 + 波次规划
- ✅ 升级阈值表 — MaxCompute vs EMR 选型决策

**缺什么**：
- ❌ Hive→MaxCompute 的 SQL 兼容性差异清单（如 UDF 迁移、Hive 特有语法）
- ❌ HDFS→OSS-HDFS 的数据迁移具体方案（ossutil/DataX/jindo distcp vs hadoop distcp）
- ❌ Oozie/Azkaban→DataWorks 的 Job 迁移策略（ETL 改写工作量评估）
- ❌ 大规模 Hive 元数据迁移到 DLF 的步骤与工具
- ❌ 500 节点级别的分批次下线策略（节点缩容与云端扩容联动）
- ❌ CDH 授权 EOL 时间线与迁移紧迫度说明

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 架构方向 | ✅ | 目标架构清晰（MaxCompute+EMR+Flink+Hologres） |
| 产品选型 | ✅ | EMR vs MaxCompute 决策框架有 |
| 迁移路径 | ⚠️ | 通用四阶段有，缺大数据专项迁移细节 |
| BOM 估算 | ⚠️ | 有参考（S5 成本表），缺 PB 级具体估算 |
| 风险 | ✅ | migration-methodology 有风险清单 |

### 缺口

- ❌ **Hive SQL→MaxCompute SQL 兼容性迁移指南**（DDL/DML/UDF/类型映射差异）
- ❌ **HDFS→OSS-HDFS/JindoFS 迁移方案**（jindo distcp vs hadoop distcp vs DataX）
- ❌ **Hive MetaStore→DLF Catalog 迁移工具与步骤**
- ❌ **ETL 调度迁移**（Oozie/Azkaban/Airflow→DataWorks 的 Job 转换规则）
- ❌ **PB 级数据量的迁移时间估算公式**（带宽/并发/校验开销）
- ❌ **CDH/HDP EOL 时间线**与迁移窗口规划

---

## BD02（模式 C — 产品选型）

**Query**：我有 500TB HDFS 数据要迁到阿里云，用什么方式最快最稳？

### 作答（基于知识库）

> **迁移方案选型**（命中 migration-methodology.md 数据迁移工具链）：
>
> | 方案 | 适用 | 带宽需求 | 时间估算（500TB） | 成本 |
> | --- | --- | --- | --- | --- |
> | ossutil + 专线在线迁移 | <10TB or 有大带宽专线 | 10Gbps 专线 | ~5 天 | 专线费 + OSS 写入 |
> | OSS Migration Tool | 跨云（S3→OSS） | 公网/专线 | 视带宽 | 免费 + 带宽 |
> | 闪电立方（Data Transport） | >10TB + 带宽不足 | 无需网络传输 | 物理搬运 5-7 天 + 上传 | 设备租赁费 |
> | 闪电立方 + ossutil 增量补齐 | **500TB 推荐** | 专线做增量 | 全量搬运 + 增量在线 | 综合最优 |
>
> **推荐方案**：闪电立方全量（500TB，~5-7 天物理运输 + 2-3 天上传到 OSS）→ 专线 10Gbps 做增量追平 → 割接。
>
> **目标存储选型**：
> - OSS 标准存储（0.12 CNY/GB/月）→ 热数据
> - OSS-HDFS（JindoFS 兼容层）→ 如需保留 HDFS 语义（EMR Spark 直读）
> - 生命周期策略：30 天后低频（0.08）→ 90 天归档（0.033）

### 知识库命中分析

- `migration-methodology.md` 数据迁移工具链：✅ 闪电立方 / OSS Migration Tool / ossutil 都有
- `aliyun-products.md` OSS 产品卡：✅ 存储分层定价、生命周期策略
- EMR 产品卡：✅ OSS-HDFS 兼容说明
- 具体的 HDFS→OSS 的 distcp 命令与参数：❌ 缺

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 方案选型 | ✅ | 闪电立方 + 增量补齐方案清晰 |
| 时间估算 | ⚠️ | 有框架但缺精确公式 |
| 成本 | ⚠️ | OSS 存储成本有，闪电立方设备费缺具体数字 |
| 完整性 | ✅ | 工具链覆盖全 |

### 缺口

- ❌ **闪电立方具体定价**（设备租赁费、运输费、起步量）
- ❌ **HDFS→OSS distcp 具体参数与调优**（并发度/bandwidth限制/校验策略）
- ❌ **500TB 迁移时间精确估算公式**

---

## BD03（模式 B — 方案设计）

**Query**：自建 Kafka 集群（3 Broker，200 Topic，峰值 50 万 TPS 写入）+ 下游自建 Spark Streaming 实时消费，整体要迁到阿里云。方案？

### 作答（基于知识库）

> **Kafka 迁移**：
> - 目标产品：阿里云消息队列 Kafka（全托管）
> - 产品卡命中：✅ 百万级 TPS 吞吐，按 Topic + 吞吐计费
>
> **下游升级**：
> - Spark Streaming → Flink 全托管（命中 S5 实时引擎选型决策）
> - 理由：Flink 精确一次语义 + 亚秒级延迟 vs Spark Streaming 微批（秒级）
>
> **可拼出的骨架**：
> ```
> 数据源 → 阿里云 Kafka（同步迁移Topic）→ Flink CDC/SQL → Paimon/Hologres
> ```
>
> **缺什么关键迁移信息**：
> - ❌ Kafka 数据迁移方案（MirrorMaker 2 / Confluent Replicator / 阿里云 Kafka 迁移工具？）
> - ❌ Topic 元数据（分区数/副本/ACL/offset）如何平迁？
> - ❌ 消费端切换策略（双读 vs offset 迁移 vs 从 latest 消费？）
> - ❌ Kafka Connect connector 如何迁移到阿里云 Kafka Connect？
> - ❌ Spark Streaming→Flink 的任务改写指导（窗口/State/Checkpoint 映射）

### 知识库命中分析

- `aliyun-products.md` Kafka 产品卡：✅ 百万级 TPS、与 Flink 集成
- `aliyun-products.md` Flink 产品卡：✅ 全托管 + Connector 体系
- S5 关键决策点"实时引擎"：✅ Flink 全托管 vs 自建 Flink on EMR
- **Kafka 集群迁移具体方案**：❌ 完全缺失
- **Spark Streaming→Flink 改写指南**：❌ 缺失
- migration-methodology.md：⚠️ 仅覆盖"服务器/DB/对象"迁移，无消息队列迁移

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 目标架构 | ✅ | Kafka + Flink + Paimon + Hologres 清晰 |
| 迁移路径 | ❌ | Kafka→Kafka 迁移方法完全空白 |
| 改写指导 | ❌ | Spark Streaming→Flink 无对应内容 |
| 产品选型 | ✅ | 产品卡足够支撑 |

### 缺口

- ❌ **Kafka 集群迁云方案**（MirrorMaker 2 / 阿里云 Kafka 迁移服务 / Topic 平迁步骤）
- ❌ **消费端 offset 迁移策略**（双读期间如何保证不丢不重）
- ❌ **Spark Streaming→Flink 改写映射表**（DStream→DataStream、窗口→Flink Window、State→Flink State）
- ❌ migration-methodology.md 缺 "消息队列迁移" 专节

---

## BD04（模式 F — 30 秒判断）

**Query**：客户问"EMR、MaxCompute、Hologres 三个大数据产品到底怎么分？30 秒给我讲明白。"

### 作答（基于知识库）

> **30 秒结论**：
> - **MaxCompute** = 全托管离线数仓，SQL 为主，PB 级 T+1 批处理，最便宜（0.3 CNY/GB 按量或 150/CU/月）
> - **EMR** = 托管开源大数据集群（Spark/Hive/Flink/Presto/StarRocks），需要开源生态兼容性或 Python/Scala 自定义算法时选它
> - **Hologres** = 实时 OLAP，毫秒级交互查询，接实时大屏/BI/用户画像，每秒百万级写入
>
> **一句话**：T+1 离线跑 SQL → MaxCompute；需要开源/ML → EMR；实时查询/看板 → Hologres。三个经常并用。

### 知识库命中分析

- S5 产品定位决策表：✅ 完美命中
- MaxCompute/Hologres/EMR 产品卡：✅ 全部有
- 成本对比：✅ 有具体数字

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 速度 | ✅ | <30 秒可出 |
| 准确性 | ✅ | 定位清晰有据 |
| 完整性 | ✅ | 三者分工 + "并用"建议 |

### 缺口

- 无显著缺口 ✅

---

## BD05（模式 B — 方案设计）

**Query**：我们有一个 Oracle 数据仓库（50TB，3000+ 存储过程，大量 PL/SQL），要迁到阿里云。怎么搞？

### 作答（基于知识库）

> **迁移模式**：Replatform（R2）— Oracle DW → MaxCompute（全托管数仓）
>
> **工具链**（命中 migration-methodology.md）：
> - **ADAM**：Oracle/DB2 迁移评估 → 兼容性分析 + SQL 改写 + 性能对比
> - **DTS**：数据迁移
>
> **可给出的骨架**：
> ```
> Phase 1: ADAM 兼容性评估（3000+ PL/SQL → 识别改写量）
> Phase 2: MaxCompute UDF + DataWorks 调度 替代 PL/SQL 逻辑
> Phase 3: DTS 全量 + 增量迁移数据（50TB）
> Phase 4: 双跑验证 → 割接
> ```
>
> **缺什么**：
> - ❌ ADAM 具体评估报告样例（兼容性百分比、改写难度分级）
> - ❌ PL/SQL → MaxCompute SQL/UDF 的改写规则对照表
> - ❌ Oracle→MaxCompute 的类型映射（NUMBER/DATE/CLOB/RAW 等）
> - ❌ 存储过程迁移策略（哪些用 DataWorks 调度、哪些重写为 Spark/Python）
> - ❌ 50TB Oracle→MaxCompute 的数据通道选型（DTS 直连？DataX？Sqoop？OGG？）
> - ❌ Oracle RAC→MaxCompute 的性能对比基准

### 知识库命中分析

- migration-methodology.md 工具链表：✅ ADAM 有一行描述
- MaxCompute 产品卡：✅ 能力边界清晰
- DataWorks 产品卡：✅ 调度 + 治理
- **ADAM 详细使用流程**：❌ 仅一行工具描述，无操作指南
- **Oracle→MaxCompute 改写指导**：❌ 完全缺失
- **DataX/Sqoop 大数据迁移工具**：❌ 产品卡缺失

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 方向 | ✅ | ADAM+MaxCompute 方向正确 |
| 迁移路径 | ❌ | ADAM 操作/改写规则/数据通道全缺 |
| 工作量评估 | ❌ | 3000+ 存储过程改写量无法估算 |
| 风险 | ⚠️ | 通用风险清单有，Oracle 专项风险缺 |

### 缺口

- ❌ **ADAM 使用流程与评估报告解读**
- ❌ **Oracle SQL/PL/SQL → MaxCompute SQL 改写规则**
- ❌ **Oracle 数据类型→MaxCompute 类型映射表**
- ❌ **DataX 产品卡**（阿里开源全域数据同步工具，大数据场景高频使用）
- ❌ **Oracle→MaxCompute 数据通道选型对比**（DTS vs DataX vs OGG+Kafka vs Sqoop）

---

## BD06（模式 B — 方案设计）

**Query**：我们 CDH 6.3 集群授权明年到期，Cloudera 报价涨了 3 倍。要迁到阿里云 EMR，给个完整方案。

### 作答（基于知识库）

> **可给出的框架**：
> - 迁移模式：Replatform（R2）— CDH → EMR（保持开源生态，换底座）
> - EMR 支持：Hadoop/Spark/Flink/Hive/Presto/Trino/Hudi/Iceberg/Paimon/Doris/StarRocks
> - EMR 形态：EMR on ECS（传统集群）/ EMR on ACK（K8s 弹性）/ EMR Serverless Spark
>
> **四阶段框架可复用**：✅
>
> **关键缺失**：
> - ❌ CDH→EMR 组件版本对照（CDH Hadoop 3.x → EMR Hadoop 版本？CDH Spark 2.4 → EMR Spark 3.x？）
> - ❌ CDH 管理平台（Cloudera Manager）→ EMR 管控面的功能对照
> - ❌ CDH 安全（Kerberos/Ranger/Sentry）→ EMR 安全体系映射
> - ❌ CDH HDFS NN HA/Federation → EMR HDFS 或 OSS-HDFS 的迁移步骤
> - ❌ CDH Hive MetaStore → EMR HMS or DLF 的迁移
> - ❌ CDH Oozie → DataWorks 的 Job 迁移
> - ❌ CDH Impala → StarRocks/Trino on EMR 的性能对比
> - ❌ 迁移期间的双集群并行运行方案与成本控制

### 知识库命中分析

- EMR 产品卡：✅ 支持全开源栈
- migration-methodology.md：✅ 四阶段 + 6R + 波次规划
- S5 数据湖仓：✅ 目标架构参考
- **CDH→EMR 专项迁移**：❌ 完全空白
- **CDH 组件版本对照**：❌ 无
- **CDH 安全体系迁移**：❌ 无

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 方向 | ✅ | CDH→EMR 方向明确 |
| 迁移细节 | ❌ | CDH 专项内容为零 |
| 版本兼容 | ❌ | 组件版本映射完全缺失 |
| 安全迁移 | ❌ | Kerberos/Ranger 迁移无指导 |

### 缺口

- ❌ **CDH/HDP→EMR 专项迁移指南**（组件对照、版本映射、管控面对比）
- ❌ **CDH 安全体系→EMR 安全映射**（Kerberos/Ranger/Sentry→EMR LDAP/Ranger/RAM）
- ❌ **Cloudera Manager→EMR 管控面功能对照**
- ❌ **CDH Impala→StarRocks/Trino 性能对比与迁移**
- ❌ **CDH 集群规模→EMR 规格选型对照**（CDH 节点配置→EMR 节点类型推荐）

---

## BD07（模式 C — 产品选型）

**Query**：我们自建了 Airflow 做大数据调度，有 2000+ DAG。要不要换 DataWorks？区别在哪？怎么迁？

### 作答（基于知识库）

> **DataWorks 能力**（命中产品卡）：
> - DAG 调度 + 数据质量 + 血缘追踪 + 数据分级
> - 与 MaxCompute/Hologres/EMR/Flink 深度集成
> - 数据开发 IDE（SQL + Python + Shell）
>
> **vs Airflow 对比**（基于产品知识推断）：
>
> | 维度 | DataWorks | 自建 Airflow |
> | --- | --- | --- |
> | 运维 | 全托管 | 需运维（HA/DB后端/Worker扩容） |
> | 与阿里云集成 | 原生深度集成 | 需自建 Operator |
> | 数据治理 | 内置血缘/质量/分级 | 需额外工具（如 Great Expectations） |
> | 代码灵活度 | 较弱（模板化） | 强（纯 Python DAG） |
> | 生态 | 阿里云闭环 | 开放社区 |
>
> **迁移方案**：❌ 完全缺失
> - 不知道如何将 2000+ Airflow DAG 转为 DataWorks 节点
> - 不知道 Airflow 的 Variable/Connection/Hook → DataWorks 资源组/数据源映射
> - 不知道是否有自动化迁移工具

### 知识库命中分析

- DataWorks 产品卡：✅ 能力描述清晰
- S5 中的 DataWorks 定位：✅ "全流程调度治理"
- **DataWorks vs Airflow 详细对比**：❌ 仅能推断
- **Airflow→DataWorks 迁移方法**：❌ 完全空白
- **DolphinScheduler→DataWorks**：❌ 无

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 产品对比 | ⚠️ | DataWorks 能力有，Airflow 对位推断 |
| 迁移指导 | ❌ | 零内容 |
| 决策框架 | ⚠️ | 能给出"什么时候不该迁"（代码灵活度需求高 → 保留 Airflow） |

### 缺口

- ❌ **DataWorks vs Airflow/DolphinScheduler 详细对比表**（调度能力/权限/告警/API/扩展性）
- ❌ **Airflow DAG→DataWorks 节点 迁移策略**（自动化 vs 手动改写 vs 并行期）
- ❌ **大数据调度迁移通用方法论**（DAG 映射规则、依赖关系重建、变量/连接迁移）

---

## BD08（模式 B — 方案设计）

**Query**：我们现在用 Spark Streaming + Hive + MySQL 做准实时数仓（T+30min 延迟），想升级到真实时（秒级）。阿里云怎么做？

### 作答（基于知识库）

> **推荐架构**（直接命中 S5 实时路径）：
>
> ```
> MySQL → Flink CDC → Flink ETL(ODS→DWD→DWS) → Paimon(OSS)
>                                                     │
>                                             Hologres Dynamic Table
>                                             (自动同步 Paimon)
>                                                     │
>                                               Quick BI / App
> ```
>
> **端到端延迟**：数据变更 → 可查询 = **秒级**
>
> **关键选型**（命中 S5 决策点表）：
> - 实时引擎：Flink 全托管（免运维，精确一次）
> - 湖格式：Paimon（Flink 原生集成，流式 Upsert）
> - OLAP 服务层：Hologres（毫秒级交互查询，支持 Paimon Dynamic Table 自动同步）
> - 批处理兜底：MaxCompute（T+1 数据校正）
>
> **成本参考**（S5 成本表）：
> - 中型场景（100GB/天增量）：MC 100CU + Flink 20CU + Hologres 32CU + OSS 15TB ≈ 45,000/月
>
> **迁移路径**：
> 1. Spark Streaming 任务逐步改写为 Flink SQL/DataStream
> 2. Hive 表迁移到 Paimon 格式（Flink 一条 CTAS 语句）
> 3. MySQL 下游查询切 Hologres（延迟从分钟级 → 秒级）
> 4. 并行期双跑验证数据一致性

### 知识库命中分析

- S5 实时路径（Flink + Paimon + Hologres）：✅ 完全命中
- S5 关键决策点表：✅ 湖格式选型 Paimon vs Iceberg
- Flink 产品卡：✅ 全托管 + Connector
- Hologres 产品卡：✅ Dynamic Table
- 成本估算：✅ S5 有规模参考
- Spark Streaming→Flink 改写指导：❌ 缺

### 评分

| 维度 | 评分 | 说明 |
| --- | --- | --- |
| 目标架构 | ✅ | Flink+Paimon+Hologres 标准推荐 |
| 产品选型 | ✅ | 决策框架完整 |
| 迁移路径 | ⚠️ | 方向对，改写细节缺 |
| 成本 | ✅ | 有参考量级 |

### 缺口

- ❌ **Spark Streaming→Flink 改写指南**（窗口/State/Checkpoint 映射关系）
- ⚠️ Hive→Paimon 数据格式迁移的具体 CTAS 语句和注意事项

---

## 综合结论

### 通过维度 ✅

1. **产品定位（BD04）**：MaxCompute/EMR/Hologres 三者分工 30 秒清晰
2. **数据迁移工具链（BD02）**：闪电立方/OSS Migration Tool/DTS/SMC 覆盖全
3. **实时数仓升级（BD08）**：Flink+Paimon+Hologres 实时路径完整可用
4. **通用迁移方法论**：四阶段 + 6R + 波次规划 + 风险清单跨场景复用

### 严重缺口 ❌

| # | 缺口类别 | 影响场景 | 优先级 |
| --- | --- | --- | --- |
| 1 | CDH/HDP→EMR 专项迁移指南 | Hadoop 集群替代 | **P0** |
| 2 | Kafka 集群迁移方案（MirrorMaker/offset/双读） | 实时链路迁云 | **P0** |
| 3 | Hive SQL→MaxCompute SQL 兼容性与改写 | Hive 数仓迁移 | **P0** |
| 4 | Oracle→MaxCompute 改写规则 + ADAM 详解 | Oracle 数仓替代 | **P1** |
| 5 | ETL 调度迁移方法论（Airflow/Oozie→DataWorks） | 任务迁移 | **P1** |
| 6 | HDFS→OSS-HDFS/JindoFS 迁移实操 | 存储层迁移 | **P1** |
| 7 | Spark Streaming→Flink 改写映射 | 实时计算升级 | **P2** |
| 8 | DataX 产品卡 | 大数据同步高频工具 | **P2** |
| 9 | 闪电立方详细定价 | BOM 准确性 | **P2** |
| 10 | PB 级迁移时间估算公式 | 项目规划 | **P2** |

### 整体评估

| 指标 | 数值 |
| --- | --- |
| 平均支撑度 | **76.0%** |
| ✅ 通过（≥85%） | 3/8 |
| ⚠️ 部分通过（50-85%） | 4/8 |
| ❌ 未通过（<50%） | 1/8 |
| P0 缺口数 | 3 |
| P1 缺口数 | 3 |
| P2 缺口数 | 4 |

### 结论

**知识库在大数据领域的"产品选型+目标架构"能力已经很强（S5+产品卡+迁移方法论），但在"迁移专项路径"方面存在系统性空白。** 核心问题是：`migration-methodology.md` 只覆盖了"服务器/数据库/对象存储"三条通道，缺少"大数据平台迁移"这一专项通道（涉及 Hadoop 生态、Kafka 消息队列、ETL 调度三大子场景）。

### 演进建议

#### 短期 P0（ROI 最高，预计 4h）

| 任务 | 预期文件 | 工作量 |
| --- | --- | --- |
| 新增 `references/bigdata-migration.md` — 大数据平台专项迁移方法论 | 新文件 | 3h |
| - CDH/HDP→EMR 组件版本映射 + 安全迁移 + 管控面对照 | | |
| - Hive SQL→MaxCompute SQL 兼容性差异表（DDL/DML/UDF/类型） | | |
| - Kafka 集群迁移方案（MirrorMaker2 + offset + 双读策略） | | |
| DataX 产品卡追加到 `aliyun-products.md` | 增量 | 30min |

#### 中期 P1（3h）

| 任务 | 预期文件 |
| --- | --- |
| ADAM 详细使用指南 + Oracle→MaxCompute 改写规则 | bigdata-migration.md |
| ETL 调度迁移方法论（Oozie/Airflow/DolphinScheduler→DataWorks） | bigdata-migration.md |
| HDFS→OSS-HDFS (JindoFS) 迁移实操（jindo distcp 参数+调优） | bigdata-migration.md |

#### 长期 P2（持续）

| 任务 | 说明 |
| --- | --- |
| Spark Streaming→Flink 改写映射表 | API 级对照 |
| 闪电立方详细定价与 SLA | 补充到产品卡 |
| PB 级迁移时间估算公式 | 补充到 migration-methodology.md |
| 大数据迁移客户案例（如某银行 Hadoop→MaxCompute） | 增强说服力 |
