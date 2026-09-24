# 自动化回归报告 — 2026-09-24 15:26 

> **测试器**：scripts/run-regression.py
> **用例库**：tests/regression-cases.yaml (v1.8)
> **覆盖文件**：23 个 markdown / 共 1165795 字符
> **PASS 阈值**：命中率 ≥ 85%；🔴 **且 `forbidden` 不变量零命中**（命中即 FAIL，与命中率无关）

## 总览

- **整体命中率**：100.0%
- **PASS 数**：85/85
- **FAIL 数**：0/85
- **forbidden 不变量**：共 15 条，违反 **0** 条

## 用例结果矩阵

| ID | 模式 | 场景 | 命中 / 总数 | 命中率 | forbidden 违反 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | F | Tair vs 自建 Redis 30 秒判断 | 4/4 | 100% | — | ✅ PASS |
| T02 | C | Qwen-Plus vs Qwen-Turbo 选型 | 4/4 | 100% | — | ✅ PASS |
| T03 | C | 视频点播平台存储+分发选型 | 8/8 | 100% | — | ✅ PASS |
| T04 | B | 零售连锁全渠道数据中台 | 8/8 | 100% | — | ✅ PASS |
| T05 | B | SaaS 多租户架构 | 7/7 | 100% | — | ✅ PASS |
| T06 | E | 阿里云 vs 火山引擎 AI MaaS | 7/7 | 100% | — | ✅ PASS |
| T07 | D | 教育行业上云特征 | 6/6 | 100% | — | ✅ PASS |
| T08 | B | 车联网 5000 万设备接入 | 7/7 | 100% | — | ✅ PASS |
| T09 | C | MaxCompute vs EMR Spark 选型 | 5/5 | 100% | — | ✅ PASS |
| T10 | F | ALB vs MSE 网关 vs API Gateway | 9/9 | 100% | — | ✅ PASS |
| BD01 | B | 自建 Hadoop/Hive 500节点迁 MaxCompute+EMR | 7/7 | 100% | — | ✅ PASS |
| BD02 | C | HDFS 500TB 迁 OSS 选型 | 5/5 | 100% | — | ✅ PASS |
| BD03 | B | 自建 Kafka 迁云 + Flink 实时链路 | 5/5 | 100% | — | ✅ PASS |
| BD04 | F | 30秒 EMR vs MaxCompute vs Hologres | 6/6 | 100% | — | ✅ PASS |
| BD05 | B | Oracle 数仓 50TB 迁 MaxCompute | 5/5 | 100% | — | ✅ PASS |
| BD06 | B | CDH/HDP EOL 迁 EMR | 6/6 | 100% | — | ✅ PASS |
| BD07 | C | DataWorks vs Airflow/DolphinScheduler | 5/5 | 100% | — | ✅ PASS |
| BD08 | B | Spark Streaming→Flink+Paimon+Hologres 实时升级 | 6/6 | 100% | — | ✅ PASS |
| S01 | C | WAF 3.0 版本选型（基础/高级/企业/旗舰） | 6/6 | 100% | — | ✅ PASS |
| S02 | B | 企业安全合规方案（等保/DDoS/WAF/云安全中心） | 5/5 | 100% | — | ✅ PASS |
| LZ01 | B | Landing Zone 多账号管理架构 | 5/5 | 100% | — | ✅ PASS |
| MG01 | B | IDC 迁云 6R 决策 + 数据迁移工具链 | 5/5 | 100% | — | ✅ PASS |
| MG02 | C | 迁移方法论四阶段选型 | 5/5 | 100% | — | ✅ PASS |
| AI01 | B | 企业 AI Agent 平台方案（百炼+RAG+多Agent） | 6/6 | 100% | — | ✅ PASS |
| AI02 | C | AIGC 内容生产选型（万相/HappyHorse/CosyVoice） | 5/5 | 100% | — | ✅ PASS |
| AI03 | F | 百炼 vs PAI-EAS 成本交叉点 30秒判断 | 5/5 | 100% | — | ✅ PASS |
| PP01 | C | PolarDB 家族购买路径核验完整性 | 6/6 | 100% | — | ✅ PASS |
| PP02 | C | RDS 家族购买路径核验完整性 + Serverless 下线 | 6/6 | 100% | — | ✅ PASS |
| PP03 | C | ADB / MaxCompute / Hologres 购买路径核验 | 7/7 | 100% | — | ✅ PASS |
| PP04 | C | ClickHouse 双版本购买路径核验 | 6/6 | 100% | — | ✅ PASS |
| PP05 | C | Lindorm 购买路径 + Serverless 无法新购 | 6/6 | 100% | — | ✅ PASS |
| PP06 | C | EMR 家族购买路径核验 + HA Master 3 起步 | 6/6 | 100% | — | ✅ PASS |
| PP07 | C | Flink 全托管无作业级 Serverless | 5/5 | 100% | — | ✅ PASS |
| PP08 | C | DataWorks 资源组购买路径核验 | 5/5 | 100% | — | ✅ PASS |
| PP09 | C | Tair / OSS / PAI / 百炼 购买路径核验 | 6/6 | 100% | — | ✅ PASS |
| PP10 | C | 采购路径核验清单结构完整性（红色预警清单 + 匿名核验边界） | 9/9 | 100% | — | ✅ PASS |
| RG01 | C | 百炼知识库（RAG）规格计费与权限红线 | 8/8 | 100% | — | ✅ PASS |
| RG02 | C | 向量检索 / RAG 检索引擎 12 条产品线选型 | 9/9 | 100% | — | ✅ PASS |
| RG03 | B | 私有化部署路线（PAI-EAS 独享 GPU / ACS / 一体机） | 8/8 | 100% | — | ✅ PASS |
| RG04 | B | S10 企业内部知识库（员工侧 RAG）场景方案 | 10/10 | 100% | — | ✅ PASS |
| RG05 | C | 核验项 C13/C14 与文档解析计费口径 | 6/6 | 100% | — | ✅ PASS |
| OL01 | C | 六引擎 OLAP 场景选型（ADB/Hologres/Doris/SelectDB/StarRocks/ClickHouse） | 9/9 | 100% | — | ✅ PASS |
| OL02 | C | OLAP 选型关键版本门槛与厂商 benchmark 存疑清单 | 5/5 | 100% | — | ✅ PASS |
| OL03 | C | 阿里云上开源 OLAP 售卖映射与内部实战口径 | 5/5 | 100% | — | ✅ PASS |
| NET01 | C | 出云流量费计费模型：带宽 vs 流量双模式 + CDT 统一出账 | 7/7 | 100% | — | ✅ PASS |
| NET02 | C | 出云流量避坑：BGP 精品无免费额度与买带宽仍收流量费排查 | 5/5 | 100% | — | ✅ PASS |
| AC01 | C | AgentCore 产品归属与术语（三个平级产品 / AgentTeams 一名两指 / 本地纳管 Agent） | 14/14 | 100% | — | ✅ PASS |
| AC02 | C | AgentCore 五个计费项单价（算力/网关/存储 CU + 协作管控面门槛费 + CDT 出账） | 8/8 | 100% | — | ✅ PASS |
| AC03 | C | CU 换算公式与「换算示例 ≠ 规格菜单」红线 | 7/7 | 100% | — | ✅ PASS |
| AC04 | C | 地域价表只有内地一行同价 + 新加坡 ap-southeast-1 无单价禁外推 | 7/7 | 100% | — | ✅ PASS |
| AC05 | C | 三项依赖产品（CMS/PrivateLink/SchedulerX3）→ AgentCore 账单 ≠ 全成本 | 7/7 | 100% | — | ✅ PASS |
| AC06 | C | 报价三硬缺口（新加坡单价 / 数据处理量单价 / 算力 CU 规格档位） | 6/6 | 100% | — | ✅ PASS |
| AC07 | C | 协作管控面限免活动窗口与边界（强时效，2026-10-18 后必须复核） | 8/8 | 100% | — | ✅ PASS |
| AC08 | C | 限免期实例连续 30 天无操作即停用回收且不可逆 | 6/6 | 100% | — | ✅ PASS |
| AC09 | C | SLA 可用率 99.9%（非 99.95/99.99）+ 两条必说限定词 | 7/7 | 100% | — | ✅ PASS |
| AC10 | C | SLA 赔偿三档 15%/30%/100% + Workspace 服务单元 + 出账金额基数 + 2 个月时限 + 例外第 (7) 条 | 13/13 | 100% | — | ✅ PASS |
| AC11 | C | 账号集成 30 用户硬上限 / 无微信账号集成 / 无 LDAP-SCIM 目录同步 | 8/8 | 100% | — | ✅ PASS |
| AC12 | C | slug 陷阱：configure-dingtalk-account-integration 正文其实是飞书 | 6/6 | 100% | — | ✅ PASS |
| AC13 | C | AgentCore 六条数值型配额（SubAgent/记忆空间/MCP 描述/纳管并发/VPC 交换机） | 7/7 | 100% | — | ✅ PASS |
| AC14 | C | SLR 权限面排障：RAM 搜 Magic / magic.aliyuncs.com / hiclaw-* / 158 条 Action | 8/8 | 100% | — | ✅ PASS |
| AC15 | C | 未商用能力清单 + AgentCore 不是公测产品（严禁据 AgentTeams 公测免费外推） | 8/8 | 100% | — | ✅ PASS |
| AC16 | C | AgentTeams 迁移：不自动 / 交互式 6 步 / 5 类不迁 / 术语映射仅 1 条有证据 / 四项缺口 | 14/14 | 100% | — | ✅ PASS |
| AG01 | C | AI 网关产品族归属与定位（三平级子产品 / 原API网关下线时间 / 三类接入） | 11/11 | 100% | 0/1 | ✅ PASS |
| AG02 | C | AI 网关四形态选型与起步量级（Serverless 标准/企业/旧版 + 专享实例） | 12/12 | 100% | — | ✅ PASS |
| AG03 | B | AI 网关报价三本账 + 六类连带（AI Credits 是独立商品） | 13/13 | 100% | 0/3 | ✅ PASS |
| AG04 | F | 🔴 AI 网关 SLA 分档与「无赔偿区」（协议原文 > 产品页宣称） | 7/7 | 100% | 0/2 | ✅ PASS |
| AG05 | F | AI 网关容量规格与 🔴 QPS 口径官方无定义 | 6/6 | 100% | — | ✅ PASS |
| AG06 | F | 🔴 自建认证 404 是设计行为（合思案根因 + 宽松模式不兜底 4xx） | 8/8 | 100% | — | ✅ PASS |
| AG07 | C | AI 网关鉴权四条路 + 🔴 MCP 认证方式官方口径冲突（C9 已修订，须实测） | 10/10 | 100% | 0/3 | ✅ PASS |
| AG08 | F | 🔴 限流是四套不是一套 + 超限返回码全部文档未说明（不可类推 429） | 6/6 | 100% | — | ✅ PASS |
| AG09 | F | 🔴 Fallback 默认在限流命中时也触发 + AI 缓存与 TTL 空白 | 5/5 | 100% | — | ✅ PASS |
| AG10 | C | MCP 接入形态 + 🔴 工具级鉴权对 tools/list 的作用（按权限过滤而非拒绝） | 10/10 | 100% | 0/4 | ✅ PASS |
| AG11 | F | 🔴 插件 slug↔官方标题交叉错位（对客只写插件名）+ 插件延时数字稀缺 | 8/8 | 100% | — | ✅ PASS |
| AG12 | B | 🔴 RAM/SLR 与多租户架构级结论（无 ARN 定义 → 只能分账号或分实例） | 7/7 | 100% | — | ✅ PASS |
| AG13 | F | 可观测与 OpenAPI 元信息（%s 占位配额 / 35 Action 无流控条目 / 日志字段错字） | 6/6 | 100% | — | ✅ PASS |
| AG14 | B | 集成配方 + 🔴 压缩比≠节省率 + Vertex AI 页无跨境网络要求 | 9/9 | 100% | 0/1 | ✅ PASS |
| AG15 | G | 🔴 元层用例：抓取工艺五种失效模式与覆盖率审计口径（防工艺知识退化） | 9/9 | 100% | — | ✅ PASS |
| AG16 | C | 🔴 选型硬门槛与单向门（R2a E 节：这 6 条原只藏子页，速查卡必须有） | 7/7 | 100% | 0/1 | ✅ PASS |
| AG17 | F | 🔴 三个 Action 计数消歧（179 SLR / 140 OpenAPI / 57 AgentCore 侧 apig） | 4/4 | 100% | — | ✅ PASS |
| GW01 | C | AI网关/云原生API网关 外部认证 ext-auth service_name 与 FQDN 命名规则 | 8/8 | 100% | — | ✅ PASS |
| GW02 | F | API 网关三种形态产品谱系与原API网关 EOL | 6/6 | 100% | — | ✅ PASS |
| GW03 | C | Serverless 版 AI 网关不支持插件的硬限制与三级作用域 | 6/6 | 100% | — | ✅ PASS |
| GW04 | B | 网关外部认证 A路(全局认证鉴权) vs B路(ext-auth) 选型与超时单位陷阱 | 9/9 | 100% | — | ✅ PASS |
| GW05 | C | MCP 鉴权：tools/list 能否鉴权 / 传输层鉴权 / 消费者认证 / HTTP转MCP / forward_auth | 9/9 | 100% | — | ✅ PASS |
| GW06 | E | 火山引擎 API 网关外部认证对标（Envoy 内核 / 仅实例级 / 同私有网络 / 精确匹配 / GET或POST / 邀测） | 6/6 | 100% | — | ✅ PASS |

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
| `云原生API网关` | ✅ |
| `AI 网关` | ✅ |
| `原 API 网关` | ✅ |
| `三种形态` | ✅ |

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

