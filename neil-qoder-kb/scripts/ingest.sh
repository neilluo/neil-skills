#!/bin/bash
# =============================================================================
# Qoder Cloud Agent 知识库 Ingest 脚本
#
# 功能：调用 qodercli 读取 raw/ 中的变化，按照 SCHEMA.md 规则更新 wiki/
# 用法：
#   首次初始化：./ingest.sh --full
#   增量更新：  ./ingest.sh              （自动检测 raw/ 变化）
#   Lint 检查：./ingest.sh --lint
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RAW_DIR="$KB_DIR/raw"
WIKI_DIR="$KB_DIR/wiki"
SCHEMA="$KB_DIR/SCHEMA.md"
LOG_FILE="$WIKI_DIR/log.md"

# 确保 wiki 目录存在
mkdir -p "$WIKI_DIR/entities" "$WIKI_DIR/concepts" "$WIKI_DIR/guides" "$WIKI_DIR/comparisons"

# 参数解析
MODE="${1:-incremental}"

case "$MODE" in
  --full)
    echo "=== 全量 Ingest 模式 ==="
    RAW_FILES=$(find "$RAW_DIR" -name "*.md" | sort)
    PROMPT="你是知识库维护者。请按照 SCHEMA.md 的规则，对 raw/ 目录下的所有文件执行全量 ingest。

具体任务：
1. 读取 raw/ 下所有 markdown 文件
2. 为每个核心实体（Agent, Environment, Session, Event, Skill, Memory Store, Vault, Deployment, File）创建 wiki/entities/ 下的实体页
3. 为跨实体的通用机制创建 wiki/concepts/ 下的概念页（乐观并发控制、Session状态机、SSE事件流、权限模型、多Agent线程、容器沙箱）
4. 为操作型内容创建 wiki/guides/ 下的指南页（快速开始、排障指南、生产环境清单）
5. 创建 wiki/comparisons/ 下的对比页（工具vs技能、记忆vs文件）
6. 创建 wiki/index.md（全量索引）
7. 创建 wiki/log.md（首次 ingest 记录）

重要规则：
- 严格遵循 SCHEMA.md 中的页面格式规范
- 使用 [[page-name]] 格式做交叉引用
- wiki 是提炼和综合，不是 raw 的复制粘贴
- 每个页面标注来源 raw 文件
- 面向'回答用户问题'来组织内容"
    ;;
  --lint)
    echo "=== Lint 检查模式 ==="
    PROMPT="你是知识库维护者。请对 wiki/ 执行 Lint 健康检查，按照 SCHEMA.md 中'操作：Lint'部分的检查项逐条执行：
1. 检查页面间是否有矛盾说明
2. 检查 raw/ 已更新但 wiki 未同步的内容
3. 检查没有入站引用的孤立页
4. 检查内容中提到但未创建的概念
5. 检查所有 [[link]] 是否指向存在的页面

输出格式：按严重程度分级列出问题，给出修复建议。"
    ;;
  *)
    echo "=== 增量 Ingest 模式 ==="
    # 检测 raw/ 中的变化（通过 git 或时间戳）
    CHANGED_FILES=$(find "$RAW_DIR" -name "*.md" -newer "$LOG_FILE" 2>/dev/null || find "$RAW_DIR" -name "*.md")
    if [ -z "$CHANGED_FILES" ]; then
      echo "未检测到 raw/ 变化，跳过 ingest。"
      exit 0
    fi
    echo "检测到变化文件："
    echo "$CHANGED_FILES"
    PROMPT="你是知识库维护者。raw/ 目录中以下文件有更新：
$(echo "$CHANGED_FILES" | sed "s|$RAW_DIR/||g")

请按照 SCHEMA.md 的规则执行增量 ingest：
1. 读取变化的 raw 文件，理解变化内容
2. 更新 wiki/ 中受影响的页面（实体页、概念页、指南页）
3. 添加或更新交叉引用
4. 如果有新概念/新实体，创建新页面
5. 更新 wiki/index.md
6. 在 wiki/log.md 追加本次操作记录"
    ;;
esac

echo ""
echo "调用 qodercli 执行 ingest..."
echo ""

# 调用 qodercli 执行 ingest
cd "$KB_DIR"
qodercli --dangerously-skip-permissions -p "$PROMPT"

echo ""
echo "=== Ingest 完成 ==="
