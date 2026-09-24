# AI 网关蒸馏 · 覆盖率审计报告

生成：2026-09-21 ｜ 生成器：`scripts/audit-doc-coverage.py`（确定性扫描 + docId 实时 301 解析）

## 一、扫描面

- raw 快照：**186** 个（`raw/aliyun-docs/ai-gateway`）
- 已知清单：core 189 + deferred 250 = **439** 个 slug
- 本产品内链（slug 形态）唯一目标：**160** 个
- `document_detail/<数字ID>` 形态链接：唯一 docId **378** 个
- 跨产品 help.aliyun.com 链接：**1** 个
- 站外链接（terms.alicdn.com / 第三方）：**202** 个

## 二、判定结果

| 类别 | 数量 | 含义 |
|---|---|---|
| 命中既有清单 | 358 | 内链目标已在 core/deferred 内 → 无遗漏 |
| 🆕 新候选（清单外） | 1 | 需主控裁决是否补抓 |
| ☠️ 死链 | 0 | docId 解析返回 4xx/5xx |

### 🆕 新候选明细

| slug / docId | 被哪些快照引用 | 备注 |
|---|---|---|
| `api-apig-2024-03-27-createsecret` | api-apig-2024-03-27-overview-ai-gateway, api-apig-2024-03-27-ram-ai-gateway | docId 3045062 → https://help.aliyun.com/zh/api-gateway/ai-gateway/developer-reference/api-apig-2024-03-27-createsecret (HTTP 200)，落在本产品内但清单未收录 |

## 三、跨产品链接（不纳入本产品范围，仅登记）

| 目标产品 | 链接数 |
|---|---|
| `api-gateway` | 1 |

## 四、站外权威源（需单独补抓的协议原文等）

- 🔴 https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg ｜ 被 access-vertex-ai-through-ai-gateway 引用
- 🔴 https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250905155227889/20250905155227889.html ｜ 被 service-level-agreement 引用

## 五、本方法检测不到的残留面（必须如实声明）

若某页同时满足「近日新增 + 未进 llms.txt + 无任何快照内链 + 非顶级栏目」，
上述方法**检测不到**，需 JS 拉实时目录树 API 才能穷尽。
→ 蒸馏产物**不得宣称「全站蒸馏」**，须把这条边界写进溯源节。
