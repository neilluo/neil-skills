# 大数据平台专项迁云方法论 — bigdata-migration.md

> **定位**：通用 `migration-methodology.md` 的大数据领域专项扩展。覆盖 Hadoop 生态（CDH/HDP）、Hive 数仓、Kafka 消息队列、Oracle 数仓、ETL 调度、HDFS 存储 6 大子场景的迁移路径与改写规则。
> **触发**：方案设计 / 客户评估涉及"自建大数据平台→阿里云"主题时引用此文档；与 `cloud-solutions.md` S5 数据湖仓一体方案配合使用。
> **证据等级**：[官方] help.aliyun.com + [实战-ATA 推断] + [推断]

---

## 0. 大数据迁云全景图

```
源端（自建/竞品云）              目标（阿里云）
─────────────────              ─────────────
Hadoop HDFS    ──[迁移层]──▶   OSS / OSS-HDFS（JindoFS）
Hive 数仓      ──[迁移层]──▶   MaxCompute / EMR Hive
Spark/MR       ──[迁移层]──▶   EMR Spark / MaxCompute Spark / Serverless Spark
Kafka          ──[迁移层]──▶   阿里云 Kafka / RocketMQ
Oozie/Airflow  ──[迁移层]──▶   DataWorks
HBase          ──[迁移层]──▶   Lindorm / Tablestore
Impala/Presto  ──[迁移层]──▶   StarRocks / Trino on EMR / Hologres
Oracle DW      ──[迁移层]──▶   MaxCompute（+ ADAM 评估）
HMS（Hive 元数据）─[迁移层]─▶   DLF Catalog
```

**通用四阶段（参考 migration-methodology.md）**：
- Phase 1 评估（Assess）2-4 周：摸资产、跑 ADAM、识别改写量
- Phase 2 规划（Plan）2-4 周：目标架构、波次、双跑策略
- Phase 3 执行（Migrate）8-20 周：分批数据迁移 + 任务改写
- Phase 4 优化（Optimize）持续：成本/性能/治理

---

## 1. CDH/HDP → 阿里云 EMR 专项迁移

> **背景**：Cloudera CDH 6.3 / CDP 7.x、Hortonworks HDP 已被 Cloudera 收购，授权费 2024 年起涨 2-3 倍，且 CDH 5/6 已 EOL。**典型客户痛点**：授权续费贵 + 国产化合规要求 + 集群规模到瓶颈。

### 1.1 组件版本映射对照

| CDH 6.3 组件 | 版本 | EMR 5.x（Hadoop 系） | EMR 数据湖（DataLake） | 备注 |
| --- | --- | --- | --- | --- |
| Hadoop（HDFS+YARN） | 3.0.0 | Hadoop 3.2.x | Hadoop 3.3.x | EMR 默认开启 OSS-HDFS 替代 HDFS |
| Hive | 2.1.1 | Hive 3.1.x | Hive 3.1.x + DLF | UDF 一般兼容；HiveServer2 端口/Thrift 不变 |
| Spark | 2.4.0 | Spark 3.3.x | Spark 3.5.x | Spark 2.x→3.x 需注意 Datetime/Decimal 行为变化 |
| HBase | 2.1.0 | HBase 2.4.x | 推荐迁 Lindorm | HBase 客户端兼容 |
| Impala | 3.2.0 | ❌ 不支持 | StarRocks / Trino | Impala SQL 90% 可改写为 StarRocks/Trino |
| Kafka | 2.2.1 | Kafka 2.8.x | 阿里云 Kafka 3.x | 协议兼容，客户端无需改 |
| Oozie | 5.1.0 | ❌ 不支持 | DataWorks | 任务必须重新建模 |
| Sqoop | 1.4.7 | Sqoop 1.4.7 | DataX/DTS | 推荐换 DataX |
| Sentry/Ranger | Sentry 2.1 | Ranger 2.x | Ranger 2.x + RAM | Sentry → Ranger 需重写策略 |
| Cloudera Manager | 6.3 | EMR 控制台 | EMR 控制台 + ECS 运维助手 | 监控指标全部对齐 |

### 1.2 安全体系迁移

