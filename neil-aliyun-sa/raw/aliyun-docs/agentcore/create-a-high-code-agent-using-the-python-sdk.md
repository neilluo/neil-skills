---
source_url: https://help.aliyun.com/zh/agentcore/create-a-high-code-agent-using-the-python-sdk
fetch_date: 2026-09-20
product: AgentCore
slug: create-a-high-code-agent-using-the-python-sdk
body_sha256: e74085330d8a8250db88951a7be06475887a0fac1afda87b24f0fdf1b87fa0df
body_bytes: 7525
migration_status: current
---

本文介绍如何使用 AgentCore Python SDK 构建一个调用平台模型的 Agent，并通过容器镜像部署到 AgentCore，在控制台验证对话结果。  

## 准备工作
* 已开通 AgentCore 服务，并创建 Workspace。

* 已在本地安装并启动 Docker。

* 已准备企业版容器镜像服务 ACR 实例和镜像仓库，并具备镜像推送权限。

## 镜像要求
<table> <thead> <tr> <td> <p>检查项</p> </td> <td> <p>要求</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>镜像架构</p> </td> <td> <p>必须支持 <code>linux/amd64</code>（x86_64）。不要使用仅支持 <code>arm64</code> 的镜像。</p> </td> </tr> <tr> <td> <p>Shell 环境</p> </td> <td> <p>必须同时提供 <code>/bin/bash</code> 和 <code>/bin/sh</code>，且两者均可执行。</p> </td> </tr> <tr> <td> <p>镜像仓库</p> </td> <td> <p>当前仅支持企业版 ACR。实例需开启公开匿名拉取，镜像仓库需设为公开。不要将密钥或业务数据打入公开镜像。</p> </td> </tr> <tr> <td> <p>网络可达</p> </td> <td> <p>镜像仓库必须从 Agent 运行环境网络可达，并允许平台拉取镜像。本地能够推送镜像，不代表云端能够拉取。</p> </td> </tr> </tbody> </table> **说明**：未开启「允许访问 VPC」时，通过公网拉取镜像。如 ACR 实例配置了公网访问白名单，请将目标 Workspace 的公网出口 IP 加入白名单；该 IP 可在 Agent 创建页的「网络配置」中查看。开启「允许访问 VPC」后，平台会尝试通过 VPC 拉取镜像，需确保 ACR 的网络访问配置允许该 VPC 访问。

## 步骤 1：配置模型连接
> **说明**：已有可用模型连接时，可跳过本步骤。记录模型连接名称及其中的模型名称，后续在代码中引用。

