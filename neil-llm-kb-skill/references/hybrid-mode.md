# Hybrid Mode — 代码+文档混合知识化 SOP

## 适用条件

- 项目同时存在 manifest 文件（代码）和独立文档文件
- Init 阶段 `PROJECT_TYPE` 判定为 `Hybrid`
- 典型场景：
  - 有 `docs/` 目录的代码库
  - 附带设计文档/RFC 的工程项目
  - 包含 README 族 + 源代码 的开源项目
  - 代码库 + 运维文档 + 用户手册 的企业项目

---

## 核心策略：双轨蒸馏

Hybrid Mode 不是简单地"两个模式都跑一遍"，而是**按内容性质分流到最适合的蒸馏管道**，并在 wiki 层面实现**统一交叉引用**。

```
源文件
  │
  ├─ 代码文件（.ts/.java/.go/...）→ Codebase Pipeline
  │   └─ 产出：模块概览 / ADR / 数据流 / 配置地图 / 依赖图谱
  │
  ├─ 文档文件（.md/.pdf/.docx）→ Document Pipeline
  │   └─ 产出：领域综述 / 实体页 / 对比分析 / 指南 / 时间线
  │
  └─ 两者在 wiki/ 层统一交叉引用
      └─ [[module-name]] ↔ [[concept-name]] ↔ [[guide-name]]
```

---

## 分流规则

### 自动分流（默认）

| 文件类型 | 分流目标 | 依据 |
|---------|---------|------|
| `src/**`, `lib/**`, `cmd/**`, `pkg/**` | Codebase Pipeline | 源代码目录 |
| `test/**`, `tests/**`, `spec/**` | Codebase Pipeline | 测试代码 |
| `docs/**`, `documentation/**` | Document Pipeline | 文档目录 |
| `*.md`（项目根目录） | Document Pipeline | README/CONTRIBUTING/CHANGELOG |
| `config/**`, `.env*` | Codebase Pipeline（配置地图） | 配置文件 |
| `scripts/**` | Codebase Pipeline | 运维脚本 |
| `design/**`, `rfc/**`, `adr/**` | Document Pipeline | 设计决策文档 |

### 歧义处理

当文件归属不明确时：

| 歧义场景 | 处理方式 |
|---------|---------|
| `src/docs/` 内的 markdown | 代码内文档 → Codebase Pipeline（作为模块文档） |
| 代码中的超长注释块 | 保留在 Codebase Pipeline，不单独拆出 |
| Jupyter Notebook (`.ipynb`) | 代码+文档混合 → 按 cell 类型分流 |
| API 文档（OpenAPI/Swagger） | Codebase Pipeline → 生成 API 表面文章 |
| 架构决策记录（项目内 ADR） | Document Pipeline → 但关联到 Codebase ADR 页面 |

---

## 统一 Wiki 结构

Hybrid Mode 的 wiki 目录在标准结构基础上增加明确分区：

```
kb/
├── raw/                         # 统一的 raw 层
│   ├── code/                    # 代码相关源（可选细分）
│   └── docs/                    # 文档相关源
├── wiki/
│   ├── index.md                 # 统一索引（分区标注来源管道）
│   ├── inbox.md
│   ├── log.md
│   ├── entities/                # 统一实体目录
│   │   ├── module-auth.md       # ← 来自 Codebase Pipeline
│   │   ├── module-payment.md    # ← 来自 Codebase Pipeline
│   │   ├── redis.md             # ← 来自 Document Pipeline
│   │   └── kubernetes.md        # ← 来自 Document Pipeline
│   ├── concepts/                # 统一概念目录
│   │   ├── auth-adr.md          # ← Codebase: 架构决策
│   │   ├── auth-dataflow.md     # ← Codebase: 数据流
│   │   ├── microservice.md      # ← Document: 领域综述
│   │   └── twelve-factor.md     # ← Document: 概念页
│   ├── guides/                  # 统一指南目录
│   │   ├── auth-config.md       # ← Codebase: 配置地图
│   │   ├── deploy-guide.md      # ← Document: 操作指南
│   │   └── local-setup.md       # ← Document: 操作指南
│   └── comparisons/             # 统一对比目录
│       ├── auth-dependencies.md # ← Codebase: 依赖图谱
│       └── redis-vs-memcached.md # ← Document: 对比分析
└── references/
```

### index.md 分区格式

```markdown
# Wiki 索引

## Entities（实体）

### 代码模块
- [[module-auth]] — 认证授权模块
- [[module-payment]] — 支付处理模块

### 技术组件
- [[redis]] — 缓存与会话管理
- [[kubernetes]] — 容器编排平台

## Concepts（概念）

### 架构决策
- [[auth-adr]] — 认证模块架构决策记录
- [[auth-dataflow]] — 认证流程数据流图

### 技术概念
- [[microservice]] — 微服务架构综述
- [[twelve-factor]] — 十二要素应用方法论

## Guides（指南）

### 配置运维
- [[auth-config]] — 认证模块配置地图
- [[local-setup]] — 本地开发环境搭建

### 操作流程
- [[deploy-guide]] — 生产部署指南

## Comparisons（对比）
- [[auth-dependencies]] — 认证模块依赖图谱
- [[redis-vs-memcached]] — 缓存方案对比
```

---

## 交叉引用规则（Hybrid 特殊规则）

