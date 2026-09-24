---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/security-and-compliance/service-association-role-provided-only-when-involved-otherwise-no-need
fetch_date: 2026-09-21
product: AI Gateway
slug: service-association-role-provided-only-when-involved-otherwise-no-need
body_sha256: 7c009c4450d6c5cb396ecc4413877de467ecc5edabc08a5ecb4d04cb3785edd4
body_bytes: 14652
migration_status: current
---

AI网关服务关联角色是为实现特定功能而设计的预定义RAM角色。本文将介绍AI网关服务关联角色的应用场景以及如何管理服务关联角色。  

## 服务关联角色的应用场景
* **AliyunServiceRoleForNativeApiGw** ：当AI网关需要访问[专有网络VPC](https://help.aliyun.com/document_detail/34217.html)、[容器服务 Kubernetes 版](https://help.aliyun.com/document_detail/86737.html#concept-cbm-1zc-l2b)、[函数计算FC](https://help.aliyun.com/document_detail/2511874.html)、[企业级分布式应用服务EDAS](https://help.aliyun.com/document_detail/42934.html#concept-2038209)、[微服务引擎MSE](https://help.aliyun.com/document_detail/126761.html)、[负载均衡SLB](https://help.aliyun.com/document_detail/196874.html)、[负载均衡NLB](https://help.aliyun.com/document_detail/439121.html)、[云服务器ECS](https://help.aliyun.com/document_detail/25367.html)、[应用实时监控服务ARMS](https://help.aliyun.com/document_detail/42781.html)等云服务的资源时，可通过自动创建的AI网关服务关联角色AliyunServiceRoleForNativeApiGw获取访问权限。

* **AliyunServiceRoleForNativeApiGwInvokeFC**：当AI网关需要调用FC服务时，可通过自动创建的AI网关服务关联角色AliyunServiceRoleForNativeApiGwInvokeFC完成网关功能。

* **AliyunServiceRoleForNativeApiGwInvokeKMS** ：当云原生API网关需要调用密钥管理KMS服务时，可通过自动创建的云原生API网关服务关联角色`AliyunServiceRoleForNativeApiGwInvokeKMS`获取访问权限。

## RAM用户使用服务关联角色需要的权限
如果使用RAM用户创建或删除服务关联角色，必须联系管理员为该RAM用户授予管理员权限（AliyunNativeApiGwFullAccess）或在自定义权限策略的`Action`语句中为RAM用户添加以下权限：

* 创建服务关联角色：`ram:CreateServiceLinkedRole`

* 删除服务关联角色：`ram:DeleteServiceLinkedRole`

关于授权的详细操作，请参见[服务关联角色](https://help.aliyun.com/document_detail/160674.html#concept-2448621/section-x3u-5xc-09l)。

## 权限说明
## AliyunServiceRoleForNativeApiGw
AI网关服务关联角色（AliyunServiceRoleForNativeApiGw）具备的访问权限说明如下：

## 专有网络VPC
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "vpc:AllocateEipAddress",
        "vpc:AllocateEipAddressPro",
        "vpc:DescribeEipAddresses",
        "vpc:AssociateEipAddress",
        "vpc:UnassociateEipAddress",
        "vpc:ReleaseEipAddress",
        "vpc:ModifyEipAddressAttribute",
        "vpc:ModifyBypassToaAttribute",
        "vpc:AddCommonBandwidthPackageIp",
        "vpc:RemoveCommonBandwidthPackageIp",
        "vpc:TagResources",
        "vpc:DescribeVSwitches",
        "vpc:DescribeVSwitchAttributes",
        "vpc:DescribeVpcs",
        "vpc:CreateVSwitch",
        "vpc:DescribeVpcAttribute",
        "vpc:DescribeVRouters",
        "vpc:DescribeRouteTables",
        "vpc:DescribeRouteEntryList"
      ],
      "Resource": "*"
}
```

## 容器服务ACK
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "cs:DescribeClusterDetail",
        "cs:DescribeClusterInnerServiceKubeconfig",
        "cs:RevokeClusterInnerServiceKubeconfig",
        "cs:GetUserConfig",
        "cs:DescribeClusterUserKubeconfig",
        "cs:GetClusterById",
        "cs:GetClustersByUid",
        "cs:DescribeClustersV1",
        "cs:ListClusters",
        "cs:GetClusters",
        "cs:DescribeClusterNodePools"
      ],
      "Resource": "*"
}
```

