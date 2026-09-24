# AI 网关知识页评审 · R2a（语义一致性专项）

- 评审员：R2a（独立评审，窄范围：A 跨文件口径一致性 / C 与既有页面冲突 / E SA 可用性）
- 日期：2026-09-21
- 对象：`knowledge/aliyun-ai-gateway*.md`（7 文件，约 9400 行）
- 状态：**已完成**（本报告全程增量落盘，每查完一个主题即写盘）
- 范围纪律：**只做 A（跨文件口径一致性）/ C（与既有页面矛盾）/ E（SA 可用性）三节**。未做交叉引用有效性、章节号存在性、H1/表格列数/页眉要素/行数阈值/`W1~W7` 代号残留（已由 `scripts/lint-aigw-pages.py` 机械覆盖）；未做单条数字回源核验（R1 已抽 74 条）；未逐页通读 9400 行。
- **只读声明**：本次审计除本报告文件外**未写入/修改任何文件**，`knowledge/`、`raw/`、`index.md`、`changelog.md` 全部未动。
- 工具调用预算：约 25 次（含 grep 定位与定点 Read），全部命令在正文中可复算。
- 报告口径：每条缺陷均给出**双方 `文件:行号` + 双方原文摘录**，并附基线（`raw/aliyun-docs/ai-gateway/`）核验命令；凡属主控已裁决（C1~C12）的口径**不作为缺陷重报**，只检查裁决是否在 7 个文件里被一致执行。表述差异未升级为口径矛盾（例：主题 9a「10 条」两侧实质结论相同，仅标 🟡 P2；主题 3 中 `-traffic` 的「本分片内 [文档未说明]」带范围限定与交叉指向，判为一致）。

---

## A 节 · 跨文件同一事实口径一致性

**查了什么**：主控指定的 10 个接缝高风险主题，逐一在 7 个文件中定位「同一事实的多处表述」并比对口径。
**怎么查的**：全部用 grep 定位关键词 → 读命中行上下文，不做通读。可复算命令见每条主题下的 `grep`。
**判定图例**：`一致` / `不一致` / 🔴 `一方标 [官方矛盾] 另一方写成确定事实`。

> 已先读 `tests/ai-gateway-rulings-2026-09-21.md`（R1~R10、C1~C12）与 `tests/ai-gateway-review-r1-fidelity-2026-09-21.md`（D1~D8、7 条已修缺陷）。凡主控已裁决口径（C1/C2 SLA 无赔偿区、C3 入网流量出账方、C4 公测计费页 slug↔正文、C6 slug 交叉错位、C7 frontend-gray 优先级、C8 策略名、C9 MCP 仅 API Key、C10 401/403、C11 Nacos 版本、C12 TLS1.3）**不作为缺陷重报**，只检查「裁决后的口径是否在 7 个文件里被一致地执行」。

---

### 主题 1 · SLA 可用率与赔偿档位（主页 §14.6/§15.5 ↔ `-billing` §3.9）

**判定：`一致`**（裁决 C1/C2 已被两侧一致执行）

```bash
cd /Users/neil/Desktop/neilskills/neil-aliyun-sa/knowledge
grep -n "99\.9\|99\.95\|99\.99\|赔偿\|代金券" aliyun-ai-gateway.md aliyun-ai-gateway-billing.md
```

| 事实 | 主页 | `-billing` | 比对 |
|---|---|---|---|
| SLA 协议承诺（法律口径） | `aliyun-ai-gateway.md:1292`「**普通实例 ≥99.99%** ／ **serverless 实例 ≥99.90%**」 | `aliyun-ai-gateway-billing.md:799-800`「serverless实例 **不低于 99.90%**」「普通实例 **不低于 99.99%**」 | 一致 |
| 无赔偿区 | `aliyun-ai-gateway.md:1185-1186`「**[99.90%, 99.95%) 无赔偿**」（企业版 / 旧版） | `aliyun-ai-gateway-billing.md:823-824`「🔴 **0.05 pp 无赔偿区**」 | 一致（同一区间、同一结论） |
| 赔偿档位 | `aliyun-ai-gateway.md:1189`「三档 **15% / 30% / 100%**」 | `aliyun-ai-gateway-billing.md:842-847` 六行表，两组各 15%/30%/100%，边界「低于 99.99%(99.90%) 但等于或高于 99.00%」 | 一致（主页是压缩表述，未丢边界语义） |
| 赔偿方式与上限 | `aliyun-ai-gateway.md:1189`「仅限代金券，总额不超过当月该实例月度服务费用（不含代金券抵扣部分）」 | `aliyun-ai-gateway-billing.md:836` 逐字同义 | 一致 |
| 申请时限 | `aliyun-ai-gateway.md:1189`「次月第 5 个工作日后、不晚于相关月份结束后 2 个月」 | `aliyun-ai-gateway-billing.md:873` 原文逐字 | 一致 |
| 产品页 99.99% 无限定 | `aliyun-ai-gateway.md:245`「[文档未说明] 本页 `SLA 99.99%` **未带实例类型限定**」+ `:1353`「🔴 **99.99% 不得用于赔偿主张**（裁决 C1）」 | `aliyun-ai-gateway-billing.md:820-829` 同口径 | 一致 |

无问题。

---

### 主题 2 · 四形态起步价与实例费（主页 §15.3 ↔ `-billing` §3 ↔ `aliyun-products.md` 指针卡）

**判定：`一致`（三处数字逐一相同）**

```bash
grep -n "0\.245\|7\.9335\|3,997\.5\|0\.005\|0 元起步\|实例费" \
  aliyun-ai-gateway.md aliyun-ai-gateway-billing.md aliyun-products.md
```

| 形态 | 主页 `aliyun-ai-gateway.md:1268-1271` | `-billing` | `aliyun-products.md:1836` |
|---|---|---|---|
| Serverless 标准版 | 「**0 元起步，无实例费**」 | `:215`「**0 元**（官方明写「0 元起步，无实例费」）」、`:26` | 「**0 元起步无实例费**」 |
| Serverless 企业版 | 「实例费 **0.245 元/小时**（参考单价）+ 用量」 | `:198`「0.245 元/小时」、`:216` 满月 176.4 元 `[推断]` | 「实例费 **0.245 元/小时**（参考单价）+ 用量」 |
| Serverless（旧） | 「CU 兜底 **0.50 元/小时**（内地，`[推断]`）」 | `:380`「中国内地 0.50 元/小时 / 360.0 元/月」、`:27`「CU 数不足 10 万按 10 万计算」 | 「CU **0.005 元/千CU**…**不足 10 万按 10 万计**（内地兜底 ≈0.50 元/小时 `[推断]`）」 |
| 专享实例 | 「最低 `aigw.small.x1` **7.9335 元/小时** / **3,997.5 元/月**（内地）」 | `:69`「中国内地…aigw.small.x1 7.9335 3,997.5」 | 「最低 `aigw.small.x1` **7.9335 元/小时 / 3,997.5 元/月**（内地）」 |
| 金融云倍率 | `:1178`「**金融云 = 内地 × 1.9**（专享实例）」 | `:120`「金融云 = **1.9×**」、`:372`「Serverless（旧）**无金融云行**…禁止外推」 | 「**金融云 = 内地 ×1.9**」 |

三处均带「参考单价 / `[推断]` / 不得外推」限定词，**未发现任何一处把参考价写成成交价**。无问题。

---

### 主题 3 · AI Credits 单价 / 独立商品 / 折算率空白口径

**判定：`一致`（R1 修完后，「模型侧有文档、AI 增强侧真空白」的二分口径在 4 个文件里统一）**

```bash
grep -n "AI Credits\|Credits" aliyun-ai-gateway*.md | grep -v "^aliyun-ai-gateway-plugins"
grep -n "Credits\|计费\|收费\|免费\|公测" aliyun-ai-gateway-plugins.md | head
```

| 事实 | 出处 | 口径 |
|---|---|---|
| Credit 单价 | `-billing:28`「Credit 单价 **0.01 元/Credit**」；主页 `:1279`「AI Credits 账单（**0.01 元/Credit**，独立商品…）」；`aliyun-products.md:1838`「**0.01 元/Credit**」 | 一致 |
| 是否独立商品 | `-billing:425`「独立的按量付费开通型商品，与网关实例的基础计费相互独立」；主页 `:1177`「**AI Credits 是独立商品，网关账单里看不到**」；`aliyun-products.md:1838` | 一致 |
| 单向门 | `-billing:428`「**开通后不支持退订和关闭**」；主页 §15.9 未单列但不冲突 | 一致 |
| 折算率空白 | 主页 `:10`「**AI 增强能力的 Credits 折算率查无**（模型调用侧的 Credits 单价机制有文档：`Credits/1M tokens`、默认 0）」；主页 `:1286` 完整二分表述；`-billing:447-456` §3.5.4 同一二分（含「本条原标题为『Credits 折算率全库查无』…主控已收窄」留痕）；`-traffic:1288/1298` 把智能路由口径明确推给 `ai-credits-billing-details` 并声明「不在 W3 分片」；`-mcp-agent:409/520` 语义检索与工具精选「**[文档未说明]**」；`-plugins:11/317/1507`「34 页对 `AI Credits`/`Credits`/`计费`/`收费`/`免费`/`公测` **全部 0 命中**」 | **一致**。`-traffic` 的「本分片内 [文档未说明]」是**分片限定的真话**且带交叉指向，不构成与 `-billing` §3.5.3「智能路由｜是」的矛盾 |

⚠️ 但 `-billing:11` 与 `aliyun-products.md:1839` 仍残留**收窄前的旧表述**：

- `aliyun-ai-gateway-billing.md:11`：「…AI Credits 折算率**全库查无** → 任何数字不得直接作为对客承诺价」
- `aliyun-products.md:1839`：「**AI Credits 折算率全库查无**（「一次智能路由吃几个 Credit」无解）」
- `aliyun-products.md:1870`（决策树内）：「AI Credits 折算率**全库查无**」
- 对照已收窄口径：`aliyun-ai-gateway.md:10` / `:1286` / `:1339`、`-billing:449`「本条原标题为「Credits 折算率全库查无」…**主控已收窄**」、`-billing:519` G9「🔴 **注意区分**：模型调用侧的 Credits 单价机制**有**文档」

**🟠 P1**：R1 的 D3 修正只落到了正文（§3.5.4 / 主页 §15），**没落到 `-billing` 页眉「对客纪律」和 `aliyun-products.md` 指针卡 + 决策树**。三处仍写「全库查无」，与同库四处「模型侧有文档（`model-metadata`：Credits/1M tokens、默认 0）」直接对不上。SA 只读页眉或只读 `aliyun-products.md` 指针卡（这是最可能的入口）会得到**过宽的错误否定结论**——客户若已配好模型 Credits 单价，SA 会答错「算不出来」。
> 注：这不是「表述差异」。同一份 KB 里 A 处说「全库查无」= 任何一侧都没有；B 处说「模型侧有文档、只有 AI 增强侧查无」。B 是对 A 的**明确收窄并留了修正痕迹**，A 未同步 = 口径不一致。

