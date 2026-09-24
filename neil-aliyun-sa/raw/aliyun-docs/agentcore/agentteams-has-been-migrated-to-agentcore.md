---
source_url: https://help.aliyun.com/zh/agentcore/agentteams-has-been-migrated-to-agentcore
fetch_date: 2026-09-20
product: AgentCore
slug: agentteams-has-been-migrated-to-agentcore
body_sha256: 7212d3cfde13c172127d8bc2cd53289a63763c773160b89677e92e65a5f86e42
body_bytes: 9426
migration_status: migrated-legacy
---

通过官方交互式迁移服务，将一个 AgentTeams（AT）实例的控制面资源迁移至一个新的 AgentCore（AC）Workspace。本文介绍迁移的适用范围、限制条件、环境准备和完整操作步骤，帮助完成从 AT 到 AC 的平滑过渡。  

## 适用范围
本迁移适用于将一个 AT 实例迁移至一个新的 AC Workspace。默认在同一地域创建同名 Workspace；如需跨地域迁移，需要在迁移过程中单独确认。

可迁移的控制面资源包括：Workspace 网络配置、协作能力、本地 User、模型供应商/模型、凭证元数据、MCP、Skill、Agent 模板、纳管 Agent、Team 配置。

## 迁移限制
以下内容不在本次迁移范围内：

* OSS 中 Agent 的运行时数据，包括运行期间产生的配置、记忆、临时产物、任务产物及相关持久化数据。

* 账号集成中的钉钉、飞书同步配置。

* Agent 的外部访问配置。

* 历史任务、会话、调用与用量数据。

* 业务连通性、第三方服务可用性和业务验收。

  新 Workspace 会生成新的 Endpoint。迁移完成后，需结合业务安排完成调用方切换、外部渠道验证和业务验收。

迁移期间，不要对所选 AT 实例进行创建、更新或删除。若源端资源发生变更，需暂停迁移并重新执行资源清单与导出，以保证迁移结果与源端一致。

迁移服务会先展示源端资源清单。源端明确返回停止、禁用、失败、删除等异常状态的资源只会在清单中说明，不会导出、进入迁移计划或在 AC 创建；源接口未返回状态不视为异常。

## 前提条件
开始迁移前，确认以下条件已满足：

* 具备读取源 AT 实例并在目标地域创建 AC Workspace 及其资源所需的操作权限。

* 本次迁移使用阿里云主账号。

* 已准备可用的阿里云 CLI Profile，或已明确确认使用默认 Profile。

* 已确定用于列出 AT 实例的源 Region。

  如需跨地域迁移，还需注意以下事项：
* 跨地域迁移需在迁移流程中单独确认目标地域。

* 默认在源实例所在地域创建同名的新 Workspace；跨地域时需额外指定目标地域。

  迁移服务会先列出该 Region 中可用的 AT 实例供选择，无需自行前往控制台查询实例 ID。

## 迁移准备
### 安装迁移 Skill