## 函数计算FC
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "fc:ListAliases",
        "fc:ListServices",
        "fc:ListServiceVersions",
        "fc:ListFunctions",
        "fc:ListFunctionVersions",
        "fc:ListTriggers"
      ],
      "Resource": "*"
}
```

## 企业级分布式应用服务EDAS
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "edas:ReadNamespace",
        "edas:ReadService",
        "edas:ListUserDefineRegion"
      ],
      "Resource": "*"
}
```

## 微服务引擎MSE
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "mse:ListAnsServices",
        "mse:ListEngineNamespaces",
        "mse:ListClusters",
        "mse:QueryConfig"
      ],
      "Resource": "*"
}
```

## 负载均衡SLB
```
HELPCODEESCAPE-json
 {
      "Effect": "Allow",
      "Action": [
        "slb:SetLoadBalancerName",
        "slb:CreateLoadBalancer",
        "slb:AddBackendServers",
        "slb:SetBackendServers",
        "slb:RemoveBackendServers",
        "slb:CreateLoadBalancerTCPListener",
        "slb:DescribeLoadBalancerTCPListenerAttribute",
        "slb:SetLoadBalancerTCPListenerAttribute",
        "slb:CreateLoadBalancerHTTPListener",
        "slb:DescribeLoadBalancerHTTPListenerAttribute",
        "slb:SetLoadBalancerHTTPListenerAttribute",
        "slb:CreateLoadBalancerHTTPSListener",
        "slb:DescribeLoadBalancerHTTPSListenerAttribute",
        "slb:SetLoadBalancerHTTPSListenerAttribute",
        "slb:StartLoadBalancerListener",
        "slb:StopLoadBalancerListener",
        "slb:DeleteLoadBalancerListener",
        "slb:DescribeLoadBalancers",
        "slb:DescribeLoadBalancerAttribute",
        "slb:DescribeHealthStatus",
        "slb:CreateLoadBalancerForCloudService",
        "slb:DeleteLoadBalancer",
        "slb:ModifyLoadBalancerInternetSpec",
        "slb:RemoveTags",
        "slb:AddTags",
        "slb:SetLoadBalancerUDPListenerAttribute",
        "slb:CreateLoadBalancerUDPListener",
        "slb:CreateVServerGroup",
        "slb:DeleteVServerGroup",
        "slb:SetVServerGroupAttribute",
        "slb:ModifyVServerGroupBackendServers",
        "slb:AddVServerGroupBackendServers",
        "slb:ModifyLoadBalancerInstanceSpec",
        "slb:ModifyLoadBalancerInternetSpec",
        "slb:RemoveVServerGroupBackendServers",
        "slb:SetLoadBalancerModificationProtection",
        "slb:SetLoadBalancerDeleteProtection",
        "slb:DescribeLoadBalancerUDPListenerAttribute  ",
        "slb:DescribeTags",
        "slb:DescribeVServerGroups",
        "slb:DescribeVServerGroupAttribute",
        "slb:DescribeLoadBalancerListeners",
        "slb:ListTagResources",
        "slb:TagResources",
        "slb:UntagResources"
      ],
      "Resource": "*"
}
```

## 负载均衡NLB
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "nlb:TagResources",
        "nlb:UnTagResources",
        "nlb:ListTagResources",
        "nlb:CreateLoadBalancer",
        "nlb:DeleteLoadBalancer",
        "nlb:GetLoadBalancerAttribute",
        "nlb:ListLoadBalancers",
        "nlb:UpdateLoadBalancerAttribute",
        "nlb:UpdateLoadBalancerAddressTypeConfig",
        "nlb:UpdateLoadBalancerZones",
        "nlb:CreateListener",
        "nlb:DeleteListener",
        "nlb:ListListeners",
        "nlb:UpdateListenerAttribute",
        "nlb:StopListener",
        "nlb:StartListener",
        "nlb:GetListenerAttribute",
        "nlb:GetListenerHealthStatus",
        "nlb:CreateServerGroup",
        "nlb:DeleteServerGroup",
        "nlb:UpdateServerGroupAttribute",
        "nlb:AddServersToServerGroup",
        "nlb:RemoveServersFromServerGroup",
        "nlb:UpdateServerGroupServersAttribute",
        "nlb:ListServerGroups",
        "nlb:ListServerGroupServers",
        "nlb:LoadBalancerLeaveSecurityGroup",
        "nlb:LoadBalancerJoinSecurityGroup",
        "nlb:GetJobStatus",
        "nlb:UpdateLoadBalancerProtection"
      ],
      "Resource": "*"
}
```

