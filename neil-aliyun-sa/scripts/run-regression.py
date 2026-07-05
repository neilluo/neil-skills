#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neil-aliyun-sa 知识库自动化回归测试

用法:
    python3 scripts/run-regression.py [--threshold 0.85] [--out tests/regression-YYYY-MM-DD.md]

逻辑:
    1. 读 tests/regression-cases.yaml 用例库
    2. 遍历 knowledge/ 与 references/ 全部 .md 文件
    3. 每个用例:
       - 对每个 keyword 在全文里 grep 是否命中(大小写不敏感)
       - 命中率 = 命中数 / keyword 总数
       - >=threshold 视为 PASS
    4. 输出 Markdown 报告到 tests/regression-<日期>.md
"""

from __future__ import annotations
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

# 简易 YAML 解析(避免引入 PyYAML 依赖)
def parse_yaml(text: str) -> dict:
    import yaml  # 优先使用 PyYAML
    return yaml.safe_load(text)


def load_cases(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return parse_yaml(text)
    except ImportError:
        sys.stderr.write("[warn] PyYAML 不可用,改用最小解析器\n")
        return _mini_yaml(text)


def _mini_yaml(text: str) -> dict:
    """Fallback YAML 解析(只覆盖本用例库的格式)"""
    data = {"version": None, "threshold": 0.85, "files": {"knowledge": [], "references": []}, "cases": []}
    cur_section = None
    cur_case = None
    cur_list_for = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("version:"):
            data["version"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("threshold:"):
            data["threshold"] = float(line.split(":", 1)[1].strip())
        elif line.startswith("files:"):
            cur_section = "files"
        elif line.startswith("  knowledge:") and cur_section == "files":
            cur_list_for = ("files", "knowledge")
        elif line.startswith("  references:") and cur_section == "files":
            cur_list_for = ("files", "references")
        elif line.startswith("cases:"):
            cur_section = "cases"
            cur_list_for = None
        elif cur_section == "files" and line.startswith("    -"):
            val = line.split("-", 1)[1].strip()
            data["files"][cur_list_for[1]].append(val)
        elif cur_section == "cases" and re.match(r"^\s*-\s*id:", line):
            cur_case = {"keywords": []}
            data["cases"].append(cur_case)
            cur_case["id"] = line.split(":", 1)[1].strip()
            cur_list_for = None
        elif cur_section == "cases" and re.match(r"^\s+keywords:", line):
            cur_list_for = ("case", "keywords")
        elif cur_list_for == ("case", "keywords") and re.match(r"^\s+-\s*", line):
            val = line.split("-", 1)[1].strip().strip('"')
            cur_case["keywords"].append(val)
        elif cur_section == "cases" and cur_case is not None and re.match(r"^\s+\w+:", line):
            k, v = line.strip().split(":", 1)
            cur_case[k.strip()] = v.strip().strip('"')
            cur_list_for = None
    return data


def load_corpus(root: Path, files: list[str]) -> dict[str, str]:
    corpus = {}
    for rel in files:
        p = root / rel
        if p.exists():
            corpus[rel] = p.read_text(encoding="utf-8")
        else:
            corpus[rel] = ""
    return corpus


def hit(text_blob: str, keyword: str) -> bool:
    # 关键词命中:大小写不敏感子串匹配
    return keyword.lower() in text_blob.lower()


def run(root: Path, threshold: float, out: Path) -> int:
    cases_path = root / "tests" / "regression-cases.yaml"
    spec = load_cases(cases_path)

    files = spec["files"]["knowledge"] + spec["files"]["references"]
    corpus = load_corpus(root, files)
    blob = "\n".join(corpus.values())

    results = []
    for case in spec["cases"]:
        keywords = case["keywords"]
        per_kw = []
        hits = 0
        for kw in keywords:
            ok = hit(blob, kw)
            per_kw.append((kw, ok))
            if ok:
                hits += 1
        rate = hits / len(keywords) if keywords else 0
        status = "PASS" if rate >= threshold else "FAIL"
        results.append({
            "id": case["id"],
            "mode": case.get("mode", "?"),
            "title": case.get("title", ""),
            "rate": rate,
            "hits": hits,
            "total": len(keywords),
            "status": status,
            "details": per_kw,
        })

    pass_n = sum(1 for r in results if r["status"] == "PASS")
    total = len(results)
    overall = sum(r["rate"] for r in results) / total if total else 0

    # 写报告
    now = dt.datetime.now()
    lines = []
    lines.append(f"# 自动化回归报告 — {now:%Y-%m-%d %H:%M %Z}")
    lines.append("")
    lines.append(f"> **测试器**：scripts/run-regression.py")
    lines.append(f"> **用例库**：tests/regression-cases.yaml (v{spec.get('version','?')})")
    lines.append(f"> **覆盖文件**：{len(corpus)} 个 markdown / 共 {sum(len(c) for c in corpus.values())} 字符")
    lines.append(f"> **PASS 阈值**：命中率 ≥ {threshold:.0%}")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(f"- **整体命中率**：{overall:.1%}")
    lines.append(f"- **PASS 数**：{pass_n}/{total}")
    lines.append(f"- **FAIL 数**：{total - pass_n}/{total}")
    lines.append("")
    lines.append("## 用例结果矩阵")
    lines.append("")
    lines.append("| ID | 模式 | 场景 | 命中 / 总数 | 命中率 | 状态 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for r in results:
        emoji = "✅" if r["status"] == "PASS" else "❌"
        lines.append(f"| {r['id']} | {r['mode']} | {r['title']} | {r['hits']}/{r['total']} | {r['rate']:.0%} | {emoji} {r['status']} |")
    lines.append("")
    lines.append("## 详细命中明细")
    lines.append("")
    for r in results:
        lines.append(f"### {r['id']} — {r['title']}  [{r['status']}]")
        lines.append("")
        lines.append("| 关键词 | 命中 |")
        lines.append("| --- | --- |")
        for kw, ok in r["details"]:
            lines.append(f"| `{kw}` | {'✅' if ok else '❌'} |")
        lines.append("")
    lines.append("## 文件覆盖")
    lines.append("")
    lines.append("| 文件 | 字符数 |")
    lines.append("| --- | --- |")
    for f, c in corpus.items():
        lines.append(f"| `{f}` | {len(c):,} |")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")

    # 控制台摘要
    print(f"\n=== 回归测试完成 ===")
    print(f"整体命中率: {overall:.1%}")
    print(f"PASS: {pass_n}/{total}  FAIL: {total - pass_n}/{total}")
    print(f"报告已写入: {out}")
    for r in results:
        emoji = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {emoji} {r['id']} [{r['mode']}] {r['title']} — {r['hits']}/{r['total']} ({r['rate']:.0%})")

    return 0 if pass_n == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--threshold", type=float, default=0.85)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    if args.out:
        out = Path(args.out)
        if not out.is_absolute():
            out = root / out
    else:
        date = dt.datetime.now().strftime("%Y-%m-%d")
        out = root / "tests" / f"regression-{date}.md"

    sys.exit(run(root, args.threshold, out))


if __name__ == "__main__":
    main()