---

### 主题 4 · 数据处理量公网/私网单价（主页 §14.5 ↔ `-billing` §3.2.4）

**判定：`一致`**

```bash
grep -n "0\.037\|0\.049\|数据处理量" aliyun-ai-gateway.md aliyun-ai-gateway-billing.md aliyun-products.md
```

| 事实 | 主页 | `-billing` | `aliyun-products.md` |
|---|---|---|---|
| 公网 / 私网 | `:1174`「专享实例**私网 0.049 元/GB/h > 公网 0.037 元/GB/h**」；`:1284` 同 | `:128-129`「公共云 公网 0.037／私网 0.049」、`:135`「🔴 **SA 反直觉点**」 | `:1837` ①「数据处理量私网 **0.049** > 公网 **0.037** 元/GB·小时」 |
| 金融云档 | `:1178` 只讲实例费 ×1.9 | `:130-131`「金融云 公网 0.07／私网 0.093」 | — |
| Serverless 新版 | — | `:200`「数据处理量…**不区分公网/私网**，0.037 元/GB/小时」 | — |
| 地域粒度差 | — | `:144`「🔴 本表地域粒度与 3.2.3 实例费用表不一致（同页内部口径差）」 | — |

三处「私网更贵」的反直觉结论口径完全一致，且都带 `[官方｜free-product-templates]` 溯源。无问题。

---

### 主题 10 · Serverless 新版公测是否已结束 / 何时开始计费（🔴 主控指定专查残留）

**判定：`一致`（未发现第三、第四处旧口径残留）**

```bash
grep -n "公测\|免费试用\|免费使用" aliyun-ai-gateway.md aliyun-ai-gateway-traffic.md \
  aliyun-ai-gateway-auth.md aliyun-ai-gateway-mcp-agent.md aliyun-ai-gateway-ops.md \
  aliyun-ai-gateway-plugins.md aliyun-products.md
```

全库 7+1 文件对「公测」的命中逐条过了一遍，**没有任何一处以现在时宣称「新版 Serverless 仍处公测 / 仍免费」**：

| 命中处 | 是否残留旧口径 |
|---|---|
| `aliyun-ai-gateway.md:478-481` §2.5 `[官方矛盾]` | ❌ 不是残留。原文 A 是**逐字引用 2026-07 发布记录**（带 `[new-feature-release-notes-ai-gateway]` 溯源），紧随其后 `:481` 已写明「**公测 2026-08-31 结束、2026-09-01 起正式商业化并开始计费**」+「2026-09-21 主控修正」留痕 |
| `aliyun-ai-gateway.md:955` §2.12 时间线 | ❌ 已带「⚠️ **该公测已结束**…🔴 严禁再对客说「新版 Serverless 还在公测/还免费」」 |
| `aliyun-ai-gateway.md:311` | ❌ 只是「口径滞后于 2026-07 的多租 Serverless 公测」的历史陈述，不涉现状 |
| `-billing:164/168/302/462/475/536-576/747-748` | ❌ 全部是**带时间边界的历史口径**：`:541-544` 时间线表（2026-08-31 结束 / 2026-09-01 商业化 / 快照日 2026-09-21 已在商业化后）；`:548`「公测期计费口径（**已过期**，仅作历史/存量核对用）」；`:576`「🔴 **已过期动作项**」 |
| `-plugins:11/317/1507` | ❌ 「公测」只出现在「34 页对 `公测` 0 命中」的检索词列表里，非现状断言 |
| `-ops:776/961` | ❌ 只是 ComfyUI 配方的「是否为公测能力 [文档未说明]」空白项，与 Serverless 新版无关 |
| `-traffic:1194/1196/1290/1337` | ❌ 讲的是**联网搜索（阿里云信息查询服务）的 15 天免费试用**，与 Serverless 公测是两个对象，不构成口径冲突 |
| `aliyun-products.md:1836/1865` | ❌ 指针卡与决策树只写「0 元起步无实例费」，**未写「公测」也未写「免费」**，与商业化后口径不冲突 |
| `aliyun-products.md:484/487/1824` | ❌ 分别是在线迁移服务、AgentCore，非 AI 网关 |

🟡 **P2（可选优化，非缺陷）**：`aliyun-products.md` 指针卡（1833-1844）**完全没提商业化时间点**。指针卡是 SA 最可能的第一入口，卡里写「Serverless 标准版 0 元起步无实例费」而不写「2026-09-01 起已商业化计费、存量公测实例已自动转商业化」，客户拿公测期印象来问时 SA 少了最关键的一句时间锚。建议补一句，但不构成口径矛盾（卡内没有任何「公测中」表述）。

---

### 主题 5 · 自建认证的路径拼接 / 前缀匹配 / 宽松模式兜底范围（主页 §14.1 ↔ `-auth` §6.6 ↔ `-plugins` ext-auth）

**事实层判定：`一致`。解法层判定：`不一致`（🟠 P1 ×2）**

```bash
grep -n "前缀匹配\|宽松模式\|forward_auth\|ext-auth\|endpoint_mode" \
  aliyun-ai-gateway.md aliyun-ai-gateway-auth.md aliyun-ai-gateway-plugins.md
cd ../raw/aliyun-docs/ai-gateway && grep -ril "endpoint_mode\|ext_auth\|ext-auth\|外部鉴权" .
```

**（1）三条事实完全一致，无问题**：

| 事实 | 主页 | `-auth` |
|---|---|---|
| 真实鉴权 Path = 鉴权API + 原始请求 Path | `:1123`「鉴权请求的真实Path是鉴权API加上原始业务请求的Path后的结果，即/validateToken/order」 | `:300` 同一段逐字 |
| 鉴权 API 的 Path 需前缀匹配 | `:1125`「设置鉴权服务提供的鉴权API的Path，API的Path需是前缀匹配。」 | `:285`/`:314` 同一逐字 |
| 宽松模式仅覆盖「连接失败或 5xx」→ 404 兜不住 | `:1129`/`:1131`/`:1135`「**即使开了官方推荐的宽松模式，也无法兜底，仍然全量拒绝**」 | `:303`「🔴 `[推断]` **兜不住**。404 属 4xx，不在宽松模式覆盖的「连接失败或 5xx」范围内」+ `:306` 推理链明示 |
| 两个「Path 匹配」概念不可混 | `:1138` | `:310-323` §6.6.4 整节 |

主页 `:1133` 明确写「推理链已在 [§6.6](aliyun-ai-gateway-auth.md) 展开」，双向对得上。`aliyun-products.md:1837` ③ 的压缩表述也与两侧一致。

**（2）🟠 P1 — 拥有该主题的 `-auth` §6.6 没有承载「解法」，只给了客户已明确拒绝的那个方案**

- `aliyun-ai-gateway-auth.md:308`（§6.6.3「对客一句话结论」，该节自称 `:254`「🔴🔴 …本章最高价值段」）：
  > 「客户的鉴权服务**必须提供前缀匹配**的鉴权 API（SpringMVC 写 `@RequestMapping("/check/")`），或在网关侧把「鉴权API」配成能与拼接结果匹配的前缀。」
- `aliyun-ai-gateway.md:1141-1142`（主页 §14.1）：
  > 「**解法（`[开源]` 证据，Higress 源码…）**：ext-auth 插件有两种 `endpoint_mode`，其中 **`forward_auth`** 模式固定 path、不拼接原始请求 Path…→ **客户的精确匹配认证接口零改动**。🔴 …「你把 SpringMVC 改成前缀匹配」**是客户明确拒绝的方案**。正确答案在客户已经打开的那个插件里。」
- `aliyun-products.md:1868`（决策树）也带 forward_auth。
- 实测：`grep -n "ext-auth\|forward_auth\|endpoint_mode" aliyun-ai-gateway-plugins.md aliyun-ai-gateway-auth.md` → **两个文件 0 命中**。

即：三处（主页 §14.1、主页 §15.7 表 `:1328`、`aliyun-products.md:1868`）给了零改动解法，**唯独拥有该主题的 `-auth` §6.6 与插件章 `-plugins` §9 完全没有**。SA 从子页进入（这是查细节的自然路径）拿到的只有客户已经拒绝的方案。严重度 🟠 P1（不会答错事实，但会给出无效建议）。

**（3）🟠 P1 — forward_auth 这条「解法」在 AI 网关官方文档里 0 命中，主页未标注这一不确定性**

```bash
cd raw/aliyun-docs/ai-gateway && grep -ril "endpoint_mode\|ext_auth\|ext-auth" .   # → 0 个文件
grep -rln "外部认证" .   # → 仅 upload-plug-in.md（优先级总表一行：外部认证｜插件｜认证阶段｜300）
```

- 主页 `:1141` 已诚实标注证据等级为 `[开源]`（Higress 源码），这点做得对；
- 但主页 `:1141`/`:1328` 与 `aliyun-products.md:1868` 都写成祈使式「**解法 = ext-auth 插件 `endpoint_mode: forward_auth`**」，**没有任何一处标注**「AI 网关官方 186 快照对 `ext-auth`/`endpoint_mode` **零命中**，AI 网关控制台的『外部认证』插件是否暴露该配置项 `[文档未说明]`，属 Higress 开源侧证据，对客前必须在 AI 网关实例上实测」。
- 对照 KB 自己的纪律：`-plugins:233` 对 `cluster-key-rate-limit` 的 `rejected_code` 等每个字段都标了默认值与来源；`-auth:369` 对自建认证的未定义分支逐条标 `[文档未说明]`。同一份 KB 里，这条**唯一无官方文档支撑的对客配置指令**反而是标注最弱的。
- `-plugins:277` 的「外部认证」行只写「§6（W4）」交叉指向，不含任何配置项 → 读者在插件章也查不到 `endpoint_mode`。

严重度 🟠 P1：客户按此配置若在 AI 网关控制台找不到该字段，会直接判 SA 给错方案。

---

### 主题 6 · MCP 是否支持 JWT 消费者认证（主页 §15.8 ↔ `-auth` ↔ `-mcp-agent`）

**判定：🔴 `不一致`（一方已按裁决 C9 写成对客红线，另一方写成确定事实）**

