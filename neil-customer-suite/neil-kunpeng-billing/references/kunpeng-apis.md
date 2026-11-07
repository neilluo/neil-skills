# 鲲鹏 / devata 账单体系接口备忘（neil-kunpeng-billing）

> 本文件是「怎么把数据拿下来」的备忘；「拿到之后怎么组织」看 [../../neil-customer-arch/docs/arch_schema.md](../../neil-customer-arch/docs/arch_schema.md)。
> 所有内网 endpoint 均需 cookie 会话鉴权（浏览器已登录状态），无法用 curl 直接调。

## 0. 入口链路

```
devata「我的客户」
  → 客户详情页（cid）
    → 「账号360」跳转 CRM360：https://crm360.aliyun-inc.com/…?cid=<CID>
      → 「账单信息」Tab
        ├─ 结算单明细（商品级）      → crm360 /bill/getBillDetailList.json
        └─ 实例级账单明细（跳转）    → usercenter2 /bill/queryMonthConsumeReport  ← 金矿在这
```

URL 模板：

| 用途 | 模板 |
|---|---|
| CRM360 账号360 | `https://crm360.aliyun-inc.com/#/customer/360?cid=<CID>` |
| CRM360 商品级结算单 | `https://crm360.aliyun-inc.com/bill/getBillDetailList.json?uid=<UID>&pageSize=200&currentPage=1&chargeType=postpay&startMonth=<YYYYMM>&endMonth=<YYYYMM>` |
| usercenter2 实例级账单页 | `https://usercenter2.aliyun-inc.com/bill/consumeReport?uid=<UID>&startMonth=<YYYYMM>&endMonth=<YYYYMM>` |
| usercenter2 查询接口 | `POST https://usercenter2.aliyun-inc.com/bill/queryMonthConsumeReport` |

坤启实测值：见套件 `../../config/customers.json` 的 `customers[kunqi].devata`（cid/uid/account 单一事实源，本文档不留第二份拷贝）。

## 1. CRM360 商品级（只作备查，脚本不用）

```
GET /bill/getBillDetailList.json
  ?uid=<UID>&pageSize=200&currentPage=1
  &chargeType=postpay            # postpay | prepay | 全量
  &startMonth=202611&endMonth=202611
```

- 返回：`data.list[]`，字段 `productCode` / `commodityName` / `requireAmount`（应付）/ `orderId` / `pretaxGrossAmount` 等。
- 用途：快速看产品组合与金额排序（几十行），**没有实例维度**。
- ⚠ 与 usercenter2 **跨域不通**：在 crm360 页签里 fetch usercenter2 会被 CORS 拦，反之亦然。
  所以 `scripts/fetch_bills.js` 全部走 usercenter2 域，商品级改用 `PRODUCT_CONSUME_MONTH` 替代。

## 2. usercenter2 实例级（核心）

```
POST /bill/queryMonthConsumeReport
Content-Type: application/json
X-CSRF-TOKEN: <从页面提取，见 §2.1>

{
  "loginUserId": "<UID>",
  "startMonth": "202611",
  "endMonth": "202611",
  "pipCode": "rds",                 // 可选：产品码过滤
  "pipCodeFilter": "IN",
  "commodityCodeFilter": "IN",
  "resourceGroup": "enter-prod",    // 可选：直接传组名字符串
  "tableType": "INSTANCE_CONSUME_MONTH",
  "filterZeroBills": false,         // 必须 false
  "currentPage": 1,
  "pageSize": 500                   // 上限 500
}
```

### 2.1 CSRF token 提取法

token 内联在该页 HTML 的 `beforeSend → setRequestHeader` 里，不在 meta/cookie。脚本用正则从
`document.documentElement.outerHTML` 提取，按优先级试四条：

```js
/X-CSRF-TOKEN['"]\s*,\s*['"]([^'"]+)['"]/i
/setRequestHeader\(\s*['"]X-CSRF-TOKEN['"]\s*,\s*['"]([^'"]+)['"]\s*\)/i
/['"]csrfToken['"]\s*[:=]\s*['"]([^'"]+)['"]/i
/X-CSRF-TOKEN['"]?\s*[:=]\s*['"]([^'"]+)['"]/i
```

兜底：`meta[name=csrf-token]` → cookie `XSRF-TOKEN`。提不到就 warn 但继续（可能 403）。

### 2.2 tableType 取值

