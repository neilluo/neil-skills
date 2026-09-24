---
source_url: https://help.aliyun.com/zh/agentcore/service-linked-role-1
fetch_date: 2026-09-20
product: AgentCore
slug: service-linked-role-1
body_sha256: c0217c0195b6f66a05a4a8a3fe42fa689693646d3200b6406590cb89bbb5a340
body_bytes: 9211
migration_status: current
---

<br />

首次使用 AgentCore 服务前，需要创建服务关联角色，以授权 AgentCore 访问其所依赖的其他云服务。本文介绍如何创建、验证和删除 AgentCore 服务关联角色。

## 服务关联角色概述
服务关联角色（Service Linked Role，SLR）是 AgentCore 在阿里云访问控制 RAM 中预定义的角色，用于授权 AgentCore 访问其所依赖的其他云服务。首次使用 AgentCore 前必须完成服务关联角色的创建，否则 AgentCore 服务无法正常运行。

## 创建服务关联角色
首次访问 AgentCore 控制台时，系统会自动检测服务关联角色是否存在。如果角色不存在，按以下步骤完成创建。

1. 登录 [AgentCore 控制台](https://agentcore.console.aliyun.com/)。

2. 页面提示**授权服务关联角色**。

3. 单击**立即授权**。

4. 按照提示，**开通依赖云产品**，然后点击页面上的刷新按钮。

5. 角色创建成功后，页面自动跳转至 AgentCore 控制台首页，即可正常使用 AgentCore 服务。

## 验证服务关联角色
如需确认 AgentCore 服务关联角色是否已创建，可通过 RAM 控制台进行查询。

1. 登录 [RAM 控制台](https://ram.console.aliyun.com/roles)，进入**角色**页面。

2. 在搜索框中输入 Magic 并搜索。

3. 如果列表中显示对应角色，表示服务关联角色已创建成功。

## 服务关联角色权限说明
### AliyunServiceRoleForAgentCore

#### **应用场景**

允许 AgentCore 操作安全组、OSS、AI网关等云产品的操作，以便完成 AgentCore 实例的相关配置

#### **权限说明**

```
HELPCODEESCAPE-json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "oss:PutBucket",
        "oss:ListOssBucket",
        "oss:ListBuckets",
        "oss:GetBucketAcl",
        "oss:PutBucketTagging"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cms:PutWorkspace",
        "ram:CreateServiceLinkedRole",
        "cms:CreateEntityStore",
        "cms:CreateUmodel",
        "cms:ListWorkspaces",
        "log:GetLogStoreLogs",
        "cms:GetServiceObservability",
        "cms:CreateServiceObservability"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "airegistry:GetNamespace",
        "airegistry:ListNamespaces",
        "airegistry:ListSkills",
        "airegistry:Read",
        "airegistry:Write",
        "mse:ListSkills",
        "airegistry:GetSkillDetail",
        "mse:GetSkillDetail",
        "airegistry:GetSkillVersionDetail",
        "mse:GetSkillVersionDetail",
        "airegistry:CreateSkillDraft",
        "mse:CreateSkillDraft",
        "airegistry:UpdateSkillDraft",
        "mse:UpdateSkillDraft",
        "airegistry:DeleteSkillDraft",
        "mse:DeleteSkillDraft",
        "airegistry:DownloadSkillVersion",
        "mse:DownloadSkillVersion",
        "airegistry:AttachSecurityGroupToVpcEndpoint",
        "airegistry:ListVpcEndpointServiceZones",
        "airegistry:CreateVpcEndpoint",
        "airegistry:GetVpcEndpoint",
        "airegistry:ListVpcEndpoints",
        "airegistry:CreateNamespaceWithSource"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:GetObject",
        "oss:GetObjectAcl",
        "oss:GetObjectTagging",
        "oss:DeleteObject",
        "oss:DeleteObjectTagging",
        "oss:PutObject",
        "oss:PutObjectAcl",
        "oss:PutObjectTagging",
        "oss:RestoreObject",
        "oss:ListObjects",
        "oss:ListObjectVersions"
      ],
      "Resource": "acs:oss:*:*:hiclaw-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "apig:CreateGateway",
        "apig:DeleteGateway",
        "apig:GetGateway",
        "apig:GetConsumer",
        "apig:BatchDeleteConsumerAuthorizationRule",
        "apig:CreateConsumer",
        "apig:CreateConsumerAuthorizationRule",
        "apig:CreateConsumerAuthorizationRules",
        "apig:DeleteConsumer",
        "apig:DeleteConsumerAuthorizationRule",
        "apig:GetConsumerAuthorizationRule",
        "apig:ListConsumerAuthorizationRules",
        "apig:QueryConsumerAuthorizationRules",
        "apig:RemoveConsumerAuthorizationRule",
        "apig:UpdateConsumer",
        "apig:UpdateConsumerAuthorizationRule",
        "apig:ListConsumers",
        "apig:CreateService",
        "apig:CreateHttpApi",
        "apig:UpdateService",
        "apig:DeleteHttpApi",
        "apig:DeleteService",
        "apig:ListHttpApis",
        "apig:ListServices",
        "apig:DeployHttpApi",
        "apig:CreateHttpApiRoute",
        "apig:CreatePolicy",
        "apig:CreatePolicyAttachment",
        "apig:DeletePolicy",
        "apig:ListHttpApiRoutes",
        "apig:UpdateHttpApiRoute",
        "apig:CreateMcpServer",
        "apig:DeployMcpServer",
        "apig:GetMcpServer",
        "apig:ImportHttpApi",
        "apig:ListPluginClasses",
        "apig:CreatePluginAttachment",
        "apig:CreateAndAttachPolicy",
        "apig:UpdateMcpServer",
        "apig:UpdatePluginAttachment",
        "apig:ListPolicies",
        "apig:UpdateAndAttachPolicy",
        "apig:UnDeployMcpServer",
        "apig:DeleteMcpServer",
        "apig:ListMcpServers",
        "apig:ListDomains",
        "apig:CreateDomain",
        "apig:GetHttpApi",
        "apig:GetService",
        "apig:GetEnvironment",
        "apig:UpdateHttpApi",
        "apig:InvokeHttpApi",
        "apig:ListSslCerts",
        "apig:UpdateDomain",
        "apig:UndeployHttpApi",
        "apig:RemoveConsumerAuthorizationRule",
        "apig:UpdateNetworkAccess"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecs:BatchValidateSecurityGroup",
        "ecs:DescribeSecurityGroupAttribute",
        "ecs:DescribeSecurityGroupReferences",
        "ecs:DescribeSecurityGroups",
        "ecs:DescribeSecurityGroupSnapshotAttributes",
        "ecs:ValidateSecurityGroup",
        "ecs:ApplySecurityGroupSnapshot",
        "ecs:AssociateSecurityGroupSnapshotPolicy",
        "ecs:AuthorizeSecurityGroup",
        "ecs:AuthorizeSecurityGroupEgress",
        "ecs:ConfigureSecurityGroupPermissions",
        "ecs:CreateSecurityGroup",
        "ecs:CreateSecurityGroupSnapshotPolicy",
        "ecs:DeleteSecurityGroup",
        "ecs:DeleteSecurityGroupSnapshotPolicy",
        "ecs:ModifySecurityGroupAttribute",
        "ecs:ModifySecurityGroupEgressRule",
        "ecs:ModifySecurityGroupPolicy",
        "ecs:ModifySecurityGroupRule",
        "ecs:ModifySecurityGroupSnapshotPolicy",
        "ecs:RevokeSecurityGroup",
        "ecs:RevokeSecurityGroupEgress",
        "ecs:UnassociateSecurityGroupSnapshotPolicy",
        "ecs:DescribeSecurityGroupSnapshotPolicies",
        "ecs:DescribeSecurityGroupSnapshots",
        "ecs:DescribeSnapshotPolicyAssociatedSecurityGroups",
        "ecs:DescribeNetworkInterfaces",
        "ecs:CreateNetworkInterface",
        "ecs:DeleteNetworkInterface",
        "ecs:CreateNetworkInterfacePermission",
        "ecs:DescribeNetworkInterfacePermissions",
        "ecs:DeleteNetworkInterfacePermission",
        "ecs:DescribeNetworkInterfaceAttribute",
        "ecs:AddTags",
        "ecs:DescribeEipAddresses",
        "ecs:ListTagResources"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "vpc:DescribeVSwitchAttributes",
        "vpc:CreateNatGateway",
        "vpc:DescribeVpcs",
        "vpc:DescribeNatGateways",
        "vpc:AllocateEipAddress",
        "vpc:DescribeEipAddresses",
        "vpc:AssociateEipAddress",
        "vpc:CreateSnatEntry",
        "vpc:DescribeSnatTableEntries"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "privatelink:CreateVpcEndpoint",
        "privatelink:DeleteVpcEndpoint",
        "privatelink:UpdateVpcEndpointAttribute",
        "privatelink:GetVpcEndpointAttribute",
        "privatelink:ListVpcEndpointServicesByEndUser"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "bss:ModifyInstance",
      "Resource": "*"
    },
    {
      "Action": "ram:DeleteServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "magic.aliyuncs.com"
        }
      }
    },
    {
      "Action": "ram:CreateServiceLinkedRole",
      "Resource": "*",
      "Effect": "Allow",
      "Condition": {
        "StringEquals": {
          "ram:ServiceName": "privatelink.aliyuncs.com"
        }
      }
    }
  ]
}
```

## 删除服务关联角色
**警告**

删除服务关联角色后，AgentCore 服务将无法正常运行。如需重新使用 AgentCore，须再次创建服务关联角色。请谨慎操作。

删除前，请确保满足以下条件：

* AgentCore workspace下无运行中的 Agent。

* 没有依赖该角色的其他资源。

确认满足以上条件后，登录 [RAM 控制台](https://ram.console.aliyun.com/roles)，进入**角色** 页面，找到 AgentCore 服务关联角色并点击**删除角色**。