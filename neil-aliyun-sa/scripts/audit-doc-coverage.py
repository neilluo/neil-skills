#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
覆盖率审计：raw 快照内链 BFS + document_detail 数字形态实时解析

🔴 2026-09-20 AgentCore 实测教训：只扫 `/zh/<product>/<slug>` 会**系统性漏掉** raw 里的
   `document_detail/<数字ID>.html` 形态链接（当时 50 个快照里有 72 条、28 个唯一 docId）。
   两种形态都要扫，数字形态需实时 301 解析反查落点。

用法：
  python3 scripts/audit-doc-coverage.py \
      --rawdir raw/aliyun-docs/ai-gateway \
      --core /tmp/aigw_core_urls.tsv \
      --deferred /tmp/aigw_deferred_urls.tsv \
      --product-prefix https://help.aliyun.com/zh/api-gateway/ai-gateway/ \
      --out-md tests/ai-gateway-coverage-audit-2026-09-21.md \
      --out-new /tmp/aigw_new_candidates.tsv
"""
import argparse
import concurrent.futures as cf
import re
import subprocess
from collections import defaultdict
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 任意 help.aliyun.com 链接（含 .md / .html / 无后缀）
HELP_LINK_RE = re.compile(
    r"https?://help\.aliyun\.com/(?P<path>[^\s)\"'<>]+)")
DOCID_RE = re.compile(r"document_detail/(?P<id>\d+)")


def strip_body(p: Path) -> str:
    """剥掉 10 行 frontmatter，只留原始正文。"""
    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    return "\n".join(lines[10:])


def slug_of(url: str) -> str:
    u = url.split("#")[0].split("?")[0].rstrip("/")
    for suf in (".md", ".html"):
        if u.endswith(suf):
            u = u[: -len(suf)]
    return u.rsplit("/", 1)[-1]


def resolve_docid(docid: str):
    """实时 301 解析 document_detail/<id> → 最终 URL。"""
    url = "https://help.aliyun.com/document_detail/%s.html" % docid
    cmd = ["curl", "-sSL", "-A", UA, "--max-time", "30",
           "-o", "/dev/null", "-w", "%{http_code}\t%{url_effective}", url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        parts = p.stdout.strip().split("\t")
        return docid, (parts[0] if parts else "?"), (parts[1] if len(parts) > 1 else url)
    except Exception as e:  # noqa
        return docid, "ERR", str(e)[:120]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rawdir", required=True)
    ap.add_argument("--core", required=True)
    ap.add_argument("--deferred", required=True)
    ap.add_argument("--product-prefix", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-new", required=True)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    def load_tsv(p):
        d = {}
        for ln in Path(p).read_text(encoding="utf-8").splitlines():
            if ln.strip():
                f = ln.split("\t")
                d[f[0]] = f
        return d

    core, deferred = load_tsv(a.core), load_tsv(a.deferred)
    known = set(core) | set(deferred)

    rawdir = Path(a.rawdir)
    files = sorted(rawdir.glob("*.md"))

    inproduct_links = defaultdict(set)   # slug -> {引用它的快照}
    docid_links = defaultdict(set)
    crossproduct = defaultdict(set)
    external = defaultdict(set)

    for f in files:
        body = strip_body(f)
        for m in HELP_LINK_RE.finditer(body):
            full = m.group(0)
            path = m.group("path")
            dm = DOCID_RE.search(full)
            if dm:
                docid_links[dm.group("id")].add(f.stem)
                continue
            if path.startswith("zh/") and ("/api-gateway/ai-gateway/" in full
                                            or full.startswith(a.product_prefix)):
                inproduct_links[slug_of(full)].add(f.stem)
            else:
                crossproduct[full.split("#")[0].split("?")[0]].add(f.stem)
        for m in re.finditer(r"https?://terms\.alicdn\.com/[^\s)\"'<>]+", body):
            external[m.group(0).split("#")[0]].add(f.stem)
        for m in re.finditer(r"https?://(?!help\.aliyun\.com|terms\.alicdn\.com)[^\s)\"'<>]+", body):
            external[m.group(0).split("#")[0].split("?")[0]].add(f.stem)

    # docId 实时解析
    resolved = {}
    if docid_links:
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for docid, code, final in ex.map(resolve_docid, sorted(docid_links)):
                resolved[docid] = (code, final)

    # 分类
    # 🔴 首版缺陷（主控自审发现）：docId 解析落点若落在**其他产品**（RAM/VPC/user-center/WAF/CDT…），
    #    首版只判 `slug in known`，于是把 173 条跨产品链接全洗成「🆕 新候选」，制造假警报。
    #    正确判据：先看落点 URL 是否在本产品前缀内，**再**判是否已在清单。
    def in_product(url: str) -> bool:
        return "/api-gateway/ai-gateway/" in url or url.startswith(a.product_prefix)

    hit_known, new_candidates, dead = [], [], []
    docid_crossproduct = defaultdict(list)
    for slug, refs in sorted(inproduct_links.items()):
        if slug in known:
            hit_known.append((slug, refs, "slug 形态内链"))
        else:
            new_candidates.append((slug, refs, "slug 形态内链，llms.txt 未收录"))
    for docid, refs in sorted(docid_links.items()):
        code, final = resolved.get(docid, ("?", ""))
        s = slug_of(final) if final else ""
        if code.startswith("4") or code.startswith("5"):
            dead.append((docid, code, final, refs))
        elif not in_product(final or ""):
            docid_crossproduct[(final or "?").split("#")[0].rstrip("/")].append((docid, refs))
        elif s and s in known:
            hit_known.append((s, refs, "docId %s → 落点已收录" % docid))
        else:
            new_candidates.append((s or docid, refs,
                                   "docId %s → %s (HTTP %s)，落在本产品内但清单未收录"
                                   % (docid, final, code)))

    Path(a.out_new).write_text(
        "\n".join("\t".join([s, ";".join(sorted(r)), note]) for s, r, note in new_candidates)
        + ("\n" if new_candidates else ""), encoding="utf-8")

    out = []
    out.append("# AI 网关蒸馏 · 覆盖率审计报告")
    out.append("")
    out.append("生成：2026-09-21 ｜ 生成器：`scripts/audit-doc-coverage.py`（确定性扫描 + docId 实时 301 解析）")
    out.append("")
    out.append("## 一、扫描面")
    out.append("")
    out.append(f"- raw 快照：**{len(files)}** 个（`{a.rawdir}`）")
    out.append(f"- 已知清单：core {len(core)} + deferred {len(deferred)} = **{len(known)}** 个 slug")
    out.append(f"- 本产品内链（slug 形态）唯一目标：**{len(inproduct_links)}** 个")
    out.append(f"- `document_detail/<数字ID>` 形态链接：唯一 docId **{len(docid_links)}** 个")
    out.append(f"- 跨产品 help.aliyun.com 链接：**{len(crossproduct)}** 个")
    out.append(f"- 站外链接（terms.alicdn.com / 第三方）：**{len(external)}** 个")
    out.append("")
    out.append("## 二、判定结果")
    out.append("")
    out.append(f"| 类别 | 数量 | 含义 |")
    out.append(f"|---|---|---|")
    out.append(f"| 命中既有清单 | {len(hit_known)} | 内链目标已在 core/deferred 内 → 无遗漏 |")
    out.append(f"| 🆕 新候选（清单外） | {len(new_candidates)} | 需主控裁决是否补抓 |")
    out.append(f"| ☠️ 死链 | {len(dead)} | docId 解析返回 4xx/5xx |")
    out.append("")
    if new_candidates:
        out.append("### 🆕 新候选明细")
        out.append("")
        out.append("| slug / docId | 被哪些快照引用 | 备注 |")
        out.append("|---|---|---|")
        for s, refs, note in new_candidates:
            r = ", ".join(sorted(refs)[:4]) + ("…" if len(refs) > 4 else "")
            out.append(f"| `{s}` | {r} | {note} |")
        out.append("")
    if dead:
        out.append("### ☠️ 死链明细")
        out.append("")
        for docid, code, final, refs in dead:
            out.append(f"- docId `{docid}` → HTTP {code} ｜ 被 {len(refs)} 个快照引用")
        out.append("")
    out.append("## 三、跨产品链接（不纳入本产品范围，仅登记）")
    out.append("")
    prods = defaultdict(list)
    for u, refs in crossproduct.items():
        m = re.search(r"help\.aliyun\.com/zh/([^/]+)/", u)
        prods[m.group(1) if m else "(其他形态)"].append((u, refs))
    out.append("| 目标产品 | 链接数 |")
    out.append("|---|---|")
    for p, lst in sorted(prods.items(), key=lambda kv: -len(kv[1])):
        out.append(f"| `{p}` | {len(lst)} |")
    out.append("")
    out.append("## 四、站外权威源（需单独补抓的协议原文等）")
    out.append("")
    for u, refs in sorted(external.items()):
        if "terms.alicdn.com" in u or "alicdn.com" in u:
            out.append(f"- 🔴 {u} ｜ 被 {', '.join(sorted(refs))} 引用")
    out.append("")
    out.append("## 五、本方法检测不到的残留面（必须如实声明）")
    out.append("")
    out.append("若某页同时满足「近日新增 + 未进 llms.txt + 无任何快照内链 + 非顶级栏目」，")
    out.append("上述方法**检测不到**，需 JS 拉实时目录树 API 才能穷尽。")
    out.append("→ 蒸馏产物**不得宣称「全站蒸馏」**，须把这条边界写进溯源节。")
    out.append("")

    Path(a.out_md).write_text("\n".join(out), encoding="utf-8")
    print(f"快照 {len(files)} ｜ 内链唯一目标 {len(inproduct_links)} ｜ docId {len(docid_links)} "
          f"｜ 命中 {len(hit_known)} ｜ 新候选 {len(new_candidates)} ｜ 死链 {len(dead)}")
    print(f"报告 → {a.out_md}")
    if new_candidates:
        print("\n🆕 新候选（前 30）：")
        for s, refs, note in new_candidates[:30]:
            print(f"  {s:60s} refs={len(refs)} {note}")


if __name__ == "__main__":
    main()
