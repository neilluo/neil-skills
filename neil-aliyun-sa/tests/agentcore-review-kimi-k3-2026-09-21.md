# AgentCore 蒸馏页评审核查报告

## 0. 核查覆盖
V1~V12 完成情况: V1 完成｜V2 完成｜V3 完成｜V4 完成｜V5 完成｜V6 完成｜V7 完成｜V8 完成｜V9 完成｜V10 完成｜V11 完成｜V12 完成
实际工具调用次数: 21
抽查的 raw 文件数: 24（agentcore 侧 19 + agentteams 侧 12，去重后；其中全文精读 6 个：billing-instructions / exemption / product-overview / sla-fulltext / service-linked-role-1 / agentteams-has-been-migrated-to-agentcore，其余为定点 grep/sed 核查）

## 1. 逐组判定（每组一行，严格此格式）
### V1｜OK
- 核了: §4.2 计费项总表 5 行的单价/计费维度/参考地域，及有无漏项多项
- 反证: 无矛盾，raw 逐字一致。`agentcore-billing-instructions.md:14` 同序 5 行：算力 CU「CNY 0.0000694/CU」「上海」、网关 CU「CNY 0.0000015/CU」、存储 CU「CNY 0.00025/CU」、协作专享管控面「实例/小时」「CNY 3/小时」、公网流量「GB（由云数据传输 CDT 统一计费和出账）」「CNY 0.8/GB」，与页面逐项逐字一致，无漏项无多项。

### V2｜OK
- 核了: CU 换算系数（1 vCPU·s=1 CU、1 GB·s=0.5 CU）、三组算力算例、网关 1 请求=1 CU、长连接每 30 秒折 1 次、0.015 元/万次、三组网关算例、存储 CU 定义与 720 小时口径、§4.8 全部自推导月量级算式
- 反证: 无矛盾，raw 逐字一致（`agentcore-billing-instructions.md:24-50`）。页面自推导数字复算全部成立：0.4997×720=359.784、1800×0.0000694=0.12492、3×720=2160、2160÷359.784=6.003、2880×30×100×0.0000015=12.96、359.78+1.8+1.5+80=443.08、+2160=2603.08。唯一瑕疵是两节推导尾数不一致（359.784 vs 359.77），记入 S4/D-4，不判本组 F。

### V3｜OK
- 核了: 地域价表行数/覆盖地域/是否同价、新加坡单价缺失表述
- 反证: 无矛盾。`agentcore-billing-instructions.md:58-62`「各地域定价」下仅「中国内地地域」一个子节、仅 1 行「北京、杭州、上海、深圳｜0.0000694｜0.0000015｜0.00025｜3」，表后以 `<br />` 结束；`新加坡` 在该文件命中 0 次（实测）。支持地域 5 行含「新加坡｜ap-southeast-1」见 `agentcore-product-overview.md:32`。页面表述与 raw 实际缺失情况一致。（页面所述"英文页/价格页/HTML 三处亦无"不在本地 raw 内，不纳入判定。）

### V4｜OK
- 核了: 活动起止（精确到秒与时区）、原价、限免排除项、0 元账单口径、30 天无操作回收与不可逆、FAQ 四条
- 反证: 无矛盾，raw 逐字一致。`acentcore-collaboration-control-face-exemption-description.md:13`「2026 年 09 月 18 日 00:00:00 --- 2026 年 10 月 18 日 23:59:59（北京时间，GMT+8）」；`:23`「限免不包括：Agent运行时的算力、存储和网关请求等其它费用」；`:27`「协作管控面原价 ¥3/小时」；`:30`「账单仍会正常推送，限免期间协作管控面金额为 0 元」；`:32`「活动结束后计费策略另行通知」；`:36`「限免期间创建的协作管控面实例在连续 30 天无操作时会被停用并自动回收资源」；`:40` FAQ 四行逐字相同。「共 31 天」「距结束 27 天（蒸馏时点 2026-09-21）」换算成立。

### V5｜OK
- 核了: 三项依赖产品名称/用途/开通方式
- 反证: 无矛盾，raw 逐字一致。`agentcore-product-overview.md:35`：CMS（云监控）「用于写入 Tracing 数据」「跳转云监控控制台开通」、PrivateLink（私网连接）「提供私网访问能力」「点击后自动开通」、SchedulerX3「提供分布式任务调度能力」「跳转售卖页购买」。§4.5 与 §8.4 两处表述一致。

