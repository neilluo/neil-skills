# AI 网关（AI Gateway）· 阿里云 API 网关产品族 — 专题主页

> **所属**：neil-aliyun-sa 知识库 · Wiki 层专题页家族（7 文件，本页为主页与导航入口）
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`https://help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（**186** 个快照 = 149 个有正文页 + 37 个 TOC 容器页）+ SLA 协议全文外部源 1 页
> **事实标注体系**：`[官方｜slug]` raw 有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕：`tests/ai-gateway-rulings-2026-09-21.md`
>
> 🔴 **对客纪律**（三条铁律，违反任一条即为事故）
> 1. **价格不得直接对客承诺** —— 专享实例规格单价被官方 2 处「以控制台/价格页为准」推走、Serverless 新版 6 项自称「参考单价」、**AI 增强能力的 Credits 折算率查无**（模型调用侧的 Credits 单价机制有文档：`Credits/1M tokens`、默认 0）。报价前必须走购买页核验（清单见 §15.9）。
> 2. **SLA 必须带实例类型限定引用，且存在「无赔偿区」** —— SLA 协议只承诺 serverless 实例 ≥99.90%、普通实例 ≥99.99%；产品页宣称的 99.95% 落在 **[99.90%, 99.95%) 无赔偿区**（裁决 C2）。
> 3. **文档未说明的一律说「文档未说明」** —— 全库共 **550** 处 `[文档未说明]` 标注，这些是官方空白，不许用先验填。

---

## 专题页家族导航

| 文件 | 章节 | 行数 | 什么时候翻它 |
|---|---|---|---|
| **本页** `aliyun-ai-gateway.md` | §0 溯源与范围 · §1 定位与产品族 · §2 形态与容量 · §14 实战避坑 · §15 SA 速查卡 | 1413 | 第一次接触 AI 网关、要给客户讲选型、要背速查卡 |
| [aliyun-ai-gateway-billing.md](aliyun-ai-gateway-billing.md) | §3 计费与商务（含 §3.9 SLA 与赔偿） | 963 | 报价、算总成本、讲 SLA 赔偿、欠费/退款 |
| [aliyun-ai-gateway-traffic.md](aliyun-ai-gateway-traffic.md) | §4 核心对象模型 · §5 流量治理与成本控制 | 1347 | 讲对象层级与依赖顺序、多模型路由、Fallback、Token 限流、FinOps 配额、AI 缓存 |
| [aliyun-ai-gateway-auth.md](aliyun-ai-gateway-auth.md) | §6 鉴权与消费者体系 · §7 AI 安全护栏与 RAM 权限 | 1247 | 客户问鉴权怎么配、消费者体系、内容安全、RAM 最小权限、多租户隔离 |
| [aliyun-ai-gateway-mcp-agent.md](aliyun-ai-gateway-mcp-agent.md) | §8 MCP 与 Agent API 生态 | 1411 | MCP 上架/托管/HTTP转MCP、语义检索、工具精选、Agent API、HiChat |
| [aliyun-ai-gateway-plugins.md](aliyun-ai-gateway-plugins.md) | §9 插件体系 | 1541 | 插件目录与参数、插件延时、自定义插件开发、与内置鉴权的边界 |
| [aliyun-ai-gateway-ops.md](aliyun-ai-gateway-ops.md) | §10 可观测与运维 · §11 门户与开放平台 · §12 实践教程 · §13 OpenAPI 与 RAM 元信息 | 1549 | 日志/追踪/监控、开发者门户、7 个集成配方、OpenAPI 自动化、错误码 |

---

## §0 溯源与范围声明

### 0.1 本次蒸馏的范围与裁决

| 项 | 结论 |
|---|---|
| **产品归属** | AI 网关是 **API 网关产品族下三个平级子产品之一**（云原生API网关 / AI 网关 / 原API网关），不是独立 productCode 文档根。证据：父级 `https://help.aliyun.com/zh/api-gateway/llms.txt`「## 子产品」并列三条，各自拥有独立 llms.txt |
| **本次范围** | 仅 AI 网关子树。云原生API网关、原API网关**未纳入**（原API网关已公告 2026-08-23 停止新购、2027-09-21 全面下线） |
| **源清单** | 官方按产品 llms.txt `https://help.aliyun.com/zh/api-gateway/ai-gateway/llms.txt`，**438** 个链接（4254B 的父级 llms.txt 另存为归属证据） |
| **纳入 core** | **189** 页（按栏目：产品概述 19 / 快速入门 3 / 操作指南 140〔含内链 BFS 新发现 1〕/ 实践教程 9 / 安全合规 7 / 服务支持 3 / 开发参考元页 8）。按抓取 verdict 分：**148 个有正文页**（147 OK + 1 OK-STUB）+ **37 个 TOC 容器页** + **4 个无正文节点**（FAIL-NOMD，不落盘）；另有外部源 SLA 协议全文 1 页 → **参与蒸馏的事实来源 = 149 页** |
| **登记 `[deferred]`** | **250** 页逐 Action / 逐数据结构 OpenAPI 参考页（`api-apig-2024-03-27-*`），沿 AgentCore 侧 AgentRun 317 页先例。**破例纳入 8 个元页**（OpenAPI 概览 / 服务接入点 / RAM 授权信息 / 流控配额 / 公共错误码 / 变更集 / API参考容器 / 开发参考容器）——它们不是逐 Action 页，对 SA 做自动化与最小权限设计有直接价值 |
| **补抓外部源** | SLA 协议全文（terms.alicdn.com）—— help 侧 `support/service-level-agreement` 只有 196B 入口桩 |
| **归属判据修正** | 🔴 归属看 **llms.txt 收录关系**，不看 URL 前缀。首版按前缀判归属，误踢 3 页（含**本次时点的现行计费权威源**「Serverless 新版商业化公告，2026-09-01 起计费」）。裁决 R2 |
| **落地形态** | 扁平 7 文件（不建子目录，与既有 `knowledge/` 同形）。裁决 R3 |

**已裁决的 12 条矛盾**（C1~C12，含裁决依据）见 `tests/ai-gateway-rulings-2026-09-21.md` R5；**未裁决的约 40 条**保留在各专题页的 `[官方矛盾]` 标注中，双方原文并列。

### 0.2 raw 层构成与🔴五种抓取失效模式

抓取通道 = 官方 `.md` Agent 通道（URL 加 `.md` 返回纯 Markdown，纯 curl，无需浏览器）。
抓取器：`scripts/fetch-aliyun-docs.py`（确定性脚本，非 subagent 抓取 → 产物可复算、无二手结论污染）。

| # | 失效模式 | 表现 | 判据 | 本次命中 |
|---|---|---|---|---|
| 1 | **软 200** | 不存在的 slug 返回 HTTP 200 + 约 **24893B** SPA HTML 外壳 | body 前 60 字节以 `<!doctype`/`<html` 开头 | 0（负控实验证实检测器有效，见下） |
| 2 | **CT 不符** | 返回非 markdown Content-Type | CT 不含 `markdown` | 0 |
| 3 | **空 body** | 0 字节 | `len(body)==0` | 0 |
| 4 | 🔴 **Document Not Found 桩**（本次新发现） | CT=markdown、HTTP **200 或 404**（同一 slug 两次抓取状态码不同）、body 恒为 **86B** 固定文案 | 正则匹配固定文案 | **4**（`api-product-management` / `model-metadata-and-provider-management` / `open-platform` / `portal-management` —— 均为导航树里的目录节点，无正文，不落盘） |
| 5 | 🔴 **服务端静默截断**（本次新发现） | HTTP 200、CT=markdown、**Content-Length 与 body 自洽**、**两次抓取 SHA256 完全一致** → 截断在服务端 | 末行是悬挂结构标记 / HTML 标签开闭不平衡 / 末行以未完结词尾结束 | **1**（`agent-api-observable`：978B，断在孤立 `*` 上，Agent API 完整指标清单不可从文档取得）。扫描器：`scripts/scan-truncated-snapshots.py` |

**TOC 容器判据**（沿 AgentCore RULINGS C1，本次再次验证）：判据 = 「正文仅由标题 + 链接列表构成、无散文」，**不是字节阈值**。本次实测 `product-overview` 765B 判 TOC、`support` 113B 判 TOC，而 86B 的 Document Not Found 桩**有散文**故不是 TOC —— 三者字节数相近而性质完全不同，字节阈值必然误判。37 个 TOC 页落盘但**不作事实来源**，只承载目录结构与 slug↔docId 对照证据。

**🔴 负控实验**（门禁全绿本身是失效信号）：抓取器上线前用伪造 slug `this-slug-does-not-exist-xyz` 跑负控 → 被正确判为 `FAIL-SOFT200`（**24893B**，与既有记忆完全一致），证明检测器真的会 FAIL，而不是恒返回 OK。

**首版抓取器的假阳性（已修）**：Document Not Found 桩同时通过前三种校验、且因「有标题+散文」也不是 TOC，首版把它判成 OK **落盘了 4 页垃圾**。已删除并加入第四重校验。

### 0.3 覆盖率审计

审计器：`scripts/audit-doc-coverage.py`（确定性扫描 + docId 实时 301 解析）｜报告：`tests/ai-gateway-coverage-audit-2026-09-21.md`

| 指标 | 数值 |
|---|---|
| 扫描快照 | 186 |
| 本产品内链唯一目标（slug 形态） | 160 |
| `document_detail/<数字ID>` 形态唯一 docId | **378** |
| 命中既有清单 | **358** |
| 新候选 | **1** |
| 死链 | **0** |

🔴 **只扫 slug 形态会系统性漏掉 378 条 docId 链接** —— 与 AgentCore 侧（50 快照 / 72 条 / 28 docId）同一教训，本次规模大 5 倍。两种形态都必须扫，数字形态需实时 301 解析反查落点。

**首版审计器的假警报（已修）**：docId 解析落点若落在其他产品（RAM / VPC / user-center / WAF / CDT / NAT / MSE / SLB / openapi），首版只判 `slug in known`，把 **173 条跨产品链接全洗成「🆕 新候选」**。修正后新候选从 174 → 1。判据必须**先看落点是否在本产品内，再判是否已收录**。

**唯一新候选**：`api-apig-2024-03-27-createsecret`（docId 3045062）—— 属 deferred 的 OpenAPI 逐 Action 页，登记为 **llms.txt 收录缺口**，不影响核心范围。

**内链 BFS 的实际增益**：发现 `gateway-managed-mcp-services` 未被 llms.txt 收录；抓取后实测其正文 SHA256 与已收录的 `mcp-gateway-management` **完全相同**（`ec7aa8c7…`，6094B，`diff` 为空）→ 是**别名而非新内容**。知识页只写一份，溯源双标两个 slug。

**完备性门禁**：`scripts/assign-distill-shards.py` 用集合运算证明 **149 个有正文快照 = 149 条 worker 指派**，无遗漏、无重复、无幽灵 slug（TOC 37 + FAIL-NOMD 4 不参与指派）。

### 0.4 🔴 驳回的两条 worker 结论（防止假账进 KB）

| worker 结论 | 主控复核 | 裁决 |
|---|---|---|
| W7：「`observation-analysis` 是**孤儿页**，存在于 raw 但不在任何 shard TSV，构成覆盖缺口」 | 该页 manifest verdict = **TOC**（382B，正文只有 3 条链接，主控已 `cat` 全文确认） | ❌ **驳回**。TOC 容器按契约本就不作事实来源、不指派，**不是覆盖缺口**。W7 未读取它的行为完全正确，只是把它误判成了遗漏 |
| W4：「`authentication`(629B)、`consumer-management`(452B)、`global-authentication`(504B) 未出现在任何 TSV，可能是覆盖缺口」 | 三者 verdict 均为 **TOC** | ❌ **驳回**，同上 |

**为什么必须留痕**：worker 的「发现」若被主控直接采信写进知识页，就会把一个不存在的覆盖缺口固化成 KB 里的「已知问题」，后续 Lint 会反复追这条假账。这与既有教训（主控的错误前提会被 worker 洗成「已确认的发现」回传）是**同一失效的两个方向**。

**主控自己的错误前提（worker 正确抵制，记此自省）**：主控在 W7 提示词里断言 `access-vertex-ai-through-ai-gateway` 含「跨地域/跨境网络要求」。W7 通读 924 行 + 关键词检索后**明确否认**：全页只有「VPC 必须绑定公网 NAT 网关」这一条网络要求，跨境专线/GA/CEN/数据出境合规/延迟量级**全部 `[文档未说明]`**，并写明「SA 不得据本页承诺跨境网络方案」。✅ W7 的抵制正确，主控的提示词断言无据 —— 验证了「给方法不给结论」这条纪律必须继续执行。

### 0.5 本方法检测不到的残留面（🔴 不得宣称「全站蒸馏」）

若某页同时满足「近日新增 + 未进 llms.txt + 无任何快照内链 + 非顶级栏目」，上述方法**检测不到**，需 JS 拉实时目录树 API 才能穷尽。
llms.txt 本身是**快照会滞后**（本次已实证 2 处收录缺口）。故本页家族的准确表述是：
**「截至 2026-09-21 的官方 llms.txt 收录范围 + 一轮内链 BFS 增量发现，189 页全覆盖；不含 250 页 OpenAPI 逐 Action 参考」**。

### 0.6 🔖 `W1`~`W7` 分工代号对照表（正文引用解析器）

正文与子页里出现的 `W1`~`W7` 是**本次蒸馏批次的分工代号**（7 路并行蒸馏 worker），**不是产品术语**。
保留代号是为了让每条结论可追溯到「谁蒸的、蒸了哪几页、边界怎么划的」—— 与本 KB 既有约定同形
（`aliyun-agentcore.md` 里约 26 处 `RULINGS §x/B/G/D` 引用指向 `tests/agentcore-distill-rulings-*.md`）。
**读到 `W*` 时按下表解析**：

| 代号 | 落地文件 | 章节 | 蒸馏页数 | 主题 |
|---|---|---|---|---|
| **W1** | 本页 `aliyun-ai-gateway.md` | §1 + §2 | 17 | 产品定位与产品族归属、实例形态与容量规格、地域、引擎版本、实例与网络底座 |
| **W2** | `aliyun-ai-gateway-billing.md` | §3（含 §3.9） | 11 | 全部计费口径、商业化时间线、账单/欠费/退款、SLA 可用率与赔偿档位 |
| **W3** | `aliyun-ai-gateway-traffic.md` | §4 + §5 | 21 | 对象模型与依赖顺序、Model API 与路由、供应商与模型元信息、智能路由、Fallback、Token 限流、FinOps 配额、AI 缓存 |
| **W4** | `aliyun-ai-gateway-auth.md` | §6 + §7 | 20 | 消费者体系、四类内置鉴权、密钥与 KMS、AI 安全护栏、IP 黑白名单、RAM 身份与权限策略、SLR |
| **W5** | `aliyun-ai-gateway-mcp-agent.md` | §8 | 21 | MCP 四类接入、HTTP to MCP 字段参考、Tool 组装、语义检索、工具精选、调试、灰度、Agent API、HiChat |
| **W6** | `aliyun-ai-gateway-plugins.md` | §9 | 34 | 插件机制与目录总表、AI 增强/认证/流量/安全/转换类插件、自定义插件开发、插件性能参考 |
| **W7** | `aliyun-ai-gateway-ops.md` | §10~§13 | 25 | 日志与链路追踪与监控、开发者门户与开放平台、7 个集成配方、OpenAPI 概览/接入点/RAM/流控配额/错误码/变更集 |
| 主控 | 本页 | §0 + §14 + §15 | — | 溯源与范围声明、实战避坑汇编、SA 速查卡、口径裁决、装配与门禁 |

合计 149 页有正文快照，**集合运算证明无遗漏、无重复、无幽灵 slug**（`scripts/assign-distill-shards.py`）。
各 worker 上报的边界移交与重叠项，已由主控在 §14 / §15 与 `tests/ai-gateway-rulings-2026-09-21.md` R5 收口。

### 0.7 工艺制品清单（全部在版本控制内，`outputs/` 被 gitignore 故不落那里）

| 制品 | 路径 |
|---|---|
| llms.txt 快照（本产品 + 父级归属证据） | `tests/ai-gateway-llms-2026-09-21.txt`、`tests/api-gateway-parent-llms-2026-09-21.txt` |
| 文档树与分片清单（含范围裁决与分类判据） | `tests/ai-gateway-doctree-shards-2026-09-21.md` |
| 抓取 manifest（189 行 × 13 列，含每页 verdict 与 sha256） | `tests/ai-gateway-fetch-manifest-2026-09-21.tsv` |
| 覆盖率审计报告 | `tests/ai-gateway-coverage-audit-2026-09-21.md` |
| 蒸馏契约（7 路 worker 共读） | `tests/ai-gateway-distill-contract-2026-09-21.md` |
| **主控裁决留痕（R1~R10 + C1~C12）** | `tests/ai-gateway-rulings-2026-09-21.md` |
| 可复用脚本 | `scripts/build-doc-inventory.py`（llms.txt→清单+分片）、`scripts/fetch-aliyun-docs.py`（五重校验抓取）、`scripts/audit-doc-coverage.py`（双形态覆盖率审计）、`scripts/assign-distill-shards.py`（派工完备性门禁）、`scripts/scan-truncated-snapshots.py`（截断扫描）、`scripts/assemble-ai-gateway-pages.py`（装配） |

## §1 产品定位与产品族归属

### 1.1 官方定位（原文口径）

> 「为应对上述挑战，**云原生API网关推出AI网关产品**，作为企业AI应用与模型服务、工具及其他Agent之间的**核心连接组件**，通过提供协议转换、安全防护、流量治理和统一观测等能力，协助企业构建和管理 AI 原生应用。」
> —— [官方原文｜what-is-an-ai-gateway]

> 「AI网关提供包括模型、MCP Server与Agent的代理能力」；产品对比页把 AI 网关的版本描述概括为「**统一代理模型API、MCP Server和Agent API，并提供丰富的集成、安全和治理能力**」[官方原文｜what-is-an-ai-gateway｜product-comparison]

控制台入口：`https://apig.console.aliyun.com/#/ai-gateway-overview`（概述页给出的链接）；操作类页面统一给 `https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway`（默认落杭州地域）。[官方｜what-is-an-ai-gateway｜create-a-gateway-instance]
[推断] 两个入口 host 不同（`apig` vs `apigw`），SA 给客户贴链接时需注意 —— 由 what-is-an-ai-gateway 的 `apig.console.aliyun.com` + 其余操作页的 `apigw.console.aliyun.com` 推出两者并存。

### 1.2 AI 网关解决什么问题：官方拆的三类场景 × 挑战

| 场景 | 官方归纳的挑战 | 挑战要点（限定词照抄） | 来源 slug |
|---|---|---|---|
| AI 应用访问各类模型服务 | 「三多两高」 | **多模型**：不同供应商 API 规范/认证机制/调用方式存在差异，「缺乏标准化的抽象层支持多模型并行调用」；**多模态**：「与文生文大模型统一兼容OpenAI标准不同」，多模态在传输协议（SSE、WebSocket、WebRTC）、通信模式（同步/异步）、请求响应结构上「缺乏统一标准」；**多场景**：实时语音转换要求低延迟（low RT），长文本理解强调处理稳定性；**安全要求高**：数据泄露风险，「尤其是在使用外部或开源模型时」；**稳定性要求高**：模型服务「受限于底层算力资源，普遍存在较低的接口限流阈值」，RT 和成功率「波动较大」 | what-is-an-ai-gateway |
| AI 应用调用外部工具 | 「精准安全」 | 工具数增长后「若将全部工具列表输入大模型进行推理选择，会导致 token 消耗显著上升」；「候选工具过多可能引发模型误选」；「已出现如 **MCP 恶意投毒**等新型攻击手段」 | what-is-an-ai-gateway |
| AI 应用被外部访问（含被其他 AI 应用访问，走 A2A 等协议） | 「稳定灵活」 | 三类构建方式（**高代码**：Spring AI Alibaba / ADK / LangChain；**低代码**：百炼等可视化拖拽；**零代码**：JManus 等仅提示词配置）导致「接入方式缺乏统一标准」；「若未采取有效的隔离与容错机制，单点故障可能引发连锁反应」 | what-is-an-ai-gateway |

### 1.3 核心能力矩阵（SA 可直接引用）

| 能力域 | 具体能力 | 关键限定 / 数字 | 来源 slug |
|---|---|---|---|
| 统一代理的服务类型 | AI 服务、Agent 服务、容器服务、Nacos 服务、DNS 服务、固定地址、SAE 服务、FC 服务、计算巢 MCP 服务（共 9 类） | AI 服务涵盖百炼、OpenAI、Minimax、Anthropic、Amazon Bedrock、Azure，兼容 Ollama、vLLM、SGLang 自建模型；Agent 服务支持百炼、Dify 及用户自定义 Agent 工作负载，「可配置API-KEY和APP-ID」；**容器服务：单个 AI 网关实例最多可关联 3 个容器集群**（与配额表冲突，见 §2.7）；FC 服务「可绕过HTTP Trigger，直接与后端服务集成」 | what-is-an-ai-gateway |
| 健康检查 | 主动健康检查、被动健康检查两种模式 | 被动健康检查由引擎 **2.1.10（2025-08-13）** 引入 | what-is-an-ai-gateway｜engine-version-description |
| 模型负载均衡 | Model API 预置 **3 种**：单模型服务 / 多模型服务（按模型名称）/ 多模型服务（按比例） | 单模型服务「当显示指定模型名称时，用户请求中传入的模型名称将被忽略」[原文如此，「显示」疑为「显式」]；按名称示例 `deepseek-*`→DeepSeek、`qwen-*`→百炼；按比例「适用于新模型灰度发布等场景」 | what-is-an-ai-gateway |
| 自定义路由 | Model API 支持按请求特征（如特定 Header）转发 | Agent API 同样支持基于请求特征的灰度发布 | what-is-an-ai-gateway |
| 消费者鉴权 | **API-KEY、JWT、HMAC 三种**；Model API / MCP Server / Agent API 均可按需开启。🔴 **但 MCP 场景的认证方式官方口径冲突**（本页 §1.3 依据的是概述页，而 MCP 消费者认证专页称「目前仅支持 API Key」，2026-01 发布记录又称「MCP Server 支持 JWT 认证」）→ **不得据本行对客承诺 MCP 支持 JWT，须实测**（裁决 C9 已修订，见 §15.7 与 [-auth §6.4](aliyun-ai-gateway-auth.md)） | 「对于安全敏感的场景，用户可将消费者凭证托管到 KMS 上」 | what-is-an-ai-gateway（+ `[官方矛盾]` consumer-certification / new-feature-release-notes-ai-gateway） |
| 消费者观测指标 | QPS（AI请求QPS/流式响应QPS/非流式响应QPS）、请求成功率、token 消耗数/s（输入/输出/总计）、请求平均 RT（非流式RT/流式RT/流式首包RT）、缓存命中数、限流统计、按模型 token 统计、按消费者 token 统计、风险统计 | 成功率与 RT 均「支持按秒、15秒、分钟粒度进行统计」；RT 单位毫秒 | what-is-an-ai-gateway |
| 计量计费 | 以消费者为维度，「提供特定消费者在指定时间段内调用特定模型所消耗的Token数量等明细数据」 | —— | what-is-an-ai-gateway |
| 限流维度 | 基于消费者、模型名称、请求 Header 等；可限「单位时间内的请求数、并发数、连接数及 Token 数」 | —— | what-is-an-ai-gateway |
| AI 安全防护维度 | **5 个**：`contentModeration` 内容合规检测、`promptAttack` 提示词攻击检测、`sensitiveData` 敏感内容检测、`maliciousFile` 恶意文件检测、`waterMark` 数字水印标识 | 支持按 API 配置启用；防护范围含「敏感词、合规性、提示词注入攻击及爆破攻击」 | what-is-an-ai-gateway |
| AI 安全拦截策略档位 | **高**：风险等级 low、medium、high 均拦截；**中**：medium、high 拦截；**低**：仅拦截 high；**观察模式**：不拦截，仅记录 | 各防护维度可分别配置独立拦截策略 | what-is-an-ai-gateway |
| 插件体系 | 内置扩展策略与插件 + 用户自定义插件；「所有策略与插件均支持热插拔与热更新，确保配置变更过程中服务流量不受影响」 | Model API 预置 **5 项**核心策略：工具精选、安全防护、限流、缓存、联网搜索 | what-is-an-ai-gateway |
| 安全三层 | 网络安全（SSL 证书、WAF 防护、IP 黑白名单）／数据安全（消费者侧身份鉴权避免 API Key 暴露、后端鉴权与 API Key 管理、KMS 托管密钥「防止敏感信息在网关本地落盘」）／内容安全（AI 安全护栏 + 数据脱敏插件，「在请求转发前去除敏感信息」） | WAF 在 Serverless 上不可用，见 §2.11.8 | what-is-an-ai-gateway｜view-gateway-instance-details |
| 多模态代理 | 「支持代理 HTTP 和 WebSocket 协议的多模态模型调用」 | —— | what-is-an-ai-gateway |
| Agent 接入 | 直连 ACK、FC、SAE；服务发现统一暴露不同计算平台的 AI 应用；提供 **REST 到 A2A 协议的转换能力**；推荐「基于A2A协议通过Nacos AI Registry实现服务的注册与发现」 | 百炼低代码应用「支持统一代理接入，并可扩展二次鉴权机制」 | what-is-an-ai-gateway |
| 工具治理 | HTTP to MCP 转换（存量 API 自动转 MCP Server）、虚拟 MCP Server 按需组合工具列表、智能工具路由（网关侧按请求内容自动筛选工具集合）、MCP Server 级鉴权 + **单个工具粒度**的访问权限配置 | 「实现Provider与Consumer独立定义各自的MCP Server」 | what-is-an-ai-gateway |

