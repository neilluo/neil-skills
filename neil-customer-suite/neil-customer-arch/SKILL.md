---
name: neil-customer-arch
description: 把 arch.json（schema v2）渲染成客户云架构图。输入是 neil-kunpeng-billing 归线产出的 arch.json（也可来自任何符合 arch_schema v2 的生产者），输出单文件 HTML 架构图（主路径，默认对客脱敏）或 Excalidraw 可编辑源（legacy）。仅用户主动要求画架构图/渲染 arch.json/出对客架构图时触发；账单抽取与归线走 neil-kunpeng-billing，每日资源快照与客户动态走 neil-customer-radar。当用户提到 画架构图 / 渲染架构图 / arch.json 出图 / 客户架构图 / 对客架构图 / Excalidraw 架构图 / 云架构图 时使用。
---

# neil-customer-arch

> 定位（2026-11-08 从 neil-kunpeng-expert 拆出）：本 skill 是**渲染层**，只消费 arch.json
> （schema v2）、产出架构图，**不抽账单、不归线**。arch.json 由同套件
> [neil-kunpeng-billing](../neil-kunpeng-billing/SKILL.md) 的 aggregate.py 产出（也可来自任何
> 符合契约的生产者）。契约文档 [docs/arch_schema.md](docs/arch_schema.md) 随本 skill 落地，
> 是唯一接口，改任何字段前先改它、两侧同步。
> 纯标准库、零第三方依赖；渲染器只认 v2，遇 v1 输入直接报错退出，禁静默兼容。

把一份 arch.json 画成客户能看懂的云架构图。两种产物：

- **HTML 主路径**（render_arch_html.py）：单文件 HTML，内联 CSS 无外链，默认即对客脱敏。
- **Excalidraw legacy**（render_excalidraw_arch.py）：可编辑源，仅在需要 Excalidraw 时按需使用。

- **输出契约**：[docs/arch_schema.md](docs/arch_schema.md)（v2，aggregate 产出 / 渲染消费的唯一接口）。
- **渲染条文**：[AGENTS.md](AGENTS.md)（层级顺序、泳道布局、跨泳道依赖表达、对客脱敏红线、交付目录分层）。

## 渲染流程

### 主路径 —— HTML 架构图

```bash
# 对客脱敏（默认）：隐全部金额/UID/CID/schema/生成时间，evidence 内 UID 掩码 •••
python3 scripts/render_arch_html.py /tmp/<customer>-bill-arch/arch.json \
  -o /tmp/<customer>-bill-arch/arch.html

# 内部版（带成本/UID/CID）：显式加 --internal，自动加红色「内部版：禁止对客外发」横幅
python3 scripts/render_arch_html.py /tmp/<customer>-bill-arch/arch.json \
  -o /tmp/<customer>-bill-arch/internal/arch.html --internal
```

布局（v2，见 docs/arch_schema.md）：summary_flow 链 → edge 全球边缘顶带 → 业务泳道置顶
（每道「入口｜计算｜数据/消息」三列 ＋ 观测横条贯穿 ＋ 依赖 chips）→ 平台共享层 → 基础设施沉底
（核心库｜消息流｜分析同步｜治理注册｜容器网络 五列 ＋ 可观测底座横条）；risks 贴 P0/P1/P2 badge。

### legacy —— Excalidraw 可编辑源

```bash
python3 scripts/render_excalidraw_arch.py /tmp/<customer>-bill-arch/arch.json \
  -o /tmp/<customer>-bill-arch/arch.excalidraw
```

v1 六列泳道 + 右缘 trunk 箭头；跨泳道依赖用泳道级 trunk 路由（AGENTS.md 第 6-7 条）。

⚠ **legacy 未对齐 v2**（AGENTS.md 第 8 条）：其 LAYER_ORDER 仍是 v1 六列，直接喂 aggregate
真实 v2 产出会**静默丢掉 infra 五列的卡片**（不报错）。需要 Excalidraw 可编辑源时，必须先升级
LAYER_ORDER 对齐 v2 再用。

## 对客脱敏红线（务必先看）

render_arch_html.py **默认即对客脱敏**：隐全部金额/UID/CID/schema/生成时间，evidence 内 UID 掩码 •••，
折叠术语改写。带成本须显式 `--internal`，且自动加红色「内部版：禁止对客外发」横幅。
**交付前必须 grep 校验对客件「¥/月均/UID/CID」零命中**（AGENTS.md 第 9 条）。
一切带钱/带 UID 的产物一律放 `internal/` 子目录，禁与对客件混放同层——混放是误发根因（第 10 条）。

## 测试

```bash
python3 tests/test_render.py      # 26 例，stdlib unittest；两份 tracked 脱敏 fixture，两渲染器各喂各的契约
```

两份 fixture 不可混用（AGENTS.md 第 12 条）：`arch_fixture.json` 是 v1 六列结构，喂 legacy
excalidraw；`arch_fixture_v2.json` 对齐 aggregate 真实 v2 产出，喂 HTML 主渲染器。
TestHtmlRenderer 覆盖主渲染器的概览链、脱敏红线、v2 列完整性、层级顺序、chip 依赖、
v1 输入拒绝、横幅；TestLegacyV2Gap 把 legacy 未对齐 v2 的缺口钉成显式信号。

渲染 e2e 目检闭环：render_arch_html.py 出 HTML → 浏览器/Read 目检 → 修 → 重渲染；禁只凭 JSON 宣称完成。
Excalidraw 官方渲染器超像素上限时用 sips -Z 3400 缩放后分段目检。
