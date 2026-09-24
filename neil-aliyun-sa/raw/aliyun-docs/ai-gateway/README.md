# raw/aliyun-docs/ai-gateway — 阿里云 API 网关 · AI 网关 官方文档快照

**归档日期**：2026-09-21  
**来源**：`https://help.aliyun.com/zh/api-gateway/ai-gateway/`（官方按产品 llms.txt 收录 **438** 链接 → 本次范围 core **189** 页；另 **250** 页逐 Action OpenAPI 参考登记 `[deferred]` 未抓）  
**本目录**：**186** 个 `.md` 快照（= manifest 内落盘 185 页 + 主控补抓的 SLA 协议全文外部源 1 页）+ `SHA256SUMS.txt` + 本 README  
**索引**：官方 `https://help.aliyun.com/zh/llms.txt` → `zh/api-gateway/llms.txt`（产品族归属证据）→ `zh/api-gateway/ai-gateway/llms.txt`（438 链接）+ 一轮快照内链 BFS 增量发现

---

## 一、抓取通道与🔴五种失效模式

help.aliyun.com 任意文档 URL 追加 `.md` 后缀即返回纯 Markdown 正文（`Content-Type: text/markdown;charset=UTF-8`），**纯 curl 可取，不需要浏览器渲染**。

抓取器：`scripts/fetch-aliyun-docs.py`（确定性脚本，非 subagent 抓取 → 产物可复算、无二手结论污染）。每页 verdict 记录在 `tests/ai-gateway-fetch-manifest-2026-09-21.tsv`。

| # | 失效模式 | 表现 | 判据 | 本次命中 |
|---|---|---|---|---|
| 1 | **软 200** | 不存在的 slug 返回 HTTP 200 + 约 **24893B** SPA HTML 外壳 | body 前 60 字节以 `<!doctype`/`<html` 开头 | 0（负控实验用伪造 slug 证实检测器会 FAIL） |
| 2 | **CT 不符** | 非 markdown Content-Type | CT 不含 `markdown` | 0 |
| 3 | **空 body** | 0 字节 | `len(body)==0` | 0 |
| 4 | 🔴 **Document Not Found 桩**（本次新发现） | CT=markdown、HTTP **200 或 404**（同一 slug 两次抓取状态码不同）、body 恒为 **86B** 固定文案 | 正则匹配 `# Document Not Found` + `does not have Markdown content available` | **4**（不落盘，见下方清单） |
| 5 | 🔴 **服务端静默截断**（本次新发现） | HTTP 200、CT=markdown、**Content-Length 与 body 自洽**、**两次抓取 SHA256 一致** → 截断在服务端 | 末行是悬挂结构标记（孤立 `*`）/ HTML 标签开闭不平衡 | **1**（`agent-api-observable`，978B，断在孤立 `*` 上）。扫描器 `scripts/scan-truncated-snapshots.py` |

**TOC 容器判据**（沿 2026-09-20 AgentCore RULINGS C1，本次再次验证）：
判据 = 「正文仅由标题 + 链接列表构成、无散文」，**不是字节阈值**。本次判出 **37** 个 TOC 容器页，**落盘但不作事实来源**，只承载目录结构与 slug↔docId 对照证据。实测 `product-overview` 765B 判 TOC、`support` 113B 判 TOC，而 86B 的 Document Not Found 桩**有散文**故不是 TOC —— 三者字节数相近而性质完全不同，字节阈值必然误判。

## 二、frontmatter 与 SHA256 校验方法

每个快照前 10 行为 7 字段 frontmatter（`source_url` / `fetch_date` / `product` / `slug` / `body_sha256` / `body_bytes` / `migration_status`），正文自第 11 行起**逐字保留**（含官方错字、HTML `<table>` 残留、`HELPCODEESCAPE-*` 代码块语言标记残留，一律不修）。

```bash
# SHA256 只对「原始正文」计算，不含 frontmatter，故直接 -c 会全部 FAILED（设计使然，非快照损坏）
tail -n +11 <file>.md | shasum -a 256      # 正确校验方法
```

`.md` 通道**不含页面 H1 标题**，各页官方标题取自 llms.txt 的链接文字（见下方目录树映射）。

## 三、目录树映射（栏目 → slug → 官方标题 → verdict）

图例：✅ = 有正文（可作事实来源）｜ 📁 = TOC 容器（不作事实来源）｜ 🔗 = 入口桩指向外部协议原文

