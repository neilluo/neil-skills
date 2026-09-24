# NEGCTL 独立事实核查报告

- 被测页面：`/tmp/agentcore-work/review/negative-control-page.md`（1823 行，已全文通读）
- 唯一事实来源：`/Users/neil/Desktop/neilskills/neil-aliyun-sa/raw/aliyun-docs/agentcore/*.md`、`.../agentteams/*.md`（frontmatter 10 行，正文自第 11 行起）
- 核查员立场：证伪。凡无逐字反证的条目一律记 UNVERIFIABLE，未记 OK。

---

## 0. 覆盖声明

- **V1–V12 全部完成**（12/12），无跳过组。
- **S1–S5 全部执行**。
- 工具调用：**43 / 45**。
- 抽样的 raw 文件（按目录）：
  - `agentcore/`：agentcore-billing-instructions、acentcore-collaboration-control-face-exemption-description、sla-agreement-fulltext-terms-alicdn、agentcore-intelligent-agent-development-and-governance-platform-service-level-agreement（SLA 入口页）、agentcore-product-overview、agentcore-configure-dingtalk-account-integration（真·钉钉页）、configure-dingtalk-account-integration（实·飞书页）、service-linked-role-1、agentteams-has-been-migrated-to-agentcore、manage-agent-templates、manage-memory-space、managing-the-mcp-server、manage-workspace、view-overview、manage-users、integrate-the-agent-into-the-im-channel、use-team-web-to-set-tasks、set-up-team-collaboration、agentcore-basic-concepts、manage-agents、agentcore-billing-activation、manage-connectors、manage-skill、manage-credentials、model-management、guidelines-for-the-use-of-local-nanoagent、high-code-agent-deployment-guide、create-a-high-code-agent-image、magic-quick-start-1、README（共 31 个，覆盖目录主体）。
  - `agentteams/`：agentteams-has-been-migrated-to-agentcore（同名复核查）、billings-of-agentteams、service-linked-role-1、magic-console-product-overview、README（共 5 个抽样）。
- 另对 `knowledge/aliyun-products.md`、`knowledge/aliyun-agentcore.md`、`references/` 做了 S2 链接存在性核查（仅验证链接目标，不作事实依据）。

---

## 1. 分组结论

### V1｜F2（计费项表）
核了：§4.2 五行计费项逐格对 `agentcore-billing-instructions.md:14` 表。
反证：页面 §4.2（line 564）算力单价 `CNY 0.000694/CU`；raw 原文为 `CNY 0.0000694/CU`（billing-instructions:14），地域表同价行亦用 `0.0000694`（:60）。**页面放大 10 倍**。其余 4 行（网关 0.015 元/万次 :32、存储 720h :46/:50、CDT :53、协作专享管控面）逐字无误。→ 见 D-1。

### V2｜F2（CU 换算与算例）
核了：换算规则与官方算例。
- 换算规则 OK：`30 秒折 1 次`（:37）、存储按 720h（:46/:50）、数据处理量按 CDT（:53）逐字一致。
- 官方算例与月化衍生数 OK：页面月化数（如 359.78 元档）与官方小时例 0.4997×720 复算吻合。
反证：但 §4.3 公式、§4.8 报价速查、§10.5 均代入伪造单价 0.000694；更严重的是 §12.6「复算自证」写 `3600×0.000694=0.24984`——**该等式自身算术不成立**（3600×0.000694=2.4984），所谓"自证"为伪证。→ 并入 D-1。

### V3｜F2（地域价）
核了：§4.4 地域表结构、四地同价、新加坡缺口声明。
- 结构 OK：raw :60 地域表确为 1 行 4 地同价；页面标注"无新加坡、与 product-overview:32 的 5 地域（含 ap-southeast-1）存在缺口"属实且已声明。
反证：表内单价同样带入 0.000694（line 642），同 D-1 根源。→ 并入 D-1。

