# AGENTS.md — neil-kunpeng-expert 工作手册

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

## Excalidraw 渲染（render_excalidraw_arch.py）
10. **cross_links 绘制块必须位于全局 normalize 平移之后**：normalize 会平移全部元素，之前绘制则 trunk 坐标过期、竖线穿泳道。
11. **cross_links 箭头不绑定（startBinding/endBinding=None）**：绑定箭头会被渲染器按 focus/gap 重路由，覆盖手工 Manhattan 点。跨泳道依赖用泳道级 trunk 路由（竖线只走所有泳道右侧白边，每 link 偏移 8px；横线只走泳道外缘白边段）。
12. arrow() 契约：x/y 为锚点绝对坐标、points 为相对偏移，调用方负责换算；arrow() 内禁二次归一化（会把绝对 x/y 抹零）。
13. 渲染验证闭环：render_excalidraw.py 出 PNG → Read 目检 → 修 → 重渲染；禁只凭 JSON 宣称完成。官方渲染器超像素上限时用 sips -Z 3400 缩放后分段目检。

## 交付与协作
14. 过程文件只落 /tmp/kunqi-bill-arch/；交付副本放 ~/Desktop/kunqi-bill-arch/ 与工作区投递；neil-skills 仓库内只留 skill 源码与测试。
15. 换客户复用：归线规则串（VPC/SLS/命名）是坤启实测值，必须经 --rules 覆盖，禁改脚本默认值。

## 架构组织与渲染（v2，2026-11-05 用户拍板）
16. 架构图主渲染器是 render_arch_html.py（单文件 HTML）；excalidraw 渲染器降级为 legacy 可编辑源，仅按需使用。
17. 层级顺序固定：edge 全球边缘顶带 → 业务泳道（lines 置顶）→ 平台共享层 → 基础设施沉底。业务/共享/基建的价值层级自上而下，禁把 infra 放上面。
18. 泳道内三列「入口｜计算｜数据/消息」；观测是横切关注点，做泳道内全宽横条（observe），禁做第四列。infra 五列（核心库/消息流/分析同步/治理注册/容器网络）＋可观测底座横条。
19. 跨泳道依赖在 HTML 里用源泳道底部依赖 chip 表达（⤓ label → 目标泳道名），不画 SVG 箭头；excalidraw legacy 用右缘 trunk 自由箭头（AGENTS 10-12 条仍有效）。
20. arch.json schema 版本以 meta.schema_version 为准（当前 v2）；渲染器只认 v2，遇 v1 输入直接报错退出，禁静默兼容。
21. **对客材料红线**：render_arch_html.py **默认即对客脱敏**（隐全部金额/UID/CID/schema/生成时间，evidence 内 UID 掩码 •••，折叠术语改写）；带成本须显式 `--internal`，且自动加红色「内部版：禁止对客外发」横幅。交付前 grep 校验对客件「¥/月均/UID/CID」零命中。
22. **交付目录分层**：对客目录顶层只放脱敏件；一切带钱/带 UID 的产物（内部版 HTML、excalidraw、PNG、analysis/promo-guard md、arch/rg_links/bill_instances json）一律放 `internal/` 子目录，禁与对客件混放同层——混放是误发根因。
