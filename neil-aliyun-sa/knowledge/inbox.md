# Inbox — Raw 层注册入口

> **Karpathy LLM Wiki 角色**：本文件是 Raw Sources 层的**索引与状态机**，跟踪每个来源的生命周期。
> 实体存储位于 `raw/` 目录（不可变副本）。
>
> **写入优先红线**：收到任何投喂资料的第一个动作就是在这里登记一条 pending 记录，再做分析。
> 状态机：`pending`（已登记，未处理） → `processing`（蒸馏中） → `done`（已落盘到 knowledge/）。
> 格式：`- [状态] 日期 | 类型 | 标题 | URL | raw/归档路径 | 落地文件`
>
> **与 raw/ 的关系**：
> - inbox.md = 索引（知道有什么、什么状态）
> - raw/ = 实体（原始内容的不可变副本）
> - knowledge/ = 编译产物（蒸馏后的结构化知识）

## Pending（待处理）

> **[raw-pending] 标记说明**：官方文档（help.aliyun.com）按 AGENTS.md 策略仅存 URL+摘要，无需全文归档；
> ATA 文章已全部存入 raw/ata/ 目录（含 SHA256）。以下官方文档条目标记 `[done]` 表示已按策略完成归档。

> 以下为种子语料 —— 等待逐篇蒸馏。每篇蒸馏前先移到 Processing，蒸馏后再移到 Done 并指明落地文件。

### 2026-09-21 阿里云 API 网关 · AI 网关 全站官方文档蒸馏


- [done] 2026-09-21 | 官方文档（help.aliyun.com，`.md` Agent 通道直取）| **AI 网关（AI Gateway）全量**（入口页 https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/what-is-an-ai-gateway ；官方按产品 llms.txt `https://help.aliyun.com/zh/api-gateway/ai-gateway/llms.txt` 共 **438** 个链接 → 本次范围 core **189** 页：产品概述 19 / 快速入门 3 / 操作指南 140 / 实践教程 9 / 安全合规 7 / 服务支持 3 / 开发参考元页 8；另 **250** 页逐 Action OpenAPI 参考登记 `[deferred]`）+ **1 个外部源**（terms.alicdn.com SLA 协议全文，help 侧仅 196B 入口桩）| https://help.aliyun.com/zh/api-gateway/ai-gateway/ | `raw/aliyun-docs/ai-gateway/`（**186** 个 .md = 148 有正文 + 37 TOC 容器 + 1 SLA 全文；含 README.md 316 行 + SHA256SUMS.txt 185 条）| **新建 `knowledge/aliyun-ai-gateway.md` 专题页家族 7 文件（9471 行 / 411 张表 / `[官方｜slug]` 290 · `[官方原文]` 49 · `[官方矛盾]` 99 · `[文档未说明]` 550 · `[推断]` 201 · `[原文如此]` 49）** + `aliyun-products.md` 指针卡 21 行与 AI 选型决策树新分支 + `index.md`（产品知识 2 行 + raw 状态区 + 11 条交叉引用实体）+ `tests/regression-cases.yaml` v1.7（语料 16→23、用例 62→**77**，AG01~AG15，**本 KB 首次引入 8 条 `forbidden` 否证不变量**）+ `tests/` 7 份工艺制品 + `scripts/` 7 个可复用脚本 + `run-regression.py` 新增 forbidden 支持
- **范围裁决（主控 2026-09-21，R1/R2）**：① AI 网关是 **API 网关产品族的三个平级子产品之一**（云原生API网关 / AI 网关 / 原API网关，证据 = 父级 `https://help.aliyun.com/zh/api-gateway/llms.txt`「## 子产品」并列三条，各自拥有独立 llms.txt）→ 本次范围**仅 AI 网关子树**，云原生API网关与原API网关不纳入（原API网关已公告 2026-08-23 停止新购、2027-09-21 全面下线）；② 开发参考 **250** 页逐 Action / 逐数据结构 OpenAPI 参考页按 AgentCore 侧 AgentRun 317 页 `[deferred]` 先例登记延后，**破例纳入 8 个元页**（OpenAPI 概览 / 服务接入点 / RAM 授权信息 / 流控配额 / 公共错误码 / 变更集 / API参考容器 / 开发参考容器）；③ 🔴 **归属判据 = llms.txt 收录关系，不是 URL 前缀** —— 首版按前缀判归属误踢 3 页（含**本次时点的现行计费权威源**「Serverless 新版商业化公告，2026-09-01 起计费」），已修正。
- [deferred] 2026-09-21 | 官方文档 | **AI 网关开发参考 250 页逐 Action / 逐数据结构 OpenAPI 参考**（`api-apig-2024-03-27-*`）| https://help.aliyun.com/zh/api-gateway/ai-gateway/developer-reference/ | 清单已存 `/tmp/aigw_deferred_urls.tsv` 与 `tests/ai-gateway-doctree-shards-2026-09-21.md` 第四节；🔴 已知 llms.txt 收录缺口 1 条：`api-apig-2024-03-27-createsecret`（docId 3045062，靠内链 301 解析发现），**建议单独排期**
- [deferred] 2026-09-21 | 官方文档 | **AI 网关同族相邻子产品**：云原生API网关（AI 网关的内核与插件体系同源、`apig:` Action 前缀共用、SLA 宣称 99.99%）/ 原API网关（传统版，2026-08-23 停新购、2027-09-21 下线，存量迁移话术）| https://help.aliyun.com/zh/api-gateway/{cloud-native-api-gateway,traditional-api-gateway}/llms.txt | 未纳入本次范围
- [done] 2026-09-21 | 实战资料（本 KB 外，用户当日产出）| **合思（易快报）AI 网关鉴权阻塞案**：客户答复 + 内部决策建议 + 群聊原始记录（ext-auth `endpoint_mode: forward_auth` 源码级核实、自建鉴权「鉴权API + 原始请求Path 拼接」为设计行为、HTTP转MCP 下工具级消费者鉴权作用于 tools/list 的官方原文反证、MCP 上架入驻千问办公的通道错配）| /Users/neil/Desktop/neilskills/neil-llm-kb-skill/合思-AI网关鉴权-{客户答复,内部决策建议}.md + .tmp-hesi-chat-raw.md | `raw/misc/practice-2026-09-21-hesi-aigw-auth-{customer-reply,internal-decision}.md` + `practice-2026-09-21-hesi-chat-raw.md` | `knowledge/aliyun-ai-gateway.md` §14.1~§14.3（🔴 internal-decision 含同事口径纠正，已标 **勿外发**）
- **抓取方法沉淀（在 2026-09-20 AgentCore 五条之上新增两条，共七条）**：①~⑤ 见下方 AgentCore 条目；⑥ 🔴 **第四种失效模式「Document Not Found 桩」** —— `.md` 通道对导航树里无正文的目录节点返回 CT=markdown + HTTP **200 或 404**（同一 slug 两次抓取状态码不同，故状态码更加不可作判据）+ 恒 **86B** 固定文案，**同时通过前三种校验且有散文故也不是 TOC**，首版抓取器判成 OK 落盘 4 页垃圾；⑦ 🔴 **第五种失效模式「服务端静默截断」** —— HTTP 200 + CT 合格 + **Content-Length 与 body 自洽** + **两次抓取 SHA256 完全一致**（证明截断在服务端不在抓取器），判据是**结构性的**（末行是孤立 `*`/`-`、HTML 标签开闭不平衡、末行以未完结词尾结束），实测 186 快照仅 `agent-api-observable` 1 页命中（978B）。**工艺升级**：抓取/审计/派工/装配**全部脚本化**（`scripts/{build-doc-inventory,fetch-aliyun-docs,audit-doc-coverage,assign-distill-shards,scan-truncated-snapshots,assemble-ai-gateway-pages,gen-raw-readme}.py`）而非交给 subagent → 产物可复算、无二手结论污染；派工用**集合运算做完备性门禁**（149 有正文快照 = 149 条指派，无遗漏/无重复/无幽灵 slug）；🔴 **门禁必须做负控**（剔除被测对象证明会 FAIL + 注入必然命中的禁写串证明否证逻辑生效），本次负控 1 抓出「指针卡太密集导致 AG01~03 假绿」的真缺陷。