### RG01 — 百炼知识库（RAG）规格计费与权限红线  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `0.03 元/知识库·小时` | ✅ |
| `0.2 元/RCU·小时` | ✅ |
| `720 小时` | ✅ |
| `初步召回的总切片数` | ✅ |
| `SearchFilters` | ✅ |
| `不能当安全边界` | ✅ |
| `2027-01-16` | ✅ |
| `qwen3-rerank` | ✅ |

### RG02 — 向量检索 / RAG 检索引擎 12 条产品线选型  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `DashVector` | ✅ |
| `Milvus 版` | ✅ |
| `OpenSearch 向量检索版` | ✅ |
| `pgvector` | ✅ |
| `OpenStore` | ✅ |
| `FalconSeek` | ✅ |
| `HGraph` | ✅ |
| `DiskANN` | ✅ |
| `2000 维` | ✅ |

### RG03 — 私有化部署路线（PAI-EAS 独享 GPU / ACS / 一体机）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `learn_EasDedicatedPrepay_public_cn` | ✅ |
| `GU30` | ✅ |
| `GU120` | ✅ |
| `3,661` | ✅ |
| `SDWebUI` | ✅ |
| `GPU 切分` | ✅ |
| `gn8v` | ✅ |
| `AI Stack` | ✅ |

