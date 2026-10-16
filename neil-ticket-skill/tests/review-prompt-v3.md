你是资深工程师，对 Qoder skill「neil-ticket-skill」做第三轮专项评审（只读：禁止改任何文件、禁止执行 dws）。根目录 /Users/neil/Desktop/neilcodebase/neil-skills/neil-ticket-skill。历史评审与修复见 tests/review-2026-10-14-glm53.md、review-2026-10-14-ultimate-a.md、review-2026-10-14-ultimate-b.md、review-2026-10-14-kimi-k3.md 与 reference.md「开放项与取舍记录」；本轮不重复历史发现，只专项查七项：
1 重复度：scripts/ticket.py 内（及与 tests 之间）重复代码块，量化「重复行/总行」，目标 <5%，列每处重复块位置与合并方案。
2 死代码：定义但从未被调用的函数/变量/import/分支（给 AST 级或 grep 级证据）。
3 命令风格：dws 调用风格一致性（argv 构造、重试退避、错误信封处理、输出取值），列不一致处。
4 架构分层：采集/解析/门禁/渲染/发布/配置 六层边界是否清晰；新增「客户 / 卡片事件类型 / 输出目标」三种扩展各自要动哪几层。
5 内聚：列「改一个功能需改多文件」的清单，判定是内聚缺陷还是合理分层。
6 冗长方法：top5「本可 10 行却写了更多」的函数，给重构思路与估计行数。
7 规范沉淀：列应沉淀进 AGENTS.md（该 skill 现无）的规则条目（评审发现+隐含约定），写成可直接粘贴的规则句式。
输出 markdown 七节，≤1200 字，所有结论带 file:line。
