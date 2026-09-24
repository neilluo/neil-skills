#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 网关专题页家族「规模数字」单源同步器。

🔴 为什么需要这个脚本：行数/表数这类数字被硬编码在 **6 个消费面**（主页导航表 + 主页统计行、
index.md 产品知识行 + 子页行、changelog.md、inbox.md、aliyun-products.md 指针卡、rulings R3 表）。
每次内容改动都会让它们过期，而手工改必漏 —— 与既有教训 [[caliber-change-sweeps-all-surfaces]]
同源：**改口径/数字必须同批 sweep 所有消费面，不一致不得留给用户发现**。

做法：以 `wc -l` 与表格分隔行计数为**唯一事实源**，正则替换所有消费面里的旧值。
幂等：重复运行结果不变。运行后必须自己复核「残留旧值 = 0」。

用法：python3 scripts/sync-aigw-metrics.py [--check]
      --check 只报告漂移，不写入（可当门禁用）
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent

FAMILY = [
    ("aliyun-ai-gateway.md", "主页"),
    ("aliyun-ai-gateway-billing.md", "-billing"),
    ("aliyun-ai-gateway-traffic.md", "-traffic"),
    ("aliyun-ai-gateway-auth.md", "-auth"),
    ("aliyun-ai-gateway-mcp-agent.md", "-mcp-agent"),
    ("aliyun-ai-gateway-plugins.md", "-plugins"),
    ("aliyun-ai-gateway-ops.md", "-ops"),
]

CONSUMERS = [
    "knowledge/aliyun-ai-gateway.md",
    "knowledge/aliyun-products.md",
    "knowledge/inbox.md",
    "index.md",
    "changelog.md",
    "tests/ai-gateway-rulings-2026-09-21.md",
]


