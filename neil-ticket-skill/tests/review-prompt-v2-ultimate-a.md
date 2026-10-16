你是资深 Python 工程师，对 /Users/neil/Desktop/neilcodebase/neil-skills/neil-ticket-skill/scripts/ticket.py 与 tests/ 做代码级评审（只读，禁止改文件、禁止执行 dws）。背景：钉钉工单巡检脚本，dws CLI 经 subprocess 调用；已知陷阱 15 条与第一轮 GLM-5.3 评审修复清单见同目录 ../reference.md 与 ../tests/review-2026-10-14-glm53.md（先读这两份再读代码）。

任务：
1. 修复核验：对照 GLM 报告逐条核验代码里对应修法是否正确完整（结构化 130003、失败隔离、create 查重、空页告警、sanitize 三重门禁、转义、最早建单卡、跟进节），点出 over-fix/under-fix/修引入的新 bug。
2. 残留缺陷表：P0/P1/P2，每条给 文件:行号、触发条件、后果、修法。重点：并发与 ThreadPool 异常路径、分页边界、重试幂等、正则误配、门禁可绕过性、JSON 信封差异。
3. 测试盲区：tests/run-regression.py 与 fixture 没盖住的高风险路径（≤5 条）。
输出 markdown 三节，总长 ≤900 字，不复述代码。
