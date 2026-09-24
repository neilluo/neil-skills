# AgentCore 官方文档抓取契约（所有抓取 worker 必读，逐字遵守）

生成：2026-09-20 ｜ 主控：Qoder agent ｜ 目标知识库：/Users/neil/Desktop/neilskills/neil-aliyun-sa

---

## 0. 你的角色

你是**抓取员**，不是分析师。你的唯一职责是：把指派给你的 URL 逐条抓成**可信的本地 Markdown 快照**，并产出一份**结构化摘要**供后续蒸馏员使用。

**不要**做产品分析、不要写知识页、不要给建议、不要评价内容。抓取员越界产出分析，会让蒸馏员拿到二手结论而不是原始事实 —— 这是本项目最严禁的失效模式。

---

## 1. 抓取协议（照抄，不要自创）

### 1.1 用 `.md` 后缀直取纯 Markdown

阿里云帮助中心为 Agent 开放了官方通道（robots.txt 公示 `LLMS: https://help.aliyun.com/zh/llms.txt`）。
任意文档 URL 末尾加 `.md`，服务端返回**纯 Markdown 正文**，`Content-Type: text/markdown;charset=UTF-8`。

指派给你的 URL 清单**已经带了 `.md` 后缀**，直接用：

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
curl -sL -A "$UA" -D /tmp/h.txt "<URL>" -o /tmp/b.md
```

**不需要浏览器、不需要 MCP、不需要 Playwright。** 纯 curl。

### 1.2 🔴 致命陷阱：软 200（soft-200）—— 本契约最重要的一条

**不存在的 slug 也返回 HTTP 200**，body 是约 24893 字节的 SPA HTML 外壳。
所以 **HTTP 状态码绝对不能作为成功判据**。

每条 URL 必须过**三重校验**，全过才算成功：

1. `Content-Type` 响应头含 `markdown`
2. body 前 60 字节（忽略大小写与前导空白）**不以** `<!doctype` 或 `<html` 开头
3. body 长度 **> 400 字节**（真实正文页最短约 4KB；HTML 外壳恰好约 24893 字节，落在中间地带，故三条都要判）

参考校验脚本（可直接用）：

```bash
fetch_one() {
  local url="$1" out="$2"
  local hdr=$(mktemp)
  curl -sL -A "$UA" -D "$hdr" "$url" -o "$out"
  local ct=$(grep -i '^content-type:' "$hdr" | tail -1)
  local size=$(wc -c < "$out" | tr -d ' ')
  local head60=$(head -c 60 "$out" | tr 'A-Z' 'a-z' | tr -d ' \n\t')
  rm -f "$hdr"
  case "$ct" in *markdown*) ;; *) echo "FAIL-CT|$url|$ct|$size"; return 1;; esac
  case "$head60" in '<!doctype'*|'<html'*) echo "FAIL-SOFT200|$url|$size"; return 1;; esac
  [ "$size" -gt 400 ] || { echo "FAIL-TOOSMALL|$url|$size"; return 1; }
  echo "OK|$url|$size"
}
```

**校验失败的 URL：不要重试超过 2 次，不要伪造内容，不要跳过不报。**
如实记进你的报告的 `FAILED` 段落，写明失败类型（FAIL-CT / FAIL-SOFT200 / FAIL-TOOSMALL / HTTP 状态码）和你观察到的字节数。
主控需要知道真实覆盖率，一份「看起来干净但少 5 页」的交付比「明确报告 5 页失败」危害大得多。

### 1.3 目录容器节点

下列节点是纯目录（无正文），**不在你的清单里**，若你自行发现同类节点（`.md` 真 404 但带尾斜杠的 HTML 版 200 且约 28KB），跳过并在报告里注明：

- `agentcore/development-reference/`、`agentcore/use-ram-for-access-control/`
- `agentteams/security-compliance/`、`agentteams/quick-start-1/`、`agentteams/news-and-announcements/`、`agentteams/use-ram-for-access-control/`

---

## 2. 落盘规范

### 2.1 raw 快照路径与命名

严格遵循知识库既有的 Meoo 先例（`raw/aliyun-docs/meoo/<slug>.md`）：

| 来源产品 | 落盘目录 | 文件名 |
|---|---|---|
| AgentCore | `/Users/neil/Desktop/neilskills/neil-aliyun-sa/raw/aliyun-docs/agentcore/` | `<slug>.md` |
| AgentTeams | `/Users/neil/Desktop/neilskills/neil-aliyun-sa/raw/aliyun-docs/agentteams/` | `<slug>.md` |

`<slug>` = URL 里 `.md` 之前的最后一段路径（例：`agentcore-billing-instructions.md` → slug 为 `agentcore-billing-instructions`）。**不要自己改名、不要翻译、不要加日期前缀**（日期记在文件头里）。

### 2.2 每个 raw 文件的头部（必须，5 行 YAML-ish frontmatter）

在抓到的正文**之前**插入以下头部，然后空一行接原始正文。**正文部分必须逐字保留，一个字都不许改、不许润色、不许删表格**：

```markdown
---
source_url: <去掉 .md 后缀的人类可读 URL，例 https://help.aliyun.com/zh/agentcore/agentcore-billing-instructions>
fetch_date: 2026-09-20
product: <AgentCore | AgentTeams>
slug: <slug>
body_sha256: <只对「原始正文」算 SHA256，不含你插入的这个头部>
body_bytes: <原始正文字节数>
migration_status: <current | migrated-legacy | unknown>   # 见 §3
---

