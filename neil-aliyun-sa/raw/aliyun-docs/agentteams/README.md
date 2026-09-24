# raw/aliyun-docs/agentteams — 阿里云 AgentTeams 官方文档快照（遗留文档）

🔴 **本产品已迁移至 AgentCore，以下为遗留文档，口径不得当现役事实使用。**
判定依据（RULINGS C5）：本目录 18 页中仅 `agentteams-has-been-migrated-to-agentcore` 1 页含迁移字样，其余 17 页正文零迁移提示、全部现役口吻（`billings-of-agentteams` 甚至写「当前处于公测阶段，产品本身免费」）——**legacy 属性是集合级的、页面不自证**，由权威迁移页 + 「AgentCore 侧存在对应新页」联合判定。不得因某页无迁移字样而反推其现役有效。现役口径请查 `../agentcore/`。

**归档日期**: 2026-09-20
**来源**: https://help.aliyun.com/zh/agentteams/ （18 个 URL 全部落盘为 .md 快照，其中 2 个为已归档的 TOC 容器页，见下）
**索引**: 官方 `https://help.aliyun.com/zh/llms.txt` 及按产品 llms.txt + 站内 BFS；目录层级取自各页 `window.__ICE_PAGE_PROPS__.docDetailData.storeData.breadcrumb`（AgentTeams 侧各页 breadcrumb 取自 doctree，标注处照录）

## 抓取通道说明（官方 .md Agent 通道）

help.aliyun.com 任意文档 URL 追加 `.md` 后缀即返回纯 Markdown 正文（例：`https://help.aliyun.com/zh/agentteams/manage-users.md`）。

🔴 **软 200 陷阱**：不存在的 slug 也返回 **HTTP 200** + 约 **24893 字节**的 SPA HTML 外壳，故 HTTP 状态码不能作为成功判据。本批快照的成功判据是**三重校验**：
1. `Content-Type` 含 `markdown`；
2. body 前 60 字节非 `<!doctype`；
3. 正文非纯链接清单（TOC 容器）。

补充（RULINGS C1）：字节数不能作为容器节点判据，字节阈值仅用于识别约 24893B 的软 200 HTML 外壳。本目录落盘了 2 个通过校验的 TOC 容器页（`product-overview-1.md`、`operating-guide-1.md`），仅用于 slug↔document_detail ID 对照与目录结构证据，**不作事实来源**。

`.md` 通道正文**不含页面 H1 标题**（18 页中 16 页以导语段开头，仅 2 个 TOC 容器页带 H1，SHARD-4 digest 观察 2），本 README 各页标题取自 doctree / 目录页链接文字。

## 目录树映射（一级栏目 → 子页 slug.md → 官方标题 ｜ 逐页标注 migration_status）

migration_status 分布（frontmatter 实测）：**migrated-legacy 17 页 ／ unknown 1 页（`view-dashboards-and-monitoring-1`）／ current 0 页**。

### 产品简介（`product-overview-1.md` 已归档 ｜ migrated-legacy ｜ 纯链接目录页：175B、仅 2 条 document_detail 链接，承载「AgentTeams 产品概述=3040377、费用说明=3045332」的 slug↔ID 对照证据，**不作事实来源**）
- `magic-console-product-overview.md` — AgentTeams 产品概述 ｜ migrated-legacy
- `billings-of-agentteams.md` — AgentTeams 费用说明 ｜ migrated-legacy（🔴 RULINGS G6 最高危：自称「当前处于公测阶段，产品本身免费」但无日期/有效期/任何单价；迁移后计费归属无处可查；页面自身 8/9/7 三数并存口径不一致。不得据此推断 AgentCore 免费）

