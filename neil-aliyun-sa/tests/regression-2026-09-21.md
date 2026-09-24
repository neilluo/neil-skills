# 自动化回归报告 — 2026-09-21 12:12 

> **测试器**：scripts/run-regression.py
> **用例库**：tests/regression-cases.yaml (v1.3)
> **覆盖文件**：13 个 markdown / 共 235097 字符
> **PASS 阈值**：命中率 ≥ 85%

## 总览

- **整体命中率**：100.0%
- **PASS 数**：30/30
- **FAIL 数**：0/30

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
| T10 | F | ALB vs MSE 网关 vs API Gateway | 9/9 | 100% | ✅ PASS |
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
| GW01 | C | AI网关/云原生API网关 外部认证 ext-auth service_name 与 FQDN 命名规则 | 8/8 | 100% | ✅ PASS |
| GW02 | F | API 网关三种形态产品谱系与原API网关 EOL | 6/6 | 100% | ✅ PASS |
| GW03 | C | Serverless 版 AI 网关不支持插件的硬限制与三级作用域 | 6/6 | 100% | ✅ PASS |
| GW04 | B | 网关外部认证 A路(全局认证鉴权) vs B路(ext-auth) 选型与超时单位陷阱 | 9/9 | 100% | ✅ PASS |

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
| `S10` | ✅ |

## 文件覆盖

| 文件 | 字符数 |
| --- | --- |
| `knowledge/aliyun-products.md` | 70,385 |
| `knowledge/cloud-solutions.md` | 47,004 |
| `knowledge/industry-landscape.md` | 14,480 |
| `knowledge/ai-trends.md` | 25,039 |
| `knowledge/competitor-cloud.md` | 18,893 |
| `knowledge/company-profiles.md` | 9,920 |
| `references/architecture-templates.md` | 9,724 |
| `references/migration-methodology.md` | 8,897 |
| `references/bigdata-migration.md` | 17,483 |
| `references/well-architected.md` | 3,597 |
| `references/caf-landing-zone.md` | 4,646 |
| `references/cloud-product-mapping.md` | 3,098 |
| `references/customer-playbook.md` | 1,931 |

## 负控实验（Negative Control，2026-09-21）

> 全绿/满分是失效信号。本节证明「新增用例在本次改动之前会 FAIL」。
> **方法**：未改动工作树——用只读方式取两套改动前语料到 /tmp 临时目录：
> ① `cp` 快照本次编辑前的工作树 13 个语料文件 → `/tmp/kb-baseline-20260921/`（含 2026-08-08 未提交改动，即编辑前的真实状态）；
> ② 只读 git 命令 `git show HEAD:neil-aliyun-sa/<file>`（HEAD=3723a5a）→ `/tmp/kb-head-20260921/`。
> 匹配逻辑与 run-regression.py 完全一致：同 files 清单（13 文件拼接 blob）、大小写不敏感子串、阈值 0.85。脚本：`/tmp/negctl-20260921.py`。

### 结果矩阵（改动前）

| 用例 | 基线1：编辑前工作树快照 | 基线2：git HEAD(3723a5a) | 改动后（本报告正文） |
| --- | --- | --- | --- |
| GW01（ext-auth/service_name/FQDN） | **0/8 = 0% → FAIL** | **0/8 = 0% → FAIL** | 8/8 = 100% PASS |
| GW02（三种形态谱系/EOL） | **0/6 = 0% → FAIL** | **0/6 = 0% → FAIL** | 6/6 = 100% PASS |
| GW03（Serverless 插件硬限制） | **0/6 = 0% → FAIL** | **0/6 = 0% → FAIL** | 6/6 = 100% PASS |
| GW04（A路 vs B路/超时陷阱） | **0/9 = 0% → FAIL** | **0/9 = 0% → FAIL** | 9/9 = 100% PASS |
| T10 完整 9 词（v1.3 扩词后） | 6/9 = 67% → **FAIL**（仅 v1.3 新增 4 词单算 = 1/4 = 25%） | 6/9 = 67% → **FAIL** | 9/9 = 100% PASS |

### 旧版本命中数 = 0 的关键词清单（两套基线一致，共 30 个）

- **GW01（8 个全 0）**：`ext-auth`、`service_name`、`FQDN`、`my-svc.dns`、`svc.cluster.local`、`forward_auth`、`path_prefix`、`外部认证`
- **GW02（6 个全 0）**：`云原生 API 网关`、`AI 网关`、`原 API 网关`、`2026-08-23`、`2027-09-21`、`全面下线`
- **GW03（6 个全 0）**：`Serverless版不支持`、`专享实例`、`插件市场`、`路由级`、`域名级`、`插件规则`
- **GW04（9 个全 0）**：`全局认证鉴权`、`自建的鉴权服务`、`鉴权API`、`x-mse-external-authz-check-result`、`endpoint_mode`、`failure_mode_allow`、`status_on_error`、`宽松模式`、`S10`
- **T10 v1.3 新增词（3 个 0 命中）**：`云原生API网关`（无空格写法）、`AI 网关`、`原 API 网关`；第 4 个新增词 `三种形态` 在旧库已有 3 处命中（Tair/ACK 卡），故 T10 旧版为 6/9=67% 而非 0%，仍 < 0.85 FAIL——证明 T10 原 5 词确系假绿，扩词后才有判别力。

### 结论