| CDH 安全 | EMR 对位 | 迁移动作 |
| --- | --- | --- |
| Kerberos KDC | EMR Kerberos（可选）+ RAM | 推荐**关闭 Kerberos**，改 RAM + Ranger；如必须保留 KDC，EMR 支持 |
| Sentry（已 EOL） | Ranger 2.x | Sentry 策略导出（CSV）→ Ranger Policy Import 工具 |
| HDFS ACL | OSS Bucket Policy + JindoFS ACL | 重新设计权限模型（按命名空间/Schema/Table） |
| LDAP/AD 集成 | RAM SSO + LDAP 同步 | 通过 IDaaS 单点登录对接 |
| 数据脱敏（HiveCBO） | DLF + DataWorks 数据分级 | 列级脱敏策略移植 |

### 1.3 管控面对照

| Cloudera Manager 功能 | EMR 对应 | 缺口 |
| --- | --- | --- |
| 集群部署/扩缩容 | EMR 控制台 + OpenAPI | ✅ 持平 |
| 服务启停/配置变更 | EMR 控制台一键变更 | ✅ 持平 |
| 主机/服务监控 | CloudMonitor + ARMS Prometheus | ✅ 更强 |
| 报警 | CloudMonitor 报警规则 | ✅ 持平 |
| 滚动升级 | EMR 滚动升级 | ✅ 持平 |
| 自定义 Parcel | ❌ 不支持 | 需改用 EMR 软件配置 + bootstrap action |
| Cloudera Backup | OSS 跨区域复制 + DLF 元数据备份 | 需重新设计备份策略 |

### 1.4 CDH→EMR 6 周迁移波次模板

```
Week 1-2  Assess: ADAM 兼容性扫描 + 资产清单 + ROI 估算
Week 3-4  Plan:   目标 EMR 集群规格选型 + 网络/安全设计 + 双跑预算
Week 5    Wave 0: 试点（1 个开发库 + 50 个 Hive 任务）端到端验证
Week 6    Wave 1: 元数据迁移（HMS → DLF）+ ETL 改写并行
Week 7-8  Wave 2: 数据迁移（HDFS → OSS-HDFS，jindo distcp）
Week 9-10 Wave 3: 任务切流（DataWorks 双跑 7 天）
Week 11   割接 + 业务验证 + Sentry/Ranger 策略验收
Week 12   CDH 集群下线 + 成本结算
```

### 1.5 Impala → StarRocks / Trino 选型

| 维度 | StarRocks（推荐） | Trino on EMR |
| --- | --- | --- |
| 性能 | TPC-DS 比 Impala 快 1.5-3x | 与 Impala 相当 |
| 数据存储 | 自带列存（MV、物化视图） | 直读外部表（Hive/Iceberg/Hudi） |
| 部署 | EMR StarRocks 形态 | EMR Trino 集群 |
| 适用 | 需高性能 OLAP + 内表加速 | 多源联邦查询 |
| Impala SQL 兼容 | 90% 改写量小 | 95% 几乎无改 |

---

## 2. Hive SQL → MaxCompute SQL 兼容性与改写

> **背景**：MaxCompute 兼容 Hive SQL ~80%。剩余 20% 需要改写。一份大型数仓（5000+ Hive 脚本）通常需要 1-2 个 SA + 2-3 个开发同学协作 6-12 周完成全量改写与验证。

### 2.1 类型映射表

| Hive 类型 | MaxCompute 2.0 类型 | 注意事项 |
| --- | --- | --- |
| TINYINT/SMALLINT/INT/BIGINT | TINYINT/SMALLINT/INT/BIGINT | ✅ 完全一致 |
| FLOAT/DOUBLE | FLOAT/DOUBLE | ✅ |
| DECIMAL(p,s) | DECIMAL(p,s) | ⚠️ 默认 38,18；MC 2.0 才完全等价 |
| STRING/VARCHAR/CHAR | STRING/VARCHAR/CHAR | ✅ |
| BOOLEAN | BOOLEAN | ✅ |
| DATE/TIMESTAMP | DATE/TIMESTAMP/DATETIME | ⚠️ MC TIMESTAMP 精度纳秒；DATETIME 毫秒 |
| BINARY | BINARY | ✅ MC 2.0 支持 |
| ARRAY/MAP/STRUCT | ARRAY/MAP/STRUCT | ✅ |
| INTERVAL | INTERVAL_DAY_TIME / INTERVAL_YEAR_MONTH | ✅ |
| UNIONTYPE | ❌ 不支持 | 需拆为多列 |

