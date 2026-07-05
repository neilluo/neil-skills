# 场景 × 产品矩阵速查 — cloud-product-mapping.md

> **定位**：业务场景 → 反查推荐产品组合的工具表。
> **使用方式**：方案设计模式 B 的第二步——拿到场景先查这张表，找到候选组合，再去 `aliyun-products.md` 查每个产品的能力卡。

## 主索引：场景 → 产品组合

### 计算 / 应用部署

| 场景 | 推荐产品组合 | 关键决策点 |
| --- | --- | --- |
| 单体应用快速上线 | ECS + RDS + OSS + SLB | 规模小 / 团队小 |
| 微服务化中型业务 | ACK + RDS + Tair + MSE + ALB | 服务治理需求 |
| Serverless 轻应用 | SAE / FC + RDS + OSS | 流量波动大、不愿管运维 |
| 弹性容器（突发） | ACK + ECI 弹性 / ACS | 大促、批量任务 |
| AI 推理服务 | PAI-EAS / 百炼 + GPU ECS / ACS-GPU | 模型自持 vs MaaS |
| 大数据离线计算 | MaxCompute + DataWorks | TB-PB 级离线 |
| 流计算 | Flink + Hologres + Lindorm | 实时 / 准实时 |

### 存储 / 数据

| 场景 | 推荐产品组合 | 关键决策点 |
| --- | --- | --- |
| 海量对象存储 | OSS + 生命周期 + CDN/DCDN | 标准/低频/归档分层 |
| 共享文件系统 | NAS（通用） / CPFS（高性能 AI） | 是否 HPC / AI 训练 |
| 高性能块存储 | ESSD PL1/2/3 | IOPS / 时延要求 |
| OLTP 数据库 | RDS / PolarDB | 单机 vs 分布式 |
| HTAP | Hologres / PolarDB-X / AnalyticDB | 实时分析 |
| 时序数据 | Lindorm 时序 / 时序数据库 TSDB | IoT / 监控 |
| KV 缓存 | Tair（增强 Redis） | 会话 / 计数 / 排行榜 |
| 向量检索 | Lindorm 向量 / Hologres 向量 / OpenSearch | RAG 场景 |
| 数据湖 | OSS + DLF + MaxCompute / EMR | 湖仓一体 |
| BI 报表 | Quick BI + Hologres / AnalyticDB | 自助分析 |

### 网络

> 详见 `aliyun-network-api-skills` skill 七大主题。

| 场景 | 推荐产品组合 | 关键决策点 |
| --- | --- | --- |
| 公网入口 | EIP + ALB + WAF | L7 应用 |
| L4 入口 | NLB / CLB | 高性能 / TCP |
| 公网出口 | NAT 网关 + EIP | 多机出网 |
| SNAT 高弹 | NAT 增强型 | 大规模出网 |
| 跨地域互联 | CEN（推荐）/ 高速通道 | 多 Region 业务 |
| 混合云接入 | 高速通道 / VPN / SAG | 物理专线 vs 加密隧道 vs 分支 |
| 出海加速 | GA + DCDN | 海外用户访问 |
| 私网服务暴露 | PrivateLink | 跨账号 / VPC 服务 |
| IP 治理 | IPAM + Anycast EIP | 大规模 IP 规划 |
| 网络可视 | NIS + VPC Flow Log | 诊断 / 排障 |

### 安全

| 场景 | 推荐产品组合 | 关键决策点 |
| --- | --- | --- |
| Web 应用防护 | WAF + DDoS 高防 + CDN | 应用层 + 网络层联动 |
| 主机安全 | 云安全中心 / Aegis | 漏洞 / 基线 / 入侵 |
| 内部边界 | Cloud Firewall + 安全组 | 微隔离 |
| 数据加密 | KMS + RDS TDE + OSS 加密 | 静态数据 |
| 运维堡垒 | 堡垒机 / 云盾访问代理 | 4A / 审计 |
| 合规审计 | ActionTrail + SLS + Config | 等保 / 监管 |

### AI / 大模型

| 场景 | 推荐产品组合 | 关键决策点 |
| --- | --- | --- |
| 通用对话 / Agent | 百炼（API 直调）+ Lindorm 向量 | MaaS 优先 |
| 私有化推理 | PAI-EAS + GPU ECS / ACS GPU | 自持模型 |
| 模型微调 | PAI-DLC + CPFS + OSS 模型仓 | 训练规模 |
| 多模态生成 | 通义万相 / DashScope + OSS | 创意生产 |
| 智能客服 / Agent | 百炼应用 / Agent 编排 | 工具调用复杂度 |
| RAG 知识库 | 百炼应用 + OSS + Lindorm 向量 | 切片 / 召回策略 |

### 行业典型

| 行业场景 | 推荐组合速记 |
| --- | --- |
| 出海 SaaS | 海外 Region + GA + DCDN + WAF 海外 + 合规日志 |
| 双活 / 异地多活 | CEN + DTS 双向 + 多活中间件（MSE/RocketMQ）+ 同/异地 RDS |
| 金融监管 | 金融云 / 等保三级 + KMS + 堡垒机 + 多账号隔离 + 合规审计 |
| 政企信创 | 专有云 / 飞天 + 信创实例 + 国密 + 等保 |
| 工业 IoT | IoT 平台 + Lindorm 时序 + Flink + DataV |

---

## 反向索引：产品 → 主要适用场景

### ECS
- 通用计算、单体应用、自定义 OS、需要本地盘 / 高性能存储

### ACK / ACS
- 微服务化业务、容器化部署、自动扩缩、CI/CD 集成

### FC / SAE
- 事件驱动、轻应用、Web 后端、ETL、定时任务

### RDS / PolarDB
- 通用 OLTP；需要规模扩展时上 PolarDB；分布式上 PolarDB-X

### Lindorm
- 宽表、时序、IoT、向量、文件 —— 多模融合；规模大于 RDS 时优先

### MaxCompute
- 离线大数据、数据仓库、ETL、数据治理（与 DataWorks 一起）

### Hologres
- 实时数仓、BI 提速、向量召回；与 MaxCompute 加速对接

### 百炼 vs PAI
- **百炼**：MaaS、应用编排、Agent、工具调用 —— 业务直接接入
- **PAI**：模型训练、私有化推理、大规模 GPU 资源管理

---

## 待补充

- [ ] 加入每条组合的"参考客户案例"列
- [ ] 加入"量级报价"列（小/中/大）
- [ ] 与竞品的对位（参考 `knowledge/competitor-cloud.md`）
