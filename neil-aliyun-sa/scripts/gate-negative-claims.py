#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨页否定句门禁（negative-claim gate）。

🔴 为什么需要：2026-09-21 AI 网关蒸馏的独立评审 R1 抽样 74 条，查出 **5 处 D3「空白被填」**
（知识页断言「文档未说明／全库查无」，而 raw 或本家族另一页其实写了）。R1 的根因判断是：
**`[文档未说明]` 被 worker 当成「我这个分片没读到」用，而页首图例把它定义为「raw 查无此项」（全库口径）**。
7 路并行蒸馏时，A 分片的「查无」很可能就写在 B 分片的页里 —— 4 次中有 3 次答案已被本 KB 另一文件正确写下。
抽样只能撞见一部分，**这类缺陷必须机械全扫**。

判据：对每一条否定句，抽出其中的**关键名词**，去 `raw/` 与 `knowledge/` 全库反查；
命中即列为待裁决项（**不自动判定为错** —— 否定句可能只针对某个侧面，需人工看证据裁决）。

用法：
  python3 scripts/gate-negative-claims.py [--only-main] [--min-term-len 3]
退出码：0 = 无待裁决项；1 = 有待裁决项（供 CI/收口门禁用）
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent
KNOWLEDGE_GLOB = "knowledge/aliyun-ai-gateway*.md"
RAW_DIR = KB / "raw/aliyun-docs/ai-gateway"

# 🔴 分级：只有**全称否定**（断言「整个文档集里都没有」）才是高风险、值得机械全扫的对象。
# 普通的 `[文档未说明]` 多半只是「本页没写这个参数」，是对的，扫它会产生数百条噪声
# （首版把两者混在一起 → 655 行否定句里报出 488 处待裁决，完全不可用）。
STRONG_MARKERS = (
    "全库查无", "全站查无", "零命中", "0 命中", "全部缺失", "全缺", "无任何",
    "无法从文档", "不可从文档", "均未说明", "均未给", "全部未说明", "查无此词",
    "无迁移方案", "无单价", "未公开", "一个都没", "全部 0", "均无", "全无",
    "全页无", "全篇无", "全文无", "全文检索", "21 页", "34 页", "189 页",
)
# 🔴 已剔除的标记 `186 `：它会命中每个子页页眉的「186 个快照」，纯属自指噪声（首版误报源）。
WEAK_MARKERS = ("[文档未说明]", "查无", "未说明", "未给")


def strength(line: str):
    if any(m in line for m in STRONG_MARKERS):
        return "STRONG"
    if any(m in line for m in WEAK_MARKERS):
        return "weak"
    return None


# 高精度关键名词：反引号内标识符、「」内术语、ASCII 标识符。
# 🔴 不抽裸中文名词 —— 裸中文词在 186 个 raw 文件里几乎必然命中，判别力为零（首版噪声主因）。
BACKTICK = re.compile(r"`([^`]{2,60})`")
QUOTED = re.compile(r"[「『\"']([^」』\"']{2,40})[」』\"']")
ASCII_ID = re.compile(r"\b([A-Za-z][A-Za-z0-9_]{2,}(?:[./-][A-Za-z0-9_]+)*)\b")

# 停用词：这些在任何页都会命中，无判别力
STOP = set("""
文档 说明 未说明 官方 本页 本章 本节 该页 客户 用户 支持 配置 控制台 产品 实例 网关
阿里云 需要 可以 如果 因为 所以 但是 以及 或者 例如 如下 以上 以下 其他 相关 具体
全部 所有 任何 没有 不是 这个 那个 我们 你们 他们 一个 一些 什么 怎么 如何 为什么
页面 内容 信息 数据 参数 字段 表格 数字 单价 计费 费用 价格 配额 上限 限制 能力 功能
raw slug http https help aliyun com zh api gateway AI MCP SLA TODO
""".split())


def load_corpus():
    raw = {}
    for p in sorted(RAW_DIR.glob("*.md")):
        raw[p.stem] = p.read_text(encoding="utf-8", errors="ignore")
    know = {}
    for p in sorted(KB.glob(KNOWLEDGE_GLOB)):
        know[p.name] = p.read_text(encoding="utf-8", errors="ignore")
    return raw, know


