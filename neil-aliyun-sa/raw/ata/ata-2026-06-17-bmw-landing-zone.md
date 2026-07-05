# 宝马落地阿里云Landing Zone Accelerator：AI驱动全链路自动化方案

> **来源**：ATA | **作者**：淘飞 | **发布日期**：2026-01-14
> **URL**：https://ata.atatech.org/articles/11020552831?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE
> **SHA256**：16475af560c8d7194cb1a2b2b4fd555113e6c4bcb6c1d0f69c14c3a8f05bdd31
> **归档日期**：2026-06-28 | **状态**：raw（不可变）

---

导读 对于大部分同学来说应该是首次听到Landing Zone Accelerator这个概念，如果你对基于Terraform自动化搭建Landing Zone感兴趣，那这篇文章就是你要找的，且是历史上首次介绍 如果你对如何搭建全链路的企业级Terraform架构感兴趣，那这篇文章会回答你的问题，且包含阿里云最新提供的产品技术方案 如果你对存量资源如何通过AI高效迁移到已有Terraform架构感兴趣，那这篇文章会包含技术方案和实际客户落地案例，大概率也是历史首次 引言 提起宝马Landing Zone，可能熟悉的同学都知道在几年前宝马上云的时候就做过Landing Zone上云规划，并且我们都知道Landing Zone是一个一次性的上云规划方案，为什么宝马现在又重新再做Landing Zone的工作呢？ 带着这个疑问，我们一起看一下作为一家对技术和安全合规有着高要求的跨国企业，宝马在2025年又在Landing Zone和云上IT治理方面做了哪些工作。 同时如果你的客户有基于IaC技术自动化在阿里云上搭建Landing Zone的需求，那么我们为宝马提供的方案具备高度可复用性，可重点关注。 客户需求 起因是宝马自动驾驶业务要新上云，按要求，在应用正式上云之前同样需要通过Landing Zone做上云规划，客户就思考之前我们就做过Landing Zone，这次业务上云有没有可复用的地方，是否还需要从零到一手动搭建Landing Zone，同时宝马在中国除了华晨宝马外还有宝马中国、宝马金融等不同的业务都有对云的要求，如何做到云上基础的管理和治理框架是一致的，同时尽量自动化，而不是全部通过人工分别从零搭建。 基于此宝马提出他们要构建一套统一的云上管理、治理架构和能力，命名FPCC.NEXT（下一代公共云框架），客户向我们提出了这个想法，并与我们共同探讨如何构建。 技术方案 方案确定 初期前线同学跟客户对焦后带着下面这个图中的需求找到了包含开放平台在内的多个产品团队来沟通支持计划，看到这个脑图后我们发现客户的需求基本都是Landing Zone中的内容，包含部分云卓越架构Well-Architected Framework中的内容，因此开放平台就正式开始对接了客户这个需求。 我们到客户现场专门进行了拜访沟通需求细节，客户明确了他们的具体要求： 采用基于Terraform的IaC技术构建可复用的云上管理和治理框架，即Landing Zone 这套框架具备版本化、状态化、CICD能力 最好拥有托管式的运行环境，不用自己搭建和维护Terraform运行环境，他们现在采购了Terraform Cloud，每年付费几十万，成本太高了，也不想自己搭建维护，因为没有业务价值。 基于以上要求客户要实现整个宝马在中国不同云上业务的管理和治理架构的统一性，拉齐不同子公司和业务在云的IT治理水平，同时提升搭建效率，基于同一套IaC架构，只需要按照不同业务要求修改不同的参数配置即可自动化的搭建和维护。 我们关注到这个需求不仅仅是宝马需要，其他云上有IaC、自动话要求的客户同样有需求，且目前国内还没有云厂商能够原厂提供这样的能力，因此我们内部讨论后决定以原厂产品化方式来支持，提供可复用到不同客户的产品化解决方案。内部正式立项为Landing Zone Accelerator（Landing Zone加速器），并用脑图快速确定了整个产品方案要实现的能力，如下图： 方案研发 基于客户需求并考虑到客户复用性以及面向企业级的全链路IaC架构，我们进行了如下的方案设计： 采用基于Terraform实现IaC，并进行源码开源 版本化：集成Git，提供基于Git的IaC代码版本化管理、多人协作能力 CICD支持：基于Git支持Code Review、审批与CICD能力，同时还可以在Pipeline中添加IaC规范校验能力 托管的运行时环境：基于阿里云自动化服务台的托管式Terraform运行环境，免Terraform运行环境运维 Stack支持：阿里云自动化服务台提供了云原生的自研Stack能力 中心化状态文件管理：基于Git + 阿里云自动化服务平台提供了基于阿里云OSS的中心化Terraform State文件管理方式，更适合企业级多人协作开发。 Landing Zone业务部分我们支持了Landing Zone六大核心模块的自动化搭建，客户根据企业实际需要修改源码配置即可快速自动化搭建符合最佳实践和企业要求的云上Landing Zone框架。 过去采用IaC技术的企业一直以来都有一个困扰，由于各种原因一旦通过其他非IaC入口修改了云上资源后会带来云上资源与IaC State文件不一致的问题，从而带来资源一致性和故障风险，如何解决这个问题，我们在本次项目中为了给客户提供一个完整可靠的企业级IaC能力，我们除了满足客户业务需求外，还额外新增了IaC状态一致性保障方案，我们在自动化服务台原生支持了State Checker能力，支持定时自动检查、手动检查、CICD过程中自动检查State一致性，出现问题后显示告知客户那些资源不一致，供客户根据不同情况进行资源一致性对齐。 State Checker执行链路架构图： 方案重要特性 全链路IaC工程化能力：这是过去企业中严重缺少的能力，企业中缺少一套企业级的IaC采用最佳实践，尤其是开箱即用的标准化方案和源码，我们阿里云首次提供了，这也是国内首家提供此能力的云厂商 托管式运行引擎：过往企业要么自建维护Terraform运行时环境，或者少部分企业采购Terraform Cloud类服务，甚至部分企业在工作电脑上直接运行，在Landing Zone Accelerator项目中我们不但为客户提供了全链路符合IaC最佳实践的企业级IaC能力，同时还提供了基于阿里云自动化服务台云原生的托管式Terraform运行环境，同时还自研支持了Stack编排能力，Terraform Stack过去只有付费的Terraform Cloud客户才能使用，宝马也向我们反馈，过去他们要每年花费几十万来采购Terraform Cloud，这也是他们的痛点之一，我们的自动化服务台是提供给客户在云上构建IaC基础设施的免费云基础设施能力。 状态化管理：这是IaC中重要的概念与特性，通过Landing Zone Accelerator，可以真正让企业具备云资源的状态化、版本化管理能力，同时借助自动化服务台原生提供的State Checker能力，让客户同时具备了IaC状态文件与云端资源一致性检查能力。 AI Coding：最后不得不说的是AI Coding，项目立项之初，基于过去多年对Terraform和目前AI的了解，我们决定采用AI Coding，同时我们内部设置了一个激进的目标，计划100%通过AI Coding，最终结果验证也是完全可行的，所有代码我们基本100%都是通过AI完成的，Terraform足够标准化，所有的Terraform Provider信息都是开源的，这样AI Coding更加可行，甚至涉及到新语法的自研Stack能力通过我们提供一个语法说明和Demo后AI同样可以高质量完成，这极大降低了企业采用Landing Zone Accelerator的成本。 方案交付 按计划我们将整个交付分为了两期： 一期交付内容 源码-->Git-->自动化服务台完整IaC CICD管理流程 Landing Zone Accelerator核心模块业务代码 目标：完成核心能力研发测试后交付给客户开始试用，并基于客户实际情况解决反馈的问题 二期计划 State Checker：持续检查本地仓库与远程仓库状态一致性 完整的整体项目文档 源码开源到Github，Landing Zone Accelerator发布到官网上线 提供包含完整开源代码、官方文档的正式可对外官方发布的版本。 第一期实施 实际在第一期交付过程中，客户新提出了非常多基于实际场景的需求，比如： 多环境隔离：面向集团型企业、进行多环境隔离的企业，如何支持统一云平台团队中心化统一管控，而不是完全独立构建维护多个CICD流程 Policy分离：实际企业中对各类安全、合规等策略配置量是非常大的，这些不适合都放到同一个Terraform模板文件中，Policy内容本身要跟Policy资源进行拆分，且支持一个Policy资源包含N个Policy文件拆分管理，他们的Global在AWS上实际就是这么做的 存量资源导入：除了开源Terraform默认提供的方式外，能否有更好的存量资源迁移方式 .... 客户提出很多大大小小的新想法和需求，这些都是合理的，也都是过往几年我们拜访其他客户过程中发现的共性问题，因此我们计划将这些能多客户复用的能力都加入到项目二期中提供，完整的内容包含： 需求 进展 导入Open API 已完成 State Checker 已完成 Policy分离 已完成 多环境隔离 已完成 部署环境迁出MA账号 系统限制需要保持在MA中 宝马内部自建Github Action Runner 宝马内部解决 操作审计修改为以SLS为入口 已完成 云防火墙支持多账号+多账号Demo 已完成 账号工厂创建VPC并关联Private Zone 已完成 CloudSSO（初始化用户+支持系统设置） 已完成 全局唯一名称添加随机字符串减少人工配置 已完成 Private Zone首次开通失败问题修复 已完成 配置审计账号组支持文件夹类型 已完成 管控策略绑定支持目录名称映射 已完成 配置审计支持合规包管理 已完成 支持WAF3.0+Demo规则 已完成 账号工厂新增云监控联系人管理 已完成 自动化服务台Stack删除联动Destroy 已完成 第二期实施 标准部署 第二期交付我们按照计划为客户完整交付了整个完整的Landing Zone Accelerator能力，且客户已经预先准备好了环境，现场将他们测试环境的包含上百个云账号的Landing Zone架构迁移到了Landing Zone Accelerator新架构，值得一提的是，我们本次交付是超出了原定交付目标的。 原定目标：完成技术架构部署后帮助客户基于我们自动化服务台新发布的存量资源导入Open API完成一个Demo资源的迁入，后面更多账号、资源交给客户自行完成迁移。 实际：在完成既定部署目标后，我们现场经过快速的讨论和对焦后，决定尝试通过AI赋能帮助客户完成存量所有账号和管控策略资源的迁移，借助AI我们不但可以帮助客户解决存量迁移的重大难题，同时效率也足够高，因此我们现场连夜加班完成了迁移脚本的编写和技术验证，第二天上午到客户现场进行了迁移实施，下午我们按原差旅计划返程。 存量资源迁移 了解Terraform的同学都知道存量资源迁入Terraform管理是一件困难且耗时的事情，是挡在很多企业完全采用基于Terraform的IaC技术管理云资源的一座大山，今天随着阿里云自动化服务台资源导入Open API的开放和AI技术的成熟，让这一过程变得越来越可行。当然我们目前只完成了资源目录（云账号、组织架构）、管控策略两个大场景的验证，并没有完成所有资源的AI迁移验证，针对复杂的网络类资源相信会有更高的挑战，但这确实为我们和企业开启了一个IaC采用的新路径。 以下是部分AI生成的迁移脚本： export_rd_control_policies.py（完整可用脚本）： #!/usr/bin/env python3
"""
阿里云资源目录 (Resource Directory) - 导出管控策略到 JSON 文件
"""