### V6｜OK
- 核了: 99.9%、赔偿三档区间与比例、赔偿基数、上限与可叠加、代金券性质、申请时限、两条范围限定词、协议级排除、例外第 (7) 条、§7.8 全部 grep 命中数声明
- 反证: 无矛盾，raw 逐字一致。`sla-agreement-fulltext-terms-alicdn.md:13`「版本生效日期：2026-09-18」；`:17`「除非另有约定，本协议不适用于 AgentCore 公测、邀测、免费的功能及版本，也不适用于 AgentCore 本地云版本」；`:59-61`「Agent 运行时服务可用性不低于 99.9%。」「本承诺仅针对 AgentCore 平台自身的 Agent 运行时服务…不在本协议保障范围内」；`:91-93` 三档「≥ 99.0% 且 < 99.9%｜15%」「≥ 95.0% 且 < 99.0%｜30%」「< 95.0%｜100%」；`:95`「不超过该服务单元当月月度服务费用的 100%；不同服务单元分别计算、可叠加…服务代金券…不可提现、转让或折现」；`:99`「每月第五（5）个工作日后…两（2）个月内…超出申请时限的赔偿申请将不被受理」；`:79` 第 (7) 条逐字一致。负面声明实测成立：`99.95`/`99.99`/`限免`/`协作`/`管控面`/`地域`/`新加坡`/`工单`/`控制台`/`有效期`/`AgentRun`/`AgentTeams`/`持久性`/`可靠性` 在协议全文命中均 0；`公测`/`邀测`/`免费`/`本地云` 各 1 次且全在 :17。

### V7｜OK
- 核了: 该条是否标 [推断]、两条依据原文是否存在、推理是否成立
- 反证: 无矛盾。页面 §7.7 明确标 `[推断]`；依据①「活动期间，所有账号的 AgentCore 协作管控面实例均享受限时免费」（`acentcore-...exemption-description.md:17`）+「协作管控面原价 ¥3/小时，活动期间不产生费用」（`:27`）+ SLA「不适用于…免费的功能及版本」（`sla-...alicdn.md:17`）；依据②「限免不包括：Agent运行时的算力、存储和网关请求等其它费用」（exemption `:23`）。两条原文均真实存在，「限免管控面→免费功能→协议级排除；Agent 运行时仍付费→99.9% 仍有效」推理成立，且页面已列三重限定（除非另有约定/协议未列举该活动/管控面本身无承诺），未越界成官方结论。

### V8｜OK
- 核了: 6 条硬配额逐条回源
- 反证: 无矛盾，raw 逐字一致。①「最多可配置20个SubAgent」`manage-agent-templates.md:31`；②「长度为 1～64 个字符，只能包含小写字母、数字和短划线」+「同一 Workspace 内的记忆空间名称必须唯一」`manage-memory-space.md:90`；③「可选，最多 1024 个字符」同 `:90`；④「工具的描述信息，不超过 1000 个字符」`managing-the-mcp-server.md:20`；⑤「默认并发数为 2，支持设置为 1～8」`guidelines-for-the-use-of-local-nanoagent.md:256`；⑥「需选择至少 2 个交换机，并确保覆盖至少 2 个不同可用区。」`manage-workspace.md:29` 与 `view-overview.md:60` 双页同文。

### V9｜OK
- 核了: 30 用户上限三处逐字、IM 平台清单、微信真实覆盖与页面表述边界
- 反证: 无矛盾。「目前，同步仅支持导入 30 人以内的成员。」`agentcore-configure-dingtalk-account-integration.md:24`；「当前账号集成的钉钉应用最多支持 30 个用户，超出后账号集成将失败。」同页 `:58`；飞书同句 `configure-dingtalk-account-integration.md:78`。IM 清单「接入钉钉、飞书或企业微信机器人」`integrate-the-agent-into-the-im-channel.md:11`。`微信` 在 agentcore 侧 32 个正文快照中确仅命中 2 页（product-overview:19 账号集成宣称 + im-channel 消息通道），第三处命中在 agentteams/magic-console-product-overview.md:22（AgentTeams 场景描述，超出页面声明的"32 页"口径边界）；企业微信凭证为「Bot ID、Secret」+「连接方式设置为长连接」（im-channel `:33,:83-100`），确为消息通道非账号集成。页面「不得承诺微信扫码登录」结论未越界。

