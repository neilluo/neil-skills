# 阿里云产品知识库 — aliyun-products.md

> **定位**：每个阿里云产品的“能力卡”——能做什么 / 不能做什么 / 选型场景 / 报价量级 / 避坑要点。
> **更新方式**：每蒸馏一个产品的官方文档或 ATA 文章后，落到对应小节。
> **写法**：保持可扫读，限制单产品 < 200 字 + 链接索引；详细参数走 help.aliyun.com 实时查。

**↔️ Cross-references**：
- 场景应用 → [cloud-solutions.md](cloud-solutions.md)(产品如何组合成方案)
- 竞品对位 → [competitor-cloud.md](competitor-cloud.md)(同类产品跨云对比)
- 客户实践 → [company-profiles.md](company-profiles.md)(哪些客户在用)
- AI 产品演进 → [ai-trends.md](ai-trends.md)(百炼/PAI/通义变化趋势)
- 选型矩阵 → [../references/cloud-product-mapping.md](../references/cloud-product-mapping.md)(场景反查产品)

**[[wikilink]] 实体索引**：本文件核心实体 → [[ECS]] [[ACK]] [[ACS]] [[FC]] [[PolarDB]] [[RDS]] [[Tair]] [[Hologres]] [[MaxCompute]] [[百炼]] [[PAI]] [[MSE]] [[RocketMQ]] [[Kafka]] [[WAF]] [[SLB]] [[OSS]] [[CDN]] [[Flink]] [[DataWorks]] [[StarRocks]]

---

## 计算

### ECS（弹性计算服务）

**官方定位**：阿里云核心 IaaS，按需获取虚拟机实例。
**能做**：
- 7 代实例族覆盖通用/计算/内存/大数据/本地盘/GPU/FPGA
- 秒级创建、分钟级交付；支持抢占式实例（Spot）降本 60-90%
- 弹性网卡、安全组、置放群组、专有宿主机
- 存储：系统盘/数据盘 ESSD PL0-PL3；本地盘 SSD/HDD
- 镜像市场、自定义镜像、快照

**不擅长**：流量波动极大（秒级伸缩走 FC/ECI）；纯容器化业务（ACK/ACS 更合适）

**典型选型场景**：传统应用迁移、自定义 OS/内核、GPU 独占训练、HPC
**对位竞品**：AWS EC2 / Azure VM / GCP Compute Engine
**报价量级**：通用型 2c4g ≈ 130 元/月（按量 0.28 元/时）；包年包月 7 折起
**避坑**：实例规格停售迁移（g5→g7/g8a）；跨可用区不支持 ENI 直迁；突发型 t6 有 CPU 积分限制
**官方文档**：https://help.aliyun.com/zh/ecs/
**证据等级**：[官方]
**最近更新**：2026-06-17（help.aliyun.com 蒸馏）

---

### ACK（容器服务 Kubernetes）

**官方定位**：企业级 Kubernetes 托管服务，支持 Pro/Standard/Serverless(ASK) 三种形态。
**能做**：
- 托管控制面（Pro 版 SLA 99.95%）+ 自动升级 + 安全加固
- 节点池（普通/托管/GPU/ARM/抢占式）；集群自动伸缩 CA/VPA/HPA
- 容器网络 Terway（ENI 直通 VPC 网络）、Flannel
- 安全沙箱容器（runV/Kata）、机密计算 TEE
- 生态集成：ARMS、SLS、ACR、MSE（Nacos/网关）、服务网格 ASM

**不擅长**：只跑几个容器、不想管节点（→ ACS/SAE）；极简函数（→ FC）

**典型选型场景**：微服务集群化部署、AI 推理弹性（GPU + 分时调度）、混合云多集群
**对位竞品**：AWS EKS / Azure AKS / GCP GKE
**报价量级**：Pro 版集群管理费 0.64 元/小时（≈ 460 元/月）+ Worker 节点 ECS 费用 [官方]
**避坑**：Terway vs Flannel 选对（Terway 网络策略强但 ENI 配额有限）；节点维护需关注 K8s 版本 EOL
**官方文档**：https://help.aliyun.com/zh/ack/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ACS（容器计算服务）

**官方定位**：Serverless Kubernetes 运行时，无需管理节点。
**能做**：
- 100% Serverless，无 Node 运维；Pod 秒级启动
- 兼容标准 K8s API（kubectl/Helm/ArgoCD 直接使用）
- GPU Serverless（分时共享/整卡）
- 自动弹性（基于指标自动伸缩 Pod）
- 原生对接 VPC/SLB/SLS/ARMS

**不擅长**：需要定制 Node OS/内核驱动（→ ACK）；长期稳态大规模跑（成本高于 ACK+Reserved）

**典型选型场景**：AI 推理弹性、CI/CD Job Runner、事件驱动型批处理、快速 PoC
**对位竞品**：AWS Fargate / Azure Container Apps / GCP Cloud Run（K8s 模式）
**报价量级**：按 Pod vCPU/Memory 秒计费；1 vCPU + 2GiB ≈ 0.0001 元/秒
**避坑**：Pod 启动冷启动（镜像缓存可优化）；大量常驻 Pod 成本高于 ACK 包年节点
**官方文档**：https://help.aliyun.com/zh/acs/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ECI（弹性容器实例）

**官方定位**：无服务器容器实例，按需创建，秒级计费。
**能做**：
- 无需管理底层 ECS，直接运行容器镜像
- 用于 ACK 的虚拟节点弹性扩容（大促峰值）
- 支持 GPU 实例（AI 推理突发）
- 与 VPC/SLS/ARMS 原生集成

**不擅长**：长期运行（成本高）；需要持久化本地存储（→ ECS + 本地盘）

**典型选型场景**：ACK 弹性节点（Virtual Kubelet）、批量计算、CI/CD 构建
**对位竞品**：AWS Fargate / Azure Container Instances
**报价量级**：按 vCPU/Memory/GPU 秒计费
**避坑**：镜像大则冷启动慢（用 ImageCache 加速）；ECI Pod 没有 SSH
**官方文档**：https://help.aliyun.com/zh/eci/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### SAE（Serverless 应用引擎）

**官方定位**：面向应用的 Serverless PaaS，无需管理集群和节点。
**能做**：
- 支持 Java/PHP/Node/Python/Go/自定义镜像
- 内置微服务治理（注册发现、配置、灰度）
- 自动弹性（定时/指标触发）、最小缩到 0 实例
- 内置日志、监控、链路追踪
- 支持多发布策略（灰度、蓝绿）

**不擅长**：极端定制化（自定义内核/GPU/特殊网络）→ ACK；纯函数/事件驱动 → FC

**典型选型场景**：中小型 Web 应用、Spring Cloud 微服务快速上线、运维人力不足团队
**对位竞品**：AWS App Runner / Azure Container Apps / GCP Cloud Run
**报价量级**：1 vCPU + 2GiB ≈ 0.12 元/时（支持包月 8 折）；缩到 0 时不收费
**避坑**：冷启动时间（Java 应用需预热或用 GraalVM）；VPC 内网访问需配置关联
**官方文档**：https://help.aliyun.com/zh/sae/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### FC（函数计算）

**官方定位**：事件驱动的 Serverless 计算平台，毫秒级弹性。
**能做**：
- 毫秒级冷启动（预留实例可实现零冷启动）
- 支持 HTTP / API / OSS / MQ / Timer / EventBridge 等 40+ 触发器
- 内置 GPU（推理场景）
- Custom Runtime（任意语言/框架/容器镜像）
- 弹性扩缩（0→N 实例，并发度控制）

**不擅长**：长时间运行任务 >15 分钟（→ ECS/ACS）；复杂微服务治理（→ ACK/SAE）

**典型选型场景**：API 后端、Webhook、ETL 管道、定时任务、AI 推理（短时突发）
**对位竞品**：AWS Lambda / Azure Functions / GCP Cloud Functions
**报价量级**：按调用次数 + 执行时间 + 内存计费；100万次调用 ≈ 1.33 元；预留实例另计
**避坑**：并发配额默认 300（需申请提升）；大依赖包影响冷启动；注意单实例多并发模式
**官方文档**：https://help.aliyun.com/zh/fc/
**证据等级**：[官方+实战]
**最近更新**：2026-06-17

**跨云迁移实战** [实战-ATA 11020645626]：
- AWS Lambda → FC：800+ 函数迁移合并为 600+（零数据丢失）
- 运行时选择：custom.debian10（持久 HTTP 服务器）优于原生 Python runtime
- Layer 优化：50MB→5MB 包体，冷启动降 30-50%
- 无预留冷启动：7900ms（需预留实例或 Initializer 预热连接池）
- 跨云 VPN 延迟：40ms+（北京AWS→深圳阿里云）
- 配套工具：Cloud Native API Gateway + Serverless Devs + ARMS + SLS

---

### ESS（弹性伸缩）

**官方定位**：自动管理 ECS/ECI 实例数量的弹性服务。
**能做**：
- 定时伸缩 + 动态伸缩（CPU/内存/自定义指标）+ 预测伸缩
- 多可用区调度 + 多实例规格兜底
- 实例创建时自动加入 SLB 后端 + 添加 RDS 白名单
- 生命周期钩子（优雅缩容）
- 最新支持容器化（与 ACK 节点池联动）

**不擅长**：单独使用（只是伸缩调度器，需搭配 ECS/SLB 等）

**典型选型场景**：Web 应用峰谷弹性、大促扩缩容、定时跑批任务
**对位竞品**：AWS Auto Scaling / Azure VMSS / GCP MIG
**报价量级**：服务本身免费；只按实际创建的 ECS 实例计费
**避坑**：冷却时间设置不当导致频繁伸缩抖动；多 AZ 最小实例数需覆盖高可用
**官方文档**：https://help.aliyun.com/zh/ess/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 计算选型快速决策

```
需要 K8s API？
├── Yes → 要管节点？
│   ├── Yes → ACK Pro
│   └── No → ACS
├── No → 要管实例/OS？
│   ├── Yes → ECS + ESS
│   └── No → 需要微服务治理？
│       ├── Yes → SAE
│       └── No → 事件驱动/短任务？
│           ├── Yes → FC
│           └── No → SAE 或 ECS
```

---

## 存储

### OSS（对象存储服务）

**官方定位**：海量、安全、低成本、高可靠的云存储，支持 99.9999999999%（12个9）数据持久性。
**能做**：
- 四种存储类型：标准 / 低频访问 / 归档 / 冷归档（深度归档）
- 生命周期管理自动降冷
- 跨地域复制（CRR）、版本控制、WORM 合规保留
- 图片/视频处理、数据湖直接分析（DLF/MaxCompute/Spark）
- 传输加速、CDN 回源、事件通知（FC/MNS/EventBridge）

**不擅长**：低延迟随机读写（→ ESSD/NAS）；POSIX 文件语义（→ NAS）；强事务（→ 数据库）

**典型选型场景**：网站静态资源、日志归档、大数据存储底座、备份/容灾、数据湖
**对位竞品**：AWS S3 / Azure Blob / GCP Cloud Storage
**报价量级**：标准 0.12 元/GB/月；低频 0.08；归档 0.033；冷归档 0.015
**避坑**：跨区域流量费易忽略；小文件大量 LIST 操作费用可观；归档取回需等待
**官方文档**：https://help.aliyun.com/zh/oss/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### NAS（文件存储）

**官方定位**：支持 NFS/SMB 协议的共享文件存储。
**能做**：
- 通用型（SSD/容量型）：POSIX 兼容，多实例共享挂载
- 极速型（NAS Plus）：低延迟高 IOPS（数据库/容器持久卷）
- CPFS 版本（高性能并行文件系统）
- 自动弹性容量（无需预置）、快照、加密、跨可用区

**不擅长**：单机高 IOPS 块存储（→ ESSD）；对象存储海量小文件（→ OSS）

**典型选型场景**：容器持久卷（ACK PV）、共享配置/代码、CMS 媒体文件、AI 训练数据集（通用型）
**对位竞品**：AWS EFS / Azure Files / GCP Filestore
**报价量级**：通用容量型 0.35 元/GB/月；通用性能型 1.85；极速型 2.6
**避坑**：容量型时延较高（10ms 级）不适合数据库；跨可用区访问有额外流量费
**官方文档**：https://help.aliyun.com/zh/nas/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### CPFS（并行文件存储）