import json
import os

from alibabacloud_resourcedirectorymaster20220419.client import Client as RdClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_resourcedirectorymaster20220419 import models as rd_models


def create_client(access_key_id: str, access_key_secret: str) -> RdClient:
    """创建资源目录客户端"""
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="resourcedirectory.aliyuncs.com"
    )
    return RdClient(config)


def list_control_policies(client: RdClient, policy_type: str = None) -> list:
    """列出所有管控策略"""
    runtime = util_models.RuntimeOptions()
    policies = []
    page_number = 1
    page_size = 100

    while True:
        request = rd_models.ListControlPoliciesRequest(
            page_number=page_number,
            page_size=page_size,
            policy_type=policy_type
        )

        try:
            response = client.list_control_policies_with_options(request, runtime)
            if response.body.control_policies and response.body.control_policies.control_policy:
                for policy in response.body.control_policies.control_policy:
                    policies.append({
                        "policy_id": policy.policy_id,
                        "policy_name": policy.policy_name,
                        "description": policy.description,
                        "policy_type": policy.policy_type,
                        "effect_scope": policy.effect_scope,
                        "attachment_count": policy.attachment_count
                    })

                # 检查是否还有更多页
                if len(response.body.control_policies.control_policy) < page_size:
                    break
                page_number += 1
            else:
                break
        except Exception as e:
            print(f"列出管控策略失败: {e}")
            break

    return policies