## 云服务器ECS
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "ecs:CreateSecurityGroup",
        "ecs:AuthorizeSecurityGroup",
        "ecs:AuthorizeSecurityGroupEgress",
        "ecs:RevokeSecurityGroup",
        "ecs:RevokeSecurityGroupEgress",
        "ecs:DeleteSecurityGroup",
        "ecs:JoinSecurityGroup",
        "ecs:LeaveSecurityGroup",
        "ecs:DescribeSecurityGroups",
        "ecs:DescribeInstances",
        "ecs:CreateNetworkInterface",
        "ecs:DeleteNetworkInterface",
        "ecs:DescribeNetworkInterfaces",
        "ecs:CreateNetworkInterfacePermission",
        "ecs:DescribeNetworkInterfacePermissions",
        "ecs:DeleteNetworkInterfacePermission",
        "ecs:DescribeSecurityGroupAttribute",
        "ecs:AddTags",
        "ecs:DescribeEipAddresses",
        "ecs:DescribeNetworkInterfaceAttribute",
        "ecs:ModifyNetworkInterfaceAttribute",
        "ecs:AssignPrivateIpAddresses",
        "ecs:UnassignPrivateIpAddresses",
        "ecs:AssignIpv6Addresses",
        "ecs:UnassignIpv6Addresses",
        "ecs:AttachNetworkInterface",
        "ecs:DetachNetworkInterface",
        "ecs:ListTagResources"
      ],
      "Resource": "*"
}
```

## 应用实时监控服务ARMS
```
HELPCODEESCAPE-json
{
      "Effect": "Allow",
      "Action": [
        "arms:OpenArmsService",
        "arms:GetAlertRules",
        "arms:ReportCustomIncidents",
        "arms:AddPrometheusInstance",
        "arms:GetAuthToken",
        "arms:GetClusterAllUrl",
        "arms:OpenArmsServiceSecondVersion",
        "arms:CheckServiceStatus",
        "arms:OpenVCluster",
        "arms:GetPrometheusApiToken",
        "arms:ListDashboards",
        "arms:GetExploreUrl",
        "arms:CreateDefaultCloudProductPrometheusAlertRule",
        "arms:ListNotificationPolicies",
        "arms:ListDispatchRule",
        "arms:CreateDispatchRule",
        "arms:CreateOrUpdateNotificationPolicy",
        "arms:DescribeContactGroups",
        "arms:SearchContactGroup",
        "arms:CreatePrometheusAlertRule"
      ],
      "Resource": "*"
    }