### 产品概述（19 页 = ✅16 + 📁3）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `ai-credits-billing-details` | AI Credits 计费说明 | ✅ OK | 2213 | current | `d6a127199d6c` |
| `ai-gateway-capacity-description` | 网关类型 | ✅ OK | 15992 | current | `1ab29872180d` |
| `ai-gateway-commercialization-announcement` | AI 网关 Serverless 新版商业化公告（2026年9月起计费） | ✅ OK | 973 | current | `e359bff7747a` |
| `announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta` | AI网关Serverless新版公测公告 | ✅ OK | 3969 | current | `d66577f88ef2` |
| `capacity-description` | AI网关-容量规格与资源配额 | ✅ OK | 7972 | current | `0295b622c7a3` |
| `description-of-arrears` | AI 网关欠费与到期处理 | ✅ OK | 3348 | current | `a90050a24f3c` |
| `dynamics-and-announcements` | AI网关-动态与公告 | 📁 TOC | 306 | current | `9812d931ebb2` |
| `engine-version-description` | AI 网关引擎版本说明 | ✅ OK | 5988 | current | `3e9a7c579b62` |
| `free-product-templates` | AI网关-专享实例计费说明 | ✅ OK | 7573 | current | `083c60377536` |
| `new-feature-release-notes-ai-gateway` | 新功能发布记录 | ✅ OK | 14419 | current | `57ba67c154fd` |
| `overview-of-billing-during-the-serverless-public-preview-of-the` | AI网关Serverless新版公测计费说明 | ✅ OK | 6768 | current | `bd8e371519fc` |
| `product-billing` | 产品计费 | 📁 TOC | 899 | current | `7f55a1fb1e3d` |
| `product-comparison` | AI 网关与 Higress 开源版对比 | ✅ OK | 3748 | current | `873655b9a25e` |
| `product-overview` | 产品概述 | 📁 TOC | 765 | current | `38c695a462d7` |
| `query-bills` | 查看 AI 网关账单 | ✅ OK | 1374 | current | `cc6189e8d31c` |
| `refund` | AI 网关退款说明 | ✅ OK | 2582 | current | `18744f7f6f31` |
| `serverless-old-billing-details` | AI网关Serverless旧版计费说明 | ✅ OK | 3164 | legacy | `94e0ebc30898` |
| `supported-regions` | AI 网关开服地域 | ✅ OK | 1985 | current | `c5d63ae4b322` |
| `what-is-an-ai-gateway` | AI 网关产品概述 | ✅ OK | 19843 | current | `cfb5fa8b42cf` |

### 快速入门（3 页 = ✅2 + 📁1）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `getting-started` | 快速入门 | 📁 TOC | 239 | current | `e40764ba91ab` |
| `manage-the-ai-api` | Model API 管理快速入门 | ✅ OK | 7403 | current | `56efbe5d1308` |
| `mcp-service-management` | MCP 服务管理快速入门 | ✅ OK | 11442 | current | `0c9cc817ea32` |

