# Well-Architected 框架速查 — well-architected.md

> **来源**：阿里云 Well-Architected Framework（卓越架构框架），叠加 [Cloud Network Well-Architected Design](https://help.aliyun.com/zh/cloud-network-well-architected-design/) 与 [Aliyun Cloud Security Guide](https://help.aliyun.com/zh/acsg/)。
> **定位**：方案设计模式 B 的体检表 —— 任何方案都要按 5 大支柱过一遍。
> **使用方式**：方案设计时，每个支柱都要给出"做了什么 / 为什么这样做 / 量化指标"。

## 五大支柱总览

| 支柱 | 核心问题 | 关键阿里云产品 | 主要工具 |
| --- | --- | --- | --- |
| **成本 Cost** | 钱花在刀刃上 | RI / SCU / Savings Plan / 抢占式 / 资源弹性 | 费用中心、费用分析 |
| **可靠 Reliability** | 故障发生时仍可用 | 多可用区、跨地域、备份、容灾、限流 | ARMS、Chaos、AHAS |
| **性能 Performance** | 满足业务延时 / 吞吐 | 计算 / 存储 / 网络规格选型、缓存、CDN | ARMS、压测 PTS |
| **安全 Security** | 数据 / 系统不出事 | WAF、Anti-DDoS、Cloud Firewall、KMS、RAM、堡垒机 | 云安全中心 |
| **卓越运营 Operational Excellence** | 持续可观测、可演进 | SLS、ARMS、CloudMonitor、ROS、OOS、CloudOps | DevOps 工具链 |

---

## 1. 成本支柱

**核心原则**：用对、用足、用够。

**优化方向**：
- **采购模式优化**：按量 → RI（包年包月） / SCU / Savings Plan；非生产或可重启业务用抢占式实例
- **资源弹性**：固定基线 + 弹性峰值；ESS / ACK HPA / FC / SAE 自动扩缩
- **存储分层**：OSS 标准 → 低频 → 归档 → 冷归档；冷热数据生命周期策略
- **数据库优化**：只读实例分担读流量；PolarDB Serverless；存算分离归档冷数据
- **网络成本**：内网传输免费、跨地域走 CEN；流量包；CDN 回源比

**红线**：成本和性能 / 可靠存在 trade-off，不要为了省钱牺牲核心 SLA。

## 2. 可靠支柱

**核心原则**：假设一切都会坏，问题是怎么坏、坏了多久。

**层次**：
- **基础设施层**：多可用区部署（同城三 AZ）、跨地域容灾（异地）
- **数据层**：备份策略（RPO）、副本同步（RTO）、跨地域复制（OSS / RDS / 数据库）
- **应用层**：无状态化、健康检查、灰度发布、蓝绿、金丝雀
- **流量层**：限流（Sentinel / AHAS / ALB）、熔断、降级、削峰（MQ）
- **演练**：故障注入（AHAS Chaos）、定期演练

**典型架构**：
- 同城双活 / 同城三可用区
- 异地多活（参考淘宝海外 TaobaoBonus 双活模式）

## 3. 性能支柱

**核心原则**：先量化目标（QPS / TPS / P95 时延 / 吞吐 / 数据量），再做选型。

**计算性能**：
- ECS 实例族选择（通用 / 计算 / 内存 / GPU / 大数据）
- 容器：ACK Pro vs ACS（Serverless）vs ECI 弹性扩
- Serverless：FC（毫秒级冷启动 + 预留实例）

**存储性能**：
- OSS：标准 + 加速（OSS Accelerate）
- ESSD：PL0/1/2/3 不同 IOPS / 时延档位
- CPFS：高性能并行文件系统（AI 训练、HPC）

**网络性能**：
- VPC 内网：单 VPC 25Gbps - 100Gbps + 弹性
- 跨地域：CEN + GA 加速
- 边缘：DCDN / ENS 全球加速

**数据库性能**：
- 读写分离、分库分表、HTAP（Hologres / PolarDB-X）
- 缓存：Tair（Redis 增强）
- 向量检索：Lindorm 向量 / Hologres / OpenSearch

## 4. 安全支柱

**对应文档**：[阿里云安全建设指南 ACSG](https://help.aliyun.com/zh/acsg/)

**纵深防御层次**：

1. **身份与访问** — RAM / 主子账号 / SSO / MFA / RAM Policy 最小权限
2. **网络边界** — VPC 隔离、安全组、NACL、Cloud Firewall
3. **应用边界** — WAF（OWASP Top 10）、API 网关
4. **抗攻击** — Anti-DDoS（高防 / 原生防护）、Bot 管理
5. **主机** — 云安全中心 / Aegis（漏洞、基线、入侵）
6. **数据** — KMS 加密、数据脱敏、DLP、审计 SLS
7. **日志审计** — 操作审计 ActionTrail、SLS 长期归档、合规检查 Config

**合规框架**：
- 国内：等保 2.0（一/二/三/四级）、关基保护、数据安全法、个人信息保护法
- 海外：GDPR、CCPA、HIPAA、SOC2
- 行业：金融监管、车联网、医疗

## 5. 卓越运营支柱

**核心原则**：可观测、可自动化、可演进。

**可观测三柱**：
- **指标 Metrics**：CloudMonitor / ARMS / Prometheus 服务
- **日志 Logs**：SLS（采集 + 检索 + 告警 + 投递）
- **链路 Tracing**：ARMS Application Real-Time Monitoring（全栈）

**自动化运维**：
- IaC：ROS（资源编排）、Terraform Provider
- 运维编排：OOS（Operation Orchestration Service）
- CI/CD：云效、Jenkins on K8s、ACR 制品仓
- GitOps：ArgoCD / Flux

**变更管理**：
- 灰度发布、蓝绿、金丝雀
- 回滚预案、变更窗口
- ChatOps / 应急响应

---

## 网络架构设计指南（Network WAD）速查

**对应文档**：https://help.aliyun.com/zh/cloud-network-well-architected-design/

**七大场景**（与 `aliyun-network-api-skills` skill 完全对齐）：
1. 公网访问（出 / 入）—— EIP / NAT / SLB
2. 负载均衡选型 —— L4（CLB/NLB） / L7（ALB） / L3（GWLB）
3. 跨地域互联 —— CEN / GA / 高速通道
4. 混合云接入 —— 高速通道 / VPN / 智能接入网关
5. VPC 间 / 服务间私网打通 —— 对等连接 / PrivateLink / CEN
6. IP 地址管理 —— IPAM / Anycast EIP
7. 网络可视化与诊断 —— NIS / VPC Flow Logs / CEN 流量分析

**详细产品组合见** [references/cloud-product-mapping.md](cloud-product-mapping.md) 网络章节。

---

## 用法清单

方案设计时把这张清单走一遍：

- [ ] 成本：采购模式 + 弹性 + 存储分层是否考虑
- [ ] 可靠：单可用区 / 多可用区 / 异地容灾的级别说清楚
- [ ] 性能：核心指标量化（QPS / 时延 / 数据量）+ 容量预估
- [ ] 安全：6 层防御每一层是否覆盖 + 合规要求列出
- [ ] 运营：监控 / 日志 / 链路 + IaC / CI-CD / 变更管理
