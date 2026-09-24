# raw/aliyun-docs/agentcore — 阿里云 AgentCore（智能体构建和治理平台）官方文档快照

**归档日期**: 2026-09-20
**来源**: https://help.aliyun.com/zh/agentcore/ （指派 37 个 URL：32 个 .md 快照落盘 + 5 个 TOC 容器节点未落盘，见下方清单；另有 RULINGS §4 T1 单独指派的 SLA 协议全文快照 `sla-agreement-fulltext-terms-alicdn.md` 于归档收口前落盘，本目录 .md 快照合计 33 个）
**索引**: 官方 `https://help.aliyun.com/zh/llms.txt` 及按产品 llms.txt + 站内 BFS；目录层级取自各页 `window.__ICE_PAGE_PROPS__.docDetailData.storeData.breadcrumb`（breadcrumb 缺失处标「(推断)」，未洗成确定）

## 抓取通道说明（官方 .md Agent 通道）

help.aliyun.com 任意文档 URL 追加 `.md` 后缀即返回纯 Markdown 正文（例：`https://help.aliyun.com/zh/agentcore/manage-agents.md`）。

🔴 **软 200 陷阱**：不存在的 slug 也返回 **HTTP 200** + 约 **24893 字节**的 SPA HTML 外壳，故 HTTP 状态码不能作为成功判据。本批快照的成功判据是**三重校验**：
1. `Content-Type` 含 `markdown`；
2. body 前 60 字节非 `<!doctype`；
3. 正文非纯链接清单（TOC 容器）。

补充（RULINGS C1）：字节数不能作为容器节点判据，字节阈值仅用于识别约 24893B 的软 200 HTML 外壳。通过校验的 TOC 容器页（本目录的 `operating-guide.md`、`magic-quick-start-1.md`）已落盘，但**不作事实来源**，仅提供目录结构与 slug 对照证据。

`.md` 通道正文**不含页面 H1 标题**（SHARD-2/SHARD-4 digest 实测观察），本 README 各页标题取自父级目录页链接文字或 doctree。

## 目录树映射（一级栏目 → 子页 slug.md → 官方标题）

除单独标注外，各页 frontmatter 的 migration_status 均为 `current`。

### 产品简介（容器节点 `product-overview`，未归档）
- `agentcore-product-overview.md` — AgentCore 产品概述
- `agentcore-basic-concepts.md` — AgentCore 基本概念
- `agentcore-billing-instructions.md` — AgentCore 计费说明

### 动态与公告（容器节点 `magic-quick-start`，未归档；其 slug 字面为「快速入门」但 H1 是「动态与公告」，`magic` 系内部代号）
- `acentcore-collaboration-control-face-exemption-description.md` — AgentCore协作管控面限免说明（🔴 slug 官方拼错，缺 g，原样保留；强时效公告：活动期 2026-09-18 00:00:00 至 2026-10-18 23:59:59 GMT+8）
- `agentcore-billing-activation.md` — AgentCore 计费开通说明（自 2026-09-18 00:00:00 GMT+8 起开启计费）
- `agentteams-has-been-migrated-to-agentcore.md` — AgentTeams 迁移至 AgentCore ｜ migration_status: **migrated-legacy**（权威迁移页；agentteams/ 目录另有同 slug 独立快照）

### 安全合规（容器节点 `security-compliance`，未归档）
- 使用RAM进行访问控制（容器节点 `use-ram-for-access-control`，未归档）：
  - `service-linked-role-1.md` — 服务关联角色（推断；`security-compliance` TOC 未直接列出本页，推断挂于「使用RAM进行访问控制」之下）
- `agentcore-intelligent-agent-development-and-governance-platform-service-level-agreement.md` — 智能体构建和治理平台 AgentCore 服务等级协议（仅 611 字节：只有「2026-09-18 生效」与 terms.alicdn.com 协议全文入口，可用率百分比/赔偿口径/例外条款均在外部协议原文页，见 RULINGS §3.4）
  - `sla-agreement-fulltext-terms-alicdn.md` — 智能体构建和治理平台 AgentCore 服务等级协议·**协议全文**（RULINGS §4 T1 补抓；source_url 为 terms.alicdn.com 外部协议原文页 `legal-agreement/terms/b_end_product_protocol/20260907141143820/20260907141143820.html`，非 help.aliyun.com `.md` 通道；body_bytes 4476，migration_status: current。该文件落盘晚于 3 个 partial 生成，故**不在**本目录 SHA256SUMS.txt 内，其校验值记录于自身 frontmatter 的 body_sha256）

### 操作指南（`operating-guide.md` 已归档 ｜ migration_status: **unknown** ｜ 纯链接目录页，不作事实来源）
- `view-overview.md` — 查看概览
- `manage-workspace.md` — 管理 Workspace
- `manage-connectors.md` — 管理连接器
- Agent 管理（容器节点 `agent-management`，未归档）：
  - `manage-agents.md` — 管理 Agent
  - `high-code-agent-deployment-guide.md` — 高代码 Agent 部署与使用指南
  - `guidelines-for-the-use-of-local-nanoagent.md` — 本地纳管 Agent 使用指南（🔴 官方术语是「本地纳管 Agent」，正文零次出现「NanoAgent」，见下方 slug 陷阱）