### 操作指南（140 页 = ✅111 + 📁25 + 无正文4）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `add-policies-and-plug-ins` | 策略与插件 | 📁 TOC | 623 | current | `a1c4671ea833` |
| `agent-api-management` | Agent API管理 | 📁 TOC | 567 | current | `6137a94feb37` |
| `agent-api-observable` | Agent API 可观测 | ✅ OK | 978 | current | `1f35979c8026` |
| `agent-management-access-and-observation` | Agent 管理 | ✅ OK | 17862 | current | `bcd540b95e63` |
| `ai-auxiliary-plug-in-development` | AI 辅助插件开发 | ✅ OK | 2537 | current | `09e0e83ab50b` |
| `ai-cache-1` | AI 缓存策略 | ✅ OK | 13592 | current | `97fad884f113` |
| `ai-cue-decorator` | AI 提示词模板插件 | ✅ OK | 2596 | current | `833647075778` |
| `ai-cue-template` | AI 提示词插件 | ✅ OK | 4248 | current | `9f6edb243aa6` |
| `ai-fallback` | Model API AI Fallback | ✅ OK | 3414 | current | `e1b61d2c7127` |
| `ai-observable` | Model API 可观测 | ✅ OK | 2572 | current | `00b748cc15f5` |
| `ai-plug-in` | AI插件 | 📁 TOC | 815 | current | `f9b3981d373c` |
| `ai-rag` | AI RAG 插件 | ✅ OK | 4674 | current | `a080221ac3ee` |
| `ai-request-response-intelligent-transformation` | AI 请求响应转换插件 | ✅ OK | 3330 | current | `34f58205cd73` |
| `ai-retrieval-agent` | AI RAG 检索代理 | ✅ OK | 13994 | current | `e262264d0053` |
| `ai-retrieval-augmented-generation-enhanced` | AI 检索增强生成加强版 | ✅ OK | 16066 | current | `03c899db23c0` |
| `api-product-introduction` | API 产品概念介绍 | ✅ OK | 1697 | current | `0f2df82afdf6` |
| `api-product-management` | API 产品管理 | ❌未落盘 FAIL-NOMD | 86 | — | `00abaf93ea71` |
| `authentication` | 认证鉴权 | 📁 TOC | 629 | current | `21bf04a9e232` |
| `authorization-management` | 消费者授权管理 | ✅ OK | 2999 | current | `4a06d6f6bc48` |
| `basic-auth-plug-ins` | basic-auth 插件 | ✅ OK | 5994 | current | `d77ff2002671` |
| `bot-detect-plug-ins` | bot-detect 插件 | ✅ OK | 2744 | current | `38b0087efe89` |
| `browser-cache-control` | cache-control 浏览器缓存插件 | ✅ OK | 2034 | current | `65f047340512` |
| `canary-header-plugin` | canary-header 插件 | ✅ OK | 3600 | current | `a5a22cfe446a` |
| `change-the-protocol-and-certificate-of-the-domain-name` | 更换域名协议和证书 | ✅ OK | 1079 | current | `4a1ec7888cb0` |
| `configure-a-modelapi-throttling-policy` | 配置 Model API Token 限流策略 | ✅ OK | 22633 | current | `883e5bbc324b` |
| `configure-ai-log-policy` | 配置 AI 日志策略 | ✅ OK | 16380 | current | `fd880d9d4344` |
| `configure-dns-server` | 配置 DNS 服务器 | ✅ OK | 1597 | current | `39df29e83d1e` |
| `configure-jwt-authentication` | 全局 JWT 认证鉴权配置 | ✅ OK | 4407 | current | `9aeb294ad3cb` |
| `configure-oidc-authentication` | 全局 OIDC 认证鉴权配置 | ✅ OK | 6367 | current | `77558ba34559` |
| `configure-oidc-login-for-portal` | 门户 OIDC 单点登录配置 | ✅ OK | 4869 | current | `3c19a637eeea` |
| `configure-policies-and-plug-ins` | Agent API 策略与插件配置 | ✅ OK | 15542 | current | `66a36e8e2e35` |
| `configure-policies-and-plugins-1` | MCP Server 策略与插件配置 | ✅ OK | 14124 | current | `587d87b23ddb` |
| `configure-self-built-authentication` | 全局自建认证鉴权配置 | ✅ OK | 17267 | current | `b08578f2b7fc` |
| `configure-service-health-checks` | 配置服务健康检查 | ✅ OK | 7494 | current | `b0464ef2748b` |
| `configure-smart-routing` | 配置智能路由 | ✅ OK | 13423 | current | `d6404f4c6652` |
| `consumer-authentication` | Model API 消费者鉴权 | ✅ OK | 3379 | current | `11cac8ddcf7d` |
| `consumer-authentication-authentication` | 消费者认证鉴权 | ✅ OK | 14876 | current | `4f14872bee1d` |
| `consumer-certification` | MCP 消费者认证 | ✅ OK | 3208 | current | `8004271da85d` |
| `consumer-certification-1` | Agent API 消费者认证 | ✅ OK | 2817 | current | `5974539d6805` |
| `consumer-management` | 消费者管理 | 📁 TOC | 452 | current | `51a178e478ae` |
| `consumer-quotas-management` | AI网关-管理消费者配额 | ✅ OK | 8274 | current | `9533bdd1d724` |
| `content-security-protection` | AI 安全防护 | ✅ OK | 13917 | current | `4e8048352513` |
| `create-a-domain-name` | 创建域名 | ✅ OK | 6438 | current | `be5cc23545d8` |
| `create-a-gateway-instance` | 创建 AI 网关实例 | ✅ OK | 14377 | current | `7ccd2971a5fd` |
| `create-a-service-source` | 添加 ACK 容器服务来源 | ✅ OK | 2612 | current | `9ea0f77bb4e6` |
| `create-an-api-product-of-the-agent-api-type` | 创建 Agent API 类型产品 | ✅ OK | 2676 | current | `078a3f60dbf2` |
| `create-an-api-product-of-the-model-api-type` | 创建 Model API 类型产品 | ✅ OK | 3196 | current | `282b0755bd57` |
| `create-portal` | 创建开发者门户 | ✅ OK | 2971 | current | `743f22bace07` |
| `create-secret-key` | 创建密钥 | ✅ OK | 1900 | current | `4bbe0202c2b7` |
| `creating-a-consumer` | 创建消费者 | ✅ OK | 4132 | current | `20594c597f4d` |
| `creating-services` | 添加后端服务 | ✅ OK | 18183 | current | `854054b3c37d` |
| `current-limiting` | Model API 限流策略 | ✅ OK | 22270 | current | `1a213773d185` |
| `custom-response-plugin` | custom-response 插件 | ✅ OK | 3171 | current | `e69424221731` |
| `deactivate-or-delete-a-consumer` | 停用或删除消费者 | ✅ OK | 779 | current | `b38d751de340` |
| `debug-mcp-services` | AI 网关-调试MCP服务（控制台与MCP Inspector） | ✅ OK | 3322 | current | `b52b2abef5e9` |
| `degraphql-plugin` | DeGraphQL 插件 | ✅ OK | 5165 | current | `547ec5eabc15` |
| `delete-a-domain-name` | 编辑或删除域名 | ✅ OK | 799 | current | `30b4c40100d5` |
| `deployment-portal` | 部署开发者门户服务 | ✅ OK | 8008 | current | `95332647ca8d` |
| `develop-gateway-plug-ins-using-the-go-language` | Go 语言开发网关插件 | ✅ OK | 28735 | current | `e67cf020e00f` |
| `develop-plug-ins-1` | 开发插件 | 📁 TOC | 329 | current | `dee0707aac24` |
| `developer-guide` | 开放平台开发者操作指南 | ✅ OK | 4399 | current | `a566a3858aed` |
| `developing-gateway-plug-ins-using-rust-and-c-languages` | Rust 与 C++ 开发网关插件 | ✅ OK | 515 | current | `95f56b980e89` |
| `domain-name-management-1` | 域名管理 | 📁 TOC | 525 | current | `1c791b577caf` |
| `edit-and-delete-secret-key` | 编辑与删除密钥 | ✅ OK | 802 | current | `842f3cd46a34` |
| `enable-gateway-link-tracing` | 开启网关链路追踪 | ✅ OK | 2045 | current | `fe545d01f9ae` |
| `enable-gateway-log-delivery` | 开启网关日志投递 | ✅ OK | 10210 | current | `fa3950cb531f` |
| `enable-mcp-service-log-delivery` | 开启 MCP 服务日志投递 | ✅ OK | 9425 | current | `696f2e317725` |
| `flow-control` | 流量管控 | 📁 TOC | 679 | current | `d973d16da28c` |
| `front-end-grayscale-plug-in` | frontend-gray 前端灰度插件 | ✅ OK | 16020 | current | `1f82fc2feef7` |
| `gateway-managed-mcp-services` | MCP网关管理（llms.txt 未收录，内链 BFS 发现） | ✅ OK | 6094 | current | `ec7aa8c726c3` |
| `gateway-management` | 网关管理 | 📁 TOC | 506 | current | `9e4893b1be1e` |
| `geographic-location-of-ip` | geo-ip 插件 | ✅ OK | 4322 | current | `842f8b8fe511` |
| `global-authentication` | 全局认证鉴权 | 📁 TOC | 504 | current | `58306341b644` |
| `hichat-ai-interaction-center` | HiChat AI 交互中心 | ✅ OK | 2575 | current | `9f6f38f0f45f` |
| `hmac-auth-plug-ins` | hmac-auth 插件 | ✅ OK | 13117 | current | `22a895f41b7f` |
| `hsts-plug-in` | hsts 插件 | ✅ OK | 1860 | current | `99739133cfc4` |
| `http-real-ip-plug-ins` | http-real-ip 插件 | ✅ OK | 384 | current | `ba8674c8b1df` |
| `http-to-mcp-field-configurations` | HTTP to MCP 配置字段参考（YAML/认证/模板语法） | ✅ OK | 35517 | current | `a97308233f38` |
| `jwt-auth-plug-ins` | jwt-auth 插件 | ✅ OK | 16630 | current | `4f2aa5f9d4bb` |
| `jwt-logout-plug-ins` | jwt-logout 插件 | ✅ OK | 17636 | current | `d3d437b8702f` |
| `key-auth-plug-ins` | key-auth 插件 | ✅ OK | 6839 | current | `c26c36718466` |
| `key-rate-limit-plugin` | key-rate-limit 插件 | ✅ OK | 4070 | current | `58def42d3d54` |
| `label` | 实例标签管理 | ✅ OK | 1975 | current | `7080671b38f9` |
| `manage-agent-apis` | 管理 Agent API | ✅ OK | 2613 | current | `e65019eed1f4` |
| `manage-global-authentication` | 全局认证鉴权管理 | ✅ OK | 1713 | current | `1197783ef28f` |
| `manage-plug-ins` | 插件安装启用与卸载 | ✅ OK | 5041 | current | `1844b5983476` |
| `manage-providers` | 管理供应商 | ✅ OK | 3552 | current | `d46da71511db` |
| `manage-service-sources` | 管理服务来源 | ✅ OK | 1070 | current | `14ba1c779e50` |
| `manage-services` | 查看、编辑与删除服务 | ✅ OK | 2003 | current | `d75d45968d34` |
| `managing-the-model-api` | 管理 Model API | ✅ OK | 23549 | current | `63ba448ec121` |
| `mcp-gateway-management` | 创建网关托管 MCP 服务 | ✅ OK | 6094 | current | `ec7aa8c726c3` |
| `mcp-grayscale-release` | MCP 服务灰度发布 | ✅ OK | 1830 | current | `926153394ff5` |
| `mcp-observable` | MCP 服务可观测 | ✅ OK | 1438 | current | `dca042103a73` |
| `mcp-server-product` | 创建 MCP Server 类型产品 | ✅ OK | 2624 | current | `2378494af377` |
| `mcp-service-management-1` | MCP服务管理 | 📁 TOC | 1264 | current | `864aa44a633e` |
| `mcp-tool-assembly` | MCP Tool 组装 | ✅ OK | 731 | current | `0c0c00888dcf` |
| `model-api-management` | Model API管理 | 📁 TOC | 628 | current | `fcc692fb9b9d` |
| `model-metadata` | 管理模型元信息 | ✅ OK | 8625 | current | `83a83a792a36` |
| `model-metadata-and-provider-management` | 模型元信息与供应商管理 | ❌未落盘 FAIL-NOMD | 86 | — | `00abaf93ea71` |
| `modifying-gateway-parameter-configurations` | 修改网关引擎参数 | ✅ OK | 6988 | current | `ba05db2b0ad8` |
| `more-policies-and-plugins` | API 级策略与插件配置 | ✅ OK | 16275 | current | `2de86ee097ea` |
| `networked-search` | 联网搜索策略 | ✅ OK | 7606 | current | `dfb88bef18bf` |
| `oauth-plugin` | oauth 插件 | ✅ OK | 9209 | current | `70f220812679` |
| `observation-analysis` | 观测分析 | 📁 TOC | 382 | current | `c0ead6fd19e0` |
| `open-platform` | 开放平台 | ❌未落盘 FAIL-NOMD | 86 | — | `00abaf93ea71` |
| `parameter-access-control` | param-access-control 参数访问控制 | ✅ OK | 6371 | current | `0fde97d27239` |
| `platform-plug-ins` | 平台插件 | 📁 TOC | 408 | current | `4bdc34b6c42d` |
| `plug-in-market` | 插件市场 | 📁 TOC | 730 | current | `dd35f52823be` |
| `plug-in-performance-reference` | 插件性能参考 | ✅ OK | 4051 | current | `8bed33aefe6e` |
| `policy-management` | 策略管理 | 📁 TOC | 231 | current | `ba1afc8dfc86` |
| `portal-management` | 门户管理 | ❌未落盘 FAIL-NOMD | 86 | — | `00abaf93ea71` |
| `product-category-management` | API 产品分类管理 | ✅ OK | 2370 | current | `ffaf4edec303` |
| `reference-secret-key` | 引用密钥 | ✅ OK | 3303 | current | `68624b3fe4f6` |
| `request-block-plugin` | request-block 插件 | ✅ OK | 3928 | current | `f1c917ac4588` |
| `request-response-capture-1` | API网关请求/响应采集（Body最大5KB/日志字段与版本要求） | ✅ OK | 5690 | current | `6712f66b31a0` |
| `resource-group` | 资源组管理 | ✅ OK | 2818 | current | `c66c98c3680b` |
| `route-list` | Model API 自定义路由管理 | ✅ OK | 4293 | current | `68b648784d6f` |
| `routing-management` | Agent API 自定义路由管理 | ✅ OK | 3176 | current | `3210a7e03a0c` |
| `safety-protection` | 安全防护 | 📁 TOC | 434 | current | `bf3a80a3ce2e` |
| `secret-key-management` | 密钥管理 | 📁 TOC | 336 | current | `cad65547896b` |
| `security-capability-management` | 安全能力管理 | 📁 TOC | 400 | current | `c50afadb5744` |
| `semantic-retrieval` | MCP 语义检索 | ✅ OK | 11015 | current | `a375c272c9c7` |
| `service` | 服务 | 📁 TOC | 442 | current | `33ce0457f009` |
| `service-management` | 服务管理 | 📁 TOC | 196 | current | `491ddedca93b` |
| `service-source` | 服务来源 | 📁 TOC | 238 | current | `1182b53ca056` |
| `set-security-group-rules` | 配置安全组授权规则 | ✅ OK | 6475 | current | `719ed7a2752c` |
| `set-the-gateway-ip-whitelist-and-whitelist` | 设置网关 IP 黑白名单 | ✅ OK | 2746 | current | `6fd460ae6e33` |
| `setting-the-specified-https-cipher-suite` | 设置 HTTPS 加密套件 | ✅ OK | 4253 | current | `c643047df963` |
| `synchronizing-nacos-mcp-services` | 同步 Nacos MCP 服务 | ✅ OK | 1933 | current | `50c95c278709` |
| `tags-and-resources` | 标签与资源 | 📁 TOC | 194 | current | `0ec2d8002f6c` |
| `the-traffic-tag-plugin` | traffic-tag 插件 | ✅ OK | 8159 | current | `09d5c8f9e030` |
| `throttle-based-on-cluster-keys` | cluster-key-rate-limit 插件 | ✅ OK | 13186 | current | `3af72be5acae` |
| `tool-selection` | 工具精选策略 | ✅ OK | 11045 | current | `f80feebb5ae2` |
| `transport-protocol` | 传输协议 | 📁 TOC | 576 | current | `3e779f5ee5aa` |
| `upload-plug-in` | 发布自定义插件 | ✅ OK | 10444 | current | `703e12e8332c` |
| `user-guide` | 操作指南 | 📁 TOC | 1686 | current | `5063c01a6b00` |
| `view-gateway-instance-details` | 查看网关实例详情 | ✅ OK | 1006 | current | `8ea1354bbcf1` |
| `view-gateway-monitoring-data` | 查看网关监控数据 | ✅ OK | 3186 | current | `c1d528b9f127` |
| `waf-plugin` | waf 插件 | ✅ OK | 2956 | current | `e64675d433c4` |
| `webide-writing-plug-ins` | WebIDE 编写插件 | ✅ OK | 6073 | current | `289a21b0b27a` |

