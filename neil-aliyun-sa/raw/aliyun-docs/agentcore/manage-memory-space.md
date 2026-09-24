---
source_url: https://help.aliyun.com/zh/agentcore/manage-memory-space
fetch_date: 2026-09-20
product: AgentCore
slug: manage-memory-space
body_sha256: bd40a4e2a4d2aa07020b5d5f4d50dd3b17c51ac50ad6e8828b42a77bff927687
body_bytes: 14287
migration_status: current   # 见 FETCH-CONTRACT §3
---

<br />

记忆空间用于管理 Agent 的长期记忆和会话历史。通过本文，可以了解两类数据的用途和隔离方式，完成记忆空间的创建与日常管理，并将记忆能力接入 Agent 或应用。

## **功能介绍**
### 长期记忆

长期记忆是从输入文本或对话消息中提取的偏好、事实和需求等信息。应用可以在后续交互中检索这些信息，帮助 Agent 更好地理解用户。

例如，用户在一次对话中提到"推荐餐厅时，请优先考虑素食餐厅"。这项偏好可以形成长期记忆，在后续推荐餐厅时作为回答参考，无需用户在每次会话中重复说明。

长期记忆适用于以下场景：

* 保存用户偏好，提供个性化服务。

* 记录可复用的事实和需求，支持跨会话交互。

* 按业务范围检索信息，为 Agent 的回答提供参考。

输入内容与生成的记忆不一定一一对应。提交一段文本或一组消息后，可能生成多条记忆，也可能不生成新记忆。

### 会话历史

会话历史是按会话组织的消息记录。一个会话包含多条消息，消息通过角色和内容描述交互过程，例如用户提出的问题和助手给出的回答。

通过会话历史，可以查看已有会话、会话关联的业务用户和 Agent，以及指定会话中的消息内容。会话历史适用于回看一次会话的交互内容、了解用户提出需求时的上下文，以及辅助分析 Agent 的回答和交互效果。

长期记忆与会话历史的区别如下。
<table> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <thead> <tr> <td> <p><b>对比项</b></p> </td> <td> <p><b>长期记忆</b></p> </td> <td> <p><b>会话历史</b></p> </td> </tr> </thead> <tbody> <tr> <td> <p>保存的内容</p> </td> <td> <p>从输入中提取的偏好、事实和需求等信息</p> </td> <td> <p>会话中的消息记录</p> </td> </tr> <tr> <td> <p>主要用途</p> </td> <td> <p>在后续交互中检索和复用信息</p> </td> <td> <p>查看和追溯交互过程</p> </td> </tr> <tr> <td> <p>查看方式</p> </td> <td> <p>查看记忆列表、详情，或进行语义检索</p> </td> <td> <p>查看会话列表，再查看指定会话的消息</p> </td> </tr> <tr> <td> <p>示例</p> </td> <td> <p>用户偏好素食餐厅</p> </td> <td> <p>用户表达该偏好时的消息，以及助手的回复</p> </td> </tr> </tbody> </table>  
**说明**

创建记忆空间后，还需要通过支持的接入方式写入数据。创建空间本身不会自动收集所有 Agent 的对话；会话历史中展示的内容取决于应用实际提交的消息。

### 使用 Scope 隔离记忆

Scope 用于按业务用户、Agent 和会话组织和隔离记忆。以下字段均由应用自行定义和传入。
<table> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>含义</b></p> </td> <td> <p><b>示例</b></p> </td> </tr> </thead> <tbody> <tr> <td> <p><code>userId</code></p> </td> <td> <p>业务用户标识</p> </td> <td> <p><code>user-001</code></p> </td> </tr> <tr> <td> <p><code>agentId</code></p> </td> <td> <p>业务 Agent 标识</p> </td> <td> <p><code>travel-agent</code></p> </td> </tr> <tr> <td> <p><code>sessionId</code></p> </td> <td> <p>业务会话标识</p> </td> <td> <p><code>session-001</code></p> </td> </tr> </tbody> </table>

写入记忆时，可以根据需要填写这些字段，关联记忆的业务归属。查询长期记忆时，指定的字段参与精确过滤，未指定的字段不参与过滤；多个字段同时指定时，需要同时满足这些条件。

例如：

* 仅指定 `userId`：查询该业务用户跨 Agent、跨会话的记忆。

* 指定 `userId` 和 `agentId`：查询该业务用户与指定 Agent 相关的记忆。

* 同时指定三个字段：将范围限定到该业务用户与指定 Agent 的某次会话。

不指定 Scope 筛选条件时，不限制这三个维度，查询范围为当前记忆空间。`userId` 是业务字段，不对应 RAM 用户或调用身份；应用需要自行维护这些业务标识，并在写入和查询时一致使用。

### 使用 Metadata 标记记忆