1. 登录[AgentCore](https://agentcore.console.aliyun.com/)控制台，选择目标 Workspace。

2. 在左侧导航栏单击**模型连接** ，单击**添加模型连接**。

3. 选择模型供应商，模型连接名称填写 `content-model`，按供应商要求配置 API 端点和 API Key。

4. 在**模型配置** 中选择 `qwen3.8-max`，保存连接并验证模型可用性。模型配置的详细操作，请参见[管理模型](https://help.aliyun.com/document_detail/3052299.html)。

## 步骤 2：创建应用文件
在本地新建项目目录，并创建以下四个文件。示例使用模型连接 `content-model` 和模型 `qwen3.8-max`；使用其他资源时，替换 `app.py` 中 `core.model(...)` 的对应参数。

### app.py：应用入口

```
HELPCODEESCAPE-python
import logging

from agentcore import AsyncAgentCore
from agentcore.server import AgentCoreServer

logging.basicConfig(level=logging.INFO)
core = AsyncAgentCore.auto()
model_client = None


async def startup():
    global model_client
    try:
        # 改为当前 Workspace 中的模型连接名称和模型名称。
        model_client = await core.model("content-model", model="qwen3.8-max")
    except Exception:
        logging.exception("Agent 启动失败")
        await core.aclose()
        raise


server = AgentCoreServer(
    startup=startup,
    shutdown=core.aclose,
    readiness=lambda: model_client is not None,
)


@server.invoke
async def invoke(request, context):
    messages = [
        {"role": message.role.value, "content": message.content}
        for message in request.messages
    ]
    response = await model_client.invoke(messages)
    return response["choices"][0]["message"]["content"]
```

应用通过 `core.model()` 获取模型客户端，调用模型后返回回答。`AgentCoreServer` 提供 AG-UI 和 OpenAI Chat Completions 服务接口。
> **说明**：本示例返回模型生成的完整回答，不演示逐字输出或工具调用。应用转发请求中已有的对话消息，不额外保存聊天历史。

### requirements.txt：依赖声明

```
HELPCODEESCAPE-text
alibabacloud-agentcore-sdk[server]==0.1.1
```

### Dockerfile：镜像构建配置

```
HELPCODEESCAPE-dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 9000
CMD ["uvicorn", "app:server", "--host", "0.0.0.0", "--port", "9000"]
```

> **说明**：本示例使用的 python:3.11-slim 已提供 /bin/bash 和 /bin/sh，无需额外安装。更换基础镜像时，请确保满足前述镜像要求。

### .dockerignore：构建文件范围

```
HELPCODEESCAPE-text
*
!app.py
!requirements.txt
!Dockerfile
```

## 步骤 3：构建并推送镜像
在 ACR 镜像仓库页面获取并执行登录命令。登录成功后，在项目目录执行以下命令，构建并推送镜像。将 `IMAGE` 替换为实际的镜像地址。

```
HELPCODEESCAPE-bash
IMAGE='你的Registry地址/命名空间/仓库名:quickstart-v1'
docker build --platform linux/amd64 -t "$IMAGE" .
docker push "$IMAGE"
```

> **说明**：上述命令已通过 --platform linux/amd64 指定目标架构。在 Apple Silicon 等 ARM 设备上构建时也需保留此参数，避免生成仅支持 arm64 的镜像。

## 步骤 4：部署 Agent
1. 在目标 Workspace 左侧导航栏，单击 **Agent** 。单击**创建 Agent** ，选择**自定义代码 / 镜像**，配置以下参数。

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Agent 名称</p> </td> <td> <p>示例：<code>my-first-agent</code></p> </td> </tr> <tr> <td> <p>容器镜像</p> </td> <td> <p>选择已推送镜像所在的 ACR 仓库及 <code>quickstart-v1</code> 版本</p> </td> </tr> <tr> <td> <p>启动命令</p> </td> <td> <p><code>uvicorn app:server --host 0.0.0.0 --port 9000</code></p> </td> </tr> <tr> <td> <p>服务端口</p> </td> <td> <p><code>9000</code>。与应用监听端口保持一致。</p> </td> </tr> <tr> <td> <p>执行角色</p> </td> <td> <p>选择已授权该 Agent 访问所需资源的角色</p> </td> </tr> <tr> <td> <p>协议配置</p> </td> <td> <p>启用 AG-UI，路径为 <code>/ag-ui/agent</code></p> </td> </tr> <tr> <td> <p>高级配置 → 健康检查</p> </td> <td> <p>路径设置为 <code>/readyz</code>，端口设置为 <code>9000</code></p> </td> </tr> </tbody> </table>

<!-- -->

2. 按需完成其余配置，确认后创建并部署 Agent，等待应用就绪。本示例无需配置环境变量。

> **说明** ：控制台健康检查默认路径为 `/ready`，本示例需修改为 `/readyz`。服务端口和健康检查端口均使用 `9000`。

## 步骤 5：验证 Agent
1. 打开 Agent 调试页面，选择 AG-UI，发送以下消息。

> 你好，请用一句话介绍你能做什么。

2. 查看对话结果。Agent 正常返回回答，表示模型调用和应用部署成功。

## 常见问题
* 镜像无法启动：核对镜像拉取权限、镜像架构和启动命令。

* 健康检查失败：核对 `9000` 端口和 `/readyz` 路径；如日志显示「Agent 启动失败」，继续查看后面的异常原因。

* 模型调用失败：核对代码中的模型连接名、模型名，以及控制台的模型配置和 Agent 执行角色权限。

## 了解更多
模型、MCP、Skill、记忆、凭证及框架集成的详细用法，请参见 [AgentCore Python SDK 使用指南](https://help.aliyun.com/document_detail/3061225.html)与 [AgentCore Node.js SDK 使用指南](https://help.aliyun.com/document_detail/3061224.html)。