### 强制交叉引用场景

| 场景 | 要求 |
|------|------|
| 代码模块提到某技术 | 模块页面必须引用对应技术实体页 |
| 文档描述某模块行为 | 文档页面必须引用对应代码模块页 |
| ADR 引用外部框架 | ADR 必须引用框架实体页 |
| 配置地图引用外部服务 | 配置页必须引用服务实体页 |
| 部署指南涉及代码模块 | 指南必须引用模块概览页 |

### 引用方向约定

```
代码模块概览 ──引用──→ 使用的技术实体
技术实体页 ──反向引用──→ 使用它的代码模块
部署指南 ──引用──→ 涉及的模块 + 使用的技术
架构决策 ──引用──→ 相关概念 + 影响的模块
```

### frontmatter 标注

Hybrid Mode 页面的 frontmatter 增加 `pipeline` 字段：

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
pipeline: codebase | document | hybrid
module: <module-name>  # 仅 codebase pipeline 页面
domain: <domain-name>  # 仅 document pipeline 页面
evidence: primary | derived | inferred
sources: [raw/...]
---
```

---

## Ingest 流程（Hybrid 特化）

### Step 1: 分流判定

收到新源文件时，先判定分流目标：

```
新源文件
  │
  ├─ 文件路径匹配代码目录？ → Codebase Pipeline
  ├─ 文件路径匹配文档目录？ → Document Pipeline
  ├─ 文件是 manifest/config？ → Codebase Pipeline
  ├─ 文件是纯文本/PDF/DOCX？ → Document Pipeline
  └─ 无法判定？ → 读取前 200 字推断 → 标注 [inferred]
```

### Step 2: 按对应 Pipeline 执行蒸馏

- Codebase 文件 → 按 codebase-mode.md 规则生成 5 类代码文章
- Document 文件 → 按 document-mode.md 规则生成 5 类文档文章

### Step 3: 建立跨管道引用（Hybrid 独有）

蒸馏完成后，扫描新页面：

1. 提取页面中提到的技术名词/模块名
2. 检查另一管道是否已有对应页面
3. 若有 → 双向添加 [[wikilink]]
4. 若无 → 记录为"潜在连接点"（lint 时处理）

### Step 4: 统一更新 index.md

在对应分区和子分区中添加新条目。

---

## Lint 扩展（Hybrid 特殊检查）

在标准 6 维检查基础上，增加 Hybrid Mode 专属检查：

### 维度 7: 跨管道引用缺失 → P1

**检查内容**：代码模块页面未引用它使用的技术实体，或反之。

**检测方法**：
1. 读取所有 `pipeline: codebase` 页面，提取提到的技术名词
2. 检查对应 `pipeline: document` 的实体页面是否存在
3. 若存在但未 [[引用]] → 报告缺失

**输出**：
```
⚠️ P1 跨管道引用缺失
- wiki/entities/module-auth.md 提到 "Redis" 但未引用 [[redis]]
  → 建议：添加 [[redis]] 到交叉引用区
- wiki/entities/redis.md 未被任何代码模块页面引用
  → 建议：在使用 Redis 的模块页面添加引用
```

### 维度 8: 管道标注缺失 → P2

**检查内容**：页面 frontmatter 缺少 `pipeline` 字段。

---

## 与纯模式的关键差异

| 维度 | Codebase Mode | Document Mode | Hybrid Mode |
|------|--------------|---------------|-------------|
| 分流 | 不需要 | 不需要 | **必须做** |
| 目录结构 | 按代码模块 | 按文档主题 | 统一目录 + frontmatter 区分 |
| 交叉引用 | 模块间 | 文档间 | **跨管道 + 管道内** |
| Lint 额外检查 | 无 | 无 | 跨管道引用 + pipeline 标注 |
| index.md | 扁平 | 扁平 | **分层子分区** |
| Ingest 复杂度 | 中 | 中 | **高**（需分流 + 跨引用） |

---

## 示例：Spring Boot 项目 + 运维文档

```
project/
├── pom.xml                     → Codebase
├── src/main/java/...           → Codebase
├── src/test/java/...           → Codebase
├── docs/
│   ├── architecture.md         → Document
│   ├── deployment-guide.md     → Document
│   └── api-reference.md        → Document（但内容关联 Codebase API）
├── README.md                   → Document
└── docker-compose.yml          → Codebase（配置地图）
```

**Ingest 后 wiki 产出**：

| 来源 | Pipeline | 生成页面 |
|------|----------|---------|
| `src/main/java/auth/` | Codebase | `entities/module-auth.md` + `concepts/auth-adr.md` + `concepts/auth-dataflow.md` |
| `docker-compose.yml` | Codebase | `guides/module-auth-config.md`（合并到配置地图） |
| `docs/architecture.md` | Document | `concepts/system-architecture.md` |
| `docs/deployment-guide.md` | Document | `guides/production-deploy.md` |
| `docs/api-reference.md` | Document | `entities/api-surface.md`（与 Codebase API 表面交叉引用） |

**跨管道引用**：
- `entities/module-auth.md` ↔ `concepts/system-architecture.md`（架构文档描述了 auth 模块）
- `guides/production-deploy.md` ↔ `guides/module-auth-config.md`（部署需要配置）
- `entities/api-surface.md` ↔ `concepts/auth-dataflow.md`（API 文档对应数据流）
