---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/security-and-compliance/ai-gateway-system-permission-policy-reference
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-gateway-system-permission-policy-reference
body_sha256: d53a32db9ff4a1bc4f078f8a16de898cfe29ab51b5da4314707a84522d205810
body_bytes: 2841
migration_status: current
---

本文描述AI网关支持的所有系统权限策略及其对应的权限描述，供您授权RAM身份时参考。  

## **什么是系统权限策略**
权限策略是用语法结构描述的一组权限的集合，可以精确地描述被授权的资源集、操作集以及授权条件。阿里云访问控制（RAM）产品提供了两种类型的权限策略：系统策略和自定义策略。系统策略统一由阿里云创建，策略的版本更新由阿里云维护，用户只能使用不能修改。自定义策略由用户管理，策略的版本更新由用户维护。用户可以自主创建、更新和删除自定义策略。在产品迭代过程中，APIG会向系统策略中添加新的权限，用来支持新的功能和能力。系统策略的更新将会影响所有授予了该策略的 RAM 身份，包括 RAM 用户、RAM 用户组和 RAM 角色。有关 RAM 权限策略的更多信息，请参阅[权限策略概览](https://help.aliyun.com/document_detail/93732.html)。  
**说明**

产品系统策略旨在帮助用户快速入门，仅需简单配置即可通过控制台访问该产品及其依赖产品。虽然系统策略包含的权限同样适用于 OpenAPI 或 CLI 等访问方式，但为了提高安全性，我们推荐您在这些场景下使用自定义策略，按需授予人员及应用特定 API 的访问权限。

系统策略可进一步细分为产品系统策略、服务角色策略和服务关联角色策略三类。部分云产品仅提供三类策略中的一类或两类，请以本文实际展示的策略类型为准。

## 产品系统策略
### AliyunAPIGFullAccess

您可以将 AliyunAPIGFullAccess 策略授权给RAM身份。本策略定义了管理 AI 网关的权限。

### AliyunAPIGReadOnlyAccess

您可以将 AliyunAPIGReadOnlyAccess 策略授权给RAM身份。本策略定义了 AI 网关的只读权限。

## 服务关联角色策略
### AliyunServiceRolePolicyForNativeApiGw

APIG使用服务关联角色 AliyunServiceRoleForNativeApiGw 来访问您在其他云产品中的资源。AliyunServiceRolePolicyForNativeApiGw是AliyunServiceRoleForNativeApiGw专用的授权策略。本策略由APIG定义和使用，您不能修改或删除，请勿将其授权给服务关联角色之外的RAM身份。

## 授权操作参考
RAM 身份默认没有任何权限，需要由阿里云账号管理员为其授权后才能访问阿里云账号下的资源。为保证资源的数据安全，建议您遵循最小授权原则为允许访问云资源的身份授予恰好够用的权限。授权的详细操作请参见：

* [管理RAM用户的权限](https://help.aliyun.com/document_detail/116146.html)

* [为RAM用户组授权](https://help.aliyun.com/document_detail/116815.html)

* [管理RAM角色的权限](https://help.aliyun.com/document_detail/116147.html)