```

## AliyunServiceRoleForNativeApiGwInvokeFC
AI网关服务关联角色（AliyunServiceRoleForNativeApiGwInvokeFC）具备的访问权限说明如下：

```
HELPCODEESCAPE-json
{
    "Effect": "Allow",
    "Action": "fc:InvokeFunction",
    "Resource": "*"
}
```

### AliyunServiceRoleForNativeApiGwInvokeKMS

AI网关服务关联角色（AliyunServiceRoleForNativeApiGwInvokeKMS）具备的访问权限说明如下：

```
HELPCODEESCAPE-json
{
    "Effect": "Allow",
    "Action": [
        "kms:ListKmsInstances",
        "kms:ListKeys",
        "kms:GenerateDataKey",
        "kms:Decrypt",
        "kms:CreateSecret",
        "kms:DeleteSecret",
        "kms:UpdateSecret",
        "kms:DescribeSecret",
        "kms:GetSecretValue",
        "kms:PutSecretValue",
        "kms:TagResource",
        "kms:UntagResource"
    ],
    "Resource": "*"
}
```

## 查看服务关联角色
当服务关联角色创建成功后，您可以在[RAM控制台的角色页面](https://ram.console.aliyun.com/roles)，通过搜索服务关联角色名称（AliyunServiceRoleForNativeApiGw、AliyunServiceRoleForNativeApiGwInvokeFC）查看该服务关联角色的以下信息：

* **基本信息**

  在AliyunServiceRoleForNativeApiGw或AliyunServiceRoleForNativeApiGwInvokeFC角色详情页面的**基本信息**区域，查看角色基本信息，包括角色名称、创建时间、角色ARN和备注等。
* **权限策略**

  在AliyunServiceRoleForNativeApiGw或AliyunServiceRoleForNativeApiGwInvokeFC角色详情页面的**权限管理**页签，单击权限策略名称，查看权限策略内容以及该角色可授权访问哪些云资源。
* **信任策略**

  在AliyunServiceRoleForNativeApiGw或AliyunServiceRoleForNativeApiGwInvokeFC角色详情页的**信任策略管理** 页签，查看信任策略内容。信任策略是描述RAM角色可信实体的策略，可信实体是指可以扮演RAM角色的实体用户身份。服务关联角色的可信实体为云服务，您可以通过信任策略中的`Service`字段查看。

关于如何查看服务关联角色的详细操作，请参见[查看RAM角色](https://help.aliyun.com/document_detail/116241.html#task-188120)。

## 删除服务关联角色
**说明**

当长时间不使用AI网关时，可前往[RAM控制台](https://ram.console.aliyun.com/)手动删除服务关联角色。
1. 使用阿里云账号登录[RAM控制台](http://ram.console.aliyun.com/)，在左侧导航栏中单击**身份管理** \> **角色**。

2. 在**角色** 页面的搜索框输入您希望删除的角色名称（例如`AliyunServiceRoleForNativeApiGw`）。

3. 在搜索结果中找到目标角色，单击其**操作** 列下的**删除角色**。

4. 在弹出的确认对话框中，输入角色名称进行二次确认，然后单击**删除角色**。

**重要**

删除云原生API网关服务关联角色后，依赖该角色的功能将无法正常使用，请谨慎删除。

## 常见问题
## 为什么我的RAM用户无法自动创建AI网关服务关联角色（AliyunServiceRoleForNativeApiGw）？
您需要拥有指定的权限，才能自动创建或删除AliyunServiceRoleForNativeApiGw。因此，在RAM用户无法自动创建AliyunServiceRoleForNativeApiGw时，您需要为其添加以下权限策略。

```
HELPCODEESCAPE-json
{
    "Statement": [
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "acs:ram:*:主账号ID:role/*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": [
                        "nativeapigw.aliyuncs.com"
                    ]
                }
            }
        }
    ],
    "Version": "1"
}
```

**说明**

请将主账号ID替换为您实际的阿里云账号ID。

## 为什么我的RAM用户无法自动创建AI网关服务关联角色（AliyunServiceRoleForNativeApiGwInvokeFC）？
您需要拥有指定的权限，才能自动创建或删除AliyunServiceRoleForNativeApiGwInvokeFC。因此，在RAM用户无法自动创建AliyunServiceRoleForNativeApiGwInvokeFC时，您需要为其添加以下权限策略。

```
HELPCODEESCAPE-json
{
    "Statement": [
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "acs:ram:*:主账号ID:role/*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": [
                        "invokefc.nativeapigw.aliyuncs.com"
                    ]
                }
            }
        }
    ],
    "Version": "1"
}
```

**说明**

请将主账号ID替换为您实际的阿里云账号ID。

## 相关文档
更多关于服务关联角色的信息，请参见[服务关联角色](https://help.aliyun.com/document_detail/160674.html#concept-2448621)。