**官方定位**：高性能并行文件系统，专为 AI 训练和 HPC 设计。
**能做**：
- 聚合带宽 100GB/s+，百万级 IOPS
- 支持 POSIX / RDMA 客户端
- 原生支持 GPU 集群多机并行读写训练数据
- 容量最大数十 PB

**不擅长**：通用 Web 文件共享（overkill）；小规模场景（→ NAS）

**典型选型场景**：大模型训练数据存储、HPC（气象/基因/物理模拟）、渲染农场
**对位竞品**：AWS FSx for Lustre / Azure Managed Lustre / GCP Parallelstore
**报价量级**：按容量+带宽计费；100TB 起步，约数万元/月
**避坑**：客户端需安装专用驱动；网络要求高（RDMA/eRDMA 推荐）；起步规模大
**官方文档**：https://help.aliyun.com/zh/cpfs/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### EBS（块存储 / 云盘）

**官方定位**：为 ECS 提供持久化块存储，类比物理硬盘。
**能做**：
- ESSD 系列：PL0(10000 IOPS) / PL1(50000) / PL2(100000) / PL3(1000000)
- ESSD AutoPL：自动突发性能
- 高效云盘、SSD 云盘（旧型号）
- 快照（增量）、跨地域复制、加密
- 多重挂载（共享块存储）

**不擅长**：跨实例共享文件（→ NAS/CPFS）；大容量低成本归档（→ OSS）

**典型选型场景**：数据库数据盘、系统盘、高性能 IO 需求（Oracle/MySQL）
**对位竞品**：AWS EBS / Azure Managed Disks / GCP Persistent Disk
**报价量级**：ESSD PL1 1元/GB/月；PL0 0.5；高效 0.35
**避坑**：PL 等级与容量挂钩（PL2 需≥461GB）；跨 AZ 不可直接挂载；快照增量但首次全量大
**官方文档**：https://help.aliyun.com/zh/ebs/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Tablestore（表格存储）

**官方定位**：Serverless 多模型数据库，支持宽表/时序/消息模型。
**能做**：
- Schema-free 宽列存储（万亿行、PB 级）
- 内置时序引擎（IoT 设备数据）
- 通道服务（CDC 流式消费变更）
- 多元索引（全文/范围/地理/嵌套）
- Serverless 完全按量

**不擅长**：复杂 SQL（→ RDS/PolarDB）；强事务（ACID 跨行有限）；标准 Redis 协议（→ Tair）

**典型选型场景**：IoT 设备时序数据、消息/Feed 流、元数据宽表、日志索引
**对位竞品**：AWS DynamoDB / Azure Cosmos DB (Table API) / GCP Bigtable
**报价量级**：CU 计费（读/写吞吐 + 存储）；Serverless 起步极低
**避坑**：查询模式需提前设计主键 + 二级索引；跨分区事务受限
**官方文档**：https://help.aliyun.com/zh/tablestore/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 存储选型快速决策

```
需要什么访问方式？
├── HTTP RESTful API → OSS
├── POSIX 文件系统 →
│   ├── AI 训练 / HPC → CPFS
│   └── 通用共享 → NAS
├── 块设备（挂载磁盘） → EBS（ESSD）
└── NoSQL 宽表/时序 → Tablestore
```

---

## 网络

### VPC（专有网络）

**官方定位**：隔离的云上私有网络环境，所有云资源的网络基础。
**能做**：
- 自定义 CIDR（10/172/192 段）、交换机、路由表
- 安全组（实例级防火墙）、网络 ACL（子网级）
- 弹性网卡 ENI（多 IP、安全组隔离）
- 流日志（VPC Flow Logs）
- 辅助 CIDR 扩展

**不擅长**：跨 VPC 互通需额外组件（CEN/对等连接/PrivateLink）

**典型选型场景**：所有云上业务的基础网络隔离单元
**对位竞品**：AWS VPC / Azure VNet / GCP VPC
**报价量级**：VPC/交换机免费；弹性网卡有配额限制
**避坑**：CIDR 规划需提前（不支持缩小）；交换机跨 AZ 不共享；安全组规则数有上限
**官方文档**：https://help.aliyun.com/zh/vpc/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### CEN（云企业网）

**官方定位**：全球多 VPC / 多地域 / 多账号的企业级互联网络。
**能做**：
- 转发路由器 TR（地域级网络核心，支持路由策略/流量分析）
- 跨地域带宽（阿里云骨干网，低延迟高可靠）
- 多账号跨 VPC 互通（支持 Resource Directory 体系）
- VBR/VPN 网关接入（混合云）
- 流量调度、分段路由、ER 策略

**不擅长**：单 VPC 内部路由（VPC 自身即可）；L7 应用级路由（→ ALB/MSE 网关）

**典型选型场景**：多地域组网、集团多账号互通、混合云 Hub-Spoke、Landing Zone 网络底座
**对位竞品**：AWS Transit Gateway / Azure Virtual WAN / GCP Network Connectivity Center
**报价量级**：转发路由器基础版免费；企业版按连接数+流量计费；跨地域带宽 ≈ 6-18 元/Mbps/天
**避坑**：跨地域带宽需提前购买（峰值不够会丢包）；路由条目有上限需规划
**官方文档**：https://help.aliyun.com/zh/cen/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### GA（全球加速）

**官方定位**：基于阿里云全球网络加速用户访问，智能路由就近接入。
**能做**：
- 全球 Anycast 加速 IP（用户就近接入 POP 点）
- 智能路由（选择最优路径）
- 跨地域四层/七层加速
- 支持 TCP/UDP/HTTP/HTTPS
- 终端节点组（多地域后端自动切换）

**不擅长**：替代 CDN 做静态内容分发（→ DCDN/CDN）；VPC 内部加速（→ CEN）

**典型选型场景**：出海应用加速、全球化 SaaS、游戏加速、跨境办公
**对位竞品**：AWS Global Accelerator / Azure Front Door / GCP Cloud CDN + LB
**报价量级**：实例费 ≈ 300 元/月 + 带宽费（按地域）
**避坑**：与 CDN/DCDN 定位不同（GA=网络层加速，CDN=内容缓存）；需提前备案
**官方文档**：https://help.aliyun.com/zh/ga/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### CLB（传统型负载均衡）

**官方定位**：L4 负载均衡（TCP/UDP），高性能转发。
**能做**：支持 TCP/UDP 四层转发、会话保持、健康检查、跨可用区容灾
**不擅长**：L7 高级路由（→ ALB）；超大规模连接（→ NLB）

**典型选型场景**：传统四层转发、已有存量配置
**对位竞品**：AWS NLB/CLB Legacy
**报价量级**：实例费 + LCU 计费；共享型免费但有规格限制
**避坑**：共享型实例性能不保证；新项目推荐 NLB 替代
**官方文档**：https://help.aliyun.com/zh/slb/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ALB（应用型负载均衡）

**官方定位**：L7 负载均衡，支持 HTTP/HTTPS/gRPC/WebSocket 高级路由。
**能做**：
- 基于 Host/Path/Header/Cookie/Query 的高级路由
- 内置 WAF 联动、限流、重定向
- 支持灰度发布（权重路由）
- gRPC 原生支持
- 多证书 SNI、HTTPS 卸载

**不擅长**：纯四层 TCP/UDP（→ NLB）；全球加速入口（→ GA）

**典型选型场景**：微服务 API 网关、K8s Ingress（ACK ALB Ingress Controller）、Web 应用
**对位竞品**：AWS ALB / Azure Application Gateway / GCP HTTP(S) LB
**报价量级**：实例费 ≈ 37 元/月 + LCU 计费
**避坑**：ALB 实例有可用区属性；gRPC 需 HTTPS 监听；与 ACK Ingress Controller 版本需匹配
**官方文档**：https://help.aliyun.com/zh/alb/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### NLB（网络型负载均衡）

**官方定位**：超高性能 L4 负载均衡，单实例亿级并发连接。
**能做**：
- TCP/UDP/TCPSSL 四层转发
- 单实例支持 1 亿并发连接、100Gbps 带宽
- DSR（Direct Server Return）模式降低延迟
- 跨可用区高可用
- 支持 PrivateLink 作为服务提供者

**不擅长**：L7 路由规则（→ ALB）；HTTP Header 级操作（→ ALB）

**典型选型场景**：高性能游戏网关、IoT 百万连接、数据库代理、Kubernetes L4 Service
**对位竞品**：AWS NLB / Azure Load Balancer / GCP Network LB
**报价量级**：实例费 ≈ 14 元/月 + LCU 计费
**避坑**：NLB 目前不支持 HTTP 健康检查（用 TCP 健康检查替代）
**官方文档**：https://help.aliyun.com/zh/nlb/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### NAT 网关

**官方定位**：VPC 内多实例共享公网出入口。
**能做**：SNAT（多实例共享出公网）、DNAT（端口映射入公网）、增强型百 Gbps 级、按量/包年
**不擅长**：L7 流量调度（→ ALB）

**典型选型场景**：VPC 统一出网、多实例共享 EIP、安全出口收敛
**对位竞品**：AWS NAT Gateway / Azure NAT Gateway
**报价量级**：增强型 ≈ 43 元/月 + 流量费
**避坑**：SNAT 连接数有限制（默认 100 万/s）；大规模出网需多 NAT 分担
**官方文档**：https://help.aliyun.com/zh/nat-gateway/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### VPN 网关

**官方定位**：通过加密隧道连接云上 VPC 与线下 IDC/分支机构。
**能做**：IPsec VPN（站点到站点）、SSL VPN（P2S 远程接入）、BGP 动态路由、双隧道冗余
**不擅长**：大带宽专线需求（→ 高速通道物理专线）；跨地域骨干互联（→ CEN）

**典型选型场景**：混合云加密互通（备选方案/低成本方案）、远程办公 VPN
**对位竞品**：AWS Site-to-Site VPN / Azure VPN Gateway
**报价量级**：5Mbps ≈ 375 元/月
**避坑**：IPsec 受互联网质量影响（抖动/丢包）；生产环境推荐专线+VPN备份双链路
**官方文档**：https://help.aliyun.com/zh/vpn-gateway/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 高速通道（Express Connect）

**官方定位**：物理专线接入阿里云，提供高质量私网连接。
**能做**：独享/共享物理端口（1G/10G/100G）、VBR 虚拟边界路由器、BGP、冗余链路
**不擅长**：快速部署（物理专线需数周施工）；小带宽临时连接（→ VPN）

**典型选型场景**：金融/政企强合规专线互联、IDC 混合云、大带宽数据同步
**对位竞品**：AWS Direct Connect / Azure ExpressRoute / GCP Cloud Interconnect
**报价量级**：独享端口 1G ≈ 1500 元/月 + 出方向流量
**避坑**：冗余设计（双专线+VPN 备份）；跨地域需 CEN 中转
**官方文档**：https://help.aliyun.com/zh/express-connect/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### PrivateLink

**官方定位**：通过私网将服务安全暴露给其他 VPC/账号消费，无需公网。
**能做**：
- 服务提供者创建终端节点服务 → 消费者创建终端节点 → 私网直通
- 跨账号/跨 VPC 服务暴露（无需 VPC Peering/CEN 全通）
- 支持 NLB/CLB/ALB 作为后端

**不擅长**：全网互通（→ CEN）；公网暴露（→ EIP/ALB）

**典型选型场景**：SaaS 提供方暴露服务、跨账号微服务内部调用、安全合规（数据不出 VPC）
**对位竞品**：AWS PrivateLink / Azure Private Link
**报价量级**：终端节点费 + 数据处理费（约 0.01 元/GB）
**避坑**：每个终端节点服务需绑定 NLB/ALB；可用区需对齐
**官方文档**：https://help.aliyun.com/zh/privatelink/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Anycast EIP

