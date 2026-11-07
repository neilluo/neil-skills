# AGENTS.md — neil-kunpeng-billing 工作手册

> 拆分（2026-11-08）：原 neil-kunpeng-expert 拆为两半——本 skill 只管**账单抽取 + 归线**，
> 产出 arch.json（schema v2）即止；渲染层（render_arch_html.py / render_excalidraw_arch.py）
> 与渲染相关条文（原第10-13条 Excalidraw、第16-22条 架构组织与渲染v2/对客脱敏）已搬去
> [../neil-customer-arch/AGENTS.md](../neil-customer-arch/AGENTS.md)。arch.json 契约文档随渲染层落在
> [../neil-customer-arch/docs/arch_schema.md](../neil-customer-arch/docs/arch_schema.md)，改字段两侧同步。

## 数据抽取（鲲鹏/devata 账单）
1. 实例级账单唯一金矿是 usercenter2 `POST /bill/queryMonthConsumeReport`（tableType=INSTANCE_CONSUME_MONTH/PRODUCT_CONSUME_MONTH/ACCOUNT_CONSUME_MONTH）；CRM360 `getBillDetailList.json` 只有商品级，仅作快速预览。fetch 必须在 usercenter2 域内页签执行（跨域不通）。
2. CSRF token 从页面 HTML 的 `setRequestHeader('X-CSRF-TOKEN', ...)` 正则提取；cookie 会话鉴权，无 token 参数。
3. `default resource group` 查询必报 INSTANCE_NUM_TOO_LARGE：按 pipCode 或 resourceGroup 分片，禁全量。
4. fc/gpdb/acs 行数 6 千~7 万：用"实例根"饱和抽样（连续 2 页无新根即停，上限 12 页），禁全拉。
5. sae/prometheus/cbs/xtrace/alimt/cbwp 无实例维度（INSTANCE 查询 total=0）：只能 PRODUCT 级取证，图上标"产品级证据"。
6. 残缺月（出账未到月末）只进证据不进月均；--months-complete 显式声明完整月。

## 归线与折叠（aggregate.py）
7. 资源组只覆盖有状态面；计算/模型面无组标签，按 命名前缀→VPC→SLS project→kind 顺序旁证归线，归线依据写进 comp.attribution。
8. 每层 COMP ≤12、全图 ≤120：fc 按函数族折、eip/cdt 无组标签归 infra、ecs 按规格族折、sls 按 project 折、长尾进"其他 ×N"。折叠规则改动必须同步 tests/test_aggregate.py 用例。
9. comp id 确定性（line+layer+族slug）；cross_links 与 risks 的 target 必须解析到真实 comp id，未解析进 meta.warnings 且 CI 视为失败。
10. arch.json schema 版本以 meta.schema_version 为准（当前 v2）；aggregate.py 只产 v2，v1 归线规则 1-4 已在 v2 内保留（见 arch_schema.md「归线/分块规则」节）。

## 交付与协作
11. 过程文件只落 /tmp/kunqi-bill-arch/；交付副本放 ~/Desktop/kunqi-bill-arch/ 与工作区投递；neil-skills 仓库内只留 skill 源码与测试。
12. 换客户复用：归线规则串（VPC/SLS/命名）是坤启实测值，必须经 --rules 覆盖，禁改脚本默认值。
13. internal/ 真数据（risks_kunqi.json / cross_links_kunqi.json / customer-view-kunqi.md / 真坤启 arch_fixture.json）一律 gitignored，PUBLIC 红线禁入库；tests/test_aggregate.py 对 internal/ 用 `@skipUnless` 守卫，clean clone 上自动 skip 不崩。
