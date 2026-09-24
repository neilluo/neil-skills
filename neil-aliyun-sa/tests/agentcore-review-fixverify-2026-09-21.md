# AgentCore 蒸馏页 fix-verification 报告

- 复核员：Kimi-K3（与上轮评审同一模型族，本轮仅复核 7 项修复）
- 被测页面：`/Users/neil/Desktop/neilskills/neil-aliyun-sa/knowledge/aliyun-agentcore.md`（1863 行）
- 方法：页面定点核读 + 回归 raw 独立重算 + 回归脚本实测 + 负控实验独立复现。工具调用约 21 次。

## 1. 逐项判定

### FX-1｜PASS-FIXED
- 核了: §8.2 表值、统计口径说明、全页 160/ram 5 残留、raw 独立重算、邻近结论未被误改。
- 反证/证据:
  - 表值已改：line 1324「| `ram` | **3**（另有 2 处 `"ram:ServiceName"` 是 **Condition 键**，不计入 Action）」；line 1328「| **合计** | **158** 条（含 2 条重复项：`ram:CreateServiceLinkedRole`、`apig:RemoveConsumerAuthorizationRule`；去重后 **156** 条唯一 Action）」。
  - 口径说明已补：line 1313「🔴 **统计口径：解析策略 JSON 的 `"Action"` 字段（数组形式与标量形式都计），排除 Condition 键（如 `"ram:ServiceName"`）；裸 grep 会把 2 个 Condition 键误计为 Action 而得出 160**」。
  - 全页扫 `160`：命中仅 line 318/1603/1695（`16039 字节`，无关）、759/766/798/1615/1643（`2160`，无关）、927（IP `118.178.89.160`，无关）、1313/1333/1807/1854（口径说明与 D6/D-1 留痕，合法）。全页扫 `ram 5`：仅 line 1333/1807/1854 三处留痕，合法。无非留痕残留。
  - raw 独立重算（python 解析 `raw/aliyun-docs/agentcore/service-linked-role-1.md` 策略 JSON）：Action 合计 **158**，前缀分布 apig 57 / ecs 36 / airegistry 17 / oss 16 / vpc 9 / mse 7 / cms 6 / privatelink 5 / ram 3 / log 1 / bss 1；重复项恰为 `ram:CreateServiceLinkedRole`×2、`apig:RemoveConsumerAuthorizationRule`×2；唯一 Action **156**；`schedulerx` 命中 0；正文 `ram:ServiceName` 恰 2 处（Condition 键）；裸 grep `ram:` = 5。与页面逐字一致。
  - 邻近结论未误改：line 1329 `schedulerx` 0、1320 `oss 16`（5 Bucket + 11 对象级）、1301 `magic.aliyuncs.com`、1309/1320 `acs:oss:*:*:hiclaw-*` 均原样。

