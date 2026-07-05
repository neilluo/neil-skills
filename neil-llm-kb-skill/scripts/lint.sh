#!/bin/bash
# LLM Wiki Knowledge Base — Lint Script
# Usage: ./lint.sh [--auto-fix] [--score]
#
# 对知识库执行 6 维健康检查，输出 P0/P1/P2 分级报告。
# --auto-fix：自动修复可安全处理的问题（格式错误、孤立页 index 补充）
# --score：同时输出 KB Health Score 量化评分

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 如果 kb 目录不在脚本的父目录，尝试在当前目录找
if [ ! -d "$KB_DIR/wiki" ]; then
  KB_DIR="$(pwd)/kb"
fi

if [ ! -d "$KB_DIR/wiki" ]; then
  echo "ERROR: 未找到 wiki/ 目录。请在知识库根目录或其 scripts/ 子目录运行。"
  exit 1
fi

MODE="${1:-standard}"
EXTRA_INSTRUCTIONS=""

case "$MODE" in
  --auto-fix)
    EXTRA_INSTRUCTIONS="
## 自动修复规则
以下问题可以自动修复（无需人工确认）：
- Wikilink 格式错误（含 .md 后缀）→ 自动移除后缀
- 孤立页 → 在 index.md 对应分区补充引用
- 过时标记 → 自动添加 [stale-YYYY] banner

以下问题需报告但不自动修复：
- P0 矛盾 → 需要判断哪个版本正确
- 缺页 → 需要决定是创建还是删除引用
- 数据空白 → 需要决定是否值得补充"
    ;;
  --score)
    EXTRA_INSTRUCTIONS="
## 额外输出：KB Health Score
在 Lint 报告末尾，追加 KB Health Score 量化评分：
- 结构完整性（/25）
- 内容质量（/30）
- 连通性（/20）
- 新鲜度（/15）
- 覆盖率（/10）
- 总分（/100）+ 等级（A+/A/B/C/D）
- 按 ROI 排序的改进建议 Top 3"
    ;;
  --auto-fix-score|--score-auto-fix)
    EXTRA_INSTRUCTIONS="
## 自动修复规则
以下问题可以自动修复（无需人工确认）：
- Wikilink 格式错误（含 .md 后缀）→ 自动移除后缀
- 孤立页 → 在 index.md 对应分区补充引用
- 过时标记 → 自动添加 [stale-YYYY] banner

## 额外输出：KB Health Score
在 Lint 报告末尾，追加 KB Health Score 量化评分（5 维度 + 总分 + 等级）。"
    ;;
esac

PROMPT="你是知识库维护者。对 kb/ 目录下的 wiki 知识库执行全面 Lint 健康检查。

## 6 维检查
1. **矛盾检测**（P0）— 同一事实跨页不一致
2. **过时检测**（P1）— updated 字段 > 6 月
3. **孤立页检测**（P2）— 无入站 [[引用]] 的页面
4. **缺页检测**（P1）— 被 [[link]] 引用但文件不存在
5. **[[wikilink]] 完整性**（P1）— 格式错误或指向不存在
6. **数据空白**（P2）— raw/ 未处理的源 + 覆盖不足领域

## 输出格式
按 P0 → P1 → P2 优先级排列，每条含：
- 问题编号（[P0-001]）
- 问题描述
- 涉及文件
- 修复建议

## 操作后记录
在 wiki/log.md 追加一行：
| YYYY-MM-DD | 🔍 Lint | 发现 X 问题（P0:a/P1:b/P2:c），自动修复 Y 项 |
$EXTRA_INSTRUCTIONS"

echo "=== 知识库 Lint 健康检查 ==="
echo "模式：$MODE"
echo ""
echo "调用 qodercli 执行..."
cd "$KB_DIR"
qodercli --dangerously-skip-permissions -p "$PROMPT"

echo ""
echo "=== Lint 完成 ==="