### 2.2 DDL 差异

| Hive | MaxCompute | 改写规则 |
| --- | --- | --- |
| `CREATE TABLE ... STORED AS ORC/PARQUET` | `CREATE TABLE ... ` (默认 AliORC) | 移除 STORED AS，使用默认存储 |
| `LOCATION 'hdfs://...'` | 不支持任意 LOCATION | 外部表用 OSS 路径，普通表内部存储 |
| `PARTITIONED BY (...)` | `PARTITIONED BY (...)` | ✅ 一致 |
| `CLUSTERED BY ... INTO N BUCKETS` | ❌ 不支持 Hash Bucket | 改用 CLUSTERED BY HASH/RANGE |
| `TBLPROPERTIES (...)` | `LIFECYCLE N` | 用 LIFECYCLE 控制生命周期 |
| 动态分区写入参数 | `odps.sql.allow.fullscan=true` 等 | 改 SET 命令 |

### 2.3 DML / 函数差异（高频踩坑）

| Hive 写法 | MaxCompute 写法 | 说明 |
| --- | --- | --- |
| `SELECT * FROM t WHERE rand()<0.1` | `SAMPLE(...)` 函数 | rand() 行为有差异 |
| `LATERAL VIEW EXPLODE(...)` | `LATERAL VIEW EXPLODE(...)` | ✅ 一致 |
| `STR_TO_MAP / GET_JSON_OBJECT` | `JSON_TUPLE` / `GET_JSON_OBJECT` | 90% 兼容 |
| `DATE_SUB/DATE_ADD` | `DATEADD` (新)，DATE_SUB 也支持 | 新代码推荐 DATEADD |
| `REGEXP_EXTRACT / REGEXP_REPLACE` | 同名函数 | ✅ 一致 |
| `INSERT OVERWRITE LOCAL DIRECTORY` | ❌ 不支持本地输出 | 改 INSERT INTO + UNLOAD 到 OSS |
| `LOAD DATA INPATH ...` | `TUNNEL UPLOAD` 命令行 | 改用 MC Tunnel |
| Hive UDF（Java JAR） | MC Java UDF | 重打包，改继承类（UDF/UDAF/UDTF） |
| Hive Python UDF（streaming） | MC Python 3 UDF | 需重写为 PyODPS 标准 |

### 2.4 自动化改写工具链

| 工具 | 用途 | 推荐度 |
| --- | --- | --- |
| **MMA**（MaxCompute Migration Assistant，官方） | 一键迁移 Hive Schema + 数据 + 部分 SQL 改写 | ★★★★★ 首选 |
| ADAM（数仓兼容性评估） | Oracle/Teradata 优先；Hive 也支持评估 | ★★★ |
| 人工改写 + DataWorks 内置编辑器 | 复杂 UDF/PL-Hive | ★★★★ 兜底 |

**MMA 三步走**：
1. **Schema 迁移**：自动建 MaxCompute 表（含 DDL 转换）
2. **数据迁移**：底层走 OSS 中转（自动 distcp + tunnel upload）
3. **任务校验**：Hive vs MC 双跑结果对比（行数 + 抽样列）

### 2.5 PL-Hive / PL-SQL 类逻辑改写

Hive HPL/SQL（变量 / 流程控制 / 游标）和 Oracle PL/SQL 在 MaxCompute 的对应：

| 源端 | MaxCompute 对应 | 备注 |
| --- | --- | --- |
| Hive 变量 `${hivevar:x}` | MC 参数 `${x}` + DataWorks 调度参数 | 直接替换 |
| Hive `IF / WHILE / FOR` | MC SCRIPT 模式 + IF/WHILE | MC 2.0 SCRIPT 支持 |
| 存储过程 | DataWorks ODPS Script 节点 + Shell/Python 节点 | 拆分为 DAG |
| 游标遍历 | 改写为集合 SQL（推荐） | 性能提升 10-100x |
| Oracle PL/SQL（DECLARE/BEGIN/END） | MC SCRIPT + UDF 兜底 | 需人工评估 |

---