def terms_of(line: str):
    """只抽高精度术语：反引号内、「」内、ASCII 标识符。"""
    out = []
    for rx in (BACKTICK, QUOTED):
        for m in rx.finditer(line):
            t = m.group(1).strip()
            if t and t not in STOP and not t.startswith("http"):
                out.append(t)
    for m in ASCII_ID.finditer(line):
        t = m.group(1)
        if t in STOP or t.lower() in {s.lower() for s in STOP}:
            continue
        out.append(t)
    # 去重保序，最多 4 个
    seen, res = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            res.append(t)
    return res[:4]



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-weak", action="store_true",
                    help="连普通 `[文档未说明]` 一起扫（默认只扫全称否定；开启会产生数百条噪声）")
    ap.add_argument("--out", default=str(KB / "tests/ai-gateway-negclaim-gate-2026-09-21.md"))
    a = ap.parse_args()

    raw, know = load_corpus()
    findings = []
    scanned = 0
    strong_n = 0

    for fname, text in know.items():
        for ln, line in enumerate(text.splitlines(), 1):
            st = strength(line)
            if st is None or (st == "weak" and not a.include_weak):
                continue
            scanned += 1
            if st == "STRONG":
                strong_n += 1
            for t in terms_of(line):
                raw_hits = [slug for slug, rt in raw.items() if t in rt]
                know_hits = [kn for kn, kt in know.items() if kn != fname and t in kt]
                if raw_hits or know_hits:
                    findings.append(dict(file=fname, line=ln, term=t, strength=st,
                                         raw=raw_hits[:4], raw_n=len(raw_hits),
                                         know=know_hits[:3], know_n=len(know_hits),
                                         ctx=line.strip()[:160]))

    by_loc = defaultdict(list)
    for f in findings:
        by_loc[(f["file"], f["line"])].append(f)

    L = []
    L.append("# AI 网关知识页 · 跨页否定句门禁报告")
    L.append("")
    L.append("生成：2026-09-21 ｜ 生成器：`scripts/gate-negative-claims.py`（机械全扫，非抽样）")
    L.append("")
    L.append("## 判据与定位")
    L.append("")
    L.append("独立评审 R1（`tests/ai-gateway-review-r1-fidelity-2026-09-21.md`）抽样 74 条查出 **5 处 D3「空白被填」**，")
    L.append("根因＝**`[文档未说明]` 被分片 worker 当成「我这个分片没读到」用，而页首图例定义它是「raw 查无此项」（全库口径）**。")
    L.append("7 路并行蒸馏时 A 分片的「查无」常常就写在 B 分片的页里（R1 实测：4 次中有 3 次答案已被本家族另一页正确写下）。")
    L.append("抽样只能撞见一部分 → 本脚本做**全库机械扫描**。")
    L.append("")
    L.append("### 🔴 精度设计（首版教训）")
    L.append("")
    L.append("首版把**全部**否定句（含 550 处普通 `[文档未说明]`）都扫，且抽裸中文名词做反查 →")
    L.append("**655 行里报出 488 处待裁决**，完全不可用：裸中文词在 186 个 raw 文件里几乎必然命中，判别力为零。")
    L.append("修正为两条：① **只扫全称否定**（`全库查无`/`零命中`/`全页无`/`N 页…0 命中` 这类断言「整个文档集都没有」的句子）")
    L.append("——普通 `[文档未说明]` 多半只是「本页没写这个参数」，本身是对的，要扫请显式加 `--include-weak`；")
    L.append("② **只抽高精度术语**：反引号内标识符、「」内术语、ASCII 标识符，不抽裸中文词。")
    L.append("")
    L.append(f"- 扫描文件：{len(know)} 个（`{KNOWLEDGE_GLOB}`）")
    L.append(f"- 命中否定标记的行：**{scanned}** 行（其中全称否定 **{strong_n}** 行）")
    L.append(f"- 反查语料：raw `{RAW_DIR.name}/` {len(raw)} 个快照 + 本家族其余 {len(know)-1} 个知识页")
    L.append(f"- **待裁决项：{len(by_loc)} 处**（涉及 {len(findings)} 个术语命中）")
    L.append("")
    L.append("🔴 **待裁决 ≠ 缺陷**：否定句可能只针对某个侧面（例：「未说明限流超限返回码」与 raw 里出现 `429` 可以并存，")
    L.append("若那个 429 属于另一套机制）。本脚本只负责**把证据摆出来**，裁决由主控逐条做并记入")
    L.append("`tests/ai-gateway-rulings-2026-09-21.md`。")
    L.append("")
    L.append("## 待裁决清单")
    L.append("")
    L.append("| # | 位置 | 术语 | raw 命中 | 本家族他页命中 | 否定句原文（截断） |")
    L.append("|---|---|---|---|---|---|")
    for i, ((fname, ln), items) in enumerate(sorted(by_loc.items()), 1):
        terms = ", ".join("`%s`" % x["term"] for x in items)
        raws = ", ".join("`%s`" % s for s in items[0]["raw"]) or "—"
        if items[0]["raw_n"] > 4:
            raws += " +%d" % (items[0]["raw_n"] - 4)
        knows = ", ".join(x.replace("aliyun-ai-gateway", "…") for x in items[0]["know"]) or "—"
        ctx = items[0]["ctx"].replace("|", "\\|")
        L.append("| %d | `%s:%d` | %s | %s | %s | %s |" % (
            i, fname.replace("aliyun-ai-gateway", "…"), ln, terms, raws, knows, ctx))
    L.append("")
    L.append("## 复核命令（可复算）")
    L.append("")
    L.append("```bash")
    L.append("grep -rn \"<术语>\" raw/aliyun-docs/ai-gateway/ | head")
    L.append("grep -rn \"<术语>\" knowledge/aliyun-ai-gateway*.md | head")
    L.append("python3 scripts/gate-negative-claims.py            # 只扫全称否定（默认，可当门禁）")
    L.append("python3 scripts/gate-negative-claims.py --include-weak   # 连普通 [文档未说明] 一起扫（噪声大）")
    L.append("```")
    L.append("")

    Path(a.out).write_text("\n".join(L), encoding="utf-8")
    print("扫描 %d 个知识页 / %d 行否定句（全称否定 %d 行）→ 待裁决 %d 处（%d 个术语命中）"
          % (len(know), scanned, strong_n, len(by_loc), len(findings)))
    print("报告 → %s" % a.out)
    return 1 if by_loc else 0



if __name__ == "__main__":
    sys.exit(main())