### V10｜F2
- 核了: nanoagent vs 本地纳管、AgentTeams 在现役页的指代、§9.8「仅此 1 处」实测声明
- 反证: 主体成立——剥离 frontmatter 后 `grep -ci nanoagent`=0、「本地纳管」=4（`guidelines-for-the-use-of-local-nanoagent.md`）；「定时任务在协作客户端（AgentTeams）中创建和管理」`use-team-web-to-set-tasks.md:24`；「协作客户端 (WEB)/(API)」`set-up-team-collaboration.md:43`，消歧成立。🔴 但 §9.8 称「该词在 AgentCore 侧 32 个正文快照中除迁移页外仅此 1 处出现」，实测 `agentcore-product-overview.md:44` 亦含「AgentTeams」（迁移页链接「AgentTeams 迁移至 AgentCore」），即迁移页外至少 2 处、分布在 2 个文件，且该处指①——页面自己的 §1.1 正是引用 :44 作指代①的证据，§9.8 与 §1.1 亦自相矛盾。详见 D-1。

### V11｜F2
- 核了: Action 总数、各前缀条数、schedulerx 命中、ServiceName、OSS ARN、删除前提
- 反证: 多数成立——oss=16（Bucket 级 5 + 对象级 11，`:57-61` + `:112-122`）✓；`schedulerx` 命中 0 ✓；ServiceName=magic.aliyuncs.com（`ram:DeleteServiceLinkedRole` 的 Condition，`:265-272`）✓；另一 Condition=privatelink.aliyuncs.com（`:275-281`）✓；对象级 Resource=`acs:oss:*:*:hiclaw-*`（`:124`）✓；删除前提 2 条与警告（`:291-297`）✓；角色名/搜 Magic/首次必须创建（`:16,:36,:41`）✓。🔴 但页面称 ram=5、合计 160 条；对策略 JSON 解析实测：Action 条目总数 **158**，ram 动作仅 **3** 条（`ram:CreateServiceLinkedRole`×2、`ram:DeleteServiceLinkedRole`×1）；多出的 2 是 `:270/:280` 的 Condition 键 `"ram:ServiceName"` 被字符串 grep 计入了"动作"。详见 D-2。

### V12｜OK
- 核了: 迁移形态/粒度/6 步/主账号/CLI 3.3.0/2 插件 3 Skill/两种模式/不回滚/新 Endpoint/源端冻结/异常资源口径/10 类可迁移逐字/5 类不迁移逐字/迁后 5 件事/敏感信息口径/迁移完成定义/4 项缺口声明/术语映射表 19 条两态
- 反证: 无矛盾，全部与 `agentteams-has-been-migrated-to-agentcore.md` 逐字一致：可迁移 10 类（`:16`）、不迁移 5 类（`:21-29`）、新 Endpoint（`:31`）、源端冻结（`:33`）、异常资源（`:35`）、前提 4 条（`:40-46`）、CLI≥3.3.0+2 插件（`:84-88`）、3 Skill（`:60-64`）、6 步（`:114-127`）、标准/危险模式表（`:118`）、「服务不会自动回滚、删除已创建资源或跳过失败项」（`:120`）、Team 最后恢复（`:127`）、迁后 5 件事（`:132-140`）、敏感信息（`:142`）、失败三选一（`:145`）、「迁移完成…不表示调用方已切换…」（`:149`）。生效时间/是否强制/控制台是否可进/新页映射 4 项确为 raw 未覆盖，页面如实标缺口。术语映射表 19 条（1 条 ✅/18 条 ❌）计数相符，抽查 14 条证据引文全部逐字命中（management-skill:20、manage-instances-1:13/54、magic-console-product-overview:11/28、manage-worker-templates-1:11、local-worker-user-guide:12、manage-workers-and-worker-teams:18/23、manage-users:20、management-models-and-suppliers-1:18、managing-the-mcp-server:22、configure-dingtalk-account-integration:20、service-linked-role-1:36/41、view-dashboards-and-monitoring-1:11）。

