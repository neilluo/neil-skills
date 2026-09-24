---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/resource-group
fetch_date: 2026-09-21
product: AI Gateway
slug: resource-group
body_sha256: c66c98c3680b0cbc6c876971f19b2bf18d88d8e61ecf49e3c99afe1ed23b6fdc
body_bytes: 2818
migration_status: current
---

资源组对您拥有的云资源从用途、权限、归属等维度上进行分组，实现企业内部多用户、多项目的资源分级管理。一个云资源只能属于一个资源组，云资源之间的关联关系不会因加入资源组而发生变化。本文介绍如何管理、配置资源组，以及如何通过资源组筛选实例。  

## 使用说明
* 一个资源组可以包含不同地域的云资源。例如，资源组A中可以同时包含华北2（北京）地域和华东1（杭州）地域的实例。

* 资源组会继承RAM用户（子账号）的全局权限。即如果您授权RAM用户管理所有的阿里云资源，那么阿里云账号（主账号）下所有的资源组也会出现在该RAM用户中。

## 管理资源组
关于如何增加、删除、修改和查看资源组，请参见[管理资源组](https://help.aliyun.com/document_detail/94383.html)。

## 设置资源组
**说明**

如果您没有选择资源组，系统会自动将该资源归属到**默认资源组**。

### 创建实例时设置

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标地域，并单击**创建实例**。

2. 在产品购买页面，选择该实例归属**资源组** 。其他参数配置，请参见[创建网关实例](https://help.aliyun.com/document_detail/2881527.html#bb12f8672d7l0)。

### 创建域名时设置

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，单击**域名**，并在顶部菜单栏选择地域。

3. 单击**添加域名** ，并在添加域名面板中，选择该域名归属**资源组** 。其他参数配置，请参见[创建域名](https://help.aliyun.com/document_detail/2881840.html)。

### 创建 Model API时设置

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Model API** ，然后单击**创建Model API**。

3. 在**创建Model API** 面板中，选择该API归属**资源组** 。其他参数配置，请参见[创建Model API](https://help.aliyun.com/document_detail/2859333.html#9d7f312e31snz)。

### 创建 Agent API时设置

1. 打开[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)**实例** 页面，在顶部菜单栏选择目标实例所在地域，并单击目标**实例ID**。

2. 在左侧导航栏，单击**Agent API** ，然后单击**创建 Agent API**。

3. 在**创建Model API** 面板中，选择该API归属**资源组** 。其他参数配置，请参见[创建Agent API](https://help.aliyun.com/document_detail/2937089.html#11c3f902e3aqz)。