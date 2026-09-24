# 阿里云产品知识库 — aliyun-products.md

> **定位**：每个阿里云产品的“能力卡”——能做什么 / 不能做什么 / 选型场景 / 报价量级 / 避坑要点。
> **更新方式**：每蒸馏一个产品的官方文档或 ATA 文章后，落到对应小节。
> **写法**：保持可扫读，限制单产品 < 200 字 + 链接索引；详细参数走 help.aliyun.com 实时查。

> **📋 产品卡模板扩展（2026-08-05 新增）**：所有**主要数据库 / 大数据产品**卡（ADB / Hologres / ClickHouse / PolarDB / RDS / MaxCompute / EMR / Lindorm / Flink 等）必须包含以下 4 个固定字段（模式B 第 6 步 / 模式C 红线 2 的执行支撑）：
> 1. **购买路径**：commodityCode + 购买页 URL（`common-buy.aliyun.com/?commodityCode=…` 或产品页"立即购买"入口）
> 2. **最低起步约束**：节点数 / 网关数 / 存储容量 / ACU / CU 的强制下限与步长（如 Hologres 网关 ≥ 2、ADB 企业版 ≥ 3 节点步长 3、EMR Master ≥ 3）
> 3. **规格页可用性**：`✅ 有独立规格页` / `❌ Serverless 无规格页` / `⚠️ 部分（按 CU/RCU 池计量）` / `⚠️ 只能预付资源包`
> 4. **采购流程兼容性**：`包月-可锁定预算` / `按量-需专项审批` / `采购走不通-仅按量`
>
> **当前进度**（2026-08-05 二版核验后）：
> - **详细核验数据的唯一权威来源** = [../references/pricing-verification-checklist.md § 3.1 全域速查表 v2](../references/pricing-verification-checklist.md) — 通过 5 个 subagent 并行核验，覆盖 30+ 主要 DB/大数据/AI/存储产品的 commodityCode / 最低起步 / 规格页可用性 / 采购流程兼容性四字段
> - **红色预警清单** = [../references/pricing-verification-checklist.md § 3.2](../references/pricing-verification-checklist.md) — 11 条已下线/无法新购/不可转包月的 SKU 警戒清单（如 RDS SQL Server Serverless 已停售、Lindorm Serverless 无法新购、PolarDB/RDS Serverless 均不能转包月）
> - **本文件（aliyun-products.md）的角色**：产品**业务/技术能力卡**，不再重复堆放 4 字段；只在 ADB / Hologres / ClickHouse / PolarDB / RDS / MaxCompute / EMR / Flink / DataWorks / Tair / 百炼 / PAI 等主要产品卡末尾放"⚠️ 报价前必读"锚链指向速查表相应行
> - **回归保障**：`scripts/check-purchase-paths.py` 每次执行前会检查速查表是否覆盖所有主要产品名 + 4 字段关键词齐全

**↔️ Cross-references**：
- 场景应用 → [cloud-solutions.md](cloud-solutions.md)(产品如何组合成方案)
- 竞品对位 → [competitor-cloud.md](competitor-cloud.md)(同类产品跨云对比)
- 客户实践 → [company-profiles.md](company-profiles.md)(哪些客户在用)
- AI 产品演进 → [ai-trends.md](ai-trends.md)(百炼/PAI/通义变化趋势)
- 选型矩阵 → [../references/cloud-product-mapping.md](../references/cloud-product-mapping.md)(场景反查产品)
- **采购路径核验** → [../references/pricing-verification-checklist.md](../references/pricing-verification-checklist.md)（报价前 10 条硬门禁清单 + 20+ 产品购买路径速查表）

**[[wikilink]] 实体索引**：本文件核心实体 → [[ECS]] [[ACK]] [[ACS]] [[FC]] [[PolarDB]] [[RDS]] [[Tair]] [[Hologres]] [[MaxCompute]] [[百炼]] [[PAI]] [[MSE]] [[RocketMQ]] [[Kafka]] [[WAF]] [[SLB]] [[OSS]] [[CDN]] [[Flink]] [[DataWorks]] [[StarRocks]] [[云原生API网关]] [[AI网关]] [[ext-auth]]

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
**报价量级**：标准 0.12 元/GB/月；低频 0.08；归档 0.033；冷归档 0.015；深度冷归档 0.0075（LRS 中国内地按量目录价；ZRS 标准 0.15/低频 0.10，归档族仅 LRS）
**存储计费规则速查（LRS 中国内地，2026-08-26 官方核验，源：aliyun.com/price/detail/oss + storage-fees + lifecycle 费用页）**：①最低存储时长与起算点：低频 30 天/归档 60 天从 **Last Modified（上传）时间**起算，冷归档/深度冷归档 180 天从**转换时间**起算；不足时长按剩余时间补收存储费——30 天生命周期（3 天标准+27 天降冷）下低频刚好不触发补收、归档补 30 天、冷归档/深度冷归档补约 153 天；②取回费 元/GB：低频 0.0325、归档 0.06（归档直读 0.2）、冷归档 0.2/0.06/0.03（高优先级/标准/批量）、深度冷归档 0.13/0.018，标准免费；③解冻时延：归档约 1 分钟（或直读实时）、冷归档 1~12 h、深度冷归档 12/48 h；④非标准类型 64 KB 最小计量单元；请求费标准 PUT 0.01 元/万次（每地域每月前 500 万次免费）、低频/归档族 PUT/GET 0.1/万次，生命周期转换按 PUT 类计费；⑤短生命周期（30 天）选型结论：冷归档纯成本判死（有效 0.102 元/GB > 低频 0.084）；归档存储费反比低频低约 11%（0.0747），分界线在取回费——冷数据回读比例 >≈38% 时低频赢、近零回读归档省约 11%；深度冷归档存储最省（0.057）但 12/48 h 解冻，官方定位"年访问不到 1 次"，仅零回读+容忍天级取回才值得
**流量费用速查（出向，中国内地，2026-08-25 官方核验）**：①外网流出（公网直出 NetworkOut）**0.50 元/GB**（闲时 00:00-08:00 **0.25**）；②OSS→CDN 回源流出（CdnOut）**0.15 元/GB**（OSS 侧收；CDN 边缘→用户下行另由 CDN 收约 0.24 元/GB，缓存命中后实际回源量远小于下行量）；③**内网流出免费**（同地域 ECS/VPC 走内网 Endpoint）；④跨区域复制（CRR）**0.50 元/GB**；⑤传输加速 Endpoint 叠加 **1.25 元/GB**；入方向全部免费；4xx/5xx 请求不产生流量费。预付费流量包：下行流量包 100GB 49元/月、1TB 505元/月、10TB 4874元/月（≈0.48~0.49 元/GB）；回源流量包 1TB 153.6元/半年。🔴 **OSS 流量由 OSS 独立计费，不并入 CDT，CDT 共享流量包不能抵扣 OSS 流量**（CDT 覆盖 ECS/EIP/CLB/FC 等，见「出云流量费」条目）。海外地域单价另查价格计算器。优化抓手：下载分发前置 CDN、同地域消费走内网 Endpoint、稳定直出买下行流量包
**避坑**：跨区域流量费易忽略；小文件大量 LIST 操作费用可观；归档取回需等待；🔴 **AsyncFetch（异步取回，镜像回源族扩展 API，可主动提交任务让 OSS 后台从源站 URL 异步抓取文件写入 Bucket，SDK 侧为 SetBucketAsyncTask/GetBucketAsyncTask）已下线、不再支持新开通**——原 API 文档已 404，仅存错误码页 0041-00000401（2026-08-25 核验）；替代：镜像回源（GET 404 触发同步按需回源，仍正常支持）/ 在线迁移服务（批量主动迁移，含 HTTP 源站）/ 自建 FC+ECS 抓取上传
**官方文档**：https://help.aliyun.com/zh/oss/
**证据等级**：[官方]
**最近更新**：2026-08-26

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

### ENI（弹性网卡）

**官方定位**：在 VPC 中为 ECS 实例提供网络接口和 IP 地址的虚拟网卡。文档归属 **ECS 用户指南**（不在 VPC 目录下），API 在 ECS 2014-05-26 命名空间。

**类型（官方仅两类 + 两个特殊形态）**：
- **主网卡（Primary）**：实例创建时默认自带，每实例仅 1 个，**不可解绑、不支持热插拔、随实例释放**（主网卡保留仅部分地域开放）
- **辅助弹性网卡（Secondary）**：可独立创建、动态绑解绑、跨实例迁移，可关联与主网卡不同的安全组
- **Trunk 中继网卡**：仅 OpenAPI `Type=Trunk` 出现且标注「邀测中」，用户指南无独立说明 → 不对客承诺
- **ERI（弹性 RDMA 网卡）**：不是独立网卡类型，是 ENI 上开启 RDMA 的通讯模式（`NetworkInterfaceTrafficMode=HighPerformance`）

**关键属性与不可变项**：VPC（**创建后不可更改**）、交换机（决定可用区，必须与实例同 AZ）、MAC（唯一标识）、主私网 IPv4 + 辅助私网 IPv4、IPv6、安全组（可变）、绑定的 EIP。同一实例的多张 ENI 可分属同 AZ 下不同交换机。

**绑定/解绑规则**：
- **必须同 VPC + 同可用区**，不支持跨 AZ、不支持跨 VPC；一个 ENI 同时只能附加到 1 台实例
- 实例状态需「运行中」或「已停止」，**部分规格不支持热插拔，只能停机操作**
- 解绑 ≠ 删除：解绑后进入「待绑定」，IP/安全组配置保留可复用；**删除才释放私网 IP 并退出安全组**
- 随实例释放默认开启；关闭后网卡保留 —— 私网 IPv4/IPv6 保留、EIP 绑定关系保留、安全组关联解除

**配额（与实例规格强绑定）**：

| 规格 | 可绑 ENI 数 | 单网卡私网 IPv4 数 |
|---|---|---|
| ecs.g7.large | 3 | 6 |
| ecs.g8i.4xlarge | 8 | 30 |
| ecs.g7.32xlarge | 15 | 30 |
| ecs.g9i.48xlarge | 15 | 50 |

未绑定状态的 ENI 最多分配 10 个私网 IP；已绑定后受实例规格上限约束。单张 ENI 最多关联 10 个安全组。账号级地域配额走配额中心 `q_elastic-network-interfaces`（**默认值文档未明确**）。

**典型选型场景**：高可用/故障切换（网卡带 IP 漂移到备机）、多网卡业务与管理流量隔离、多私网 IP（多应用/负载均衡）、容器 Terway ENI 直通、组播源、eRDMA 高性能网络、网卡保留复用

**报价量级**：**ENI 本身免费**（仅受配额限制）；辅助私网 IP 是否单独计费 → 文档未明确；挂在 ENI 上的 EIP 独立计费

**避坑**：
- 🔴 **多网卡不会叠加实例网络带宽**（带宽由实例规格决定）—— 客户常误以为加网卡能扩带宽
- 🔴 同一子网挂多张 ENI 易触发**非对称路由**，官方建议改用「单网卡 + 多辅助私网 IP」
- 跨可用区不支持 ENI 直迁（迁移/容灾方案的高频卡点）
- 托管弹性网卡（云产品代持）只可看不可操作，越权报 `InvalidOperation.EniServiceManaged`

**官方文档**：https://help.aliyun.com/zh/ecs/user-guide/eni-overview
**证据等级**：[官方]
**最近更新**：2026-08-11

---

### EIP（弹性公网 IP）

**官方定位**：**可独立购买和持有的公网 IPv4 地址资源**（独立产品目录 `help.aliyun.com/zh/eip/`，非 VPC 子功能），支持与云资源动态绑定/解绑。

**可绑定对象（2026-08-11 官方口径）**：专有网络型 ECS（实际绑到其主网卡）、**辅助弹性网卡 ENI**、**私网 CLB**、公网 ALB、公网 NLB（ALB/NLB 需在负载均衡侧操作，每可用区 1 个 EIP）、公网 NAT 网关（1 个网关最多 20 个 EIP）、HaVip（1:1，需配额中心申请权限）。ECI 侧文档明确支持绑 EIP，但 EIP 产品文档未列入（跨产品口径不一致）。

**不能绑**：经典网络 ECS、**公网类型 CLB**（自带固定公网 IP，不可解绑换绑）、已有固定公网 IP 或已绑其他 EIP 的 ECS、已配 DNAT 条目的 ECS、跨地域资源。一个 EIP 同时只能绑 1 个云资源。

**EIP 绑 ENI 的三种模式（官方术语，"直通模式/cut-through" 不是阿里云术语）**：

| 模式 | API Mode | OS 内可见 EIP | 可绑 EIP 数 | 网卡类型 | 私网功能 | NAT ALG |
|---|---|---|---|---|---|---|
| 普通模式 | `NAT` | 否（需 DescribeEipAddresses 查） | = ENI 私网 IP 数（一一映射） | 主网卡 + 辅助网卡 | 可用 | 不支持（H.323/SIP/DNS/RTSP 等） |
| EIP 网卡可见模式（不推荐） | `BINDED` | 是 | 1（仅主私网 IP） | 仅辅助网卡 | **不可用** | 支持 |
| 多 EIP 网卡可见模式 | `MULTI_BINDED` | 是（需配静态 IP） | 10 | 仅辅助网卡 | 可用 | 支持 |

`MULTI_BINDED` **已停止接受新用户申请**；官方现推荐用 **VPC 附加网段**实现 EIP 网卡可见。包月 EIP 以 `BINDED` 模式绑辅助网卡时，EIP 到期释放会导致该网卡私网功能失效。

**带宽上限与突破路径**：
- 按使用流量计费：单 EIP 峰值 **200 Mbps**（非承诺指标）；单账号单地域该类 EIP 实际带宽总和 ≤ **5 Gbps**
- 按固定带宽计费：单 EIP 峰值 **500 Mbps**（业务承诺指标）；单账号单地域总和 ≤ **50 Gbps**（更大需找客户经理）
- 更大带宽 → 加入**共享带宽**（原带宽峰值失效；需 EIP 为按量 + 同地域 + 同线路；>1 Gbps 自动开分布式限速；BGP 多线北京/杭州/上海/香港 ≈ **3.36 元/Mbps/天**，青岛 3.12，东京 3.84；BGP 精品 香港/东京 9.667、新加坡 16.634 —— 2026-08-11 官网快照，以购买页为准）
- 全球就近接入 → **Anycast EIP**，单实例带宽峰值上限 5000 Mbps

**一台 ECS 挂多个 EIP 的唯一路径**：直绑只能 1 个。多 EIP 必须过辅助 ENI，两条官方路径：① 多张辅助 ENI 各绑 1 个 EIP（数量受规格族限制）；② 1 张辅助 ENI 分配多个辅助私网 IP，普通模式下 EIP 与私网 IP 一一绑定（10 个私网 IP → 最多 10 个 EIP）。单账号 EIP 默认配额 20 个。

**与固定公网 IP 的关系**：固定公网 IP 只能在创建实例时分配、不可换绑、随实例删除；**ECS/公网 CLB 的固定公网 IP 可转 EIP，IP 不变但操作不可逆**；包月 ECS 仅「按使用流量计费」的公网带宽可转，到期前 24h 不支持，**中国香港 BGP 精品线路不支持转换**。

**与 NAT 网关的关系（高频坑）**：公网 NAT 网关**自身不带公网 IP，必须绑 EIP**；出口 IP 优先级 = **实例固定公网 IP/EIP > DNAT IP 映射 > SNAT 条目绑定的 EIP**，即**已绑 EIP 的实例不走 SNAT**（排查"出口 IP 不对"必查此处，需先解绑 EIP；固定公网 IP 要先转 EIP 再解绑）；已绑 EIP 的 ECS 不支持配 DNAT，存量并存时优先走 EIP。

**地域限制**：**不支持跨地域绑定**（EIP 与云资源必须同地域）；**支持跨可用区**（EIP 无可用区属性）。中国地区 ECS 经 EIP 访问境外 ECS 延迟高，官方建议同 Region 部署或走 CEN。

**避坑速记**：`ifconfig` 看不到公网 IP 是普通模式的正常行为、不是故障；公网 CLB 不能绑 EIP（常被误当成"SLB 都能绑"）；EIP 绑不上 ECS 的四大原因（跨地域 / 已有公网 IP / 经典网络 / 实例状态异常）；EIP API 每用户每天 >500 次调用触发限速。

**计费拆解（2026-08-28 官方核验，源：/zh/eip/billing-overview + /zh/eip/pay-as-you-go/）**：两段式 = **公网网络费（流量费或带宽费）+ EIP 配置费（公网 IP 保有费）**；三种组合：按量·按流量（小时出账）/ 按量·按固定带宽（日出账，当日改带宽取当日最大值）/ 包年包月·按固定带宽（预付更优惠）。公网网络费按 EIP 自身规则结算**与所绑资源类型无关**；仅出向计费入向免费。
- **配置费单价**：中国内地 15 地域 **0.02 元/小时/个**（≈14.6 元/月）；首尔/东京/美欧巴墨 0.03；港/新/马尼拉/雅加达/曼谷/马来/迪拜 0.04（按固定带宽模式表述为 0.48/0.72/0.96 元/天/个，折合相同）
- **免配置费三情形**：① EIP **直接绑**专有网络型 ECS/ECI 且账号 EIP 配额 ≤2000（绑辅助网卡——哪怕已挂实例、NAT、CLB 照收；配额 >2000 后持有全部开收）② 从 IP 地址池分配（改收池保有费，北京示例 0.05 元/小时/个，池内未分配 IP 也收）③ BYOIP 自带 IP 上云
- 🔴 **按量 EIP 不绑任何资源也收配置费**，不用及时释放；欠费限 1 Kbps，7 天内补缴恢复，7 天后自动释放
- **流量单价（按流量，BGP 多线）**：内地 0.80（青岛 0.72/港 1.00/新马泰菲柔 0.75/吉隆坡首尔 0.80/东京 0.60/美欧 0.50/圣保罗 0.78/迪拜利雅得 1.00）；🔴 精品 3.0（港/东京等）与 5.16（新）元/GB，无免费额度不可抵扣
- **2024-12-17（UTC+8）分界**：之后首次创建按流量 EIP 的账号流量费自动走 **CDT** 出账（阶梯 0.80→0.75→0.70→0.65 + 220GB/月免费额度）；存量账号可自愿升级，升级后全部存量+新增切 CDT
- **带宽单价（按固定带宽，BGP 多线，5Mbps 阶梯）**：1~5M **0.96 元/Mbps/天** + 超 5M **3.36**（内地/港/新等；青岛 0.72/3.12、东京 1.152/3.84、迪拜 3.36/3.36）；超 5M 部分 ≈100.8 元/Mbps/月——大带宽贵的原因，量大转共享带宽；精品 9.667（港/东京等）/16.634（新）元/Mbps/天
- 官方示例（杭州）：按流量 60GB/天 = 48+0.3 元；按带宽 20Mbps 用 15h = [0.96×5+3.36×15]×15/24+0.3 = 34.8 元
- **官方文档**：什么是 EIP：https://help.aliyun.com/zh/eip/product-overview/what-is-eip ｜ 计费概述（原文「按 EIP 的出方向流量累计值收取，入方向流量不参与计费」）：https://help.aliyun.com/zh/eip/billing-overview ｜ 按量计费规则：https://help.aliyun.com/zh/eip/pay-as-you-go/ ｜ 限制：https://help.aliyun.com/zh/eip/product-overview/limits
**证据等级**：[官方]（计费单价 2026-08-28 核验，共享带宽价为 2026-08-11 快照）
**最近更新**：2026-08-28

---

### 出云流量费 / 公网费用计费模型（带宽 vs 流量 + CDT）

**对客高频问题**："什么是出云流量费？是不是只能按量？我买了带宽为什么还收流量费？"——统一用本条目回答。

**定义**：出云流量 = 数据从阿里云资源流向公网（出方向 egress），如 ECS 对外提供访问/响应下载、OSS 公网下载、API 返回数据。**入方向流量不计费**（全行业通行规则，阿里云 ECS/EIP/CDT 官方文档均明确）。账单上常以「云数据传输 CDT—按量付费出云流量」出现。

**概念辨析：ECS 公网带宽 vs EIP vs CDT**[2026-08-28]：三者不在同一层——ECS 公网带宽与 EIP 是**公网接入资源**（"路"），CDT 是**计费出账产品**（"账本"）。①ECS 公网带宽=实例附带能力非独立产品：创建时勾选分配固定公网 IP+设带宽，IP 与实例绑死（不可换绑/随实例删除/可转 EIP 且不可逆）；②EIP=独立购买的公网 IP 资源，动态绑/解绑 ECS、NAT、私网 CLB、辅助 ENI（同地域），两段计费（配置费+公网费）；③CDT 无需开通，凡"按使用流量"计费的出向流量（ECS 公网/EIP/CLB 公网/IPv6 网关/FC/网关类，共享带宽·GA·Anycast EIP 按主流量=出入取大）自动归入，账号维度合并累计阶梯计费；**按固定带宽属预付费，不走 CDT、不叠加流量费、也不享受 220GB 免费额度**——"买了带宽还扣流量费"几乎都是账单里混了别的按流量路径，CDT 控制台明细可定位。选型：IP 不动→实例固定公网 IP；要弹性（换绑/故障切换/给 NAT 做出口）→EIP；量大且稳→固定带宽绕开 CDT 阶梯。

**高频问答：「独享/共享」带宽是独立产品吗？网络产品全家福怎么分层？**[2026-08-28]：①🔴 不存在叫"独享带宽"的产品——"独享/共享"是**带宽使用形态**：独享=按固定带宽计费的带宽峰值归单一资源独用（ECS 公网带宽/EIP 各自按 Mbps 计价），共享=**共享带宽**这一独立产品（多个按流量 EIP 加入同一带宽池，按池峰值包月或按主流量=MAX(入,出)计费）；②全家福按层记：私网底座 VPC/ENI → 公网 IP 资源 EIP/Anycast EIP（全球就近接入）→ 出公网（出向）NAT 网关（多机共享出口）/EIP 直绑 → 入公网（对外服务）CLB/ALB/NLB（+WAF）→ 分发加速 CDN/DCDN → 互联 CEN（跨地域多账号）/GA（终端用户加速）/VPC 对等连接 → 混合云 高速通道/VPN 网关/PrivateLink；③记忆锚：**"买什么"都在资源层，CDT 只出现在账单层**（凡按使用流量计费的出向流量自动归入、阶梯 0.80→0.65、220GB/月免费），按固定带宽=预付费包断不走 CDT。

**三种付费方式（纠正"只能按量"的误解）**：
| 方式 | 计费逻辑 | 特点 | 适用 |
|---|---|---|---|
| ① 按固定带宽计费 | 按带宽峰值 × 时长（可包年包月锁预算） | 该资源流量**不再另收**流量费；带宽是承诺指标（EIP 固定带宽单实例峰值 500Mbps） | 流量稳定、利用率不极低 |
| ② 按使用流量计费 | 按实际出网 GB 后付费（CDT 阶梯） | 带宽峰值仅是上限非承诺（EIP 此类峰值 200Mbps） | 流量波动/突发 |
| ③ 预付费资源包 | 共享流量包抵扣 CDT 第一阶梯（0~10TB），覆盖按流量计费的 ECS/EIP/CLB/共享带宽（FC 除外）；CDN/OSS 另有各自流量包 | 本质是预付费流量 | 流量大且可预估 |

**CDT（云数据传输）口径（2026-08-24 官方核验）**：CDT 是公网/跨地域流量的**统一计费出账产品**，本身仅按量计费——所有"按流量计费"实例的出云流量自动归入 CDT 合并累计阶梯计费（多产品合并、区分地域、小时出账）。覆盖公网产品：ECS/EIP/CLB 公网/IPv6 网关/FC/模型在线服务/云原生 API 网关/MSE 云原生网关（按出向），共享带宽/GA/Anycast EIP（按主流量=出入取大）。跨地域：CEN/VPC 对等连接/专线网关等（无阶梯）。**固定带宽计费（ECS/EIP/共享带宽固定带宽）已预付费，不走 CDT、不叠加流量费、也不享受免费额度**。
- 免费额度（2025-06-01 起）：**220GB/月/账号**（中国内地 20GB + 非中国内地 200GB），仅出向、仅 BGP（多线）、当月不结转；按账号维度非实例维度。
- 阶梯价（BGP 多线，2026-08-24 快照）：中国内地 0~10TB **0.80 元/GB** → 10~50TB 0.75 → 50~150TB 0.70 → 150TB+ 0.65；亚太 0.70 起、欧美 0.50 起、中东/南美 0.78 起。
- BGP（多线）_精品（回国优化）：**无免费额度、不可用流量包/资源包抵扣**，亚太 3.00 元/GB 起——避坑点。
- ECS 公网示例（杭州）：固定带宽 10Mbps 包月 ≈ 525 元/月；按流量 0.8 元/GB。

**"买了带宽为什么还收流量费"排查路径**：①带宽计费只覆盖按固定带宽计费的那条路径，账单上的出云流量费来自**其他按流量计费的路径**——常见：按流量计费的 EIP、NAT 网关绑的 EIP、CLB/ALB 公网流量、OSS 公网下载、FC/网关公网出、跨地域 CEN 流量；②控制台显示的"带宽 200Mbps"若该 EIP 是按流量计费模式，只是峰值上限不是包断；③到 CDT 控制台看各产品流量明细定位来源。

**高频问答：ECS 从外部网站下载（如视频抓取）再传 OSS，收流量费吗？**[2026-08-28]：两段都近乎免费——①下载=入方向流量免费，仅需公网出口，按流量计费时出向只有请求/ACK 小包≈0、按固定带宽则付带宽费不另收流量费（赶时间选固定带宽，下载速度由带宽上限决定）；②ECS→OSS **同地域+内网 Endpoint（oss-cn-<region>-internal.aliyuncs.com）= 免费**（OSS 入向全免+内网流出免费）；🔴 唯一踩坑点=跨地域或误用公网 Endpoint，OSS 不收钱但 ECS 公网出向按 CDT 0.8 元/GB 首阶计费。实际账单≈ECS 实例费+带宽费+OSS 存储费（标准 0.12 元/GB/月）+请求费。后续若从 OSS 对外分发另计外网直出 0.5 元/GB（建议前置 CDN）；目标站在境外则用海外地域 ECS（内地可达性差）。另提示客户抓取内容涉及版权/对方服务条款。

**高频问答：纯下载场景"只付 ECS 的钱就能拿免费入云流量"成立吗？EIP 买按量还是包月？**[2026-08-28]：结论=**成立，须同时满足**：①EIP 选**按量付费·按使用流量·直绑 VPC 型 ECS**——配置费按官方免收规则免除（直绑+账号 EIP 配额≤2000），流量费只计出向而入向占绝对大头（出向仅请求/ACK≈0）→ EIP 账单≈0；②按流量模式下**带宽峰值设多少不花钱**（峰值只是限速帽，按实际出向 GB 计费），不存在"买一个 100M/200M 的 EIP"的买法，直接设 200M 帽；**包年包月 EIP 只有按固定带宽一种**=纯下载场景白付带宽钱，不选；③ECS 创建时**不勾固定公网 IP**（与 EIP 互斥）——100M 是 ECS 固定公网 IP 路线（按流量峰值上限）、200M 是按流量 EIP 路线，二选一。吞吐口径：200M 满载≈**2.1TB/天**（5TB/天≈3 路、50TB/天≈24 路并行）；200M 为非承诺尽力而为=用速率确定性换免费，要稳速得付固定带宽；小规格实例可能被规格族「网络带宽基础」再压一层。配合 ECS→OSS 内网 Endpoint 写，全链路公网费≈0。

**高频问答：在线迁移服务收费吗？外部 URL（如火山引擎）文件能直接迁到 OSS 吗？**[2026-08-28，官方计费项页 + HTTP/HTTPS 准备文档核验]：服务本身公测期**不收服务费**，周边费用照收——源端流出/下行流量（第三方云按其价格收，如火山引擎出向）、源端与目的端 API 请求费（List/Head/Get/Put/分片）、归档数据解冻取回费、跨境传输加速费（目的端 OSS 收）；目的端 OSS 入向流量免费，只付 PUT 请求与存储费。HTTP/HTTPS 源现为**清单制**：需做 manifest.json + example.csv.gz（Url/Key 必填且须 URL 编码，单 csv.gz ≤100MB，清单先传到 OSS 或 AWS S3 再在源地址填列表路径）；Url 须能直接 GET/HEAD 访问，🔴 不支持重定向（301/302）的 URL，时限签名 URL 须确保任务执行前不过期。源端是火山 TOS/腾讯 COS/华为 OBS/AWS S3/七牛且有 AK/SK → 走「第三方云存储」源类型更顺；OSS 作源端时与迁移部署地域同地域免外网读取费、跨地域产生外网读流量。单条或极少量文件不值得做清单，curl 下载 + ossutil cp 上传更实际。

