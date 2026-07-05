# 斜杠命令（Qoder CLI / Desktop）

> 来源: https://docs.qoder.com/zh/cli/command + qodercli 1.0.16 本地实测 [2026-06-28]
> 对照: https://code.claude.com/docs/en/commands (Claude Code 70+ 命令)
> 结论: Qoder CLI 文档仅列 16 个内置命令，实测支持 40+ 个（含 TUI + Skill + Prompt 三类）

## 概述

命令是 Qoder CLI/Desktop 中通过 `/` 前缀触发的快捷操作。分三类：
- **TUI 命令**：提供交互式界面（仅交互模式可用）
- **Skill 命令**：加载 Skill 后作为 prompt 注入（支持 headless）
- **Prompt 命令**：直接向对话提交预设提示词（支持 headless）

## 实测验证结果（qodercli 1.0.16）

验证方法：`echo "/<command>" | qodercli --permission-mode bypass_permissions 2>&1`
- "TUI-ONLY" = 命令被识别但需交互模式
- "Skill activated" = Skill 被加载执行
- "Unknown skill" = 命令名被识别但本地未安装对应 skill

### TUI 命令（已验证 22 个）

| 命令 | 用途 | Claude Code 对应 |
|------|------|-----------------|
| /agents | 管理 Subagent | /agents ✓ |
| /tasks | 查看后台任务 | /tasks ✓ |
| /diff | 查看变更差异 | /diff ✓ |
| /context | 上下文可视化 | /context ✓ |
| /background | 后台运行 | /background ✓ |
| /branch | 分支对话 | /branch ✓ |
| /rewind | 回退对话/代码 | /rewind ✓ |
| /btw | 快速提问 | /btw ✓ |
| /config | 配置管理 | /config ✓ |
| /memory | 记忆管理 | /memory ✓ |
| /model | 模型选择 | /model ✓ |
| /skills | 技能管理 | /skills ✓ |
| /status | 系统状态 | /status ✓ |
| /resume | 恢复会话 | /resume ✓ |
| /permissions | 权限管理 | /permissions ✓ |
| /mcp | MCP 管理 | /mcp ✓ |
| /hooks | Hook 配置 | /hooks ✓ |
| /help | 帮助 | /help ✓ |
| /export | 导出对话 | /export ✓ |
| /copy | 复制响应 | /copy ✓ |
| /usage | 用量统计 | /usage ✓ |
| /login | 登录 | /login ✓ |
| /logout | 登出 | /logout ✓ |
| /exit | 退出 | /exit ✓ |
| /rename | 重命名会话 | /rename ✓ |
| /remote-control | 远程控制 | /remote-control ✓ |
| /plugin | 插件管理 | /plugin ✓ |

### Skill 命令（已验证激活）

| 命令 | 实测结果 | Claude Code 对应 |
|------|---------|-----------------|
| /compact | 执行成功（压缩对话） | /compact ✓ |
| /batch | "Skill batch activated" | /batch ✓ |
| /goal | "No active goal" | /goal ✓ |
| /security-review | "Skill activated" | /security-review ✓ |
| /loop | "Skill loop activated" | /loop ✓ |
| /deep-research | "Skill deep-research activated" | /deep-research ✓ |
| /simplify | "Skill simplify activated" | /simplify ✓ |
| /init | 执行成功 | /init ✓ |

### 命令名已识别但本地未安装 Skill

| 命令 | 实测结果 | Claude Code 有？ |
|------|---------|----------------|
| /doctor | "Unknown skill: doctor" | ✓ |
| /fork | "Unknown skill: fork" | ✓ |
| /fast | "Unknown skill: fast" | ✓ |
| /advisor | "Unknown skill: advisor" | ✓ |
| /code-review | "Unknown skill: code-review" | ✓ |
| /cd | "Unknown skill: cd" | ✓ |
| /focus | "Unknown skill: focus" | ✓ |
| /recap | "Unknown skill: recap" | ✓ |
| /teleport | "Unknown skill: teleport" | ✓ |
| /schedule | "Unknown skill: schedule" | ✓ |
| /run | "Unknown skill: run" | ✓ |
| /verify | "Unknown skill: verify" | ✓ |

### 未识别的命令

| 命令 | 实测结果 | Claude Code 有？ | 说明 |
|------|---------|----------------|------|
| /workflows | 未识别 | ✓ | 可能合并到 /tasks |
| /clear | 未识别 | ✓ | 可能用 /compact 替代 |
| /effort | 未识别 | ✓ | 可能合并到 /model |

## Claude Code 独有命令（Anthropic 平台特有）

以下命令为 Anthropic 平台特有，Qoder 不太可能实现：

| 命令 | 说明 |
|------|------|
| /radio | Claude FM 电台 |
| /stickers | 订购贴纸 |
| /passes | 分享免费周 |
| /chrome | Chrome 扩展管理 |
| /mobile | 移动端下载 |
| /setup-bedrock | AWS Bedrock 配置 |
| /setup-vertex | Google Vertex 配置 |
| /upgrade | 升级付费计划 |
| /privacy-settings | 隐私设置 |
| /usage-credits | 用量积分 |
| /powerup | 功能教程 |
| /team-onboarding | 团队引导 |
| /release-notes | 变更日志 |
| /install-github-app | GitHub App 安装 |
| /install-slack-app | Slack App 安装 |
| /web-setup | Web 连接配置 |
| /autofix-pr | PR 自动修复 |
| /ultraplan | 云端计划 |
| /ultrareview | 云端审查 |

## Qoder Desktop 命令文档现状

Desktop 文档（docs.qoder.com/user-guide/commands）仅描述了**自定义命令系统**（用户级/项目级 .md 文件），未列出任何内置命令。与 CLI 共享同一引擎，实际内置命令集应与 CLI 一致。

## 自定义命令

### 存储位置

| 级别 | 路径 | 生效范围 |
|------|------|---------|
| 项目级 | `.qoder/commands/<name>.md` | 仅当前项目 |
| 用户级 | `~/.qoder/commands/<name>.md` | 所有项目 |

### 命名规范

- 小写字母 + 数字 + 连字符 + 下划线
- 子目录用 `:` 分隔命名空间（如 `git/commit.md` → `/git:commit`）
- 目录含 SKILL.md 时注册为单个命令

### Headless 使用

```bash
qodercli -p '/review 重点检查注释覆盖情况'
qodercli -p '/git-commit'
```