## 3. Kafka 集群迁云方案

> **背景**：自建 Apache Kafka / Confluent Kafka → 阿里云 Kafka 全托管。核心挑战：**Topic 元数据平迁、消费 offset 衔接、双读期保不丢不重、客户端零改动**。

### 3.1 三种迁移模式对比

| 模式 | 工具 | 停机 | 双跑成本 | 适用 |
| --- | --- | --- | --- | --- |
| **A. MirrorMaker 2（MM2）镜像同步** | Kafka 自带 | 零停机 | 高（双集群+双倍带宽） | 主流推荐 |
| **B. 阿里云 Kafka 数据迁移工具** | 控制台 → Connector | 零停机 | 中 | 仅适合阿里云内部跨实例 |
| **C. 应用层双写双读** | 业务改造 | 零停机 | 高（业务改造） | 业务可改造 + 短迁移期 |

### 3.2 MirrorMaker 2 标准流程（推荐）

```
源 Kafka(自建)                         阿里云 Kafka
   │                                       │
   ├── Topic A,B,C   ──[MM2 同步]──▶   Topic A,B,C
   │                                       │
   ├── Producer (在源端写)                 ├── Consumer 阶段1（仅读源端）
   │                                       │
   │            （切流时刻 T0）            │
   │                                       │
   ├── Producer 切到目标端写  ─────────▶  写阿里云 Kafka
   │                                       │
   └── Consumer 阶段2（切到读阿里云）────▶ 消费目标端

关键里程碑：
T-30 天：搭建 MM2 集群（推荐 EMR/独立 ECS），开始同步全量+增量
T-7 天 ：监控 MM2 lag <1000 条且持续稳定
T-1 天 ：演练割接（含回滚）
T0     ：源端 Producer 停写 → 等 MM2 lag=0 → 阿里云 Producer 开写
T+1 小时：Consumer 切流（消费组 offset 由 MM2 翻译同步）
T+7 天 ：观察期，源集群保留只读
T+14 天：源集群下线
```

**MM2 关键参数**：
- `replication.factor=3`（目标端副本）
- `sync.topic.acls.enabled=true`（同步 ACL）
- `sync.topic.configs.enabled=true`（同步配置）
- `consumer.group.offsets.sync.enabled=true`（同步消费组 offset）

### 3.3 Topic 元数据平迁清单

| 元数据项 | MM2 自动同步 | 需手动确认 |
| --- | --- | --- |
| Topic 名 / 分区数 | ✅ | ⚠️ 阿里云 Kafka 分区上限：专业版 1000 |
| 副本数 | ✅（按 replication.factor 配置） | |
| 配置（retention/segment.bytes 等） | ✅ | |
| ACL | ✅（需开启 sync.topic.acls） | 阿里云 Kafka ACL 模型差异 |
| 消费组 offset | ✅（按 RemoteClusterUtils 翻译） | 切流后验证 lag |
| Schema Registry（如使用） | ❌ | 阿里云 Kafka Schema Registry 单独迁 |
| Kafka Connect 任务 | ❌ | 在阿里云重建 Connector |

### 3.4 客户端改造点

| 客户端项 | 是否需改 | 说明 |
| --- | --- | --- |
| bootstrap.servers | ✅ | 改成阿里云 Kafka VPC 端点 |
| 协议（PLAINTEXT/SASL_SSL） | 视配置而定 | 阿里云 Kafka 默认 SASL_PLAIN/SSL |
| client.id / group.id | ❌ | 保持不变 |
| 序列化器（Avro/JSON/Protobuf） | ❌ | 兼容 |
| Kafka 客户端版本 | ⚠️ | 推荐 ≥2.4，避免老客户端协议问题 |

### 3.5 Spark Streaming → Flink 改写映射

> 同步迁移消息系统时，下游实时计算建议从 Spark Streaming 升级到 Flink（精确一次 + 亚秒级）。