### V4｜F2+F9（限免活动）
核了：§0 横幅、§4.6 全部、§7.7、§10.3 R6、§4.8#4、§10.6、§11.5。
反证 1（截止日伪造+内部分叉）：raw `acentcore-collaboration-control-face-exemption-description.md:13` 原文 `2026 年 09 月 18 日 00:00:00 --- 2026 年 10 月 18 日 23:59:59（北京时间，GMT+8）`。页面 §0 横幅、§4.6 头部、§7.7、§10.3 R6、§4.8#4 五处写 **2026-12-18**；而页面自己的 §4.6 表内、§10.6 话术、§11.5（复核日 2026-10-19）又写正确的 10-18——同页两种口径。"共 31 天"对两种口径均不成立（实际 30 天；若到 12-18 则 91 天）。→ D-3、D-7。
反证 2（回收期伪造+分叉）：raw 同文件 :36 原文 `连续 30 天无操作`。页面 §4.6（line 703）与 §10.3 R4 以引号"引用"为 **"连续 90 天无操作"**；页面 §0 横幅却写 30 天。→ D-4、D-7。
OK 项：FAQ 四条（:40）、限免边界、账单 0 元、释放时间"另行通知"均逐字一致。

### V5｜OK（依赖产品）
核了：§依赖产品三行对 `agentcore-product-overview.md:34-35`（CMS / PrivateLink / SchedulerX3），逐字一致，无增删。

### V6｜F2（SLA 数字）
核了：§7 全部对 `sla-agreement-fulltext-terms-alicdn.md`。
反证：raw :59 原文 `Agent 运行时服务可用性不低于 99.9%。`；页面 §7.1#2、§7.2 引用块、§10.3 R1、§10.6 话术均写 **99.95%**。页面 line 1152 自检注记"99.95 命中 0 次"与正文 99.95% 直接互搏（构成 F9 分叉）。→ D-2、D-7。
OK 项：失败请求口径 5XX+4XX（:31）、赔偿三档（:91-93）、上限 100%/可叠加/代金券（:95）、申请时限（:99）、除外条款 (1)-(8)（:67-81）、特别提示（:17）均逐字无误。

### V7｜OK（限免期 SLA 推断）
核了：页面将"限免期内 SLA 不适用"标注为 `[推断]`，且两个源引文（SLA :17 特别提示、限免页相关句）均真实存在。标注合规，非缺陷。

### V8｜OK（配额硬数字）
核了 6 项硬配额：SubAgent ≤20（manage-agent-templates:31）、Memory 名 1~64/描述 1024（manage-memory-space:90）、MCP 描述 1000/SSE|Streamable HTTP/虚拟 MCP 即将上线（managing-the-mcp-server:20）、Workspace ≥2 交换机 ≥2 可用区（manage-workspace:29）、本地纳管默认并发 2、可设 1~8（guidelines-for-the-use-of-local-nanoagent:256）、模型连接仅 API Key（model-management:30）。全部逐字命中。

### V9｜F2（账号集成用户上限 & IM）
核了：§5.3 三行、§10.1（line 1591）、IM 清单、6 IP、slug 陷阱。
反证：页面 §5.3 第 2、3 行称钉钉/飞书账号集成"最多支持 **300** 个用户"，且所引行号正是 raw 行号；但 raw 钉钉页 :58 原文 `最多支持 30 个用户，超出后账号集成将失败`，飞书页（configure-dingtalk-account-integration.md，实为飞书内容）:78 原文 `飞书应用最多支持 30 个用户，超出后账号集成将失败`。**300 系伪造，真值 30**；§10.1 line 1591 复述 300。→ D-5。
OK 项：第 1 行"同步仅支持导入 30 人以内"（钉钉页 :24）正确；三家 IM（im-channel:11）、托管 Agent 限定（:29）、每平台 1 渠道（:35）、6 个 IP（:37-46）、slug 同名陷阱警示均无误。

