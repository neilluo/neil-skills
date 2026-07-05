#!/bin/bash
# =============================================================================
# Qoder Products 知识库自动同步脚本
# 
# 功能：从官网 https://docs.qoder.com 拉取 Cloud Agents + QoderWake 文档并更新本地知识库
# 建议配置 crontab 每晚 22:00 执行：
#   0 22 * * * /path/to/sync-docs.sh >> /path/to/sync-docs.log 2>&1
# =============================================================================

set -euo pipefail

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KB_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMP_DIR=$(mktemp -d)
UPDATED=0

# ─── Cloud Agents ───
CA_DIR="${KB_ROOT}/raw/cloud-agents"
CA_BASE_URL="https://docs.qoder.com/zh/cloud-agents"
declare -A CA_DOCS=(
  ["overview.md"]="overview"
  ["quickstart.md"]="quickstart"
  ["define-agent.md"]="define-agent"
  ["environments.md"]="environments"
  ["sessions.md"]="sessions"
  ["tools.md"]="tools"
  ["events-stream.md"]="events-stream"
  ["skills.md"]="skills"
  ["memory-stores.md"]="memory-stores"
  ["managed-agents.md"]="managed-agents"
  ["permission-policies.md"]="permission-policies"
  ["files.md"]="files"
  ["outcomes.md"]="outcomes"
  ["vaults.md"]="vaults"
  ["container-reference.md"]="container-reference"
)

# ─── QoderWake ───
QW_DIR="${KB_ROOT}/raw/qoderwake"
QW_BASE_URL="https://docs.qoder.com/zh/qoderwake"
declare -A QW_DOCS=(
  ["overview.md"]="overview"
  ["installation.md"]="installation"
  ["create-waker.md"]="create-waker"
  ["conversation-tasks.md"]="conversation-tasks"
  ["automated-tasks.md"]="automated-tasks"
  ["group-tasks.md"]="group-tasks"
  ["examples.md"]="examples"
  ["manage-wakers.md"]="manage-wakers"
)

echo "=========================================="
echo "知识库同步开始: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# 清理函数
cleanup() {
  rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# 通用同步函数
sync_product() {
  local product_name="$1"
  local target_dir="$2"
  local base_url="$3"
  shift 3
  # remaining args are key=value pairs
  
  echo ""
  echo "── 同步产品: ${product_name} ──"
  mkdir -p "$target_dir"
}

# 对每个文档执行检查和更新（Cloud Agents）
echo ""
echo "── 同步产品: Cloud Agents ──"
mkdir -p "$CA_DIR"
for local_file in "${!CA_DOCS[@]}"; do
  remote_path="${CA_DOCS[$local_file]}"
  remote_url="${CA_BASE_URL}/${remote_path}"
  local_path="${CA_DIR}/${local_file}"
  temp_file="${TEMP_DIR}/ca_${local_file}"

  echo ""
  echo "检查: ${local_file} (${remote_url})"

  # 下载远程内容
  if ! curl -sL --fail "${remote_url}" -o "$temp_file" 2>/dev/null; then
    echo "  ⚠️  下载失败，跳过: ${remote_url}"
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
    echo "  🔄 内容有更新，正在同步..."
    cp "$temp_file" "$local_path"
    UPDATED=$((UPDATED + 1))
  else
    echo "  ✅ 无变化"
  fi
done

# 对每个文档执行检查和更新（QoderWake）
echo ""
echo "── 同步产品: QoderWake ──"
mkdir -p "$QW_DIR"
for local_file in "${!QW_DOCS[@]}"; do
  remote_path="${QW_DOCS[$local_file]}"
  remote_url="${QW_BASE_URL}/${remote_path}"
  local_path="${QW_DIR}/${local_file}"
  temp_file="${TEMP_DIR}/qw_${local_file}"

  echo ""
  echo "检查: ${local_file} (${remote_url})"

  if ! curl -sL --fail "${remote_url}" -o "$temp_file" 2>/dev/null; then
    echo "  ⚠️  下载失败，跳过: ${remote_url}"
    continue
  fi

  if [ ! -f "$local_path" ]; then
    echo "  🆕 新文件，直接写入"
    cp "$temp_file" "$local_path"
    UPDATED=$((UPDATED + 1))
    continue
  fi

  local_sha=$(shasum -a 256 "$local_path" | cut -d' ' -f1)
  remote_sha=$(shasum -a 256 "$temp_file" | cut -d' ' -f1)

  if [ "$local_sha" != "$remote_sha" ]; then
    echo "  🔄 内容有更新，正在同步..."
    cp "$temp_file" "$local_path"
    UPDATED=$((UPDATED + 1))
  else
    echo "  ✅ 无变化"
  fi
done

echo ""
echo "=========================================="
echo "同步完成: $(date '+%Y-%m-%d %H:%M:%S')"
echo "更新文件数: ${UPDATED}"
echo "=========================================="

# 如果有更新，自动触发 ingest
if [ $UPDATED -gt 0 ]; then
  echo ""
  echo "检测到 ${UPDATED} 个文件更新，触发 ingest..."
  "$SCRIPT_DIR/ingest.sh"
fi