### RG04 — S10 企业内部知识库（员工侧 RAG）场景方案  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `S10` | ✅ |
| `员工侧 RAG` | ✅ |
| `BFF` | ✅ |
| `Recall@5` | ✅ |
| `合理拒答率` | ✅ |
| `渗透率` | ✅ |
| `section_path` | ✅ |
| `RRF` | ✅ |
| `Auto-Merge` | ✅ |
| `长上下文不能替代 RAG` | ✅ |

### RG05 — 核验项 C13/C14 与文档解析计费口径  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `C13 Serverless 最低门槛费` | ✅ |
| `C14 计费口径的计量基数` | ✅ |
| `docmind_general_dp_cn` | ✅ |
| `EnhancementMode=VLM` | ✅ |
| `0.02 元/页` | ✅ |
| `0.04 元/页` | ✅ |

### OL01 — 六引擎 OLAP 场景选型（ADB/Hologres/Doris/SelectDB/StarRocks/ClickHouse）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `ClickBench` | ✅ |
| `单表大宽表` | ✅ |
| `复杂多表 JOIN` | ✅ |
| `高并发主键点查` | ✅ |
| `存算分离` | ✅ |
| `HSAP` | ✅ |
| `羲和` | ✅ |
| `玄武` | ✅ |
| `SelectDB Cloud 原生内核` | ✅ |

