#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 help.aliyun.com 按产品 llms.txt 生成蒸馏 URL 清单 + 分片。

用法：
  python3 scripts/build-doc-inventory.py \
      --llms /tmp/aigw-llms.txt \
      --product ai-gateway \
      --url-prefix https://help.aliyun.com/zh/api-gateway/ai-gateway/ \
      --out-md tests/ai-gateway-doctree-shards-2026-09-21.md \
      --out-core /tmp/aigw_core_urls.tsv \
      --out-deferred /tmp/aigw_deferred_urls.tsv

分类规则（与 2026-09-20 AgentCore/AgentRun 先例一致）：
  core      — 叙事文档，进入本次蒸馏
  deferred  — 逐 Action / 逐数据结构的 OpenAPI 参考页，登记延后
  meta      — 开发参考里的元页（概览/接入点/RAM/配额/错误码/变更集/容器），破例纳入 core

判据全部基于 slug 字面结构，不做语义猜测；不确定的归 core（宁可多抓，抓取阶段再用
三重校验剔除 TOC 容器与软 200）。
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)(?::\s*(?P<desc>.*))?$")
SECTION_RE = re.compile(r"^(?P<hashes>#+)\s+(?P<title>.+?)\s*$")

# 开发参考下「元页」白名单。
# 🔴 必须是**精确 slug 允许表**，不能用关键词子串匹配：子串法会把
#    `api-apig-2024-03-27-getresourceoverview`（含 overview）、
#    `api-apig-2024-03-27-*gatewayquotarule*` 共 10 页（含 quota）、
#    `api-apig-2024-03-27-struct-httpapiparameter-ai-gateway`（pa**ram**eter 含 ram）
#    误纳为元页 —— 首版实测多纳 11 页逐 Action 参考页。判据要匹配语法结构，不匹配裸词。
# 形态 A：不带 APIG 版本前缀的参考类容器/索引页
META_EXACT_SLUGS = {
    "developer-reference",
    "api-reference",
    "sdk-reference",
    "cli-reference",
}
# 形态 B：带 `api-apig-2024-03-27-` 前缀的元页（其 tail 精确枚举）
APIG_META_TAILS = {
    "overview-ai-gateway",   # OpenAPI 概览
    "endpoint-ai-gateway",   # 服务接入点
    "ram-ai-gateway",        # RAM 授权信息 Action/Resource/Condition
    "quota-ai-gateway",      # OpenAPI 流控配额
    "changeset-ai-gateway",  # OpenAPI 变更集
    "errorcodes",            # 公共错误码
}
APIG_PREFIX = "api-apig-2024-03-27-"


def slug_of(url: str) -> str:
    """取 URL 最后一段（去掉 .md / 尾斜杠 / query）。"""
    u = url.split("#")[0].split("?")[0]
    u = u.rstrip("/")
    if u.endswith(".md"):
        u = u[:-3]
    return u.rsplit("/", 1)[-1]


def is_meta_reference_page(slug: str) -> bool:
    """开发参考下的元页（概览/接入点/RAM/配额/错误码/变更集/参考索引容器）。"""
    if slug in META_EXACT_SLUGS:
        return True
    if slug.startswith(APIG_PREFIX) and slug[len(APIG_PREFIX):] in APIG_META_TAILS:
        return True
    return False


def is_openapi_action_page(slug: str) -> bool:
    """APIG 2024-03-27 逐 Action / 逐数据结构参考页的 slug 形态。"""
    if not slug.startswith("api-apig-"):
        return False
    return not is_meta_reference_page(slug)



def parse(llms_path: Path):
    rows = []
    section = "(preamble)"
    for raw_line in llms_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        m = SECTION_RE.match(line)
        if m and line.startswith("#"):
            section = m.group("title").strip()
            continue
        m = LINK_RE.match(line)
        if not m:
            continue
        url = m.group("url").strip()
        title = m.group("title").strip()
        desc = (m.group("desc") or "").strip()
        rows.append({
            "section": section,
            "title": title,
            "url": url,
            "slug": slug_of(url),
            "desc": desc,
            "is_container": desc == "",   # 无摘要的多为目录容器节点
        })
    return rows