```bash
grep -n "JWT" aliyun-ai-gateway.md aliyun-ai-gateway-mcp-agent.md aliyun-ai-gateway-auth.md | grep -i "mcp\|API Key\|仅支持"
cd ../raw/aliyun-docs/ai-gateway && sed -n '190p' what-is-an-ai-gateway.md && grep -n "仅支持" consumer-certification.md
```

**A 方（裁决后口径：MCP 仅 API Key，不得承诺 JWT）**

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-ai-gateway.md:1325` | 「\| 1 \| **消费者 API-Key** \| 最常见，MCP 场景**唯一官方支持** \| MCP 场景**不得承诺 JWT**（裁决 C9） \|」 |
| `aliyun-ai-gateway-auth.md:11`（页眉对客纪律） | 「MCP 场景对客口径为「**仅支持 API Key**」，不得承诺 JWT。」 |
| `aliyun-ai-gateway-auth.md:112` | 「① MCP 场景**仅支持 API Key**」 |
| `aliyun-ai-gateway-mcp-agent.md:42`（§8.1 限制表首行） | 「消费者认证方式 \| MCP 服务消费者授权"目前仅支持 **API Key** 认证" \| mcp-service-management」 |
| `aliyun-ai-gateway-mcp-agent.md:334`/`:518` | 「🔴 **硬限制（官方原文）**："消费者认证方式需使用API Key，**不支持JWT认证方式的消费者使用语义检索**。"」 |
| `aliyun-products.md:1841` | 「MCP 场景对客口径为「**仅支持 API Key**」不得承诺 JWT」 |

**B 方（写成确定事实：MCP Server 可开启 JWT）**

| 文件:行 | 原文摘录 |
|---|---|
| 🔴 `aliyun-ai-gateway.md:167`（§1.3 能力总表） | 「\| 消费者鉴权 \| **API-KEY、JWT、HMAC 三种**；Model API / **MCP Server** / Agent API **均可按需开启** \| 「对于安全敏感的场景，用户可将消费者凭证托管到 KMS 上」 \| what-is-an-ai-gateway \|」 |
| `aliyun-ai-gateway.md:1022`（§2.12 时间线 2026-01） | 「…**MCP Server 支持 JWT 认证**」 |

**核对基线**（证明这确实在讲同一件事，不是表述差异）：
- `raw/…/what-is-an-ai-gateway.md:190` 逐字：「对于每一个 **Model API、MCP Server 和 Agent API**，均可按需开启消费者鉴权。AI 网关支持 **API-KEY、JWT、HMAC** 三种消费者鉴权方式。」→ 主页 `:167` 是**忠实转述**，但**未带任何限定、未标 `[官方矛盾]`、未指向 C9**。
- `raw/…/consumer-certification.md:36` 与 `:55` 逐字：「认证方式目前仅支持**API Key**认证。」
- 两页 `migration_status` 同为 `current`，同一天快照 → 这是**真实的官方矛盾**，RULINGS C9 已裁：以专页「仅支持 API Key」为对客口径，🔴 不得承诺 MCP 支持 JWT。

**🔴 P0 缺陷 A6-1**：`aliyun-ai-gateway.md:167`（§1.3 能力总表）把被 C9 明确否掉的一方写成了**无条件确定事实**，且 §1.3 是主页最靠前的能力清单（第 161~177 行），SA 读主页第一屏就会拿到「MCP Server 支持 JWT 消费者鉴权」。同一文件 `:1325`（§15.7，第 1325 行）给出相反的红线。**同一文件内自相矛盾 + 跨文件与 `-auth`/`-mcp-agent`/`aliyun-products.md` 四处对撞**。修法：`:167` 的「关键限定」列补「🔴 MCP 场景官方专页称『仅支持 API Key』，不得承诺 JWT（裁决 C9，见 §15.7 / `-auth` §6.4）」。

**🟠 P1 缺陷 A6-2**：`aliyun-ai-gateway-auth.md:152` 的矛盾标注**未同步 C9 裁决**：
> `:152`「🔴 **`[官方矛盾]` MCP 是否支持 JWT**（**不裁决**，双方原文）」

而 RULINGS C9 已裁（「以专页 `consumer-certification` 的『仅支持 API Key』为对客口径（R4-3），同时保留矛盾标注」）。`-auth` 页眉 `:11` 落了裁决口径，但**拥有该矛盾的正文小节仍写「不裁决」且未给对客应采哪一方** → 读者停在 §6.4 会得到「两边都可能对」的印象。修法：`:152` 改为「（**裁决 C9：以专页『仅支持 API Key』为对客口径**，双方原文保留如下）」。

**🟠 P1 缺陷 A6-3（提请主控复核，我不裁决）**：主页 `:1022` 引用的 2026-01 发布记录「MCP Server 支持 JWT 认证」与 C9 之间**没有交叉引用**，且按 RULINGS **R4 自己的优先级表**，「**带日期的公告 / 发布记录 / 变更集**」= 优先级 **2**，「专页」= 优先级 **3** —— C9 的依据是 R4-3（专页优先），但存在一条**优先级更高的带日期发布记录**支持相反结论。RULINGS C9 的矛盾双方只列了 `consumer-certification` 与 `consumer-authentication-authentication`（两者都是专页/入口页），**未把 2026-01 发布记录纳入比较**。
→ 这不是我判「C9 错了」，而是：**同一份 KB 里同时存在「不得承诺 MCP 支持 JWT」（4 处）和「2026-01 起 MCP Server 支持 JWT 认证」的官方发布记录引用（1 处），两者互不引用**，SA 无从判断该说哪句。建议主控把发布记录这条纳入 C9 复核，或在 `:1022` 就地加「⚠️ 与裁决 C9 的对客口径冲突，对客前须核实」。

---

### 主题 7 · 插件优先级数字（`-plugins` §9.2 总表 ↔ 各插件小节 ↔ 主页 §14.10）

**判定：`一致`（差异全部是官方自身的 `[官方矛盾]`，且已被 `-plugins` 逐条标注，主页未与之冲突）**

```bash
grep -n "优先级" aliyun-ai-gateway-plugins.md | head -50
sed -n '/### 14.10/,/### 14.11/p' aliyun-ai-gateway.md
cd ../raw/aliyun-docs/ai-gateway && grep -o "ai-prompt-template</p></td><td><p>[^<]*</p></td><td><p>[0-9]*" upload-plug-in.md
```

| 比对项 | 总表（`-plugins:117-160`，逐字照抄 `upload-plug-in`） | 各插件小节 | 主页 | 判定 |
|---|---|---|---|---|
| `ai-prompt-decorator` | `:157` 区段「ai-prompt-decorator｜默认阶段｜**450**」 | `:326`「运行属性 \| 执行阶段 `默认阶段`，执行优先级 `450` \| `ai-cue-template`」 | `:1147` 区（§14.10 表）「**ai-prompt-decorator** \| prepend/append，优先级 **450**」 | 一致 |
| `ai-prompt-template` | 「ai-prompt-template｜默认阶段｜**500**」 | `:352`「执行优先级 `500` \| `ai-cue-decorator`」 | §14.10「**ai-prompt-template** \| templates，优先级 **500**」 | 一致 |
| `frontend-gray` | `:133`「前端灰度｜插件｜认证阶段｜**450**」 | `:1085`「🔴 `[官方矛盾]`（优先级）：本页「运行属性」写…**`1000`**，而 `upload-plug-in` 总表写…**`450`**。双方原文已摘，**不裁决**」 | 主页**未出现** frontend-gray（`grep -n "前端灰度\|frontend-gray" aliyun-ai-gateway.md` → 0 命中） | 无冲突（裁决 C7 = 不裁决，`-plugins:11` 页眉已带 C7 警示）。⚠️ 见 E 节 E2-③：这条 C7 红线只在插件章，主页速查卡没有 |
| `ai-rag` | 「ai-rag｜默认阶段｜**405**」 | `:381`「执行优先级 `400` ← 🔴 `[官方矛盾]`：总表写…**405**」 | 未出现 | 无冲突（已标注） |
| `ai-transformer` | 「请求/响应转换｜认证阶段｜**410**」 | `:436`「认证阶段，执行优先级 `410`」；`:252`/`:445` 标 `[官方矛盾]`（**系列归类**：传输协议 vs AI 系列） | 未出现 | 数字一致，归类矛盾已标注 |
| 六个认证插件 | `:138-147` OAuth2 350 / JWT 340 / HMAC 330 / Basic 320 / Key 310 / 外部认证 300 / OPA 225 / JWT Logout 50 | `:515` 逐列回填同数字；`:521` 明示「六个认证插件页**都没有「运行属性」小节**，阶段与优先级只能从 `upload-plug-in` 总表回填」 | 未出现 | 一致（且诚实标注了回填来源） |
| `key-rate-limit` / `cluster-key-rate-limit` | 「基于Key限流｜默认阶段｜**10**」「基于Key集群限流｜默认阶段｜**20**」 | `:874`「默认阶段 / **10**（总表；插件页无「运行属性」）｜默认阶段 / **20**（页内「运行属性」与总表两处一致）」 | 未出现 | 一致 |
| `custom-response` | **总表未收录** | `:245`「`upload-plug-in` 总表**未收录** custom-response（阶段/优先级 `[文档未说明]`）」 | 未出现 | 一致（空白被如实标注） |

无缺陷。`-plugins` 对优先级的处理是本次审计里标注质量最高的一块：总表逐字照抄、页内值与总表值并列、差异一律 `[官方矛盾]` 不自行调和、缺失一律 `[文档未说明]`。

---

### 主题 8 · SLR 的 Action 条数与产品前缀分布（主页 §14.8 ↔ `-auth` §7.6 ↔ `-ops` §13）

**判定：数字`一致`；🟡 P2 一处「两张表被并列在同一句里」的易误读**

```bash
grep -n "179\|178\|166\|165\|140 个\|66 个\|47\.1" \
  aliyun-ai-gateway.md aliyun-ai-gateway-auth.md aliyun-ai-gateway-ops.md aliyun-products.md