### 2026-09-20 智能体构建和治理平台 AgentCore 全站官方文档蒸馏


- [done] 2026-09-20 | 官方文档（help.aliyun.com，`.md` Agent 通道直取）| **智能体构建和治理平台 AgentCore 全量**（官方 llms.txt 收录 **39** 个 slug → **32** 个帮助中心正文快照落盘 + **7** 个无正文 TOC 容器节点未落盘；产品简介/基本概念/计费说明/计费开通/协作管控面限免/SLR/SLA 入口 + 操作指南：概览·工作空间·连接器·Agent 管理·高代码 Agent 部署·本地纳管 Agent·Agent 模板·记忆空间·模型管理·技能·MCP Server·凭证 + 团队协作·Team Web 定时任务·用户管理·IM 渠道·钉钉集成·飞书集成 + SDK 概览·Python SDK·Node.js SDK·Python SDK 建高代码 Agent）**+ 1 个外部源**（SLA 协议全文 terms.alicdn.com，4476B/93 行）| https://help.aliyun.com/zh/agentcore/ | raw/aliyun-docs/agentcore/（**33** 个 .md + README.md + SHA256SUMS.txt 33 条）| **新建 knowledge/aliyun-agentcore.md**（1861 行 / 13 节 / 86 张表 / [官方] 287 · [推断] 49 · [官方矛盾] 17）+ knowledge/aliyun-products.md 12 行指针卡 + AI 选型决策树补 1 行 + index.md + tests/regression-cases.yaml（AC01~AC16 共 16 用例 134 关键词）
- [done] 2026-09-20 | 官方文档（help.aliyun.com）| **多智能体治理与协作平台 AgentTeams 全量**（官方 llms.txt 收录 **22** 个 slug → **18** 个快照落盘，其中 2 个为容器页破例保留以承载 slug↔document_detail ID 对照证据 + 4 个容器节点未落盘）🔴 **已迁移至 AgentCore，遗留文档**：逐页判 migration_status = **migrated-legacy 17 / unknown 1 / current 0**；🔴 关键判定：**17/18 页正文零迁移字样、全部现役口吻**，legacy 属性是**集合级、页面不自证**的，判据 = 权威迁移页 +「AgentCore 侧存在对应新页」联合推定 | https://help.aliyun.com/zh/agentteams/ | raw/aliyun-docs/agentteams/（**18** 个 .md + README.md 含顶部迁移横幅 + SHA256SUMS.txt 18 条）| knowledge/aliyun-agentcore.md §9（迁移对照与遗留口径，含 19 条术语映射表 —— 🔴 **仅 1 条有页面证据 Skill↔Skill，其余 18 条「页面未说明」**）
- **范围裁决（主控 2026-09-20）**：help.aliyun.com 上 AgentCore(productCode 3052261) / AgentTeams(3034770) / AgentRun(3049178) 是**三个平级独立产品**，非父子关系（证据：官方 `https://help.aliyun.com/zh/llms.txt` 第 82/83/84 行并列三条）。本次范围 = **AgentCore 37 + AgentTeams 18 = 55 页**（用户所指 https://help.aliyun.com/zh/agentcore 及其已并入的 AgentTeams 遗留料）。
- [deferred] 2026-09-20 | 官方文档 | **智能体 AgentRun 全量 317 页**（317 页中 262 页为 OpenAPI/CLI 参考，55 页为叙事文档；独立产品，非本次范围）| https://help.aliyun.com/zh/agentrun/ | 目录树与分片清单已存 `tests/agentcore-doctree-shards-2026-09-21.md`（1126 行；SHARD-5~7 叙事 55 条 / SHARD-A1~A14 OpenAPI 262 条；🔴 含软 200 三重校验协议与已排除的 37 条实测 404 死链清单，直接可复用），**建议单独排期蒸馏为 knowledge/aliyun-agentrun.md**
- [deferred] 2026-09-20 | 官方文档 | AgentCore 同族相邻产品：Agent 观测与优化 AgentLoop(3033820) / 智能体身份 Agent Identity / 智能体安全中心(asc) / 智能体沙箱(3053819，llms.txt 描述与 SAE 串了、归属存疑) | help.aliyun.com 各产品根 | 未纳入本次范围
- **抓取方法沉淀（可复用到任何 help.aliyun.com 产品）**：① 官方在 `robots.txt` 公示 `LLMS: https://help.aliyun.com/zh/llms.txt`，且有**按产品的 llms.txt**，比站内 BFS 更全（AgentCore 侧 llms 39 节点 vs BFS 30 节点）；② 任意文档 URL **加 `.md` 后缀**即返回纯 Markdown 正文（`Content-Type: text/markdown`），纯 curl 可取、无需浏览器渲染；③ 🔴 **软 200 陷阱**：不存在的 slug 也返回 HTTP 200 + 约 24893 字节的 SPA HTML 外壳，**HTTP 状态码不能作为成功判据**，必须三重校验（Content-Type 含 markdown + body 前 60 字节不以 `<!doctype`/`<html` 开头 + body > 400 字节）；④ 页面权威层级取自 HTML 里 `window.__ICE_PAGE_PROPS__.docDetailData.storeData.breadcrumb`；⑤ llms.txt 是快照会滞后（AgentRun 侧死链率 8.9%，37 条实测 404），抓取时宜从每页 recommendDocs / 正文内链做增量发现。
- **抓取契约**：`tests/agentcore-fetch-contract-2026-09-21.md`（4 路并行 worker 共读；含软 200 三重校验脚本、raw frontmatter 规范、migration_status 判定、digest「只抄不评」6 条纪律、9 条红线）。**蒸馏契约**：`tests/agentcore-distill-contract-2026-09-21.md`（7 条铁律 + 13 节 owner 分工表）。🔴 二者与裁决留痕、3 份评审报告原落 `outputs/`，因 `outputs/*` 被 gitignore（该目录定位＝可丢弃生成物）与本 KB「Git = 审计」原则冲突，已迁入受版本控制的 `tests/` 并与既有 `lint-*`/`regression-*` 同形扁平命名

### 2026-08-11 灵骏裸金属（钉钉文档 2 篇）


