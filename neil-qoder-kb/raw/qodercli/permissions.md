# 权限

> 来源: https://docs.qoder.com/zh/cli/permissions

## 权限模式

| 模式 | 适用场景 | 行为 |
|------|---------|------|
| default | 常规交互式使用 | 安全读取自动执行；敏感操作请求确认 |
| accept_edits | 日常编码任务 | 自动批准安全文件编辑；Shell 命令仍检查 |
| auto | 自动化运行、Goal 执行 | 零弹窗；风险动作被拒绝或 AI 分类器判断 |
| bypass_permissions (YOLO) | 可信本地实验 | 跳过所有批准提示 |
| dont_ask | headless 流程 | 从不询问；需确认的动作被拒绝 |

### Plan 模式
独立工作状态，可与任意权限模式共存。`/plan` 进入/退出。只读探索+输出方案。

### Goal 模式
自主执行状态。`/goal set <目标>` 进入，自动切 auto 模式。

### 切换
- Shift+Tab：循环切换权限模式
- Ctrl+Y：直达 YOLO 模式
- `--permission-mode <mode>`：启动参数指定

## 权限决策

三种结果：allow（立即执行）、ask（需确认）、deny（阻止）

### 决策顺序
1. 检查 deny 规则
2. 工具自身安全检查
3. ask 规则
4. allow 规则和模式自动允许
5. 最终 ask 由运行环境消费

## 规则配置

配置位置：
- `~/.qoder/settings.json` — 用户级
- `${project}/.qoder/settings.json` — 项目级
- `${project}/.qoder/settings.local.json` — 本地项目级

规则语法：
```json
{
  "permissions": {
    "allow": ["Read", "Bash(git *)"],
    "deny": ["Bash(rm -rf *)"],
    "ask": ["Write(*.env)"]
  }
}
```

工具名支持通配符 `*`，Bash 工具支持参数匹配 `Bash(pattern)`。
