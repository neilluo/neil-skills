---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/routing-management
fetch_date: 2026-09-21
product: AI Gateway
slug: routing-management
body_sha256: 3210a7e03a0c4cabb3c58aef25146c5312603a6489cc8f73ddba384321ec1745
body_bytes: 3176
migration_status: current
---

Agent API 支持自定义路由，您可以按请求特征进行精细化路由的能力。本文介绍Agent API的自定义路由管理。  

## **创建路由**
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**，进入目标API页面。

3. 单击**创建路由** ，在**创建路由**面板，进行如下配置：

   * **路由名称**：自定义路由名称。

   * **路径（Path）**：设置匹配HTTP请求中的Path参数。

     * 相同匹配规则时Path越长优先级越高。

     * 不同匹配规则时**等于** \> **前缀是** \> **正则匹配**。

       * **等于** ：即完全匹配。例如，Path等于`/user`。

       * **前缀是** ：以前缀作为匹配条件。例如，Path以`/user`开头。

       * **正则匹配**：以正则表达式作为匹配条件。

   * **更多匹配规则** ：如需创建多个相同路径的路由，需要对**方法（Method）** 、**请求头（Header）** 和**请求参数（Query）**进行配置，以区分不同路由。

   * **服务列表**：在服务列表中选择服务。默认不展示以consumers开头的服务。

## 编辑路由
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**，进入目标API页面。

3. 在路由列表页面选择目标路由，单击页面右侧**编辑路由** ，完成**基本信息** 和**后端服务** 配置修改。单击**确定**即可完成路由修改。

## 发布路由
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**，进入目标API页面。

3. 在路由列表页面选择目标路由，单击页面右侧**发布路由** ，在确认弹框中单击**确定**，即可对已创建的路由进行发布。

## 下线路由
1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**，进入目标API页面。

3. 在路由列表页面选择目标路由，单击页面右侧![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3359958471/p962889.png)图标，然后单击**下线** ，在**确认下线** 弹框中单击**下线**，即可完成路由下线。

## 删除路由
**说明**

您可以将已创建但未发布的路由或已下线的路由删除。

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)，选择您实例所在的地域。

2. 进入目标实例页面，选择左侧导航栏的**Agent API**，进入目标API页面。

3. 在路由列表页面选择目标路由，单击页面右侧![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3359958471/p962889.png)图标，然后单击**删除** ，在删除路由弹框中单击**删除**，即可完成路由删除。