cd ../raw/aliyun-docs/ai-gateway && grep -c "apig:" service-association-role-provided-only-when-involved-otherwise-no-need.md
```

| 事实 | 主页 §14.8 | `-auth` §7.6 | 判定 |
|---|---|---|---|
| SLR-A（`AliyunServiceRoleForNativeApiGw`）Action 数 | `:1203`「原文 **166 行** / 去重 **165** 条 Action，**9 个产品前缀**」 | `:1085` 合计行「**9 个产品** \| **166** \| **165** \| **1 项重复**」；`:1087`「`slb:ModifyLoadBalancerInternetSpec` …出现 **2 次**…原文 **166** 行、去重后 **165** 条」 | 一致（含重复项归因也一致） |
| 前缀分布 | `:1203`「`slb` 45、`nlb` 30、`ecs` 28、`arms` 20、`vpc` 19、`cs` 11、`fc` 6、`mse` 4、`edas` 3；另有 `InvokeFC` 1 条、`InvokeKMS` 12 条」 | `:1100`「`slb` 45 ｜ `nlb` 30 ｜ `ecs` 28 ｜ `arms` 20 ｜ `vpc` 19 ｜ `kms` 12 ｜ `cs` 11 ｜ `fc` 6+1 = **7** ｜ `mse` 4 ｜ `edas` 3」 | 一致（45+30+28+20+19+11+6+4+3=166；主页把 InvokeFC 的 1 条单列，`-auth` 并入 `fc`=7，同一事实两种呈现） |
| 三个 SLR 合计 | `:1203`「**三个 SLR 合计 179 条 / 去重 178 条**」 | `:1100`「**三个 SLR 合计**：原文 **179** 条 Action，去重后 **178** 条」 | 一致 |
| `Resource` 全为 `"*"` | `:1201`「SLR 三个角色的 **`Resource` 全为 `"*"`，无资源级收窄**」 | `:1066`「三个 SLR 的**每一条** Statement 都是 `"Resource": "*"`」；`:1129` 同 | 一致 |
| RAM 授权信息页的 `apig:` Action | `:1201`「**140 个 Action 中 66 个（47.1%）** 标「全部资源」」；`:1244`「140 个 Action 中无 Model API / Agent API…专属 Action」 | `-auth:662` 明示「`apig:` 下完整 Action 枚举、资源类型 ARN 全集**归 W7**」 | 一致（`-auth` 主动让位，未重复计数） |
| 同上 | — | `-ops:992`「合计 **140 个 Action，无重名**」；`:1136`「Action 总数 **140 个**」；`:1153`「**全部资源** \| **66** \| 47.1%」；`:1165`「只有 74 个支持资源级授权，66 个（47.1%）…」 | 一致（66+74=140 ✓） |
| `aliyun-products.md:1840` | 「SLR 三个角色的 `Resource` **全为 `"*"`**；140 个 Action 中 **66 个（47.1%）**」 | — | 与主页 `:1201` 同句式 |

**🟡 P2 缺陷 A8-1（易误读，非数字矛盾）**：主页 `:1201` 与 `aliyun-products.md:1840` 把**两张不同的表**用分号并列在同一句里：

> `aliyun-ai-gateway.md:1201`：「SLR 三个角色的 **`Resource` 全为 `"*"`，无资源级收窄**；**140 个 Action 中 66 个（47.1%）** 标「全部资源」；MCP / AI 模型元信息 / 消费者组 / 插件四类对象在 RAM 层面根本没有 ARN 定义」

- 前半句的对象是 **SLR 策略 JSON**（`AliyunServiceRolePolicyForNativeApiGw` 等，**179/178 条**，前缀为 slb/nlb/ecs/…，**`apig:` 命中 = 0 条**，已实测 `grep -c "apig:" service-association-role-….md` → **0**）；
- 后半句的「140 个 Action」对象是 **AI 网关自己的 RAM 授权信息页**（`api-apig-2024-03-27-ram-ai-gateway`，全是 `apig:` 前缀）。
- 句中未点明这是两张表，紧接着的 `:1203` 才给出 179/178。客户问「AI 网关的服务关联角色有多少权限」时，只读 `:1201` 的 SA 可能答成「140 个 Action，其中 66 个不能资源级授权」——那是**另一个对象**的数字。
- 修法（≤1 句）：`:1201` 改为「…**（SLR 侧）**：SLR 三个角色的 `Resource` 全为 `"*"`…**（AI 网关自身 RAM 授权信息页侧，与 SLR 是两张不同的表）**：140 个 `apig:` Action 中 66 个…」。`-ops:11` 页眉同样只写「140 个 Action」，但其 §13.4 `:1529` 已明确溯源到 `api-apig-2024-03-27-ram-ai-gateway`，风险低于主页。

---

### 主题 9 · 限流「10 条」是配置上限还是命中上限 / 限流超限返回码（主页 §14.11 ↔ `-traffic` §5）

**9a「10 条」判定：`一致`（实质结论相同，仅标注强度不同 → 🟡 P2）**

```bash
grep -n "10 条\|同时命中" aliyun-ai-gateway.md aliyun-ai-gateway-traffic.md
```

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-ai-gateway.md:1238` | 「**限流规则「10 条」是命中上限不是配置上限**：官方问答「最多可以配置多少条」→「最多只支持**同时命中** 10 条」，问答不对齐；**配置上限两页均未说明**。」 |
| `aliyun-ai-gateway-traffic.md:600-602` | 「**[歧义｜不裁决] 「10 条」是配置上限还是命中上限**」+ 两页原文并列 |
| `aliyun-ai-gateway-traffic.md:849` | 「最多只支持同时命中 10 条规则。您可以根据业务需求灵活组合不同维度的规则，但**建议控制规则数量以确保性能**」 |
| `aliyun-ai-gateway-traffic.md:1322` | 「**单个 Model API 可配置的限流规则条数上限**（区别于「最多同时命中 10 条」）—— [文档未说明]」 |

🟡 **P2**：主页 `:1238` 用**确定句式**（「是命中上限不是配置上限」）表述，`-traffic:600` 标为 `[歧义｜不裁决]`。但两侧**实质结论相同**（都认定「同时命中 10 条」是官方明文、配置上限查无），主页也在同句尾写了「配置上限两页均未说明」。属**标注强度差**，不构成口径矛盾。可选修法：主页 `:1238` 句首加「官方明文只支持『同时命中 10 条』；是否兼作配置上限 `[歧义｜不裁决]`（见 `-traffic` §5.x）」。

**9b 限流超限返回码 判定：🔴 `不一致`（P0，R1 的 D3 修正只落了一处）**

```bash
grep -n "429" aliyun-ai-gateway.md aliyun-ai-gateway-traffic.md aliyun-ai-gateway-plugins.md
cd ../raw/aliyun-docs/ai-gateway && sed -n '54p' custom-response-plugin.md
```

**A 方（已修正口径：一般返回 429）**

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-ai-gateway-traffic.md:989` | 「🔴 **2026-09-21 主控修正（R1 判定 D3）**：限流两页本身**确实未写**状态码，但**别页有明文答案** —— `custom-response-plugin`「**触发网关限流时一般会返回429状态码**…」`[官方原文｜custom-response-plugin]`<br>**对客口径**：限流命中一般返回 **429**，且可用 custom-response 插件自定义应答内容」 |
| `aliyun-ai-gateway-plugins.md:1154` | 「`enable_on_status: [429]` + `status_code: 302` …⇒「触发网关限流时一般会返回429状态码」时改为 302」 |
| `aliyun-ai-gateway-plugins.md:245` | 「限流场景官方推荐：`enable_on_status: [429]`…」 |
| 基线核对 | `raw/…/custom-response-plugin.md:54` 逐字：「触发网关限流时一般会返回429状态码，这时请求将返回自定义应答如下。」（另 `:48`、`:80` 两处 `429` 列表项）→ **A 方有据** |

**B 方（仍是修正前的旧口径：文档未说明、不可类推、先答空白）**

| 文件:行 | 原文摘录 |
|---|---|
| 🔴 `aliyun-ai-gateway-traffic.md:11`（**页眉「对客纪律」，全文最高可见度位置**） | 「限流超限的 HTTP 状态码/响应体文档**未说明**（只有另一套 API 级策略写了默认 429，**不可套用**）…客户问「限流了返回什么」「Token 怎么算」时，**先答空白**再给实测建议，**不要拿邻近机制类推**。」 |
| 🔴 `aliyun-ai-gateway.md:1237`（主页 §14.11 避坑速记） | 「**只有④写了「Http状态码默认为429」，①②③的超限返回码全部 `[文档未说明]`，不可类推。**」 |
| `aliyun-ai-gateway-traffic.md:569`（四套限流对比表） | 「「命中任一规则即触发限流」（返回的 HTTP 状态码与响应体 **[文档未说明]**）」×3 列 |
| `aliyun-ai-gateway-traffic.md:1317`（本章空白清单 #1） | 「**限流触发后返回的 HTTP 状态码、响应体、错误码** —— current-limiting 与 configure-a-modelapi-throttling-policy 两页均 [文档未说明]（客户高频问题…）」 |
| `aliyun-ai-gateway-traffic.md:1280` | 「AiTokenRateLimit 的超限返回码在两页限流文档中均未写」 |

🔴 **P0 缺陷 A9-1**：同一个客户高频问题（「AI 网关限流了返回什么状态码？」），**同一份 KB 给出两个相反的对客口径**：
- 读 `-traffic:989` → 答「一般返回 **429**，还可用 custom-response 自定义应答」（有 `custom-response-plugin` 官方原文支撑）；
- 读 `-traffic:11` 页眉 / 主页 `:1237` / `-traffic:1317` → 答「**文档未说明**，不可类推，先答空白再建议实测」。

而且**旧口径占据了三个更高可见度的位置**（子页页眉「对客纪律」、主页避坑章、子页本章空白清单第 1 条），新口径只在正文一张表格的单元格里。SA 按阅读顺序大概率先撞到旧口径。这与主题 3 的 Credits 折算率是**同一失效模式**：R1 的 D3「空白被填」修正只改了正文落点，**没有回扫页眉 / 主页避坑章 / 本章空白清单**。

修法（三处，均为局部改写，不动 A 方结论）：
1. `-traffic:11` 页眉改为「限流超限返回码：限流两专页未写，但 `custom-response-plugin` 明文「触发网关限流时一般会返回429状态码」→ 对客口径 **一般 429**（见 §5.x）；真空白是「是否对全部限流单位一律成立」与「未装 custom-response 时的默认响应体」」。
2. `aliyun-ai-gateway.md:1237` ①②③ 后补「（🔴 但 `custom-response-plugin` 明文「触发网关限流时一般会返回429状态码」→ 一般 429；详见 `-traffic` §5.x）」。
3. `-traffic:1317` 空白 #1 从「状态码/响应体/错误码 [文档未说明]」收窄为「**默认响应体与错误码** [文档未说明]（状态码已由 `custom-response-plugin` 给出 429）」。

> 注：`-traffic:569` 对比表与 `:1280` 讲的是「**限流两专页本身**未写」，这句在其自身范围内仍为真，可保留；但建议在 `:569` 表内加一格交叉指向 `:989`。

---

### A 节小结（10 个主题）

| # | 主题 | 判定 | 缺陷 |
|---|---|---|---|
| 1 | SLA 可用率与赔偿档位 | `一致` | — |
| 2 | 四形态起步价与实例费（含 `aliyun-products.md`） | `一致` | — |
| 3 | AI Credits 单价/独立商品/折算率空白 | `不一致` | 🟠 A3-1（「全库查无」旧口径残留 3 处：`-billing:11`、`aliyun-products.md:1839`、`:1870`） |
| 4 | 数据处理量公网/私网单价 | `一致` | — |
| 5 | 自建认证路径拼接/前缀匹配/宽松模式 | 事实`一致`、解法`不一致` | 🟠 A5-2（`-auth` §6.6 缺 forward_auth 解法）、🟠 A5-3（forward_auth 官方 0 命中未标注） |
| 6 | MCP 是否支持 JWT | 🔴 `不一致` | 🔴 A6-1（主页 `:167` 写成确定事实）、🟠 A6-2（`-auth:152` 未同步 C9）、🟠 A6-3（发布记录 vs C9 未交叉） |
| 7 | 插件优先级数字 | `一致` | — |
| 8 | SLR Action 条数与前缀分布 | `一致` | 🟡 A8-1（两张表并列易误读） |
| 9 | 限流「10 条」/ 超限返回码 | 9a `一致` / 9b 🔴 `不一致` | 🟡 A9-a、🔴 A9-1（429 vs「文档未说明」，旧口径占 3 个高可见位置） |
| 10 | Serverless 公测是否结束 | `一致`（**无第三、第四处残留**） | 🟡 A10-1（指针卡缺商业化时间锚，可选） |

---

## A 节附加发现（超出 10 个主题，但属同一「跨文件对不上」类型，一并上报）

### A11 · 🔴 P0 「OpenAPI 有没有 MCP 专用 Action」—— 主页与 `-mcp-agent` 说「没有」，`-ops` 列出 8 个，raw 站在 `-ops` 一边

```bash
grep -n "CreateMcpServer\|ListMcpServers\|MCP管理\|MCP（整套）" aliyun-ai-gateway-ops.md
grep -n "OpenAPI 无 MCP 专用 Action" aliyun-ai-gateway.md
sed -n '1086,1090p' aliyun-ai-gateway-mcp-agent.md
cd ../raw/aliyun-docs/ai-gateway && grep -o "CreateMcpServer\|ListMcpServers\|DeployMcpServer\|SyncMCPServers\|UnDeployMcpServer" \
  api-apig-2024-03-27-overview-ai-gateway.md | sort | uniq -c
