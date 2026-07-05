# neil-aliyun-sa — 资深阿里云解决方案架构师 Skill

> 一个基于 **Karpathy LLM Wiki** 架构的阿里云万事通知识库与方案副驾。
> 核心理念：知识预编译一次并持续维护，而非每次查询时从原始文档重新推导。
> 灵感来源：[Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) + ATA 文章 [《一个广告行业 AI 顾问的修炼之路（11 天版）》](https://ata.atatech.org/articles/11020643601)

## 这是什么

`neil-aliyun-sa` 不是一个一次性写完的“知识库快照”，而是严格遵循 **Karpathy LLM Wiki 三层架构** 的活体知识系统：

```
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Schema (SKILL.md)                              │
│  “The key configuration file that makes the LLM a         │
│   disciplined wiki maintainer rather than a chatbot”     │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Wiki (knowledge/ + references/ + index.md)      │
│  LLM 生成并维护的结构化知识，预编译且持续更新           │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Raw Sources (raw/)                              │
│  不可变原始资料，LLM 只读不改，source of truth              │
└─────────────────────────────────────────────────────────┘
```

| Karpathy 原版概念 | 本项目实现 | 说明 |
|---|---|---|
| Raw Sources | `raw/` | 不可变原始资料归档（ATA 快照/官方文档/客户资料） |
| Wiki | `knowledge/` + `references/` | LLM 维护的结构化知识（动态+静态分离） |
| Schema | `SKILL.md` | 角色定义 + 8 种工作模式 + 红线 + 输出模板 |
| index.md | `index.md` | Wiki 内容目录 + 交叉引用表 |
| log.md | `changelog.md` | 时间线日志（Ingest/Lint/Query回写） |
| Ingest | 模式 A | 投喂 → Raw 归档 → 蒸馏到 Wiki → 更新 index |
| Query | 模式 B-F | 查询 wiki 并综合回答 |
| Query→Wiki | 模式 H | 高质量回答回写到 wiki（探索复利） |
| Lint | 模式 G | Wiki 健康检查（矛盾/过时/孤页/缺页） |

## 为什么这样设计

### 1. 不限于 SA 工作范围

Neil 的需求是"阿里云万事通"——不只输出方案，还要回答：
- "PolarDB 和 Lindorm 怎么选" → 模式 C（产品选型）
- "这个客户的赛道怎么看" → 模式 D（行业研究）
- "AWS 出海方案怎么对位" → 模式 E（竞品对比）
- "百炼最近有啥新东西" → 模式 B（先行业扫描，再落入 ai-trends.md）

所以工作模式从 reference skill 的 5 个（A-E）扩展到 6 个（A-F），并把"方案设计"提为最核心的模式 B。

### 2. 写入优先（防丢失红线）

LLM 会话随时可能被截断/上下文丢失。**资料读了但没落盘 = 等于没读**。
所以协议要求：第一个动作就是写 inbox + changelog 的"⏳ 进行中"，第二步才开始分析。

### 3. 跨源验证（提升置信度）

阿里云产品/方案信息源很多：官方文档、ATA、SA 案例、客户反馈、行业报告、竞品白皮书。
单一来源容易偏差。**三源同述 = 工程范式**，所以 knowledge 文件中标注 `[官方]` / `[实战]` / `[推断]` 三档证据等级。

### 4. 知识与参考分离

- **knowledge/** = 会随学习不断变化的（场景案例越积越多）
- **references/** = 框架性的、相对稳定的（Well-Architected 框架不会天天变）

这样蒸馏脚本不会去碰 references，知识漂移的风险被隔离。

## 目录结构（Karpathy LLM Wiki 三层映射）

```
neil-aliyun-sa/
├── SKILL.md                      # Schema 层：角色 + 8 种工作模式 + 红线
├── README.md                     # 你正在看的这份文档：设计说明
├── index.md                      # Wiki 导航：内容目录 + 交叉引用表
├── changelog.md                  # log.md：时间线日志（Ingest/Lint/Query回写）
├── raw/                          # Layer 1: Raw Sources（不可变）
│   ├── README.md                  #   raw 层说明与命名约定
│   ├── ata/                       #   ATA 内部文章快照
│   ├── aliyun-docs/               #   help.aliyun.com 官方文档片段
│   ├── customer-cases/            #   客户案例原始资料
│   ├── industry-reports/           #   行业报告、白皮书
│   ├── competitor/                #   竞品云公开资料
│   └── misc/                      #   其他来源
├── knowledge/                    # Layer 2: Wiki（动态知识）
│   ├── inbox.md                   #   Raw 注册入口（状态机）
│   ├── cloud-solutions.md         #   场景化方案库
│   ├── aliyun-products.md         #   产品能力知识库
│   ├── industry-landscape.md      #   行业地图
│   ├── ai-trends.md               #   AI 趋势
│   ├── company-profiles.md        #   客户画像
│   └── competitor-cloud.md        #   竞品云情报
├── references/                   # Layer 2: Wiki（静态参考）
│   ├── well-architected.md        #   WAF 五大支柱速查
│   ├── caf-landing-zone.md        #   CAF + Landing Zone
│   ├── cloud-product-mapping.md   #   场景×产品矩阵
│   ├── customer-playbook.md       #   客户话术
│   ├── architecture-templates.md  #   高频架构模板
│   ├── migration-methodology.md   #   IDC→云迁移方法论
│   └── bigdata-migration.md       #   大数据迁云专项
├── outputs/                      # 方案/报告输出
├── scripts/                      # 自动化脚本（回归测试等）
├── tests/                        # 测试用例 + 回归报告
└── skills/                       # 子 skill 注册目录（预留）
```

## 8 种工作模式（对齐 Karpathy 三大操作）

| 模式 | Karpathy 操作 | 触发场景 | 关键动作 |
| --- | --- | --- | --- |
| **A 资料消化** | Ingest | "学习一下 + 链接" | inbox登记 → Raw归档 → 蒸馏到Wiki → 更新index |
| **B 方案设计** | Query | "给我一个 XXX 上云方案" | 读 index定位 → 查模板 → WAF 5 支柱展开 → BOM → 风险 |
| **C 产品选型** | Query | "X 和 Y 怎么选" | 查 aliyun-products + mapping → 对比表 |
| **D 行业研究** | Query | "分析 XX 客户/赛道" | 查 industry + WebSearch → 商业→技术→切入点 |
| **E 竞品对比** | Query | "对位 AWS 怎么看" | 查 competitor-cloud → 对位表 + 卖点 |
| **F 快速洞察** | Query | "简单说说 / 值得跟进吗" | 3-5 行结论 + 1 判断 + 下一步 |
| **G Lint** | Lint | "检查知识库" / 每5次Ingest后 | 矛盾/过时/孤页/缺页检测 → P0-P2 报告 |
| **H Query回写** | Query→Wiki | 高质量输出自动触发 | 提炼核心 → 增量写入knowledge → 更新index |

## 知识来源策略

种子知识来自两路并行注入：

### 路径一：ATA 高价值文章（内部实战经验）

通过 `ata-all` skill 已识别出的高价值文章清单（按命中数 + 收藏排序）：

| 文章 ID | 标题 | 价值定位 |
| --- | --- | --- |
| 11020643601 | 一个广告行业 AI 顾问的修炼之路（11 天版） | **方法论母版**——本 skill 的协议设计直接源自此 |
| ADR/SDD 系列 | 架构决策记录与方案设计文档闭环 | 方案输出规范 |
| 宝马 Landing Zone Accelerator | 大型企业落地实践 | LZ 模板与避坑 |
| 可口可乐云原生变革 | 传统巨头数字化转型案例 | 行业 + 客户画像 |
| 莉莉丝 AWS Winback | 跨云迁移与差异化 | 竞品 + 出海 |
| 网商银行智能化定位 | 金融业 AI 落地 | 行业 + AI |
| 高可用 AI 系统 | 推理服务架构 | AI 架构 |
| 淘宝海外 TaobaoBonus | 出海架构 | 出海 + 双活 |
| Aegis AI 数字分身 | AI Agent 实践 | AI 趋势 |
| Lambda → FC 跨云迁移 | Serverless 对位 | 竞品 + Serverless |
| SA 动手系列（PD 分离部署） | 推理基础设施 | AI 架构 |
| ad-industry-cloud-insights 修炼之路 | reference skill 母版 | 方法论 |

### 路径二：help.aliyun.com/zh 官方文档（权威知识源）

经过 subagent 实地探查，整体结构覆盖：
- 21 个一级产品类目（弹性计算 / 容器 / 存储 / 网络 / 数据库 / 数据 / AI / 中间件 / 安全 / 混合云 / 物联网 / 视频云 / 通信 / 开发者 / 监控运维 / 金融 / 政企 / 出海 / 行业云 / 边缘 / Serverless）
- ~90 个核心产品文档站点
- 框架级入口：CAF（`/zh/caf/`）、Well-Architected（`/zh/product/2362200.html`）、安全建设指南（`/zh/acsg/`）、网络架构设计指南（`/zh/cloud-network-well-architected-design/`）
- 每个产品的标准结构：product-overview / getting-started / user-guide / use-cases / developer-reference / support

种子注入策略：先把**框架级文档**蒸馏到 `references/well-architected.md` 与 `references/caf-landing-zone.md`；再把**高频产品**蒸馏到 `knowledge/aliyun-products.md`；按需扩展。

## 使用方式

### 投喂学习

```
学习一下 https://ata.atatech.org/articles/XXXXX
学习一下 https://help.aliyun.com/zh/ack/...
学习一下 [本地文件路径或粘贴内容]
```

→ 触发模式 A，自动登记 inbox、写 changelog、蒸馏到合适的 knowledge 文件。

### 求方案

```
给我一个 XX 公司 XX 业务上阿里云的方案
这个 PRD 怎么落地到阿里云
帮我设计一个出海 + 大促弹性的电商架构
```

→ 触发模式 B，按 Well-Architected 五大支柱产出完整方案。

### 选型问题

```
RDS PostgreSQL 和 PolarDB PG 怎么选
ACK 和 ACS 有什么差异
SLB CLB/ALB/NLB/GWLB 各自适用什么场景
```

→ 触发模式 C，给能力对比表 + 推荐场景 + 文档链接。

### 行业 / 竞品 / 快速判断

→ 触发模式 D / E / F，详见 SKILL.md。

## 演进路径

| 阶段 | 目标 | 标志 |
| --- | --- | --- |
| **v0.1** | 骨架建立 | SKILL.md / 占位 knowledge & references / 写入优先协议 |
| **v0.2** | 框架填充 | WAF + CAF 蒸馏完成 |
| **v0.3** | 产品广度 | 66+ 产品能力卡完成 |
| **v0.4** | 场景深度 | 9 套高频场景方案 |
| **v0.5** | 行业 + 竞品 | 7 行业卡 + 竞品矩阵 + 8 客户档案 |
| **v0.6** | 迁移专项 | migration-methodology + bigdata-migration |
| **v0.7** | 自动化回归 | regression-cases.yaml + run-regression.py (100% PASS) |
| **v0.8（当前）** | Karpathy LLM Wiki 对齐 | raw/ + index.md + cross-ref + Lint + Query回写 |
| **v1.0** | 实战验证 | 跑通 3 个真实客户方案输出，无明显遗漏 |

## 与 Karpathy LLM Wiki 原版的差异

| 维度 | Karpathy 原版 | neil-aliyun-sa | 说明 |
| --- | --- | --- | --- |
| Wiki 粒度 | 每个实体/概念一个页面 | 按领域聚合为大文件 | 大文件对 LLM 上下文友好，用 cross-ref 补偿 |
| References 层 | 不存在 | 独立 references/ | 增强：静态框架与动态知识分离 |
| 证据分级 | 未提及 | [官方]/[实战]/[推断] | 增强：跨源验证体系 |
| 回归测试 | 未提及 | run-regression.py | 增强：量化质量守护 |
| 工作模式 | Ingest/Query/Lint (3) | A-H (8 种) | 细化：领域特化的 Query 分类 |
| 写入优先 | 未强调 | 不可违反红线 | 增强：防 LLM 上下文丢失 |

## 红线

见 SKILL.md 末尾的"质量红线"——9 条。**写入优先**与**跨源验证**是不可违反的两条工程纪律。
