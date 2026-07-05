# Inbox — 来源状态机

> **Karpathy LLM Wiki 角色**：本文件是 Raw Sources 层的索引与状态机。
> **写入优先红线**：收到任何更新的第一个动作就是在这里登记 pending。
>
> 格式：`[status] date | type | title | raw-file | wiki-pages`
> 状态机：pending → processing → done

## Pending（待处理）

<!-- 新来源在此登记 -->

## Processing（处理中）

<!-- 正在蒸馏的来源移到这里 -->

## Done（已完成）

- [done] 2026-06-30 | reverse-engineering | 安装产物逆向分析——知识库深度扩展（13 新页） | 本地 ~/.qoderwake/ + ~/.qoder/ | wiki/qoderwake/concepts/waker-tool-guard + waker-hook-lifecycle + waker-data-model + qmind-knowledge + waker-trigger-plugins + waker-identity-system + waker-plugin-system + waker-observability + wiki/qoderwake/entities/waker-daemon + wiki/qodercli/concepts/cli-cron-system + cli-goal-system + cli-task-tracker + cli-canvas-system

- [done] 2026-06-28 | verified-by-api | QoderCLI 斜杠命令实测验证（文档 16 命令，实测 47 命令，Claude Code 94%覆盖） | raw/qodercli/commands.md | wiki/qodercli/concepts/cli-command-system.md

- [done] 2026-06-28 | official-docs | Qoder Desktop Hooks 导入（docs.qoder.com/zh/extensions/hooks） | raw/qoderdesktop/hooks.md | wiki/qoderdesktop/concepts/desktop-hook-system.md

- [done] 2026-06-28 | official-docs | Qoder Desktop 全量导入（docs.qoder.com/zh 主站 6个页面 → 6 raw + 5 wiki） | raw/qoderdesktop/*.md | wiki/qoderdesktop/entities/* + wiki/qoderdesktop/concepts/* + wiki/qoderdesktop/guides/*

- [done] 2026-06-28 | official-docs | QoderWork 全量导入（docs.qoder.com/zh/qoderwork 7个页面 → 7 raw + 8 wiki） | raw/qoderwork/*.md | wiki/qoderwork/entities/* + wiki/qoderwork/concepts/* + wiki/qoderwork/guides/* + wiki/qoderwork/comparisons/*

- [done] 2026-06-28 | verified-by-api | QoderCLI Hooks 实测修正（官网文档仅 4 事件，实测 30 事件 + 5 Handler） | raw/qodercli/hooks.md | wiki/qodercli/concepts/cli-hook-system.md

- [done] 2026-06-28 | official-docs | QoderCLI 全量导入（16个 Web 页面 → 12个 raw + 14个 wiki） | raw/qodercli/*.md | wiki/qodercli/entities/* + wiki/qodercli/concepts/* + wiki/qodercli/guides/* + wiki/qodercli/comparisons/*

- [done] 2026-06-28 | official-docs | QoderWake 全量导入（8个 raw 文件） | raw/qoderwake/*.md | wiki/qoderwake/entities/* + wiki/qoderwake/concepts/* + wiki/qoderwake/guides/* + wiki/qoderwake/comparisons/*
- [done] 2026-06-21 | official-docs | 初始全量导入（15个raw文件） | raw/cloud-agents/*.md | wiki/cloud-agents/entities/* + wiki/cloud-agents/concepts/* + wiki/cloud-agents/guides/* + wiki/cloud-agents/comparisons/*