### 快速入门（doctree；容器节点 `quick-start-1` 未归档）
- `magic-quick-start.md` — 快速入门（7 步流程：创建服务关联角色→创建实例→配置模型→创建用户→创建 Worker 团队→创建 Worker→验证）｜ migrated-legacy
- `agentteams-has-been-migrated-to-agentcore.md` — AgentTeams 迁移至 AgentCore ｜ migrated-legacy（⚠️ 例外注记：本页是**现行有效的权威迁移操作指南**，不是过时内容——迁移工具包文件名日期 20260831，距归档日约 3 周。迁移生效时间/是否强制/截止时间均为缺口，🔴 不得把工具包文件名日期当迁移生效日期（RULINGS §3.7）。AgentCore 侧「动态与公告」栏目另有同 slug 独立快照）

### 操作指南（`operating-guide-1.md` 已归档 ｜ migrated-legacy ｜ 纯链接目录页：879B、11 条 document_detail 链接，是本片 slug↔ID 对照的唯一权威来源，**不作事实来源**）
- `configure-dingtalk-account-integration.md` — 配置钉钉账号集成 ｜ migrated-legacy（AT 侧此 slug 正文确为钉钉；🔴 AgentCore 侧同 slug 页正文却是飞书，见下方 slug 陷阱）
- `local-worker-user-guide.md` — 本地 Worker 使用指南 ｜ migrated-legacy（页内「如已迁移机器」指 Worker 换机器，非产品迁移）
- `management-models-and-suppliers-1.md` — 管理模型与供应商 ｜ migrated-legacy
- `management-skill.md` — 管理 Skill ｜ migrated-legacy（页内「下线版本/已下线」指 Skill 版本生命周期，非产品下线，不得据此判 legacy）
- `managing-the-mcp-server.md` — 管理 MCP Server ｜ migrated-legacy
- `manage-worker-templates-1.md` — 管理 Worker 模板 ｜ migrated-legacy
- `manage-users.md` — 管理用户 ｜ migrated-legacy（doctree 标题为「管理团队与成员」，与正文主题「管理用户」不一致，SHARD-4 观察 7）
- `manage-workers-and-worker-teams.md` — 管理 Worker 和 Worker 团队 ｜ migrated-legacy
- `view-dashboards-and-monitoring-1.md` — 查看仪表盘与监控 ｜ **unknown**（页面无任何时效线索；AgentCore 侧最接近的 `view-overview` 是否为其对应新页，页面与 doctree 均未说明，按契约 §3 判 unknown）

### 安全合规（容器节点 `security-compliance`、`use-ram-for-access-control` 未归档）
- 使用RAM进行访问控制：
  - `service-linked-role-1.md` — AgentTeams 服务关联角色（角色名 `AliyunServiceRoleForMagic`，服务名 `magic.aliyuncs.com`）｜ migrated-legacy
  - `manage-instances-1.md` — 管理实例 ｜ migrated-legacy（🔴 层级归属存疑：doctree breadcrumb 把本页挂在「安全合规 > 使用RAM进行访问控制」下，但正文是实例全生命周期管理，与该栏目不符；`operating-guide-1` 目录页则把本页列在「操作指南」下。疑似官方文档树挂载错误，照录不调和，SHARD-4 观察 6）
- `agentteams-dingtalk-channel-configuration-guide.md` — AgentTeams 钉钉渠道配置指南 ｜ migrated-legacy（🔴 层级归属存疑：doctree breadcrumb 标注「安全合规 > security-compliance」，与页面内容主题（IM 渠道接入）不符；`operating-guide-1` 目录页把本页列在「操作指南」下。SHARD-4 观察 6）

## TOC 容器节点处置清单

- **已落盘的容器页（2 个）**：`product-overview-1.md`（175B，未过 400B 字节阈值判 FAIL-TOOSMALL，但为保留 slug↔document_detail ID 对照证据仍逐字落盘，SHARD-4 观察 4）与 `operating-guide-1.md`（879B）。二者均为**纯链接目录页，不作事实来源**。
- **未归档的容器节点（4 个，不在本片指派清单内）**：`agentteams/security-compliance`、`agentteams/quick-start-1`、`agentteams/news-and-announcements`、`agentteams/use-ram-for-access-control`（SHARD-4 观察 5）。
- 对照：AgentCore 侧有 5 个容器节点未落盘（product-overview 303B / magic-quick-start 363B / security-compliance 232B / agent-management 301B / im-configuration 323B），见 `../agentcore/README.md`。

