---
source_url: https://help.aliyun.com/zh/agentteams/billings-of-agentteams
fetch_date: 2026-09-20
product: AgentTeams
slug: billings-of-agentteams
body_sha256: 3da60590c2e2f3c7e0b85856a180a62aff60552fbea8d72d1d666d60e7bc9e4f
body_bytes: 3327
migration_status: migrated-legacy
---

AgentTeams 当前处于公测阶段，产品本身免费。但使用 AgentTeams 需要开通 9 个阿里云云产品作为底层依赖，这些产品按各自的计费规则独立计费，是使用前需要了解的主要成本来源。  

## 产品自身费用
AgentTeams 公测期间免费。创建实例时会跳转至售卖页，但当前无需支付费用。

## 依赖产品费用
首次使用 AgentTeams 时，需要完成[服务开通流程](https://help.aliyun.com/document_detail/3040378.html)。服务开通过程中，系统要求依次开通以下 8 个云产品；此外，实例创建时系统会使用 SLS（日志服务）。以上共 9 个依赖产品均按各自的计费规则独立计费，不包含在 AgentTeams 的免费范围内。
<table> <thead> <tr> <td><p><b>产品</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>开通方式</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><b>OSS（对象存储）</b></p></td> <td><p>提供文件和数据存储能力</p></td> <td><p>跳转 OSS 控制台开通</p></td> </tr> <tr> <td><p><b>ACS（容器计算服务）</b></p></td> <td><p>提供容器运行环境</p></td> <td><p>跳转 ACS 控制台开通</p></td> </tr> <tr> <td><p><b>CMS（云监控）</b></p></td> <td><p>用于写入 Tracing 数据</p></td> <td><p>跳转云监控控制台开通</p></td> </tr> <tr> <td><p><b>AI 网关</b></p></td> <td><p>提供 AI 模型调用的网关服务</p></td> <td><p>跳转 AI 网关控制台开通</p></td> </tr> <tr> <td><p><b>AI Registry</b></p></td> <td><p>提供Agent资产管理能力</p></td> <td><p>跳转 AI Registry 控制台开通</p></td> </tr> <tr> <td><p><b>PrivateLink（私网连接）</b></p></td> <td><p>提供私网访问能力</p></td> <td><p>系统自动开通</p></td> </tr> <tr> <td><p><b>SchedulerX3</b></p></td> <td><p>提供分布式任务调度能力</p></td> <td><p>跳转售卖页购买</p></td> </tr> <tr> <td><p><b>ACS Sandbox</b></p></td> <td><p>提供沙箱运行环境</p></td> <td><p>跳转售卖页购买</p></td> </tr> <tr> <td><p><b>SLS（日志服务）</b></p></td> <td><p>提供日志采集与存储能力</p></td> <td><p>实例创建时系统自动使用</p></td> </tr> </tbody> </table>  
**说明**

以上 8 个产品全部就绪后才能正常使用 AgentTeams。前 7 个产品的开通状态可在 AgentTeams 控制台的服务开通引导页查看。  
**重要**

如果当前账号的 SLS 项目数已达到配额上限，实例创建将显示**创建暂停** 状态。需要在 SLS 控制台释放不再使用的项目或申请提升配额，然后在 AgentTeams 控制台单击**重试**恢复创建流程。

## 实例运行时可选费用
创建 AgentTeams 实例后，根据配置需要，可能产生以下可选费用。

### NAT 网关和弹性公网 IP（EIP）

在实例详情页为 Worker 配置公网访问（SNAT）时，可以选择：

* **新建 NAT 网关**：同时需要选择或新建 EIP（弹性公网 IP）。NAT 网关和 EIP 均为独立付费资源，按各自产品定价收费。

* **使用已有 NAT 网关**：在已有 NAT 网关上添加 SNAT 规则，不额外产生 NAT 网关购买费用，但仍需关联 EIP。

如果 Worker 不需要访问公网，可跳过 NAT 网关配置，不产生此项费用。