---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/security-and-compliance/custom-permission-policy-reference-for-ai-gateway
fetch_date: 2026-09-21
product: AI Gateway
slug: custom-permission-policy-reference-for-ai-gateway
body_sha256: d1ba8d2fc3b8028c43db483fed460660d5b5fac7c291e4eafbf46986f6b374e9
body_bytes: 2894
migration_status: current
---

如果系统权限策略不能满足您的要求，您可以创建自定义权限策略实现最小授权。使用自定义权限策略有助于实现权限的精细化管控，是提升资源访问安全的有效手段。本文介绍AI网关使用自定义权限策略示例。  

## **什么是自定义权限策略**
在基于RAM的访问控制体系中，自定义权限策略是指在系统权限策略之外，您可以自主创建、更新和删除的权限策略。自定义权限策略的版本更新需由您来维护。

* 创建自定义权限策略后，需为RAM用户、用户组或RAM角色绑定权限策略，这些RAM身份才能获得权限策略中指定的访问权限。

* 已创建的权限策略支持删除，但删除前需确保该策略未被引用。如果该权限策略已被引用，您需要在该权限策略的引用记录中移除授权。

* 自定义权限策略支持版本控制，您可以按照RAM规定的版本管理机制来管理您创建的自定义权限策略版本。

## 操作文档
* [创建自定义权限策略](https://help.aliyun.com/document_detail/93733.html)

* [修改自定义权限策略内容和备注](https://help.aliyun.com/document_detail/116802.html)

* [删除自定义权限策略](https://help.aliyun.com/document_detail/116803.html)

* [管理权限策略授权](https://help.aliyun.com/document_detail/116818.html#task-221551)

* [管理自定义权限策略版本](https://help.aliyun.com/document_detail/116817.html)

## 配置AI网关常用自定义授权样例
* 示例1：授予RAM用户对AI网关实例gw-cpnx\*\*\*\*\*\*\*的读写权限。

  需要替换`regionId`与`accountId`为该网关的地域ID与云账号ID。

  ```
  HELPCODEESCAPE-json
  {
    "Statement": [
      {
        "Action": "apig:*",
        "Resource": [
          "acs:apig:*:*:gateway/gw-cpnx*******",
          "acs:apig:regionId:accountId:service/*"
        ],
        "Effect": "Allow"
      },
      {
        "Action": [
          "apig:Check*",
          "apig:ListGateway"
        ],
        "Resource": "*",
        "Effect": "Allow"
      }
    ],
    "Version": "1"
  }
  ```

* 示例2：授予RAM用户对AI网关API列表api-cpo22t5lhtgxxxxxx的读写权限。

  ```
  HELPCODEESCAPE-json
  {
    "Statement": [
      {
        "Action": [
          "apig:*"
        ],
        "Resource": "acs:apig:*:*:httpapi/api-cpo22t5lhtgxxxxxx",
        "Effect": "Allow"
      }
    ],
    "Version": "1"
  }
  ```

* 示例3：授予RAM用户对AI网关所有资源的读权限。

  ```
  HELPCODEESCAPE-json
  {
    "Version": "1",
    "Statement": [
      {
        "Action": [
          "apig:Check*",
          "apig:List*",
          "apig:Get*",
          "apig:Export*",
          "apig:Query*",
          "apig:Debug*"
        ],
        "Resource": "acs:apig:*:*:*",
        "Effect": "Allow"
      }
    ]
  }
  ```