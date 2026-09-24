#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 raw 快照的「服务端静默截断」嫌疑页。

🔴 第五种失效模式（2026-09-21 AI 网关实测新发现）：
`.md` 通道对某些页面返回 **HTTP 200 + Content-Type: markdown + Content-Length 自洽**
但正文在列表中途被切断的 body。实测 `agent-api-observable`：body_bytes=978、
content-length=978、两次抓取 SHA256 完全一致 → **截断发生在服务端，不是抓取器**。
前三重校验（CT / 非 HTML / 非 TOC）全部通过，第四重（Document Not Found 桩）也通过。

判据（结构性，非字节阈值）：正文最后一个非空行是**悬挂结构标记**——
孤立的列表符（`*` `-` `+`）、未闭合的 HTML 标签、或以连接词/冒号结尾。
"""
import re
import sys
from pathlib import Path

DANGLING = re.compile(r"^(?:[*+\-]|\d+[.)]|<\w+[^>]*>|[:：、，,（(]|>\s*)$")
# 以这些结尾高度可疑（句子未写完）
SUSPICIOUS_TAIL = re.compile(
    r"(?:[:：、，,]|包括|如下|以下|其中|以及|和|与|或|的|是|在|用于|支持|可以|请|如果|当|则)$")
UNCLOSED_TAGS = ("<table", "<tbody", "<tr", "<td", "<thead", "<ul", "<ol", "<li", "<div")


def body_of(p: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore").splitlines()[10:])


# 已判为 TOC 容器的页（纯链接目录，短是应然的）与已知「短但完整」的页不参与判定。
# 判据要匹配语法结构，不能拿字节阈值当截断证据（本项目已有教训）。
BENIGN_TAIL = re.compile(r"^(?:<br\s*/?>|\s|﻿)+$")


def check(p: Path, min_bytes: int = 0):
    raw = body_of(p)
    # 剥掉尾部良性的 <br /> 与空白（`.md` 通道的常见渲染残留，非截断证据）
    lines_all = raw.splitlines()
    while lines_all and (BENIGN_TAIL.match(lines_all[-1]) or not lines_all[-1].strip()):
        lines_all.pop()
    b = "\n".join(lines_all).rstrip()
    if not b:
        return None
    lines = [ln for ln in b.splitlines() if ln.strip()]
    last = lines[-1].strip()
    reasons = []
    if DANGLING.match(last):
        reasons.append("🔴 末行是悬挂结构标记 %r —— 列表项内容缺失" % last[:40])
    elif SUSPICIOUS_TAIL.search(last):
        reasons.append("🔴 末行以未完结词尾结束 %r" % last[-24:])
    # HTML 标签闭合平衡
    for tag in UNCLOSED_TAGS:
        o = len(re.findall(re.escape(tag) + r"[\s>]", b))
        c = b.count("</%s>" % tag[1:])
        if o != c:
            reasons.append("🔴 %s 开 %d ≠ 闭 %d" % (tag, o, c))
    if not reasons and min_bytes and len(b.encode()) < min_bytes:
        reasons.append("⚪ 正文 <%dB（信息量可能不足以支撑对客答复，非截断证据）" % min_bytes)
    return (len(b.encode()), last[:60], reasons) if reasons else None


def main():
    # 2026-09-24 双仓合并：原硬编码独立仓库绝对路径，改为按脚本自身定位知识库根
    kb = Path(__file__).resolve().parent.parent
    d = Path(sys.argv[1] if len(sys.argv) > 1 else kb / "raw/aliyun-docs/ai-gateway")
    manifest = Path(sys.argv[2] if len(sys.argv) > 2
                    else kb / "tests/ai-gateway-fetch-manifest-2026-09-21.tsv")
    verdicts = {}
    if manifest.exists():
        for ln in manifest.read_text(encoding="utf-8").splitlines()[1:]:
            f = ln.split("\t")
            verdicts[f[0]] = f[7]

    hard, soft = [], []
    files = sorted(d.glob("*.md"))
    for p in files:
        # TOC 容器页短是应然的，只做硬截断判定，不做信息量判定
        is_toc = verdicts.get(p.stem) == "TOC"
        r = check(p, min_bytes=0 if is_toc else 400)
        if not r:
            continue
        (hard if any(x.startswith("🔴") for x in r[2]) else soft).append((p.stem, r))

    print("扫描 %d 个快照" % len(files))
    print("\n=== 🔴 硬截断嫌疑（结构性证据，必须处理）：%d 个 ===\n" % len(hard))
    for stem, (nb, last, reasons) in hard:
        print("· %-58s %6dB" % (stem, nb))
        print("    末行: %s" % last)
        for x in reasons:
            print("    %s" % x)
    print("\n=== ⚪ 软提示（正文过短，信息量不足但非截断）：%d 个 ===\n" % len(soft))
    for stem, (nb, last, reasons) in soft:
        print("· %-58s %6dB" % (stem, nb))
    if not hard:
        print("（无）")



if __name__ == "__main__":
    main()
