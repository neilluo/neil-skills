#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 网关专题页家族 · 装配质量与引用完整性 lint（机械可判定部分）。

🔴 为什么是脚本而不是 subagent：本次首派的一致性评审 agent（R2）跑 59 分钟 / 120 次工具调用后
**死于模型服务错误、产物为 0**。它的任务书含 5 个维度，其中 B（交叉引用完整性）与 D（装配质量）
是**纯机械可判定**的 —— 这类检查交给 agent 既慢又会死，交给脚本则确定性、可复算、可当门禁。
（与既有教训同源：修正/审计类 Job 范围过宽 = 必死；机械判定不要交给 LLM。）
语义维度（同一事实跨页口径一致性、与既有页面冲突、SA 可用性）才需要 agent，且必须窄范围单派。

检查项：
  L1 markdown 链接目标文件是否存在
  L2 跨文件 `§N` / `§N.M` 引用在目标文件里是否真的有对应标题
  L3 装配残留：`<!-- W` 注释、`# W<n> partial` 标题、TODO/占位符、重复 H1
  L4 页眉六要素齐备 + W 代号对照表指针
  L5 每文件 < 2500 行（AGENTS.md 拆分阈值）
  L6 章节号 §1~§15 在家族内唯一、不重号
  L7 表格完整性：每行的 `|` 数与表头一致（抓拼接断表）
  L8 `W1`~`W7` 代号残留计数（有对照表则可接受，但要报数）

用法：python3 scripts/lint-aigw-pages.py [--strict]
退出码：0 = 无 P0；1 = 有 P0（--strict 下 P1 也返回 1）
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent
FAMILY = [
    "aliyun-ai-gateway.md",
    "aliyun-ai-gateway-billing.md",
    "aliyun-ai-gateway-traffic.md",
    "aliyun-ai-gateway-auth.md",
    "aliyun-ai-gateway-mcp-agent.md",
    "aliyun-ai-gateway-plugins.md",
    "aliyun-ai-gateway-ops.md",
]
HEADER_REQUIRED = ["**所属**", "**来源**", "**raw 层**", "**事实标注体系**", "**口径优先级**", "🔴 **对客纪律**"]
LINE_LIMIT = 2500

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)\s]*)?\)")
SEC_REF = re.compile(r"§(\d+(?:\.\d+)*)")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def strip_fences(text):
    """把围栏代码块内的行替换成空串，保留行号对齐。

    🔴 首版没做这步，把代码块里的 YAML/shell 注释（`# and_rule 表示…`、`# 通过 GET 方法获取`）
    误判成 H1，报了 5 条假 P1。**启发式必须匹配语法结构，不能只看行首字符。**
    """
    out, in_fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def count_cells(line: str) -> int:
    """数一行里**未转义**的 `|` 个数。

    🔴 首版直接 `line.count("|")`，把已正确转义的 `\\|`（SLS 查询语法
    `cluster_id:{id} \\| SELECT …`）与正则/枚举里的裸 `|` 一起算进去，报了 6 条假 P2。
    """
    return len(re.findall(r"(?<!\\)\|", line))


