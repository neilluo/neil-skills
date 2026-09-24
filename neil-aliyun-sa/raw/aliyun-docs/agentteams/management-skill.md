---
source_url: https://help.aliyun.com/zh/agentteams/management-skill
fetch_date: 2026-09-20
product: AgentTeams
slug: management-skill
body_sha256: e8eb2118b88163053c72134fa46c33029d1136ec78904c3af1f770324dc07304
body_bytes: 3964
migration_status: migrated-legacy
---

<br />

智能体需要调用专业技能（Skill），例如发送通知、查询数据或触发工作流。本文介绍如何管理 Skill。

## **导入Skill**
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Skill 管理**。

3. 点击**导入 Skill**。

4. 选择方式：

   1. **上传文件**：将本地已打包为ZIP格式的Skill上传到控制台。

   2. **Nacos CLI** ：使用 Nacos CLI 工具将本地 Skill 文件夹导入控制台。按照页面提示操作。

   3. **导入预置Skill**：搜索预置的 Skill 模板并导入。

5. 点击**确认导入**。

## 创建和管理Skill
1. 登录 AgentTeams[控制台](https://agentteams.console.aliyun.com/)。

2. 在实例详情页左侧导航栏，点击**Skill 管理**。

3. 点击**新建 Skill**，配置以下信息。

   <table> <thead> <tr> <td> <p><b>参数</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>Skill 名称</b></p> </td> <td> <p>Skill 名称。对应<b>SKILL.md</b>的name字段。</p> </td> </tr> <tr> <td> <p><b>描述</b></p> </td> <td> <p>描述Skill信息，包含Skill的调用时机。对应<b>SKILL.md</b>的description字段。</p> </td> </tr> <tr> <td> <p><b>SKILL.md</b></p> </td> <td> <p>SKill的详细内容。</p> </td> </tr> </tbody> </table>
4. 点击**立即创建**。

5. 在**Skill 管理**页面，可以查看已创建的Skill。

6. 选中Skill，点击**详情**可以进入Skill详情页。

7. 选中Skill，点击**删除**可以删除Skill。

## 对Skill进行内容审核
新建的Skill版本状态为**草稿**，未正式发布。在发布前需要进行内容审核。

1. 对内容审核进行授权：在Skill详情页，如果提示需要授权角色进行内容审核，则点击**授权**。

2. 点击**提交审核** ，点击**确定**。

3. 等待安全监测完成。

   * 如果提示**安全检测通过**，则可以继续发布。

   * 否则，点击**查看结果**，根据提示修复内容中存在的风险。

## 发布Skill
只有**安全检测通过** 的Skill草稿，才能够发布。发布后该版本将对外提供服务。

1. 在Skill详情页，点击**发布版本**。

2. 点击**确定**。

3. 版本状态由**草稿** 变为**已发布**。

## 管理Skill版本
### 创建版本

1. 在Skill详情页，点击**基于此版本创建草稿**。

2. 输入**版本号**。

3. 点击**保存为草稿**。

4. 新版本的状态为**草稿**，未正式发布。

### 编辑Skill草稿

1. 在Skill详情页，点击**编辑草稿**，可以修改Skill的草稿内容。

2. 点击**保存**。

### 删除Skill草稿

1. 在Skill详情页，点击**删除草稿**。

2. 点击**确定**。

### 下线版本

1. 在Skill详情页，点击**下线版本**。

2. 点击**确定**。

3. 该版本的状态为**已下线**，该版本不再对外提供服务。

4. 若需要重新上线该版本，则点击**重新上线版本** ，点击**确定** 。该版本的状态变为**已发布**。

### 编辑版本标签

1. 在Skill详情页，点击**版本标签** 右侧的**编辑**。

2. 新增或删除版本标签。

3. 点击**保存**。

## 启用或禁用Skill
1. 在Skill详情页，在**Skill 信息** 区域，找到**状态** ，开启或关闭**已启用**开关。

2. 点击**确定**。

3. 启用Skill后，最新**已发布**版本的Skill对外提供服务；禁用Skill后，所有版本将不再对外提供服务。

## 配置Skill可见性
1. 在Skill详情页，在**Skill 信息** 区域，找到**可见性** ，开启或关闭**私有**开关。

2. 点击**确定**。

3. 将Skill设为公开后，所有人可见；设为私有后，仅自己与指定用户可见。

## 将Skill下载到本地
参考页面中**手动下载 Skill 文件** 以及**NPX 下载**区域的提示，执行操作。

<br />