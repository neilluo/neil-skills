---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/use-cases/migrate-the-official-claude-code-model-to-any-model-using-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: migrate-the-official-claude-code-model-to-any-model-using-ai-gateway
body_sha256: 852e1873a7e0e5e6d29d6c22f527ea89a07d0dd65fa4700a0f7b0df011c51dce
body_bytes: 4112
migration_status: current
---

本文介绍如何使用AI网关将Claude Code官方模型迁移至其它模型。  

## **场景概览**
当用户使用Claude Code进行开发辅助，但无法使用官方模型时，可通过AI网关将Claude Code使用的模型从官方模型迁移到其他模型服务。

通过AI网关，可实现：

* **统一接入**：统一入口屏蔽各家模型协议差异。

* **避免锁定**：避免被特定供应商锁定。

* **高可用性**：支持供应商A失败后兜底到供应商B。

* **按需路由**：根据模型名称智能路由到不同供应商。

## 前提条件
* 已创建专有网络VPC并绑定公网NAT网关，若尚未创建，请参见[专有网络与交换机](https://help.aliyun.com/document_detail/2881389.html)与[公网访问](https://help.aliyun.com/document_detail/106263.html)。

* 已创建AI网关实例，若尚未创建，请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

* 已安装Claude Code客户端。

* 已获取目标大模型供应商API Key。

## 迁移步骤
### 步骤1.创建AI服务

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，选择**服务** ，单击**创建服务** ，服务来源选择**AI服务**。

5. 在**大模型供应商** 处选择对应模型提供商，然后在**大模型配置** 中，填写API-KEY，单击**确定**完成创建。可根据实际需要创建多个不同供应商的服务，实现多模型支持和高可用保障。

   **重要**
   * API Key建议通过引用凭据方式存储在KMS中，以避免API Key泄露风险。具体操作参见钥[引用密钥](https://help.aliyun.com/document_detail/2978744.html)

### 步骤2.创建并调试Model API

1. 在左侧导航栏选择**Model API** ，单击**创建Model API** ，以文本生成为例，单击文本生成选项框中的**创建**。

2. 在**创建Model API** 页签中，完成基本信息配置，在**大模型服务** 中，服务模型选择**单模型服务** ，**服务名称** 选择已创建的AI服务，单击**确定**完成创建。

3. 创建完成后，单击右上角**调试** ，在**路由调试** 页输入Prompt，然后单击**发送请求**。

4. 模型返回正确，则验证Model API已正确路由至指定大模型服务。

   **说明**
   * 若已创建多个大模型服务，在创建Model API时可选择**多模型服务**，并配置多个AI服务。

   * 路由规则支持通配符匹配，如`qwen*`匹配所有以qwen开头的模型名称。

   * 开启Fallback后，当主要服务出错或限流时会自动切换到备用服务。

   * 可以配置多个Fallback服务，按顺序进行故障转移。

调试完成后，返回Model API列表，单击所选Model API**实例访问入口**列下的复制按钮，用以设置Claude Code环境变量。

### 步骤3.在Claude Code中使用指定模型

#### **设置环境变量**

`ANTHROPIC_BASE_URL`：设置为步骤2中复制的Model API实例访问入口。

`ANTHROPIC_AUTH_TOKEN`：如果Model API已开启认证，并配置独立的API Key，填写对应的 API Key。如果没有开启认证，需填写一个任意值，不能填空。

```
HELPCODEESCAPE-bash
export ANTHROPIC_BASE_URL=http://env-xxxxxx-cn-hangzhou.alicloudapi.com

export ANTHROPIC_AUTH_TOKEN=xxxx
```

#### **使用指定模型启动**

以qwen3模型为例。

```
HELPCODEESCAPE-python
# 使用阿里云 qwen3 模型
claude --model qwen3-coder-plus
```

### 步骤4.验证迁移效果

启动Claude Code后，可进行以下测试验证迁移效果：

1. **基础对话测试**：输入简单问题，验证模型响应正常。

2. **代码生成测试**：要求生成特定功能的代码，测试编程能力。

3. **工具调用测试**：如果使用MCP工具，可验证工具调用功能是否正常。

4. **多模型切换测试** ：通过`--model`参数切换不同模型，验证路由功能。

<br />