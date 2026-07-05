# Qoder Products Wiki 维护规则 (Schema)

> 本文件定义了 wiki/ 目录的结构规范、维护操作和质量标准。
> 每次 ingest 或 lint 时，qodercli 必须严格遵循本文件的规则。
> 支持多产品：当前覆盖 Cloud Agents + QoderWake + QoderCLI。

## 三层架构

```
raw/{product}/  → 不可变的原始文档镜像（sync-docs.sh 维护，LLM 只读不写）
wiki/{product}/ → LLM 生成并维护的结构化知识（本文件定义的规则）
SCHEMA.md      → 你正在阅读的这份规则文件
```

## 产品命名空间规则

每个产品占据独立的命名空间：
- `raw/{product}/` — 该产品的原始文档
- `wiki/{product}/` — 该产品的编译知识
- 每个产品空间内部统一使用 `entities/` `concepts/` `guides/` `comparisons/` 分类

当前产品：
| 产品 | 命名空间 | 说明 |
|------|----------|------|
| Cloud Agents | `cloud-agents` | 云端托管 Agent 沙箱 API |
| QoderWake | `qoderwake` | 本机部署数字员工团队 |
| QoderCLI | `qodercli` | 终端 AI Coding Agent（本地交互式开发助手） |
| Qoder Desktop | `qoderdesktop` | 桌面 Agentic IDE（Editor + Quest 双视图） |
| QoderWork | `qoderwork` | 桌面端智能工作助手（非编程场景） |

跨产品 [[wikilink]] 规则：文件名必须全局唯一，不同产品的实体名不得冲突。

## Wiki 目录结构

```
wiki/
├── index.md              # 多产品全量索引（必须在每次 ingest 后更新）
├── log.md                # 操作时间线（append-only）
├── inbox.md              # 来源状态机
├── cloud-agents/         # Cloud Agents 产品
│   ├── entities/
│   │   ├── agent.md
│   │   ├── environment.md
│   │   ├── session.md
│   │   ├── event.md
│   │   ├── skill.md
│   │   ├── memory-store.md
│   │   ├── vault.md
│   │   ├── deployment.md
│   │   └── file.md
│   ├── concepts/
│   │   ├── occ-versioning.md
│   │   ├── session-lifecycle.md
│   │   ├── sse-event-stream.md
│   │   ├── permission-model.md
│   │   ├── managed-agents-threading.md
│   │   ├── container-sandbox.md
│   │   └── outcome-rubric.md
│   ├── guides/
│   │   ├── quickstart.md
│   │   ├── troubleshooting.md
│   │   └── production-checklist.md
│   └── comparisons/
│       ├── tools-vs-skills.md
│       └── memory-vs-files.md
├── qoderwake/            # QoderWake 产品
│   ├── entities/
│   │   ├── waker.md
│   │   ├── role.md
│   │   ├── waker-group.md
│   │   └── connector.md
│   ├── concepts/
│   │   ├── task-types.md
│   │   ├── automated-trigger.md
│   │   ├── waker-permission.md
│   │   └── waker-memory.md
│   ├── guides/
│   │   ├── qw-quickstart.md
│   │   └── waker-config-guide.md
│   └── comparisons/
│       ├── task-types-comparison.md
│       └── cloud-agents-vs-qoderwake.md
└── qodercli/             # QoderCLI 产品
    ├── entities/
    │   ├── cli-session.md
    │   ├── cli-model.md
    │   ├── cli-skill.md
    │   ├── cli-subagent.md
    │   └── cli-plugin.md
    ├── concepts/
    │   ├── cli-permission-model.md
    │   ├── cli-memory-system.md
    │   ├── cli-hook-system.md
    │   ├── cli-tool-mcp.md
    │   ├── cli-workflow-engine.md
    │   └── cli-command-system.md
    ├── guides/
    │   ├── cli-quickstart.md
    │   └── cli-cloud-remote.md
    └── comparisons/
        └── cli-vs-cloud-agents.md
```

## 页面格式规范

每个 wiki 页面必须包含：

```markdown
# 页面标题

> 一句话描述（什么+为什么重要）

## 概述
[2-3 句核心说明]

## 详细内容
[主体内容，使用表格、代码块、列表]

## 交叉引用
- [[相关页面1]] — 关联说明
- [[相关页面2]] — 关联说明

## 来源
- raw/xxx.md（标注基于哪些 raw 文件编译）
```

## 证据等级标注

每个页面的“来源”段落必须标注证据等级：
- `[official-docs]` — 来自 docs.qoder.com 官方文档
- `[verified-by-api]` — 通过实际 API 调用验证
- `[user-reported]` — 来自用户反馈/社区报告（需标注日期）
- `[reverse-engineering]` — 通过安装产物逆向分析（配置文件/DB schema/二进制分析）

## 交叉引用规则

