# AGENTS.md — neil-customer-arch 工作手册

> 拆分（2026-11-08）：本 skill 从原 neil-kunpeng-expert 拆出，只管**渲染层**。
> 账单抽取 + 归线（产出 arch.json）在 [../neil-kunpeng-billing](../neil-kunpeng-billing/AGENTS.md)。
> arch.json 契约文档 [docs/arch_schema.md](docs/arch_schema.md) 随本 skill 落地，是唯一接口，
> 改字段前先在契约改、两侧（aggregate 产出 / 渲染消费）同步。
> 下列条文原为 neil-kunpeng-expert AGENTS.md 第 10-13（Excalidraw 渲染）、
> 第 16-22（架构组织与渲染 v2 / 对客脱敏），拆分后归此，重编号为 1-11。

## 架构组织与渲染（v2，2026-11-05 用户拍板）
1. 架构图主渲染器是 render_arch_html.py（单文件 HTML）；excalidraw 渲染器降级为 legacy 可编辑源，仅按需使用。
2. 层级顺序固定：edge 全球边缘顶带 → 业务泳道（lines 置顶）→ 平台共享层 → 基础设施沉底。业务/共享/基建的价值层级自上而下，禁把 infra 放上面。
3. 泳道内三列「入口｜计算｜数据/消息」；观测是横切关注点，做泳道内全宽横条（observe），禁做第四列。infra 五列（核心库/消息流/分析同步/治理注册/容器网络）＋可观测底座横条。
4. 跨泳道依赖在 HTML 里用源泳道底部依赖 chip 表达（⤓ label → 目标泳道名），不画 SVG 箭头；excalidraw legacy 用右缘 trunk 自由箭头（第 6-7 条）。
5. arch.json schema 版本以 meta.schema_version 为准（当前 v2）；渲染器只认 v2，遇 v1 输入直接报错退出，禁静默兼容。

## Excalidraw 渲染（render_excalidraw_arch.py，legacy）
6. **cross_links 绘制块必须位于全局 normalize 平移之后**：normalize 会平移全部元素，之前绘制则 trunk 坐标过期、竖线穿泳道。
7. **cross_links 箭头不绑定（startBinding/endBinding=None）**：绑定箭头会被渲染器按 focus/gap 重路由，覆盖手工 Manhattan 点。跨泳道依赖用泳道级 trunk 路由（竖线只走所有泳道右侧白边，每 link 偏移 8px；横线只走泳道外缘白边段）。arrow() 契约：x/y 为锚点绝对坐标、points 为相对偏移，调用方负责换算；arrow() 内禁二次归一化（会把绝对 x/y 抹零）。
8. **legacy 未对齐 v2（2026-11-08 实测钉死）**：render_excalidraw_arch.py 的 LAYER_ORDER 仍是 v1 六列
   （接入/计算/数据/消息/AI/观测），喂 aggregate 真实 v2 产出（infra 五列：核心库/消息流/分析同步/治理注册/
   容器网络）时 infra 卡片**静默丢失**（不报错）。aggregate 只产 v2 → 需要 Excalidraw 可编辑源时
   **必须先升级 LAYER_ORDER 对齐 v2 再用**，禁直接喂 arch.json 拿残缺图。tests/test_render.py 的
   TestLegacyV2Gap 把此缺口钉成显式信号：升级后那两条用例自动变红，提醒删类补正向用例。

## 对客材料红线与交付
9. **对客材料红线**：render_arch_html.py **默认即对客脱敏**（隐全部金额/UID/CID/schema/生成时间，evidence 内 UID 掩码 •••，折叠术语改写）；带成本须显式 `--internal`，且自动加红色「内部版：禁止对客外发」横幅。交付前 grep 校验对客件「¥/月均/UID/CID」零命中。
10. **交付目录分层**：对客目录顶层只放脱敏件；一切带钱/带 UID 的产物（内部版 HTML、excalidraw、PNG、analysis/promo-guard md、arch/rg_links/bill_instances json）一律放 `internal/` 子目录，禁与对客件混放同层——混放是误发根因。
11. 渲染验证闭环：render_arch_html.py 出 HTML → Read/浏览器目检 → 修 → 重渲染；excalidraw 出 PNG → Read 目检 → 修 → 重渲染；禁只凭 JSON 宣称完成。官方渲染器超像素上限时用 sips -Z 3400 缩放后分段目检。
12. **测试 fixture 用 tracked 脱敏孪生，且两渲染器各喂各的契约**：tests/test_render.py 读 tests/fixtures/ 下两份脱敏 fixture——arch_fixture.json（v1 六列结构，喂 legacy excalidraw）、arch_fixture_v2.json（v2，对齐 aggregate 真实产出，喂 HTML 主渲染器）。禁指向 gitignored 的 internal/ 真数据（clean clone 会 FileNotFoundError 且渲染测试不该依赖敏感数据）；禁拿 v1 fixture 喂 v2 主渲染器（列名不匹配会静默丢卡，已被 test_cli_rejects_real_v1_fixture 与 TestLegacyV2Gap 钉死）。