### 1.4 产品族归属与「云原生 API 网关 / 原 API 网关」的边界

我的 17 个快照**没有**给出「API 网关产品族下三个平级子产品、各自独立文档树」的明文表述。以下是快照里能拿到的全部边界证据：

| 证据 | 原文 / 事实 | 来源 slug |
|---|---|---|
| AI 网关的出品方 | 「**云原生API网关推出AI网关产品**」 | what-is-an-ai-gateway |
| 文档树 URL 前缀 | 全部 17 页 `source_url` 均为 `https://help.aliyun.com/zh/api-gateway/ai-gateway/...`（产品概述在 `product-overview/`，操作指南在 `user-guide/`） | 全部 17 页 frontmatter |
| 「普通网关」与「AI 网关」并列 | 「**AI 网关与普通网关支持区分默认告警规则类型**，AI 网关使用专属告警指标（AIGatewayEnvoyCpuUsageRate、AIGatewayEnvoyMemoryUsageRate、AIGatewayEnvoyPluginCrash）」（2026-03） | new-feature-release-notes-ai-gateway |
| 文档串味（未清理的上游产品名） | 「目前**云原生API网关**支持**HTTP** 协议和**HTTPS** 协议，且**HTTPS**协议必须关联SSL证书」—— 出现在 AI 网关的域名文档里 | change-the-protocol-and-certificate-of-the-domain-name |

[推断] 由「云原生API网关推出AI网关产品」+ 文档树挂在 `/api-gateway/ai-gateway/` 下 + 告警规则区分「AI 网关 / 普通网关」三条证据推出：AI 网关在文档与商品层面是**从云原生 API 网关派生出的独立子树**，而非云原生 API 网关的一个功能开关。但**「三者平级」「原 API 网关」的定位与迁移关系，我的快照查无明文**，需主控向 §0 范围声明或其他 worker 求证。

[文档未说明] AI 网关与「原 API 网关」（传统 API 网关）的能力边界、是否可互相迁移、是否有存量替换路径 —— 17 页里完全没有出现「原API网关」「传统API网关」字样。
[文档未说明] AI 网关实例与云原生 API 网关实例能否共用一个实例、能否互相转换形态 —— 查无。

### 1.5 AI 网关 vs Higress 开源版（逐行照抄）

> 页面导语：「本文从AI能力、成本、稳定性、性能、安全合规与微服务和 API 管理多维度介绍 AI 网关与 Higress 开源版的差异。」[官方原文｜product-comparison]

原始表格为 HTML `<table>`，**「能力维度」列使用了跨行合并渲染，部分行只有 3 个单元格**。下表按合并关系还原，未丢单元格；还原处的维度归属标 `[推断]`。

| 能力维度 | 能力 | AI 网关 | Higress 开源版 |
|---|---|---|---|
| 基本信息 | 版本描述 | 统一代理模型API、MCP Server和Agent API，并提供丰富的集成、安全和治理能力 | 具备 AI 网关的开源能力 |
| 基本信息 [推断] | 适用场景 | 开箱即用，在稳定性、性能、云产品集成和易用性上，比社区版更有优势，并提供工单、钉群等商业服务支持 | 需要使用者具备一定的开发和维护能力，自行兜底稳定性、性能、云产品集成和易用性 |
| AI 能力 | 代理 | 支持 | 支持 |
| AI 能力 [推断] | 多模型灰度 | 支持 | 支持 |
| AI 能力 [推断] | 多模型间 Failover | 支持 | 支持 |
| AI 能力 [推断] | Token 额度管理和流控 | 支持 | 支持 |
| AI 能力 [推断] | 路由配置认证 | 支持，并且具备更丰富的认证算法：`jwt`/`hmac`/`oauth2` | 支持 |
| AI 能力 [推断] | 消费者鉴权 | 支持，并且具备更精细的鉴权粒度： MCP工具 | 支持 |
| AI 能力 [推断] | 联网搜索 | 支持 | 支持 |
| AI 能力 [推断] | 企业级可观测 | 支持 | **自行构建** |
| AI 能力 [推断] | API-to-MCP | 支持 | 支持 |
| AI 能力 [推断] | MCP 协议卸载 | 支持 | 支持 |
| AI 能力 [推断] | MCP 市场 | 支持 | 支持 |
| AI 能力 [推断] | MCP工具组装 | 支持 | **自行构建** |
| 成本 | 全托管、免运维 | 支持 | **不支持** |
| 成本 [推断] | 系统搭建和扩缩容 | 支持 | **自行构建** |
| 稳定性 | 多可用区部署 | 支持 | **自行构建** |
| 稳定性 [推断] | 故障自动检测及恢复 | 支持 | **不支持** |
| 稳定性 [推断] | 限流降级 | 支持按 Token、请求数、并发数限流 | **自行构建** |
| 稳定性 [推断] | 监控告警 | 支持 | **自行构建** |
| 稳定性 [推断] | SLA | **99.99%** | **不支持** |
| 性能 | 内核优化 | **90%+** | 自行调优 |
| 性能 [推断] | 软硬一体 | **50%+** | **不支持** |
| 安全合规 | WAF 防护 | 深度集成阿里云 WAF 产品 | 自行构建 |
| 安全合规 [推断] | OIDC认证 | 深度集成阿里云 IDAAS 产品 | 自行构建 |
| 安全合规 [推断] | 加密凭证 | 深度集成阿里云 KMS 产品 | 自行构建 |
| 安全合规 [推断] | AIGC防护（安全围栏） | 深度集成阿里云内容安全产品 | 自行构建 |

来源：[官方｜product-comparison]

**SA 用法要点**
- 开源版**明确「不支持」**的 4 项：全托管免运维、故障自动检测及恢复、SLA、软硬一体。这 4 项是对客「为什么不能自己搭 Higress」的最硬论据。[官方｜product-comparison]
- 开源版需**「自行构建」**的 10 项：企业级可观测、MCP工具组装、系统搭建和扩缩容、多可用区部署、限流降级、监控告警、WAF 防护、OIDC认证、加密凭证、AIGC防护（安全围栏）。[官方｜product-comparison]
- 开源版**同样「支持」**的 10 项 AI 能力：代理、多模型灰度、多模型间 Failover、Token 额度管理和流控、路由配置认证、消费者鉴权、联网搜索、API-to-MCP、MCP 协议卸载、MCP 市场。→ [推断] 客户若只用这些能力且自有运维团队，「自建 Higress」在功能面成立，差异落在成本/稳定性/安全合规的**集成度**上，而不是 AI 功能有无。
- 认证算法差异：AI 网关明示 `jwt`/`hmac`/`oauth2`；开源版只写「支持」未列算法。[官方｜product-comparison]

[官方矛盾] 认证算法集合两页不一致：
- 原文 A：「路由配置认证｜支持，并且具备更丰富的认证算法：`jwt`/`hmac`/`oauth2`」[product-comparison]
- 原文 B：「AI 网关支持 **API-KEY、JWT、HMAC** 三种消费者鉴权方式」[what-is-an-ai-gateway]
- A 有 `oauth2` 无 `API-KEY`，B 有 `API-KEY` 无 `oauth2`。**不裁决**，归 W4。

[文档未说明] 「内核优化 **90%+**」「软硬一体 **50%+**」的**度量基准、压测条件、对比对象**（相比开源版？相比上一代？QPS 还是 RT？）—— 页面只给两个裸百分数，无任何口径。SA 引用有对客风险。
[文档未说明] 本页 `SLA 99.99%` **未带实例类型限定**，而 ai-gateway-capacity-description 明确 99.99% 只对应「实例型独享版」。见 §2.5 [官方矛盾]。
[文档未说明] AI 网关引擎版本（2.1.x）与 Higress 开源版版本号的对应关系 —— 查无。
[文档未说明] Higress 开源版是否有阿里云商业支持通道（除 AI 网关的「工单、钉群」外）—— 查无。
[文档未说明] 对比表导语点名了「微服务和 API 管理」维度，但**表内没有任何一行属于该维度**（表的维度只有：基本信息、AI 能力、成本、稳定性、性能、安全合规）→ 导语与表体不匹配，属页面自身缺口。

### 1.6 API 产品概念：三类接入的产品化封装

> 「将底层 AI API 能力封装为标准化产品，管理员可以将 MCP Server、Model API、Agent API 打包后发布到门户，供开发者浏览和订阅。」[官方原文｜api-product-introduction]

| 项目 | 内容 | 来源 slug |
|---|---|---|
| 归属 | 「API 产品是 **AI 网关开放平台的核心概念**」 | api-product-introduction |
| 支持的产品类型（目前 3 种） | **MCP Server**：将 MCP Server 封装为标准化 API 产品，供开发者订阅调用；**Model API**：将模型 API 封装为标准化 API 产品，提供统一的调用入口；**Agent API**：将 Agent API 封装为标准化 API 产品，便于开发者集成到业务场景中 | api-product-introduction |
| 生命周期状态（3 态） | **待配置**（刚创建，需要关联 API）→ **待发布**（已关联 API，可以发布到门户）→ **已发布**（已发布到门户，开发者可订阅） | api-product-introduction |
| 发布物 | 打包 API + 「搭配产品使用文档」后发布到门户；「登录门户的开发者即可浏览并订阅所需的 API 产品」 | api-product-introduction |
| 相关能力上线时间 | 2026-04「集成 **HiMarket**，支持通过控制台搭建 AI 开放平台，进行 API 产品管理、门户管理与产品分类管理」 | new-feature-release-notes-ai-gateway |

[推断] 由「API 产品是 AI 网关开放平台的核心概念」+ 2026-04 集成 HiMarket 推出：API 产品是**开放平台/开发者门户层**的对象，不是流量面对象；Model API / MCP Server / Agent API 才是流量面对象，API 产品是它们的对外售卖封装。
[文档未说明] API 产品的数量配额（每实例可创建多少个）、产品分类数量上限、订阅是否需审批、订阅后如何计费、API 产品与实例类型（标准版/企业版/独享版）的可用性关系 —— 全部查无。capacity-description 的配额表里**没有「API 产品数」这一配额项**。
[文档未说明] 生命周期是否可从「已发布」回退到「待发布」（下线动作）—— 查无。

### §1 溯源

- `what-is-an-ai-gateway` — AI 网关产品概述（19843 B）：§1.1 定位原文与控制台入口；§1.2 三类场景与「三多两高 / 精准安全 / 稳定灵活」全部挑战描述；§1.3 核心能力矩阵全部行（9 类服务、3 种负载均衡、5 个安全防护维度与 4 档拦截策略、5 项 Model API 预置策略、消费者鉴权三算法、观测指标与统计粒度、安全三层、工具治理）；§1.4「云原生API网关推出AI网关产品」；§1.5 认证算法口径矛盾的一方；§2.7 容器集群数矛盾的一方
- `product-comparison` — AI 网关与 Higress 开源版对比（3748 B）：§1.5 整张对比表（27 行，含 HTML 合并单元格还原）与「不支持 / 自行构建 / 支持」三分统计；§1.1 版本描述原文；§1.5 四处「文档未说明」；§2.5 SLA 99.99% 无限定的一方；§2.11.8 WAF 无实例类型限定的一方
- `api-product-introduction` — API 产品概念介绍（1697 B）：§1.6 全部（3 类产品、3 态生命周期、开放平台归属）
- `change-the-protocol-and-certificate-of-the-domain-name` — 更换域名协议和证书（1079 B）：§1.4「目前云原生API网关支持HTTP/HTTPS协议」串味证据（本页主体内容归 §2.11.3）
- `new-feature-release-notes-ai-gateway` — 新功能发布记录（14419 B）：§1.4「AI 网关与普通网关区分告警规则」；§1.6 HiMarket 集成时间（本页主体时间线归 §2.12）
- `capacity-description` — AI网关-容量规格与资源配额（7972 B）：§1.6「配额表无 API 产品数」这一否定性结论（本页主体归 §2.4 / 2.6 / 2.7 / 2.8）
- `ai-gateway-capacity-description` — 网关类型（15992 B）：§1.5 SLA 分档口径对照方（本页主体归 §2.1~2.3 / 2.5）
- `engine-version-description` — AI 网关引擎版本说明（5988 B）：§1.3 被动健康检查引入版本 2.1.10（本页主体归 §2.10）
- `view-gateway-instance-details` — 查看网关实例详情（1006 B）：§1.3 安全三层中 WAF 的形态限制交叉引用（本页主体归 §2.11.8）
- 未在 §1 直接引用的快照：`supported-regions`、`create-a-gateway-instance`、`modifying-gateway-parameter-configurations`、`configure-dns-server`、`set-security-group-rules`、`setting-the-specified-https-cipher-suite`、`create-a-domain-name`、`delete-a-domain-name` —— 全部用于 §2，非弃用

**本章查无**（翻过但文档确实没写、SA 会被问到的高价值问题）：
1. AI 网关与「原 API 网关」（传统 API 网关）的能力边界、存量迁移路径、能否并存 —— 17 页零提及
2. 「API 网关产品族下三个平级子产品、各自独立文档树」的官方明文 —— 只有 §1.4 的间接证据
3. AI 网关实例能否与云原生 API 网关实例共用 / 互转 —— 查无
4. Higress 开源版版本号与 AI 网关引擎 2.1.x 的对应关系 —— 查无
5. 「内核优化 90%+」「软硬一体 50%+」的度量基准与压测口径 —— 只有裸百分数
6. product-comparison 的 SLA 99.99% 是否适用全部实例类型 —— 本页无限定词
7. AI 网关支持代理的模型供应商**完整清单**（是否穷举）—— what-is-an-ai-gateway 只列 6 家商用 + 3 种自建框架，未声明完整性
8. API 产品的数量配额、分类上限、订阅审批流、订阅计费口径 —— 查无（且配额表无此项）
9. API 产品是否受实例类型限制（Serverless 标准版能否用开放平台）—— 查无
10. A2A 协议的支持程度（是否完整实现规范、支持哪些 A2A 版本）—— 只提「REST 到 A2A 协议的转换能力」和「推荐基于A2A协议通过Nacos AI Registry」
11. MCP 协议支持的版本范围 —— 查无
12. AI 网关是否代理 **WebRTC** —— what-is-an-ai-gateway 把 WebRTC 列为多模态传输协议的例子，但只明说「支持代理 HTTP 和 WebSocket」，WebRTC 是否支持未写
13. 「智能工具路由」的筛选算法、召回率、是否额外计费 —— 查无（能力细节归 W5，此处记录定位层空白）
14. product-comparison 导语承诺的「微服务和 API 管理」维度对比内容 —— 表内无对应行

---

## §2 实例形态与容量规格

### 2.1 实例类型全景 —— 官方存在三套并行的命名口径

| 口径来源 | 使用的名称 | 分几档 | 来源 slug |
|---|---|---|---|
| 「网关类型」页（产品概述） | **Serverless 标准版** / **Serverless 企业版** / **Serverless（旧）** / **实例型独享版** | 4 | ai-gateway-capacity-description |
| 「容量规格与资源配额」页（产品概述） | **Serverless 版**（下分 Serverless（旧）/ Serverless（标准版）/ Serverless（企业版））与 **专享实例版**（按规格前缀分 Small `aigw.small.*` / Medium `aigw.medium.*` / Large `aigw.large.*` 三档） | 2 大版 + 3 档 | capacity-description |
| 「创建 AI 网关实例」页（购买页商品类型） | **专享实例（按量付费）** / **专享实例（包年包月）** / **Serverless（按量付费）** | 3 | create-a-gateway-instance |

[官方矛盾] 顶配形态命名 + 购买页缺失 Serverless 三分：
- 原文 A：「**实例型独享版**｜高规格独享实例｜核心生产、高并发、高隔离或完整治理能力要求较高的业务」[ai-gateway-capacity-description]
- 原文 B：「AI 网关分为 **Serverless 版和专享实例版**两种版本，专享实例版按规格名称前缀分为 Small（`aigw.small.*`）、Medium（`aigw.medium.*`）、Large（`aigw.large.*`）三个档位」[capacity-description]
- 原文 C：「**商品类型**｜支持**专享实例（按量付费）**、**专享实例（包年包月）**与**Serverless（按量付费）**，关于三种类型的计费方式请参考专享实例计费说明」[create-a-gateway-instance]
- [推断] 由 A+B+C 推出「实例型独享版」＝「专享实例版」＝购买页的「专享实例」；但**购买页文档尚未反映 Serverless 的标准版/企业版/旧版三分**，说明 create-a-gateway-instance 口径滞后于 2026-07 的多租 Serverless 公测。不裁决。

[官方矛盾] 同一份 `capacity-description` 页面内，规格名前缀**两处写法不一致**：
- 「容量规格」表：`aigw.small.x1`、`aigw.small.x2`、`aigw.small.x4`、`aigw.medium.x1/x2/x3`、`aigw.large.x1/x2/x3/x4`（10 个全部 `aigw`）
- 同页「实例配额」表头：`aigw.small.x1`，但随后是 `apigw.small.x2`、`apigw.small.x4`、`apigw.medium.x1/x2/x3`、`apigw.large.x1/x2/x3/x4`（首列 `aigw`，其余 9 列 `apigw`）
- 交叉证据：create-a-gateway-instance 要求「选择 **aigw.medium.x1** 以上规格」，压测表头也写 `aigw.medium.x1` → 倾向 `aigw` 为正写。**按契约不裁决**，两套写法原文都在。[官方矛盾｜capacity-description｜create-a-gateway-instance]

[官方矛盾] API 对象命名 Model API vs LLM API：
- `what-is-an-ai-gateway` / `capacity-description` 用 **Model API**（配额行原文：「在线路由总数（含**Model API**路由、Agent API路由）」）
- `ai-gateway-capacity-description` 用 **LLM API**（「统一承载 **LLM API**、Agent API、MCP Server、智能路由、观测分析等 AI 网关核心能力」）
- `new-feature-release-notes-ai-gateway` 混用：2025-05「**LLM API** 支持自定义路由」vs 2025-07「**Model API**支持代理万相、cosyvoice 等多模态模型」
- `engine-version-description` 2.1.10 用「支持对 **LLM API** 配置流式场景下的首字节超时」
- [推断] 由两条发布记录同指「自定义路由」能力 + 配额行只列 Model API / Agent API 推出：LLM API 与 Model API 是同一对象的两种叫法（疑为旧称/新称）。不裁决。

### 2.2 选型判据

**官方「如何选择」表（逐行照抄）**

| 如果您需要 | 推荐选择 | 来源 slug |
|---|---|---|
| 低成本快速体验 AI 网关核心能力 | Serverless 标准版 | ai-gateway-capacity-description |
| 企业采购前 PoC 或开发测试环境 | Serverless 标准版 | ai-gateway-capacity-description |
| 正式生产业务，需要更高服务等级 | Serverless 企业版 | ai-gateway-capacity-description |
| 需要自定义域名、证书、TLS policy 或 HTTP/2 配置 | Serverless 企业版 | ai-gateway-capacity-description |
| 已有 Serverless（旧）实例，短期内不调整业务链路 | Serverless（旧）继续使用 | ai-gateway-capacity-description |
| 高并发、强隔离、高合规或完整高级治理能力 | 实例型独享版 | ai-gateway-capacity-description |

**实例类型概览（官方 4 行表）**

| 实例类型 | 产品定位 | 适用场景 | 主要特点 |
|---|---|---|---|
| Serverless 标准版 | 低门槛 AI 网关实例 | 快速试用、PoC、开发测试、低流量业务 | **0 元起步**，按量付费，使用**平台分配入口** |
| Serverless 企业版 | 生产级 Serverless AI 网关实例 | 正式生产业务、需要独立入口或自定义域名的业务 | 提供**独立入口能力**，支持自定义域名和传输加密配置 |
| Serverless（旧） | 原 Serverless 版本 | 已有存量实例继续使用、平滑过渡 | 已有实例可继续管理和使用，**能力以原版本为准** |
| 实例型独享版 | 高规格独享实例 | 核心生产、高并发、高隔离或完整治理能力要求较高的业务 | 提供更高规格、更强隔离和更完整的网关能力 |

来源：[官方｜ai-gateway-capacity-description]

**典型场景推荐（官方 8 行表）**

| 客户场景 | 推荐实例类型 | 说明 |
|---|---|---|
| 快速体验智能路由、Agent API 或 MCP Server | Serverless 标准版 | 低成本试用，适合低频调用和功能验证 |
| 企业采购前 PoC | Serverless 标准版 | 快速创建、低成本验证，后续可迁移到企业版 |
| 开发或测试环境长期保留网关实例 | Serverless 标准版 | 无实例费，适合非生产环境 |
| 正式生产业务上线 | Serverless 企业版 | 提供独立入口、更高服务等级、自定义域名和证书能力 |
| SaaS 服务对外提供稳定 API 入口 | Serverless 企业版 | 独立访问入口和自定义域名更符合对外服务诉求 |
| 已有 Serverless（旧）生产实例 | Serverless（旧）继续使用，并评估迁移 | 已有实例管理操作保持不变，迁移可按业务窗口规划 |
| 大客户核心系统或高合规业务 | 实例型独享版 | 提供更高服务等级、更强隔离和完整能力 |
| 高并发或需要完整高级治理能力 | 实例型独享版 | 适合重载和复杂治理场景 |

来源：[官方｜ai-gateway-capacity-description]

**迁移路径（官方口径，全部带「规划中 / 以控制台为准」限定）**

| 迁移方向 | 官方表述 | 时间边界 / 空白 |
|---|---|---|
| 标准版 → 企业版 | 「标准版**后续规划**支持**一键升级**为企业版，**无需资源迁移**。升级后可获得企业版的独立入口、自定义域名、传输加密配置、更高 QPS 和更高服务等级等能力」 | 「具体支持时间、升级条件和操作入口**请以产品控制台展示为准**」→ **文档级空白**（截至快照日 2026-09-21 未给上线时间） |
| Serverless（旧）→ 新版 | 「如果您希望降低使用门槛并快速体验新版 AI 能力，可以评估 Serverless 标准版。如果您希望获得生产级入口、自定义域名和更高服务等级，可以评估 Serverless 企业版。如果原实例承载核心高流量业务或依赖完整高级治理能力，可以评估实例型独享版」 | 无迁移工具 / 无自动迁移承诺；「如需新购 Serverless（旧），请以**控制台可购买范围和产品规则**为准」 |
| 企业版 → 实例型独享版 | 「当业务需要更高服务等级、更强资源隔离、高并发、完整高级治理能力或更高合规要求时，建议评估实例型独享版」 | 是否支持在线变配、是否需重建实例 —— **文档级空白** |

来源：[官方｜ai-gateway-capacity-description]

**新版 Serverless 相比 Serverless（旧）的 6 项优势（官方逐条）**

| 优势 | 原文要点 |
|---|---|
| 资源使用更高效 | 「采用**多租资源池化架构**，可提升整体资源利用效率，降低低流量和弹性波动场景下的使用门槛」 |
| 开通和扩展更灵活 | 「更适合快速创建、按需使用和弹性增长的业务场景，标准版支持 0 元起步，企业版提供生产级入口能力」 |
| 版本分层更清晰 | 「区分标准版和企业版，分别面向低成本试用、开发测试和生产业务」 |
| 能力演进更统一 | 「统一承载 LLM API、Agent API、MCP Server、智能路由、观测分析等 AI 网关核心能力，**后续新增能力会优先围绕新版 Serverless 演进**」 |
| 支持插件体系 | 「新版 Serverless 支持平台提供的插件体系，**不支持自定义插件**。用户可根据实例类型和功能开放范围使用插件能力」 |
| 迁移路径更明确 | 「已有 Serverless（旧）实例可继续使用；**新客户建议优先选择新版 Serverless 标准版或企业版**」 |

来源：[官方原文｜ai-gateway-capacity-description]
[推断] 由「后续新增能力会优先围绕新版 Serverless 演进」+「Serverless（旧）…不支持插件体系」推出：Serverless（旧）已进入能力冻结状态，SA 不应向新客户推荐旧版；存量客户的插件需求必须走新版或独享版。