- 使用 `[[page-name]]` 格式引用其他 wiki 页面
- page-name 为文件名（不含 .md 和目录前缀）
- 例：`[[session]]` 引用 `entities/session.md`
- 每个页面的「交叉引用」段落列出所有出站链接
- 每次更新页面时检查：是否有新的交叉引用需要添加

## 操作：Ingest

触发条件：sync-docs.sh 检测到 raw/ 文件有变化后自动触发。

流程：
0. **写入优先（不可违反）**：在 wiki/inbox.md 登记来源（pending）+ 在 wiki/log.md 追加"⏳ 进行中"。只有这两步完成后才开始处理。
1. 读取变化的 raw 文件（通过 git diff 或 SHA 对比识别）
2. 理解变化内容的语义
3. 更新 wiki/ 中受影响的页面：
   - 实体页：字段变化、新增 API、行为变化
   - 概念页：机制说明的修正或补充
   - 指南页：步骤变化、新增注意事项
4. 添加或更新交叉引用
5. 如果新内容引入了新概念/新实体，创建新页面
6. 更新 index.md
7. 在 log.md 追加条目

# 操作：Query

触发条件：用户向 subagent 提问。

流程：
1. 读取 wiki/index.md 定位相关页面
2. 读取相关 wiki 页面获取编译后的知识
3. 如果 wiki 中信息不足，回退到 raw/ 文件补充
4. 如果 raw/ 中也没有，使用 WebFetch 访问官网
5. 回答完成后，执行「回写判定」（见下文）

## 操作：Query 回写（Compounding）

每次 Query 回答完成后，**必须**检查以下触发条件。满足任一条即执行回写：

### 触发条件（满足任一即回写）

1. **跨页综合** — 回答综合了 3+ 个 wiki/raw 页面的内容 → 创建新的 comparison 或 concept 页
2. **纠错补充** — 回答修正了 wiki 中的错误或补充了缺失内容 → 更新对应页面
3. **新话题** — 回答涉及了 wiki 中不存在的概念/实体/操作 → 创建新页面
4. **深度解析** — 回答产生了超越 raw 文档表层的深入分析（如排障经验、最佳实践组合） → 创建 guide 页

### 回写执行步骤

1. 将回答内容按 SCHEMA 页面格式规范重新组织
2. 放入对应类型目录（entities/concepts/guides/comparisons）
3. 添加 `## 来源` 段落，注明 `来自用户查询 [YYYY-MM-DD]`
4. 添加/更新交叉引用 [[wikilink]]
5. **必须**更新 wiki/index.md
6. **必须**在 wiki/log.md 追加条目：`## [YYYY-MM-DD] query-writeback | 页面标题`

### 不回写的情况

- 纯 raw 内容的直接转述（没有综合价值）
- 一问一答式的简单查询（如"API 地址是什么"）
- 回答内容已经存在于 wiki 中（避免重复）

## 操作：Lint

触发条件：定期维护或手动触发。

检查项：
- [ ] 矛盾：页面之间是否有冲突说明
- [ ] 过时：raw/ 已更新但 wiki 未同步的内容
- [ ] 孤立页：没有任何入站 [[引用]] 的页面
- [ ] 缺页：内容中提到但尚未创建的概念
- [ ] 交叉引用完整性：所有 [[link]] 指向存在的页面

## index.md 格式

```markdown
# Wiki 索引

## 实体
- [[agent]] — Agent 配置模板（模型、提示词、工具集）
- [[session]] — 执行任务的有状态工作会话
...

## 概念
- [[occ-versioning]] — 乐观并发控制机制
...

## 指南
- [[quickstart]] — 5 步快速开始
...

## 对比
- [[tools-vs-skills]] — 工具与技能的区别
...
```

## log.md 格式

```markdown
# 操作日志

## [2026-06-21] ingest | 初始导入
- 来源：raw/ 全部 15 个文件
- 创建页面：9 个实体页 + 6 个概念页 + 3 个指南页 + 2 个对比页
- 交叉引用：已建立

## [2026-06-22] ingest | overview.md 更新
- 变化：新增 Deployment 相关内容
- 更新页面：[[agent]], [[deployment]], index.md
```

### 自进化机制

知识库支持自动化自我迭代：
- `scripts/kb-evolve.sh` — 每日自进化脚本（同步/Ingest/Lint/深度进化）
- `scripts/com.neil.kb-evolve.plist` — macOS launchd 定时任务（每天 09:30）
- 每周一额外执行深度进化：扫描安装产物变化、识别新知识点、自动创建页面

## 质量标准

1. **不重复 raw** — wiki 页面是综合和提炼，不是 raw 的复制粘贴
2. **可独立阅读** — 每个页面自成一体，无需跳转就能理解核心概念
3. **交叉引用丰富** — 平均每页至少 3 个出站引用
4. **面向回答** — 内容组织方式应该让 Agent 能快速定位并回答用户问题
5. **标注来源** — 每个页面标注基于哪些 raw 文件编译，便于追踪