def get_control_policy_detail(client: RdClient, policy_id: str) -> dict:
    """获取管控策略详情（包含 policy_document）"""
    runtime = util_models.RuntimeOptions()
    request = rd_models.GetControlPolicyRequest(policy_id=policy_id)

    try:
        response = client.get_control_policy_with_options(request, runtime)
        if response.body.control_policy:
            policy = response.body.control_policy
            return {
                "policy_document": policy.policy_document,
                "policy_name": policy.policy_name,
                "description": policy.description
            }
    except Exception as e:
        print(f"获取策略 {policy_id} 详情失败: {e}")

    return {}


def list_target_attachments(client: RdClient, policy_id: str) -> list:
    """列出管控策略绑定的目标"""
    runtime = util_models.RuntimeOptions()
    targets = []
    page_number = 1
    page_size = 100

    while True:
        request = rd_models.ListTargetAttachmentsForControlPolicyRequest(
            policy_id=policy_id,
            page_number=page_number,
            page_size=page_size
        )

        try:
            response = client.list_target_attachments_for_control_policy_with_options(request, runtime)
            if response.body.target_attachments and response.body.target_attachments.target_attachment:
                for target in response.body.target_attachments.target_attachment:
                    targets.append(target.target_id)

                # 检查是否还有更多页
                if len(response.body.target_attachments.target_attachment) < page_size:
                    break
                page_number += 1
            else:
                break
        except Exception as e:
            print(f"获取策略 {policy_id} 的绑定目标失败: {e}")
            break

    return targets