**共享带宽口径补充（2026-08-28 官方核验，源：/zh/internet-shared-bandwidth/ billing-overview + pay-by-dominant-data-transfer + subscription）**：①**按主流量 = MAX(入,出)**，仅对较大方向计费（不是相加、不是只收出向），小时出账，内地 0.80 元/GB（青岛 0.72）；🔴 **下载重场景严禁用主流量模式**——50TB/天下行 ≈ 1500TB/月主流量 ≈ **101万/月**（阶梯后），比按流量 EIP 方案贵约 50 倍；②包年包月带宽单价：内地 BGP 多线 **80 元/Mbps/月**（青岛 72）→ 1Gbps 列表价 8万/月、4.7Gbps ≈ 37.6万/月；按量按带宽 3.36 元/Mbps/天（2026-08-11 快照）；③同样有 **2024-12-17 CDT 分界**（之后首建按主流量实例自动走 CDT 阶梯+220GB 免费额度）；④**入向"免费"的速率上限（2026-08-28 原文勘误版，源：/zh/ecs/product-overview/limits「公网带宽」节 + /zh/eip/product-overview/limits）**：ECS 单实例出网峰值=按流量计费 **100Mbps**、按固定带宽**包年包月 200Mbps / 按量付费 100Mbps**（🔴 200M 只给包月），且还受实例规格族「网络带宽基础」上限约束（三层天花板）；按流量 EIP 峰值 200Mbps（非承诺）、按固定带宽 500Mbps（承诺）；账号级单地域总和：按流量 ≤5Gbps、固定带宽 ≤50Gbps（ECS/EIP 同口径，更大提工单/找客户经理）——多 EIP 叠加须多台并行或经辅助 ENI（且多网卡不叠加实例带宽），单机不可靠。
**下载场景补充判据（2026-08-28 美偲客户会议互证）**：①从内容平台（抖音/火山）跨云拉取，**云 IDC IP 大概率被反爬拦截**[实战/推断]，流量免费也拉不动，方案前必须实测；②火山/腾讯"免费拉取"是结构性优势（内容原生在其体系内网搬运），阿里云物理不可对标，对策=按流量 EIP 抓取集群（入向免费）+ 商业上以存储收入补贴通道；③客户口中的"接口拉取"= OSS AsyncFetch（已下线）或在线迁移服务（公测免服务费，但签名/重定向/反爬受限）；④⚠️ 会议口径"OSS 单用户 5G 免费带宽"查无官方出处，对客引用前须找产品侧确认。

**成本优化抓手**：流量大且稳 → 转固定带宽或共享带宽包；波动流量 → CDT 阶梯 + 共享流量包；下载分发类 → 前置 CDN（CDN 流量单价远低于 EIP 直出）；跨地域 → CEN 带宽包替代按流量。经验判据：1Mbps 满载月流量 ≈ 316GB，利用率越高固定带宽越划算。

**与家用宽带的差异（对客解释口径）**：家用宽带=零售包月（运营商把网间结算成本打包进套餐价）；云=批发逻辑，数据中心 BGP 多线接入，出向流量真实产生运营商结算/中转成本，故按 GB 单独计价，且入向免费、出向收费是全球云厂商通行规则。

**主流云厂商对比（2026-08-24 核验）**：逻辑一致（出向收费/入向免费），模式有差异——AWS ≈$0.09/GB（首 10TB）+100GB/月免费、Azure ≈$0.087/GB+100GB 免费、GCP Premium ≈$0.12/GB（Standard 档更低）+小额免费，三家**通用出网流量基本只有按 GB 计量一种模式**（无"买带宽峰值"选项，仅专线端口费是固定的），且单价普遍高于国内；国内阿里云/腾讯云/华为云均提供**按带宽/按流量双模式**+流量资源包，选项更多。
- 来源：help.aliyun.com/zh/cdt/billing-1 ｜ help.aliyun.com/zh/cdt/internet-data-transfers/ ｜ help.aliyun.com/zh/ecs/public-bandwidth ｜ hokstadconsulting.com 三家对比（GBP 口径，[推断]换算）

**证据等级**：[官方]（阿里云部分）+ [推断]（海外价格换算与"批发/零售"解释框架）
**最近更新**：2026-08-24

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
**报价量级**（三引擎 × 三形态，包年包月 2c4g 参考）[官方][2026-06]:
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

**大表 DDL：秒级加字段（Instant DDL）**[官方][2026-08-19]：
- 原理：只改数据字典元数据，不重建表/不复制存量数据，**耗时与行数无关**——9000 万行同样秒级完成，业务无感
- **表末尾加列**（版本矩阵）：8.0 **默认支持**；5.7（≥5.7.1.0.6）需开参数 `loose_innodb_support_instant_add_column=ON`；5.6（≥5.6.1.0.43）需配额 `polardb_mysql_iac_56`；5.7 分区表另需配额 `polarM_57_iac_on_partition_table`
- **任意位置增删字段**（FIRST/AFTER + 秒级删列）：仅 8.0.2 ≥ **8.0.2.2.32**，需配额 `polarm_82_instant_add_drop_col` + 参数 `loose_innodb_polar_instant_add_drop_column_enable=ON`（默认 OFF）；单表次数上限默认 16（`loose_innodb_polar_max_table_metadata_version` 1~64），超限须重建表清零（查 `INNODB_INSTANT_TABLES.TOTAL_ROW_VERSIONS`）
- 语法：`ALTER TABLE t ADD COLUMN c INT DEFAULT 0, ALGORITHM=INSTANT;`（报错 0A000=不满足条件）；8.0.2 可先 `EXPLAIN DDL` 预判；不指定算法时优先级 INSTANT>INPLACE>COPY
- 🔴 限制：不支持与**其他 DDL 同条混跑**（加字段+加索引必须拆两条）；不支持 ROW_FORMAT=COMPRESSED 表、全文索引表（任意位置功能另含空间索引表）、开启 implicit_primary_key 且无自定义主键的表；末尾加列 5.6/5.7 不支持虚拟列（8.0 支持）
- IMCI 列存索引表：8.0.1.1.42/8.0.2.2.23 及以上 `imci_enable_add_column_instant_ddl=OFF`，低版本须 ON（且秒级加列后列存索引后台静默重建、期间不可用）
- 兼容关系：末尾加列过的表可继续用任意位置功能，反向不行；INSTANT 列遇表重建类 DDL（如 OPTIMIZE TABLE）自动转普通列（数据不丢）
- 🔴 **次数上限（row version 机制）**：每执行一次 INSTANT ADD/DROP 表 row version +1（**单条 ALTER 同时加多列只 +1**），MySQL 8.0 原生硬上限 **64 次**——达上限后显式 INSTANT 报 `ERROR 4080 Maximum row versions reached`，不指定算法则自动回退 INPLACE 全表重建；PolarDB「任意位置秒级增删」把上限参数化为默认 16；`OPTIMIZE TABLE`/`TRUNCATE` 重建表清零（查 `INNODB_INSTANT_TABLES.TOTAL_ROW_VERSIONS`）[官方][MySQL官方博客实证 2026-08-19]
- 兜底（Instant 不可用时）：原生 Online DDL（INPLACE）大表需全表重建，低峰期执行 + 可走 **DMS 无锁变更**（可调度/暂停/限速，文档 /zh/dms/lock-free-structure-change 与 /zh/dms/perform-lock-free-ddl-operations）
- 文档：/zh/polardb/polardb-for-mysql/user-guide/instant-add-column、instant-add-drop-column

**官方文档**：https://help.aliyun.com/zh/polardb/
**证据等级**：[官方]
**最近更新**：2026-08-19（新增秒级加字段 Instant DDL 小节）

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

**采购路径核验字段（2026-08-05 新增，模式B 第 6 步硬门禁）**：

| 版本 | commodityCode / 购买页 URL | 规格页可用性 | 最低起步约束 ⚠️ | 采购流程兼容性 |
|------|---------------------------|-------------|----------------|--------------|
| **ADB MySQL 企业版**（Enterprise） | `ads` / `adb_mysql_enterprise` — https://common-buy.aliyun.com/?commodityCode=ads | ✅ 有独立规格页 | **节点 ≥ 3 且步长 3**（可选 3/6/9/12…，**不可选 4/5/7**） | ✅ 包月可锁定预算；⚠️ 只按总 ACU 报价与实际购买档位对不上 — **必须对齐 3 节点步长档位** |
| ADB MySQL 湖仓版 | `adb_mysql` | ✅ 有 | 存储预留 24 ACU / 计算 8 ACU 起 | ✅ 包月-可锁定预算 / 按量-需专项审批 |
| ADB PostgreSQL 弹性模式 | `gpdb` | ✅ 有 | 4 段位起 | ✅ 包月-可锁定预算 |

**⚠️ 报价避坑**（2026-08-05 实战踩坑[实战]）：ADB MySQL 企业版官方计费文档只写单 ACU 单价（如 0.36 元/ACU·时），但购买页企业版**最低 3 节点起步、步长 3**，只按总 ACU 报价与实际购买档位对不上。修复：核对购买页可选档位（3/6/9…节点），报价按最近合法档位向上取整，扩容也是按节点整数倍。

**避坑**：写入量大时需调整分区键；与 Hologres 定位有重叠（选型需明确）；企业版 3 节点起步、步长 3 的档位约束在报价前必查。
**官方文档**：https://help.aliyun.com/zh/analyticdb/
**证据等级**：[官方] + [实战]（2026-08-05 采购路径核验）
**最近更新**：2026-08-05（新增采购路径核验字段 + 企业版 3 节点起步步长约束避坑）

---

### Hologres

**官方定位**：实时数仓，毫秒级交互式分析，MaxCompute 加速器。
**能做**：
- 行存 + 列存混合，HSAP（Serving + Analytical）
- MaxCompute 外表直读（零 ETL 加速）
- 实时写入+实时查询（亚秒级）
- 向量检索（**V4.0 起 HGraph 索引替代 Proxima Graph，官方标"推荐"；新方案勿按 Proxima 写** — 2026-08-08 勘误，详见 AI 域「向量检索 / RAG 检索引擎选型」一节）
- Serverless 模式

**不擅长**：纯 OLTP 事务（→ RDS）；超低延迟缓存（→ Tair）

**典型选型场景**：实时大屏、BI 加速、用户画像秒级圈选、推荐特征服务、MaxCompute 提速
**对位竞品**：AWS Redshift Serverless / GCP BigQuery / Snowflake
**报价量级**：32CU ≈ 5200 元/月；Serverless 按 CU*时计费；计算组网关 340 元/个/月（**但购买页最低 2 个起步**，实际最低 680 元/月）

**采购路径核验字段（2026-08-05 新增，模式B 第 6 步硬门禁）**：

| 版本 / 形态 | commodityCode / 购买页 URL | 规格页可用性 | 最低起步约束 ⚠️ | 采购流程兼容性 |
|------------|---------------------------|-------------|----------------|--------------|
| Hologres 独享（Standalone） | Hologres 产品购买页 → 独享 tab | ✅ 有 | 通常 32 CU 起 | ✅ 包月-可锁定预算 |
| **Hologres 计算组实例**（多 Warehouse） | Hologres 产品购买页 → 计算组 tab | ✅ 有 | **网关 ≥ 2 个**（不是 1 个）、Warehouse ≥ 1 | ✅ 可采购，但**网关最低 2 个必须写入 BOM**；只按 1 个报价漏一半 |
| Hologres Serverless | Hologres 产品购买页 → Serverless tab | 部分（按 CU 池计量） | 无规格，按用量 | ⚠️ 仅按量-需专项审批 |

**⚠️ 报价避坑**（2026-08-05 实战踩坑[实战]）：Hologres 计算组实例官方计费文档写"网关 340 元/个/月"，但购买页网关滑块起步是 **2 个**（不是 1 个），只按 1 个报价漏一半月成本。修复：BOM 里网关数量按 min 2 起步，备注列写清"购买页网关最低 2 个约束"，重新出总价。

**避坑**：宽表列数太多影响性能（建议<300列）；Table Group 设计影响查询效率；计算组网关最低 2 个起步的约束在报价前必查。
**官方文档**：https://help.aliyun.com/zh/hologres/
**证据等级**：[官方] + [实战]（2026-08-05 采购路径核验）
**最近更新**：2026-08-05（新增采购路径核验字段 + 计算组网关最低 2 个起步避坑）

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
**报价量级（Serverless 资源组模型，2026 现行）**：整合原独享调度/集成/数据服务资源组，统一按 CU 计费（1CU=1核+4GiB）。费用=资源占用费（CU）+任务调度费（生产环境成功运行的调度实例数，空跑不计）。两种付费：包年包月（月最低 2CU）/按量付费（约 0.5 元/CU时，上海）。计算型节点在 DataWorks 侧只占调度开销 CU（如 Hologres SQL 节点固定 0.25CU、ADB Spark 节点默认 0.25CU、MaxCompute PyODPS 0.5CU）。离线同步并发<4 约 0.5CU，≥4 为 (并发-4)×0.07+0.5 CU。
**关键计费边界（面客高频澄清点）**：DataWorks 只收「平台层」的资源组 CU + 调度费；底层计算引擎 MaxCompute/Hologres/**AnalyticDB(ADB)**/EMR 的实际算力+存储费用由各产品**各自独立出账**，不含在 DataWorks 账单内。客户常见困惑"用了 DataWorks 为何还对 ADB 收费"= 误把两层当一层：DataWorks=开发/调度/搬运驾驶舱，ADB=真正存数据+跑 SQL 的引擎，两笔钱对应两件事，非重复收费。
**避坑**：调度时间窗口拥堵（合理错峰）；大量小任务时调度延迟；数据集成并发配高会线性拉高 CU；包年包月资源组不支持转按量付费。
**官方文档**：https://help.aliyun.com/zh/dataworks/new-resource-group-overview
**证据等级**：[官方]
**最近更新**：2026-07-22（更新为 Serverless 资源组计费模型 + DataWorks/ADB 分层计费边界）

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
| deepseek-v4-pro | 12元 | 24元 | 三方模型，强推理 ⚠️[需复验] |
| deepseek-v4-flash | 1元 | 2元 | 三方轻量版（2026-08-12 已复验：1/2/缓存0.2，与 DeepSeek 官方输入输出持平） |

> ⚠️ **[需复验 2026-08-12]** 上表 deepseek-v4-pro 的 12/24 元为 **2026-06 快照**，而 DeepSeek 官方 `/zh-cn/quick_start/pricing` 当前为 **3 元 / 6 元（缓存命中 0.025 元）**，恰好是 12/24 的 25%——与 competitor-cloud.md 记载的"V4-Pro 永久降价 75%"吻合，**高度疑似本表未跟进降价**。对客引用 v4-pro 价格前必须先复验百炼 model-pricing 页，不要直接用 12/24。
- Batch 调用半价；上下文缓存享有折扣
- 每个新账号开通后 90 天内免费 100万 Token
**避坑**：RAG 切片策略影响召回质量（需调优 chunk_size + overlap）；并发有 QPS 上限；输入超 256K 触发阶梯加价

**模型价格 / 结算价 API（程序化读取每模型单价与计费方式）**[官方+推断][2026-09-18，2 路 subagent 联网核验]：
- 🔴 **无任何专用询价接口**：`bailian` 2023-12-29（55 个接口，全是知识库/文件/Prompt/Memory/检索类）+ `ModelStudio` 2026-02-10（38 个）里**没有** `GetModelPrice`/`DescribePrice`/`QueryPrice` 之类。这是"文档里查不到价格 API"的根因——价格能力被拆到「模型列表」和「账单」两处，且没有 Price 关键词可搜。
- **① 目录原价 + 计费方式 → `ListModels`**（唯一价格 API 来源）。两套等价实现：DashScope HTTP `GET /api/v1/models`（API-Key 鉴权，Endpoint `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models`，支持 name/provider/capability 等筛选，SDK `Models.list()` 仅支持分页不支持筛选）；POP OpenAPI `ModelStudio`/`2026-02-10`/`ListModels`（AK/SK 鉴权，🔴 **帮助中心无独立文档页、仅 next.api.aliyun.com 可见**，且 POP 版 schema **缺 `type` 字段**）。返回体 `prices[].range_name`（分段名，无分段=Default，阶梯如 `32k<Input<=128k`）+ `prices[].prices[].{type,price,price_unit,price_name}`（type=input_token/output_token/image_number…；price_unit=每百万 tokens/每张，POP 版注释国内￥国际$）。文档原话"获取模型的**定价**和上下文长度"。来源：help.aliyun.com/zh/model-studio/list-models
  - ⚠️[推断待实测]：官方只给 token 类 + "每张"两类示例，**视频按秒/TTS 按字符/按次**的字面值官方未列全枚举，结构上通用键值对理论支持，需实调视频/TTS 模型确认。
- **② 实际结算价（含折扣真实单价 + token 用量）→ 账单接口**：
  - **首选 阿里云统一费用 `BssOpenApi.DescribeInstanceBill(IsBillingItem=true)`**（ProductCode=`bailian`[推断，先 QueryProductList 确认]）。可行关键：百炼账单「实例ID（出账粒度）」明文编码模型名，官方写死格式 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`（例 `12xxx;llm-xxx;qwen-max;output_token;app;0`；训练类为 `业务空间ID!地域!训练任务标识`）。返回 `ListPrice+ListPriceUnit`（官方直接给的目录单价，无需反推）、`Usage+UsageUnit`（token/张/秒）、`PretaxAmount`/`PretaxGrossAmount`/`InvoiceDiscount`。每模型可算：目录单价=ListPrice；实际结算均价=ΣPretaxAmount/ΣUsage；折扣率=1−ΣPretaxAmount/ΣPretaxGrossAmount。限制：近 18 个月、金额延迟 24h（实例信息 48h）、当月仅供参考、次月 3 日 12 点后可对账、限流 10 笔/秒。来源：help.aliyun.com/zh/model-studio/bill-query-and-cost-management + api.aliyun.com/document/BssOpenApi/2017-12-14/DescribeInstanceBill
  - **备选 百炼自有 `GetBillingOverview`/`GetBillingTrend`**（ModelStudio 2026-02-10）：可按 `BASE_MODEL`/`API_KEY_ID`/`WORKSPACE_ID`/`MAAS_TYPE`(inference/training/model_units/capacity_reserved)/`FEE_TYPE`/`CHARGE_TYPE` 分组，但🔴 **只返回金额，无单价、无 token/张/秒用量**。要单价必须回 DescribeInstanceBill。
- **③ 拿不到（无任何 API，仅控制台/文档页）**：折扣价、活动优惠、商务价、峰谷价、Batch 5 折、上下文缓存折扣、**免费额度余额**。model-pricing 页官方原话"本文仅展示模型调用原价，请前往百炼控制台查看活动优惠"。百炼「模型用量」页也无 API（官方 FAQ：查账号 Token 总用量须去账单详情页导出；App 不支持看免费额度/用量）。
- 🔴 **BSS 询价类不适用百炼**[推断]：`GetPayAsYouGoPrice`/`GetSubscriptionPrice`/`DescribePricingModule`/`QueryPriceEntityList` 依赖标准 SKU 定价模块（RDS/ECS 那种 ModuleCode+PriceType=Hour/Usage/Month/Year），百炼这种按 token 的 MaaS 未走商品中心 SKU 上架流程，实调 `DescribePricingModule(ProductCode=bailian)` 大概率只返回粗粒度"大模型文本消耗量"一层、展不到每模型每百万 token 单价。
- **落地方案（推断）**：目录价用 `GET /api/v1/models`；实际结算用定时任务 `DescribeInstanceBill(IsBillingItem=true)` → `InstanceID.split(";")` 解析 model_name+token_type → 按 (模型,档位) 聚合 ListPrice/Usage/PretaxAmount；官网标价对拍只能爬 model-pricing 页（无 API）。

**增速限流 / 突发限流机制**[内部][2026-07]（来源：内部文档《百炼增速/突发限流现状和未来》3.1，全文见 raw/misc/misc-2026-07-16-bailian-rate-throttling.md）：
- **现状定性**：用户维度的**静态**增速限流——按用户自身历史流量环比控制突发，**未**感知模型服务的实时负载/服务能力。
- **增速计算逻辑**（环比 5 分钟前，两条约束同时生效）：
  - token 增速上限 = max( 5 分钟前 token 流量 × 30%（典型值）, 模型维度 token 增速配置值 )
  - 请求增速上限 = token 增速上限 / 5 分钟前请求平均 token
- **模型维度 token 增速（TPM）配置值随大盘基础流量水位而异**：基础流量大的模型配置高（如 qwen-plus 1000w），基础流量小的配置低（如 qwen3-vl-plus 400w）。
  - ⚠️ **口径澄清**：此处「TPM 增速配置值」= 突发时允许的 token 增量绝对值（用于上式 max 第二项），**≠ 稳态 TPM 限额**；稳态 RPM/TPM 限额（如 qwen-plus 30000 RPM / 500w TPM）见 [[ai-trends]]「百炼 API 限流表」。
- **客户维度可配增速限流重试**：随机指数退避，重试 1/2/3/4/5 次最长引入 6/15/36/63/114 秒请求延迟。
- **演进方向**：现状为静态限流；原文含“未来”章节（本次未随图提供），方向指向**动态负载感知限流**（结合模型服务实时负载/服务能力）。
- **SA 应对建议**[推断]：客户“偶发 429 / 延迟陡增”常是触发**突发增速限流**而非稳态 TPM 超限——① 平滑爬坡（避免 5 分钟内 token 陡增 >30%）、大促前预热放量；② 高基础流量模型（qwen-plus）突发容忍度显著高于小流量模型（qwen3-vl-plus），选型/压测需按目标模型实际配置评估；③ 重试次数与延迟 SLA 需权衡（5 次退避最长约 114s，同步链路可能不可接受，建议异步化 / 降级 / 多模型分流）。

**模型监控指标口径 + 请求高延迟排查（收包耗时）**[官方+实测][2026-08]（来源：help.aliyun.com model-telemetry / cloudmonitor 接入页 + 内部 Spectrum 链路 graph.js 前端源码 + 受控慢上传实验；配套排查工具见 skill `neil-bailian-trace-debugger`）：
- **公开监控指标（Prometheus，`model-telemetry` 页）三档延迟**：
  - `model_call_duration*`（模型调用时长，含 total/均值/p50/p99）= 「单次调用**从请求到完整响应返回的总耗时**」→ 口径上**包含收包段**，约等于网关整体耗时。
  - `model_first_token_duration*`（模型首包时长）= **TTFT**，「从请求开始到接收首个生成 Token」→ 对应内部链路模型接入节点的 `first_latency`，**基本不含收包段**。
  - `model_generation_duration_per_token*`（非首包时长/每 Token 平均生成耗时），与 `model_tps_per_request`（TPS，**仅高级监控/收费**）呈倒数关系（TPS ≈ 1÷非首包时长）。
  - 官方原话:排查响应慢要**结合 TTFT + 非首 Token 延时 + 输入 Token 量**综合判断,「总耗时还受**输入长度、网络**等因素影响,不能仅凭 TPS 判断」。**公开监控无独立「收包/上行接收」指标**,收包段只体现在「总耗时 − TTFT」的差值里。
  - 关键过滤标签:`protocol`（HTTP 非流式 / SSE 流式 / WS）、`status_code`/`error_code`（仅 `model_call_count` 支持）、`workspace_id`、`model`、`apikey_id`（-1=控制台调用）。高级监控（分钟级+TPS+失败详情）收费,普通监控免费但小时级,数据留 30 天。
- **内部链路分析（Spectrum）span 字段口径**[内部,graph.js 源码实证]:`first_latency`=首包耗时 / `last_latency`=尾包耗时 / `queue_latency`=排队耗时 / `algo_latency`=算法耗时 / `duration`=整体耗时 / **`receive_duration`=收包耗时** / `retry_delay`=突发限流。链路树按 rpc_id:`0`汇总→`0.1`网关(`dashscope.aliyuncs.com`,收包字段在此)→`0.1.1`chat 接入→prefill→decode。
- 🔴 **「收包耗时」= 网关从客户端「读完整个上行请求体」的墙钟时间**(受控实验实证:4KB 小包故意分块慢传 4.8s → 收包 4788ms 而模型仅 155ms;187B 秒发 → 收包 0ms)。它**只随客户端把请求发完的快慢变化**,与下游模型耗时、排队(独立 `queue_latency`)、首包(独立 `first_latency`)**完全解耦**。
- **高延迟排查判据(SA 可对客话术)**[实战]:若「总耗时高(几百秒)但 TTFT 低(几秒~几十秒)」→ 慢在**收包段**,即**客户调用侧把请求体传上来慢,非百炼模型服务问题**(模型要等 body 收完才开工)。进一步区分"客户端 vs 网络":**看收包耗时是否随输入 token 数增长**——若不相关(实测 7.1 万 token 收 222s、15.1 万 token 反而 202s,曲线平),则**排除带宽/体积瓶颈,指向客户端排队/延迟发送**(连接已建但请求在本地等并发额度、Agent 边组装上下文边发、慢代理/隧道)。建议客户抓包量「TCP 建连→最后一个请求包」时间,查 SDK 并发上限与是否流式上传。
- **边界**:①公开 TTFT 是否含收包段官方未逐字定义(措辞"从请求开始"偏向含,标[推断]);②`receive_duration` 是**新网关埋点**,老 trace(如早期 glm-5.2 案例)网关节点无此字段;③需拆 `reasoning_tokens`/`cached_tokens`/`http_code` 时查 FBI「用户请求查询」报表(reportId 1328072),Spectrum 只给 duration/TTFT/tokens/链路。

**Token Plan（AI 大模型订阅服务）**[官方][2026-08]（来源：token-plan-overview / token-plan-personal-overview / token-plan-team-overview 三页）：
- **定位**：以 **Credits 统一计量**的订阅服务，面向 AI 编程/智能体工具（Claude Code、Cursor、Qwen Code、Qoder、Qoder CN、OpenClaw），支持文本/图片/视频/实时语音对话生成模型 + Harness 工具（web_search/t2i_search/i2i_search/web_extractor/code_interpreter）。**套餐内模型均为完整版**（含 GLM-5.2 未经量化压缩、未功能裁剪，推理/代码能力与按量付费完全一致）。**仅限工具内交互式使用，禁止裸 API 用于自动化脚本/应用后端**（违规封禁）。仅华北 2（北京）地域。
- **与 Coding Plan 关系**：两个独立产品，不可迁移/升级；Coding Plan Lite 2026-03-20 停新购、04-13 停续费升级，Pro 限量售罄不补。官方推荐转 Token Plan。
- **个人版**（同一实名主体限购 1 份；**数据会用于服务改进/模型优化**）：
  | 档位 | 限时价(原价) | 5h 限额 | 7 天限额 | 并发 Agent |
  | --- | --- | --- | --- | --- |
  | Lite | ¥39(60)/月 | 700 | 2,500 | 1-2 |
  | Standard | ¥139(180)/月 | 3,000 | 10,000 | 3-4 |
  | Pro | ¥499(600)/月 | 12,000 | 40,000 | 6-8 |
  - 双窗口限额自首次调用起算，任一触顶即暂停；可买用量包（¥100/个/月=20,000 Credits，需有效订阅、最多持 5 个）或用"额度重置"功能（耗重置次数）；额度不结转。
  - 限时权益：qwen3.8-max 夜间(22:00-08:00)5 折；qwen3.8-max-preview 限时 1 折（10 倍量），夜间再 2 折=0.2 折；预览版结束后下线或转正。
  - 升级补差价立即提额；不支持降级；**暂不支持退订**；续费仅延期不补额度；到期重购 API Key 变更。
- **团队版**（席位制，**承诺不用数据训练模型**，多租户隔离高峰不排队；专属 Base URL 兼容 OpenAI/Anthropic 接口）：
  | 座席 | 限时价(原价) | 月度额度 |
  | --- | --- | --- |
  | 标准 Standard | ¥150(198)/席/月 | 25,000 Credits |
  | 高级 Pro | ¥550(698)/席/月 | 100,000 Credits |
  | 尊享 Max | ¥1,398/席/月 | 250,000 Credits |
  - 月度总额度制，**无 5h/7 天窗口限额**；超额阻断；共享用量包 Extra Bundle ¥5,000/个=625,000 Credits，有效期 1 个月、到期清零、优先抵最近到期。抵扣顺序：席位额度→共享包。
  - 限时优惠仅适用包月新购/续费/自动续费；包年与升级座席不参与；加购按剩余时长折算，实收取折算与限时价较低者。
  - 席位管理：分配/回收自动生成专属 API Key（1 席 1 人 1 Key，禁共享）；支持加购/升级/批量/按席退订（已消耗不可退，原路退款 1-3 工作日）；退订重购 API Key+Base URL 变更。
  - 订阅周期：**计费周期按订阅月起算（非自然月）**，如 6/4 订阅则本周期至下月 4 日；订阅后**一次性发放全量月度额度**（非按天发放），**续费仅延长有效期、不为当前周期叠加补充额度**。包月/包年/连续包月包年；自动续费次日生效、到期前 9 天扣款。个人版+团队版可同时持有、独立计费。
- **Credits 计费机制**：按模型分档抵扣系数，随 Token 用量/思考模式/工具调用动态计算；视频等异步任务完成后集中结算（易短时触顶，建议低时长低分辨率试跑）。**官方抵扣公式**：`Credits 抵扣额度 = 模型推理用量(百万 tok) × 模型单价(元/百万) × 官网折扣 × 100`——即约 `单价(元/百万) × 100` = 每百万 tok 的 Credits 数（12 元/百万 tok 模型≈1,200 Credits/百万）；官方示例 qwen3.7-max 抵扣系数 0.0015（10,000 tok≈15 Credits）。另一示例 qwen3.6-plus：输入 8,349 tok≈1.67 + 缓存 40,794≈0.82 + 输出 573≈0.69 ≈ 3.18 Credits（Credits 与 Token 无固定换算，最终以控制台用量明细/账单为准）。
- **与按量付费 / 节省计划(资源包)的关系**：三者可在**同一账号并存**，靠**不同 API Key** 区分调用。Token Plan 用**专属 API Key + Base URL**，与按量付费/节省计划链路**完全隔离**（两者必须配套使用，不能混用 Key）；套餐内 **Credits 优先抵扣**。适用场景分野——**高频调用且模型相对固定→Token Plan**（预付费订阅、无需管理实例）；调用量不稳定/少量测试→按量付费；用量大且稳定、追求折扣→节省计划/资源包。三种模式的模型推理能力完全一致，仅计费模式不同。
- **模型清单差异**：个人版 14 个（qwen3.8-max/-preview、3.7-max/plus、3.6-flash、audio-tts、glm-5.2、deepseek-v4-pro/flash-0731、wan2.7-image(-pro)、happyhorse-1.1 i2v/t2v/r2v）；团队版 25 个（多 qwen3.6-plus、qwen-image-2.0(-pro)、kimi-k2.5/2.6/2.7-code、glm-5/5.1、MiniMax-M2.5、deepseek-v3.2、deepseek-v4-flash）。Token Plan 团队版清单括注「deepseek-v4-flash-0731 暂不支持 Responses API」——🔴 **该限定仅见于 Token Plan 侧**，`/zh/model-studio/deepseek-api` 与 Responses 兼容页均已将其列入支持清单、模型广场详情页也挂出了内置工具价格，判为**按量付费已放开、Token Plan 未同步**[推断]，详见下文「Responses API 内置工具与工具调用价格」小节第 ⑤ 条。
- **SA 提示**[推断]：① 企业客户关注数据训练条款→必须推团队版（个人版数据用于训练）；② 客户想用 API 集成自有应用→Token Plan 违规，走按量付费；③ 团队版折算单价 ¥0.0055-0.008/Credit，档位越高越便宜，共享包最贵（¥0.008），可作超量缓冲而非主力；④ 与 Meoo 订阅（¥39-89/月个人）是不同产品线，勿混淆。

**语音模型文件输入（fun-asr / Paraformer 系录音文件识别）× OSS 流量费**[官方+推断][2026-08-25，当日二次核验修正]（来源：fun-asr 录音文件识别 HTTP API 页 + ISI《使用录音文件识别时如何设置OSS内网地址》FAQ 页 + 《通过终端节点私网访问阿里云百炼模型或应用 API》(access-model-studio-through-privatelink，2026-08-18 更新) + OSS 控制台 Bucket 概览实测）：
- **机制**：`file_urls` 只接受 HTTP/HTTPS URL（文档口径单次请求 1 个 URL），由百炼后端按 URL 拉取音频；OSS 侧流量费取决于 URL 走哪个域名。
- **🔴 服务地域口径（二次核验修正，推翻初版）**：fun-asr 是**部署在百炼 VPC 内**的模型服务，**不是** ISI 录音文件识别服务。初版曾引用 ISI FAQ「录音文件识别服务部署于华东2（上海）/华北2（北京）/华南1（深圳）」套用到 fun-asr，**该口径不适用，已撤销**。以 PrivateLink 官方文档为准：**百炼无专属网关，仅公网 dashscope.aliyuncs.com + PrivateLink 两种接入；百炼服务所在地域：公共云 = 华北2（北京）、新加坡**（美国弗吉尼亚暂不支持私网访问）。即**中国大陆站 fun-asr 的拉取出口在北京**。
- **✅ OSS 内网 Endpoint = 免流量费，但 bucket 必须在北京**：OSS 计费侧同地域内网流出免费（见 OSS 卡「流量费用速查」）；OSS 内网 Endpoint 从同地域 VPC 可达（OSS 控制台 Bucket 概览「访问端口」表含「ECS 的 VPC 网络访问（内网）」= `oss-cn-<region>-internal.aliyuncs.com` 官方行）。因此 bucket 在华北2（北京）→ fun-asr 走内网拉取、零流量费；**上海/深圳/其他地域 bucket 的 internal 域名从北京 VPC 不可达，任务直接失败（不会降级走公网扣费）**。内网域名格式 `<BucketName>.oss-cn-beijing-internal.aliyuncs.com`。另注意：PrivateLink 连接为**单向**（仅客户 VPC 主动访问百炼，百炼不能反向访问客户 VPC），文件拉取别指望走它，就是靠 OSS 同地域内网。
- **✅ 实测验证（2026-08-25 晚，北京 ECS + 新建 dashscope PrivateLink 端点全链路跑通）**：①任务A=PrivateLink 端点域名（HTTP）提交 fun-asr + `file_urls` 用 luck-test-bucket **内网签名 URL** → **SUCCEEDED**，转写文本正常（百炼后端确实按内网 URL 拉取成功）；②任务B=公网 dashscope+公网签名 URL 对照 SUCCEEDED；③任务C=ms-happyhorse 内网匿名 URL → **FAILED `FILE_403_FORBIDDEN`**——bucket policy 拒绝匿名读取时百炼后端同样 403，与网络路径无关，须先解决对象可读性（签名 URL 或改 policy）。④OSS 内网域名从北京 VPC 解析 100.118.x、47KB 下载 0.09s；PrivateLink 端点解析 VPC IP、TCP 6ms。⑤**端点 ENI 机制**：接口端点会在客户 vSwitch 里落一张 ENI（实测解析到 10.20.192.61，与 ECS 同网段），端点域名只在该 VPC（或互通 VPC）内可达——所以端点必须建在调用方 ECS 同 VPC，这正是「为什么和我 VPC 有关」的答案：服务在百炼侧，但私网入口在你 VPC 里。⑥**两段链路独立**（实测四组合）：公网 dashscope API + 内网 OSS 签名 URL 同样 SUCCEEDED——省 OSS 流量费靠 file_urls 内网域名（后端同地域拉取），与 API 段是否走 PrivateLink 无关；PrivateLink 仅解决 API 段不出公网的合规需求，无此要求可删端点省 0.07 元/h。⑦**异步事件链路（2026-08-26 实测）**：fun-asr 与 qwen-audio-3.0-asr-flash-filetrans 任务完成均自动向北京默认事件总线发事件（source=acs.dashscope、type=dashscope:System:AsyncTaskFinish；43 文件批量全部推送），事件体**直接内嵌 output_result（含 transcription_url）**——消费方收事件后直接 GET 结果，无需轮询任务查询接口（查询接口仅作兜底）；客户侧落地=EventBridge 规则过滤 source/type 后推 HTTP 端点（公网或 VPC 私网）或 RocketMQ。坑：**EventBridge 事件查询仅控制台可用**（CLI EventCenterQueryEvents 是控制台内部 API，AK 签名直调返回 InternalError）。证据等级升为 **[实测]**。
- **实测工程坑**：①云助手 RunCommand 的 `{{param}}` 自定义参数替换**未生效**（key 原样发送报 InvalidApiKey），改 sed 内联注入；②账号开启**阻止公共访问**，`put_object_acl(public-read)` 报 0016-00000901，**签名 URL 是默认姿势**——oss2 签名与 host 无关，用 internal endpoint 的 Bucket 对象 sign_url 即得内网签名 URL；③PrivateLink 默认端点域名**仅 HTTP**（API Key 内网明文），生产建议自定义服务域名+HTTPS；④PrivateLink 计费=**0.07 元/小时·可用区 + 0.07 元/GB 双向**（验证完可 DeleteVpcEndpoint 止损）；⑤带 deny policy 的 bucket：RAM 用户 LIST/GetBucketPolicy 均 403「Access denied by bucket policy」、匿名 GET 403「because of bucket acl」、控制台主账号可读——排查权限差异先看登录身份是主账号还是 RAM；**但 RAM 签名 GetObject 实测放行（HTTP 200）**——policy 只挡列表/匿名、不挡授权读，故此类 bucket 正解=**RAM 签名内网 URL**：ms-happyhorse 真实视频（3分51秒/aac 双声道/usage 165s）走「内网签名 URL + PrivateLink + fun-asr」全链路 SUCCEEDED，ECS 内网直连 27.5MB 0.4s（72MB/s）。
- **三种失败返回语义**[Neil 口径 + 2026-08-26 三件均实测触发]：`CLIENT_ERROR` = URL 有、文件可下载、但**文件中没有音频**（实测提交 PNG 对象，message="have no audio"）｜`FILE_DOWNLOAD_FAILED` = URL 有但**不能被下载**（实测不存在对象的签名 URL 404）｜`ASR_RESPONSE_HAVE_NO_WORDS` = URL 与文件都有、音频轨正常、但**没有有效人声**（实测纯静音视频）。排查序=下载层→音频轨层→内容层；前两者修地址/修数据，最后一种正常业务返回不重试。与 `FILE_403_FORBIDDEN`（匿名拉取被 deny policy 拒，签名 URL 解决）区分：后者是 FILE_DOWNLOAD_FAILED 族的权限版本。
- **fun-asr 文档给出的两条 OSS 专属路径（均不建议生产用）**：① `oss://` 前缀临时 URL——仅 RESTful 支持、SDK 不支持；临时 URL 48h 过期、上传凭证接口限流 100 QPS 不支持扩容，官方明说「请勿用于生产环境、高并发及压测」；② 请求头 `X-DashScope-OssResourceResolve: enable`（OSS 公网临时访问不通时的兜底）——官方标注「不推荐该方式」，且 Java/Python SDK 不支持配置 headers。
- **私有 bucket 注意**：内网域名只解决「可达+免流量」，文件本身仍须可读——公共读或带签名（presigned）URL，否则 403。
- **三方式对照**：内网 Endpoint（仅北京 bucket）= 0 元流量，需实测｜公网 URL（公共读/签名）= 外网直出 0.5 元/GB（闲时 00:00-08:00 0.25），稳定可用，量大买下行流量包≈0.48-0.49 元/GB｜oss:// 临时 URL / OssResourceResolve = 生产不推荐。
- **SA 话术**[推断]：客户批量转写降本，先问 bucket 地域；在北京→直接内网域名零流量费（实测一单后切生产）；不在北京→优先把素材 bucket 迁/复制到北京，否则退回公网 URL+流量包，勿指望跨地域内网。
- **文档**：https://help.aliyun.com/zh/model-studio/access-model-studio-through-privatelink ｜ https://help.aliyun.com/zh/model-studio/fun-asr-recorded-speech-recognition-http-api ｜ https://help.aliyun.com/zh/isi/developer-reference/how-to-set-the-internal-endpoint-of-oss-when-using-recording-file-recognition（仅 ISI 产品口径）