**命名规范（官方注意事项原文）**
> 「新版统一称为 **Serverless** ，包含 **标准版** 和 **企业版** ；原版本称为 **Serverless（旧）**。」[官方原文｜ai-gateway-capacity-description]

### 2.3 四形态能力对比（官方 12 行表，逐格照抄）

| 对比项 | Serverless 标准版 | Serverless 企业版 | Serverless（旧） | 实例型独享版 |
|---|---|---|---|---|
| 推荐业务阶段 | 试用、评估、开发测试、低流量业务 | 正式生产、规模化业务 | 正式生产、规模化业务 | 核心生产、高并发、高合规业务 |
| 起步成本 | **0 元起步** | 有实例费 | 有起步费用 | 按独享规格计费 |
| 计费方式 | 按实际用量付费 | **实例费 + 按实际用量付费** | **起步费 + 按实际用量付费** | 按实例规格和实际用量计费 |
| 访问入口 | 平台分配入口 | 独立入口能力 | 独立实例入口 | 独享入口能力 |
| 架构形态 | 新架构，平台分配入口 | 新架构，独立入口能力 | 原 Serverless 旧架构 | 独享实例架构 |
| 插件体系 | 支持平台提供的插件体系，**不支持自定义插件**；具体可用插件以产品控制台展示为准 | 支持平台提供的插件体系，**不支持自定义插件**；具体可用插件以产品控制台展示为准 | **不支持插件体系** | **支持完整插件和高级治理能力** |
| 自定义域名 | **不支持关联到标准版实例** | 支持 | 支持 | 支持 |
| 证书/TLS/HTTP/2 | **不支持用户自定义配置**，平台默认 HTTPS 入口保持可用 | 支持用户配置 | 支持用户配置 | 支持 |
| 默认 QPS 限制 | **50 QPS** | **500 QPS** | **以原版本规格为准** | **以实例规格为准** |
| 服务等级 | **99.9%** | **99.95%** | **99.95%** | **99.99%** |
| AI 核心能力 | 支持 LLM API、Agent API、MCP Server、智能路由、AI 安全、Token 用量看板等核心能力 | 支持标准版核心能力，并提供更完整的生产级配置能力 | 支持 LLM API、Agent API、MCP Server、智能路由、AI 安全、Token 用量看板等核心能力 | 支持完整网关能力 |
| 高级治理能力 | **部分高级能力不开放** | 支持更多企业级能力 | 支持原版本治理能力 | 支持完整高级治理能力 |

来源：[官方｜ai-gateway-capacity-description]

**Serverless 标准版的 5 条使用限制（官方逐条，SA 避坑重点）**
1. 「默认实例级 QPS 上限为 **50**。」
2. 「**不支持**关联用户自定义域名。」
3. 「**不支持**用户自定义证书、TLS policy 或 HTTP/2 配置。」
4. 「**不提供独立公网入口**。」
5. 「标准版**后续规划**支持一键升级为企业版，无需资源迁移；具体支持时间和操作入口请以产品控制台展示为准。」
[官方原文｜ai-gateway-capacity-description]

**Serverless 标准版官方 FAQ 两条**
- 「Serverless 标准版是否适合生产业务？」→「适合**低流量、低成本、可接受平台分配入口**的轻量业务。如果需要自定义域名、独立访问入口、更高服务等级或超过默认 QPS 上限，建议选择 Serverless 企业版。」
- 「Serverless 标准版是否支持 HTTPS？」→「支持**平台默认 HTTPS 入口**。标准版**不支持**用户自定义证书、TLS policy 或 HTTP/2 配置。」
[官方原文｜ai-gateway-capacity-description]

**Serverless 企业版适用场景（官方 4 条）**：已经承载正式生产流量的 AI API、Agent API 或 MCP Server／需要稳定独立访问入口的企业业务／SaaS 或 ISV 需要向下游客户提供稳定 API 入口／需要自定义域名、证书、TLS policy 或 HTTP/2 配置的业务。
**主要优势 5 条**：生产级实例形态、独立入口能力、更高服务等级（99.95%）、自定义域名能力、传输加密配置（证书 / TLS policy / HTTP/2）。
**使用建议原文**：「如果您的业务已经进入生产阶段，或需要自定义域名、独立访问入口、更高服务等级、**超过标准版默认 QPS 上限**的能力，建议选择 Serverless 企业版。」[官方原文｜ai-gateway-capacity-description]

**实例型独享版适用场景（官方 5 条）**：大型企业核心生产系统／需要 **99.99%** 服务等级的业务／长期高并发或突发流量较高的业务／需要更完整的插件、安全、观测、治理能力／对资源隔离、合规、审计或网络控制有更高要求的业务。
**主要优势 4 条**：更强资源隔离能力（适合核心生产和高合规场景）、最高服务等级（99.99%）、完整网关能力（适合复杂插件、安全、观测和治理需求）、更稳定的性能预期（适合高吞吐、强隔离和大型客户场景）。[官方｜ai-gateway-capacity-description]

### 2.4 容量规格：专享实例版 QPS 与客户端连接数

> 页面导语：「AI 网关按实例规格提供不同的 QPS、客户端连接数上限，并对各类资源设置配额限制。本文列出**专享实例版**的容量规格，以及 Serverless 版和专享实例版的资源配额，供购买或升级实例时参考。」
> 表前限定语：「以下为**专享实例版**各实例规格对应的 QPS 和客户端连接数上限」
> [官方原文｜capacity-description]

| 实例规格 | QPS | 客户端连接数 | 限定条件 | 来源 slug |
|---|---|---|---|---|
| aigw.small.x1 | 1500 | 20000 | 专享实例版 | capacity-description |
| aigw.small.x2 | 3000 | 40000 | 专享实例版 | capacity-description |
| aigw.small.x4 | 6000 | 80000 | 专享实例版 | capacity-description |
| aigw.medium.x1 | 12000 | 160000 | 专享实例版 | capacity-description |
| aigw.medium.x2 | 24000 | 320000 | 专享实例版 | capacity-description |
| aigw.medium.x3 | 36000 | 480000 | 专享实例版 | capacity-description |
| aigw.large.x1 | 48000 | 640000 | 专享实例版 | capacity-description |
| aigw.large.x2 | 96000 | 1280000 | 专享实例版 | capacity-description |
| aigw.large.x3 | 144000 | 1920000 | 专享实例版 | capacity-description |
| aigw.large.x4 | 192000 | 2560000 | 专享实例版 | capacity-description |

[推断] 观察上表：QPS 与客户端连接数在全部 10 档上恒为 **1 : 13.33**（20000/1500 = 40000/3000 = … = 2560000/192000）；Small 档 x1→x2→x4 为 1500→3000→6000（×2、×2），Medium 档 x1→x2→x3 为 12000→24000→36000（等差 12000），Large 档 x1→x4 为 48000→96000→144000→192000（等差 48000）。→ 后缀 `xN` 表示**档位内的倍数 / 等差扩容**，`small / medium / large` 表示**基础容量台阶**（1500 / 12000 / 48000 QPS 起）。这是从数字推出的规律，官方未文字说明。

[文档未说明] 🔴 这里的 **QPS 口径**：是「HTTP 请求 QPS」还是「AI 请求 QPS」、是否区分流式 / 非流式、是否与 token 吞吐量挂钩 —— capacity-description 只写「QPS」两字，无定义。**这是 SA 做 LLM 容量规划最大的空白**：LLM 单请求耗时可达数十秒，从 QPS 折算并发连接的实际余量，文档没给方法。
[文档未说明] 「客户端连接数」是并发长连接上限还是累计连接数、是否含 WebSocket —— 查无。
[文档未说明] 各规格对应的**节点数、单节点 CPU / 内存、Pod 规格** —— 查无。create-a-gateway-instance 的压测表间接暴露「aigw.medium.x1 可跑单节点或 4 节点」，说明节点数可变，但节点数如何决定、是否可配、与 QPS 上限的关系均未写。
[文档未说明] 超出规格 QPS 后的行为（限流？降级？返回什么错误码？）—— 查无。
[文档未说明] 是否支持规格**在线升配 / 降配**、变配是否需重启、变配耗时 —— 查无（capacity-description 导语说「供购买或**升级**实例时参考」，暗示可升级，但无操作文档）。
[文档未说明] Serverless 三形态的**客户端连接数上限** —— capacity-description 只给专享实例版；ai-gateway-capacity-description 只给 QPS。查无。
[文档未说明] Serverless 的**弹性上限**（能弹到多大 QPS、自动扩容 Unit 数上限）—— 查无（发布记录 2026-05 只提到「支持对连接数、自动扩容 Unit 数的监控」）。

### 2.5 Serverless 的 QPS 与服务等级（跨页汇总，限定条件绑定）

| 实例类型 | 默认 QPS 限制 | 服务等级 | 限定条件 / 原文限定词 | 来源 slug |
|---|---|---|---|---|
| Serverless 标准版 | **50 QPS** | **99.9%** | 「**默认**实例级 QPS 上限为 50」；栏位名本身即「**默认** QPS 限制」→ 能否申请提高，文档未说明 | ai-gateway-capacity-description |
| Serverless 企业版 | **500 QPS** | **99.95%** | 「更高服务等级：服务等级为 99.95%」 | ai-gateway-capacity-description |
| Serverless（旧） | **「以原版本规格为准」** | **99.95%** | QPS 数字被推给「原版本规格」→ **文档级空白**，SA 必须去控制台实例详情核验 | ai-gateway-capacity-description |
| 实例型独享版（专享实例版） | **「以实例规格为准」**（具体值见 §2.4：1500~192000） | **99.99%** | 「最高服务等级：服务等级为 99.99%」 | ai-gateway-capacity-description｜capacity-description |
| AI 网关（**无实例类型限定**） | —— | **99.99%** | product-comparison 的 SLA 行**未带任何限定** | product-comparison |

[官方矛盾] SLA 口径：
- 原文 A（分档、带限定）：「服务等级｜99.9%（Serverless 标准版）｜99.95%（Serverless 企业版）｜99.95%（Serverless（旧））｜99.99%（实例型独享版）」[ai-gateway-capacity-description]
- 原文 B（单一值、无限定）：对比表「稳定性 / SLA」行：AI 网关 =「**99.99%**」，Higress开源版 =「不支持」[product-comparison]
- [推断] 由 A 的分档 + B 位于「AI 网关 vs 开源版」的宏观对比语境，推出 B 是拿**最高档（实例型独享版）**代表整个产品。**按契约 §3.5 不裁决**：SA 对客承诺 SLA 必须按 A 的分档报，不能用 B。
- 🔴 补充（把数字推走的原文，照实记录）：ai-gateway-capacity-description 全页 **2 次**把最终口径推走 ——
  > 「具体可购买的实例类型、功能范围、计费项、价格、**服务等级**和可用地域，请以产品控制台、价格页和**服务等级协议页面**展示为准。」
  > 「具体功能、规格、计费项、价格、**服务等级**和可购买范围，请以产品控制台、官网价格页和**服务等级协议页面**为准。」
  → **文档级空白**：本页的 99.9% / 99.95% / 99.99% 都**不是 SLA 协议正文**，赔付档位与计算方式归 W2。

[官方矛盾] Serverless 是否处于**公测 + 免费**状态：
- 原文 A（2026-07 发布记录）：「**多租 Serverless 正式开启公测**，提供企业版与标准版，**最低 0 起步**，**公测期间免费试用**。」[new-feature-release-notes-ai-gateway]
- 原文 B（网关类型页，同一快照日 2026-09-21）：Serverless 标准版「**0 元起步**，**按量付费**」；企业版「**有实例费**」「**实例费 + 按实际用量付费**」—— **全页无「公测」二字、无「免费」二字** [ai-gateway-capacity-description]
- **时间边界**（🔴 **2026-09-21 主控修正**：本条原写「公测结束时间、计费切换均未说明 → 文档级空白」，经独立评审 R1 回源判定为 **D3「空白被填」**——答案在 `ai-gateway-commercialization-announcement`，该页在 W2 分片而非 W1 分片，属**跨分片盲区**）：公测起点 **2026-07**（发布记录口径）；**公测 2026-08-31 结束、2026-09-01 起正式商业化并开始计费、存量公测实例自动转为商业化实例（配置与业务数据无需迁移）、不再需要的实例须在 9-01 前删除以免产生费用** `[官方原文｜ai-gateway-commercialization-announcement]`。**仍是真空白的一项**：公测期「网关自身免费」与企业版「实例费 0.245 元/小时」并存，**公测期企业版实例费究竟是否收取，两页均未说明**（`[官方矛盾]`，见 [§3.8](aliyun-ai-gateway-billing.md)）。SA 报价时不得把「免费」写进方案，必须走购买页核验。
- 另一时间锚点：Serverless 版本本身最早于 **2025-09** 发布（「新商品｜AI 网关发布 Serverless 版本，**最高节省 90%成本**」[new-feature-release-notes-ai-gateway]）。「最高节省 90%成本」的**对比基准文档未说明**。

### 2.6 全局配额（Region 级）

| 配额项 | 配额 | 限定条件 | 来源 slug |
|---|---|---|---|
| 单Region实例数量 | **100** | Region 级全局配额 | capacity-description |
| 单Region最大消费者组数 | **1000** | Region 级全局配额 | capacity-description |
| 单消费者组内消费者数 | **500** | 消费者组级 | capacity-description |
| 单Region最大消费者数 | **100000** | Region 级全局配额 | capacity-description |

> 官方定义：「AI 网关对各类资源设置了配额上限，分为**全局配额（Region 级别）**和**实例配额（按实例版本和规格档位区分）**。」[官方原文｜capacity-description]

[文档未说明] 全局配额是否区分实例类型（Serverless 实例是否也计入「单Region实例数量 100」）—— 查无。
[文档未说明] 「单消费者组内消费者数 500」×「单Region最大消费者组数 1000」＝50 万，远大于「单Region最大消费者数 100000」，三者如何联合约束 —— 文档未说明计算关系。

### 2.7 实例配额（逐规格，13 列全量照抄）

原始表格为 HTML `<table>`，双行表头：第一行分组 `Serverless` / `Small` / `Medium` / `Large`，第二行为具体规格名。**MCP Server数 ~ 消费者配额规则数 共 7 行每行 13 个值，与表头逐列对齐**；**最后 3 行（K8s服务来源数、安装的插件数、上传自定义插件数）每行只有 6 个值**，属官方的档位级合并单元格渲染（还原方式见该三行下方说明）。

| 配额项 | Serverless（旧） | Serverless（标准版） | Serverless（企业版） | aigw.small.x1 | apigw.small.x2 | apigw.small.x4 | apigw.medium.x1 | apigw.medium.x2 | apigw.medium.x3 | apigw.large.x1 | apigw.large.x2 | apigw.large.x3 | apigw.large.x4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MCP Server数 | 100 | 20 | 100 | 500 | 600 | 800 | 1000 | 1200 | 1600 | 2000 | 2200 | 2400 | 2600 |
| 在线路由总数（含Model API路由、Agent API路由） | 2500 | 200 | 2500 | 5000 | 6000 | 7000 | 7500 | 8000 | 9000 | 10000 | 12000 | 14000 | 16000 |
| 发布域名数 | 100 | 20 | 100 | 200 | 300 | 400 | 500 | 600 | 800 | 1000 | 1200 | 1400 | 1600 |
| 服务数 | 200 | 50 | 200 | 800 | 1200 | 1600 | 2000 | 2500 | 3000 | 4000 | 4500 | 5000 | 6000 |
| 消费者授权规则数 | 500 | 100 | 500 | 2000 | 4000 | 6000 | 8000 | 12000 | 16000 | 20000 | 27500 | 35000 | 42500 |
| 消费者数量 | 500 | 100 | 500 | 2000 | 4000 | 6000 | 8000 | 12000 | 16000 | 20000 | 27500 | 35000 | 42500 |
| 消费者配额规则数 | 500 | 100 | 500 | 2000 | 4000 | 6000 | 8000 | 12000 | 16000 | 20000 | 27500 | 35000 | 42500 |
| K8s服务来源数 ※ | 1 | N/A | 1 | 3（Small 档） | 5（Medium 档） | 5（Large 档） | — | — | — | — | — | — | — |
| 安装的插件数 ※ | N/A | 5 | 5 | 10（Small 档） | 20（Medium 档） | 30（Large 档） | — | — | — | — | — | — | — |
| 上传自定义插件数 ※ | N/A | N/A | N/A | 20（Small 档） | 50（Medium 档） | 80（Large 档） | — | — | — | — | — | — | — |

来源：[官方｜capacity-description]（规格名 `aigw` / `apigw` 前缀不一致见 §2.1 [官方矛盾]）

**※ 最后 3 行的还原说明（必须随数字一起读）**
- 原始 HTML 里这 3 行各只有 **6 个值单元格**，而表头有 **13 个规格列**。前 3 个值对应 Serverless（旧）/（标准版）/（企业版），后 3 个值对应 Small / Medium / Large **三个档位**（档位内各规格共享同一值）。
- [推断] 由「6 值 = 3 Serverless 列 + 3 档位」的整齐对应关系，以及 capacity-description 正文「专享实例版按规格名称前缀分为 Small、Medium、Large **三个档位**。不同版本和**档位**的实例配额如下」推出这 3 项是**档位级**而非**规格级**配额。
- ⚠️ 官方**没有在表内明示**哪一列对应哪一档位，也无 colspan 属性残留。SA 引用这 3 行时应说明「按档位，非按具体规格」。

**配额白名单的官方警告（原文照抄）**
> 「说明：如通过特殊白名单或特殊配置突破上述配额限制，相关使用**不属于标准配额范围**，阿里云**不对该等使用场景作出服务等级协议（SLA）承诺**。」[官方原文｜capacity-description]

→ [推断] 由该警告 + §2.5 的 SLA 分档推出：**提额 ＝ 放弃 SLA 承诺**。SA 在「配额不够就申请白名单」的方案里必须同步告知 SLA 失效风险 —— 这是商务与合规双重争点。

**Serverless 标准版配额极小的项（SA 避坑）**：MCP Server数 **20**、在线路由总数 **200**、发布域名数 **20**、服务数 **50**、消费者数量 / 消费者授权规则数 / 消费者配额规则数 各 **100**、安装的插件数 **5**、K8s服务来源数 **N/A**、上传自定义插件数 **N/A**。[官方｜capacity-description]
[推断] 由标准版「K8s服务来源数 = N/A」+「上传自定义插件数 = N/A」+ ai-gateway-capacity-description「标准版不支持自定义插件」推出：**标准版不能接容器服务来源（K8s / ACK / ACS）**，需要 ACK 后端的客户必须选企业版或独享版。

[官方矛盾] 单实例可关联的容器集群 / K8s 服务来源数：
- 原文 A（无限定）：「**容器服务**：支持运行在阿里云ACK或ACS集群上的服务，**单个AI网关实例最多可关联3个容器集群**。」[what-is-an-ai-gateway]
- 原文 B（按规格）：「K8s服务来源数｜Serverless（旧）=**1**｜Serverless（标准版）=**N/A**｜Serverless（企业版）=**1**｜Small=**3**｜Medium=**5**｜Large=**5**」[capacity-description]
- [推断] 由 B 的分档推出 A 的「最多 3 个」只对 **Small 档专享实例**成立；Medium / Large 是 **5**，Serverless（旧 / 企业版）只有 **1**，标准版是 **N/A（不支持）**。**不裁决**，SA 对客应以 B 的分档为准，A 是过度概括。

**交叉验证（非矛盾）**：capacity-description 的「安装的插件数」标准版 / 企业版 = **5**、旧版 = **N/A**，与 ai-gateway-capacity-description「标准版 / 企业版支持平台插件体系但不支持自定义插件」「Serverless（旧）不支持插件体系」一致；「上传自定义插件数」标准版 / 企业版均为 **N/A**，也与「不支持自定义插件」一致 → 该结论稳。

[文档未说明] 配额表**没有**下列 SA 高频被问的对象：API 产品数、产品分类数、**证书数**、消费者凭证 / 密钥数、AI 缓存条目数、**Model API 数**（只有「在线路由总数」）、MCP 工具数（只有 MCP Server 数）、虚拟 MCP Server 数、日志投递 Project / Logstore 数、**安全组授权条数**。
[文档未说明] 「在线路由总数」里 Model API 路由与 Agent API 路由是否 1:1 计数、一条 Model API 含多条自定义路由时如何计数 —— 查无。
[文档未说明] 「发布域名数」与「域名」管理页里的域名条目是否同一计数口径 —— 查无。
[文档未说明] 配额提升（白名单）的**申请入口、审批时效、可提升倍数上限** —— 只说了提额会失去 SLA 承诺，未说怎么办。
[文档未说明] 「资源配额扩大，适配用户的更大使用规模」（2026-03 优化项）具体扩大了哪些项、从多少到多少 —— 发布记录只有这一句，无数字；且 capacity-description 的配额表**未标版本 / 生效日期**，无法判断当前数字是扩额前还是扩额后。
[文档未说明] 「安装的插件数 5」是**同时启用**上限还是**累计安装**上限 —— 查无（归 W6）。

### 2.8 消费者授权额度计算口径（官方专节，SA 报价必用）

> 「『消费者数量』和『消费者授权规则数』是**两个独立的配额项，分别统计、分别校验**。」[官方原文｜capacity-description]

| 配额项 | 官方计算口径（原文） |
|---|---|
| **消费者数量** | 「当前网关授权关系中，**直接授权的消费者**与**通过消费者组授权引用的消费者**合并**去重**后的数量。同一个消费者被多条规则或多个消费者组引用时**只计1次**；**消费者组为空时不增加消费者数量**。」 |
| **消费者授权规则数** | 「当前网关**保留的消费者授权规则条数**。直接授权一条计1条，消费者组授权一条也计1条；**无论消费者组包含多少消费者或是否为空，都只计1条**。」 |

- 校验方式：「两项用量**分别**与对应的配额上限比较：消费者数量不超过消费者数量上限，**且**消费者授权规则数不超过消费者授权规则数上限。」
- 白名单影响：「通过白名单或特殊配置提高的配额**只改变可用上限，不改变上述计算口径**。」
- 补充原文：「各实例规格的消费者数量上限和消费者授权规则数上限分别列于上表；**其他规格以实例配额表为准**。」
来源：[官方原文｜capacity-description]

[推断] 由「消费者组授权无论组内多少消费者都只计 1 条规则」+「消费者数量按去重计」推出：**用消费者组做批量授权可显著节省「消费者授权规则数」配额**（1000 个消费者通过 1 个组授权 = 1 条规则 + 1000 个消费者计数）。这是 FinOps / 多租户方案设计的直接杠杆，落地归 W3 / W4。
[文档未说明] 🔴 第三项配额「**消费者配额规则数**」（表中与消费者数量同值）的**计算口径** —— 官方专节只解释了「消费者数量」和「消费者授权规则数」两项，第三项无口径说明。明显缺口（FinOps 相关，归 W3）。

### 2.9 开服地域与 Region ID 对照

> 页面前置约束原文：「地域是指物理的数据中心，**资源创建成功后不能更换地域**。」[官方原文｜supported-regions]
> create-a-gateway-instance 的「地域」配置项带同一条 **重要** 级提示：「资源创建成功后，不能更换地域。」[官方｜create-a-gateway-instance]

**公共云（15 个地域）**

| 地域分组 | 地域名称 | Region ID | 来源 slug |
|---|---|---|---|
| 中国 | 华北1（青岛） | cn-qingdao | supported-regions |
| 中国 | 华北２（北京） | cn-beijing | supported-regions |
| 中国 | 华北3（张家口） | cn-zhangjiakou | supported-regions |
| 中国 | 华北６（乌兰察布） | cn-wulanchabu | supported-regions |
| 中国 | 华东１（杭州） | cn-hangzhou | supported-regions |
| 中国 | 华东２（上海） | cn-shanghai | supported-regions |
| 中国 | 华南１（深圳） | cn-shenzhen | supported-regions |
| 中国 | 西南1（成都） | cn-chengdu | supported-regions |
| 中国 | 中国香港 | cn-hongkong | supported-regions |
| 亚太 | 日本（东京） | ap-northeast-1 | supported-regions |
| 亚太 | 新加坡 | ap-southeast-1 | supported-regions |
| 亚太 | 印度尼西亚（雅加达） | ap-southeast-5 | supported-regions |
| 欧洲与美国 | 美国（硅谷） | us-west-1 | supported-regions |
| 欧洲与美国 | 美国（弗吉尼亚） | us-east-1 | supported-regions |
| 欧洲与美国 | 德国（法兰克福） | eu-central-1 | supported-regions |

（地域名称中的全角数字「华北２」「华北６」「华东１」「华东２」「华南１」为原文写法 [原文如此]；同表内「华北1」「华北3」「西南1」用半角 —— 官方自身不一致）