- [done] 2026-08-11 | 内部文档（钉钉在线表格 axls）| **《灵骏产品规格code》**（nodeId `vy20BglGWOxjGpq0CgBKlr4bVA7depqY`，workspaceId `nb9XJNnNrd5BDXyA`；4 个 sheet：产品code&实例规格 A1:F134 / 列表价明细 A1:N99 / 20260418涨价清单 A1:P267 / 灵骏实例规格配置 A1:I24）| https://alidocs.dingtalk.com/i/nodes/vy20BglGWOxjGpq0CgBKlr4bVA7depqY | raw/misc/misc-2026-08-11-lingjun-bms-spec-code.md（520 行，正文 SHA256 `ccafb9ad…23fb`）+ raw/misc/misc-2026-08-11-lingjun-price-increase-20260418.md（293 行，正文 SHA256 `d8c87f7b…587f`）| **新建 knowledge/aliyun-lingjun-bms.md**（389 行，14 节）+ knowledge/aliyun-products.md（PAI 卡新增 SA 红线 ⑤⑥ + 第⑪条两套体系指针 + 两处勘误）+ index.md + changelog.md
- [done] 2026-08-11 | 内部文档（钉钉文档 adoc，原始为钉盘 dentryKey 链接）| **《灵骏裸金属实例开通及退订方法》**（nodeId `qnYMoO1rWxrkmoj2IboYZA16J47Z3je9`，createTime 2025-09-02，updateTime 2026-07-22，42 张图其中 36 张带 `Expires` 签名归档后必失效）| https://alidocs.dingtalk.com/document/preview?cid=2899384242:6044579494&docKey=3BMqYybD9pAemqwZ&dentryKey=6mW9x31EQi2VzK0Y ｜ 规范链接 https://alidocs.dingtalk.com/i/nodes/qnYMoO1rWxrkmoj2IboYZA16J47Z3je9 | raw/misc/misc-2026-08-11-lingjun-bms-provision-and-refund.md（221 行，正文 SHA256 `1b272bbb…6b70b`）| knowledge/aliyun-lingjun-bms.md § 9–11（系统盘计费红线 / 开通五步 / 退订工单流程）
- **抓取方法沉淀**：钉钉 `/i/nodes/` 链接必须先 `dws doc info` 探类型（本次一篇 `axls` 走 `dws sheet csv-get`、一篇 `adoc` 走 `dws doc read --format markdown`）；`document/preview?...dentryKey=` 链接可直接原样传 `--node`。🔴 **dws 命令不能用输出重定向 `>`、shell 变量或 for 循环**，否则 PostToolUse hook 不生效、只会拿到 `[dws-bash:pending-post-tool-use]` 占位串，必须把字面量 URL 写在命令里直接输出到 stdout。
- **关键结论**：**PAI 灵骏 `ml.*` 月价 = 灵骏裸金属 `efg*` 月单价 × 1.10**（20+ 地域×卡型精确命中，例外 3 类）；**PAI 按量 ≈ 包月 × 1.5208**；勘误上海金融云溢价 PAI +52% vs 裸金属 **+90%**、北京政务云裸金属 **×2.00**；L20A/L20B 的 GB200/GB300 猜测**零证据禁引**；新增卡型 **L20P**、**PPU810**、可用区 **成都蚂蚁**。

### 2026-08-10 Accio 官网定价与公司定位（补语雀图片缺口）


- [done] 2026-08-10 | 官方产品站 | www.accio.com `/pricing` + `/about-us`（**定向补缺**，浏览器实抓，SPA 客户端渲染 curl 取不到正文）| https://www.accio.com/pricing ｜ https://www.accio.com/about-us | 官方页按 AGENTS.md 策略仅存 URL+摘要 | knowledge/ai-trends.md 第 11 节（①产品家族界定 Accio 采购引擎 vs Accio Work 工作台 + ③个人版**五档**价格表刷新 + ⑧⑨缺口与来源鲜度）｜**关键发现**：官网比语雀多「标准版 ¥69/月=2000 积分」档位、每日登录积分按档递增 20/20/30/50/100、Free 高质量模型口径与语雀矛盾、企业版官网亦无公开价（Sales-led）
- 范围决策：**不抓** `/help`（robots.txt 标 Disallow 且与语雀 28 篇高度重叠）、**不抓** `/blog/`（消费选品趋势内容，按知识蒸馏原则属应丢弃部分）、**不抓** PLP/PDP/supplier SEO 商品页（百万级商品目录，与知识库无关）

### 2026-08-10 Accio Work 知识库（公开语雀 book）


- [done] 2026-08-10 | 官方产品文档（公开语雀）| Accio Work 知识库全站 28 篇（book_id 78769374；简介/入门指南 4 篇/核心功能 8 篇/企业版/APP/生意助手接入 5 篇/OKKI/1688/实战技巧 4 篇；其中 3 篇为空目录分组页）| https://acciowork.yuque.com/rfmg8t/ieb85b | raw/aliyun-docs/accio/{01..28}-*.md + SHA256SUMS.txt（全文归档 133KB）| knowledge/ai-trends.md（**新增第 11 节「商业化 Agent 工作台形态参考：Accio Work」**8 小节）+ index.md（raw/aliyun-docs 状态 + ai-trends 摘要 + 交叉引用新增 Accio/OKKI 与 Agent 平台商业化两实体）

### 2026-08-10 GPU 卡型 × 阿里云实例规格对应表（内部语雀 paidoc）


- [done] 2026-08-10 | 内部文档（语雀 paidoc）| 🔴 PAI 灵骏智算服务规格：GPU 卡型 × 实例规格对应表（book_id 118919 / doc_id 250470307，lakesheet 两 sheet，商业化可售 143 行 + 适配中 6 行）| https://aliyuque.antfin.com/paidoc/xh6w3l/lwgiw0bz7xpe1uho?singleDoc#zSFs | raw/misc/misc-2026-08-10-pai-lingjun-gpu-specs.md（TSV 全文，SHA256 ea88e28d…5545）| knowledge/aliyun-products.md（PAI 卡新增第 ⑩ 条「灵骏智算 GPU 卡型 × 实例规格全表」）+ index.md（raw/misc 状态 + 交叉引用新增 GPU 卡型/L20x 实体）｜**敏感级别：Alibaba Internal，严禁对客；仓库已于本日转为 private**

### 2026-08-08 企业内部知识库（员工侧 RAG）方案设计任务 → Query 回写（模式H）