## 2. 缺陷清单（按严重度排序，每条严格此格式）
### D-1｜F2｜CRITICAL｜§8.2（并波及 §8.3、§12.5 D6）
- 页面原文: 「| `ram` | **5**（其中 2 条带 Condition） | `*` |」「| **合计** | **160** 条（原文含重复项） | — |」「策略 JSON 逐条统计（2026-09-20 对 raw 重算…）」
- raw 反证: `service-linked-role-1.md:69`「"ram:CreateServiceLinkedRole"」、`:265`「"ram:DeleteServiceLinkedRole"」、`:275`「"ram:CreateServiceLinkedRole"」——全文 ram 动作仅 3 条；`:270`/`:280` 的「"ram:ServiceName"」是 Condition 键而非动作。对策略 JSON 解析实测：Action 条目合计 158（apig 57 / ecs 36 / airegistry 17 / oss 16 / vpc 9 / mse 7 / cms 6 / privatelink 5 / ram 3 / log 1 / bss 1；重复项为 ram:CreateServiceLinkedRole 与 apig:RemoveConsumerAuthorizationRule 各多 1 次）。
- 为什么是缺陷: 页面把字符串 grep 的 160（含 2 个 Condition 键）当作「Action 条目数」，ram 5/合计 160 与 raw 不符；且标注"已对 raw 重算"会误导维护者直接采信。实际影响有限：schedulerx=0、oss=16、hiclaw ARN、ServiceName 等全部下游结论不受波及。

