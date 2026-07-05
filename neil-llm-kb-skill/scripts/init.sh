#!/bin/bash
# LLM Wiki Knowledge Base — Init Script
# Usage: ./init.sh [--project-name NAME] [--purpose "PURPOSE"]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PWD}"
PROJECT_NAME="${1:-$(basename "$PROJECT_DIR")}"
KB_DIR="$PROJECT_DIR/kb"

echo "=========================================="
echo "LLM Wiki KB Init: $PROJECT_NAME"
echo "=========================================="

# Phase 1: Detect project type
detect_project_type() {
  if [ -f "package.json" ] || [ -f "pom.xml" ] || [ -f "go.mod" ] || \
     [ -f "Cargo.toml" ] || [ -f "pyproject.toml" ] || [ -f "build.gradle" ]; then
    echo "codebase"
  elif find . -maxdepth 2 -name "*.md" -o -name "*.pdf" -o -name "*.docx" | head -5 | grep -q .; then
    if [ -d "src" ] || [ -d "lib" ]; then
      echo "hybrid"
    else
      echo "document"
    fi
  else
    echo "unknown"
  fi
}

# Phase 2: Assess scale
assess_scale() {
  local file_count
  file_count=$(find . -type f \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" \
    -not -path "./target/*" \
    -not -path "./build/*" \
    -not -path "./kb/*" | wc -l | tr -d ' ')
  
  if [ "$file_count" -lt 50 ]; then
    echo "small"
  elif [ "$file_count" -lt 200 ]; then
    echo "medium"
  elif [ "$file_count" -lt 500 ]; then
    echo "large"
  else
    echo "xlarge"
  fi
}

PROJECT_TYPE=$(detect_project_type)
SCALE_TIER=$(assess_scale)

echo ""
echo "项目类型: $PROJECT_TYPE"
echo "规模等级: $SCALE_TIER"
echo ""

# Phase 3: Create directory structure
echo "创建 kb/ 目录结构..."
mkdir -p "$KB_DIR/raw"
mkdir -p "$KB_DIR/wiki/entities"
mkdir -p "$KB_DIR/wiki/concepts"
mkdir -p "$KB_DIR/wiki/guides"
mkdir -p "$KB_DIR/wiki/comparisons"
mkdir -p "$KB_DIR/references"

# Phase 4: Generate initial files
cat > "$KB_DIR/wiki/index.md" << 'EOF'
# Wiki 索引

## 实体

<!-- 由 Ingest 操作自动填充 -->

## 概念

<!-- 由 Ingest 操作自动填充 -->

## 指南

<!-- 由 Ingest 操作自动填充 -->

## 对比

<!-- 由 Ingest 操作自动填充 -->
EOF

cat > "$KB_DIR/wiki/inbox.md" << 'EOF'
# Inbox — 来源状态机

> 写入优先红线：收到任何资料的第一个动作就是在这里登记 pending。
> 格式：[status] date | type | title | raw-path | wiki-pages

## Pending（待处理）

## Processing（处理中）

## Done（已完成）
EOF

cat > "$KB_DIR/wiki/log.md" << EOF
# 操作日志

## [$(date '+%Y-%m-%d')] init | 知识库初始化

- 项目类型：$PROJECT_TYPE
- 规模等级：$SCALE_TIER
- 创建目录结构：kb/raw + kb/wiki/{entities,concepts,guides,comparisons} + kb/references
- 生成文件：index.md, inbox.md, log.md
EOF

echo ""
echo "=========================================="
echo "初始化完成!"
echo "=========================================="
echo "目录结构："
find "$KB_DIR" -type f | sed "s|$PROJECT_DIR/||" | sort
echo ""
echo "下一步："
echo "  1. 生成 SCHEMA.md（使用 qodercli 填充模板）"
echo "  2. 生成 AGENTS.md（使用 qodercli 填充模板）"
if [ "$SCALE_TIER" != "small" ]; then
  echo "  3. 推荐配置 QMD MCP（规模等级: $SCALE_TIER）"
  echo '     {"mcpServers":{"qmd":{"command":"qmd","args":["mcp"]}}}'
fi
echo "=========================================="
