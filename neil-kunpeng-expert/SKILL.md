---
name: neil-kunpeng-expert
description: 从阿里内部鲲鹏/devata 体系（CRM360 账号360 + usercenter2 费用账单）稳定抽取某客户 UID 的实例级账单数据，按资源组分离 + 命名/VPC/SLS/kind 旁证归线还原客户云上架构，产出结构化 arch.json（含成本月均、分层组件、大促风险清单），供画架构图与大促保障分析。当用户提到 鲲鹏 / devata / 账单抽取 / 客户架构还原 / 大促保障 / 资源组分离 / 实例级账单 / CRM360 / usercenter2 / 还原某客户云架构 / 从账单画架构图 时使用。
---

# neil-kunpeng-expert

从阿里内部账单系统把一个客户的云架构「抽出来、归好线、算清成本」。核心洞察：**实例级账单天然携带架构信息**
（实例 ID/昵称/规格/配置串含 VPC 与可用区/资源组/标签/计费项），做「产品语义映射 + 资源组分离 + 命名聚类」
就能还原产品组合、部署拓扑、业务线划分与成本分层——无需控制台/CMDB。

- **输出契约**：[docs/arch_schema.md](docs/arch_schema.md)（aggregate.py 产出、渲染侧消费的**唯一接口**，改任何字段前先改它）。
- **接口备忘**：[references/kunpeng-apis.md](references/kunpeng-apis.md)（两系统 endpoint、参数、tableType、CSRF 提取法、6 个坑、能力边界）。
- **客户视角修正**：[references/customer-view-kunqi.md](references/customer-view-kunqi.md)（坤启客户会议确认的账单不可见层：CF 上游/中台 Credit/net 枢纽 VPC/Lab 同柱/重保事实；对客画图时客户口径优先于账单推断）。
- **风险清单示例**：[config/risks_kunqi.json](config/risks_kunqi.json)（坤启/Converge AI 本会话实测结论）。
- **零第三方依赖**：Python 只用标准库，浏览器侧只用原生 fetch。

## 工作流（四步 + 可选渲染）

### 步骤 1 —— 浏览器接通 usercenter2

数据只能从**已登录的浏览器会话**里拿（cookie 鉴权 + 内联 CSRF token，curl 拿不到）。

1. devata「我的客户」→ 客户详情（拿 CID）→「账号360」跳 CRM360 →「账单信息」Tab →「实例级账单明细」跳到 **usercenter2**。
2. 打开一个 **usercenter2 域内**的页签：`https://usercenter2.aliyun-inc.com/bill/consumeReport?uid=<UID>&startMonth=<YYYYMM>&endMonth=<YYYYMM>`。
3. ⚠ **必须在 usercenter2 域执行 fetch**：crm360 与 usercenter2 跨域不通，商品级也改走 usercenter2 的 `PRODUCT_CONSUME_MONTH`（crm360 接口只作备查，见 references §1）。

### 步骤 2 —— 起本地接收服务

浏览器 console 里的 payload 无法直接写本地文件，用 recv_server.py 落地：

```bash
python3 scripts/recv_server.py --port 8732 --out-dir /tmp/<customer>-bill-arch
```

只绑 127.0.0.1、CORS 全开、POST 路径即文件名、tmp+rename 原子写（重跑覆盖幂等）、文件名做 basename + 后缀白名单校验（拒路径穿越）。

### 步骤 3 —— console 粘贴 fetch_bills.js 抽取

把 [scripts/fetch_bills.js](scripts/fetch_bills.js) 整段粘进 usercenter2 页签 console 回车。脚本按 `CONFIG` 驱动：

```js
const CONFIG = {
  uid: '1077748325118640',                 // 客户 UID（loginUserId）
  months: ['202609', '202610', '202611'],   // 要拉的账期（跨月逐月并集）
  monthsComplete: ['202609', '202610'],     // 参与月均的完整月（残缺月只进证据）
  groups: ['enter-prod', 'framia-prod', 'game-prod', 'concat-prod',
           'work-prod', 'anycap-prod', 'converge-prod', 'infra-prod'],
  products: ['rds', 'kvstore', 'mongodb', 'elasticsearch', /* …全量产品码… */ 'sae', 'edas'],
  saturation: ['fc', 'gpdb', 'acs'],        // 行数巨大的产品走「实例根」饱和抽样
  satMaxPages: 12, satIdleStop: 2, pageSize: 500,
  endpoint: '/bill/queryMonthConsumeReport',
  recvUrl: 'http://127.0.0.1:8732/bills_raw.json',
  concurrency: 3, delayMs: 120,
};
```

