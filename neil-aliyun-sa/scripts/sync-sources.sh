#!/bin/bash
# =============================================================================
# 阿里云 SA 知识库文档自动同步脚本
#
# 功能：从 help.aliyun.com 拉取关键产品/框架文档，SHA256 增量检测后更新 raw/
# 建议配置 crontab 每晚 23:00 执行：
#   0 23 * * * /path/to/sync-sources.sh >> /path/to/sync-sources.log 2>&1
# =============================================================================

set -euo pipefail

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RAW_DIR="${SKILL_DIR}/raw"
TEMP_DIR=$(mktemp -d)
UPDATED=0
SKIPPED=0

# ─────────────────────────────────────────────────────────────────────────────
# 可配置来源 URL 列表
# 格式：[本地文件名]="远程URL"
# 按需增删条目，新增产品/框架文档在此追加即可
# ─────────────────────────────────────────────────────────────────────────────
declare -A DOCS=(
  # ── 框架方法论 ──
  ["framework/caf-overview.html"]="https://help.aliyun.com/zh/caf/"
  ["framework/well-architected.html"]="https://help.aliyun.com/zh/product/2362200.html"
  ["framework/network-wad.html"]="https://help.aliyun.com/zh/cloud-network-well-architected-design/"
  ["framework/acsg-security.html"]="https://help.aliyun.com/zh/acsg/"

  # ── 计算 ──
  ["compute/ecs-overview.html"]="https://help.aliyun.com/zh/ecs/"
  ["compute/ack-overview.html"]="https://help.aliyun.com/zh/ack/"
  ["compute/acs-overview.html"]="https://help.aliyun.com/zh/acs/"
  ["compute/fc-overview.html"]="https://help.aliyun.com/zh/fc/"
  ["compute/sae-overview.html"]="https://help.aliyun.com/zh/sae/"

  # ── 存储 ──
  ["storage/oss-overview.html"]="https://help.aliyun.com/zh/oss/"
  ["storage/nas-overview.html"]="https://help.aliyun.com/zh/nas/"

  # ── 数据库 ──
  ["database/rds-overview.html"]="https://help.aliyun.com/zh/rds/"
  ["database/polardb-overview.html"]="https://help.aliyun.com/zh/polardb/"
  ["database/lindorm-overview.html"]="https://help.aliyun.com/zh/lindorm/"
  ["database/analyticdb-overview.html"]="https://help.aliyun.com/zh/analyticdb-for-mysql/"
  ["database/hologres-overview.html"]="https://help.aliyun.com/zh/hologres/"

  # ── 网络 ──
  ["network/vpc-overview.html"]="https://help.aliyun.com/zh/vpc/"
  ["network/cen-overview.html"]="https://help.aliyun.com/zh/cen/"
  ["network/ga-overview.html"]="https://help.aliyun.com/zh/ga/"
  ["network/alb-overview.html"]="https://help.aliyun.com/zh/slb/"

  # ── AI ──
  ["ai/bailian-overview.html"]="https://help.aliyun.com/zh/model-studio/"
  ["ai/pai-overview.html"]="https://help.aliyun.com/zh/pai/"

  # ── 安全 ──
  ["security/waf-overview.html"]="https://help.aliyun.com/zh/waf/"
  ["security/ddos-overview.html"]="https://help.aliyun.com/zh/anti-ddos/"
  ["security/cloud-firewall-overview.html"]="https://help.aliyun.com/zh/cloud-firewall/"

  # ── 中间件 ──
  ["middleware/mse-overview.html"]="https://help.aliyun.com/zh/mse/"
  ["middleware/rocketmq-overview.html"]="https://help.aliyun.com/zh/apsaramq-for-rocketmq/"
  ["middleware/eventbridge-overview.html"]="https://help.aliyun.com/zh/eventbridge/"
)

echo "=========================================="
echo "阿里云文档同步开始: $(date '+%Y-%m-%d %H:%M:%S')"
echo "来源数量: ${#DOCS[@]}"
echo "=========================================="

# 清理函数
cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# 确保 raw/ 子目录存在
for local_file in "${!DOCS[@]}"; do
  sub_dir=$(dirname "$local_file")
  mkdir -p "${RAW_DIR}/${sub_dir}"
done

# 对每个文档执行 SHA256 增量检测和更新
for local_file in "${!DOCS[@]}"; do
  remote_url="${DOCS[$local_file]}"
  local_path="${RAW_DIR}/${local_file}"
  temp_file="${TEMP_DIR}/${local_file}"

  # 确保临时目录结构存在
  mkdir -p "$(dirname "$temp_file")"

  echo ""
  echo "检查: ${local_file}"
  echo "  URL: ${remote_url}"

  # 下载远程内容（5s 超时，重试 2 次）
  if ! curl -sL --fail --max-time 30 --retry 2 \
       -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
       "${remote_url}" -o "$temp_file" 2>/dev/null; then
    echo "  ⚠️  下载失败，跳过"
    continue
  fi

  # 检查下载内容是否为空
  if [ ! -s "$temp_file" ]; then
    echo "  ⚠️  下载内容为空，跳过"
    continue
  fi

  # 如果本地文件不存在，直接写入
  if [ ! -f "$local_path" ]; then
    echo "  🆕 新文件，直接写入"
    cp "$temp_file" "$local_path"
    UPDATED=$((UPDATED + 1))
    continue
  fi

  # 计算 SHA256 对比
  local_sha=$(shasum -a 256 "$local_path" | cut -d' ' -f1)
  remote_sha=$(shasum -a 256 "$temp_file" | cut -d' ' -f1)

  if [ "$local_sha" != "$remote_sha" ]; then
    echo "  🔄 内容有更新（SHA256 不同），正在同步..."
    echo "     旧: ${local_sha:0:12}..."
    echo "     新: ${remote_sha:0:12}..."
    cp "$temp_file" "$local_path"
    UPDATED=$((UPDATED + 1))
  else
    echo "  ✅ 内容未变更，跳过"
    SKIPPED=$((SKIPPED + 1))
  fi
done

echo ""
echo "=========================================="
echo "同步完成: $(date '+%Y-%m-%d %H:%M:%S')"
echo "更新文件数: ${UPDATED}"
echo "未变更跳过: ${SKIPPED}"
echo "=========================================="

# 如果有更新，提示用户执行 ingest
if [ $UPDATED -gt 0 ]; then
  echo ""
  echo "┌──────────────────────────────────────────────────┐"
  echo "│ 检测到 ${UPDATED} 个文件有更新！                          │"
  echo "│ 建议执行 ingest 将新内容蒸馏入 knowledge 层：    │"
  echo "│                                                  │"
  echo "│   对 neil-aliyun-sa 说：「学习一下 raw/ 更新」   │"
  echo "│                                                  │"
  echo "└──────────────────────────────────────────────────┘"
else
  echo ""
  echo "所有文档均为最新，无需 ingest。"
fi