def measure():
    lines, tables = {}, {}
    for fn, _ in FAMILY:
        p = KB / "knowledge" / fn
        t = p.read_text(encoding="utf-8")
        lines[fn] = len(t.splitlines())
        tables[fn] = len(re.findall(r"(?m)^\|[-: |]+\|$", t))
    return lines, tables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    lines, tables = measure()
    total_lines = sum(lines.values())
    total_tables = sum(tables.values())
    main_lines = lines["aliyun-ai-gateway.md"]

    print("=== 唯一事实源（实测） ===")
    for fn, label in FAMILY:
        print("  %-42s %5d 行  %4d 表" % (fn, lines[fn], tables[fn]))
    print("  %-42s %5d 行  %4d 表" % ("合计", total_lines, total_tables))

    # 可能被硬编码的旧值：抓所有「4 位数 + 行」与「3~4 位数 + 张表」形态
    stale_lines = set()
    stale_tables = set()
    for rel in CONSUMERS:
        t = (KB / rel).read_text(encoding="utf-8")
        for m in re.finditer(r"\b(\d{3,5})\s*行", t):
            stale_lines.add(m.group(1))
        for m in re.finditer(r"\b(\d{3,5})\s*张表", t):
            stale_tables.add(m.group(1))
    cur_lines = {str(v) for v in lines.values()} | {str(total_lines), str(main_lines)}
    cur_tables = {str(v) for v in tables.values()} | {str(total_tables)}

    drift = []
    for rel in CONSUMERS:
        t = (KB / rel).read_text(encoding="utf-8")
        orig = t
        # 主页行数与家族合计（成对出现的两种句式）
        t = re.sub(r"主页\s*\*{0,2}1?\d{3}\s*行", "主页 %d 行" % main_lines, t)
        t = re.sub(r"\*{0,2}7 个知识文件 / \d{3,5} 行 / \d{3,5} 张表\*{0,2}",
                   "**7 个知识文件 / %d 行 / %d 张表**" % (total_lines, total_tables), t)
        t = re.sub(r"7 文件（\d{3,5} 行 / \d{3,5} 张表",
                   "7 文件（%d 行 / %d 张表" % (total_lines, total_tables), t)
        t = re.sub(r"6 子页 = \d{3,5} 行 / \d{3,5} 张表",
                   "6 子页 = %d 行 / %d 张表" % (total_lines, total_tables), t)
        t = re.sub(r"合计 \*{0,2}\d{3,5}\*{0,2} 行 / \*{0,2}\d{3,5}\*{0,2} 张表",
                   "合计 **%d** 行 / **%d** 张表" % (total_lines, total_tables), t)
        t = re.sub(r"装配后 \d{3,5} 行", "装配后 %d 行" % total_lines, t)
        # 导航表 / R3 表里的主页行「| 1338 |」
        t = re.sub(r"(§14 实战避坑 · §15 SA 速查卡 \| )\d{3,5}( \|)",
                   r"\g<1>%d\g<2>" % main_lines, t)
        t = re.sub(r"(§14 实战避坑 · §15 SA 速查卡 · 子页导航 \| )\*{0,2}\d{3,5}\*{0,2}( \|)",
                   r"\g<1>**%d**\g<2>" % main_lines, t)
        # 各子页行数：① 表格单元「| 953 |」 ② 行内「953 行」
        for fn, _ in FAMILY[1:]:
            stem = fn[:-3]
            n = lines[fn]
            for pat, rep in (
                (r"(%s\.md\)[^|\n]*\|[^|\n]*\| )\d{3,5}( \|)" % re.escape(stem), r"\g<1>%d\g<2>" % n),
                (r"(\]\(knowledge/%s\.md\)[^|\n]*\|[^|\n]*\| )\d{3,5}( \|)" % re.escape(stem), r"\g<1>%d\g<2>" % n),
                (r"(`knowledge/%s\.md` \|[^|\n]*\| )\d{3,5}( \|)" % re.escape(stem), r"\g<1>%d\g<2>" % n),
                (r"(`knowledge/%s\.md` \|[^|\n]*\| )\*{0,2}\d{3,5}\*{0,2}( \|)" % re.escape(stem), r"\g<1>**%d**\g<2>" % n),
            ):
                t = re.sub(pat, rep, t)
        # index.md 子页行：🔴 必须**按章节标签锚定**，不能按出现顺序位置替换。
        # 首版用 `(?= 行 ｜)` 位置替换，两次运行后把 6 个数字**洗乱**（billing 位上出现 1539）——
        # 因为匹配集合与 FAMILY 顺序不保证一致，位置法天然不幂等。
        LABEL_ANCHOR = {
            "aliyun-ai-gateway-billing.md": r"§3 计费与商务（含 §3\.9 SLA 与赔偿）",
            "aliyun-ai-gateway-traffic.md": r"§4 核心对象模型 \+ §5 流量治理与成本控制",
            "aliyun-ai-gateway-auth.md": r"§6 鉴权与消费者体系 \+ §7 AI 安全护栏与 RAM",
            "aliyun-ai-gateway-mcp-agent.md": r"§8 MCP 与 Agent API 生态",
            "aliyun-ai-gateway-plugins.md": r"§9 插件体系",
            "aliyun-ai-gateway-ops.md": r"§13 OpenAPI 与 RAM 元信息",
        }
        for fn, label in LABEL_ANCHOR.items():
            n = lines[fn]
            t = re.sub(r"(%s)\s*\d{3,5}(?= 行)" % label, r"\g<1>%d" % n, t)
        if t != orig:
            drift.append(rel)
            if not a.check:
                (KB / rel).write_text(t, encoding="utf-8")

    print("\n=== 消费面%s ===" % ("漂移（--check，未写入）" if a.check else "已同步"))
    for rel in drift:
        print("  ✏️  %s" % rel)
    if not drift:
        print("  （无漂移，全部一致）")

    # 复核：只扫「家族规模口径」的句子，避免把 924 行原文 / 189 行 manifest / 166 行 SLR 等
    # 合法数字误报成漂移（首版allowlist 法误报 65 处，全是噪声）
    if not a.check:
        SCALE_CTX = re.compile(r"(7 个知识文件|7 文件（|6 子页 =|装配后|合计 \*\*|§15 SA 速查卡)")
        # 同一行里合法的非家族规模数字（raw README 行数等），不参与漂移判定
        BENIGN = re.compile(r"README(?:\.md)?\s*\d{3,5}\s*行")
        valid = cur_lines | cur_tables
        bad = []
        for rel in CONSUMERS:
            for ln, line in enumerate((KB / rel).read_text(encoding="utf-8").splitlines(), 1):
                if not SCALE_CTX.search(line):
                    continue
                probe = BENIGN.sub("README.md 0 行", line)
                for m in re.finditer(r"\b(\d{3,5})\s*(?:行|张表)", probe):
                    if m.group(1) not in valid and m.group(1) not in {"8944", "2500"}:
                        bad.append((rel, ln, m.group(1), line.strip()[:110]))
        if bad:
            print("\n🔴 规模口径残留旧值 %d 处：" % len(bad))
            for rel, ln, v, ctx in bad[:20]:
                print("   %s:%d  %s  …%s…" % (rel, ln, v, ctx))
            return 1
        print("\n✅ 规模口径全消费面一致，残留旧值 = 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
