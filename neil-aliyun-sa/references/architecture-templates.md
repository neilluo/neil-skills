# 高频架构模板 — architecture-templates.md

> **定位**：高频可复用的"参考架构"，方案设计模式 B 的脚手架。
> **使用方式**：拿到客户需求 → 找最接近的模板 → 在模板上做客户化裁剪 → 按 Well-Architected 五大支柱补全。

## 模板索引

| 模板 | 适用场景 | 关键产品 |
| --- | --- | --- |
| T1：互联网建站 | 中小规模 Web 业务 | ECS + RDS + OSS + CDN + WAF + SLB |
| T2：电商大促 | 弹性扩缩 + 高可用 | ACK + ECI + PolarDB + Tair + RocketMQ + ALB |
| T3：AIGC 推理服务 | 模型推理 + GPU 弹性 | 百炼 / PAI-EAS + GPU + OSS + ARMS |
| T4：出海双活 | 跨境 + 多 Region | CEN + GA + 海外 RDS + DTS + 海外 OSS |
| T5：数据湖仓一体 | 离线 + 实时分析 | OSS + DLF + MaxCompute + Hologres + DataWorks |
| T6：Landing Zone | 多账号企业上云底座 | RD + CEN + Cloud Firewall + SLS + RAM |
| T7：金融级双活 | 同城 + 异地容灾 | 多 AZ + 异地 Region + DTS + 多活中间件 |
| T8：AI Agent 平台 | 企业 Agent 底座 | 百炼 + RAG + 工具链 + 业务系统集成 |
| T9：实时风控 | L1-L2 实时 | Flink + Tair + Lindorm + 决策引擎 |
| T10：物联网工业平台 | 设备接入 + 数据 + AI | IoT + Lindorm 时序 + Flink + DataV |

---

## T1：互联网建站

```
                       用户
                        │
                       CDN
                        │
                       WAF
                        │
                      SLB/ALB
                        │
              ┌─────────┴─────────┐
              │                   │
            ECS-1               ECS-2     (多 AZ)
              │                   │
              └─────────┬─────────┘
                        │
                ┌───────┼───────┐
                │       │       │
              RDS主   RDS备    Tair    OSS（静态资源）
                                       SLS（日志）
                                       ARMS（监控）
```

**适用规模**：日 PV 10万 - 1000万，月成本 5K - 50K。

---

## T2：电商大促弹性

```
                           用户
                            │
                          DCDN（动静加速）
                            │
                           WAF
                            │
                          ALB（HTTP/2、灰度）
                            │
              ┌─────────────┼─────────────┐
              │             │             │
           ACK 集群（Pro）  ECI 弹性     FC 函数
           （核心微服务）    （弹性计算）  （边缘逻辑）
              │             │             │
              └─────────────┼─────────────┘
                            │
                 ┌──────────┼──────────┐
                 │          │          │
           PolarDB-X     Tair      RocketMQ     OSS
           （订单/商品） （热点）  （削峰）    （图片/订单文档）
                                      │
                              异步消费 → 数据中台
                                              │
                                  Hologres（实时分析）
                                  MaxCompute（离线）
```

**关键弹性策略**：
- 常态：ACK 固定节点 + RI
- 峰值：ECI 抢占式扩缩 / ACS Serverless
- 流量削峰：MQ + 异步处理 + 限流（Sentinel）

---

## T3：AIGC 推理服务

```
                       客户端
                          │
                        API 网关 / ALB
                          │
              ┌───────────┴───────────┐
              │                       │
        百炼（MaaS）                 PAI-EAS（私有部署）
        - 标准模型                   ┌──────────────┐
        - Agent 应用                 │ 推理 Pod    │
        - RAG 工作流                 │ (vLLM)     │
                                    │ 模型: 自托管│
                                    └──────┬───────┘
                                           │
                                ┌──────────┴──────────┐
                                │ GPU ECS / ACS-GPU  │
                                │（A10/A100/H100）   │
                                └──────────┬──────────┘
                                           │
                                ┌──────────┴──────────┐
                                │ OSS（模型仓） │
                                │ Lindorm 向量（RAG）│
                                │ Tair（KV 缓存）│
                                └─────────────────────┘
                                           │
                                  ARMS（链路）+ SLS（日志）
```

**关键决策**：
- MaaS（百炼）vs 自持（PAI）：成本 + 数据敏感度 + QPS
- PD 分离部署（参考 ATA SA 动手系列）
- 推理加速：vLLM / TensorRT / ACC

---

## T4：出海双活（跨境）

```
                                 全球用户
                                    │
                              ┌─────┼─────┐
                              │     │     │
                            DCDN   GA    DCDN
                            北美   全球   东南亚
                              │   加速     │
                              └─────┬─────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
            美东 Region          中国 Region         新加坡 Region
            ┌──────────┐         ┌──────────┐         ┌──────────┐
            │ ALB+WAF │         │ ALB+WAF │         │ ALB+WAF │
            │ ACK     │ ──CEN─→│ ACK     │←─CEN──│ ACK     │
            │ RDS     │←──DTS─→│ RDS     │←─DTS─→│ RDS     │
            │ OSS     │         │ OSS主   │←──┐  │ OSS     │
            └──────────┘         └──────────┘   │  └──────────┘
                                                │
                                          OSS 跨地域复制
```

**合规要点**：
- GDPR：数据驻留、用户同意、被遗忘权
- 美国：CCPA、出口管制
- 中国出境：PIPL 个人信息保护法

---

## T5：数据湖仓一体