- [done] 2026-08-08 | 官方文档 + 官方公告（4 组 subagent 实时核验 + 独立事实核查员复核）| 百炼知识库（RAG）规格·计费·限制·检索·权限·地域·数据条款·退出成本·Retrieve API + 生命周期公告（企业知识库 2027-01-16 下线 118448 / 商业化 117726 / gte-rerank 下线 118217）| https://help.aliyun.com/zh/model-studio/ + https://www.aliyun.com/notice/118448 / 117726 / 118217 | 按 AGENTS.md 策略官方文档仅存 URL+摘要，无需全文归档 | knowledge/aliyun-products.md（百炼卡新增「知识库（RAG）完整规格与计费」13 小节）+ references/pricing-verification-checklist.md（§ 3.1b 两行 + § 3.2 预警 + C14 案例 8）
- [done] 2026-08-08 | 官方文档 | 向量检索 / RAG 检索引擎 8+ 产品线核验（OpenSearch LLM智能问答版 / OpenSearch 向量检索版 / DashVector / Milvus 版 / 阿里云 ES 集群版含 OpenStore / ES Serverless / Lindorm 向量 / ADB-PG 向量 / Hologres HGraph / Tablestore 向量 / RDS PG pgvector / Qdrant 计算巢自建）| help.aliyun.com 各产品计费与限制页 + 官方定价页 | 仅存 URL+摘要 | knowledge/aliyun-products.md（新增「向量检索 / RAG 检索引擎选型」12 条产品线速查节）+ references/pricing-verification-checklist.md（§ 3.1b + § 3.2 扩到 24 条 + C13）
- [done] 2026-08-08 | 官方文档 + 可匿名定价数据源 | PAI-EAS 独享 GPU 逐规格包月价 + Qwen3 部署最低配置 + ACS GPU 单价 + gn8v 地域约束 + 百炼专属版 AI Stack 一体机形态 | https://www.aliyun.com/page-source/price/detail/machinelearning_price + https://help.aliyun.com/zh/pai/ | 仅存 URL+摘要 | knowledge/aliyun-products.md（PAI 卡新增「EAS 独享 GPU 报价与私有化部署路线约束」9 小节）
- [done] 2026-08-08 | 官方文档 | 文档智能 DocMind 文档解析（大模型版）计费与触发机制 | https://help.aliyun.com/zh/document-mind/ | 仅存 URL+摘要 | knowledge/aliyun-products.md（新增「文档智能 DocMind」产品卡）+ references/pricing-verification-checklist.md（§ 3.1b + C14）
- [done] 2026-08-08 | Query 回写（模式H）| 企业内部知识库（员工侧 RAG）场景方案：三部署路线 / 三档向量库选型 / BFF 权限架构 / 成本量级 / POC 与八项验收指标 / 调优投入产出排序 / 效果量级（**已脱敏为区间与量级**）/ 14 条工程化踩坑 / 评测方法论 | (方案设计任务输出，非外部 URL) | 无需 raw 归档（按 AGENTS.md 策略：Query 回写直接编入 wiki）| knowledge/cloud-solutions.md（新增 S10 + S3 两处勘误锚点）+ index.md + changelog.md

### Coding Agent 工程化专项（2026-08-08，六路并行调研）— 已蒸馏


> ⚠️ **本次违反了写入优先红线**：先做调研后登记 inbox，而非收到任务第一动作就登记。已在 changelog 标注。原始资料全部落盘在项目 `research/raw/`（不在本 skill 的 raw/ 下，因体量 1.4MB+ 且属项目资产），本条为索引指针。

- [done] 2026-08-08 | ATA×56 | Loop Engineering / Graph Engineering / 常驻 Coding Agent 地毯式调研（122 关键词 → 640 篇去重 → 归档 56 篇全文） | 核心 6 篇：飞樰《Loop Engineering 概念解析》https://ata.atatech.org/articles/11020674841 、飞樰《从 Loop 到 Graph Engineering》https://ata.atatech.org/articles/11020728011 、也达《线上错误自主发现修复发布》https://ata.atatech.org/articles/11020683205 、风弦《业务流如何提升 Coding Agent》https://ata.atatech.org/articles/12020607628 、《OpenClaw 集群已在内网上线》https://ata.atatech.org/articles/11020588930 、《权限，身份，云沙箱》https://ata.atatech.org/articles/12020707208 | `loop_engineering_practice/research/raw/ata/`（56 篇，带 metadata 头） | knowledge/ai-trends.md 第11节
- [done] 2026-08-08 | Web/一手×29 | Anthropic harness/context 官方系列、Thoughtworks Radar Vol.34、Stripe minions、Devin machine setup、Cursor Cloud Agents、METR time-horizon 1.1、Sourcegraph 80% problem、Cognition don't-build-multi-agents | 官方文档按策略仅存 URL+摘要，正文已归档 | `research/raw/web/`（32 篇，二手明确标 SECONDARY） | knowledge/ai-trends.md 第11节
- [done] 2026-08-08 | GitHub×33 | 循环骨架（goose/aider/SWE-agent）+ 常驻服务（omnara/vibe-kanban/Sculptor）+ 沙箱（OpenSandbox/E2B/codex-rs）+ 评测（SWE-bench harness），star 与最近 commit 全部 `gh api` 实测 | — | `research/raw/github/`（24 文件覆盖 33 项目） | knowledge/ai-trends.md 第11.7/11.9节
- [done] 2026-08-08 | 论文/官方×24 | Graph 专项：SCIP/Kythe/Glean/CodeQL/Joern/Stack Graphs/RepoGraph(ICLR2025)/CodexGraph/cAST/LazyGraphRAG/CodePlan(arXiv 2309.12499) + 六家编排框架官方立场 | — | `research/raw/graph/` | knowledge/ai-trends.md 第11.8节
- [done] 2026-08-08 | grow 内网课程×5 | 釋心《Loop Engineering 实践：从 Harness 团队到 Loop 团队》https://grow.alibaba-inc.com/course/4810000000010637 、釋心《理论与实战》/4810000000010695 、覇天《1688 数据研发的 Loop Engineering 实践》/4810000000010723 、颜律《2 小时实战：用 Harness 搭 AI 研发管理体系》/4810000000010521 、式夏《Agent 框架落幕，Agent 工程起航？》/4810000000003454 | `research/raw/grow/`（6.6 万字，页面自带通义听悟文稿，**免 ASR**） | knowledge/ai-trends.md 第11.1/11.6节
- [done] 2026-08-08 | 源码测绘 | Multica（`~/Desktop/neilcodebase/multica`，HEAD `002ea0d87` / 2026-07-17 / v0.2.0）13 问架构测绘 + 3 处交叉核验修正（task 状态机 8 态 / LICENSE 改动版 Apache 2.0 / repocache 1288 行成熟实现） | — | `research/findings/multica.md` | 未入 skill 知识库（属项目资产）

### 2026-08-06 百炼 Token Plan 官方概述页刷新（增量核对）


- [done] 2026-08-06 | 官方文档 | 百炼 Token Plan 概述（token-plan-overview 重抓核对，Credits 抵扣公式 + 与按量付费/节省计划链路关系 + 模型完整版声明 + 团队版订阅月计费周期为本次新增/细化项）| https://help.aliyun.com/zh/model-studio/token-plan-overview | 按 AGENTS.md 策略官方文档仅存 URL+摘要，无需全文归档（2026-08-05 已首蒸三页，本次为增量刷新）| knowledge/aliyun-products.md（百炼卡 Token Plan 章节增量补充：Credits 抵扣公式/按量付费·节省计划三方关系/完整版模型/订阅月周期）

### 2026-08-05 阿里云 ClickHouse 两条产品线报价踩坑洞察（实战投喂）


- [done] 2026-08-05 | 实战踩坑 | 阿里云 ClickHouse 企业版 vs 社区兼容版报价与购买路径差异（海底捞项目实战） | (Neil 实战总结投喂 + help.aliyun.com/zh/clickhouse 计费/购买页交叉验证) | 无需 raw 全文归档（按 AGENTS.md 策略：实战洞察直接编入 wiki） | knowledge/aliyun-products.md（新增 ClickHouse 独立双线产品卡：企业版 Serverless + 社区兼容版）+ index.md（交叉引用表新增 ClickHouse 实体）

