---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-services
fetch_date: 2026-09-21
product: AI Gateway
slug: manage-services
body_sha256: d75d45968d34da7aee45327c87cd91b2837506721c14257d175663fcd61bac8a
body_bytes: 2003
migration_status: current
---

在AI 网关中添加固定地址来源的服务的后端节点地址可能发生变更，而该服务没有注册到网关服务来源，网关无法动态获取该服务的后端节点地址。需要通过变更服务手动调整服务的后端节点地址，以便网关获取。本文介绍如何查看、编辑和删除服务。  

## **查看服务**
服务创建成功后，可以查看服务。如果服务较多，还可以通过筛选、搜索来提高查找效率。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务**。

5. 查看**服务** 时，可以通过服务名称的关键字或**服务来源**的类别进行筛选。

## 编辑服务
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**服务**页签。

5. 单击需要变更的服务**操作** 列下的**编辑** 。在**编辑服务** 面板，修改服务相关参数，然后单击**确定**。

   **说明**

   您可以编辑由您自己创建的静态IP服务和DNS服务。其他类型的服务不允许编辑，例如从ACK导入的服务。

## 删除服务
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击目标**实例ID**。

4. 在左侧导航栏，单击**服务** ，并单击**服务**页签。

5. 单击需要变更的服务**操作** 列下的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4995459171/p812574.png) \> **删除** ，在确认删除对话框中单击**确定**。