## 已知快照瑕疵（RULINGS §3.5 G9 —— 逐字保留未修，raw 层不可变）

- `.md` 通道把代码块语言标记替换为渲染残留 `HELPCODEESCAPE-bash` / `HELPCODEESCAPE-json` / `HELPCODEESCAPE-plaintext`（本片 `agentteams-has-been-migrated-to-agentcore.md`、`local-worker-user-guide.md` 等页内可见）；
- 官方原文错字逐字保留：AgentCore 侧计费开通页（`../agentcore/agentcore-billing-activation.md`）的「**用户eam**」；本片自身的原文错别字「Woker」（manage-workers-and-worker-teams）、「单机删除」（manage-users）、「NPX」（management-skill，疑为 npx）。

以上均为官方 `.md` 通道产物或官方原文错字，**不是抓取损坏**；蒸馏/引用时可按语义还原，但不得改写 raw。

## 🔴 slug 命名陷阱警示（RULINGS §3.1 —— 严禁按 slug 猜内容）

**跨目录同名陷阱（本片最相关）**：`configure-dingtalk-account-integration` 在 AgentTeams 侧正文是**真钉钉集成**，而在 AgentCore 侧同 slug 页正文是**飞书集成**（官方 slug 命名错误）——同名 slug 跨产品语义不同，引用时必须带目录前缀。

RULINGS §3.1 / 任务基线全量清单（文件均在 `../agentcore/`）：

| slug | 字面暗示 | 正文实际 |
|---|---|---|
| `configure-dingtalk-account-integration`（AgentCore 侧） | 钉钉账号集成 | **飞书集成**。首句逐字：「AgentCore 支持企业成员使用飞书扫码登录，并可自动同步飞书通讯录中的用户信息。」 |
| `agentcore-configure-dingtalk-account-integration` | 钉钉账号集成 | 此页才是 AgentCore 侧**真钉钉集成**。两页是钉钉/飞书并行页，**非新旧重复，不得合并去重** |
| `guidelines-for-the-use-of-local-nanoagent` | 本地 NanoAgent | 正文 **0 次**出现「NanoAgent」；官方术语是「**本地纳管 Agent**」。NanoAgent 只存在于 slug |
| `acentcore-collaboration-control-face-exemption-description` | — | slug 官方拼错（**缺 g**），原样保留——改名会切断与官方 URL 的对应 |
| `magic-quick-start-1`（AgentCore 侧） | 快速入门 | 正文是「**SDK 参考**」4 链接目录索引页，非快速入门。对照：本片 `magic-quick-start.md`（无 -1）才是真的快速入门正文 |

另注（SHARD-4 表外补充，doctree 层面观察、非页面事实）：`agentteams-has-been-migrated-to-agentcore`、`magic-quick-start`、`managing-the-mcp-server`、`manage-users`、`service-linked-role-1` 等 slug 在 AT/AC 两侧同名并存，两侧快照相互独立，内容不保证一致。

## SHA256 清单

见同目录 `SHA256SUMS.txt`（由 `SHA256SUMS.partial-SHARD-4.txt` 合并，18 行数据，partial 已删除）。
🔴 SHA256 只对**原始正文**计算（不含 7 字段 frontmatter），`shasum -a 256 -c SHA256SUMS.txt` 会对全部文件报 FAILED —— **设计使然，非快照损坏**（RULINGS C7）。正确校验方法：`tail -n +11 <file>.md | shasum -a 256`，详见 SHA256SUMS.txt 头部注释。
（与既有 meoo/ 先例的差异：meoo 快照无 frontmatter，故其 SHA256SUMS.txt 可直接 `-c` 验过。）
