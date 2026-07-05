# Wiki 索引

## Cloud Agents

### 实体

- [[agent]] — Agent 配置模板（模型、提示词、工具集、技能）
- [[environment]] — Session 运行的容器环境模板
- [[session]] — 有状态执行实例，绑定 Agent + Environment
- [[event]] — Session 中产生的实时事件流
- [[skill]] — Agent 可关联的领域专业知识模块
- [[memory-store]] — 跨 Session 持久化记忆仓库
- [[vault]] — 安全存储凭据的密钥管理系统
- [[deployment]] — 部署链路与生产注意事项
- [[file]] — 文件上传/挂载/下载

### 概念

- [[occ-versioning]] — 乐观并发控制（版本号防冲突）
- [[session-lifecycle]] — Session 状态机（idle → processing → archived）
- [[sse-event-stream]] — SSE 协议、事件类型与断线重连
- [[permission-model]] — 工具权限策略（allow / ask / deny）
- [[managed-agents-threading]] — 多 Agent 线程模型（Coordinator + Child）
- [[container-sandbox]] — 容器沙箱规格与资源限制
- [[outcome-rubric]] — 成功标准（Rubric）定义与驱动迭代

### 指南

- [[quickstart]] — 5 步快速开始
- [[troubleshooting]] — 常见错误诊断与解决
- [[production-checklist]] — 生产环境上线清单

### 对比

- [[tools-vs-skills]] — 工具与技能的区别和选型
- [[memory-vs-files]] — 记忆存储与文件 API 的选型

## QoderWake

### 实体

- [[waker]] — 数字员工（本机部署的 AI 员工实例）
- [[role]] — 角色模板（预置 7 种 + 自定义）
- [[waker-group]] — 员工群组（Leader + 成员协作）
- [[connector]] — 外部工具/服务连接器
- [[waker-daemon]] — Daemon 守护进程（Web 控制台 / 进程管理 / 云端桥接）

### 概念

- [[task-types]] — 三种任务类型（对话 / 自动 / 群组）
- [[automated-trigger]] — 自动触发机制（定时 / 事件 / API）
- [[waker-permission]] — Waker 权限模型（工具防护 / 文件防护）
- [[waker-memory]] — Waker 记忆系统（自动沉淀 / 手动 / 系统整理）
- [[waker-tool-guard]] — Tool Guard 安全规则引擎（29条规则拦截危险工具调用）
- [[waker-hook-lifecycle]] — Worker Hook 生命周期（8阶段注入链）
- [[waker-data-model]] — 数据模型参考（70张表完整索引）
- [[qmind-knowledge]] — QMind 知识引擎（提案-审计-OCC 版本控制）
- [[waker-trigger-plugins]] — 触发器插件架构（Aone/钉钉/GitHub 3种事件源）
- [[waker-identity-system]] — 数字员工身份卡系统（9份 Markdown + plugin.json）
- [[waker-plugin-system]] — 插件双层架构（Daemon级 + Agent级）
- [[waker-observability]] — 日志与可观测性（6层日志 + traceId + 遥测）

### 指南

- [[qw-quickstart]] — 安装 → 创建 → 派活 三步快速开始
- [[waker-config-guide]] — 完整配置指南（技能/连接器/项目/权限）

### 对比

- [[task-types-comparison]] — 对话 vs 自动 vs 群组任务选型
- [[cloud-agents-vs-qoderwake]] — Cloud Agents vs QoderWake 跨产品对比

## QoderCLI

### 实体

- [[cli-session]] — 会话与运行模式（TUI / Print / ACP 三种模式）
- [[cli-model]] — 模型系统（分级 / 前沿 / 自定义 + 参数配置）
- [[cli-skill]] — 技能系统（SKILL.md 封装领域专长）
- [[cli-subagent]] — 子代理系统（独立上下文的专业执行者）
- [[cli-plugin]] — 插件系统（扩展能力打包分发）

### 概念

- [[cli-permission-model]] — 权限模型（5 种模式 + 规则语法 + 决策顺序）
- [[cli-memory-system]] — 记忆系统（AGENTS.md + 自动记忆双轨）
- [[cli-hook-system]] — 钩子系统（事件 × Matcher × Handler）
- [[cli-tool-mcp]] — 工具与 MCP 集成（内置工具 + MCP 协议）
- [[cli-workflow-engine]] — 动态工作流引擎（JS 脚本编排多 Agent）
- [[cli-command-system]] — 命令系统（内置 + 自定义斜杠命令）
- [[cli-cron-system]] — 内置 Cron 调度系统（CronCreate/Delete/List，最多 50 个任务）
- [[cli-goal-system]] — Goal 自主执行系统（目标驱动 + 预算控制 + 完成审计）
- [[cli-task-tracker]] — 内置任务追踪器（epic/task/bug + 依赖关系 + ASCII 可视化）
- [[cli-canvas-system]] — Canvas 与 Recipes 系统（.canvas.tsx 可视化制品）

### 指南

- [[cli-quickstart]] — 安装 → 登录 → 使用 三步快速开始
- [[cli-cloud-remote]] — 云端与远程执行（Cloud Mode / Remote Control / ACP）

### 对比

- [[cli-vs-cloud-agents]] — CLI vs Cloud Agents 跨产品能力对比
- [[product-family-overview]] — Qoder 产品家族架构总览（5产品能力矩阵 + 选型指南）

## Qoder Desktop

### 实体

- [[desktop-editor]] — Editor 编码视图（NEXT + Ask + Agent 三大入口）
- [[desktop-quest]] — Quest 自主委派工作台（Agent + Experts 双模式）
- [[desktop-knowledge-engine]] — 知识引擎（Repo Wiki + 知识卡片 + Memory）
- [[desktop-rules]] — 规则系统（四种类型 + AGENTS.md 兼容）

### 概念

- [[desktop-agent-mode]] — Agent 模式（自主决策 + 工具调度 + 多文件编辑）
- [[desktop-hook-system]] — 钩子系统（文档 5 事件 + 工具名双向映射，与 CLI 共用引擎）
- [[desktop-security-audit]] — 安全审计 Hook 系统（DLP + 反入侵 + Prompt注入检测，681行 common.sh）

### 指南

- [[desktop-quickstart]] — 下载 → 登录 → 体验四大入口

## QoderWork

### 实体

- [[qw-task]] — 任务与产物（自然语言描述 → AI 执行 → 本地文件交付）
- [[qw-skill]] — 技能（SKILL.md 封装可复用工作流）
- [[qw-connector]] — 连接器（浏览器 / macOS 应用 / Microsoft 365 / 集成市场）

### 概念

- [[qw-computer-use]] — 电脑操控（截屏感知 + 鼠标键盘操控桌面应用）
- [[qw-awareness]] — 意识系统（跨会话记忆 + 协作风格个性化）
- [[qw-scheduled-task]] — 定时任务（本地调度自动执行）
- [[qw-im-channel]] — IM 频道（钉钉/飞书/微信/企微接入）

### 指南

- [[qw-quickstart]] — 下载 → 登录 → 跑通第一个任务

### 对比

- [[qw-vs-qoderwake]] — QoderWork vs QoderWake 跨产品对比
