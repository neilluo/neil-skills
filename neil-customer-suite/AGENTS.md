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
   **对账门只护 traffic，holdings/maas 无门**（实测 2026-11-08）：holdings 缺行不会触发降级，
   必须靠第6条的缺行补问自愈兜底，禁指望门。
   **gate 结论必须冻结为首次分组问数的权威判定**（collect.finalize_gate）：降级后禁二次重算
   ratio——降级后 config 内行 + 原始全量 unknown 行是两次不同问数的混合口径，拼一起求和无意义，
   实测曾把失败覆盖成 passed=true 造成 `passed=true & degraded=true` 自相矛盾、丢失真实 ratio。
   不变式：degraded=True ⇒ passed=False。
   分子求和必须按 (身份键, stat_date) **去重**（gate.dedupe_records，**非 None 值优先**，禁末行
   None 覆盖真值）：ChatBI 回重复行会使 grouped_sum 翻倍 → ratio≈2 → 门必挂 → 假降级把好数据换成坏数据。
   无身份键的行用序号兜底逐行保全（丢数据比不去重更糟）。
   **根因在 parse_grouped_rows：ChatBI 常把同一(客户,日期)的不同指标拆成多个稀疏行返回**
   （实测一行只带 oss、另一行只带 ecs_vcpu），必须做**值级合并**（各指标取首个非 None）输出唯一
   record，禁逐行 append——曾致 holdings 172 行(应60)/unknown 1202 行(应338)、gate 后写覆盖丢真值、
   缺行补问按「行存在」误判已补齐。合并后实测 hesi 六指标与报表真值逐一吻合。
6. sqlDatas 列名 '/' 被替换为 '_'（公网络流量/GB→公网络流量_GB）且带 (展示值) 兄弟列：
   匹配走 questions.pick_metric_col 归一精确匹配，禁子串兜底（weekly 陷阱 5）。
   **报表字段命名自身不一致**（实测下行=公网络下行流量、上行=公网络上行流量）：走 config
   metrics.aliases 别名精确匹配；**回行列集非确定**（同问两次列集可能不同）：缺列触发
   collect._supplement_missing 补问自愈（只问缺的指标按客户+日期合并），补问后仍缺才记 failure。
   **回行行集同样非确定**（实测 2026-11-08：15 天回填 holdings 仅 27/60 行）：缺**行**触发
   collect._supplement_missing_rows 逐客户补问（一次问该客户全部缺失日期，禁逐日扇出），
   合并进 parsed[scope]，补不到才记 failure。治理原则同缺列——缺什么补什么，禁静默不完整。
   缺行补问必须在 _assemble **之前**：products 段由 holdings 派生（_derive_products）。
   **降级路径的 metrics 必须带 aliases（3-tuple）**，与主链路 _jobs 一致：曾因构造 2-tuple
   丢 aliases → 报表真名靠 alias 才能命中的指标（net_up）恒 None（实测 60/60 格全丢）。
   **降级路径也要走补问自愈**（_supplement_one）：曾因 _supplement_missing 只在降级前调用一次，
   降级回来的缺列无人补救即静默落盘。
   **fixed_key 降级回行无客户列时**：①合计行靠整行扫描（questions._row_is_total）丢弃，
   禁把全网合计当客户值；②report_customer_name 必须填 fixed_name 报表真名，禁用 customer_key
   污染（实测曾出现 report_customer_name="haidilao"）。
7. 616045 组件**无产品名维度**（仅产品团队码，2026-11-07 probe 实测）：products 段=holdings
   指标派生的产品族存在性（collect._derive_products），产品级存在性走 neil-kunpeng-billing 账单深钻，禁宣称产品名级覆盖。
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
14. 画架构图仅用户主动触发，分两层：账单深钻+归线产出 arch.json 走 neil-kunpeng-billing（要浏览器
    登录态）；渲染 arch.json 出图走 neil-customer-arch（HTML 主路径默认对客脱敏 / excalidraw legacy）。
    arch.json 契约 docs/arch_schema.md 随渲染层落在 neil-customer-arch/。radar 日批不画图。
15. HTML 看板单文件重生式刷新（数据有变化才重写），不做 QW Pages 托管（发布要桌面确认弹窗，
    会卡死无人值守 cron）；远程查看由用户手动发布。