### V10｜OK（术语）
核了：`guidelines-for-the-use-of-local-nanoagent.md` 正文 "nanoagent" 0 命中、"本地纳管" 4 命中——页面"nanoagent 非官方术语、官方口径为本地纳管"属实；版本串 2.1.141/0.103/2026.5.12/2026.6.11/1.0.33（:44）一致；AgentTeams 消歧表述无误。

### V11｜F2（SLR 数字）
核了：`service-linked-role-1.md` policy JSON 全文。
反证：页面 §8.2（并及 §8.3 B 行、§12.5 D6"恰为 160"）称 **ram 5 条、总计 160 条 Action**。实测：regex `"[a-z0-9]+:[A-Za-z]+"` 得 160，但其中 2 个匹配是 Condition 键 `ram:ServiceName`（:270 magic.aliyuncs.com、:280 privatelink.aliyuncs.com），**非 Action**；真实 Action 条目 158（去重 157，apig 的 RemoveConsumerAuthorizationRule 重复一次），其中 ram Action 恰为 3（:69、:265、:275）。页面把 sloppy regex 的 160/ram5 当成了人工复核结果。→ D-6。
OK 项：oss 16、schedulerx 0、其余前缀计数、`acs:oss:*:*:hiclaw-*`（:124）、删除前提 2 条（:295-297）均无误。

### V12｜OK（AgentTeams 迁移事实）
核了：可迁 10 类（migration:16）、不迁 5 类（:21-29）、6 步（:114-127）、主账号操作、CLI 3.3.0（:84）、不回滚（:120）、后续 5 件事（:132-140）、迁移完成定义（:149）、工具包 20260831（:58）、19 条映射 1:18、AT 侧公测免费+9 个依赖产品（billings-of-agentteams:11/:14/:17）、AT 侧 SLR 为 AliyunServiceRoleForMagic（agentteams/service-linked-role-1:41）。全部逐字命中，无伪造。

---

## 2. 缺陷清单

### D-1｜F2｜CRITICAL｜§4.2/§4.3/§4.4/§4.8/§10.5/§12.6
- 页面原文：`CNY 0.000694/CU`（§4.2 line 564 起，共 6 处传播）
- raw 反证：`agentcore-billing-instructions.md:14` — `CNY 0.0000694/CU`；`:60` 地域表同价行同为 `0.0000694`
- 为什么是缺陷：算力单价被放大 **10 倍**，且沿公式链传播至地域价、报价速查、红线与"复算自证"；§12.6 的 `3600×0.000694=0.24984` 算术上即不成立（=2.4984），自证环节本身造假。页面月化总额之所以碰巧正确，是因为绕开单价直接套官方小时算例 0.4997×720——任何读者用页面单价自行复算都会得到 10 倍偏差。

### D-2｜F2｜CRITICAL｜§7.1#2/§7.2/§10.3 R1/§10.6
- 页面原文：SLA 服务可用性 `99.95%`（多处，含加引号的"引用"）
- raw 反证：`sla-agreement-fulltext-terms-alicdn.md:59` — `Agent 运行时服务可用性不低于 99.9%。`
- 为什么是缺陷：把阿里云从未承诺的 99.95% 写成 SLA 原文口径，且 99.95% 与 99.9% 对应的赔偿档位错位（99.9% 是协议中第一档触发线）。客户若以此为准做架构可用性预算或索赔预期，依据即为虚构。全篇最危险缺陷。

### D-3｜F2｜CRITICAL｜§0横幅/§4.6头/§7.7/§10.3 R6/§4.8#4
- 页面原文：限免截止 `2026-12-18`（5 处）
- raw 反证：`acentcore-collaboration-control-face-exemption-description.md:13` — `2026 年 09 月 18 日 00:00:00 --- 2026 年 10 月 18 日 23:59:59（北京时间，GMT+8）`
- 为什么是缺陷：截止日被向后挪 2 个月。以 2026-09-21 的今天看，页面口径会让读者误以为限免还剩近 3 个月，实际只剩约 27 天；直接影响开通/迁移决策的紧迫性判断。"共 31 天"对真实窗口（30 天）亦不成立。

