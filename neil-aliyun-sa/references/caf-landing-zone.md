# CAF 与 Landing Zone 速查 — caf-landing-zone.md

> **来源**：阿里云 [Cloud Adoption Framework (CAF)](https://help.aliyun.com/zh/caf/) + Landing Zone Accelerator（参考 ATA 宝马案例）。
> **定位**：客户上云全生命周期方法论；从战略对齐 → 准备 → 迁移 → 治理 → 优化的标准化路径。

## CAF 框架（六阶段）

| 阶段 | 关键问题 | 主要产出 |
| --- | --- | --- |
| **1. 战略 Strategy** | 上云为了什么？业务诉求 → 技术诉求 | 云战略文档、ROI 假设 |
| **2. 规划 Plan** | 路径怎么走 | 应用画像、迁移波次、TCO/ROI |
| **3. 准备 Ready** | 着陆区怎么搭 | Landing Zone（账号/网络/安全/合规底盘） |
| **4. 采用 Adopt** | 怎么搬上去 | 迁移、现代化、上云模式 |
| **5. 治理 Govern** | 上去之后怎么管 | 策略 / 合规 / 成本 / 安全治理体系 |
| **6. 管理 Manage** | 长期怎么跑 | 运营体系（监控、运维、应急、优化） |

### 五大能力（横向能力）

- **业务能力**（Business） — 战略对齐、变革管理
- **人员能力**（People） — 组织 / 技能 / 文化
- **流程能力**（Process） — DevOps / ITIL / 敏捷
- **平台能力**（Platform） — 技术架构、云原生
- **治理能力**（Governance） — 合规、安全、成本、运营

---

## Landing Zone Accelerator（着陆区加速器）

### 核心组件

```
┌─────────────────── Landing Zone ───────────────────┐
│                                                     │
│  账号体系（Account Factory）                        │
│  ├─ 资源目录（Resource Directory）                  │
│  ├─ 多账号 / 主账号 / 资源账号 / 安全审计账号       │
│  └─ 控制策略（Control Policy）                      │
│                                                     │
│  网络底座（Network Foundation）                     │
│  ├─ 中心 / 辐射拓扑（Hub & Spoke）                  │
│  ├─ CEN 核心 + 多 VPC（生产 / 测试 / 共享 / 安全）  │
│  ├─ 出口网关（NAT / 防火墙）                        │
│  └─ 混合云接入（高速通道 / VPN / SAG）              │
│                                                     │
│  身份与访问（Identity）                             │
│  ├─ SSO / RAM / 角色化访问                          │
│  └─ 跨账号信任 / Assume Role                        │
│                                                     │
│  安全合规（Security & Compliance）                  │
│  ├─ 云安全中心 / WAF / Anti-DDoS                    │
│  ├─ KMS / 密钥管理                                  │
│  ├─ 操作审计 / 合规 / Config 检查                   │
│  └─ 等保 / 行业合规 baseline                        │
│                                                     │
│  运营运维（Ops）                                    │
│  ├─ 集中日志（SLS）                                 │
│  ├─ 集中监控（CloudMonitor / ARMS）                 │
│  ├─ 自动化（OOS / ROS）                             │
│  └─ FinOps 成本治理                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 多账号设计模式

**典型账号划分**：
- `Master / 管理账号` —— 不跑业务，只做治理
- `Security / 安全审计账号` —— 集中接收审计日志、安全告警
- `Log Archive / 日志归档账号` —— 长期归档
- `Shared Services` —— DNS / AD / 制品仓 / 监控
- `Network Hub` —— CEN / 防火墙 / 出口
- `Workload-Prod / Workload-Stg / Workload-Dev` —— 业务账号按环境隔离
- `Sandbox` —— 试验账号

**控制策略**：用 Resource Directory 的 Control Policy 在管理账号下达（类似 AWS SCP）。

### 网络底座模式

**Hub-and-Spoke（中心辐射）**：
- 中心 VPC：CEN 转发 + 防火墙 + NAT + 共享服务
- 业务 VPC：作为 Spoke 接入 CEN
- 混合云接入：高速通道 / VPN 接入 Hub

**多地域**：CEN 跨地域骨干 + GA 全球加速；按业务地域规划 Region。

### 安全 Baseline（开服即生效）

- 所有账号默认开启操作审计 + SLS 集中归档
- 所有 VPC 默认开 Flow Log
- 所有公网入口必经 WAF
- 所有数据库默认 KMS 加密
- 所有 RAM 用户强制 MFA + 密码策略
- 关键 API 操作默认告警
- 配置合规规则（Config）持续检查偏离

---

## 落地节奏建议（参考实战）

| 阶段 | 周期 | 关键里程碑 |
| --- | --- | --- |
| 战略对齐 | 1-2 周 | 高层共识、北极星指标 |
| 着陆区设计 | 2-4 周 | 账号 / 网络 / 安全方案评审通过 |
| 着陆区落地 | 2-4 周 | LZ Accelerator 自动化部署完成 |
| 试点应用迁移 | 4-8 周 | 1-2 个非核心应用验证 |
| 规模化迁移 | 季度级 | 按波次迁移、并行运营 |
| 治理与优化 | 持续 | FinOps、性能优化、合规演进 |

---

## 宝马 Landing Zone Accelerator 实战 [实战-ATA]

> 来源：ATA "宝马落地阿里云Landing Zone Accelerator：AI驱动全链路自动化方案" (11020552831)

### 客户背景

- 宝马在华多实体：华晨宝马、宝马中国、宝马金融
- 需求：统一云治理框架（FPCC.NEXT）、100+ 云账号统一纳管
- 之前方案：购买 Terraform Cloud（年费数十万 RMB）

### 方案架构

| 层级 | 产品组合 | 作用 |
| --- | --- | --- |
| 资源管理 | Resource Directory + 控制策略 | 多账号分级管理 |
| 身份权限 | CloudSSO + RAM 角色化 | 跨实体 SSO |
| 网络安全 | Cloud Firewall + WAF 3.0 + Private Zone | 统一安全出入口 |
| 合规审计 | Config Audit + 操作审计 | 持续合规检查 |
| IaC 自动化 | Terraform + 自动化服务台 + GitOps | 全代码管理云资源 |
| AI 驱动 | AI Coding 一次性生成 Terraform HCL | 100% 代码由 AI 生成（验证通过） |

### 关键洞察

1. **LZ Accelerator 成熟度分级**：阿里云处于 Level 3（加速器框架），与 AWS/Azure/GCP 同层；华为云/腾讯云在 Level 1-2
2. **100% AI Coding**：所有 Terraform 代码由 AI 一次性生成，验证通过率高
3. **State Checker 创新**：检测云资源实际状态与 Terraform State 的漂移（Drift Detection）
4. **遗留资源迁入**：AI 自动生成 Python 脚本，export 存量资源 → import 进 Terraform 管理
5. **成本节省**：替代 Terraform Cloud 许可费用（数十万/年）

### 可复制模式

- 多实体集团 → Resource Directory + CloudSSO + 统一 Control Policy
- IaC 落地 → Terraform + 自动化服务台（替代 Terraform Cloud）
- AI 辅助 → Landing Zone 代码由 AI 生成 + State Checker 持续校验

---

## 待蒸馏种子

- [x] ATA：宝马 Landing Zone Accelerator 实战 — 已蒸馏到上方
- [ ] ATA：可口可乐云原生变革 — ATA 搜索未找到（可能标题不同）
- [ ] help.aliyun.com /zh/caf/ 全文蒸馏
- [ ] 资源目录 Resource Directory 最佳实践
- [ ] 不同行业 LZ 差异（金融 / 政企信创 / 互联网）