### 实践教程（9 页 = ✅8 + 📁1）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `access-vertex-ai-through-ai-gateway` | AI 网关接入 Vertex AI | ✅ OK | 42868 | current | `a734c02713a6` |
| `deepseek-integration-through-ai-gateway` | AI 网关接入 DeepSeek 模型 | ✅ OK | 7855 | current | `90c21aa15ccf` |
| `enable-llm-api-compression-to-save-bandwidth-costs` | LLM API 响应压缩节省带宽 | ✅ OK | 9932 | current | `48fa37ed2e25` |
| `manage-ai-gateway-mcp-services-via-openapi` | OpenAPI 管理 MCP 服务 | ✅ OK | 122580 | current | `3b37148901f9` |
| `migrate-the-official-claude-code-model-to-any-model-using-ai-gateway` | Claude Code 迁移至任意模型 | ✅ OK | 4112 | current | `852e1873a7e0` |
| `pai-deployment-model-access-ai-gateway` | AI 网关接入 PAI-EAS 部署模型 | ✅ OK | 4661 | current | `ab9b3face4c6` |
| `proxy-comfyui-service-via-ai-gateway` | AI 网关代理 ComfyUI 服务 | ✅ OK | 1142 | current | `7e229a0c7a7f` |
| `proxy-dify-inbound-and-outbound-traffic-through-ai-gateway` | AI 网关代理 Dify 出入流量 | ✅ OK | 14578 | current | `33953fb975b8` |
| `use-cases` | 实践教程 | 📁 TOC | 1248 | current | `f818e68cea02` |