**非实时 ASR 三模型对比：fun-asr vs qwen-audio-3.0-asr-flash-filetrans vs qwen-audio-3.0-asr-flash**[官方][2026-08-26]（来源：asr-model/ 模型列表页 + 三个模型详情页 + non-realtime 用户指南，2 路 subagent 交叉核验）：
- **共同底座**：三者均为百炼非实时 ASR，**同价**北京 0.00022 元/秒、新加坡 0.00026 元/秒（≈0.792 元/小时，仅计语音时长，多音轨每轨独立计费），同限流 **600 RPM**，同一 30 语种+汉语七大方言+20 余地区口音语言表（qwen3-asr-flash 系另有一套较短列表）。
- **家族谱系**：Paraformer（较早一代，官方建议迁移）→ **Fun-ASR**（fun-asr 主版本）→ **Qwen-Audio-3.0「百聆」**（2026-07-31 上线，官方定位 Fun-ASR 的升级替代）。🔴 勿与 **qwen3-asr-flash** 系混淆——后者是另一系列，独有能力=情感识别，但无热词/说话人分离，限流仅 100 RPM。
- **三模型分工**：
  - `fun-asr`：长音频异步（HTTP 提交+轮询，X-DashScope-Async），≤12h/2GB，17 种音视频格式任意采样率，file_urls 单次 1 个 URL；说话人分离 ✓（单声道 2-100 人，建议≤2h）、句/字级时间戳固定开启、**预编译热词** vocabulary_id（权重1-5）、敏感词过滤 ✓、**不支持 Prompt Context**（仅快照 fun-asr-flash-2026-06-15 支持）；language_hints 仅 1 个值生效；结果=transcription_url（24h 有效）。
  - `qwen-audio-3.0-asr-flash-filetrans`：长音频异步（同 fun-asr 调用形态与 12h/2GB/17 格式规格），= fun-asr 的官方升级替代：**即时热词**（免预编译，权重 1-5 或 50）+ **Context Prompt 上下文增强** + `language_hints` 最多 4 语种混识；说话人分离 ✓（同规格）；句/字级时间戳；官方场景=短视频字幕/客服质检/金融双录/播客访谈/「谁说了什么」。
  - `qwen-audio-3.0-asr-flash`：**短音频同步**（HTTP 单次请求直接返回，URL/Base64 单次 1 个），≤5 分钟；大小上限两处文档冲突（模型列表页 ≤2GB vs 用户指南 ≤10MB，引用须标注）；热词+Context ✓、时间戳固定开启、**无说话人分离**、无情感识别；专项优化古诗词韵律+标点预测+数字/日期/金额 ITN 归一化。
- **选型判据**[推断]：①长音频/多人会议/通话质检 → 新项目直接 filetrans（同价能力超集），存量 fun-asr 可继续用但官方导向迁移；②≤5min 短音频且要同步低延迟拿结果 → qwen-audio-3.0-asr-flash；③要情感识别 → 只能 qwen3-asr-flash 系（无热词/分离，RPM 100）；④要实时流式 → qwen-audio-3.0-asr-flash-streaming（WebSocket，不限时长）或 fun-asr-realtime；⑤8kHz 电话场景 → fun-asr-flash-8k-realtime。
- **OSS 流量口径复用**：filetrans/flash 与 fun-asr 同为百炼 VPC 内模型服务，上文「file_urls × OSS 内网免流量（北京 bucket）」结论同族适用；**filetrans 已实测（2026-08-26）：内网签名 URL 全链路 SUCCEEDED、43 文件矩阵成功率与 fun-asr 一致、EventBridge 完成事件同样发出**；flash（同步版）仅 ≤10MB 小文件可用，批量场景不选。
- **文档**：https://help.aliyun.com/zh/model-studio/asr-model/ ｜ /qwen-audio-3-0-asr-flash ｜ /qwen-audio-3-0-asr-flash-filetrans ｜ /fun-asr ｜ /non-realtime-speech-recognition-user-guide

---

#### Anthropic 兼容接口（Messages）接入要点[官方][2026-08-10]

> 来源：help.aliyun.com/zh/model-studio/anthropic-api-messages（Anthropic兼容-Messages）+ /claude-code。适用于把 Claude Code / Claude Desktop / Anthropic SDK 指向百炼。

- **端点路径**：SDK 的 `base_url` 只填到 `/apps/anthropic`，HTTP 直调是 `POST {base_url}/v1/messages`。
  - 华北 2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`
  - 新加坡 / 法兰克福 / 东京：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`；美国（弗吉尼亚）无 WorkspaceId 前缀，为 `https://dashscope-us.aliyuncs.com/apps/anthropic`
  - `{WorkspaceId}` = 控制台「业务空间详情」里的业务空间 ID，**必须替换**，忘记替换是最高频的接入失败原因。旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 仍可用，官方建议迁新域名。
- **认证**：`x-api-key: $DASHSCOPE_API_KEY` **或** `Authorization: Bearer $DASHSCOPE_API_KEY`，二选一。`anthropic-version` 头官方示例未使用，非必需。
- 🔴 **只有 `/v1/messages`，没有 `/v1/models`**：Claude Code / Claude Desktop 的 model discovery 会自动在 base URL 后拼 `/v1/models`，必然 404 → 在客户端 Models 里**手动加模型名**跳过自动发现。另：base URL 若误填成 `.../apps/anthropic/v1/`，会拼成 `/v1/v1/models` 双 `/v1` 404。
- **支持模型**：Qwen 全系（max/plus/flash/turbo/coder/VL/开源）+ 第三方 `glm-5.2 / glm-5.1 / glm-5 / glm-4.7 / glm-4.6`、deepseek-v4-pro / v4-flash / v3.2、kimi-k2.5/2.6/2.7-code/k2-thinking、MiniMax-M2.5/M2.1。第三方模型清单标注 `tp-region-bj`（北京地域），**跨地域可用性可能不同，非北京地域调 glm-5.2 前先确认**。
- 🔴 **GLM-5.2 的 `max_tokens` 语义与众不同**（必选参数）：不传 `thinking.budget_tokens` 时，`max_tokens` = **回复内容 + 思维链之和**上限；传了 `budget_tokens` 时，`max_tokens` **仅约束回复内容**。给小了会直接被思维链吃光、`stop_reason=max_tokens` 返回空正文。
- **其他迁移差异**：`temperature` 取值 `[0, 2)`（Anthropic 官方是 `[0.0, 1.0]`）；`stop_sequences` 命中后 `stop_reason` 仍为 `end_turn` 且不回填命中序列；thinking 块的 `signature` 当前固定空串；流式 `message_start` 的 `usage` 只有 input/output，完整 4 字段在 `message_delta`。
- **结构化输出**：严格 json_schema 模式仅 deepseek 系列与 **glm 系列**支持；其他模型走普通模式时 prompt 里必须含 "json" 字样，否则报 `'messages' must contain the word 'json' in some form`。`output_config` 是百炼扩展参数（Python 用 `extra_body`，TS 用 body 透传）。
- **显式缓存**：`cache_control: {"type":"ephemeral"}`，最小可缓存长度 1024 Token，用量看 `cache_creation_input_tokens` / `cache_read_input_tokens`。
- **Key 隔离红线**：Token Plan 用**专属 API Key + 专属 Base URL**，与按量付费/节省计划链路完全隔离，两者不能混用；且 Token Plan **禁止裸 API 用于自动化脚本/应用后端**（见上节）。集成自有应用只能走按量付费 Key。
- **排障噪音提醒**[实战]：curl 在 `-v` 模式下遇到 `-X POST` + `-d` 会打印 `Note: Unnecessary use of -X or --request, POST is already inferred.` —— 这是 curl 自身的冗余提示（`-d` 已隐含 POST），**不是百炼返回的错误**，退出码 0、请求正常发出。非 verbose 模式不打印。排障时应看 HTTP 状态码与响应体，勿被此行误导。

---

#### Responses API 内置工具与「工具调用价格」[官方][2026-08-12]

> 来源：help.aliyun.com/zh/model-studio 的 `web-search` / `web-extractor` / `code-interpreter` / `compatibility-with-openai-responses-api` / `deepseek-api` 五页实时核验（curl 抓全文本地解析，2026-08-12）。触发：Neil 问模型广场 deepseek-v4-flash-0731 详情页的「工具调用价格」是什么。

**① 概念界定 —— 与 function calling 是两件事，模型卡上并列但计费完全不同**：

| | function calling（模型卡"能力"栏） | 内置工具（模型卡"工具调用价格"栏） |
| --- | --- | --- |
| 工具由谁执行 | **你自己的代码**执行，模型只输出要调哪个函数、传什么参 | **百炼服务端托管执行**，结果直接回灌进上下文 |
| 是否单独计费 | **不额外收费**（只算 Token） | **按次收费**，与 Token 费叠加 |
| 调用方式 | Chat Completions / Responses 均可 | **必须走 Responses API**（`tools=[{"type":"web_search"}]`） |

**② 三个内置工具与单价**（华北 2 北京，2026-08-12 官网口径）：

| 工具 | 作用 | 单价 | 关键限制 |
| --- | --- | --- | --- |
| `web_search` | 联网搜索（百炼自有检索链路，query 经多次改写+脱敏后才外发，不透传原文） | **4 元/千次 = 0.004 元/次**；🔴 **新加坡 73.392381 元/千次（≈18.35 倍）** | 15 RPS（主账号维度、跨 API Key 跨模型合并计） |
| `web_extractor` | 给定 URL 抓正文 | **限时免费** | "限时"即未来会收费，长周期 TCO 不能按 0 算 |
| `code_interpreter` | 沙箱执行 Python | **限时免费** | 仅 Python；**不能读写外部文件 / 装包 / 联网**；算力与时长受限 |

- Responses API 方式调用 `web_search` 时，**计费等同 `agent` 策略**（4 元/千次）。Chat Completions 侧 `search_strategy` 另有档位：`turbo` 3 元/千次、`max` 4 元/千次（均 2026-02-27 起正式计费）、`agent` 4 元/千次、`agent_max` 限时优惠（搜索 4 元/千次 + 抓取免费）。
- 🔴 **与「联网搜索 MCP」是两套独立计费**：MCP 版全部用户前 2000 次免费、之后 **29 元/千次**（比内置工具贵 ~7 倍），报价不要混用。

**③ 真正的成本大头是 Token 不是工具费**：搜到的网页正文会拼进 prompt 变成输入 Token，按模型标准价另算。官方实测例子：问"杭州天气"，未联网输入 **10 Token**，联网后 **1953 Token**。
- 折算：一次 0.004 元的 web_search，等价于 **4,000 个输入 Token @1 元/百万**。对 deepseek-v4-flash（输入 1 元/百万）这类廉价模型，**工具费常与 Token 费同量级甚至更贵**；对 qwen3.7-max（12 元/百万）则工具费可忽略。→ 报价时"便宜模型 + 高频联网"必须把工具费单列一行，别只算 Token。
- **按工具调用次数计费，不是按请求次数**：agent 类策略一轮对话可能触发多次检索，成本上限按"请求数 × 平均搜索轮数"估。

**④ 避坑**：
- 🔴 **超 15 RPS 时 API 不报错，只是静默跳过搜索**。判断是否真搜了：DashScope 看响应有无 `search_info` / `usage.plugins`；OpenAI 兼容协议无明确标识，只能看输入 Token 是否暴涨。
- 模型自行判断"不需要联网"时也不会搜，需强制走 `forced_search: true`；英文提问触发率偏低，官方建议中文提问或强制。
- deepseek-v4 系的 Responses API **仅华北 2（北京）与新加坡**；新版路径 `/compatible-mode/v1/responses`，旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停维。

**⑤ 🔴 文档冲突（对客前必须实测）—— deepseek-v4-flash-0731 到底支不支持 Responses API**：
- **说支持**：`/zh/model-studio/deepseek-api` 明写"deepseek-v4-flash、deepseek-v4-flash-0731 与 deepseek-v4-pro 支持通过 OpenAI 兼容的 Responses API 调用"；`/compatibility-with-openai-responses-api` 支持模型清单含该型号；模型广场详情页已挂出三个工具价格且标 `Responses API` 徽标。
- **说不支持**：`token-plan-team-overview`（Token Plan 团队版模型清单）与 2026-08-03 上线公告（aliyun.com/product/news/30085）均括注"**暂不支持 Responses API**"。
- **判断**[推断]：按量付费链路已放开、**Token Plan 链路未放开或文档未同步**。对客只能说"按量付费下可用，Token Plan 下需实测"，不可直接承诺。
- 另：`/zh/model-studio/web-search` 页仍写"Responses API 仅支持 Qwen3.8/3.7/3.6/3.5/qwen3-max"，**该句已过时**（未同步 DeepSeek 接入）。

**⑥ 该模型卡其他可读信息**（2026-08-12 控制台截图）：输入 1 元 / 输出 2 元 / 缓存命中 0.2 元（每百万 Token）；支持 function calling、cache 缓存、联网搜索；**不支持**结构化输出、批量推理、前缀续写、模型调优；**免费额度"不支持开启"**；页面挂官方提示"**deepseek-v4 系列模型价格近期将有所上调**" → 长周期报价需预留涨价缓冲。

**⑦ 🔴 高频误解澄清：「内置工具是 DeepSeek 模型的原生能力」——错**（与 api-docs.deepseek.com 逐项对照，2026-08-12）：

> 关键概念：**"服务端托管工具"按定义就是平台能力，不可能写在模型权重里**。模型权重能做的只有一件事——按训练好的格式吐出"我要调 web_search，query 是 XX"。真正去执行搜索 / 抓网页 / 跑 Python 的是**你连的那个平台**。同一份 deepseek-v4-flash-0731 权重，连不同平台得到的工具集完全不同：

| 工具 | DeepSeek 官方 API（api.deepseek.com） | 阿里云百炼 |
| --- | --- | --- |
| `function`（客户侧执行） | Supported | Supported |
| `web_search` | **Supported, executed on the server side**（含 `web_search_2025_08_26` 版本别名；`search_context_size`、`user_location` **被忽略**） | Supported，走**阿里自有检索链路**，4 元/千次（北京） |
| `web_extractor` | 不在支持清单 → 落入"其他 built-in tools → **Ignored**" | **百炼独有**，限时免费 |
| `code_interpreter` | 官方文档明写 **Ignored**（静默忽略，不执行也不报错） | **真的能跑**，限时免费 |
| `file_search` / `computer_use` / `mcp` | 全部 **Ignored** | 另有 MCP 广场独立体系 |

- **这张表本身就是判据**：若属模型原生能力，同一权重不会出现"在 DeepSeek 官方 `code_interpreter` 被忽略、在百炼能跑"。
- **模型原生的到底是什么**：是 **tool-use 的训练**——DeepSeek 确实把 web_search 训进了模型（带 OpenAI 式版本号 `web_search_2025_08_26`，且 `web_search_call` 输入项支持原样回传、由服务端还原搜索结果），模型知道何时该发起搜索、如何消费返回结果。**准确表述：能力 = 模型的 tool-use 训练 × 平台的工具执行托管，缺一不可；4 元/千次买的是后者。**
- **四条佐证是阿里链路而非 DeepSeek 链路**：①北京 4 元 vs 新加坡 73.39 元差 **18 倍**——模型能力不会因机房不同差 18 倍，只有采购的搜索供应商不同才会；②同一套工具同一价格也挂在 Qwen 全系上，**跨模型统一定价**；③`search_strategy`（turbo/max/agent/agent_max）、`forced_search`、`search_info`、15 RPS 限流**全是百炼扩展参数**，DeepSeek 官方 API 无此概念；④**DeepSeek 官方定价页全页 0 处提及 search 计费**，只列 Token 价。
- 🔴 **收费逻辑对比：DeepSeek 官方对 web_search 不单独计费，百炼单独计费**（全站核验，2026-08-12）。DeepSeek 官方 `/zh-cn/quick_start/pricing` 扣费规则原文只有一句：**「扣减费用 = token 消耗量 × 模型单价」**；`pricing` / `token_usage` / `rate_limit` / `responses_api` / `create-response` / `faq` / `updates` **七页全站 0 处提及搜索计费**；且其 Responses API 的 `usage` 只返回 `input_tokens`（含 `cached_tokens`）与 `output_tokens`（含 `reasoning_tokens`）——**没有任何工具调用计数字段，结构上就无法按次计费**。搜索结果仍会变成 input_tokens 计费，这点两边一致。
- 🔴 **单价对照（均为官方人民币原价，每百万 Token，无汇率折算）**：DeepSeek 官方 deepseek-v4-flash = **缓存命中 0.02 元 / 缓存未命中 1 元 / 输出 2 元**（v4-pro = 0.025 / 3 / 6）。对比百炼 deepseek-v4-flash 的 1 / 2 / **缓存命中 0.2 元**——**输入输出完全持平（百炼未加价），但缓存命中百炼是官方的整 10 倍**。高缓存命中率场景（Coding Agent 基线 70%~92%）该项会主导两侧成本差，测算不能只比输入输出单价。**两边都已公告近期涨价**（DeepSeek 原文"计划近期整体上调 DeepSeek API 服务的定价，**预计涨幅较大**"）。
- 另：DeepSeek 官方 Responses API **仅支持 deepseek-v4-flash，不支持 deepseek-v4-pro**（官方称 2026 年 8 月初增加支持），其上线动机原文写的是"为了满足大家对 **Codex** 的需求"——与百炼把 Responses API 当作 Agent 原生能力入口的定位不同。另官方 `tool_choice` 可直接指定 `{"type":"web_search"}` 强制搜索，对应百炼的 `forced_search: true`。

---

#### 知识库（RAG）完整规格与计费[官方][2026-08-08]

> 来源：help.aliyun.com/zh/model-studio 知识库计费/使用限制/检索配置/Retrieve API 系列页 + 官方公告 118448 / 117726 / 118217，4 组 subagent 实时核验 + 独立事实核查员复核。价格标注日期 **2026-08-08**。
> ⚠️ 本节是百炼 RAG 的**唯一权威口径**，与 [cloud-solutions.md S3 早期 RAG 章节](cloud-solutions.md) 若有冲突以本节为准（S3 已加勘误锚点）。

**① 规格档位 —— 只有标准版 / 旗舰版两档，不存在"高级版"**（常见误传，报价前必须纠正）：

| 档位 | 检索 QPS | 平台存储 | 规格费单价 | 折算月费 |
| --- | --- | --- | --- | --- |
| 标准版 | **1 QPS 固定、不可调** | ≤ 100 GB | 0.03 元/知识库·小时 | ≈ **21.6 元/月** |
| 旗舰版 | 50–10,000 QPS = **1–200 RCU**（1 RCU ≈ 50 QPS，所需 RCU = ⌈峰值 QPS / 50⌉）| ≤ 9,999 GB | 0.2 元/RCU·小时 | 1 RCU ≈ **144 元/月** |