### 2026-07-16 百炼增速/突发限流机制（内部文档投喂）


- [done] 2026-07-16 | 内部文档 | 百炼增速/突发限流现状和未来（3.1 现状）| (内部资料截图投喂) | raw/misc/misc-2026-07-16-bailian-rate-throttling.md | knowledge/aliyun-products.md（百炼卡「增速限流 / 突发限流机制」 + DashScope 卡交叉引用）

### Web 蒸馏（长上下文 / 思考模型延迟）— 已蒸馏


- [done] 2026-07-15 | Web/Google+GitHub | RULER(NVIDIA arXiv 2404.06654) + Context Rot(Chroma) + morphllm 2026 对比 + THUDM/LongBench | 官方/公开文献，仅存 URL+摘要 | knowledge/ai-trends.md 第10节
- [done] 2026-07-15 | Query回写 | 百炼 glm-5.2 高延迟工单排查结论（10条请求分析）| 内部工单/latency_analysis 项目 | knowledge/ai-trends.md 第10节

### ATA 高价值文章（共 12 篇候选种子）— 9/12 已蒸馏

- [done] 2026-06-17 | ATA | 一个广告行业 AI 顾问的修炼之路（11 天版） | https://ata.atatech.org/articles/11020643601 | raw/ata/ata-2026-06-17-ai-consultant-11day.md | SKILL.md（元方法论）+ knowledge/ai-trends.md
- [done] 2026-06-17 | ATA | ADR 与 SDD：从架构决策到代码落地的闭环 | https://ata.atatech.org/articles/11020634808 | raw/ata/ata-2026-06-17-adr-sdd.md | references/architecture-templates.md（ADR方法论）
- [done] 2026-06-17 | ATA | 宝马落地阿里云Landing Zone Accelerator | https://ata.atatech.org/articles/11020552831 | raw/ata/ata-2026-06-17-bmw-landing-zone.md | references/caf-landing-zone.md + knowledge/company-profiles.md
- [not-found] 2026-06-17 | ATA | 可口可乐云原生变革 | (ATA搜索未找到，可能标题不同或限制访问) | -
- [not-found] 2026-06-17 | ATA | 莉莉丝 AWS Winback | (ATA搜索未找到，仅找到重保/广告分析相关) | -
- [done] 2026-06-17 | ATA | 网商银行智能化业务定位决策系统 | https://ata.atatech.org/articles/12020553615 | raw/ata/ata-2026-06-17-mybank-ai.md | knowledge/ai-trends.md（Agent案例）
- [done] 2026-06-17 | ATA | 构建高可用AI系统 | https://ata.atatech.org/articles/11020604053 | raw/ata/ata-2026-06-17-high-availability-ai.md | knowledge/ai-trends.md（AI Infra）+ cloud-solutions.md（S3高可用模式）
- [done] 2026-06-17 | ATA | Taobao Bonus：淘海外跨境支付资产体系 | https://ata.atatech.org/articles/11020594402 | raw/ata/ata-2026-06-17-taobao-bonus.md | knowledge/cloud-solutions.md（S2跨境参考）
- [not-found] 2026-06-17 | ATA | Aegis AI 数字分身 | (ATA搜索仅返回旧安全产品，未找到AI数字分身文章) | -
- [done] 2026-06-17 | ATA | Serverless跨云迁移：从 AWS Lambda到阿里云FC | https://ata.atatech.org/articles/11020645626 | raw/ata/ata-2026-06-17-lambda-to-fc.md | knowledge/aliyun-products.md（FC卡片补充）
- [done] 2026-06-17 | ATA | SA动手系列2-PD分离技术深度实践 | https://ata.atatech.org/articles/11020600554 | raw/ata/ata-2026-06-17-pd-separation.md | knowledge/ai-trends.md（PD分离实战数据）
- [done] 2026-06-17 | ATA | Java程序员转型AI开发者：四月学习路线 | https://ata.atatech.org/articles/12020603721 | raw/ata/ata-2026-06-17-java-to-ai.md | knowledge/ai-trends.md（Agent三层次）

### help.aliyun.com 官方框架文档（共 4 篇）— ✅ 已全部蒸馏

- [done] 2026-06-17 | 官方文档 | 阿里云 Cloud Adoption Framework (CAF) | https://help.aliyun.com/zh/caf/ | references/caf-landing-zone.md
- [done] 2026-06-17 | 官方文档 | 阿里云 Well-Architected Framework | https://help.aliyun.com/zh/product/2362200.html | references/well-architected.md
- [done] 2026-06-17 | 官方文档 | Cloud Network Well-Architected Design | https://help.aliyun.com/zh/cloud-network-well-architected-design/ | references/well-architected.md (网络章节)
- [done] 2026-06-17 | 官方文档 | 阿里云安全建设指南 ACSG | https://help.aliyun.com/zh/acsg/ | references/well-architected.md (安全章节)

### help.aliyun.com 产品文档全域蒸馏（66+ 产品）— ✅ 已全部蒸馏

- [done] 2026-06-17 | 官方文档 | 计算域 7 产品（ECS/ACK/ACS/ECI/SAE/FC/ESS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 存储域 5 产品（OSS/NAS/CPFS/EBS/Tablestore） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 网络域 11 产品（VPC/CEN/GA/CLB/ALB/NLB/NAT/VPN/高速通道/PrivateLink/Anycast EIP） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 数据库域 11 产品（RDS/PolarDB/Lindorm/Tair/AnalyticDB/Hologres/MaxCompute/DataWorks/Flink/DTS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | AI 域 7 产品（百炼/PAI/千问/万相/灵码/DashScope） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 安全域 9 产品（WAF/DDoS/Cloud Firewall/云安全中心/KMS/堡垒机/RAM/ActionTrail/Config） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 中间件+监控域 12 产品（MSE/RocketMQ/Kafka/RabbitMQ/EventBridge/ARMS/SLS/CloudMonitor/ROS/ACR/CDN/DCDN） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md
- [done] 2026-06-17 | 官方文档 | 混合云/边缘 2 产品（专有云/ENS） | help.aliyun.com 各产品页 | knowledge/aliyun-products.md

### help.aliyun.com / aliyun.com 客户案例首批蒸馏（共 8 个旗舰 + 索引若干）— ✅ 已蒸馏

- [done] 2026-06-17 | 官方案例 | 南京银行 SOFAStack + OceanBase 金融分布式 | https://help.aliyun.com/zh/document_detail/194962.html | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 哈啰出行 SLS 日志统一 + 百炼 Agent | https://help.aliyun.com/zh/sls/hellobike + developer.aliyun.com/article/1647416 | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 中国一汽 红旗云妹 AI 智能体 | https://www.aliyun.com/customer-stories/automotive-2025-faw | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | bilibili 游戏迁移上云 | https://www.aliyun.com/lowcode/common/case-studies/internet-2023-bilibili | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 启迪公交 PolarDB-X + AnalyticDB | https://help.aliyun.com/zh/polardb/polardb-for-xscale/bus-traveling-tuspass | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 51Talk 智能客服 Agent | https://developer.aliyun.com/article/1647416 | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 菜鸟 PolarDB for AI | https://help.aliyun.com/zh/polardb/polardb-for-mysql/case-studies/ | knowledge/company-profiles.md
- [done] 2026-06-17 | 官方案例 | 国际客户群索引（Garuda/GCash/Lazada/周大福/老虎/恒生/众安/鹰角/KLab 等 200+） | https://www.alibabacloud.com/zh/customers | knowledge/company-profiles.md（行业映射快查）