### 安全合规（7 页 = ✅4 + 📁3）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `ai-gateway-system-permission-policy-reference` | AI 网关系统权限策略参考 | ✅ OK | 2841 | current | `d53a32db9ff4` |
| `custom-permission-policy-reference-for-ai-gateway` | AI 网关自定义权限策略参考 | ✅ OK | 2894 | current | `d1ba8d2fc3b8` |
| `identity-based-policies` | 基于身份的策略 | 📁 TOC | 353 | current | `5d0d089285fa` |
| `identity-management` | AI 网关 RAM 身份管理 | ✅ OK | 4956 | current | `d7e328e84192` |
| `identity-management-and-access-control` | 使用RAM进行访问控制 | 📁 TOC | 445 | current | `c535edea56a6` |
| `security-and-compliance` | 安全合规 | 📁 TOC | 164 | current | `febd1a87bbab` |
| `service-association-role-provided-only-when-involved-otherwise-no-need` | AI 网关服务关联角色 | ✅ OK | 14652 | current | `7c009c4450d6` |

### 服务支持（3 页 = ✅1 + 📁2）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `related-agreements` | 相关协议 | 📁 TOC | 124 | current | `f4f719af7524` |
| `service-level-agreement` | AI 网关服务等级协议 | 🔗 OK-STUB | 204 | current | `43aecb4c0973` |
| `support` | 服务支持 | 📁 TOC | 113 | current | `bfcbc60efa0f` |

