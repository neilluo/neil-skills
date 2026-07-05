# 快速开始

> 5 步跑通你的第一个 Qoder Cloud Agent。

全程只需 curl，无需安装任何 SDK。

## 前置条件

* 一个 Qoder 账号
* 终端环境（macOS / Linux / WSL）
* `curl` 和 `jq`（可选，用于格式化 JSON）

## 获取 PAT

1. 登录 [Qoder 控制台](https://qoder.com)
2. 依次点击 **设置 → 个人访问令牌**
3. 点击 **创建令牌**，设置名称和有效期
4. 导出为环境变量：

```bash
export QODER_PAT="your-personal-access-token"
```

> 令牌只在创建时显示一次，请立即保存。建议写入 `~/.bashrc` 或 `~/.zshrc`。

## 创建第一个 Session

### 步骤 1：选择环境

```bash
ENV_ID=$(curl -s https://api.qoder.com/api/v1/cloud/environments \
  -H "Authorization: Bearer $QODER_PAT" | jq -r '.data[0].id')
echo "环境 ID: $ENV_ID"
```

如果返回空数组，先创建一个默认环境：

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/environments \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"name":"default","config":{"type":"cloud","networking":{"type":"unrestricted"}}}'
```

### 步骤 2：创建 Agent

```bash
AGENT_RESPONSE=$(curl -s -X POST https://api.qoder.com/api/v1/cloud/agents \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-first-agent",
    "model": "ultimate",
    "system": "你是一个高效的编程助手，擅长代码编写和问题排查。",
    "tools": [
      {
        "type": "agent_toolset_20260401",
        "enabled_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
      }
    ]
  }')
AGENT_ID=$(echo "$AGENT_RESPONSE" | jq -r '.id')
echo "Agent ID: $AGENT_ID"
```

### 步骤 3：创建 Session

```bash
SESSION_RESPONSE=$(curl -s -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d "{
    \"agent\": \"$AGENT_ID\",
    \"environment_id\": \"$ENV_ID\"
  }")
SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.id')
echo "Session ID: $SESSION_ID"
```

> Session 创建后处于 `idle` 状态，需要发送消息后 Agent 才会开始执行。

### 步骤 4：发消息并接收事件流

```bash
# 发送消息
curl -s -X POST "https://api.qoder.com/api/v1/cloud/sessions/$SESSION_ID/events" \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "type": "user.message",
        "content": [{"type": "text", "text": "用 Python 写一个计算斐波那契数列的函数，并运行测试。"}]
      }
    ]
  }'

# 通过 SSE 流实时接收事件
curl -s -N "https://api.qoder.com/api/v1/cloud/sessions/$SESSION_ID/events/stream" \
  -H "Authorization: Bearer $QODER_PAT"
```

## 流程解析

发送 `user.message` 后，平台会：

1. **接收消息** — Session 从 `idle` 转入 `processing`（发出 `session.status_running`）
2. **启动模型请求** — 调用绑定的 Agent（发出 `span.model_request_start`）
3. **流式输出** — `agent.thinking` 是推理过程，`agent.message` 是回复正文，`agent.tool_use` 和 `agent.tool_result` 对应每次工具调用
4. **保持连接** — 定期发送 `heartbeat`（约 15 秒一次）
5. **结束本轮** — 发出 `span.model_request_end` 和 `session.status_idle`。可继续发消息。

## 常见问题

**Q: 提示 401 Unauthorized？**
A: 检查 `$QODER_PAT` 是否已正确设置，令牌是否过期。

**Q: 创建 Agent 返回 400 Bad Request？**
A: 检查请求体 JSON 格式，`model` 字段是否为有效值（如 `"ultimate"`），`tools` 是否为数组。

**Q: Session 一直处于 idle？**
A: 必须向 Session 发送 `user.message` 事件才会触发执行。

**Q: SSE 流连接中断？**
A: 重连时带 `?after_id=<last_event_id>` 查询参数，从断点继续。

**Q: GET /environments 返回空数组？**
A: 新账号没有预置环境，需手动创建。