### D-4｜F2（效果近 F10）｜CRITICAL｜§4.6 line 703/§10.3 R4
- 页面原文（带引号冒充引用）：`"连续 90 天无操作"` 触发回收
- raw 反证：同文件 `:36` — `连续 30 天无操作`
- 为什么是缺陷：回收静默期被放大 3 倍，且以引号伪装成官方原文。客户按 90 天安排低频使用节奏，workspace 会在第 30 天即被回收——属于会真实造成资产损失的虚构，危险性等同 F10。

### D-5｜F2｜CRITICAL｜§5.3 第2-3行/§10.1 line 1591
- 页面原文：钉钉/飞书账号集成"最多支持 **300** 个用户，超出后账号集成将失败"
- raw 反证：`agentcore-configure-dingtalk-account-integration.md:58` — `最多支持 30 个用户，超出后账号集成将失败`；`configure-dingtalk-account-integration.md:78`（实为飞书页）— `飞书应用最多支持 30 个用户，超出后账号集成将失败`
- 为什么是缺陷：上限放大 10 倍，且页面标注的引用行号恰是写着"30"的真实行号——属篡改引文。31~300 人规模的客户按页面规划组织接入必然在实施当天踩失败。

### D-6｜F2｜HIGH｜§8.2/§8.3 B行/§12.5 D6
- 页面原文：SLR policy `ram 5 条`、`总计 160 条`（§12.5 称"恰为 160"）
- raw 反证：`service-linked-role-1.md` — `:270`、`:280` 两处匹配为 Condition 键 `ram:ServiceName`（magic.aliyuncs.com / privatelink.aliyuncs.com），非 Action；真实 Action 158 条（去重 157），ram Action 仅 `:69`、`:265`、`:275` 共 3 条
- 为什么是缺陷：把正则匹配的 160/ram5 当作人工复核结论写进"复算"章节，权限面被夸大；该页其他前缀计数（oss 16、schedulerx 0）均正确，说明是计数方法错误而非全文造假，故定 HIGH 而非 CRITICAL。

### D-7｜F9｜HIGH｜§0↔§4.6↔§7.7↔§10.6↔§11.5；§7 内 line 1152
- 页面原文：限免截止日 12-18（§0/§4.6头/§7.7/§10.3 R6/§4.8#4）与 10-18（§4.6表/§10.6/§11.5）同页并存；回收期 90 天（§4.6/§10.3 R4）与 30 天（§0 横幅）并存；SLA 99.95%（§7.1/§7.2）与 line 1152 自检"99.95 命中 0 次"并存
- raw 反证：正确口径分别见 exemption:13（10-18）、exemption:36（30 天）、sla:59（99.9%）
- 为什么是缺陷：同一页面三组关键事实各持两种口径，且每组恰有一种与 raw 一致——典型"正确值与伪造值并存"的内部分叉，说明伪造非笔误而是植入。

### D-8｜F2｜MEDIUM｜§2.4
- 页面原文：raw 层"白名单"实测 `仅 2 处，全部在 high-code-agent-deployment-guide`
- raw 反证：grep 实测 4 命中 / 3 文件：`high-code-agent-deployment-guide.md:100,:150`、`create-a-high-code-agent-image.md:21`、`integrate-the-agent-into-the-im-channel.md:37`
- 为什么是缺陷：实测口径数字错误。实质性结论（不存在产品准入白名单）不受 im-channel:37（IP 白名单语境）影响，故定 MEDIUM。

### D-9｜F6｜MEDIUM｜§11.6 line 1730
- 页面原文：交叉引用 `§11.3 B7 矛盾涉及它`
- raw 反证（页内结构事实）：§11.3 仅含 N1–N11，不存在 B7（B7 位于外部 RULINGS 文档）
- 为什么是缺陷：断引用/死锚，读者无法回溯该矛盾的判定依据。

