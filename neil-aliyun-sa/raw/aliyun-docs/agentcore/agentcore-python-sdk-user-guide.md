---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-python-sdk-user-guide
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-python-sdk-user-guide
body_sha256: 05c7c55f20fff4cf248102e1019b6bdfd059eca28e1650193fccc330c3981d2c
body_bytes: 24534
migration_status: current
---

本文介绍使用 Python 调用 AgentCore 模型、MCP、Skill、记忆和凭证，以及通过框架构建 Agent 服务的方法。云端资源示例在 AgentCore 托管环境中运行，自定义资源示例由应用提供连接配置。

## 前提条件
1. 已开通 AgentCore，并创建 Workspace。具体操作，请参见[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)。

2. 已根据需要在 Agent 所属的 Workspace 中准备资源，并确认 Agent 具有相应访问权限。

3. 使用云端资源的示例在 AgentCore 托管的应用运行环境中执行。SDK 从运行环境获取访问配置，无需在业务代码中填写平台访问密钥。

本文使用以下示例资源名称。请替换为您实际创建的资源名称。
<table> <thead> <tr> <td> <p>资源</p> </td> <td> <p>示例值</p> </td> <td> <p>使用场景</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>模型连接</p> </td> <td> <p><code>my-model-connection</code></p> </td> <td> <p>调用模型。请参见<a href="https://help.aliyun.com/document_detail/3052299.html">管理模型</a>。</p> </td> </tr> <tr> <td> <p>模型</p> </td> <td> <p><code>qwen3.8-max</code></p> </td> <td> <p>必须已配置在所选模型连接中。框架工具示例还要求模型支持工具调用。</p> </td> </tr> <tr> <td> <p>MCP 服务</p> </td> <td> <p><code>my-mcp</code></p> </td> <td> <p>调用工具。请参见<a href="https://help.aliyun.com/document_detail/3052308.html">管理 MCP 工具</a>。</p> </td> </tr> <tr> <td> <p>Skill</p> </td> <td> <p><code>my-skill</code></p> </td> <td> <p>使用已启用且有已发布版本的 Skill。请参见<a href="https://help.aliyun.com/document_detail/3052296.html">管理 Skill</a>。</p> </td> </tr> <tr> <td> <p>MemoryStore</p> </td> <td> <p><code>my-memory</code></p> </td> <td> <p>使用记忆功能时需要。</p> </td> </tr> <tr> <td> <p>凭证</p> </td> <td> <p><code>my-api-key</code>、<code>my-mcp-header</code></p> </td> <td> <p>按需创建 API Key 凭证或 MCP Header 凭证。具体操作，请参见<a href="https://help.aliyun.com/document_detail/3052318.html">管理凭证</a>。</p> </td> </tr> </tbody> </table>

只调用模型时，无需创建 MCP、Skill、MemoryStore 或额外凭证。

## 安装 SDK
基础 SDK 支持 Python 3.10 及以上版本。本文的 LangChain 服务示例使用 Python 3.11 及以上版本。

```
HELPCODEESCAPE-bash
pip install alibabacloud-agentcore-sdk==0.1.1
```

使用 MCP、HTTP 服务、凭证或框架集成时，按需安装扩展依赖：

```
HELPCODEESCAPE-bash
pip install "alibabacloud-agentcore-sdk[mcp,server,credentials,langchain]==0.1.1"
```

<table> <thead> <tr> <td> <p>扩展依赖</p> </td> <td> <p>用途</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>mcp</code></p> </td> <td> <p>连接 MCP 服务。</p> </td> </tr> <tr> <td> <p><code>server</code></p> </td> <td> <p>使用 AgentCoreServer。</p> </td> </tr> <tr> <td> <p><code>credentials</code></p> </td> <td> <p>读取托管凭证、绑定 MCP Header 凭证。</p> </td> </tr> <tr> <td> <p><code>langchain</code>、<code>langgraph</code></p> </td> <td> <p>对应框架集成。</p> </td> </tr> <tr> <td> <p><code>agentscope</code></p> </td> <td> <p>AgentScope 2.x 集成，需要 Python 3.11 及以上版本。</p> </td> </tr> <tr> <td> <p><code>google-adk</code>、<code>pydantic-ai</code>、<code>crewai</code></p> </td> <td> <p>对应框架集成。框架本身可能有额外的 Python 版本要求。</p> </td> </tr> </tbody> </table>