**官方定位**：全球 Anycast 弹性公网 IP，用户就近接入。
**能做**：全球多 POP 点同一 IP 地址；自动就近路由；抗 DDoS 能力增强
**不擅长**：区域限定服务（普通 EIP 即可）

**典型选型场景**：全球化应用统一 IP 入口、游戏加速、DNS 权威解析
**对位竞品**：AWS Global Accelerator 的 Anycast IP
**报价量级**：实例费 + 带宽费
**官方文档**：https://help.aliyun.com/zh/anycast-eip/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 网络选型快速决策

```
跨地域互联？
├── Yes → CEN（企业级，路由策略丰富）
│         + GA（面向终端用户加速）
├── No → 混合云接入？
│   ├── 物理专线 → 高速通道
│   ├── 加密隧道 → VPN 网关
│   └── 分支自组网 → 智能接入网关
└── VPC 间服务暴露？
    ├── 全互通 → CEN 或 VPC Peering
    └── 定向服务 → PrivateLink

负载均衡选型？
├── L7（HTTP/gRPC） → ALB
├── L4 高性能 → NLB
└── 存量迁移 → CLB（新项目不推荐）
```

---

## 数据库

### RDS（关系数据库服务）

**官方定位**：全托管关系数据库，支持 MySQL / PostgreSQL / SQL Server / MariaDB。
**能做**：
- 自动备份、秒级快照恢复、跨地域灾备
- 只读实例（最多 10 个）、读写分离代理（Proxy）
- 高可用：双节点/三节点/多可用区
- 内核小版本自动升级、参数模板
- 加密（TDE + SSL）、审计日志

**不擅长**：超大规模写入（→ PolarDB）；NoSQL 场景（→ Lindorm/Tair）；实时分析（→ Hologres）

**典型选型场景**：常规 OLTP、中小型 Web 应用、ERP/CRM 后端
**对位竞品**：AWS RDS / Azure SQL Database / GCP Cloud SQL
**报价量级**（三引擎 × 三形态，包年包月 2c4g 参考）[[官方]][2026-06]:
| 引擎 | 基础版（单节点） | 高可用版（主备） | 集群版（三节点） |
| --- | --- | --- | --- |
| MySQL | ~150元/月 | ~480元/月 | ~700元/月 |
| PostgreSQL | ~140元/月 | ~460元/月 | ~680元/月 |
| SQL Server | - | ~800元/月(含授权) | - |
- Serverless 模式：MySQL 支持按 RCU 秒计费，自动启停
- 包年优惠：1年付直降 12%起，5年付降 37%起
**避坑**：实例规格升级需短暂重启；跨可用区需手动切换（高可用版自动）；连接数有上限；基础版无高可用仅适合开发测试
**官方文档**：https://help.aliyun.com/zh/rds/
**证据等级**：[官方]
**最近更新**：2026-06-28（报价多形态刷新）

---

### PolarDB

**官方定位**：云原生分布式关系数据库，存算分离架构，兼容 MySQL/PG/Oracle。
**能做**：
- 存算分离：存储最大 100TB、计算秒级弹性
- 读写分离（最多 15 只读节点）+ 全局一致性读
- Serverless 模式（自动启停 + 按秒计费）
- 全球数据库（跨地域低延迟读写）
- HTAP 能力（行列混存、并行查询）
- PolarDB-X（分布式版）：水平扩展、分库分表兼容 MySQL

**不擅长**：极简场景 RDS 够用时性价比低；NoSQL（→ Lindorm）

**典型选型场景**：中大型 OLTP（单实例超出 RDS 上限）、读多写少高弹性、Oracle 迁移
**对位竞品**：AWS Aurora / Azure Cosmos DB (Relational) / GCP AlloyDB
**报价量级**（三版本，包年包月参考）[官方][2026-06]:
| 版本 | 4c16g 参考 | 存储单价 | Serverless |
| --- | --- | --- | --- |
| PolarDB MySQL | ~2,300元/月 | 按实际存储 0.0016元/GB/小时 | 按 PCU 秒计费（0.000134元/PCU/秒） |
| PolarDB PostgreSQL | ~2,100元/月 | 同上 | 同上 |
| PolarDB-X（分布式） | ~3,500元/月（2CN+2DN） | 按节点数 | 不支持 Serverless |
- 多主架构（Multi-Master）已发布，支持多点写入
- TPC-C 世界纪录（2025 登顶）
**避坑**：PolarDB-X 分布式事务有性能折损；Serverless 冷启动约 5-10s；MySQL 版与 PG 版不可互转
**官方文档**：https://help.aliyun.com/zh/polardb/
**证据等级**：[官方]
**最近更新**：2026-06-28（报价三版本刷新）

---

### Lindorm

**官方定位**：多模数据库——宽表 + 时序 + 搜索 + 文件 + 向量五引擎融合。
**能做**：
- 宽表引擎（兼容 HBase/Cassandra API，万亿行级别）
- 时序引擎（每秒千万级写入，IoT/监控首选）
- 搜索引擎（全文检索，兼容 OpenSearch/ES API）
- 向量引擎（RAG/相似性检索，十亿级向量）
- 文件引擎（HDFS 兼容大文件存储）
- 统一实例多引擎，数据互通

**不擅长**：标准 SQL OLTP（→ RDS/PolarDB）；复杂 Join（→ Hologres/AnalyticDB）

**典型选型场景**：IoT 时序数据、用户画像宽表、RAG 向量检索、日志搜索、HBase 迁移
**对位竞品**：AWS DynamoDB + Timestream + OpenSearch / Azure Cosmos DB
**报价量级**：按 CU + 存储计费；宽表 4c8g ≈ 1600 元/月
**避坑**：多引擎间数据同步有延迟；API 兼容≠100%（HBase 0.98 API 差异）
**官方文档**：https://help.aliyun.com/zh/lindorm/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Tair（云数据库 Redis 版）

**官方定位**：兼容 Redis 的增强型内存数据库，性能增强 + 持久化 + 多模型。
**能做**：
- 100% 兼容 Redis 5/6/7 协议
- 增强数据结构：TairHash/TairString/TairZset/TairGIS/TairBloom/TairSearch/TairVector
- 三种形态：内存型（DRAM，性能3倍）、持久内存型（Intel Optane，兼顾成本与持久化）、磁盘型（SSD，大容量低成本）
- 集群架构（最大 4TB / 1024 分片 / 100万+ QPS）
- 全球分布式版（多活写入，异地 <100ms 同步）
- 向量检索（TairVector，支持 HNSW/FLAT 索引）

**性能数据** [官方]：
- 内存型：同规格 Redis 开源版 3 倍性能，多线程模型（主线程+4 IO 线程+BIO），单节点 QPS 超 20 万
- 持久内存型：社区版 90% 性能，命令级持久化（重启不丢数据）
- 磁盘型：社区版 60% 性能，TB 级容量，成本为内存型 1/5
- 延迟：内存型亚毫秒级（P99 < 1ms），持久内存型 <2ms

**不擅长**：复杂 SQL 查询（→ RDS）；大容量冷数据存储（→ Lindorm/OSS）

**典型选型场景**：缓存/会话/排行榜/计数器/分布式锁/限流/实时特征存储/向量检索
**游戏场景用法**：排行榜（ZSet，QPS 20万+）、匹配队列（List/Stream）、会话缓存（Hash）、地理围栏（GIS模块）、在线计数（String原子操作）
**对位竞品**：AWS ElastiCache for Redis / MemoryDB / Azure Cache for Redis / GCP Memorystore
**报价量级**：内存型标准版 1GB ≈ 180 元/月；集群 64GB ≈ 8000 元/月；持久内存型降低约 30%
**避坑**：大 Key（>10MB）风险导致阻塞、热 Key 需打散（单 Key QPS >10万时）、全球同步有最终一致性窗口、磁盘型不适合低延迟场景
**官方文档**：https://help.aliyun.com/zh/tair/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### AnalyticDB（MySQL 版 / PostgreSQL 版）

**官方定位**：实时数据仓库 / OLAP 引擎。
**能做**：
- MySQL 版：MPP 架构，PB 级离线+实时，兼容 MySQL 协议，弹性扩缩
- PostgreSQL 版：MPP + 向量 + 时空 + JSON，兼容 PG 生态
- 都支持实时写入+实时查询
- 与 DTS/DataWorks/Flink 无缝集成

**不擅长**：高并发点查（→ Tair/Lindorm）；事务型 OLTP（→ RDS/PolarDB）

**典型选型场景**：BI 分析、实时报表、数据仓库加速、日志分析
**对位竞品**：AWS Redshift / Azure Synapse / GCP BigQuery
**报价量级**：弹性模式 16c64g ≈ 3400 元/月
**避坑**：写入量大时需调整分区键；与 Hologres 定位有重叠（选型需明确）
**官方文档**：https://help.aliyun.com/zh/analyticdb/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Hologres

**官方定位**：实时数仓，毫秒级交互式分析，MaxCompute 加速器。
**能做**：
- 行存 + 列存混合，HSAP（Serving + Analytical）
- MaxCompute 外表直读（零 ETL 加速）
- 实时写入+实时查询（亚秒级）
- 向量检索（Proxima 引擎）
- Serverless 模式

**不擅长**：纯 OLTP 事务（→ RDS）；超低延迟缓存（→ Tair）

**典型选型场景**：实时大屏、BI 加速、用户画像秒级圈选、推荐特征服务、MaxCompute 提速
**对位竞品**：AWS Redshift Serverless / GCP BigQuery / Snowflake
**报价量级**：32CU ≈ 5200 元/月；Serverless 按 CU*时计费
**避坑**：宽表列数太多影响性能（建议<300列）；Table Group 设计影响查询效率
**官方文档**：https://help.aliyun.com/zh/hologres/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### MaxCompute

**官方定位**：超大规模离线数据仓库/数据湖计算引擎。
**能做**：
- EB 级数据处理（单作业万台并行）
- 标准 SQL（兼容 Hive）+ MapReduce + Graph + Spark
- 存算分离，按量/包年两种计费
- 与 DataWorks（调度/血缘/质量）紧密集成
- 湖仓一体（Delta Lake/Iceberg/Hudi 外表）

**不擅长**：低延迟实时查询（→ Hologres/Flink）；在线事务（→ RDS）

**典型选型场景**：企业级离线数仓、数据中台底座、大规模 ETL、机器学习数据预处理
**对位竞品**：AWS Redshift + Athena / GCP BigQuery / Azure Synapse
**报价量级**：按量 0.3 元/GB 扫描；包年 150CU ≈ 2.5万/月
**避坑**：全表扫描成本高（分区+列裁剪是基本功）；与 Hologres/Flink 分工明确
**官方文档**：https://help.aliyun.com/zh/maxcompute/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### DataWorks

**官方定位**：一站式大数据开发治理平台（调度 + 数据集成 + 数据质量 + 数据地图）。
**能做**：
- 可视化 ETL 编排 + 定时调度
- 数据集成（支持 100+ 数据源，离线/实时同步）
- 数据质量监控、数据血缘
- 数据地图（元数据管理）
- 与 MaxCompute/Hologres/EMR/Flink 深度集成

**不擅长**：纯代码工程开发（→ IDE）；实时流计算开发（→ Flink 控制台）

**典型选型场景**：企业数据中台构建、ETL 调度管理、数据治理合规
**对位竞品**：AWS Glue + Step Functions / Azure Data Factory / GCP Dataflow
**报价量级**：基础版免费；标准版/专业版按节点实例数计费
**避坑**：调度时间窗口拥堵（合理错峰）；大量小任务时调度延迟
**官方文档**：https://help.aliyun.com/zh/dataworks/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Flink（实时计算）

**官方定位**：全托管 Apache Flink 服务，企业级流批一体。
**能做**：
- 全托管 Flink（Serverless + 专属集群两种模式）
- SQL + DataStream API + Python（PyFlink）
- 实时 ETL、CEP（复杂事件处理）、实时特征工程
- 内置 Connector（Kafka/RocketMQ/SLS/Hologres/RDS/…）
- Exactly-once 语义、Checkpoint/Savepoint

**不擅长**：纯离线批处理（→ MaxCompute/Spark）；简单定时触发（→ FC/DataWorks）