```
        业务系统  ─── DTS / Canal ───┐
        日志(SLS) ─── 投递 ──────────┤
        IoT/Kafka ─── Flink ─────────┤
                                     │
                                     ▼
                              ┌──────────────┐
                              │     OSS      │ ← 数据湖（Parquet/ORC）
                              │  Data Lake   │
                              └──────┬───────┘
                                     │
                              ┌──────┴──────┐
                              │     DLF     │ ← 元数据 / 治理
                              └──────┬──────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
            MaxCompute         Hologres            EMR Spark
            （离线）           （实时分析）        （ETL/ML）
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     ▼
                                Quick BI / DataV
                                AI（PAI / 百炼调用湖数据）
```

---

## T6：Landing Zone

> 详见 `references/caf-landing-zone.md` 完整说明。
> 此处为速记图。

```
        管理账号(Master)
            │
        资源目录(RD) ─── Control Policy
            │
   ┌────────┼────────┬────────┬────────┐
 安全审计 日志归档 共享服务  网络 Hub  业务账号(Prod/Stg/Dev)
   │       │       │         │             │
  SLS    SLS归档  AD/ACR    CEN+防火墙    业务 VPC
  ActionTrail              NAT+VPN         (Spoke)
                           高速通道
```

---

## T7：金融级双活（同城 + 异地）

```
        同城（杭州）：双活
        ┌─────────────────────────────────┐
        │  AZ-A         AZ-B          AZ-C│
        │  ┌────┐      ┌────┐       ┌────┐│
        │  │APP │      │APP │       │APP ││
        │  └─┬──┘      └─┬──┘       └─┬──┘│
        │    │           │            │   │
        │  ┌─┴───────────┴────────────┴─┐ │
        │  │  分布式中间件（MSE/RocketMQ）│ │
        │  └─┬───────────┬────────────┬─┘ │
        │  ┌─┴──┐      ┌─┴──┐       ┌─┴──┐│
        │  │RDS │←Sync→│RDS │       │TAIR││
        │  │主  │      │备  │       │多副││
        │  └────┘      └────┘       └────┘│
        └─────────────┬───────────────────┘
                      │
                  CEN 跨地域
                      │
        异地（深圳）：异地容灾 RPO 分钟 / RTO 小时
        ┌─────────────────────────────────┐
        │  DTS 双向同步                    │
        │  RDS / OSS / Tair 全量复制       │
        │  DR 回切预案                      │
        └─────────────────────────────────┘
```

---

## T8：AI Agent 企业平台

> 详细方案参见 `knowledge/cloud-solutions.md` S3 节。此处为模板速记。

```
用户入口(钉钉/Web/App)
       │
  API Gateway / ALB
       │
  ┌────┴────────────────────────────┐
  │  百炼 Agent 2.0                   │
  │  ├─ 意图识别 + Planning           │
  │  ├─ RAG 知识库（向量检索）         │
  │  ├─ Workflow DAG 编排             │
  │  ├─ MCP 工具集成                  │
  │  └─ Multi-Agent 协作              │
  └────┬────────────────────────────┘
       │
  ┌────┼──────────────┐
  │    │              │
Qwen模型层      向量存储        企业API
(Max/Plus/Turbo) (Hologres/    (ERP/CRM/
                 Lindorm/      DB/DingTalk)
                 百炼内置)
       │
  AI Gateway(Higress) — 多模型容灾 0.5s 切换
       │
  ARMS + SLS（全景可观测）
```

**关键决策**：
- 百炼零代码 vs ADK 全代码：需自定义推理 → ADK
- 百炼 MaaS vs PAI-EAS 私有部署：数据不出域 / QPS>1000 → PAI
- 模型选择：复杂推理 → Qwen-Max；成本优先 → Qwen-Turbo（60% 减）
- 高可用：AI Gateway + MSE Prompt 热更新 + AgentRun 沙箱

**客户参考**：一汽红旗(BI 7天→5秒) / 哈啰(GMV+5%) / 51Talk(成本-20~30%)

---

## T9：实时风控（待补充）

- [ ] Flink + 决策引擎 + Lindorm/Tair + 反欺诈规则
- 网商银行参考架构：决策树 + FaaS + Agent 诊断（准确率 93.5%，恢复 3 分钟）[实战-ATA]

---

## T10：物联网工业平台（待补充）

- [ ] IoT + Lindorm 时序 + Flink + DataV

---

## ADR 方法论补充 [实战-ATA]

> 来源：ATA "ADR与SDD：从架构决策到代码落地的闭环" (11020634808)

**ADR (Architecture Decision Records)** — 回答"WHY"
- 核心字段：Status / Context / Options Considered / Decision / Consequences / Confidence Level
- append-only log：决策不可修改，只可被 supersede
- 注入 AI Agent 后效果：架构合规率 46% → 95%，成本/任务 -68%
- AWS/Google Cloud/Azure 2026 年均官方推荐 ADR

**SDD (Solution Design Document)** — 回答"WHAT + HOW TO VERIFY"
- ADR + SDD 闭环 = 完整决策链路

**方案设计(Mode B)适用**：每个方案输出前附 ADR 记录关键决策点 + 置信度等级

---

## 模板使用方式

1. 客户需求来 → 找匹配模板
2. 在模板基础上做规模 / 合规 / 弹性 / 安全的差异化裁剪
3. 按 Well-Architected 五大支柱补全
4. 关键决策附 ADR 记录（Why + Alternatives + Confidence）
5. 如果模板不存在或大幅偏差 → 设计完成后回灌成新模板（演进）
