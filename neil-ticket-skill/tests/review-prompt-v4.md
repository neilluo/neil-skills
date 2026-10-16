你是资深工程师，对 Qoder skill「neil-ticket-skill」做第四轮验收评审（只读：禁止改任何文件、禁止执行 dws）。根目录 /Users/neil/Desktop/neilcodebase/neil-skills/neil-ticket-skill。该 skill 刚完成：单文件→九模块包 scripts/neil_ticket/（config/transport/parse/gate/render/collect/publish/cli/__init__，shim scripts/ticket.py）、四轮多模型评审修复（报告 tests/review-2026-10-14-*.md）、规范沉淀 AGENTS.md（规则 A-P）。逐项验收并给证据（file:line 或命令输出）：
1 重复度：跨模块归一化重复块占比是否 <5%（可跑 outputs/analyze-metrics.py 复核，只读运行允许）。
2 死代码：AST 级未调用函数/未用 import/未读配置键是否为零。
3 命令风格：dws 出口是否唯一（transport.run_dws）、重试是否常量表集中、require 是否仅形状校验。
4 架构分层：九模块依赖方向是否无循环无越界；扩展契约（加客户/加事件类型/加输出目标/换传输）各自改动面是否如 AGENTS.md 规则 P 所述。
5 内聚：是否仍存在「改一个功能因内聚不足而动多文件」；规则 L 的同批清单是否合理。
6 冗长方法：是否仍有 >40 行函数或「10 行能写完却写很长」的函数。
7 规范沉淀：AGENTS.md 规则 A-P 与代码现状是否一致（逐条抽查≥8 条，列不一致项）；有无应沉淀未沉淀的发现。
另列残留缺陷表（P0/P1/P2，含 file:line）。输出 markdown，≤1000 字。
