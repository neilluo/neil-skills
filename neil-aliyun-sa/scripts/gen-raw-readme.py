#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 raw/aliyun-docs/ai-gateway/README.md（raw 层索引）。
全部数据来自 fetch manifest + SHA256SUMS，不手写清单（避免漏项与错字）。
"""
from pathlib import Path
from collections import defaultdict

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent
RAW = KB / "raw/aliyun-docs/ai-gateway"
MAN = KB / "tests/ai-gateway-fetch-manifest-2026-09-21.tsv"
OUT = RAW / "README.md"

rows = []
for ln in MAN.read_text(encoding="utf-8").splitlines()[1:]:
    f = ln.split("\t")
    rows.append(dict(slug=f[0], url=f[1], section=f[2], title=f[3], http=f[4],
                     nbytes=f[6], verdict=f[7], mstatus=f[8], sha=f[9], path=f[10],
                     reason=f[12] if len(f) > 12 else ""))

by_sec = defaultdict(list)
for r in rows:
    by_sec[r["section"]].append(r)

landed = [r for r in rows if r["path"]]
toc = [r for r in rows if r["verdict"] == "TOC"]
nomd = [r for r in rows if r["verdict"].startswith("FAIL")]
stub = [r for r in rows if r["verdict"] == "OK-STUB"]
legacy = [r for r in rows if r["mstatus"] == "legacy"]

L = []
L.append("# raw/aliyun-docs/ai-gateway — 阿里云 API 网关 · AI 网关 官方文档快照")
L.append("")
L.append("**归档日期**：2026-09-21  ")
L.append("**来源**：`https://help.aliyun.com/zh/api-gateway/ai-gateway/`（官方按产品 llms.txt 收录 **438** 链接 "
         "→ 本次范围 core **189** 页；另 **250** 页逐 Action OpenAPI 参考登记 `[deferred]` 未抓）  ")
L.append(f"**本目录**：**{len(list(RAW.glob('*.md')))}** 个 `.md` 快照（= manifest 内落盘 {len(landed)} 页 "
         f"+ 主控补抓的 SLA 协议全文外部源 1 页）+ `SHA256SUMS.txt` + 本 README  ")
L.append("**索引**：官方 `https://help.aliyun.com/zh/llms.txt` → `zh/api-gateway/llms.txt`（产品族归属证据）"
         "→ `zh/api-gateway/ai-gateway/llms.txt`（438 链接）+ 一轮快照内链 BFS 增量发现")
L.append("")
L.append("---")
L.append("")
L.append("## 一、抓取通道与🔴五种失效模式")
L.append("")
L.append("help.aliyun.com 任意文档 URL 追加 `.md` 后缀即返回纯 Markdown 正文"
         "（`Content-Type: text/markdown;charset=UTF-8`），**纯 curl 可取，不需要浏览器渲染**。")
L.append("")
L.append("抓取器：`scripts/fetch-aliyun-docs.py`（确定性脚本，非 subagent 抓取 → 产物可复算、无二手结论污染）。"
         "每页 verdict 记录在 `tests/ai-gateway-fetch-manifest-2026-09-21.tsv`。")
L.append("")
L.append("| # | 失效模式 | 表现 | 判据 | 本次命中 |")
L.append("|---|---|---|---|---|")
L.append("| 1 | **软 200** | 不存在的 slug 返回 HTTP 200 + 约 **24893B** SPA HTML 外壳 | body 前 60 字节以 `<!doctype`/`<html` 开头 | 0（负控实验用伪造 slug 证实检测器会 FAIL） |")
L.append("| 2 | **CT 不符** | 非 markdown Content-Type | CT 不含 `markdown` | 0 |")
L.append("| 3 | **空 body** | 0 字节 | `len(body)==0` | 0 |")
L.append("| 4 | 🔴 **Document Not Found 桩**（本次新发现） | CT=markdown、HTTP **200 或 404**（同一 slug 两次抓取状态码不同）、body 恒为 **86B** 固定文案 | 正则匹配 `# Document Not Found` + `does not have Markdown content available` | **%d**（不落盘，见下方清单） |" % len(nomd))
L.append("| 5 | 🔴 **服务端静默截断**（本次新发现） | HTTP 200、CT=markdown、**Content-Length 与 body 自洽**、**两次抓取 SHA256 一致** → 截断在服务端 | 末行是悬挂结构标记（孤立 `*`）/ HTML 标签开闭不平衡 | **1**（`agent-api-observable`，978B，断在孤立 `*` 上）。扫描器 `scripts/scan-truncated-snapshots.py` |")
L.append("")
L.append("**TOC 容器判据**（沿 2026-09-20 AgentCore RULINGS C1，本次再次验证）：")
L.append("判据 = 「正文仅由标题 + 链接列表构成、无散文」，**不是字节阈值**。"
         f"本次判出 **{len(toc)}** 个 TOC 容器页，**落盘但不作事实来源**，只承载目录结构与 slug↔docId 对照证据。"
         "实测 `product-overview` 765B 判 TOC、`support` 113B 判 TOC，而 86B 的 Document Not Found 桩**有散文**故不是 TOC "
         "—— 三者字节数相近而性质完全不同，字节阈值必然误判。")
L.append("")
L.append("## 二、frontmatter 与 SHA256 校验方法")
L.append("")
L.append("每个快照前 10 行为 7 字段 frontmatter（`source_url` / `fetch_date` / `product` / `slug` / "
         "`body_sha256` / `body_bytes` / `migration_status`），正文自第 11 行起**逐字保留**"
         "（含官方错字、HTML `<table>` 残留、`HELPCODEESCAPE-*` 代码块语言标记残留，一律不修）。")
L.append("")
L.append("```bash")
L.append("# SHA256 只对「原始正文」计算，不含 frontmatter，故直接 -c 会全部 FAILED（设计使然，非快照损坏）")
L.append("tail -n +11 <file>.md | shasum -a 256      # 正确校验方法")
L.append("```")
L.append("")
L.append("`.md` 通道**不含页面 H1 标题**，各页官方标题取自 llms.txt 的链接文字（见下方目录树映射）。")
L.append("")
L.append("## 三、目录树映射（栏目 → slug → 官方标题 → verdict）")
L.append("")
L.append("图例：✅ = 有正文（可作事实来源）｜ 📁 = TOC 容器（不作事实来源）｜ 🔗 = 入口桩指向外部协议原文")
L.append("")
order = ["产品概述", "快速入门", "操作指南", "实践教程", "安全合规", "服务支持", "开发参考"]
for sec in order:
    rs = by_sec.get(sec, [])
    if not rs:
        continue
    n_ok = sum(1 for r in rs if r["verdict"].startswith("OK"))
    n_toc = sum(1 for r in rs if r["verdict"] == "TOC")
    n_fail = sum(1 for r in rs if r["verdict"].startswith("FAIL"))
    L.append(f"### {sec}（{len(rs)} 页 = ✅{n_ok} + 📁{n_toc}" + (f" + 无正文{n_fail}" if n_fail else "") + "）")
    L.append("")
    L.append("| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |")
    L.append("|---|---|---|---|---|---|")
    for r in sorted(rs, key=lambda x: x["slug"]):
        icon = {"OK": "✅", "OK-STUB": "🔗", "TOC": "📁"}.get(r["verdict"], "❌未落盘")
        L.append("| `%s` | %s | %s %s | %s | %s | `%s` |" % (
            r["slug"], r["title"], icon, r["verdict"], r["nbytes"], r["mstatus"] or "—",
            r["sha"][:12]))
    L.append("")

L.append("### 外部源补抓（非 help.aliyun.com `.md` 通道）")
L.append("")
L.append("| 文件 | 来源 | 说明 |")
L.append("|---|---|---|")
L.append("| `sla-agreement-fulltext-terms-alicdn.md` | `https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250905155227889/20250905155227889.html` | "
         "**AI 网关服务等级协议全文**。help 侧 `support/service-level-agreement` 只有 %s 字节入口桩（verdict `OK-STUB`），"
         "可用率承诺与赔偿档位全在外部协议原文页。提取方式 = curl HTML → 正则剥标签 → unescape → 压缩空行，"
         "🔴 **有损**（表格被展平为逐行文本，赔偿档位的行列对应关系由蒸馏员 W2 用四步法复核后重排，方法见 "
         "`knowledge/aliyun-ai-gateway-billing.md` §3.9.4）。原始 HTML SHA256 记录在该文件 frontmatter 后的说明段。"
         "🔴 该文件**不在** `SHA256SUMS.txt` 内（其校验值见自身 frontmatter 的 `body_sha256`），"
         "与 2026-09-20 AgentCore 侧 SLA 全文补抓的处理方式一致 |"
         % next((r["nbytes"] for r in rows if r["slug"] == "service-level-agreement"), "?"))
L.append("")
L.append("## 四、🔴 未落盘的无正文节点（%d 个，verdict `FAIL-NOMD`）" % len(nomd))
L.append("")
L.append("这些节点存在于 llms.txt / 导航树，但 `.md` 通道返回 86 字节固定桩「# Document Not Found / "
         "The requested document does not have Markdown content available.」→ 无 Markdown 正文，"
         "**不落盘、不作事实来源**。它们的子页均已通过 llms.txt 收录并抓取，**无覆盖损失**。")
L.append("")
for r in sorted(nomd, key=lambda x: x["slug"]):
    L.append("- `%s` — %s（HTTP %s）" % (r["slug"], r["title"], r["http"]))
L.append("")
L.append("## 五、🔴 重复别名与部分重复（蒸馏时只写一份）")
L.append("")
L.append("| 事实 | 证据 |")
L.append("|---|---|")
L.append("| `gateway-managed-mcp-services` ≡ `mcp-gateway-management`（**完全相同的两个 slug**） | "
         "正文 SHA256 同为 `ec7aa8c726c3d0c4da7d7c0ec7c19d68f876dc7c64d793eccb588ab9d2730382`、"
         "`body_bytes` 同为 6094、`diff` 为空（主控实测）。前者 **llms.txt 未收录**，靠 `mcp-service-management-1` "
         "的内链 BFS 发现 |")
L.append("| `enable-mcp-service-log-delivery` 与 `enable-gateway-log-delivery` **部分重复** | "
         "日志字段表 SHA256 相同、`Response_Flag` 章节相同，但两页正文整体不同 → **不是重复页**，"
         "蒸馏时合并日志字段表并双标 slug（蒸馏员 W7 实测） |")
L.append("")
L.append("## 六、migration_status 判定")
L.append("")
L.append("本次 **legacy %d 页 / current %d 页**。legacy 判据 = 官方标题含「旧版/（旧）/已下线/停止服务」"
         "或 slug 含 `-old-`/`-legacy`/`serverless-old`（`scripts/fetch-aliyun-docs.py` 的 "
         "`migration_status()` 机械判定，非语义猜测）：" % (len(legacy), len([r for r in rows if r["mstatus"] == "current"])))
L.append("")
for r in legacy:
    L.append("- `%s` — %s" % (r["slug"], r["title"]))
L.append("")
L.append("⚠️ **另一类时效性内容未被 migration_status 捕获**：Serverless **新版公测**相关页"
         "（`announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta`、"
         "`overview-of-billing-during-the-serverless-public-preview-of-the`）标为 `current`，"
         "但公测已于 **2026-08-31 结束、2026-09-01 起商业化计费**"
         "（`ai-gateway-commercialization-announcement`）→ 引用这两页的免费/计费口径时**必须带时间边界**，"
         "不要写成现在时。蒸馏契约 §8 已就此下过指令。")
L.append("")
L.append("## 七、🔴 本目录不构成「全站」的边界声明")
L.append("")
L.append("1. **250 页逐 Action / 逐数据结构 OpenAPI 参考页未抓**（`api-apig-2024-03-27-*`），登记 `[deferred]`；"
         "仅破例纳入 8 个元页（概览/接入点/RAM/流控配额/错误码/变更集/两级容器）。")
L.append("2. **同族的云原生API网关、原API网关两个子产品未抓**（各有独立 llms.txt）。")
L.append("3. llms.txt 是**快照会滞后**：本次已实证 2 处收录缺口"
         "（`gateway-managed-mcp-services` 未收录；`api-apig-2024-03-27-createsecret` docId 3045062 未收录）。")
L.append("4. 若某页同时满足「近日新增 + 未进 llms.txt + 无任何快照内链 + 非顶级栏目」，"
         "本次方法（llms.txt + 内链 BFS + docId 实时 301 解析）**检测不到**，需 JS 拉实时目录树 API 才能穷尽。")
L.append("")
L.append("→ 准确表述：**「截至 2026-09-21 的官方 llms.txt 收录范围 + 一轮内链 BFS，189 页全覆盖」**，"
         "**不得宣称「全站蒸馏」**。")
L.append("")
L.append("## 八、配套工艺制品")
L.append("")
L.append("| 制品 | 路径 |")
L.append("|---|---|")
L.append("| llms.txt 快照（本产品 438 链接 + 父级归属证据） | `tests/ai-gateway-llms-2026-09-21.txt`、`tests/api-gateway-parent-llms-2026-09-21.txt` |")
L.append("| 文档树与分片清单（含范围裁决与分类判据） | `tests/ai-gateway-doctree-shards-2026-09-21.md` |")
L.append("| 抓取 manifest（189 行 × 13 列） | `tests/ai-gateway-fetch-manifest-2026-09-21.tsv` |")
L.append("| 覆盖率审计报告 | `tests/ai-gateway-coverage-audit-2026-09-21.md` |")
L.append("| 蒸馏契约（7 路 worker 共读） | `tests/ai-gateway-distill-contract-2026-09-21.md` |")
L.append("| 主控裁决留痕（R1~R10 + C1~C12） | `tests/ai-gateway-rulings-2026-09-21.md` |")
L.append("| Wiki 层产物（7 文件 / 9360 行 / 407 表） | `knowledge/aliyun-ai-gateway*.md` |")
L.append("")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("README 生成：%s（%d 行）" % (OUT, len(L)))
print("落盘 %d ｜ TOC %d ｜ FAIL-NOMD %d ｜ OK-STUB %d ｜ legacy %d"
      % (len(landed), len(toc), len(nomd), len(stub), len(legacy)))
