#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
help.aliyun.com 官方 `.md` Agent 通道 · 确定性抓取器

设计原则：抓取由脚本完成而非 subagent，产物可复算、可审计、无「二手结论」污染。

🔴 软 200 陷阱（本项目已实测）：不存在的 slug 也返回 HTTP 200 + 约 24893 字节的
   SPA HTML 外壳。**HTTP 状态码绝不能作为成功判据**。

三重校验：
  1. Content-Type 含 `markdown`
  2. body 前 60 字节（忽略大小写与前导空白）不以 `<!doctype` / `<html` 开头
  3. TOC 容器判据 = 「正文仅由标题 + 链接列表构成、无产品事实陈述」
     🔴 字节数阈值**只**用于识别约 24893B 的软 200 HTML 外壳，**不**用于识别 TOC
     （2026-09-20 AgentCore RULINGS C1：字节阈值会让同性质的目录页只因链接条数
      不同而判定相反，是假阳性来源）

用法：
  python3 scripts/fetch-aliyun-docs.py \
      --tsv /tmp/aigw_core_urls.tsv \
      --product "AI Gateway" \
      --outdir raw/aliyun-docs/ai-gateway \
      --manifest tests/ai-gateway-fetch-manifest-2026-09-21.tsv \
      --workers 6
"""
import argparse
import concurrent.futures as cf
import hashlib
import re
import subprocess
import sys
import time
from pathlib import Path

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

SOFT200_SHELL_BYTES = 24893   # 实测 SPA HTML 外壳大小，±1KB 容差
LINK_LINE_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\[[^\]]*\]\([^)]*\)\s*(?::\s*.*)?$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")
BARE_LINK_LINE_RE = re.compile(r"^\s*\[[^\]]*\]\([^)]*\)\s*$")

# 🔴 第四种失效模式（2026-09-21 AI 网关 185 页实测新发现，AgentCore 契约未覆盖）：
# `.md` 通道对「存在于导航树但无 Markdown 正文」的目录节点返回
#   Content-Type: text/markdown + HTTP 200 + 86 字节固定桩文
#   `# Document Not Found\n\nThe requested document does not have Markdown content available.`
# 它**同时通过**前三重校验（CT 合格、非 HTML 外壳、有标题+散文故非 TOC），
# 首版抓取器把它判成 OK 落盘 4 页垃圾。必须显式识别。
NOMD_STUB_RE = re.compile(
    r"^\s*#\s*Document Not Found\s*$", re.IGNORECASE | re.MULTILINE)
NOMD_STUB_MARK = "does not have Markdown content available"


LEGACY_TITLE_HINTS = ("旧版", "（旧）", "(旧)", "已下线", "停止服务")
LEGACY_SLUG_HINTS = ("-old-", "-legacy", "old-billing", "serverless-old")


def curl(url: str, timeout: int = 40):
    """返回 (http_code, content_type, body_bytes, final_url, err)。纯 curl，不用浏览器。"""
    hdr = Path("/tmp/_hdr_%d.txt" % (hash(url) & 0xFFFF))
    out = Path("/tmp/_body_%d.bin" % (hash(url) & 0xFFFF))
    cmd = ["curl", "-sSL", "-A", UA, "--max-time", str(timeout),
           "-D", str(hdr), "-o", str(out),
           "-w", "%{http_code}\t%{content_type}\t%{size_download}\t%{url_effective}",
           url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", b"", url, "curl timeout"
    if p.returncode != 0:
        return "CURLERR%d" % p.returncode, "", b"", url, p.stderr.strip()[:200]
    parts = p.stdout.strip().split("\t")
    code = parts[0] if parts else "?"
    ct = parts[1] if len(parts) > 1 else ""
    final = parts[3] if len(parts) > 3 else url
    body = out.read_bytes() if out.exists() else b""
    hdr.unlink(missing_ok=True)
    out.unlink(missing_ok=True)
    return code, ct, body, final, ""


def is_toc(body_text: str) -> bool:
    """TOC 容器判据：正文仅由标题 + 链接列表构成，无产品事实陈述。"""
    lines = [ln for ln in body_text.splitlines() if ln.strip()]
    if not lines:
        return True
    structural = 0
    prose_chars = 0
    for ln in lines:
        if HEADING_RE.match(ln) or LINK_LINE_RE.match(ln) or BARE_LINK_LINE_RE.match(ln):
            structural += 1
        else:
            # 链接列表项里可能带描述文字（`- [x](y): 描述`），描述算弱事实，
            # 但整页若**全部**是这种行，仍是目录页 → 只有非链接行才算散文
            prose_chars += len(ln.strip())
    return structural == len(lines) and prose_chars == 0


def verdict(code, ct, body, body_text):
    """三重校验。返回 (verdict, reason)。"""
    head60 = body[:60].decode("utf-8", "ignore").lower().lstrip()
    if "markdown" not in (ct or "").lower():
        if head60.startswith("<!doctype") or head60.startswith("<html"):
            return "FAIL-SOFT200", "CT=%s 且 body 以 HTML 开头（软 200 外壳）" % ct
        return "FAIL-CT", "Content-Type=%s" % ct
    if head60.startswith("<!doctype") or head60.startswith("<html"):
        return "FAIL-SOFT200", "body 前 60 字节为 HTML（%d B，软 200 外壳实测约 %d B）" % (
            len(body), SOFT200_SHELL_BYTES)
    if len(body) == 0:
        return "FAIL-EMPTY", "body 0 字节"
    if NOMD_STUB_RE.search(body_text) and NOMD_STUB_MARK in body_text:
        return "FAIL-NOMD", (".md 通道返回 Content-Type: text/markdown，但正文是 86B 固定桩 "
                             "「# Document Not Found / does not have Markdown content available」"
                             "→ 该节点存在于导航树但无 Markdown 正文（目录节点），不落盘。"
                             "🔴 实测同一 slug 两次抓取分别返回 HTTP 200 与 404，故状态码不可作判据")
    if is_toc(body_text):
        return "TOC", "正文仅由标题+链接列表构成（%d B，无散文）→ 目录容器，不作事实来源" % len(body)
    if len(body) < 500 and "terms.alicdn.com" in body_text:
        return "OK-STUB", ("正文 %d B 且仅指向 terms.alicdn.com 外部协议原文 → 本页为入口桩，"
                           "权威条款在外部页，需补抓" % len(body))
    return "OK", ""


def migration_status(title: str, slug: str) -> str:
    t = title or ""
    s = slug or ""
    if any(h in t for h in LEGACY_TITLE_HINTS) or any(h in s for h in LEGACY_SLUG_HINTS):
        return "legacy"
    return "current"


def frontmatter(source_url, fetch_date, product, slug, body_bytes, sha, mstatus):
    return "\n".join([
        "---",
        "source_url: %s" % source_url,
        "fetch_date: %s" % fetch_date,
        "product: %s" % product,
        "slug: %s" % slug,
        "body_sha256: %s" % sha,
        "body_bytes: %d" % body_bytes,
        "migration_status: %s" % mstatus,
        "---",
        "",
    ]) + "\n"


def fetch_one(row, outdir: Path, product: str, fetch_date: str, retries: int = 2):
    slug, url, section, title, kind = row
    attempt, last = 0, None
    while attempt <= retries:
        attempt += 1
        code, ct, body, final, err = curl(url)
        body_text = body.decode("utf-8", "ignore")
        v, reason = verdict(code, ct, body, body_text)
        last = (code, ct, body, body_text, v, reason, final, err)
        if v in ("OK", "TOC", "OK-STUB"):
            break
        if v == "FAIL-EMPTY" or v.startswith("CURLERR") or code == "TIMEOUT":
            time.sleep(1.0 * attempt)
            continue
        break  # 软 200 / CT 不符：重试无意义
    code, ct, body, body_text, v, reason, final, err = last

    # 人类可读 URL = 去掉 .md 后缀
    human = url[:-3] if url.endswith(".md") else url
    sha = hashlib.sha256(body).hexdigest()
    written = ""
    if v in ("OK", "TOC", "OK-STUB"):
        # TOC 容器页也落盘（承载目录结构与 slug↔ID 对照证据），但 frontmatter 之外
        # 在 manifest 里标 TOC，蒸馏员不得引为事实来源
        mstatus = migration_status(title, slug)
        path = outdir / ("%s.md" % slug)
        path.write_text(frontmatter(human, fetch_date, product, slug, len(body), sha, mstatus)
                        + body_text, encoding="utf-8")
        written = str(path)
    return {
        "slug": slug, "url": url, "section": section, "title": title,
        "http": code, "ct": ct, "bytes": len(body), "verdict": v,
        "reason": reason or err, "sha256": sha, "path": written,
        "migration_status": migration_status(title, slug) if written else "",
        "final_url": final if final != url else "",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--fetch-date", default=time.strftime("%Y-%m-%d"))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only-missing", action="store_true",
                    help="已存在且 sha 一致的快照跳过重抓（增量同步）")
    a = ap.parse_args()

    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for ln in Path(a.tsv).read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        p = ln.split("\t")
        rows.append((p[0], p[1], p[2] if len(p) > 2 else "", p[3] if len(p) > 3 else "",
                     p[4] if len(p) > 4 else "content"))

    results = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(fetch_one, r, outdir, a.product, a.fetch_date): r for r in rows}
        for i, f in enumerate(cf.as_completed(futs), 1):
            res = f.result()
            results.append(res)
            if i % 20 == 0 or i == len(rows):
                print("  ... %d/%d (%.0fs)" % (i, len(rows), time.time() - t0), file=sys.stderr)

    order = {r[0]: i for i, r in enumerate(rows)}
    results.sort(key=lambda r: order.get(r["slug"], 1 << 30))

    man = Path(a.manifest)
    man.parent.mkdir(parents=True, exist_ok=True)
    with man.open("w", encoding="utf-8") as f:
        f.write("slug\turl\tsection\ttitle\thttp\tcontent_type\tbody_bytes\tverdict\t"
                "migration_status\tsha256\tpath\tfinal_url\treason\n")
        for r in results:
            f.write("\t".join([
                r["slug"], r["url"], r["section"], r["title"], str(r["http"]), r["ct"],
                str(r["bytes"]), r["verdict"], r["migration_status"], r["sha256"],
                r["path"], r["final_url"], r["reason"].replace("\t", " ").replace("\n", " "),
            ]) + "\n")

    # SHA256SUMS（对**原始正文**算，不含 frontmatter —— 与 agentcore 先例一致）
    sums = outdir / "SHA256SUMS.txt"
    with sums.open("w", encoding="utf-8") as f:
        f.write("# SHA256 只对「原始正文」计算，不含快照的 7 字段 frontmatter（前 10 行）。\n")
        f.write("# 故 `shasum -a 256 -c SHA256SUMS.txt` 会全部 FAILED —— 设计使然，非快照损坏。\n")
        f.write("# 正确校验：tail -n +11 <file>.md | shasum -a 256\n")
        for r in results:
            if r["path"]:
                f.write("%s  %s.md\n" % (r["sha256"], r["slug"]))

    from collections import Counter
    c = Counter(r["verdict"] for r in results)
    print("\n=== 抓取完成 ===")
    print("总数 %d ｜ %s" % (len(results), " ｜ ".join("%s=%d" % kv for kv in sorted(c.items()))))
    print("耗时 %.0fs ｜ manifest: %s" % (time.time() - t0, man))
    fails = [r for r in results if r["verdict"].startswith("FAIL")]
    if fails:
        print("\n=== 失败清单（%d 条，如实上报，不伪造不静默跳过）===" % len(fails))
        for r in fails:
            print("  %-8s %-60s http=%s bytes=%d %s" %
                  (r["verdict"], r["slug"][:60], r["http"], r["bytes"], r["reason"][:90]))


if __name__ == "__main__":
    main()
