#!/bin/bash
# LLM Wiki Knowledge Base — Query Script
# Usage: ./query.sh "你的问题"
#
# 基于 wiki 知识库回答问题，按 4 层回退检索。

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

QUESTION="${1:-}"

if [ -z "$QUESTION" ]; then
  echo "用法：./query.sh \"你的问题\""
  echo ""
  echo "示例："
  echo "  ./query.sh \"Redis 的默认超时是多少？\""
  echo "  ./query.sh \"认证模块的数据流是怎样的？\""
  exit 1
fi

PROMPT="你是知识库维护者。基于 kb/ 目录下的 wiki 知识库回答以下问题。

## 问题
$QUESTION

## 检索规则（4 层回退）
1. 先读 wiki/index.md 定位相关页面
2. 读取 wiki 页面综合回答
3. 不足则回退 raw/ 查找原始材料
4. 仍不足则使用 WebSearch 补充

## 回答格式要求
- 回答完整且有据可查
- 标注来源：[primary]/[derived]/[inferred] + 具体文件路径
- 如果知识库中无相关信息，明确说明

## 回写判定
回答后评估是否需要回写到 wiki：
- 跨 3+ 页综合 → 回写
- 发现纠错 → 回写
- 新话题 → 回写
- 一次性查询 → 不回写

如需回写，执行回写门禁检查后再写入。"

echo "=== 知识库 Query ==="
echo "问题：$QUESTION"
echo ""
echo "调用 qodercli 检索..."
cd "$KB_DIR"
qodercli --dangerously-skip-permissions -p "$PROMPT"

echo ""
echo "=== Query 完成 ==="