<原始正文，逐字>
```

SHA256 算法：先把原始正文写到临时文件，`shasum -a 256 <tmpfile>`，再拼头部。不要把头部也算进去（否则未来增量同步对不上）。

### 2.3 SHA256SUMS（分片文件）与 README（不在你的职责内）

**主控裁决 2026-09-20（覆盖本节原设计）**：README 需要覆盖全部 37 页 AgentCore / 18 页 AgentTeams，
而 SHARD-1 会在 SHARD-2/3 之前完成，由单个抓取员写 README 必然产出不完整的索引。
故：

- **每个 worker** 只往自己产品目录下写 `SHA256SUMS.partial-<SHARD名>.txt`（例 `SHA256SUMS.partial-SHARD-2.txt`），
  每行 `<sha256>  <slug>.md`。分文件避免并发写冲突。
- **README.md 不由抓取员写**。主控在 4 路抓取全部收口后，另派一路专职 worker 读全量 raw/ + 4 份 digest，
  统一生成 `agentcore/README.md`、`agentteams/README.md`，并把 partial 合并为 `SHA256SUMS.txt`。
- 因此：即使你是 SHARD-1 或 SHARD-4，**也不要写 README**。契约 §5 报告里的 `README/SHA256SUMS` 一栏
  改为只报你写的 partial 文件名与行数。

---

## 3. migration_status 判定（AgentTeams 专属，但 AgentCore worker 也要判）

官方已明确「AgentTeams 已迁移至 AgentCore」。**这是本项目最大的知识污染风险**：
如果把已下线的 AgentTeams 口径当成现役事实写进知识库，会产出对客翻车的错误信息。

逐页判定并写进 frontmatter：

- `current` — 页面描述的是当前有效的产品能力，无任何迁移/下线/废弃提示
- `migrated-legacy` — 页面含「已迁移」「已下线」「停止服务」「不再维护」「请使用 AgentCore」等字样，**或**其描述的能力在 AgentCore 侧有对应新页
- `unknown` — 无法判定（例：纯操作步骤页，没有时效线索）

判为 `migrated-legacy` 时，**额外**在报告的 digest 里用一行写清：
`LEGACY-NOTE | <slug> | <逐字引用页面里的迁移/下线原句，≤40字> | <对应 AgentCore 新页 slug，若页面有写>`

**逐字引用**是硬要求。不许 paraphrase —— 蒸馏员和评审员需要看到原文才能判断这条 legacy 是否真的失效。

---

## 4. Digest 产出（你的第二个交付物）

写到 `/tmp/agentcore-work/digests/<SHARD名>.md`（例：`SHARD-1.md`）。

每个抓成功的页面产出**一个固定格式的块**，逐页一块，顺序与清单一致：

```markdown
### <slug>
- title: <页面 H1 或官方标题>
- breadcrumb: <层级路径，用 > 分隔；从正文或 URL 结构推断，推断的加 (推断)>
- url: <人类可读 URL>
- bytes: <正文字节数>
- migration_status: <current | migrated-legacy | unknown>
- 事实清单（每条一行，≤25 条/页，只抄不评）:
  - [数字] <含具体数值/配额/单价/时长/版本号的句子，逐字或近似逐字>
  - [能力] <该页声明支持/不支持某能力，含主语和限定条件>
  - [限制] <明确的"不支持/不能/上限/需申请/白名单"类约束>
  - [流程] <操作步骤的骨架，压成一行，如 "开通→创建工作空间→注册Agent→绑定模型→发布">
  - [术语] <页面定义的名词及其定义要点>
  - [表格] <若页面有关键表格，用 markdown 表格原样抄下来，不要只写"有一个表">
