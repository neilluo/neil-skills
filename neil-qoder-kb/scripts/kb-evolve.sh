#!/bin/bash
# kb-evolve.sh — 知识库自我进化脚本
# 由 macOS launchd 每天 09:30 自动触发
# 功能：同步文档 → 检测变更 → LLM Ingest → Lint 检查
#
# 调度方式：launchd plist（见 scripts/com.neil.kb-evolve.plist）
# 执行引擎：qodercli --permission-mode bypass_permissions

set -euo pipefail

# === 配置 ===
KB_DIR="/Users/neil/Desktop/neilskills/neil-qoder-kb"
QODERCLI="$HOME/.local/bin/qodercli"
LOG_DIR="$KB_DIR/logs"
LOG_FILE="$LOG_DIR/evolve-$(date +%Y%m%d).log"
MAX_TURNS=80

# === 初始化 ===
mkdir -p "$LOG_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "════════════════════════════════════════"
echo "🧬 知识库自我进化 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"

# === Step 1: 同步官方文档 ===
echo ""
echo "📡 Step 1: 同步官方文档..."
cd "$KB_DIR"

if [ -f "scripts/sync-docs.sh" ]; then
    bash scripts/sync-docs.sh 2>&1 || echo "⚠️ sync-docs.sh 执行异常（非致命，继续）"
else
    echo "⚠️ sync-docs.sh 不存在，跳过同步步骤"
fi

# === Step 2: 检测变更 ===
echo ""
echo "🔍 Step 2: 检测 raw/ 变更..."
CHANGES=$(git diff --name-only -- raw/ 2>/dev/null || echo "")
UNTRACKED=$(git ls-files --others --exclude-standard -- raw/ 2>/dev/null || echo "")

if [ -z "$CHANGES" ] && [ -z "$UNTRACKED" ]; then
    echo "✅ raw/ 无变更，执行周期性 Lint 检查..."
    
    # 无变更时执行 Lint
    "$QODERCLI" \
        -w "$KB_DIR" \
        -p "执行知识库 Lint 健康检查。检查：1) wiki 页面间是否有矛盾 2) 是否有孤立页 3) 交叉引用完整性 4) 是否有断链。输出检查结果摘要，如有 P0/P1 问题则修复。遵循 SCHEMA.md 规则。" \
        --permission-mode bypass_permissions \
        --max-turns 30 \
        --output-format text \
        2>&1 || echo "⚠️ Lint 执行异常"
    
    echo ""
    echo "✅ 周期性 Lint 完成"
else
    echo "📋 检测到变更："
    echo "$CHANGES"
    echo "$UNTRACKED"
    
    # === Step 3: LLM Ingest ===
    echo ""
    echo "🧠 Step 3: 执行 LLM Ingest..."
    
    INGEST_PROMPT="你是知识库维护者。检测到 raw/ 有以下变更：
$CHANGES
$UNTRACKED

请按 SCHEMA.md 的 Ingest 流程执行：
1. 在 inbox.md 登记 pending + log.md 追加 ⏳（写入优先）
2. 读取变化的 raw 文件，理解语义变化
3. 更新 wiki/ 中受影响的页面（或创建新页面）
4. 维护 [[wikilink]] 交叉引用
5. 更新 index.md
6. 在 inbox.md 标记 done + log.md 标记 ✅

严格遵循 SCHEMA.md 中的页面格式规范和质量标准。"

    "$QODERCLI" \
        -w "$KB_DIR" \
        -p "$INGEST_PROMPT" \
        --permission-mode bypass_permissions \
        --max-turns "$MAX_TURNS" \
        --output-format text \
        2>&1 || echo "⚠️ Ingest 执行异常"
    
    echo ""
    echo "✅ Ingest 完成"
fi

# === Step 4: 自我深化（每周一额外执行） ===
DOW=$(date +%u)  # 1=Monday
if [ "$DOW" -eq 1 ]; then
    echo ""
    echo "🔬 Step 4: 周一深度自我进化..."
    
    "$QODERCLI" \
        -w "$KB_DIR" \
        -p "执行知识库深度自我进化（每周一）。任务：
1. 扫描 ~/.qoderwake/ 和 ~/.qoder/ 的配置文件，检查是否有版本更新带来的新配置项
2. 对比现有 wiki 页面，识别可补充的深度知识
3. 如果发现新知识点，按 SCHEMA.md 创建新页面或更新现有页面
4. 执行完整 Lint 检查并修复所有问题
5. 在 log.md 记录本次自我进化的发现

重点关注：feature-config.json 变化、新增的安全规则、plugin 更新、数据库 schema 变化。" \
        --permission-mode bypass_permissions \
        --max-turns "$MAX_TURNS" \
        --output-format text \
        2>&1 || echo "⚠️ 深度进化执行异常"
    
    echo ""
    echo "✅ 深度自我进化完成"
fi

# === 清理旧日志（保留 30 天） ===
find "$LOG_DIR" -name "evolve-*.log" -mtime +30 -delete 2>/dev/null || true

echo ""
echo "════════════════════════════════════════"
echo "🏁 进化完成 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════"