Python 的安装包名为 `alibabacloud-agentcore-sdk`，代码中的导入名称为 `agentcore`。

本文示例使用 Python SDK `0.1.1`。后续版本请参见 [PyPI](https://pypi.org/project/alibabacloud-agentcore-sdk/)。

## 调用云端模型
在代码中指定模型连接名称和模型名称。SDK 根据当前 Agent 所属的 Workspace 查找模型连接，无需手动拼接模型访问地址。

```
HELPCODEESCAPE-python
import asyncio
from agentcore import AsyncAgentCore

async def main():
    async with AsyncAgentCore.auto() as core:
        model = await core.model("my-model-connection", model="qwen3.8-max")
        response = await model.invoke(
            [{"role": "user", "content": "用一句话介绍杭州。"}],
            temperature=0.2,
        )
        print(response["choices"][0]["message"]["content"])

asyncio.run(main())
```

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>my-model-connection</code></p> </td> <td> <p>模型连接的名称，不是模型名称，也不是模型连接 ID。</p> </td> </tr> <tr> <td> <p><code>model</code></p> </td> <td> <p>该连接中已配置的模型名称。</p> </td> </tr> <tr> <td> <p><code>temperature</code></p> </td> <td> <p>本次生成使用的参数。是否支持及取值范围以实际模型为准。</p> </td> </tr> </tbody> </table>

### 流式输出

在前述 Core 生命周期内，用以下代码替换普通调用。普通调用和流式调用是两次独立请求，按需选择一种。

```
HELPCODEESCAPE-python
async for chunk in model.stream([{"role": "user", "content": "用一句话介绍杭州。"}]):


    for choice in chunk.get("choices", [ ]):


        print(choice.get("delta", {}).get("content") or "", end="", flush=True)
```

> **说明** ：上述文本解析示例适用于 OpenAI/v1 协议。Anthropic 模型返回其对应协议的数据结构，不应使用 `choices` 解析。OpenAI/v1 连接可使用 `responses()` 和 `responses_stream()`。实际模型必须支持 Responses API；SDK 不会在调用失败时自动切换为 Chat Completions。当前托管模型客户端不提供 Embedding 调用。自定义模型客户端的 `embedding()` 仅适用于支持向量生成的服务和模型。

## 使用 MCP 工具
以下片段在已创建的 `core` 生命周期内执行。获取工具列表只用于发现工具，不会执行工具。

```
HELPCODEESCAPE-python
mcp = await core.mcp("my-mcp")
available_tools = await mcp.list_tools()
for tool in available_tools:
    print(tool.name, tool.description, tool.parameters)

# 替换为该 MCP 实际提供的工具名称和参数。
result = await mcp.call_tool("<工具名称>", {"<参数名称>": "<参数值>"})
```

如需让模型选择并执行工具，请使用后文的框架集成示例。模型调用本身不会自动执行 MCP 工具。

## 使用 Skill
Skill 包含任务说明和可选的辅助文件或脚本。加载 Skill 后，通过框架适配器将其接入 Agent。

```
HELPCODEESCAPE-python
skill = await core.skills.managed("my-skill", version="1.0.0")
print(skill.name, skill.version)
```

`1.0.0` 必须是该 Skill 已发布的版本。省略版本时使用平台解析出的默认版本。需要固定应用行为时，建议显式指定版本。
> **重要** ：加载 Skill 不等于执行 Skill。Skill 工具可能执行包内脚本或命令，仅使用可信来源的 Skill。不需要命令执行能力时，在应用运行环境中设置 `ALLOW_EXECUTE_COMMAND=false`。Skill 执行所需的程序和依赖仍需包含在应用运行环境中。

## 使用记忆
MemoryStore 用于保存和检索长期记忆。它与模型输入的对话历史是不同的能力：检索到记忆后，需要由业务代码或框架适配器将其作为参考信息提供给模型。

### 写入和检索记忆

以下片段在已创建的 `core` 生命周期内执行。示例会写入数据，请使用适合验证的 MemoryStore。

```
HELPCODEESCAPE-python
from agentcore.memory import MemoryScope

store = core.memory_store("my-memory")
await store.add_memories(
    scope=MemoryScope(user_id="example-user", session_id="example-session"),
    text="用户喜欢简短的中文回答。",
)

result = await store.search_memories(
    "用户有哪些回答偏好？",
    scope=MemoryScope(user_id="example-user"),
    top_k=5,
)
for hit in result.memories:
    print(hit.memory.content.text)
```

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>user_id</code></p> </td> <td> <p>业务用户的逻辑标识。用于按用户组织记忆。</p> </td> </tr> <tr> <td> <p><code>agent_id</code></p> </td> <td> <p>Agent 的逻辑标识。可按业务定义，不要求每次调用都提供。</p> </td> </tr> <tr> <td> <p><code>session_id</code></p> </td> <td> <p>会话标识。写入时可标记记忆来源；检索时传入则限定到该会话。</p> </td> </tr> <tr> <td> <p><code>top_k</code></p> </td> <td> <p>检索返回的结果数量上限。</p> </td> </tr> </tbody> </table>

使用时注意：

* MemoryStore 所属的 Workspace 来自 Core 的资源上下文，通常无需在每次记忆调用时重复传入。

* 写入时，三个范围字段均可省略，未传字段归入服务端默认范围；查询时，未传字段不限制该维度。多用户应用应显式传入所需范围，避免检索到不应共享的记忆。

* 跨会话使用用户偏好时，通常按用户写入，检索时不限定 `session_id`。

* 范围字段应由可信的业务上下文提供，不应让模型任意生成或修改。它们用于逻辑分区，不是访问凭证或权限校验的替代品。

* 新写入的记忆可能需要一定时间才能检索到。不要因为首次查询为空，就反复写入相同内容。

* 查询会话消息使用 `list_memory_session_messages()`；需要会话 ID，且用户 ID、Agent ID 至少提供一个。

### 接入框架执行流程

框架适配器可在模型执行前检索记忆，并按配置在执行后写回。仅接入模型或工具适配器不会自动启用记忆。
<table> <thead> <tr> <td> <p>框架</p> </td> <td> <p>入口</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>LangChain</p> </td> <td> <p><code>agentcore.integrations.memory.langchain</code></p> </td> </tr> <tr> <td> <p>LangGraph</p> </td> <td> <p><code>agentcore.integrations.memory.langgraph</code></p> </td> </tr> <tr> <td> <p>AgentScope 2.x</p> </td> <td> <p><code>agentcore.integrations.memory.agentscope</code></p> </td> </tr> <tr> <td> <p>Google ADK</p> </td> <td> <p><code>agentcore.integrations.memory.google_adk</code></p> </td> </tr> <tr> <td> <p>PydanticAI</p> </td> <td> <p><code>agentcore.integrations.memory.pydantic_ai</code></p> </td> </tr> <tr> <td> <p>CrewAI</p> </td> <td> <p><code>agentcore.integrations.memory.crewai</code></p> </td> </tr> </tbody> </table>

各框架的生命周期不同，记忆写入应接入对应的中间件、节点或会话保存接口，不要把整段历史在每个模型调用后重复提交。

## 使用凭证和 MCP Header
### 获取托管凭证

在平台创建凭证并授权后，可按名称读取。以下片段在 `core` 生命周期内执行。

```
HELPCODEESCAPE-python
credential = await core.credentials.get("my-api-key")
api_key = credential.value  # 交给需要该凭证的客户端，不要输出。

header_credential = await core.credentials.get("my-mcp-header")
headers = header_credential.as_headers()
```

API Key 凭证使用 `value`，MCP Header 凭证使用 `as_headers()`。不要把凭证值写入源代码、日志或对外响应。

### 为 MCP 绑定凭证

```
HELPCODEESCAPE-python
mcp = await core.mcp(
    "my-mcp",
    credential_name="my-mcp-header",
    headers={"x-business-id": "my-app"},
)
```

`credential_name` 和 `headers` 均可省略。绑定的 MCP Header 凭证必须允许应用到该 MCP。
> **重要** ： `headers` 是客户端级固定配置，作用于 MCP 握手、工具发现和工具调用，不是每次请求的用户身份参数。不要在共享客户端上修改 Header 来切换用户。Header 名称大小写不敏感。平台 Header、凭证 Header、自定义 Header 发生冲突时会报错，不进行覆盖；不能覆盖 `Authorization` 等平台认证字段，也不能手动设置 `Host`、 `Mcp-Session-Id` 等协议字段。SDK 不会自动复制全部入站 Header。

## 接入自定义资源
自有模型、MCP 服务和随应用分发的 Skill 无需注册为平台资源。以下配置由应用自己提供，示例中的环境变量不是 SDK 自动读取的配置项。

```
HELPCODEESCAPE-python
import asyncio
import os
from agentcore import AsyncAgentCore

async def main():
    async with AsyncAgentCore() as core:
        model = core.direct_model(
            provider="openai",
            model=os.environ["CUSTOM_MODEL_NAME"],
            base_url=os.environ["CUSTOM_MODEL_BASE_URL"],
            api_key=os.environ["CUSTOM_MODEL_API_KEY"],
        )
        response = await model.invoke([{"role": "user", "content": "你好"}])
        print(response["choices"][0]["message"]["content"])

        mcp = core.direct_mcp(url=os.environ["CUSTOM_MCP_URL"])
        print([tool.name for tool in await mcp.list_tools()])
        skills = await core.skills.local("./skills")
        print([skill.name for skill in skills])

asyncio.run(main())
```

<table> <thead> <tr> <td> <p>配置</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><code>CUSTOM_MODEL_NAME</code></p> </td> <td> <p>自有服务支持的模型名称。</p> </td> </tr> <tr> <td> <p><code>CUSTOM_MODEL_BASE_URL</code></p> </td> <td> <p>模型 API Base URL。OpenAI 兼容服务通常包含 <code>/v1</code>，以服务说明为准。</p> </td> </tr> <tr> <td> <p><code>CUSTOM_MODEL_API_KEY</code></p> </td> <td> <p>模型服务的 API Key。通过运行环境或密钥管理方式提供。</p> </td> </tr> <tr> <td> <p><code>CUSTOM_MCP_URL</code></p> </td> <td> <p>MCP 服务的完整访问地址。默认使用 Streamable HTTP；SSE 服务需显式设置 <code>transport="sse"</code>。</p> </td> </tr> <tr> <td> <p><code>./skills</code></p> </td> <td> <p>随应用分发的 Skill 目录。单个 Skill 应包含 <code>SKILL.md</code> 及其引用的文件。</p> </td> </tr> </tbody> </table>

直连 MCP 需要鉴权时，可通过 `headers_provider` 提供 Header；stdio 传输不使用 HTTP Header。

## 使用 LangChain 构建 Agent 服务
以下示例将云端模型、MCP 和 Skill 接入 LangChain，并通过 AgentCoreServer 提供服务。使用前请准备 `my-model-connection`、`my-mcp`、`my-skill`，并按前文安装框架依赖。

示例处理最新一条用户文本，未实现对话历史存储。多轮会话应由应用或框架维护历史和检查点。

保存为 `app.py`：

```
HELPCODEESCAPE-python
import logging
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from agentcore import AsyncAgentCore
from agentcore.integrations.langchain import AgentCoreConverter, model, skill_tools, tools
from agentcore.server import AgentCoreServer

logging.basicConfig(level=logging.INFO)
core = None
chat = None
agent = None

async def shutdown():
    try:
        if chat is not None:
            await chat.root_async_client.close()
            chat.root_client.close()
    finally:
        if core is not None:
            await core.aclose()

async def startup():
    global core, chat, agent
    core = AsyncAgentCore.auto()
    try:
        mcp = await core.mcp("my-mcp")
        skill = await core.skills.managed("my-skill")
        chat = model("my-model-connection", model_name="qwen3.8-max")
        agent = create_agent(
            model=chat,
            tools=[*tools(await mcp.list_tools()), *skill_tools([skill])],
            system_prompt="使用工具完成请求，不要编造工具执行结果。",
        )
    except Exception:
        logging.exception("Agent 初始化失败")
        await shutdown()
        raise

server = AgentCoreServer(
    startup=startup,
    shutdown=shutdown,
    readiness=lambda: agent is not None,
)

@server.invoke
async def invoke(request, context):
    if not request.messages:
        raise ValueError("请提供用户消息")
    message = request.messages[-1]
    if message.role.value != "user" or not isinstance(message.content, str):
        raise ValueError("本示例仅支持用户文本消息")
    events = agent.astream_events(
        {"messages": [HumanMessage(content=message.content)]},
        version="v2",
    )
    async for event in AgentCoreConverter().stream(events):
        yield event
```

在应用运行环境中使用以下启动命令：

```
HELPCODEESCAPE-bash
uvicorn app:server --host 0.0.0.0 --port 9000
```

示例按 OpenAI/v1 模型连接编写，关闭逻辑也对应该示例的 LangChain OpenAI 客户端。

### 部署配置

将应用代码及依赖打包并部署到 AgentCore。运行环境需包含前述 SDK 和框架依赖；如使用容器镜像，应在构建镜像时安装依赖。
<table> <thead> <tr> <td> <p>配置</p> </td> <td> <p>本文示例值</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>监听地址</p> </td> <td> <p><code>0.0.0.0</code></p> </td> </tr> <tr> <td> <p>服务端口</p> </td> <td> <p><code>9000</code></p> </td> </tr> <tr> <td> <p>Python 启动命令</p> </td> <td> <p><code>uvicorn app:server --host 0.0.0.0 --port 9000</code></p> </td> </tr> <tr> <td> <p>存活检查</p> </td> <td> <p><code>GET /healthz</code></p> </td> </tr> <tr> <td> <p>就绪检查</p> </td> <td> <p><code>GET /readyz</code></p> </td> </tr> </tbody> </table>

平台配置的端口应与应用实际监听端口一致。SDK 不执行代码上传、镜像构建或应用部署。

## 调用 Agent 服务
将下面的 `https://<agent-endpoint>` 替换为应用实际访问地址，并按应用的访问要求补充认证信息。该地址是 Agent 应用地址，不是模型供应商地址。

### AG-UI

```
HELPCODEESCAPE-bash
curl -N 'https://<agent-endpoint>/ag-ui/agent' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "example-thread-1",
    "runId": "example-run-1",
    "messages": [{"id": "message-1", "role": "user", "content": "查看可用 Skill，并按其说明完成一个示范。"}],
    "state": {},


    "tools": [ ],



    "context": [ ],


    "forwardedProps": {}
  }'
```

每次运行使用新的 `runId`。同一对话可以复用 `threadId`，但它不会让上述示例自动保存历史。请求中的 `tools: [ ]` 不会禁用 Agent 代码中已配置的工具。

正常执行以 `RUN_STARTED` 开始，以 `RUN_FINISHED` 结束。发生工具调用时，会输出工具调用和结果事件，并通过相同的 `toolCallId` 关联。是否调用工具由模型和任务决定。运行失败时输出 `RUN_ERROR`。

### OpenAI Chat Completions

```
HELPCODEESCAPE-bash
curl -N 'https://<agent-endpoint>/openai/v1/chat/completions' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "agentcore",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": true
  }'
```

流式响应以 `[DONE]` 结束。将 `stream` 改为 `false` 可获取单个 JSON 响应。

`model` 是 OpenAI 请求格式中的必填字段。本示例始终使用应用代码指定的模型连接，不会根据这个字段自动切换下游模型。查询应用的协议模型列表可使用 `GET /openai/v1/models`，该列表不是 Workspace 的模型目录。

### 协议选择

<table> <thead> <tr> <td> <p>内容</p> </td> <td> <p>AG-UI</p> </td> <td> <p>OpenAI Chat Completions</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>文本输出</p> </td> <td> <p>支持。</p> </td> <td> <p>支持。</p> </td> </tr> <tr> <td> <p>多条消息边界</p> </td> <td> <p>保留文本消息的开始、内容和结束事件。</p> </td> <td> <p>同一次 completion 的文本聚合到一条 assistant 消息。</p> </td> </tr> <tr> <td> <p>工具调用</p> </td> <td> <p>输出工具调用事件，保留调用 ID。</p> </td> <td> <p>输出 <code>tool_calls</code>。</p> </td> </tr> <tr> <td> <p>工具结果</p> </td> <td> <p>输出独立的工具结果事件。</p> </td> <td> <p>不提供独立的工具结果响应事件。</p> </td> </tr> <tr> <td> <p>适用场景</p> </td> <td> <p>展示 Agent 多步执行过程、工具调用与结果。</p> </td> <td> <p>接入使用 Chat Completions 格式的客户端。</p> </td> </tr> </tbody> </table>

两种协议的 SSE 在输出空闲 15 秒后发送心跳注释。心跳不是模型输出，也不表示业务执行已经完成。
> **重要** ：框架服务示例已在服务端执行工具。客户端不要将收到的工具调用轨迹再执行一次。需要完整执行过程时，应将框架完整事件流交给 `AgentCoreConverter`，不要只提取文本。每个请求创建独立转换器。转换器保留结构化消息边界和工具关联，不通过正文猜测消息类型。

## 其他框架集成
<table> <thead> <tr> <td> <p>框架</p> </td> <td> <p>入口</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>LangChain</p> </td> <td> <p><code>agentcore.integrations.langchain</code></p> </td> </tr> <tr> <td> <p>LangGraph</p> </td> <td> <p><code>agentcore.integrations.langgraph</code></p> </td> </tr> <tr> <td> <p>AgentScope 2.x</p> </td> <td> <p><code>agentcore.integrations.agentscope</code></p> </td> </tr> <tr> <td> <p>Google ADK</p> </td> <td> <p><code>agentcore.integrations.google_adk</code></p> </td> </tr> <tr> <td> <p>PydanticAI</p> </td> <td> <p><code>agentcore.integrations.pydantic_ai</code></p> </td> </tr> <tr> <td> <p>CrewAI</p> </td> <td> <p><code>agentcore.integrations.crewai</code></p> </td> </tr> </tbody> </table>

上述框架入口也提供执行事件转换器，输入应使用对应框架的完整事件流。例如 LangChain/LangGraph 使用 `astream_events(version="v2")`。

CrewAI 完整事件入口需要 CrewAI 1.15.20 及以上版本；其轨迹在执行完成后输出，不是逐 Token 实时输出。不同框架的事件输入和输出时机不同，不应直接复用另一框架的事件处理方式。

## 常见问题
### 找不到模型连接、MCP 或 Skill，如何排查？

检查应用所在 Workspace、资源名称和访问权限。模型连接名称与模型名称是两个参数；Skill 还需要检查是否已启用、所选版本是否已发布。不要用另一 Workspace 的资源 ID 替代名称。

### 为什么加载了 MCP 和 Skill，模型仍没有调用工具？

`list_tools()` 和 Skill 加载只完成资源准备。还需将工具交给 Agent 框架，并选择支持工具调用的模型。即使已配置工具，简单问题也可能不需要调用工具。

### 为什么首次检索不到刚写入的记忆？

记忆处理和可检索状态可能存在延迟。先检查写入是否成功及读写范围是否一致，稍后重新查询，不要直接重放写入操作。

### 相同会话 ID 是否会自动恢复历史？

不会。AgentCoreServer 负责协议接入，不替应用持久化对话历史。由应用或框架管理会话状态；长期记忆不能替代完整的会话历史或框架检查点。

### 必须使用 AgentCoreServer 吗？

不必。可以在现有 Web 服务或 Agent 执行器中使用模型、MCP、Skill、Memory 和凭证接口。使用 AgentCoreServer 只是复用其协议封装，不是调用云端资源的前提。

### 浏览器跨域访问失败，如何处理？

SDK 默认不放开跨域。由应用或接入网关按实际前端来源配置 CORS。不要将允许所有来源作为使用敏感凭证接口的默认配置。

### 如何记录排障日志？

可通过 `logging.basicConfig(level=logging.INFO)` 开启日志。保留错误堆栈、请求 ID 和失败操作，避免输出访问密钥、完整 Header 或用户敏感内容。

应用生命周期内复用 Core，退出时关闭。推荐使用异步上下文管理器，或调用 `await core.aclose()`。不要在每次 HTTP 请求结束后关闭其他请求仍在使用的共享 Core。

## 相关文档
* [管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)

* [管理模型](https://help.aliyun.com/document_detail/3052299.html)

* [管理 MCP 工具](https://help.aliyun.com/document_detail/3052308.html)

* [管理 Skill](https://help.aliyun.com/document_detail/3052296.html)

* [Python SDK 安装包](https://pypi.org/project/alibabacloud-agentcore-sdk/)