- 同一知识库**每自然日最多变配 1 次**；**变配本身不收费**。
- **免费额度**：一次性 **720 小时**，**仅抵扣标准版规格费**；**旗舰版无免费额度**；新用户自开通起 **30 天有效**。

**② 计费结构与扣费顺序**：
- 总费用 = **规格费**（按运行时长 / RCU·小时，**与实际用量无关**）+ **模型调用费**（Token：文档解析 / Embedding / Rerank / 生成）。
- 扣费顺序：**免费额度 > 资源包 > 按量付费**。
- **删除知识库才停止计费**（停用/不调用不停计费）——与 Flink"释放工作空间才停计费"同类陷阱。

**③ 预付资源包（可锁定预算的唯一路径）**：

| 资源包 | 档位与价格 |
| --- | --- |
| RAG 标准版 | 1 个/月 **20 元**；1 个/季 **59**；1 个/年 **239**；10 个/年 **2,099**；50 个/年 **9,999**；100 个/年 **18,999** |
| RAG 旗舰版 | 1 RCU/月 **139**；1 RCU/季 **399**；1 RCU/年 **1,599**；10 RCU/年 **14,999**；30 RCU/年 **41,999**；50 RCU/年 **65,999** |

- 资源包**有效期 1 年、过期作废**；未使用部分可申请退款。
- ⚠️ **节省计划只能抵扣模型调用费，不能抵扣知识库规格费**——报价时不要用节省计划折扣去打规格费。

**④ ⚠️ 报价避坑（本轮最重要洞察）— Rerank 按「初步召回的总切片数」计费，不是最终返回数**：
- 初步**向量**检索 TopK 默认 **50** + 初步**关键词**检索 TopK 默认 **50**（各自范围 10–100），两路切片**全部进 Rerank**。
- 官方示例：单次检索 ≈ **0.03755 元**（Query 向量化 0.00005 + Rerank 0.0375）；一个应用**挂 4 个知识库 → 0.1502 元/次**（线性放大）。
- 量级测算（44,000 轮/月、默认 50+50、500 token/切片）：**Rerank 月费 ≈ 1,100 元**，而规格费仅 **144 元** → **TCO 主体是 Rerank token，而不是规格费、也不是生成模型**。
- **降本三杠杆**：① 调低初步召回 TopK（50+50 → 20+20 可近似线性降本）；② 非必要场景关 Rerank；③ 避免一个应用挂多个知识库（挂 N 个 ≈ N 倍检索费）。

**⑤ 文档与配额限制**：
- 单文件：pdf/docx/doc/wps/pptx/ppt **≤150 MB 且页数 ≤1000**；txt/markdown/html **≤10 MB**；xlsx/xls **≤10 MB 且 10 万行内**；图片 **≤20 MB**；音视频 **≤512 MB**。
- 每业务空间：文件数 **10 万**、类目 **500**（可工单扩）、数据表 **1,000**。
- 导入：控制台单次 **50 个文件**；API 批量不受限但**建议 ≤500**；**导入文件仅支持查看最近 90 天内的**。
- 平台存储**限时免费**提供 **20 万文件 / 1 TB**。

**⑥ 检索能力与参数边界**：
- 单次返回分片上限 **20**（`RerankTopN` 取值 [1-20]，**默认 5**），单分片 **≤6000 token**；`DenseSimilarityTopK + SparseSimilarityTopK` 之和 **≤200**。
- 支持：混合检索（`qwen3-rerank(hybrid)` 含 BM25 得分）、多路召回 + 权重（**权重仅在同类型知识库之间生效**）、知识库路由（由 **qwen-plus** 判定）、`SearchFilters` 元数据过滤。
- `SearchFilters` 语义：**子分组之间强制 AND、不可改**；`tags` 数组内为 OR。⚠️ **知识库创建后无法再配置 metadata 抽取**；**排序模型模式（qa / similar / custom）创建后不可改**。
- ⚠️ **知识库内 embedding 维度被平台固定**为 **512**（text-embedding-v4 / v3）或 **1024**（multimodal-v1），**不可更改**——即"v4 支持 64–2048 维可选"这条在知识库场景内不成立。

**⑦ 🔴 权限红线（企业内部知识库场景的首要风险）**：
- 百炼知识库的隔离粒度只到 **RAM 子账号 + 业务空间成员**，属于**运维管理权限**，**不是终端用户的文档可见性**。
- `SearchFilters` 由**调用方在请求体传入、服务端不校验调用者身份** → **不能当安全边界**。
- 落地必须：① 自研 **BFF 服务端强制注入**过滤条件（客户端永不可传）；② 强隔离场景按**部门/密级拆独立 IndexId**。

**⑧ 地域与私网**：
- 知识库**仅华北 2（北京）**；新加坡仅 **2025-04-21 前存量用户**有预览权限。
- PrivateLink 只有一个终端节点服务 **`com.aliyuncs.dashscope`**（覆盖模型 API / 应用 API）；**知识库与数据管理 API（`bailian.cn-beijing.aliyuncs.com`）能否走私网，官方文档未覆盖，需工单确认**[需登录复验/需工单]。

**⑨ 数据条款（SA 必须主动披露的双句）**：
- 官方明文"**绝不会将您的数据用于模型训练**" + AES-256 传输加密 + SOC 2 审计。
- 但**同一页另有**"根据相关法律法规要求，阿里云百炼将存储模型与应用调用时产生的数据"——**SA 应主动披露后一句**，不要只念前一句。

**⑩ 退出成本（Exit Cost）**：
- **不支持一键导出**，需自研调 `ListChunks` 批量拉取。
- 欠费 **15 天**后数据永久删除；**自购 ADB-PG 作向量存储时为 8 天**。

**⑪ API（自研应用可直连）**：
- 独立 Retrieve API：`POST /{WorkspaceId}/index/retrieve`，endpoint **`bailian.cn-beijing.aliyuncs.com`**，版本 **2023-12-29**；**仅适用于文档搜索类知识库**。
- RAM 用户需授权 **`AliyunBailianDataFullAccess`**。

**⑫ 🔴 生命周期红线（报价/选型前必查）**：
- **旧版「企业知识库」模块 2027-01-16 下线**（公告 `aliyun.com/notice/118448`），相关 API 将无法调用 → 必须迁到新版「知识库」模块。
- 知识库 **2026-01-04 已开启商业化收费**（公告 117726）。
- **`gte-rerank` 已于 2026-05-30 下线**（公告 118217），替代为 **`qwen3-rerank`**；注意 **`gte-rerank-v2` 仍在售**（0.8 元/百万 token），两者不要混淆。

**⑬ Embedding / Rerank 单价**（元/百万 token，北京，2026-08-08）：

| 模型 | 单价 | 备注 |
| --- | --- | --- |
| qwen3.7-text-embedding | **0.5** | 2560–256 维可选，单批 128K token，**当前最强文本向量** |
| text-embedding-v4 | 0.5（**Batch 0.25**）| 2048–64 维，单批 33K token |
| text-embedding-v3 | 0.5 | 存量索引兼容 |
| qwen3-vl-embedding | 文本 **0.7** / 图片视频 **1.8** | 多模态 |
| qwen3-rerank | **0.5** | gte-rerank 的替代（后者已下线）|
| qwen3-vl-rerank | 文本 **0.7** / 图片 **1.8** | 多模态排序 |
| gte-rerank-v2 | **0.8** | 仍在售；ADB-PG 内置 RAG Service 也用它 |

- 北京地域各模型均有 **100 万 token / 90 天**免费额度。

**⚠️ 报价前必读**：知识库规格费 + Rerank 计量基数两项已写入 [../references/pricing-verification-checklist.md § 3.1 / § 3.2 / C14](../references/pricing-verification-checklist.md)。