def classify(rows, product_prefix):
    """
    🔴 归属判据 = **llms.txt 收录**，不是 URL 前缀（2026-09-21 主控自审修正）。

    首版按 `url.startswith(product_prefix)` 判归属，把 3 页**确实属于 AI 网关文档集**
    但挂在父级 `/zh/api-gateway/` 路径下的页面误判为 external 踢出范围：
      - `ai-gateway-commercialization-announcement`（🔴 Serverless 新版商业化公告，
        2026-09-01 起计费 —— 本次蒸馏时点的**现行计费权威源**，漏掉是硬伤）
      - `consumer-quotas-management`（AI网关-管理消费者配额 / FinOps）
      - `request-response-capture-1`（API网关请求/响应采集）
    这与 [[aliyun-help-center-md-channel]]「产品归属别从首页导航推断」同源：
    **收录关系看 llms.txt，不看 URL 视觉层级。**
    """
    core, deferred = [], []
    for r in rows:
        u = r["url"]
        in_llms_scope = True   # rows 全部来自本产品 llms.txt，收录即归属
        if "/developer-reference/" in u and is_openapi_action_page(r["slug"]):
            r["cls"] = "deferred"
            r["reason"] = "OpenAPI 逐 Action / 逐数据结构参考页"
            deferred.append(r)
        elif not in_llms_scope:
            r["cls"] = "external"
            r["reason"] = "非本产品 llms.txt 收录"
            deferred.append(r)
        else:
            r["cls"] = "core"
            if "/developer-reference/" in u:
                r["reason"] = "开发参考元页（精确 slug 允许表破例纳入）"
            elif not u.startswith(product_prefix):
                r["reason"] = ("挂在父级 api-gateway 路径下但被 AI 网关 llms.txt 收录 → 属本产品文档集"
                               "（首版曾误判 external）")
            else:
                r["reason"] = "叙事文档"
            core.append(r)
    return core, deferred