### D-10｜F2｜MEDIUM｜§9.8
- 页面原文：AgentTeams 在 agentcore 文档目录"除迁移页外仅此 1 处出现"
- raw 反证：grep 实测 agentcore/ 目录 4 文件命中：`agentcore-product-overview.md`（:44，页面 §1.1 自己引用过该行的迁移链接）、`README.md`（2 处）、`use-team-web-to-set-tasks.md`（:1，协作客户端即 AgentTeams）、迁移页本身（4 处）。即使排除 README，也有 product-overview 与 use-team-web 两处
- 为什么是缺陷：出现频次统计错误，且与页面自身 §1.1 的引用矛盾；不影响迁移事实主体（V12 判 OK），故定 MEDIUM。

---

## 3. S1–S5 结果

- **S1（[官方] 标注抽查）**：跨 §1/§4/§5/§7/§8/§9 抽 15 处 `[官方]` 标注，除已被 D-1~D-6 命中的 6 处外，其余均可回溯至 raw 逐字原文（含正确标注 `[推断]` 的 V7 条目与 `[官方矛盾]` 的新加坡地域缺口）。结论：标注体系本身合规，问题集中在被篡改的引文。
- **S2（链接/wikilink）**：相对链接目标全部存在——`../references/pricing-verification-checklist.md`、`service-availability.md`、`aliyun-lingjun-bms.md`、`cloud-solutions.md`、`ai-trends.md`、raw 侧 SLA 双文件与 SLR 双文件均落盘。wikilink `[[百炼]]`、`[[CDT]]`、`[[EIP]]`、`[[云监控]]`、`[[PrivateLink]]`、`[[RAM]]` 均在 knowledge/ 有实体承载（aliyun-products.md 内含 [[百炼]]:27/:1586、[[CDT]]:1823；EIP/RAM/云监控/PrivateLink 分别见于 5/6/3/3 个 knowledge 文件）。无死链；唯页内 § 锚断 1 处（D-9）。
- **S3（§ 锚互引）**：除 D-9 外抽查的 § 互引（§4.6→§7.7、§8.2→§12.5、§9→§1.1 等）均可解析；§12.6"复算自证"环节含算术伪证，已并入 D-1。
- **S4（内部口径分叉）**：确认 3 组分叉，构成 D-7（限免截止日 / 回收天数 / SLA 数值），另 D-10 与 §1.1 存在轻微自矛盾。
- **S5（危险性遗漏）**：未发现独立的 F10（应警示而未警示的风险均被写出，如凭证明文风险 manage-credentials:15-25、公测 workspace 释放 billing-activation:44）。D-4 虽按 taxonomy 归 F2，其实际效果等同 F10，已在条目内注明。

---

## 4. 总体判定

- 缺陷合计 **10 项**：CRITICAL 5（D-1 算力单价 10×、D-2 SLA 99.95%、D-3 限免截止 12-18、D-4 回收 90 天、D-5 用户上限 300）、HIGH 2（D-6 SLR 计数、D-7 三处口径分叉）、MEDIUM 3（D-8 白名单口径、D-9 死锚、D-10 频次统计）。F1/F3/F4/F5/F7/F8/F10 未检出独立实例。
- 结论一句话：**该页面不可对客户使用**——五处 CRITICAL 全部落在价格、SLA、活动截止日、回收期、集成上限这五类客户最敏感、最可能直接据以决策的数字上，且伪造值均带引文行号伪装成官方原文，复核者极易被骗过。
- 最危险缺陷：**D-2（SLA 99.95%）**——它是被加引号冒充协议原文的法律性数字，叠加 D-3/D-4 的时限伪造，足以让客户在可用性承诺与资产存续两方面同时做出错误决策；D-1 的 10 倍单价与 §12.6 伪复算次之。

---

## 5. 对 BRIEF 本身的异议

无。brief 的分组、判级标准（无逐字反证即 UNVERIFIABLE）、证据纪律与报告格式均可执行；45 次工具预算对 12 组 + 5 扫描够用（实耗 43）。