### 2026-06-23 MSE Nacos 深度蒸馏 + 全产品 Lint

- [done] 2026-06-23 | 官方文档 | MSE Nacos 实例版本选型指南 | https://help.aliyun.com/zh/mse/product-overview/select-an-edition | knowledge/aliyun-products.md（MSE 卡刷新）
- [done] 2026-06-23 | 官方文档 | MSE Nacos 引擎版本特性 | https://help.aliyun.com/zh/mse/product-overview/edition-features | knowledge/aliyun-products.md
- [done] 2026-06-23 | 官方文档 | MSE 开发版+专业版计费 | https://help.aliyun.com/zh/mse/product-overview/billing-description-of-developer-edition-instances-and-professional-edition-instances | knowledge/aliyun-products.md
- [done] 2026-06-23 | 官方文档 | MSE 企业版计费指南 | https://help.aliyun.com/zh/mse/product-overview/nacos-platinum-edition-billing-description | knowledge/aliyun-products.md
- [done] 2026-06-23 | meta | 全产品 Lint（健康检查 + 报价量级版本维度审查） | (内部触发) | tests/lint-2026-06-23.md（14 个条目，1 个 P0 已修，6 个 P1 待办）

### 2026-06-26 EMR Serverless StarRocks 深度蒸馏

- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 产品概述 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/product-overview/what-is-emr-serverless-starrocks | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 规格规划建议 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/instance-specification-planning-and-suggestions | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档 | EMR Serverless StarRocks 计费方式 | https://help.aliyun.com/zh/emr/emr-serverless-starrocks/product-overview/billable-items/ | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档（StarRocks 社区） | 主键表设计指南 | https://docs.starrocks.io/zh/docs/table_design/table_types/primary_key_table/ | knowledge/aliyun-products.md
- [done] 2026-06-26 | 官方文档（StarRocks 社区） | 导入概览 | https://docs.starrocks.io/zh/docs/loading/Loading_intro/ | knowledge/aliyun-products.md

### 2026-06-28 ATA LLM Wiki 知识工程专项

- [done] 2026-06-28 | ATA | 从 LLM Wiki / Obsidian-Wiki / GBrain 来看 Agent时代知识的"自组织"与"自进化" | https://ata.atatech.org/articles/11020627647 | raw/ata/ata-2026-06-28-llm-wiki-self-evolution.md | knowledge/ai-trends.md
- [done] 2026-06-28 | ATA | 别让你的知识腐烂——Karpathy LLM Wiki 在 KBase 的实践 | https://ata.atatech.org/articles/11020627230 | raw/ata/ata-2026-06-28-kbase-llm-wiki.md | knowledge/ai-trends.md

### help.aliyun.com / aliyun.com 客户案例后续待蒸馏（深度档案）

- [done] 2026-06-28 | 官方案例 | PolarDB 客户案例深度蒸馏（心动网络/真有趣/雅迪科技） | https://help.aliyun.com/zh/polardb/polardb-for-mysql/case-studies/ | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | 三一重工工业互联网架构 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | 完美日记/逸仙电商上云路径 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | SHEIN 出海架构 | (公开报道汇总，curator 补源后重新激活) | knowledge/company-profiles.md
- [deferred] 2026-06-17 | 官方案例 | Lazada 全栈电商架构 | (待补 URL，curator 补源后重新激活) | knowledge/company-profiles.md
- [cancelled-merged] 2026-06-17 | 官方案例 | 网商银行金融分布式 | 已由 ATA 文章 ata-2026-06-17-mybank-ai.md 蒸馏到 knowledge/ai-trends.md，不再单独补充

### 2026-09-21 云原生API网关 / AI网关 深度蒸馏（外部认证专项）


> 16 篇已全文归档 raw/aliyun-docs/（每篇头部含 source_url / fetched_date / page_last_modified / summary 四行元信息）。落地：knowledge/aliyun-products.md 新增「云原生 API 网关（APIG）/ AI 网关【深度卡】」+ 三处产品名消歧（MSE 卡/原API Gateway 卡/选型速查表）；knowledge/cloud-solutions.md 新增 S10 + S3 口径订正；index.md / ai-trends.md / architecture-templates.md 交叉引用同步。

- [done] 2026-09-21 | 官方文档 | 云原生API网关「配置自建认证鉴权」（页面更新 2026-09-20，A 路全文） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/configure-self-built-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-configure-self-built-authentication.md | knowledge/aliyun-products.md（深度卡 A 路）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | AI网关「配置自建认证鉴权」（2026-06-02，与 apig 版配置表逐字一致，diff 复核） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-self-built-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-configure-self-built-authentication.md | knowledge/aliyun-products.md（深度卡 A 路）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「Go语言开发网关插件」（2026-04-28，第 462/467 行 = 服务 FQDN 命名规则与 .static 逻辑端口 80 原文出处） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/develop-plug-ins-in-go | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-develop-plug-ins-in-go-service-fqdn.md | knowledge/aliyun-products.md（FQDN 对照表）
- [done] 2026-09-21 | 官方文档 | AI网关「Go语言开发网关插件」（2026-04-23，第 462 行注释与 apig 版逐字相同） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/develop-gateway-plug-ins-using-the-go-language | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-develop-plug-ins-go-service-fqdn.md | knowledge/aliyun-products.md（FQDN 对照表）
- [done] 2026-09-21 | 开源文档 | Higress ext-auth 插件 README（B 路完整字段表 / service_name 定义第 47 行 / envoy vs forward_auth / 全部示例 YAML） | https://raw.githubusercontent.com/alibaba/higress/main/plugins/wasm-go/extensions/ext-auth/README.md | raw/aliyun-docs/aliyun-docs-2026-09-21-higress-ext-auth-plugin-readme.md | knowledge/aliyun-products.md（深度卡 B 路）+ cloud-solutions.md（S10 配置骨架）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「创建服务」（七种服务来源参数表 / TLS 三档） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-create-service.md | knowledge/aliyun-products.md（前置步骤）
- [done] 2026-09-21 | 官方文档 | AI网关「创建服务」（八类来源；DNS 域名 `<DNS域名>:<服务端口>` / 外网地址需 NAT 网关原文出处） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-services | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-creating-services.md | knowledge/aliyun-products.md（前置步骤）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「服务来源管理」（ACK 1.18+/建议 1.28+、同 VPC、安全组授权、Nacos MCPEnabled=true） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/create-service-source | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-create-service-source.md | knowledge/aliyun-products.md（前置步骤）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「插件安装启用卸载」（官方插件=Higress官方/社区插件=Higress社区；三级作用域） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/enable-plugin | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-enable-plugin.md | knowledge/aliyun-products.md（B 路安装启用）
- [done] 2026-09-21 | 官方文档 | AI网关「插件安装启用卸载」（第 31 行：仅专享实例型AI网关支持安装与启用插件，Serverless版不支持） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-plug-ins | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-manage-plug-ins.md | knowledge/aliyun-products.md（避坑 🔴）+ cloud-solutions.md（S10）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「认证鉴权插件清单」（6 插件，无 ext-auth） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-authentication-plugin-index.md | knowledge/aliyun-products.md（B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | AI网关「认证鉴权插件清单」（同 6 插件，无 ext-auth） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-authentication-plugin-index.md | knowledge/aliyun-products.md（B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | MSE 云原生网关「认证鉴权插件清单」（7 插件含 edas-service-auth，无 ext-auth） | https://help.aliyun.com/zh/mse/user-guide/authentication-authentication | raw/aliyun-docs/aliyun-docs-2026-09-21-mse-authentication-plugin-index.md | knowledge/aliyun-products.md（MSE 卡消歧 + B 路在架性说明）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「全局认证鉴权」机制对比（JWT/OIDC/自建三种方式） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/global-authentication-1 | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-global-authentication.md | knowledge/aliyun-products.md（A 路定位）
- [done] 2026-09-21 | 官方文档 | 云原生API网关「计费概述」（专享实例 apigw 全规格单价表 + 数据处理费 0.037/0.049 + CDT，页面更新 2026-06-18） | https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/product-overview/billing-overview | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-billing-overview.md | knowledge/aliyun-products.md（计费）+ cloud-solutions.md（S10 成本）
- [done] 2026-09-21 | 官方文档 | AI网关「专享实例计费说明」（aigw 全规格单价表，页面更新 2026-07-29） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/free-product-templates | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-billing-dedicated-instance.md | knowledge/aliyun-products.md（计费）+ cloud-solutions.md（S3 成本订正 + S10）