Metadata 用于为长期记忆添加自定义业务标记，例如分类、来源和主题。标记由字符串键值对组成。
<table> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <thead> <tr> <td> <p><b>标记</b></p> </td> <td> <p><b>示例值</b></p> </td> <td> <p><b>含义</b></p> </td> </tr> </thead> <tbody> <tr> <td> <p><code>category</code></p> </td> <td> <p><code>dietary-preference</code></p> </td> <td> <p>饮食偏好类记忆</p> </td> </tr> <tr> <td> <p><code>source</code></p> </td> <td> <p><code>conversation</code></p> </td> <td> <p>来源于对话</p> </td> </tr> </tbody> </table>

Scope 表达记忆的业务归属，Metadata 表达记忆的业务属性。两者可以组合使用，例如在某个用户的记忆范围内筛选饮食偏好类记忆。

## 使用前准备
使用记忆空间前，请确认已完成以下准备：

* 已开通 AgentCore，并创建目标 Workspace。

* 当前账号具备相应的记忆空间访问和管理权限。

* 已选择目标地域和 Workspace。

记忆空间归属于指定地域的 Workspace。查看数据前，请确认所选地域和 Workspace 与创建时一致。有关 Workspace 的创建和切换方法，请参见[管理 Workspace](https://help.aliyun.com/document_detail/3052311.html)。

## 创建记忆空间
按以下步骤创建记忆空间：

1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 选择目标地域和 Workspace。在 Workspace 详情页左侧导航栏，选择**资产管理** \> **记忆空间**。

3. 单击**创建记忆空间**。

4. 在**创建记忆空间**对话框中配置以下参数。

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>记忆空间名称</p> </td> <td> <p>必填。长度为 1～64 个字符，只能包含小写字母、数字和短划线（<code>-</code>），用于标识和区分不同的记忆空间。例如 <code>travel-assistant</code>。同一 Workspace 内的记忆空间名称必须唯一；不同 Workspace 可以使用相同名称。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>可选，最多 1024 个字符，用于说明记忆空间的用途。例如"旅行助手用户偏好"。</p> </td> </tr> </tbody> </table>

<!-- -->

5. 单击**创建**。

6. 等待记忆空间状态变为 `Ready` 后，再写入或检索记忆。创建需要一定时间；提交成功后可查看状态，避免在空间尚未就绪时重复创建。

## 查看和使用长期记忆
### 查看记忆列表和详情

进入目标记忆空间后，查看已写入的长期记忆。查看时重点关注以下信息：

* 记忆内容：保存了哪些偏好、事实和需求。

* Scope：记忆关联的业务用户、Agent 和会话。

* Metadata：记忆的分类、来源等标记。

* 记忆 ID：用于准确定位某条记忆。

如果空间中尚无数据，需要先通过应用接入或 API 写入内容。

### 筛选记忆

根据业务需求设置筛选条件。例如，需要查看某个用户的饮食偏好时，可以指定该用户的 `userId`，并使用相应的 Metadata 标记筛选。
<table> <colgroup></colgroup> <colgroup></colgroup> <thead> <tr> <td> <p><b>查看需求</b></p> </td> <td> <p><b>Scope 条件</b></p> </td> </tr> </thead> <tbody> <tr> <td> <p>某个用户的记忆</p> </td> <td> <p><code>userId</code></p> </td> </tr> <tr> <td> <p>某个 Agent 的记忆</p> </td> <td> <p><code>agentId</code></p> </td> </tr> <tr> <td> <p>某次会话的记忆</p> </td> <td> <p><code>sessionId</code></p> </td> </tr> <tr> <td> <p>某个用户与指定 Agent 的记忆</p> </td> <td> <p><code>userId</code>、<code>agentId</code></p> </td> </tr> <tr> <td> <p>某个用户在指定会话中的记忆</p> </td> <td> <p><code>userId</code>、<code>sessionId</code></p> </td> </tr> </tbody> </table>

以上为记忆查询的筛选语义，控制台可配置的筛选项以页面实际提供的能力为准。

### 检索相关记忆

语义检索用于根据自然语言问题查找相关记忆。例如，输入"用户有哪些饮食偏好？"，可查找与饮食偏好有关的信息。

检索时可以结合 Scope 和 Metadata 限定范围。返回结果还会受到返回数量、相似度和重排设置的影响。列表查询适合查看和遍历记忆，语义检索适合查找与问题相关的记忆；需要确认某条记忆是否存在时，优先查看列表或按记忆 ID 查询。

### 维护记忆

当用户偏好变化或记忆内容需要纠正时，可以更新对应记忆；不再需要的记忆可以删除。产品提供按记忆 ID 查询、更新和删除的 API；控制台操作入口以页面实际支持情况为准。

例如，用户将偏好从"素食餐厅"调整为"素食和海鲜餐厅都可以"时，应用可以更新对应的长期记忆。

## 查看会话历史
### 查看会话列表

在目标记忆空间中查看会话历史，了解已记录的会话及其业务归属。用户标识、Agent 标识和会话标识可以帮助区分不同交互；同一个用户可能与多个 Agent 交互，也可能与同一个 Agent 进行多次会话。

### 查看会话消息

选择目标会话，查看其中的消息内容及角色，了解用户与 Agent 的交互过程。查看时应结合会话的业务归属定位目标，避免将不同用户或 Agent 下的同名会话混淆。  
**说明**

会话历史展示消息记录，长期记忆展示提取出的信息。提交的消息没有生成新记忆，并不等于没有会话消息记录。

## 管理记忆空间
### 查看记忆空间列表和空间信息

在**记忆空间**页面的列表中查看已创建的记忆空间，可通过搜索框按记忆空间名称筛选。

尚未创建任何记忆空间时，列表显示"暂无记忆空间"。

**概览** 页面的资源摘要会统计当前 Workspace 下已创建的记忆空间数量。在记忆空间管理页面还可以查看空间的名称、描述和状态；空间状态为 `Ready` 后，可以进行记忆读写操作。

### 修改描述

通过修改描述说明空间用途，便于区分不同业务使用的记忆空间。

### 删除记忆空间

不再使用某个记忆空间时，可以执行删除操作。删除是异步操作，提交后需等待完成。  
**警告**

删除记忆空间会删除空间内的数据。重新创建同名空间不能恢复已删除的数据。删除前请确认目标地域、Workspace 和记忆空间。

## 将记忆空间接入 Agent 或应用
要让 Agent 在后续交互中使用记忆，应用需要完成以下流程：

1. **写入内容**：将需要记忆的文本或对话消息提交到记忆空间，并关联 Scope 和 Metadata。

2. **检索记忆**：收到新问题时，在合适的业务范围内检索相关记忆。

3. **用于回答**：将检索结果与当前问题一起提供给模型。

例如，旅行助手在新会话中收到餐厅推荐请求时，可以按用户标识检索饮食偏好，再结合偏好生成回答。

开发者可以通过 SDK 或 API 接入，相关能力如下。
<table> <colgroup></colgroup> <colgroup></colgroup> <thead> <tr> <td> <p><b>能力</b></p> </td> <td> <p><b>API</b></p> </td> </tr> </thead> <tbody> <tr> <td> <p>创建、查看、列出、更新和删除记忆空间</p> </td> <td> <p><code>CreateMemoryStore</code>、<code>GetMemoryStore</code>、<code>ListMemoryStores</code>、<code>UpdateMemoryStore</code>、<code>DeleteMemoryStore</code></p> </td> </tr> <tr> <td> <p>写入记忆</p> </td> <td> <p><code>AddMemories</code></p> </td> </tr> <tr> <td> <p>语义检索记忆</p> </td> <td> <p><code>SearchMemories</code></p> </td> </tr> <tr> <td> <p>列出、查询、更新和删除记忆</p> </td> <td> <p><code>ListMemories</code>、<code>GetMemory</code>、<code>UpdateMemory</code>、<code>DeleteMemory</code></p> </td> </tr> <tr> <td> <p>查看会话列表和消息</p> </td> <td> <p><code>ListMemorySessions</code>、<code>ListMemorySessionMessages</code></p> </td> </tr> </tbody> </table>

API 中保留 `MemoryStore` 作为记忆空间的资源标识名称。

## 常见问题
### 创建记忆空间后，Agent 会自动记住所有对话吗？

创建空间只完成资源准备。还需要配置相应的接入方式，或由应用提交文本和对话消息。应用使用哪些记忆、何时写入和检索，取决于具体的接入流程。

### 长期记忆和会话历史有什么区别？

会话历史用于回看消息和交互过程；长期记忆用于保存可复用的信息，并在后续交互中检索。例如，"用户提出素食要求及助手的回复"属于会话历史，"用户偏好素食餐厅"属于长期记忆。

### Scope 和 Metadata 应该如何选择？

Scope 表达记忆的业务归属，例如用户、Agent 和会话；Metadata 表达记忆的业务属性，例如分类和主题。

例如，"某个用户 `user-001` 的饮食偏好"中，用户标识放入 Scope，饮食偏好分类放入 Metadata。

### 为什么没有看到预期的记忆？

先确认所选地域、Workspace 和记忆空间，再检查输入内容是否已提交，以及筛选条件是否正确。输入内容与生成的记忆不保证一一对应，应以实际写入结果为准。

### 为什么列表中能看到，语义检索没有返回？

语义检索受查询文本、Scope、Metadata、返回数量和检索阈值影响，不保证返回全部符合筛选条件的记忆。需要确认某条记忆是否存在时，可以查看列表或按记忆 ID 查询。

### 为什么查询到了其他会话的记忆？

查询长期记忆时，未填写 `sessionId` 表示不限制会话，因此可能返回跨会话的记忆。需要限定某次会话时，填写对应的 `sessionId`。未填写 `userId` 或 `agentId` 时，也不会限制对应维度。

## 相关文档
[查看概览](https://help.aliyun.com/document_detail/3052310.html)：查看 Workspace 下 Agent 的运行状态与资源摘要。