**典型选型场景**：实时数仓 ETL、实时风控、IoT 数据处理、实时特征计算
**对位竞品**：AWS Kinesis Data Analytics / Azure Stream Analytics / GCP Dataflow
**报价量级**：Serverless 1CU ≈ 0.5 元/时；专属集群按 ACU 包月
**避坑**：Checkpoint 间隔设置影响恢复速度和性能；State 大时需调优 RocksDB 后端
**官方文档**：https://help.aliyun.com/zh/flink/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### DTS（数据传输服务）

**官方定位**：异构数据库迁移/同步/订阅一站式服务。
**能做**：
- 数据迁移（全量+增量，几乎零停机）
- 实时同步（支持双向同步、单向同步、多对一）
- 数据订阅（CDC，程序消费数据库变更）
- 支持 10+ 数据库引擎互通
- 预检查 + 监控 + 数据校验

**不擅长**：ETL 复杂变换（→ DataWorks/Flink）；文件级同步（→ OSS 跨域复制）

**典型选型场景**：数据库上云迁移、跨地域灾备同步、异构数据库实时复制、CDC 事件消费
**对位竞品**：AWS DMS / Azure DMS / GCP Database Migration Service
**报价量级**：按规格+同步链路数计费；small ≈ 600 元/月
**避坑**：大对象（LOB）同步延迟；DDL 兼容性（某些 DDL 不支持自动同步需手动）
**官方文档**：https://help.aliyun.com/zh/dts/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### DataX（开源 + DataWorks 数据集成）

**官方定位**：阿里巴巴开源的离线数据同步工具，被 DataWorks 数据集成深度集成，是大数据搬迁与异构同步的事实标准。
**能做**：
- 100+ Reader/Writer 插件（MySQL/Oracle/SQL Server/PG/HDFS/OSS/MaxCompute/Hive/HBase/MongoDB/ES/Kafka/Redis/…）
- 单机/分布式两种模式：开源 DataX 单机即可拉数；DataWorks 数据集成提供独享/公共资源组，支持分布式并发
- 离线全量 + 增量（基于水位列）+ 整库迁移向导
- 与 DataWorks 调度、数据质量、血缘联动；支持脏数据收集、限速限并发
- 大数据迁云核心工具：Hive→MaxCompute、HDFS→OSS-HDFS、Oracle→MaxCompute、MySQL→Hologres 等典型链路

**不擅长**：实时 CDC（→ DTS / Flink CDC）；复杂 ETL 变换（→ DataWorks Flow / Flink）；超低延迟（秒级以内 → Flink）

**典型选型场景**：大数据迁云全量+增量、异构离线同步、数据中台数据接入层、跨云跨账号数据搬运
**对位竞品**：AWS Glue（Spark-based）/ Apache Sqoop / Talend / Informatica
**报价量级**：开源版 0 元；DataWorks 数据集成独享资源组按 CU 计费（4CU ≈ 1500 元/月起）
**避坑**：JVM 堆内存与 channel 数需根据源/目标吞吐手动调；脏数据策略默认严格（建议先 dirty-tolerance）；Hive 分区表需启用分区动态发现
**官方文档**：https://help.aliyun.com/zh/dataworks/user-guide/data-integration-overview/ ; 开源 https://github.com/alibaba/DataX
**证据等级**：[官方+开源]
**最近更新**：2026-06-18

---

### 数据库选型快速决策

```
关系型 OLTP？
├── 小中型 → RDS
├── 大型/弹性/读多 → PolarDB
├── 分布式/分库分表 → PolarDB-X
└── Oracle 迁移 → PolarDB-O

分析型 OLAP？
├── 离线数仓(PB) → MaxCompute
├── 实时交互查询 → Hologres
├── 通用 OLAP → AnalyticDB
└── 流计算 → Flink

NoSQL？
├── KV 缓存 → Tair
├── 宽表/时序/向量 → Lindorm
├── Serverless 文档存储 → Tablestore
└── 文档 DB（MongoDB 兼容） → MongoDB 版
```

---

## AI

### 百炼（Model Studio）

**官方定位**：一站式大模型开发与应用平台，MaaS（Model as a Service）。
**能做**：
- 模型调用（通义千问 Qwen 全系列 + 第三方 DeepSeek/Llama/…）
- 应用编排（Agent 工具链、工作流 DAG）
- RAG 知识库（文档上传 + 切片 + 向量 + 召回）
- Prompt 工程（Playground + 评测 + 版本管理）
- 模型微调（SFT/LoRA/全参数）

**不擅长**：大规模自主训练（→ PAI）；私有化GPU部署管理（→ PAI-EAS）

**典型选型场景**：企业 AI 应用快速上线、智能客服、知识问答 Agent、内容生成
**对位竞品**：AWS Bedrock / Azure OpenAI Service / GCP Vertex AI
**报价量级**（中国内地，每百万 Token，含思维链）[官方][2026-06]:
| 模型 | 输入 | 输出 | 定位 |
| --- | --- | --- | --- |
| qwen3.7-max | 12元 | 36元 | 旗舰推理，1M 上下文 |
| qwen3.7-plus | 2元 | 8元 | 能力成本均衡，1M 上下文，内置工具 |
| qwen3.6-flash | 1.2元 | 7.2元 | 轻量低成本，1M 上下文 |
| deepseek-v4-pro | 12元 | 24元 | 三方模型，强推理 |
| deepseek-v4-flash | 1元 | 2元 | 三方轻量版 |
- Batch 调用半价；上下文缓存享有折扣
- 每个新账号开通后 90 天内免费 100万 Token
**避坑**：RAG 切片策略影响召回质量（需调优 chunk_size + overlap）；并发有 QPS 上限；输入超 256K 触发阶梯加价
**官方文档**：https://help.aliyun.com/zh/model-studio/
**证据等级**：[官方]
**最近更新**：2026-06-28（Qwen3.7 + DeepSeek v4 定价刷新）

---

### PAI（人工智能平台）

**官方定位**：全生命周期 AI 开发平台——数据标注→训练→推理→部署。
**能做**：
- **DSW**：云端 Notebook（GPU/CPU，JupyterLab）
- **DLC**：分布式训练（支持 PyTorch/TF/MindSpore，千卡级）
- **EAS**：在线推理服务（模型部署、自动扩缩、A/B Test、蓝绿发布）
- **Designer**：可视化建模（拖拽式 ML Pipeline）
- GPU 资源池化（PD 分离、vGPU、弹性配额组）
- 模型仓库 + 数据集管理

**不擅长**：业务侧直接集成（→ 百炼 API）；无代码应用编排（→ 百炼 Agent）

**典型选型场景**：大模型预训练/微调（千卡集群）、模型私有化部署、ML 工程平台
**对位竞品**：AWS SageMaker / Azure ML / GCP Vertex AI (Training)
**报价量级**：DSW A10 实例 ≈ 13 元/时；DLC 按 GPU 时长计费；EAS 按实例规格
**避坑**：训练任务 Checkpoint 频率设置（OOM 或断点恢复）；EAS 冷启动优化需预热
**官方文档**：https://help.aliyun.com/zh/pai/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 通义千问（Qwen）

**官方定位**：阿里云自研大语言模型系列，从轻量到旗舰全尺寸覆盖。
**能做**：
- Qwen-Max：旗舰级推理、长文本（128K+ context）
- Qwen-Plus：平衡性价比
- Qwen-Turbo：轻量高速，适合简单任务
- Qwen-VL：多模态（图文理解）
- Qwen-Audio：语音理解
- Qwen-Coder：代码生成
- 开源生态（Qwen2.5 系列，72B/14B/7B/1.5B 开源权重）

**不擅长**：图像生成（→ 通义万相）；语音合成/克隆（→ CosyVoice）

**典型选型场景**：企业 AI 助手、Agent 底座、RAG 问答、代码辅助
**对位竞品**：GPT-4o / Claude / Gemini / DeepSeek
**报价量级**：通过百炼 API 统一计费，见百炼产品卡定价表
**模型矩阵**（Qwen3.7 系列）:
- qwen3.7-max：旗舰推理，1M 上下文，256K 思考预算
- qwen3.7-plus：能力成本均衡，内置工具+结构化输出
- qwen3.6-flash：轻量低成本，效果接近旗舰
- qwen3.5-omni-plus：全模态（文本+图像+音频+视频）
**避坑**：不同模型 context 长度差异大（选对版本）；多模态需用 omni 或 VL 版本；开源版不包含内置工具
**官方文档**：https://help.aliyun.com/zh/dashscope/
**证据等级**：[官方]
**最近更新**：2026-06-28（Qwen3.7 系列刷新）

---

### 通义万相

**官方定位**：AI 图像/视频生成模型。
**能做**：文生图、图生图、图片编辑、背景生成、人像修复、视频生成
**不擅长**：文本理解/推理（→ 千问）；专业视频编辑（→ 传统剪辑）

**典型选型场景**：广告创意素材、电商商品图、数字人、营销内容批量生产
**对位竞品**：Midjourney / DALL-E / Stable Diffusion / Runway
**报价量级**：通过百炼 API 按次计费
**官方文档**：https://help.aliyun.com/zh/dashscope/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Qoder CN 系列（原通义灵码）

**官方定位**：Agentic Coding & Work Platform——从 AI 代码助手升级为智能体自主开发与办公工作台。2026 年 5 月 20 日由"通义灵码"正式更名为 Qoder CN。
**产品线**：
- **Qoder CN**（编码插件）：VS Code / JetBrains IDE 插件，提供代码补全(NEXT引擎)、对话编程、Agent 自主任务(Quest)、Repo Wiki 代码库知识引擎
- **QoderWork CN**（桌面应用）：非编码场景的 AI 桌面助手，覆盖文件管理、数据分析、文档撰写、研究调研等日常办公
- **Qoder CN CLI**（终端形态）：命令行原生 Agent，适合 DevOps/运维/自动化场景
- **Cloud Agents CN**（云端托管）：云端自主智能体，支持后台长时间任务执行

**能做**：
- 代码补全（Qwen-Coder-Qoder 深度定制模型）、代码生成、代码解释、单测生成、代码评审
- Quest 模式：自主智能体接手复杂多步开发任务（多文件编辑、调试、部署）
- 知识引擎(Knowledge Engine)：自动索引代码库结构，规范驱动开发
- MCP Server 支持：连接外部工具和数据源
- 多任务并行调度、子智能体编排

**不擅长**：模型训练（→ PAI）；非 Qwen 生态模型的私有化部署

**典型选型场景**：开发者日常编码提效、Agent 自主开发任务、代码库理解与导航、团队规范落地
**对位竞品**：GitHub Copilot / Cursor / Windsurf / Amazon Q Developer
**报价量级**：Pro 59 元/月(2000 Credits)；Teams 99 元/席·月(3000 Credits)；资源包 1000 Credits/40 元
**与 Qoder 全球版的关系**：Qoder(qoder.com) 面向全球市场，Qoder CN(qoder.com.cn) 面向中国市场，底层能力对等，CN 版支持国产模型部署 + 金融/政务合规要求
**官方文档**：https://help.aliyun.com/zh/lingma/ | 官网：https://qoder.com.cn
**证据等级**：[官方]
**最近更新**：2026-06-17（品牌更名后全面更新）

---

### DashScope（灵积模型服务）

**官方定位**：模型 API 网关，百炼底层的模型调用通道。
**能做**：
- 统一 API 调用多种模型（文本/图像/音频/视频/Embedding/Rerank）
- 兼容 OpenAI SDK 格式
- 模型推理、Batch 推理
- 多模态输入（图文音混合）

**不擅长**：应用编排（→ 百炼平台）；模型管理（→ PAI）

**典型选型场景**：程序直接调用模型 API（无需百炼应用编排层）
**对位竞品**：OpenAI API / Anthropic API / Azure OpenAI Endpoint
**报价量级**：与百炼共享定价
**官方文档**：https://help.aliyun.com/zh/dashscope/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### AI 选型快速决策

