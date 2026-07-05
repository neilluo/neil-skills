#!/usr/bin/env python3
"""
LLM Wiki KB 回归测试脚本

用法：python3 scripts/regression-template.py [--threshold 0.85] [--out tests/report.md]

逻辑：
1. 读取 tests/regression-cases.yaml
2. 遍历 wiki/ 全部 .md 文件
3. 每个用例检查关键词子串匹配（大小写不敏感）
4. 命中率 >= threshold 为 PASS
5. 输出 Markdown 报告
"""

import argparse
import datetime as dt
import os
import sys
from pathlib import Path

try:
    import yaml
    def load_yaml(text):
        return yaml.safe_load(text)
except ImportError:
    # Minimal YAML parser fallback
    def load_yaml(text):
        """Fallback: parse simple YAML structure"""
        import json
        # Try JSON first (some YAML is valid JSON)
        try:
            return json.loads(text)
        except:
            pass
        # Minimal parser for our specific format
        data = {"threshold": 0.85, "cases": []}
        current_case = None
        current_list = None
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if line.startswith('threshold:'):
                data["threshold"] = float(line.split(':', 1)[1].strip())
            elif line.startswith('cases:'):
                pass
            elif stripped.startswith('- id:'):
                current_case = {"id": stripped.split(':', 1)[1].strip(), "keywords": []}
                data["cases"].append(current_case)
                current_list = None
            elif stripped.startswith('title:') and current_case:
                current_case["title"] = stripped.split(':', 1)[1].strip().strip('"')
            elif stripped.startswith('keywords:'):
                current_list = "keywords"
            elif current_list == "keywords" and stripped.startswith('- '):
                current_case["keywords"].append(stripped[2:].strip().strip('"'))
            elif stripped.startswith('mode:') and current_case:
                current_case["mode"] = stripped.split(':', 1)[1].strip()
        return data


def load_corpus(wiki_dir: Path) -> str:
    """Load all markdown files in wiki/ as one text blob"""
    texts = []
    for md_file in sorted(wiki_dir.rglob("*.md")):
        texts.append(md_file.read_text(encoding="utf-8"))
    return "\n".join(texts)


def check_hit(corpus: str, keyword: str) -> bool:
    """Case-insensitive substring match"""
    return keyword.lower() in corpus.lower()


def run(kb_dir: Path, threshold: float, output: Path) -> int:
    """Run regression tests and generate report"""
    cases_path = kb_dir / "tests" / "regression-cases.yaml"
    if not cases_path.exists():
        print(f"ERROR: {cases_path} not found")
        return 1

    wiki_dir = kb_dir / "wiki"
    if not wiki_dir.exists():
        print(f"ERROR: {wiki_dir} not found")
        return 1

    # Load test cases
    spec = load_yaml(cases_path.read_text(encoding="utf-8"))
    cases = spec.get("cases", [])
    threshold = spec.get("threshold", threshold)

    # Load corpus
    corpus = load_corpus(wiki_dir)
    corpus_size = len(corpus)

    # Run tests
    results = []
    for case in cases:
        keywords = case.get("keywords", [])
        hits = 0
        details = []
        for kw in keywords:
            ok = check_hit(corpus, kw)
            details.append((kw, ok))
            if ok:
                hits += 1
        rate = hits / len(keywords) if keywords else 0
        status = "PASS" if rate >= threshold else "FAIL"
        results.append({
            "id": case.get("id", "?"),
            "title": case.get("title", ""),
            "mode": case.get("mode", "?"),
            "rate": rate,
            "hits": hits,
            "total": len(keywords),
            "status": status,
            "details": details,
        })

    # Calculate overall
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    total_cases = len(results)
    overall_rate = sum(r["rate"] for r in results) / total_cases if total_cases else 0

    # Generate report
    now = dt.datetime.now()
    lines = [
        f"# 回归测试报告 — {now:%Y-%m-%d %H:%M}",
        "",
        f"> 阈值: {threshold:.0%} | 用例数: {total_cases} | 语料: {corpus_size:,} 字符",
        "",
        "## 总览",
        "",
        f"- **整体命中率**: {overall_rate:.1%}",
        f"- **PASS**: {pass_count}/{total_cases}",
        f"- **FAIL**: {total_cases - pass_count}/{total_cases}",
        "",
        "## 用例矩阵",
        "",
        "| ID | 模式 | 标题 | 命中/总数 | 命中率 | 状态 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        emoji = "✅" if r["status"] == "PASS" else "❌"
        lines.append(f"| {r['id']} | {r['mode']} | {r['title']} | {r['hits']}/{r['total']} | {r['rate']:.0%} | {emoji} {r['status']} |")
    
    lines.extend(["", "## 详细明细", ""])
    for r in results:
        lines.append(f"### {r['id']} — {r['title']} [{r['status']}]")
        lines.append("")
        lines.append("| 关键词 | 命中 |")
        lines.append("| --- | --- |")
        for kw, ok in r["details"]:
            lines.append(f"| `{kw}` | {'✅' if ok else '❌'} |")
        lines.append("")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    # Console summary
    print(f"\n=== 回归测试完成 ===")
    print(f"整体命中率: {overall_rate:.1%}")
    print(f"PASS: {pass_count}/{total_cases}  FAIL: {total_cases - pass_count}/{total_cases}")
    print(f"报告: {output}")
    for r in results:
        emoji = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {emoji} {r['id']} [{r['mode']}] {r['title']} — {r['hits']}/{r['total']} ({r['rate']:.0%})")

    return 0 if pass_count == total_cases else 1


def main():
    parser = argparse.ArgumentParser(description="LLM Wiki KB Regression Test")
    parser.add_argument("--kb-dir", default=str(Path(__file__).resolve().parent.parent),
                       help="Knowledge base root directory")
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir)
    if args.out:
        output = Path(args.out)
    else:
        date = dt.datetime.now().strftime("%Y-%m-%d")
        output = kb_dir / "tests" / f"regression-{date}.md"

    sys.exit(run(kb_dir, args.threshold, output))


if __name__ == "__main__":
    main()
