#!/bin/bash
# LLM Wiki Knowledge Base — Ingest Script
# Usage:
#   首次全量：./ingest.sh --full
#   增量更新：./ingest.sh            (自动检测 raw/ 变化)
#   Lint检查：./ingest.sh --lint

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 如果 kb 目录不在脚本的父目录，尝试在当前目录找
if [ ! -d "$KB_DIR/wiki" ]; then
  KB_DIR="$(pwd)/kb"
fi

RAW_DIR="$KB_DIR/raw"
WIKI_DIR="$KB_DIR/wiki"
SCHEMA="$KB_DIR/SCHEMA.md"
LOG_FILE="$WIKI_DIR/log.md"
HASH_DIR="$KB_DIR/.hashes"

mkdir -p "$HASH_DIR"
mkdir -p "$WIKI_DIR/entities" "$WIKI_DIR/concepts" "$WIKI_DIR/guides" "$WIKI_DIR/comparisons"

MODE="${1:-incremental}"

# SHA256 check function
check_changed() {
  local file="$1"
  local hash_file="$HASH_DIR/$(basename "$file").sha256"
  local current_hash
  current_hash=$(shasum -a 256 "$file" | cut -d' ' -f1)
  
  if [ -f "$hash_file" ]; then
    local stored_hash
    stored_hash=$(cat "$hash_file")
    if [ "$current_hash" = "$stored_hash" ]; then
      return 1  # Not changed
    fi
  fi
  
  echo "$current_hash" > "$hash_file"
  return 0  # Changed
}

case "$MODE" in
  --full)
    echo "=== 全量 Ingest 模式 ==="
    CHANGED_FILES=$(find "$RAW_DIR" -name "*.md" | sort)
    PROMPT="你是知识库维护者。请按照 SCHEMA.md 规则，对 raw/ 下所有文件执行全量 ingest。

具体任务：
1. 先在 wiki/inbox.md 登记所有来源（写入优先）
2. 在 wiki/log.md 追加 ⏳ 进行中
3. 读取每个 raw 文件，执行 2-Step CoT（先分析，再生成）
4. 为关键实体/概念创建 wiki 页面（四段落格式）
5. 建立 [[wikilink]] 交叉引用
6. 更新 wiki/index.md
7. inbox 状态改 done，log 标记完成

重要：每页 ≤15 页更新预算。遵循 SCHEMA.md 页面格式。"
    ;;
  --lint)
    echo "=== Lint 检查模式 ==="
    PROMPT="你是知识库维护者。请对 wiki/ 执行 6 维 Lint 健康检查：
1. 矛盾检测（P0）
2. 过时检测（P1）
3. 孤立页检测（P2）
4. 缺页检测（P1）
5. [[wikilink]] 完整性（P1）
6. 数据空白（P2）

输出：按 P0/P1/P2 分级报告，每条含问题描述+涉及文件+修复建议。
在 wiki/log.md 记录本次 Lint。"
    ;;
  *)
    echo "=== 增量 Ingest 模式 ==="
    CHANGED_FILES=""
    for file in "$RAW_DIR"/*.md; do
      [ -f "$file" ] || continue
      if check_changed "$file"; then
        CHANGED_FILES="$CHANGED_FILES $file"
      fi
    done
    
    if [ -z "$CHANGED_FILES" ]; then
      echo "未检测到 raw/ 变化（SHA256 校验通过），跳过 ingest。"
      exit 0
    fi
    
    echo "检测到变化文件："
    echo "$CHANGED_FILES" | tr ' ' '\n' | sed "s|$RAW_DIR/||g"
    
    PROMPT="你是知识库维护者。raw/ 中以下文件有更新（SHA256 检测到变化）：
$(echo "$CHANGED_FILES" | tr ' ' '\n' | sed "s|$RAW_DIR/||g")

按 SCHEMA.md 规则执行增量 ingest：
1. 写入优先：inbox.md 登记 + log.md 追加 ⏳
2. 2-Step CoT：先分析变化内容，再更新 wiki 页面
3. 预算控制：最多更新 15 页
4. 维护 [[wikilink]] 交叉引用
5. 更新 index.md + inbox done + log 完成"
    ;;
esac

echo ""
echo "调用 qodercli 执行..."
cd "$KB_DIR"
qodercli --dangerously-skip-permissions -p "$PROMPT"

echo ""
echo "=== 操作完成 ==="