```
需要自己训练/微调模型？
├── 大规模预训练 → PAI-DLC + CPFS + GPU 集群
├── 轻量微调(SFT/LoRA) → 百炼微调 或 PAI
└── 不需要 → 直接调百炼 API

部署方式？
├── MaaS（API 调用） → 百炼 / DashScope
├── 私有化部署（自持模型） → PAI-EAS
└── 边缘推理 → ACS GPU / ECI GPU

应用类型？
├── 对话/Agent → 百炼 + Qwen
├── RAG 知识库 → 百炼 RAG + Lindorm 向量
├── 图像生成 → 通义万相
├── 代码辅助/智能开发 → Qoder CN 系列（原通义灵码）
└── 语音识别/合成 → 百炼语音模型
```

---

## 中间件

### MSE（微服务引擎）

**官方定位**：一站式微服务治理平台——注册中心 + 配置中心 + 网关 + 治理。100% 兼容开源 Nacos/ZooKeeper/Eureka/Sentinel。
**能做**：
- **Nacos 注册配置中心**（托管 Nacos 集群，四版本：开发版/专业版/企业版/Serverless）
- **ZooKeeper**：托管 ZK 集群
- **云原生网关**：API 网关（统一入口/限流/鉴权/路由/协议转换）
- **Sentinel**：流量治理（限流/熔断/降级/热点防护）
- **服务治理**：无侵入式（Agent）全链路灰度、标签路由
- **AI/Agent 生态**（企业版 Nacos 3.x）：MCP Registry、A2A Registry、AI 安全护栏

**不擅长**：消息队列（→ RocketMQ/Kafka）；全链路追踪（→ ARMS）

**Nacos 四版本对比**（关键决策表）：
| 维度 | 开发版 | 专业版 | 企业版 | Serverless |
| --- | --- | --- | --- | --- |
| 节点 | 单节点 | 默认 3 节点 | 默认 3 节点（独享） | 自动弹性 |
| SLA | 无 | 99.95% | 99.99% | 99.9% |
| 协议 | gRPC（2.x） | gRPC（2.x） | gRPC（3.x） | gRPC（2.x） |
| 推送性能（vs 开源） | 持平 | +202% | +300% | +202% |
| 多 AZ 容灾 | ❌ | ✅ | ✅ | ✅ |
| 推空保护 | ❌ | ✅ | ✅ | ✅ |
| 高级安全（密钥轮转/磁盘加密） | ❌ | ❌ | ✅ | ❌ |
| AI Agent（MCP/A2A Registry） | ❌ | ❌ | ✅ | ❌ |
| 计费 | CPU/内存×节点 | CPU/内存×节点 | 实例规格×节点 | 按最大连接数阶梯 |
| 适用 | 仅开发测试 | 主流生产首选 | 核心生产+AI Agent | 流量波动/小流量 |

**典型选型场景**：
- Spring Cloud/Dubbo 微服务注册发现与治理 → Nacos 专业版（首选）
- AI Agent 注册发现 / MCP 工具集市 → Nacos 企业版（Nacos 3.x）
- 潮汐流量 / 小型业务 / 每小时连接数 < 100 → Serverless（成本更低）
- 开发测试环境 → 开发版

**对位竞品**：AWS App Mesh + API Gateway / Azure Service Fabric / Istio + Envoy

**报价量级**（中国内地，2026-06）：
- 开发版：1C2G ≈ 118 元/月，2C4G ≈ 221 元/月（年包 6 折/月包 7 折）
- 专业版：2C4G ≈ 369 元/月/节点（3 节点 = 1107 元/月），8C16G ≈ 1294 元/月/节点；首购 6 折
- 企业版：Small ≈ 724 元/月/节点，Medium.x1 ≈ 1377 元/月/节点（3 节点起售）
- Serverless：按每小时最大连接数阶梯（< 100 连接最划算）；可叠加节省计划再省 5-20%
- 公网网络费：SLB 带宽另计（中国内地 1Mbps ≈ 35 元/月起）

**避坑**：
- 基础版（Nacos 1.x）已停止新购，不要选；老用户尽快升专业版
- 普通实例（开发/专业/企业）与 Serverless 实例**不能互相迁移**，选型要一次到位
- 专业版可平滑升级到企业版，反向不行
- 实例运行即扣费，不支持暂停；不用了立即释放
- Nacos 容量规划（注册实例数/配置推送频率/最大连接数）
- 全链路灰度需配合 Agent；自建 Nacos 客户端版本要兼容 gRPC

**官方文档**：https://help.aliyun.com/zh/mse/  
**版本选型**：https://help.aliyun.com/zh/mse/product-overview/select-an-edition  
**计费指南**：开发/专业版 https://help.aliyun.com/zh/mse/product-overview/billing-description-of-developer-edition-instances-and-professional-edition-instances ；企业版 https://help.aliyun.com/zh/mse/product-overview/nacos-platinum-edition-billing-description  
**证据等级**：[官方]
**最近更新**：2026-06-23（4 篇官方文档蒸馏，补全四版本矩阵 + AI Agent 能力 + 真实价格）

---

### RocketMQ（消息队列）

**官方定位**：分布式消息中间件，低延迟高可靠。
**能做**：
- 普通消息 / 顺序消息 / 事务消息 / 定时消息 / 延迟消息
- 亿级消息堆积无压力
- 消息轨迹 / 死信队列
- gRPC 协议（5.x 版本）+ HTTP 接入
- Serverless 版本（按量弹性）

**不擅长**：大数据流式管道（→ Kafka）；AMQP 协议兼容（→ RabbitMQ）；事件驱动编排（→ EventBridge）

**典型选型场景**：电商订单解耦、金融事务消息、异步通知、削峰填谷
**对位竞品**：AWS SQS + SNS / Azure Service Bus / GCP Pub/Sub
**报价量级**（5.x 系列，Serverless 为主售模式）[官方][2026-06]:
| 系列 | 计费模式 | 参考价 |
| --- | --- | --- |
| Serverless 共享版 | 按消息数+存储 | 资源包 59元/月 抵扣 100元额度 |
| Serverless 独享版 | 预留+弹性 | 预留基础费+超出按量 |
| 包年包月（旧版） | 固定规格 | ~600元/月起（已停售新购） |
- 重要：原标准版/专业版已不再支持新购，Serverless 为当前主推
- RocketMQ for AI：支持 Multi-Agent 通信、大规模任务调度
**避坑**：消费者组内广播模式与集群模式混淆；消息体大小限制（4MB）；存量标准版与 Serverless 不可互迁
**官方文档**：https://help.aliyun.com/zh/apsaramq-for-rocketmq/
**证据等级**：[官方]
**最近更新**：2026-06-28（Serverless 为主售模式刷新）

---

### Kafka（消息队列 Kafka 版）

**官方定位**：全托管 Apache Kafka，大数据流式管道。
**能做**：
- 高吞吐（百万级 TPS）
- 与 Flink / MaxCompute / SLS / Hologres 无缝对接
- Connector Hub（100+ Source/Sink）
- 3 副本高可靠 + 自动扩缩分区

**不擅长**：事务消息（→ RocketMQ）；低延迟点对点（→ RocketMQ）；AMQP（→ RabbitMQ）

**典型选型场景**：日志采集管道、实时数据 ETL、大数据入湖入仓、IoT 数据流
**对位竞品**：AWS MSK / Azure Event Hubs / Confluent Cloud
**报价量级**（三种计费模式）[官方][2026-06]:
| 系列 | 计费模式 | 参考价 |
| --- | --- | --- |
| Serverless 基础版 | 按流量+存储+分区数 | 流量费 0.55元/GB起(阶梯) |
| Serverless 专业版 | 同上+增强能力 | 流量费略高+连接器等功能 |
| 包年包月 | 固定规格 | 2c4g ~900元/月 + 磁盘 |
- 10倍无损弹性（存算分离架构），计算成本比开源降低 50%+
- 公网带宽另计（出流量 + 带宽小时费）
**避坑**：Partition 数量规划（太多影响选举和重平衡）；Consumer Lag 监控；Serverless 与包年包月不可互转
**官方文档**：https://help.aliyun.com/zh/apsaramq-for-kafka/
**证据等级**：[官方]
**最近更新**：2026-06-28（三形态刷新）

---

### RabbitMQ（消息队列 AMQP 版）

**官方定位**：兼容 AMQP 0-9-1 协议的全托管消息服务。
**能做**：Exchange 路由（Direct/Fanout/Topic/Headers）、消息确认、延迟队列、死信路由
**不擅长**：超高吞吐（→ Kafka）；事务消息（→ RocketMQ）

**典型选型场景**：AMQP 协议迁移、中小规模微服务解耦、与已有 RabbitMQ 客户端兼容
**对位竞品**：AWS Amazon MQ / Azure Service Bus / CloudAMQP
**报价量级**：Serverless 按消息量计费；专业版实例 ≈ 500 元/月
**避坑**：单队列消息堆积过多影响消费性能；与 Kafka/RocketMQ 生态不通用
**官方文档**：https://help.aliyun.com/zh/apsaramq-for-rabbitmq/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### EventBridge（事件总线）

**官方定位**：Serverless 事件驱动架构核心——事件路由 + 过滤 + 转换 + 投递。
**能做**：
- 统一事件总线（阿里云产品事件 + 自定义事件 + SaaS 事件）
- 事件规则（过滤/转换/投递到 FC/MQ/HTTP/SLS 等）
- 事件追溯 + Schema Registry
- 定时触发（替代简单 Cron）
- CloudEvents 标准

**不擅长**：高吞吐流式处理（→ Kafka/Flink）；复杂业务消息（→ RocketMQ）

**典型选型场景**：事件驱动架构、跨服务松耦合、SaaS 集成、运维事件联动
**对位竞品**：AWS EventBridge / Azure Event Grid
**报价量级**：按事件投递次数计费；100 万次 ≈ 1.5 元
**避坑**：事件大小限制（64KB）；投递延迟非实时（秒级）
**官方文档**：https://help.aliyun.com/zh/eventbridge/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 消息选型快速决策

```
业务消息（订单/事务/通知）？ → RocketMQ
大数据流式管道（日志/ETL）？ → Kafka
AMQP 协议兼容？ → RabbitMQ
事件驱动编排（松耦合触发）？ → EventBridge
简单队列+通知？ → MNS（老产品，新项目不推荐）
```

---

## 安全

### WAF（Web 应用防火墙）

**官方定位**：L7 应用层安全防护，防御 Web 攻击和 Bot。
**能做**：
- OWASP Top 10 防护（SQL注入/XSS/命令注入/…）
- Bot 管理（爬虫/薅羊毛/暴力破解）
- CC 防护（速率限制）
- API 安全（OpenAPI 发现 + 异常检测）
- 与 ALB/CLB/CDN/DCDN 联动

**不擅长**：DDoS 网络层攻击（→ Anti-DDoS）；主机入侵检测（→ 云安全中心）

**典型选型场景**：Web 应用/API 防护、电商防薅羊毛、合规要求（等保/GDPR）
**对位竞品**：AWS WAF / Azure WAF / Cloudflare WAF
**报价量级**（WAF 3.0，四版本）[官方][2026-06]:
| 版本 | 包年包月 | 适用场景 |
| --- | --- | --- |
| 基础版 | 980元/月 | 小型 Web 应用基本防护 |
| 高级版 | 3,880元/月 | 中大型 Web + API 安全 |
| 企业版 | 9,800元/月 | 企业级全面防护 |
| 旗舰版 | 29,800元/月 | 大流量高安全要求 |
- WAF 3.0 新增按量付费模式（按请求数计费，适合流量波动大的场景）
- QPS 扩展：3元/QPS/月起（阶梯优惠，10w+ QPS 可降至 1.8元）
- 增值：API 安全 5000-20000元/月；Bot 管理 8000元/月
**避坑**：自定义规则需调优（误杀风险）；HTTPS 证书需上传；与 CDN 搭配时注意回源；弹性 QPS 超限可能进沙箱
**官方文档**：https://help.aliyun.com/zh/waf/
**证据等级**：[官方]
**最近更新**：2026-06-28（WAF 3.0 四版本刷新）

---

