---
source_url: https://help.aliyun.com/zh/agentcore/manage-skill
fetch_date: 2026-09-20
product: AgentCore
slug: manage-skill
body_sha256: c1bfb9dddeffcf4c32134deafeed5c06c86dc22b502240c5204cb3e9b489cae2
body_bytes: 3127
migration_status: current   # 见 FETCH-CONTRACT §3
---

智能体需要调用专业技能（Skill），例如发送通知、查询数据或触发工作流。本文介绍如何管理 Skill。  

## **创建和管理Skill**
1. 登录 [AgentCore](https://agentcore.console.aliyun.com/)控制台。

2. 在Workspace详情页左侧导航栏，点击**Skill 管理**。

3. 点击**创建 Skill**。

4. 选择方式：

   1. 上传技能包：将本地已打包为ZIP格式的Skill上传到控制台。

   2. **Nacos CLI** ：使用 Nacos CLI 工具将本地 Skill 文件夹导入控制台。按照页面提示操作。

   3. **通过Markdown定义** ：配置**Skill 名称** 、**描述** ，并在**Markdown内容**下输入Skills.md进行配置。可以设置Skill的可见性。

5. 点击**立即创建**。

6. 选中Skill，点击**详情**可以进入Skill详情页。

7. 选中Skill，点击**删除**可以删除Skill。

## 从Skill广场导入Skill
1. 登录 AgentCore 控制台。

2. 在Workspace详情页左侧导航栏，点击**Skill 管理**。

3. 切换到Skill 广场。

4. 选择需要导入的Skill。

5. 点击**详情**可以进入Skill详情页。

6. 点击**导入**可以进入导入页面。

7. 点击**确认导入**。

## 对Skill进行内容审核
新建的Skill版本状态为**草稿**，未正式发布。在发布前需要进行内容审核。

1. 对内容审核进行授权：在Skill详情中的**内容与调试**页查看Skill的详细信息。

2. 点击**提交审核** ，点击**确定**。

3. 等待安全监测完成。

   * 如果提示**安全检测通过**，则可以继续发布。

   * 否则，点击**查看结果**，根据提示修复内容中存在的风险。

## 发布Skill
只有**安全检测通过** 的Skill草稿，才能够发布。发布后该版本将对外提供服务。

1. 在Skill详情页的**版本管理** ，点击**发布**。

2. 点击**确认发布**。

3. 版本状态由**草稿** 变为**已发布**。

## 管理Skill版本
### 创建版本

1. 在**版本管理** 页，点击**创建版本**。

2. 配置**基于此版本创建**、新版本号和变更说明。

3. 点击创建版本。

### 编辑Skill草稿

1. 在内容与调试页面，选择对应版本号，可以修改Skill的草稿内容。

2. 点击保存变更。

### 编辑版本标签

1. 在Skill详情页的概览，点击**版本标签** 右侧的**编辑**。

2. 新增或删除版本标签。

3. 点击**保存**。

## 启用或禁用Skill
1. 在Skill详情页的概览部分，在基本信息区域，找到**状态**，开启或关闭开关。

2. 点击**确定**。

3. 启用Skill后，最新**已发布**版本的Skill对外提供服务；禁用Skill后，所有版本将不再对外提供服务。

## 配置Skill可见性
1. 在Skill详情页的概览部分，在基本信息区域，找到**可见性** ，开启或关闭**私有**开关。

2. 点击**确定**。

3. 将Skill设为公开后，所有人可见；设为私有后，仅自己与指定用户可见。

## 将Skill下载到本地
1. 在Skill详情页的版本管理部分，找到需要下载的Skill版本。

2. 点击下载。

<br />