### OL02 — OLAP 选型关键版本门槛与厂商 benchmark 存疑清单  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `25.3` | ✅ |
| `43.0s` | ✅ |
| `存疑清单` | ✅ |
| `TPC-DS 对决` | ✅ |
| `版本门槛` | ✅ |

### OL03 — 阿里云上开源 OLAP 售卖映射与内部实战口径  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `EMR Serverless StarRocks` | ✅ |
| `唯一封装 SelectDB Cloud 原生内核` | ✅ |
| `迁移工具成熟度` | ✅ |
| `一票否决项` | ✅ |
| `StarRocks＞Doris` | ✅ |

### NET01 — 出云流量费计费模型：带宽 vs 流量双模式 + CDT 统一出账  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `出云流量` | ✅ |
| `按固定带宽计费` | ✅ |
| `按使用流量计费` | ✅ |
| `共享流量包` | ✅ |
| `220GB` | ✅ |
| `0.80 元/GB` | ✅ |
| `入方向流量不计费` | ✅ |

### NET02 — 出云流量避坑：BGP 精品无免费额度与买带宽仍收流量费排查  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `BGP（多线）_精品` | ✅ |
| `无免费额度` | ✅ |
| `不走 CDT` | ✅ |
| `CDT 控制台` | ✅ |
| `316GB` | ✅ |

### AC01 — AgentCore 产品归属与术语（三个平级产品 / AgentTeams 一名两指 / 本地纳管 Agent）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `智能体构建和治理平台 AgentCore` | ✅ |
| `3052261` | ✅ |
| `3034770` | ✅ |
| `3049178` | ✅ |
| `三个平级独立产品` | ✅ |
| `多智能体治理与协作平台 AgentTeams` | ✅ |
| `智能体 AgentRun` | ✅ |
| `已迁移至 AgentCore` | ✅ |
| `协作客户端 (WEB)` | ✅ |
| `协作客户端(API)` | ✅ |
| `定时任务在协作客户端（AgentTeams）中创建和管理` | ✅ |
| `本地纳管 Agent` | ✅ |
| `guidelines-for-the-use-of-local-nanoagent` | ✅ |
| ``nanoagent` 在正文命中 0 次` | ✅ |

### AC02 — AgentCore 五个计费项单价（算力/网关/存储 CU + 协作管控面门槛费 + CDT 出账）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `CNY 0.0000694/CU` | ✅ |
| `CNY 0.0000015/CU` | ✅ |
| `CNY 0.00025/CU` | ✅ |
| `3 元/小时起 = 2160 元/月固定项` | ✅ |
| `协作专享管控面 **3 元/小时 = 2160 元/月**（按 720h）` | ✅ |
| `0.8 元/GB` | ✅ |
| `云数据传输CDT` | ✅ |
| `由 CDT 统一计费和出账` | ✅ |

### AC03 — CU 换算公式与「换算示例 ≠ 规格菜单」红线  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `3600 CU` | ✅ |
| `0.5 CU/(GB·秒)` | ✅ |
| `7200 CU` | ✅ |
| `3600 × 0.0000694 = **CNY 0.2498**` | ✅ |
| `7200 × 0.0000694 = **CNY 0.4997**` | ✅ |
| `换算示例，不是可选规格档位` | ✅ |
| `选择所需 CPU 和内存` | ✅ |

### AC04 — 地域价表只有内地一行同价 + 新加坡 ap-southeast-1 无单价禁外推  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `中国内地 4 地域单价完全一致` | ✅ |
| `地域价表只有「北京、杭州、上海、深圳」**一行且四地完全同价**` | ✅ |
| `ap-southeast-1` | ✅ |
| `Regions in the Chinese mainland` | ✅ |
| `无任何单价（RULINGS B4 硬缺口）` | ✅ |
| `对客严禁用中国内地单价外推新加坡` | ✅ |
| `新加坡单价**官方未公开**，需走商务/工单确认后再报` | ✅ |

### AC05 — 三项依赖产品（CMS/PrivateLink/SchedulerX3）→ AgentCore 账单 ≠ 全成本  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `CMS（云监控）` | ✅ |
| `用于写入 Tracing 数据` | ✅ |
| `PrivateLink（私网连接）` | ✅ |
| `SchedulerX3` | ✅ |
| `跳转售卖页购买` | ✅ |
| `这 0.8 元/GB 不出现在 AgentCore 账单里` | ✅ |
| `客户按 AgentCore 账单核成本会漏项` | ✅ |