**官方文档**：https://help.aliyun.com/zh/model-studio/ （Token Plan：.../token-plan-overview；知识库计费：.../billing-for-knowledge-base）
**证据等级**：[官方]；其中“增速限流 / 突发限流机制”条目为 [内部]（内部文档，非公开可验证）；“SA 提示”为 [推断]；知识库（RAG）章节为 [官方]（4 组 subagent 实时核验 + 独立事实核查复核），其中标 [需登录复验/需工单] 的字段未获官方文档覆盖
**最近更新**：2026-08-08（**新增「知识库（RAG）完整规格与计费」章节**：两档规格/免费额度 720 小时/资源包价目/Rerank 按初步召回总切片计费的报价避坑/文档与检索限制/权限红线/仅北京/数据条款双句/退出成本/Retrieve API/企业知识库 2027-01-16 下线 + gte-rerank 已下线/Embedding·Rerank 单价表）；2026-08-06（Token Plan 章节增量刷新：Credits 抵扣公式 + 按量付费/节省计划三方关系 + 完整版模型 + 订阅月计费周期）；2026-08-05（新增 Token Plan 订阅服务章节）；2026-07-16（新增增速/突发限流机制）；2026-06-28（Qwen3.7 + DeepSeek v4 定价刷新）

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
**报价量级**：DSW A10 实例 ≈ 13 元/时；DLC 按 GPU 时长计费；EAS 按实例规格（逐规格包月价见下方 EAS 独享章节）
**EAS 服务调用形态**[官方][2026-08-24]：部署后默认提供**共享网关 HTTP 调用**（公网/VPC 内网地址与 Token 在控制台「服务详情 → 调用信息」查看），请求头携带 Authorization Token（公网与内网调用均强制）；协议支持 HTTP/JSON（默认）与 gRPC（性能敏感/流式，部署时手动开启）；进阶接入可选专属网关 / VPC 高速直连 / NLB 负载均衡 / Nacos 服务发现。注意：走共享网关、专属网关时安全组不生效；走 NLB/Nacos/VPC 直连受安全组限制。文档：[调用方式总览](https://help.aliyun.com/zh/pai/methods-for-calling-services/) / [共享网关公网或内网调用](https://help.aliyun.com/zh/pai/call-via-shared-gateway-public-network-intranet) / [VPC 高速直连](https://help.aliyun.com/zh/pai/call-a-service-over-the-vpc-direct-connection-channel)
**避坑**：训练任务 Checkpoint 频率设置（OOM 或断点恢复）；EAS 冷启动优化需预热

---

#### EAS 独享 GPU 报价与私有化部署路线约束[官方][2026-08-08]

> 来源：`https://www.aliyun.com/page-source/price/detail/machinelearning_price`（**可匿名取的官方定价页数据源**，含 EAS 独享逐规格包月价，**仅华东 2 上海**）+ help.aliyun.com/zh/pai 部署文档 + ACS GPU 计费页 + 百炼专属版/AI Stack 官方页。价格标注日期 **2026-08-08**。

**① EAS 独享包月价（元/月，华东 2 上海）**：

| 实例规格 | 配置 | 包月价 |
| --- | --- | --- |
| `ml.gu7i.c8m30.1-gu30` | 8C30G + 1×GU30（24 GB 显存）| **3,661** |
| `ml.gu7i.c16m60.1-gu30` | 16C60G + 1×GU30 | **3,876** |
| `ml.gu7i.c32m188.1-gu30` | 32C188G + 1×GU30 | **4,307** |
| `ecs.gn7i-c8g1.2xlarge` | 1×A10（24 GB）| **5,033** |
| `ecs.gn7i-c32g1.8xlarge` | 1×A10，32C | **7,027** |
| `ecs.gn6i-c4g1.xlarge` | 1×T4（16 GB）| **3,683** |
| `ecs.gn7e-c16g1.4xlarge` | 16C125G + 80 GB 显存 | **18,344** |
| `ecs.c7.4xlarge` | CPU 16C32G | **1,722** |
| `ecs.c7.8xlarge` | CPU 32C64G | **3,444** |
| `ecs.g7.4xlarge` | CPU 16C64G | **2,210** |

- 同族 **2 / 4 / 8 卡线性倍增**。**GU30 = 24 GB 显存，性能对标 A10**。
- ⚠️ **GU60(48G) / GU120(96G) / L20 无公开价，需登录复验**[需登录复验]。
- ⚠️ **阿里云 8 代对应 L20（`gn8is`）而非 L40S；L40S 在阿里云不存在**——对客材料不要写 L40S。

**② 购买路径与计费起点**：
- commodityCode：包月 **`learn_EasDedicatedPrepay_public_cn`** / 按量 **`learn_EasDedicatedPostpay_public_cn`**（匿名访问均 302 到登录页）。
- **机器实例创建成功即计费**（哪怕未部署任何服务）；包月**自购买次日 00:00 起算**；系统盘免费 200 GiB。
- **节省计划仅抵扣 EAS 公共资源组按量，独享 / 专属资源组不适用**。

**③ 两条硬约束**：
- ⚠️ **EAS Serverless 官方明文「目前仅 SDWebUI 支持部署 Serverless 服务」**（2026-07-28 版文档仍如此）→ **通用 LLM 走不通**。
- ✅ **EAS 独享资源组支持 GPU 切分**：`gpu_memory` 与 `gpu_core_percentage` 是"**且**"关系；`gpu:1` 表示**独占整卡并忽略切分字段**。可让 LLM + embedding + rerank **共用一张卡**，边际成本接近零。官方适用范围写"仅使用 EAS 资源组或资源配额"→ [推断] 公共资源组不支持切分。

**④ Qwen3 官方部署最低配置**：

| 模型 | 最低显存 |
| --- | --- |
| 0.6B / 1.7B / 4B / 8B | 1 卡 A10 或 GU30（24 GB）|
| 8B 开 RoPE 缩放到 131072 | 48 GB |
| 14B | 1 卡 GU60（48 GB）|
| **32B 与 30B-A3B** | **1 卡 GU120（96 GB）** |
| 235B-A22B | 8 × 96 GB |
| 235B-A22B-FP8 | 4 × 96 GB |

- 官方原句：**FP8 里只有 235B 的算力需求比原模型减少，其他 FP8 与非 FP8 无区别**。
- 推理引擎可选 **SGLang / vLLM / BladeLLM**；Model Gallery 已接入 **Qwen3 全部 22 个模型**一键部署/微调/评测；embedding 可选 **bge-m3**（vLLM 或 FlagEmbedding 部署）；**rerank 是否可一键部署未查到，需控制台确认**[需登录复验]。

**⑤ 开源模型最小显存锚点**（来自 Hologres 内置 AI 模型规格表，可作 EAS 选型参照，比 PAI 表更保守，适合保守报价）：
- Qwen3-Embedding-0.6B **8 GB** / 4B **32 GB** / 8B **48 GB**；bge-large-zh-v1.5 **16 GB**；bge-base-zh-v1.5 **12 GB**；bge-small-zh-v1.5 **8 GB**；gte-sentence-embedding-chinese-large **16 GB**。
- Qwen3-8B **32 GB** / 14B **48 GB** / 32B **96 GB**。
- bge-reranker-v2-m3 参数 **568M**、F32 权重 **2.27 GB**，fp16 约 **8 GB 卡足够**，可切分共卡。
- ⚠️ **`gte-rerank` 无开源权重**，只有百炼 API 版 `gte-rerank-v2`——客户要"私有化 rerank"必须换 bge-reranker 系列或 qwen3-rerank 的开源对应物。

**⑥ ACS GPU 按量单价**（元/卡·小时，default / best-effort）：

| 卡型 | default | best-effort |
| --- | --- | --- |
| T4 | 6.20 | 2.48 |
| A10 | 6.90 | 2.76 |
| G49E（48G）| 14.96 | 5.98 |
| G59（32G）| 14.28 | 5.71 |
| P16EN（96G）| 14.82 | 5.93 |
| L20N（48G）| 43.68 | 17.47 |
| L20NE（72G）| 48.84 | 19.54 |

- 配套 vCPU **0.06 元/核·h**、内存 **0.03 元/GiB·h**；**ACS 不收集群管理费**；创建/启动失败的 Pod 不收费。
- **best-effort ≈ default 的 40%，但可被驱逐**——不适合承载常驻问答链路的唯一副本。

**⑦ 🔴 国内高端 GPU 的硬约束**：
- **`gn8v` / `gn8v-tee`**（单卡 96 GB HBM3、带宽 4 TB/s、NVLINK 900 GB/s、单 GPU 39.5 TFLOPS FP32）官方明文"**目前仅支持海外等部分地域，如有需求请联系阿里云销售人员**"。
- ⚠️ 官方文档**从不使用 "H20" 型号名**，对客材料应沿用官方措辞（`gn8v`）。

**⑧ 成本结论**[推断]：
- 常驻 7×24 场景，**PAI-EAS 独享包月在同卡型上最便宜**：GU30 **3,661** vs ACS A10 ≈ **6,350** vs ECS ≈ **6,400**。
- **ACS 只在"白天开夜里关"或突发扩容时更省**；**ACK 自建只在已有 GPU 存量或需极端定制推理引擎时才有理由**。
- 300 人企业 / 日活 100 人 × 20 轮场景：峰值并发不到 2、单卡利用率 <5% → **私有化比调 API 贵一到两个数量级**。
- **结论：私有化的决策依据是合规与数据主权，不是成本**——这是对客最重要的一句定调。

**⑨ 离线交付形态（Sales-led，无自助入口）**：
- **百炼专属版 AI Stack 一体机**：内置 DeepSeek R1/V3 满血版 + Qwen 72B/14B/7B + QwenVL + 文档解析模型 + RAG 排序模型 + 四合一 RAG 应用；自研推理引擎 **OpenTrek-LLM**。⚠️ 官方页"单机 16 卡全精度 16/8/4bit 支持高并发满血版 DeepSeek"是**性能描述而非最低起配**，**起配未公开**。
- **AI Stack**（平头哥 APG 服务器）：**真武 M890** 8 卡 / 单卡 144 GB / 片间 800 GB/s / 机间 3.2 Tbps / 支持 FP8·FP4；**真武 810E** 16 卡 / 96 GB 每卡 / 总显存 1.5 TB+ / 机间 1.6 Tbps；含 AI 网关；单机版可作边缘站点接入飞天企业版。案例：国家电网安徽电力。
- 两者均**无公开价目表、无控制台自助开通、纯 Sales-led 项目制**。
- 🔴 **禁止对客户承诺"完全离线 / air-gapped"**：公开材料只写"本地化私有部署 / 数据无需上传云端"，**没有 air-gapped 技术承诺文字**；且百炼专属版含"联网搜索"功能，预设外网可达。

**⑩ 🔴🔴 灵骏智算服务（Lingjun）GPU 卡型 × 实例规格全表**[内部][2026-08-10]（来源：内部语雀 paidoc《PAI 灵骏智算服务规格》，全表已归档 [../raw/misc/misc-2026-08-10-pai-lingjun-gpu-specs.md](../raw/misc/misc-2026-08-10-pai-lingjun-gpu-specs.md)，SHA256 `ea88e28d…5545`）

> 🔴 **本节为 Alibaba Internal，严禁对客**。含内部按月目录价、内部代号 ↔ NVIDIA 芯片映射、`ncp` 渠道标注、机密计算 SKU、受管制加速卡分地域可售状态。
> **对客口径**：只讲官方对客实例规格名 + 官网价；**不得**出现 L20x 解码、目录价、ncp。与第 ⑦ 条呼应——ECS 侧官方从不写 "H20" 只写 `gn8v`，灵骏侧内部表才写 H20/H20-3e，两套命名不可混用。

**规格命名解码**[推断]（由全表 143 行规律反推，非官方定义）：`ml.g{供给线}{代次}{型号字母}f.{卡数}.{CPU 规格}`

- 供给线：**`gu`** = NVIDIA 直采线（型号名直写 A800/A100/H800/H100/H20/H200）｜**`gx`** = NVIDIA **ncp（Nvidia consuming partner）渠道线**（型号用内部代号 L20x）｜**`gp`** = 平头哥 PPU 线｜**`ga`** = AMD 线
- 代次：`7` = Ampere 代（A100/A800/PPU810）｜`8` = Hopper 代（H800/H100/H20/H200/L20X-Z）｜`9` = 新一代机架级（L20A/B/C/D、PPU1.5）
- 后缀：**`.cc`** = 机密计算版（如 `ml.gu8tef.8.46xlarge.cc`）｜`.ch` = 适配中｜`-ha4`/`-gu108`/`-gu100` = 硬件批次/配置变体

**卡型 ↔ 内部代号映射**（文档明确标注的部分，[内部]）：

| 内部代号 | 实际芯片 | 显存 | 出现规格族 |
| --- | --- | --- | --- |
| **L20Y** | **H800** | 80 GB | `gx8xf` / `gx8xbf` |
| **L20Z** | **H100** | 80 GB | `gx8ef` / `gx8ecf` |
| **L20X** | **H200** | 141 GB | `gx8sf` / `gx8sef` / `gx8sdf` |
| L20C | 文档未标注 | 192 GB | `gx9cf` / `gx9cxf` |
| L20D | 文档未标注 | 288 GB | `gx9df` / `gx9dxf` / `gx9dwf` / `gx9dqf` / `gx9def` / `gx9dzf` |
| L20A | 文档未标注 | 192 GB | `gx9axf` / `gx9af`（**72 卡机架**）|
| L20B | 文档未标注 | 288 GB | `gx9bxf`（**72 卡机架**）|

- ⚠️ L20A/B/C/D **文档未给出芯片对应**。按显存与 72 卡机架形态**推测**为 GB200（192 GB）/ GB300（288 GB）NVL72 系列[推断]——**未经确认，禁止在任何对内外材料中引用**。

**主力卡型报价速查**（国内站按月目录价，8 卡整机除非另注；按量单价为元/分钟）：

| 卡型 | 显存 | 代表规格 | CPU/Mem | 主力地域与目录价 | 按量 |
| --- | --- | --- | --- | --- | --- |
| A800 | 80 GB | `ml.gu7xf.8xlarge-gu108` | 96C/1600G | 乌兰察布 **¥151,725** | 5.2682 |
| A100 | 80 GB | `ml.gu7ef.8xlarge-gu100` | 96C/1600G | 乌兰察布 **¥168,584** | 5.8536 |
| **H20** | 96 GB | `ml.gu8tf.8.40/46xlarge` | 160-184C/1800G | 乌兰察布 **¥186,247**；京/沪/杭 ¥198,994；新加坡 ¥264,933 | 6.47-9.20 |
| **H20-3e** | 141 GB | `ml.gu8tef.8.46xlarge` | 184C/1800G | 乌兰察布 **¥214,184**；京/沪/深 ¥228,842；港 ¥308,937；马来 ¥313,514；新 ¥331,821；法兰克福 ¥343,264；迪拜 ¥411,917 | 7.44-14.30 |
| H20-3e 机密版 | 141 GB | `ml.gu8tef.8.46xlarge.cc` | 184C/1800G | 北京 **¥276,805**（+21% vs 普通版）| 无按量 |
| **H800** | 80 GB | `gu8xf`(NIC) / `gx8xf`(DPU) | 160-216C/1800G | 乌兰察布 **¥448,771**；上海 ¥480,185(ncp)；深圳 ¥515,116 | 13.78-17.89 |
| **H100** | 80 GB | `gu8ef` / `gx8ef`(L20Z) | 160-216C/1800G | 上海 **¥456,930**（最低）；新加坡 ¥591,302；`-ha4` 新加坡 ¥706,440 | 15.87-20.53 |
| **H200** | 141 GB | `gx8sf` / `gx8sef`(L20X) | 160-192C/1800G | 京/沪/杭/深 **¥502,623**；新加坡 ¥650,432；亚特兰大(`gu8sf`) ¥650,432 | 17.45-22.58 |
| L20C | 192 GB | `gx9cf.8.62/70xlarge` | 248-280C/2744G | 乌兰察布/北京 **¥854,459** | 29.67 |
| L20D | 288 GB | `gx9df.8.62xlarge` 等 6 变体 | 248C/3684G | 沪/京/中卫/乌兰察布 **¥1,008,260**；日本 ¥1,058,200；马来 ¥1,149,416 | 35.01-39.91 |
| **L20A（72 卡）** | 192 GB | `ml.gx9axf.72.612xlarge` | 2448C/15300G | 新加坡 / 泰国 **¥11,660,000** | 404.86 |
| **L20B（72 卡）** | 288 GB | `ml.gx9bxf.72.612xlarge` | 2448C/15300G | 马来西亚（柔佛州）**¥14,575,000** | 506.08 |
| PPU810E（16 卡）| 96 GB | `ml.gp7vf.16.40/46xlarge` | 176-184C/1800G | 京/沪/杭 **¥184,215**；乌兰察布 ¥184,829；**上海金融云 ¥280,007**（+52%）| 6.40-12.15 |
| PPU810（8 卡）| 96 GB | `ml.gp7ef.8.40xlarge` | 160C/1800G | 乌兰察布 **¥283,245** | 9.83 |
| Mi308X（AMD）| 192 GB | `ml.ga8xf.8.46xlarge` | 184C/1800G | 杭州/广州 **¥189,518** | 6.58 |
| PPU1.5（64 卡）| 144 GB | `ml.gp9af.64.496xlarge.ch` | 1984C/16680G | 乌兰察布 **¥2,420,000**（状态：**适配中**）| 84.03 |

**地域与可售性要点**：

- **国内可售的最高端 NVIDIA 卡是 H200（141 GB，¥502,623）与 L20C/L20D**；**H100/H800 国内仅上海/深圳/乌兰察布有**，H100 主力在新加坡。
- **72 卡机架级（L20A/L20B）仅海外**：新加坡、泰国、马来西亚柔佛州——**国内无**。
- **H20/H20-3e 覆盖最广**（乌兰察布/京/沪/杭/深/港/新/马/法兰克福/迪拜），是**出海 + 国内双可用**的性价比主力。
- **上海金融云溢价显著**：同 PPU810E 规格比通用地域贵 **52%**（¥280,007 vs ¥184,215）——金融客户报价必须单独取数。
- 海外同卡型普遍贵 30-60%（如 H20-3e 迪拜比乌兰察布贵 **92%**），**出海方案的算力成本不能套用国内价**。
- 表内另有 `适配中` sheet（H200 `gx8sf` 系列新加坡/上海"导入中"），**状态非"可售卖"的规格不得进入 BOM**。

**SA 使用红线**[推断]：

- ① 这是**内部目录价（List）**，不是成交价，也**不是官网对客价**——对客报价须走官方渠道价 + 折扣审批，本表只用于**判断量级、比地域、比卡型**。
- ② **卡型选型顺序建议**：能用 H20-3e（141 GB）就不上 H200——显存同为 141 GB 而目录价仅 **¥228,842 vs ¥502,623（省 54%）**，差异在算力与互联带宽，**推理场景优先 H20-3e，训练/长上下文预填充才需要 H200 及以上**。
- ③ 国产/AMD 替代已具备可售规格：**Mi308X（192 GB，¥189,518）显存最大而价格接近 H20 档**，PPU810E 16 卡 ¥184,215——**信创/供应链备份场景的现实选项**。
- ④ 与 EAS 独享（第 ⑧ 条）的分野：**灵骏 = 整机/集群级裸算力（8 卡起，月级 15 万起）**，EAS 独享 = 单卡粒度托管推理。**客户 <8 卡需求不要报灵骏**。
- ⑤ **PaaS 溢价只有 10%**：与灵骏裸金属（IaaS 形态）逐地域逐卡型对账，**本表 `ml.*` 月价 = 裸金属同卡同地域月单价 × 1.10**，在 20+ 组合上精确成立（例外：PPU810E 两侧同价、新加坡 H100、`ncp` 标注行）。客户纠结"自己运维裸金属 vs 用 PAI 托管"时，**10% 是很有说服力的数字**，比多数人预期低。详见 [aliyun-lingjun-bms.md § 2](aliyun-lingjun-bms.md)。
- ⑥ **按量 ≈ 包月 × 1.52**（按 730h/月折算）：A800/H800/L20C/L20D/L20A 五组实测 `元/分钟 × 43,800 ÷ 月价` 稳定在 **1.5208±0.0006**，不是常见的 2–3 倍。**短周期 POC 走按量的经济性比直觉好得多**，可主动提。[推断]

**⑪ 灵骏两套体系的关系（2026-08-11 新增）**：智能计算灵骏有**两个独立商品、两套命名、两套价格**——本条 ⑩ 是 **PAI 灵骏（PaaS，`ml.*` 命名）**；**灵骏裸金属（IaaS，`bccluster_eflocomputing_public_cn`，模块值 `efg1/efg2/efg3.*`）** 的商品 code、分地域列表价（含六档固费分期折扣阶梯）、逐机型硬件规格与 RDMA 网络世代、加白标签体系、2026-04-18 调价清单、开通与退订实操流程，全部沉淀在专题页 **[aliyun-lingjun-bms.md](aliyun-lingjun-bms.md)**（来源：钉钉《灵骏产品规格code》+《灵骏裸金属实例开通及退订方法》）。

> **勘误（与上文"地域与可售性要点"配套读）**：**上海金融云溢价有两套口径**——PAI 侧 `ml.*` 是 **+52%**（¥280,007 vs ¥184,215），**灵骏裸金属侧是 +90%**（¥350,009 vs ¥184,215），北京政务云裸金属侧为**精确 ×2.00**（¥368,430）。两套不能混用，报行业云必须先确认客户买的是 PAI 还是裸金属。
> **勘误**：下文"证据等级"里的 **L20A/L20B 芯片推测（GB200/GB300）至今无任何官方证据**，2026-08-11 的裸金属表也未给出映射，**禁止对内对外引用该猜测**；可确证的只有 `.ch72`=72 卡机架、`efg3.*`=机架级商品、仅海外在售、L20B 显存 288GB > L20A 192GB。

**⚠️ 报价前必读**：EAS 独享 / Serverless / GU60·GU120 无公开价三项已写入 [../references/pricing-verification-checklist.md § 3.1 / § 3.2](../references/pricing-verification-checklist.md)。灵骏 `ml.*` 规格**无 common-buy 自助购买页**，属集群级 Sales-led 交付，报价须走内部取价流程。

**官方文档**：https://help.aliyun.com/zh/pai/ ；定价数据源 https://www.aliyun.com/page-source/price/detail/machinelearning_price
**证据等级**：[官方]（EAS 逐规格包月价 / Qwen3 部署配置 / ACS 单价 / gn8v 地域约束 / 一体机形态）+ [内部]（第 ⑩ 条灵骏卡型/目录价/代号映射，来源内部语雀 paidoc，**严禁对客**）+ [推断]（成本结论、公共资源组不支持 GPU 切分、灵骏命名规律解码、L20A/B/C/D 芯片推测、SA 使用红线）+ [需登录复验]（GU60/GU120/L20 价格、rerank 一键部署）
**最近更新**：2026-08-11（**第 ⑩ 条新增 SA 红线 ⑤⑥**：PAI/裸金属 ×1.10 溢价定律、按量≈包月×1.52；**新增第 ⑪ 条**指向灵骏裸金属专题页 [aliyun-lingjun-bms.md](aliyun-lingjun-bms.md)；**两处勘误**：上海金融云溢价 PAI +52% vs 裸金属 +90%、L20A/L20B 芯片推测禁止引用）；2026-08-10（**新增第 ⑩ 条灵骏智算 GPU 卡型 × 实例规格全表**：命名解码 / L20Y-Z-X↔H800-H100-H200 映射 / 17 个卡型族目录价与按量价 / 地域可售性 / 4 条 SA 红线）；2026-08-08（新增 EAS 独享 GPU 报价与私有化部署路线约束章节）；2026-06-17

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

### Meoo（秒悟）— 云端 AI Vibe Coding 全栈应用工厂

**官方定位**：一款云端 AI 开发工具，自称"会编程、懂设计、自部署的全能 AI 伙伴"。以自然语言驱动，一句话生成前端 UI + 后端逻辑 + 数据库 + 部署上线的**完整可运行全栈应用**（网页/H5/微信小程序）。运营主体为**通义云启（杭州）信息技术有限公司**，团队版通过阿里云主账号开通、成员用 RAM 子账号登录，与 [[百炼]] / [[Qoder CN]] 同属阿里云 AI 应用矩阵，但定位面向"业务/非工程师"的 Vibe Coding 端到端交付，与 Qoder（面向开发者的 IDE Agent）互补而非替代。

**产品形态**：
- **网页端**（meoo.com）：主用户界面，聊天式生成 + 可视化预览 + 一键发布
- **Meoo CLI**（`npm i -g @aliyun-meoo/cli`）：让 Claude Code / Codex / Cursor / Qoder / QoderWork / Cline 等**外部本地 Agent** 接管 Meoo 云端资源（数据库/登录/存储/百炼模型/部署），主打"本地 Agent 写代码 + Meoo 接管后端"的联合工作流。优先支持 Vite + React 与纯前端项目，需 Node 20+
- **小程序模式**：Meoo 作为微信第三方服务商代开发/代上传/代提审微信小程序，账号仍归主体所有；支持 H5 快速预览 + 微信真机预览双通道

**四种 Agent 工作模式**（首页可切换，2026-06-08 上线记忆功能会自动记住上次选择）：
- **Agent - 复杂任务**：深度推理，长周期任务闭环（"规划→执行→反思"）
- **Swarms - 蜂群模式**：并发多 Agent 极速交付，简单/明确任务或 Token 预算有限时用（Free 2 次 / Pro 10 次 / Max 不限）
- **Plan - 规划模式**：先出 PRD/需求文档，用户确认后再全自动执行，避免黑盒返工
- **Design - 设计模式**（2026-05-25 DesignMode）：先生成多套视觉方案供选择，风格调整不消耗积分，含 BrowserUse 自动化 + Meoo 助理 Agent 全局记忆

**核心能力**：
- **一句话全栈生成**：前端（Web/H5）+ 后端逻辑 + 数据库 schema + 数据写入
- **原生云服务后端**（open on demand）：Supabase-like 一站式 BaaS，含**独立数据库、文件存储（单文件上限 50MB）、用户注册登录（GoTrue，支持手机号/邮箱/微信小程序）、实时消息、密钥管理、Edge Functions**；单行数据 1MB 上限，大文件走文件桶存 URL
- **AI 服务开箱即用**：应用需要 AI 时自动开通 Service AK，写入 `MEOO_PROJECT_API_KEY` 环境变量，Edge Function 服务端调用（不暴露给前端），端点为 `api.meoo.host/meoo-ai/compatible-mode/v1/*`（OpenAI 兼容）
- **技能 Skills**：Prompt 之上的模块化能力封装，可在应用/对话中复用；官方**技能市场**（meoo.com/skills）支持搜索、下载、上传 zip 技能包、AI 语义搜索意图；团队版有专属**团队技能市场**
- **版本管理**：版本历史/回滚/多版本代码对比
- **多人实时协作**：同一项目多人编辑，含权限
- **可视化修改**（2026-07-02 上线）：预览页手动微调，点选元素替换文本/图片，无需重新生成
- **代码下载导出**（Pro/Max）+ **前端项目导入**（2026-06-22，支持 React/Vue+Vite/Webpack/纯 HTML/微信小程序，ZIP ≤100MB）
- **微信小程序全链路**：代注册 = 不支持，代开发/代上传/代提审 = 支持
- **自定义域名**：Max 独享独立域名 + 免费 SSL 证书 + 免费续期；团队版赠 5 个 ICP 备案码 + 10 个三级子域名；备案仍需去 beian.aliyun.com 走阿里云
- **发布权限管控**（2026-06-09）：互联网公开 / 指定人访问（按秒悟昵称）/ 仅自己访问三档
- **Night Plan 错峰折扣**（2026-06-29 起，仅 Pro/Max，网页端）：**每日 22:00-次日 08:00（UTC+8），Qwen3.7-Max 2 折 / Qwen3.7-Plus 4 折**

**内置支持模型清单**（2026-07 现价，按 1K tokens 积分）：
| 模型 | 定位 | 输入积分 | 输出积分 | 缓存命中 |
|------|------|---------|---------|---------|
| **qwen3.7-max**（限时五折） | 旗舰智能体/长程自主 | 6 | 18 | 0.6 |
| **qwen3.7-plus**（限时八折） | 多模态视觉→代码 | 1.6 | 6.4 | 0.16 |
| **qwen3.6-plus / plus-Preview** | 中国最强编程/多模态 | 2 | 12 | 0.2 |
| **kimi-k2.5** | 200K+ 超长上下文 | 4 | 21 | 0.8 |
| **GLM-5.2** | 1M 无损上下文/项目级 | 8 | 28 | 2 |
| **GLM-5.1** | 8 小时长程闭环 | 6 | 24 | 0.6 |
| **GLM-5** | Function Calling/中文稳 | 4 | 18 | 0.8 |
| **MiniMax-M2.5** | 多模态/前端美感 | 2.1 | 8.4 | 0.21 |
| **deepseek-v3.2** | 代码推理 | 2 | 3 | 0.2 |
| **qwen3-vl-plus** | 视觉理解 | 1 | 10 | 0.1（缓存创建 1.25） |
| **qwen-image-2.0 / wan2.7-image** | 图像生成 | — | 200/张 | — |
| 手机短信验证码 | — | 35/条（20 条免费） | — | — |
| 邮箱验证码 | — | 2/条（20 条免费） | — | — |

**订阅套餐（个人）**：（限时价，标准价见下）
| 权益 | Free | Pro（¥89 → 限时 ¥39/月） | Max（¥199 → 限时 ¥89/月） |
|------|------|-------|--------|
| 每月积分 | 0（新人首月 1w） | 100,000 | 200,000 |
| 每日登录赠送 | 2,000（7 天有效） | 2,000 | 2,000 |
| 云服务数 | 1（限免） | 8 | 20 |
| 数据存储 | 5GB（限免） | 20GB | 100GB |
| 同时访问 | 100 | 200 | 600 |
| 蜂群次数 | 2（限免） | 10 | 不限 |
| 协作邀请 | — | 5 | 20 |
| 水印移除/代码导出 | — | ✓ | ✓ |
| 三级子域名 / 独立域名 | — | — | 5 个 / ✓ |
| beta 抢先体验 | — | — | ✓ |

**订阅套餐（团队版）**：**席位制 + 积分共享池**，只有一档
- **￥698/月 起**（含 5 席位）；追加席位 **￥60/席位·月，每席位赠 6.9w 积分**
- 连续包年 ￥8,376/年起（含 5 席位），追加席位 ￥720/席位·年
- 首购赠 5w 积分；含云服务 50 个 / 40GB / 同时访问 1000 人 / 每项目云函数 50 个上限
- 团队权益：管理员控制台（成员/额度/看板）、5 个 ICP 备案码、10 个三级子域名、发布代码备份、团队技能市场、应用仅团队可见
- 角色：Owner（全权）/ Admin（除计费管理外全权）/ Member（个人应用 + 用团队积分），支持邀请链接 + 有效期 + 席位到期立即阻断权限
- 席位规则：增席位立即生效；减席位下周期生效并按"最近登录时间"剥离；成员数超席位数会出现"冻结态"（数据保留可恢复）
- 变更规则：**单向升级不可降级**，Pro→Max 可、Max→Pro 不可；仅支持自动续费（默认到期前 1 天扣款），可后台"不续订"，5 天无理由退款

**能做的应用形态**：
- 产品落地页 / SaaS 原型 / H5 营销活动页 / CRM/OA/考勤/库存等内部管理系统 / 电商预订 / 社区团购 / 内容付费 / 抽奖答题投票 H5 / 个人企业官网 / AI 智能应用（剧本杀/客服）
- **形态限制**：仅面向**中国大陆**部署（服务器在国内，不支持香港/海外节点，海外用户访问速度不保证）；付费用户走**阿里云共享账单**（不用另买 ECS/RDS，除非要绑独立域名走 ICP 备案时需自购 ECS 拿备案码）

**不擅长 / 边界**：
- 复杂后端算法/大数据/流处理/微服务治理（→ 走 [[ACK]] / [[MaxCompute]] / [[MSE]]）
- 私有化部署（在阿里云上是全托管 SaaS，无输出私有部署形态）
- 海外/多地域应用（明确不支持）
- 需要接入用户自有阿里云资源（云服务仅限 Meoo 内置池）
- Safari 兼容差（推荐 Chrome 130+）；暂不支持个人版 RAM 子账号登录（团队版通过 RAM 子账号）

**典型选型场景**：
1. 业务/运营/PM 快速做 SaaS 原型或 H5 活动页
2. 中小企业无 IT 团队做官网/CRM/预订系统
3. 设计师把作品集变成可交互网站
4. 开发者用外部 Agent 做前端 + Meoo CLI 一键部署 + 云服务后端
5. 微信小程序快速搭建 + 代提审

**对位竞品**：
- 全球：Vercel v0 / Bolt.new / Lovable / Replit Agent / Cursor Composer
- 国内：字节 Trae / MiniMax 空间 / 百度秒哒
- 差异化卖点：**内置 Supabase-like 云服务后端 + 微信小程序全链路 + 阿里云生态（RAM/备案/万网）+ 中文场景 + 多模型选择器**

**避坑点**：
1. **本地 CLI 与网页端别双写**：网页后台默认空项目，你在本地 CLI 改完不同步上云就点"发布"会覆盖本地成果；改动必须先 `同步到 meoo 云端` 再动网页
2. **云服务开通有 3 分钟延迟**：命令返回成功≠数据库已 ready，等 2-3 分钟再连
3. **手机号/邮件验证码消耗积分**：超 20 条免费额度后按 35/2 积分扣，会被恶意刷号；上线前配好速率限制
4. **1MB 单行 / 50MB 单文件上限**：图片视频走文件桶存 URL，别塞进数据表
5. **单向套餐升级**：Max→Pro 不能降；退款仅 5 天无理由，积分增购不退
6. **境外访问不保证**：海外用户体验差；港澳台/新马泰等场景不适合选 Meoo
7. **可视化微调仅新建项目**：老项目不能升级启用；仅网页应用支持，小程序/App 不支持
8. **模型选择要看任务性质**：Kimi 长文本 / GLM-5 Function Calling / MiniMax 前端美感 / Qwen3.7-Max 复杂全栈 / Qwen3.7-Plus 视觉转代码

**监管与合规**：算法与模型均已备案。主要备案信息：通义千问 `ZheJiang-TongYiQianWen-20230901`、通义万相 `Shanghai-TongYiWanXiang-202410090024`、Moonshot `Beijing-MoonShot-20231016`、ChatGLM `Beijing-ChatGLM-20230821`、MiniMax `Shanghai-MiniMax-202505230046`、DeepSeek Chat `Beijing-DeepseekChat-202404280016`。用户协议签约主体：**通义云启（杭州）信息技术有限公司**；订阅版由通义云启 + 阿里云共同提供，云资源问题指向阿里云侧协议。

**报价量级速查（现价，2026-07）**：
- 个人：Free/Pro ¥39 限时（原 ¥89）/ Max ¥89 限时（原 ¥199）
- 团队版：起步 ¥698/月（5 席位起）+ 每追加席 ¥60/月
- 积分增购阶梯折扣：≥10w 积分 98 折 / ≥50w 95 折 / ≥100w 88 折
- 短信/邮件超额外挂：35 / 2 积分每条

**关键更新时间线**（摘 file-10）：
- 2026-07-03 沙箱手动重启 · 2026-07-02 预览页手动微调 · 2026-06-29 Night Plan 错峰折扣 · 2026-06-28 手机端浏览器访问 · 2026-06-22 前端项目导入 · 2026-06-18 GLM-5.2 上线 · 2026-06-10 Meoo CLI · 2026-06-09 手机/邮箱注册登录 + 中文自定义域名 + 应用访问权限管控 · 2026-06-05 小程序生成 · 2026-06-04 Qwen3.7-Plus · 2026-05-25 DesignMode + BrowserUse + Meoo 助理 Agent + 全局记忆 · 2026-05-22 Qwen3.7-Max · 2026-05-15 GLM-5.1 · 2026-04-29 Plan 模式 + 取消发布

**官方文档**：https://docs.meoo.com/ | 官网：https://meoo.com/ | 技能市场：https://meoo.com/skills
**联系邮箱**：meoo@service.aliyun.com
**证据等级**：[官方]（源自 docs.meoo.com/llms.txt 全部 34 页官方文档，SHA256 已归档 raw/aliyun-docs/meoo/）
**最近更新**：2026-07-07

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
**限流机制**：模型 API 的增速/突发限流在此网关层实施，机制与配额（TPM 配置、突发增速 30%、重试退避）详见百炼卡「增速限流 / 突发限流机制」章节
**官方文档**：https://help.aliyun.com/zh/dashscope/
**证据等级**：[官方]
**最近更新**：2026-07-16（补充限流机制交叉引用）

---

### 文档智能 DocMind（文档解析）

**官方定位**：文档结构化解析与理解服务——把 PDF/Word/PPT/图片/音视频转成带版面结构的机器可读结果，是 RAG 入库流水线的上游环节。
**能做**：版面分析、OCR、阅读顺序还原、表格/公式/文本样式检测、跨页合并、大模型（多模态）增强解析、音视频转写。
**不擅长**：向量化与检索（→ 百炼知识库 / 向量库）；业务语义抽取的深度定制（→ 自研 + VLM）。

**典型选型场景**：企业知识库入库前的文档解析、合同/报表/扫描件结构化、图表密集材料的多模态解析。

**计费（大模型版文档解析）**[官方][2026-08-08]：

| 计费项 | 单价 | 免费额度 |
| --- | --- | --- |
| 图文类型 **基础链路** | **0.02 元/页** | 每月赠 **3,000 页**（每月 1 号重置）|
| 图文类型 **增强链路** | **0.04 元/页** | 同上共用 |
| **视频**增强链路 | **0.002 元/秒** | 一次性赠 **100 小时** |
| **音频**增强链路 | **0.00035 元/秒** | 一次性赠 **100 小时** |

- 音视频**强制开增强链路**。
- **计量口径**：pdf / word / ppt 按**实际页数**；图片按**张**；excel / html / epub / mobi 按**中文每 2000 字符或英文每 2000 词折 1 页**。
- 扣费顺序：**免费额度 → 资源包（`docmind_general_dp_cn`）→ 按量**，**自然月阶梯计价**。

**两条链路的能力差异**：
- **基础链路**：版面分析 / OCR / 阅读顺序 / 表格·公式·文本样式检测 / 跨页合并。
- **增强链路**：由多模态大模型做版面与 OCR。⚠️ 官方只写 `EnhancementMode=VLM`，**未点名 Qwen-VL，勿在对客材料写具体模型名**。

**⚠️ 触发机制（直接决定解析费口径，最易算错的一处）**：
- 只设 `LlmEnhancement=true` 是**有条件触发**——仅 PPT 类 `layoutConf ≤ 0.8`、chart 图表块才走大模型。
- 要**全量多模态**必须显式设 **`EnhancementMode=VLM`**；复杂表格另需 **`OutputHtmlTable=true`**。
- 按错这个开关，报价会在"3,000 页免费额度内"与"全量 0.04 元/页"之间差出两个量级。

**SA 量级锚点**[推断]：10 万份文档 × 均 50 页 = **500 万页**，若全量走增强链路，一次性解析费 ≈ **20 万元**。缓解办法：**电子版走基础链路 + 只对扫描件与图表密集文档走增强链路 + 分批入库**。

**⚠️ 与百炼知识库的计费归属未明（必须工单书面确认）**：
- 百炼知识库内部使用解析时，官方计费文档**未列出任何独立解析计费项**（关键词"文档智能 / DocMind / 按页"出现 0 次），但**也没有明文承诺免费**。
- 且知识库提供"大模型文档解析 / Qwen VL 解析"选项，其 **Token 费用归属未说明** → **需工单书面确认**[需工单]。这一条在 10 万份文档级别的项目里是六位数量级的不确定性。

**官方文档**：https://help.aliyun.com/zh/document-mind/
**证据等级**：[官方]（单价 / 免费额度 / 计量口径 / 触发参数）+ [推断]（500 万页量级锚点）+ [需工单]（百炼知识库内解析计费归属）
**最近更新**：2026-08-08（首次建卡）

---

### 向量检索 / RAG 检索引擎选型（12 条产品线速查）[官方][2026-08-08]

> **建立背景**：一次企业内部知识库（员工侧 RAG）方案设计任务中，4 组 subagent 实时核验 help.aliyun.com 官方文档 + 官方公告 + 技术社区实践沉淀，经独立事实核查员复核。**本节的目的是让 SA 在 RAG 选型第一轮就排除采购走不通的产品**，而不是等报价被客户 IT 打回。
> 采购四字段（commodityCode / 最低起步 / 规格页可用性 / 采购流程兼容性）的权威来源仍是 [../references/pricing-verification-checklist.md § 3.1](../references/pricing-verification-checklist.md)；本节侧面补充**技术能力边界与适合规模**。

**① 一屏速查（在售状态 + 采购可行性 + 适合规模）**：

| 产品 | 在售状态 | 购买入口 / commodityCode | 规格页 | 最低起步 | 计费 | 报价量级 | 适合规模 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 百炼知识库（RAG）| ✅ 在售、在迭代 | 控制台开通，无 common-buy | ⚠️ 仅两档规格 | 标准版 1 知识库 | 按小时规格费 + 模型 Token | 21.6 元/月起（旗舰 144 元/RCU·月）| 零运维、快速上线，**TCO 主体是 Rerank** |
| **OpenSearch-LLM 智能问答版** | ⚠️ 在售但**功能迭代停滞**（新功能发布记录止于 2024-06-20）| `opensearch_pre` | ✅ 有 | 存储 **[1,100] GB 硬顶** | 标准版计算 CU **强制按量** | 标准版 2GB 包月 **223.82 元/月**；专业版 2GB+2×gpu.v100.32g.x4 **5,912.4 元/月**（上海）| ❌ **不建议向新客户主推** |
| **OpenSearch 向量检索版** | ✅ 在售 | 后付费 `opensearch_ha3post_public_cn`（预付费码未查到）| ✅ 有 | 单节点方案（1 数据节点 + 0 查询节点 + 1 分片）| 包月 + 按量 | 单节点最小可用 ≈ **895 元/月**；3 节点例 ≈ **3,324 元/月** | 中小规模、需全文 + 向量混合 |
| **DashVector** | ⚠️ 在售且在迭代（最新公告 2025-12-09）但**采购走不通** | `dashvector_vector_public_cn` | ❌ 无包月 | — | 🔴 官方明文"**当前仅支持按量付费**"、"**降配，暂不支持**" | P.small 起 **0.375 元/h**；S.small 起 **0.25 元/h**（≈180 元/月）| **第一轮就该排除** |
| **向量检索服务 Milvus 版** | ✅ 在售 | **无 common-buy 码**，走 `milvus.console.aliyun.com` 创建页 | ✅ 有 | 按 CU | 包月 + 按量，年付有优惠 | 服务/计算节点性能型 **157 元/CU·月**、容量型 **211 元/CU·月**（杭沪京深；乌兰察布 142/190）；官方示例标准版 24CU 服务 + 16CU 计算 = **7,144 元/月**；存储 0.00025 元/GB·h | **亿级向量** |
| **阿里云 Elasticsearch（集群版）** | ✅ 在售 | `elasticsearchpre`（包月）| ✅ 有，但**单价不披露** | 专有主节点**固定 3 个不可改**；节点数须为可用区整数倍 | 包月 + 弹性节点强制按量 | 🔴 **节点规格单价官方文档不披露**，明确"以购买页查看明细为准"→ **必须登录复验**；弹性节点北京 **0.42 元/ECU·h**（1 ECU ≈ 1核4G）| 百万~千万级，且需**文档/字段级权限** |
| **ES Serverless 版** | ✅ 在售 | `elasticsearch_serverless_spn_cn`（节省计划）| ❌ **无规格页**（只选应用类型）| — | ❌ 无包月，只有节省计划 | 🔴 **有最低门槛费**：检索增强型 8.17 约 **160.272 元/月**；日志分析型约 **4,351.32 元/月** | **POC 可用，转生产必须换集群版** |
| **Lindorm 向量引擎** | ✅ 在售 | `hitsdb_lindormnextpre_public_cn` | ✅ 有 | ⚠️ **必须同时开通**宽表引擎 ≥2.7.0 + 向量引擎 + 搜索引擎 ≥3.9.22.3 + 搜索索引；搜索节点**仅支持单可用区实例** | 包月 + 按量 | 宽表节点 4核16G **600 元/节点·月**、8核32G **1,248**；存储标准型 **0.7** / 容量型 **0.12** / 性能型 **2.0** 元/GB·月 | **单索引可到百亿向量** |
| **AnalyticDB PostgreSQL 向量** | ✅ 在售 | `GreenplumPre` / `GreenplumPost`（购买页有 `vector_optimizor` 开关）| ✅ 有 | 存储弹性高可用最低 **2C16G×4 节点**；高性能基础版 **2C8G×2 节点**；存储 **≥50 GB/节点**；Master ≤8 CU 免费 | 包月（1年8.5折/2年7折/3年5折）+ 按量 | 北京示例：基础版 2C8G×2 + 50GB×2 ESSD PL0 ≈ **815 元/月**；高可用 4C32G×4 + 100GB×4 ESSD PL1 ≈ **4,264 元/月**（单节点 382.50 / 865.99）| 百万~千万级 + 需 SQL 分析融合 |
| **Hologres 向量** | ✅ 在售 | `hologram_combo_public_cn` | ✅ 有 | 按 CU | 包月 + 按量；Serverless Computing / 计算组弹性资源 / 备份快照**均仅后付费** | 计算 **170 元/CU·月**（按量 0.3542 元/CU·h）、标准存储本地冗余 **1 元/GB·月** | 768 维参考容量：全内存约 **500 万向量/Worker**、混合索引约 **1 亿向量/Worker** |
| **Tablestore 多元索引 + 向量** | ✅ 在售 | `ots_standard_public_cn` | ⚠️ VCU 模式有规格 | 🔴 CU 模式官方明确"**无法控制整体资源使用上限**"（财务风控不通过）→ 必须用 **VCU 模式 + 预留 VCU** | 按量 / VCU 预留 | 1 VCU = 4核16GB，弹性步长 0.1 VCU | ⚠️ **每索引 ≤5 个向量字段、维度上限 4096、TopK ≤1000** |
| **RDS PostgreSQL + pgvector** | ✅ 在售（官方插件）| `rds` PG 页 | ✅ 有 | PG ≥14 且内核小版本 ≥20230430；**PG17 需 ≥20241030** | 包月 + 按量 | 见 RDS 卡 | **≤50 万向量小档首选**，完全在客户 VPC、可叠加 RLS |
| **Qdrant / Milvus 自建** | ✅ 社区版 | Qdrant 官方**计算巢部署模板** `ServiceId service-eeb5dfd73a414b6e849c`（`type=user` 资源建在客户账号内，需填自有 VPC/vSwitch）| — | ECS 规格自定 | 软件费 **0**，只付 ECS/云盘/带宽 | 仅 IaaS 成本 | 有自运维能力 + 极致成本敏感；**无厂商 SLA** |

**② 逐产品的关键约束与避坑**：

- **OpenSearch-LLM 智能问答版**：**每实例最高访问限流 10 QPS**；专业版 GPU **[1,10] 个不可降配**；存储硬顶 100 GB。**官方重心已转向「AI 搜索开放平台」(`opensearch_platform_public_cn`) 与向量检索版** → 新客户不要主推。
- **OpenSearch 向量检索版**：SSD 族含 **50 GB 免费存储、步长 50 GB**；单节点最小可用 ≈ 895 元/月（实例租用 248.48 + 数据节点云盘型 4核32G 646.81）。⚠️ **强制实例 VPC/vSwitch 与客户端 ECS 一致，否则 403**。
- **DashVector**：维度上限 **20000**（最高的一档）；但"仅按量 + 不支持降配"两条足以让企业采购流程走不通 → **第一轮排除**。
- **Milvus 版**：创建时**自动在所选 VPC 内建不可删除终端节点 `实例名-milvus-vpce`**，默认仅内网。🔴 **数据落盘的账号归属与存储介质官方文档未公开**——法务条款要求"数据存自有 VPC/账号内"时，**须工单确认后才能签**[需工单]。
- **阿里云 ES 集群版**：**FalconSeek 向量内核**（`knn_type` 支持 HNSW / RabitQGraph / QGraph / QC / Linear）；`tags_filter` **前置过滤在图遍历早期剪枝，比原生 filter 快**；支持 **document / field level security**（这是"权限下压到数据层"的关键差异化能力）。
  - 🔴 **OpenStore 存算分离六项硬约束**：① 内核增强版 **7.10 或 8.17**；② 最低 **2core8G**；③ **最少 4 个数据节点**；④ **单节点本地缓存 ≥50 GB**；⑤ 总逻辑共享存储 **≥160 GB**；⑥ **暂不支持三可用区**。另有**地域/可用区白名单**：杭州 J/K、北京 K/F/I、上海 E/G/L、深圳 C/D/E、香港 B/C/D、美东1 A/B。共享存储使用率 **95% 自动阻断写入**（可临时提到 98%）。
- **ES Serverless**：应用类型三选（检索通用型 7.10 / 检索增强型 8.17 向量增强 / 日志分析型）。**最低门槛费**会击穿"POC 省钱"叙事 → 已升级为核验项 **C13**。
- **Lindorm 向量**：维度上限 **32768**（HNSW / FLAT / IVFPQ）；SQL 内可 `MATCH...AGAINST` + `vector_distance` **融合检索**并用 **HINT 控制 pre/post filter**。🔴 **存储按购买时选择的容量计费，而非实际用量（官方明文）**——与 Milvus / Tablestore 相反，容量规划错了直接多付钱。搜索/向量节点单价与最小节点数**需登录复验**[需登录复验]。
- **ADB PostgreSQL 向量**：内置 **RAG Service**（Embedding text-embedding-v3/v4 **0.0006 元/千 token**、Rerank gte-rerank-v2 **0.00096 元/千 token**）。⚠️ **高效云盘已停止新购**；**Serverless Pro（2025-06 商用）**定位替代旧版 Serverless，最低 **16 ACU + 缓存 64 GB**，**旧版不能自助升级 Pro**。
- **Hologres 向量**：🔴 **V4.0 起 HGraph 索引替代 Proxima Graph**（官方标"推荐"）——**新方案不要再按 Proxima 写**（本知识库 Hologres 卡的"Proxima 引擎"表述已在此勘误）。
- **Tablestore 向量**：**DiskANN 图索引**；CU 模式无法设资源上限这一条通常直接卡在客户财务风控。
- **RDS PG + pgvector**：🔴 **`vector` 类型上限 16000 维，但建索引上限仅 2000 维** → **3072 维 embedding（如 text-embedding-3-large）无法直接建 HNSW/IVFFlat**，必须选 1024 / 1536 维。索引：HNSW(`m`/`ef_construction`) / IVFFlat(`lists`，**`probes = lists` 时会退化为全表扫描**) / 阿里云增强 **RabitQ**。官方不锁 pgvector 版本号 → 用 `pg_available_extension_versions` 自查 + `ALTER EXTENSION vector UPDATE`。**可叠加行级安全策略（RLS）把可见性下压到数据层**，是权限敏感场景的最强解。

**③ 三档数据规模的默认选型**[推断]：

| 数据规模 | 首选 | 次选 | 理由 |
| --- | --- | --- | --- |
| 小档 **≤50 万向量** | **RDS PG + pgvector** | 百炼知识库 | 完全在客户 VPC + RLS 权限下压 + 无额外产品线 |
| 中档 **百万~千万** | **阿里云 ES 内核增强版** | **ADB-PG 向量** | ES 给 doc/field level security；ADB-PG 给 SQL 分析融合 |
| 大档 **亿级** | **Milvus 版** | **Lindorm 向量** | Milvus 专业向量引擎；Lindorm 单索引百亿 + 宽表融合 |

**④ 报价前必读**：本节 8 个新产品线的采购四字段已同步写入 [../references/pricing-verification-checklist.md § 3.1 全域速查表 + § 3.2 红色预警清单 + C13/C14](../references/pricing-verification-checklist.md)。

**证据等级**：[官方]（在售状态 / commodityCode / 硬约束 / 单价）+ [推断]（三档规模默认选型）+ [需登录复验]（ES 节点单价、Lindorm 搜索/向量节点单价、OpenSearch 向量检索版预付费码）+ [需工单]（Milvus 数据落盘账号归属）
**最近更新**：2026-08-08（首次建节）

---

### 智能体构建和治理平台 AgentCore（productCode 3052261）— 指针卡[官方][2026-09-21]

**定位**：智能体构建和治理平台，以 Workspace 为资源与权限边界，覆盖 Agent 构建/运行/协作/接入/治理/可观测。🔴 **归属辨析**：与 **AgentTeams**（3034770，**已迁移至 AgentCore**）、**AgentRun**（3049178，独立托管运行时，**未蒸馏**）是 help.aliyun.com 上的**三个平级独立产品**，非父子。
**报价量级（5 计费项速查）**：算力 CU **0.0000694 元/CU**｜网关 CU **0.0000015 元/CU**｜存储 CU **0.00025 元/CU**｜协作专享管控面 **3 元/小时**（≈2160 元/月）｜公网流量 **0.8 元/GB**（走 [[CDT]]）—— 参考地域均标「上海」，北京/杭州/上海/深圳**完全同价**。
**避坑（🔴 三条最高危红线）**：① SLA **99.9%** 但**仅覆盖平台自身 Agent 运行时服务**，且**整份协议不适用于公测/邀测/免费功能及本地云版本**；② 协作管控面**限免至 2026-10-18**，官方「活动结束后计费策略另行通知」，且限免期实例**连续 30 天无操作即不可逆回收**；③ 钉钉/飞书账号集成**最多 30 个用户，超出即失败**。
🔴 **报价三硬缺口**：新加坡单价未公开（**禁用内地价外推**）｜「数据处理量」有计费名目**无单价**｜算力 CU **无规格档位枚举**（「1 vCPU+2GB=7200 CU」是换算示例非规格菜单）。
**依赖产品（交叉引用）**：CMS 云监控（写入 Tracing 数据）/ PrivateLink（点击**后**自动开通）/ SchedulerX3（跳转售卖页购买）→ 🔴 **AgentCore 账单 ≠ 全成本**。
🔴 **术语警示**：官方术语是「**本地纳管 Agent**」不是 NanoAgent（NanoAgent 只存在于 slug）；「**AgentTeams**」在 AgentCore 现役文档里指**协作客户端 (WEB)**，与已迁移的同名产品不是一回事。
**指针**：详见专题页 [knowledge/aliyun-agentcore.md](aliyun-agentcore.md)（含 §10 SA 对客红线 12 条 / §11 官方矛盾 N1~N11 与缺口总登记 / §12 溯源与覆盖率边界）；raw 快照 `raw/aliyun-docs/{agentcore,agentteams}/`（51 个文件含 SHA256）。
**证据等级 / 来源**：`[官方]` help.aliyun.com `.md` Agent 通道，抓取 2026-09-20，蒸馏 2026-09-21 ｜ **最近更新**：2026-09-21（首次建卡＝指针卡，完整知识不在本页）

---

### API 网关 · AI 网关（AI Gateway）— 指针卡[官方][2026-09-21]

**定位**：云原生 API 网关面向 AI 原生应用的**托管入口**，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，**兼容 OpenAI 协议**；支持 **Model API / Agent API / MCP Server** 三类接入。🔴 **归属辨析**：AI 网关是 **API 网关产品族下三个平级子产品之一**（云原生API网关 / **AI 网关** / 原API网关），非独立 productCode 文档根；原API网关已公告 **2026-08-23 停止新购、2027-09-21 全面下线**。
**形态与起步量级（4 选 1）**：Serverless 标准版 **0 元起步无实例费**（🔴 配额极小：MCP Server 20 / 路由 200 / 域名 20 / 插件 5，且 **K8s 服务来源 = N/A → 不能接 ACK**）｜Serverless 企业版 实例费 **0.245 元/小时**（参考单价）+ 用量｜Serverless 旧版 CU **0.005 元/千CU**、CU 系数 **Model API 10 / MCP 5 / Agent API 2**、**不足 10 万按 10 万计**（内地兜底 ≈0.50 元/小时 `[推断]`）｜专享实例最低 `aigw.small.x1` **7.9335 元/小时 / 3,997.5 元/月**（内地），**金融云 = 内地 ×1.9**，最高 `aigw.large.x4` **192,000 QPS / 256 万连接**。
**避坑（🔴 四条最高危红线）**：① **数据处理量私网 0.049 > 公网 0.037 元/GB·小时** —— 「全走内网更便宜」在这项上不成立；② **SLA 存在「无赔偿区」**：协议只承诺 serverless 实例 ≥**99.90%**、普通实例 ≥**99.99%**，而产品页宣称企业版/旧版 **99.95%** → **[99.90%, 99.95%) 无赔偿**，且赔偿**仅限代金券**；③ **自建认证是设计行为不是 bug**：真实鉴权 Path = **鉴权API + 原始请求Path**、且鉴权 API「**需是前缀匹配**」→ 客户的精确匹配接口必然 404，而 **404 不在宽松模式（仅覆盖连接失败与 5xx）兜底范围**，解法是 ext-auth 插件 `endpoint_mode: forward_auth`；④ **Fallback 默认在「被网关限流」时也触发** → 限流流量会打到备用模型，产生额外 Token 费。
🔴 **报价三本账 + 六类连带**：总成本 = 网关账单 + **AI Credits 账单**（0.01 元/Credit，**独立商品**，须先建实例再单独开通，网关账单里看不到）+ 模型服务账单；另有 CDT 公网流量 / SLS 日志 / 云监控企业版或 Tracing / KMS / AI 安全护栏商品（`lvwang_guardrail_public_cn`）**单价文档全部未说明**。
🔴 **报价硬缺口**：专享实例规格单价被 2 处「以控制台/价格页为准」推走｜Serverless 新版 6 项全是「参考单价」**无地域单价表**｜**AI 增强能力的 Credits 折算率查无**（「一次智能路由吃几个 Credit」无解；模型调用侧有文档＝模型元信息配 Credits/1M tokens、默认 0）｜**9 类资源配额在错误码页全是 `%s` 占位**｜**QPS 口径官方无定义**（HTTP QPS 还是 AI QPS？是否区分流式？）→ 不要拿规格表承诺大模型并发能力。
🔴 **多租户架构级结论**：SLR 三个角色的 `Resource` **全为 `"*"` 无资源级收窄**；140 个 Action 中 **66 个（47.1%）** 标「全部资源」；**MCP / AI 模型元信息 / 消费者组 / 插件四类对象在 RAM 层面根本没有 ARN 定义** → **多租户隔离只能分账号或分实例**，讲方案时必须先说这条。另：**突破配额白名单后官方明示「不作 SLA 承诺」→ 提额＝弃 SLA**。
**术语与 slug 警示**：🔴 `ai-cue-template`（官方标题「AI 提示词插件」）正文实为 **ai-prompt-decorator**，`ai-cue-decorator`（标题「AI 提示词模板插件」）正文实为 **ai-prompt-template** —— **标题与 slug 交叉错位，对客只写插件名**；日志字段官方拼作 `ai_log.safechack_status`（**写 SLS 查询必须照抄错字**）；🔴 **MCP 消费者认证方式官方口径冲突（裁决 C9 已修订）**：2026-01 发布记录称「MCP Server 支持 JWT 认证」，专页仍称「目前仅支持 API Key」→ 按 R4 优先级（带日期发布记录 > 静态专页）倾向支持 JWT，但**对客须实测、不得仅凭文档承诺**；🔴 **A2A 协议转换有官方明文**（概述页「提供 REST 到 A2A 协议的转换能力」+ 推荐基于 A2A 经 Nacos AI Registry 注册发现），**但 189 页里查无配置方法** → 可说有能力、给不出配置步骤，落地前须实测。
**依赖/连带（交叉引用）**：🔴 **公网流量出账方按形态分**——专享实例走 [[CDT]] 统一出账；**Serverless 新版由网关侧按 0.8 元/GB 计入网关账单（出网+入网）**，自配 NAT 网关则出网部分不在网关侧计费（漏报即少算一整项）；MCP 语义检索依赖向量库与 Embedding/Rerank 模型调用（是否消耗 Credits **全页查无**）；🔴 **[[aliyun-agentcore]] 的 MCP Server 由 API 网关承载**（其 SLR 含 **57 条 `apig:` Action**、AgentTeams 9 个依赖产品明列「AI 网关」）→ 客户用 AgentCore 会**同时产生 AI 网关账单**。
**指针**：详见专题页家族 [knowledge/aliyun-ai-gateway.md](aliyun-ai-gateway.md)（主页 §0 溯源 / §1 定位 / §2 形态容量 / §14 实战避坑 / §15 SA 速查卡）+ 6 个子页 [-billing](aliyun-ai-gateway-billing.md) / [-traffic](aliyun-ai-gateway-traffic.md) / [-auth](aliyun-ai-gateway-auth.md) / [-mcp-agent](aliyun-ai-gateway-mcp-agent.md) / [-plugins](aliyun-ai-gateway-plugins.md) / [-ops](aliyun-ai-gateway-ops.md)；合计 **9471** 行 / **411** 张表**；raw 快照 `raw/aliyun-docs/ai-gateway/`（**186** 个文件含 SHA256SUMS 与 README）。
**证据等级 / 来源**：`[官方]` help.aliyun.com `.md` Agent 通道，抓取 + 蒸馏均 2026-09-21 ｜ 标注分布 `[官方｜slug]` 290 · `[官方原文]` 49 · `[官方矛盾]` 99 · `[文档未说明]` 550 · `[推断]` 201 ｜ **最近更新**：2026-09-21（首次建卡＝指针卡，完整知识不在本页）

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

模型调用入口与治理？（2026-09-21 新增）
├── 单一供应商、直连即可、无需统一鉴权与计量 → 直接调百炼 / 第三方模型 API
└── 需要 多模型路由 / Token 限流 / Fallback / 计量分账 / 内容合规护栏 / MCP 服务上架 / 统一消费者鉴权
                  → AI 网关（API 网关产品族三子产品之一；详见 knowledge/aliyun-ai-gateway.md 专题页家族）
                    ├── PoC / 开发测试 → Serverless 标准版（0 元起步无实例费；🔴 配额极小且 K8s 服务来源=N/A，不能接 ACK）
                    ├── 生产（要独立入口 + 自定义域名） → Serverless 企业版（实例费 0.245 元/小时，参考单价）
                    ├── 核心系统（要完整插件体系 + 自定义插件） → 专享实例（aigw.small.x1 7.9335 元/小时起 ~ aigw.large.x4 192,000 QPS）
                    ├── 已有认证接口不愿改 → 🔴 走 ext-auth 插件 endpoint_mode: forward_auth，不要走「自建认证」（后者要求鉴权 API 前缀匹配且会拼接原始 Path）
                    └── 开源替代 = Higress 自建（官方对比页称全托管免运维 / 99.99% SLA / 内核优化 90%+；🔴 属概述页宣称，口径优先级最低档，不得用于赔偿主张）
                    🔴 报价必读：三本账（网关 + AI Credits 独立商品 + 模型服务）+ 六类连带（CDT/SLS/云监控/KMS/AI安全护栏），AI 增强能力的 Credits 折算率查无

应用类型？
├── 对话/Agent → 百炼 + Qwen
│                 └── 多来源 Agent 统管 / Team 协作 / 治理与观测 → AgentCore（智能体构建和治理平台，productCode 3052261；详见 knowledge/aliyun-agentcore.md）；与百炼非可互换＝百炼在模型与 RAG 服务侧、AgentCore 在 Agent 构建与治理平台侧 [推断]（分工依据 raw/aliyun-docs/agentcore/agentcore-product-overview.md:11 官方定位逐字「将自研、开源 Harness、商业 SaaS Agent 多来源统管于一个平台」）
├── RAG 知识库 → 百炼知识库（零运维）；向量库要选型 → 见「向量检索 / RAG 检索引擎选型」一节
│                 └── 小档 ≤50万向量 → RDS PG+pgvector；中档 百万~千万 → 阿里云 ES / ADB-PG；大档 亿级 → Milvus 版 / Lindorm
├── 文档解析入库 → 文档智能 DocMind（基础链路 0.02 / 增强链路 0.04 元/页）
├── 图像生成 → 通义万相
├── 代码辅助/智能开发（开发者/IDE 侧） → Qoder CN 系列（原通义灵码）
├── Vibe Coding（业务/无代码/端到端全栈） → Meoo（秒悟，含微信小程序）
└── 语音识别/合成 → 百炼语音模型
```

---

## 中间件

### MSE（微服务引擎）

**官方定位**：一站式微服务治理平台——注册中心 + 配置中心 + 网关 + 治理。100% 兼容开源 Nacos/ZooKeeper/Eureka/Sentinel。
**能做**：
- **Nacos 注册配置中心**（托管 Nacos 集群，四版本：开发版/专业版/企业版/Serverless）
- **ZooKeeper**：托管 ZK 集群
- **云原生网关**（MSE 产品线内的网关形态，文档在 help.aliyun.com/zh/mse/ 下）：API 网关（统一入口/限流/鉴权/路由/协议转换）。⚠️ 名称消歧（2026-09-21）：现在主推的「**云原生API网关**」属于 **API 网关（APIG）产品线**（与 AI 网关、原API网关并列三种形态），不是 MSE 的子功能 → 详见下方 [云原生 API 网关（APIG）/ AI 网关 深度卡](#云原生-api-网关apig--ai-网关深度卡)。MSE 侧网关文档线（认证插件清单含 edas-service-auth）与 APIG 线独立维护 [官方]；两者的承接/迁移关系官方未说明
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
**SLA**：可用性承诺 ≥99.95%（以单个事件总线/事件流为维度，按自然月统计）；赔偿分档——99%≤可用性<99.95% 赔当月服务费 15%，<99% 赔 30%，代金券形式，需事故月结束后 2 个月内申请。免责含客户自身配置错误（事件源/目标/安全组/VPC）、预告知维护割接、不可抗力等。注意 99.95% 是服务可用性，非端到端投递时延保障（投递秒级非强实时）。来源：terms.alicdn.com SLA 协议 20251030 版
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

### 云原生 API 网关（APIG）/ AI 网关【深度卡】

> 2026-09-21 蒸馏 16 篇官方/开源文档（raw/aliyun-docs/aliyun-docs-2026-09-21-*，共 188KB），专项补齐「网关外部认证（接客户自建鉴权服务）」与产品谱系消歧。与下方 [原 API Gateway（传统版）卡](#api-gateway原-api-网关--传统版--apigateway) 并列，新项目一律看本卡。

**官方定位**：基于 Envoy 内核和开源 Higress，将流量网关、微服务网关、K8s Ingress 三合一；提供 REST API/HTTP API/WebSocket API 全生命周期管理、Nginx Ingress 兼容与迁移、限流降级、JWT/OIDC/mTLS 认证鉴权、插件市场、日志投递与链路追踪，支持专享实例和 Serverless 实例，SLA 99.99% [官方]（help.aliyun.com/zh/api-gateway/llms.txt 子产品行）。

#### 产品谱系：三种形态 [官方]

llms.txt 第 3 行逐字：「**API 网关（API Gateway）提供云原生 API 网关、AI 网关和原 API 网关三种形态**，涵盖路由转发、流量治理、协议转换、鉴权认证等核心能力。」

| 形态 | 产品线/文档路径 | 定位 | 状态（截至 2026-09-21） |
| --- | --- | --- | --- |
| 云原生 API 网关（apig） | help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/ | Envoy+Higress 内核，流量/微服务/Ingress 三合一；专享实例 + Serverless 实例 | 在售主推 |
| AI 网关（aigw） | help.aliyun.com/zh/api-gateway/ai-gateway/ | 云原生 API 网关**面向 AI 原生应用的托管入口**（同一产品的 AI 实例形态）；专享实例 + Serverless 实例 | 在售主推 |
| 原 API 网关（传统版 / apigateway） | help.aliyun.com/zh/api-gateway/traditional-api-gateway/ | RESTful/SOAP 接口托管 + SDK 自动生成 | **2026-08-23 停止新购、2027-09-21 全面下线**，存量实例迁移至云原生 API 网关 |

- llms.txt 第 41 行逐字：「原 API 网关（传统版）……产品将于 **2026 年 8 月 23 日停止新购、2027 年 9 月 21 日全面下线，存量实例请迁移至云原生 API 网关**」[官方]
- ⚠️ **截至 2026-09-21，原 API 网关已过停止新购日期**（2026-08-23 已过）[推断：由官方日期与当前日期对比得出]
- 名称消歧：MSE 产品线内另有「MSE 云原生网关」文档线（认证插件清单含 edas-service-auth，help.aliyun.com/zh/mse/user-guide/authentication-authentication）[官方]，与 APIG 产品线的「云原生API网关」是两套文档目录；两者的承接/迁移关系**官方未说明**。

#### AI 网关定位与两种规格 [官方]

llms.txt 第 40 行逐字：「**AI 网关是云原生 API 网关面向 AI 原生应用的托管入口**，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，兼容 OpenAI 协议；支持 Model API/Agent API/MCP Server 三类接入，覆盖多模型路由、按比例灰度、HTTP to MCP 转换、A2A 协议转换、消费者 API-Key/JWT/HMAC 鉴权、KMS 凭证托管、Token 限流、Fallback、语义缓存、AI 安全护栏（内容合规/提示词攻击/敏感数据/恶意文件/水印）与全链路可观测；**提供专享实例与 Serverless 实例，按实例规格或 AI Credits 计费**。」

- **不是**百炼/DashScope 的模型网关：它是网关产品（APIG）的一种实例形态，作为 AI 应用的统一入口**代理**百炼等 17+ 家模型供应商（含自建 Ollama/vLLM/SGLang），模型能力本身由供应商提供（创建 AI 服务时官方明确「本AI服务所提供的大模型能力并非由AI网关直接提供」）[官方]
- 能力清单（从上行提炼）：①Model API / Agent API / MCP Server 三类接入；②多模型路由 + 按比例灰度；③HTTP to MCP 转换；④A2A 协议转换；⑤消费者鉴权（API-Key/JWT/HMAC）；⑥KMS 凭证托管；⑦Token 限流；⑧Fallback；⑨语义缓存；⑩AI 安全护栏；⑪全链路可观测 [官方]
- **专享实例**：独占物理资源，适合性能/隔离性要求高的场景；**支持安装与启用插件** [官方]
- **Serverless 实例**：新版公测 2026-08-31 结束、2026-09-01 起商业化计费（存量自动转商业化，不用的实例须在 9-1 前删除）；**不支持安装插件**（见避坑 🔴）[官方]

#### 能力边界

**擅长**：
- 统一入口三合一（流量网关 + 微服务网关 + K8s Ingress），Nginx Ingress 兼容迁移
- 微服务/AI 双场景路由：REST/HTTP/WebSocket API 全生命周期、多模型路由、MCP Server 托管
- 认证鉴权体系：JWT/OIDC/mTLS、消费者认证（API-Key/JWT/HMAC）、**自建鉴权服务对接（全局认证鉴权）**、Higress WASM 插件生态（key-auth/basic-auth/hmac-auth/jwt-auth/oauth/jwt-logout 等平台插件）
- AI 增强：Token 限流、语义缓存、Fallback、AI 安全护栏、按比例灰度
- 插件扩展：官方插件（Higress 官方开放到插件市场的插件）/ 社区插件（Higress 社区贡献）/ 自定义插件（用户上传 WASM，Go 1.24 编译需网关 ≥2.1.5），插件规则支持路由级/域名级/实例级三级作用域 [官方]

**不擅长**：
- L4 纯负载均衡（→ NLB）；七层简单转发不需要 API 管理时（→ ALB）
- 模型推理本身（→ 百炼/PAI-EAS）；Agent 编排（→ 百炼 ADK）
- Dubbo/HSF 深度服务治理与注册发现（→ MSE Nacos/Sentinel；自建鉴权服务的鉴权协议也仅支持 HTTP，不支持 Dubbo）
- Serverless 版 AI 网关的插件扩展（官方硬限制，装不了插件）
- 传统 RESTful/SOAP API 托管 + SDK 自动生成（原 API 网关的能力面，但该产品已停止新购）

#### 网关外部认证的两条路（本次蒸馏核心）

客户已有自建认证/鉴权服务（自定义 Token 格式，非 JWT 可本地验签），要在网关入口统一鉴权，有 A/B 两条路。**两条路的前置步骤相同：先把认证服务注册为网关「服务」**。

##### 前置步骤：创建服务 / 服务来源 [官方]

- 入口：控制台 → 实例 → 左侧「服务」→「创建服务」，选择服务来源；若服务在 ACK/Nacos 中，需先在「服务 → 来源」页签「创建来源」
- 服务来源类型与关键参数：

| 服务来源 | 关键参数/约束 | 出处 |
| --- | --- | --- |
| DNS 域名 | 服务地址格式 `<DNS域名>:<服务端口>`（AI 网关文档原文），支持多个以英文逗号分隔；**外网地址需配置 NAT 网关**；无需预先配置服务来源 | aigw-creating-services（apig 版 create-service 该栏原文写作 `<后端节点IP>:<服务端口>`，两处表述不一致，DNS 来源建议按 AI 网关文档口径填域名） |
| 固定地址 | 服务地址格式 `<IP>:<服务端口>`；外网地址需 NAT 网关；无需服务来源 | aigw-creating-services / apig-create-service |
| 容器服务（ACK/ACS/ACK Serverless） | 需先创建「来源」：**集群版本 ≥1.18（建议 1.28+）**、**必须与网关同 VPC**（跨 VPC 需重建网关实例）、节点池**安全组需开放服务全部端口**；单网关最多关联 3 个 ACK 集群来源 | apig-create-service-source / aigw-creating-services |
| MSE Nacos | 需先创建「来源」：仅展示 `MCPEnabled = true` 的实例；同 VPC；单网关最多关联 1 个 Nacos 实例 | apig-create-service-source / aigw-creating-services |
| TLS 模式（DNS/固定地址） | 默认关闭；单向 TLS（HTTPS 访问）；双向 TLS（mTLS） | apig-create-service / aigw-creating-services |
| 其他来源 | FC 函数计算（仅 3.0）、SAE Kubernetes 服务、云工作流 CloudFlow（网关 ≥2.1.8，仅 apig）、AI 服务（17+ 模型供应商）、Agent 服务（百炼/Dify/自定义，仅 aigw） | 两篇创建服务文档 |

- 服务 FQDN 命名规则（**service_name 的取值形态**，apig 与 aigw 两份 Go 插件文档第 462 行注释逐字相同 [官方]）：

> 「带服务类型的完整 FQDN 名称，例如 `my-svc.dns`, `my-svc.static`, `service-provider.DEFAULT-GROUP.public.nacos`, `httpbin.my-ns.svc.cluster.local`」

| 服务来源类型 | FQDN 命名格式 | 官方/开源原文示例 |
| --- | --- | --- |
| DNS 域名 | `<服务名>.dns` | `my-svc.dns` [官方]；`ext-auth.dns` [开源 ext-auth README 第 47 行] |
| 固定地址（静态IP） | `<服务名>.static` | `my-svc.static` [官方]；第 467 行注释「**静态IP类型服务的逻辑端口是80**」 |
| MSE Nacos | `<服务名>.<分组>.<命名空间>.nacos` | `service-provider.DEFAULT-GROUP.public.nacos` [官方] |
| 容器服务（K8s） | `<服务名>.<命名空间>.svc.cluster.local` | `httpbin.my-ns.svc.cluster.local` [官方]；`ext-auth.my-ns.svc.cluster.local` [开源] |

- ⚠️ 存疑：`.static` 类型服务的端口口径——官方仅有代码注释「逻辑端口是80」，若认证服务实际监听 8080 该填什么**官方未说明**（ext-auth 插件可另配 `service_port`，但全局认证鉴权的端口行为未说明）→ 建议优先用 **DNS 域名来源**规避 [推断]

##### A 路：安全管理 → 全局认证鉴权 →「自建的鉴权服务」[官方]

入口：实例 → **安全管理 → 全局认证鉴权 → 创建鉴权**，鉴权类型选「**自建的鉴权服务**」。官方明确云原生API网关全局认证鉴权只有 **JWT / OIDC / 自建认证鉴权** 三种方式（global-authentication 文档），自建 Token 格式对应第三种。

鉴权流程（官方原文语义）：网关截取原始业务请求的 **Path（含 Query Parameters）+ HTTP 方法 + Token** 组成新请求发给自建鉴权服务；「假设自建鉴权服务的鉴权API是 `/validateToken`，那么鉴权请求的真实 Path 是**鉴权API加上原始业务请求的Path**后的结果，即 `/validateToken/order`」——即**鉴权API是前缀拼接语义**。

完整配置项表（apig 与 aigw 两份官方文档 diff 后配置表逐字一致，仅产品名措辞与控制台入口不同）：

| 配置项 | 说明 |
| --- | --- |
| 开启 | 是否开启网关鉴权 |
| 鉴权名称 | 自定义名称 |
| 鉴权类型 | 选「自建的鉴权服务」 |
| 鉴权服务 | 从服务管理中选择已添加的服务。**仅支持 HTTP 协议，不支持 Dubbo 等**；多端口 K8s Service **默认取第一个端口**，要用其他端口需在容器服务中另建一个只含目标端口的 Service |
| 鉴权API | 鉴权服务的 Path，**前缀匹配**。SpringMVC 示例：鉴权 API 为 `/check` 时需 `@RequestMapping("/check/")` 处理 `/check/**` |
| Token位置 | Token 所在请求 Header，常见 Authorization、Cookie；下拉或手动输入 |
| 鉴权请求中允许携带的头部 | 按需配置额外头部；**Host、Method、Path、Content-Length 默认自动添加**，无需手动配 |
| 鉴权响应中允许保留的头部 | 鉴权响应头回填到客户端请求；同名头部值会被覆盖 |
| 鉴权请求中允许携带Body | 勾选后鉴权请求带原始 Body；「Body最大字节数」单位字节 |
| 超时时间 | **单位：秒，默认 10 秒** |
| 模式 | **宽松模式**（鉴权服务不可用——连接失败或 5xx——时**放行**客户端请求，官方建议）/ **严格模式**（不可用时**拒绝**） |
| 简单条件（授权） | **白名单模式**（名单内 Hosts/Paths 免鉴权，其余都鉴权）/ **黑名单模式**（名单内才鉴权）。规则条件=域名+路径（精确/前缀末尾加`*`/正则 Google Re2）+大小写敏感+请求头（等于/不等于/存在/不存在/包含/不包含/前缀/后缀/正则，多 Header 为「与」）；多行规则之间为「或」 |
| 复杂条件（授权） | YAML 配置 **Envoy permission 数据结构**，与/或/非组合条件（and_rule/or_rules/not_rule）；满足条件才执行鉴权 |

复杂条件官方示例（正则匹配域名，逐字抄自 raw）：

```yaml
permissions:
# and_rule 表示下面的所有 rules 条件同时成立时执行鉴权
- and_rule:
    rules:
      - url_path:
          # 前缀匹配路径
          path:
            prefix: /
      - header:
          # 正则匹配
          safe_regex_match:
            regex: "(exampleA\\.com|exampleB\\.com)"
          # 支持HTTP Pseudo-Header规范，可通过":authority"这个Header来获取域名
          name: ":authority"
```

（注意官方提示：regex 需**完全匹配**而非部分匹配，`test.exampleA.com` 不会命中上例。）

鉴权结果判定 [官方]：
- 鉴权服务返回 **200** → 放行，网关继续转发原始业务请求
- 返回 **401/403** → 网关直接把鉴权服务的响应返回客户端（拒绝）
- 若认证服务受业务限制必须**统一返 200** → 用内置响应头 **`x-mse-external-authz-check-result`**：`true` 放行 / `false` 拒绝

管理与生效：**创建完成后需在全局认证鉴权页面手动点「开启」才生效**；只有**关闭状态才可删除**；详情页可追加「创建授权信息」（域名+Path+匹配方式）。

A 路作用域说明：配置入口在实例级「安全管理 → 全局认证鉴权」，授权范围仅靠简单条件（Hosts/Paths/Header 黑白名单）与复杂条件（Envoy permission YAML）表达；**能否像插件一样按路由级/域名级作用域挂载，官方未说明**；**是否有实例规格限制（如 Serverless 版能否使用 A 路），官方未说明**。「apig 与 aigw 两条产品线 A 路配置一致」是主控对两份官方原文逐字对比得出的**推断**（本次 diff 复核：配置表除产品名措辞外一致），官方并未声明两者一致。

##### B 路：插件市场 Higress `ext-auth` 插件（控制台中文名「外部认证」）[开源]

出处：alibaba/higress 仓库 `plugins/wasm-go/extensions/ext-auth/README.md`（渲染页 higress.ai/docs/latest/plugins/authentication/ext-auth/）。插件执行阶段=**认证阶段**，优先级 **360**。实现参考 Envoy 原生 ext_authz filter 的 HTTP 部分。
注意：help.aliyun.com 三条产品线（云原生API网关/AI网关/MSE 云原生网关）的「认证鉴权」平台插件清单页均只有 key-auth/basic-auth/hmac-auth/jwt-auth/oauth/jwt-logout（MSE 另有 edas-service-auth），**均不含 ext-auth** [官方]；阿里云官方文档定义「官方插件=Higress 官方开放到插件市场的插件」，而 ext-auth 是 Higress 官方仓库插件，但**当前是否在阿里云插件市场在架，官方未说明**（以控制台插件市场实况为准）。

顶层字段表（逐字抄自 README）：

| 名称 | 数据类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `http_service` | object | 是 | - | 外部授权服务配置 |
| `match_type` | string | 否 | | 可选 `whitelist` 或 `blacklist` |
| `match_list` | array of MatchRule | 否 | | 请求匹配规则列表，支持按域名、方法、路径和请求头是否存在进行匹配 |
| `failure_mode_allow` | bool | 否 | false | 设为 true 时，即使与授权服务通信失败或其返回 5xx，仍接受客户端请求 |
| `failure_mode_allow_header_add` | bool | 否 | false | 与上一项同为 true 时，失败放行会加头 `x-envoy-auth-failure-mode-allowed: true` |
| `status_on_error` | int | 否 | **403** | 授权服务无法访问或 5xx 时返回给客户端的状态码 |

`http_service` 字段表：

| 名称 | 数据类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `endpoint_mode` | string | 否 | **envoy** | 可选 `envoy` 或 `forward_auth` |
| `endpoint` | object | 是 | - | 发送鉴权请求的 HTTP 服务信息 |
| `timeout` | int | 否 | **1000** | ext-auth 服务连接超时时间，**单位毫秒** |
| `authorization_request` | object | 否 | - | 发送鉴权请求配置 |
| `authorization_response` | object | 否 | - | 处理鉴权响应配置 |

`endpoint` 字段表：

| 名称 | 数据类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `service_name` | string | **是** | - | 「输入授权服务名称，**带服务类型的完整 FQDN 名称**，例如 `ext-auth.dns` 、`ext-auth.my-ns.svc.cluster.local`」（README 第 47 行逐字）——即填网关「服务」里已注册服务的带服务类型后缀 FQDN，**不是裸域名也不是裸服务名**，四种来源格式见上方 FQDN 对照表 |
| `service_port` | int | 否 | **80** | 授权服务的服务端口 |
| `service_host` | string | 否 | - | 请求授权服务时设置的 Host 头，不填时和 FQDN 保持一致 |
| `path_prefix` | string | `endpoint_mode=envoy` 时**必填** | - | envoy 模式下鉴权请求的路径**前缀**（拼接原始请求路径） |
| `request_method` | string | 否 | GET | forward_auth 模式下鉴权请求的 HTTP Method |
| `path` | string | `endpoint_mode=forward_auth` 时**必填** | - | forward_auth 模式下鉴权请求的**固定路径** |

`authorization_request` 字段表：

| 名称 | 数据类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `allowed_headers` | array of StringMatcher | 否 | - | 匹配项的客户端请求头加入鉴权请求；**自动包含 `Authorization` 头**（forward_auth 模式还会自动加 `X-Forwarded-*`） |
| `allowed_properties` | array of AllowedProperty | 否 | - | 把 Envoy filter state 的 property（如 `route_name`）映射为 HTTP header 发给授权服务 |
| `headers_to_add` | map[string]string | 否 | - | 附加到鉴权请求的固定头；同名客户端请求头被覆盖 |
| `with_request_body` | bool | 否 | false | 缓冲客户端请求体并发送至鉴权请求（GET/OPTIONS/HEAD 不生效） |
| `max_request_body_bytes` | int | 否 | **10MB** | 内存中保存请求体的最大尺寸；达到该值**返回 413 且不启动授权过程**，**此设置优先于 `failure_mode_allow`** |

`authorization_response` 字段表：

| 名称 | 数据类型 | 必填 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| `allowed_upstream_headers` | array of StringMatcher | 否 | - | 匹配项的鉴权响应头加入原始客户端请求（转发给后端）；同名覆盖 |
| `allowed_client_headers` | array of StringMatcher | 否 | - | 不设置时请求被拒绝则鉴权响应的**全部**头返回客户端；设置后仅匹配项返回 |

辅助类型：StringMatcher（exact/prefix/suffix/contains/regex 五选一）；MatchRule（match_rule_domain 支持 `*.bar.com` 泛域名 / match_rule_method / match_rule_path / match_rule_type / match_rule_headers）；HeaderPresenceCondition（name + exists，值为空串仍视为存在）。

两种 `endpoint_mode` 差异（README 原文语义）：

| 维度 | envoy 模式（默认） | forward_auth 模式 |
| --- | --- | --- |
| HTTP Method | 用**原始请求**的 Method | 用配置的 `request_method`（默认 GET） |
| 路径 | `path_prefix` **前缀拼接**原始请求路径（同 A 路语义） | 固定 `path`，不拼接 |
| 额外头 | 自动带 `Authorization` | 自动带 `Authorization` + `x-forwarded-proto` / `x-forwarded-method` / `x-forwarded-host` / `x-forwarded-uri`（原始 path 含参数） |
| 适用 | 鉴权接口按业务 Path 分路径 | **认证接口是固定路径时必须用此模式** |

黑白名单：默认**白名单**模式，白名单为空时所有请求都鉴权；whitelist 匹配即跳过鉴权，blacklist 匹配才鉴权；单规则内条件 AND、`match_list` 规则间 OR。

完整示例 YAML（逐字抄自 Higress README；假设 ext-auth 服务在 K8s 中 serviceName=`ext-auth`、命名空间 `backend`、端口 `8090`、路径 `/auth`）：

envoy 模式（示例1）：

```yaml
http_service:
  endpoint_mode: envoy
  endpoint:
    service_name: ext-auth.backend.svc.cluster.local
    service_port: 8090
    path_prefix: /auth
  timeout: 1000
```

envoy 模式带头透传的增强版（示例2，鉴权响应头 `x-user-id`/`x-auth-version` 回填后端请求）：

```yaml
http_service:
  authorization_request:
    allowed_headers:
      - exact: x-auth-version
    headers_to_add:
      x-envoy-header: true
  authorization_response:
    allowed_upstream_headers:
      - exact: x-user-id
      - exact: x-auth-version
  endpoint_mode: envoy
  endpoint:
    service_name: ext-auth.backend.svc.cluster.local
    service_host: my-domain.local
    service_port: 8090
    path_prefix: /auth
  timeout: 1000
```

forward_auth 模式（示例1）：

```yaml
http_service:
  endpoint_mode: forward_auth
  endpoint:
    service_name: ext-auth.backend.svc.cluster.local
    service_port: 8090
    path: /auth
    request_method: POST
  timeout: 1000
```

forward_auth 模式下鉴权服务**实际收到的抓包请求**（原始请求为 `GET /users?apikey=...`，Host: foo.bar.com）：

```
POST /auth HTTP/1.1
Host: ext-auth.backend.svc.cluster.local
Authorization: xxx
X-Forwarded-Proto: HTTP
X-Forwarded-Host: foo.bar.com
X-Forwarded-Uri: /users?apikey=9a342114-ba8a-11ec-b1bf-00163e1250b5
X-Forwarded-Method: GET
Content-Length: 0
```

（envoy 模式下则收到 `POST /auth/users?apikey=... HTTP/1.1`，即前缀拼接效果。鉴权服务返回 5xx 时客户端收到 `status_on_error` 默认 403 + 鉴权服务全量响应头。）

安装启用（B 路操作路径）[官方]：插件市场（或实例 → 插件）→ 安装 → **规则配置**（选择生效范围：**MCP/路由级** / **域名级**（特定域名优先级高于泛域名）/ **实例级**（全局兜底））→ 启用。卸载前需先停用规则；未启用卸载会连带删除规则配置。

##### A/B 路选型建议

| 场景 | 推荐 | 理由 |
| --- | --- | --- |
| Serverless 版 AI 网关 | **只能 A 路** | 官方原文：仅专享实例型 AI 网关支持安装与启用插件，Serverless 版不支持 |
| 需要按路由/域名细粒度挂载外部认证 | **B 路** | 插件规则官方支持路由级/域名级/实例级三级作用域；A 路作用域仅实例级入口 + 黑白名单表达（路由级挂载官方未说明） |
| 认证接口是固定路径（如统一 POST /auth） | **B 路 forward_auth 模式** | A 路与 B 路 envoy 模式都是前缀拼接语义，固定路径需 forward_auth 的 `path` |
| 只想要实例全局「一层鉴权」+ 白名单放行健康检查/登录接口 | A 路即可 | 简单条件白名单直接表达，无需装插件 |
| 需要把鉴权响应头（如 x-user-id）透传给后端 | 两路都行 | A 路「鉴权响应中允许保留的头部」；B 路 `allowed_upstream_headers` |
| 需要 failure 放行/拒绝精细控制 + 自定义失败状态码 | B 路 | `failure_mode_allow` + `status_on_error`；A 路对应宽松/严格模式（状态码不可自定义，官方未说明） |
| 复杂与/或/非授权条件 | A 路复杂条件（Envoy permission YAML）或 B 路 match_list | A 路表达力更强（not_rule 嵌套）；B 路 MatchRule 仅 AND/OR 两层 |

#### MCP 维度：MCP 服务鉴权（2026-09-21 收口补充）

> 来源：MCP 官方规范（raw/standards/standards-2026-09-21-*，2025-06-18/2025-11-25/2026-07-28/draft 四版关键结论一致）+ AI 网关 MCP 官方文档 5 篇（raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-{debug-mcp-services, consumer-certification, http-to-mcp-field-configurations, new-feature-release-notes, engine-version-description}.md）+ Higress ext-auth 源码摘录（raw/misc/misc-2026-09-21-higress-ext-auth-source-excerpts.md）+ ATA 实操摘录（raw/ata/ata-2026-09-21-*，⚠️ SSO 限制仅归档摘录）。

##### 协议层事实 [规范]（MCP 官方规范，最新版 2026-07-28）

- 「The Model Context Protocol provides authorization capabilities **at the transport level**」→ 鉴权在**传输层**（传输层鉴权，统一覆盖所有 MCP 方法），不在 MCP 方法语义层
- 「Authorization is **OPTIONAL** for MCP implementations」→ 是否鉴权是**服务器级**选择，不是方法级选择
- 「MCP servers **MUST** validate access tokens **before processing the request**…ensure **no data is returned to unauthorized parties**」
- 「Servers **SHOULD** implement proper authentication for **all connections**」（transports Security Warning 第 3 条）
- Streamable HTTP：「The server **MUST** provide a single HTTP endpoint path (…**MCP endpoint**) that supports both POST and GET methods」（即**单一 MCP endpoint**）「Every JSON-RPC message sent from the client **MUST** be a new HTTP POST request to the MCP endpoint」
- 规范**显式预设网关介入**：头部镜像 body 字段的目的是「so that **intermediaries (load balancers, gateways**, observability tooling) can route and inspect requests without parsing the body」
- 标准栈：OAuth 2.1(draft-13) + RFC6750 Bearer + RFC8414 + RFC7591 + RFC8707；MCP Server = OAuth 2.1 resource server；MUST 实现 RFC 9728（`/.well-known/oauth-protected-resource`）；MUST 在 401 里回 `WWW-Authenticate: Bearer resource_metadata="..."`
- **不存在任何 per-method 免鉴权白名单**：规范里没有 "unprotected endpoints" 概念（grep `unprotected`/`anonymous`/`without auth` 于 authorization.mdx 四版 + transports + lifecycle.mdx + server/tools.mdx + security_best_practices.mdx + tutorials/security/* 全部 0 命中；lifecycle.mdx 与 server/tools.mdx 里 `authoriz|authenticat|credential` 出现 0 次）

🔑 **推论 [推断]（推理链条）**：`initialize`/`tools/list`/`tools/call` 在 HTTP 层是**同一 path、同一 method(POST)**，网关不解析 body 就**物理上无法区分**这三类 JSON-RPC 消息 → 任何声称「某方法能鉴权、某方法不能」的说法，只可能发生在鉴权被挂到 **MCP 语义层**（按 MCP 服务/工具挂消费者认证）时，在 HTTP 传输层不成立。

##### 三种鉴权能力的本质区别 [官方]（选型核心表）

| 能力 | 凭证来源 | 校验位置 | 能否调客户自有接口 | 作用维度 |
| --- | --- | --- | --- | --- |
| 内置认证插件（key-auth/basic-auth/hmac-auth/jwt-auth/jwt-logout/oauth） | 网关自发 | 网关本地 | ❌ | 插件三级作用域 |
| **消费者认证**（AI 网关，支持 MCP 服务级/工具级） | 网关自发（API Key） | 网关本地 | ❌ | MCP 服务级 > MCP 工具级 |
| **自建鉴权**（安全管理→全局认证鉴权）/ **ext-auth 插件** | 客户自有 | **回调客户 HTTP 接口** | ✅ | 自建鉴权=实例级；ext-auth=插件三级作用域 |

- [官方] 消费者认证：「支持为 MCP 服务和 MCP 工具配置消费者认证」「MCP服务级别消费者认证权限高于MCP工具级别」「开启消费者认证后，若没有配置授权关系，将无法访问当前API」「认证方式目前仅支持 **API Key** 认证」
- 🔴 **官方文档自相矛盾（必须记录）**：consumer-certification.md 称「仅支持 API Key」，但发布记录 2026-01 称「MCP Server 支持 JWT 认证」→ 文档口径滞后，**以控制台实际为准**
- [官方] `ApiKeyIdentityConfig` 支持 `apikeySource` = Header / Query String，且「仅AI网关Header模式允许1-3项」→ **双层组合方案的关键**：把网关 API Key 放独立头或 query，`Authorization` 留给客户自有 PAT
- 🔴 [推断，**未实测**] **双层组合方案**：外层 MCP 服务级消费者认证（API Key 放独立头/query）兜住全部方法 + 内层 ext-auth 回调客户 PAT 校验接口。架构可行、未实测，上线前必须在客户环境验证。

##### HTTP转MCP 场景的鉴权语义 [官方]

- 工具由 Swagger/OpenAPI3 导入或自定义 YAML，**存放在网关**；`tools/list` 由网关按 YAML 应答，**不回调客户后端**；只有 `tools/call` 才真正打到客户服务（http-to-mcp-field-configurations 全文已归档）
- ⚠️ 但**不能**因此说「tools/list 无需鉴权」：①官方《调试MCP服务》第 29 行逐字——「如果所选消费者只授权了 MCP工具级别消费者认证，且仅授权某些工具的情况下，**HTTP转MCP的场景中获取工具列表只能看到和调用有权限的工具**；直接代理场景调试的时候能看到全部工具，选择授权的工具调用是ok的，没权限的会403」→ **工具级鉴权在 HTTP转MCP 下确实作用于 tools/list（做结果过滤）**。这条官方原文的价值：任何「tools/list 不能鉴权」的内部口径都与它冲突；②tools/list 会泄露工具目录元数据
- [实战] ATA 11020495607 陈思亮(玄斧) 2025-10-29《AI网关-Restful API转换MCP的桥梁》：唯一真正的 HTTP转MCP + 消费者鉴权端到端实操（「新建消费者｜为后续MCP接口鉴权使用」→「为mcp添加消费者鉴权」→「调试界面选择…消费者、api key…点击连接测试连通性，正常情况会提示连接成功并左侧框会列出该mcp服务的工具列表」）→ **证明消费者鉴权下连接与列工具均需 API Key**（SSO 限制，归档为摘录 raw/ata/ata-2026-09-21-http-to-mcp-consumer-auth-excerpts.md）
- 调试细节 [官方]：MCP Inspector 配置「`Header Name` 为 `Authorization` 不需要修改，在 `Bearer Token` 中填入 `HereIsToken`」（调试MCP服务 第 60 行）→ 网关消费者 API Key 以 `Authorization: Bearer <key>` 形态传递（见下方 Bearer 前缀存疑项）
- 火山侧同构事实 [官方-竞品]：「HTTP 转换为 MCP 时，仅支持通过 Streamable HTTP 协议访问网关」→ 详见 competitor-cloud.md「火山引擎 API 网关/AI 网关对标」

##### 引用限定（🔴 防污染，2026-09-21 收口核实）

- **ATA 11020742807**（骁霆/王炳松 2026-08-09《基于阿里云 AI 网关的万镜一刻 API 接入方案》§5.5）的五句结论——「生效优先级由路由级向下递减：MCP/路由级 → Model API 级 → Agent API 级 → 域名级 → 实例级」「实例级规则是兜底规则，实测在自定义 HTTP 类型 Model API 链路上可能不触发」「Model API 级规则在当前控制台版本下，自定义 HTTP 类型 API 不出现在可选列表中」「域名必须精确填写，不能使用通配符 `*`」「规则页必须显示『当前生效状态：已生效』」——已逐字复核**全部准确**，**但必须带限定引用**：这些是「**域名级自定义 WASM 插件**绑定在**自定义 HTTP 类型 Model API 链路**」上的实测，**不是 MCP 链路**；该文 `MCP` 仅出现 1 次（就在优先级链那串里），`ext-auth`/`外部认证`/`tools/list`/`initialize`/`tools/call`/`消费者` 均 0 命中 → **不能作为 MCP 鉴权证据引用**；「实例级不触发」**不可外推到 MCP 场景**（摘录+限定已归档 raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md）
- 「实例级」语义存在张力：官方称实例级是「当路由和域名级规则都没有匹配到的时候则匹配该规则」的兜底；ATA 实测称其在自定义 HTTP 类型 Model API 链路上可能不触发 → **实操建议：优先用域名级，不要依赖实例级**（已列入避坑）
- **ATA 11020591207**（鹤渡/章丹鹰）「AI 网关（aigw）：云原生 API 网关面向 AI 场景的专属版本，定位是 AI 应用与模型服务之间的核心连接层」引文准确，但该文**无插件生效维度内容**（`生效` 0 命中），主题是配置与底层资源的「引用悬空」一致性校验 → **不是生效维度的出处**
- **ATA 11020729615** 筱奥《MCP Server 与 Client 之间的鉴权：从协议到工程落地》（2026-07-30）讲的是**内部 Aone MCP 网关（Normandy），不是阿里云 AI 网关**，只能当模式参考（「网关在收到 MCP Client 的连接请求时，会校验请求中携带的身份凭证…凭证无效或缺失则直接返回 401 Unauthorized」= 连接即鉴权，覆盖 initialize/tools/list）→ **引用时必须写清「非阿里云产品」限定，否则污染知识库**

#### ext-auth `forward_auth` 模式源码级细节（2026-09-21 收口补充）[开源]

> 出处：alibaba/higress main 分支 `plugins/wasm-go/extensions/ext-auth/main.go` + `config/config.go` 关键片段（摘录归档 raw/misc/misc-2026-09-21-higress-ext-auth-source-excerpts.md，⚠️ 摘录而非全文）。这是「**不改客户认证接口**」解法的源码级依据，也是本次收口最重要的可复用知识。

**1. 路径拼接只发生在 envoy 模式**：

```go
requestMethod := httpServiceConfig.RequestMethod
requestPath := httpServiceConfig.Path
if httpServiceConfig.EndpointMode == config.EndpointModeEnvoy {
    requestMethod = ctx.Method()
    requestPath = path.Join(httpServiceConfig.PathPrefix, ctx.Path())
}
```

→ forward_auth 用固定 `path` 原样发出鉴权请求；原始路径通过 `X-Forwarded-Uri`（**含 query**）传递。自动附加头共 **6 个**：`x-forwarded-proto/method/host/uri` + 兼容用的 `x-original-method/uri`（源码注释「Compatible with older versions」→ 说明 `X-Forwarded-*` 是较新能力）。

**2. `Authorization` 头无条件透传**（源码位置在 `endpoint_mode` 分支**之外**、也在 `allowed_headers` 循环**之外**）：

```go
// Add the Authorization header if present
authorization := util.ExtractFromHeader(reqHeaders, HeaderAuthorization)
if authorization != "" { extAuthReqHeaders.Set(HeaderAuthorization, authorization) }
```

→ 只要原始请求带 Authorization 就透传，与 endpoint_mode 和 allowed_headers 均无关。**推论：客户自有 PAT 校验逻辑一行不用改。**

**3. 🔴 `with_request_body` 与 GET 冲突会导致插件加载失败**（config/config.go）：

```go
if withRequestBody.Bool() && (httpService.RequestMethod == http.MethodGet || ...Options || ...Head) {
    return errors.New(fmt.Sprintf("requestMethod %s does not support with_request_body set to true", httpService.RequestMethod))
}
```

且 forward_auth 下 `request_method` 缺省即 GET；envoy 模式 `RequestMethod` 为空串 → **该校验只在 forward_auth 触发**。配错则配置解析失败、**插件整体不生效**（维护者口径：「只要有一个插件的配置加载异常，两个插件的配置都不会正常生效」）。

**4. `match_list` 路径匹配用不含 query 的 path**（`wrapper.GetRequestPathWithoutQuery()`）；不配 `match_type`/`match_list` → 默认白名单模式且名单为空 → **所有请求都鉴权**。

**5. 🔴 `match_type`/`match_list` 必须与 `http_service` 同级**（维护者 hanxiantao 原话：「`match_type` 、 `match_list` 和 `http_service` 是一个层级的。」discussions/2142），嵌进 `http_service` 里会**静默失效**。

**6. 默认 fail-closed 细节**：`status_on_error` 默认 403；`failure_mode_allow` **只对 ≥500 生效**（`if statusCode >= http.StatusInternalServerError && config.FailureModeAllow`）；授权服务返 4xx 时按**原状态码**拒绝（不走 status_on_error、不受 failure_mode_allow 影响）；连接失败(err≠nil)被当作 500 处理，**故超时会放行**（源码注释「Since the handling logic for call errors and HTTP status code 500 is the same, we directly use 500 here.」）。

**7. 🔴 填 IP/裸域名报 `bad argument`**：`failed to call ext auth server: error status returned by host: bad argument`（真实案例 discussions/3991，`service_name: "10.24.11.27"`）。维护者 CH3CHO FAQ：「`bad argument` 错误在绝大部分场景下都是由于配置了网关并不知晓的服务信息。Wasm 插件只能请求网关拿到的 Cluster 信息…而不能直接指定目标服务的地址和端口来请求。」

**8. K8s Service 默认只下发绑了路由的**（FAQ：「针对 K8s 内的 Service，Higress 默认只会下发关联了路由的 K8s 服务」）→ 认证服务没绑任何路由时网关拿不到 cluster。解法：造一条永不匹配的路由，或改用 DNS 服务来源。别用 `127.0.0.1`（指向网关自身）；连通性排查用 `telnet`/`nc` 不用 `ping`。

#### 产品缺口 / 可提产研的需求（2026-09-21 收口补充）

- [推断] **自建鉴权缺「固定路径鉴权」语义**：Higress 开源 ext-auth 早有 `forward_auth` 模式（固定 path + 可配 method），但阿里云「自建认证鉴权」控制台只暴露了前缀拼接语义（等价于 envoy 模式）→ **需求建议**：控制台增加「鉴权路径匹配模式」选项（前缀拼接 / 精确固定路径），或在插件配置里显式暴露 `endpoint_mode: forward_auth`。**这不是架构改造，是把自家开源已有能力透出到控制台。**
- [官方未说明] ext-auth 是否在阿里云插件市场在架：三条产品线官方文档 0 命中，官方认证插件清单只有 6 个不含 ext-auth，目前只有客户与售后的对话作证 → 以控制台实况为准
- [存疑] 商业版 ext-auth 是否支持 forward_auth：本卡证据读自开源 main 分支；`x-original-*` 头带「Compatible with older versions」注释说明 `X-Forwarded-*` 是较新能力；最新公开引擎版本 2.1.23（2026-09-03）→ **上线前必须在客户实例实测**
- [存疑] ext-auth 走 HTTPS/TLS 到 443 是否可行：官方仅说自定义 Wasm 出站「目前仅支持 http 调用」，ext-auth 用同一 wrapper client，TLS 未验证
- 🔴 [存疑·**最可能导致落地失败的细节**] **Authorization 格式风险**：客户接口可能期望裸 `Authorization: <PAT>`，而 MCP 标准认证走 `Bearer <token>`（官方 debug 文档的 MCP Inspector 就是用 `Bearer Token` 字段），客户端很可能自动加 `Bearer ` 前缀 → 必须提前确认客户 verify 接口是否容忍 Bearer 前缀

#### 避坑

- 🔴 **插件仅专享实例型 AI 网关支持，Serverless 版装不了插件**（官方原文：「仅专享实例型AI网关支持安装与启用插件，Serverless版不支持」）→ 客户用 Serverless 时必须走 A 路（A 路在 Serverless 上是否可用官方未说明，需实测/工单确认）
- 🔴 **超时单位陷阱**：A 路「超时时间」单位**秒**（默认 10）；B 路 `timeout` 单位**毫秒**（默认 1000）。数值同为 10/1000 但单位差 1000 倍——把 B 路的 1000 当秒填进 A 路≈16 分钟挂住，把 A 路的 10 当毫秒填进 B 路=10ms 瞬间超时
- 🔴 **鉴权路径拼接语义**：A 路「鉴权API」是**前缀**，真实鉴权 Path = 鉴权API + 原始业务 Path（`/validateToken` + `/order` = `/validateToken/order`）；B 路 envoy 模式同理用 `path_prefix` 拼接。认证接口若是固定路径，必须 B 路 `forward_auth` 模式配 `path`
- 🔴 **service_name 不是裸域名**：B 路必须填带服务类型后缀的完整 FQDN（`xxx.dns` / `xxx.static` / `xxx.<组>.<命名空间>.nacos` / `xxx.<ns>.svc.cluster.local`），且该服务必须先在网关「服务」里注册
- `.static` 服务端口口径存疑：官方只有代码注释「静态IP类型服务的逻辑端口是80」，实际监听 8080 时怎么填**官方未说明** → 优先 DNS 域名来源规避 [存疑]
- A 路鉴权服务**仅支持 HTTP 协议**，不支持 Dubbo；多端口 K8s Service **默认取第一个端口**，要用其他端口需另建只含目标端口的 Service
- 鉴权结果判定：200 放行、401/403 直接回客户端；认证服务必须统一返 200 时用 `x-mse-external-authz-check-result` 头（true 放行/false 拒绝）
- A 路创建后**忘记点「开启」不生效**；删除必须先关闭
- B 路 `max_request_body_bytes`（默认 10MB）超限直接返 **413 且不启动授权**，优先级高于 `failure_mode_allow`——大 Body 上传接口要么调大要么别开 `with_request_body`
- A 路宽松模式=鉴权服务挂了**放行**（官方建议但安全风险自负）；严格模式=挂了**拒绝**。B 路对应 `failure_mode_allow`（默认 false=拒绝）
- 外网认证服务地址需配 NAT 网关，否则网关出不去
- ACK 来源必须与网关同 VPC（跨 VPC 要重建网关实例），集群 ≥1.18（建议 1.28+），安全组放行
- 🔴 **优先用域名级，不要依赖实例级兜底**：官方称实例级是「当路由和域名级规则都没有匹配到的时候则匹配该规则」的兜底，但 ATA 11020742807 实测（**限定于自定义 HTTP 类型 Model API 链路，非 MCP，不可外推**）称实例级规则可能不触发 → 需要全局覆盖时优先配域名级规则，并在规则页确认「当前生效状态：已生效」（详见上方「引用限定」）
- 🔴 B 路 forward_auth 配 `with_request_body: true` 而 `request_method` 缺省（GET）→ 配置解析直接报错、**插件整体不生效**；`match_type`/`match_list` 嵌进 `http_service` 里会**静默失效**（必须同级）——两条详见上方「forward_auth 源码级细节」
- 🔴 消费者 API Key 经 `Authorization: Bearer <key>` 传递（官方 MCP Inspector 调试口径），若客户自有 verify 接口期望裸 PAT，**Bearer 前缀是否容忍必须提前确认** [存疑]（见「产品缺口」节）

#### 报价量级（中国内地，官方价，页面更新 2026-06-18 / 2026-07-29，2026-09-21 归档）

**云原生API网关专享实例（apigw 规格）** [官方]：计费项 = 网关实例费 + 数据处理费 + 公网流量费（CDT 统一出账）；按量付费（小时，不足 1 小时按 1 小时）或包年包月（**首购 6 折**）；网关内置 SLB 无需另购。

| 实例规格 | 按量（元/小时） | 包月（元/月） |
| --- | --- | --- |
| apigw.dev.x1 | 0.826 | 416 |
| apigw.small.x1 | 1.935 | 975 |
| apigw.small.x2 | 3.702 | 1,866 |
| apigw.small.x4 | 7.007 | 3,531 |
| apigw.medium.x1 | 14.025 | 7,069 |
| apigw.medium.x2 | 27.621 | 13,921 |
| apigw.medium.x3 | 41.216 | 20,773 |
| apigw.large.x1 | 54.812 | 27,625 |
| apigw.large.x2 | 109.193 | 55,033 |
| apigw.large.x3 | 163.575 | 82,442 |
| apigw.large.x4 | 217.956 | 109,850 |

其他地域相对中国内地的倍率（按 dev.x1/small.x1 锚点核算，全规格一致）[官方+推断(倍率为本卡计算)]：金融云 ≈1.90x、中国香港/东京 ≈1.50x、新加坡/雅加达/法兰克福 ≈1.38x、美国（弗吉尼亚/硅谷）≈1.20x。

**AI 网关专享实例（aigw 规格，中国内地）** [官方]：

| 实例规格 | 按量（元/小时） | 包月（元/月） |
| --- | --- | --- |
| aigw.small.x1 | 7.9335 | 3,997.5 |
| aigw.small.x2 | 15.1782 | 7,650.6 |
| aigw.small.x4 | 28.7287 | 14,477.1 |
| aigw.medium.x1 | 56.1 | 28,276 |
| aigw.medium.x2 | 110.484 | 55,684 |
| aigw.medium.x3 | 164.864 | 83,092 |
| aigw.large.x1 | 213.7668 | 107,737.5 |
| aigw.large.x2 | 425.8527 | 214,628.7 |
| aigw.large.x3 | 637.9425 | 321,523.8 |

（金融云/港日/新加坡雅加达法兰克福/美国地域价目表见 raw 归档 aigw-billing-dedicated-instance.md，倍率与 apigw 相同。）

**数据处理量费用**（两产品同价）[官方]：公共云公网 **0.037 元/GB/小时**、私网 **0.049 元/GB/小时**；金融云公网 0.07、私网 0.093。数据处理量=请求+响应数据量之和，按小时结算。公网流量另走 CDT 计费。

**AI Credits** [官方]（2026-09-21 收口补归档：raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md）：AI 增强能力的按量计费单位，**0.01 元/Credit**；**仅智能路由等 AI 增强能力消耗 Credits，普通 LLM API 代理透传和自定义模型服务调用不消耗**；需先创建 AI 网关实例再单独开通，**开通后不支持退订**，未使用时不产生费用。

**Serverless** [官方]（2026-09-21 收口补归档：raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md + aliyun-docs-2026-09-21-aigw-commercialization-announcement.md）：新版公测 **2026-08-31 结束，9 月 1 日起商业化计费**（存量实例自动转商业化，无需迁移；不用的实例 9-1 前删除避免费用）。旧版 Serverless CU 计费：**Model API / MCP Server / Agent API 的 CU 系数分别为 10 / 5 / 2**，中国内地单价 **0.005 元/千CU**，**最小计费粒度 1000 CU、不足 10 万按 10 万计**（每小时结算请求 CU 费 + 公网流量费）；新客户建议选新版 Serverless 标准版或企业版。

**对位竞品**：AWS API Gateway / Azure APIM / Kong Enterprise / GCP Apigee；AI 网关形态对位 AWS Bedrock Gateway、Cloudflare AI Gateway；开源内核即 Higress（可自建平替但失去托管 SLA）

**典型选型场景**：微服务统一入口（替代 Nginx Ingress/Kong）、K8s Ingress 三合一、SaaS 多租户 API 管理 + 自建认证统一鉴权（→ cloud-solutions.md S11）、AI 应用统一入口（多模型路由/Token 限流/语义缓存/AI 护栏）、MCP Server 托管与 HTTP to MCP、对外开放 API + 消费者认证

**官方文档**（本次 16 篇归档的 source_url，raw/aliyun-docs/aliyun-docs-2026-09-21-*）：
- 配置自建认证鉴权（A 路）：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/configure-self-built-authentication （apig，页面更新 2026-09-20）；https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-self-built-authentication （aigw，2026-06-02）
- 全局认证鉴权类型（JWT/OIDC/自建）：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/global-authentication-1
- Go 语言开发网关插件（FQDN 命名规则出处）：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/develop-plug-ins-in-go ；https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/develop-gateway-plug-ins-using-the-go-language
- Higress ext-auth 插件 README（B 路 schema）：https://raw.githubusercontent.com/alibaba/higress/main/plugins/wasm-go/extensions/ext-auth/README.md （渲染页 https://higress.ai/docs/latest/plugins/authentication/ext-auth/ ）[开源]
- 创建服务：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service ；https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-services
- 服务来源管理：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service-source
- 插件安装启用卸载：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/enable-plugin ；https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-plug-ins
- 认证鉴权插件清单（三线均无 ext-auth）：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/authentication ；https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/authentication ；https://help.aliyun.com/zh/mse/user-guide/authentication-authentication
- 计费：https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/billing-overview ；https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/free-product-templates
- 谱系/计费补充（2026-09-21 收口已补归档 raw）：llms.txt 全文 → raw/aliyun-docs/aliyun-docs-2026-09-21-apig-llms-index.md ；AI Credits https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/ai-credits-billing-details → raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md ；Serverless 旧版计费 https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/serverless-old-billing-details → raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md ；Serverless 商业化公告 https://help.aliyun.com/zh/api-gateway/ai-gateway-commercialization-announcement → raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-commercialization-announcement.md
- MCP 维度（2026-09-21 收口补充归档）：调试MCP服务 https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/debug-mcp-services ；消费者认证 https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-certification ；HTTP转MCP字段配置 https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/http-to-mcp-field-configurations ；新功能发布记录 https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/new-feature-release-notes-ai-gateway ；引擎版本说明 https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/engine-version-description （均归档 raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-*.md）
- MCP 官方规范 [规范]：https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization （另归档 2025-11-25 版 authorization 与 2026-07-28 版 transports/streamable-http，raw/standards/standards-2026-09-21-*）
- Higress ext-auth 源码 [开源]：https://github.com/alibaba/higress/tree/main/plugins/wasm-go/extensions/ext-auth （main.go/config.go 关键片段摘录归档 raw/misc/misc-2026-09-21-higress-ext-auth-source-excerpts.md）
- ATA 实操/实测（SSO 限制，归档为摘录）：11020495607 陈思亮(玄斧)《AI网关-Restful API转换MCP的桥梁》→ raw/ata/ata-2026-09-21-http-to-mcp-consumer-auth-excerpts.md ；11020742807 骁霆/王炳松《基于阿里云 AI 网关的万镜一刻 API 接入方案》§5.5 → raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md （含 🔴 引用限定）

**证据等级**：[官方]（help.aliyun.com 归档原文，2026-09-21 已全量补归档）/ [规范]（MCP 官方规范 raw/standards/）/ [开源]（Higress ext-auth README + main.go/config.go 源码摘录）/ [实战]（ATA 摘录）/ [官方-竞品]（火山引擎，见 competitor-cloud.md）/ [推断]（已逐条标注：EOL 日期对比、.static 端口存疑、两产品线 A 路一致性、地域倍率计算、MCP 方法不可区分推论、双层组合方案）/ [存疑]（商业版 forward_auth、HTTPS/TLS 443、Bearer 前缀容忍度——均需客户实例实测）
**最近更新**：2026-09-21（收口补充：MCP 鉴权维度 + 三种鉴权能力对照 + forward_auth 源码级细节 + 产品缺口 + 引用限定修正；原 16+9 篇文档深度蒸馏，外部认证专项 + 三形态谱系消歧）

---

### API Gateway（原 API 网关 / 传统版 / apigateway）

> ⚠️ **EOL 警示 [官方]**：本卡为「**原 API 网关（传统版 / apigateway）**」，是 API 网关三种形态中的传统形态（另两种为云原生 API 网关、AI 网关）。官方公告：**2026-08-23 停止新购（截至 2026-09-21 已过）、2027-09-21 全面下线，存量实例请迁移至云原生 API 网关**（help.aliyun.com/zh/api-gateway/llms.txt，2026-09-21 复核）。**新项目勿选本卡产品 → 见 [云原生 API 网关（APIG）/ AI 网关 深度卡](#云原生-api-网关apig--ai-网关深度卡)**。以下内容对存量客户仍然有效，保留不删。

**官方定位**：API 全生命周期管理（发布/管理/认证/限流/计费）的网关 PaaS。
**能做**：HTTP/HTTPS/WebSocket、签名/JWT/AppCode 鉴权、按分钟限流、参数映射、协议转换（HTTP→HSF/Dubbo）、API 市场售卖、灰度发布、监控告警
**不擅长**：服务治理深度场景（→ MSE 云原生网关）；超低延迟内部网关（→ ALB + 自建鉴权）

**典型选型场景**：对外开放 API、SaaS 多租户 API 管理、内部微服务 API 统一入口、API 经济变现、Open API 平台（⚠️ 均为存量场景；新项目 → 云原生 API 网关/AI 网关）
**对位竞品**：AWS API Gateway / Azure APIM / Kong Enterprise / 腾讯云 API 网关
**报价量级**：共享版 ¥0.06/万次调用 + ¥0.8/GB 流量；专享版按实例规格 ¥0.5/h 起
**官方文档**：https://help.aliyun.com/zh/api-gateway/
**证据等级**：[官方]
**最近更新**：2026-09-21（加 EOL 警示与三形态消歧交叉引用；既有内容保留，原蒸馏 2026-06-18）

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

### 云数据库 ClickHouse（企业版 Enterprise + 社区兼容版 Community Compatible）

**官方定位**：阿里云托管的 ClickHouse 服务，面向 PB 级实时 OLAP 分析。产品由**两条完全不同的产品线**组成，架构/计费/购买路径/存储单价均不同，**报价前必须先分清用哪一条**。

> **⚠️ SA 高压线（2026-08-05 海底捞项目实战踩坑）**：ClickHouse 报价的最大坑，是把两条产品线混为一谈——只看计费文档拿到"企业版 0.49987 元/CCU·时"这样漂亮的单价，实际打开购买页却发现**企业版根本没有"选规格"的按钮**，只能按用量出账 + 预购资源包抵扣。客户 IT 采购流程若要求"预算可锁定/金额可申请"，Serverless 按量模式走不通。**报价前必做**：走一遍 buy.aliyun.com 实际购买路径确认能选到对应规格，再拉计费文档核对单价。

#### 两条产品线速查

| 维度 | **企业版**（Enterprise / Serverless） | **社区兼容版**（Community Compatible） |
|------|--------------------------------------|--------------------------------------|
| **架构** | 存算分离，计算 CCU + OSS 持久存储 | 存算一体，ClickHouse 节点 + ESSD 云盘（PL1/PL2/PL3） |
| **计费模式** | **仅按量**（Serverless），0.49987 元/CCU·时（1 CCU = 1 核 4GB） | **包月 + 按量**均有 |
| **规格购买页** | **无具体规格购买按钮**，开通后按用量出账；可预购计算/存储资源包（-51%/-49% 抵扣） | 32 核 128GB × N 节点 + PL1/PL2/PL3 云盘，支持 1-24 节点（双副本）或 1-48 节点（单副本） |
| **CCU 底层规格** | 抽象 CCU 池，用户不感知物理节点 | 显式节点规格（8/16/32/64/104 核等） |
| **典型适用** | 弹性尖峰、开发测试、内部试点、Serverless 首选 | **客户 IT 采购流程可锁定预算**、存算一体对齐现状（如客户已有 PolarDB 云盘）、生产主推 |

#### 购买页 4 个 Tab 全景（避坑关键 — 2026-08-05[实战]）

阿里云 ClickHouse 购买页共 4 个 tab，**企业版没有"选规格"的独立 tab**：

1. **社区兼容版 · 包年包月**（commodityCode=`clickhouse_pre_public_cn`）— 可选节点规格、副本数、云盘类型/容量
2. **企业版 & 社区兼容版 · 按量付费**（commodityCode=`clickhouse_go_public_cn`）— **企业版在此 tab 下没有具体规格按钮**，只是入口性质；社区兼容版按量可在此 tab 选规格
3. **企业版计算资源包**（仅买抵扣券，预付 -49%~-51%）
4. **企业版存储资源包**（仅买抵扣券，OSS 存储部分）

#### 计费单价明细

**企业版（Enterprise / Serverless）**：
- 计算：0.49987 元/CCU·时（1 CCU = 1 核 4GB）→ 32 核 128GB × 720h ≈ ¥11,517/月
- OSS 存储按量：0.00033 元/GB·时 × 720 ≈ 0.2376 元/GB·月
- OSS 存储包（预付 -49%）：**0.12 元/GB·月** → 1.8TB ≈ ¥216/月
- 企业版也有 ESSD_L1 计算实例：0.0021 元/GB·时 × 720 ≈ 1.512 元/GB·月（单副本），多可用区 0.002625×720 ≈ **1.89 元/GB·月**

**社区兼容版（Community Compatible）**：
- 计算 32 核 128GB × 1 节点双副本（包月）：约 **¥10,810.80/月**
- 计算 32 核 128GB × 1 节点（按量）：22.482 元/时 × 720 ≈ ¥16,187/月
- ESSD PL1 云盘（**含双副本**）：**实测 2 元/GB·月** → 1.8TB ≈ ¥3,600/月（官方多 AZ 单副本 1.89 元/GB·月 + 双副本溢价推算[实战验证]）
- ESSD PL1 云盘（按量）：5.04 元/时 × 720 ≈ ¥3,629/月

#### 同规格 List 价横向对比（32 核 128GB × 1 节点双副本 + 1.8TB，北京多可用区，2026-08-05[实战]）

| 版本 & 计费 | 计算 | 存储 | **月合计（List）** | 采购可行性 |
|-------------|------|------|-------------------|-----------|
| 企业版按量（Serverless） | ¥11,517 | ¥216（OSS 存储包） | **¥11,733/月** | ❌ 最便宜但**客户采购流程走不通**（无金额可锁定） |
| 社区兼容版包月 | ¥10,810.80 | ¥3,600（PL1 含双副本） | **¥14,410.80/月** | ✅ **客户能采购**（规格明确、金额锁定） |
| 社区兼容版按量 | ¥16,187 | ¥3,629 | **¥19,816/月** | ⚠️ 最贵，仅用于短期弹性/POC |

#### SA 报价前必做的 4 条避坑规则（2026-08-05 实战总结[实战]）

1. **不能只看计费文档拿单价** — 必须走一遍 buy.aliyun.com 实际购买路径，确认能否选到对应规格；企业版报价前先问客户"你们采购流程能不能报按量？"
2. **关注购买页的"最低起步"约束** — CK 社区兼容版最低 1 节点；同类产品 Hologres 网关最低 2 个、ADB 企业版最低 3 节点，报价时先看 min 起步别报低了
3. **客户 IT 采购流程通常要求"预算可锁定"** — Serverless 按量不适合作为主推（采购申请填不了金额），推 Serverless 前先确认财务/采购部认不认可
4. **竞品/客户已有 PolarDB 云盘的情况** — 推 CK 优先选**社区兼容版包月**（存算一体、规格明确、可与客户现状对齐），而非企业版 Serverless；除非客户明确要 Serverless 弹性

#### 存储单价对照速记（企业版 vs 社区兼容版差异极大）

| 存储介质 | 单价（元/GB·月） | 备注 |
|---------|-----------------|------|
| 企业版 OSS 按量 | 0.2376 | 0.00033 元/GB·时 × 720 |
| 企业版 OSS 存储包 | **0.12** | 预付约 -49%，最便宜 |
| 企业版 ESSD_L1 单副本 | 1.512 | 0.0021 × 720 |
| 企业版 ESSD_L1 多可用区 | **1.89** | 0.002625 × 720 |
| 社区兼容版 PL1 云盘双副本 | **2.00** | 实测（1800GB → ¥3,600）[实战] |

**结论**：企业版 OSS 存储单价约为社区兼容版 PL1 云盘的 **1/17**，是企业版 Serverless 在纯存储成本上的核心优势；但企业版无法在购买页锁定规格价格，是采购流程的核心短板。

**能做**（两版共同能力）：ClickHouse 100% 兼容 SQL、宽表 OLAP、列存压缩、Materialized View、TTL 冷热分离、AutoMergeTree 系列引擎、Kafka Engine 实时导入、S3/OSS 联邦查询。
**不擅长**：高并发点查（→ Tair/Lindorm）、事务写入（→ RDS/PolarDB）、复杂 JOIN 星型分析（→ Hologres/StarRocks 更优）、超低延迟看板（→ StarRocks 主键表）。

**典型选型场景**：
- 日志/事件流大宽表分析（Kafka → CK）
- 用户行为分析、广告归因、埋点分析（PV/UV/漏斗）
- 时序指标存储与聚合（IoT/监控二次聚合）
- **对客户已有开源 ClickHouse 集群做 lift-and-shift 上云**（社区兼容版首选）

**对位竞品**：ClickHouse Cloud（原厂）/ ByteHouse（火山引擎，与 CK 血缘）/ 腾讯云 CDW ClickHouse / AWS 无原生 CK 托管（用户自建 on EC2/EKS） / 阿里云 EMR Serverless StarRocks（架构不同但场景高度重叠）

**与 EMR Serverless StarRocks 的选型分野**：
- 明细 OLAP + 超大宽表 + 已有 CK 生态 → **ClickHouse**（社区兼容版）
- 实时主键更新（Upsert/Partial Update）+ 高并发 BI 报表 + 数据湖联邦 → **StarRocks**
- 见 [aliyun-products.md 数据库选型速查表 / EMR Serverless StarRocks 卡]

**官方文档**：
- 产品主页：https://www.aliyun.com/product/clickhouse
- 计费说明：https://help.aliyun.com/zh/clickhouse/product-overview/billing-overview
- 购买页：https://common-buy.aliyun.com/?commodityCode=clickhouse_pre_public_cn

**采购路径核验字段（2026-08-05 新增，模式B 第 6 步硬门禁）**：

| 版本 | commodityCode / 购买页 URL | 规格页可用性 | 最低起步约束 ⚠️ | 采购流程兼容性 |
|------|---------------------------|-------------|----------------|--------------|
| **ClickHouse 企业版**（Enterprise / Serverless） | `clickhouse_go_public_cn`（按量入口 tab，**企业版在此 tab 下无具体规格按钮**）+ `clickhouse_computing_resource_package` / `clickhouse_storage_resource_package`（资源包 tab） | ❌ **无独立规格页** | 无规格约束，按 CCU 用量 | ❌ 采购流程通常走不通（无金额可锁定）；仅当客户接受按量或用预付资源包锁定金额时可推 |
| **ClickHouse 社区兼容版**（Community Compatible） | `clickhouse_pre_public_cn`（包月）+ `clickhouse_go_public_cn`（按量） | ✅ 有独立规格页（可选节点规格 8/16/32/64/104 核 + 副本数 + ESSD PL1/PL2/PL3 云盘） | 双副本模式 1-24 节点 / 单副本模式 1-48 节点 | ✅ 包月-可锁定预算（客户能采购）；按量-需专项审批 |

**⚠️ 报价避坑**（2026-08-05 海底捞项目实战[实战]）：ClickHouse 企业版计费文档明写"0.49987 元/CCU·时"这样漂亮的单价，实际打开购买页却发现**企业版根本没有"选规格"的按钮**，只能按用量出账 + 预购资源包抵扣。若客户 IT 采购流程要求"预算可锁定/金额可申请"，Serverless 按量模式走不通。修复：优先推荐**社区兼容版包月**（¥14,410.80/月，规格明确、金额锁定）；企业版仅作为"客户接受按量"时的备选，并同时报预付资源包锁定金额（-49%~-51% 抵扣）。

**证据等级**：[实战]（2026-08-05 海底捞项目实测购买路径 + List 价核对）+ [官方]（计费文档单价 + 购买页 commodityCode）
**最近更新**：2026-08-05（补齐采购路径核验字段与四字段模板对齐）

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
| 向量检索/RAG | 百炼知识库 / RDS PG+pgvector / 阿里云 ES / ADB-PG / Milvus 版 / Lindorm | 零运维 → 百炼知识库；≤50万向量 → RDS PG+pgvector；百万~千万 → ES/ADB-PG；亿级 → Milvus 版/Lindorm；**DashVector 仅按量不可降配，第一轮排除** |
| 文档解析 | 文档智能 DocMind | 电子版 → 基础链路 0.02 元/页；扫描件/图表密集 → 增强链路 0.04 元/页（须显式 `EnhancementMode=VLM`）|
| 视频 | VoD / Live / RTC / MPS | 点播 → VoD；直播 → Live；实时互动 → RTC；纯转码/AI → MPS |
| IoT | IoT Platform / Link IoT Edge | 设备接入 → IoT Platform；边缘计算 → Link IoT Edge |
| 中间件 | MSE / RocketMQ / Kafka / 云原生API网关(APIG) / AI网关 | 业务消息 → RocketMQ；流式 → Kafka；微服务注册治理 → MSE Nacos；API/微服务/Ingress 统一入口 → **云原生API网关**；AI 应用入口（多模型路由/Token限流/MCP）→ **AI网关**；~~API 管理 → API Gateway~~ **原API网关（传统版）已于 2026-08-23 停止新购、2027-09-21 全面下线，新项目勿选** → 见云原生API网关/AI网关深度卡 |
| 安全 | WAF / DDoS / 云安全中心 / RAM | 6 层纵深防御全覆盖 |
| 监控 | ARMS / SLS / CloudMonitor / OOS | APM → ARMS；日志 → SLS；基础 → CM；自动化运维 → OOS |

---

### ACK Pro vs ACS 底层原理辨析（2026-08-17 Query回写）

**结论**：K8s 上层语义一样，底层算力承载不一样。
- **相同（控制面/接口层）**：控制面均由阿里云托管；都兼容 K8s 原生 API/kubectl/Helm/RBAC/CSI；ACS 集群可直接显示在 ACK 控制台管理。
- **不同（数据面，本质差异）**：
  - ACK Pro = **节点模型**：先购 ECS/裸金属做 Worker 节点，Pod 调度到用户节点，节点运维归用户；计费 = 集群管理费 0.64 元/时 + 节点按规格时长。
  - ACS = **无节点 Serverless**：无容量/节点规划，只申请 Pod 由 ACS 自动匹配算力；**每个 Pod 底层用轻量级安全沙箱完全强隔离**（官方原文）；计费 = 集群管理免费 + Pod 按 vCPU/内存/GPU 秒级按量。
- **血缘**：ACS 是 ACK Serverless（原 ASK）的新一代升级，与 ECI 一脉相承。
- **判据**：要不要"自己管节点"是分水岭。DaemonSet/内核调优/自定义节点OS/节点亲和/稳态压成本 → ACK Pro；免节点运维/秒级弹性/按Pod付费/AI推理批处理突发 → ACS。
- 证据等级 [官方]，来源 help.aliyun.com/zh/cs/product-overview/product-introduction 与 /zh/cs/user-guide/acs-pod-instance-overview

### ACS 官方使用限制明细（大型应用迁移核对清单，2026-08-17 Query回写）

**机制根因**：ACS 通过虚拟节点对接 K8s，Pod 打散分布在整个阿里云资源池、无真实节点 → 节点级特性一律受限。
**K8s 应用限制表**（官方原文，校验失败处理策略）：
- DaemonSet：Pod 运行但无法正常工作 → 替代 Sidecar
- NodePort Service：**拒绝提交** → 替代 type=LoadBalancer
- hostNetwork/hostIPC/hostPID/HostUsers：强制改写为 false
- Privileged / allowPrivilegeEscalation：启动失败 → 用 capability/sysctl
- Linux capabilities：仅白名单 NET_RAW/NET_ADMIN/NET_BIND_SERVICE/CHOWN/DAC_OVERRIDE/FSETID/FOWNER/KILL/MKNOD/SETPCAP/SETFCAP/SYS_CHROOT/SYS_PTRACE/AUDIT_WRITE
- HostPath：限制挂载宿主机文件（仅 /etc/localtime readOnly 等例外）
- 确需放开可提工单，但按安全责任共担模型自担风险
**算力质量**：default 型=有算力扰动但无强制驱逐（对应 K8s QoS Guaranteed，交易核心用这个）；BestEffort 型=**存在强制抢占驱逐、提前 5 分钟事件通知**（仅离线批处理）。
**规格与计费细节**：最小 0.25vCPU/0.5GiB，0.5vCPU/1GiB 步长；16Gi 及以下内存开销 ACS 承担，>16Gi 开销分摊进 Pod（JVM 留余量）；系统盘 30G 内免费超出计费；Pod 每次启动远程拉镜像（ACR+VPC，镜像缓存优化冷启动）。
**交易系统迁移要点**：配额红线单地域按量 vCPU 默认 300 须提前扩；状态组件走 RDS/Tair/MQ 云产品不搬 ACS；SLA 单实例 99.9%/多 AZ 99.95% 需多 AZ 冗余补 99.99；稳态大规模常驻成本高于 ACK 包年，节省计划（按天承诺）可缓解；推荐无状态先迁双跑灰度、核心链路最后切，峰谷比大走"ACK 基座+ACS 弹性"混合。
- 证据等级 [官方]，来源 help.aliyun.com/zh/cs/user-guide/acs-pod-instance-overview（2026-08-17 抓取）

### ACK Pro vs ACS 对客介绍框架：一个根因讲透（2026-08-17 Query回写）

**根因**：两者交付的不是同一层次的东西——ACK Pro 交付「机器」（真实 ECS 节点，控制面托管），ACS 交付「算力」（无节点，Pod 跑在共享资源池现拉的安全沙箱里，跑完即走）。
**所有"ACS 不行"都是根因的逻辑推论，不是功能阉割**：DaemonSet=「每台机器一个副本」没有机器无从谈起；hostPath/hostNetwork=没有宿主机；privileged/内核调优=沙箱多租户共享动内核即动邻居；峰值确定性=ACK 节点是买断的、ACS 算力是池子现取靠库存；不能 SSH=没有你的机器可登。
**对客定位一句话**：ACK Pro=帮你管好大脑（控制面），身体（节点）还是你的；ACS=连身体都不用管，只交 Pod 我出算力。
**类比**：ACK Pro=长租车位（固定、自由、自己保养）；ACS=代客泊车（只管交车取车，别要求停哪个位）。
**三判据**：①依赖宿主机（DaemonSet/内核/固定端口/主机 agent）→ 只能 ACK Pro；②负载形状：稳态常驻→ACK 包年便宜，脉冲潮汐跑完即走→ACS 按秒省；③有无节点运维团队。
**交易类负载结论**：核心稳态基座 ACK Pro（容量买断/确定性/成本可控）+ 弹性峰值与非核心无状态 ACS（秒弹/免运维），一个管确定性一个管弹性，非二选一。
- 证据等级 [官方]（产品形态/限制）+ [推断]（介绍框架与类比）

### SAE→ACS 迁移判据（2026-08-17 Query回写，坤启案例提炼）

**框架纠偏**：SAE→ACS 是 Serverless 换 Serverless，"免节点免运维"不是迁移理由（SAE 已给）。真正的理由=**SAE 无 K8s API 的封闭 PaaS，ACS=SAE 体验+标准 K8s 界面**（kubectl/YAML/GitOps/RRSA/CSI/Gateway API）。对客口径："拿回工程自由度与开源生态，不失去 Serverless 省心"。
**适用画像**：工程能力强、偏好开源标准、反感封闭治理、有多云就绪诉求、有 Agent/沙箱类负载（每任务一沙箱秒级起停 SAE 给不了）。反之运维人力不足、要内置治理开箱即用的中小团队留 SAE。
**可行性三支撑**：①SAE 底层即 K8s，环境变量/探针/弹性(底层 HPA)/SLB/域名路由一一映射，镜像部署应用镜像直接复用（JAR/WAR/代码包须重新镜像化，SAE 托管镜像不可外带）；②SAE-ACK 双跑 bp.364（MSE 打通东西向）官方灰度载体，回退=流量切回 SAE 热备；③坤启测试环境已迁 ACS 实证。
**三边界**：①目标架构分工=ACK Pro 稳态基座+ACS 弹性/突发/Agent+ACK One 统一交付，非全量 ACS；②FC 必须一起决策（坤启 FC ¥6.0 万≈SAE ¥5.8 万），常驻/长连接负载归拢容器层，纯事件驱动留 FC，避免双份计费；③SAE 内置能力替代清单：灰度→Argo Rollouts、治理→MSE、监控→ARMS。
**成本口径**：勿承诺迁移降本——SAE 费用转移为 ACK 节点包月+ACS 秒级，收益在削峰与利用率；降本杠杆另算（坤启=ADB Supabase/云市场模型/CDT）。
- 证据等级 [官方]（映射/双跑/底层 K8s）+ [实战]（坤启案例）+ [推断]（判据框架）