### 开发参考（8 页 = ✅6 + 📁2）

| slug | 官方标题 | verdict | 字节 | migration_status | sha256 前 12 |
|---|---|---|---|---|---|
| `api-apig-2024-03-27-changeset-ai-gateway` | APIG OpenAPI 变更集 | ✅ OK | 4794 | current | `d43ff3eeb924` |
| `api-apig-2024-03-27-endpoint-ai-gateway` | APIG 服务接入点 | ✅ OK | 5841 | current | `e834d597b328` |
| `api-apig-2024-03-27-errorcodes` | AI 网关公共错误码（403/409/500 与 APIG.ErrorCode 排查） | ✅ OK | 43253 | current | `3ebbb2e3277d` |
| `api-apig-2024-03-27-overview-ai-gateway` | AI网关OpenAPI概览（HTTP API/接口/模型供应商管理） | ✅ OK | 35490 | current | `7de54d46a0b1` |
| `api-apig-2024-03-27-quota-ai-gateway` | APIG OpenAPI 流控配额 | ✅ OK | 34173 | current | `30306a18c1c8` |
| `api-apig-2024-03-27-ram-ai-gateway` | AI网关-RAM授权信息 Action/Resource/Condition定义 | ✅ OK | 56328 | current | `3dc5dfbc2639` |
| `api-reference` | API参考 | 📁 TOC | 1042 | current | `4bd2dd201aaa` |
| `developer-reference` | 开发参考 | 📁 TOC | 117 | current | `37fdddc4c0a6` |

