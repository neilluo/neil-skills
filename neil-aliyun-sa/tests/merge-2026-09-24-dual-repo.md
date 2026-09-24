# 双仓合并留痕 — 2026-09-24

> 把独立仓库 `neil-aliyun-sa` 的全部内容并入统一仓库 `neil-skills/neil-aliyun-sa`。
> 分支：`merge/neil-aliyun-sa-standalone`。本文档是逐文件裁决与门禁结果的唯一权威留痕。

## 1. 输入

| 角色 | 路径 | 状态 |
|---|---|---|
| base（共同祖先快照） | `neil-skills` commit `3723a5a`（2026-07-06「consolidate all neil-* skills」） | 只读 |
| ours（统一仓库工作树） | `/Users/neil/Desktop/neilcodebase/neil-skills/neil-aliyun-sa` | 合并前工作树有 2026-09-21 未提交改动 → 先落成检查点提交 `c839b1d` |
| theirs（独立仓库工作树） | `/Users/neil/Desktop/neilskills/neil-aliyun-sa`（remote `git@github.com:neilluo/neil-aliyun-sa.git`，`master` @ `067bffa` 2026-08-10） | 工作树含 2026-08→09-21 未提交改动，全程只读、未写回 |

规模差：统一仓库侧 82 文件 / 独立仓库侧 431 文件。分叉自 2026-07-05，两侧各自蒸馏，**内容互有增减**（不是简单的新旧关系）。

## 2. 方法

三方合并 `git merge-file`（base = `3723a5a` 版本，ours = 检查点工作树，theirs = 独立仓库工作树），按文件类别处理：

| 类别 | 数量 | 处置 |
|---|---|---|
| 仅独立仓库侧存在 | 385 | **381 个整体并入**；4 个不入库：`.ctxdb-manifest.json`（2 字节空壳）、`scripts/__pycache__/{gate-negative-claims,run-regression}.cpython-314.pyc`（编译产物，且 `__pycache__/` 本就在 .gitignore 内）、`vibe_images/attachment-image-1.png`（434KB 孤儿截图，**全库 0 引用**——未提交，仍留在工作树待 curator 处置）|
| 仅统一仓库侧存在 | 36 | 全部保留（2026-09-21 网关专项 raw 25 + ATA 摘录 2 + 火山 4 + MCP 规范 4 + Higress 源码摘录 1） |
| 两侧都有 · 逐字相同 | 25 | 不动 |
| 两侧都有 · 自动合并干净 | 15 | 取 `git merge-file` 结果（含 `SKILL.md`、`scripts/run-regression.py`、`knowledge/aliyun-products.md`、`company-profiles.md`、`competitor-cloud.md`、`industry-landscape.md`、`architecture-templates.md` 等） |
| 两侧都有 · 有冲突 | 6 | 手工消解，共 18 个冲突块（下表） |

冲突块分布：`changelog.md` 1、`index.md` 5、`knowledge/ai-trends.md` 1、`knowledge/cloud-solutions.md` 3、`knowledge/inbox.md` 2、`tests/regression-2026-09-21.md` 6。

## 3. 四处口径裁决（撞号 / 撞名）

| # | 冲突 | 裁决 | 依据 |
|---|---|---|---|
| 1 | `cloud-solutions.md` 两侧各建了一个 `## S10`：独立仓库侧 = 企业内部知识库（员工侧 RAG），统一仓库侧 = 客户自有认证接口接入网关统一鉴权 | **RAG 保持 S10，网关场景 → S11** | 引用面：RAG 侧 54 处含回归用例 RG04 标题 + 11 份历史回归报告（不可改写的既成记录）；网关侧 33 处且全部落在 2026-09-21 当日新增内容内。S11 节开头放了编号说明 |
| 2 | `ai-trends.md` 统一仓库侧顶层新增 `## 10. 长上下文延迟治理` / `## 11. Coding Agent 工程化`，与独立仓库侧「关键追踪线」内 `### 10./### 11./### 12.` 撞号 | **顶层节 → 第13节 / 第14节**，子编号 10.x→13.x、11.x→14.x | 保持全局编号唯一；改动仅限两侧新增内容的自身标题与交叉引用，正文零改写 |
| 3 | `tests/regression-2026-09-21.md` 两侧同名异文（独立仓库侧 828 行 / v1.6 / 62 例；统一仓库侧 518 行 / v1.3→v1.4 / 32 例 + 两轮负控），互不包含 | **独立仓库侧保留原名，统一仓库侧改名 `regression-2026-09-21-apig.md`** 并在文件头加来源说明；`changelog.md` 内 3 处引用同步指向新文件名 | 历史执行记录不得互相覆盖；改名代价小于合并正文 |
| 4 | 回归用例库版本两侧各自演进（v1.4 vs v1.7） | **→ v1.8**，用例 32 ∪ 79 = 85 例 | 逐条比对 26 个共有用例：只有 T10 有差异（统一仓库侧 5 词扩到 9 词）→ 取九词超集；语料清单取独立仓库侧 23 文件超集；`run-regression.py` 取独立仓库侧版本（多 `forbidden` 否证不变量支持） |

## 4. 连带修正（同批 sweep，不留不一致消费面）