def shard(rows, per_shard=26):
    """按栏目聚簇分片：同栏目尽量落同一片，便于蒸馏员建立局部语境。"""
    shards = []
    cur, cur_sec = [], None
    for r in rows:
        if cur_sec is not None and r["section"] != cur_sec and len(cur) >= per_shard * 0.6:
            shards.append(cur)
            cur = []
        cur.append(r)
        cur_sec = r["section"]
        if len(cur) >= per_shard:
            shards.append(cur)
            cur = []
    if cur:
        shards.append(cur)
    return shards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--llms", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--url-prefix", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-core", required=True)
    ap.add_argument("--out-deferred", required=True)
    ap.add_argument("--per-shard", type=int, default=26)
    a = ap.parse_args()

    rows = parse(Path(a.llms))
    core, deferred = classify(rows, a.url_prefix)
    shards = shard(core, a.per_shard)

    # TSV：slug <TAB> url <TAB> section <TAB> title <TAB> is_container
    def write_tsv(path, items):
        with open(path, "w", encoding="utf-8") as f:
            for r in items:
                f.write("\t".join([
                    r["slug"], r["url"], r["section"], r["title"],
                    "container" if r["is_container"] else "content",
                ]) + "\n")

    write_tsv(a.out_core, core)
    write_tsv(a.out_deferred, deferred)

    # Markdown 审计报告
    by_sec = {}
    for r in rows:
        by_sec.setdefault(r["section"], {"core": 0, "deferred": 0, "external": 0})
        by_sec[r["section"]][r["cls"]] += 1

    out = []
    out.append(f"# {a.product} 文档树 · 分片清单与范围裁决")
    out.append("")
    out.append(f"生成：2026-09-21 ｜ 生成器：`scripts/build-doc-inventory.py`（确定性解析，非 LLM 归纳）｜ "
               f"源：`{a.llms}`")
    out.append("")
    out.append(f"llms.txt 链接总数 **{len(rows)}** = core **{len(core)}** + deferred **{len(deferred)}**")
    out.append("")
    out.append("## 一、按栏目分类计数")
    out.append("")
    out.append("| 栏目 | core（本次蒸馏） | deferred（延后） | external |")
    out.append("|---|---|---|---|")
    for sec, c in by_sec.items():
        out.append(f"| {sec} | {c['core']} | {c['deferred']} | {c['external']} |")
    out.append(f"| **合计** | **{len(core)}** | **{len(deferred)}** | "
               f"**{sum(c['external'] for c in by_sec.values())}** |")
    out.append("")
    out.append("分类判据（**精确 slug 允许表，非关键词子串**）：`/developer-reference/` 下 slug 形如 "
               "`api-apig-2024-03-27-*` → deferred（逐 Action / 逐数据结构参考页），"
               "除非其 tail 精确等于 {overview-ai-gateway, endpoint-ai-gateway, ram-ai-gateway, "
               "quota-ai-gateway, changeset-ai-gateway, errorcodes}，或 slug 精确等于 "
               "{developer-reference, api-reference, sdk-reference, cli-reference} → core。"
               "其余栏目一律 core。**不做语义猜测**，判据可复算。")
    out.append("")
    out.append("> 🔴 首版曾用关键词子串白名单（overview/quota/ram/...），实测误纳 11 页逐 Action 页："
               "`getresourceoverview`（含 overview）、10 个 `*gatewayquotarule*`（含 quota）、"
               "`struct-httpapiparameter-ai-gateway`（pa**ram**eter 含 ram）。已改为精确允许表。")
    out.append("")
    out.append("## 二、core 分片（蒸馏 worker 指派单位）")
    out.append("")
    for i, sh in enumerate(shards, 1):
        secs = sorted({r["section"] for r in sh})
        out.append(f"### SHARD-{i}（{len(sh)} 页 ｜ 栏目：{'、'.join(secs)}）")
        out.append("")
        for r in sh:
            flag = " 📁容器" if r["is_container"] else ""
            out.append(f"- `{r['slug']}.md` — {r['title']}{flag}")
        out.append("")
    out.append("## 三、纳入 core 的开发参考元页（白名单破例，逐条列出以便复核）")
    out.append("")
    for r in core:
        if "/developer-reference/" in r["url"]:
            out.append(f"- `{r['slug']}.md` — {r['title']}")
            if r["desc"]:
                out.append(f"  - 摘要：{r['desc']}")
    out.append("")
    out.append("## 四、deferred 清单（登记不蒸馏）")
    out.append("")
    out.append(f"共 **{len(deferred)}** 条，明细见同批生成的 TSV。前 20 条示例：")
    out.append("")
    for r in deferred[:20]:
        out.append(f"- `{r['slug']}` — {r['title']} ｜ {r.get('reason','')}")
    out.append("")
    out.append("## 五、可复算性")
    out.append("")
    llms_bytes = Path(a.llms).read_bytes()
    out.append(f"- llms.txt 快照：`{a.llms}`，{len(llms_bytes)} 字节，"
               f"SHA256 `{hashlib.sha256(llms_bytes).hexdigest()}`")
    out.append(f"- core TSV：`{a.out_core}`（{len(core)} 行）")
    out.append(f"- deferred TSV：`{a.out_deferred}`（{len(deferred)} 行）")
    out.append("- 重跑本脚本应产出逐字节相同的 MD 与 TSV（除时间戳行外）。")
    out.append("")

    Path(a.out_md).write_text("\n".join(out), encoding="utf-8")
    print(f"core={len(core)} deferred={len(deferred)} shards={len(shards)} -> {a.out_md}")


if __name__ == "__main__":
    main()