- `manage-agent-templates.md` — 管理 Agent 模板
- `manage-memory-space.md` — 管理和使用记忆空间
- `model-management.md` — 管理模型
- `manage-skill.md` — 管理 Skill
- `managing-the-mcp-server.md` — 管理 MCP 工具
- `manage-credentials.md` — 管理凭证
- `set-up-team-collaboration.md` — 建立团队协同 (推断) ｜ breadcrumb: 操作指南 > Team 协作 (推断)
- `use-team-web-to-set-tasks.md` — 使用 Team Web 设置任务 (推断) ｜ breadcrumb: 操作指南 > Team 协作 (推断)
- `manage-users.md` — 用户管理 (推断)
- IM配置（容器节点 `im-configuration`，未归档；其 323B 目录正文提供了以下三页的官方标题）：
  - `integrate-the-agent-into-the-im-channel.md` — 将 Agent 接入 IM 渠道（由 im-configuration 容器页归属推断）
  - `agentcore-configure-dingtalk-account-integration.md` — 配置钉钉账号集成（由 im-configuration 容器页归属推断；此页才是真钉钉集成）
  - `configure-dingtalk-account-integration.md` — 配置飞书账号集成（由 im-configuration 容器页归属推断；🔴 slug 含 dingtalk 但正文是飞书，见下方 slug 陷阱）

### 开发参考 > SDK 参考 (推断)（`magic-quick-start-1.md` 已归档 ｜ 纯链接目录页（H1「SDK 参考」+ 4 条链接），不作事实来源）
- `agentcore-sdk-overview.md` — AgentCore SDK 概述（由 magic-quick-start-1 容器页归属推断）
- `agentcore-python-sdk-user-guide.md` — AgentCore Python SDK 使用指南 (推断)
- `agentcore-node-js-sdk-user-guide.md` — AgentCore Node.js SDK 使用指南 (推断)
- `create-a-high-code-agent-using-the-python-sdk.md` — 使用 Python SDK 快速创建高代码 Agent (推断)

## 未归档的 TOC 容器节点清单（无正文价值，未落盘；TOC 结构已保留在 /tmp/agentcore-work/digests/）

| 容器节点 | 正文字节数 | 内容 |
|---|---|---|
| `agentcore/product-overview` | 303B | H1「产品简介」+ 3 条子页链接 |
| `agentcore/magic-quick-start` | 363B | H1「动态与公告」+ 3 条子页链接 |
| `agentcore/security-compliance` | 232B | H1「安全合规」+ 2 条子页链接 |
| `agentcore/agent-management` | 301B | H1「Agent 管理」+ 3 条子页链接 |
| `agentcore/im-configuration` | 323B | IM配置目录 + 3 条子页链接 |

对照：AgentTeams 侧的 `product-overview-1`（175B）与 `operating-guide-1`（879B）两个容器页**已落盘**（承载 slug↔document_detail ID 对照证据），见 `../agentteams/README.md`；它们同为纯链接目录页，不作事实来源。

## 已知快照瑕疵（RULINGS §3.5 G9 —— 逐字保留未修，raw 层不可变）

- `.md` 通道把代码块语言标记替换为渲染残留 `HELPCODEESCAPE-bash` / `HELPCODEESCAPE-json` / `HELPCODEESCAPE-plaintext`；
- `agentcore-billing-activation.md`（计费开通页）含官方原文错字「**用户eam**」（疑为「用户 Team」缺字，SHARD-1 digest 注记）。

以上均为官方 `.md` 通道产物或官方原文错字，**不是抓取损坏**；蒸馏/引用时可按语义还原，但不得改写 raw。

## 🔴 slug 命名陷阱警示（RULINGS §3.1 —— 严禁按 slug 猜内容）

| slug | 字面暗示 | 正文实际 |
|---|---|---|
| `configure-dingtalk-account-integration` | 钉钉账号集成 | **飞书集成**（官方 slug 命名错误）。首句逐字：「AgentCore 支持企业成员使用飞书扫码登录，并可自动同步飞书通讯录中的用户信息。」 |
| `agentcore-configure-dingtalk-account-integration` | 钉钉账号集成 | 此页才是**真钉钉集成**。两页是钉钉/飞书并行页，**非新旧重复，不得合并去重** |
| `guidelines-for-the-use-of-local-nanoagent` | 本地 NanoAgent | 正文 **0 次**出现「NanoAgent」（剥离 frontmatter 后 grep -ci = 0）；官方术语是「**本地纳管 Agent**」（「本地纳管」命中 4 次）。NanoAgent 只存在于 slug |
| `acentcore-collaboration-control-face-exemption-description` | — | slug 官方拼错（**缺 g**，acentcore ≠ agentcore），原样保留——改名会切断与官方 URL 的对应（RULINGS 假阳性清单 #3） |
| `magic-quick-start-1` | 快速入门 | 正文是「**SDK 参考**」4 链接目录索引页（H1「SDK 参考」，442B），非快速入门 |

关联红线（RULINGS §3.5 G8）：钉钉/飞书账号集成各有硬上限「最多支持 30 个用户，超出后账号集成将失败」。

## SHA256 清单

见同目录 `SHA256SUMS.txt`（由 `SHA256SUMS.partial-SHARD-{1,2,3}.txt` 合并，32 行数据，partial 已删除；后补落盘的 `sla-agreement-fulltext-terms-alicdn.md` 不在 3 个 partial 覆盖范围内，未列入，其校验值见该文件 frontmatter 的 body_sha256）。
🔴 SHA256 只对**原始正文**计算（不含 7 字段 frontmatter），`shasum -a 256 -c SHA256SUMS.txt` 会对全部文件报 FAILED —— **设计使然，非快照损坏**（RULINGS C7）。正确校验方法：`tail -n +11 <file>.md | shasum -a 256`，详见 SHA256SUMS.txt 头部注释。
（与既有 meoo/ 先例的差异：meoo 快照无 frontmatter，故其 SHA256SUMS.txt 可直接 `-c` 验过。）