| Spark Streaming | Flink | 备注 |
| --- | --- | --- |
| `KafkaUtils.createDirectStream` | `KafkaSource.builder()` | DataStream API |
| DStream `.map / .filter` | DataStream `.map / .filter` | 语义一致 |
| `reduceByKeyAndWindow` | `keyBy().window().reduce()` | 窗口语义更细 |
| 微批触发（batch interval） | 真流式（默认） | 延迟从秒级 → 毫秒级 |
| `updateStateByKey` | `KeyedProcessFunction + ValueState` | State 管理更强 |
| Checkpoint to HDFS | Checkpoint to OSS | 改 state.backend 配置 |
| 重启恢复（spark.streaming.recover） | Savepoint / Retained Checkpoint | 显式指定 |

---

## 4. HDFS → OSS-HDFS / JindoFS 迁移实操

### 4.1 工具选型矩阵

| 数据规模 | 带宽情况 | 推荐方案 | 时间估算（500TB） |
| --- | --- | --- | --- |
| < 10TB | 公网/百兆 | ossutil + ossimport | 视带宽，~3-7 天 |
| 10-100TB | 千兆专线 | jindo distcp（在线） | ~3-5 天 |
| 100TB-1PB | 万兆专线 | jindo distcp + 闪电立方混合 | ~5-10 天 |
| > 1PB | 任何 | **闪电立方**离线 + 增量在线 | 物理运输 7-14 天 + 增量 |

### 4.2 jindo distcp 推荐参数

```bash
hadoop jar jindo-distcp-tool-x.x.x.jar \
  --src hdfs://nameservice1/warehouse/ \
  --dest oss://bucket/warehouse/ \
  --parallelism 200 \
  --bandwidth 800 \
  --enableTransaction \
  --enableCMS \
  --diff \
  --policy update
```

- `parallelism`：并发数（建议 200-500，看集群 CPU）
- `bandwidth`：单 mapper 带宽限制（MB/s），防把专线打满
- `enableTransaction`：保证最终一致
- `--diff`：增量同步（仅传变更）
- 校验：自动 CRC + 抽样 MD5

### 4.3 OSS-HDFS vs JindoFS vs OSS 标准

| 形态 | HDFS 语义 | 性能 | 成本 | 推荐场景 |
| --- | --- | --- | --- | --- |
| **OSS-HDFS（公测/正式）** | 完整支持 rename/append/dir | 接近 HDFS | OSS 成本 + 少量管理费 | EMR 集群最佳搭档 |
| **JindoFS（缓存层）** | HDFS 兼容 + 本地缓存 | 比直读 OSS 快 2-5x | 缓存盘成本 | EMR 计算节点本地加速 |
| **OSS 标准** | 弱 rename（O(N)） | 一般 | 最低 | 冷数据 / 归档 |

**强烈推荐**：EMR + OSS-HDFS + JindoFS 缓存三件套，是 CDH HDFS 的最佳替代。

### 4.4 Hive MetaStore（HMS）→ DLF Catalog 迁移

```
源 HMS（MySQL）   ──[ MMA / 自定义脚本 ]──▶   DLF Catalog
   │                                             │
   ├── DB / Table / Partition 元数据          ├── 同结构存入 DLF
   ├── LOCATION（HDFS 路径）                  ├── LOCATION 改写为 OSS 路径
   └── SerDe / 表属性                         └── 兼容映射（90%+）
```

**步骤**：
1. 导出 HMS：`mysqldump hive_metastore` 或用 MMA 拉取
2. LOCATION 路径批量替换：`hdfs://nameservice1/warehouse/db1/t1` → `oss://bucket/warehouse/db1/t1`
3. 通过 MMA 或 DataWorks 元数据迁移工具批量导入 DLF
4. 验证：在 EMR/MaxCompute/Hologres 中跨引擎读同一张表，确认 Catalog 共享

---

## 5. Oracle 数仓 → MaxCompute（含 PL/SQL 改写）

### 5.1 ADAM 评估流程

> ADAM = **Advanced Database & Application Migration**，阿里云官方的异构数据库迁移评估工具。

```
Phase 1：采集    ADAM Agent 抓取 Oracle 元数据 + SQL 样本（30 天）
Phase 2：评估    生成评估报告（兼容性 / 工作量 / 风险）
Phase 3：转换    自动改写工具改 90% 标准 SQL，剩余人工
Phase 4：验证    双跑 + 数据校验（MD5 + 行数 + 业务指标）
```

**ADAM 兼容性输出（典型 Oracle→MC）**：
- DDL 兼容：85-95%
- 标准 SQL（SELECT/INSERT）：80-90%
- PL/SQL 存储过程：30-50%（需人工改写）
- 系统函数：70-85%

