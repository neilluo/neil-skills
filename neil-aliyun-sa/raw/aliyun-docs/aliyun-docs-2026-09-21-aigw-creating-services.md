<!-- source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-services -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-09-20 -->
<!-- summary: AI 网关「创建服务」官方全文：AI 服务/Agent 服务/DNS 域名/固定地址/容器服务/SAE Kubernetes/函数计算 FC/MSE Nacos 八类服务来源的创建步骤与参数（含 DNS 域名与固定地址的服务地址格式 <域名或IP>:<端口>、外网地址需配置 NAT 网关、TLS 三档模式）。客户把自有认证接口注册进 AI 网关的前置步骤出处。 -->

您需要将已有的服务添加到网关中，登记为路由备选服务，以便网关获取服务地址。AI 网关支持以容器服务、固定地址、DNS域名和FC函数计算等几种形式添加服务。  

## **操作步骤**
网关通过服务动态感知后端资源变化，实现流量路由、治理和安全防护的统一管理。AI网关支持创建[AI 服务](#f8681fbfe2aof)、[Agent服务](#b81b6555a7vtt)、[DNS 域名](#6497449208dxn)、[固定地址](#51a0be76c4jx5)、[容器服务](#b8a93e3d38x81)、[SAE Kubernetes服务](#9bac0c62d7vtn)、[函数计算FC](#879b88517122e) 和 [MSE Nacos](#b16cc0561fxr8)。

### AI 服务

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源** ：选择**AI服务**。

   * **服务名称**：自定义服务名称。

   * **大模型供应商** ：支持**千问云 / 阿里云百炼** 、PAI-EAS、**Deepseek** 、**OpenAI兼容（OpenAI Compatible）** 、**OpenAI** 、**Azure** 、**Gemini** 、**Bedrock** 、**Claude** 、**月之暗面** 、**百川智能** 、**零一万物** 、**智谱AI** 、**混元** 、**阶跃星辰** 、**星火** 、**豆包** 、**MiniMax**。

     **重要**

     本AI服务所提供的大模型能力并非由AI网关直接提供。在使用前，请您自行评估该服务的适用性和可靠性，并确保您的使用行为完全符合相关法律法规及产品使用协议的要求。对于因违反上述规定而产生的一切后果，我们将不承担任何责任。
   * **模型协议**：选择与服务通信的协议，支持 OpenAI/v1 和原生协议两种。选择供应商后系统会填充默认值，可根据需要修改。

     * **OpenAI/v1**：使用 OpenAI 兼容协议，适用于大多数供应商。

     * **原生协议** ：使用供应商原生 API 协议。选择原生协议时，服务地址将切换为对应的原生协议地址（如阿里云百炼为 `https://dashscope.aliyuncs.com`）。

     **说明**

     Bedrock **端点模式**为 Mantle 时，仅支持 Anthropic 兼容协议（/v1/messages），不支持 OpenAI/v1 协议，且无法启用 Prompt Caching 功能。
   * **服务接入点**：大模型服务的 BaseURL。选择供应商后，系统会自动填充对应的服务地址，也可根据实际需求手动修改。

     > Azure 服务提供商服务地址格式： `https://{endpoint}/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}`
     > OpenAI 兼容（OpenAI Compatible）服务地址格式： `http://{endpoint}/v1`

     各供应商配置示例如下：
     <table> <thead> <tr> <td> <p><b>供应商</b></p> </td> <td> <p><b>服务地址（base_url）</b></p> </td> <td> <p><b>可用模型</b></p> </td> <td> <p><b>特殊配置说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>阿里云百炼</p> </td> <td> <p><code>https://dashscope.aliyuncs.com/compatible-mode/v1</code></p> </td> <td> <p>qwen-max、qwen-plus、qwen-turbo、qwen-long、qwen-vl-max、qwen-vl-plus、qwen-vl-ocr、deepseek-r1、deepseek-v3</p> </td> <td> <p>需选择<b>地域</b>，支持多地域切换</p> </td> </tr> <tr> <td> <p>Bedrock</p> </td> <td> <p><code>https://bedrock-runtime.{awsRegion}.amazonaws.com</code></p> </td> <td> <p>无预设（用户自行输入模型名）</p> </td> <td> <p>需配置 awsRegion、<b>端点模式</b>（Runtime 或 Mantle）和认证方式（API Key 或 AK/SK）；Mantle 模式仅支持 Anthropic 兼容协议</p> </td> </tr> <tr> <td> <p>Vertex AI</p> </td> <td> <p>用户手动输入</p> </td> <td> <p>无预设</p> </td> <td> <p>需配置<b>鉴权方式</b>（GCP Service Account 或 Vertex AI Express Mode）；GCP 模式需填写 JSON 格式的 GCP Service Account KEY，自动解析 vertexProjectId</p> </td> </tr> <tr> <td> <p>Azure</p> </td> <td> <p><code>https://{endpoint}?api-version={api-version}</code></p> </td> <td> <p>gpt-3、gpt-35-turbo、gpt-4、gpt-4o、gpt-4o-mini</p> </td> <td> <p>endpoint 为 Azure OpenAI 资源的接入点地址</p> </td> </tr> <tr> <td> <p>OpenAI</p> </td> <td> <p><code>https://api.openai.com/v1</code></p> </td> <td> <p>gpt-3、gpt-35-turbo、gpt-4、gpt-4o、gpt-4o-mini</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>OpenAI兼容（OpenAI Compatible）</p> </td> <td> <p><code>http://{endpoint}/v1</code></p> </td> <td> <p>无预设（用户自行输入模型名）</p> </td> <td> <p>仅支持满足 OpenAI 接口标准的 AI 服务</p> </td> </tr> <tr> <td> <p>DeepSeek</p> </td> <td> <p><code>https://api.deepseek.com/v1</code></p> </td> <td> <p>deepseek-chat、deepseek-reasoner</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>豆包</p> </td> <td> <p><code>https://ark.cn-beijing.volces.com/api/v3</code></p> </td> <td> <p>doubao-seed-1-6-250615、doubao-seed-1-6-flash-250715、doubao-seed-1-6-thinking-250715、doubao-1-5-thinking-vision-pro-250428</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>Gemini</p> </td> <td> <p><code>https://generativelanguage.googleapis.com/v1beta/openai</code></p> </td> <td> <p>gemini-1.5-flash、gemini-1.5-pro</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>MiniMax</p> </td> <td> <p><code>https://api.minimaxi.com/v1</code></p> </td> <td> <p>abab6.5s、abab6.5g、abab6.5t、abab5.5s</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>月之暗面</p> </td> <td> <p><code>https://api.moonshot.cn/v1</code></p> </td> <td> <p>moonshot-v1-8k、moonshot-v1-32k、moonshot-v1-128k</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>智谱AI</p> </td> <td> <p><code>https://open.bigmodel.cn/api/paas/v4</code></p> </td> <td> <p>GLM-4-Plus、GLM-4-0520、GLM-4-Long、GLM-4-AirX、GLM-4-Air、GLM-4-FlashX、GLM-4-Flash、GLM-4-AllTools、GLM-4</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>PAI-EAS</p> </td> <td> <p>通过<b>工作空间</b>和<b>EAS服务</b>选择自动获取</p> </td> <td> <p>无预设（动态获取）</p> </td> <td> <p>需依次选择<b>工作空间</b>、<b>EAS服务</b>和<b>连接类型</b>（私网或公网）；API-KEY 自动获取，无需手动配置</p> </td> </tr> <tr> <td> <p>Claude</p> </td> <td> <p><code>https://api.anthropic.com</code></p> </td> <td> <p>claude-3-5-sonnet-latest、claude-3-5-haiku-latest、claude-3-opus-latest</p> </td> <td> <p>可选开启<b>使用 Claude Code OAuth Token</b>以兼容 Claude Code 客户端调用</p> </td> </tr> <tr> <td> <p>百川智能</p> </td> <td> <p><code>https://api.baichuan-ai.com/v1</code></p> </td> <td> <p>Baichuan4-Turbo、Baichuan4-Air、Baichuan4、Baichuan3-Turbo、Baichuan3-Turbo-128k、Baichuan2-Turbo</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>零一万物</p> </td> <td> <p><code>https://api.lingyiwanwu.com/v1</code></p> </td> <td> <p>yi-lightning、yi-large、yi-medium、yi-medium-200k、yi-spark、yi-large-rag、yi-large-fc、yi-large-turbo</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>混元</p> </td> <td> <p><code>https://hunyuan.tencentcloudapi.com</code></p> </td> <td> <p>hunyuan-turbo-latest、hunyuan-turbo、hunyuan-large、hunyuan-pro、hunyuan-standard-256K、hunyuan-standard、hunyuan-lite</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>阶跃星辰</p> </td> <td> <p><code>https://api.stepfun.com</code></p> </td> <td> <p>step-1-8k、step-1-32k、step-1-128k、step-1-256k、step-2-16k、step-1-flash</p> </td> <td> <p>---</p> </td> </tr> <tr> <td> <p>星火</p> </td> <td> <p><code>https://spark-api-open.xf-yun.com</code></p> </td> <td> <p>lite、generalv3、pro-128k、generalv3.5、max-32k、4.0Ultra</p> </td> <td> <p>---</p> </td> </tr> </tbody> </table>
   * **API-KEY** ：访问大模型需要的 API-KEY 凭证。选择**大模型供应商**后，按以下方式获取：

     * **阿里云百炼** ：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/?apiKey=1)[阿里云百炼控制台](https://modelstudio.console.alibabacloud.com/?apiKey=1)获取。

     * **PAI-EAS** ：选择**工作空间** 和**EAS服务**后自动获取，无需手动配置。

     * **Bedrock**：使用 API Key 模式时，支持引用 KMS 密钥或手动输入；使用 AK/SK 模式时，需填写 awsAccessKey 和 awsSecretKey。

     * 其他供应商：请前往对应供应商平台获取 API-KEY，或咨询服务提供商。

3. 配置完成后单击**确定**，完成创建。

### Agent服务

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源**：选择Agent 服务。

   * **服务名称**：自定义服务名称。

   * **服务供应商** ：支持选择**千问云 / 阿里云百炼** 、**Dify** 、**自定义**。

     **重要**

     请注意，本Agent服务所提供的智能体相关能力并非由云原生API网关直接提供。在使用前，请您自行评估该服务的适用性和可靠性，并确保您的使用行为完全符合相关法律法规及产品使用协议的要求。对于因违反上述规定而产生的一切后果，我们将不承担任何责任。

     ## 阿里云百炼
     --------

     * **API地址** ：输入Agent服务的接入点地址。默认为：`https://dashscope.aliyuncs.com/api/v1`。

     * **APP ID** 、**API KEY** ：您可在[阿里云百炼控制台](https://bailian.console.aliyun.com/?spm=5176.29160146.0.0.df81338c2pKrmO&apiKey=1#/api-key)获取[应用的ID和 API Key](https://help.aliyun.com/document_detail/2712195.html#c38fb45bc6sje)。

       在 API Key 管理页面，单击**我的** Tab 页签查看个人 API Key 列表，单击右上角**创建我的API-KEY** 可新建 API Key，单击已有 API Key 操作列的**查看**可获取完整 Key 值。

     ## Dify
     -------

     * **API地址** ：输入Agent服务的接入点地址。默认为：`https://api.dify.ai/v1`。

     * **应用类型** ：支持选择**Agent** 或**Workflow**。

       * **Agent**：智能体类型。

       * **Workflow**：工作流类型。

     * **API KEY**：请咨询服务供应商获取。

     ## 自定义
     ------

     * **API地址**：输入Agent服务的接入点地址。

     * **API KEY**：请咨询服务供应商获取。

3. 配置完成后单击**确定**，完成创建。

### DNS 域名

**说明**

AI 网关支持根据DNS解析的结果作为后端服务地址。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源** ：选择**DNS域名**。

   * **服务名称**：自定义服务名称。

   * **服务地址** ：服务的后端节点地址，不同来源的服务，后端节点有所不同。格式为`<DNS域名>:<服务端口>`，支持填写多个，以英文`,`分隔。

     **重要**

     如果指定的是外网地址，需要[配置NAT网关](https://help.aliyun.com/document_detail/121139.html)。
   * **TLS模式**：默认关闭。

     * **关闭**：访问服务时，无需开启TLS。

     * **单向TLS**：需要使用HTTPS访问服务时开启单向TLS。

     * **双向TLS（mTLS）**：需要做双向认证时开启mTLS。

3. 配置完成后单击**确定**，完成创建。

### 固定地址

**说明**

如果该服务没有服务发现机制，需要手动添加服务的后端节点地址。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源** ：选择**固定地址**。

   * **服务名称**：自定义服务名称。

   * **服务地址** ：服务的后端节点地址，不同来源的服务，后端节点有所不同。格式为`<IP>:<服务端口>`，支持填写多个，以英文`,`分隔。

     **重要**

     如果指定的是外网地址，需要[配置NAT网关](https://help.aliyun.com/document_detail/121139.html)。
   * **TLS模式**：默认关闭。

     * **关闭**：访问服务时，无需开启TLS。

     * **单向TLS**：需要使用HTTPS访问服务时开启单向TLS。

     * **双向TLS（mTLS）**：需要做双向认证时开启mTLS。

3. 配置完成后单击**确定**，完成创建。

### 容器服务

**说明**

如果在网关中添加了容器服务作为服务来源，网关会从ACK/ACK Serverless集群获取服务列表，将服务列表中的服务及其后端节点地址添加到网关中。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。选择您实例所在的地域，并单击目标实例ID。在左侧导航栏单击**服务**。

2. **创建来源**

   1. 单击**来源** 页签，然后单击**创建来源** ，在**创建来源**面板中，配置以下参数：

      * **来源类型** ：选择**容器服务**，通过K8s Server发现后端服务。

      * **ACK/ACS/ACK Serverless 集群**：选择后端服务所在的集群。

        **重要**
        * 如当前VPC下不存在 ACK/ACS/ACK Serverless 集群，则需要[创建ACK托管集群](https://help.aliyun.com/document_detail/95108.html)，再选择该集群。

        * 如果需要添加其他VPC下的服务来源，请重新[创建指定VPC下的网关实例](https://help.aliyun.com/document_detail/2796788.html)后，再选择该集群。

        * 单个网关实例最多只能关联3个ACK容器服务。

        * 云原生API网关只能添加同VPC内的Nacos或者ACK，不支持跨VPC添加服务来源。

   2. 配置完成后单击**确定**，完成创建。

3. **创建服务**

   1. 单击**服务** 页签，然后单击**创建来源** ，在**创建来源**面板中，配置以下参数：

      * **服务来源** ：选择**容器服务**。

        > 网关会从ACK/ ACK Serverless集群获取服务列表，将服务列表中的服务及其后端节点地址添加到网关中。
      * **命名空间**：选择集群的命名空间。默认不展示arms-prom、kube-system和mse-pilot命名空间的服务。

      * **服务列表**：在服务列表中选择服务。默认不展示以consumers开头的服务。

   2. 配置完成后单击**确定**，完成创建。

### SAE Kubernetes服务

**重要**

添加SAE Kubernetes作为服务来源时，SAE应用需要开启[K8s Service服务注册发现](https://help.aliyun.com/document_detail/445981.html)。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源** ：**SAE Kubernetes服务** 。SAE应用需要开启[基于K8s ServiceName配置应用服务访问](https://help.aliyun.com/document_detail/445981.html)。

   * **命名空间**：选择集群的命名空间。默认不展示arms-prom、kube-system和mse-pilot命名空间的服务。

   * **服务列表** ：在服务列表中选择服务。默认不展示以`consumers:`开头的服务。

3. 配置完成后单击**确定**，完成创建。

### 函数计算FC

**重要**

支持函数计算3.0，暂不支持函数计算2.0的服务来源。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，在网关列表页，选择您实例所在的地域，并单击目标实例ID。单击左侧导航栏的**服务** ，单击**创建服务**。

2. 在**创建服务**面板中，配置以下参数：

   * **服务来源** ：**函数计算 FC**。

   * 函数列表：在函数列表中选择函数。

   * 版本或别名：选择函数的版本或别名。

3. 配置完成后单击**确定**，完成创建。

### MSE Nacos

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。选择您实例所在的地域，并单击目标实例ID。在左侧导航栏单击**服务**。

2. **创建来源**

   1. 单击**来源** 页签，然后单击**创建来源** ，在**创建来源**面板中，配置以下参数：

      * **来源类型** ：选择**MSE Nacos**，通过 MSE Nacos 注册中心发现后端服务。

      * **Nacos 集群**：选择Nacos 集群。

        **重要**
        * 如果当前VPC下不存在MSE Nacos集群，则需要先[创建MSE Nacos集群](https://help.aliyun.com/document_detail/2852403.html)，再选择该Nacos集群。

        * 如果需要添加其他VPC下的服务来源，请重新[创建指定VPC下的网关实例](https://help.aliyun.com/document_detail/2796788.html)，再选择该Nacos集群。

        * 集群列表仅展示`MCPEnabled = true`的MSE Nacos实例，可在MSE Nacos参数设置中更改。

        * 单个网关实例最多只能关联1个Nacos实例。

   2. 配置完成后单击**确定**，完成创建。

3. **创建服务**

   1. 单击**服务** 页签，然后单击**创建服务** ，在**创建服务**面板中，配置以下参数：

      * **服务来源** ：选择**MSE Nacos**。

        > 网关会从Nacos 集群获取服务列表，将服务列表中的服务及其后端节点地址添加到网关中。
      * **命名空间**：选择命名空间。默认不展示arms-prom、kube-system和mse-pilot命名空间的服务。

      * **服务列表** ：在服务列表中选择服务。默认不展示以`consumers:`开头的服务。

   2. 配置完成后单击**确定**，完成创建。