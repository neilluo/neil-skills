# AI 网关蒸馏 · 主控裁决留痕（RULINGS）

生成：2026-09-21 ｜ 主控：Qoder agent ｜ 上游工艺先例：`tests/agentcore-distill-rulings-2026-09-21.md`

> 本文件记录**主控做出的所有范围/口径/归属裁决**，以及**驳回的 worker 结论**。
> 蒸馏 worker 只报事实与矛盾，不裁决；裁决集中在这里，便于后续复核与翻案。

---

## R1 范围裁决

| 项 | 裁决 | 依据 |
|---|---|---|
| 产品归属 | AI 网关是 **API 网关产品族下三个平级子产品之一**（云原生API网关 / AI 网关 / 原API网关），非独立 productCode 文档根 | 父级 `https://help.aliyun.com/zh/api-gateway/llms.txt`「## 子产品」并列三条，各自拥有独立 llms.txt |
| 本次范围 | **仅 AI 网关子树**。云原生API网关、原API网关不纳入 | curator 指令给的是 `ai-gateway/product-overview/what-is-an-ai-gateway` |
| 原API网关 | 不纳入，且**不宜纳入**：已公告 2026-08-23 停止新购、2027-09-21 全面下线 | 父级 llms.txt 子产品描述 |
| 开发参考 250 页 | 登记 `[deferred]`，不蒸馏 | 逐 Action / 逐数据结构 OpenAPI 参考页；沿 AgentCore 侧 AgentRun 317 页先例 |
| 开发参考 8 个元页 | **破例纳入核心** | 概览 / 服务接入点 / RAM 授权信息 / 流控配额 / 公共错误码 / 变更集 / API参考容器 / 开发参考容器 —— 对 SA 做自动化与最小权限设计有直接价值，且不是逐 Action 页 |
| SLA 协议全文 | **补抓外部源** terms.alicdn.com | help 侧 `support/service-level-agreement` 只有 196B 入口桩；沿 AgentCore 侧 RULINGS §4 T1 先例 |

**最终范围**：llms.txt 438 链接 → core **189** 页（含 8 元页 + 1 内链发现页）+ 外部 SLA 全文 1 页；deferred **250** 页。

---

## R2 🔴 归属判据修正：llms.txt 收录 ≠ URL 前缀（主控自审发现）

首版分类器按 `url.startswith(".../ai-gateway/")` 判归属，把 **3 页确实属于 AI 网关文档集、但挂在父级
`/zh/api-gateway/` 路径下**的页面误判为 external 踢出范围：

| slug | 官方标题 | 为什么漏掉是硬伤 |
|---|---|---|
| `ai-gateway-commercialization-announcement` | AI 网关 Serverless 新版商业化公告（2026年9月起计费） | 🔴 **本次蒸馏时点（2026-09-21）的现行计费权威源**：公测 2026-08-31 结束、2026-09-01 起商业化计费。漏掉＝整章计费口径停留在公测期 |
| `consumer-quotas-management` | AI网关-管理消费者配额 | FinOps 配额是 AI 网关区别于云原生API网关的差异化能力 |
| `request-response-capture-1` | API网关请求/响应采集（Body最大5KB/日志字段与版本要求） | Body 采集 5KB 上限是可观测章的硬限制 |

**裁决**：归属判据改为 **llms.txt 收录关系**，不看 URL 视觉层级。
与既有记忆 [[aliyun-help-center-md-channel]]「产品归属别从首页导航推断，要看 productCode 与 llms.txt」同源 —— 本次把该原则从「产品间归属」推广到「产品内路径层级归属」。
修正后 core 由 185 → 188（+3），已在 `scripts/build-doc-inventory.py` 的 `classify()` docstring 留痕。

---

## R3 落地形态裁决：7 个扁平文件，不建子目录