### AC06 — 报价三硬缺口（新加坡单价 / 数据处理量单价 / 算力 CU 规格档位）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `报价三硬缺口` | ✅ |
| `新加坡单价 / 数据处理量单价 / 算力 CU 可选规格档位` | ✅ |
| `数据处理量` | ✅ |
| `请求体和响应体的数据量按**『数据处理量』单独计费**` | ✅ |
| `无单价、无计量单位（RULINGS B6 = 硬缺口）` | ✅ |
| `算力 CU 的可选规格档位 = **硬缺口**` | ✅ |

### AC07 — 协作管控面限免活动窗口与边界（强时效，2026-10-18 后必须复核）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `2026-09-18 00:00:00 ~ 2026-10-18 23:59:59（北京时间，GMT+8）` | ✅ |
| `本节 2026-10-18 后必须复核` | ✅ |
| `距活动结束 27 天` | ✅ |
| `活动结束后计费策略另行通知` | ✅ |
| `原价 3 元/小时` | ✅ |
| `限免不包括：Agent运行时的算力、存储和网关请求等其它费用` | ✅ |
| `限免期间协作管控面**金额为 0 元**` | ✅ |
| `账单出现 0 元行**不是漏计**` | ✅ |

### AC08 — 限免期实例连续 30 天无操作即停用回收且不可逆  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `连续 30 天无操作` | ✅ |
| `限免期间创建的` | ✅ |
| `停用并自动回收资源` | ✅ |
| `不能。停用为不可逆操作` | ✅ |
| `在 30 天内使用一次协作功能即可重置计时` | ✅ |
| `Agent 与资产配置均保留，仅协作功能不可用` | ✅ |

### AC09 — SLA 可用率 99.9%（非 99.95/99.99）+ 两条必说限定词  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Agent 运行时服务可用性不低于 99.9%` | ✅ |
| `99.9% 不随实例规格 / 地域 / 付费方式分档` | ✅ |
| `全文 `99.95` 命中 **0** 次` | ✅ |
| `仅针对 AgentCore 平台自身的 Agent 运行时服务` | ✅ |
| `除非另有约定` | ✅ |
| `本协议不适用于` | ✅ |
| `本地云版本` | ✅ |

### AC10 — SLA 赔偿三档 15%/30%/100% + Workspace 服务单元 + 出账金额基数 + 2 个月时限 + 例外第 (7) 条  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `≥ 99.0% 且 < 99.9%` | ✅ |
| `≥ 95.0% 且 < 99.0%` | ✅ |
| `不超过该服务单元当月月度服务费用的 100%` | ✅ |
| `不同服务单元分别计算、可叠加` | ✅ |
| `不可提现、转让或折现` | ✅ |
| `按出账金额计，不含以代金券、优惠券及赠送额度抵扣的部分` | ✅ |
| `未达标月份结束后 **2 个月**内` | ✅ |
| `逾期后果：**不受理**` | ✅ |
| `第 (7) 条对客必须主动讲` | ✅ |
| `实例启停、文件删除等不可逆操作` | ✅ |
| `经客户授权的` | ✅ |
| `在客户授权范围内` | ✅ |
| `一律不赔` | ✅ |

### AC11 — 账号集成 30 用户硬上限 / 无微信账号集成 / 无 LDAP-SCIM 目录同步  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `最多支持 30 个用户，超出后账号集成将失败` | ✅ |
| `30 用户硬上限` | ✅ |
| `钉钉、微信、飞书` | ✅ |
| `微信只有消息通道、无账号集成` | ✅ |
| `无任何微信账号集成页` | ✅ |
| `无 LDAP/SCIM` | ✅ |
| `仅支持通过本地账号方式进行认证` | ✅ |
| `企业目录同步需另配 IDaaS` | ✅ |

### AC12 — slug 陷阱：configure-dingtalk-account-integration 正文其实是飞书  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `configure-dingtalk-account-integration` | ✅ |
| `agentcore-configure-dingtalk-account-integration` | ✅ |
| `这一页是飞书集成，不是钉钉` | ✅ |
| `配置飞书账号集成` | ✅ |
| `AgentCore 支持企业成员使用飞书扫码登录` | ✅ |
| `标题对、slug 错` | ✅ |

### AC13 — AgentCore 六条数值型配额（SubAgent/记忆空间/MCP 描述/纳管并发/VPC 交换机）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `最多可配置20个SubAgent` | ✅ |
| `1~64 字符` | ✅ |
| `最多 1024 个字符` | ✅ |
| `不超过 1000 个字符` | ✅ |
| `默认并发数为 2，支持设置为 1～8` | ✅ |
| `--max-concurrent-tasks` | ✅ |
| `需选择至少 2 个交换机，并确保覆盖至少 2 个不同可用区` | ✅ |

### AC14 — SLR 权限面排障：RAM 搜 Magic / magic.aliyuncs.com / hiclaw-* / 158 条 Action  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `在搜索框中输入 **`Magic`** 并搜索` | ✅ |
| `magic.aliyuncs.com` | ✅ |
| `acs:oss:*:*:hiclaw-*` | ✅ |
| `AliyunServiceRoleForAgentCore` | ✅ |
| `AliyunServiceRoleForMagic` | ✅ |
| `SLR 策略 Action 前缀构成（158 条）` | ✅ |
| ``schedulerx` 命中 0 条` | ✅ |
| `mse.console.aliyun.com/#/magic-console/` | ✅ |

