# AGENTS.md — neil-customer-suite 工作手册

## 凭据与仓库安全
1. **本仓库为 PUBLIC**：FBI token、客户流量/保有量数据、快照 outputs 一律禁止入库。token 只存
   `~/.qwenworkcn/secrets/fbi_token.json`（600）或环境变量 ACCESS_TOKEN；config 只写取用位置。
   `neil-customer-radar/outputs/` 由套件 .gitignore 全量排除。
2. 统一客户表 `config/customers.json` 是唯一事实源；三套 cid 分列（dingtalk.service_group_cid /
   maas_cid / devata.cid+uid），禁混用。加客户=仅改本表，代码零改动。

## ChatBI 取数（neil-customer-radar）
3. 传输层契约逐行移植自 neil-weekly-service-report chatbi.py：限流 201000 长退避、
   instantQueryMode=False、queryUpdateChat 瞬态 201000 续轮询。改动须同步回写出处。
4. **分组问数优先**：一问按客户+统计日分组回全量行矩阵，禁逐客户扇出问数（限流面）。
   创建错开 create_stagger_seconds=8，轮询并发 ≤4（限流卡在 createChat 频率不卡轮询）。
5. **合计对账门**：分组问数全量行（config 内+unknown 行）求和 vs 报表匿名合计行，
   |ratio-1|>gate_tolerance(0.05) 或 traffic 空 → 降级逐客户问数并标 degraded。
   实测 2026-11-07：ChatBI 自然语言→SQL 有非确定性（同问两次回行集合可能不同），对账门是唯一防线。
6. sqlDatas 列名 '/' 被替换为 '_'（公网络流量/GB→公网络流量_GB）且带 (展示值) 兄弟列：
   匹配走 questions.pick_metric_col 归一精确匹配，禁子串兜底（weekly 陷阱 5）。
   **报表字段命名自身不一致**（实测下行=公网络下行流量、上行=公网络上行流量）：走 config
   metrics.aliases 别名精确匹配；**回行列集非确定**（同问两次列集可能不同）：缺列触发
   collect._supplement_missing 补问自愈（只问缺的指标按客户+日期合并），补问后仍缺才记 failure。
7. 616045 组件**无产品名维度**（仅产品团队码，2026-11-07 probe 实测）：products 段=holdings
   指标派生的产品族存在性（collect._derive_products），产品级存在性走 kunpeng 账单深钻，禁宣称产品名级覆盖。
8. 报表缺行客户（流量为零者不在 traffic 组件）≠ 停用：分析层以 holdings 为存在性锚点。

## dws 执行契约（宿主约束，2026-11-07 实测）
9. **dws 禁止被 Python subprocess 调用**（宿主 guard 拦截，报 unsupported shell shape）：
   store 层只产 argv 清单（outputs/store-plan-*.json），由 agent/cron agent 逐条直接执行 dws。
10. `+record-upsert-by-key` 的 create 路径 read-back 校验有**最终一致性假阳性**
    （create 实际成功但 verification 报 "read-back found no record"，status=unknown）：
    store-plan 每条带 on_unknown 元数据（query_argv+rule）：查到记录且 cells 正确→不重试；
    查不到→重试一次；仍查不到→报错停。禁见 unknown 就盲重放（重试会双写）；update 路径正常。
11. 非交互环境 composite 命令必须显式 `--yes`；建 Base 用 `base create --folder-id <节点URL>`，
    建后必须 `drive info` 回读 folderId 校验落位（adoc 文档节点可当 Base 父容器，2026-11-07 实测）。

## 分析与交付
12. 事件 ID 确定性：`<customer_key>:<event_type>:<metric>:<start_date>`；事件表按 ID 单键 upsert 幂等。
    信号只报证据（日期区间+幅度+原始值），禁下「客户在迁云」类结论。
13. 网络异动默认阈值（config thresholds，禁硬编码）：公网 7 日均值 |Δ|≥30% 且连续 3 天同向；
    专线流出 7 日均值跌 >50% 或归零=P1 迁移疑似。
14. 画架构图仅用户主动触发，走 neil-kunpeng-expert（账单深钻+归线+渲染）；radar 日批不画图。
15. HTML 看板单文件重生式刷新（数据有变化才重写），不做 QW Pages 托管（发布要桌面确认弹窗，
    会卡死无人值守 cron）；远程查看由用户手动发布。