| 候选 | 裁决 |
|---|---|
| 单文件 `knowledge/aliyun-ai-gateway.md` | ❌ 7 路 partial 合计 **8944 行**，远超 AGENTS.md 的 2500 行拆分阈值 |
| 建 `knowledge/ai-gateway/` 子目录 | ❌ 既有 `knowledge/` 是**扁平**结构（`aliyun-agentcore.md` / `aliyun-lingjun-bms.md` / `geospatial-products.md` …），建子目录破坏同形性 |
| **扁平 + 后缀命名 7 文件** | ✅ 采纳。AGENTS.md 自己给的拆分示例就是 `aliyun-products-compute.md` / `aliyun-products-database.md` 这种同形后缀命名 |

落地清单（装配后实测行数，每个文件均 < 2500 行阈值；合计 **9471** 行 / **411** 张表）：

| 文件 | 章节 | 行数 |
|---|---|---|
| `knowledge/aliyun-ai-gateway.md` | §0 溯源与范围 · §1 定位与产品族 · §2 形态与容量 · §14 实战避坑 · §15 SA 速查卡 · 子页导航 | **1413** |
| `knowledge/aliyun-ai-gateway-billing.md` | §3 计费与商务（含 §3.9 SLA 与赔偿） | **963** |
| `knowledge/aliyun-ai-gateway-traffic.md` | §4 核心对象模型 · §5 流量治理与成本控制 | **1347** |
| `knowledge/aliyun-ai-gateway-auth.md` | §6 鉴权与消费者体系 · §7 AI 安全护栏与 RAM 权限 | **1247** |
| `knowledge/aliyun-ai-gateway-mcp-agent.md` | §8 MCP 与 Agent API 生态 | **1411** |
| `knowledge/aliyun-ai-gateway-plugins.md` | §9 插件体系 | **1541** |
| `knowledge/aliyun-ai-gateway-ops.md` | §10 可观测与运维 · §11 开发者门户与开放平台 · §12 实践教程与集成配方 · §13 OpenAPI 与 RAM 元信息 | **1549** |

标注分布（主控 `grep` 实测）：`[官方｜slug]` 290 ｜ `[官方原文]` 49 ｜ `[官方矛盾]` 99 ｜ `[文档未说明]` 550 ｜ `[推断]` 201 ｜ `[原文如此]` 49。
7 路 partial 原始产出 8944 行 → 装配后 9471 行（差额 = 7 个统一页眉 + 主控的 §0/§14/§15 与 W1 正文合并）。
装配器：`scripts/assemble-ai-gateway-pages.py`（只做页眉归一与拼接，**不改 partial 正文一字** —— 避免装配环节引入新失真）。

**`aliyun-products.md` 不加正文**（该文件已 2667 行、超阈值），仅加一张 ≤15 行指针卡 —— 沿 2026-09-20 AgentCore 先例。

---

## R4 口径优先级规则（矛盾裁决的通用依据）

**默认不裁决**：官方文档自相矛盾时保留 `[官方矛盾]` 标签 + 双方原文，这是本 KB 的既有约定
（`aliyun-agentcore.md` 有 17 处 `[官方矛盾]`）。**只有当矛盾会影响对客答复时**才按下表裁决，
且裁决必须在正文注明「主控裁决 + 依据」。

| 优先级 | 来源类型 | 理由 |
|---|---|---|
| 1（最高） | **法律协议原文**（terms.alicdn.com 的 SLA/服务条款） | 有法律效力，赔偿争议只看这个 |
| 2 | **带日期的公告 / 发布记录 / 变更集** | 时效性可判定，越新越权威 |
| 3 | **专页**（如 `debug-mcp-services`） | 比聚合页（如 `mcp-service-management`）更新更细；实测聚合页内容偏旧 |
| 4 | **正文表格** | 表格是结构化事实；同页散文常是未同步更新的旧文案 |
| 5（最低） | 产品概述页的能力宣称、导航页描述 | 营销口径，常无实例类型/地域限定 |

🔴 **禁止用「静态参考页越像权威越可能过期」的直觉反向裁决**：
本次实测 `product-comparison` 宣称「SLA 99.99%」无限定，而 SLA 协议原文按实例类型分档 ——
按 R4 第 1 条，**协议原文胜出**，产品页宣称降级为「营销口径，不得用于赔偿主张」。

---