**金融云（1 个地域）**

| 地域分组 | 地域名称 | Region ID | 来源 slug |
|---|---|---|---|
| 亚太 | 华东2（上海）金融云 | cn-shanghai-finance-1 | supported-regions |

[官方矛盾] 开服地域清单与发布记录的「开服」条目不一致：

| 发布记录声称的开服 | 时间 | supported-regions 表里是否存在 |
|---|---|---|
| 「开服｜新增**青岛**地域」 | 2025-07 | ✅ 存在（cn-qingdao） |
| 「开服｜新增**韩国**地域」 | 2025-08 | ❌ **不存在**（表中无任何韩国 / 首尔 / ap-northeast-2 条目） |
| 「开服｜新增**马来西亚**地域」 | 2025-12 | ❌ **不存在**（表中无马来西亚 / 吉隆坡 / ap-southeast-3 条目） |
| 「开服｜新增**亚特兰大**地域」 | 2026-03 | ❌ **不存在**（「欧洲与美国」只有硅谷 us-west-1、弗吉尼亚 us-east-1、法兰克福 eu-central-1） |

- 原文 A：「开服｜新增韩国地域。」（2025-08）／「开服｜新增马来西亚地域。」（2025-12）／「开服｜新增亚特兰大地域。」（2026-03）[new-feature-release-notes-ai-gateway]
- 原文 B：supported-regions 公共云表仅 15 行，止于 `eu-central-1`，无上述 3 个地域 [supported-regions]
- **不裁决**。可能解释均为推测、不作事实：supported-regions 页未同步更新，或这 3 个地域仅对特定实例类型 / 特定账号开放。
- 🔴 **SA 影响**：客户在韩国 / 马来西亚 / 亚特兰大落地的方案，**必须先在购买页实测该地域是否可选**，既不能只引用 supported-regions 表，也不能只引用发布记录。

[文档未说明] 各地域支持的**实例类型差异**（Serverless 标准版 / 企业版是否全地域可用？）—— supported-regions 只列地域，不做能力矩阵。已知唯一的地域级能力限制是 Gzip 硬件加速的 7 个地域（§2.11.2）。
[文档未说明] 金融云地域支持的实例类型、规格档位、是否有能力裁剪 —— 查无。
[文档未说明] 各地域的可用区数量、是否都支持多可用区部署 —— 查无（create-a-gateway-instance 只说「自动分配 2 个可用区」）。
[文档未说明] 是否存在政务云 / 其他专有云地域 —— 查无。

### 2.10 引擎版本演进（20 个版本全量）

| 版本号 | 发布时间 | 引入 / 修复的能力（照抄要点） | 来源 slug |
|---|---|---|---|
| 2.1.23 | 2026-09-03 | FinOps 支持消费者组能力；FinOps 兼容后端服务返回时存在的两种 cache 语义（OpenAI 和 Claude 格式），修复 cache 多算问题 | engine-version-description |
| 2.1.22 | 2026-08-13 | 优化多模态长耗时场景下的内存资源使用；优化开启 WAF 时的内存资源使用 | engine-version-description |
| 2.1.21 | 2026-07-27 | 修复 FinOps 在非标准断开连接导致计量丢失和消费者未配置 credit 时 FinOps 默认阈值为 0 的问题；修复 Wasm 插件性能问题；修复 2.1.20 版本问题，导致 Ingress 接入方式 basic_auth 能力异常的问题 | engine-version-description |
| 2.1.20 | 2026-07-07 | finopts[原文如此] 支持自定义 credit 功能和周期功能；**新增了请求/响应采集能力，替代 Lua 插件打印请求/响应日志功能** | engine-version-description |
| 2.1.19 | 2026-06-05 | 支持 finopts[原文如此] 功能；修复了特殊场景下 fallback 导致异常问题 | engine-version-description |
| 2.1.18 | 2026-05-14 | 修复特殊场景下网关重启和升级失败的问题；修复特殊场景下**域名级黑白名单不生效**的问题；修复特殊场景下 **MCP Tools 丢失**的问题 | engine-version-description |
| 2.1.17 | 2026-03-26 | **熔断策略支持滑动窗口统计能力**；**访问日志过滤器支持域名采样规则和默认采样率**；修复特殊场景下 fallback 请求 body 丢失；修复特殊场景下用户自定义证书过期时间为空 | engine-version-description |
| 2.1.16 | 2026-02-04 | WASM 过滤器请求数据缓冲区处理 bug 修复；AI 功能内存优化；**引入全局请求速率限制机制**（可通过运行时配置或 Wasm 模块动态控制单个 I/O 循环中所有连接的最大请求数量）；Istio 指标中增加租户 ID 信息 | engine-version-description |
| 2.1.15 | 2025-12-25 | 支持 **cluster header 模式的路由**；修改 pilot agent 和 **envoy** 之间的 gRPC keepalive 时间避免超时关闭 xds 连接；**SDS 超时时间默认值增加到 300s**；增加非 recover 场景下的 wasm rebuild 限制（**最多同时存在 2 个 vm**）；支持对接 nacos mcp 时配置多个域名；修复 redis 功能在更新服务配置后减轻[原文如此]失败的问题；WAF 功能增强 | engine-version-description |
| 2.1.14 | 2025-12-1 | 优化网关过载处理逻辑；支持 Wasm 插件中配置 Redis 异步客户端的 buffer 配置；提升网关中访问 Redis 的功能稳定性；**MCP 直接代理场景支持 MCP 协议转换能力** | engine-version-description |
| 2.1.13 | 2025-10-24 | **WAF 接入支持远程 xagent 模式**；优化插件 rebuild 逻辑；优化 K8s 服务来源场景下 namespace 数量过多可能导致的初始化问题；优化 K8s 服务来源场景下**密钥轮转时可能出现 503** 的问题 | engine-version-description |
| 2.1.12 | 2025-09-19 | 修复 fallback 请求日志字段显示不正确；优化整体内存使用；**优化大量域名下的配置生效速度** | engine-version-description |
| 2.1.11 | 2025-08-21 | **支持对接 nacos 实现 mcp 工具组装功能**；**支持对接用户自己的 KMS 实例存储加密凭证** | engine-version-description |
| 2.1.10 | 2025-08-13 | **支持被动健康检查**；**支持对 LLM API 配置流式场景下的首字节超时**；修复上个版本引入的兼容性问题 | engine-version-description |
| 2.1.9 | 2025-08-11 | 优化路由配置推送机制（防止配置错误引起路由失败）；优化配置频繁更新时 Wasm 插件内存使用；**优化 Lua 插件安全性，禁用 loadlib 等高危操作**；修复 Waf 集成模块在极端场景下异常退出 | engine-version-description |
| 2.1.8 | 2025-07-08 | 优化自动扩容能力和开启大量插件时的资源开销 | engine-version-description |
| 2.1.7 | 2025-07-03 | 新增 **websocket 无损下线**功能；支持 **Open Kruise Game** 的优雅下线功能 | engine-version-description |
| 2.1.6 | 2025-06-12 | **支持 McpServer 代理功能** | engine-version-description |
| 2.1.5 | 2025-05-29 | **支持 REST API To MCP 功能**；优化 Ingress 中限流配置的生效范围 | engine-version-description |
| 2.1.4 | 2025-05-08 | **支持 MCP 能力** | engine-version-description |

来源：[官方｜engine-version-description]

**MCP 能力演进主线（判断客户所需最低引擎版本用）**

| 能力 | 首次声明版本 | 发布时间 |
|---|---|---|
| MCP 能力（首次） | 2.1.4 | 2025-05-08 |
| REST API To MCP | 2.1.5 | 2025-05-29 |
| McpServer 代理 | 2.1.6 | 2025-06-12 |
| 对接 nacos 的 MCP 工具组装 | 2.1.11 | 2025-08-21 |
| MCP 直接代理场景的 MCP 协议转换 | 2.1.14 | 2025-12-1 |
| 对接 nacos mcp 时配置多个域名 | 2.1.15 | 2025-12-25 |

[推断] 上表「首次声明版本」由「该版本条目首次声明支持该能力」推出；官方**未使用**「需 ≥ x.x.x」句式（唯一例外见下）。

**引擎版本依赖的唯一一处显式硬约束（来自发布记录，非引擎版本页）**
> 「Token 限流策略支持依据引擎版本过滤限流模式，**每周/每月限流（TokenPerWeek/TokenPerMonth/RequestPerWeek/RequestPerMonth）需引擎版本 ≥ 2.1.15**」（2026-03 优化项）[官方原文｜new-feature-release-notes-ai-gateway]

→ [推断] 由 engine-version-description 的 2.1.15 条目（2025-12-25）+ 上述发布记录推出：2.1.15 是周 / 月级 Token 限流的门槛版本。**engine-version-description 页面本身没有记录这条依赖** —— 两页信息不对称，SA 查版本能力必须两页都看。

[文档未说明] 🔴 **引擎是否基于 Higress / Envoy**：engine-version-description **通篇没有「Higress」字样**；「envoy」只出现在 2.1.15「修改 pilot agent 和 envoy 之间的 gRPC keepalive 时间」，另有 2.1.16「**Istio** 指标中增加租户 ID 信息」；发布记录 2026-03 的专属告警指标名为 `AIGatewayEnvoyCpuUsageRate` / `AIGatewayEnvoyMemoryUsageRate` / `AIGatewayEnvoyPluginCrash`，2026-01 提到「在 Dify 的模型供应商中提供官方 **Higress** 插件」。→ [推断] 由 envoy + Istio + pilot agent + Wasm 插件体系推出引擎为 Envoy 系（xDS 控制面），但**「AI 网关引擎 = Higress」这一等式在我的快照里没有明文**；product-comparison 只说 Higress 开源版「具备 AI 网关的开源能力」，未说 AI 网关基于 Higress。
[文档未说明] 2.1.4 之前的版本（2.0.x / 1.x）历史 —— 表止于 2.1.4（2025-05-08）。
[文档未说明] 🔴 引擎版本的**升级方式**（自动 / 手动）、是否需重启、是否影响在途请求、能否回滚、能否指定版本、各实例类型可升级的版本范围 —— 全部查无。运维高危空白。仅有间接线索：2.1.18 修复过「特殊场景下网关重启和升级失败的问题」，2.1.21 修复过「2.1.20 版本问题」，2.1.10 提到「修复上个版本引入的兼容性问题」→ 说明升级 / 新版确有翻车先例。
[文档未说明] 版本发布节奏承诺 —— [推断] 由 2.1.4（2025-05-08）→ 2.1.23（2026-09-03）共 20 版跨约 16 个月推出平均约 25 天一版；期间 2025-12-1→2025-12-25、2026-03-26→2026-05-14 有明显间隔。官方无节奏承诺。
[文档未说明] Serverless 标准版 / 企业版 / 旧版能否使用全部引擎版本、是否有版本裁剪 —— 查无。
[文档未说明] `finopts` 与 `FinOps` 是否同一能力 —— [推断] 由 2.1.19「支持 finopts 功能」→ 2.1.20「finopts 支持自定义 credit 功能和周期功能」→ 2.1.21/2.1.22/2.1.23 改写为「FinOps」，且发布记录 2026-05/06/07 全用「FinOps」，推出 `finopts` 是 `FinOps` 的笔误 [原文如此]。

### 2.11 实例创建与网络底座

#### 2.11.1 创建实例：配置项与决策含义

| 配置项 | 官方说明要点 | 决策含义 | 来源 slug |
|---|---|---|---|
| 商品类型 | 专享实例（按量付费）／专享实例（包年包月）／Serverless（按量付费） | 命名口径冲突见 §2.1 | create-a-gateway-instance |
| 地域 | 「资源创建成功后，**不能更换地域**」（**重要**级提示） | 一次性决策，选错只能重建 | create-a-gateway-instance｜supported-regions |
| 网关名称 | 「推荐用环境或环境加业务领域命名，例如test、order-prod等，**最大长度为64个字符**」 | 64 字符上限 | create-a-gateway-instance |
| 网关规格 | 「根据实际需求选择节点规格…**Serverless版本无网关规格**」 | Serverless 无规格可选 → 其容量只能按 §2.5 的默认 QPS 判断 | create-a-gateway-instance |
| 资源组 | 支持默认资源组或已有资源组，可单击「创建资源组」 | 「以组为单元进行权限管理、资源部署、资源监控」 | create-a-gateway-instance |
| 网络访问类型 | **公网**／**私网**／**公网+私网** 三种。公网：「公网访问网关时，将会产生相应的公网流量费用，公网流量将基于**云数据传输CDT**进行统一计费和出账，采用 **BGP（多线）模式**」；私网：「**私网无流量费用**」；公网+私网：公网侧同公网计费，「访问私网无流量费用」 | 🔴 **连带计费**：选公网即引入 CDT 计费项，不在网关账单内（单价本页未给） | create-a-gateway-instance |
| 专有网络 | 「网关所在的VPC与**服务所在的VPC需保持一致**」；「在选择VPC时，会显示是否存在容器或Nacos集群，避免误选VPC」 | 🔴 后端服务跨 VPC 时需先做 VPC 打通，这是方案设计前置条件 | create-a-gateway-instance |
| 可用区选择 | **自动分配**：「选择一个交换机，系统会**自动分配2个可用区**部署网关节点」；**手动选择**：「手动选择部署网关节点的可用区和交换机」 | 默认即 2 AZ 部署（对应 product-comparison「多可用区部署｜支持」） | create-a-gateway-instance |
| 交换机 | 选择网关实例运行的交换机，可前往专有网络管理控制台创建 | —— | create-a-gateway-instance |
| 日志服务 | 选中「**使用日志服务（SLS）**」→「开通日志服务SLS并开启网关日志投递功能，提供日志分析和仪表盘」 | 🔴 **连带开通 + 连带计费**（SLS 独立计费，本页未给单价）；「日志服务无限制」（指创建后仍可开） | create-a-gateway-instance |
| 服务关联角色 | 「**已自动创建**。允许AI网关访问其他云产品等服务」 | 无需手动建 SLR；细节归 W4 | create-a-gateway-instance |

**创建耗时**：「网关实例创建过程**预计需要1～5分钟**时间。」成功判据：实例页面「**运行状态** 为 **运行中**」。[官方原文｜create-a-gateway-instance]

[文档未说明] 购买页是否有「安全组」配置项 —— 见 §2.11.4 [官方矛盾]。
[文档未说明] 公网入口能否**后开**（创建时选私网、之后加公网）：发布记录 2026-04 只有「支持**开通公网后关闭公网**」，反向未提；标准版明确「不提供独立公网入口」。
[文档未说明] 网关实例的**默认监听端口清单** —— view-gateway-instance-details 说「网络信息」区域可查看「**端口**、VPC 和**安全组**」，但未列端口值。
[文档未说明] 网关名称的字符集限制（只给了 64 字符长度上限）—— 查无。

#### 2.11.2 Gzip 硬件加速（有强决策含义的创建期开关）

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 定义 | 「通过专用硬件设备来实现数据的快速压缩和解压缩技术。通过将 Gzip 格式的解压缩任务**从 CPU 卸载到专用硬件设备**上，显著提升处理效率并降低 CPU 负载」 | create-a-gateway-instance |
| 🔴 开启时机 | 「开启Gzip硬件加速**只能在创建网关实例时进行开启，不支持创建后开启**」；「若在购买时未勾选**启用 Gzip 硬件加速**，则无法开启此配置」 | create-a-gateway-instance |
| 🔴 实例类型限制 | 「**Serverless版不支持Gzip硬件加速**」（未区分标准版 / 企业版 / 旧版） | create-a-gateway-instance |
| 🔴 地域限制 | 「Gzip硬件加速支持的地域为**杭州、北京、上海、深圳、乌兰察布、中国香港和新加坡**」（7 个）；「目前在支持的地域中，**存在部分可用区不支持的情况，具体以产品购买页为准**」 | create-a-gateway-instance |
| 🔴 规格限制 | 「**网关规格**：选择 **aigw.medium.x1 以上规格**」 | create-a-gateway-instance |
| 可用区选择 | 「勾选**支持Gzip硬件加速**的可用区，并选择交换机」 | create-a-gateway-instance |
| 创建后的参数入口 | 实例 → **参数配置** → **网关引擎参数** → 编辑 **`EnableGzipHardwareAccelerate`** 参数 | create-a-gateway-instance |
| 客户端要求 | 「需要客户端能够处理Gzip压缩的数据，对于支持的客户端需要在请求头中添加 `Accept-Encoding: gzip`」 | create-a-gateway-instance |

[官方矛盾] `EnableGzipHardwareAccelerate` 参数在参数表中不存在：
- 原文 A：「在**网关引擎参数**区域编辑 **EnableGzipHardwareAccelerate** 参数」[create-a-gateway-instance]
- 原文 B：modifying-gateway-parameter-configurations 的 **20 个参数全表**中，只有 **`EnableHardwareAccelerate`**（bool，取值 [true, false]，默认 **true**，「将 **TLS 证书**的验证和卸载转移到硬件中执行，可大幅提高 HTTPS 请求的性能」）和 **`EnableGzip`**（bool，默认 **false**），**没有 `EnableGzipHardwareAccelerate`** [modifying-gateway-parameter-configurations]
- [推断] 两个名字相近但语义不同：`EnableHardwareAccelerate` 是 **TLS 卸载**硬件加速，`EnableGzipHardwareAccelerate` 是 **Gzip 压缩**硬件加速。A 指向的参数在 B 的参数表里缺失 → **文档级空白**：Gzip 硬件加速参数的取值范围与默认值查无。不裁决。

**性能参考数据（官方压测，照抄）**

压缩比统计口径原文：
> 「根据**核心地域内已启用 Gzip 的实例统计**，大部分实例的压缩比集中在 **10% 到 50%** 之间，意味着开启 Gzip 后，这些用户平均可**节省 50% 以上的流量**。」[官方原文｜create-a-gateway-instance]
> 官方对压缩比的定义：「压缩比（即**压缩后数据大小与压缩前数据大小的比值**）很大程度上受到数据本身的影响。**压缩比越低，代表压缩的效果越好**，压缩比越高，代表压缩的效果越差」；「如果数据中存在大量重复模式或结构（如文本中的字母、单词和标点），Gzip 压缩效果会更好」；「对于随机性高、熵值大的数据（如图片、视频、已压缩文件等），由于其内部重复性较低，压缩比通常较高，**压缩效果有限**」[官方原文｜create-a-gateway-instance]

CPU 压测表（原文表头照抄；压测数据为「一份大小约为120k的JSON文本」）：