从 AgentCore 团队提供的发布渠道获取对应版本的 `migrate-agentteams-agentcore-*.zip`。当前交付包可从[官方下载链接](https://agentteams-release-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/asserts/agentteams-to-agentcore-migration-tool-20260831.zip)获取。安装包包含以下三个 Skill，首次使用时都需要安装：

* `alibabacloud-agentteams-manage`：管理和查看源端 AgentTeams（AT）实例及其资源。

* `alibabacloud-agentcore-manage`：管理和查看目标 AgentCore（AC）Workspace 及其资源。

* `migrate-agentteams-agentcore`：按确认的范围执行 AT 到 AC 的迁移。

  首次安装时，将三个目录安装到当前用户的 `.agents` Skill 目录：

```
HELPCODEESCAPE-bash
unzip -q ~/Downloads/migrate-agentteams-agentcore-*.zip -d ~/Downloads/migrate-agentteams-agentcore-install
mkdir -p ~/.agents/skills
package=~/Downloads/migrate-agentteams-agentcore-install/migrate-agentteams-agentcore
cp -R "$package/bundled-skills/alibabacloud-agentteams-manage" ~/.agents/skills/
cp -R "$package/bundled-skills/alibabacloud-agentcore-manage" ~/.agents/skills/
cp -R "$package" ~/.agents/skills/migrate-agentteams-agentcore
```

安装后，重新打开一个支持 `.agents` Skill 的 Agent 会话，并使用 `$migrate-agentteams-agentcore` 发起迁移。若任一同名 Skill 已存在，按最新发布说明完成升级；如本地有自定义内容，先备份或请求服务支持后再更新。

### 准备阿里云 CLI

迁移 Skill 依赖以下本机组件：

* 阿里云 CLI `aliyun`，版本 3.3.0 或更高。

* AgentTeams 插件 `aliyun-cli-agentteams`。

* AgentCore 插件 `aliyun-cli-agentcore`。

  阿里云 CLI 的安装和更新请参考[安装/更新 CLI](https://help.aliyun.com/document_detail/121541.html)。安装基础 CLI 后，执行以下命令安装插件：

```
HELPCODEESCAPE-bash
aliyun plugin install --names aliyun-cli-agentteams
aliyun plugin install --names aliyun-cli-agentcore
```

迁移服务会在开始前检查 CLI 和插件是否可用；只有获得确认后才会执行本地检查或安装。

### 准备工作目录

迁移服务会在确认后创建一个仅当前用户可访问的本地工作目录，用于保存迁移过程中的必要文件和最终报告。建议在桌面使用以下目录格式：

```
HELPCODEESCAPE-plaintext
/Users/<当前用户>/Desktop/agentteams-to-agentcore-<源实例名称或ID>-<日期>
```

同一实例在同一天再次发起迁移时，使用新的目录；续跑已有迁移时，使用原目录。

迁移服务会持续展示当前阶段和结果。资源数量较多或包含 Registry 内容时，导出、上传和验证可能需要较长时间；请等待服务给出该步骤的完成或失败结果。

## 操作步骤
1. **确认迁移说明**。阅读并确认迁移范围、限制、需要自行完成的后续事项和失败处理方式。

2. **选择执行方式**。选择以下一种确认方式：

   <table> <thead> <tr> <td> <p><b>确认方式</b></p> </td> <td> <p><b>适用场景与确认范围</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>标准模式（逐项确认，默认）</b></p> </td> <td> <p>适合首次迁移或希望逐项查看范围和结果的场景。每个本地准备、只读查询、导出、资源类型创建和重试步骤都需要单独确认。</p> </td> </tr> <tr> <td> <p><b>危险模式（分阶段批量确认，可选）</b></p> </td> <td> <p>适合已完成迁移评审、希望减少会话确认次数的场景。执行方式确认覆盖本地依赖检查、实例列表、工作目录准备和源端资源清单；导出前仍确认一次；展示完整 DAG 后，导入前再确认一次。导入确认会连续执行多个 AC 写操作、回读和最终验证。</p> </td> </tr> </tbody> </table>

   首次迁移建议使用标准模式。两种方式下，任一创建或验证失败都会立即暂停；服务不会自动回滚、删除已创建资源或跳过失败项。
3. **确认账户信息并选择源实例**。确认主账号、CLI Profile 使用方式和源 Region。迁移服务会列出该 Region 的 AT 实例供选择。

4. **确认目标并查看源端资源清单**。确认默认或自定义的目标 Workspace 与本地工作目录。迁移服务随后以只读方式读取选定实例的资源清单，并展示各类资源的数量和名称。

5. **导出并生成迁移计划**。确认迁移期间暂停源端变更后，迁移服务读取所需资源详情、生成资源依赖关系和按类型的迁移计划。资源较多或包含 Registry 内容时，这一步可能需要较长时间。仅在确认后，完整的 Model Provider/MCP 配置才会写入本地私有导出，用于后续创建目标资源。

6. **恢复 AC 资源并生成报告**。迁移服务会先展示资源依赖图，再按依赖顺序创建资源并在每一类资源完成后验证。协作能力启用且成员资源完成后，Team 会作为最后一类资源恢复。标准模式下，每个资源类型需要单独确认；危险模式下，会在展示完整 DAG 后一次性确认全部 AC 创建、回读和最终验证。所有资源批次结束后，服务自动验证目标资源并生成脱敏的迁移验证报告和用户报告。

## 迁移验证与后续操作
根据最终报告确认 Workspace、资源类型和未完成项的迁移状态，并完成以下必要操作：

* 对 Credential 重新绑定真实 value。

* 使用 AC 生成的初始密码登录后，立即重置 Local User 密码。

* 在 AC 重新配置 IdP 和 IM Channel。

* 对 External Agent 完成接入以及运行时、模型、工具、凭据和网络绑定。

* 切换 Endpoint 调用方并完成业务验证。

  为保护敏感信息，密码、Credential value、API Key、Token、ClientSecret 和完整鉴权配置不会出现在普通清单、会话输出或最终报告中。Model Provider/MCP 的完整配置仅在确认后写入本地私有导出，迁移完成后请按组织的数据保留和安全要求处理。

## 失败处理与服务支持
当资源创建或验证失败时，迁移服务会保留已成功创建的目标资源并暂停，不会自动删除或回滚。可以选择：重试当前步骤；在了解失败资源及其下游影响后跳过该失败项，继续处理明确不受影响的资源；或中止迁移。未经明确选择，服务不会自动跳过失败项或继续后续写操作。

如果无法根据安全错误信息判断问题，或确认重试后仍然失败，请暂停迁移并请求 AgentTeams/AgentCore 服务支持。请求支持时，需提供迁移名称、源/目标资源标识、发生时间、安全错误码、RequestId、HTTP 状态和受影响资源名称；请勿提供密码、API Key、Token、ClientSecret 或私有导出文件。

迁移完成表示已批准的资源迁移步骤和目标验证已完成；不表示调用方已切换、第三方渠道已验证或业务验收已完成。