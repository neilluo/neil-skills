# CLI Permission Model — 权限模型

> 五种权限模式和规则语法，控制工具调用的自动化程度与安全边界。

## 概述

权限模型决定 Qoder CLI 如何处理工具调用——在"自动化程度"和"安全宽松度"两个维度上定位。通过模式选择 + 规则配置 + 工具安全检查三层机制协同工作。

## 五种权限模式

| 模式 | 自动化 | 安全性 | 适用场景 |
|------|--------|--------|---------|
| `default` | 中 | 高 | 常规交互式使用 |
| `accept_edits` | 中高 | 中 | 日常编码（自动批准文件编辑） |
| `auto` | 高 | 中低 | Goal 执行、自动化运行 |
| `bypass_permissions` (YOLO) | 最高 | 最低 | 可信本地实验 |
| `dont_ask` | — | 高 | headless 流程（不弹窗，不确定就拒绝） |

## 特殊工作状态

- **Plan 模式**：只读探索 + 输出方案，可与任意权限模式共存。`/plan` 切换。
- **Goal 模式**：自主执行状态，自动切 `auto`。`/goal set <目标>` 进入。

## 模式切换

| 方式 | 说明 |
|------|------|
| Shift+Tab | 循环切换所有模式 |
| Ctrl+Y | 直达 YOLO |
| `--permission-mode <mode>` | 启动时指定 |
| `--yolo` | 快捷方式 = bypass_permissions |

## 权限决策顺序

```
deny 规则 → 工具安全检查 → ask 规则 → allow 规则/模式自动允许 → 最终 ask
```

三种结果：
- **allow** — 立即执行
- **ask** — TUI 弹窗/Headless 拒绝/Hooks 决定
- **deny** — 阻止执行

## 规则配置

配置位置（三级合并）：
```
~/.qoder/settings.json                    # 用户级
${project}/.qoder/settings.json           # 项目级
${project}/.qoder/settings.local.json     # 本地项目级
```

语法：
```json
{
  "permissions": {
    "allow": ["Read", "Bash(git *)"],
    "deny": ["Bash(rm -rf *)"],
    "ask": ["Write(*.env)"]
  }
}
```

支持通配符 `*`，Bash 工具支持参数模式匹配。

## 交叉引用

- [[cli-session]] — 会话中的权限模式设置
- [[cli-hook-system]] — Hooks 可介入权限决策（退出码 2 = 阻止）
- [[cli-subagent]] — 每个 Subagent 可独立设置权限模式
- [[cli-tool-mcp]] — MCP 工具同样经过权限系统
- [[permission-model]] — Cloud Agents 的权限模型对比

## 来源

- raw/qodercli/permissions.md [official-docs]