### 5.2 Oracle 类型 → MaxCompute 类型映射

| Oracle | MaxCompute 2.0 | 备注 |
| --- | --- | --- |
| NUMBER(p,s) | DECIMAL(p,s) | s 默认 0；p>38 需拆分 |
| NUMBER（无精度） | DOUBLE | 精度损失风险，需评估 |
| VARCHAR2(n) | STRING / VARCHAR(n) | STRING 无长度限制 |
| CHAR(n) | CHAR(n) | ✅ |
| DATE | DATETIME | Oracle DATE 含时分秒 |
| TIMESTAMP(n) | TIMESTAMP | 纳秒精度 |
| CLOB / NCLOB | STRING（≤8MB） | 大于 8MB 需拆分 / 转 OSS |
| BLOB / RAW | BINARY | 大对象建议存 OSS + 路径 |
| ROWID | ❌ 不支持 | 用业务主键替代 |
| LONG / LONG RAW | STRING / BINARY | 已在 Oracle 弃用 |

### 5.3 PL/SQL → MaxCompute SCRIPT + UDF 改写规则

| Oracle PL/SQL | MaxCompute 等价 | 改写难度 |
| --- | --- | --- |
| `DECLARE ... BEGIN ... END;` 匿名块 | MC SCRIPT 模式 | 易 |
| 流程控制（IF/LOOP/WHILE/FOR） | MC SCRIPT 流程控制 | 易 |
| 变量声明 | MC SCRIPT 变量 / DataWorks 参数 | 易 |
| 游标（CURSOR） | **集合 SQL 改写**（首选） | 中 |
| 存储过程 / 函数 | DataWorks 节点（ODPS Script + Shell + Python） | 中 |
| 包（PACKAGE） | DataWorks 业务流程 + 命名规范 | 中 |
| 异常（EXCEPTION） | MC SCRIPT TRY/CATCH（部分支持）+ DataWorks 失败重试 | 中 |
| 触发器（TRIGGER） | ❌ 不支持 | 改业务侧或 DTS 同步 + Flink CDC |
| 物化视图（MView） | MC 物化视图 + DataWorks 调度刷新 | 中 |
| Merge Statement | MC 支持 MERGE INTO（2.0+） | 易 |
| 系统函数（NVL/DECODE/SUBSTR） | MC 同名函数全部支持 | 易 |
| 序列（SEQUENCE） | ❌ 不支持，用 ROW_NUMBER() OVER() | 易 |
| 分析函数（ROW_NUMBER/LAG/LEAD） | MC 完全支持 | 易 |
| 自定义函数（FUNCTION） | MC Java/Python UDF | 中 |
| Oracle Hint | ❌ 不支持，MC 自动优化 | 易（删除即可） |
| 分区交换 | MC 分区自动管理 + ALTER TABLE | 易 |

**改写工作量估算公式（推断）**：
```
工作量（人天） = 标准 SQL 数 × 0.05
              + 简单 PL/SQL 过程数 × 0.5
              + 复杂 PL/SQL 过程数 × 2-5
              + UDF 数 × 1
              + 集成测试 × 总过程数 × 0.2
```

### 5.4 数据通道选型（Oracle → MaxCompute）

| 工具 | 适用 | 吞吐 | 增量支持 | 推荐度 |
| --- | --- | --- | --- | --- |
| **DTS Oracle → MaxCompute** | 主流方案 | 50-200 MB/s | ✅ Redo log 解析 | ★★★★★ |
| **DataX Oracle Reader → ODPS Writer** | 全量批迁 | 100+ MB/s | ❌ 仅全量 | ★★★★ |
| **OGG → Kafka → Flink → MaxCompute** | 大型实时迁移 | 500+ MB/s | ✅ | ★★★★ 大客户 |
| **导出 CSV → OSS → MC Tunnel** | 离线小数据 | 视网络 | ❌ | ★★ 兜底 |

---

## 6. ETL 调度迁移（Airflow / Oozie / DolphinScheduler → DataWorks）

### 6.1 调度产品对比

