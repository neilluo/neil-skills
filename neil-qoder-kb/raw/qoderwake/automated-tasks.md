# 自动任务

> 让员工按定时、事件或 API 触发自动开工，并支持通过 PAT 调用 API 触发任务。

自动任务让员工自己跑起来，适合"每天跑一次"、"监听某个仓库变化就自动响应"这类场景。

进入 **Waker 详情 → 触发任务 → 新建**，可配置：

* **任务名和描述**：员工读了就知道要做什么。
* **AI 模型**：选哪个模型。
* **工作目录**：在本地哪个目录、哪个仓库或哪个项目工作区里执行。
* **触发方式**（最多 5 种，可混用）：
  * **定时**：一次性 / 周期性 / 复杂周期（每天 9 点、每周一、每月 1 号等）。
  * **事件驱动**：监听 GitHub 仓库的 Issue / PR / 评论变化。
  * **API 触发**：通过 HTTP 调用从外部系统触发任务执行，适合 CI、Webhook、内部平台集成。
* **最大次数 / 截止日期**（可选）：限制任务不要无限跑。

保存后，员工按你设的节奏自动干活。你可以随时暂停 / 启用、立即运行测试、查看运行历史。

## 通过 API 触发任务

QoderWake API 使用 **PAT（Personal Access Token，个人访问令牌）** 进行身份认证。所有 API 请求必须在 HTTP 头中携带有效的 PAT。

### 获取 PAT

1. **登录 Qoder 控制台**：访问 [Qoder 控制台](https://qoder.com) 并登录账号。
2. **进入服务集成**：打开 **个人设置 → 服务集成**。
3. **新建令牌**：点击 **新建令牌**，设置名称与过期时间。
4. **复制并保存令牌**：复制生成的令牌（仅显示一次）。PAT 以 `pt-` 前缀开头，格式如 `pt-your-token-here`。

> **警告**：请勿将 PAT 提交到代码仓库或公开分享。

### Bearer 头格式

在每个请求的 `Authorization` 头中以 Bearer 方式传递 PAT：

```plaintext
Authorization: Bearer pt-your-token-here
```

### 调用示例

用下面的 `curl` 请求触发指定自动任务。`<auto_generate_invoke_key>` 是创建自动任务时由系统生成的调用 key，可在任务详情页获取。

```bash
curl -X POST 'https://api.qoder.com/v1/qoderwake/automation/invoke/<auto_generate_invoke_key>' \
  --header 'Authorization: Bearer pt-your-token-here' \
  --header 'Content-Type: application/json' \
  --data '{
    "prompt": "your appended prompt here"
  }'
```

请求体中的 `prompt` 是本次调用追加给员工的提示词，会与任务描述合并后传递。
