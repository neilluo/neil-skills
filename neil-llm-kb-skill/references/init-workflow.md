# Init — 知识库初始化 SOP

## 前置条件

- 当前目录为待初始化的项目根目录
- 操作者具备目录读写权限
- 已确认该目录尚未初始化知识库（不存在 `kb/` 目录）

---

## 步骤

### Step 1: 检测项目类型

扫描根目录下的文件，判定项目类型：

| 检测条件 | 项目类型 |
|---------|---------|
| 存在 manifest 文件（`package.json` / `pom.xml` / `go.mod` / `Cargo.toml` / `pyproject.toml`） | **Codebase** |
| 仅存在 `.md` / `.pdf` / `.docx` 文件 | **Document** |
| 同时存在 manifest 文件和文档文件 | **Hybrid** |

输出变量：`PROJECT_TYPE = Codebase | Document | Hybrid`

### Step 2: 规模评估

统计项目中的有效文件（排除 `node_modules/`、`.git/`、`build/`、`dist/` 等常见忽略目录）：

| 文件数 | SCALE_TIER |
|--------|-----------|
| < 50 | small |
| 50 - 200 | medium |
| 200 - 500 | large |
| 500+ | xlarge |

输出变量：`SCALE_TIER = small | medium | large | xlarge`

同时记录：`TOTAL_FILES`（文件总数）、`TOTAL_SIZE`（总大小 MB）

### Step 3: 扫描代表性文件

采样 10-20 个文件进行读取，采样策略：

1. README / 入口文件（必选）
2. 配置文件（如 `tsconfig.json`、`webpack.config.js`）
3. 核心模块入口（`src/index.*`、`src/main.*`）
4. 按目录均匀分布采样剩余名额

目标：理解项目**领域**（做什么）和**结构**（怎么组织）

### Step 4: 生成 SCHEMA.md

从 `SCHEMA-TEMPLATE.md` 模板填充参数：

- `PROJECT_TYPE`：Step 1 结果
- `SCALE_TIER`：Step 2 结果
- `DOMAIN`：Step 3 推断的项目领域
- `PRIMARY_LANGUAGE`：主要编程语言
- `WIKI_CATEGORIES`：根据项目类型确定的 wiki 分类

约束：生成文件 ≤ 200 行

### Step 5: 生成 AGENTS.md

从 `AGENTS-TEMPLATE.md` 模板填充参数，对齐 Linux Foundation `agents.md` 标准格式：

```markdown
# Agents

## Knowledge Engineer
- Role: 知识库维护
- Capabilities: ingest / query / lint / update
- Boundaries: 不修改源代码，不执行部署

## Code Analyst (仅 Codebase/Hybrid)
- Role: 代码结构分析
- Capabilities: 模块识别 / 架构提取 / 依赖分析
- Boundaries: 只读分析，不重构代码
```

### Step 6: 创建 kb/ 目录骨架

```
kb/
├── raw/                    # 原始源文件归档（不可变）
├── wiki/
│   ├── entities/           # 实体页面（具体的人/工具/服务/模块）
│   ├── concepts/           # 概念页面（原理/模式/方法论）
│   ├── guides/             # 指南页面（How-to/最佳实践）
│   ├── comparisons/        # 对比页面（A vs B 分析）
│   ├── index.md            # 知识库索引
│   ├── inbox.md            # 待处理队列
│   └── log.md              # 操作日志
└── references/             # （可选）外部参考资料
```

执行命令序列：
```bash
mkdir -p kb/raw
mkdir -p kb/wiki/entities
mkdir -p kb/wiki/concepts
mkdir -p kb/wiki/guides
mkdir -p kb/wiki/comparisons
# 若 PROJECT_TYPE == Codebase 或 Hybrid
mkdir -p kb/references
```

### Step 7: 生成 wiki/index.md

创建空骨架索引：

```markdown
# 知识库索引

> 自动生成，随 ingest/query 回写更新

## Entities（实体）

<!-- 格式：- [[page-name]] — 一句话描述 -->

## Concepts（概念）

<!-- 格式：- [[page-name]] — 一句话描述 -->

## Guides（指南）

<!-- 格式：- [[page-name]] — 一句话描述 -->

## Comparisons（对比）

<!-- 格式：- [[page-name]] — 一句话描述 -->
```

### Step 8: 生成 inbox.md + log.md

**wiki/inbox.md**（状态机模板）：

```markdown
# Inbox — 待处理队列

## Pending（待处理）

<!-- 格式：- [ ] YYYY-MM-DD source-slug | 来源描述 -->

## Processing（处理中）

<!-- 格式：- [~] YYYY-MM-DD source-slug | 正在处理... -->

## Done（已完成）

<!-- 格式：- [x] YYYY-MM-DD source-slug | 完成，生成 N 页 -->
```

**wiki/log.md**（首条记录）：

```markdown
# 操作日志

| 日期 | 操作 | 详情 |
|------|------|------|
| YYYY-MM-DD | 🎉 Init | 项目类型: PROJECT_TYPE / 规模: SCALE_TIER / 文件数: TOTAL_FILES |
```

### Step 9: QMD MCP 配置建议

**条件**：仅当 `SCALE_TIER >= medium` 时执行

输出 QMD（Qoder Memory Daemon）配置建议：

```json
{
  "mcp_config": {
    "knowledge_base_path": "kb/",
    "auto_ingest": true,
    "ingest_budget": 15,
    "lint_interval": "every_5_ingests",
    "wiki_format": "markdown_wikilink",
    "scale_tier": "<SCALE_TIER>",
    "ignore_patterns": [
      "node_modules/", ".git/", "build/", "dist/",
      "target/", "__pycache__/", "*.lock"
    ]
  }
}
```

---

## 输出物清单

| 输出物 | 路径 | 说明 |
|--------|------|------|
| SCHEMA.md | `kb/SCHEMA.md` | 知识库元数据 |
| AGENTS.md | `kb/AGENTS.md` | Agent 角色定义 |
| 目录骨架 | `kb/raw/` + `kb/wiki/` | 完整目录结构 |
| index.md | `kb/wiki/index.md` | 知识库索引（空骨架） |
| inbox.md | `kb/wiki/inbox.md` | 状态机队列 |
| log.md | `kb/wiki/log.md` | 首条 init 记录 |
| QMD 配置 | 终端输出 | 仅 medium+ 规模 |

---

## 验证检查点

初始化完成后，逐项确认：

- [ ] `kb/` 目录存在
- [ ] `kb/raw/` 目录存在且为空
- [ ] `kb/wiki/entities/` 目录存在
- [ ] `kb/wiki/concepts/` 目录存在
- [ ] `kb/wiki/guides/` 目录存在
- [ ] `kb/wiki/comparisons/` 目录存在
- [ ] `kb/wiki/index.md` 存在且包含四个分区标题
- [ ] `kb/wiki/inbox.md` 存在且包含三个状态区
- [ ] `kb/wiki/log.md` 存在且包含 init 首条记录
- [ ] `kb/SCHEMA.md` 存在且 ≤ 200 行
- [ ] `kb/AGENTS.md` 存在且符合 Linux Foundation 格式
- [ ] 若 `SCALE_TIER >= medium`，QMD 配置已输出

全部通过后，Init 流程完成。