### Anti-DDoS（DDoS 防护）

**官方定位**：网络层/传输层 DDoS 攻击防护。
**能做**：
- **原生防护**：免费基础防护（5Gbps）+ 增强版（按需提升阈值）
- **高防**：高防 IP（Tbps 级清洗能力）；BGP + Anycast
- 支持 TCP/UDP/HTTP/HTTPS/WebSocket
- 智能调度（联动 CDN + WAF + 高防）

**不擅长**：应用层攻击精细防护（→ WAF）；主机级防护（→ 云安全中心）

**典型选型场景**：游戏行业、金融支付、电商大促、政府网站防攻击
**对位竞品**：AWS Shield / Azure DDoS Protection / Cloudflare
**报价量级**：原生增强版 ≈ 数千元/月；高防按清洗带宽计费，30Gbps ≈ 2万/月
**避坑**：高防 IP 会改变回源 IP（需配合 X-Forwarded-For）；带宽超套餐会触发黑洞
**官方文档**：https://help.aliyun.com/zh/anti-ddos/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Cloud Firewall（云防火墙）

**官方定位**：云原生网络防火墙，覆盖互联网边界 + VPC 间 + 主机间三层。
**能做**：
- 互联网边界防火墙（南北向流量控制）
- VPC 间防火墙（东西向微隔离）
- 主机边界防火墙（替代安全组高级场景）
- 入侵防御（IPS）+ 威胁情报联动
- 流量可视化、访问控制策略

**不擅长**：应用层防护（→ WAF）；DDoS（→ Anti-DDoS）

**典型选型场景**：企业级网络边界管控、等保合规（出口/入口/内部分区隔离）
**对位竞品**：AWS Network Firewall / Azure Firewall / Palo Alto VM-Series
**报价量级**：按保护资产数+处理流量计费；高级版 ≈ 5000 元/月起
**避坑**：VPC 间防火墙需 CEN 转发路由器配合；策略条目数有限
**官方文档**：https://help.aliyun.com/zh/cloud-firewall/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 云安全中心（Security Center）

**官方定位**：统一安全运营中心——主机安全 + 容器安全 + 漏洞 + 基线 + 入侵检测。
**能做**：
- 服务器漏洞检测与修复（CVE + 应用漏洞）
- 安全基线检查（等保/CIS）
- 入侵检测（挖矿/勒索/后门/提权/异常登录）
- 容器安全（镜像扫描 + 运行时防护）
- 安全态势评分、告警关联分析
- 云产品安全配置检查

**不擅长**：网络边界防护（→ Cloud Firewall/WAF）；DDoS 清洗（→ Anti-DDoS）

**典型选型场景**：主机安全运营、等保合规检查、多云安全统一管理
**对位竞品**：AWS GuardDuty + Inspector / Azure Defender / GCP Security Command Center
**报价量级**：企业版 ≈ 90 元/台/月；高级版 ≈ 30 元/台/月
**避坑**：Agent 安装是前提（未安装则无数据）；告警量大时需配合自动化处置规则
**官方文档**：https://help.aliyun.com/zh/security-center/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### KMS（密钥管理服务）

**官方定位**：密钥全生命周期管理，加密/解密/签名/密钥轮转。
**能做**：
- 对称/非对称密钥管理（AES/RSA/SM 系列）
- 信封加密（数据加密密钥由 KMS 保护）
- 凭据管家（Secrets Manager，管理数据库密码/AK/证书）
- 自动轮转
- HSM 托管（符合 FIPS 140-2 Level 3）
- 与 OSS/RDS/EBS/SLS 等产品集成（一键加密）

**不擅长**：证书签发（→ SSL 证书服务）；DLP 数据脱敏（→ SDDP）

**典型选型场景**：数据加密合规、密钥集中管理、CI/CD 凭据保护
**对位竞品**：AWS KMS / Azure Key Vault / GCP Cloud KMS
**报价量级**：按密钥数+API 调用计费；软件密钥 ≈ 2.8 元/个/天
**避坑**：跨地域密钥不互通（需每个 Region 创建）；调用频率有限制
**官方文档**：https://help.aliyun.com/zh/kms/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 堡垒机

**官方定位**：运维审计 + 权限管控 + 操作录像的运维堡垒系统。
**能做**：SSH/RDP/SFTP 运维代理、双因素认证、命令审计、操作录像回放、工单审批
**不擅长**：主机安全检测（→ 云安全中心）；网络防护（→ Cloud Firewall）

**典型选型场景**：等保合规（4A）、运维安全管控、多人共管服务器审计
**对位竞品**：AWS Systems Manager Session Manager / CyberArk / JumpServer
**报价量级**：按授权资产数计费；50 台 ≈ 1800 元/月
**避坑**：需在 VPC 内部署；大规模资产需升级规格
**官方文档**：https://help.aliyun.com/zh/bastion-host/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### RAM（访问控制）

**官方定位**：身份与访问管理——用户/角色/策略/SSO。
**能做**：
- RAM 用户、用户组、角色（Role）
- 策略（Policy）：系统策略 + 自定义策略（JSON）
- 跨账号访问（AssumeRole）
- SSO 单点登录（SAML 2.0 / OIDC）
- MFA / 密码策略 / AccessKey 管理
- STS 临时凭证

**不擅长**：细粒度数据行级权限（→ 应用层鉴权）

**典型选型场景**：所有阿里云环境的身份基础设施
**对位竞品**：AWS IAM / Azure AD + RBAC / GCP IAM
**报价量级**：免费
**避坑**：策略条目 20 条限制（组合使用）；AK 泄露是头号安全风险
**官方文档**：https://help.aliyun.com/zh/ram/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ActionTrail（操作审计）

**官方定位**：记录所有云 API 操作日志，用于安全审计和合规。
**能做**：
- 自动记录所有阿里云 API 调用（管控事件+数据事件）
- 投递到 SLS / OSS 长期归档
- 跨账号聚合审计（Resource Directory 场景）
- 实时查询近 90 天事件

**不擅长**：业务层审计日志（→ 应用自身 + SLS）

**典型选型场景**：合规审计（等保/SOX/GDPR）、安全事件溯源、变更追踪
**对位竞品**：AWS CloudTrail / Azure Activity Log / GCP Cloud Audit Logs
**报价量级**：管控事件免费；数据事件按投递量计费
**避坑**：默认只保存 90 天（需配置跟踪投递到 OSS/SLS 做长期保存）
**官方文档**：https://help.aliyun.com/zh/actiontrail/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### Config（配置审计）

**官方定位**：持续监控云资源配置合规性。
**能做**：
- 预置 200+ 合规规则（等保/CIS/自定义）
- 资源配置变更追踪
- 不合规自动修复（OOS 联动）
- 跨账号合规聚合（Resource Directory）

**不擅长**：实时入侵检测（→ 云安全中心）；操作审计（→ ActionTrail）

**典型选型场景**：持续合规检查、安全 Baseline 漂移检测、多账号治理
**对位竞品**：AWS Config / Azure Policy / GCP Organization Policy
**报价量级**：按评估次数计费；持续记录约 0.001 元/条
**避坑**：规则太多可能产生告警疲劳（按优先级分组）
**官方文档**：https://help.aliyun.com/zh/config/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 安全纵深防御架构

```
┌──────────────────────────────────────────────────┐
│ L1: 网络边界 — Anti-DDoS + Cloud Firewall        │
├──────────────────────────────────────────────────┤
│ L2: 应用边界 — WAF + API 安全                     │
├──────────────────────────────────────────────────┤
│ L3: 身份认证 — RAM + SSO + MFA                    │
├──────────────────────────────────────────────────┤
│ L4: 主机/容器 — 云安全中心                        │
├──────────────────────────────────────────────────┤
│ L5: 数据安全 — KMS + 加密 + SDDP                  │
├──────────────────────────────────────────────────┤
│ L6: 审计合规 — ActionTrail + SLS + Config          │
└──────────────────────────────────────────────────┘
```

---

## 监控运维

### ARMS（应用实时监控服务）

**官方定位**：全栈可观测——APM + 前端监控 + Prometheus + 告警。
**能做**：
- 应用性能监控（Java/PHP/Node/Go 无侵入式 Agent）
- 分布式链路追踪（OpenTelemetry 兼容）
- Prometheus 托管服务（免运维 + 长期存储）
- 前端监控（RUM，页面性能/JS 错误/API 状态）
- 自定义大盘 + Grafana 托管
- 智能告警（AI 基线 + 组合告警）

**不擅长**：日志检索（→ SLS）；基础设施监控（→ CloudMonitor）

**典型选型场景**：微服务 APM、K8s 集群可观测、全链路诊断
**对位竞品**：AWS X-Ray + CloudWatch / Azure Monitor / Datadog / New Relic
**报价量级**：APM 按 Agent 数 ≈ 90 元/月/Agent；Prometheus 按时间序列数
**避坑**：Agent 对 JVM 有微量开销（< 5%）；时间序列爆炸时成本上升
**官方文档**：https://help.aliyun.com/zh/arms/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### SLS（日志服务）

**官方定位**：一站式日志/时序/Trace 平台——采集+检索+分析+告警+投递。
**能做**：
- 50+ 数据源自动采集（ECS/K8s/OSS/RDS/WAF/ActionTrail/…）
- 实时检索（秒级，PB 级数据）
- SQL 分析 + PromQL + 可视化大盘
- 告警（通知 + 事件降噪 + 自动化处理 Webhook）
- 投递 OSS/MaxCompute/Hologres 做长期分析
- AIOps（智能巡检/根因分析/日志聚类）

**不擅长**：APM 级别链路分析（→ ARMS）；基础设施层指标（→ CloudMonitor）

**典型选型场景**：集中日志平台、安全审计归档（等保）、运营分析、DevOps 日志
**对位竞品**：AWS CloudWatch Logs + OpenSearch / Azure Monitor Logs / Splunk / ELK
**报价量级**：按写入流量+存储+索引流量计费；1GB/天 ≈ 6 元/月
**避坑**：索引字段越多成本越高（按需索引）；Shard 数规划影响写入和查询并发
**官方文档**：https://help.aliyun.com/zh/sls/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### CloudMonitor（云监控）

**官方定位**：阿里云基础设施和服务的统一监控平台。
**能做**：
- 200+ 云产品免费基础监控指标
- 自定义监控（上报自定义指标）
- 告警规则（阈值/无数据/组合）+ 多渠道通知
- 事件监控（系统事件/自定义事件）
- 站点监控（HTTP/TCP/Ping 可用性）
- 与 OOS 联动（告警自动修复）

**不擅长**：深度 APM（→ ARMS）；日志检索分析（→ SLS）

**典型选型场景**：云资源基础监控告警、站点可用性监控、系统事件感知
**对位竞品**：AWS CloudWatch Metrics / Azure Monitor Metrics
**报价量级**：基础免费；高精度/自定义/站点按量收费
**避坑**：默认监控频率为 60s（需自定义的到 15s/1s）；告警通道需配置联系人
**官方文档**：https://help.aliyun.com/zh/cms/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ROS（资源编排）

**官方定位**：Infrastructure as Code（IaC），基于模板自动化创建和管理云资源。
**能做**：
- JSON/YAML 模板声明式编排
- 支持 400+ 阿里云资源类型
- 偏差检测（实际 vs 期望配置）
- 更新策略（滚动/替换/保留）
- 模块化 + 嵌套栈
- Terraform Provider 兼容

**不擅长**：运维编排/日常操作（→ OOS）；CI/CD 流水线（→ 云效/Jenkins）

**典型选型场景**：Landing Zone 自动化部署、环境一致性（Dev/Staging/Prod）、灾备切换
**对位竞品**：AWS CloudFormation / Azure ARM/Bicep / GCP Deployment Manager
**报价量级**：服务免费（只收资源费用）
**避坑**：模板复杂时执行超时；更新栈时注意资源替换策略
**官方文档**：https://help.aliyun.com/zh/ros/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ACR（容器镜像服务）

