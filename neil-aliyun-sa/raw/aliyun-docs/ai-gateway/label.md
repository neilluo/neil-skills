---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/label
fetch_date: 2026-09-21
product: AI Gateway
slug: label
body_sha256: 7080671b38f9b217274ae32fcf2b899db92ef18bab1eee037b0b0ce81f3f063a
body_bytes: 1975
migration_status: current
---

标签是云资源的标识，帮助您从不同维度对具有相同特征的云资源进行分类、搜索和聚合，提高资源管理效率。本文介绍如何编辑和使用标签。  

## 使用说明
* 产品标签、设备标签和分组标签的结构为**标签键** ：**标签值**。

  **重要**

  ACS开头的标签为系统预留标签，请勿使用此值作为标签的**标签键**。
* 每个AI网关实例最多可设置20个标签。

## 编辑标签
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

<!-- -->

3. AI网关提供了两种添加应用标签的方式：在实例页面编辑和在基本信息页签编辑。

   * **在实例页面编辑** ：在目标实例的**标签** 列，将鼠标悬停至![标签](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3157482371/p878426.png)图标，然后在弹出的气泡中单击**编辑**。

   * **基本信息页签编辑** ：单击目标实例ID，在**基本信息** 页签的**基本信息** 区域，单击**标签** 所在单元格的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2272676371/p903972.png)图标。

4. 在**编辑标签**页面，可以增加、删除和修改标签。

   * 增加或修改标签：填写**标签键** 和**标签值** ，然后单击**确定**。

   * 删除标签：单击对应标签右侧的![删除](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3157482371/p878425.png)图标，然后单击**确定**。

## 使用标签过滤
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**实例**，并在顶部菜单栏选择地域。

3. 在**实例** 页面，单击**标签筛选**，选择需要过滤的标签键。或者在搜索框中输入标签键搜索，可以过滤出使用此标签的实例。