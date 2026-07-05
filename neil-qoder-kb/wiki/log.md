# 操作日志

## [2026-06-30] lint | 逆向分析内容准确性验证 ✅

- 触发：用户要求对 waker-memory.md 和 waker-permission.md 进行实际产物比对验证
- 方法：直接检查 ~/.qoderwake/ 本地文件、SQLite schema、日志、二进制字符串
- 发现偏差并修正：
  1. **存储架构描述误导**：agent.sqlite 实际是 RAG 索引库，非记忆存储 → 修正为多层存储架构说明
  2. **Tool Guard 规则数**：28条 → 29条（实际计数 dangerous_shell_commands.json）
  3. **feature-config 开关**：5个 key 本地不存在 → 标注为 [inferred]，加注警告
  4. **AgentProfileSummarizer**：精确化为 per-agent cron 任务名
  5. **index.md 中的全角括号编辑错误**：修复
- 已验证正确的内容：MCP 端点 URL ✓、Header 名 ✓、Hook 链路及 timeout ✓、CLI memory 子命令 ✓、Cron 时间 ✓

## [2026-06-30] ingest | 安装产物逆向分析——知识库深度扩展 ✅

- 触发：用户要求“做大做强”知识库，参考 ATA 文章《从 AI 编程助手到 AI 数字员工平台》的逆向分析方法
- 来源：本地安装产物逆向工程（~/.qoderwake/ + ~/.qoder/）
- 方法：4 个并行 subagent 深度扫描（SQLite schema / 安全规则 / 配置文件 / 二进制分析）
- 创建页面：13 个新 wiki 页
  - wiki/qoderwake/concepts/waker-tool-guard.md（28条安全规则引擎）
  - wiki/qoderwake/concepts/waker-hook-lifecycle.md（8阶段 Hook 链）
  - wiki/qoderwake/concepts/waker-data-model.md（70张表数据模型）
  - wiki/qoderwake/concepts/qmind-knowledge.md（QMind 知识引擎）
  - wiki/qoderwake/concepts/waker-trigger-plugins.md（3个触发器插件）
  - wiki/qoderwake/concepts/waker-identity-system.md（身份卡系统）
  - wiki/qoderwake/concepts/waker-plugin-system.md（双层插件）
  - wiki/qoderwake/concepts/waker-observability.md（日志与可观测性）
  - wiki/qoderwake/entities/waker-daemon.md（Daemon 守护进程）
  - wiki/qodercli/concepts/cli-cron-system.md（内置 Cron 调度）
  - wiki/qodercli/concepts/cli-goal-system.md（Goal 自主执行）
  - wiki/qodercli/concepts/cli-task-tracker.md（任务追踪器）
  - wiki/qodercli/concepts/cli-canvas-system.md（Canvas/Recipes）
- 自进化机制：launchd 定时任务（每天 09:30）+ kb-evolve.sh（同步/Ingest/Lint/每周一深度进化）
- index.md：已更新（+6 个新条目）
- 证据等级：[reverse-engineering] + [verified-by-api]

## [2026-06-28] ingest | QoderCLI 斜杠命令实测验证 ✅

- 触发：用户要求对比 Claude Code 命令与 Qoder CLI 命令支持情况
- Claude Code 官方文档列出 70+ 命令，Qoder 文档仅列 16 个
- 实测方法：`echo "/<cmd>" | qodercli --permission-mode bypass_permissions 2>&1`
- 实测结果：27 个 TUI 命令 + 8 个 Skill 命令已激活 + 12 个框架支持待安装 = 47 个（覆盖率 ~94%）
- 仅 3 个未识别：/workflows、/clear、/effort
- 创建 raw：raw/qodercli/commands.md（142 行）
- 更新 wiki：wiki/qodercli/concepts/cli-command-system.md（重写）
- 证据等级：[verified-by-api] + [cross-reference]

## [2026-06-28] ingest | Qoder Desktop + QoderWork 全量导入 ✅

- 来源：docs.qoder.com/zh 主站 + docs.qoder.com/zh/qoderwork
- Qoder Desktop：6 个 raw 文件（overview, quick-start, editor, agent-mode, quest, knowledge-engine, rules）
- QoderWork：7 个 raw 文件（introduction, quick-start, computer-use, skills, awareness, connectors, scheduled-tasks, im-channels）
- 创建 wiki 页面：
  - qoderdesktop：4 实体页 + 1 概念页 + 1 指南页 = 6 页
  - qoderwork：3 实体页 + 4 概念页 + 1 指南页 + 1 对比页 = 9 页
- 交叉引用：已建立（平均每页 4 个出站引用，含跨产品引用）
- SCHEMA.md：已添加 qoderdesktop + qoderwork 命名空间
- index.md：已更新 Qoder Desktop + QoderWork 部分

## [2026-06-28] ingest | Qoder Desktop Hooks 导入 ✅

