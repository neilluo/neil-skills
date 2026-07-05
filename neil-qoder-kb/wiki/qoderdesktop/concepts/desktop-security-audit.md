# 安全审计 Hook 系统

> Qoder Desktop 和 QoderCLI 共享的安全审计框架，通过 681 行 common.sh 脚本集成 DLP（数据防泄漏）、Anti-Intrusion（反入侵）、AIGC Injection（注入检测）三重安全检测，拦截致命操作、凭据窃取和 Prompt 注入。

## 概述

安全审计 Hook 是 Qoder 产品线（Desktop + CLI）共享的深度安全防护机制，位于 `~/.qoder/hooks/` 目录。与 QoderWake 的 [[waker-tool-guard]] 规则引擎不同，这套系统面向**更底层的安全检测**——不仅检查工具调用参数，还检测反弹 Shell、凭据窃取模式、数据外传、Prompt 注入等高级威胁。

核心脚本 `common.sh`（681 行）被所有 Hook 脚本共享调用。

## 目录结构

```
~/.qoder/hooks/
├── common.sh                      # 共享安全检测库（681行）
├── PreToolUse.sh                  # 工具调用前检测
├── PostToolUse.sh                 # 工具调用后审计
├── PostToolUseFailure.sh          # 工具调用失败审计
├── UserPromptSubmit.sh            # Prompt 提交安全检测
├── SessionStart.sh                # 会话启动审计
├── SessionEnd.sh                  # 会话结束审计
├── Stop.sh                        # 模型输出捕获 + git 安全检查
└── Notification.sh                # Agent 通知捕获
```

## 三重安全检测

### 1. DLP（Data Loss Prevention）— 数据防泄漏

检测 Agent 是否尝试将敏感数据外传：
- 检查输出中是否包含 API 密钥模式（AWS / GCP / Azure / GitHub Token 等）
- 检查文件操作目标是否为敏感路径（~/.ssh / ~/.aws / ~/.kube）
- 检查网络请求是否包含凭据参数

### 2. Anti-Intrusion — 反入侵检测

检测 Agent 是否执行恶意操作：
- **反弹 Shell 检测**：nc/bash -i/python -c 等反弹模式
- **致命操作检测**：rm -rf /、mkfs、dd 等破坏性命令
- **凭据窃取检测**：cat ~/.ssh/id_rsa、export TOKEN= 等模式
- **提权检测**：sudo、su、chmod 4755（SUID）

### 3. AIGC Injection — Prompt 注入检测

在 `UserPromptSubmit.sh` 中检测：
- 用户输入是否包含系统指令覆盖尝试
- 是否包含角色扮演攻击（"Ignore previous instructions"）
- 是否包含内网地址泄漏

## Hook 事件覆盖

| Hook 文件 | 事件 | 检测内容 |
|-----------|------|----------|
| PreToolUse.sh | 工具调用前 | 致命操作、反弹 Shell、凭据窃取、数据外传 |
| PostToolUse.sh | 工具调用后 | 全量审计日志 |
| PostToolUseFailure.sh | 工具失败后 | 失败原因审计 |
| UserPromptSubmit.sh | Prompt 提交 | 注入检测、敏感信息、内网泄漏 + Security API 调用 |
| SessionStart.sh | 会话启动 | 会话环境审计 |
| SessionEnd.sh | 会话结束 | 会话收尾审计 |
| Stop.sh | 模型输出 | 输出捕获 + git 安全检查 |
| Notification.sh | Agent 通知 | 通知内容捕获 |

## common.sh 核心函数

| 函数 | 说明 |
|------|------|
| check_fatal_operation | 检查致命 Shell 命令 |
| check_reverse_shell | 检测反弹 Shell 模式 |
| check_credential_theft | 检测凭据窃取行为 |
| check_data_exfiltration | 检测数据外传尝试 |
| check_prompt_injection | 检测 Prompt 注入 |
| check_sensitive_path | 检查敏感文件路径访问 |
| audit_log | 统一审计日志写入 |
| call_security_api | 调用安全检测 API |

## 与其他安全机制的关系

```
用户输入 → UserPromptSubmit Hook（Injection 检测）
  ↓
Agent 决策 → 调用工具
  ↓
PreToolUse Hook（common.sh 安全检测）
  ├── Desktop/CLI: 8 个 .sh 脚本（DLP + Anti-Intrusion + AIGC）
  └── QoderWake:   Tool Guard 规则引擎（28 条 regex 规则）
  ↓
工具执行
  ↓
PostToolUse Hook（审计日志）
```

**分工**：
- `common.sh` 系列：模式检测为主，面向高级威胁（反弹 Shell、凭据窃取）
- [[waker-tool-guard]]：正则匹配为主，面向常见危险命令（rm/mv/sudo）
- 两者在 QoderWake 中**叠加生效**（双重防护）

## 与 QoderCLI 的关系

Desktop Hook 脚本和 CLI Hook 共享 `~/.qoder/hooks/` 目录：
- Desktop IDE 和 CLI 使用相同的 Hook 引擎
- Desktop 的 [[desktop-hook-system]] 文档标注 "IDE/JB插件与 CLI 共享配置文件"
- 实际部署的 Hook 脚本数（8个）远超官方文档描述的事件数（4个）

## 交叉引用

- [[desktop-hook-system]] — Desktop Hook 系统的上层设计
- [[cli-hook-system]] — QoderCLI 的 30 事件 + 5 Handler Hook 引擎
- [[waker-tool-guard]] — QoderWake 的安全规则引擎（互补关系）
- [[waker-hook-lifecycle]] — QoderWake 的 Hook 注入链
- [[cli-permission-model]] — 权限模型与安全检测的关系

## 来源

- ~/.qoder/hooks/ 目录结构（8 个脚本 + common.sh 681 行） [reverse-engineering] 2026-06-30
- QoderCLI 1.0.16 Hook 实测验证 [verified-by-api] 2026-06-28
