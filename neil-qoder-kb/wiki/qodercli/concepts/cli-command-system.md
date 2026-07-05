# CLI Command System — 命令系统

> Qoder CLI/Desktop 的斜杠命令体系。文档列 16 个内置命令，实测 40+（TUI 22 + Skill 8 + 待安装 12）。与 Claude Code 70+ 命令高度同构。

## 概述

命令通过 `/` 前缀触发，分三类执行模式：
- **TUI 命令**：弹出交互界面，仅交互模式可用
- **Skill 命令**：加载 bundled skill，支持 headless（`-p`）
- **自定义命令**：用户编写的 .md 文件，注册为 prompt 命令

**验证版本**：qodercli 1.0.16，验证方法 `echo "/<cmd>" | qodercli --permission-mode bypass_permissions 2>&1`

## 命令覆盖度（vs Claude Code）

| 类别 | Claude Code | Qoder CLI 实测 | 覆盖率 |
|------|-------------|---------------|--------|
| 核心 TUI 命令 | ~30 | 27 已识别 | ~90% |
| Bundled Skill 命令 | ~12 | 8 已激活 + 12 待安装 | ~100%（框架支持） |
| 平台特有命令 | ~19 | 不适用（Anthropic 独有） | N/A |
| **总计（去除平台特有）** | **~50** | **~47** | **~94%** |

## TUI 命令（27 个已验证）

| 命令 | 用途 | 说明 |
|------|------|------|
| /agents | 管理 Subagent 配置 | |
| /tasks | 查看后台任务 | |
| /diff | 查看未提交变更 + 逐 turn diff | |
| /context | 上下文用量可视化 | |
| /background | 后台运行会话 | 别名 /bg |
| /branch | 分支对话 | |
| /rewind | 回退对话/代码到检查点 | 别名 /checkpoint, /undo |
| /btw | 快速侧面提问 | |
| /config | 配置管理 | 别名 /settings |
| /memory | 记忆管理（AGENTS.md） | |
| /model | 模型选择 | |
| /skills | 技能列表与管理 | |
| /status | 系统状态 | |
| /resume | 恢复历史会话 | 别名 /continue |
| /permissions | 权限规则管理 | 别名 /allowed-tools |
| /mcp | MCP 服务器管理 | |
| /hooks | Hook 配置查看 | |
| /help | 帮助 | |
| /export | 导出对话为文本 | |
| /copy | 复制最后响应到剪贴板 | |
| /usage | 用量统计 | 别名 /cost, /stats |
| /login | 登录 | |
| /logout | 登出 | |
| /exit | 退出 | 别名 /quit |
| /rename | 重命名会话 | |
| /remote-control | 远程控制 | 别名 /rc |
| /plugin | 插件管理 | |

## Skill 命令（8 个已激活）

| 命令 | 实测结果 | 说明 |
|------|---------|------|
| /compact | 执行成功 | 压缩对话历史 |
| /batch | Skill activated | 大规模并行变更（worktree） |
| /goal | 返回状态 | 持续工作直到条件满足 |
| /security-review | Skill activated | 安全审查 |
| /loop | Skill activated | 循环执行 prompt |
| /deep-research | Skill activated | 多源深度研究 |
| /simplify | Skill activated | 代码简化审查 |
| /init | 执行成功 | 初始化 AGENTS.md |

## 框架已支持但需安装 Skill（12 个）

| 命令 | 说明 |
|------|------|
| /doctor | 诊断安装问题 |
| /fork | 派生子代理 |
| /fast | 快速模式 |
| /advisor | 第二模型顾问 |
| /code-review | 代码审查 |
| /cd | 切换工作目录 |
| /focus | 聚焦视图 |
| /recap | 会话摘要 |
| /teleport | 拉取 Web 会话 |
| /schedule | 定时任务 |
| /run | 运行并验证应用 |
| /verify | 验证代码变更 |

## 未识别（3 个 Claude Code 命令）

| 命令 | Claude Code 用途 | Qoder 替代 |
|------|----------------|-----------|
| /workflows | 工作流面板 | /tasks 可能覆盖 |
| /clear | 清除对话 | /compact |
| /effort | 思考深度调节 | /model 内含 |

## 自定义命令系统

### 存储路径

```
~/.qoder/commands/<name>.md          # 用户级（全项目生效）
${project}/.qoder/commands/<name>.md  # 项目级（优先于用户级）
```

### 命名规范

- 小写字母 + 数字 + 连字符 + 下划线
- 子目录 → `:` 命名空间（`git/commit.md` → `/git:commit`）
- 目录含 SKILL.md → 注册为单个 Skill 命令

### Headless 使用

```bash
qodercli -p '/review 重点检查注释'
qodercli -p '/git-commit'
```

## 交叉引用

- [[cli-hook-system]] — Hooks 也通过 /hooks 命令管理
- [[cli-skill]] — Skill 命令是 SKILL.md 封装
- [[cli-plugin]] — 插件可注册额外命令
- [[cli-subagent]] — /agents 管理子代理配置

## 来源

- raw/qodercli/command.md [official-docs]
- raw/qodercli/commands.md [verified-by-api] (2026-06-28)
- https://code.claude.com/docs/en/commands [cross-reference]
