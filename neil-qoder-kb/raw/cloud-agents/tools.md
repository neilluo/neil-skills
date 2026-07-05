# Agent 工具

> 为 Agent 配备内置、MCP 和自定义工具。

工具决定了 Agent **能做什么**。通过 `tools` 字段精确控制 Agent 的能力边界。

## 可用工具

| 工具名 | 用途 | 典型场景 |
|--------|------|------|
| `Bash` | Shell 命令执行 | 安装依赖、运行脚本 |
| `Read` | 文件读 | 查看文件、代码阅读 |
| `Write` | 文件写（创建/覆盖） | 生成报告、产出物 |
| `Edit` | 文件局部编辑 | 改配置、改代码 |
| `Glob` | 通配符列文件 | 找代码文件 |
| `Grep` | 文件内容搜索 | 定位字符串 |
| `WebFetch` | HTTP GET 单页面 | 拉文档/页面 |
| `WebSearch` | 联网搜索 | 检索资料 |
| `DeliverArtifacts` | 投递产出文件给用户 | 文件/报告等可交付产物 |

## 配置格式

```json
{
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "enabled_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
    }
  ]
}
```

注意：
* `enabled_tools` 省略或空数组 = 启用全部内置工具
* 整个 `tools` 字段省略或 `[]` = Agent 完全没有工具
* `enabled_tools` 非空时是白名单，列表外的工具完全不可见

## 自定义 Client-Side 工具

```json
{
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "enabled_tools": ["Read", "Write"]
    },
    {
      "type": "custom",
      "name": "lookup_order",
      "description": "根据订单 ID 查询订单。",
      "input_schema": {
        "type": "object",
        "properties": {
          "order_id": {"type": "string"}
        },
        "required": ["order_id"]
      }
    }
  ]
}
```

自定义工具规则：
* `name`、`description`、`input_schema` 必填
* 调用时 Session 以 `requires_action` 暂停
* 客户端通过 `user.custom_tool_result` 回传结果
* 不能与内置工具名冲突
* `mcp__` 前缀保留给 MCP 工具

## 常见问题

**Q：不配置 tools 会怎样？**
A：Agent 没有工具，只能纯文本对话。

**Q：能否在 Session 级别覆盖工具？**
A：不支持。工具绑定在 Agent 上。

**Q：tools 数组顺序重要吗？**
A：不重要。Agent 自主决定调用哪个工具。
