# 定义 Agent

> 创建可复用、可版本化的 Agent 配置。

Agent 是 Qoder Cloud Agents 的核心配置模板，描述了 AI 代理的能力边界。一个 Agent 可被多个 Session 复用；修改 Agent 不影响已运行的 Session。

## 核心要素

| 要素 | 含义 |
|------|------|
| **模型** | Agent 的智力水平 |
| **系统提示词** | Agent 的行为准则 |
| **工具集** | Agent 能执行的操作 |
| **Skills** | Agent 可调用的高级技能 |

## Agent 配置字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | — | 系统生成，`agent_` 前缀 + 32 字符十六进制 |
| `type` | string | — | 固定为 `"agent"` |
| `name` | string | 是 | Agent 名称（≤ 64 字符） |
| `description` | string | 否 | 描述信息，默认 `""` |
| `model` | string | 是 | 模型标识 |
| `system` | string | 否 | 系统提示词 |
| `tools` | array | 否 | 可用工具列表 |
| `skills` | array | 否 | 关联的 Skill ID 列表 |
| `mcp_servers` | array | 否 | MCP 服务器配置列表 |
| `metadata` | object | 否 | 自定义键值对 |
| `version` | integer | — | 版本号，从 1 开始递增 |
| `archived` | boolean | — | 是否已归档 |
| `created_at` | string | — | 创建时间 |
| `updated_at` | string | — | 最后更新时间 |

## 创建 Agent

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "code-reviewer",
    "model": "ultimate",
    "system": "你是代码审查专家。逐行审查代码并以 Markdown 输出问题与改进建议。",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "enabled_tools": ["Bash", "Read", "Write"]
      }
    ],
    "metadata": {
      "team": "backend",
      "purpose": "code-review"
    }
  }'
```

成功返回 **201 Created**，`version` 从 `1` 开始。

## 查询 Agent

```bash
# 获取单个 Agent
curl -s https://api.qoder.com/api/v1/cloud/agents/agent_xxx \
  -H "Authorization: Bearer $QODER_PAT"

# 分页列表
curl -s "https://api.qoder.com/api/v1/cloud/agents?limit=20" \
  -H "Authorization: Bearer $QODER_PAT"
```

## 更新 Agent

更新 Agent **必须**携带当前 `version`（乐观并发控制 OCC）：

```bash
curl -s -X PUT https://api.qoder.com/api/v1/cloud/agents/agent_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "code-reviewer",
    "model": "ultimate",
    "system": "你是资深代码审查专家，专注安全漏洞和性能问题。",
    "version": 1
  }'
```

成功返回 **200 OK**，`version` 自动 +1。

## 更新语义

* 创建时 `version` 从 `1` 开始
* 每次成功更新，`version` 自动 +1
* 缺少 `version` → 400 `invalid_request_error`
* `version` 不一致 → 409 `conflict_error`

### 处理 409 冲突

1. `GET` 最新 Agent 拿到当前 `version`
2. 合并自己的变更
3. 用新 `version` 重新 `PUT`

## 最佳实践

1. **命名规范** — 用 `团队-用途` 格式，如 `backend-code-review`
2. **提示词精炼** — `system` 写清角色、输出格式、限制条件
3. **最小工具集** — 只配置任务所需的工具
4. **善用 metadata** — 用标签分类管理
5. **生产环境锁版本** — 创建 Session 时用 `{"id": ..., "version": ...}` 形式

## 常见问题

**Q：更新 Agent 后，正在运行的 Session 会受影响吗？**
A：不会。Session 在创建时绑定了 Agent 的特定版本。

**Q：`tools` 数组为空可以吗？**
A：可以。不带工具的 Agent 只能进行纯文本对话。

**Q：如何回滚到旧版本的 Agent？**
A：目前不支持自动回滚。需手动 `PUT` 回旧配置（携带最新 `version`）。