### AC15 — 未商用能力清单 + AgentCore 不是公测产品（严禁据 AgentTeams 公测免费外推）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `快速创建**：表单式低代码创建，即将上线` | ✅ |
| `虚拟 MCP` | ✅ |
| `注册 Agent（待上线）` | ✅ |
| `高代码 Agent（待上线）` | ✅ |
| `本页不是「公测产品页」` | ✅ |
| `13 页「公测」命中 **0**` | ✅ |
| `AgentCore 已商用计费、无准入白名单` | ✅ |
| `自称「公测阶段、产品本身免费」的是 **AgentTeams**` | ✅ |

### AC16 — AgentTeams 迁移：不自动 / 交互式 6 步 / 5 类不迁 / 术语映射仅 1 条有证据 / 四项缺口  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `不自动迁移` | ✅ |
| `交互式 6 步` | ✅ |
| `不在本次迁移范围内（5 类，逐字照抄）` | ✅ |
| `仅 1 条有页面证据（Skill ↔ Skill）` | ✅ |
| `其余 **18 条均为「页面未说明」**` | ✅ |
| `不得把 Worker↔Agent 等术语映射当官方等价关系` | ✅ |
| `Worker → Agent` | ✅ |
| `迁移生效时间/是否强制/有无截止时间/AgentTeams 控制台是否还能进` | ✅ |
| `官方未公布截止时间` | ✅ |
| `严禁把文件名当迁移生效日期` | ✅ |
| `agentteams-to-agentcore-migration-tool-20260831.zip` | ✅ |
| `新的 Endpoint` | ✅ |
| `不得据 AgentTeams「当前处于公测阶段，产品本身免费」推断 AgentCore 免费` | ✅ |
| `严禁外推到 AgentCore` | ✅ |

### AG01 — AI 网关产品族归属与定位（三平级子产品 / 原API网关下线时间 / 三类接入）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `API 网关产品族` | ✅ |
| `云原生API网关` | ✅ |
| `原API网关` | ✅ |
| `2026-08-23 停止新购` | ✅ |
| `2027-09-21 全面下线` | ✅ |
| `兼容 OpenAI 协议` | ✅ |
| `Model API / Agent API / MCP Server` | ✅ |
| `托管入口` | ✅ |
| `what-is-an-ai-gateway` | ✅ |
| `Higress 开源版` | ✅ |
| `product-comparison` | ✅ |

forbidden 不变量（1 条，命中即 FAIL）：

- ✅ 未命中 `AI 网关是独立 productCode 文档根`

### AG02 — AI 网关四形态选型与起步量级（Serverless 标准/企业/旧版 + 专享实例）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `0 元起步` | ✅ |
| `0.245 元/小时` | ✅ |
| `0.005 元/千CU` | ✅ |
| `7.9335` | ✅ |
| `3,997.5` | ✅ |
| `金融云 = 内地 ×1.9` | ✅ |
| `aigw.small.x1` | ✅ |
| `192,000` | ✅ |
| `K8s 服务来源 = N/A` | ✅ |
| `capacity-description` | ✅ |
| `在线路由总数` | ✅ |
| `1,280,000` | ✅ |

### AG03 — AI 网关报价三本账 + 六类连带（AI Credits 是独立商品）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `0.01 元/Credit` | ✅ |
| `独立商品` | ✅ |
| `先建实例再单独开通` | ✅ |
| `lvwang_guardrail_public_cn` | ✅ |
| `CDT` | ✅ |
| `AI 增强能力的 Credits 折算率查无` | ✅ |
| `Credits/1M tokens` | ✅ |
| `私网 0.049` | ✅ |
| `公网 0.037` | ✅ |
| `账单地板` | ✅ |
| `超额累进` | ✅ |
| `消费者规则扩容数` | ✅ |
| `延停权益` | ✅ |

forbidden 不变量（3 条，命中即 FAIL）：

- ✅ 未命中 `私网比公网便宜`
- ✅ 未命中 `AI Credits 折算率全库查无`
- ✅ 未命中 `仍处公测`

### AG04 — 🔴 AI 网关 SLA 分档与「无赔偿区」（协议原文 > 产品页宣称）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `不低于 99.90%` | ✅ |
| `不低于 99.99%` | ✅ |
| `无赔偿区` | ✅ |
| `仅限代金券` | ✅ |
| `2025-09-10` | ✅ |
| `低于 99.00% 但等于或高于 95.00%` | ✅ |
| `不晚于相关月份结束后 2 个月` | ✅ |

forbidden 不变量（2 条，命中即 FAIL）：

- ✅ 未命中 `99.95% 的 SLA 承诺`
- ✅ 未命中 `SLA 承诺 99.95%`

### AG05 — AI 网关容量规格与 🔴 QPS 口径官方无定义  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `1,500` | ✅ |
| `12,000` | ✅ |
| `144,000` | ✅ |
| `2,560,000` | ✅ |
| `QPS 口径官方无定义` | ✅ |
| `13000 QPS` | ✅ |

