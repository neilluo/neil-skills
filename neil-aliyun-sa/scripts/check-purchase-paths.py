#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neil-aliyun-sa 采购路径核验清单哨兵脚本

用法:
    python3 scripts/check-purchase-paths.py [--out tests/purchase-paths-YYYY-MM-DD.md]

背景:
    2026-08-05 三次连续踩坑（ClickHouse 企业版无规格页 / Hologres 网关最低2个 /
    ADB MySQL 企业版最低3节点步长3）暴露 SA 出报价对比时"只看计费文档拿单价、未验证
    购买页有没有对应'选规格'入口"的系统性流程漏洞。

    本哨兵脚本在 CI/回归时执行，确保 references/pricing-verification-checklist.md 的
    § 3.1 速查表 v2 覆盖所有主要 DB/大数据/AI/存储产品家族，且每行都含 4 个必备字段：
      1) commodityCode 或专属购买域名（购买路径）
      2) 最低起步约束（节点/规格/网关/CU）
      3) 规格页可用性（✅/❌/⚠️）
      4) 采购流程兼容性（可锁定/需审批/走不通）

    覆盖度不足 → 退出码 = 1（CI 阻断）。
"""

from __future__ import annotations
import argparse
import datetime as dt
import re
import sys
from pathlib import Path


# ==== 期望覆盖的产品家族清单（若新增家族在此处追加）====
# 每个 entry = (家族名, [该家族必须命中的关键词列表])
EXPECTED_FAMILIES = [
    # 数据库家族
    ("PolarDB MySQL 集群版", ["PolarDB MySQL 集群版", "polardb-buy.aliyun.com"]),
    ("PolarDB MySQL Serverless", ["PolarDB MySQL Serverless", "不支持转包月"]),
    ("PolarDB-X", ["PolarDB-X", "drds_polarxpre_public_cn"]),
    ("RDS MySQL 高可用版", ["RDS MySQL 高可用版"]),
    ("RDS MySQL Serverless", ["RDS MySQL Serverless"]),
    ("RDS PostgreSQL Serverless", ["RDS PostgreSQL Serverless"]),
    ("RDS SQL Server Serverless (已下线)", ["RDS SQL Server Serverless", "已停售"]),
    # OLAP / 数仓家族
    ("ADB MySQL 企业版", ["ADB MySQL 企业版", "节点 ≥ 3，步长 3"]),
    ("ADB PostgreSQL 弹性模式", ["ADB PostgreSQL", "GreenplumPre"]),
    ("MaxCompute", ["MaxCompute", "odpsplus"]),
    ("Hologres 计算组", ["Hologres 计算组", "网关 ≥ 2"]),
    ("ClickHouse 企业版", ["ClickHouse 企业版", "0.49987"]),
    ("ClickHouse 社区兼容版", ["ClickHouse 社区兼容版", "clickhouse_pre_public_cn"]),
    # 大数据家族
    ("Lindorm 宽表", ["Lindorm 宽表引擎", "hitsdb_lindormnextpre_public_cn"]),
    ("Lindorm Serverless (无法新购)", ["Lindorm Serverless", "无法新购"]),
    ("EMR on ECS", ["EMR on ECS", "Master ≥ 3"]),
    ("EMR Serverless Spark", ["EMR Serverless Spark"]),
    ("EMR Serverless StarRocks", ["EMR Serverless StarRocks"]),
    ("Flink 全托管", ["Flink 全托管", "管控资源固定 2 CU"]),
    ("Flink 作业级 Serverless (不存在)", ["作业级 Serverless"]),
    ("DataWorks Serverless 资源组", ["DataWorks Serverless 资源组"]),
    # Cache / AI / 存储家族
    ("Tair 内存型", ["Tair 内存型", "kvstore_pretair_public_cn"]),
    ("Tair Serverless", ["Tair Serverless"]),
    ("百炼 Token Plan 个人版", ["百炼 Token Plan 个人版"]),
    ("百炼 Token Plan 团队版", ["百炼 Token Plan 团队版"]),
    ("PAI-EAS 独享", ["PAI-EAS 独享", "learn_EasDedicatedPrepay_public_cn"]),
    ("PAI-EAS Serverless (仅 SDWebUI)", ["PAI-EAS Serverless", "SDWebUI"]),
    ("PAI-DSW", ["PAI-DSW"]),
    ("OSS 资源包", ["OSS", "存储包"]),
    # 向量检索 / RAG / 文档解析家族（2026-08-08 新增，§ 3.1b）
    ("百炼知识库标准版", ["百炼知识库标准版", "0.03 元/知识库·小时"]),
    ("百炼知识库旗舰版", ["百炼知识库旗舰版", "0.2 元/RCU·小时"]),
    ("DashVector (仅按量+不可降配)", ["DashVector", "降配，暂不支持"]),
    ("向量检索服务 Milvus 版", ["向量检索服务 Milvus 版", "milvus.console.aliyun.com"]),
    ("阿里云 Elasticsearch 集群版", ["阿里云 Elasticsearch 集群版", "elasticsearchpre"]),
    ("ES Serverless (最低门槛费)", ["ES Serverless 版", "elasticsearch_serverless_spn_cn", "最低门槛费"]),
    ("OpenSearch-LLM 智能问答版", ["OpenSearch-LLM 智能问答版", "opensearch_pre"]),
    ("OpenSearch 向量检索版", ["OpenSearch 向量检索版", "opensearch_ha3post_public_cn"]),
    ("文档智能 DocMind", ["文档智能 DocMind", "docmind_general_dp_cn"]),
]

# ==== 结构性关键词（新增章节/维度时必须出现）====
STRUCTURAL_KEYWORDS = [
    "全域速查表 v2",
    "§ 3.1b",
    "红色预警",
    "匿名核验的边界",
    "登录复验",
    "C11 版本可售性时效",
    "C12 Serverless 语义粒度",
    "C13 Serverless 最低门槛费",
    "C14 计费口径的计量基数",
]

# ==== 4 字段完整性关键词（每个字段类别的代表词，至少一条必须出现）====
FIELD_KEYWORDS = {
    "购买路径 (commodityCode)": ["commodityCode", "common-buy.aliyun.com"],
    "最低起步约束": ["最低起步", "≥", "起步", "步长"],
    "规格页可用性": ["有独立规格页", "无独立规格页", "Serverless 无", "按 CU 池", "按 RCU 池"],
    "采购流程兼容性": ["包月-可锁定预算", "采购走不通-仅按量", "按量-需专项审批", "可锁定", "走不通"],
}


def read_checklist(root: Path) -> str:
    path = root / "references" / "pricing-verification-checklist.md"
    if not path.exists():
        print(f"[FATAL] Checklist not found: {path}", file=sys.stderr)
        sys.exit(2)
    return path.read_text(encoding="utf-8")


def check_families(text: str) -> list[tuple[str, list[str], list[str]]]:
    """Returns list of (family, missing_keywords, matched_keywords)."""
    results = []
    for family, kws in EXPECTED_FAMILIES:
        missing = []
        matched = []
        for kw in kws:
            if kw.lower() in text.lower():
                matched.append(kw)
            else:
                missing.append(kw)
        results.append((family, missing, matched))
    return results


def check_structural(text: str) -> list[tuple[str, bool]]:
    return [(kw, kw.lower() in text.lower()) for kw in STRUCTURAL_KEYWORDS]


def check_fields(text: str) -> dict[str, tuple[int, int]]:
    """Returns dict: field_category -> (hits, total_kws)."""
    out = {}
    for cat, kws in FIELD_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw.lower() in text.lower())
        out[cat] = (hits, len(kws))
    return out


def render_report(results, structural, fields) -> tuple[str, bool]:
    today = dt.date.today().isoformat()
    lines = [f"# Purchase Paths Sentinel — {today}", ""]

    # Family coverage
    lines.append("## 一、产品家族覆盖度")
    lines.append("")
    lines.append("| 家族 | 状态 | 命中关键词 | 缺失关键词 |")
    lines.append("|------|------|-----------|-----------|")
    total_families = len(results)
    passed_families = 0
    for family, missing, matched in results:
        status = "✅" if not missing else "❌"
        if not missing:
            passed_families += 1
        lines.append(
            f"| {family} | {status} | {', '.join(matched) if matched else '—'} | {', '.join(missing) if missing else '—'} |"
        )
    coverage_pct = 100.0 * passed_families / total_families if total_families else 0
    lines.append("")
    lines.append(f"**覆盖度**: {passed_families}/{total_families} = {coverage_pct:.1f}%")
    lines.append("")

    # Structural
    lines.append("## 二、清单结构完整性")
    lines.append("")
    lines.append("| 结构关键词 | 状态 |")
    lines.append("|-----------|------|")
    struct_pass = 0
    for kw, ok in structural:
        struct_pass += 1 if ok else 0
        lines.append(f"| {kw} | {'✅' if ok else '❌'} |")
    lines.append("")
    lines.append(f"**通过**: {struct_pass}/{len(structural)}")
    lines.append("")

    # 4 fields
    lines.append("## 三、4 字段完整性抽样")
    lines.append("")
    lines.append("| 字段类别 | 关键词命中数 |")
    lines.append("|---------|-------------|")
    field_pass = 0
    for cat, (hits, total) in fields.items():
        ok = hits >= 1
        field_pass += 1 if ok else 0
        lines.append(f"| {cat} | {hits}/{total} {'✅' if ok else '❌'} |")
    lines.append("")
    lines.append(f"**通过**: {field_pass}/{len(fields)}")
    lines.append("")

    # Verdict
    fatal = passed_families < total_families or struct_pass < len(structural) or field_pass < len(fields)
    verdict = "❌ FAIL — 需修复上表标 ❌ 项" if fatal else "✅ PASS — 采购路径核验清单结构完整"
    lines.append("---")
    lines.append("")
    lines.append(f"## 结论: {verdict}")
    lines.append("")
    lines.append("**执行时机**: 每次修改 `references/pricing-verification-checklist.md` 或新增 DB/大数据/AI 产品家族后必跑；每月 Lint 时抽跑一次")
    lines.append("")
    return "\n".join(lines), fatal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    text = read_checklist(root)

    results = check_families(text)
    structural = check_structural(text)
    fields = check_fields(text)

    report, fatal = render_report(results, structural, fields)

    if args.out:
        out_path = Path(args.out)
    else:
        out_path = root / "tests" / f"purchase-paths-{dt.date.today().isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"\n[report saved] {out_path}")
    sys.exit(1 if fatal else 0)


if __name__ == "__main__":
    main()