| QPS | 硬件加速gzip/aigw.medium.x1/**单节点** CPU消耗 | 软件gzip/aigw.medium.x1/**4节点** CPU消耗 |
|---|---|---|
| 2000 | 9% | 11% |
| 5000 | 26% | 28% |
| 10000 | 56% | 56% |
| 13000 | 69% | 72% |

> 官方结论原文：「`开启Gzip硬件加速/单节点`的CPU消耗与`软件Gzip/4节点`的CPU消耗基本上持平。相当于原本需要4个节点才能承载，开启Gzip硬件加速后仅需要1个节点，**可以节省大约75%的实例资源**。」[官方原文｜create-a-gateway-instance]

→ [推断] 由「单节点硬件加速 ≈ 4 节点软件 Gzip」+「节省约 75% 实例资源」推出：**对以文本 / JSON 为主且需要压缩的客户，选 aigw.medium.x1 + Gzip 硬件加速可能比直接选更大规格更省钱**（前提：专享实例 + 7 个支持地域 + 支持 Gzip 硬件加速的可用区）。这是 SA 报价量级的直接杠杆。

⚠️ [官方矛盾] 压测 QPS 超出规格标称上限：
- 原文 A：压测表跑到 **13000 QPS**（aigw.medium.x1）[create-a-gateway-instance]
- 原文 B：「aigw.medium.x1｜QPS **12000**｜客户端连接数 160000」[capacity-description]
- 13000 > 12000（超 8.3%）。**不裁决** —— SA 不应把 13000 当作 medium.x1 的可承诺容量；压测口径（是否含节点数差异、是否为极限压测）文档未说明。

[文档未说明] Gzip 硬件加速是否**额外收费**、是否有独立计费项 —— 查无（🔴 连带计费空白）。
[文档未说明] 「核心地域」具体指哪些地域 —— 压缩比统计的样本范围未定义。
[文档未说明] `ZipAlgorithm` 支持 `brotli`（§2.11.7），但 **brotli 是否也有硬件加速** —— 查无。
[文档未说明] 「aigw.medium.x1 **以上**规格」是否含 medium.x1 本身 —— 压测表用的正是 medium.x1，倾向含；但「以上」的边界官方未明确。

#### 2.11.3 域名与证书

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 能力 | 「AI网关提供**多域名管理能力**，便于您管理不同域名下的协议、证书及路由配置。同时也支持**泛域名匹配**，例如绑定了`*.hello.com`这个泛域名之后，可以通过`1.hello.com`、`2.hello.com`等域名同时访问」 | create-a-domain-name |
| 🔴 前提条件 | 「完成相关域名的**备案**。」+「**中国地域独立域名需要在阿里云备案或者在阿里云备案接入，海外地域不需要域名备案**」 | create-a-domain-name |
| 域名格式 | 完整域名（`hello.com`）或泛域名（`*.hello.com`）；「在这个域名下，您可以**独立管理该域名的协议及证书**，**路由配置可以通过域名实现相互隔离**」 | create-a-domain-name |
| 🔴 泛域名 vs 证书的重要限制 | 「`*.hello.com`可以匹配`a.hello.com`、`b.hello.com`和`a.b.hello.com`等类型的域名，但是如果申请的证书域名是`*.hello.com`，则证书**只能用于`a.hello.com`、`b.hello.com`，不能用于`a.b.hello.com`**」（**重要**级提示） | create-a-domain-name |
| 协议与端口 | **HTTP：支持80端口**；**HTTPS：支持443端口** | create-a-domain-name｜change-the-protocol-and-certificate-of-the-domain-name |
| 证书来源 | 「选择HTTPS协议所关联的**阿里云SSL证书服务**上的证书」；未购买 / 上传可单击「购买/上传证书」跳转**数字证书管理服务**控制台 | create-a-domain-name |
| 强制 HTTPS | 「开启强制HTTPS，表示**只生效HTTPS端口**，正常HTTP端口将被**拒绝访问**，请求将被**重定向至HTTPS**」 | create-a-domain-name |
| HTTP/2 开关（3 选 1） | **使用网关实例配置**：「根据参数配置中 `EnableHttp2` 的值决定当前域名是否使用HTTP/2，并跟随参数配置中 `EnableHttp2` 的值动态变化」；**开启**：「当前域名在TLS握手成功后使用HTTP/2协议通信」；**关闭**：不使用。补充说明：「当协议配置为HTTP协议时，网关会利用 **HTTP Upgrade 协议**根据客户端要求自动升级为HTTP/2。因此，您**只有在使用了HTTPS协议时才需要按需配置HTTP/2开关**」 | create-a-domain-name |
| TLS 版本 | **最小TLS版本**「默认为 **1.0**」；**最大TLS版本**「默认为 **1.3**」 | create-a-domain-name |
| 加密算法套件 | **默认** 或 **自定义**；默认套件 14 条（见 §2.11.5） | create-a-domain-name |
| mTLS | **客户端双向认证 mTLS**：「开启或者关闭…**默认关闭**」；开启后需配置**客户端双向认证 CA 证书**，「用于验证客户端身份」 | create-a-domain-name |
| 资源组 | 「选择目标资源组。您可单击右侧的**创建资源组**」 | create-a-domain-name |
| 编辑 / 删除 | 域名列表页 → 操作列「编辑」/「删除」；删除时「在**确认删除域名**对话框中**输入当前的域名**，然后单击**删除**」 | delete-a-domain-name |
| 更换协议 / 证书 | 域名详情页 →「编辑」→ 更换协议（单击**域名**右侧下拉列表选协议）或更换证书（单击**证书**右侧下拉列表选证书）；触发场景：「SSL证书到期、域名所有者发生变更、或者需要将网站的协议从HTTP升级到HTTPS」；「**HTTPS协议必须关联SSL证书**」 | change-the-protocol-and-certificate-of-the-domain-name |
| 无 DNS 解析时的验证方式 | `curl http://hello.com --resolve "hello.com:80:{公网IP}"`；`curl -v -k https://hello.com --resolve "hello.com:443:{公网IP}" --cacert my-cert.pem`；前提「当前域名的路径下已配置可访问的路由」 | create-a-domain-name |

[文档未说明] 删除域名时是否级联删除关联的路由 / 证书绑定、是否有引用检查 —— 查无（对比：安全组授权页明确提供了「级联删除」勾选项，域名页没有）。运维高危空白。
[文档未说明] 单实例可绑定的**证书总数配额** —— capacity-description 配额表无「证书数」项（只有「发布域名数」）。
[文档未说明] 是否支持 SNI 多证书、是否支持国密（SM2 / SM3 / SM4）套件 —— 查无。
[文档未说明] 域名是否跨实例共享、是否支持全局域名 —— 查无。
[文档未说明] mTLS 的 CA 证书轮转方式、是否支持多 CA —— 查无。
[文档未说明] 证书到期是否有告警 / 自动续期 —— 查无（引擎 2.1.17 只修复过「用户自定义证书过期时间为空的问题」）。

#### 2.11.4 安全组授权规则

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 核心机制 | 「AI网关和后端服务所在的节点**分别处于不同安全组内**。您可以通过设置安全组规则为AI网关授予访问后端服务的权限」 | set-security-group-rules |
| 托管安全组 | 「根据您选择的安全组类型，AI网关会创建相应**托管安全组**管理网关的实例节点」 | set-security-group-rules |
| 授权动作方向 | 「需要您在**后端服务的安全组内**为AI网关授予必要的**端口范围访问权限**」 | set-security-group-rules |
| 生成的规则属性 | 「这些规则的授权策略均为**允许**，优先级为 **1**，协议类型为**自定义 TCP**，端口范围分别为 `8080/8080` 和 `1/65535`，授权对象为 AI 网关对应的安全组」 | set-security-group-rules |
| 端口范围语法 | 「**起始值/终止值**」；「可以输入多个端口范围，每输入一个端口范围单击回车，即可生效。例如，**`1/65535` 表示所有端口**，**`8080/8080` 表示单个端口 8080**」 | set-security-group-rules |
| 协议类型 | 「选择安全组后，确认**协议类型**为 **TCP**」 | set-security-group-rules |
| 获取目标安全组（容器服务 ACK） | 容器服务管理控制台 → 集群列表 → 单击目标集群名称 → 节点管理 > 节点池 → 单击对应的节点 → **基本信息**页签 → 获取安全组的 ID | set-security-group-rules |
| 获取目标安全组（ECS） | ECS 管理控制台 → 实例与镜像 > 实例 → 单击目标 ECS 实例 → **安全组**页签 → 获取安全组的 ID | set-security-group-rules |
| 🔴 删除的级联陷阱 | 「**默认只删除AI网关的安全组规则**，如需将目标节点所在安全组的规则一并删除，您还需要勾选**级联删除该安全组内的上述入方向规则。**」（**重要**级提示） | set-security-group-rules |
| 🔴 实例删除后残留 | 「AI网关实例已删除后，**无法再通过AI网关控制台访问安全组授权页签**，但网关此前创建的**托管安全组仍会残留在VPC中，导致VPC无法删除**（报错码 **`DependencyViolation.SecurityGroup`**）。此时请通过ECS控制台手动清理」；清理路径：ECS 管理控制台 → 网络与安全 > 安全组 → 顶部选残留安全组所在地域 → 通过**专有网络VPC ID**筛选或通过安全组名称定位 → 操作列「删除」→ 确定；「安全组清理完成后，重新执行VPC删除操作；**若该VPC由ROS资源栈创建，请重试删除对应的ROS资源栈**」 | set-security-group-rules |
| 官方建议 | 「为了避免这种情况发生，建议您在配置安全组授权时**扩大端口范围，可以将范围选成 `1/65535`**」 | set-security-group-rules |
| 排障 FAQ 1 | 「安全组已经授权，为什么服务还是访问不通？」→ ①「首先需要确认您的目标服务所部署的节点是否正确。有可能存在服务部署在了A节点上，但是给B节点所在的安全组授权」；②「您的目标节点是否设置了**多个安全组**。如果是多个安全组，**建议给每个安全组都授权**」 | set-security-group-rules |
| 排障 FAQ 2 | 「之前网关访问服务是通的，现在突然间不通了」→ ①「首先确认您的服务本身没有问题。您可以对同一安全组内的其他节点使用 `curl` 命令检查服务的连通性」；②「确认您发布的服务对外暴露的**端口是否有变更**。例如以前端口为8080，在AI网关只给8080端口授权了，之后又将端口变更为8081，这时需要重新调整云安全组授权规则端口」 | set-security-group-rules |
| 官方拓扑示例 | 「service-sg1中的Pod可以处理来自**8080/8080**端口的请求」；「service-sg2中的ECS可以处理来自**80/9000**端口的请求」 | set-security-group-rules |

[官方矛盾] 购买页是否有「安全组」配置项：
- 原文 A：「您在购买AI网关时需要选择 **VPC 和安全组类型**（建议与后端服务所在安全组类型一致），根据您选择的安全组类型，AI网关会创建相应托管安全组管理网关的实例节点」[set-security-group-rules]
- 原文 B：create-a-gateway-instance 的 11 个配置项（商品类型 / 地域 / 网关名称 / 网关规格 / 资源组 / 网络访问类型 / 专有网络 / 可用区选择 / 交换机 / 日志服务 / 服务关联角色）中，**没有「安全组」或「安全组类型」** [create-a-gateway-instance]
- 交叉证据：view-gateway-instance-details 说实例详情「**网络信息**」区域可查看「**端口**、**VPC** 和**安全组**」→ 安全组确实存在且可查 [view-gateway-instance-details]
- [推断] 由 A + B + 详情页可查推出：安全组要么在购买页存在但创建文档漏写，要么由系统按 VPC 自动分配托管安全组。**不裁决** → **文档级空白**：SA 无法从文档确认「普通安全组 vs 企业级安全组」的选择时机与影响。

[文档未说明] 安全组类型的可选项（普通 / 企业级）及其对网关能力的影响 —— 查无。
[文档未说明] 单实例可授权的安全组数量上限、单个安全组可授权的端口范围条数上限 —— 查无。
[文档未说明] 托管安全组的命名规则（只说「通过安全组名称定位」）—— 查无。
[文档未说明] Serverless 各形态是否也需要做安全组授权（标准版无独立入口、无网关规格）—— 查无。
[文档未说明] 是否支持 UDP / ICMP 协议授权（页面只提 TCP）—— 查无。

#### 2.11.5 HTTPS 加密套件与 TLS 版本

**AI 网关支持的加密套件全表（14 条，两页集合一致）**

| 套件名称 | setting-the-specified-https-cipher-suite 的「支持的TLS版本列表」 | 是否属于 create-a-domain-name 的「默认加密算法套件」 |
|---|---|---|
| ECDHE-ECDSA-AES128-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是（支持版本：TLS 1.0, TLS 1.1, TLS 1.2, TLS 1.3） |
| ECDHE-ECDSA-AES256-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-RSA-AES128-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-RSA-AES256-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是 |
| AES128-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是 |
| AES256-SHA | TLS 1.0、TLS 1.1、TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-ECDSA-AES128-GCM-SHA256 | TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-ECDSA-CHACHA20-POLY1305 | TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-RSA-AES128-GCM-SHA256 | TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-RSA-CHACHA20-POLY1305 | TLS 1.2、TLS 1.3 | ✅ 是 |
| AES128-GCM-SHA256 | TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-ECDSA-AES256-GCM-SHA384 | TLS 1.2、TLS 1.3 | ✅ 是 |
| ECDHE-RSA-AES256-GCM-SHA384 | TLS 1.2、TLS 1.3 | ✅ 是 |
| AES256-GCM-SHA384 | TLS 1.2、TLS 1.3 | ✅ 是 |

来源：[官方｜setting-the-specified-https-cipher-suite｜create-a-domain-name]
[推断] 两页各列 14 条且**集合完全相同**（仅顺序不同：套件页 SHA 类在前，域名页 GCM / CHACHA20 类在前），推出「默认加密算法套件」=「AI 网关支持的全部套件」，即**默认不做裁剪**。

**官方对加密套件构成的解释（原文）**：「一个HTTPS加密套件通常包括以下几个组成部分：1. **密钥交换算法**：用于安全地交换加密通信的密钥。常见的密钥交换算法包括RSA、Diffie-Hellman（DH）和ECDHE（椭圆曲线Diffie-Hellman）。2. **消息认证码（MAC）算法**：用于确保数据的完整性和认证，常见的MAC算法包括HMAC-SHA256、HMAC-SHA384等。3. **对称加密算法**：用于加密数据本身性[原文如此]，常见的对称加密算法包括AES（高级加密标准）、ChaCha20等。」[官方原文｜setting-the-specified-https-cipher-suite]

**能力定性原文**：「为了进一步满足您在使用网关时，对于安全性、兼容性、性能优化以及其他合法合规的要求，**AI网关支持客户端选择指定的加密套件**。」[官方原文｜setting-the-specified-https-cipher-suite]

**配置路径**：控制台左侧导航「**域名**」→ 顶部选地域 →「**添加域名**」或目标域名「操作」列「**编辑**」→ 在**域名**下拉列表中选择 **HTTPS** 协议 → 单击「**高级选项**」→ 在「**加密算法套件**」单选框中选择「**自定义**」→ 在可选算法列表中勾选需要设置的算法 → 确定。[官方｜setting-the-specified-https-cipher-suite]

**官方验证方法（照抄命令，已把渲染残留的 `HELPCODEESCAPE-bash` 修回 `bash`）**
```bash
curl -iv --ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256' https://bantian.alijam.top/get --resolve "bantian.alijam.top:443:8.154.33.131"
```
判定标准：「指定套件`ECDHE-ECDSA-AES128-GCM-SHA256`请求正常返回成功，**双方协商使用加密套件 `ECDHE-ECDSA-AES128-GCM-SHA256`**」；验证输出关键行：`* Cipher selection: ECDHE-ECDSA-AES128-GCM-SHA256`、`* ALPN, offering h2`、`* ALPN, offering http/1.1`、`* Connected to bantian.alijam.top (8.154.33.131) port 443`。[官方｜setting-the-specified-https-cipher-suite]

[官方矛盾] 自定义加密套件在 TLS 1.3 下是否生效：
- 原文 A（套件页）：14 条套件中 8 条标注「支持的TLS版本列表：TLS 1.2、**TLS 1.3**」，6 条标注「TLS 1.0、TLS 1.1、TLS 1.2、**TLS 1.3**」—— **全部 14 条都声明支持 TLS 1.3** [setting-the-specified-https-cipher-suite]
- 原文 B（域名页，**说明**级提示）：「**指定加密套件只会在协商结果为TLS 1.0-1.2时有效，协商结果为TLS1.3时不生效。**」[create-a-domain-name]
- **不裁决**。[推断] 由 B 的措辞「**指定**加密套件」（即用户自定义选择这一动作）+ A 的表头「**支持的**TLS版本列表」推出一种可能读法：A 表达套件本身在 TLS 1.3 下可被协商（TLS 1.3 有独立的 cipher suite 机制），B 表达**用户手动裁剪套件列表这一动作在协商到 TLS 1.3 时不起作用**。仅为推断，SA 对客应按 **B（更保守）**执行并建议客户实测协商结果。
- 🔴 SA 影响：合规客户常要求「禁用弱套件、只保留指定套件」。若客户端协商到 TLS 1.3，**该要求可能无法通过网关侧配置强制达成**；需结合「最小 / 最大 TLS 版本」（默认 1.0 / 1.3）把最大版本压到 1.2 才能让指定套件生效 —— **这一步骤文档未给出，属 [推断]**。

[文档未说明] 是否有预置的 **TLS policy** 策略集（可选值清单）—— ai-gateway-capacity-description **3 次**提到「TLS policy」（「需要自定义域名、证书、**TLS policy** 或 HTTP/2 配置」「不支持用户自定义证书、TLS policy 或 HTTP/2 配置」「支持用户配置证书、TLS policy 和 HTTP/2」），但**没有任何一页定义 TLS policy 的可选值**。术语级空白。
[文档未说明] 默认 TLS 版本范围（1.0~1.3）能否在**实例级**统一收紧、是否影响标准版的平台默认 HTTPS 入口 —— 查无。
[文档未说明] TLS 1.0 / 1.1 是否有下线计划 —— 查无（默认最小版本仍是 1.0，合规客户会问）。
[文档未说明] 是否支持 TLS 会话复用 / 会话票据 / OCSP Stapling —— 查无。
[文档未说明] `EnableHardwareAccelerate`（TLS 硬件卸载，默认 true）是否有地域 / 规格限制 —— Gzip 硬件加速侧有明确「7 地域 + aigw.medium.x1 以上 + Serverless 不支持」，TLS 侧**无任何限制说明**。
[文档未说明] Serverless 标准版「平台默认 HTTPS 入口」使用的证书主体、TLS 版本与套件 —— 查无。

#### 2.11.6 DNS 服务器配置

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 目的 | 「为服务配置DNS服务器可以实现高效、安全的**内部域名解析**，确保内部服务的访问稳定性和可靠性。通过合理配置DNS服务器，可以实现对内部服务域名的集中管理，**避免因外部DNS故障或网络波动导致的服务不可用问题**」 | configure-dns-server |
| 使用场景（3 类） | ①**自定义DNS需求**：「满足用户对内网DNS的自定义配置需求」；②**内部服务解析**：「后端服务位于VPC内时，AI网关使用内网DNS正确路由请求」；③**混合云环境**：「统一管理内部和外部服务的DNS解析」 | configure-dns-server |
| 🔴 使用限制 | 「**DNS服务器列表最大限制5个**」 | configure-dns-server |
| 配置入口 | 实例 → 左侧导航「**服务**」→「**服务**」页签 →「**创建服务**」或目标服务「操作」列「**编辑**」→「**更多设置**」→「**一键填充内网DNS解析服务地址**」 | configure-dns-server |
| 一键填充逻辑 | 「当您开通内网DNS服务解析时，阿里云会**自动为您的VPC分配内网DNS解析服务地址**。系统自动填充内网DNS解析服务地址」 | configure-dns-server |
| 手动添加 | 「**最多可配置5个DNS服务器**，也可单击 **+ 添加** 手动添加」；「手动输入地址的格式为 **`IP:端口`**」 | configure-dns-server |
| 依赖产品 | 内网 DNS 服务解析（PrivateZone，控制台 `dnsnext.console.aliyun.com/privateDNS/introduce`） | configure-dns-server |
| 相关能力 | what-is-an-ai-gateway：「支持在AI服务中配置API-KEY，并针对**内部服务地址指定自定义DNS Server**」；「**DNS 服务**：支持通过DNS解析方式访问后端服务，**允许指定专用DNS Server以解析私有网络或内部域名**」 | what-is-an-ai-gateway |
| 时间线信号 | 2026-02 优化项：「**Agent 服务支持配置内网 DNS 解析**」（说明此前 Agent 服务不支持） | new-feature-release-notes-ai-gateway |

[推断] 由「配置入口在**服务**的『更多设置』里」+「DNS服务器列表最大限制5个」推出：**5 个上限是「单个服务」级别**，不是实例级别。但原文未写「每服务」作用域 → 严格说属 [文档未说明]，此处标为推断，SA 应实测确认。
[文档未说明] 🔴 5 个上限的**作用域**（每服务 / 每实例 / 每 Region）—— 原文无作用域限定词。
[文档未说明] DNS 解析超时、重试次数、是否支持 DNS over TLS/HTTPS、是否支持 search domain / ndots —— 查无。
[文档未说明] 内网 DNS 与公网 DNS 混用时的优先级 —— 查无。
[文档未说明] 一键填充依赖的「内网DNS服务解析」是否**独立开通、独立计费** —— 页面只给跳转链接，未说计费。🔴 潜在连带计费空白。
[文档未说明] DNS 服务器是否支持域名形式（原文只给 `IP:端口` 格式）—— 查无。

#### 2.11.7 网关引擎参数全表（20 个可改参数）

> 官方前置约束：「为保证实例的稳定运行，**仅支持对控制台中开放的参数进行修改，未在控制台中呈现的参数不支持修改**」；「修改网关引擎参数值时，请参考网关引擎参数页面中的**取值范围**」；「修改网关参数**可能会对网络连接和应用程序的使用产生影响**，因此在进行此类操作之前，请了解可修改参数的取值范围及其作用」[官方原文｜modifying-gateway-parameter-configurations]
> 路径：实例 → 左侧导航「**参数配置**」→「**网关引擎参数**」区域 → 目标参数「操作」列「**编辑**」→ 设置参数值 →「**确认**」

| 参数名称 | 参数类型 | 取值范围 | 默认值 | 参数描述（照抄） |
|---|---|---|---|---|
| DownstreamConnectionBufferLimits | int64 | [0, 2147483647] | **32768** | 作用于网关连接，单条链接的buffer大小，配置后会影响吞吐和网关的内存使用, 单位byte |
| PathWithEscapedSlashes | string | KEEP_UNCHANGED / REJECT_REQUEST / UNESCAPE_AND_REDIRECT / UNESCAPE_AND_FORWARD | **KEEP_UNCHANGED** | 确定 URI 路径中包含 %2F、%2f、%5C 或 %5c 这些转义的请求的操作, 默认为KEEP_UNCHANGED（保持不变） |
| DownstreamIdleTime | int32 | [0, 600] | **180** | 客户端到网关处于指定的时间内[0-600]没有请求，则会断开链接。单位为秒。**重启才会生效** |
| EnableHardwareAccelerate | bool | [true, false] | **true** | 将 **TLS 证书**的验证和卸载转移到硬件中执行，可大幅提高 HTTPS 请求的性能 |
| InitialStreamWindowSize | int64 | [65535, 2147483647] | **65535** | 作用于请求环节，网关同客户端使用http2时协商的stream初始窗口大小。单位为byte |
| UpstreamIdleTimeout | int32 | [0, 600] | **30** | 默认到上游的idle时间。单位为秒 |
| ZipAlgorithm | array | [gzip, brotli] | **gzip** | 开启压缩后使用的算法，可以选择brotli，gzip，**如果此时EnableGzip未开启，将自动开启EnableGzip选项** |
| EnableCustomAuthConfigPush | bool | [true, false] | **false** | 作用于使用自建的鉴权服务的场景，开启后**鉴权规则变更不会引起连接中断**，适用于WebSocket和在线业务场景 |
| EnableProxyProtocol | bool | [true, false] | **true** | 是否开启Proxy协议，**如果网关入口流量使用NLB接入，如果不开启则无法获取客户端的真实IP**，开启后对于非Proxy协议请求没有影响 |
| PreserveHeaderFormat | bool | [true, false] | **false** | 是否保持header头大小写, http1.1规范中 header头不区分大小写进行识别，**为了保证与http2规范兼容，默认会统一转化为小写** |
| KeepAliveHeaderTimeout | int32 | [0, 600] | **0** | 用于生成Keep-Alive响应头返回给客户端，告知连接的保活时间。单位为秒。例如配置为10时，会返回响应头：'keep-alive: timeout=10'。**配置为0时，不会返回该响应头** |
| EnableHttp3 | bool | [true, false] | **false** | 是否开启http3 |
| AlwaysSetRequestIdInResponse | bool | [true, false] | **true** | 用于控制在响应中是否始终包含请求ID |
| EnableGzip | bool | [true, false] | **false** | 作用于请求与响应环节，启用gzip会对请求响应进行压缩，**会减少网关流量，增加网关cpu消耗** |
| InitialConnectionWindowSize | int64 | [65535, 2147483647] | **1048576** | 作用于请求环节，网关同客户端使用http2时连接级别初始窗口大小。单位为byte |
| DownstreamHttp2MaxConcurrentStream | int64 | [0, 2147483647] | **100** | 作用于请求环节，**客户端使用http2时一条链接上最大并发数** |
| EnableSlashMerge | bool | [true, false] | **false** | 作用于请求环节，是否合并请求中多余的'/', 开启后www.a.com//b多余的'/'会被合并，将会同www.a.com/b一致 |
| EnableGenerateRequestId | bool | [true, false] | **true** | 作用于请求范围，根据配置会在请求头中生成requestId，以便追踪请求 |
| WebsocketTermGracePeriod | int32 | [20, 900] | **20** | 当网关实例**升级、重启**等需要关闭连接的场景下，为Websocket连接维持的保活时间。单位为秒 |
| XffTrustedNum | int32 | [0, 10] | **0** | 作用于请求环节，**网关前可信任的代理个数**，会影响网关是否会使用客户端产生的x-forwarded-for和x-request-id等请求头 |

来源：[官方｜modifying-gateway-parameter-configurations]

**SA 高频决策点（均有原文依据）**
- 🔴 **`DownstreamIdleTime` 默认 180 秒、取值上限 600 秒，且「重启才会生效」** → LLM 长请求 / 长连接场景若客户端空闲超 180s 会被网关断开；调大最多也只能到 600s，且**改完必须重启实例**。这是 SA 最容易被追问的参数。
- 🔴 **`UpstreamIdleTimeout` 默认仅 30 秒**（取值 [0, 600]）→ 到上游的空闲连接 30s 即回收；对模型服务连接复用有直接影响。
- 🔴 **`DownstreamHttp2MaxConcurrentStream` 默认 100** → 高并发客户端走 HTTP/2 时可能撞到单连接 100 并发流上限，需与 §2.4「客户端连接数」配额分开看。
- 🔴 **`XffTrustedNum` 默认 0**，「会影响网关是否会使用客户端产生的x-forwarded-for和x-request-id等请求头」→ 默认**不信任任何前置代理**；客户若在网关前挂 SLB / CDN / WAF，需按实际代理层数设置（取值 0~10），否则取不到真实客户端 IP。[推断] 由默认值 0 + 参数描述推出这会连带影响 IP 黑白名单与按消费者限流的准确性 —— 官方未展开这条影响链。
- 🔴 **`EnableProxyProtocol` 默认 true**，「如果网关入口流量使用 **NLB** 接入，如果不开启则无法获取客户端的真实IP」→ 与 `XffTrustedNum` 是两套真实 IP 获取机制，方案里要说清用哪一套。
- **`PreserveHeaderFormat` 默认 false**（header 统一转小写，为兼容 http2）→ 后端若做大小写敏感的 header 校验会踩坑。
- **`ZipAlgorithm` 默认 gzip、可选 brotli**，且「如果此时EnableGzip未开启，**将自动开启EnableGzip选项**」→ 改压缩算法会**隐式打开** `EnableGzip`（默认 false），这是隐式副作用。
- **`EnableGzip` 默认 false**，官方明示权衡：「会减少网关流量，**增加网关cpu消耗**」→ 与 §2.11.2 的 Gzip 硬件加速（节省约 75% 实例资源）配套理解。
- **`EnableHttp3` 默认 false** → HTTP/3 需手动开启。
- **`EnableCustomAuthConfigPush` 默认 false**：「开启后鉴权规则变更不会引起连接中断，适用于 **WebSocket** 和在线业务场景」→ 自建鉴权 + WebSocket 长连接的方案建议开启（落地归 W4）。
- **`WebsocketTermGracePeriod` 默认 20 秒、取值 [20, 900]**：实例升级 / 重启时 WebSocket 的保活窗口 → 与引擎升级的兼容性直接相关。
- **`EnableHardwareAccelerate` 默认 true**（TLS 硬件卸载）→ 与 Gzip 硬件加速不同，**无地域 / 规格限制说明**。
- **`DownstreamConnectionBufferLimits` 默认 32768 byte**、**`InitialStreamWindowSize` 默认 65535 byte**、**`InitialConnectionWindowSize` 默认 1048576 byte** → 大 prompt / 大响应体（多模态、长文本）场景的调优点，官方明示 buffer「配置后会影响吞吐和网关的内存使用」。
以上均 [官方｜modifying-gateway-parameter-configurations]（除标注 [推断] 者）。

[官方矛盾] `EnableHttp2` 参数在参数表中缺失：
- 原文 A：域名配置的 HTTP/2 开关有一项「**使用网关实例配置**：根据参数配置中 **`EnableHttp2`** 的值决定当前域名是否使用HTTP/2，并跟随参数配置中 `EnableHttp2` 的值动态变化」[create-a-domain-name]
- 原文 B：modifying-gateway-parameter-configurations 的 20 个参数表中**没有 `EnableHttp2`**，只有 `EnableHttp3`（默认 false）[modifying-gateway-parameter-configurations]
- 交叉证据：ai-gateway-capacity-description 把「**HTTP/2 配置**」列为 Serverless 标准版不支持、企业版 / 旧版 / 独享版支持的能力项
- **不裁决** → **文档级空白**：`EnableHttp2` 的默认值、取值范围、是否实例级参数，全部查无。SA 无法回答「网关默认是否开 HTTP/2」。

[文档未说明] 🔴 修改参数后**哪些需重启、哪些热生效**：20 个参数中只有 `DownstreamIdleTime` 明确写「重启才会生效」，其余 19 个**均未说明生效方式**。高危空白。
[文档未说明] 参数修改是否有审计记录、能否批量导出 / 导入、是否有参数模板 —— 查无。
[文档未说明] Serverless 各形态是否开放全部 20 个参数 —— 查无（标准版明确不支持自定义 TLS / HTTP/2，[推断] 参数面也受限，但无明文）。
[文档未说明] 「重启网关」的影响面与耗时：view-gateway-instance-details 只说基本信息页签可「**重启网关**」，未说是否中断流量、耗时多久。
[文档未说明] 参数取值的**推荐值 / 调优指引**（除默认值外）—— 查无。官方只说「修改网关参数可能会对网络连接和应用程序的使用产生影响」。
[文档未说明] `KeepAliveHeaderTimeout` 默认 0（不返回 keep-alive 头）对长连接客户端的实际影响 —— 查无。

#### 2.11.8 实例详情页与形态相关的能力开关

| 项目 | 官方口径 | 来源 slug |
|---|---|---|
| 基本信息区域 | 可查看「**实例ID**、**实例名称**和**实例类型**等基本信息」 | view-gateway-instance-details |
| 运行信息区域 | 可查看实例「**运行状态**、**实例规格**和**接入点**」等运行信息 | view-gateway-instance-details |
| 网络信息区域 | 可查看「**端口**、**VPC** 和**安全组**」等网络信息 | view-gateway-instance-details |
| 基本信息页签可做的操作 | 「可以在**基本信息**页签修改**实例名称**、管理端口、修改标签、**重启网关** 和 **开启WAF防护**」 | view-gateway-instance-details |
| 🔴 形态限制 | 「**Serverless版AI网关不支持开启WAF防护**」（未区分标准版 / 企业版 / 旧版） | view-gateway-instance-details |

[官方矛盾] Serverless 与 WAF：
- 原文 A：「**Serverless版AI网关不支持开启WAF防护**」[view-gateway-instance-details]
- 原文 B：product-comparison 把「**WAF 防护**｜深度集成阿里云 WAF 产品」列为 AI 网关相对 Higress 开源版的优势，**未带实例类型限定**；what-is-an-ai-gateway 把「集成 SSL 证书、**WAF 防护**及 IP 黑白名单功能，在网络入口层抵御恶意流量与攻击」列为网络安全能力，也**未带限定** [product-comparison｜what-is-an-ai-gateway]
- **不裁决**。[推断] 由 A 的明确否定 + ai-gateway-capacity-description「Serverless 标准版…**部分高级能力不开放**」推出：WAF 是**专享实例独有能力**，Serverless 全系不可用。SA 对合规客户要求 WAF 时，应直接推独享版。
- 时间线佐证：引擎 2.1.13（2025-10-24）「**WAF接入支持远程xagent模式**」、2.1.15（2025-12-25）「**WAF 功能增强**」、2.1.22（2026-08-13）「**优化开启WAF时的内存资源使用**」→ [推断] 推出开启 WAF 有额外内存开销（否则无需专门优化），但**开销数字文档未说明**。

[文档未说明] 「管理端口」能改哪些端口、端口范围、是否影响已有域名绑定 —— 查无。
[文档未说明] 🔴 开启 WAF 是否**连带开通 WAF 产品并独立计费** —— 查无（连带计费空白，归 W2 / W4）。
[文档未说明] 「接入点」的形态（公网 / 私网 IP、域名、数量上限、移除影响）—— 发布记录 2026-07 有「**网关接入点支持移除**」，但接入点定义与移除影响均未说明。
[文档未说明] 实例「运行状态」的完整枚举 —— 除「运行中」外，发布记录 2025-10「修复**停止状态**的实例不支持续费的问题」→ 存在「停止」状态，但状态机文档未给。
[文档未说明] 「修改标签」的标签数量上限、与资源组的关系 —— 查无（归 W7）。

### 2.12 新功能发布记录：对 SA 有决策含义的时间线信号

发布记录覆盖 **2025-05 ~ 2026-07**（共 14 个月度小节）。下面只抽取**对选型 / 报价 / 避坑有决策含义**的信号；纯能力列表不重述（细节归对应 worker）。

#### A. 商品与形态时间线（🔴 最高决策价值）

| 时间 | 变更类型 | 原文 | SA 含义 |
|---|---|---|---|
| 2025-09 | **新商品** | 「AI 网关发布 **Serverless 版本**，最高节省 **90%成本**」 | 这是「Serverless（旧）」的发布点。「最高节省 90%成本」的**对比基准文档未说明** |
| 2026-07 | **新功能** | 「**多租 Serverless 正式开启公测**，提供**企业版与标准版**，**最低 0 起步**，**公测期间免费试用**」 | 🔴 新版 Serverless 的起点。⚠️ **该公测已结束**：官方商业化公告明文「AI 网关 Serverless 新版公测将于 **2026 年 8 月 31 日** 结束，并自 **2026 年 9 月 1 日**起正式商业化」「正式商业化并**开始计费**」「存量公测实例将默认保留并**自动转为商业化实例**，实例配置和业务数据无需迁移」`[官方原文｜ai-gateway-commercialization-announcement]` → **本知识库快照日 2026-09-21 已在商业化后 20 天，🔴 严禁再对客说「新版 Serverless 还在公测/还免费」**。商业化后的计费项与价格官方明示「请以官网价格页、产品控制台和账单展示为准」→ 见 [§3 计费](aliyun-ai-gateway-billing.md) 与 §15.9 必核清单 |

[推断] 由 2025-09「发布 Serverless 版本」+ 2026-07「多租 Serverless 开启公测，提供企业版与标准版」+ ai-gateway-capacity-description「新版 Serverless 采用**多租资源池化架构**」「Serverless（旧）为**原 Serverless 版本**」推出：2025-09 版 = 今日「Serverless（旧）」，2026-07 版 = 今日「Serverless 标准版 + 企业版」。**旧版从发布到被归入「旧」只经过约 10 个月** → SA 应预期旧版能力冻结（「不支持插件体系」、「后续新增能力会优先围绕新版 Serverless 演进」）。

#### B. 开服地域时间线（与 §2.9 地域表冲突）

| 时间 | 原文 | supported-regions 表是否收录 |
|---|---|---|
| 2025-07 | 「开服｜新增**青岛**地域」 | ✅ cn-qingdao |
| 2025-08 | 「开服｜新增**韩国**地域」 | ❌ 未收录 |
| 2025-12 | 「开服｜新增**马来西亚**地域」 | ❌ 未收录 |
| 2026-03 | 「开服｜新增**亚特兰大**地域」 | ❌ 未收录 |

来源：[官方矛盾｜new-feature-release-notes-ai-gateway｜supported-regions]（详见 §2.9）

#### C. 配额、规格与计量相关的信号

| 时间 | 原文 | SA 含义 |
|---|---|---|
| 2026-03 | 优化｜「**资源配额扩大，适配用户的更大使用规模**」 | ⚠️ **无数字**。capacity-description 的配额表**未标版本 / 生效日期** → 无法判断当前表里的数字是扩额前还是扩额后。SA 引用配额表时必须提示「可能已调整，以控制台为准」 |
| 2026-03 | 优化｜「**Token 限流策略支持依据引擎版本过滤限流模式，每周/每月限流（TokenPerWeek/TokenPerMonth/RequestPerWeek/RequestPerMonth）需引擎版本 ≥ 2.1.15**」 | 🔴 我的快照中**唯一**一处「能力 ← 引擎版本」的显式门槛声明（引擎版本页本身没有）。归 W3 落地 |
| 2026-03 | 新功能｜「**AI 网关与普通网关支持区分默认告警规则类型**，AI 网关使用专属告警指标（AIGatewayEnvoyCpuUsageRate、AIGatewayEnvoyMemoryUsageRate、AIGatewayEnvoyPluginCrash）」 | §1.4 产品族边界证据；三个专属指标名可用于监控方案设计（归 W7） |
| 2026-05 | 新功能｜「支持对**连接数、自动扩容 Unit 数**的监控」 | 🔴 首次暴露「**自动扩容 Unit**」这一扩容 / 计量概念，但 **Unit 的定义、单价、各规格 Unit 上限全部查无** → 与 §2.4 的「节点数」空白同源。Serverless 报价的关键缺口 |
| 2026-03 | 优化｜「解决用户**同时配置健康检测和大模型负载均衡**导致的配置推送失败问题，**产品侧增加互斥校验**」 | 🔴 设计行为而非 bug：健康检测与大模型负载均衡**互斥**（归 W3 落地，此处记时间锚点） |
| 2025-10 | 修复｜「修复**停止状态的实例不支持续费**的问题」 | 实例存在「停止」状态；2025-10 前停止态无法续费（归 W2） |

#### D. 网络与入口相关的信号

| 时间 | 原文 | SA 含义 |
|---|---|---|
| 2026-04 | 新功能｜「**支持开通公网后关闭公网**」 | 公网入口可**后关**。反向（创建时私网、之后开公网）**未提及** → [文档未说明] |
| 2026-07 | 优化｜「**网关接入点支持移除**」 | 接入点可移除；定义 / 数量上限 / 移除影响均未说明 |
| 2026-07 | 新功能｜「**支持与全球加速 GA 的集成**」 | 🔴 跨境 / 全球低延迟场景的新方案组件，**连带开通 GA 产品**（计费归 W2，方案细节本页未展开） |
| 2026-04 | 新功能｜「支持配置**第三方代理 Base URL**」 | 走第三方代理访问海外模型的能力起点之一 |
| 2026-03 | 优化｜「创建 AI 服务时，**Base URL 支持配置 Claude、Gemini 等模型的第三方代理平台地址**」 | 与上条共同说明：第三方代理方案在 2026-03 / 04 才成型（归 W3） |

#### E. 开放平台 / API 产品相关（与 §1.6 呼应）

| 时间 | 原文 |
|---|---|
| 2026-04 | 新功能｜「**集成 HiMarket，支持通过控制台搭建 AI 开放平台，进行 API 产品管理、门户管理与产品分类管理**」 |

#### F. FinOps / Credits 时间线（🔴 与 W2 / W3 强相关，此处只记时间锚点与矛盾）

| 时间 | 原文要点 |
|---|---|
| 2026-05 | 「AI 网关新增 **FinOps 消费者配额能力**，支持消费者在**实例级别**设置 Token 配额，支持按**自然日/月/年**设置配额周期，支持配额规则**时区设置、配额重置及配额使用水位监控**」；「新增 **Credits 配额维度**。创建配额规则时，在**规则类型**中可选择 **Token 配额或 Credits 配额**。**Credits 为统一计量单位，跨模型归一化成本**。两种配额类型的设置方式相同，均支持按**自然日/周/月**设置重置周期、时区设置、配额重置及用量监控」 |
| 2026-06 | 「**上线FinOps能力**，支持消费者级别的Token配额限制」；「支持**消费者组**，可对消费者按组划分，实现消费者组级别的API授权」；「支持**千问云以及百炼Token Plan**的对接」 |
| 2026-07 | 「**FinOps 支持自定义周期配额，支持 Credits 管控**」；「支持**模型资产管理**，提供模型元信息与供应商管理，可对模型进行 **Credits 配额管控**」 |

⚠️ **同页内部口径不一致（不裁决，仅报告，归 W3）**
1. [官方矛盾] FinOps 上线时间：2026-05 小节写「AI 网关**新增** FinOps 消费者配额能力」，2026-06 小节写「**上线**FinOps能力，支持消费者级别的Token配额限制」—— 同一能力在相邻两月分别用「新增」和「上线」。原文如上。
2. [官方矛盾] 配额周期粒度：2026-05 **同一段落**里，Token 配额写「支持按**自然日/月/年**设置配额周期」，紧接着写「两种配额类型的设置方式相同，均支持按**自然日/周/月**设置重置周期」—— **「日/月/年」vs「日/周/月」在同一段冲突**。且 2026-03 另有「Token 限流支持 **7 天、30 天**限制，支持更灵活的用量控制场景」。三处口径并存。
3. `finopts`（引擎 2.1.19 / 2.1.20）与 `FinOps`（引擎 2.1.21+、发布记录）写法不一 —— [推断] 前者为笔误 [原文如此]。

#### G. 其他有方案含义的时间锚点（简表，细节归对应 worker）

| 时间 | 信号（原文摘要） | 建议归属 |
|---|---|---|
| 2025-05 | 「**内容安全**升级为 **AI 安全围栏**」（术语变更）；「支持将**搜索**设置为默认关闭，通过客户端参数手动启用搜索」；「AI 服务支持直接**对接 PAI EAS** 并在运行时自动获取 API-KEY」；「支持**直接添加 PAI-EAS 服务作为 AI 服务后端**」；「支持**从 Nacos MCP Registry 导入 MCP Server**」；「**LLM API 支持自定义路由**」 | W4 / W3 / W5 |
| 2025-06 | 「新增 **Agent API**，支持代理**百炼应用和 Dify**」（Agent API 的诞生点）；「**AI 缓存**支持语义化缓存策略」；「Model API 支持 **fine_tuning 接口**」 | W5 / W3 |
| 2025-07 | 「Model API 支持代理**万相、cosyvoice 等多模态模型**」「支持代理 **rerank 模型**」「支持为 openAI 兼容协议添加 **responses 接口**」；「MCP Server 支持包括 **tool 调用在内的可观测**」；「MCP Server 支持 **MCP 工具级别消费者认证**」；优化「MCP 配置格式错误时透出详细错误信息」「MCP Server 配置保存时增加预检」 | W3 / W5 / W4 |
| 2025-08 | 「支持**密钥管理**，通过对接 **KMS**，实现消费者凭证、API-KEY、插件配置中的敏感信息等的安全管理」；「新增**虚拟 MCP Server**，可自由组装已有 MCP Server 的工具」；「Model API 支持 **ComfyUI 服务**」 | W4 / W5 |
| 2025-09 | 「MCP 工具支持**语义检索**」；「MCP Server 支持 **Tool 组装**」；「MCP Server 支持**按比例灰度服务**」；「**Agent API 支持策略与插件**」；「AI 网关支持在日志中**开关 question 和 answer 的写入**」；「AI 安全防护支持按多个防护维度分别设置拦截策略」 | W5 / W7 / W4 |
| 2025-10 | 「Model API 支持**服务节点的负载感知路由**，可基于推理框架的监控数据智能调度服务节点」；「Model API 限流策略新增**请求数和并发数**维度，且支持在 **embedding、rerank 和多模态**场景开启」；「Embedding 场景的 Model API 支持按模型名称路由到多个服务提供商」；「多模态、Embedding 和 Rerank 场景的 Model API 支持设置策略和插件」；「Agent API 新增可观测大盘」；「自定义协议的 Agent API 支持按请求权重路由到多个后端服务」；优化「openAI 兼容协议下 AI 观测支持记录 responses API 的 question 和 answer」 | W3 / W5 / W7 |
| 2025-11 | 「直接代理的 MCP Server 支持展示**工具粒度的消费者授权、工具组装和语义检索**」；「服务支持 **Cloudflow**」；「**AI 安全防护支持图片防护**」 | W5 / W3 / W4 |
| 2025-12 | 「新增**风险管理能力**」；「自定义协议的 Model API 支持配置**路由级 fallback**」；「对于**非安全的鉴权插件**进行风险提示」；「同步自 Nacos 的 MCP Server 支持移除和编辑域名」；「支持代理 **vertex AI 上的 gemini3** 模型」；「代理的 **Azure openAI** 服务支持不包含 deployment-id 的 endpoint 格式」 | W4 / W3 / W5 |
| 2026-01 | 「Model API 支持 **Vertex AI 的原生 Gemini 协议**，覆盖 Gemini、Nano Banana、Veo3 等模型」；「在 Dify 的模型供应商中提供官方 **Higress 插件**，方便用户接入 AI 网关代理模型」；「百炼 Agent API 支持接入 **AI 安全护栏**」；「MCP Server 支持 **JWT 认证**」（🔴 **此条与 MCP 消费者认证专页「目前仅支持 API Key」直接冲突，且按 R4 优先级本条〔带日期发布记录〕高于专页〔静态页〕→ 裁决 C9 已据此修订，对客须实测**，见 §15.7 与 [-auth §6.4](aliyun-ai-gateway-auth.md)） | W3 / W5 / W4 |
| 2026-02 | 「支持百炼 **Embedding 原生协议**」；「Agent API 支持 **AI 可观测**」；「Agent API 支持**调试能力**」；「新增 **API 创建模板**，快速创建简单文本模型代理与高可用模型代理」；「**Agent 服务支持配置内网 DNS 解析**」；「更新百炼 Anthropic 兼容接口标准」 | W5 / W7 / W3 |
| 2026-03 | 「支持百炼语言识别 **Fun-ASR** 及 **Qwen3-vl-embedding** 模型」；「支持**模型日志字段参数映射**，将模型返回的字段与网关的日志字段映射」；「**Bedrock** 服务支持 **Prompt Caching** 配置，可降低推理成本和响应延迟」；「**Claude** 服务支持 **ClaudeCodeMode** 配置，解决 Claude Code 对接时的鉴权冲突问题」；「AI 安全护栏防护维度新增**自定义 Agent（CustomLabel）**」；「创建 AI 服务时，**Bedrock 供应商支持选择端点模式（Mantle 或 Runtime）**，Mantle 模式下自动使用 Anthropic 协议且**不支持 Prompt Caching**」 | W3 / W4 / W7 |
| 2026-04 | 「支持 **AI 安全护栏脱敏能力**，包括**文本脱敏和图片脱敏**」；「支持**自定义配置 AI 安全护栏的返回信息**」 | W4 |
| 2026-05 | 「**AWS Bedrock** 服务支持 **Anthropic 协议**调用」；「支持对接安全护栏**自定义 Agent 规则**，支持返回拦截信息及对应 **RequestID**」 | W3 / W4 |
| 2026-06 | 「支持接入 **KlingAI** 等类型的文生图、文生视频模型」；「支持 **VertexAI Claude** 模型的 **OpenAI 与 Anthropic** 访问协议」；「支持 **AI 服务多 API Key 场景下的 Failover**，提升模型调用的稳定性与成功率」 | W3 |
| 2026-07 | 「自定义 Model/Agent API 支持 **HTTP 重写**」；「安全护栏支持**并行检测配置**」 | W3 / W4 |

来源：[官方｜new-feature-release-notes-ai-gateway]

[文档未说明] 🔴 发布记录**没有任何「下线 / 停止服务 / 不兼容变更」类型的条目**（14 个月度小节出现的变更类型只有：新功能、优化、修复、开服、新商品）→ SA 无法从本页获知任何能力的废弃时间线。典型缺口：「Serverless（旧）」何时停售、引擎 2.1.20 用「请求/响应采集能力」**替代** Lua 插件打印日志后旧方式何时下线 —— 均无日期。
[文档未说明] 每条发布记录的**生效范围**（哪些实例类型 / 哪些地域 / 是否需升级引擎版本才生效）—— 全表无一条标注，唯一例外是 §2.10 的「≥ 2.1.15」。
[文档未说明] 发布记录未覆盖 2025-05 之前的历史（AI 网关的商业化发布时间点）—— 查无。
[文档未说明] 「最低 0 起步」的「最低」是何含义（是否指标准版）—— 2026-07 原文未展开。

### §2 溯源

- `ai-gateway-capacity-description` — 网关类型（15992 B）：§2.1 实例类型概览与「实例型独享版」命名；§2.2「如何选择」6 行表、典型场景推荐 8 行表、迁移建议 3 条、新版 Serverless 6 项优势、命名规范原文；§2.3 四形态能力对比 12 行表全量、标准版 5 条使用限制与 2 条 FAQ、企业版 4 场景 + 5 优势 + 使用建议、独享版 5 场景 + 4 优势；§2.5 服务等级四档（99.9 / 99.95 / 99.95 / 99.99）与「以控制台 / SLA 协议页面为准」2 处推诿原文；§2.11.5「TLS policy」术语 3 次出现但无定义；§2.11.8「部分高级能力不开放」用于 WAF 推断
- `capacity-description` — AI网关-容量规格与资源配额（7972 B）：§2.1「Serverless 版 / 专享实例版」+ Small/Medium/Large 三档命名、`aigw` vs `apigw` 前缀矛盾；§2.4 专享实例版 10 档 QPS 与客户端连接数全表；§2.6 全局配额 4 项；§2.7 实例配额 10 项 × 13 规格全表（含最后 3 行合并单元格还原说明）、白名单失去 SLA 承诺的警告原文、K8s 服务来源数矛盾方；§2.8 消费者数量 / 消费者授权规则数计算口径专节全文
- `supported-regions` — AI 网关开服地域（1985 B）：§2.9 公共云 15 地域 + 金融云 1 地域全表、「资源创建成功后不能更换地域」原文、全角/半角数字不一致
- `engine-version-description` — AI 网关引擎版本说明（5988 B）：§2.10 全部 20 个版本（2.1.4~2.1.23）的版本号 / 发布时间 / 描述、MCP 能力演进主线、envoy / Istio / pilot agent 线索、`finopts` 笔误；§1.3 被动健康检查引入版本
- `create-a-gateway-instance` — 创建 AI 网关实例（14377 B）：§2.11.1 购买页 11 个配置项全表（含 CDT 公网流量连带计费、VPC 一致性约束、自动分配 2 可用区、SLS 连带开通、SLR 自动创建、1~5 分钟创建耗时、64 字符名称上限、Serverless 无网关规格）；§2.11.2 Gzip 硬件加速全部限定条件（创建期-only、Serverless 不支持、7 地域、aigw.medium.x1 以上）、压缩比 10%~50% 统计口径、CPU 压测 4 行表、节省约 75% 实例资源结论、`EnableGzipHardwareAccelerate` 参数矛盾方；§2.1 `aigw.medium.x1` 交叉证据
- `modifying-gateway-parameter-configurations` — 修改网关引擎参数（6988 B）：§2.11.7 全部 20 个参数的名称 / 类型 / 取值范围 / 默认值 / 描述、"仅支持控制台开放参数"约束、12 条 SA 决策点、`EnableHttp2` 缺失矛盾方、`EnableGzipHardwareAccelerate` 缺失矛盾方
- `create-a-domain-name` — 创建域名（6438 B）：§2.11.3 备案前提（中国地域需备案 / 海外不需）、泛域名与证书的重要限制、HTTP 80 / HTTPS 443、强制 HTTPS 行为、HTTP/2 三档开关与 `EnableHttp2` 引用、TLS 最小 1.0 / 最大 1.3 默认值、14 条默认加密算法套件、mTLS 默认关闭、资源组、curl 验证命令；§2.11.5「指定加密套件在 TLS1.3 不生效」矛盾方
- `setting-the-specified-https-cipher-suite` — 设置 HTTPS 加密套件（4253 B）：§2.11.5 14 条套件与各自支持的 TLS 版本列表全表、加密套件三部分构成原文、自定义套件配置路径、curl --ciphers 验证命令与判定标准；TLS 1.3 矛盾方
- `set-security-group-rules` — 配置安全组授权规则（6475 B）：§2.11.4 托管安全组机制、授权方向、生成规则属性（允许 / 优先级 1 / 自定义 TCP）、端口范围语法（`1/65535`、`8080/8080`）、ACK 与 ECS 两条获取路径、级联删除陷阱、实例删除后残留安全组与 `DependencyViolation.SecurityGroup` 清理流程（含 ROS 资源栈）、2 条排障 FAQ、「购买时需选择 VPC 和安全组类型」矛盾方
- `configure-dns-server` — 配置 DNS 服务器（1597 B）：§2.11.6 DNS 服务器上限 5 个、3 类使用场景、服务级配置入口、一键填充内网 DNS 逻辑、`IP:端口` 手动格式、PrivateZone 依赖
- `view-gateway-instance-details` — 查看网关实例详情（1006 B）：§2.11.8 三个信息区域字段、基本信息页签 5 项可操作、「Serverless版AI网关不支持开启WAF防护」；§2.11.4 安全组可查的交叉证据
- `delete-a-domain-name` — 编辑或删除域名（799 B）：§2.11.3 编辑 / 删除路径与「输入当前域名」二次确认
- `change-the-protocol-and-certificate-of-the-domain-name` — 更换域名协议和证书（1079 B）：§2.11.3 更换协议 / 证书路径、3 类触发场景、「HTTPS 协议必须关联 SSL 证书」、端口 80 / 443；§1.4「云原生API网关」串味证据
- `new-feature-release-notes-ai-gateway` — 新功能发布记录（14419 B）：§2.12 全部 A~G 分组时间线（2025-05 ~ 2026-07 共 14 个月度小节）；§2.5 公测 + 免费矛盾方与 2025-09 Serverless 发布锚点；§2.9 开服地域矛盾方；§2.10「≥ 2.1.15」唯一显式版本门槛；§2.7「资源配额扩大」无数字信号
- `what-is-an-ai-gateway` — AI 网关产品概述（19843 B）：§2.7「最多可关联 3 个容器集群」矛盾方；§2.11.6 AI 服务 / DNS 服务的自定义 DNS Server 能力；§2.11.8 WAF 无限定矛盾方
- `product-comparison` — AI 网关与 Higress 开源版对比（3748 B）：§2.5 SLA 99.99% 无限定矛盾方；§2.11.8 WAF 无限定矛盾方；§2.11.1「多可用区部署 支持」交叉证据
- `api-product-introduction` — API 产品概念介绍（1697 B）：本章未直接引用（内容全部落在 §1.6）

**本章查无**（翻过但文档确实没写、SA 会被问到的高价值问题）：
1. 🔴 **QPS 的口径定义**（HTTP 请求 QPS 还是 AI 请求 QPS、是否区分流式、是否与 token 吞吐挂钩）—— LLM 容量规划的头号空白
2. 🔴 **Serverless（旧）的具体规格档位、QPS、客户端连接数** —— 官方原文「以原版本规格为准」，数字被推走
3. 🔴 **Serverless 标准版 / 企业版的客户端连接数上限、自动扩容 Unit 上限与 Unit 单价** —— 全部查无，Serverless 报价无法从文档算出
4. 🔴 **专享实例各规格的单价 / 实例费 / 起步费金额** —— 官方 2 次「请以产品控制台、官网价格页…为准」，文档级空白（归 W2 复核）
5. 🔴 **各规格对应的节点数、单节点 CPU / 内存、Pod 规格**，以及节点数与 QPS 上限的关系、能否手动指定节点数
6. 🔴 **规格在线升配 / 降配是否支持、是否需重启、变配耗时** —— 只有「供购买或升级实例时参考」一句暗示
7. 🔴 **超出规格 QPS / 连接数后的行为**（限流？降级？错误码？）—— 查无
8. 🔴 **引擎版本的升级方式**（自动 / 手动）、是否需重启、能否回滚、能否指定版本、Serverless 是否有版本裁剪 —— 全部查无
9. 🔴 **引擎是否基于 Higress** —— 只有 envoy / Istio / pilot agent / Higress 插件 4 条间接线索，无明文等式
10. 🔴 **20 个网关引擎参数中 19 个的生效方式**（需重启 or 热生效）—— 只有 `DownstreamIdleTime` 写了「重启才会生效」
11. 🔴 **`EnableHttp2` 与 `EnableGzipHardwareAccelerate` 两个参数的默认值与取值范围** —— 被其他页引用但参数表里没有
12. 🔴 **购买页是否有「安全组 / 安全组类型」配置项**，以及安全组类型（普通 / 企业级）的可选项与影响
13. 🔴 **配额提升（白名单）的申请入口、审批时效、可提升上限** —— 只说了提额会失去 SLA 承诺
14. 🔴 **各地域支持的实例类型差异**（Serverless 标准版 / 企业版是否全地域可用）、金融云地域的能力裁剪 —— 查无
15. 🔴 **韩国 / 马来西亚 / 亚特兰大 3 个「已开服」地域为何不在地域表里** —— 矛盾双方原文都在，无解释
16. **配额表缺失的对象**：API 产品数、产品分类数、证书数、密钥数、AI 缓存条目数、Model API 数、MCP 工具数、虚拟 MCP Server 数、安全组授权条数、日志 Logstore 数
17. **「消费者配额规则数」的计算口径** —— 官方专节只解释了另外两项
18. **「在线路由总数」的计数规则**（一条 Model API 含多条自定义路由如何计）、「发布域名数」与域名管理页条目的口径关系
19. **DNS 服务器 5 个上限的作用域**（每服务 / 每实例 / 每 Region）；DNS 超时 / 重试 / search domain / 是否支持域名形式
20. **内网 DNS 服务解析（PrivateZone）是否独立开通、独立计费** —— 潜在连带计费空白
21. **公网入口能否后开**（只说了「支持开通公网后关闭公网」）；「接入点」的定义 / 数量上限 / 移除影响
22. **网关默认监听端口清单**；「管理端口」可改哪些端口、端口范围
23. **「TLS policy」的可选值清单** —— 术语被引用 3 次，无一处定义
24. **TLS 1.0 / 1.1 是否有下线计划**；是否支持国密套件；是否支持 SNI 多证书；TLS 会话复用 / OCSP Stapling
25. **证书总数配额、证书到期告警 / 自动续期**
26. **删除域名是否级联删除关联路由 / 证书绑定、是否有引用检查**
27. **Gzip 硬件加速是否额外计费**；「核心地域」指哪些地域；brotli 是否也有硬件加速；「aigw.medium.x1 以上」是否含 x1 本身
28. **「重启网关」是否中断流量、耗时多久**；实例「运行状态」的完整状态机
29. **开启 WAF 是否连带开通 WAF 产品并独立计费**；WAF 的额外内存开销数字
30. **多可用区**：是否支持 3 AZ、跨 AZ 容灾的 SLA 口径、单 AZ 故障时的行为
31. **发布记录的生效范围**（每条新功能适用哪些实例类型 / 地域 / 最低引擎版本）—— 全表无标注
32. **任何能力的下线 / 停售时间线**（含 Serverless（旧）停售时间、Lua 日志打印方式的下线时间）
33. **AI 网关的商业化发布时间点**（发布记录只到 2025-05）

### 边界内容移交提示（本章读到但建议归其他 worker 落地）

| 内容 | 所在 slug | 建议归属 |
|---|---|---|
| 计费方式（实例费 / 起步费 / 按量）、SLA 赔付档位、CDT 公网流量单价、SLS 连带计费 | ai-gateway-capacity-description、create-a-gateway-instance | **W2** |
| 日志字段说明全表（`ai_log` 及其 12 个子字段 api/cache_status/consumer/fallback_from/input_token/llm_first_token_duration/llm_service_duration/model/output_token/response_type/safechack_status[原文如此]/token_ratelimit_status，以及 authority、bytes_received、duration、request_id、trace_id、upstream_service_time 等 24 个通用字段） | create-a-gateway-instance | **W7** |
| 消费者 / 消费者组 / 消费者配额规则的业务语义与 FinOps 落地 | capacity-description、new-feature-release-notes-ai-gateway | **W3 / W4** |
| 服务类型 9 类的配置字段、健康检查参数、智能路由、Fallback、AI 缓存 | what-is-an-ai-gateway、new-feature-release-notes-ai-gateway | **W3** |
| 消费者鉴权 4 类算法（含 oauth2 口径冲突）、KMS 托管、IP 黑白名单、AI 安全护栏 5 维度与 4 档策略的落地配置 | what-is-an-ai-gateway、product-comparison | **W4** |
| MCP 三类接入、虚拟 MCP Server、Tool 组装、语义检索、工具级授权 | what-is-an-ai-gateway、engine-version-description、new-feature-release-notes-ai-gateway | **W5** |
| 插件数量配额的语义（同时启用 vs 累计安装）、自定义插件开发 | capacity-description | **W6** |
| 专属告警指标 3 个（AIGatewayEnvoyCpuUsageRate / MemoryUsageRate / PluginCrash）、访问日志域名采样规则 | new-feature-release-notes-ai-gateway、engine-version-description | **W7** |
| API 产品管理 / 门户管理 / 产品分类管理（HiMarket） | api-product-introduction、new-feature-release-notes-ai-gateway | **W7**（开发者门户）|
| 7 个集成配方相关信号（PAI-EAS、ComfyUI、Dify、Claude Code / ClaudeCodeMode、Vertex AI、响应压缩 = Gzip） | new-feature-release-notes-ai-gateway、create-a-gateway-instance | **W7** |

---

## §14 实战避坑（含真实客户案）

> 本章 = 主控汇编。素材来源两类：① 7 路蒸馏员在各专题页标出的高价值陷阱；② **2026-09-21 合思（易快报）AI 网关鉴权阻塞案**的真实对客材料，已归档 `raw/misc/practice-2026-09-21-hesi-aigw-auth-{customer-reply,internal-decision}.md` 与群聊原始记录 `practice-2026-09-21-hesi-chat-raw.md`。
> 🔴 **`internal-decision` 那份含对同事既有口径的纠正与产研需求，标注「勿外发」，不得整篇或片段转发给客户。**

### 14.1 🔴 自建认证鉴权：404 是设计行为，不是 bug（合思案根因）

**现象**：客户已有认证接口 `GET /api/mcp/personal-tokens/verify`（精确匹配、用 `Authorization` 头收 PAT），挂到 AI 网关「自建认证」后全量 404，被当成网关故障在售后通道处理了 4 天。

**根因（官方明文，`[官方原文｜configure-self-built-authentication]`）**：以下三段均已由主控回源逐字核对 ——
第 1 段在 raw **第 33 行**（正文散文，逐字一致）；第 2、3 段在 raw 的**配置项 HTML 表格单元**内
（「鉴权API」单元与「模式」单元，原文第 3 段是 `<ul><li>` 两项列表，此处按契约允许的格式归一化展平为散文，
**去标签去空白后与 raw 逐字一致**，已用脚本双向比对验证）：

> 假设自建鉴权服务的鉴权API是/validateToken，那么鉴权请求的真实Path是鉴权API加上原始业务请求的Path后的结果，即/validateToken/order。

> 设置鉴权服务提供的鉴权API的Path，API的Path需是前缀匹配。

（紧接的官方示例：「您的鉴权服务基于SpringMVC构建，对外开放的鉴权API为/check，那么处理/check/的请求设置如下：`@RequestMapping("/check/")`」）

> 支持宽松模式和严格模式，建议您使用宽松模式。  宽松模式：当鉴权服务不可用时（鉴权服务建立连接失败或者返回5xx请求），网关接受客户端请求。  严格模式：当鉴权服务不可用时（鉴权服务建立连接失败或者返回5xx请求），网关拒绝客户端请求。

**三条合起来的含义**（主控归纳）：① 真实鉴权 Path 是**拼接**出来的，不是原样转发；② 鉴权 API 的 Path **必须是前缀匹配**；③ 宽松模式的兜底触发条件被官方**穷举**为「建立连接失败 **或者** 返回 5xx」——**4xx 不在其中**。

🔴 **更狠的一层（`[推断]`，推理链已在 [§6.6](aliyun-ai-gateway-auth.md) 展开）**：客户的精确匹配接口返回 **404**，属 4xx，不在宽松模式覆盖范围内。所以：

> **即使开了官方推荐的宽松模式，也无法兜底，仍然全量拒绝。**

**同页还有两个同源陷阱**：
- 同一页有**两个不同的「Path 匹配」概念**：鉴权 API 的 Path **仅前缀匹配**，而授权规则的 Path **支持精确/前缀/正则**。客户极易混。
- 复杂条件里 `safe_regex_match.regex`「**需要完全匹配，而非部分匹配**」→ 写 `test.exampleA.com` 这类不完全正则会**不命中即无需鉴权直接放行**，是**放开而非收紧**，属安全事故面。

**解法（`[开源]` 证据，Higress 源码 `plugins/wasm-go/extensions/ext-auth/main.go`）**：ext-auth 插件有两种 `endpoint_mode`，其中 **`forward_auth`** 模式固定 path、不拼接原始请求 Path，且 `Authorization` 头源码级无条件透传 → **客户的精确匹配认证接口零改动**。
🔴 群里从 9/18 到 9/21 没有人提过这个模式；「你把 SpringMVC 改成前缀匹配」是客户明确拒绝的方案。**正确答案在客户已经打开的那个插件里。**

🔴 **证据等级与前置实测要求（A5-3 修正）**：`ext-auth` / `endpoint_mode` / `forward_auth` 三个词在 **186 个 AI 网关官方快照里 0 命中**（实测 `grep -ril`），官方唯一相关记载是 `upload-plug-in` 插件优先级总表里的一行「外部认证｜插件｜认证阶段｜300」，**不含任何配置项说明**。故此解法的证据是 **Higress 开源侧**（`[开源]`）而非 AI 网关官方文档，**AI 网关控制台的「外部认证」插件是否暴露 `endpoint_mode` 配置项属 `[文档未说明]`** → 🔴 **对客给出此方案前必须在客户的 AI 网关实例上实测确认该字段存在**，否则会被客户判为给错方案。

**SA 教训**：客户说「网关有 bug」时，先查官方文档里的**设计行为条款**（「需是」「会拼接」「不支持」这类限定词），再查插件的**配置模式枚举**。这两处藏着绝大多数「疑似故障」。

### 14.2 🔴 MCP 工具级鉴权到底管不管 tools/list（合思案的口径纠正）

同事断言「http转mcp 场景 tools/call 能走外部认证插件，但 initialize 和 tools/list 不行」。**该断言无文档支撑，且与官方原文直接冲突**：

`[官方原文｜debug-mcp-services]`：
> 「如果所选消费者只授权了 MCP工具级别消费者认证，且仅授权某些工具的情况下，**HTTP转MCP的场景中获取工具列表只能看到和调用有权限的工具**；直接代理场景调试的时候能看到全部工具，选择授权的工具调用是ok的，没权限的会403。」

→ HTTP转MCP 下工具级鉴权**就是作用于 tools/list 的**（表现为**按权限过滤**，不是拒绝整个列表）；直接代理场景 tools/list 能看全部，拦截点在 **tool 调用**（403）。

**架构上也不自洽**：MCP 规范把鉴权放在传输层，Streamable HTTP 强制「单一 MCP endpoint，每条 JSON-RPC 消息都是一次新的 HTTP POST」。`initialize`/`tools/list`/`tools/call` 在 HTTP 层**同 path 同 method**，而 ext_authz 跑在 MCP 协议解析之前 → **物理上无法按方法区分**。

**SA 教训**：「某方法能、某方法不能」这类断言，要么有官方原文，要么能被协议层结构解释。两者都没有时**不要转述给客户**，先回源核。详见 [§8.10.3](aliyun-ai-gateway-mcp-agent.md)。

### 14.3 通道错配比技术难题更耗时（合思案的流程教训）

客户真实诉求是 **MCP 上架入驻千问办公生态**，却被当成网关配置故障在售后（AES）通道里处理了 4 天。这是**流程错配，不是能力问题**。
**SA 教训**：接客户问题时先判「这是配置故障 / 产品能力咨询 / 生态入驻诉求」，第三类的正确通道不是售后。

### 14.4 Fallback 默认会在「被限流」时也触发（W3 发现，极易漏）

`[官方｜ai-fallback]`：Fallback 默认在「被网关限流或其它形式拦截」时**也会**触发，除非开启「**仅Fallback后端服务错误**」。
→ 🔴 限流命中的流量会**打到备用模型**，绕开客户预期的「限流即拒绝」语义，并产生**额外调用量与额外 Token 费**。
**SA 教训**：客户同时配了 Token 限流 + Fallback 时，必须提醒这一条，否则账单会超出预期且难以归因。原文藏在一个表格单元格里。

### 14.5 计费侧的反直觉点（W2 发现）

| 陷阱 | 事实 | 对客影响 |
|---|---|---|
| **「全走内网更便宜」在数据处理量这项上不成立** | 专享实例**私网 0.049 元/GB/h > 公网 0.037 元/GB/h** `[官方｜free-product-templates]` | 客户按直觉做网络设计会算反 |
| **Model API 的 CU 系数是 Agent API 的 5 倍** | Serverless（旧）CU 系数 Model API **10** / MCP Server **5** / Agent API **2** `[官方｜serverless-old-billing-details]` | 混用三类 API 时成本结构完全不同 |
| **Serverless（旧）有账单地板** | 「CU 数不足 10 万按 10 万计算」→ 内地 **0.50 元/小时**兜底（`[推断]` 100000÷1000×0.005） | 低频/空闲实例不是「不用不花钱」。⚠️ 官方未说明地板是按实例还是按账号统计 |
| **AI Credits 是独立商品，网关账单里看不到** | 「独立的按量付费开通型商品，与网关实例的基础计费相互独立」；须**先建实例再单独开通**；「不设置包量」 | 🔴 **报「AI 网关总成本」至少三本账**：网关账单 + AI Credits 账单 + 模型服务账单 |
| **金融云 = 内地 × 1.9**（专享实例） | 实例费用表有金融云档，Serverless（旧）**无金融云行** | 🔴 禁止用公共云 0.005 元/千CU 外推金融云 |

### 14.6 SLA 的「无赔偿区」（裁决 C2，本次最高商务风险发现）

| 形态 | 产品页宣称服务等级 | SLA 协议承诺 | SLA 赔偿首档起点 | 缺口 |
|---|---|---|---|---|
| Serverless 标准版 | 99.9% | serverless 实例 ≥99.90% | 低于 99.90% | 无 |
| **Serverless 企业版** | **99.95%** | serverless 实例 **≥99.90%** | **低于 99.90%** | 🔴 **[99.90%, 99.95%) 无赔偿** |
| **Serverless（旧）** | **99.95%** | serverless 实例 **≥99.90%** | **低于 99.90%** | 🔴 **同上** |
| 实例型独享版 | 99.99% | 普通实例 ≥99.99% | 低于 99.99% | 无 |

赔偿方式**仅限代金券**，总额不超过当月该实例月度服务费用（不含代金券抵扣部分）；三档 15% / 30% / 100%；申请须在次月第 5 个工作日后、且**不晚于相关月份结束后 2 个月**。
🔴 **对客不得用产品页的 99.95% 主张赔偿。** 详见 [§3.9](aliyun-ai-gateway-billing.md)。

### 14.7 配额与形态的硬门槛（W1 发现）

- 🔴 **Serverless 标准版不能接容器服务来源**：标准版「K8s服务来源数 = **N/A**」「上传自定义插件数 = **N/A**」，且官方明写「标准版不支持自定义插件」→ `[推断]` **需要 ACK/ACS 后端的客户必须选企业版或独享版**。
- **标准版配额极小**：MCP Server 数 **20**、在线路由总数 **200**、发布域名数 **20**、服务数 **50**、消费者/授权规则/配额规则各 **100**、安装插件数 **5**。→ 只适合 PoC 与开发测试，**不要拿标准版报价生产**。
- 🔴 **突破配额白名单后官方明示「不作 SLA 承诺」** → **提额＝弃 SLA**，这是商务争点，方案里必须写明。
- **配额表缺 10 类 SA 高频被问对象**：API 产品数、产品分类数、证书数、密钥数、AI 缓存条目数、Model API 数（只有「在线路由总数」）、MCP 工具数（只有 MCP Server 数）、虚拟 MCP Server 数、日志 Project/Logstore 数、安全组授权条数。

### 14.8 RAM 与多租户的架构级结论（W4/W7 发现）

- 🔴 **多租户隔离无法靠 RAM 资源级授权实现**：SLR 三个角色的 **`Resource` 全为 `"*"`，无资源级收窄**；140 个 Action 中 **66 个（47.1%）** 标「全部资源」；**MCP / AI 模型元信息 / 消费者组 / 插件四类对象在 RAM 层面根本没有 ARN 定义** → 只能**分账号或分实例**。对客讲多租户方案时必须先说这条。
- **管理员全权限策略名有两个**（`AliyunAPIGFullAccess` 与 `AliyunNativeApiGwFullAccess`，裁决 C8 未裁）→ 授权指引里**两个都给**，授权失败换另一个试。
- **SLR 会连带操作大量其他云产品资源**：`AliyunServiceRoleForNativeApiGw` 原文 166 行 / 去重 **165** 条 Action，9 个产品前缀 —— `slb` 45（含唯一重复项 `slb:ModifyLoadBalancerInternetSpec`）、`nlb` 30、`ecs` 28、`arms` 20、`vpc` 19、`cs` 11、`fc` 6、`mse` 4、`edas` 3；另有 `InvokeFC` 1 条、`InvokeKMS` 12 条。**三个 SLR 合计 179 条 / 去重 178 条**。含 **11 个 `Delete*`/`Release*` 删除类 Action** 与 `arms:OpenArmsService`、`arms:AddPrometheusInstance` 这类**开通类** Action。
  → 🔴 **连带账单至少 6 类**：公网流量/CDT、SLS 日志、云监控企业版或 Tracing、模型服务、KMS、AI 安全护栏商品（`lvwang_guardrail_public_cn`）。**单价文档全部未说明** → **AI 网关账单 ≠ 全成本**，与 [[aliyun-agentcore]] 的「依赖产品独立计费」同一对客话术。
- **「内容安全」所需的 SLR 角色名查无**：`content-security-protection` 说「开启内容安全防护策略前，需授权服务关联角色」但**未给角色名**，而 SLR 页 3 个角色中**无任何内容安全/绿网相关角色**（`[官方矛盾]`）。
- **AI 安全护栏的「恶意文件检测」与「数字水印」：能力已官宣，落地方式未文档化**（🔴 2026-09-21 主控修正，原写「不要对客承诺」过严，且与本页 §1.2 自相矛盾）：产品概述页 `what-is-an-ai-gateway` **明文列出 5 个防护维度**，含 `maliciousFile` **恶意文件检测** 与 `waterMark` **数字水印标识**（raw 第 236/238 行，见本页 §1.2 与 §2.3 表）；但**专页 `content-security-protection` 全页查无这两个词**，只有「恶意URL检测」，**没有任何配置项、参数、开关或生效说明**。
  → **对客口径**：可以说「产品规划了这两项能力（官方产品概述页有列）」，🔴 **但不能承诺「照文档能配出来」**，也不要给客户演示配置路径；客户明确要这两项时**转 AI 安全护栏商品侧（`lvwang_guardrail_public_cn`）确认或走工单**。这是典型的「概述页有能力清单、操作页无落地文档」型缺口。

### 14.8a 🔴 三个 Action 计数必须消歧（R2a 判定 P1：57 / 140 / 179 常被混为一谈）

本知识库里出现三个不同的「Action 条数」，**它们说的是三件完全不同的事**，混用会直接导致权限方案做错：

| 数字 | 是什么 | 谁调谁 | 来源 | 用途 |
|---|---|---|---|---|
| **179 条 / 去重 178** | **AI 网关自己的服务关联角色（SLR）**里的 Action | **AI 网关服务** → 代客户操作**其他云产品**（SLB/NLB/ECS/ARMS/VPC/CS/FC/MSE/EDAS/KMS） | `service-association-role-…`（本页 §14.8） | 判断「开通 AI 网关会连带创建/操作哪些资源」、「账单 ≠ 全成本」 |
| **140 个** | **AI 网关 OpenAPI** 的 Action 总数 | **客户/自动化脚本** → 调 AI 网关 | `api-apig-2024-03-27-overview-ai-gateway`（[-ops §13.1](aliyun-ai-gateway-ops.md)） | 判断「能不能用 OpenAPI 做 IaC」、流控配额、错误码 |
| **57 条 `apig:`** | **AgentCore 的 SLR** 里 `apig:` 前缀的 Action | **AgentCore 服务** → 调 **AI 网关的 OpenAPI** | [[aliyun-agentcore]] §SLR（`service-linked-role-1.md`） | 判断「客户用 AgentCore 为什么会连带产生 AI 网关账单」 |

🔴 **关键否证（主控 2026-09-21 实测）**：**AI 网关自己的 SLR 里 `apig:` 前缀 = 0 条**（正则提取全部 Action 后按前缀计数：`slb` 44 唯一 / `nlb` 30 / `ecs` 28 / `arms` 20 / `vpc` 19 / `kms` 12 / `cs` 11 / `fc` 7 / `mse` 4 / `edas` 3 = **178**）。
**含义**：AI 网关的 SLR **不含调用自身 OpenAPI 的权限** —— 那 57 条 `apig:` 只存在于 **AgentCore** 的 SLR 里，是 AgentCore 为了替客户建 MCP Server 而去调 AI 网关 API。**不要把 57 当成 AI 网关的权限面。**

⚠️ **提取陷阱（主控自己差点踩）**：裸正则 `"(prefix:Name)"` 会把该页里 **2 处 `ram:CreateServiceLinkedRole`**（用户侧要添加的权限策略，不是 SLR 的 Action）和 **2 处 `ram:ServiceName`**（Condition 键，根本不是 Action）一并计入，得到 **182** 条。**182 − 4 = 178**，与逐块解析结果一致。复算时务必按 `"Statement"` 块切分并排除 `Condition` 段。

### 14.9 会被客户照抄的官方错字（`[原文如此]`，照抄才对）

| 位置 | 错字 | 后果 |
|---|---|---|
| `enable-gateway-log-delivery` | 日志字段 `ai_log.safechack_status`（疑为 safecheck） | 🔴 **写 SLS 查询语句时必须照抄错字**，改对了查不到 |
| `proxy-dify-inbound-and-outbound-traffic-through-ai-gateway` | 负载均衡 YAML 键名 `Ib_config`（大写 I，疑为 `lb_config`）；「以**前提取**匹配负载均衡为例」（应为「前缀匹配」） | 客户照抄可能不生效，改对也可能不生效 → **必须先实测** |
| `geographic-location-of-ip` | 参数名字段表写 `ip_protocol`，同页示例与另一页示例写 `ipProtocal`（缺下划线且 protocol 拼错） | 照抄示例可能不生效 |
| `hmac-auth-plug-ins` | 示例里 consumers 命名 `consumer-1` 而 allow 列表写 `consumer1` | 🔴 **按此示例配置无人能通过鉴权** |
| `key-auth-plug-ins` | 403 错误信息写 "Request denied by **Basic** Auth check"；「实例级开启」正文写「开启 **Basic Auth** 认证」 | 复制残留，客户看到会困惑 |
| `engine-version-description` | `finopts`（应为 FinOps，2.1.19/2.1.20 两条） | 检索时两种拼写都要搜 |
| `creating-services` | AI 网关文档里写「并非由**云原生API网关**直接提供」「**云原生API网关**只能添加同VPC内的Nacos或者ACK」 | 产品名串用，别据此判断产品归属 |
| `manage-providers` | 「也可以创建自定义供应商，也可创建自定义供应商」（重复） | 无实质影响 |

### 14.10 slug ↔ 官方标题交叉错位（裁决 C6，🔴 最容易答错的一处）

| slug | llms.txt 官方标题 | 正文实际插件名 | 正文能力 |
|---|---|---|---|
| `ai-cue-template` | AI 提示词**插件** | **ai-prompt-decorator** | prepend/append，优先级 450 |
| `ai-cue-decorator` | AI 提示词**模板**插件 | **ai-prompt-template** | templates，优先级 500 |

第三方交叉验证：`geographic-location-of-ip` 页把 prepend/append 明确称为「AI提示词**装饰器**插件」。
🔴 **对客给配置示例时必须写插件名（`ai-prompt-decorator` / `ai-prompt-template`），不要写 slug，也不要引用官方标题** —— 标题与正文是错位的。

### 14.11 其他高频踩坑速记

- **AI 缓存 ≠ 浏览器缓存插件**：`ai-cache-1`（AI 语义/精确缓存，命中时输入输出 tokens 均为 0）与 `browser-cache-control`（cache-control 插件）是两个能力，客户常混。精确缓存「缓存时长默认为1800秒」，**语义化缓存无任何 TTL 配置项**。
- **压缩比 ≠ 节省率**：官方定义「压缩比 = 压缩后/原始」，故 2.8% ⇔ 节省 97.2%。LLM API 响应压缩实测**流式 92%–97%、非流式 28%–40%**（另有「最高可减少 90% 以上」与「可节省最高 97%」两处不同口径，均照抄未合并）。
- **TLS 1.3 下自定义加密套件可能不生效**（裁决 C12 未裁）：一页说 14 条套件全部支持 TLS 1.3，另一页说「协商结果为 TLS1.3 时不生效」→ 按保守方设计并实测协商结果。
- **限流是四套东西不是一套**：① 控制台 Model API 限流 ② OpenAPI Token 限流（`[推断]` 与①是同一策略 `AiTokenRateLimit` 的两个配置面，官方未明文声明）③ FinOps 消费者配额 ④ API 级流量控制/并发控制/熔断。④写了「Http状态码默认为429」；🔴 **①②的超限返回码在限流专页确实未写，但 `custom-response-plugin` 页明文「触发网关限流时一般会返回429状态码」并给了自定义应答样例** → **对客可答 429**（出处是自定义应答插件页，官方未说明它是否对全部限流单位一律成立）；**③ FinOps 配额超限的返回码仍全部 `[文档未说明]`**（只写「消费者将无法继续调用模型」），不可类推。
- **限流规则「10 条」是命中上限不是配置上限**：官方问答「最多可以配置多少条」→「最多只支持**同时命中** 10 条」，问答不对齐；**配置上限两页均未说明**。
- **插件延时只有两个数字**：`key-auth` **20 微秒**、`basic-auth` **30 微秒**，其余全部无数字只有「都是微秒级的」；另有一处 **0.19 毫秒**。**性能测试条件全缺**（实例规格/引擎版本/QPS/并发/报文大小/是否流式/测试日期）→ 🔴 **客户拿 0.19 毫秒做容量规划不可复现，不要背书**。
- **`DownstreamConnectionBufferLimits`**：两个插件页都要求客户调高并警告「内存使用将有显著增加」，但**无默认值、无上限、无内存增量数字**。
- **`jwt-logout` 在 Redis 不可用时的降级策略未说明**（放行还是拒绝），只给了 500 错误码 → 可用性风险点。
- **9 类资源配额在错误码页全是 `%s` 占位符** → 容量规划必须走配额中心/工单，不能从文档取数。
- 🔴 **A2A 协议转换确有官方明文（2026-09-21 主控修正，R2a 判定 P0-3，原断言为假）**：产品概述页 `what-is-an-ai-gateway` 第 125 行逐字「AI 网关通过服务发现功能，统一暴露部署于不同计算平台的 AI 应用，并**提供 REST 到 A2A 协议的转换能力**，实现存量 HTTP 应用向 A2A 协议的自…」；第 117 行「推荐**基于A2A协议通过Nacos AI Registry实现服务的注册与发现**」；第 29 行「AI应用常通过 **A2A** 等协议实现应用间的通信与调用」。**本页 §1.2（第 176 行）本来就正确收录了这三条**，是本条避坑把它们否掉了 → 同文件自相矛盾。
  **原断言的成因**：`-mcp-agent`（W5 分片 21 页）全文检索 A2A 确实零命中，主控把这条**分片级**否定外推成「189 页零命中」的**全库级**断言 —— 与 R1 查出的 5 处 D3 同一失效模式（`[文档未说明]` 被当「我这个分片没读到」用）。
  **仍然成立的空白**：A2A 的**配置方法、支持范围、是否有专门页面**在 189 页里确实查无（只有概述页的能力宣称）→ 对客可以说「产品提供 REST→A2A 转换能力（官方概述页明文）」，🔴 **但给不出配置步骤，落地前须实测或走工单**。。
- 🔴 **2026-09-21 主控修正（R2a 判定 P0-1，原断言为假）**：**OpenAPI 有 MCP 专用 Action** —— `api-apig-2024-03-27-overview-ai-gateway` 的「MCP管理」分组列出 **8 个**：`CreateMcpServer`、`UpdateMcpServer`、`GetMcpServer`、`ListMcpServers`、`DeleteMcpServer`、`DeployMcpServer`、`UnDeployMcpServer`、`SyncMCPServers`（同步 Nacos MCP 到网关）`[官方｜api-apig-2024-03-27-overview-ai-gateway]`（主控已回源 grep 实证 7 个不同名 + `DeployMcpServer` 出现 2 次）。**原断言的来源是 `-mcp-agent` §8.18 只读了「用 OpenAPI 管理 MCP 服务」那一页里的 6 个 Action**，那 6 个确实全是通用 HttpApi/Plugin 资源 —— 但**不能由此推出全量 OpenAPI 没有 MCP 专用 Action**（典型的分片视野外推）。本条与本页 §14.8/§15.10 引用的 `apig:CreateMcpServer`／`apig:DeployMcpServer`（AgentCore SLR 内）本来就该互相印证。
- **仍然成立的空白**：140 个 Action 中**无 Model API / Agent API / AI 服务 / AI 日志策略的专属 Action** → 「用 OpenAPI 管理 Model API」的映射关系 `[文档未说明]`；且这 8 个 MCP Action **零错误码**（一律推给「错误中心」）。
- **35 个 Action 无流控配额条目**（概览 140 vs 配额页 105，反向差集为 0）：**FinOps 配额规则 9 个、AI 模型元信息 10 个、消费者组 8 个整套全缺** —— 恰好是 AI 网关区别于云原生 API 网关的差异化能力。

---

## §15 SA 速查卡（对客必背）

### 15.1 一句话定位

AI 网关 = **云原生 API 网关面向 AI 原生应用的托管入口**，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，**兼容 OpenAI 协议**；支持 **Model API / Agent API / MCP Server** 三类接入。
`[官方原文｜官方 llms.txt 产品描述]` 🔴 **来源更正（2026-09-21 主控修正，R1 判定 D7 / DEF-7）**：本句原标 `[官方｜what-is-an-ai-gateway]`，实测这三个短语在 **186 个 raw 快照里 0 命中**，逐字出自**官方按产品 llms.txt 的产品描述行**（父级 `api-gateway/llms.txt` 与 `ai-gateway/llms.txt` 各 1 处，均已归档 `tests/api-gateway-parent-llms-2026-09-21.txt` 与 `tests/ai-gateway-llms-2026-09-21.txt`）。llms.txt 是**官方来源但等级低于文档正文**（它是索引摘要，非产品页），对客引用时宜表述为「官方产品简介」而不是「产品概述页原文」。产品概述页 `what-is-an-ai-gateway` 自身的定位表述见 §1.1。

### 15.2 产品族三兄弟（别搞混）

| 子产品 | 定位 | 状态 |
|---|---|---|
| **云原生 API 网关** | Envoy 内核 + 开源 Higress，流量网关/微服务网关/K8s Ingress 三合一 | 现役，本次**未蒸馏** |
| **AI 网关** | 面向大模型调用：多模型路由、Token 限流、内容审核、语义缓存、MCP、AI 安全护栏 | 现役，**本专题页家族** |
| **原 API 网关**（传统版） | RESTful/SOAP 托管 + SDK 自动生成 | 🔴 **2026-08-23 停止新购、2027-09-21 全面下线**，存量迁云原生API网关 |

### 15.3 形态选型（4 选 1）

| 形态 | 起步成本 | 计费方式 | 服务等级（产品页宣称） | 适用 |
|---|---|---|---|---|
| Serverless 标准版 | **0 元起步，无实例费** | 按实际用量 | 99.9% | PoC、开发测试。🔴 配额极小、不能接 K8s 服务来源、不支持自定义插件 |
| Serverless 企业版 | 实例费 **0.245 元/小时**（参考单价）+ 用量 | 实例费 + 按量 | 99.95% | 生产、需独立入口与自定义域名 |
| Serverless（旧） | CU 兜底 **0.50 元/小时**（内地，`[推断]`） | 仅按量（请求 CU + 公网流量） | 99.95% | 存量。官方建议新客户选新版 |
| 专享实例（实例型独享版） | 最低 `aigw.small.x1` **7.9335 元/小时** / **3,997.5 元/月**（内地） | 按量 或 包年包月 | 99.99% | 核心系统、需完整插件与自定义插件 |

🔴 **报价铁律**：以上「参考单价」与实例费均需走购买页核验；**金融云 = 内地 × 1.9**（专享实例）；不给单价的地域禁止外推。

### 15.4 三本账（🔴 客户问「多少钱」必答）

```
AI 网关总成本 = ① 网关账单（实例费 + 数据处理量 + 公网流量）
              + ② AI Credits 账单（0.01 元/Credit，独立商品，须先建实例再单独开通，网关账单里看不到）
              + ③ 模型服务账单（百炼/第三方/自建）
              + ④ 连带云产品（公网流量〔🔴 专享实例走 CDT 统一出账；Serverless 新版由网关侧按 0.8 元/GB 计入网关账单，自配 NAT 则出网部分不在网关侧计费〕 / SLS 日志 / 云监控企业版或 Tracing / KMS / AI 安全护栏商品）—— 除公网流量外单价文档全部未说明
```

关键单价（内地，快照时点）：专享实例数据处理量 **公网 0.037 / 私网 0.049 元/GB·小时**（🔴 私网更贵）；Serverless（旧）CU **0.005 元/千CU**，CU 系数 **Model API 10 / MCP Server 5 / Agent API 2**，**不足 10 万按 10 万计**；公网流量走 **CDT** 统一出账。

🔴 **Credits 折算率要分两侧说**（2026-09-21 主控修正，原写「全库查无」过宽，经 R1 回源判定为 D3）：**模型调用侧有文档** —— 模型元信息可配「输入/输出/缓存 Credits 单价」，「单位 **Credits/1M tokens**，如填写必须为大于等于 0 的数字，最多两位小数，**默认值为 0**」`[官方原文｜model-metadata]`，故原则上可算（Token 量 × 单价 ÷ 1M），但默认 0 且官方未说明填 0 的后果；**AI 增强能力侧才是真空白** —— 「一次智能路由消耗几个 Credit」、按请求还是按 Token 还是按候选模型数折算、语义检索与工具精选是否消耗 Credits，**全部 `[文档未说明]`** → 这三项的成本无法估算，必须工单确认。详见 [§3.5.4](aliyun-ai-gateway-billing.md)。

### 15.5 SLA（🔴 必须带实例类型说）

| SLA 协议承诺（法律口径） | 赔偿 |
|---|---|
| **普通实例 ≥99.99%** ／ **serverless 实例 ≥99.90%** | 三档 **15% / 30% / 100%** 月度服务费用，**仅限代金券** |

计算口径：服务周期 = 一个自然月；可用性 = （1 − Σ每5分钟错误率 / 5分钟总个数）×100%；错误率 = 每5分钟失败请求数 / 每5分钟有效总请求数。
申请时限：次月第 5 个工作日后，**不晚于相关月份结束后 2 个月**。
🔴 **企业版/旧版 Serverless 的 [99.90%, 99.95%) 是无赔偿区**（裁决 C2）；除外情况 11 条（用户配置/后端服务/客户端/公网二级域名/超配额/欠费/黑客攻击等）不计入失败请求。协议生效日 **2025-09-10**。

### 15.6 容量规格（专享实例，10 档）

| 规格 | QPS | 客户端连接数 | 按量单价（内地，元/小时） |
|---|---|---|---|
| aigw.small.x1 | 1,500 | 20,000 | 7.9335 |
| aigw.small.x2 | 3,000 | 40,000 | 15.1782 |
| aigw.small.x4 | 6,000 | 80,000 | 28.7287 |
| aigw.medium.x1 | 12,000 | 160,000 | 56.1 |
| aigw.medium.x2 | 24,000 | 320,000 | 110.484 |
| aigw.medium.x3 | 36,000 | 480,000 | 164.864 |
| aigw.large.x1 | 48,000 | 640,000 | 213.7668 |
| aigw.large.x2 | 96,000 | 1,280,000 | 425.8527 |
| aigw.large.x3 | 144,000 | 1,920,000 | 637.9425 |
| aigw.large.x4 | 192,000 | 2,560,000 | `[文档未说明]`（规格表有、价格表无此档） |

🔴 **QPS 口径官方无定义**（HTTP QPS 还是 AI QPS？是否区分流式？与 token 吞吐何关系？）—— **LLM 容量规划的头号空白，不要拿这张表直接承诺客户的大模型并发能力**。
⚠️ 官方压测曾跑到 aigw.medium.x1 **13000 QPS**，高于标称 **12000**（`[官方矛盾]`）。

### 15.7 地域

公共云 **15 个地域** + 金融云（详见 [§2](#§2-实例形态与容量规格)）。
🔴 发布记录里提到 2025-08 韩国、2025-12 马来西亚、2026-03 亚特兰大「开服」，但 `supported-regions` 公共云表**这 3 个地域全部不存在**（`[官方矛盾]`）→ **对客报地域前必须查控制台实际可购列表，不要引用发布记录**。

### 15.8 鉴权四条路（客户问「怎么鉴权」的答题框架）

| 路 | 机制 | 适用 | 🔴 关键限制 |
|---|---|---|---|
| 1 | **消费者 API-Key** | 最常见；MCP 消费者认证**专页**称目前仅支持它 | 🔴 **[官方矛盾·裁决 C9 已修订]**：2026-01 发布记录明文「MCP Server 支持 **JWT 认证**」，而 MCP 消费者认证专页仍写「目前仅支持 **API Key**」；按 R4 优先级（**带日期发布记录 > 静态专页**）倾向前者，但专页未标废弃 → **对客须在客户实例上实测确认，不得仅凭任一侧文档承诺** |
| 2 | **JWT**（全局 JWT 认证 / 消费者 JWT 凭证） | 已有 IdP、要传递身份声明 | 官方对「网关用公钥还是私钥验签」**四处表述不一致**（`[官方矛盾]`） |
| 3 | **OIDC**（全局 OIDC / 门户 OIDC 单点登录） | 企业 SSO、开发者门户 | scope 分隔符两页不一致（分号 vs 空格）；🔴 OIDC 用户的准入控制点**前移到企业 IdP**，门户「开发者自动审批」开关对其失效 |
| 4 | **自建认证**（外部鉴权服务 / ext-auth 插件） | 客户已有认证接口，不愿改 | 🔴 **鉴权 API 的 Path 需前缀匹配，且真实 Path = 鉴权API + 原始请求Path**；精确匹配接口必然 404，且 **404 不在宽松模式兜底范围**。解法 = ext-auth 插件 `endpoint_mode: forward_auth`（见 §14.1） |

另有 **HMAC** 与插件形态的 basic-auth / key-auth / hmac-auth / jwt-auth / jwt-logout / oauth（详见 [§9.4](aliyun-ai-gateway-plugins.md)）。
🔴 **「插件形态鉴权」与「产品内置消费者鉴权」能否叠加、叠加时执行顺序、插件 YAML 里的 `consumers` 与控制台「消费者」对象是否同一实体 —— 全部 `[文档未说明]`**，这是对客最容易被问住的三个问题，答「文档未说明 + 建议实测」。

### 15.9 🔴 报价前必核清单（文档把数字推走的地方）

| 项 | 文档状态 | 核验途径 |
|---|---|---|
| 专享实例各规格单价 | 2 处「以控制台/价格页/SLA 协议页面为准」 | 购买页 `common-buy.aliyun.com` |
| Serverless 新版 6 项单价 | 全部自称「参考单价」，**无任何地域单价表** | 购买页 + 工单 |
| **AI 增强能力**的 Credits 折算率（模型调用侧有文档：Credits/1M tokens、默认 0） | AI 增强能力侧**查无** | 工单 |
| AI 安全护栏商品价 | 只指向 `lvwang_guardrail_public_cn` 购买页 | 购买页 |
| 退款金额/比例 | 全外链 | 费用中心 |
| 9 类资源配额 | 错误码页全是 `%s` 占位 | 配额中心 / 工单 |
| 连带 6 类云产品单价 | 文档全部未说明 | 各产品定价页（CDT / SLS / 云监控 / KMS） |
| 延停权益额度 | 按账号历史消费**每月动态算** | 无法给确定值，只能说明机制 |
| 请求次数阶梯是超额累进还是全量按档 | **未说明**（差异 >20%） | 工单 |
| 地域实际可购列表 | 与发布记录矛盾 | 控制台 |

### 15.10 与相邻产品的关系（交叉引用）

- **[[aliyun-agentcore]]**：AgentCore 的服务关联角色策略里含 **57 条 `apig:` Action**（含 `apig:CreateMcpServer`/`DeployMcpServer`）→ **AgentCore 的 MCP Server 由 API 网关承载**；AgentTeams 的 9 个依赖产品里明确列了「AI 网关」。🔴 客户用 AgentCore 时会**同时产生 AI 网关账单**，两边的「依赖产品独立计费」话术一致。
- **[[百炼]]**：AI 网关是百炼模型的对客统一入口方案之一（多模型路由 + Fallback + Token 限流 + 计量分账）；坤启案的 action ① 就是「百炼稳定性（提额 + fallback + **AI 网关计量分账**）」。
- **云原生 API 网关**：同族同内核（Envoy/Higress），插件体系与 RAM Action 前缀 `apig:` 共用；本次未蒸馏。
- **Higress 开源版**：官方对比页称全托管免运维、99.99% SLA、内核优化 90%+、深度集成 WAF/IDAAS/KMS。🔴 该页是概述页宣称（口径优先级最低档），**99.99% 不得用于赔偿主张**（裁决 C1）。
- 🔴 **公网流量出账方按形态不同，不可一概说「走 CDT」**（2026-09-21 主控修正，R2a 判定 P0-2）：**专享实例** = 「通过云数据传输 CDT 统一计费」`[官方｜free-product-templates]`；**Serverless 新版（标准版/企业版）** = 「**公网出网和入网流量均由网关侧计费，单价为 0.8 元/GB**」`[官方原文｜overview-of-billing-during-the-serverless-public-preview-of-the]`，且官方补一条关键例外：「如果自行配置了 NAT 网关，公网出网流量走该 NAT 网关，则**网关侧不产生此部分费用**」。🔴 **§15.3 把企业版推荐给生产 → 报价必须把这项 0.8 元/GB（出网+入网）算进网关账单，漏报即少算一整项。**

### 15.11 🔴 选型硬门槛与单向门（R2a E 节判定：这 6 条只藏子页，速查卡必须有）

**选型硬门槛（不满足就直接淘汰该形态，不要先报价再发现）**

| 门槛 | 官方原文 | 淘汰谁 | 来源 |
|---|---|---|---|
| **Serverless 版不能开 WAF** | 「**Serverless版AI网关不支持开启WAF防护。**」 | 有 WAF 合规要求的客户 → 只能选**专享实例** | `view-gateway-instance-details` |
| **Agent 管理只支持新版 Serverless 两档** | 「**仅支持新版 Serverless 网关的标准版和企业版**，旧版 Serverless 和实例型…」 | 要用 Agent 纳管 → **旧版 Serverless 与专享实例都不行** | `agent-management-access-and-observation` |
| **标准版不能接容器服务来源** | 标准版「K8s服务来源数 = **N/A**」+「不支持自定义插件」 | 后端在 ACK/ACS → 必须**企业版或专享实例**（`[推断]`，见 §14.7） | `capacity-description`、`ai-gateway-capacity-description` |
| 🔴 **突破配额白名单 = 放弃 SLA** | 「如通过特殊白名单或特殊配置突破上述配额限制，相关使用不属于标准配额范围，**阿里云不对该等使用场景作出服务等级协议（SLA）承诺**」 | 所有想提额的客户 —— **提额与 SLA 二选一**，方案里必须写明 | `capacity-description` |

**单向门（开了就回不去，签约前必须让客户知道）**

| 单向门 | 官方原文 | 🔴 对客怎么说 |
|---|---|---|
| **AI Credits 开通后不可逆** | 「**开通后不支持退订和关闭。**只要您不使用对应的 AI 增强能力，就不会产生 Credits 费用。」 | 是**不可逆开关**，但**不用就不产生费用** → 不是成本陷阱，是「退订不了」的合规/审计问题。客户有「所有商品必须可退订」内控要求时会卡住，**签约前先问** |
| **AI Credits 目前只覆盖智能路由** | 「目前 AI 增强能力**仅先支持智能路由**，后续能力将陆续支持，**具体可用能力以产品控制台展示为准**」 | 🔴 这条**收窄了 §15.4 的空白**：语义检索、工具精选**当前不在 AI Credits 计费范围内**（因为 AI 增强能力目前只有智能路由）。所以对客可以说「这两项目前不额外烧 Credits」，但要带上「官方写明后续能力陆续支持、以控制台为准」的时间限定 —— **不要说成永久免费** |
| **SLA 赔偿逾期失权** | 「赔偿申请必须限于在网关实例没有达到可用性的相关月份结束后**两（2）个月内**提出。**超出申请时限的赔偿申请将不被受理**」 | 🔴 **且官方未写申请渠道**（`[文档未说明]`）→ 客户出事时要**立即提工单**并自己记好时限，别等季度复盘 |

**两条未裁决的官方矛盾会影响选型，对客必须说明「文档打架、需实测」**（详见 `tests/ai-gateway-rulings-2026-09-21.md`）：
- **C7**：`frontend-gray` 插件优先级有 **1000 与 450** 两个官方数字，直接决定前端灰度能否拿到真实客户端 IP。
- **C11**：Nacos 版本要求有「**企业版** 3.0 及以上」与「**铂金版** 3.0 及以上」两个口径 → 按更高要求（铂金版）预检。

---

## 溯源总表

| 层 | 位置 | 说明 |
|---|---|---|
| Raw | `raw/aliyun-docs/ai-gateway/`（186 快照 + README + SHA256SUMS） | 不可变源层，逐字保留官方原文含错字与渲染残留 |
| Raw（实战） | `raw/misc/practice-2026-09-21-hesi-*`（3 文件） | 合思案对客答复 + 内部决策建议（**勿外发**）+ 群聊原始记录 |
| Wiki | 本文件 + 6 个子页 | 预编译知识，每条事实带 slug 溯源 |
| 工艺制品 | `tests/ai-gateway-*`（6 份） | 清单/manifest/覆盖率审计/蒸馏契约/裁决留痕 |
| 可复用脚本 | `scripts/{build-doc-inventory,fetch-aliyun-docs,audit-doc-coverage,assign-distill-shards,scan-truncated-snapshots,assemble-ai-gateway-pages}.py` | 可直接用于任何 help.aliyun.com 产品的全站蒸馏 |

**统计（主控实测，非估算）**：7 路蒸馏 worker 共产出 **8944** 行 partial，装配为 **7 个知识文件 / 9471 行 / 411 张表**（表格行合计 3606）。
标注分布：`[官方｜slug]` **290** ｜ `[官方原文]` **49** ｜ `[官方矛盾]` **99** ｜ `[文档未说明]` **550** ｜ `[推断]` **201** ｜ `[原文如此]` **49**。
复算命令：`grep -o '\[官方矛盾\]' knowledge/aliyun-ai-gateway*.md | wc -l`（其余标注同理）。
