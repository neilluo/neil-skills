---
source_url: https://help.aliyun.com/zh/agentcore/manage-credentials
fetch_date: 2026-09-20
product: AgentCore
slug: manage-credentials
body_sha256: b9c17cb8661f3dd797afd5617b9423e0742bba3eb9043d4c8ff90bf4624d0c1a
body_bytes: 1958
migration_status: current   # 见 FETCH-CONTRACT §3
---

## 凭证简介
凭证用于保存访问外部服务所需的认证信息。AgentCore 需要先通过凭证完成对模型供应商等外部服务的身份认证，才能正常调用其能力。目前支持的凭证类型为key-value形式，以环境变量形式提供。

## 暴露凭证的安全风险
API Key 等凭证等同于访问外部服务的身份密钥。一旦泄露，他人即可冒用该凭证调用对应服务，可能造成资费损失、配额被占用、数据泄露或服务被滥用等风险。

为降低风险，建议遵循以下做法：

* 不在代码仓库、日志、截图、聊天或工单等场景中以明文形式暴露凭证。

* 遵循最小权限原则，为不同用途或环境使用相互独立的凭证。

* 定期轮换凭证；一旦怀疑泄露，立即在对应供应商侧吊销原凭证并更换新凭证。

借助 AgentCore 的凭证统一管理，可有效降低上述风险：凭证集中存放在 Workspace 中，由Agent 等资源按需引用或绑定，无需在多处重复填写或以明文形式硬编码，从而缩小凭证的暴露面。

## 创建凭证
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在左侧导航栏点击**凭证管理**。

3. 点击右上角**创建凭证**。

4. 配置：

<table> <thead> <tr> <td> <p>参数</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Key</p> </td> <td> <p>必填。凭证的环境变量名，例如 OPENAI_API_KEY。</p> </td> </tr> <tr> <td> <p>Value</p> </td> <td> <p>必填。凭证值。默认隐藏。</p> </td> </tr> <tr> <td> <p>描述</p> </td> <td> <p>选填。凭证用途的描述信息。</p> </td> </tr> </tbody> </table>

## 管理凭证
### 查看凭证详情

点击**详情**查看凭证信息。

### 编辑凭证信息

点击**编辑**进行编辑。

### 删除凭证

点击**删除** \> **确认删除**以删除该凭证。