## R5 已裁决的具体矛盾（仅列影响对客答复的）

| # | 矛盾 | 裁决 | 依据 | 上报方 |
|---|---|---|---|---|
| C1 | SLA 可用率：`product-comparison` 称「99.99%」无限定 ↔ SLA 协议原文按实例类型分档（普通实例 / serverless 实例两档） | **以 SLA 协议原文为准**，且必须**带实例类型限定**引用。产品页的 99.99% 标为营销口径 | R4-1 | W1 / W2 |
| C2 | 🔴 **SLA 承诺值与产品页宣称值之间存在「无赔偿区」**：SLA 只承诺 serverless 实例 ≥99.90%、首档赔偿要求「低于 99.90%」，但产品页宣称企业版/旧版 Serverless 为 99.95% | **按 SLA 协议执行**：可用性落在 [99.90%, 99.95%) 区间时**无赔偿**。🔴 对客不得用产品页的 99.95% 承诺赔偿 | R4-1；这是本次蒸馏**最高商务风险发现** | W2 |
| C3 | 公网入网流量计费主体：公测公告「按 CDT 计费」↔ 新版计费说明「由网关侧计费」 | **两页互不引用、均未说明切换** → 保留 `[官方矛盾]`，对客口径：**以商业化后的账单实际出账方为准，报价前必须走购买页/工单确认** | R4-2 无法判定谁更新（公测公告带日期但已被商业化公告取代；新版计费说明自身 slug 与正文口径打架，见 C4） | W2 |
| C4 | `overview-of-billing-during-the-serverless-public-preview-of-the`：slug 与标题写「**公测**计费说明」，正文却写「本文适用于…**商业化后**的计费说明」 | **该页 6 项单价的口径归属无法从本页判定** → 全章引用该页数字时**必须标注此不确定性**，不得当作确定的商业化单价 | 同页自相矛盾，R4 无从适用 | W2 |
| C5 | 智能路由的请求侧模型：`managing-the-model-api` 用 IntentCode 意图分类（Coder/Math/Translation/Flash/Complex）↔ `configure-smart-routing` 要求显式 `auto/<balanced\|cheap\|quality\|fast>` 且明说「不是固定模型名称或强制规则」 | **两套口径并存，均不废弃** → 保留 `[官方矛盾]`。对客答复：**以配置页 `configure-smart-routing` 的 `auto/*` 为准做配置**（专页优先，R4-3），IntentCode 表按「文档未说明其与 auto/* 的映射关系」处理 | R4-3 | W3 |
| C6 | 插件 slug ↔ 插件名交叉错位：`ai-cue-template`（标题「AI 提示词插件」）正文实为 ai-prompt-decorator；`ai-cue-decorator`（标题「AI 提示词模板插件」）正文实为 ai-prompt-template | **以正文能力+参数结构+优先级为准**（R4-4），即 W6 判定的「两者互换」成立；🔴 **对客给配置示例时必须写插件名而非 slug**，并注明官方标题与 slug 存在交叉错位 | R4-4；第三方交叉验证：`geographic-location-of-ip` 页把 prepend/append 明确称为「AI提示词装饰器插件」 | W6 |
| C7 | `frontend-gray` 插件优先级：页内「认证阶段 1000」↔ 插件总表「认证阶段 450」 | **不裁决**（两个数字会导致完全不同的执行顺序，且都可能对）→ 保留 `[官方矛盾]`，并标注**这是必须先实测再对客承诺的项**（1000 排在 http-real-ip(980) 之前、450 排在其之后，直接决定前端灰度能否拿到真实客户端 IP） | 无更高优先级来源 | W6 |
| C8 | 管理员全权限策略名：`AliyunAPIGFullAccess` ↔ `AliyunNativeApiGwFullAccess` | **不裁决**，但🔴 对客给授权指引时**两个名字都要给**并说明「文档存在两个策略名，授权失败时换另一个试」—— 这条直接影响能否授权成功 | 无更高优先级来源 | W4 |
| C9 | MCP 是否支持 JWT 消费者认证 | 🔴 **已修订（2026-09-21，R2a 复裁推翻原判）**。**原判**：以专页 `consumer-certification`「目前仅支持 API Key」为对客口径（依据 R4-3 专页优先），不得承诺 JWT。**推翻理由**：原判**漏比了一条优先级更高的证据** —— `new-feature-release-notes-ai-gateway` 的 **2026-01 变更表**明文「**MCP Server 支持 JWT 认证。**」（主控已回源 `grep` 实证，同页另有一条更早的「MCP Server 支持 MCP 工具级别消费者认证」）。按本文件 R4 自己的优先级表，**带日期的发布记录 = 优先级 2 > 静态专页 = 优先级 3**，且与既有教训「越像权威的静态页过期越无破绽」一致。**修订后裁决**：倾向「支持 JWT」，但两页 `migration_status` 同为 `current`、专页未标废弃 → 🔴 **对客不得仅凭任一侧文档承诺，必须先在客户实例上实测确认**。**已 sweep 的消费面（9 处）**：`-auth` 页眉对客纪律 / `-auth` §6.4 设计行为限制表 / `-auth` §6.4 矛盾框标题与新增高优先级一方原文 / 主页 §1.3 能力总表（🔴 原为 P0：把被否掉的一方写成无条件确定事实）/ 主页 §2.12 时间线 2026-01 行 / 主页 §15.7 鉴权四条路表 / `-mcp-agent` §8.1 限制表 / `aliyun-products.md` 指针卡 / `index.md` 交叉引用行 / 本 changelog「对客必背」摘要 | R4-2 > R4-3 | W4 报出矛盾、R2a 复裁发现漏证 |
| C10 | 「已开认证但未授权」返回 401 还是 403（同页散文说 401，同页两张错误码表说 403） | **以错误码表为准**（R4-4）→ 对客口径 **403**；散文的 401 标注为文档瑕疵 | R4-4 | W4 |
| C11 | Nacos 版本要求：「MSE Nacos**企业版** 3.0 及以上」↔「MSE Nacos**铂金版** 3.0 及以上」 | **不裁决** → 对客口径：**按更高要求（铂金版）预检**，两版都试；保留矛盾标注 | 两页 migration_status 均为 current，无从判定新旧 | W5 |
| C12 | TLS 1.3 下自定义加密套件是否生效：`setting-the-specified-https-cipher-suite` 称 14 条套件全部支持 TLS 1.3 ↔ `create-a-domain-name` 称「协商结果为 TLS1.3 时不生效」 | **不裁决**，但🔴 对客口径按**更保守的一方**（TLS 1.3 下自定义套件可能不生效）设计，并建议客户实测协商结果 | 无更高优先级来源；这是安全配置，保守优先 | W1 |

**未裁决的矛盾**（约 40 条）全部保留在各专题页的 `[官方矛盾]` 标注中，双方原文并列，交后续 Lint 或产研确认。

---

## R6 🔴 抓取通道的五种失效模式（工艺沉淀，可复用到任何 help.aliyun.com 产品）

前四种来自 2026-09-20 AgentCore 蒸馏 + 本次修正，**第五种是本次新发现**：

| # | 失效模式 | 表现 | 判据 | 处置 |
|---|---|---|---|---|
| 1 | **软 200** | 不存在的 slug 返回 HTTP 200 + 约 **24893B** SPA HTML 外壳 | body 前 60 字节以 `<!doctype`/`<html` 开头 | 不落盘，记 `FAIL-SOFT200` |
| 2 | **CT 不符** | 返回非 markdown Content-Type | `Content-Type` 不含 `markdown` | 不落盘，记 `FAIL-CT` |
| 3 | **空 body** | 0 字节 | `len(body)==0` | 不落盘，记 `FAIL-EMPTY` |
| 4 | 🔴 **Document Not Found 桩**（本次新发现） | CT=markdown、HTTP 200 **或 404**（同一 slug 两次抓取状态码不同！）、body 恒为 **86B** 固定文案 `# Document Not Found / The requested document does not have Markdown content available.` | 正则匹配该固定文案 | 不落盘，记 `FAIL-NOMD`。**首版抓取器把它判成 OK 落盘了 4 页垃圾**，因为它同时通过前三种校验且「有标题+散文」故也不是 TOC |
| 5 | 🔴 **服务端静默截断**（本次新发现） | HTTP 200、CT=markdown、**Content-Length 与 body 自洽**、**两次抓取 SHA256 完全一致** → 截断发生在服务端而非抓取器。实测 `agent-api-observable`：978B，正文在列表第 3 项处断在一个孤立 `*` 上 | 末行是悬挂结构标记（孤立 `*`/`-`/`+`）、HTML 标签开闭不平衡、末行以未完结词尾结束 | **不能自动修复**，只能在知识页标注「该页官方 `.md` 通道返回截断正文，指标清单不完整」；全量扫描 186 快照仅 **1 页**命中 |

**TOC 容器判据（沿 AgentCore RULINGS C1，本次再次验证）**：
判据 = 「正文仅由标题 + 链接列表构成、无散文」，**不是字节阈值**。
本次实测 `product-overview` 765B 判 TOC、`support` 113B 判 TOC、而 86B 的 Document Not Found 桩**有散文**故不是 TOC —— 三者字节数相近而性质完全不同，字节阈值必然误判。
本次 189 页中判出 **37 个 TOC 容器**，落盘但不作事实来源（承载目录结构与 slug↔docId 对照证据）。

**负控实验（门禁不能只看全绿）**：抓取器上线前用**伪造 slug** 跑负控 —— `this-slug-does-not-exist-xyz` 被正确判为 `FAIL-SOFT200`（24893B，与既有记忆完全一致），证明检测器真的会 FAIL，而不是恒返回 OK。

---

## R7 🔴 驳回的 worker 结论（主控独立复核后不采纳）

| # | worker 结论 | 主控复核 | 裁决 |
|---|---|---|---|
| B1 | W7：「`observation-analysis` 是**孤儿页**，存在于 raw 但不在任何 shard TSV，构成覆盖缺口，建议补派」 | `observation-analysis` 在 manifest 里 verdict = **TOC**（382B，正文只有 3 条链接：查看网关监控数据 / 开启网关日志投递 / 开启网关链路追踪 —— 主控已 `cat` 全文确认） | ❌ **驳回**。TOC 容器按契约红线 7 本就不作事实来源、不指派。**不是覆盖缺口**。W7 未读取该页的行为完全正确，只是把它误判成了遗漏 |
| B2 | W4：「raw 里的 `authentication`(629B)、`consumer-management`(452B)、`global-authentication`(504B) 未出现在任何 W*.tsv，可能是覆盖缺口」 | 三者在 manifest 里 verdict 均为 **TOC** | ❌ **驳回**，同 B1 |
| B3 | 完备性门禁的独立证据 | `scripts/assign-distill-shards.py` 用集合运算证明：**149 个有正文快照 = 149 条指派**，无遗漏、无重复、无幽灵 slug（TOC 37 + FAIL-NOMD 4 不参与指派） | ✅ 覆盖面无缺口，B1/B2 的前提不成立 |

> **为什么必须留痕**：worker 的「发现」若被主控直接采信写进知识页，就会把一个不存在的覆盖缺口
> 固化成 KB 里的「已知问题」，后续 Lint 会反复追这条假账。这与既有教训
> [[main-control-premise-poisons-fanout]]（主控的错误前提会被 worker 洗成「已确认的发现」回传）
> 是**同一失效的两个方向** —— 本次是 worker 的错误前提差点被主控洗成结论。

**主控自己的错误前提（worker 正确抵制，记此自省）**：
主控在 W7 提示词里断言 `access-vertex-ai-through-ai-gateway` 含「跨地域/跨境网络要求」。
W7 通读 924 行 + 关键词检索后**明确否认**：全页只有「VPC 必须绑定公网 NAT 网关」这一条网络要求，
跨境专线/GA/CEN/数据出境合规/延迟量级**全部 `[文档未说明]`**，并写明「SA 不得据本页承诺跨境网络方案」。
✅ **W7 的抵制是正确的**，主控的提示词断言无据。这验证了蒸馏契约 §0「严禁用先验补全」真的起了作用 ——
提示词里的具体断言 worker 会当权威照写，**给方法不给结论**这条纪律必须继续执行。

---

## R8 重复与别名

| 事实 | 证据 | 处置 |
|---|---|---|
| `gateway-managed-mcp-services` ≡ `mcp-gateway-management` | 两者正文 SHA256 同为 `ec7aa8c7…`、body_bytes 同为 6094、`diff` 为空（主控实测） | 知识页只写一份内容，溯源双标两个 slug |
| `enable-mcp-service-log-delivery` 与 `enable-gateway-log-delivery` **部分重复** | 日志字段表 SHA256 相同、Response_Flag 章节相同，但两页正文整体不同（W7 实测） | 不是重复页，合并写日志字段表并双标 slug |

---

## R9 llms.txt 收录缺口（官方索引不完整，需靠内链 BFS 补）

| slug | 情况 | 处置 |
|---|---|---|
| `gateway-managed-mcp-services` | **llms.txt 未收录**，靠 `mcp-service-management-1` 的内链 BFS 发现；实为 `mcp-gateway-management` 的别名 | 已抓取（见 R8） |
| `api-apig-2024-03-27-createsecret`（docId 3045062） | llms.txt 未收录，靠 `document_detail/3045062` 实时 301 解析发现落在本产品内 | 属 deferred 的 OpenAPI 逐 Action 页，**登记为 llms.txt 缺口**，不影响核心范围 |
| `product-billing` TOC 未收录 AI Credits 计费说明 | W2 发现：计费目录页完全没列 `ai-credits-billing-details` | 该页已在 core 内（llms.txt 产品概述栏目直接收录），无损失；但说明**目录页不能作为覆盖率判据** |

**覆盖率审计最终结果**（`tests/ai-gateway-coverage-audit-2026-09-21.md`）：
186 快照 ｜ 本产品内链唯一目标 160 ｜ `document_detail/<数字ID>` 形态唯一 docId **378** ｜ 命中既有清单 **358** ｜ 新候选 **1**（= R9 第 2 条）｜ 死链 **0**。

🔴 **只扫 slug 形态会系统性漏掉 378 条 docId 链接** —— 与 AgentCore 侧（50 快照 / 72 条 / 28 docId）同一教训，本次规模大 5 倍。

---

## R10 报价与对客纪律（本次蒸馏产出的硬约束）

1. **文档把价格推走的地方，SA 必须另走购买页核验**。实测被推走的项：专享实例各规格单价（2 处「以控制台/价格页/SLA 协议页面为准」）、Serverless 新版全部 6 项单价（只有「参考单价」无地域单价表）、AI Credits 折算率（**全库查无**「一次智能路由消耗几个 Credit」）、退款金额与比例（全外链）、AI 安全护栏商品价（只指向 `lvwang_guardrail_public_cn` 购买页）。
2. **不给单价的地域禁止用内地价外推**（沿 AgentCore 侧新加坡先例）。
3. **配额白名单突破后官方明示「不作 SLA 承诺」** → 提额＝弃 SLA，这是商务争点，必须在方案里写明。
4. **9 类资源配额在错误码页全是 `%s` 占位符** → 容量规划必须走配额中心/工单，不能从文档取数。
5. **连带计费至少 6 类**（公网流量/CDT、SLS 日志、云监控企业版或 Tracing、模型服务、KMS、AI 安全护栏商品），单价文档全部未说明 → 🔴 **AI 网关账单 ≠ 全成本**，与 [[aliyun-agentcore]] 的「依赖产品独立计费」同一对客话术。
6. **SLR 的 Resource 全为 `"*"`，无资源级收窄**；140 个 Action 中 66 个（47.1%）标「全部资源」；MCP / AI 模型元信息 / 消费者组 / 插件四类对象**在 RAM 层面根本没有 ARN 定义** → 🔴 **多租户隔离无法靠 RAM 资源级授权实现，只能分账号或分实例**。这条是架构级结论，对客讲多租户方案时必须先说。