### D-2｜F2｜CRITICAL｜§9.8
- 页面原文: 「实测该词在 AgentCore 侧 32 个正文快照中除迁移页外仅此 1 处出现，且指的是②。」
- raw 反证: `agentcore-product-overview.md:44`「* [AgentTeams 迁移至 AgentCore](https://help.aliyun.com/document_detail/3052611.html)」——迁移页之外第二个含「AgentTeams」的正文快照（另一处为 use-team-web-to-set-tasks.md:24），且该处指①遗留产品。
- 为什么是缺陷: 「仅此 1 处」实测为至少 2 处（2 个文件各 1 次），声明的 grep 结论与 raw 不符，并与本页 §1.1（引用同一行作指代①证据）自相矛盾。消歧结论本身（① vs ②）仍正确，故实际危害低，但属自报实测口径错误。

### D-3｜F2｜CRITICAL｜§2.4（并波及 §0 横幅的同源表述）
- 页面原文: 「准入『白名单』｜grep -n 白名单 × 13 页｜仅 2 处，全部在 high-code-agent-deployment-guide，且均为 ACR 侧网络白名单」
- raw 反证: `integrate-the-agent-into-the-im-channel.md:37`「配置机器人时，请开通卡片读写权限。如果启用了 IP 白名单，还需将以下 IP 地址加入白名单：」（该页为操作指南、且本页 §5.5 正引用其 6 个 IP）；另 `create-a-high-code-agent-using-the-python-sdk.md:21` 亦命中「白名单」。
- 为什么是缺陷: 在「操作指南层」这一页面自述口径下，high-code 之外至少还有 IM 渠道页命中，「仅 2 处全部在 high-code」与 raw 不符。保留意见：页面未列出 13 页清单，若该集合刻意排除 IM 渠道页则无法完全证伪；但排除一个操作指南页而纳入另一个不合常理。重要减损：负载结论「无一处是产品准入白名单」仍成立（IM 的 IP 白名单同为网络白名单），客户不会被误导去"申请加白"。

### D-4｜F9｜HIGH｜§10.5 vs §4.8
- 页面原文: §10.5「7200 CU/h × 0.0000694 元/CU × 720 h = 359.77 元（官方单小时算例 0.4997 元 × 720）」；§4.8「官方算例…× 720 小时 = 359.784 元」
- raw 反证: `agentcore-billing-instructions.md:29`「7200 × 0.0000694 = CNY 0.4997」——0.4997 × 720 = 359.784 ≠ 359.77；精确式 7200×0.0000694×720 = 359.7696。
- 为什么是缺陷: 同一推导月费在两节给出不同精确值（359.784 vs 359.77），且 §10.5 括号内自称的算式（0.4997×720）结果与其等号左边的 359.77 自相矛盾。头条值 ≈359.8 两节一致，客户面数字不受影响，故实际危害很低。

## 3. S1~S5 附加扫描结果
S1 [官方] 抽查: 抽了 16 条（§4.2 计费表、§4.3 CU 换算与算例、§4.5 依赖产品、§4.6 限免全部、§7.1-7.6 SLA 九处、§2.3 六条配额、§5.3 30 用户三处、§5.4 manage-users 认证方式（AC+AT 两页）、§5.5 IM 清单/6 IP/企业微信长连接、§3.1 Agent 类型表含两处「待上线」、§2.2.1 Qoder 连接器、§3.3 五行最低版本号、§5.1 团队限制②「暂不支持」、§6.2 SDK 包身份、§6.3 Python 3.10/3.11/0.1.1、§9.5 AT 计费 8/9/7 与 9 行依赖表）｜16 条通过｜0 条 F4
S2 链接: 12（knowledge 内 5：aliyun-products/service-availability/aliyun-lingjun-bms/cloud-solutions/ai-trends；references 1：pricing-verification-checklist；raw 相对链接 6）+ 6 个 [[wikilink]]｜死链数 0｜[[百炼]]/[[CDT]]/[[EIP]]/[[云监控]]/[[PrivateLink]]/[[RAM]] 在 aliyun-products.md 均有对应条目（云监控 :2298、PrivateLink :653、RAM :2165、CDT 见 :455 出云流量费节）；lingjun §14.6（:359）、cloud-solutions S3（:243）、ai-trends §11（:328）锚点均在
S3 §锚点: 约 40 处 §x.y 内部引用｜断锚数 0｜§2.3/§2.4/§3.1-3.6/§4.2-4.10/§5.1-5.6/§6.1-6.6/§7.1-7.9/§8.1-8.6/§9.1-9.11/§10.1-10.6/§11.1-11.6/§12.1-12.7 表头全部存在
S4 口径分叉: 1 条｜即 D-4（359.784 vs 359.77）。限免窗口（§0/§4.6/§7.7/§10.6 一致）、SLA 99.9%（§0/§7/§10.3 R1 一致）、30 用户上限（§0/§5.3/§10.1 一致）、单价（§4.2/§4.4/§10.5 一致）、依赖产品 3 项（§4.5/§8.4/§10.5 一致）均无分叉
S5 危险性靠遗漏: 0 条｜逐项想过"照做会否受损"：30 天不可逆回收（§4.6/R4 已显著标注）、SLR 删除前提与警告（§8.1）、迁移不回滚留半成品（§9.3）、危险模式批量确认（§9.3）、IM 拉群权限外溢（§5.5/§10.4-8）、bootstrap token 明文仅展示一次+泄露即重签（§3.3）、`--` 后参数整体替换（§3.3/§10.4-1）、公开镜像仓库不得打入密钥（§3.2/§6.5）、健康检查端口不匹配触发重启（§3.2/§10.4-2）、SLA 例外 (7) Agent 授权操作不赔（§7.6/R10）、高代码 Agent 暂不支持 Team 协作（§5.1/§6.5）、记忆空间删除不可恢复（§2.2.2）——权限前提/副作用/不可逆性/赔偿例外均已随能力描述给出，未发现"准确但漏前提"的条目

## 4. 总体裁决
CRITICAL 3 条 ｜ HIGH 1 条 ｜ MEDIUM 0 条 ｜ UNVERIFIABLE 0 条
一句话结论: 不能直接原样拿去做对客作战，但离可用只差修 4 处——页面全部承重事实（5 计费项单价、CU 换算、地域价、限免窗口、SLA 99.9% 与三档赔偿、6 条配额、30 用户上限、SLR 安全结论、迁移 10 迁/5 不迁/6 步）逐字核过全部命中 raw；最危险的一条是 §8.2 自称"已对 raw 重算"的 SLR 统计表仍把 2 个 Condition 键计成 Action（ram 5→实 3、合计 160→实 158），它不伤及任何安全结论，却会动摇读者对全页"实测 0 命中"类自证语句的信任——而这类语句正是本页的立身之本。

## 5. 我对本核查书本身的异议
无。核查书给出的被测页路径、raw 目录、frontmatter 前 10 行规则（正文确从第 11 行起，已实测）、slug 缺 g 警示（`acentcore-...` 确为官方拼错）、V4 文件名、V11 关注点（oss 条数）均与本地 raw 实测一致；未发现主控抄错数字或给错路径。