### AG06 — 🔴 自建认证 404 是设计行为（合思案根因 + 宽松模式不兜底 4xx）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `需是前缀匹配` | ✅ |
| `鉴权API加上原始业务请求的Path` | ✅ |
| `forward_auth` | ✅ |
| `endpoint_mode` | ✅ |
| `建立连接失败或者返回5xx请求` | ✅ |
| `404 属 4xx` | ✅ |
| `safe_regex_match` | ✅ |
| `需要完全匹配，而非部分匹配` | ✅ |

### AG07 — AI 网关鉴权四条路 + 🔴 MCP 认证方式官方口径冲突（C9 已修订，须实测）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `消费者 API-Key` | ✅ |
| `全局 JWT 认证` | ✅ |
| `OIDC` | ✅ |
| `自建认证` | ✅ |
| `仅支持 API Key` | ✅ |
| `hmac-auth` | ✅ |
| `准入控制点` | ✅ |
| `MCP Server 支持 JWT 认证` | ✅ |
| `裁决 C9 已修订` | ✅ |
| `带日期发布记录` | ✅ |

forbidden 不变量（3 条，命中即 FAIL）：

- ✅ 未命中 `MCP 场景**不得承诺 JWT**`
- ✅ 未命中 `MCP 场景仅支持 API Key`
- ✅ 未命中 `唯一官方支持`

### AG08 — 🔴 限流是四套不是一套 + 超限返回码全部文档未说明（不可类推 429）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `AiTokenRateLimit` | ✅ |
| `同时命中` | ✅ |
| `Http状态码默认为429` | ✅ |
| `TokenPerMinute` | ✅ |
| `消费者配额` | ✅ |
| `FinOps` | ✅ |

### AG09 — 🔴 Fallback 默认在限流命中时也触发 + AI 缓存与 TTL 空白  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `仅Fallback后端服务错误` | ✅ |
| `1800秒` | ✅ |
| `语义化缓存` | ✅ |
| `browser-cache-control` | ✅ |
| `tokens 均为 0` | ✅ |

### AG10 — MCP 接入形态 + 🔴 工具级鉴权对 tools/list 的作用（按权限过滤而非拒绝）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `HTTP to MCP` | ✅ |
| `网关托管` | ✅ |
| `Nacos` | ✅ |
| `获取工具列表只能看到和调用有权限的工具` | ✅ |
| `Streamable HTTP` | ✅ |
| `语义检索` | ✅ |
| `工具精选` | ✅ |
| `ec7aa8c7` | ✅ |
| `提供 REST 到 A2A 协议的转换能力` | ✅ |
| `查无配置方法` | ✅ |

forbidden 不变量（4 条，命中即 FAIL）：

- ✅ 未命中 `A2A 协议转换 189 页零命中`
- ✅ 未命中 `A2A 协议转换的配置步骤见`
- ✅ 未命中 `OpenAPI 无 MCP 专用 Action`
- ✅ 未命中 `公网流量统一由 CDT 计费出账`

### AG11 — 🔴 插件 slug↔官方标题交叉错位（对客只写插件名）+ 插件延时数字稀缺  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `ai-prompt-decorator` | ✅ |
| `ai-prompt-template` | ✅ |
| `ai-cue-template` | ✅ |
| `ai-cue-decorator` | ✅ |
| `20 微秒` | ✅ |
| `30 微秒` | ✅ |
| `0.19毫秒` | ✅ |
| `性能测试条件全缺` | ✅ |

### AG12 — 🔴 RAM/SLR 与多租户架构级结论（无 ARN 定义 → 只能分账号或分实例）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `47.1%` | ✅ |
| `AliyunServiceRoleForNativeApiGw` | ✅ |
| `InvokeKMS` | ✅ |
| `多租户隔离只能分账号或分实例` | ✅ |
| `AliyunAPIGFullAccess` | ✅ |
| `AliyunNativeApiGwFullAccess` | ✅ |
| `不作 SLA 承诺` | ✅ |

### AG13 — 可观测与 OpenAPI 元信息（%s 占位配额 / 35 Action 无流控条目 / 日志字段错字）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `safechack_status` | ✅ |
| `%s` | ✅ |
| `35 个 Action 无流控配额条目` | ✅ |
| `UpdatePluginAttachment` | ✅ |
| `5KB` | ✅ |
| `Response_Flag` | ✅ |

### AG14 — 集成配方 + 🔴 压缩比≠节省率 + Vertex AI 页无跨境网络要求  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `92%–97%` | ✅ |
| `28%–40%` | ✅ |
| `压缩比 = 压缩后/原始` | ✅ |
| `公网 NAT 网关` | ✅ |
| `Ib_config` | ✅ |
| `PAI-EAS` | ✅ |
| `ComfyUI` | ✅ |
| `Dify` | ✅ |
| `Claude Code` | ✅ |

forbidden 不变量（1 条，命中即 FAIL）：

- ✅ 未命中 `Vertex AI 配方要求跨境专线`

### AG15 — 🔴 元层用例：抓取工艺五种失效模式与覆盖率审计口径（防工艺知识退化）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `软 200` | ✅ |
| `24893` | ✅ |
| `Document Not Found` | ✅ |
| `服务端静默截断` | ✅ |
| `agent-api-observable` | ✅ |
| `378` | ✅ |
| `负控实验` | ✅ |
| `TOC 容器` | ✅ |
| `不得宣称「全站蒸馏」` | ✅ |