def get_policy_tags(client: RdClient, policy_ids: list) -> dict:
    """获取管控策略的标签 {policy_id: {tag_key: tag_value}}（支持分页）"""
    if not policy_ids:
        return {}

    runtime = util_models.RuntimeOptions()
    tags_map = {}

    # 初始化所有策略为空标签
    for policy_id in policy_ids:
        tags_map[policy_id] = {}

    try:
        # ListTagResources 一次最多查询 50 个资源
        batch_size = 50
        for i in range(0, len(policy_ids), batch_size):
            batch = policy_ids[i:i + batch_size]
            next_token = None

            while True:
                request = rd_models.ListTagResourcesRequest(
                    resource_type="controlpolicy",
                    resource_id=batch,
                    max_results=100,
                    next_token=next_token
                )
                response = client.list_tag_resources_with_options(request, runtime)

                if response.body.tag_resources:
                    for tag in response.body.tag_resources:
                        # 过滤掉以 "acs:" 开头的标签
                        if tag.tag_key.startswith("acs:"):
                            continue
                        policy_id = tag.resource_id
                        if policy_id not in tags_map:
                            tags_map[policy_id] = {}
                        tags_map[policy_id][tag.tag_key] = tag.tag_value

                # 检查是否有下一页
                if response.body.next_token:
                    next_token = response.body.next_token
                else:
                    break
    except Exception:
        pass

    return tags_map