**官方定位**：容器镜像全生命周期管理——构建+存储+分发+安全扫描。
**能做**：
- OCI 标准镜像仓库（Docker/Helm Chart/OCI Artifact）
- 镜像构建（源码到镜像，Dockerfile 自动构建）
- 镜像安全扫描（CVE 漏洞）
- 全球镜像同步（跨地域加速分发）
- 与 ACK/ACS/SAE/FC 深度集成

**不擅长**：CI/CD 流水线编排（→ 云效/Jenkins）；运行时安全（→ 云安全中心）

**典型选型场景**：容器化团队的镜像仓库、多地域部署镜像同步、安全合规扫描
**对位竞品**：AWS ECR / Azure ACR / GCP Artifact Registry / Docker Hub
**报价量级**：个人版免费（3 命名空间）；企业版按实例规格 ≈ 500 元/月起
**避坑**：个人版限制较多（并发拉取/命名空间/镜像保留策略）；企业版选对地域
**官方文档**：https://help.aliyun.com/zh/acr/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### CDN（内容分发网络）

**官方定位**：静态内容全球加速分发。
**能做**：
- 3200+ 全球节点缓存静态内容
- HTTPS/HTTP2/HTTP3 加速
- 图片处理（缩放/裁剪/水印/WebP）
- 边缘脚本（EdgeRoutine/EdgeScript）
- 日志实时投递 + 数据分析

**不擅长**：动态内容加速（→ DCDN）；全球网络加速（→ GA）

**典型选型场景**：网站静态加速、视频点播分发、下载加速
**对位竞品**：AWS CloudFront / Azure CDN / Cloudflare / Akamai
**报价量级**：按流量阶梯计费；国内 0.24 元/GB 起
**避坑**：缓存策略设置不当导致源站压力；HTTPS 证书管理；刷新预热有频率限制
**官方文档**：https://help.aliyun.com/zh/cdn/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### DCDN（全站加速）

**官方定位**：动静分离全站加速，兼具 CDN + 动态路由优化。
**能做**：
- 动态内容回源路由优化（智选最优路径）
- 静态内容边缘缓存
- WebSocket 加速
- 边缘安全（WAF/DDoS/Bot 防护集成）
- 边缘函数（ER）

**不擅长**：纯静态内容（CDN 更经济）；全球 TCP/UDP 加速（→ GA）

**典型选型场景**：电商动态页面、API 加速、游戏资源动静混合、出海加速
**对位竞品**：AWS CloudFront (dynamic) / Cloudflare / Akamai Ion
**报价量级**：按请求数+流量计费；动态请求 0.15 元/万次
**避坑**：动态加速成本高于纯 CDN；需合理分离动静
**官方文档**：https://help.aliyun.com/zh/dcdn/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### 可观测三柱选型

```
指标 Metrics → CloudMonitor（基础）+ ARMS Prometheus（高级）
日志 Logs → SLS
链路 Tracing → ARMS APM

IaC → ROS（阿里云原生）/ Terraform（多云）
运维编排 → OOS
CI/CD 制品 → ACR（镜像）+ 云效/Jenkins（流水线）
```

---

## 混合云 / 边缘

### 专有云（Apsara Stack）

**官方定位**：阿里云公有云技术栈的本地化输出，用于客户自有数据中心。
**能做**：完整飞天栈私有化部署、与公有云产品能力对齐、混合云管控面
**不擅长**：快速迭代（私有化版本滞后公有云 6-12 月）；小规模场景（成本高）

**典型选型场景**：政府/金融/军工等强合规数据不出境、大型企业 IDC 扩容
**对位竞品**：AWS Outposts / Azure Stack / GCP Anthos (on-prem)
**报价量级**：项目制，百万级起步
**官方文档**：https://help.aliyun.com/zh/apsara-stack/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

### ENS（边缘节点服务）

**官方定位**：将计算能力下沉到边缘节点（MEC），降低端到端延迟。
**能做**：边缘 ECS/容器实例、边缘存储、边缘转发、全国 300+ 边缘节点
**不擅长**：大规模集中计算（→ 中心 ECS/ACK）

**典型选型场景**：音视频流处理、CDN 边缘计算、AR/VR、车联网、工业边缘
**对位竞品**：AWS Wavelength + Local Zones / Azure Edge Zones
**报价量级**：按边缘实例规格+带宽计费
**官方文档**：https://help.aliyun.com/zh/ens/
**证据等级**：[官方]
**最近更新**：2026-06-17

---

## 视频 / 音视频

### MPS（媒体处理服务 / 智能媒体服务 IMS）

**官方定位**：一站式音视频转码、剪辑、AI 智能处理服务。
**能做**：标准/窄带/极窄带/H.265/AV1 转码；HLS/DASH 打包；视频审核（鉴黄/暴恐/广告）；智能剪辑/封面/字幕；AI 拆条
**不擅长**：超低延迟实时处理（→ RTC）；纯直播分发（→ Live）

**典型选型场景**：UGC/PGC 平台转码、版权视频处理、智能营销素材生成、播客/课件加工
**对位竞品**：AWS MediaConvert + Rekognition Video / 腾讯云 MPS / 火山多媒体
**报价量级**：转码按分钟（标清 ¥0.005/min、4K HEVC ¥0.10/min）；AI 处理另计
**官方文档**：https://help.aliyun.com/zh/ims/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

### VoD（视频点播）

**官方定位**：集音视频采集、上传、存储、转码、分发、播放器于一体的一站式 PaaS。
**能做**：分片上传/断点续传、转码模板、HLS/DASH 加密（HLS 标准/Aliyun-Private/PlayReady/Widevine）、防盗链/Referer/IP 黑白名单、播放统计、CDN 加速
**不擅长**：直播（→ Live）；强自定义播放体验（→ 自建播放器 + OSS + CDN）

**典型选型场景**：在线教育课程、企业培训、媒体平台点播、UGC 短视频平台、政企内部视频门户
**对位竞品**：AWS Elemental MediaTailor + S3 + CloudFront / 腾讯云点播 / 七牛云点播
**报价量级**：存储 ¥0.099/GB·月 + 转码 + CDN 流量（¥0.20/GB 起）；典型千万 MAU 平台月费 50w-200w
**官方文档**：https://help.aliyun.com/zh/vod/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

### Live（视频直播）

**官方定位**：直播推拉流、转码、录制、截图、CDN 分发的一站式直播 PaaS。
**能做**：RTMP/WebRTC/SRT 推流、HLS/HTTP-FLV/RTMP 拉流、低延迟直播（LL-HLS/RTS 1-3 秒）、连麦混流、鉴权、回看、转点播
**不擅长**：强互动连麦（→ RTC + Live 旁路推流）；超大规模 P2P 分发（→ PCDN）

**典型选型场景**：电商带货直播、教育大班课、赛事直播、企业发布会、游戏直播平台
**对位竞品**：AWS IVS / 腾讯云直播 LVB / 火山视频云
**报价量级**：推流免费、转码 ¥0.01/min（标清）-¥0.20/min（4K HEVC）、CDN 下行 ¥0.18-0.24/GB；千万级并发场景月费 200w-1000w
**官方文档**：https://help.aliyun.com/zh/live/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

### RTC（音视频通信）

**官方定位**：基于 WebRTC 的低延迟（<400ms）实时音视频互动 PaaS。
**能做**：1v1/多人通话、连麦、互动课堂、屏幕共享、空间音频、AI 降噪/回声消除、旁路推流到 Live、SDK 全平台覆盖（iOS/Android/Web/Windows/macOS/小程序/Unity）
**不擅长**：单向大并发分发（→ Live）；非实时音视频（→ VoD）

**典型选型场景**：在线教育互动课堂、社交连麦、远程问诊、协同办公、客服音视频、元宇宙实时语音
**对位竞品**：声网 Agora（强对位）/ 腾讯云 TRTC / AWS Chime SDK / 即构 ZEGO
**报价量级**：音频 ¥0.0059/min·人、视频 720p ¥0.0118/min·人、4K ¥0.0708/min·人
**官方文档**：https://help.aliyun.com/zh/rtc/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

## IoT / 物联网

### IoT Platform（物联网平台 / Link IoT）

**官方定位**：海量设备接入、消息流转、设备管理、规则引擎、孪生模型的 IoT PaaS 底座。
**能做**：MQTT/CoAP/HTTPS/Modbus/OPC-UA 多协议接入、单实例千万级设备、TSL 物模型、规则引擎转 RDS/Lindorm/MNS/RocketMQ/FC、OTA、设备分组/标签、子设备网关、跨地域容灾
**不擅长**：边缘计算重场景（→ Link IoT Edge）；时序大数据分析（→ Lindorm TSDB + Hologres）

**典型选型场景**：智能家居、车联网 T-Box 接入、工业设备/传感器接入、智慧能源/水务/燃气、共享设备（充电桩/换电柜）
**对位竞品**：AWS IoT Core / Azure IoT Hub / 华为云 IoTDA / 腾讯云 IoT Explorer
**报价量级**：企业版按消息条数计费（基础 ¥0.0001/条），千万设备月费 5w-50w
**官方文档**：https://help.aliyun.com/zh/iot/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

## 接入 / 网关补充

### SAG（智能接入网关）

**官方定位**：通过软硬件智能网关将分支机构、门店、IDC、办公室一键接入阿里云 VPC/CEN。
**能做**：硬件 SAG-100WM/1000/SD-WAN、APP 客户端（手机/PC）、自动选路、IPSec/SSL VPN、本地内网穿透、4G/5G 备份链路
**不擅长**：核心数据中心专线级带宽（→ 高速通道 Express Connect）；超大规模骨干网（→ CEN-TR）

**典型选型场景**：连锁零售门店上云、银行网点回连总部、企业混合办公、跨国小型分支接入、SD-WAN 替代 MPLS
**对位竞品**：AWS Site-to-Site VPN + Direct Connect / Cisco Meraki SD-WAN / 华为云 SD-WAN
**报价量级**：硬件 SAG-100WM ¥4980/台 + 流量包；APP ¥0/账号/月（10 账号免费）
**官方文档**：https://help.aliyun.com/zh/smartag/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

### API Gateway（API 网关）

**官方定位**：API 全生命周期管理（发布/管理/认证/限流/计费）的网关 PaaS。
**能做**：HTTP/HTTPS/WebSocket、签名/JWT/AppCode 鉴权、按分钟限流、参数映射、协议转换（HTTP→HSF/Dubbo）、API 市场售卖、灰度发布、监控告警
**不擅长**：服务治理深度场景（→ MSE 云原生网关）；超低延迟内部网关（→ ALB + 自建鉴权）

**典型选型场景**：对外开放 API、SaaS 多租户 API 管理、内部微服务 API 统一入口、API 经济变现、Open API 平台
**对位竞品**：AWS API Gateway / Azure APIM / Kong Enterprise / 腾讯云 API 网关
**报价量级**：共享版 ¥0.06/万次调用 + ¥0.8/GB 流量；专享版按实例规格 ¥0.5/h 起
**官方文档**：https://help.aliyun.com/zh/api-gateway/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

## 大数据补充

### EMR（开源大数据平台 E-MapReduce）

**官方定位**：一站式开源大数据平台，托管 Hadoop/Spark/Flink/Hive/Presto/Trino/Hudi/Iceberg/Paimon/Doris/StarRocks 等全家桶。
**能做**：EMR on ECS（VM 集群）、EMR on ACK（K8s 弹性）、EMR Serverless Spark/StarRocks、数据湖格式 Hudi/Iceberg/Paimon、与 OSS-HDFS/MaxCompute/Hologres 互通
**不擅长**：纯托管 SaaS 体验（→ MaxCompute）；强实时 OLAP 且不想管集群（→ Hologres）

**典型选型场景**：自建 Hadoop/Spark 上云、湖仓一体（Paimon + StarRocks）、Flink 实时计算、客户已有开源生态需保留、AI 训练数据预处理
**对位竞品**：AWS EMR / Azure HDInsight / 华为云 MRS / Databricks（部分场景）
**报价量级**：EMR on ECS = ECS 集群 + EMR 软件费（约 +20%）；Serverless Spark ¥0.66/CU·h；Serverless StarRocks 见下方独立卡
**官方文档**：https://help.aliyun.com/zh/emr/
**证据等级**：[官方]
**最近更新**：2026-06-26