```

**A 方（写成确定事实：没有 MCP 专用 Action）**

| 文件:行 | 原文摘录 |
|---|---|
| 🔴 `aliyun-ai-gateway.md:1244`（§14.11 其他高频踩坑速记） | 「**OpenAPI 无 MCP 专用 Action**：管理 MCP 的**唯一写操作**是 `UpdatePluginAttachment`（`pluginConfig` = YAML 的 base64）+ `ImportHttpApi`；且 140 个 Action 中**无** Model API / Agent API / AI 服务 / AI 日志策略的专属 Action」 |
| 🔴 `aliyun-ai-gateway-mcp-agent.md:1086-1087`（§8.18.1） | 「**🔴 关键结论：OpenAPI 层面没有"MCP 专用 Action"**」／「6 个 Action 全部是通用 **HttpApi / Plugin / PluginAttachment** 资源，**没有** `CreateMcpServer`、`ListMcpServers`、`CreateMcpTool`、`DeleteMcpServer` 之类。」 |

**B 方（列出 8 个 MCP 专用 Action）**

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-ai-gateway-ops.md:999`（§13.1 Action 分组，合计 140） | 「\| MCP管理 \| **8** \| `CreateMcpServer`、`UpdateMcpServer`、`GetMcpServer`、`ListMcpServers`、`DeleteMcpServer`、`DeployMcpServer`、`UnDeployMcpServer`、`SyncMCPServers`（同步 Nacos MCP 到网关） \|」 |
| `aliyun-ai-gateway-ops.md:1172`（§13.4「66 个标为『全部资源』的 Action」清单内） | 「\| **MCP（整套）** \| **8** \| `CreateMcpServer`、…、`SyncMCPServers` \|」 |
| `aliyun-ai-gateway-ops.md:1098` | 「集中在 **MCP 管理**（`CreateMcpServer`/…/`SyncMCPServers` 全部为 `50/1(s)`）」 |
| `aliyun-agentcore.md:1335` | 「策略含 `apig:CreateMcpServer`/`DeployMcpServer` 等 → MCP Server 由 API 网关承载」 |
| `aliyun-ai-gateway.md:1350`（§15.10，**与 `:1244` 同文件相距 106 行**） | 「AgentCore 的服务关联角色策略里含 **57 条 `apig:` Action**（含 **`apig:CreateMcpServer`/`DeployMcpServer`**）」 |

**基线核验（raw 站在 B 方）**：
```
raw/…/api-apig-2024-03-27-overview-ai-gateway.md : CreateMcpServer 1 / DeployMcpServer 1 / ListMcpServers 1 / SyncMCPServers 1 / UnDeployMcpServer 1
raw/…/api-apig-2024-03-27-ram-ai-gateway.md      : CreateMcpServer 2 / DeployMcpServer 4 / ListMcpServers 2
raw/…/api-apig-2024-03-27-quota-ai-gateway.md    : 命中
```

**判定：🔴 P0 不一致，且 A 方为错。** `-mcp-agent:1087` 的表述在其**自身范围内**（`openapi-management-mcp` 那一页只列了 6 个 Action）是真的，但它被写成了「**🔴 关键结论：OpenAPI 层面没有 MCP 专用 Action**」这种**全局断言**，没有任何范围限定词；主页 `:1244` 进一步把它升级成「**唯一写操作**是 `UpdatePluginAttachment` + `ImportHttpApi`」。而同一 KB 的 `-ops` §13.1 用脚本逐组计数给出 140 个 Action 里 **MCP管理 = 8 个**，raw 三个元页均命中 `CreateMcpServer`。

**对客后果**：SA 按 `:1244`/`:1086` 会告诉客户「AI 网关没有 MCP 的 OpenAPI，只能用 `UpdatePluginAttachment` 改 base64 插件配置来做自动化」——这是**错的**，客户会据此设计一套更复杂、更脆弱的自动化方案，而实际有 `CreateMcpServer`/`DeployMcpServer`/`SyncMCPServers` 等专用 Action 可用。同时它与主页自己 `:1350` 引用的 `apig:CreateMcpServer` 直接对撞。

**修法**：
1. `aliyun-ai-gateway.md:1244` 改为「🔴 **MCP 的 OpenAPI 分两套口径**：`openapi-management-mcp` 专页只列 6 个**通用** Action（HttpApi/Plugin/PluginAttachment，写操作只有 `UpdatePluginAttachment` + `ImportHttpApi`）；而 OpenAPI 概览/RAM/配额三个元页另有 **8 个 MCP 专用 Action**（`CreateMcpServer`/`UpdateMcpServer`/`GetMcpServer`/`ListMcpServers`/`DeleteMcpServer`/`DeployMcpServer`/`UnDeployMcpServer`/`SyncMCPServers`，见 `-ops` §13.1）。两套的关系官方未说明 `[官方矛盾]` → 自动化设计以概览页 8 个为准，`[文档未说明]`  remains for Model API / Agent API / AI 服务 / AI 日志策略（这些确实无专属 Action）」。
2. `aliyun-ai-gateway-mcp-agent.md:1086` 标题加范围限定：「**本页（`openapi-management-mcp`）涉及的 6 个 Action 中没有 MCP 专用 Action**」，并在 `:1087` 后补「⚠️ 但 OpenAPI 概览页另有 8 个 MCP 专用 Action（归 W7 §13.1），本条不得读作『AI 网关 OpenAPI 无 MCP 专用 Action』」。

---

### A12 · 🔴 P0 公网流量出账方（CDT vs 网关侧）—— 主页 §15 与指针卡写成无条件 CDT，`-billing` 按形态分两种

```bash
grep -n "CDT" aliyun-ai-gateway.md aliyun-ai-gateway-billing.md aliyun-products.md
```

**A 方（无条件 CDT）**

| 文件:行 | 原文摘录 |
|---|---|
| 🔴 `aliyun-ai-gateway.md:1354`（§15.10 与相邻产品的关系） | 「**CDT**：公网流量**统一由 CDT 计费出账**。」 |
| `aliyun-ai-gateway.md:1284`（§15.4 三本账） | 「…**公网流量走 CDT 统一出账**。」（前两项分别限定「专享实例」「Serverless（旧）」，第三项**无限定词**） |
| `aliyun-ai-gateway.md:1281`（§15.4 总成本公式） | 「④ 连带云产品（**CDT 公网流量** / SLS 日志 / …）」；而同式 ① 写「网关账单（实例费 + 数据处理量 + **公网流量**）」→ **公网流量同时出现在 ① 和 ④** |
| `aliyun-products.md:1842`（指针卡·依赖/连带） | 「走 **[[CDT]] 出公网流量账单**」 |
| `aliyun-products.md:1838`（指针卡·报价三本账） | 「另有 **CDT 公网流量** / SLS 日志 / …单价文档全部未说明」 |
| `aliyun-ai-gateway.md:1204`（§14.8） | 「连带账单至少 6 类：**公网流量/CDT**、SLS 日志…」 |