def export_policy_to_file(policy_data: dict, output_dir: str):
    """导出单个策略到 JSON 文件"""
    # 使用策略名称作为文件名，替换不合法字符
    filename = policy_data["name"].replace("/", "_").replace("\\", "_").replace(":", "_")
    filepath = os.path.join(output_dir, f"{filename}.json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(policy_data, f, ensure_ascii=False, indent=2)

    return filepath


def main():
    # 从环境变量读取 AK
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

    # 输出目录
    output_dir = "control_policies"

    if not access_key_id or not access_key_secret:
        print("错误: 请设置环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        return

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    try:
        client = create_client(access_key_id, access_key_secret)

        # 列出所有自定义管控策略（不导出系统策略）
        print("正在获取管控策略列表...")
        policies = list_control_policies(client, policy_type="Custom")

        if not policies:
            print("未找到自定义管控策略")
            return

        print(f"找到 {len(policies)} 个自定义管控策略")

        # 收集所有策略 ID 用于获取标签
        all_policy_ids = [policy["policy_id"] for policy in policies]

        # 获取所有策略的标签
        tags_map = get_policy_tags(client, all_policy_ids)

        # 处理每个策略
        for i, policy in enumerate(policies, 1):
            policy_id = policy["policy_id"]
            policy_name = policy["policy_name"]
            print(f"[{i}/{len(policies)}] 处理策略: {policy_name}")

            # 获取策略详情（包含 policy_document）
            detail = get_control_policy_detail(client, policy_id)

            # 获取绑定目标
            target_ids = list_target_attachments(client, policy_id)

            # 解析 policy_document（JSON 字符串）
            policy_document = {}
            if detail.get("policy_document"):
                try:
                    policy_document = json.loads(detail["policy_document"])
                except json.JSONDecodeError:
                    policy_document = detail["policy_document"]

            # 构建输出数据
            policy_data = {
                "name": policy_name,
                "description": policy.get("description") or "",
                "policy_document": policy_document,
                "target_ids": target_ids
            }

            # 添加标签（只有有标签时才输出）
            tags = tags_map.get(policy_id, {})
            if tags:
                policy_data["tags"] = tags

            # 导出到文件
            filepath = export_policy_to_file(policy_data, output_dir)
            print(f"  已导出到: {filepath}")

        print(f"\n完成! 共导出 {len(policies)} 个策略到 {output_dir}/ 目录")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
 export_rd_control_policy_mapping.py（完整可用脚本）： #!/usr/bin/env python3
"""
阿里云资源目录 (Resource Directory) - 导出管控策略 Terraform 资源映射
生成格式: import_and_get_result(identifier, 'preventive:alicloud_resource_manager_control_policy.default["{policy_name}"]', "{target_id}")
"""

import os

from alibabacloud_resourcedirectorymaster20220419.client import Client as RdClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_resourcedirectorymaster20220419 import models as rd_models


def create_client(access_key_id: str, access_key_secret: str) -> RdClient:
    """创建资源目录客户端"""
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="resourcedirectory.aliyuncs.com"
    )
    return RdClient(config)


def list_control_policies(client: RdClient, policy_type: str = None) -> list:
    """列出所有管控策略（支持分页）"""
    runtime = util_models.RuntimeOptions()
    policies = []
    page_number = 1
    page_size = 100

    while True:
        request = rd_models.ListControlPoliciesRequest(
            page_number=page_number,
            page_size=page_size,
            policy_type=policy_type
        )

        try:
            response = client.list_control_policies_with_options(request, runtime)
            if response.body.control_policies and response.body.control_policies.control_policy:
                for policy in response.body.control_policies.control_policy:
                    policies.append({
                        "policy_id": policy.policy_id,
                        "policy_name": policy.policy_name
                    })

                # 检查是否还有更多页
                if len(response.body.control_policies.control_policy) < page_size:
                    break
                page_number += 1
            else:
                break
        except Exception as e:
            print(f"列出管控策略失败: {e}")
            break

    return policies


def list_target_attachments(client: RdClient, policy_id: str) -> list:
    """列出管控策略绑定的目标（支持分页）"""
    runtime = util_models.RuntimeOptions()
    targets = []
    page_number = 1
    page_size = 100

    while True:
        request = rd_models.ListTargetAttachmentsForControlPolicyRequest(
            policy_id=policy_id,
            page_number=page_number,
            page_size=page_size
        )

        try:
            response = client.list_target_attachments_for_control_policy_with_options(request, runtime)
            if response.body.target_attachments and response.body.target_attachments.target_attachment:
                for target in response.body.target_attachments.target_attachment:
                    targets.append(target.target_id)

                # 检查是否还有更多页
                if len(response.body.target_attachments.target_attachment) < page_size:
                    break
                page_number += 1
            else:
                break
        except Exception as e:
            print(f"获取策略 {policy_id} 的绑定目标失败: {e}")
            break

    return targets


def export_to_file(policies_with_targets: list, output_file: str):
    """导出管控策略映射到文件"""
    # 按 policy_name 排序
    sorted_policies = sorted(policies_with_targets, key=lambda x: x["policy_name"])

    with open(output_file, "w", encoding="utf-8") as f:
        # 先输出所有 policy
        for policy in sorted_policies:
            policy_name = policy["policy_name"]
            policy_id = policy["policy_id"]
            tf_policy = f'alicloud_resource_manager_control_policy.default["{policy_name}"]'
            f.write(f'import_and_get_result(identifier, \'preventive:{tf_policy}\', "{policy_id}")\n')

        # 再输出所有 attachment
        for policy in sorted_policies:
            policy_name = policy["policy_name"]
            policy_id = policy["policy_id"]
            for target_id in policy["target_ids"]:
                attachment_key = f'{policy_name}-{target_id}'
                tf_attachment = f'alicloud_resource_manager_control_policy_attachment.default["{attachment_key}"]'
                attachment_id = f'{policy_id}:{target_id}'
                f.write(f'import_and_get_result(identifier, \'preventive:{tf_attachment}\', "{attachment_id}")\n')


def main():
    # 从环境变量读取 AK
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

    # 输出文件路径
    output_file = "rd_control_policy_mapping.csv"

    if not access_key_id or not access_key_secret:
        print("错误: 请设置环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        return

    try:
        client = create_client(access_key_id, access_key_secret)

        # 列出所有自定义管控策略
        print("正在获取管控策略列表...")
        policies = list_control_policies(client, policy_type="Custom")

        if not policies:
            print("未找到自定义管控策略")
            return

        print(f"找到 {len(policies)} 个自定义管控策略")

        # 获取每个策略的绑定目标
        policies_with_targets = []
        for i, policy in enumerate(policies, 1):
            policy_id = policy["policy_id"]
            policy_name = policy["policy_name"]
            print(f"[{i}/{len(policies)}] 处理策略: {policy_name}")

            target_ids = list_target_attachments(client, policy_id)
            policies_with_targets.append({
                "policy_id": policy_id,
                "policy_name": policy_name,
                "target_ids": target_ids
            })

        # 导出到文件
        export_to_file(policies_with_targets, output_file)

        print(f"\n已导出到 {output_file}")

        # 同时打印到控制台
        print("\n" + "=" * 40 + "\n")
        with open(output_file, "r", encoding="utf-8") as f:
            print(f.read())

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
 最终的导入脚本（仅包含1条导入脚本Demo）： # 导入资源
import_and_get_result(identifier, 'preventive:alicloud_resource_manager_control_policy.default["DenyDeleteInstance"]', "cp-AIvKzsDmOWQqnvBM")
 AI生成迁移脚本的原理： 第一步：让AI按资源类型分别生成导出阿里云不同云资源到本地Json文件和Stack的脚本（export_rd_control_policies.py），将存量云资源导出到本地环境并生成对应Terraform Stack代码 第二步：让AI按资源类型分别生成将第一步导出的资源映射到阿里云自动化服务台格式的脚本（export_rd_control_policy_mapping.py） 第三步：运行AI生成的导入脚本（一个资源对应一条导入脚本）完成资源导入 小提示：导入脚本AI用了多久几次生成的呢？一次！是的，一次！只要我们迁移脚本逻辑关系描述正确一次搞定，验证完后现场我们还是有点小震惊的。 回答2个迁移同学过程中可能会遇到的问题： Q1：不同云资源之间的资源关系怎么解决，这是过去存量资源导入难点之一 A1：由于第一步资源导出脚本中存在资源ID和资源关联ID，因此这个关系导入到Terraform后还是保留的，我们为宝马导入的资源包含了资源目录文件夹、成员账号、管控策略，这里面就是有资源关系的，成员账号属于哪个文件夹、管控策略要下发到哪个成员账号或文件夹。 Q2：资源导入到Terraform State文件后Terraform模板代码或者Terraform Stack代码怎么编写，不能手动编写吧 A2：AI生成，在第一步我们从阿里云导出资源的时候用AI自动生成了Terraform Stack代码，由于我们宝马是基于Terraform Stack做开发的，当然也可以通过脚本修改生成Terraform代码，做到存量资源100%脚本化、自动化迁移，不需要手动写代码、建立关系等操作。 Landing Zone Accelerator正式发布 方案发布 如今，Landing Zone Accelerator已经正式在官方发布并开源 官网地址：https://help.aliyun.com/zh/caf/landing-zone-accelerator 开源地址：https://github.com/aliyun/landing-zone-accelerator-on-alibaba-cloud 我们为宝马交付的是基于自动化服务台 + Git + Terraform的全链路企业级IaC架构，实际开源的时候我们会分为2部分来开源： Landing Zone Accelerator纯Terraform业务代码（已发布） 基于自动化服务台 + Git/云效的企业级IaC采用脚手架（已在宝马落地，开源流程进行中，有需要的客户已可以开始预先沟通） 这样做是为了方便不同企业的复用，不同企业可以根据自己对运行时环境、CICD流程的要求、是否采用阿里云Terraform Stack等实际情况灵活落地。 方案复用 我们在为宝马现场部署的过程中，另外一家客户桥水也并行开始了Landing Zone Accelerator能力的落地。近期有很多采用Terraform的企业，当了解到Landing Zone Accelerator能力后都很感兴趣，Landing Zone Accelerator不仅仅是Landing Zone加速器，也是一套企业采用基于Terraform实现IaC的全流程最佳实践，而这也正是过去很多企业采用Terraform过程中缺少的能力。 竞品分析 云厂商 是否支持 LZA 技术实现方式 官方名称 阿里云 是 Terraform + GitOps + 基于自动化服务台的托管式运行环境 Landing Zone Accelerator AWS 是 AWS CDK + YAML 配置驱动 AWS Landing Zone Accelerator Azure 是 Azure Policy + Terraform Azure Landing Zone Accelerator GCP 是 分阶段模块化基于Terraform部署 Cloud Foundation Fabric (Fabric FAST) 国外3朵云都提供了Landing Zone Accelerator能力，其中AWS没有基于Terraform，这也是宝马觉得不好的地方，这不利于他们进行多云管理。 国内云厂商目前还在控制台搭建和Terraform Demo的阶段，并没有提供完整功能的IaC化Landing Zone搭建能力。这也是几年前GCP提供的方式，当时受到开发者吐槽后升级为了今天分阶段模块化基于Terraform的完整解决方案。 直观来讲，如果我们将原厂提供的Landing Zone搭建能力分为3个阶段，那各云厂商所处阶段如下： 阶段 核心特征 云厂商 Level 1: 方案向导阶段 控制台有一个 Landing Zone 按钮，点点点完成基础配置 华为云、腾讯云 Level 2: IaC Demo 阶段 官方提供几个 Terraform 代码包，用户下载后自行执行 华为云、腾讯云 Level 3: 加速器框架 (LZA) 配置驱动、GitOps 支撑、支持版本升级、生命周期管理 阿里云 、AWS、Azure、GCP 总结与展望 我们结合宝马对Landing Zone架构升级的机会，从零到一新构建了基于Terraform的Landing Zone IaC化搭建和持续管理能力，这也是过去几年阿里云Landing Zone最大的一次技术升级，为采用Terraform技术来管理云资源的客户提供了整套企业级方案，尤其是国际客户更倾向采用Terraform来管理云资源，除了对外的客户采用外，对内和对伙伴通过这套标准化架构极大提升了Landing Zone交付效率。 同时，通过Landing Zone Accelerator方案我们也回答了一个问题，在实际落地过程中，阿里云对Terraform的支持度到底怎么样，Landing Zone Accelerator 100%通过阿里云原厂提供的Terraform Provider完成了整个Landing Zone上云框架的搭建，覆盖了包含资源管理、身份权限、财务、网络、安全、合规在内的Landing Zone六大核心模块，虽然目前并不是100%资源都支持Terraform管理，但客户常用的云资源基本都经过了多个客户和方案的反复验证。 宝马说，开源的方式非常好，后续我们在使用过程中遇到的问题，将通过开源渠道向你们反馈或贡献我们的使用最佳实践，未来我们会通过Landing Zone Accelerator服务更多需要通过Terraform管理云资源的上云客户，同时通过与客户的持续共建不断提升Landing Zone Accelerator的方案能力。