| tableType | 粒度 | 用途 |
|---|---|---|
| `INSTANCE_CONSUME_MONTH` | 实例 × 计费项 | **核心**。字段最全，含配置串/标签/资源组/IP |
| `PRODUCT_CONSUME_MONTH` | 产品 × 商品 | 替代 crm360 商品级；补无实例维度产品；对账合计 |
| `ACCOUNT_CONSUME_MONTH` | 账号 × 结算通道 | 全账号合计校验（**不参与产品级对账，会重复计**） |

### 2.3 接口语义

- `startMonth === endMonth` = 单月查询。**跨月要逐月发请求再并集**（传区间会拿到聚合/报错，口径不清）。
- 分页：`pageSize <= 500`，`total` 给总行数；末页判定用 `list.length < pageSize`。
- 响应壳可能是 `{data:{list,total}}` / `{data:[...]}` / `{list,total}`，脚本三种都兼容。

### 2.4 INSTANCE 级行字段

| 字段 | 含义 | 架构还原价值 |
|---|---|---|
| `instanceId` | 实例 ID（常带 `;地域;计费维度` 后缀） | 分号前段 = 实例根 |
| `instanceNick` | 实例昵称 | **命名归线主证据**（如 `game-rec-prod`、`credit-prod`） |
| `instanceSpec` | 规格（如 `redis.shard.with.proxy.large.ce`） | 容量/档位判断 |
| `instanceAllocation` | 配置串 | **金矿**：`网络类型:专有网络;可用区:ap-southeast-1b;系列:高可用版;存储空间:500GB;…` |
| `region` / `zoneName` | 地域 / 可用区名 | 部署拓扑；单可用区 = 单点风险 |
| `internetIp` / `intranetIp` | 公网 / 私网 IP | 出口面识别 |
| `resourceGroupName` | 资源组 | **归线规则 1**（直接命中） |
| `instanceTag` | 标签串 `key:project value:enter; key:biz_id value:coding; key:env value:prod` | 业务线/环境归线 |
| `commodityName` | 商品名 | kind 细分（Tair vs Redis、NLB vs CLB） |
| `pipCode` | 产品码 | kind 主依据 |
| `chargeType` | `postpay` / `prepay` | 包月摊销 vs 按量弹性 |
| `requireAmount` | 应付金额（元） | 成本 |
| `resName` | 资源名 | 辅助命名 |
| `hashKey` | 行唯一键 | **去重键**（group_rows 与 instance_rows 覆盖同一批行） |

配置串正则提取：`VPC` → `/vpc-[0-9a-z]{6,}/`；`可用区` → `/可用区[:：]([^;]+)/`；
标签 project → `/key:\s*project\s+value:\s*([^;\s]+)/i`。

## 3. 六个坑（本会话实测）

1. **跨域不通**：crm360 与 usercenter2 互不能 fetch。所有请求（含商品级）都在 **usercenter2 域内页签**执行；
   crm360 接口只作备查（§1）。
2. **default resource group 会报 `INSTANCE_NUM_TOO_LARGE`**：默认组实例数超限，查询直接失败。
   必须**按 pipCode 或 resourceGroup 分片**：`fetch_bills.js` 的做法是「逐产品拉 INSTANCE」+「逐资源组拉 group」，
   从不查 default 组。
3. **部分产品无实例维度**：`sae` / `prometheus(cms)` / `cbs` / `xtrace` 等 `INSTANCE_CONSUME_MONTH` 返回 `total=0`，
   只能走 `PRODUCT_CONSUME_MONTH` 取证。aggregate.py 对「无行级证据的产品」自动生成产品级 COMP
   （`note` 标 `无实例维度·产品级取证`，`evidence` = pipCode）。
4. **高基数产品全拉不现实**：`fc` 7 万行 / `gpdb` 3 万行 / `acs` 6 千行。用**「实例根」饱和抽样**：
   逐页拉取提取根 ID（`fc` = functions/ 名去尾部 hash；`gpdb` = instanceId 分号前段；`acs` = 前 16 字符），
   **连续 2 页无新增根即停，最多 12 页**。根折叠成「族」（`family_of`：丢尾部含数字长串）后，
   每族一个 COMP，`cost=null`（金额无法拆到族），基数写进 `name`（如 `FC 函数 ×30`）与 `meta.saturation`。
5. **资源组下拉是 datalist 懒加载**，但 **API 的 `resourceGroup` 参数直接传组名字符串即可**（如 `'enter-prod'`），
   不需要先在 UI 里选中。组名清单从 §1 商品级或 UI 下拉一次性抄进 CONFIG.groups。
6. **当月可能是残缺月**（只出账到某天，如 202611 只到 4 日）：**月均成本只算完整月**。
   `--months-complete 202609,202610` 指定完整月；残缺月的行只进证据（`comp.months`），
   只在残缺月出现的 COMP `cost=null`。`meta.cost_coverage` 给逐月「行级 vs 产品级」对账比例。

