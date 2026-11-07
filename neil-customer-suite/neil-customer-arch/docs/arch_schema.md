# arch.json 契约 v2（neil-kunpeng-billing 抽取归线链 → neil-customer-arch 渲染链 的唯一接口）

> 归属（2026-11-08 拆分）：本契约文档随渲染层落在 neil-customer-arch/docs/。
> 生产方 neil-kunpeng-billing/scripts/aggregate.py 产出 arch.json（引用本文件 38 处规则注释，
> 路径 `../neil-customer-arch/docs/arch_schema.md`）；消费方本 skill 的两个渲染器读 arch.json。
> 改任何字段前先改本文件，两侧同步。

版本：v2（2026-11-05，取代 v1）。变更动机：架构图改为「业务层置顶、共享/基础设施沉底、观测横贯」的组织方式；渲染器改为单文件 HTML（excalidraw 渲染器降级为可选 legacy）。

## 分层哲学（v2 核心）

```
┌ 全球边缘与加速（edge）      CDN / GA+CDT / WAF / 共享带宽 / 证书 / 无标签EIP池
├ 业务层（lines，置顶）        每条产品线一泳道：入口 | 计算 | 数据(含消息) 三列
│                             ＋ 观测横条（observe，贯穿三列：SLS project/logstore、PROM、DAS）
├ 平台共享层（shared）         统一入口 APIGW | context/记忆 | 模型路由 | 共享计算池 ＋ 观测横条
└ 基础设施（infra，沉底）      核心库 | 消息流 | 分析同步 | 治理注册 | 容器网络 ＋ 可观测底座横条
```

依据：业务层是价值交付面（客户视角自上而下）；共享层与基础设施是支撑面；观测天然是横切关注点（同一 SLS project/PROM 服务该泳道的入口、计算、数据三块），故在泳道内做横条而非第四列。

## 顶层结构

```json
{
  "meta": {"customer","brand","cid","uid","account","months","months_complete",
           "generated_at","sources","schema_version":"v2"},
  "summary_flow": ["全球用户","边缘加速 CDN/GA/WAF","业务层 入口→计算→数据",
                   "平台共享层 APIGW/context/模型路由","基础设施 数据/消息/治理"],
  "edge":   {"name":"全球边缘与加速","comps":[<COMP>],"note":"…"},
  "lines":  [<LINE>],
  "shared": <SHARED>,
  "infra":  <INFRA>,
  "cross_links": [{"from":"<comp_id>","to":"<comp_id>","label":"…","kind":"data|ai|msg"}]
}
```

## LINE（业务泳道）

```json
{"id":"enter","name":"Enter Pro（生应用/网页）","group":"enter-prod",
 "attribution":"resource_group","vpc":"vpc-…","color":"enter","cost_month":13193,
 "layers":{"入口":[<COMP>],"计算":[<COMP>],"数据":[<COMP>]},
 "observe":[<COMP>],
 "risks":[{"level":"P0|P1|P2","target":"<comp_id>","text":"…"}]}
```

- layers 固定三键；消息类 COMP（ons/alikafka 实例归属本泳道者）并入「数据」列，渲染列标题显示为「数据 / 消息」。
- observe：该泳道横切观测组件（kind ∈ sls/prom/cms/arms/hdm 且归线到本泳道者）。
- 顺序：lines 数组顺序即渲染顺序（enter, framia, game, concat, work, anycap）。

## SHARED / INFRA

```json
shared = {"name","group","cost_month",
  "layers":{"入口":[…],"计算":[…],"数据":[…],"AI":[…]},
  "observe":[…]}
infra  = {"name","group","cost_month",
  "layers":{"核心库":[…],"消息流":[…],"分析同步":[…],"治理注册":[…],"容器网络":[…]},
  "observe":[…]}   // 可观测底座：PROM/企业云监控/ARMS/OTel/k8s-log SLS
```

## COMP（不变，沿用 v1）

```json
{"id","kind","name","evidence","spec","cost","note"}
```
kind 词表沿用 v1（nlb,clb,apigw,eip,cdn,ga,waf,fc,acs,ack,sae,supabase,rds,redis,tair,
mongo,es,clickhouse,adbpg,oss,nas,kafka,rocketmq,dts,maxcompute,bailian,model_ext,
memory,sls,prom,cms,arms,nacos,sentry,other）。

## 归线/分块规则（neil-kunpeng-billing/scripts/aggregate.py v2 内置）

1. v1 归线规则 1-4 全部保留（资源组→命名→VPC→SLS→kind；Supabase 池折叠；完整月均值）。
2. 观测剥离：kind ∈ {sls,prom,cms,arms,hdm} 的 COMP 从 layers 移入所属 line/shared/infra 的 observe。
3. edge 提取：无组标签且 kind ∈ {cdn,ga,waf,cbwp,cas} 或（kind=eip 且无组标签）→ edge；
   有组标签/CREATE_BY_NLB 的 EIP 留在所属泳道入口。
4. infra 列映射（infra 组内）：rds/kvstore/mongo→核心库；alikafka/ons/eventbridge→消息流；
   gpdb/dts/odps→分析同步；mse/dms/ecs(ADDC)/hbr/cas?→治理注册（cas 已去 edge）；
   ack(clb 托管)/nat/ntr/privatelink/pvtz/disk/ecs(其余)→容器网络。
5. shared 列映射：apigw→入口；acs/ack 共享池与未归线 fc 族（wagt/work-runtime）→计算；
   adbpg(context)/oss/rds/tair/记忆池→数据；bailian/model_ext/memory/护栏→AI。
6. 折叠阈值沿用 v1（每列 ≤12、长尾「其他 ×N」）；observe 横条不折叠上限但 >8 条折「其他」。
7. comp id 规则：`<line>_<col>_<slug>`，col ∈ access|compute|data|ai|core|msg|ana|gov|net|edge；
   observe 内 comp id 用 `<line>_obs_<slug>`。cross_links/risks 的 target 必须随 id 迁移同步更新
   （neil-kunpeng-billing/internal/cross_links_kunqi.json、neil-kunpeng-billing/internal/risks_kunqi.json，
   gitignored 真数据；由 aggregate.py `--risks` 与 payload `meta.rules` 消费，渲染层不直接读）。

## 渲染约定（render_arch_html.py）

- 单文件 HTML，CSS grid；edge 顶带 → lines 泳道 → shared → infra 顺序纵向排布。
- 泳道内：三列等宽 grid；observe 横条置于三列下方、泳道内全宽，浅灰底＋虚线上边框。
- cross_links 不画 SVG 箭头：在源泳道底部渲染依赖 chip「⤓ <label> → <目标泳道名>」，
  目标为 shared/infra 时 chip 指向对应带名。
- 风险 badge 贴卡片右上角：P0 红 / P1 橙 / P2 黄；泳道头显示 name + group + 月均成本。
- 颜色沿用 v1 渲染器 LINE_COLORS 七键（palette 出处见 render_excalidraw_arch.py 头注）。
