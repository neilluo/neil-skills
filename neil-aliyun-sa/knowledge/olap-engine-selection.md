# OLAP 引擎选型专题：ADB / Hologres / Doris / SelectDB / StarRocks / ClickHouse

> **来源**：2026-08-21 深度调研（7 路 subagent 并发：官方文档/GitHub/公开 benchmark/中英文社区/ATA 内部实战，三源交叉验证）。
> **配套交付**：完整深度报告见 outputs/OLAP六引擎场景适用性调研报告.md。
> **证据等级**：[官方]/[GitHub]/[社区]/[厂商]（利益相关方营销）/[内部]（ATA）/[共识]（≥2 独立来源一致）/[推断]。
> **⚠️ 对客脱敏**：标 [内部] 的条目含集团内实践与 SA 内部口径，对客使用前须脱敏。

---

## 1. 一句话定位速查

| 引擎 | 定位 | 最强场景 | 明确短板 |
|---|---|---|---|
| ClickHouse | 极致单表列存聚合引擎（Yandex 开源，49.4k star，月度发版） | 单表大宽表聚合、日志/行为/可观测、时序、压缩比、ClickBench 单表榜首 | 复杂多表 JOIN（易 OOM）、点查、频繁更新、分片复制运维 |
| Apache Doris | 运维最简 MySQL 兼容多面手（百度 Palo→Apache 顶级，15.8k star） | 实时数仓、ES 替代日志检索、混合检索、中小团队一库多用 | 单表极限性能不及 CK、湖仓深度不及 SR、无完整 ACID |
| SelectDB | Doris 原创团队商业发行版（飞轮科技，融资近 10 亿，阿里云参投） | 同 Doris + 托管/存算分离商业增强；阿里云上以全托管数据库售卖 | 无公开价目 |
| StarRocks | 湖仓与复杂 JOIN 最聚焦 MPP（2020 fork 自 Doris，LF 项目，12k star） | 数据湖加速（Iceberg 读写最全）、多表 JOIN、高频实时更新、高并发 BI | 写放大偏高、纯日志生态弱于 CK/Doris |
| Hologres | 阿里生态 Serving+分析一体（HSAP，VLDB 2020，闭源） | 高并发主键点查（64CU 行存 43.6 万 QPS [官方]）、MaxCompute 零 ETL 加速、实时大屏 | 绑定阿里云生态、闭源 benchmark 不可独立验证 |
| AnalyticDB | 阿里云 MySQL 生态通用实时数仓（羲和+玄武，Spark+湖仓，闭源） | MySQL 生态建仓、多源联合、湖仓+Spark、AI 融合（ai_generate/百亿向量） | 超高 QPS 点查让位 Hologres、脱离阿里云生态无意义 |

## 2. 场景 → 引擎映射（多源一致共识）

| 场景 | 首选 | 备选 | 判据 |
|---|---|---|---|
| 数据在 MaxCompute/Flink 生态 + 高并发点查/Serving | **Hologres** | ADB | 生态亲和第一判据；Hologres 直读盘古存储 |
| MySQL 生态实时数仓/多源联合/Spark 湖仓 | **ADB MySQL 湖仓版** | Hologres | 协议亲和；ADB OLAP 分析更强[内部] |
| 单表日志/行为/可观测海量聚合 | **ClickHouse** | Doris（倒排）| ClickBench 共识：单表 CK 领先 SR/Doris 约 2 倍+ |
| 开源、场景杂、替 ES、团队小 | **Doris**（托管→SelectDB） | StarRocks | 无 ZK 运维最简；功能广度路线 |
| 湖仓加速/复杂多表 JOIN/高频更新/高并发 BI | **StarRocks**（阿里云→EMR Serverless SR） | Doris | Iceberg 读写最全；CBO+Pipeline |
| 高并发主键点查（画像/维表/特征服务） | **Hologres 行存** | ADB 行存引擎(2026-02)/Doris 行存/SR 主键表 | 均需 POC；CK 明确不适合 |
| 高频 CDC 实时更新 | SR 主键表 ≈ Doris MOW | Hologres/ADB | 避免 CK（最终一致语义） |
| 纯离线 T+1 超大规模 | MaxCompute | — | 这六个 OLAP 引擎都不选 |

## 3. 交叉验证结论（可直接引用）

**[共识] 可信清单**：
1. CK 单宽表/日志性能顶级：ClickBench 官方榜单（2026 实解析）CK 18.1s vs SR 43.0s vs Doris 48.4s（c6a.4xlarge），Tinybird/袋鼠云同向。注意 ClickBench 只测单表。
2. CK 短板=复杂 JOIN/点查/更新/运维——有赞、哈啰、携程迁移动机与 HN 抱怨一致，连对手都承认，全领域可信度最高的一条。
3. Doris≈StarRocks 同源同量级，独立实测互有胜负（差距 10–40%），无代差；差异在路线（Doris 功能广度 vs SR 湖仓深度）与治理/商业公司。
4. 迁移模式共识：CK→Doris/SR 动因=JOIN/并发/更新短板；Druid/Kylin/ES→Doris 动因=多组件统一+降本。
5. ⚠️ Hologres/ADB 为闭源云产品，所有 benchmark 均出自阿里云渠道，结构性不可独立验证，引用须标口径。