- S10→S11 消费面：`knowledge/cloud-solutions.md`（索引 2 行 + 场景节标题 + 方案使用方式 S1-S9→S1-S11）、`index.md`（知识层表 + Mermaid 节点与 4 条边 + 交叉引用表 5 行）、`knowledge/aliyun-products.md`、`knowledge/company-profiles.md`（3 处）、`knowledge/competitor-cloud.md`、`tests/regression-cases.yaml`（网关用例关键词 `S10`→`S11`，避免误命中 RAG 的 S10 造成假绿）。
- 历史原文（changelog 条目、inbox done 记录、当日回归报告正文）中的旧称 **不改写**，由编号说明与本文档兜住口径。
- `scripts/` 里 7 个脚本硬编码 `KB = Path("/Users/neil/Desktop/neilskills/neil-aliyun-sa")` → 改为 `Path(__file__).resolve().parent.parent`，否则在统一仓库里跑门禁会读错知识库。

## 5. 门禁结果

| 门禁 | 结果 |
|---|---|
| `scripts/run-regression.py`（v1.8，23 文件 / 1,165,795 字符） | ✅ **85/85 PASS，命中率 100%，`forbidden` 不变量 15 条违反 0**，退出码 0 → 报告 `tests/regression-2026-09-24.md` |
| **负控（合并专用）**：同一份 v1.8 用例库跑**合并前**语料（`c839b1d` 工作树） | ✅ **53/85 FAIL、整体命中率 46.9%、退出码 1** —— 证明新增 53 例由本次并入的内容真实驱动，门禁非空转 |
| `scripts/lint-aigw-pages.py` L1~L8 | ✅ P0/P1/P2 = 0/0/0（W 代号残留 309 处为既有登记项）；报告与独立仓库侧版本逐字一致，重跑未改写历史 |
| `scripts/check-purchase-paths.py` | ✅ PASS（采购路径核验清单结构完整，4/4 字段项通过），报告 `tests/purchase-paths-2026-09-24.md` |
| 行级完备性审计（46 个共同文件，逐行取并集校验） | ✅ 独立仓库侧共 **25 行**未逐字保留，**逐条核对全部为「被统一仓库侧更长/更正版覆盖」或「本次有意改写」**：`aliyun-products.md` 3 行（MSE「云原生网关」加了名称消歧、原 API 网关卡改题、中间件速查行区分三形态）、`cloud-solutions.md` 4 行（上下文缓存行扩写、Higress ~2,000 [推断] 行按官方价订正为 aigw.small.x1 3,997.5 并连带改合计、S1-S10→S1-S11）、`ai-trends.md` 1 行（AI Gateway(Higress) 加口径注）、`competitor-cloud.md` 1 行（火山索引行状态从「待蒸馏」更新为「部分蒸馏」）、`raw/README.md` 1 行（misc 行加「含开源代码摘录」）、`cases.yaml` version 行、`index.md` 14 行（表格行按两侧并集重写 + 改名后的 footer）。其中 `index.md` 的 `raw/aliyun-docs/` 行首稿曾压缩掉独立仓库侧的 agentcore/ai-gateway 两个 README 内容与子目录链接，**已回补为 958 字超集版**。 |
| 统一仓库侧行级核对 | 缺失行仅三类：撞号标题/引用（裁决 1-3）、被独立仓库侧超集覆盖的旧变体（如 `SKILL.md` 方案输出步骤重编号、`run-regression.py` 旧实现）、旧 Ingest 计数器行；`tests/regression-2026-09-21.md` 该路径下的 130 行为改名而非删除（→ `regression-2026-09-21-apig.md`，已逐字校验为超集） |
| 文件集 parity | ✅ 合并后工作树 = 独立仓库 431 − 剔除 4 + 统一仓库独有 36 + 本次新增 4（`regression-2026-09-21-apig.md` / `regression-2026-09-24.md` / `purchase-paths-2026-09-24.md` / 本文件）＝ **467**；入库 467 文件（`vibe_images/` 孤儿图未 add；独立仓库侧 `.ctxdb-manifest.json` 与两个 `.pyc` 亦未并入），其中 knowledge 20 / raw 367 / tests 53 / scripts 13 / references 8；独立仓库侧文件除剔除项外零丢失，统一仓库侧 36 个独有文件零丢失（逐个 `[ -f ]` 校验） |

## 6. 遗留债（合并后新增，下次 Lint 必须处理）

1. 🔴 **网关主题双写**：统一仓库侧 2026-09-21 把「云原生API网关/AI网关深度卡」写进 `aliyun-products.md`，独立仓库侧同主题已拆出 `knowledge/aliyun-ai-gateway*.md` 7 张专题页（9471 行）。同一事实两处并存 → 需做去重并页，**以专题页为主口径**。
2. 🔴 `aliyun-products.md` 现 ~3400 行，超 AGENTS.md 的 2500 行拆分阈值（合并前两侧各自已在阈值边缘）。
3. `knowledge/inbox.md` 的 Pending 列表为两侧并集，全局日期序仅尽力而为。
4. Ingest 计数器：合并后按 **24 次** 口径（独立仓库侧 22 + 统一仓库侧 09-21 的 2 轮），已严重超阈值。
4. `vibe_images/attachment-image-1.png` 全库 0 引用，建议直接删除（独立仓库里那份是同源副本）。
5. 独立仓库工作树本次为**只读**，其未提交改动仍在原处；`~/.qoder/skills/neil-aliyun-sa` 仍软链到独立仓库，如需以统一仓库为唯一真源，须另行改软链。