> 补充口径（2026-09-21 收口已补归档 raw，原「未单独归档」备注作废）：三形态谱系/EOL 时间线/AI 网关能力清单出自 https://help.aliyun.com/zh/api-gateway/llms.txt → raw/aliyun-docs/aliyun-docs-2026-09-21-apig-llms-index.md ；AI Credits（0.01 元/Credit、开通后不支持退订）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md ；Serverless 旧版 CU 系数（10/5/2、0.005 元/千CU、最小 1000 CU 不足 10 万按 10 万计）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md ；Serverless 新版商业化公告（公测 2026-08-31 结束）→ raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-commercialization-announcement.md 。

### 2026-09-21 收口补充（MCP 鉴权维度 + 火山引擎对标 + 合思画像 + forward_auth 源码取证）


> 本轮为上一轮网关蒸馏的收口：MCP 维度与竞品对标两路取证在上一轮开跑后才回来，本次补入并修正引用限定。新增 raw 20 个文件（aliyun-docs ×9、standards ×4【新目录】、competitor ×4、misc ×1、ata ×2）。ATA 内网站点被 SSO 拦截，两篇 ATA 仅能归档**逐字摘录**（头部已注明「摘录而非全文」）；客户现场记录含敏感信息不落 raw（脱敏红线）。

- [done] 2026-09-21 | 官方文档 | AI网关「调试MCP服务」（第 29 行工具级鉴权过滤 tools/list 反证 + 第 60 行 Bearer Token 调试配置） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/debug-mcp-services | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-debug-mcp-services.md | knowledge/aliyun-products.md（MCP 维度）+ cloud-solutions.md（S10 实战案例）
- [done] 2026-09-21 | 官方文档 | AI网关「消费者认证」（MCP服务级/工具级、服务级权限高于工具级、仅支持 API Key、ApiKeyIdentityConfig apikeySource=Header/QueryString） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/consumer-certification | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-consumer-certification.md | knowledge/aliyun-products.md（三种鉴权能力对照表）
- [done] 2026-09-21 | 官方文档 | AI网关「HTTP转MCP 配置字段说明」（工具 YAML 存放网关侧、tools/list 不回调后端） | https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/http-to-mcp-field-configurations | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-http-to-mcp-field-configurations.md | knowledge/aliyun-products.md（HTTP转MCP 鉴权语义）
- [done] 2026-09-21 | 官方文档 | AI网关「新功能发布记录」（2026-01 MCP Server 支持 JWT 认证 → 与 consumer-certification「仅支持 API Key」矛盾，文档口径滞后） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/new-feature-release-notes-ai-gateway | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-new-feature-release-notes.md | knowledge/aliyun-products.md（🔴 官方文档自相矛盾记录）
- [done] 2026-09-21 | 官方文档 | AI网关「引擎版本说明」（最新公开引擎版本 2.1.23 / 2026-09-03） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/engine-version-description | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-engine-version-description.md | knowledge/aliyun-products.md（产品缺口存疑项）
- [done] 2026-09-21 | 官方文档 | AI Credits 计费详情（补归档，上一轮仅在线复核） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/ai-credits-billing-details | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-ai-credits-billing.md | knowledge/aliyun-products.md（计费备注已改为已归档路径）
- [done] 2026-09-21 | 官方文档 | Serverless（旧）计费详情（CU 系数 10/5/2，补归档） | https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/serverless-old-billing-details | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-serverless-old-billing.md | knowledge/aliyun-products.md（计费备注已改为已归档路径）
- [done] 2026-09-21 | 官方文档 | AI网关 Serverless 商业化公告（补归档） | https://help.aliyun.com/zh/api-gateway/ai-gateway-commercialization-announcement | raw/aliyun-docs/aliyun-docs-2026-09-21-aigw-commercialization-announcement.md | knowledge/aliyun-products.md（计费）
- [done] 2026-09-21 | 官方文档 | API 网关产品线 llms.txt 全文索引（三形态谱系/EOL/AI 网关定位出处，补归档） | https://help.aliyun.com/zh/api-gateway/llms.txt | raw/aliyun-docs/aliyun-docs-2026-09-21-apig-llms-index.md | knowledge/aliyun-products.md（产品谱系）
- [done] 2026-09-21 | 标准规范 | MCP 官方规范 Authorization 章（2026-07-28 版 + 2025-11-25 版，四版关键结论一致；无 per-method 免鉴权白名单） | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization ；https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization | raw/standards/standards-2026-09-21-mcp-spec-2026-07-28-authorization.md + standards-2026-09-21-mcp-spec-2025-11-25-authorization.md | knowledge/aliyun-products.md（MCP 协议层事实 [规范]）
- [done] 2026-09-21 | 标准规范 | MCP 官方规范 Streamable HTTP 传输章（2026-07-28 版，单一 MCP endpoint / 每条 JSON-RPC 消息一个 POST / 网关中介预设 / Security Warning 第 3 条）+ Transports 总览页 | https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http | raw/standards/standards-2026-09-21-mcp-spec-2026-07-28-transports-streamable-http.md + standards-2026-09-21-mcp-spec-2026-07-28-transports.md | knowledge/aliyun-products.md（MCP 协议层事实）
- [done] 2026-09-21 | 竞品文档 | 火山引擎 API 网关「MCP 服务」（HTTP转MCP 仅支持 Streamable HTTP；身份认证=Key Auth 插件） | https://www.volcengine.com/docs/6569/1816086 （经 getDocDetail API 取 MDContent，绕开 SPA JS 壳陷阱） | raw/competitor/competitor-2026-09-21-volc-apig-mcp-service.md | knowledge/competitor-cloud.md（火山 API 网关/AI 网关对标）
- [done] 2026-09-21 | 竞品文档 | 火山引擎「外部认证鉴权」插件（仅实例级、同私有网络硬约束、认证地址自由路径、认证方法可选 GET/POST、前缀或精确匹配、Host/Method/Path/Content-Length 默认走 header） | https://www.volcengine.com/docs/6569/1798159 | raw/competitor/competitor-2026-09-21-volc-apig-external-authentication.md | knowledge/competitor-cloud.md（外部认证对标核心表）
- [done] 2026-09-21 | 竞品文档 | 火山引擎「安全与认证概述」（外部认证=自定义 Token/实例级别/适用已有自建认证体系） | https://www.volcengine.com/docs/6569/2502428 | raw/competitor/competitor-2026-09-21-volc-apig-security-certification-overview.md | knowledge/competitor-cloud.md
- [done] 2026-09-21 | 竞品文档 | 火山引擎「什么是 API 网关」（采用 Envoy 内核，兼容 Kubernetes Ingress 标准 → 技术底座同源结论） | https://www.volcengine.com/docs/6569/82992 | raw/competitor/competitor-2026-09-21-volc-apig-what-is-api-gateway.md | knowledge/competitor-cloud.md
- [done] 2026-09-21 | 开源源码 | Higress ext-auth main.go/config.go 关键片段（endpoint_mode 分支、Authorization 无条件透传、with_request_body×GET 校验、DefaultStatusOnError=403、failure_mode_allow 仅 ≥500、GetRequestPathWithoutQuery）⚠️ 摘录而非全文 | https://github.com/alibaba/higress/tree/main/plugins/wasm-go/extensions/ext-auth | raw/misc/misc-2026-09-21-higress-ext-auth-source-excerpts.md | knowledge/aliyun-products.md（forward_auth 源码级细节）
- [done] 2026-09-21 | ATA | 陈思亮(玄斧)《AI网关-Restful API转换MCP的桥梁》11020495607（唯一 HTTP转MCP+消费者鉴权端到端实操）⚠️ SSO 拦截，仅归档逐字摘录 | https://ata.atatech.org/articles/11020495607 | raw/ata/ata-2026-09-21-http-to-mcp-consumer-auth-excerpts.md | knowledge/aliyun-products.md（MCP 维度 [实战]）
- [done] 2026-09-21 | ATA | 骁霆/王炳松《基于阿里云 AI 网关的万镜一刻 API 接入方案》11020742807 §5.5 五句引文（逐字复核准确）+ 🔴 引用限定（限自定义 HTTP 类型 Model API 链路，非 MCP；不可外推）⚠️ SSO 拦截，仅归档摘录 | https://ata.atatech.org/articles/11020742807 | raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md | knowledge/aliyun-products.md（引用限定 + 避坑「优先域名级」）
- [done] 2026-09-21 | ATA（未归档，登记限定） | 鹤渡/章丹鹰 11020591207（aigw 定位引文准确但无插件生效维度内容，`生效` 0 命中）；筱奥 11020729615《MCP Server 与 Client 之间的鉴权》（**内部 Aone MCP 网关 Normandy，非阿里云产品**，只可当模式参考） | https://ata.atatech.org/articles/11020591207 ；https://ata.atatech.org/articles/11020729615 | （SSO 拦截未归档，限定已写入 raw/ata/ata-2026-09-21-wanjing-yike-plugin-scope-excerpts.md 尾注） | knowledge/aliyun-products.md（引用限定节）
- [done] 2026-09-21 | 客户现场记录 | 合思信息（原易快报）：2026-09-16 现场会议（千问办公生态 MCP 上架诉求）+ 内部记录 2026-04-23（华为云 300 万+ 存量无搬迁计划）+ SA 归属链变更（罗勤/傲罗 2026-09-15 生效）+ S10 网关鉴权 case（A 路 404 → forward_auth 解法）⚠️ 敏感：token/PAT 与客户测试域名**不落盘**（脱敏红线），故不归档 raw | （内部记录，无公开 URL） | - | knowledge/company-profiles.md（合思画像）+ cloud-solutions.md（S10 实战案例）