### FX-2｜PASS-FIXED
- 核了: §9.8 现文、与 §1.1 的一致性、raw 独立 grep。
- 反证/证据:
  - §9.8 已改：line 1524「实测该词在 AgentCore 侧 32 个正文快照中除迁移页外出现 **2 处**：`agentcore-product-overview.md:44`（指①已迁移的独立产品）与 `use-team-web-to-set-tasks.md:24`（指②协作客户端）。**两处指代不同对象，正是本条命名歧义的实证。**」
  - 与 §1.1 不再矛盾：§1.1 line 66 以 `agentcore-product-overview.md:44` 为指代①的证据，§9.8 现把同一行同样归为① —— 两处口径一致。
  - raw 独立 grep（`grep -rn AgentTeams`，排除迁移页、README.md、SHA256SUMS.txt）：恰 2 命中 —— `agentcore-product-overview.md:44`「* [AgentTeams 迁移至 AgentCore](https://help.aliyun.com/document_detail/3052611.html)」与 `use-team-web-to-set-tasks.md:24`「定时任务在协作客户端（AgentTeams）中创建和管理。」。「除迁移页外 2 处」成立。

### FX-3｜PASS-FIXED
- 核了: §2.4 双口径、承重结论保留、§0 横幅同步、raw 独立 grep。
- 反证/证据:
  - §2.4 已改且双口径俱在：line 251「**4 处 / 3 个文件**（🔴 此为 `grep -c` 的**匹配行数**口径；按**出现次数**为 **7 次** —— `high-code-agent-deployment-guide` 3 次、`create-a-high-code-agent-using-the-python-sdk` 2 次、`integrate-the-agent-into-the-im-channel` 2 次。两种口径都已列出…）」。
  - 承重结论原样保留：line 251 末尾「🔴 **无一处是产品准入白名单** —— 即 **AgentCore 无准入加白门槛**，客户不需要申请白名单即可开通」。
  - §0 横幅已同步：line 19「`白名单` 字样在全部 32 个正文快照中实测 **4 处 / 3 个文件**，全为 ACR 镜像仓库或 IM 渠道的网络白名单，无一处是产品准入，见 §2.4」。
  - raw 独立 grep（排除 README/SHA256SUMS）：`grep -c` 命中行 = high-code 2 + python-sdk 1 + im-channel 1 = **4 行 / 3 文件**；`grep -o` 出现次数 = high-code 3 + python-sdk 2 + im-channel 2 = **7 次**。与页面一致；四处语境（high-code:100 ACR 公网白名单、high-code:150 排障表「公网白名单或 VPC 访问配置」、python-sdk:21 ACR 白名单、im-channel:37 IM 渠道 IP 白名单）均为网络白名单，「无一处是产品准入」成立。

### FX-4｜PASS-FIXED
- 核了: 两节三个数字与「差 0.014 元」逐字一致、全页 359.77 扫描、独立算术。
- 反证/证据:
  - §4.8 第 2 条 line 744 与 §10.5 line 1642 关键句逐字一致：「官方算例 0.4997 元/小时 × 720 小时 = **359.784 元/月**；按未取整单价精确计算 7200 CU × 0.0000694 元/CU × 720 h = **359.7696 元/月**。本页统一取 **≈359.8 元/月**（两种口径差 **0.014 元**，源自官方对单小时值的四舍五入）」（§4.8 前多「算式：」引导词，数字与差值表述完全一致）。
  - 全页扫 `359.77`：仅 line 1857（§12.7 D-4 缺陷留痕）1 处命中，合法；§4.8/§10.5 正文零命中。
  - 独立算术：0.4997 × 720 = 359.784 ✓；7200 × 0.0000694 = 0.49968，× 720 = 359.7696 ✓；359.784 − 359.7696 = 0.0144 ≈ 0.014 ✓。

### FX-5｜PASS-FIXED
- 核了: 精度约定说明存在性与表述、是否化解上轮 F9、小计/合计独立验算。
- 反证/证据:
  - 说明已存在且表述清楚：line 764「> **本表精度约定**（主控裁决 2026-09-21）：本表按**两位小数**呈现，`359.78 元` = 官方算例 `0.4997 元/小时 × 720 h = 359.784 元` 的两位小数显示；`小计 443.08`、`合计 2603.08` 均由此两位小数值累加得出，**表内自洽**。§4.8 第 2 条与 §10.5 给出的是**完整精度口径**（359.784 / 359.7696 / 统一取 ≈359.8）。两处**不是矛盾，是精度层级不同**：对客报价用 ≈359.8，表内累加用两位小数。」
  - **F9 化解了**。四个数（359.78 / 359.784 / 359.7696 / ≈359.8）现在各有明确角色且互相指向：表内 359.78 被声明为 359.784 的两位小数显示；359.7696 与 359.784 的 0.014 差已归因；≈359.8 被声明为统一对客口径。每个承载面要么直接用 ≈359.8（line 744/746/766/1642），要么（组合月账单表）紧贴精度约定说明出现，不存在无注释的孤立场值。不构成新的口径分叉。
  - 独立验算：359.78 + 1.80 + 1.50 + 80.00 = **443.08** ✓（line 758）；443.08 + 2160.00 = **2603.08** ✓（line 760）。表内自洽。

### FX-6｜PASS-FIXED
- 核了: §12.1 现文与独立计数。
- 反证/证据:
  - 已改：line 1760「本页**约 26 处** `RULINGS §x / B* / G* / D*` 形式的引用指向它（另有 2 处为文件名提及）」。
  - 独立复核：`grep -o -i rulings | wc -l` = **29**；其中文件名提及（`agentcore-distill-rulings-2026-09-20.md`，line 6 与 line 1760）恰 2 处；§12.1 自述（`RULINGS §x`）1 处；29 − 2 − 1 = **26**，与清单预期一致。附注：26 处中 25 处为 §/B/G/D 形式，1 处为「RULINGS R3」（line 116，R* 形式）——页面用「约」已覆盖此微小口径差，不构成缺陷。

### FX-7｜PASS-FIXED
- 核了: 占位注释清除、§12.7 对 4 条缺陷的描述与我上轮报告的一致性、降级理由成立性、负控与回归陈述的事实性。
- 反证/证据:
  - 占位注释已清除：全页 grep `<!--` / `由主控在评审` / `占位` 零命中；§12.7（line 1823~1863）为完整评审与回归记录。
  - 描述与我上轮报告（`/tmp/agentcore-work/review/Kimi-K3/report.md` line 58~76）一致：D-1（ram 5→3、合计 160→158）、D-2（「仅此 1 处」实为 2 处且与 §1.1 矛盾）、D-3（「仅 2 处全部在 high-code」实为跨文件）、D-4（359.77 vs 359.784，自称算式 0.4997×720 与 359.77 自相矛盾）四条的事实陈述与定级对照（CRITICAL→HIGH / CRITICAL→MEDIUM / CRITICAL→MEDIUM / HIGH→LOW）逐项吻合；「4 条事实层面全部成立，无一驳回」（line 1861）属实。
  - 降级理由**成立**（详见 §3 逐条意见）。
  - 负控（评审闸）：`/tmp/agentcore-work/review/Kimi-K3-NEGCTL/report.md` 确认 5 类伪造（算力单价 0.000694 / SLA 99.95% / 限免截止 2026-12-18 / 回收 90 天 / 300 用户）全部被抓出、全部 CRITICAL，与 §12.7 line 1846~1848 陈述一致。
  - 回归（闸 1）：我独立重跑 `python3 scripts/run-regression.py` → **62/62 PASS、exit 0**（yaml 实有 62 用例，含 AC01~AC16，`knowledge/aliyun-agentcore.md` 已在 files.knowledge line 11）。负控陈述我**独立复现**：在页面临时副本注入同类 6 处篡改后 → **PASS 57/62、FAIL 5/62、exit 1**，红的恰为 **AC02/AC03/AC07/AC09/AC11**（AC11 6/8=75% 由「30 个用户」+「30 用户硬上限」两字面形态同时被篡改所致），与 §12.7 line 1836 逐字吻合；恢复后页面 SHA256 与篡改前一致。（注：首轮我只篡改「30 个用户」一种形态时 AC11 以 7/8=87.5% 仍 PASS，印证 §12.7「灵敏度已知边界」自述属实。）

## 2. STILL-ISSUE / NEW-ISSUE 明细（若有）

无。

## 3. 总体裁决

PASS-FIXED 7/7 ｜ STILL-ISSUE 0 ｜ NEW-ISSUE 0

🔴 本页现在能否直接用于对客作战: **能** —— 4 条缺陷已全部真修（表值、口径说明、同源横幅、留痕四层同步），承重数字我逐项独立重算命中 raw，但 §0 的 2026-10-18 限免到期复核与 §11.2 三硬缺口「如实告知官方未公开」两条纪律不可跳过。

🔴 对主控 3 项降级裁决的意见（另附 D-4 一并）:
- **D-1 CRITICAL→HIGH：同意。** 错值只在内部统计表，未传播到任何对客结论；我上轮报告已自述「实际影响有限：schedulerx=0、oss=16、hiclaw ARN、ServiceName 等全部下游结论不受波及」。但它打在「已对 raw 重算」类自证语句上，HIGH 比 MEDIUM 更能反映其对页面立身之本（可溯源性）的杀伤力，降级一档恰当。
- **D-2 CRITICAL→MEDIUM：同意。** 消歧结论（①vs②）本身正确，客户面不被误导；错误限于自报 grep 计数与内部矛盾，属可信度问题。我上轮亦自述「消歧结论本身仍正确，故实际危害低」。
- **D-3 CRITICAL→MEDIUM：同意。** 承重结论「无一处是产品准入白名单」在 4 处/3 文件的正确口径下依然成立（新增两处同为 ACR/IM 网络白名单），客户不会被误导去申请加白；错误限于计数与归属，降级成立。
- **D-4 HIGH→LOW：同意。** 头条值 ≈359.8 两节本就一致，0.014 元差在 360 元量级上无客户面影响；修复后根因（官方对单小时值四舍五入）已写明，两节表述逐字统一。

## 4. 我对本复核清单的异议

无。清单给出的旧值/新值与预期计数（158 / ram 3 / 2 处 / 4 行 7 次 / 359.784 / 359.7696 / 0.014 / 29−2−1=26 / 57+5 exit 1）经我逐项独立复算全部与 raw 及实测一致。
