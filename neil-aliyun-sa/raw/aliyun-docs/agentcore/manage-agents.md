---
source_url: https://help.aliyun.com/zh/agentcore/manage-agents
fetch_date: 2026-09-20
product: AgentCore
slug: manage-agents
body_sha256: e3d0b72debf609002a36fd1f4fc6ac03a3310bec4da10b10554a6306cf5952c3
body_bytes: 3155
migration_status: current   # 见 FETCH-CONTRACT §3
---

## 创建 Agent
### 选择创建方式

点击**创建Agent**后，先选择创建方式：

* **托管 Harness**：选定 Harness 后托管运行，Agent 模板可选。以下步骤以该方式为例。

* **自定义代码 / 镜像** ：使用容器镜像部署，支持自定义逻辑。具体操作请参见[高代码 Agent 部署与使用指南](https://help.aliyun.com/document_detail/3062132.html)。

* **快速创建**：表单式低代码创建，即将上线。

### 基本信息

1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在左侧导航栏，点击Agent。

3. 点击**创建Agent**。

4. 选择**托管Harness**。

   1. 选择Harness。

   2. 选择是否使用模板配置Agent。

   3. 填写**Agent 名称**。

   4. 进行模型连接并选择模型。

   5. （可选）填写**描述**。

#### **Token 配额**

可以通过开关开启/关闭Token配额管理功能，输入配额上限并选择计量周期（天/周/月）来实现。

### 文件配置

输入Agent的系统提示词来描述Agent的角色、职责和工作方式。  
**说明**

未选择 Agent 模板时，仅需填写系统提示词，无需准备 SOUL.md / AGENTS.md。

### Agent 资产配置

创建页以页签形式提供 Skill、SubAgent、工具、知识库、凭证五类资产，可按需绑定。

#### **Skill**

可以从左侧选择可用技能为Agent绑定该Skill。

#### **SubAgent**

点击**添加SubAgent**为Agent添加SubAgent。需要配置SubAgent的名称及系统提示词、Skill等信息。

#### **工具**

可在该页签中为Agent绑定工具。

#### **知识库**

可在该页签中为Agent绑定知识库。

#### **凭证**

可以从左侧选择可用凭证为Agent绑定该凭证。

### 资源配置

* **规格**：选择实例所需的 CPU 和内存。

* **实例最大Session数**：设置单个实例承载的 Session 数量上限。

* **Session TTL（秒）**：设置平台 Session 的存活时间参数；这不是模型单次生成的超时时间。

* **自动扩缩容** ：开启后需设置**最小实例数** 与**最大实例数**。

### 网络配置

* **允许默认网卡访问公网**：Agent 需要访问公网模型服务或其他公网接口时，按需开启。

* **允许访问 VPC**：Agent 需要访问 Workspace 的 VPC 资源时，按需开启。开启后使用当前 Workspace 的 VPC 配置。

完成以上配置后，点击**立即创建**以创建Agent。

## 管理Agent
1. 点击**详情**，可以查看Agent信息。

2. 点击**删除**，可以删除已创建的Agent。

3. 点击编辑，可以编辑Agent信息。

## 查看Agent概况
可以从顶部查看Agent工作情况。
<table> <thead> <tr> <td> <p><b>字段</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Agent总数</b></p> </td> <td> <p>创建的Agent总数。</p> </td> </tr> <tr> <td> <p><b>运行Agent</b></p> </td> <td> <p>正常运行的Agent 个数。</p> </td> </tr> <tr> <td> <p><b>异常Agent</b></p> </td> <td> <p>异常状态的Agent 个数。</p> </td> </tr> </tbody> </table>