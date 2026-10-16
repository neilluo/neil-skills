你是资深工程师 + 阿里云客户服务业务专家，对 /Users/neil/Desktop/neilcodebase/neil-skills/neil-ticket-skill 的文档与契约层做评审（只读，禁止改文件、禁止执行 dws）。读：SKILL.md、reference.md、config/customers.json、templates/daily-report.md、tests/review-2026-10-14-glm53.md，并抽查 scripts/ticket.py 验证文档宣称与实现是否一致。

任务：
1. 契约一致性：SKILL.md/reference 的每条流程宣称（三段链路、门禁、降级、口径、加客户步骤、维护操作表）与代码实现逐条对照，列「虚标/漏标/错标」表。
2. 业务改进（≤5 条按价值排序）：日报口径、实质状态、降级、跨天跟进、配置化加客户之外，还有什么更高价值改进；漏报/误报残余风险。
3. 性能（≤3 条）：dws 调用量与并发还有无安全可拿的收益（稳定性优先）。
4. 口径冲突：若你认为 reference 某条陷阱或取舍记录不成立，列出并说明裁决所需证据。
输出 markdown 四节，总长 ≤900 字。