---

### EMR Serverless StarRocks（全托管 OLAP 分析引擎）

**官方定位**：基于开源 StarRocks 的全托管 Serverless OLAP 服务，兼容 MySQL 协议，面向实时数仓、多维分析、数据湖查询。

**能做**：
- **两种架构**：存算一体版（FE+BE，3 副本高可用）| 存算分离版（FE+CN，OSS 持久存储+本地缓存）
- **四种表模型**：主键表（Primary Key，实时 Upsert）/ 明细表（Duplicate Key）/ 聚合表（Aggregate Key）/ 更新表（Unique Key）
- MPP 全面向量化引擎（SIMD），CBO 优化器（Cascades-like），查询性能对比 ClickHouse/Doris 同级
- 智能物化视图（自动刷新+查询透明改写）
- 数据湖联邦查询：External Catalog 直查 Hive/Iceberg/Hudi/Delta Lake/Paimon（Parquet/ORC/CSV）
- AI+OLAP（Beta）：SQL 内调用 LLM
- 全托管免运维：可视化管控台、自动升级、StarRocks Manager（权限/慢 SQL/数据管理）

**不擅长**：纯事务型写入（→ RDS/PolarDB）；超高并发点查 KV 场景（→ Tair/Lindorm）；ETL 数据加工调度（→ DataWorks+Flink）

**典型选型场景**：
- 实时数仓（Flink/CDC→StarRocks 秒级可见）
- 多维 BI 报表（OLAP Cube 替代）
- 湖仓一体查询加速层（Paimon/Iceberg 上层 StarRocks 加速）
- 用户画像大宽表（主键表 Partial Update）
- 实时指标看板（高 QPS 低延迟）

**对位竞品**：ClickHouse Cloud / Snowflake / BigQuery / 腾讯云 CDWPG / 火山引擎 ByteHouse / Apache Doris（SelectDB）

#### 规格体系（1CU = 1 核 + 4GB 内存，标准规格；1RCU = 1 核 + 8GB，内存增强型）

| 节点类型 | 可选 CU | 用途 |
|----------|---------|------|
| FE | 4/8/16/32/64 CU × 3（或 5 高并发） | 元数据管理、查询规划、事务协调 |
| BE（存算一体） | 8/16/32/64 CU × N | 计算 + 本地存储，3 副本 |
| CN（存算分离） | 8/16/32/64 CU × N | 无状态计算，秒级弹性，OSS 持久 |

#### BE/CN 规格规划公式（查询维度）

```
CU总数 = 扫描数据总行数 / CPU处理能力(行/秒) / 预期响应时间(秒) × QPS
```
CPU 处理能力参考：高复杂度 SQL ≈ 2000 万行/s，中复杂度 ≈ 5000 万行/s，低复杂度 ≈ 1 亿行/s。

| 场景规模 | 复杂度 | QPS | 建议规格 |
|----------|--------|-----|----------|
| 5000 万行 | 高 | 50 | 16CU × 4 BE |
| 10 亿行 | 中 | 50 | 64CU × 6 BE |
| 300 亿行 | 高 | 10 | 64CU × 8 BE |

FE 选型表：BE 总 CU <120→8CU×3；120~1000→16CU×3；1000~3000→32CU×3；≥3000→64CU×3。高并发点查建议 FE 增至 5 节点。

#### 存储规划

- **存算一体**：总存储 = 原始数据 × 3 副本 / 压缩比(3:1~5:1)；单 BE 磁盘 = 总存储 / 80% / BE 数；ESSD PL1 达到最大 IO 需 460GB+
- **存算分离**：缓存空间 = 原始数据 / 压缩比 × 热数据比例；**主键表场景需额外 +20% 缓冲**（主键索引占缓存盘）

#### 主键表（Primary Key Table）— 实时更新核心

**适用场景**：实时 CDC 同步（Flink-CDC/Canal→StarRocks）、多流 JOIN 大宽表（Partial Update）、冷热数据分区更新。
**写入模式**：Delete+Insert（Merge-on-Write），查询性能比 Merge-on-Read 的 Unique Key 表高 3~10 倍。

**主键索引内存公式**：
```
索引内存 = (主键字节数 + 9) × 行数 × 副本数 × 1.5
```
示例：bigint(8B) 主键，5000 万行，3 副本 → (8+9)×5000 万×3×1.5 ≈ 3.8GB

**持久化索引**（`enable_persistent_index = true`，默认开启）：大部分索引落盘（SSD），内存压力降 80%+，性能接近全内存。存算分离版 3.3.2 起支持对象存储持久化。

**写入吞吐经验值**：[实战]
- 单 32CU BE 节点 Stream Load：纯追加约 80-120MB/s，80% 更新场景约 50-80MB/s（compaction 开销）
- 第三方 benchmark（16 核 128GB BE×3，120GB 数据）：首次全量写入约 37-38MB/s/节点，增量更新约 70-74MB/s/节点

**Compaction 调优**：
- `update_compaction_num_threads_per_disk`：默认 1，高写入建议 2-4
- 导入 bucket 数 ≥ BE 节点数（推荐 10-20）
- 批次间隔 ≥ 10s，避免小文件风暴
- `write_buffer_size`：写入与查询并发时适当调大

**限制**：主键列必须包含分区列+分桶列；仅支持 Hash 分桶；单主键编码后 ≤128B；建表后不可修改主键。

#### 导入方式矩阵

| 方式 | 适用场景 | 数据量 | 格式 |
|------|----------|--------|------|
| Stream Load | 本地文件/小批量实时 | ≤10GB | CSV/JSON |
| Broker Load | HDFS/OSS/S3 批量 | 数十~数百 GB | CSV/Parquet/ORC/JSON |
| Routine Load | Kafka 实时流 | 微批 MB~GB | CSV/JSON/Avro |
| Pipe | HDFS/S3 批量或实时 | 100GB~TB | Parquet/ORC |
| Flink Connector | Flink 实时写入 | 实时流 | 自定义 |
| Insert Into | SQL 结果集/小数据 | 按内存 | SQL |

#### 计费详表（华东 2 标准规格 ESSD）

| 计费模式 | CU 单价 | 208CU 集群月成本 |
|----------|---------|-----------------|
| 包年包月 | ¥157/CU/月 | ≈ ¥32,700/月 |
| 按量付费 | ¥0.3272/CU/时 | ≈ ¥49,000/月（7×24） |

存储另计：ESSD PL1 包月 ¥1.5/GB/月，按量 ¥0.0021/GB/时。
内存增强型（1RCU=1 核 8GB）：包月 ¥208.8/CU/月，按量 ¥0.4351/CU/时。
乌兰察布最低：标准 ¥141.28/CU/月，按量 ¥0.2944/CU/时。
海外最贵日本东京：按量 ¥0.4862/CU/时。

#### 选型决策树

```
实时更新 ≥30% → 主键表（存算一体更稳，存算分离更弹性）
    ├─ 写入吞吐需求 → 按 50-80MB/s/32CU BE 估算节点数
    ├─ 数据量 <1TB → 存算一体（性能确定性强）
    └─ 数据量 >5TB 或冷热明显 → 存算分离（成本低，弹性扩缩）
纯 OLAP 查询 → 明细表/聚合表 + 物化视图
湖上加速 → 存算分离 + External Catalog
```

**避坑要点**：
1. 主键表 compaction 跟不上写入会触发限速 → 提前调大 compaction 线程
2. 主键索引全内存模式在大数据量（>10 亿行）下 OOM 风险 → 务必开 persistent_index
3. 存算一体 3 副本写放大约 3×，大量更新时磁盘 IO 是瓶颈 → 多磁盘拆分
4. BE 规格选型不能只看查询 CU 公式，写入场景需独立按吞吐估算
5. 包月比按量便宜约 33%（约 6.7 折），长期运行务必转包月
6. 高性能存储（本地 SSD i2g/i3/i4）和大规格存储（HDD d2s）按整机规格计费，非 CU 体系

**官方文档**：https://help.aliyun.com/zh/emr/emr-serverless-starrocks/
**证据等级**：[官方] + [实战]（写入吞吐经验值来自第三方 benchmark + 客户 POC）
**最近更新**：2026-06-26

---

### Quick BI（智能 BI）

**官方定位**：阿里云原生的企业级 BI 与数据可视化产品（Gartner ABI 魔力象限连续 4 年入选）。
**能做**：拖拽式仪表板、即席查询、订阅推送（钉钉/邮件）、数据填报、行级权限、移动端、嵌入式（IFrame/JS SDK）、AI 智能问数（结合通义千问）
**不擅长**：极复杂自定义可视化（→ DataV）；自助探索深度（→ Tableau/PowerBI 仍占优）

**典型选型场景**：企业经营驾驶舱、销售/运营看板、客户嵌入式 BI、政府数据公开、行业 SaaS 自带 BI 模块
**对位竞品**：Tableau / Power BI / 帆软 FineBI / 观远 Guandata / Apache Superset
**报价量级**：标准版 ¥1980/账号·年（5 账号起），高级版 ¥2880/账号·年，专业版按节点报价
**官方文档**：https://help.aliyun.com/zh/quick-bi/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

## 运维补充

### OOS（运维编排服务）

**官方定位**：阿里云原生的免费自动化运维编排服务，类似 AWS Systems Manager。
**能做**：模板化运维任务（YAML/JSON）、批量执行 Shell/PowerShell、参数仓库、定时任务、补丁管理、合规审计、跨账号编排、与 RAM/ActionTrail/CloudMonitor 联动
**不擅长**：复杂业务流编排（→ 函数计算/SAE 工作流）；CI/CD（→ 云效 Flow）

**典型选型场景**：批量打补丁、批量重启 ECS、统一变更窗口、合规巡检（CIS/等保自查）、多账号资源批量配置、自助式日常运维（事故应急脚本一键执行）
**对位竞品**：AWS Systems Manager / Azure Automation / 华为云 COC / Ansible Tower
**报价量级**：免费（仅按底层调用的 ECS/RDS 等资源计费）
**官方文档**：https://help.aliyun.com/zh/oos/
**证据等级**：[官方]
**最近更新**：2026-06-18

---

## 全产品域选型速查表

| 产品域 | 核心产品 | 一句话选型建议 |
| --- | --- | --- |
| 计算 | ECS / ACK / ACS / SAE / FC | 有 K8s → ACK/ACS；无 K8s + 微服务 → SAE；事件驱动 → FC |
| 存储 | OSS / NAS / CPFS / EBS | 对象 → OSS；共享文件 → NAS；AI 训练 → CPFS；块 → EBS |
| 网络 | VPC / CEN / ALB / NLB / GA / SAG | 多地域 → CEN；L7 → ALB；L4 → NLB；出海 → GA；分支接入 → SAG |
| 数据库 | RDS / PolarDB / Lindorm / Tair | OLTP → RDS/PolarDB；NoSQL → Lindorm/Tair |
| 大数据 | MaxCompute / Hologres / Flink / EMR | 全托管离线 → MC；实时 OLAP → Hologres；流计算 → Flink；开源生态 → EMR |
| BI | Quick BI / DataV | 报表/驾驶舱 → Quick BI；大屏可视化 → DataV |
| AI | 百炼 / PAI / Qwen | MaaS → 百炼；自训练 → PAI；模型调用 → DashScope |
| 视频 | VoD / Live / RTC / MPS | 点播 → VoD；直播 → Live；实时互动 → RTC；纯转码/AI → MPS |
| IoT | IoT Platform / Link IoT Edge | 设备接入 → IoT Platform；边缘计算 → Link IoT Edge |
| 中间件 | MSE / RocketMQ / Kafka / API Gateway | 业务消息 → RocketMQ；流式 → Kafka；微服务 → MSE；API 管理 → API Gateway |
| 安全 | WAF / DDoS / 云安全中心 / RAM | 6 层纵深防御全覆盖 |
| 监控 | ARMS / SLS / CloudMonitor / OOS | APM → ARMS；日志 → SLS；基础 → CM；自动化运维 → OOS |