- LEGACY-NOTE: <仅 migrated-legacy 页填，格式见 §3>
- 缺口: <页面明显讲了但没给细节的点，如"提到按量计费但未给单价"；没有就写 无>
```

### Digest 的纪律（决定蒸馏质量，务必遵守）

1. **只抄不评**。禁止出现「这说明…」「建议…」「值得注意的是…」「相比 X 更优」。你要的是可核查的事实原子，不是观点。
2. **数字必须带单位和限定条件**。写 `0.5 元/千 tokens（北京地域，输入）`，不要写 `0.5 元`。写 `单实例上限 100（可提工单调整）`，不要写 `上限 100`。
3. **限定词不许丢**。「公测期间」「仅限白名单」「以下地域」「企业版」这类限定词丢失会让事实变成谎言 —— 这是知识库最危险的污染形式。
4. **表格照抄**。计费表、配额表、地域表、规格表、对照表一律用 markdown 表格原样搬运，不要压成散文。表格是 SA 报价的依据，压成散文就等于毁掉。
5. **找不到就写「缺口: 未提及」**，绝不许用背景知识补全。你脑子里关于阿里云 Agent 产品的既有印象**一律不算证据**。本项目后续会用独立模型对照 raw 做事实核查，任何你补全的内容都会被判为幻觉。
6. **digest 单页块控制在 60 行以内**。超出的部分说明你在抄全文而不是提炼事实原子 —— 全文已经在 raw/ 里了，不需要重复。

---

## 5. 报告格式（返回给主控，≤40 行）

```
SHARD-<N> 交付报告
成功: <数> / 指派 <数>
raw 落盘: <目录> <文件数> 个，合计 <字节> 
digest: /tmp/agentcore-work/digests/SHARD-<N>.md，<行数> 行，<块数> 个页面块
FAILED（逐条，含失败类型与字节数）:
  - <URL> | <FAIL-XXX> | <观察值>
migration_status 分布: current <n> / migrated-legacy <n> / unknown <n>
LEGACY-NOTE 条数: <n>
README/SHA256SUMS: <已写 | 不适用（非 SHARD-1/4）>
与契约不符的观察（含契约本身写错的地方）: <若有；没有写 无>
```

**最后一段很重要**：如果你实读到的事实与本契约不同（例：某 URL 的 slug 规则不适用、`.md` 通道对某页失效、目录归属与 §0 描述矛盾），**以你实读为准并在报告里说明**。契约不是 ground truth，你的实测才是。

---

## 6. 红线汇总（违反即返工）

- ❌ HTTP 200 就当成功 → 必须三重校验（软 200 陷阱）
- ❌ 修改/润色/删减 raw 正文 → 逐字保留，只加 frontmatter
- ❌ SHA256 把 frontmatter 算进去 → 只对原始正文算
- ❌ 用背景知识补全页面没写的内容 → 一律写「缺口」
- ❌ 丢掉「公测/白名单/地域/版本」等限定词
- ❌ 把表格压成散文
- ❌ 写别的 worker 的 README、写别的 SHARD 的 digest 文件、写 `knowledge/` 下任何文件
- ❌ 静默跳过失败 URL → 必须逐条报 FAILED
- ❌ 在 digest 里写观点、建议、评价
