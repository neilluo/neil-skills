---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-billing-activation
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-billing-activation
body_sha256: da1afa81070d2fd731b5efed233fcceda0313c2b051d516578f1c287dc546720
body_bytes: 2694
migration_status: current
---

AgentCore 自北京时间 2026 年 09 月 18 日 00:00:00 起开启计费服务。首次使用或此前已使用 AgentCore 的用户，需在控制台完成服务开通后继续使用。  

## 概述
AgentCore 自北京时间 2026 年 09 月 18 日 00:00:00 起开启计费服务。首次使用或此前已使用 AgentCore 的用户，需在控制台完成**服务开通**后继续使用。开通行为本身不产生费用，您已有的 Agent 资产与配置在开通后原样可用。

## 计费生效时间
<table> <thead> <tr> <td><p><b>项</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>生效时间</p></td> <td><p>2026 年 09 月 18 日 00:00:00（GMT+8）</p></td> </tr> <tr> <td><p>生效后</p></td> <td><p>按实际资源消耗按量计费</p></td> </tr> </tbody> </table>

## 为什么需要手动开通
AgentCore 是独立的云服务商品，计费关系需由账号本人确认。开通过程不涉及数据搬迁或资产重建。

## 如何开通
1. 登录 AgentCore 控制台，页面将提示当前账号未开通服务。

2. 点击**立即开通** ，在确认弹窗中核对计费方式与用户协议，点击**确认开通**。

3. 按引导完成服务关联角色授权与依赖云产品开通。

4. 开通成功后返回控制台，即可继续使用。

**说明**

若为子账号，可能提示权限不足，请联系主账号管理员完成授权后重试。

## 存量资产与数据是否受影响
**不受影响。** 具体如下：
<table> <thead> <tr> <td><p><b>对象</b></p></td> <td><p><b>开通后表现</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>Agent / 用户eam</p></td> <td><p>完整保留，可直接运行</p></td> </tr> <tr> <td><p>Skill / MCP Server / Agent模板</p></td> <td><p>完整保留，配置与版本不变</p></td> </tr> <tr> <td><p>模型与凭证配置</p></td> <td><p>完整保留，无需重新配置</p></td> </tr> <tr> <td><p>历史会话、运行与观测记录</p></td> <td><p>保留，可继续查看</p></td> </tr> <tr> <td><p>正在运行的任务</p></td> <td><p>不受影响，继续执行</p></td> </tr> <tr> <td><p>协作配置（已开通协作管控面者）</p></td> <td><p>保留，可通过客户端继续使用</p></td> </tr> </tbody> </table>

## 未开通时的表现
* 已有Agent和相关资产继续可用

* 无法通过控制台进行Agent和资产管理

* 如果长期未开通，公测期间创建的workspace及其资源将会被释放，具体释放时间另行通知

## 计费规则
请参考[AgentCore 计费说明](https://help.aliyun.com/document_detail/3057998.html)。