4 个新用例（GW01-GW04，29 个关键词）在两套改动前基线上**全部 0 命中、全部 FAIL**；扩词后的 T10 在改动前也 FAIL（67%）。改动后 30/30 全 PASS 由本次写入的知识真实驱动，非假绿。

---

# 收口补充回归（2026-09-21 第二轮：MCP 维度 + 火山对标）

> **测试器**：scripts/run-regression.py（逻辑未改动）
> **用例库**：tests/regression-cases.yaml (**v1.4**，新增 GW05/GW06；GW01-GW04/T10 等既有用例未改动)
> **覆盖文件**：13 个 markdown（与首轮相同清单）
> **PASS 阈值**：命中率 ≥ 85%
> ⚠️ 本节为**追加**，首轮结果与负控节原样保留在上方。

## 总览

- **整体命中率**：100.0%
- **PASS 数**：32/32
- **FAIL 数**：0/32
- 既有用例（T01-GW04 共 30 个）全部保持 PASS（无回归）；新增 2 用例：

| ID | 模式 | 场景 | 命中 / 总数 | 命中率 | 状态 |
| --- | --- | --- | --- | --- | --- |
| GW05 | C | MCP 鉴权：tools/list 能否鉴权 / 传输层鉴权 / 消费者认证 / HTTP转MCP / forward_auth | 9/9 | 100% | ✅ PASS |
| GW06 | E | 火山引擎 API 网关外部认证对标（Envoy 内核 / 仅实例级 / 同私有网络 / 精确匹配 / GET或POST / 邀测） | 6/6 | 100% | ✅ PASS |

## 新增用例命中明细

### GW05 [PASS]

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

### GW06 [PASS]

| 关键词 | 命中 |
| --- | --- |
| `采用 Envoy 内核` | ✅ |
| `仅支持在实例级别生效` | ✅ |
| `相同私有网络` | ✅ |
| `精确匹配` | ✅ |
| `GET 或 POST` | ✅ |
| `邀测` | ✅ |

## 负控实验（Negative Control，收口补充轮）

> 全绿是失效信号。本节证明「GW05/GW06 在本轮改动之前会 FAIL」。
> **方法（未改动工作树）**：
> ① 基线1 = 本轮**编辑前**工作树 13 个语料文件的 `cp` 快照 → `/tmp/kb-closeout-baseline-20260921/`（即上一轮蒸馏完成后的状态）；
> ② 基线2 = 只读 git 命令 `git show HEAD:neil-aliyun-sa/<file>`（HEAD=3723a5a，含上两轮之前状态）→ `/tmp/kb-head-closeout/`。
> 匹配逻辑与 run-regression.py 完全一致：同 13 文件拼接 blob、大小写不敏感子串计数、阈值 0.85。

### 每个关键词的旧版命中数（逐词实测）

| 关键词 | 基线1（编辑前工作树） | 基线2（git HEAD 3723a5a） |
| --- | --- | --- |
| GW05 `tools/list` | **0** | **0** |
| GW05 `initialize` | 3（⚠️ 均为无关英文用法：aliyun-products:153 `Initialize`、ai-trends:401 Agent 初始化语境 ×2，非 MCP 鉴权） | 1（同为 aliyun-products:153 无关用法） |
| GW05 `Streamable HTTP` | **0** | **0** |
| GW05 `单一 MCP endpoint` | **0** | **0** |
| GW05 `消费者认证` | 2（上一轮能力清单/选型场景泛提及，非 MCP 语境） | **0** |
| GW05 `HTTP转MCP` | **0** | **0** |
| GW05 `forward_auth` | 18（上一轮 B 路 ext-auth 内容已含） | **0** |
| GW05 `X-Forwarded-Uri` | 2（上一轮 B 路示例已含） | **0** |
| GW05 `传输层鉴权` | **0** | **0** |
| GW06 `采用 Envoy 内核` | **0** | **0** |
| GW06 `仅支持在实例级别生效` | **0** | **0** |
| GW06 `相同私有网络` | **0** | **0** |
| GW06 `精确匹配` | **0** | **0** |
| GW06 `GET 或 POST` | **0** | **0** |
| GW06 `邀测` | **0** | **0** |

### 结果矩阵（改动前 → 改动后）

| 用例 | 基线1：编辑前工作树 | 基线2：git HEAD(3723a5a) | 本轮改动后 |
| --- | --- | --- | --- |
| GW05（MCP 鉴权 9 词） | **4/9 = 44% → FAIL** | **1/9 = 11% → FAIL** | 9/9 = 100% PASS |
| GW06（火山对标 6 词） | **0/6 = 0% → FAIL** | **0/6 = 0% → FAIL** | 6/6 = 100% PASS |

### 结论

- GW06 六个关键词在两套基线上**全部 0 命中、全 FAIL**——本轮火山对标知识全部为新增。
- GW05 在两套基线上均 FAIL（44% / 11% < 85%）。如实说明：`forward_auth`/`X-Forwarded-Uri`/`消费者认证`/`initialize` 4 词在基线1 已有命中，系上一轮 ext-auth B 路与无关英文用法所致（逐词出处见上表）；MCP 语义判别词（`tools/list`、`Streamable HTTP`、`单一 MCP endpoint`、`HTTP转MCP`、`传输层鉴权`）在两套基线全部 0 命中。对基线2（git HEAD）除 1 处无关 `Initialize` 外全部 0 命中。
- 未删除任何关键词、未降低阈值；改动后 32/32 全 PASS 由本轮写入的 MCP 维度与火山对标知识真实驱动。
