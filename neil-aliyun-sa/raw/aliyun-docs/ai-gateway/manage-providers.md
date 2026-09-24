---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-providers
fetch_date: 2026-09-21
product: AI Gateway
slug: manage-providers
body_sha256: d46da71511db2cf25cbe2e70f996573e1f307fe2733d68c5a4302cf7fce98877
body_bytes: 3552
migration_status: current
---

AI 网关通过供应商（Provider）资源标识和管理模型服务的提供方，本文介绍如何在 AI 网关实例中管理供应商，包括查看、创建、编辑和删除操作。  

## 供应商概述
供应商是 AI 网关中用于标识模型和服务所属大模型供应商的资源。系统支持预置供应商，也可以创建自定义供应商，也可创建自定义供应商。

* **预置供应商**：系统内置，不可编辑和删除，可被模型和服务引用。

* **自定义供应商**：用户自行创建，可编辑名称，可删除（需无引用）。

供应商与服务的**供应商配置模版**为独立概念，不互相影响。

## 前提条件
* 已[创建网关实例](https://help.aliyun.com/document_detail/2881527.html)。

除上述条件外，管理供应商无需额外的 RAM 权限、实例规格或地域限制。

## 查看供应商列表
1. 登录[AI 网关控制台](https://apig.console.aliyun.com/?spm=5176.6660585.apigateway_aipost_public_cn-top.i1.29127992temjdc#/ai-gateway-overview)，在网关列表页选择实例所在的地域，并单击目标实例 ID。

2. 在左侧导航栏单击**模型元信息管理**，进入模型管理页面。

3. 单击**供应商**页签，查看当前实例下的供应商列表。

供应商列表包含以下列：
<table> <thead> <tr> <td><p><b>列名</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>名称</p></td> <td><p>供应商的展示名称</p></td> </tr> <tr> <td><p>标识</p></td> <td><p>系统自动生成的唯一标识</p></td> </tr> <tr> <td><p>关联模型数</p></td> <td><p>当前供应商绑定的模型数量</p></td> </tr> <tr> <td><p>更新时间</p></td> <td><p>最近一次资源更新时间</p></td> </tr> <tr> <td><p>操作</p></td> <td><p>查看、编辑、删除</p></td> </tr> </tbody> </table>

## 创建供应商
1. 在供应商列表中，单击**创建供应商**。

2. 打开创建面板，配置以下参数：

   <table> <thead> <tr> <td><p><b>参数</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>名称</p></td> <td><p>必填。供应商的展示名称，支持重名。</p></td> </tr> <tr> <td><p>标识</p></td> <td><p>必填。由系统自动生成，创建后不可编辑，页面中为禁用态。</p></td> </tr> </tbody> </table>
3. 配置完成后，单击**确定**。新供应商将出现在供应商列表中。

## 编辑供应商
1. 在供应商列表中，找到目标自定义供应商。预置供应商不可编辑。

2. 单击操作列的**编辑**，修改名称。标识不可修改。

3. 单击**确定**保存。页面提示保存成功后，供应商列表中展示更新后的名称。

## 删除供应商
1. 在供应商列表中，找到目标自定义供应商。预置供应商不可删除。

2. 单击操作列的**删除** ，在确认弹窗中单击**确定**。

**成功标志**：供应商从列表中移除。

若供应商已被模型或服务引用，则禁止删除。弹窗将显示关联的模型或服务列表，请先前往对应页面解除引用后再执行删除。

## 供应商在服务中的引用
创建或编辑服务时，可在**高级设置**中关联供应商。

具体操作请参见[创建服务](https://help.aliyun.com/document_detail/2881570.html)。

**高级设置** 中的**供应商** 字段与**供应商配置模版**为两个独立概念，不互相筛选、不互相继承配置。