### 2026-07-07 Meoo（秒悟）AI Vibe Coding 产品官方文档


- [done] 2026-07-07 | 官方文档 | Meoo 介绍 Tab（欢迎/订阅套餐&积分/快速开始/Night Plan/使用技巧/FAQ/更新日志/开票流程）8 页 | https://docs.meoo.com/ | raw/aliyun-docs/meoo/{index,coindesc,file-3,meoo-night-plan,file-12,faq,file-10,file-7}.md | knowledge/aliyun-products.md（Meoo 产品卡）
- [done] 2026-07-07 | 官方文档 | Meoo 功能特性 Tab（Agent 模式/AI 服务/自定义域名/技能/网页搭建/文件存储/支持模型/可视化修改/多人协作/云服务/技能市场/CLI/微信小程序×2）14 页 | https://docs.meoo.com/ | raw/aliyun-docs/meoo/{agent,ai,custom-dependent-domain,file,file-1,file-11,file-2,file-4,file-5,file-6,file-9,meoo-cli,wechat-faq,wechat-miniprogram-desc}.md | knowledge/aliyun-products.md
- [done] 2026-07-07 | 官方文档 | Meoo 团队版 Tab（立即开始/订阅定价/账号登录/团队设置/成员角色/积分管理/席位增购/应用管理）8 页 | https://docs.meoo.com/ | raw/aliyun-docs/meoo/team-*.md | knowledge/aliyun-products.md（团队版章节）
- [done] 2026-07-07 | 官方文档 | Meoo 产品协议 Tab（用户协议/隐私政策/算法备案/技能创建规范）4 页 | https://docs.meoo.com/ | raw/aliyun-docs/meoo/guides/{terms-of-service,privacy,beian,untitled-page}.md | knowledge/aliyun-products.md（监管与合规）

### 2026-08-10 企业级 AI 战略汇报资料包调研（制造业/光伏方向）


- [done] 2026-08-10 | ATA 内网检索 | 60 关键词 × 2026 年内文章，去重 501 篇；核心精读 18 篇，其中 6 篇逐句回源核查 | https://ata.atatech.org/ | knowledge/ai-trends.md 第 10 节 + knowledge/industry-landscape.md 制造卡
- [done] 2026-08-10 | 云知道（yunzhidao.alibaba-inc.com） | GTM 弹药库/市场洞察报告/阿里云总体资料库/MaaS 弹药库全量 5000 篇文档元数据（覆盖 2026-04-14 至 2026-08-10），53 条引用已逐条核对 ID 与标题 | https://yunzhidao.alibaba-inc.com/doc/detail/{id} | knowledge/ai-trends.md 10.9 + knowledge/industry-landscape.md 制造卡可对标案例

## Processing（蒸馏中）

<!-- 正在分析的资料移到这里 -->

## Done（已落盘）

- [done] 2026-06-17 | meta | neil-aliyun-sa skill 骨架建立 | (无外部 URL) | SKILL.md / README.md / changelog.md / knowledge × 6 / references × 5
- [done] 2026-06-17 | 元方法论 | 修炼之路 11 天版 —— 自我演进知识库的协议设计原则（写入优先 / 跨源验证 / 知识与参考分离 / 6 种工作模式） | https://ata.atatech.org/articles/11020643601 | SKILL.md（六种模式 + 写入优先 + 跨源验证）+ README.md（设计说明）