**[厂商] 存疑清单（勿对客直接引用）**：SelectDB"Doris 快 CK 14 倍"（CK 失败按 0 秒计）；SelectDB RTABench"6 倍"（自建基准）；SR"ClickBench 登顶"（2023 历史状态，当前 CK 快 SR 约 2.4 倍）；ADB"TPC-H 第一/12 万 QPS"（无版本无复现）；Hologres"SSB 快 CK 35%"（对比 2021 年 CK 21.8 老版本）；所有迁移案例倍数均单一厂商渠道。

**两大阵营从未正面 TPC-DS 对决**：SR 官方只对比 Trino、Doris 官方不做横向——各发布对自己有利的参照系。

## 4. 关键版本门槛（对客承诺能力前必核对）

| 能力 | Doris | StarRocks | ClickHouse |
|---|---|---|---|
| 存算分离 | 3.0（2024-06）GA | 3.0 引入（3.1+ 生产可用） | Cloud/阿里云企业版 |
| 实时更新 | 2.0 MOW | 2.0 主键表 GA | lightweight update/delete 仍 Beta（25.8） |
| JSON/半结构化 | 2.1 Variant→3.0 稳定 | 4.0 Flat JSON V2 默认 | **25.3 才生产可用** |
| 向量检索 | 4.0（2025-10） | 3.4 向量索引 | 25.8 GA |
| 全文检索 | 4.0 SEARCH()+BM25 | 4.0 主键表倒排/4.1 存算分离 Beta | — |
| AI 函数 | 4.0 SQL AI 函数 | 4.1 ai_query | 收购 Langfuse（Agentic Analytics） |

## 5. 阿里云售卖映射与内部实战 [内部]

**售卖映射**：StarRocks→EMR Serverless StarRocks（包月 ¥157/CU 起，乌兰察布 ¥141.28）；Doris→SelectDB 全托管（阿里云是唯一封装 SelectDB Cloud 原生内核的云厂商）；ClickHouse→企业版（Serverless，⚠️ 无规格购买入口）+社区兼容版（包月可锁定）；Hologres/ADB 为自研托管。

**SA 内部口径**：
- 开源偏好客户次序：StarRocks＞Doris（清洵三引擎横评原话），提示开源需客户自备专家团队。
- 内部横评自测（100G–1T）：500G 以下 Hologres≈SR＞Doris，1T SR 领先；强调按场景 POC。
- 2023 年打 SR"存算耦合"的攻击点**已过时**——SR Serverless 存算分离已成熟售卖（长安深蓝跨云 winback 案例）。
- 迁移工具成熟度是一票否决项：SR 迁移工具有未文档化坑（truncate 删表重迁/需关 compaction）；CK→Hologres 无成熟工具、SQL 改造巨大（大参林案例）。
- ADB 并非不可挑战：集团内菜鸟 WMS 自建 Doris 替换 ADB（成本+SQL 责任隔离）、ESA 用 CK 替换 DRDS+ADB（百亿日志）；1688 金算子用 SelectDB 账单点查 RT 16ms；滔搏上云把 Doris+SR 统一为 SR；申通三引擎并存是常态。
- Hologres 内部心智：行存主键点查=维表/在线服务化（菜鸟物流百亿维表）；双11 大屏/淘菜菜/大淘系 DT。ADB 内部场景：淘宝订单交易、品牌数据银行圈人 10min→5s、DAS 8GB/s。

## 6. 商业公司变动信号（2026）

- **CelerData 2026-05 更名 PhoenixAI**，定位 Agentic AI Database，2026-06 B 轮 $8000 万——StarRocks 商业战略有变数，跟踪其社区投入。
- ClickHouse Inc 2026-01 Series D $400M（**估值约 $150 亿**；$63.5 亿是 2024 年 C 轮旧估值，勿混用），收购 Langfuse（LLM 可观测），重心向 Cloud/AI 倾斜。
- SelectDB（飞轮）融资近 10 亿人民币，阿里云参投；仓库定位语改"hybrid search database for AI agents"。
- ⚠️ Uber 被报道将 ClickHouse 日志栈迁往 Pinot（upsert/维表 join 需求）——CK 更新短板在顶级用户持续暴露。

## 7. SA 报价/采购提醒（承接 pricing-verification-checklist）

CK 企业版仅按量无规格入口（采购流程走不通，推社区兼容版包月）；Hologres 计算组网关最低 2 个；ADB MySQL 企业版最低 3 节点步长 3；EMR Serverless StarRocks FE 最低 4CU×3。详见 references/pricing-verification-checklist.md。
