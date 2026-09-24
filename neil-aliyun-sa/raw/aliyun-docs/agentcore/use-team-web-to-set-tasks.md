---
source_url: https://help.aliyun.com/zh/agentcore/use-team-web-to-set-tasks
fetch_date: 2026-09-20
product: AgentCore
slug: use-team-web-to-set-tasks
body_sha256: a25aee7981c5025fcd665292bb6624d718b4928e9608181595d47e381d812e53
body_bytes: 5609
migration_status: current
---

定时任务用于让 Agent 按预设的时间或频率自动执行指定任务。本文介绍如何进入协作客户端，以及创建和管理定时任务。  

## 使用说明
定时任务的调度能力基于阿里云 SchedulerX。需要周期性或定点执行的工作，如日报、定期巡检，可以交给 Agent 自动完成，无需每次手动触发。

## 应用场景
* 周期性报告：让 Agent 按天或按周汇总相关信息并生成报告，如每日项目进展摘要。

* 定期巡检：让 Agent 定期检查服务或任务状态，发现异常时主动向团队汇报。

* 定时提醒：让 Agent 在指定时间向团队发送提醒，如会议提醒、截止事项通知。

## 进入协作客户端
定时任务在协作客户端（AgentTeams）中创建和管理。进入协作客户端的步骤如下：

1. 在左侧导航栏，点击Team 协作。

2. 在接入管理页签的连接点区域，找到协作客户端 (WEB)卡片。

3. 点击打开，进入协作客户端登录页。

4. 在登录页展开Matrix 实例设置，配置Homeserver URL。Homeserver URL 为协作客户端 (API)连接点的公网 URL。

5. 输入用户的密码，登录进入团队工作区。

6. 在左侧导航栏，点击定时任务，进入定时任务页面。

## 创建定时任务
1. 在定时任务配置页签，点击新定时任务。

2. 填写任务标题。

3. 选择目标团队。

4. 选择指派，即执行该任务的 Agent。

5. 选择优先级。优先级分为紧急、高、中、低，默认为中。

6. 选择执行周期和时间，如每天 19:00、每小时第 30 分。

7. 填写任务内容。

8. 点击创建定时任务。

## 管理定时任务
### 查看定时任务概况

在定时任务配置页签顶部，可以查看定时任务概况。
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>定时任务总数</p> </td> <td> <p>创建的定时任务总数。</p> </td> </tr> <tr> <td> <p>已启用</p> </td> <td> <p>已启用的定时任务个数。</p> </td> </tr> <tr> <td> <p>未启用</p> </td> <td> <p>未启用的定时任务个数。</p> </td> </tr> </tbody> </table>

### 查看任务信息

定时任务配置页签以卡片展示各定时任务。页面上方可以搜索任务、按团队和状态筛选，或勾选只看我创建的。
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>任务标题</p> </td> <td> <p>定时任务的标题。</p> </td> </tr> <tr> <td> <p>任务内容</p> </td> <td> <p>定时任务执行的具体内容。</p> </td> </tr> <tr> <td> <p>优先级</p> </td> <td> <p>任务的优先级，分为紧急、高、中、低。</p> </td> </tr> <tr> <td> <p>执行周期</p> </td> <td> <p>任务的执行周期和时间，如每天 19:00。</p> </td> </tr> <tr> <td> <p>分配给</p> </td> <td> <p>执行该任务的 Agent。</p> </td> </tr> <tr> <td> <p>目标团队</p> </td> <td> <p>任务归属的团队。</p> </td> </tr> </tbody> </table>

### 启用或禁用定时任务

可以通过卡片上的开关开启/关闭定时任务。

### 编辑定时任务

点击编辑，可以编辑定时任务的配置。

### 手动执行

点击手动执行，可以立即手动执行一次定时任务。

### 执行记录

点击执行记录，可以查看该定时任务的执行记录。

### 删除定时任务

点击删除，可以删除定时任务。

## 查看执行记录
定时任务页面包含定时任务配置和执行记录两个页签。在执行记录页签，可以查看定时任务的执行情况。

页面上方可以按团队、任务和状态筛选执行记录，并切换查看活跃任务或归档任务。
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>执行时间</p> </td> <td> <p>任务的执行时间。</p> </td> </tr> <tr> <td> <p>任务</p> </td> <td> <p>执行记录对应的定时任务。</p> </td> </tr> <tr> <td> <p>任务耗时</p> </td> <td> <p>本次任务执行的耗时。</p> </td> </tr> <tr> <td> <p>状态</p> </td> <td> <p>任务的执行状态。</p> </td> </tr> </tbody> </table>

## 查看任务
任务页面展示团队工作区内的全部任务。

页面上方可以查看任务概况和任务状态分布。
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>任务总数</p> </td> <td> <p>任务的总数。</p> </td> </tr> <tr> <td> <p>待确认</p> </td> <td> <p>待确认的任务个数。</p> </td> </tr> </tbody> </table>

任务页面以看板形式按状态分为待确认、已创建、执行中、已完成和已取消五列。页面上方可以新建任务、搜索任务、按团队筛选，或勾选只看我创建的；右侧可以切换查看活跃任务或归档任务。
<table> <thead> <tr> <td> <p>字段</p> </td> <td> <p>说明</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>任务标题</p> </td> <td> <p>任务的标题。</p> </td> </tr> <tr> <td> <p>任务内容</p> </td> <td> <p>任务的具体内容。</p> </td> </tr> <tr> <td> <p>优先级</p> </td> <td> <p>任务的优先级。</p> </td> </tr> <tr> <td> <p>分配给</p> </td> <td> <p>执行该任务的 Agent。</p> </td> </tr> <tr> <td> <p>团队</p> </td> <td> <p>任务归属的团队。</p> </td> </tr> </tbody> </table>