### 外部源补抓（非 help.aliyun.com `.md` 通道）

| 文件 | 来源 | 说明 |
|---|---|---|
| `sla-agreement-fulltext-terms-alicdn.md` | `https://terms.alicdn.com/legal-agreement/terms/b_end_product_protocol/20250905155227889/20250905155227889.html` | **AI 网关服务等级协议全文**。help 侧 `support/service-level-agreement` 只有 204 字节入口桩（verdict `OK-STUB`），可用率承诺与赔偿档位全在外部协议原文页。提取方式 = curl HTML → 正则剥标签 → unescape → 压缩空行，🔴 **有损**（表格被展平为逐行文本，赔偿档位的行列对应关系由蒸馏员 W2 用四步法复核后重排，方法见 `knowledge/aliyun-ai-gateway-billing.md` §3.9.4）。原始 HTML SHA256 记录在该文件 frontmatter 后的说明段。🔴 该文件**不在** `SHA256SUMS.txt` 内（其校验值见自身 frontmatter 的 `body_sha256`），与 2026-09-20 AgentCore 侧 SLA 全文补抓的处理方式一致 |

## 四、🔴 未落盘的无正文节点（4 个，verdict `FAIL-NOMD`）

这些节点存在于 llms.txt / 导航树，但 `.md` 通道返回 86 字节固定桩「# Document Not Found / The requested document does not have Markdown content available.」→ 无 Markdown 正文，**不落盘、不作事实来源**。它们的子页均已通过 llms.txt 收录并抓取，**无覆盖损失**。