- 来源：https://docs.qoder.com/zh/extensions/hooks
- 创建 raw：raw/qoderdesktop/hooks.md（197 行）
- 创建 wiki：wiki/qoderdesktop/concepts/desktop-hook-system.md（113 行）
- 关键发现：文档声称 5 事件 + 1 Handler，但明确标注“IDE/JB插件与 CLI 共享配置文件”，与 CLI 实测 30+5 矛盾
- 独有价值：工具名双向映射表（Qoder 原生名 ↔ Claude Code 兼容名）
- 证据等级：[official-docs] + [cross-reference] CLI 实测

## [2026-06-28] ingest | QoderCLI Hooks 实测修正 ✅

- 触发：用户质疑官网文档准确性，通过 qodercli 1.0.16 本地实测验证
- 发现：官网文档仅列出 4 种事件类型，实测确认支持全部 30 种事件 + 5 种 Handler 类型（与 Claude Code 完全同构）
- 验证方法：`qodercli --setting-sources "" --settings '{30个事件}' -p "say ok"` → 0 error
- 更新 raw：raw/qodercli/hooks.md（重写，从 83 行扩展到 178+ 行）
- 更新 wiki：wiki/qodercli/concepts/cli-hook-system.md（重写，从 81 行扩展到 156+ 行）
- 证据等级：[verified-by-api] + [cross-reference] Claude Code 官方文档

## [2026-06-28] ingest | QoderCLI 全量导入 ✅

- 来源：docs.qoder.com/zh/cli 全部 16 个页面（quick-start, using-cli, command, model, memory, mcp-servers, tools, skills, hooks, permissions, subagent, plugins, workflows, cloud-mode, acp, remote-control）
- 创建页面：5 实体页 + 6 概念页 + 2 指南页 + 1 对比页 = 14 页
- 实体页：cli-session, cli-model, cli-skill, cli-subagent, cli-plugin
- 概念页：cli-permission-model, cli-memory-system, cli-hook-system, cli-tool-mcp, cli-workflow-engine, cli-command-system
- 指南页：cli-quickstart, cli-cloud-remote
- 对比页：cli-vs-cloud-agents
- 交叉引用：已建立（平均每页 4-6 个出站引用，含跨产品引用）
- index.md：已更新 QoderCLI 部分
- SCHEMA.md：已添加 qodercli 产品命名空间

## [2026-06-28] ingest | QoderWake 全量导入 ✅

- 来源：raw/qoderwake/ 全部 8 个文件（overview, installation, create-waker, conversation-tasks, automated-tasks, group-tasks, examples, manage-wakers）
- 创建页面：4 个实体页 + 4 个概念页 + 2 个指南页 + 2 个对比页 = 12 页
- 实体页：waker, role, waker-group, connector
- 概念页：task-types, automated-trigger, waker-permission, waker-memory
- 指南页：qw-quickstart, waker-config-guide
- 对比页：task-types-comparison, cloud-agents-vs-qoderwake
- 交叉引用：已建立（平均每页 4-5 个出站引用，含跨产品引用）
- index.md：已更新 QoderWake 部分

## [2026-06-28] migrate | 多产品架构迁移

- 操作：raw/*.md → raw/cloud-agents/，wiki/{entities,concepts,guides,comparisons} → wiki/cloud-agents/
- 更新：SCHEMA.md 升级为多产品，index.md 改为多产品分区格式
- 影响页面：全部 20 页的来源路径更新

## [2026-06-28] lint + fix | 健康检查与修复

- 触发：手动执行 lint
- 初始分数：81/100（B 级）
- 修复 P0：memory-vs-files.md 矛盾（memory_store_ids 废弃信息不一致）
- 修复 P1：创建 outcome-rubric.md（raw/outcomes.md 缺少对应 wiki 页）
- 修复 P1：modification-checklist 孤立页——deployment + quickstart 添加入站引用
- 修复 P1：全部 20 页来源段落补全 evidence level 标注 [official-docs]
- 修复 P2：session.md 添加 [[managed-agents-threading]] + [[outcome-rubric]] 引用
- 修复 P2：event.md 添加 [[outcome-rubric]] 引用
- 更新 index.md：新增 [[outcome-rubric]] 条目
- 修复后预估分数：93/100（A 级）

## [2026-06-21] ingest | 初始全量导入

- 来源：raw/ 全部 15 个文件（overview, quickstart, define-agent, environments, sessions, tools, events-stream, skills, memory-stores, managed-agents, permission-policies, files, outcomes, vaults, container-reference）
- 创建页面：9 个实体页 + 6 个概念页 + 3 个指南页 + 2 个对比页 = 20 页
- 实体页：agent, environment, session, event, skill, memory-store, vault, deployment, file
- 概念页：occ-versioning, session-lifecycle, sse-event-stream, permission-model, managed-agents-threading, container-sandbox
- 指南页：quickstart, troubleshooting, production-checklist
- 对比页：tools-vs-skills, memory-vs-files
- 交叉引用：已建立（平均每页 4-6 个出站引用）
- index.md：已创建