### AG16 — 🔴 选型硬门槛与单向门（R2a E 节：这 6 条原只藏子页，速查卡必须有）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Serverless版AI网关不支持开启WAF防护` | ✅ |
| `仅支持新版 Serverless 网关的标准版和企业版` | ✅ |
| `K8s服务来源数 = **N/A**` | ✅ |
| `不对该等使用场景作出服务等级协议（SLA）承诺` | ✅ |
| `开通后不支持退订和关闭` | ✅ |
| `仅先支持智能路由` | ✅ |
| `超出申请时限的赔偿申请将不被受理` | ✅ |

forbidden 不变量（1 条，命中即 FAIL）：

- ✅ 未命中 `AI Credits 开通后会持续产生费用`

### AG17 — 🔴 三个 Action 计数消歧（179 SLR / 140 OpenAPI / 57 AgentCore 侧 apig）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `AI 网关自己的 SLR 里 `apig:` 前缀 = 0 条` | ✅ |
| `182 − 4 = 178` | ✅ |
| `ram:CreateServiceLinkedRole` | ✅ |
| `不要把 57 当成 AI 网关的权限面` | ✅ |

### GW01 — AI网关/云原生API网关 外部认证 ext-auth service_name 与 FQDN 命名规则  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `ext-auth` | ✅ |
| `service_name` | ✅ |
| `FQDN` | ✅ |
| `my-svc.dns` | ✅ |
| `svc.cluster.local` | ✅ |
| `forward_auth` | ✅ |
| `path_prefix` | ✅ |
| `外部认证` | ✅ |

### GW02 — API 网关三种形态产品谱系与原API网关 EOL  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `云原生 API 网关` | ✅ |
| `AI 网关` | ✅ |
| `原 API 网关` | ✅ |
| `2026-08-23` | ✅ |
| `2027-09-21` | ✅ |
| `全面下线` | ✅ |

### GW03 — Serverless 版 AI 网关不支持插件的硬限制与三级作用域  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `Serverless版不支持` | ✅ |
| `专享实例` | ✅ |
| `插件市场` | ✅ |
| `路由级` | ✅ |
| `域名级` | ✅ |
| `插件规则` | ✅ |

### GW04 — 网关外部认证 A路(全局认证鉴权) vs B路(ext-auth) 选型与超时单位陷阱  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `全局认证鉴权` | ✅ |
| `自建的鉴权服务` | ✅ |
| `鉴权API` | ✅ |
| `x-mse-external-authz-check-result` | ✅ |
| `endpoint_mode` | ✅ |
| `failure_mode_allow` | ✅ |
| `status_on_error` | ✅ |
| `宽松模式` | ✅ |
| `S11` | ✅ |

### GW05 — MCP 鉴权：tools/list 能否鉴权 / 传输层鉴权 / 消费者认证 / HTTP转MCP / forward_auth  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `tools/list` | ✅ |
| `initialize` | ✅ |
| `Streamable HTTP` | ✅ |
| `单一 MCP endpoint` | ✅ |
| `消费者认证` | ✅ |
| `HTTP转MCP` | ✅ |
| `forward_auth` | ✅ |
| `X-Forwarded-Uri` | ✅ |
| `传输层鉴权` | ✅ |

### GW06 — 火山引擎 API 网关外部认证对标（Envoy 内核 / 仅实例级 / 同私有网络 / 精确匹配 / GET或POST / 邀测）  [PASS]

| 关键词 | 命中 |
| --- | --- |
| `采用 Envoy 内核` | ✅ |
| `仅支持在实例级别生效` | ✅ |
| `相同私有网络` | ✅ |
| `精确匹配` | ✅ |
| `GET 或 POST` | ✅ |
| `邀测` | ✅ |

## 文件覆盖

| 文件 | 字符数 |
| --- | --- |
| `knowledge/aliyun-products.md` | 169,033 |
| `knowledge/aliyun-agentcore.md` | 122,486 |
| `knowledge/aliyun-ai-gateway.md` | 102,526 |
| `knowledge/aliyun-ai-gateway-billing.md` | 51,730 |
| `knowledge/aliyun-ai-gateway-traffic.md` | 84,715 |
| `knowledge/aliyun-ai-gateway-auth.md` | 84,963 |
| `knowledge/aliyun-ai-gateway-mcp-agent.md` | 92,173 |
| `knowledge/aliyun-ai-gateway-plugins.md` | 114,014 |
| `knowledge/aliyun-ai-gateway-ops.md` | 114,499 |
| `knowledge/cloud-solutions.md` | 57,308 |
| `knowledge/industry-landscape.md` | 16,141 |
| `knowledge/ai-trends.md` | 36,963 |
| `knowledge/competitor-cloud.md` | 22,243 |
| `knowledge/company-profiles.md` | 13,422 |
| `knowledge/olap-engine-selection.md` | 4,539 |
| `references/architecture-templates.md` | 11,494 |
| `references/migration-methodology.md` | 8,897 |
| `references/bigdata-migration.md` | 17,483 |
| `references/well-architected.md` | 3,597 |
| `references/caf-landing-zone.md` | 4,646 |
| `references/cloud-product-mapping.md` | 3,098 |
| `references/customer-playbook.md` | 1,931 |
| `references/pricing-verification-checklist.md` | 27,894 |