| 维度 | DataWorks | Airflow | Oozie | DolphinScheduler |
| --- | --- | --- | --- | --- |
| 部署 | 全托管（按 DPU 计费） | 自建 | 自建 + Hadoop 绑定 | 自建 |
| 调度模型 | DAG + 业务流程 + 节点 | DAG（Python） | XML Workflow | DAG（拖拽） |
| 数据治理 | ✅ 血缘 / 质量 / 分级 | ❌（需 OpenLineage） | ❌ | 部分 |
| 阿里云产品集成 | ✅ 原生（MC/Flink/EMR/Hologres） | 需自建 Operator | ❌ | 需 Hook |
| 权限 | RAM + 项目空间 | RBAC | LDAP/Kerberos | LDAP |
| 报警 | 钉钉/邮件/Webhook | 邮件/Slack/自定义 | 邮件 | 邮件/钉钉 |
| 代码灵活度 | 中（节点 + Python 脚本） | **高（纯 Python DAG）** | 低 | 中 |
| 大规模 DAG | 5万+ 任务/天 | 集群可扩展 | 视集群 | 集群可扩展 |

### 6.2 迁移策略（按调度类型）

| 源端 | 推荐迁移方式 | 自动化程度 |
| --- | --- | --- |
| **Oozie**（XML Workflow） | DataWorks 业务流程一对一映射 + 自定义工具批量转换 | 高（结构简单） |
| **Airflow** | 按业务模块切片人工改写 + 保留 Airflow 作为复杂 Python 任务的过渡 | 中 |
| **DolphinScheduler** | DataWorks DAG 直接导入（部分版本支持 JSON 互转） | 中-高 |
| **Crontab + Shell** | DataWorks Shell 节点 + 调度规则 | 高 |
| **企业自研调度** | 中间表过渡（先 export 任务列表 + 依赖关系，再批量建 DataWorks 节点） | 视格式 |

### 6.3 Airflow → DataWorks 映射对照

| Airflow 概念 | DataWorks 对应 | 改造点 |
| --- | --- | --- |
| DAG | 业务流程 | 一个 DAG = 一个业务流程 |
| Task | 节点（ODPS SQL / Shell / Python / Spark） | 按算子类型选节点 |
| Operator | 节点类型 | 自定义 Operator 改 PyODPS / Shell |
| BashOperator | Shell 节点 | 一对一 |
| PythonOperator | PyODPS / Python 资源 | 上传依赖包 |
| SparkSubmitOperator | EMR Spark 节点 / MC Spark | 改任务提交方式 |
| Sensor（如 ExternalTaskSensor） | 跨流程依赖 / 触发器 | 用依赖配置替代 |
| Variable / Connection | 调度参数 / 数据源管理 | 集中迁移到 DataWorks |
| Schedule (cron) | 调度配置 | 一对一 |
| XCom（任务间传值） | 节点上下文 / 临时表 | 结构调整 |
| SubDag / TaskGroup | 业务流程嵌套 | 改子流程 |
| Hook | 数据源 / API 调用节点 | 重写 |
| 失败重试策略 | 节点重试配置 | 一对一 |

### 6.4 调度迁移 Checklist

- [ ] 资产盘点：DAG 数 / Task 数 / 自定义 Operator 数 / 外部依赖数
- [ ] 依赖识别：跨 DAG 依赖 / 跨系统依赖 / 数据时效要求
- [ ] 双跑设计：源端继续跑（输出对账表） + 目标端并行跑（输出对账表） + 自动 diff
- [ ] 调度参数迁移：变量 / 密钥 / 数据源连接全部 RAM 化
- [ ] 报警链路：钉钉机器人 / 值班链路 / SLA 配置同步
- [ ] 灰度策略：先迁低优先级 DAG（报表），再迁高优先级（业务核心）
- [ ] 业务停跑窗口：双跑期至少 7 天且数据完全一致

---

## 7. HBase → Lindorm 迁移（补充）

| 维度 | HBase（自建） | Lindorm |
| --- | --- | --- |
| API 兼容 | 100% HBase API | 100% HBase 1.x/2.x API + 增强 |
| 性能 | 基线 | 单机性能 2-5x 提升 |
| 多模 | 仅宽表 | 宽表 + 时序 + 搜索 + 文件 + 向量 |
| 工具 | LTS（Lindorm 数据传输服务） | LTS 支持全量+增量 |
| 迁移流程 | LTS 配置 → 全量 → 增量 → 双读 → 切流 | 标准化流程，~2 周 |

