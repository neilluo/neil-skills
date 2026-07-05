# Tool Guard 安全规则引擎

> QoderWake 的 LLM 工具调用安全防护系统，通过 28 条预置规则拦截危险 Shell 命令和网络请求，是数字员工安全运行的核心保障。

## 概述

Tool Guard 是 QoderWake 内置的安全规则引擎，通过 `PreToolUse` Hook 在每次 LLM Agent 调用工具前进行拦截检查。规则库位于 `~/.qoderwake/resources/security/tool-guard-rules/dangerous_shell_commands.json`，覆盖 Bash 和 WebFetch 两种工具类型。

核心设计原则：**默认拒绝危险操作，宁可误拦不可漏放**。

## 架构

```
LLM Agent → 调用 Tool → PreToolUse Hook 触发
                              ↓
                    qoderwake_permission_guard
                              ↓
                    规则匹配（28条 regex）
                              ↓
                  ┌─ 无匹配 → 放行
                  ├─ HIGH 匹配 → 询问用户 / 阻断
                  └─ CRITICAL 匹配 → 直接阻断
```

## 规则分类（5 大类）

### 1. Command Injection（命令注入）

| 规则 ID | 严重度 | 防护目标 |
|---------|--------|----------|
| TOOL_CMD_DANGEROUS_RM | HIGH | rm 命令防数据丢失 |
| TOOL_CMD_DANGEROUS_MV | HIGH | mv 防意外覆盖文件 |
| TOOL_CMD_FS_DESTRUCTION | CRITICAL | mkfs/dd 磁盘格式化/擦除 |
| TOOL_CMD_DOS_FORK_BOMB | CRITICAL | fork 炸弹与批量 kill |
| TOOL_CMD_SYSTEM_REBOOT | CRITICAL | reboot/shutdown/halt |
| TOOL_CMD_SERVICE_RESTART | HIGH | systemctl/launchctl 服务管理 |
| TOOL_CMD_PROCESS_KILL | HIGH | kill/pkill/killall |
| TOOL_CMD_SYSTEM_TAMPERING | HIGH | 修改 cron/SSH/sudoers 文件 |
| TOOL_CMD_UNSAFE_PERMISSIONS | HIGH | chmod 777/chattr 不可变标志 |
| TOOL_CMD_IFS_INJECTION | HIGH | $IFS 变量绕过空格分隔 |
| TOOL_CMD_CONTROL_CHARS | CRITICAL | 不可打印控制字符注入 |
| TOOL_CMD_UNICODE_WHITESPACE | HIGH | Unicode 空白字符混淆 |

### 2. Code Execution（代码执行）

| 规则 ID | 严重度 | 防护目标 |
|---------|--------|----------|
| TOOL_CMD_PIPE_TO_SHELL | CRITICAL | curl\|bash 远程代码执行 |
| TOOL_CMD_REVERSE_SHELL | CRITICAL | nc/bash -i 反弹 shell |
| TOOL_CMD_OBFUSCATED_EXEC | HIGH | base64 -d\|sh 混淆执行 |
| TOOL_CMD_PRIVILEGE_ESCALATION | CRITICAL | sudo/su/doas/pkexec 提权 |
| TOOL_CMD_JQ_SYSTEM | HIGH | jq 内置 system() 函数 |
| TOOL_CMD_JQ_FILE_FLAGS | HIGH | jq -f/-c 文件加载 |
| TOOL_CMD_ZSH_DANGEROUS | HIGH | zmodload/sysopen/ztcp |

### 3. Network Abuse（网络滥用）

| 规则 ID | 严重度 | 防护目标 |
|---------|--------|----------|
| TOOL_WEBFETCH_LOCAL_LOOPBACK | HIGH | 127.0.0.1/169.254.169.254 SSRF |
| TOOL_WEBFETCH_FILE_SCHEME | HIGH | file:///gopher:///ftp:// |

### 4. Sensitive File Access（敏感文件访问）

| 规则 ID | 严重度 | 防护目标 |
|---------|--------|----------|
| TOOL_CMD_PROC_ENVIRON | HIGH | /proc/*/environ 凭据泄露 |

### 5. Shell Evasion（Shell 逃逸）

| 规则 ID | 严重度 | 防护目标 |
|---------|--------|----------|
| SHELL_EVASION_COMMAND_SUBSTITUTION | HIGH | $()、\`\`、<()、=() 替换 |
| SHELL_EVASION_OBFUSCATED_FLAGS | HIGH | $'...' ANSI-C 引用混淆 |
| SHELL_EVASION_BACKSLASH_WHITESPACE | HIGH | 反斜杠转义空白绕过 |
| SHELL_EVASION_BACKSLASH_OPERATOR | HIGH | 反斜杠转义操作符绕过 |
| SHELL_EVASION_NEWLINE | HIGH | 换行隐藏第二条命令 |
| SHELL_EVASION_COMMENT_QUOTE_DESYNC | HIGH | # 注释中引号使解析器错位 |

## 关键设计

### 白名单机制（excludePatterns）

规则支持 `excludePatterns` 字段，允许特定安全操作通过：
- 例：`TOOL_CMD_DANGEROUS_RM` 可配置白名单 `rm -rf node_modules`、`rm *.tmp`
- 白名单优先级高于规则匹配

### 决策链

```
规则命中 → 检查 excludePatterns → 评估严重度
  ├─ CRITICAL → 直接阻断，返回 remediation 建议
  ├─ HIGH → 根据 feature-config 决定：阻断 / 询问用户 / 降级放行
  └─ 无命中 → 放行
```

### 双语支持

每条规则包含：
- `description`：英文技术描述
- `description_zh`：中文描述
- `remediation`：修复/替代建议

### 工具粒度匹配

- **Bash 工具**：匹配所有 `TOOL_CMD_*` 和 `SHELL_EVASION_*` 规则
- **WebFetch 工具**：仅匹配 `TOOL_WEBFETCH_*` 规则

## 与 QoderCLI 的关系

Tool Guard 通过 `qoderwake_permission_guard` Hook 注入到底层 QoderCLI 的执行流程中。QoderCLI 自身的 [[cli-permission-model]] 提供 5 种权限模式，Tool Guard 是在此之上的**额外安全层**——即使 CLI 处于 `auto` 模式，Tool Guard 仍可阻断 CRITICAL 级别操作。

## 交叉引用

- [[waker-permission]] — Waker 权限模型的整体设计
- [[waker-hook-lifecycle]] — Hook 生命周期中 Tool Guard 的触发位置
- [[permission-model]] — Cloud Agents 的权限模型（对比参考）
- [[cli-permission-model]] — QoderCLI 的 5 种权限模式

## 来源

- ~/.qoderwake/resources/security/tool-guard-rules/dangerous_shell_commands.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/workers/*/. qoder-plugin/hooks/hooks.json [reverse-engineering] 2026-06-30