def headings_of(text):
    """返回该文件里所有可被 §x.y 引用的编号集合（跳过代码块）。"""
    nums = set()
    for line in strip_fences(text):
        m = HEADING.match(line)
        if not m:
            continue
        h = m.group(2)
        for n in SEC_REF.findall(h):
            nums.add(n)
            # 标题写 `§3.9` 时，也允许被引作 `3.9`；写 `### 3.5.4` 时同理
        m2 = re.match(r"^(\d+(?:\.\d+)*)\s", h)
        if m2:
            nums.add(m2.group(1))
    return nums


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--out", default=str(KB / "tests/ai-gateway-lint-2026-09-21.md"))
    a = ap.parse_args()

    texts = {fn: (KB / "knowledge" / fn).read_text(encoding="utf-8") for fn in FAMILY}
    # 结构类检查一律用「去代码块」视图，避免把代码注释误判成标题
    bare = {fn: strip_fences(t) for fn, t in texts.items()}
    heads = {fn: headings_of(t) for fn, t in texts.items()}

    p0, p1, p2 = [], [], []

    # L1 链接目标存在性
    for fn, t in texts.items():
        for ln, line in enumerate(t.splitlines(), 1):
            for m in MD_LINK.finditer(line):
                tgt = m.group(1)
                if tgt.startswith(("http://", "https://", "mailto:")):
                    continue
                p = (KB / "knowledge" / tgt) if not tgt.startswith(("/", "tests/", "raw/", "scripts/")) else (KB / tgt)
                if not p.exists():
                    p0.append(("L1 断链", "%s:%d" % (fn, ln), "链接目标不存在：%s" % tgt))

    # L2 跨文件 §N 引用可解析
    for fn, t in texts.items():
        for ln, line in enumerate(t.splitlines(), 1):
            for m in re.finditer(r"\[([^\]]*§\d+(?:\.\d+)*[^\]]*)\]\(([^)#\s]+\.md)\)", line):
                label, tgt = m.group(1), m.group(2)
                if tgt not in heads:
                    p1.append(("L2 目标文件不在家族内", "%s:%d" % (fn, ln), "%s → %s" % (label, tgt)))
                    continue
                for n in SEC_REF.findall(label):
                    if n not in heads[tgt]:
                        p1.append(("L2 章节号不存在", "%s:%d" % (fn, ln),
                                   "引用 %s 指向 %s，但该文件无 §%s 标题" % (label, tgt, n)))

    # L3 装配残留（用去代码块视图）
    for fn, blines in bare.items():
        for ln, line in enumerate(blines, 1):
            if line.strip().startswith("<!-- W"):
                p1.append(("L3 partial 注释残留", "%s:%d" % (fn, ln), line.strip()[:90]))
            if re.match(r"^#\s+W\d partial", line):
                p1.append(("L3 partial 标题残留", "%s:%d" % (fn, ln), line.strip()[:90]))
            if re.search(r"\bTODO\b|待补占位|占位符文本|XXX_PLACEHOLDER", line):
                p1.append(("L3 TODO/占位符", "%s:%d" % (fn, ln), line.strip()[:90]))
        h1 = [i for i, l in enumerate(blines, 1) if l.startswith("# ")]
        if len(h1) != 1:
            p1.append(("L3 H1 数量异常", fn, "H1 出现在第 %s 行（应恰好 1 个）" % h1))

    # L4 页眉六要素 + 代号对照表指针
    for fn, t in texts.items():
        head = "\n".join(t.splitlines()[:16])
        miss = [k for k in HEADER_REQUIRED if k not in head]
        if miss:
            p1.append(("L4 页眉缺要素", fn, "缺 %s" % ", ".join(miss)))
        if fn != FAMILY[0] and "分工代号" not in head:
            p2.append(("L4 缺 W 代号对照表指针", fn, "子页页眉宜指向主页 §0.6 对照表"))
        if fn == FAMILY[0] and "W1`~`W7" not in t and "W1`~`W7" not in t.replace("`", ""):
            p1.append(("L4 主页缺 W 代号对照表", fn, "正文有 W1~W7 引用但主页无对照表"))

    # L5 行数阈值
    for fn, t in texts.items():
        n = len(t.splitlines())
        if n > LINE_LIMIT:
            p0.append(("L5 超拆分阈值", fn, "%d 行 > %d（AGENTS.md 规定必须拆分）" % (n, LINE_LIMIT)))

    # L6 章节号唯一性（家族级，用去代码块视图）
    owner = defaultdict(list)
    for fn, blines in bare.items():
        for line in blines:
            m = HEADING.match(line)
            if m and len(m.group(1)) == 2:
                for n in re.findall(r"§(\d+)(?=\s|$|）)", m.group(2)):
                    owner[int(n)].append((fn, m.group(2)[:40]))
    for n, locs in sorted(owner.items()):
        if len(locs) > 1:
            p1.append(("L6 顶级章节号重复", "§%d" % n, "出现在 %s" % "、".join("%s(%s)" % x for x in locs)))
    missing = [n for n in range(1, 16) if n not in owner]
    if missing:
        p1.append(("L6 章节号缺失", "家族", "§1~§15 中缺 %s" % missing))

    # L7 表格完整性（用去代码块视图，代码块内的示例表不参与判定）
    for fn, blines in bare.items():
        lines = blines
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith("|") and i + 1 < len(lines) \
                    and re.match(r"^\s*\|[-: |]+\|\s*$", lines[i + 1]):
                ncol = count_cells(lines[i])
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    if count_cells(lines[j]) != ncol:
                        p2.append(("L7 表格列数不一致", "%s:%d" % (fn, j + 1),
                                   "该行 %d 个未转义 `|`，表头 %d 个（可能是拼接断表，或单元格内含**未转义**的裸 `|`）"
                                   % (count_cells(lines[j]), ncol)))
                    j += 1
                i = j
            else:
                i += 1

    # L8 W 代号残留计数
    wcount = {}
    for fn, t in texts.items():
        c = len(re.findall(r"\bW[1-7]\b", t))
        if c:
            wcount[fn] = c

    L = []
    L.append("# AI 网关专题页家族 · 装配质量与引用完整性 lint")
    L.append("")
    L.append("生成：2026-09-21 ｜ 生成器：`scripts/lint-aigw-pages.py`（机械可判定项，确定性、可复算）")
    L.append("")
    L.append("## 为什么这一半是脚本而不是 agent")
    L.append("")
    L.append("首派的一致性评审 agent（R2）任务书含 5 个维度，跑 **59 分钟 / 120 次工具调用后死于模型服务错误、产物为 0**。")
    L.append("其中 **B 交叉引用完整性** 与 **D 装配质量** 是纯机械可判定的，交给 agent 既慢又会死；")
    L.append("改由本脚本承担（L1~L8）。**语义维度**（同一事实跨页口径一致性 / 与既有页面冲突 / SA 可用性）")
    L.append("才需要 agent，且必须**窄范围单派**。")
    L.append("")
    L.append("## 结果")
    L.append("")
    L.append("| 级别 | 条数 | 含义 |")
    L.append("|---|---|---|")
    L.append("| 🔴 P0 | %d | 必须修：断链、超拆分阈值 |" % len(p0))
    L.append("| 🟠 P1 | %d | 应修：章节号引用不存在、装配残留、页眉缺要素、章节号重复/缺失 |" % len(p1))
    L.append("| 🟡 P2 | %d | 观感与可维护性：表格列数不一致、缺代号指针 |" % len(p2))
    L.append("")
    for tag, items in (("🔴 P0", p0), ("🟠 P1", p1), ("🟡 P2", p2)):
        if not items:
            continue
        L.append("### %s（%d 条）" % (tag, len(items)))
        L.append("")
        L.append("| 检查项 | 位置 | 说明 |")
        L.append("|---|---|---|")
        for k, loc, msg in items[:120]:
            L.append("| %s | `%s` | %s |" % (k, loc, msg.replace("|", "\\|")[:200]))
        if len(items) > 120:
            L.append("| … | … | 另有 %d 条同类，从略 |" % (len(items) - 120))
        L.append("")
    L.append("## L8 `W1`~`W7` 分工代号残留计数")
    L.append("")
    L.append("代号是蒸馏批次的内部分工标识，**主页 §0.6 已提供对照表解析器**（与 `aliyun-agentcore.md` 里")
    L.append("约 26 处 `RULINGS §x` 引用的既有约定同形），故保留不算缺陷，但计数留档以便后续决定是否改写：")
    L.append("")
    L.append("| 文件 | `W1`~`W7` 出现次数 |")
    L.append("|---|---|")
    for fn, c in sorted(wcount.items(), key=lambda kv: -kv[1]):
        L.append("| `%s` | %d |" % (fn, c))
    L.append("| **合计** | **%d** |" % sum(wcount.values()))
    L.append("")
    L.append("## 家族规模（实测）")
    L.append("")
    L.append("| 文件 | 行数 | 表数 |")
    L.append("|---|---|---|")
    tl = tt = 0
    for fn in FAMILY:
        t = texts[fn]
        n = len(t.splitlines())
        tb = len(re.findall(r"(?m)^\|[-: |]+\|$", t))
        tl += n
        tt += tb
        L.append("| `%s` | %d | %d |" % (fn, n, tb))
    L.append("| **合计** | **%d** | **%d** |" % (tl, tt))
    L.append("")

    Path(a.out).write_text("\n".join(L), encoding="utf-8")
    print("L1~L8 lint：🔴 P0=%d ｜ 🟠 P1=%d ｜ 🟡 P2=%d ｜ W 代号残留=%d 处"
          % (len(p0), len(p1), len(p2), sum(wcount.values())))
    for tag, items in (("P0", p0), ("P1", p1)):
        for k, loc, msg in items[:12]:
            print("  %s %s @ %s — %s" % (tag, k, loc, msg[:110]))
        if len(items) > 12:
            print("  %s …另有 %d 条，见报告" % (tag, len(items) - 12))
    print("报告 → %s" % a.out)
    bad = len(p0) + (len(p1) if a.strict else 0)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