脚本做的事：自动从页面 HTML 正则提取 X-CSRF-TOKEN → 逐月×逐产品拉 INSTANCE（分页 500）→ saturation 产品走饱和抽样（逐页提根，连续 2 页无新增即停，最多 12 页）→ 逐月×逐资源组拉 group → 逐月拉 PRODUCT/ACCOUNT 级 → 组装 `{meta, instance_rows, group_rows, product_rows, saturation, failures, progress}` 一次性 POST 到 recv_server。有进度 `console.log`、单产品失败不中断（记入 `failures`）、重跑覆盖幂等；回传失败兜底存 `window.__kunpeng_payload`。

### 步骤 4 —— aggregate 出 arch.json

```bash
python3 scripts/aggregate.py \
  --in /tmp/<customer>-bill-arch/bills_raw.json \
  --out /tmp/<customer>-bill-arch/arch.json \
  --months-complete 202609,202610 \
  --risks config/risks_kunqi.json
```

按 docs/arch_schema.md 的归线规则产出 arch.json：资源组直接命中 → 命名前缀/标签 → VPC → SLS project → kind 兜底；
月均只算完整月；`instance_rows`/`group_rows` 用 hashKey 去重（否则金额翻倍）；饱和抽样族基数进 `name`、`cost=null`；
无实例维度产品（sae/prometheus/…）由 product_rows 补 COMP；风险按 target/evidence 解析到真实 comp id，解析不到落 `meta.unresolved_risks` 并 warn。
换客户时用 `--rules rules.json` 或 payload `meta.rules` 覆盖命名/VPC/SLS 规则（默认值是坤启实测串）。

### 步骤 5 —— 渲染架构图（HTML 主路径）

arch.json（schema v2）喂给 `scripts/render_arch_html.py` 产出单文件 HTML 架构图：

```bash
python3 scripts/render_arch_html.py /tmp/<customer>-bill-arch/arch.json \
  -o /tmp/<customer>-bill-arch/arch.html
```

布局（v2，docs/arch_schema.md）：summary_flow 链 → edge 全球边缘顶带 → 业务泳道置顶
（每道「入口｜计算｜数据/消息」三列 ＋ 观测横条贯穿 ＋ 依赖 chips）→ 平台共享层 → 基础设施沉底
（核心库｜消息流｜分析同步｜治理注册｜容器网络 五列 ＋ 可观测底座横条）；risks 贴 P0/P1/P2 badge。

legacy：`scripts/render_excalidraw_arch.py` 仍可用（v1 六列泳道 + 右缘 trunk 箭头），
仅在需要 Excalidraw 可编辑源时使用；其 fixture 测试保留。

## 六个坑（务必先看，references/kunpeng-apis.md §3 有完整版）

1. **跨域不通**：crm360 与 usercenter2 互不能 fetch。所有请求（含商品级）都在 **usercenter2 域内页签**执行。
2. **default 组报 `INSTANCE_NUM_TOO_LARGE`**：默认组实例数超限。必须按 pipCode 或 resourceGroup 分片，从不查 default 组。
3. **部分产品无实例维度**：sae/prometheus(cms)/cbs/xtrace 等 INSTANCE 查询 `total=0`，只能走 PRODUCT 级取证。
4. **高基数产品全拉不现实**：fc 7 万行 / gpdb 3 万行 / acs 6 千行。用「实例根」饱和抽样（fc=functions/ 名去尾 hash，gpdb=分号前段，acs=前 16 字符；连续 2 页无新根即停，最多 12 页）。
5. **资源组下拉是 datalist 懒加载**，但 API 的 `resourceGroup` 参数直接传组名字符串即可（如 `'enter-prod'`），不必先在 UI 选中。
6. **当月可能是残缺月**（只出账到某天）：月均成本只算完整月（`--months-complete`），残缺月只进证据不进均值。

补充：`filterZeroBills=false` 必须开（否则漏掉在用但 0 元的组件，那些是架构存在性证据）；同一 pipCode 商品级/实例级口径有差异，以实例级为准。

## 能力边界

能还原：产品组合全景、实例清单与规格、部署拓扑（地域/VPC/可用区）、环境-业务线划分、数据同步链路（DTS 对）、成本分层。
还原不出（需控制台/OpenAPI/链路数据补）：VPC 子网划分、安全组规则、服务间调用关系、SLS logstore 完整清单、SAE 应用清单、Pod 级瞬时拓扑。详见 references §5。

## 测试

```bash
python3 tests/test_aggregate.py     # 标准库 unittest，自造 fixture 覆盖归线/月均/饱和抽样/去重/风险挂接
```