**B 方（按形态分两种，`-billing` 内部自洽且有原文）**

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-ai-gateway-billing.md:394`（§3.4.7） | 「🔴 与新版 Serverless 的**根本差异**：旧版公网流量走 **CDT 出账**，**新版公网出入网流量走网关侧账单 0.8 元/GB**。同一客户从旧版迁到新版，公网流量这一项的**出账产品和单价口径都会变**」 |
| `aliyun-ai-gateway-billing.md:269-270`（§3.3） | 「公网出网流量 \| … \| **网关侧** \| 0.8 元/GB \| 「如果自行配置了 NAT 网关…**网关侧不产生此部分费用**」」／「公网入网流量 \| … \| **网关侧** \| 0.8 元/GB」 |
| `aliyun-ai-gateway-billing.md:495-496`（§3.7 连带表） | 「公网流量 · **专享实例** → **CDT**」／「公网流量 · **Serverless（旧）** → **CDT**」（**新版不在此表，因为新版走网关侧**） |
| `aliyun-ai-gateway-billing.md:565-566`（§3.8.1） | 「公测期（2026-07-31～08-31）\| **CDT**」／「商业化后（2026-09-01 起）\| **网关侧**（进 AI 网关账单）\| 0.8 元/GB」 |
| RULINGS **C3** | 「两页互不引用、均未说明切换 → 保留 `[官方矛盾]`，对客口径：**以商业化后的账单实际出账方为准，报价前必须走购买页/工单确认**」 |

**判定：🔴 P0 不一致。** 主页 §15（速查卡，SA 的第一入口）与 `aliyun-products.md` 指针卡把「公网流量走 CDT」写成**无条件事实**，而 `-billing` 明确区分：**专享实例 / Serverless（旧）→ CDT**，**Serverless 新版（标准版/企业版）→ 网关侧账单 0.8 元/GB（出网+入网都收）**。RULINGS C3 还要求「以账单实际出账方为准、报价前必须核验」，这条口径**在主页 §15 与指针卡里都不存在**。

**为什么这是 P0 而不是 P1**：主页 §15.3 选型表把 **Serverless 企业版推荐给「生产」**，即**最可能被选的形态恰好是唯一不走 CDT 的那个**。SA 只看 §15 会：① 漏报 0.8 元/GB × (出网+入网) 的网关侧费用；② 把客户引到 CDT 定价页去核一个不会出现在 CDT 账单里的费用；③ 漏掉「自建 NAT 网关可免网关侧出网流量费」这个真实的省钱开关（`-billing:269`/`:274`）。

**修法**：
1. `aliyun-ai-gateway.md:1354` 改为「**CDT**：**专享实例与 Serverless（旧）**的公网流量统一由 CDT 计费出账；🔴 **Serverless 新版（标准版/企业版）的公网出网+入网流量改由网关侧计费，0.8 元/GB（参考单价），不进 CDT 账单**（裁决 C3 未裁切换说明，报价前以账单实际出账方为准 + 购买页核验；自建 NAT 网关可免网关侧出网流量费）。见 `-billing` §3.3/§3.4.7/§3.8.1」。
2. `aliyun-ai-gateway.md:1284` 第三项补形态限定；`:1281` 公式把「公网流量」从 ① 与 ④ 的二义中拆开（新版进 ①，专享/旧版进 ④）。
3. `aliyun-products.md:1842`/`:1838` 同步加形态限定（指针卡是 SA 最可能的唯一入口）。

---

## C 节 · 与知识库既有页面的冲突

**查了什么**：`aliyun-products.md`（主控新加的 AI 网关指针卡 1833-1844 + AI 选型决策树 1861-1870）、`aliyun-agentcore.md`（`apig` 相关）、`service-availability.md`（SLA 四层交付模型）。只查**矛盾**，不查重复。

**怎么查的**：
```bash
grep -n "AI 网关\|AI网关" knowledge/aliyun-products.md
sed -n '1833,1870p' knowledge/aliyun-products.md          # 指针卡 + 决策树逐行与 7 个新文件比对
grep -n "57\|apig:\|AliyunServiceRoleFor" knowledge/aliyun-agentcore.md
grep -c "网关" knowledge/service-availability.md            # → 0
cd raw/aliyun-docs/ai-gateway && grep -ril "a2a" .          # → 仅 what-is-an-ai-gateway.md
```

### C-1 🔴 P0 · A2A 协议转换：指针卡写「189 页零命中」，但 raw 里核心页明确宣称该能力，主页自己也正向引用了它

**三方原文**：

| 文件:行 | 原文摘录 | 性质 |
|---|---|---|
| 🔴 `aliyun-products.md:1841`（指针卡·术语与 slug 警示） | 「**A2A 协议转换 189 页零命中**不得承诺」 | 全局否定断言 |
| 🔴 `aliyun-ai-gateway.md:1243`（§14.11） | 「**A2A 协议转换：21 页全文检索零命中** → llms.txt 产品描述里写了「A2A 协议转换」，但**核心范围文档查无**，不得对客承诺。」 | 由 21 页外推到「核心范围文档查无」 |
| `aliyun-ai-gateway-mcp-agent.md:11`/`:732`/`:1371` | 「A2A 协议转换 **21 页零命中**，不得对客承诺」／「本章 **21 页**快照中未出现 "A2A" 字样（已全文检索确认）」 | **范围限定正确**（21 页 = W5 分片） |
| ⚔️ `aliyun-ai-gateway.md:176`（§1.3 能力总表，正向） | 「Agent 接入 \| 直连 ACK、FC、SAE；服务发现统一暴露不同计算平台的 AI 应用；提供 **REST 到 A2A 协议的转换能力**；推荐「基于A2A协议通过Nacos AI Registry实现服务的注册与发现」 \| … \| **what-is-an-ai-gateway**」 | 正向能力宣称，带 slug |
| `aliyun-ai-gateway.md:289`（§1 空白清单第 10 条） | 「A2A 协议的**支持程度**（是否完整实现规范、支持哪些 A2A 版本）—— **只提**「REST 到 A2A 协议的转换能力」和「推荐基于A2A协议通过Nacos AI Registry」」 | ✅ 这才是准确口径 |
| `aliyun-products.md:1897`/`:1911` | 「**AI/Agent 生态**（企业版 Nacos 3.x）：MCP Registry、**A2A Registry**、AI 安全护栏」 | 同文件内另一处正向引用 A2A |

**基线核验（可复算）**：
```bash
cd raw/aliyun-docs/ai-gateway && grep -ril "a2a" .     # → 仅 ./what-is-an-ai-gateway.md（1 个文件）
grep -in "a2a" what-is-an-ai-gateway.md                # → 3 行命中：29 / 117 / 125
```
`what-is-an-ai-gateway.md:125` 逐字：
> 「**灵活性**：AI 网关通过服务发现功能，统一暴露部署于不同计算平台的 AI 应用，并**提供 REST 到 A2A 协议的转换能力，实现存量 HTTP 应用向 A2A 协议的自动化升级**。」

而 `what-is-an-ai-gateway` **就是 curator 指令给定的入口页、属 core 189 页之内**（RULINGS R1）。

**判定**：
- `aliyun-products.md:1841` 的「**189 页零命中**」= **可复算为假**（1 个核心页 3 行命中）。🔴 **P0**：SA 会据此对客否认一项官方概述页明文宣称的能力。
- `aliyun-ai-gateway.md:1243` 的「**核心范围文档查无**」= 同样为假，且**与同文件 `:176`/`:289` 自相矛盾**（`:176` 正向引用了同一页的同一句话）。🔴 **P0**。
- `-mcp-agent` 三处的「**21 页**零命中」范围限定诚实，**不算缺陷**，但「不得对客承诺」这个结论超出了 21 页能支撑的范围 → 🟠 P1（建议改为「本分片 21 页查无配置/版本细节；能力宣称见主页 §1.3，支持程度 `[文档未说明]`」）。
- ✅ **准确口径已存在于 `aliyun-ai-gateway.md:289`**：能力被官方提及，但「是否完整实现规范、支持哪些 A2A 版本、如何配置」查无。三处否定断言应统一收敛到这一条。

> 附注（工艺面，非缺陷）：`tests/ai-gateway-negclaim-gate-2026-09-21.md` 的第 29/38/104 行**已经把 `what-is-an-ai-gateway` 登记为这三条否定声明的反证来源**，说明门禁抓到了，但**修正没有回落到知识页**。与主题 3 / 主题 9b 是同一失效模式：**修正只落在被发现的那一处，页眉、避坑章、空白清单、指针卡未回扫**。

### C-2 🟡 P2 · `aliyun-products.md` 指针卡与主页的装配统计数字不同步（9404 vs 9417）

| 文件:行 | 原文摘录 |
|---|---|
| `aliyun-products.md:1843` | 「合计 **9404** 行 / **408** 张表」 |
| `aliyun-ai-gateway.md:1368` | 「装配为 **7 个知识文件 / 9417 行 / 408 张表**」 |
| RULINGS R3 | 「合计 **9404** 行 / **408** 张表」（逐文件 1368/955/1347/1237/1409/1539/1549） |

实测 `wc -l knowledge/aliyun-ai-gateway*.md` = **9417**（1370/963/1347/1238/1409/1541/1549）→ 主页 `:1368` 的 9417 是**当前真值**，`aliyun-products.md:1843` 与 RULINGS R3 的 9404 是 **R1 七条修复前**的旧值。
🟡 P2（纯观感，不影响对客答复；且行数类检查可能已被 `scripts/lint-aigw-pages.py` 覆盖，此处只报「指针卡与主页数字不一致」这一点）。

### C-3 🟠 P1 · `aliyun-agentcore.md` 的 57 条 `apig:` Action vs 新页的 179/178 与 140 —— **不是同一对象，但没有任何一处把三者并排说清**

**三个数字分别是**（均已实测核对）：

| 数字 | 对象 | 出处 | 是否含 `apig:` 前缀 |
|---|---|---|---|
| **57** | `AliyunServiceRoleForAgentCore`（**AgentCore 的 SLR**）策略里 `apig` 前缀的 Action 数 | `aliyun-agentcore.md:1317`「\| `apig`（云原生 API 网关 / AI 网关） \| **57** \| `*` \|」；`:1328`「合计 **158** 条（含 2 条重复…去重后 **156** 条）」；`:1345`「apig 57 / ecs 36 / airegistry 17 / oss 16 / …」 | 是（57 条） |
| **140** | AI 网关自己的 **RAM 授权信息页**（`api-apig-2024-03-27-ram-ai-gateway`）里 `apig:` Action 全集 | `-ops:992`/`:1136`「合计 **140 个 Action，无重名**」；`:1153`「全部资源 **66** \| 47.1%」 | 是（全部 140 条） |
| **179 / 178** | AI 网关自己的**三个 SLR**（`AliyunServiceRoleForNativeApiGw` / `…InvokeFC` / `…InvokeKMS`）策略里的 Action 数 | 主页 `:1203`；`-auth:1100` | **否，0 条**（实测 `grep -c "apig:" raw/…/service-association-role-provided-only-when-involved-otherwise-no-need.md` → **0**；前缀为 slb/nlb/ecs/arms/vpc/cs/fc/mse/edas/kms） |

**判定：三者确实在讲三个不同对象，两两之间无数字矛盾**（57 应 ⊂ 140；179/178 与 140 无交集）。但：

1. 🟠 **P1 · 没有任何一处写出「AI 网关自身的 SLR 里 `apig:` 前缀 = 0 条」这个关键区分点。** 主页 §14.8 把「SLR 三个角色的 `Resource` 全为 `"*"`」与「140 个 Action 中 66 个…」并列在同一句（`:1201`，详见 A8-1），紧接着 `:1203` 才给 179/178；而 `:1350`（§15.10）又给出 AgentCore 的 57 条 `apig:`。读者在**同一屏内**遇到 66/140、179/178、57 三个 Action 计数，**没有一句消歧**。
   → 客户问「AI 网关的服务关联角色有多大权限」时，SA 可能答成「140 个 Action，66 个不能资源级授权」（那是 AI 网关**自身**的 RAM Action 表，不是 SLR），或答成「57 条」（那是 **AgentCore** 的 SLR）。
2. 🟠 **P1 · `aliyun-agentcore.md:1317` 把 `apig` 前缀注解为「云原生 API 网关 / AI 网关」**，而 RULINGS R1 与主页 §15.2 明确二者是**平级子产品**（各自独立 llms.txt）。`-ops:1529` 记 AI 网关的 RamCode 也是 `apig` → 前缀共用属实，但 agentcore 侧的注解容易让读者以为「57 条 = AI 网关的全部 RAM Action」。**建议在 `:1317` 补一句「`apig` 是 API 网关产品族共用 RamCode；AI 网关自身的 RAM Action 全集为 140 条（见 `aliyun-ai-gateway-ops.md` §13.4），57 条只是 AgentCore SLR 实际申请到的子集」**。
3. ✅ **做对的地方**：主页 `:1350` 与 `aliyun-products.md:1842` 都正确地把 57 条归属到「AgentCore 的服务关联角色」，并据此推出「AgentCore 的 MCP Server 由 API 网关承载 → 客户用 AgentCore 会同时产生 AI 网关账单」，两侧「依赖产品独立计费」话术一致。这条跨页交叉引用是**加分项**，不是缺陷。
4. 🔴 **连带发现（已计入 A11 P0）**：主页 `:1350` 引用的 `apig:CreateMcpServer`/`DeployMcpServer` 与同文件 `:1244`「OpenAPI 无 MCP 专用 Action」直接对撞；`-ops:999` 与 raw 证明 `:1244` 为错。

### C-4 ✅ `service-availability.md` 与新页**无矛盾**（该页 0 处提及网关），但有一个 🟡 P2 归类空白

```bash
grep -c "网关" knowledge/service-availability.md    # → 0
```

- `service-availability.md` 的**四层交付模型**（① SLA 承诺条款 / ② 产品状态看板 / ③ 客户专属服务报告 / ④ 客户自有资源实测可用率）是**产品无关的渠道模型**，不对任何产品做可用率归类；全文**没有**出现「网关」二字 → **与 AI 网关新页不存在任何数字或结论冲突**。
- 🟡 **P2（归类空白，非矛盾）**：该页 `:21` 已经建立了一个「个别产品有 SLA 特例」的登记位——「🔴 个别产品无可用率百分比承诺（如智能计算灵骏 SLA 只有报修退订机制，见 aliyun-lingjun-bms.md §14.6），对客引用前必须打开该产品 SLA 原文确认」。AI 网关恰好是**同一类特例**且更隐蔽（有百分比承诺，但存在 **[99.90%, 99.95%) 无赔偿区**、赔偿仅限代金券、11 条除外、申请窗口仅 2 个月且逾期失权、**申请渠道 `[文档未说明]`（空白 G20）**）。建议在 `:21` 后补一行指向 `aliyun-ai-gateway-billing.md` §3.9。**不改也不构成冲突**，故列 P2。

### C-5 ✅ `aliyun-products.md` 指针卡 + 决策树的其余数字与结论**逐项核对一致**

指针卡 `1833-1844` 与决策树 `1861-1870` 中所有可与 7 个新文件比对的数字/结论，除 C-1（A2A）、C-2（行数）、A3-1（Credits「全库查无」）、A12（CDT）四项外**全部一致**：

| 指针卡/决策树表述 | 新文件对应处 | 判定 |
|---|---|---|
| `:1836` 四形态起步价与配额（MCP Server 20 / 路由 200 / 域名 20 / 插件 5、K8s 服务来源 = N/A） | 主页 `:1194-1195`（§14.7）、`:1268-1271`（§15.3）、`-billing:215-218` | 一致 |
| `:1836` CU 系数 Model API 10 / MCP 5 / Agent API 2、不足 10 万按 10 万计、内地兜底 ≈0.50 元/小时 `[推断]` | 主页 `:1175-1176`、`-billing:365`/`:380` | 一致 |
| `:1836` `aigw.large.x4` 192,000 QPS / 256 万连接 | 主页 `:1311`（§15.6 表末行） | 一致 |
| `:1837` ① 私网 0.049 > 公网 0.037 | `-billing:128-129`/`:135`、主页 `:1174` | 一致 |
| `:1837` ② SLA 无赔偿区 [99.90%, 99.95%)、赔偿仅限代金券 | 主页 `:1185-1189`、`-billing:823-829`/`:836` | 一致 |
| `:1837` ③ 自建认证：鉴权API+原始Path、需前缀匹配、404 不在宽松模式（连接失败与 5xx）范围、解法 forward_auth | 主页 `:1123-1141`、`-auth:300-308` | 一致（但见 A5-2/A5-3：`-auth` 侧缺 forward_auth） |
| `:1837` ④ Fallback 默认在被限流时也触发 | 主页 `:1166-1168`（§14.4）、`-traffic:1304` | 一致 |
| `:1838` 三本账 + 六类连带（CDT/SLS/云监控/KMS/AI安全护栏 `lvwang_guardrail_public_cn`） | 主页 `:1204`/`:1278-1281`、`-billing:495-502`、`-auth:1209` | 一致（CDT 一项见 A12） |
| `:1839` 9 类资源配额在错误码页全是 `%s` 占位 | 主页 `:1242`、`-ops:11` | 一致 |
| `:1839` QPS 口径官方无定义 | 主页 `:1313` | 一致 |
| `:1840` SLR `Resource` 全为 `"*"`、66/140（47.1%）、四类对象无 ARN、多租户只能分账号或分实例、提额＝弃 SLA | 主页 `:1196`/`:1201`、`-ops:1165`/`:1247`、`-auth:1066` | 一致（并列易误读见 A8-1） |
| `:1841` slug 交叉错位（`ai-cue-template`→ai-prompt-decorator / `ai-cue-decorator`→ai-prompt-template）、`ai_log.safechack_status` 错字照抄、MCP 仅 API Key | 主页 `:1222` 区（§14.10）、`:1209`（§14.9）、`:1325`；`-plugins:11`；`-auth:11` | 一致 |
| `:1843` raw 186 快照 | 主页 `:1362`、RULINGS R6 | 一致（实测 `ls raw/…/*.md \| wc -l` = 187 = 186 快照 + README.md） |
| `:1865-1869` 决策树四分支（标准版 PoC / 企业版生产 / 专享核心系统 / ext-auth forward_auth / Higress 99.99% 不得用于赔偿主张） | 主页 `:1268-1271`、`:1328`、`:1353`（裁决 C1） | 一致 |

---

## E 节 · SA 可用性（明天要给客户讲「AI 网关选型 + 报价」）

### E1 · 只带主页 §15 速查卡，能否答出四问？

| 问题 | §15 能否独立答出 | 依据 / 缺什么 |
|---|---|---|
| **四形态怎么选** | ⚠️ **基本能，缺 3 条选型级硬门槛** | §15.3 表有「适用」列 + 标准版三条 🔴 限制（配额极小 / 不能接 K8s / 不支持自定义插件），§15.6 有 10 档容量。**缺**：① **WAF 在 Serverless 上不可用**（只在 §1.3 `:174` 一句带过 + §2.11.8，§15.3 选型表未列 → 安全合规客户选企业版会踩空）；② **Agent 管理仅支持新版 Serverless 标准版/企业版，旧版与实例型网关不支持**（`-mcp-agent:54`，§15 全篇 0 命中 → 客户选专享实例做核心系统时，Agent 管理能力直接没有）；③ **提额＝弃 SLA**（只在 §14.7 `:1196`，§15.5 SLA 卡未提 → 「配额不够就申请白名单」是最常见的方案动作，而它同时废掉 SLA） |
| **多少钱** | ⚠️ **能起价，但公网流量出账方答错** | §15.3 起步价 + §15.4 三本账 + §15.6 十档单价 + §15.9 十项必核清单，结构完整、限定词到位（参考单价 / `[推断]` / 禁止外推）。🔴 **但 §15.4 `:1284`「公网流量走 CDT 统一出账」与 §15.10 `:1354`「CDT：公网流量统一由 CDT 计费出账」对 Serverless 新版是错的**（见 A12，P0）。另 §15.4 未提 **AI Credits「开通后不支持退订和关闭」的单向门**（见 E2-①） |
| **SLA 多少** | ✅ **能，且是全套里质量最高的一节** | §15.5 给了协议承诺（普通 ≥99.99% / serverless ≥99.90%）、三档赔偿 15%/30%/100%、仅限代金券、可用性计算公式、申请时限（次月第 5 工作日后 + 2 个月内）、无赔偿区（裁决 C2）、11 条除外、生效日 2025-09-10。**唯一缺**：赔偿**申请渠道 `[文档未说明]`（空白 G20，`-billing:880`）**——客户问「那我去哪申请」时 §15 答不出 |
| **有什么坑** | ⚠️ **§15 自身没有「坑」清单，坑分散在 §14** | §15 各节内嵌 🔴 行（`:1273` 报价铁律、`:1296` 无赔偿区、`:1313` QPS 口径无定义、`:1319` 地域与发布记录矛盾、`:1328` 自建认证、`:1331` 插件鉴权三问、`:1339` Credits 折算率）+ §15.9 必核清单，覆盖了**报价类**坑。但 §14 的 11 个避坑条目里，**§15 完全没有对应指针**的有：§14.4 Fallback 被限流也触发（`:1166`）、§14.9 官方错字须照抄（`:1209`，如 `ai_log.safechack_status`）、§14.10 slug↔插件名交叉错位（`:1222` 区，裁决 C6）、§14.11 的 35 个 Action 无流控配额条目（`:1245`）。已实测复核：`sed -n '1249,1370p' aliyun-ai-gateway.md | grep -n "safechack\|ai-cue\|ai-prompt\|错字\|429"` → **0 命中**（只有 `%s` 占位一项在 §15.9 `:1342` 有对应，不算缺）。**建议 §15 末尾加一张 ≤10 行的「§14 避坑索引表」**，否则 SA 只带 §15 出门会漏掉 C6/C7 这类「必须实测再承诺」的红线 |

### E2 · 对客高危信息只藏在子页深处、速查卡没有（5 例）

| # | 高危信息 | 藏在哪（文件:行） | §15 是否有 | 为什么高危 |
|---|---|---|---|---|
| ① | **AI Credits「开通后不支持退订和关闭」**——单向门，只能靠「不用」避费 | `aliyun-ai-gateway-billing.md:428` | ❌ 0 命中（`grep -n "不支持退订" aliyun-ai-gateway.md` → 无） | 客户采购/合规流程常硬性要求「可退订」；且 `-billing:660` 另记「refund 页只覆盖包年包月与按量计费，**完全没提 AI Credits**」→ 一旦开通，退款路径也是空白。§15.4 三本账把它列为「独立商品，须先建实例再单独开通」，**读起来像可选项，没说是不可逆的** |
| ② | **Agent 管理仅支持新版 Serverless 标准版/企业版**，「旧版 Serverless 网关和实例型网关暂不支持」 | `aliyun-ai-gateway-mcp-agent.md:54` | ❌ 0 命中 | 这是**选型级**约束：§15.3 把「核心系统」导向专享实例，而专享实例**用不了 Agent 管理**。客户按 §15.3 选完型再发现能力缺失，属方案返工 |
| ③ | **`frontend-gray` 优先级存在 1000 / 450 两个官方数字（裁决 C7 未裁）**，「1000 则在 http-real-ip(980) 之前，450 则在其之后，**直接影响前端灰度能否拿到真实客户端 IP**」 | `aliyun-ai-gateway-plugins.md:1085`；页眉 `:11`「（裁决 C7，未裁）→ **必须先实测再对客承诺**」 | ❌ 0 命中（`grep -n "前端灰度\|frontend-gray" aliyun-ai-gateway.md` → 无） | RULINGS C7 自己写明「这是必须先实测再对客承诺的项」。前端灰度 + 真实客户端 IP 是高频组合（IP 灰度/IP 黑白名单都依赖它），SA 不知道有这条未裁矛盾就会直接承诺行为 |
| ④ | **MSE Nacos 版本要求「企业版 3.0」vs「铂金版 3.0」（裁决 C11 未裁）**，对客须按更高要求（铂金版）预检 | `aliyun-ai-gateway-mcp-agent.md:269`、`:35`、`:53` | ❌ 0 命中（`grep -n "铂金版" aliyun-ai-gateway.md` → 无） | Nacos 同步是 MCP 四类接入形态之一，版本档位直接决定客户要不要**升级 MSE 实例（产生费用）**。按企业版预检可能到现场才发现要铂金版 |
| ⑤ | **SLA 赔偿申请渠道 `[文档未说明]`（空白 G20）** + 「逾期不受理」是硬性失权 | `aliyun-ai-gateway-billing.md:880`、`:879`、`:885`（`[推断]` 2026-08 未达标须在 2026-10-31 前提出） | ⚠️ §15.5 `:1295` 只有时限，**无渠道、无「逾期即失权」的措辞** | §15.5 是 SLA 唯一速查位。客户在故障后第 61 天来问赔偿时，SA 需要当场说出「已过时限、不被受理」；而「去哪申请」官方查无 → 必须走工单/TAM，这句话 §15 没给 |

> 另有 2 条边缘候选（未计入上表，供主控取舍）：MCP 测试域名「每天整个域名限额 **1000 次**」（`-mcp-agent:45`，§15 无）；Fallback「后端为 **FC 函数**时当前版本 fallback 策略**失效**」+「仅支持 HTTP 服务之间」（`-mcp-agent:49-50`，§15 无，而 §14.4 只讲了 Fallback 被限流触发的那一面）。

### E3 · 速查卡写了、但子页找不到依据的「孤儿结论」（3 例）

| # | 孤儿结论（文件:行） | 子页/raw 实况 | 严重度 |
|---|---|---|---|
| ① | `aliyun-ai-gateway.md:1244`（§14.11 高频踩坑速记）「**OpenAPI 无 MCP 专用 Action**：管理 MCP 的**唯一写操作**是 `UpdatePluginAttachment` + `ImportHttpApi`」 | **被子页与 raw 双重否证**：`-ops:999` 列出 MCP管理 **8 个** Action（`CreateMcpServer`/`UpdateMcpServer`/`GetMcpServer`/`ListMcpServers`/`DeleteMcpServer`/`DeployMcpServer`/`UnDeployMcpServer`/`SyncMCPServers`）；`-ops:1172` 把「MCP（整套）8」计入 66 个「全部资源」清单；raw 三个元页（overview / ram / quota）均命中 `CreateMcpServer`。且**同文件 `:1350`** 自己引用了 `apig:CreateMcpServer`/`DeployMcpServer` | 🔴 **P0**（详见 A11） |
| ② | `aliyun-ai-gateway.md:1354`（§15.10）「**CDT**：公网流量**统一由 CDT 计费出账**」；`:1284`（§15.4）「公网流量走 **CDT** 统一出账」 | **被子页限定否证**：`-billing:394`「旧版走 CDT 出账，**新版公网出入网流量走网关侧账单 0.8 元/GB**」；`-billing:269-270` 新版出网/入网均「**网关侧** \| 0.8 元/GB」；`-billing:495-496` 连带表只把**专享实例**与 **Serverless（旧）**归给 CDT；RULINGS **C3** 要求「以商业化后账单实际出账方为准，报价前必须走购买页/工单确认」 | 🔴 **P0**（详见 A12） |
| ③ | `aliyun-ai-gateway.md:1243`（§14.11）「A2A 协议转换…**核心范围文档查无**，不得对客承诺」 | **被同文件与 raw 否证**：同文件 `:176` 正向引用「提供 **REST 到 A2A 协议的转换能力**」`[官方｜what-is-an-ai-gateway]`、`:289` 记「只提『REST 到 A2A 协议的转换能力』」；raw `what-is-an-ai-gateway.md:125` 逐字「提供 REST 到 A2A 协议的转换能力，实现存量 HTTP 应用向 A2A 协议的自动化升级」。子页 `-mcp-agent:732` 的范围只到「本章 **21 页**」，支撑不了「核心范围文档查无」 | 🔴 **P0**（详见 C-1） |

> 说明：三例都在主页的 §14.11 / §15.10 / §15.4，即**主页的「速记 + 速查 + 交叉引用」三个高可见位置**，而不是子页。这与本次装配工艺（7 个 worker 各自产出、装配器不改正文）的失效方向一致：**主页的 §14/§15 是主控在装配后另写的合并层，它压缩子页结论时丢掉了子页的范围限定词**（「本章 21 页」「旧版/新版分别」「本页涉及的 6 个 Action」），把**范围限定的真话**压成了**全局断言的假话**。A3-1（Credits「全库查无」残留在页眉与指针卡）与 A9-1（429 修正未回扫页眉/避坑章/空白清单）是同一根因的另两个方向。

---

## 结论

**这批页面能不能直接拿去对客答疑？**

**不能直接拿去，但差距很小、且全部可定位。** 事实层与标注纪律的质量高于预期：主控指定的 10 个接缝主题里 **6 个完全一致**（SLA 与赔偿档位、四形态起步价、数据处理量公私网单价、插件优先级、SLR Action 计数、Serverless 公测时间线——**专查的第三/第四处旧口径残留 = 0**），`-billing` §3.9 与 `-plugins` §9.2 两个高风险章节的内部自洽度尤其好。缺陷**不在事实层，而在「压缩层」**：主页 §14/§15 与 `aliyun-products.md` 指针卡在压缩子页结论时**丢掉了范围限定词**，把子页的范围限定真话升级成了全局断言假话；以及**修正只落在被发现的那一处**（R1 的 D3 修正改了正文，没回扫页眉、避坑章、空白清单、指针卡）。

**必须先修的 P0（5 条，全部给了双方原文与修法）**：

| # | P0 | 位置 | 一句话 |
|---|---|---|---|
| 1 | **A11 / E3-①** | `aliyun-ai-gateway.md:1244` + `aliyun-ai-gateway-mcp-agent.md:1086-1087` | 「OpenAPI 无 MCP 专用 Action」为假——`-ops:999` 列出 8 个、raw 三个元页命中 `CreateMcpServer`；会让 SA 给客户设计错误的自动化方案，且与同文件 `:1350` 自相矛盾 |
| 2 | **A12 / E3-②** | `aliyun-ai-gateway.md:1354`、`:1284`、`:1281`；`aliyun-products.md:1842`、`:1838` | 「公网流量统一走 CDT」对 **Serverless 新版为假**（新版走网关侧 0.8 元/GB，出网+入网），而 §15.3 恰好把新版企业版推荐给生产 → 直接漏报一项账单 |
| 3 | **C-1 / E3-③** | `aliyun-products.md:1841`；`aliyun-ai-gateway.md:1243` | 「A2A 协议转换 189 页零命中 / 核心范围文档查无」可复算为假（raw `what-is-an-ai-gateway.md:125` 明文宣称该能力），且与同文件 `:176`/`:289` 对撞；准确口径已在 `:289`，收敛过去即可 |
| 4 | **A6-1** | `aliyun-ai-gateway.md:167`（§1.3 能力总表） | 「Model API / **MCP Server** / Agent API 均可按需开启 API-KEY、**JWT**、HMAC」写成无条件确定事实，与裁决 C9 及同文件 `:1325`、`-auth:11`/`:112`、`-mcp-agent:42`、`aliyun-products.md:1841` 五处「MCP 仅支持 API Key、不得承诺 JWT」直接对撞 |
| 5 | **A9-1** | `aliyun-ai-gateway-traffic.md:11`（页眉）、`:1317`（空白 #1）；`aliyun-ai-gateway.md:1237`（§14.11） | 限流超限返回码：`-traffic:989` 已按 R1/D3 修正为「一般返回 **429**」（`custom-response-plugin:54` 有官方原文），但**三个更高可见度位置仍是「文档未说明、不可类推、先答空白」** → 同一问题两个相反对客口径 |

**紧随其后的 P1（5 条，建议同批修）**：A3-1（Credits「全库查无」旧口径残留于 `-billing:11`、`aliyun-products.md:1839`、`:1870`）｜A5-2（`-auth` §6.6 只有客户已拒绝的方案，缺 forward_auth）｜A5-3（forward_auth 在 AI 网关官方 186 快照 0 命中，未标 `[文档未说明]`）｜A6-2（`-auth:152` 仍写「不裁决」，未同步 C9）｜C-3（57 / 140 / 179 三个 Action 计数无一处消歧，且未写明「AI 网关自身 SLR 内 `apig:` = 0 条」）。
**另请主控复核（不由我裁决）**：A6-3 —— RULINGS **C9 的依据是 R4-3（专页优先）**，但存在一条**优先级更高的带日期发布记录**（主页 `:1022`，2026-01「MCP Server 支持 JWT 认证」）支持相反结论，且 C9 的矛盾双方未纳入该发布记录；两者互不引用，SA 无从判断该说哪句。

**一句总评**：接缝缺陷确实存在且集中在「主页压缩层 + 页眉/清单未回扫」这一个可复用的失效模式上，5 条 P0 全是局部改写、不动任何已裁决口径即可修完；修完后这批页面对客可用性很高——尤其 `-billing` §3.9（SLA）与 `-plugins` §9.2（优先级）两章可以直接当交付材料用。