补充口径坑（analysis.md 记录）：
- `filterZeroBills=false` 必须开，否则漏掉「在用但不花钱」的组件（PrivateZone、告警管理、旧版 API 网关）——这些是架构存在性证据。
- 同一 pipCode 在商品级与实例级口径略有差异（如 sae/edas/mse 的 SchedulerX 归属），**以实例级 pipCode 为准**并交叉核对。
- CDT 跨境金额里含共享带宽 cbwp 过境部分，勿与 EIP 重复相加。

## 4. 数据回传链路（浏览器 → 本地）

浏览器 console 里的 payload 无法直接写本地文件，走本地 HTTP 接收服务：

```bash
# 1) 起服务（只绑 127.0.0.1，CORS 全开，POST 路径即文件名，tmp+rename 原子写）
python3 scripts/recv_server.py --port 8732 --out-dir /tmp/<customer>-bill-arch

# 2) usercenter2 页签 console 粘贴 scripts/fetch_bills.js（改 CONFIG）
#    脚本末尾 fetch POST → http://127.0.0.1:8732/bills_raw.json

# 3) 归线聚合出 arch.json
python3 scripts/aggregate.py \
  --in /tmp/<customer>-bill-arch/bills_raw.json \
  --out /tmp/<customer>-bill-arch/arch.json \
  --months-complete 202609,202610 \
  --risks internal/risks_kunqi.json
```

回传失败兜底：payload 存在 `window.__kunpeng_payload`，可 `copy(JSON.stringify(window.__kunpeng_payload))`
手动粘进文件。

### bills_raw.json 结构（fetch_bills.js 产出 = aggregate.py 输入）

```jsonc
{
  "meta": {
    "uid": "1077748325118640",
    "months": ["202609", "202610", "202611"],
    "months_complete": ["202609", "202610"],
    "sources": ["usercenter2:/bill/queryMonthConsumeReport"],
    "config": { "groups": [...], "products": [...], "saturation": ["fc","gpdb","acs"], "pageSize": 500 },
    "generated_at": "ISO8601", "csrf_found": true, "elapsed_ms": 123456
  },
  "instance_rows": [ { "month": "202609", "tableType": "INSTANCE_CONSUME_MONTH", "pipCode": "rds", "...原始行字段" } ],
  "group_rows":    [ { "month": "202609", "tableType": "INSTANCE_CONSUME_MONTH", "resourceGroupName": "enter-prod", "..." } ],
  "product_rows":  [ { "month": "202609", "tableType": "PRODUCT_CONSUME_MONTH", "pipCode": "sae", "requireAmount": 10355 } ],
  "saturation":    [ { "pipCode": "fc", "month": "202609", "pages": 12, "rootCount": 6000, "familyCount": 9,
                       "total": 74751, "sampled": 6000, "converged": true,
                       "roots": [ { "root": "prod-coding-agent-…", "family": "prod-coding-agent", "region": "新加坡" } ] } ],
  "failures":      [ { "scope": "INST 202609/sae", "message": "…", "apiCode": "…" } ],
  "progress":      { "INST 202609/rds": 20, "GRP 202609/enter-prod": 18, "SAT 202609/fc": { "roots": 6000, "families": 9, "converged": true } }
}
```

`instance_rows` 与 `group_rows` 会覆盖同一批账单行（同一实例既按产品拉到、又按组拉到），
aggregate.py 用 `hashKey`（缺失时用 month|pip|instanceId|commodity|chargeType|amount 复合键）去重，**否则金额翻倍**。

### 旧格式兼容

`--rg-links rg_links.json` 可并入上一版存档（`{groups:{<组>:[{p,id,nk,sp,m:{month:金额},al,tg}]}, aux:{...}}`），
脚本摊平成 group_rows 后与主输入一起去重。`aux` 段（vpcs/sgs/k8s/eips/logstores）不并入，只在 warnings 提示。

## 5. 账单还原的能力边界

能还原：产品组合全景、实例清单与规格、部署拓扑（地域/VPC/可用区）、环境-业务线划分（标签+命名）、
数据同步链路（DTS 对）、成本分层。

还原不出（需控制台/OpenAPI/链路数据补）：VPC 内子网划分、安全组规则、服务间调用关系（谁调谁）、
SLS logstore 完整清单、SAE 应用清单（无实例维度账单，只能靠 `CreatedBySAE` 的 NLB 旁证）、
Pod 级瞬时拓扑（serverless 实例 ephemeral，账单只留计费行）。
