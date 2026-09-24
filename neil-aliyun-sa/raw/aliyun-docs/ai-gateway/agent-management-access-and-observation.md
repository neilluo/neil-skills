---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/agent-management-access-and-observation
fetch_date: 2026-09-21
product: AI Gateway
slug: agent-management-access-and-observation
body_sha256: bcd540b95e63d80d074e57c732570170bfb681b4b09ddaa965d2b8f6bc780a8d
body_bytes: 17862
migration_status: current
---

AI 网关通过 Agent 资源统一维护 Agent 对外提供服务和调用模型时使用的访问配置，并汇总相关观测数据。完成配置后，可在 Agent 拓扑图 查看 Agent API、Model API、消费者、策略和插件之间的关系，也可以按 Agent 查看模型调用和会话用量。本文介绍如何创建和配置 Agent、将 Agent 客户端接入 AI 网关，以及如何查看 Agent 统计和会话用量统计。  
**说明**

Agent 管理仅支持新版 Serverless 网关的标准版和企业版，旧版 Serverless 网关和实例型网关暂不支持。各网关类型的能力差异请参见[网关类型](https://help.aliyun.com/document_detail/2922542.html)。

## Agent 资源与支持的能力
Agent 是 AI 网关的一种管理资源，用于集中维护访问配置、汇总观测数据。根据 Agent 类型，可以配置以下一种或两种访问能力：

* Agent 访问：将 Agent 服务通过 Agent API 对外提供，并统一配置路由、消费者认证、策略和插件。适用于用户或其他应用调用 Agent 的场景。

* 模型访问：将 Agent 使用的 Model API 与代表 Agent 身份的消费者绑定，并统一配置模型协议、访问地址、授权、策略和插件。适用于 Agent 调用模型的场景。

不同 Agent 类型支持的访问能力如下。
<table> <thead> <tr> <td><p><b>Agent 类型</b></p></td> <td><p><b>Agent 访问</b></p></td> <td><p><b>模型访问</b></p></td> <td><p><b>适用场景</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>百炼</p></td> <td><p>支持</p></td> <td><p>不支持</p></td> <td><p>通过 AI 网关对外提供百炼应用。</p></td> </tr> <tr> <td><p>Dify</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>同时管理 Dify 应用的入站访问和模型调用。</p></td> </tr> <tr> <td><p>Claude Code</p></td> <td><p>不支持</p></td> <td><p>支持</p></td> <td><p>管理 Claude Code 的模型调用。</p></td> </tr> <tr> <td><p>DeepSeek Harness</p></td> <td><p>不支持</p></td> <td><p>支持</p></td> <td><p>管理 DeepSeek Harness 的模型调用。</p></td> </tr> <tr> <td><p>Codex</p></td> <td><p>不支持</p></td> <td><p>支持</p></td> <td><p>管理 Codex 的模型调用。</p></td> </tr> <tr> <td><p>自定义</p></td> <td><p>支持</p></td> <td><p>支持</p></td> <td><p>根据业务需要配置 Agent 访问、模型访问或两者同时配置。</p></td> </tr> </tbody> </table>

配置访问能力并产生调用数据后，可以使用以下观测能力。
<table> <thead> <tr> <td><p><b>能力</b></p></td> <td><p><b>用途</b></p></td> <td><p><b>适合解决的问题</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>会话用量统计</p></td> <td><p>从会话、轮次和模型调用三个层级查看 Token、Credits、耗时、缓存命中率和工具调用。</p></td> <td><p>哪些会话用量较高或耗时较长？Token 或 Credits 用量主要集中在哪个轮次或哪次模型调用？</p></td> </tr> <tr> <td><p>Agent 统计</p></td> <td><p>按 Agent 查看请求量、Token 消耗、错误率、模型回退（Fallback）率、延迟，以及模型和消费者分布。</p></td> <td><p>哪个模型或消费者用量较高？错误率和延迟是否异常？模型回退是否频繁发生？</p></td> </tr> </tbody> </table>

## 前提条件
根据使用的功能，提前准备以下条件：

* 已创建新版 Serverless 标准版或企业版 AI 网关，创建方式请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 配置 Agent 访问前，准备可访问的 Agent 后端服务。

* 配置模型访问时，待绑定的消费者需已获得所选 Model API 的访问权限。

* 使用会话用量统计时，会话分析需要使用网关访问日志。

## Agent 管理
### 创建 Agent

1. 登录 [AI 网关控制台](https://apig.console.aliyun.com/)，选择目标地域和新版 Serverless AI 网关实例。

2. 在左侧导航栏，单击 **Agent 管理**。

3. 单击 **创建 Agent**。

4. 配置以下基本信息。

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>Agent 名称</b></p></td> <td><p>当前网关内 Agent 的唯一名称。支持英文字母、数字、短划线（-）和下划线（_），长度不超过 64 个字符。创建后不可修改。</p></td> </tr> <tr> <td><p><b>Agent 类型</b></p></td> <td><p>选择百炼、Dify、Claude Code、DeepSeek Harness、Codex 或自定义。Agent 类型决定后续可配置的访问能力，创建后不可修改。</p></td> </tr> </tbody> </table>
5. 根据需要展开 **Agent 访问能力配置（选填）** 或 **模型访问能力配置（选填）** ，完成相关配置；也可直接单击 **确定**，在创建 Agent 后再配置。

创建成功后，控制台自动进入 **Agent 拓扑图** 页签。

### 配置 Agent 访问

Agent 访问用于将 Agent 服务通过 AI 网关对外提供。配置前，请准备可访问的 Agent 后端服务。百炼、Dify 和自定义类型支持该能力。

1. 进入配置入口：创建 Agent 时展开 **Agent 访问能力配置（选填）** ，或创建后在 **Agent 拓扑图** 页签的 **Agent 访问** 区域配置。

2. 选择已有域名，或单击 **添加域名** 创建域名。设置访问路径，将 Agent API 路由到对应的 Agent 后端服务。

3. 如需校验调用方身份，在 **消费者认证** 卡片开启认证，并为消费者或消费者组授权。

4. 如需对请求进行治理，在 **策略与插件** 卡片添加所需策略或插件。

5. 确认 Agent API、消费者认证以及策略和插件的配置无误。

配置完成后，调用方可通过 Agent API 的域名和访问路径访问 Agent。  
**说明**

Agent 拓扑图展示 Agent 与相关资源之间的关系。Agent API、服务、路由、域名和消费者仍需在各自的资源页面管理；这些资源发生变更后，拓扑图会同步更新。

### 配置模型访问

模型访问用于管理 Agent 调用模型时使用的访问地址、协议和消费者身份。Dify、Claude Code、DeepSeek Harness、Codex 和自定义类型支持该能力。

1. 进入配置入口：创建 Agent 时展开 **模型访问能力配置（选填）** ，或创建后在 **Agent 拓扑图** 页签的 **模型访问** 区域配置。

2. 选择已有 Model API，并确认模型协议、BasePath 和域名。如果没有可用的 Model API，可以通过页面入口创建。Agent 客户端需要使用此处显示的接入点和 BasePath 访问模型，Model API 的管理方式请参见[管理 Model API](https://help.aliyun.com/document_detail/2859333.html)。

3. 在 **消费者绑定** 卡片绑定一个或多个消费者。同一个 Model API 可以关联多个 Agent，但在同一个 Model API 下，同一个消费者只能绑定到一个 Agent，AI 网关根据这一绑定关系将模型调用统计到对应 Agent。如果没有可用的消费者，可以单击 **创建消费者** 。绑定前，请确保消费者已获得所选 Model API 的访问权限；在此处绑定消费者不会自动为其授权。消费者的创建方式请参见[创建消费者](https://help.aliyun.com/document_detail/2882031.html)。

4. 如需记录模型请求或进行内容安全防护，在 **策略与插件** 卡片开启或添加相应策略，例如 **AI 请求日志** 、**AI 安全防护**。

5. 确认 Model API、消费者绑定以及策略和插件的配置无误。

### 编辑 Agent

Agent 名称和 Agent 类型创建后不可修改，可以修改 Agent 的访问配置和关联资源。

1. 在 **Agent 管理** 页面找到目标 Agent，在 **操作** 列单击 **编辑**；也可以单击 Agent 名称进入拓扑图后调整相关配置。

2. 修改 Agent 访问或模型访问配置。

3. 单击 **确定** 保存。

### 删除 Agent

1. 在 **Agent 管理** 页面找到目标 Agent，在 **操作** 列单击 **删除**。

2. 阅读删除提示，确认无误后完成删除。

删除 Agent 会解除该 Agent 与相关资源之间的关系，并移除相关授权，但不会删除关联的 Agent API、Model API、服务、域名、消费者或消费者组。如不再使用这些资源，请前往对应资源页面单独处理。

## Agent 接入
配置模型访问后，需要将实际运行的 Agent 客户端改为通过 AI 网关调用模型。接入后，Agent 的模型请求会经过 AI 网关，可以使用消费者认证、策略与插件，并查看 Agent 统计和会话用量统计。

### 获取接入信息

1. 在 **Agent 管理** 页面，单击目标 Agent 名称。

2. 在 **Agent 拓扑图** 页签，单击 Agent 卡片的 **Agent 接入**。

3. 在接入指引选择 API 协议和接入点，并填写访问模型、模型显示名称及用于鉴权的消费者。

4. 根据页面生成的指引，获取以下信息：

   * 由接入点和 Model API BasePath 组成的 API 地址

   * Model API 使用的协议

   * 所选消费者的 API Key

   * Agent 客户端需要使用的模型名称和显示名称

### 配置并验证客户端

控制台会根据 Agent 类型生成接入步骤，具体配置以页面生成的接入指引为准。以 DeepSeek Harness 为例，支持以下两种配置方式：

* 平台手动配置：进入 DeepSeek Harness 的 **设置** \> **模型** \> **添加自定义提供方**，按接入指引填写 Provider ID、显示名称、API 地址、API 协议和 API Key，然后添加模型。

* 本地配置文件：按照接入指引合并 `~/.dsh/settings.yaml`，并设置所需环境变量。

对于其他 Agent 类型，按照控制台生成的接入指引操作。如果客户端未提供专用指引，可使用其自定义端点或自定义模型提供方配置，填写 AI 网关生成的 API 地址、协议、消费者 API Key 和模型名称。

完成配置后，在 Agent 客户端发起一次模型调用。如果模型正常返回响应，并且可以在 AI 网关查到这次调用，说明接入成功。在观测页面查证调用记录时，请注意：会话用量统计需要先开启会话分析，且只分析开启后新产生的调用，当日会话大盘约有 5 分钟的数据延迟；模型访问统计需要订阅每日分析，系统按日生成分析结果。  
**重要**

消费者 API Key 属于访问凭证，请勿写入代码仓库或公开文档，建议通过客户端的凭据管理或环境变量保存。

## Agent 观测
### 会话用量统计

**会话用量统计** 位于 **FinOps** 下，仅展示已配置模型访问的 Agent。该功能将模型请求按会话和轮次整理，帮助找到用量较高或耗时较长的会话，并进一步定位出现异常的模型调用。数据层级如下：

* 会话（Session）：用户与 Agent 的一次完整对话，可包含一个或多个轮次。

* 轮次（Turn）：用户的一次提问及 Agent 完成该问题的处理过程，一个轮次可能因工具调用、重试等产生多次模型调用。

* 模型调用：轮次内实际发起的一次模型请求，可查看模型名称、输入输出类型、结束原因、首 Token 延迟（TTFT）、Token 和耗时等信息。

#### 开启会话分析

1. 在目标 AI 网关实例的左侧导航栏，选择 **FinOps** \> **会话用量统计**。

2. 如果页面提示尚未开启，按照页面说明开启会话分析。会话分析需要使用网关访问日志：如果已开启标准访问日志投递，系统会直接使用现有配置；如果尚未开启，页面会引导完成配置。

开启会话分析后，只分析新产生的调用，不会补充开启前的历史会话。  
**说明**

AI 网关不单独收取日志费用，日志服务 SLS 会根据实际使用量计费，具体计费方式请参见[开启网关日志投递](https://help.aliyun.com/document_detail/2882057.html)。

#### 查看会话大盘

1. 在 **会话用量统计** 页面选择 Agent 和日期。

2. 选择 **会话大盘** 页签。

3. 查看以下内容。

   <table> <thead> <tr> <td><p><b>分析区域</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>概览</b></p></td> <td><p>所选 Agent 当日的会话数和消费者数。</p></td> </tr> <tr> <td><p><b>会话性能与资源消耗分布</b></p></td> <td><p>会话 Token、会话耗时和会话 Credits 的 P50、P90。</p></td> </tr> <tr> <td><p><b>Session 排行</b></p></td> <td><p>分别按 Token、总耗时和 Credits 展示用量较高的会话。</p></td> </tr> <tr> <td><p><b>消费者用量排名</b></p></td> <td><p>分别按会话数、Token 和 Credits 展示消费者用量。</p></td> </tr> </tbody> </table>

当日会话大盘约有 5 分钟的数据延迟，且会话大盘和会话列表的更新时间可能不同，两处数据在短时间内可能不一致。

#### 查看会话列表和详情

1. 选择 **会话列表** 页签。

2. 输入会话名称或会话 ID，搜索目标会话。

3. 查看会话的消费者、Token、Credits、缓存命中率、工具调用数量、模型调用总耗时、会话总耗时和开始时间。

4. 在目标会话的 **操作** 列单击 **查看详情**。

5. 在详情页查看以下信息：

   * 会话基本信息及轮次 Token、Credits 和耗时分布

   * 按 Token、耗时和 Credits 排列的轮次排行

   * 轮次时间线及每个轮次内的模型调用明细

   * 模型名称、输入输出类型、结束原因、工具调用、调用结果、首 Token 延迟（TTFT）、Token、Credits、开始时间和耗时。

会话总耗时表示从会话首次请求开始到最后一次请求结束的实际经过时间，其中包含轮次之间的等待时间；模型调用总耗时是会话内各次模型调用耗时之和。排查慢会话时，可以结合轮次时间线和模型调用明细，判断耗时主要来自模型调用、工具调用，还是轮次间等待。

### Agent 统计

在 **Agent 管理** 页面找到目标 Agent，单击 **操作** 列的 **统计** ；也可以进入 Agent 详情页后选择 **统计** 页签。统计页面包含 **模型访问** 和 **Agent 访问** 两个页签。配置相应访问能力并产生调用数据后，页面才会展示统计结果。

#### 查看模型访问统计

模型访问统计用于分析 Agent 调用模型时的请求量、Token 消耗、稳定性和延迟。

1. 在 Agent 的 **统计** 页签，选择 **模型访问**。

2. 打开 **订阅每日分析** 。分析数据来自日志服务 SLS 的 `apig-access-log`，系统按日生成分析结果。

3. 选择需要查看的分析日期。

4. 查看以下内容。

   <table> <thead> <tr> <td><p><b>分析区域</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>核心指标</b></p></td> <td><p>总请求数、总 Token、错误率、Fallback 率和请求延迟 P95。</p></td> </tr> <tr> <td><p><b>智能洞察</b></p></td> <td><p>根据所选日期的访问数据，提示 Token 消耗、错误率、Fallback 率或延迟方面的异常，并给出排查建议。当天没有请求时，延迟和错误率会显示为 0，不能据此判断性能。</p></td> </tr> <tr> <td><p><b>流量结构</b></p></td> <td><p>模型请求占比、各模型 Token 消耗、消费者分布和分时请求趋势。</p></td> </tr> <tr> <td><p><b>成本归因</b></p></td> <td><p>输入与输出 Token 占比，以及文本、图像、推理、缓存等 Token 类型分布。</p></td> </tr> <tr> <td><p><b>稳定性与延迟</b></p></td> <td><p>首 Token 延迟、每输出 Token 生成耗时、整体请求延迟、HTTP 5xx、Fallback 和响应标志。</p></td> </tr> <tr> <td><p><b>消费者明细</b></p></td> <td><p>各消费者的请求数、请求占比、Token、Token 占比和错误率。</p></td> </tr> </tbody> </table>

模型访问统计按 Agent 区分数据。即使多个 Agent 使用同一个 Model API，也可以根据消费者与 Agent 的绑定关系，分别查看每个 Agent 的模型调用数据。

#### 查看 Agent 访问统计

Agent 访问统计用于查看调用方访问 Agent API 时的请求量、错误率和延迟。

1. 在 Agent 的 **统计** 页签，选择 **Agent 访问**。

2. 选择分析日期，查看 Agent API 的访问统计。

如果当前 Agent 类型不支持 Agent 访问，或尚未完成 Agent 访问配置，页面不会展示相关数据。

## 常见问题
### 创建 Agent 后，为什么没有立即产生统计数据？

创建 Agent 后，只保存了名称和类型。还需要配置访问能力，并让实际请求经过 AI 网关，统计页面才会产生数据。查看模型访问统计前，需要订阅每日分析；查看会话用量统计前，需要开启会话分析。

### 会话用量统计中为什么找不到某个 Agent？

会话用量统计只展示已配置模型访问的 Agent。请先在 Agent 拓扑关联 Model API 并绑定消费者，然后通过该消费者发起模型调用。

### 模型访问统计中的延迟为 0，是否表示性能很好？

不一定。如果所选日期没有请求，延迟、错误率等指标会显示为 0，但不能据此判断性能。请先确认总请求数和请求趋势，再查看延迟和稳定性。

### 为什么会话总耗时明显大于模型调用总耗时？

会话总耗时包含轮次之间的等待时间，模型调用总耗时只计算各次模型调用的耗时。结合会话详情的轮次时间线，可以判断耗时主要来自模型调用、工具调用，还是轮次间等待。