---

## 8. 大数据迁移项目模板（可直接套用）

### 8.1 阶段时长基线

| 集群规模 | 评估 | 规划 | 执行 | 优化 | 总周期 |
| --- | --- | --- | --- | --- | --- |
| 50 节点 / 100TB | 2 周 | 2 周 | 6-8 周 | 持续 | 3 个月 |
| 200 节点 / 1PB | 3 周 | 3 周 | 12-16 周 | 持续 | 5-6 个月 |
| 500 节点 / 5PB | 4 周 | 4 周 | 20-24 周 | 持续 | 8-10 个月 |

### 8.2 关键 KPI

- **数据一致性**：源 vs 目标 行数 100% 匹配；金额/状态字段抽样 MD5 100% 匹配
- **任务一致性**：双跑期任务结果 diff = 0（数值/记录数）
- **性能指标**：目标端任务执行时长 ≤ 源端 1.1x（允许 10% 波动）
- **成本指标**：上云后 12 个月 TCO ≤ 自建 0.7x（典型 30% 节省）
- **稳定性**：上云后首月任务成功率 ≥ 99.5%

### 8.3 高频踩坑（实战提醒）

1. **Hive UDF jar 不兼容** — Hive 2.x UDF 在 MC 需重打包，继承类不同（`UDF` → `com.aliyun.odps.udf.UDF`）
2. **HDFS 小文件问题** — 直接 distcp 到 OSS 后 Hive/MaxCompute 任务慢，需先合并小文件（Hive ALTER TABLE CONCATENATE 或 Spark coalesce）
3. **Kafka MM2 lag 不稳定** — 检查同步线程数（tasks.max）+ 网络带宽，避免源集群顺序消费瓶颈
4. **Oracle 时区** — Oracle TIMESTAMP WITH TIME ZONE 在 MC 需统一转 UTC 存储
5. **ETL 死锁** — Airflow 中 SubDag/Sensor 翻译到 DataWorks 时易出现循环依赖，需用 DAG 可视化工具校验
6. **元数据不一致** — HMS 迁 DLF 后注意 SerDe 类全名（org.apache.hadoop.hive.serde2.* 大部分兼容，自定义 SerDe 需上传 jar）
7. **资源配额误差** — MC CU 与自建 CPU 不可直接换算，建议按"扫描数据量 + 历史 CPU 时"双指标估算
8. **数据校验慢** — 5PB 数据全量 MD5 不现实，改抽样（每分区 1% 行 + 关键字段 GROUP BY 校验）

---

## 9. 与其他文档的引用关系

| 关联文档 | 关系 |
| --- | --- |
| `references/migration-methodology.md` | 通用 4 阶段框架，本文是其大数据领域专项扩展 |
| `references/architecture-templates.md` | 引用 T5 数据湖仓模板作为目标态 |
| `knowledge/cloud-solutions.md` S5 | 数据湖仓一体方案，迁移完成后的目标架构 |
| `knowledge/aliyun-products.md` | EMR / MaxCompute / DataWorks / Flink / Hologres / Kafka / DataX / Lindorm 产品卡 |
| `references/well-architected.md` | 迁移后的优化阶段评审依据 |

---

## 10. 客户案例索引（待持续蒸馏）

- **某股份制银行**：CDH 6.3 → EMR + MaxCompute，120 节点 / 800TB / 2 万 ETL 任务，6 个月完成 [推断]
- **某汽车主机厂**：Oracle 数仓 30TB + 1500 PL/SQL → MaxCompute，ADAM 评估改写 4 个月 [推断]
- **某互联网平台**：自建 Kafka 60 节点 → 阿里云 Kafka 专业版，MM2 平迁 3 周完成 [推断]
- **菜鸟物流**：Hadoop + 数据湖仓融合，PolarDB for AI 加速 [官方]

> 后续蒸馏 ATA 文章后填充具体数字与决策点。

---

**最近更新**：2026-06-18
**维护人**：neil-aliyun-sa skill
**反馈渠道**：在 `knowledge/inbox.md` 登记新案例，定期蒸馏入此文档