- `api-product-management` — API 产品管理（HTTP 404）
- `model-metadata-and-provider-management` — 模型元信息与供应商管理（HTTP 404）
- `open-platform` — 开放平台（HTTP 404）
- `portal-management` — 门户管理（HTTP 404）

## 五、🔴 重复别名与部分重复（蒸馏时只写一份）

| 事实 | 证据 |
|---|---|
| `gateway-managed-mcp-services` ≡ `mcp-gateway-management`（**完全相同的两个 slug**） | 正文 SHA256 同为 `ec7aa8c726c3d0c4da7d7c0ec7c19d68f876dc7c64d793eccb588ab9d2730382`、`body_bytes` 同为 6094、`diff` 为空（主控实测）。前者 **llms.txt 未收录**，靠 `mcp-service-management-1` 的内链 BFS 发现 |
| `enable-mcp-service-log-delivery` 与 `enable-gateway-log-delivery` **部分重复** | 日志字段表 SHA256 相同、`Response_Flag` 章节相同，但两页正文整体不同 → **不是重复页**，蒸馏时合并日志字段表并双标 slug（蒸馏员 W7 实测） |

## 六、migration_status 判定

本次 **legacy 1 页 / current 184 页**。legacy 判据 = 官方标题含「旧版/（旧）/已下线/停止服务」或 slug 含 `-old-`/`-legacy`/`serverless-old`（`scripts/fetch-aliyun-docs.py` 的 `migration_status()` 机械判定，非语义猜测）：

- `serverless-old-billing-details` — AI网关Serverless旧版计费说明

⚠️ **另一类时效性内容未被 migration_status 捕获**：Serverless **新版公测**相关页（`announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta`、`overview-of-billing-during-the-serverless-public-preview-of-the`）标为 `current`，但公测已于 **2026-08-31 结束、2026-09-01 起商业化计费**（`ai-gateway-commercialization-announcement`）→ 引用这两页的免费/计费口径时**必须带时间边界**，不要写成现在时。蒸馏契约 §8 已就此下过指令。

## 七、🔴 本目录不构成「全站」的边界声明

1. **250 页逐 Action / 逐数据结构 OpenAPI 参考页未抓**（`api-apig-2024-03-27-*`），登记 `[deferred]`；仅破例纳入 8 个元页（概览/接入点/RAM/流控配额/错误码/变更集/两级容器）。
2. **同族的云原生API网关、原API网关两个子产品未抓**（各有独立 llms.txt）。
3. llms.txt 是**快照会滞后**：本次已实证 2 处收录缺口（`gateway-managed-mcp-services` 未收录；`api-apig-2024-03-27-createsecret` docId 3045062 未收录）。
4. 若某页同时满足「近日新增 + 未进 llms.txt + 无任何快照内链 + 非顶级栏目」，本次方法（llms.txt + 内链 BFS + docId 实时 301 解析）**检测不到**，需 JS 拉实时目录树 API 才能穷尽。

→ 准确表述：**「截至 2026-09-21 的官方 llms.txt 收录范围 + 一轮内链 BFS，189 页全覆盖」**，**不得宣称「全站蒸馏」**。

## 八、配套工艺制品

| 制品 | 路径 |
|---|---|
| llms.txt 快照（本产品 438 链接 + 父级归属证据） | `tests/ai-gateway-llms-2026-09-21.txt`、`tests/api-gateway-parent-llms-2026-09-21.txt` |
| 文档树与分片清单（含范围裁决与分类判据） | `tests/ai-gateway-doctree-shards-2026-09-21.md` |
| 抓取 manifest（189 行 × 13 列） | `tests/ai-gateway-fetch-manifest-2026-09-21.tsv` |
| 覆盖率审计报告 | `tests/ai-gateway-coverage-audit-2026-09-21.md` |
| 蒸馏契约（7 路 worker 共读） | `tests/ai-gateway-distill-contract-2026-09-21.md` |
| 主控裁决留痕（R1~R10 + C1~C12） | `tests/ai-gateway-rulings-2026-09-21.md` |
| Wiki 层产物（7 文件 / 9360 行 / 407 表） | `knowledge/aliyun-ai-gateway*.md` |

