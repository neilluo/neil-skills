# AI 网关专题页家族 · 事实保真审计（独立评审员 R1）

- **审计日**：2026-09-21
- **评审员**：R1（独立，与 7 个蒸馏 worker 无关联；假设 worker 可能出错）
- **裁判基线**：`raw/aliyun-docs/ai-gateway/*.md`（186 个官方快照 + 1 个 SLA 外部源；`README.md` 无 frontmatter）
- **审计对象指纹**（审计期间文件被并发修改过，以下为**本报告全部行号所依据的稳定版本**，SHA256 前 16 位）：

| 文件 | mtime | bytes | sha256(16) | 行数 |
|---|---|---|---|---|
| `knowledge/aliyun-ai-gateway.md` | 2026-09-21 17:29:54 | 174291 | `efe836ad3e6862b1` | 1368 |
| `knowledge/aliyun-ai-gateway-billing.md` | 17:20:07 | 97385 | `59821938a117ddff` | 955 |
| `knowledge/aliyun-ai-gateway-traffic.md` | 17:20:07 | 161235 | `2d605f27b7e8284b` | 1347 |
| `knowledge/aliyun-ai-gateway-auth.md` | 17:20:07 | 154381 | `f5f00f45cb5a8621` | 1237 |
| `knowledge/aliyun-ai-gateway-mcp-agent.md` | 17:20:07 | 166678 | `4387b0a441a9eb8c` | 1409 |
| `knowledge/aliyun-ai-gateway-plugins.md` | 17:20:07 | 191333 | `27ebf6085230bf36` | 1539 |
| `knowledge/aliyun-ai-gateway-ops.md` | 17:20:07 | 200201 | `caee45c1ee1839d0` | 1549 |

> ⚠️ **行号时效性**：本次审计开始时 7 个文件在 16:46~16:54 之间，审计过程中被重写为 17:20:07 / 17:29:54 版本（行数各 +2~+30）。**本报告所有行号均已按上表版本重新定位并二次复核**，与上表 SHA 一一对应。若文件再次被改写，行号需重新解析（定位锚点串已在每条给出，可直接 grep 复算）。

- **基线完整性自检**（先证明裁判尺没被掰弯）：用脚本对 186 个快照重算「去掉 10 行 frontmatter 后的正文 SHA256」，与各自 frontmatter 的 `body_sha256` 比对 → **185 命中 / 0 不符**（1 个因分割正则未匹配未计入）。`raw/aliyun-docs/ai-gateway/SHA256SUMS.txt` 自述「`shasum -c` 会全部 FAILED —— 设计使然」，实测确认，**不是快照损坏**。→ 基线可信。

---

## 1. 抽样清单

### 1.1 带数字的断言（42 条 = 7 文件 × 6，优先价格／SLA／配额／限流／地域）

| # | 文件:行号 | 断言摘要 | 回源 slug | 判定 |
|---|---|---|---|---|
| N01 | `aliyun-ai-gateway.md:447` | §2.4 专享实例 10 档 QPS/客户端连接数：`aigw.small.x1`=1500/20000 … `aigw.large.x4`=192000/2560000 | `capacity-description` | ✅ 一致（10 行 × 2 列全对） |
| N02 | `aliyun-ai-gateway.md:491` | §2.6 全局配额：单Region实例数 100／消费者组 1000／组内消费者 500／单Region消费者 100000 | `capacity-description` | ✅ 一致（4/4） |
| N03 | `aliyun-ai-gateway.md:504` | §2.7 实例配额 13 列 × 10 行（MCP Server数 100/20/100/500…2600 等） | `capacity-description` | ✅ 一致（脚本逐格比对 0 差异；含 3 行「6 值 → 3 档位」还原） |
| N04 | `aliyun-ai-gateway.md:592` | §2.9 公共云 15 地域 + 金融云 1 地域及 Region ID（`cn-qingdao`…`eu-central-1`／`cn-shanghai-finance-1`） | `supported-regions` | ✅ 一致（16/16，含全角数字「华北２」「华东１」照录） |
| N05 | `aliyun-ai-gateway.md:617` | §2.10 引擎版本 20 个（2.1.23／2026-09-03 … 2.1.4／2025-05-08） | `engine-version-description` | ✅ 一致（20/20 版本号+日期+要点） |
| **N06** | **`aliyun-ai-gateway.md:955`** | §2.12「**截至快照日 2026-09-21 仍处公测**；公测结束时间、免费范围、转商用后计费口径**全部未说明**」 | `new-feature-release-notes-ai-gateway`（所标）；反证在 `ai-gateway-commercialization-announcement` | ❌ **D3 + D8**（DEF-1） |
| N07 | `aliyun-ai-gateway-billing.md:69` | §3.2.3 实例费用 45 行单价表（5 地域档 × 9 规格） | `free-product-templates` | ✅ 一致（脚本逐格比对 45/45 行 × 4 列，0 差异） |
| N08 | `aliyun-ai-gateway-billing.md:131` | §3.2.4 数据处理量 公共云公网 0.037／私网 0.049／金融云公网 0.07／私网 0.093 元/GB/小时 | `free-product-templates` | ✅ 一致（4/4；示例 0.037×5+0.037×10=0.555、0.049×5+0.049×10=0.735 亦逐字对） |
| N09 | `aliyun-ai-gateway-billing.md:198` | §3.3.3 Serverless 新版 6 项参考单价：实例费 0.245 元/小时、请求 0.008--0.015 元/万次、数据量 0.037 元/GB/小时、规则扩容 0.02 元/100个/小时、公网出/入网各 0.8 元/GB | `overview-of-billing-during-the-serverless-public-preview-of-the` | ✅ 一致（6/6，含官方「参考单价」用词） |
| N10 | `aliyun-ai-gateway-billing.md:230` | §3.3.4 阶梯单价：0--50万次 0.015／50--100万次 0.012／100万次以上 0.008 元/万次 | 同 N09 | ✅ 一致（3/3，含原文双连字符 `--` 照录） |
| N11 | `aliyun-ai-gateway-billing.md:364` | §3.4.5 CU 单价 4 档：内地 0.005／港+东京 0.0075／新+雅+法 0.007／美国 0.006 元/1000CU | `serverless-old-billing-details` | ✅ 一致（4/4；倍率列 1.5/1.4/1.2 为标注 `[推断]`，算术正确） |
| N12 | `aliyun-ai-gateway-billing.md:792`+`:834` | §3.9.2/3.9.4 SLA 承诺 serverless 99.90%／普通 99.99%；赔偿 15%/30%/100% 三档，档位边界「低于99.99%但等于或高于99.00%」等 | `sla-agreement-fulltext-terms-alicdn` | ✅ 一致（含展平表 4 个 U+FEFF rowspan 占位符位于原文第 120/126/138/144 行，与知识页自述**完全吻合**） |
| N13 | `aliyun-ai-gateway-traffic.md:571` | §5.1 限流「最多只支持**同时命中** 10 条规则」 | `current-limiting` | ✅ 一致（raw:48 与 raw:194 两处均为「同时命中 10 条」） |
| N14 | `aliyun-ai-gateway-traffic.md:1015` | §5.7 FinOps 限额「最小值为 1，默认值为 60000」 | `consumer-quotas-management` | ✅ 一致（逐字） |
| N15 | `aliyun-ai-gateway-traffic.md:1021` | §5.7「单次创建或编辑配额规则操作，最多可选择 1000 个消费者」 | `consumer-quotas-management` | ✅ 一致（逐字） |
| N16 | `aliyun-ai-gateway-traffic.md:576` | §5.1/5.7 版本门槛「引擎版本为 2.1.19 及以上，如需使用 Credits 配额能力，请升级至 2.1.20 及以上」+「版型不能是旧版本 Serverless 规格」 | `consumer-quotas-management` | ✅ 一致 |
| N17 | `aliyun-ai-gateway-traffic.md:1019` | §5.7 9 个可选时区清单 + 默认 UTC+8（北京/上海/新加坡/香港） | `consumer-quotas-management` | ✅ 一致（9/9，顺序与文字逐字） |
| N18 | `aliyun-ai-gateway-traffic.md:1107`+`:1113` | §5.8 AI 缓存：向量化超时默认 5000ms、向量库超时默认 3000ms、精确缓存 TTL 默认 1800 秒、相似度阈值取值 (0,1) 建议 0.8~0.9 | `ai-cache-1` | ✅ 一致（raw:74/91/117/89） |
| N19 | `aliyun-ai-gateway-auth.md:181` | §6.5.2 JWT 支持算法 **13 种**：ES256/384/512、RS256/384/512、PS256/384/512、HS256/384/512、EdDSA | `consumer-authentication-authentication` | ✅ 一致（raw:126；清点确为 13） |
| N20 | `aliyun-ai-gateway-auth.md:182` | §6.5.2「过期时间需要小于 7 天」；代码注释「//设置过期时间，并且小于7天」；示例 `date.addSeconds(120*60)` | `consumer-authentication-authentication` | ✅ 一致（raw:137 / raw:98） |
| N21 | `aliyun-ai-gateway-auth.md:214` | §6.5.4 错误码：JWT 401×3（`Jwt missing`/`Jwt expired`/`Jwt verification fails`）+ 403 `Access Denied`；API Key 401×3 + 403 `Unauthorized consumer.`（含原文错字 `Muti`） | `consumer-authentication-authentication` | ✅ 一致（8/8 逐字，`Muti` 错字正确照录并标 `[原文如此]`） |
| N22 | `aliyun-ai-gateway-auth.md:1084` | §7.6.2 SLR-A：9 个产品 Action **166 行 / 去重 165 / 只读 71 / 写 94**；分项 slb 45(重复1)／nlb 30／ecs 28／arms 20／vpc 19／cs 11／fc 6／mse 4／edas 3 | `service-association-role-provided-only-when-involved-otherwise-no-need` | ✅ 一致（**脚本独立复算完全命中**：166 行、去重 165、只读 71、写 94、唯一重复项 `slb:ModifyLoadBalancerInternetSpec`；`"slb:DescribeLoadBalancerUDPListenerAttribute  "` 两个尾随空格亦确证） |
| N23 | `aliyun-ai-gateway-auth.md:1099` | §7.6.2 三 SLR 合计 **179 条 / 去重 178**；InvokeKMS `kms` 12 条；InvokeFC 为单字符串 `fc:InvokeFunction`（非数组） | 同 N22 | ✅ 一致（166+1+12=179；kms 12 条清单逐条对上） |
| N24 | `aliyun-ai-gateway-auth.md:771` | §7.1.4 防护等级 4 档（低＝仅拦高风险／中＝仅拦中高／高＝拦所有风险／观察模式＝不拦截）+ 5 个 Service 名 | `content-security-protection` | ✅ 一致（raw:52 与 raw:129 两处均为 4 档，逐字） |
| N25 | `aliyun-ai-gateway-mcp-agent.md:45` | §8.10「如果使用的是AI网关提供的测试域名，存在调用限额，**每天整个域名限额1000次**」 | `debug-mcp-services`、`mcp-service-management` | ✅ 一致（两页各一处，`debug-mcp-services:25`／`mcp-service-management:159`，逐字相同） |
| N26 | `aliyun-ai-gateway-mcp-agent.md:271` | §8.6「网关升级过程大约需要持续 **5\~10 分钟**」 | `synchronizing-nacos-mcp-services` | ✅ 一致（raw:23，含 `\~` 转义照录） |
| N27 | `aliyun-ai-gateway-mcp-agent.md:266` | §8.6 MSE Nacos **3.0** 及以上 + 网关引擎 **2.1.6** 及以上；`[官方矛盾]` 专页写「企业版」/快速入门页写「铂金版」 | `synchronizing-nacos-mcp-services`、`mcp-service-management` | ✅ 一致，且**矛盾为真**（raw:14「MSE Nacos企业版3.0」vs raw:102「MSE Nacos铂金版3.0」；两页引擎版本均 2.1.6） |
| N28 | `aliyun-ai-gateway-mcp-agent.md:389` | §8.8 语义检索：纯向量 0.319-0.324秒／RRF 0.351-0.352秒／总错误 4,214个（4.7%）／「350毫秒以内」／「约30毫秒延迟」 | `semantic-retrieval` | ✅ 一致（raw:120/124/134/128）；其 `[官方矛盾]` 亦为真：raw:128 称「均控制在350毫秒以内」而 raw:68 表内 RRF k=10=0.3519s(=351.9ms) 确已超 |
| N29 | `aliyun-ai-gateway-mcp-agent.md:448`-`450` | §8.9.3 工具精选：准确性最高提升 **6%**／工具集超 **50** 个后 RT 显著下降／**500** 个工具场景响应速度最高提升 **7倍**／Token 费用降低 **4\~6倍**／评测规模 50/100/200/300/400/500 | `tool-selection` | ✅ 一致（raw:37-44，逐项对上；3 个评测模型名 `qwen3-235b-a22b-instruct-2507`／`gte-rerank-v2`／`qwen3-30b-a3b-instruct-2507` 亦逐字） |
| N30 | `aliyun-ai-gateway-mcp-agent.md:16` | §8 卷首：`gateway-managed-mcp-services` 与 `mcp-gateway-management` 正文 `body_sha256` 均为 `ec7aa8c7…30382`、`body_bytes` 均 6094 | 两页 frontmatter | ✅ 一致（两文件 frontmatter 实测 sha256 与 bytes 完全相同，确为别名） |
| N31 | `aliyun-ai-gateway-plugins.md:220` | §9.2.1 主表 **27** 个有独立参数页的插件 | `upload-plug-in` + 各插件页 | ✅ 一致（脚本数得 27 行，插件名清单与各 slug 一一对应） |
| N32 | `aliyun-ai-gateway-plugins.md:267` | §9.2.3 仅在优先级总表出现、无独立参数页的插件 **20** 项 | `upload-plug-in` | ✅ 一致（脚本数得 20 行） |
| N33 | `aliyun-ai-gateway-plugins.md:1396` | §9.6.4「key-auth 插件只会为每个请求增加 **20微秒**左右的延时，basic-auth 插件…增加 **30微秒**左右」 | `plug-in-performance-reference` | ✅ 一致（raw 逐字） |
| N34 | `aliyun-ai-gateway-plugins.md:1419` | §9.6.4 四语言对比：C++ 0.19毫秒／Golang 0.20毫秒／Rust 0.21毫秒／AssemblyScript 0.21毫秒 | `plug-in-performance-reference` | ✅ 一致（raw:109 表 4 行逐字） |
| N35 | `aliyun-ai-gateway-plugins.md:1293` | §9.6.2 Go 需 **1.24版本以上**；「使用 Go 1.24 编译的插件需要AI网关版本**不低于`2.1.5`**」；TinyGo 0.29 + Go 1.20 → Go 1.24；下载文件 `go1.24.4.*` | `develop-gateway-plug-ins-using-the-go-language` | ✅ 一致（raw:29/32/14/36-52；`type.ActionPause`→`types.HeaderStopAllIterationAndWatermark`、`go-re2`→`regexp` 三条迁移改动亦逐字） |
| N36 | `aliyun-ai-gateway-plugins.md:228` | §9.4.6 hmac-auth 请求 Body 上限 **32MB**（413 `Request Body Too Large.`／「请求Body超过限制大小：32MB。」）；`x-ca-signature-method` 默认 HmacSHA256 | `hmac-auth-plug-ins` | ✅ 一致（raw:287 错误码表 + raw:232） |
| N37 | `aliyun-ai-gateway-ops.md:113` | §10.6 访问日志字段 **27 个**（两页共用） | `enable-gateway-log-delivery`、`enable-mcp-service-log-delivery` | ✅ 一致（两页各解析出 27 个字段行，字段名逐个对上） |
| N38 | `aliyun-ai-gateway-ops.md:168` | §10.7 `Response_Flag` **23 个** | 同 N37 | ✅ 一致（raw 为无序列表非表格，清点 23 项：UH/UF/NR/URX/NC/DT/DC/LH/UT/LR/UR/UC/DI/FI/RL/UAEX/RLSE/IH/SI/DPE/UPE/UMSDR/OM，顺序与释义逐字一致） |
| N39 | `aliyun-ai-gateway-ops.md:266` | §10.8.4 内置模板 **15 个**（OpenAI 6 + 百炼 9），含 6+9 条具体路径 | `configure-ai-log-policy` | ✅ 一致（OpenAI 6 路径、百炼 9 路径全部在 raw 命中，无多无少） |
| N40 | `aliyun-ai-gateway-ops.md:325` | §10.9 版本门槛 云原生API网关 **2.1.18+**／AI 网关 **2.1.20+**；Body 最大采集默认 **5120（5 KB）**；上限「全托管 5 KB（5120 字节）／非全托管 200 KB（204800 字节）」 | `request-response-capture-1` | ✅ 一致（版本表、6 个配置项默认值、4 条 Body 规则全部逐字；「Serverless版不支持该功能」亦逐字） |
| N41 | `aliyun-ai-gateway-ops.md:992`+`:1072` | §13.1 OpenAPI 合计 **140 个 Action，无重名**，16 组分布 9/5/10/8/5/3/12/8/13/5/8/6/2/1/3/42；§13.3 配额页 **105 行**、缺口 **35 个**、反向差集 **0** | `api-apig-2024-03-27-overview-ai-gateway`、`api-apig-2024-03-27-quota-ai-gateway` | ✅ 一致（**脚本独立复算完全命中**：16 组每组数字逐一相等、总数 140、unique 140、dups 空；配额页 105 行、差集 35、反向差集 0；缺口按主题 10/9/8/5/3 亦逐项对上） |
| N42 | `aliyun-ai-gateway-ops.md:1291` | §13.5 错误码分布 409:**67**／400:**23**／403:**3**／404:**13**／500:**5** | `api-apig-2024-03-27-errorcodes` | ✅ 一致（脚本按 HTTP 状态码计数：`{'400':23,'403':3,'404':13,'409':67,'500':5}`，合计 111，**五个数字全中**） |

**小计：42 条抽样，41 ✅ 一致 / 1 ❌ 缺陷。**

#### 1.1b 附带完成的「整表级」机械复算（不计入 42 条配额，但均已逐格比对）

| 对象 | 规模 | 结果 |
|---|---|---|
| billing §3.2.3 实例费用单价表 | 45 行 × 4 列 | ✅ 0 差异 |
| main §2.3 四形态能力对比表 | 12 行 × 4 列 = 48 单元格（归一化后逐格 in raw） | ✅ 48/48 命中 |
| main §2.7 实例配额表 | 13 列 × 10 行 + 表头双行 + 3 行档位级还原 | ✅ 0 差异 |
| ops §13.4.1 RAM 资源类型分布 | 66/22/18/18/7/5/3/1 = 140 | ✅ 脚本聚合后逐项相等（Domain 18 = 域名5+消费者9+密钥4，与知识页拆分完全一致） |
| ops §13.4.2 访问级别分布 | none 96／get 12／list 9／create 9／delete 8／update 6 = 140 | ✅ 逐项相等；其 `[官方矛盾]`（说明文字称取值为 Write/Read/List，表内实为 none/get/list/create/delete/update）**为真** |
| ops §12 配方7 压缩算法表 | 8 行（ZSTD/GZIP/Brotli/QATZip × 流式/非流式，压缩比+CPU） | ✅ 0 差异（rowspan 空单元补算法名已自行披露） |
| billing §3.4.6 CU 地板推导 | 0.50/0.60/0.70/0.75 元/小时 + 360/432/504/540 元/满月 | ✅ 算术正确，且明确标 `[推断]` |
| main §2.4 QPS:连接数 比例 | 恒为 1:13.33（20000/1500 … 2560000/192000） | ✅ 10 档全部成立 |
| main §15.3 金融云 = 内地 × 1.9 | 15.07365 / 7.9335 | ✅ = 1.90000 |

### 1.2 `[官方原文]` 逐字引用 · 字符级比对（抽 18 条，要求 5 条）

归一化规则（比对前对**双方**同等施加）：HTML 标签剥离 → markdown 链接 `[文字](url)` → `文字` → 反斜杠转义 `\~ \* \_ \|` 还原 → U+00A0/U+FEFF/U+200B 删除 → `* ` > | # - • 与全部空白删除 → 中文引号「」『』""统一为 `"` → NFKC。

| # | 文件:行号 | 引用摘要 | 回源 slug | 判定 |
|---|---|---|---|---|
| V1 | `aliyun-ai-gateway-billing.md:760-762` | SLA §2.1 可用性计算公式 +「（注：服务周期内5分钟总个数=12 x 24 x 该服务周期的天数）」 | `sla-agreement-fulltext-terms-alicdn` | ✅ 逐字（121 字符归一化后完全命中，含 `x` 用小写字母而非 `×`、`Σ` 保留） |
| V2 | `aliyun-ai-gateway-traffic.md:581` | 「注意：消费者配额与消费者限流互补。配额是 FinOps 维度，控制周期内总使用量；限流是 QPS/并发维度，控制瞬时使用量。」 | `consumer-quotas-management` | ✅ 逐字（59 字符） |
| V3 | `aliyun-ai-gateway-ops.md:314` | 「请求/响应采集是网关的一项日志增强能力…该功能在网关级别生效，作用于该网关下的所有流量。」 | `request-response-capture-1` | ✅ 逐字（137 字符；raw 中为 2 个自然段，知识页合段属无害归一化） |
| V4 | `aliyun-ai-gateway-plugins.md:1396` | 「## 平台插件性能 / 平台提供的插件对请求延迟的影响都是微秒级的，例如key-auth插件只会为每个请求增加20微秒左右的延时，basic-auth插件只会为每个请求增加30微秒左右的延时。」 | `plug-in-performance-reference` | ✅ 逐字（82 字符，连标题一并照抄） |
| V5 | `aliyun-ai-gateway-auth.md:196` | 网关侧验签 3 步（未带 Token→401；用 jwks 中**私钥**验签→401；再校验授权） | `consumer-authentication-authentication` | ✅ 逐字（3 句分别 47/59/38 字符全部命中；整段未命中仅因 raw 为 `1. 2. 3.` 有序列表，属格式差异） |
| **V6** | **`aliyun-ai-gateway-plugins.md:263`** | `[官方原文]`「**AI提示词装饰器插件的配置示例如下**：`prepend: - role: system …`」，标注出自 `geographic-location-of-ip` | `geographic-location-of-ip` | ❌ **D4 + D7**（DEF-6） |
| V7 | `aliyun-ai-gateway.md:391` | §2.3「四形态能力对比（官方 12 行表，逐格照抄）」 | `ai-gateway-capacity-description` | ✅ 逐字（48 单元格全部命中，「逐格照抄」的自我声明成立） |
| V8 | `aliyun-ai-gateway-ops.md:923` | 「根据压缩算法的测试结果，QATZip 在综合性能上表现更优…QATZip 的 CPU 消耗为 20.9%，低于 ZSTD 的 23.6%。」 | `enable-llm-api-compression-to-save-bandwidth-costs` | ✅ 逐字（161 字符） |
| V9 | `aliyun-ai-gateway-ops.md:888` | 「注：压缩比 = 压缩后大小 / 原始大小…2.8% 表示压缩后数据仅为原始数据的 2.8%，节省了 97.2% 的带宽。」 | 同 V8 | ✅ 逐字（69 字符） |
| V10 | `aliyun-ai-gateway-billing.md:828` | SLA §3.1「赔偿方式仅限于用于购买网关产品的代金券，且赔偿总额不超过…（不含用代金券抵扣的费用）。」 | `sla-agreement-fulltext-terms-alicdn` | ✅ 逐字（112 字符） |
| V11 | `aliyun-ai-gateway-auth.md:887` | 「网关IP黑名单和白名单是AI 网关提供的安全防护能力之一。您可以通过配置黑、白名单来拒绝或允许特定IP的访问请求。」 | `set-the-gateway-ip-whitelist-and-whitelist` | ✅ 逐字（56 字符，含「AI 网关」中间那个原文空格） |
| V12 | `aliyun-ai-gateway.md:523` | 「说明：如通过特殊白名单或特殊配置突破上述配额限制，相关使用不属于标准配额范围，阿里云不对该等使用场景作出服务等级协议（SLA）承诺。」 | `capacity-description` | ✅ 逐字（66 字符） |
| V13 | `aliyun-ai-gateway.md:1123` | §14.1 段1「假设自建鉴权服务的鉴权API是/validateToken…即/validateToken/order。」并自述「在 raw **第 33 行**」 | `configure-self-built-authentication` | ✅ 逐字，**且「raw 第 33 行」这一行号自述经实测为真**（`sed -n 33p` 即该句） |
| V14 | `aliyun-ai-gateway.md:1129` | §14.1 段3 宽松/严格模式（触发条件穷举为「建立连接失败或者返回5xx请求」） | `configure-self-built-authentication` | ✅ 逐字（HTML 表格单元 + `<ul><li>` 展平，知识页已自行披露展平并声明「去标签去空白后与 raw 逐字一致」——**该声明经字符级比对成立**） |
| V15 | `aliyun-ai-gateway.md:1151` | §14.2「如果所选消费者只授权了 MCP工具级别消费者认证…没权限的会403。」 | `debug-mcp-services` | ✅ 逐字（raw:39；原文含 markdown 链接 `[MCP工具级别消费者认证](https://…)`，知识页取链接文字，属允许的归一化） |
| V16 | `aliyun-ai-gateway-billing.md:760` 附近 §3.9.1 | SLA 1.1–1.5 五条术语定义（服务周期＝自然月；有效请求＝所有请求；失败请求需「网关原因」+ 前 7 个自然日每分钟均值×故障时间兜底；每5分钟错误率公式；月度服务费用＝单实例且代金券不计入） | `sla-agreement-fulltext-terms-alicdn` | ✅ 逐字（5/5，与 raw:32-42 一字不差） |
| V17 | `aliyun-ai-gateway-billing.md:865` 附近 §3.9.5 | SLA §3.2「每月第五（5）个工作日后…相关月份结束后两（2）个月内提出。超出申请时限的赔偿申请将不被受理。」 | `sla-agreement-fulltext-terms-alicdn` | ✅ 逐字（raw:152） |
| V18 | `aliyun-ai-gateway-billing.md:877` 起 §3.9.6 | SLA §2.3 十一条除外情形，含原文编号缺陷 (1)(2)(3)(3)(4)(5)(6)(7)(9)(10)(11) | `sla-agreement-fulltext-terms-alicdn` | ✅ 逐字（11 项内容与编号**全部与 raw:78-98 一致**；「（3）重复、（8）缺失」为 raw 真实缺陷，照录正确） |

**小计：18 条抽样，17 ✅ 逐字 / 1 ❌ 缺陷。**

### 1.3 `[推断]` 推理链可导出性（抽 7 条，要求 5 条）

| # | 文件:行号 | 推断结论 | 推理链前提是否都在 raw | 判定 |
|---|---|---|---|---|
| I1 | `aliyun-ai-gateway-billing.md:765-776` | SLA 月度「错误预算」：普通实例 S≤0.864 ≈ 4.32 分钟/月；serverless S≤8.64 ≈ 43.2 分钟/月；2 月按 28 天为 0.8064/8.064 | ✅ 前提＝raw §2.1 公式 + 注「12 x 24 x 该服务周期的天数」+ §2.2 两个承诺值。算术复算：(1−0.9999)×8640=0.864、×5min=4.32；(1−0.999)×8640=8.64、×5=43.2；12×24×28=8064 → **全对** | ✅ 未越界（明确标 `[推断]`，并声明「SLA 原文只给公式、不给分钟数」） |
| I2 | `aliyun-ai-gateway-billing.md:353` | 同一次调用走 Model API 的 CU 成本是 Agent API 的 5 倍、MCP Server 的 2 倍 | ✅ 前提＝raw 系数 Model 10／MCP 5／Agent 2（`serverless-old-billing-details`）。10÷2=5、10÷5=2 → **对** | ✅ 未越界 |
| I3 | `aliyun-ai-gateway-auth.md:1090` | SLR-A 165 条去重 Action 中 94 条为写/变更类（≈57%），故 SLR 是「不可收窄的账号级宽权限面」 | ✅ 前提＝raw Action 清单 + `Resource` 全为 `"*"` + 「本策略由APIG定义和使用，您不能修改或删除」。**本审计用其自述口径（Describe/List/Get/Query/Search/Check/Read 前缀归只读）独立复算 → 只读 71／写 94，94/165=56.97%** | ✅ 未越界，且**方法可复现**；已自我声明「此归类为 SA 自行推导，不可当作官方口径引用」 |
| I4 | `aliyun-ai-gateway.md:531-535` | `what-is-an-ai-gateway`「单个AI网关实例最多可关联3个容器集群」只对 **Small 档专享实例**成立；Medium/Large 为 5，Serverless(旧/企业版) 为 1，标准版 N/A | ✅ 前提 A＝raw `what-is-an-ai-gateway:140` 逐字；前提 B＝`capacity-description` K8s服务来源数行 `1/N-A/1/3/5/5`。3 恰为 Small 档值 → **推理成立** | ✅ 未越界，`[官方矛盾]` 双方原文并列且明示不裁决 |
| I5 | `aliyun-ai-gateway-plugins.md:1428` | 官方基准的自定义插件单请求开销约是 key-auth 的 **6~10 倍** | ✅ 前提＝190~210微秒（0.19~0.21毫秒换算）vs 20~30微秒。190/30=6.33、210/20=10.5 → 区间正确；并自我限定「两者工作负载不同，不可推广为『自定义插件一定慢 10 倍』」 | ✅ 未越界 |
| I6 | `aliyun-ai-gateway-traffic.md:583` | 控制台限流①与 OpenAPI Token 限流② 是**同一策略的两个配置面** | ✅ 5 条前提中 4 条实测成立：`type="AiTokenRateLimit"`、6 种判断条件↔limitType、3 种单位↔limitMode、`x-higress-llm-model` 转换一致；「三段文字逐字相同」中 **2 段确为逐字**（固定 TTL 段、分布式偏差段），**第 3 段有 1 处标点差**（见 §2 D6 观察项） | ✅ 结论未越界（标点差不影响同一策略判定）；已声明「两页均未明文声明二者为同一策略 → 标 [推断]」 |
| I7 | `aliyun-ai-gateway-plugins.md:265` | `ai-cue-template` 页实际承载 **ai-prompt-decorator**、`ai-cue-decorator` 页实际承载 **ai-prompt-template**（两 slug 语义互换） | ✅ 4 条前提实测全部为真：`ai-cue-template` 正文优先级 450 + prepend/append；`ai-cue-decorator` 正文 500 + templates；`upload-plug-in` 总表 ai-prompt-decorator=450 / ai-prompt-template=500；`geographic-location-of-ip` 页确以「AI提示词**装饰器**插件」+「ai-prompt-decorator」称呼 prepend/append 能力 | ✅ 结论成立（其**佐证之一的引用文字**有误 → 见 DEF-6，属引用瑕疵不属推断越界） |

**小计：7 条抽样，7 ✅ 推理链可从 raw 导出 / 0 ❌ 越界。**（另记 1 条 D6 边缘观察项，非缺陷计数）

### 1.4 `[文档未说明]` 反查（抽 7 条，要求 5 条）—— 全库 grep，不限所标 slug

| # | 文件:行号 | 声称查无的事项 | 全库反查结果 | 判定 |
|---|---|---|---|---|
| U1 | `aliyun-ai-gateway-billing.md:448`（并见 `:11`、`aliyun-ai-gateway.md:10/1284/1337`） | AI Credits 折算率：「一次智能路由决策消耗多少 Credit、**按请求次数还是按 Token 还是按候选模型数折算** —— `[文档未说明]`」；主页更称「**全库查无**」 | ❌ **raw 里有**：`model-metadata.md:64`「以下参数为可选配置，**用于控制模型调用时的 Credits 消耗**」；`:65` 输入/输出/缓存 Token 消耗三项均写「**单位 Credits/1M tokens**，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0」；`:23`「**Credits 信息**：输入/输出/缓存 Token 消耗的 Credits 单价」→「按 Token 折算」这一支**已被 raw 明确回答** | ❌ **D3**（DEF-3） |
| U2 | `aliyun-ai-gateway-traffic.md:989` | Token 限流「**超限返回什么？**」＝`[文档未说明]`（限定 current-limiting 与 configure-a-modelapi-throttling-policy 两页） | ❌ **raw 里有**：`custom-response-plugin.md:54`「**触发网关限流时一般会返回429状态码**，这时请求将返回自定义应答如下。」+ `:48` `enable_on_status: - 429` 完整配置样例。该页对「网关限流」作**一般性**陈述，未排除 AiTokenRateLimit | ❌ **D3**（DEF-4） |
| U3 | `aliyun-ai-gateway-auth.md:909` | ⑦ **网关自身的出口 IP 清单**（客户需在上游 LLM 供应商侧加白的地址） | ✅ **确无**：全库 grep `出口IP｜出口 IP｜网关的公网IP｜回源IP` → **0 命中** | ✅ 判定正确 |
| U4 | `aliyun-ai-gateway-billing.md:871` 附近 §3.9.5 | SLA 赔偿**申请渠道/入口**（工单、控制台入口或表单） | ✅ **确无**：全库 grep `赔偿申请｜索赔｜提交工单.*赔偿` → 仅命中 `sla-agreement-fulltext-terms-alicdn:150/152` 的「3.2赔偿申请时限」正文，**通篇无渠道/入口** | ✅ 判定正确 |
| U5 | `aliyun-ai-gateway.md:518` 附近 §2.7 | 配额提升（白名单）的**申请入口、审批时效、可提升倍数上限** | ✅ **确无**：全库 grep「白名单」相关命中仅 `capacity-description` 的「不属于标准配额范围/不作 SLA 承诺」与 `consumer-quotas-management` 的「只改变可用上限」，**无任何申请流程** | ✅ 判定正确 |
| U6 | `aliyun-ai-gateway-billing.md:304` 与 `:578` | 「Serverless（旧）…**存量实例能否／如何迁移到新版**」`[文档未说明]`；`:578` 汇总表更以**无 slug 限定**的口径写「旧版→新版迁移｜🔴 `[文档未说明]` **无迁移方案**、无停售/下线时间表」 | ❌ **raw 里有（「能否」被明确回答）**：`ai-gateway-capacity-description.md:153` 有独立小节「**### 从 Serverless（旧）迁移到新版 Serverless**」；`:116`「已有 Serverless（旧）实例的客户，可根据业务需求**逐步评估迁移到新版 Serverless 或实例型独享版**」；`:34`「**迁移路径更明确**…已有客户可…**逐步评估迁移**到新版」；`:118`「如需新购 Serverless（旧），请以控制台可购买范围和产品规则为准」（即**未停售**）。「如何」的具体操作步骤确无 | ❌ **D3**（DEF-5，部分成立） |
| U7 | `aliyun-ai-gateway-traffic.md:1119` 附近 §5.8 | **语义缓存的 TTL** —— 「语义化缓存段没有任何 TTL / 缓存时长 / 过期配置项」 | ✅ **确无**：`ai-cache-1.md` 全文 `TTL｜缓存时长｜过期` 仅命中 **1 处**（`:117`，属**精确缓存**段「缓存时长（秒）默认为1800秒」）；语义缓存配置段（`:66-91`）实测只有 缓存键生成策略／文本向量化(AI服务·模型名称·超时5000ms)／向量库(服务提供者·服务地址·Collection·API Key·相似度阈值·超时3000ms)，**无 TTL** | ✅ 判定正确 |

**小计：7 条抽样，4 ✅ 判定正确 / 3 ❌ D3。**

---

## 2. 缺陷明细（按 D1~D8 分组）

### D1 数字失真 —— **0 条**

抽样的 42 条数字断言 + §1.1b 的 9 项整表级机械复算中，**未发现任何一处数值、单位、地域/实例类型/版本限定条件与 raw 不符**。特别复核过的易错点全部通过：
- 45 行价格表逐格（含 `1,212.09075`／`610,895.22` 这类 5 位小数与千分位混排）→ 0 差异；
- 13 列 × 10 行配额表（含官方把 `aigw` 误写为 `apigw` 的 8 个列名）→ 知识页照录错字并在 §2.1 标 `[官方矛盾]`，未「顺手修正」；
- SLA 展平表的 rowspan 重建（4 个 U+FEFF 占位符的行号自述 120/126/138/144）→ 与 raw 实测行号**逐一相符**；
- 单位陷阱：微秒（key-auth 20/basic-auth 30）vs 毫秒（0.19~0.21）未被混用，且知识页主动写出换算并警告「两个不同单位，不可混用」。

### D2 无源断言 —— **0 条**（另记 1 条 P2 溯源缺口，不计入 D2）

未发现蒸馏员用先验知识冒充产品事实的情形。唯一接近的边界情形已查明**不是**先验知识：

- `aliyun-ai-gateway.md:1260`（§15.2 产品族三兄弟）「原 API 网关…**2026-08-23 停止新购、2027-09-21 全面下线**，存量迁云原生API网关」；同页 `:37` 亦出现该日期。
  - 全库反查：`raw/aliyun-docs/ai-gateway/*.md` 中 `2026-08-23｜2027-09-21｜停止新购｜全面下线` **0 命中**。
  - 但**可溯源**：`tests/api-gateway-parent-llms-2026-09-21.txt:41` 逐字为「…产品将于 **2026 年 8 月 23 日停止新购、2027 年 9 月 21 日全面下线**，存量实例请迁移至云原生 API 网关。」同文件 `:3` 亦支撑「RESTful/SOAP 接口托管与 SDK 自动生成」、`:40` 支撑「Envoy 内核和开源 Higress…三合一」。→ **非编造**。
  - **P2 溯源缺口**：该行**未带任何 slug／制品路径标注**，而其来源是 `tests/` 工艺制品而非 `raw/`；按本家族自己的图例（`[官方｜slug]` = 「raw 快照有明文依据」），§15.2 三行均属**图例体系外的无标注断言**。SA 若被追问出处将无法从知识页定位。
  - 同类：`aliyun-ai-gateway.md:1252`（§15.1 一句话定位）见 D7 DEF-7。

### D3 空白被填 —— **4 条**（🔴 P0，本次最严重的缺陷类型）

#### DEF-1 🔴 P0｜D3 + D8｜`knowledge/aliyun-ai-gateway.md:955`（§2.12 A 表 2026-07 行）

- **知识页原文**：
  > | 2026-07 | **新功能** | 「**多租 Serverless 正式开启公测**，提供**企业版与标准版**，**最低 0 起步**，**公测期间免费试用**」 | 🔴 新版 Serverless 的起点。**截至快照日 2026-09-21 仍处公测**；公测结束时间、免费范围、转商用后计费口径**全部未说明**（见 §2.5 [官方矛盾]） |
- **raw 原文**（`ai-gateway-commercialization-announcement.md`，`migration_status: current`、`fetch_date: 2026-09-21`）：
  > `:11` 尊敬的阿里云用户，AI 网关 Serverless 新版公测将于 **2026 年 8 月 31 日** 结束，并自 **2026 年 9 月 1 日**起正式商业化。
  > `:14` 自 2026 年 9 月 1 日起，AI 网关 Serverless 新版结束公测，**正式商业化并开始计费**。
  > `:17` 存量公测实例将**默认保留并自动转为商业化实例**，实例配置和业务数据无需迁移。
  > `:19` 如您不再需要继续使用相关实例，请在 **2026 年 9 月 1 日正式商业化前提前删除**，避免商业化后产生费用。
- **缺陷**：三重错误叠加。(a) **把已结束的状态写成现在时**——快照日 2026-09-21 已在商业化（09-01）之后 **20 天**，「仍处公测」为假；(b) **把 raw 明文写了的三项说成「全部未说明」**——公测结束时间（08-31）、转商用后计费口径（09-01 起开始计费）、免费范围（公测期网关自身费用不收费，见 `announcement-…-public-beta:28`）三项**全都有**；(c) **D8 时效性丢失**——「公测期间免费试用」被放进「SA 含义」列时未带 2026-07-31~08-31 的时间边界。
- **交叉证据（同一 KB 内部自相矛盾）**：`aliyun-ai-gateway-billing.md` §3.8.1 时间线**完整且正确**地记录了 2026-08-31 结束 / 2026-09-01 商业化 / 存量自动转换 / 「9 月 1 日前删除」窗口在快照时点**已关闭**，并 7 次引用 `ai-gateway-commercialization-announcement`。而主页对该 slug 的引用次数为 **0**。
- **对客后果**：SA 读主页速查会告诉客户「Serverless 新版还在公测、还免费」，实际已计费 20 天；客户公测期建的实例已按商业化口径扣费。**这是本次审计发现的唯一会直接导致对客报错价格/报错状态的缺陷。**

#### DEF-2 🔴 P0｜D3（+ D5 矛盾未标）｜`knowledge/aliyun-ai-gateway.md:481`（§2.5 `[官方矛盾]` 块第 3 项）

- **知识页原文**：
  > - **时间边界**：公测起点为 **2026-07**（发布记录口径）；**公测结束时间、结束后计费如何切换、免费范围是否含企业版实例费，两页均未说明** → **文档级空白**。SA 报价时不得把「免费」写进方案，必须走购买页核验。
- **raw 原文**：同 DEF-1 四条；另 `announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta.md:14`「AI 网关 Serverless 新版公测时间为 **7 月 31 日至 8 月 31 日**」、`:28`「公测期间，AI 网关 Serverless 新版的**网关自身费用不收费**，仅**公网入网流量按照 CDT…计费**」、`:29` 表内「AI 网关 Serverless 新版网关自身费用｜不收费」（**未按标准版/企业版区分，即含企业版实例费**）。
- **缺陷**：三个被声称「未说明」的问题**全部有明文答案**：结束时间＝2026-08-31；计费切换＝2026-09-01 起商业化计费、入网流量出账主体由 CDT 迁到网关侧 0.8 元/GB（billing §3.8.1 已正确记录此迁移）；免费范围是否含企业版实例费＝含（「网关自身费用不收费」未区分版型）。
  虽然句中有「**两页**均未说明」的范围限定词（就 `new-feature-release-notes-ai-gateway` 与 `ai-gateway-capacity-description` 这两页而言为真），但：(i) 结论落点是无限定的「→ **文档级空白**」；(ii) 家族图例把 `[文档未说明]`/空白定义为「**raw 查无此项**」（全库口径），故此处违反自定语义；(iii) **D5**：该 `[官方矛盾]` 块只并列了发布记录与网关类型页两方，**漏掉了能终结该矛盾的第三方页面**（商业化公告），使一个 raw 中已有确定答案的问题被固化为「不裁决的矛盾」。
- **对客后果**：与 DEF-1 同源，会让 SA 在报价单上写「公测免费（口径未定）」而不是「已于 2026-09-01 起商业化计费」。

#### DEF-3 🔴 P0｜D3｜`knowledge/aliyun-ai-gateway-billing.md:448`（§3.5.4）+ `aliyun-ai-gateway.md:10 / 1284 / 1337`

- **知识页原文**（billing:448）：
  > 官方说「按实际使用量折算为 Credits 消耗」、「Credits 消耗量与实际使用的 AI 增强能力类型和用量相关」，但**全页没有给出任何折算率**：一次智能路由决策消耗多少 Credit、**按请求次数还是按 Token 还是按候选模型数折算** —— `[文档未说明]`。
  （主页 `:10`「AI Credits 折算率**全库查无**」；`:1284`「🔴 **AI Credits 折算率全库查无** —— 「一次智能路由消耗几个 Credit」无法从文档得出」；`:1337` §15.9 必核清单「| AI Credits 折算率 | **全库查无** | 工单 |」；billing `:511` 空白登记 G9「全页无此项」）
- **raw 原文**（`model-metadata.md`）：
  > `:64` 以下参数为可选配置，**用于控制模型调用时的 Credits 消耗**。
  > `:65` 输入 Token 消耗｜选填。**单位 Credits/1M tokens**，如填写必须为大于等于 0 的数字，最多两位小数。默认值为 0（输出 Token 消耗、缓存 Token 消耗同）
  > `:23` **Credits 信息**：输入/输出/缓存 Token 消耗的 Credits 单价。
- **缺陷**：知识页把折算维度枚举成「按请求次数 / 按 Token / 按候选模型数」三选一并判为查无，而 raw **明确回答是「按 Token」**，且给出了量纲 `Credits/1M tokens` 与三项（输入/输出/缓存）分别计价的结构。
  **同一 KB 内部反证**：`aliyun-ai-gateway-traffic.md:244`、`:274`、`:1291`、`:1310` **四处正确记录了** `Credits/1M tokens` 与默认 0、最多两位小数；`:1048`/`:1343` 也只把「**换算公式**」列为查无（措辞准确）。即 W5 拿到了事实、W2 与主控在主页写成了「全库查无」——**主页的「全库查无」被本家族自己的 traffic 页证伪**。
  **公允界定**：`model-metadata` 的 Credits 单价是**用户选填的模型元信息**（默认 0，服务于 FinOps/Token 用量看板核算），**不是** AI Credits 计费商品的官方公布折算率；「一次**智能路由**决策消耗几个 Credit」这一**具体**问题确仍查无。因此缺陷落在「**全库查无**」这个全库级否定词与「按请求次数还是按 Token」这个已被回答的枚举上，不落在「智能路由单价未知」上。
- **对客后果**：中等偏高。SA 会对客说「文档完全没写 Credits 怎么折算」，从而漏掉「模型元信息里可按 Credits/1M tokens 配置输入/输出/缓存三项单价」这一**客户自己就能配**的成本核算抓手；同时 §15.9「报价前必核清单」把一个部分可答项列为纯工单项。

#### DEF-4 🔴 P0｜D3｜`knowledge/aliyun-ai-gateway-traffic.md:989`（§5.6 Token 限流计量口径表）

- **知识页原文**：
  > | **超限返回什么？** | **[文档未说明]** —— current-limiting 与 configure-a-modelapi-throttling-policy 两页**均未给出限流触发后的 HTTP 状态码、响应体或错误码**。（对照：`more-policies-and-plugins` 的流量控制/并发控制/熔断策略明确「Http状态码……默认为429」，但那是**另一套策略**，不能直接套用到 AiTokenRateLimit） |
  同一判断在主页面被放大为对客口径：`aliyun-ai-gateway.md:1238`「**只有④写了「Http状态码默认为429」，①②③的超限返回码全部 `[文档未说明]`，不可类推。**」
- **raw 原文**（`custom-response-plugin.md`）：
  > `:54` **触发网关限流时一般会返回429状态码**，这时请求将返回自定义应答如下。
  > `:47-50` 配置样例：`enable_on_status:` `- 429` / `status_code: 302` / `headers:` `- Location=https://example.com`
  > `:56-59` 对应响应：`HTTP/1.1 302 Found` / `Location: https://example.com`
- **缺陷**：raw 存在一条对「**网关限流**」作**一般性**陈述的原文（未限定策略种类、未排除 AiTokenRateLimit），并给出可自定义 429 响应的完整配置路径。按家族图例（`[文档未说明]` = 「**raw 查无此项**」，全库口径），此格应为「raw 有『一般会返回 429』的概括性表述（`custom-response-plugin`），但未针对 AiTokenRateLimit 单独确认」，而非「查无」。
  该页已主动做了跨页对照（引 `more-policies-and-plugins` 的 429 并说明不可类推），说明**作者做过跨页检索但漏检了 `custom-response-plugin`**——而 `custom-response-plugin` 正是 W6（plugins）分片内的页，且 `aliyun-ai-gateway-plugins.md:1152` **已正确引用了这句 429**。→ 又是一处「一个 worker 拿到事实、另一个 worker 判为查无」的家族级漏检。
- **对客后果**：中等。SA 会对客说「文档没写限流返回什么码」，而客户在 `custom-response` 插件页能直接看到「一般会返回429」；且漏掉了一个真实可用的方案（用 `enable_on_status:[429]` + `status_code:302` 把限流打到友好页）。

#### DEF-5 🔴 P0（部分成立）｜D3｜`knowledge/aliyun-ai-gateway-billing.md:304`（§3.4.1）与 `:578`（§3.8.1 汇总表末行）

- **知识页原文**：
  > `:304` 🔴 `[文档未说明]` Serverless（旧）是否**停售**、是否有**下线时间表**、存量实例**能否／如何迁移到新版** —— 三页（旧版计费说明、公测公告、商业化公告）均无迁移方案。商业化公告只讲了「存量**公测**实例」的处理（见 §3.6），**没讲 Serverless（旧）存量实例**。
  > `:578` | 旧版→新版迁移 | 🔴 `[文档未说明]` **无迁移方案**、无停售/下线时间表 | — |（来源列为「—」，即**无 slug 限定的全库级否定**）
- **raw 原文**（`ai-gateway-capacity-description.md`）：
  > `:153` **### 从 Serverless（旧）迁移到新版 Serverless**（独立小节）
  > `:155` 如果您希望降低使用门槛并快速体验新版 AI 能力，可以评估 Serverless 标准版。如果您希望获得生产级入口、自定义域名和更高服务等级，可以评估 Serverless 企业版。如果原实例承载核心高流量业务或依赖完整高级治理能力，可以评估实例型独享版。
  > `:34` **迁移路径更明确**：已有 Serverless（旧）实例可继续使用；新客户建议优先选择新版…已有客户可根据业务阶段、入口能力、服务等级和治理能力需求，**逐步评估迁移**到新版 Serverless 或实例型独享版。
  > `:116` 已有 Serverless（旧）实例的客户，可根据业务需求**逐步评估迁移**到新版 Serverless 或实例型独享版。
  > `:118` **如需新购 Serverless（旧），请以控制台可购买范围和产品规则为准。**
- **缺陷**：「**能否**迁移」被 raw 明确回答为**能**（且有专门的「迁移建议 → 从 Serverless（旧）迁移到新版 Serverless」小节给出三条按业务画像选目标形态的指引）；「**是否停售**」被 `:118` 反向否证（官方仍在讲「如需新购 Serverless（旧）」的可购买范围，即未宣布停售）。`:578` 那行以无 slug 限定的口径写「无迁移方案」，按家族图例属**把 raw 有的说成没有**。
  **公允界定**：`:304` 有「三页（旧版计费说明、公测公告、商业化公告）」的范围限定，就这三页而言为真；且 raw 确实**没有**「如何迁移」的**技术操作步骤**（无数据/配置搬迁流程、无双跑切换指引），也**没有**下线时间表。故本条为**部分成立**：错在把「无操作步骤」写成「无迁移方案／能否未说明」，并以无限定形式进汇总表。
  注：W2 在 §3.4.6 曾引用 `ai-gateway-capacity-description`（说明该页在其视野内），却未回查该页的「迁移建议」小节。
- **对客后果**：中等。SA 会对存量旧版客户说「官方没有迁移方案」，而官方其实给了目标形态选型指引；也会漏掉「旧版目前仍可按控制台可购买范围新购」这一事实。

### D4 引用不逐字 —— **1 条**（🟠 P1）

#### DEF-6 🟠 P1｜D4 + D7｜`knowledge/aliyun-ai-gateway-plugins.md:263`（§9.2.2）

- **知识页原文**：
  > 第三方交叉验证（`geographic-location-of-ip` 页）：`[官方原文]`「**AI提示词装饰器插件的配置示例如下**：`prepend: - role: system …`」—— 即 `prepend`/`append` 结构对应**装饰器（decorator）**，与 `ai-cue-template` 这个 slug 的字面语义相反。
- **raw 实测**：
  - `geographic-location-of-ip.md:48` 实际为：「**AI提示词插件的配置示例如下：**」（**无「装饰器」三字**）
  - 被引字符串「AI提示词装饰器插件的配置示例如下：」在 `geographic-location-of-ip.md` 中出现次数 = **0**；它只出现在 **`ai-cue-template.md:86`**
  - 归一化后字符级双向比对：`❌ ABSENT from geographic-location-of-ip` / `✅ FOUND in ai-cue-template`
- **缺陷定性**：标了 `[官方原文]` 却**不是该 slug 的原文**（D4）；同时**归错了 slug**（D7）。差异不是格式归一化（不是 `<br>`、表格、markdown 链接、空白、引号），而是**实词「装饰器」的增删** —— 而「装饰器」三字恰恰是这条佐证唯一的论证载荷（用来证明 prepend/append 对应 decorator）。
- **公允界定（缺陷影响面小）**：该页**另有**支撑同一结论的原文，且知识页在别处已正确引用：`geographic-location-of-ip.md:38` 小节标题「基于geo-ip插件的能力，扩展**AI提示词装饰器**插件携带用户地理位置信息」、`:39`「请确保同时开启geo-ip插件和**AI提示词装饰器插件**…**ai-prompt-decorator** 插件的priority配置500」。`aliyun-ai-gateway-plugins.md:328` 与 `aliyun-ai-gateway.md:1229`（§14.10）引用的正是这些**真实存在**的句子且逐字无误。→ **§9.2.2 的最终结论（两 slug 语义互换）成立**，只是这一条佐证引错了句子和页。
- **对客后果**：低（结论不受影响）。但**工艺后果不低**：这是全库唯一一处 `[官方原文]` 标签下的实词级失真，会削弱「凡标 `[官方原文]` 即可闭眼照抄」这条使用契约的可信度；且客户若按 slug 去官网核对这一句会核不上。

### D5 矛盾未标 —— **1 条**（并入 DEF-2，不重复计数）

- `aliyun-ai-gateway.md:478-481` 的 `[官方矛盾]`「Serverless 是否处于公测 + 免费状态」只并列了 `new-feature-release-notes-ai-gateway`（2026-07 开启公测、免费试用）与 `ai-gateway-capacity-description`（0 元起步/有实例费，全页无「公测」「免费」字样）两方，**未纳入 `ai-gateway-commercialization-announcement`**（公测 2026-08-31 结束、2026-09-01 起商业化计费）。第三方页面**足以终结该矛盾**（两页并不冲突：一页讲 7 月开的公测、一页讲 9 月已转商用，是时间先后而非口径冲突），漏纳导致一个**已有确定答案的问题被标成「不裁决的官方矛盾」**，并进一步衍生 DEF-1／DEF-2 的「未说明」。
- **对照（做得对的部分）**：本审计另行抽验的 5 处 `[官方矛盾]` **全部为真矛盾**，不是蒸馏员臆造：
  1. SLA 99.90% vs 产品页 99.95%（企业版 0.05pp 无赔偿区）— `sla-…:66` vs `ai-gateway-capacity-description` 能力对比表「服务等级」行 ✅
  2. Nacos「企业版」vs「铂金版」— `synchronizing-nacos-mcp-services:14` vs `mcp-service-management:102` ✅
  3. 语义检索「均在350毫秒以内」vs 表内 RRF k=10 = 0.3519s — `semantic-retrieval:128` vs `:68` ✅
  4. IP 黑白名单「网关全局、域名和路由级别」三级 vs 配置项表仅两级 — `set-the-gateway-ip-whitelist-and-whitelist:11` vs 同页配置表「生效粒度」行 ✅
  5. RAM「访问级别取值为 Write/Read/List」vs 表内实为 none/get/list/create/delete/update（96 个 none）— `api-apig-2024-03-27-ram-ai-gateway` 说明文字 vs 表格实测 ✅

### D6 推断越界 —— **0 条**（另记 1 条边缘观察项，不计入缺陷）

7 条 `[推断]` 抽样全部可从其引用的官方事实导出，无一处偷渡先验知识；且每条都自带「官方未明写／不可当作官方口径引用」的自我限定。算术类推断（I1 错误预算 0.864/8.64/4.32min/43.2min/8064；I2 5倍/2倍；I3 只读71写94、94/165=56.97%；I5 6~10倍）**本审计逐条独立复算，全部成立**。
唯一使用了 raw 之外知识的推断是 `aliyun-ai-gateway-ops.md:1082` 附近对配额记法 `N/M(s)` 的解释（「按**阿里云通用流控记法**，表示 M 秒内最多 N 次」），但已明示「**此推断未经 raw 证实**，SA 对客报数时应同时给出原文记法」→ 属**已披露**的外部知识，不构成越界。

- **观察项（不判缺陷）**：`aliyun-ai-gateway-traffic.md:583` 的 `[推断]` 推理链中称「两页的『固定 TTL 时间窗口』说明段、『更新配置后……通常在几秒内生效』、『分布式架构……轻微偏差』**三段文字逐字相同**」。实测：第 1、3 段确为逐字相同；第 2 段有**一处标点差** —— `current-limiting.md:222`「…推送到网关数据面**，**通常在几秒内生效。」vs `configure-a-modelapi-throttling-policy.md:417`「…推送到网关数据面**。**通常在几秒内生效。」（逗号 vs 句号）。属纯标点、不改变语义，且不影响「同一策略两个配置面」的结论 → 记为「逐字相同」措辞的轻微过强，非 D4/D6 缺陷。

### D7 归属／引用错 slug —— **2 条**（🟡 P2 / 🟠 P1）

#### DEF-7 🟡 P2｜D7｜`knowledge/aliyun-ai-gateway.md:1252`（§15.1 一句话定位）

- **知识页原文**：
  > AI 网关 = **云原生 API 网关面向 AI 原生应用的托管入口**，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，**兼容 OpenAI 协议**；支持 **Model API / Agent API / MCP Server** 三类接入。`[官方｜what-is-an-ai-gateway]`
- **raw 实测**（对 `what-is-an-ai-gateway.md` 逐关键词计数）：

  | 关键词 | 在 `what-is-an-ai-gateway` | 在全部 186 个快照 |
  |---|---|---|
  | `托管入口` | **0** | **0** |
  | `兼容 OpenAI 协议`／`兼容OpenAI协议` | **0** | **0** |
  | `Model API/Agent API/MCP Server` | **0** | **0** |
  | `MiniMax` | **0** | 2（`deepseek-integration-through-ai-gateway` 等） |

  该句实际逐字出自 **`tests/api-gateway-parent-llms-2026-09-21.txt:42`**（父级 llms.txt「## 子产品 → AI 网关」条目描述）：「AI 网关是云原生 API 网关面向 AI 原生应用的**托管入口**，统一代理百炼/OpenAI/MiniMax/Anthropic/Amazon Bedrock/Azure 及 Ollama/vLLM/SGLang 自建模型，**兼容 OpenAI 协议**；支持 **Model API/Agent API/MCP Server** 三类接入…」。
- **缺陷**：内容真实、可溯源，但**标注的 slug 里没有该内容**（该内容在 `raw/` 内 0 命中，只存在于 `tests/` 的父级 llms.txt 制品）。按 D7 定义＝「标注的 slug 里没有该内容（内容在别的页）」。
- **对客后果**：低（该句是官方 llms.txt 的产品自述，本身可引）；但 §15.1 是「对客必背」速查卡的第一行，SA 被客户或同事追问出处时会被指向一个**不含该句**的 raw 页面，白白消耗信任。

#### DEF-6（同上，D4 + D7 并发）——见 D4 段，不重复计数。

- **对照（slug 归属做对的部分）**：本次抽验中所有**跨页易混 slug** 的归属均正确，包括最易错的一组：`capacity-description`（配额/QPS，专享实例版）与 `ai-gateway-capacity-description`（实例类型/服务等级）是**两个不同的 raw 文件**，知识页在 §2.4/§2.5/§2.6/§2.7 中**分别正确引用**，未混用；`ai-cue-template`↔`ai-prompt-decorator`、`ai-cue-decorator`↔`ai-prompt-template` 的官方错位被主动识别并给出「对客必须写插件名不要写 slug」的纪律；`gateway-managed-mcp-services` 与 `mcp-gateway-management` 的别名关系用 body_sha256 实测证明（本审计复核 sha 与 bytes 完全相同）。

### D8 时效性丢失 —— **1 条**（并入 DEF-1，不重复计数）

- `aliyun-ai-gateway.md:955` 把「公测期间免费试用」写进「SA 含义」列并断言「截至快照日 2026-09-21 **仍处公测**」，未带 2026-07-31~2026-08-31 的时间边界（该边界在 raw `announcement-…-public-beta:14` 与 `ai-gateway-commercialization-announcement:11` 中均有明文）。
- **对照（时效性做对的部分）**：`aliyun-ai-gateway-billing.md` §3.8.1 专门设立「🔴 公测口径必须带时间边界，不能写成现在时」小节，正确写出「公测窗口 = 2026-07-31 ～ 2026-08-31（共 32 天）」并披露「**公测公告全文没有出现年份**，年份只能从商业化公告反推」；§3.8.1 末还标注「🔴 **已过期动作项**：『9 月 1 日前删除』这一窗口在快照时点（2026-09-21）**已关闭**」；`aliyun-ai-gateway-traffic.md:1067`、`aliyun-ai-gateway-plugins.md` 等亦对「新增 FinOps 功能」等无日期表述统一挂「上线时间 `[文档未说明]`」。**7 个文件中 6 个的时效性处理是规范的，问题集中在主页 §2。**

---

## 3. 保真率

### 3.1 按抽样类型

| 抽样类型 | 抽样数 | ✅ 一致 | ❌ 缺陷 | 保真率 |
|---|---|---|---|---|
| 带数字的断言（6/文件 × 7） | 42 | 41 | 1 | **97.6%** |
| `[官方原文]` 字符级逐字 | 18 | 17 | 1 | **94.4%** |
| `[推断]` 推理链可导出性 | 7 | 7 | 0 | **100%** |
| `[文档未说明]` 全库反查 | 7 | 4 | 3 | **57.1%** |
| **合计** | **74** | **69** | **5** | **93.2%** |

### 3.2 按缺陷类型（去重后的独立缺陷实例 = 7 条）

| 类型 | 条数 | 严重度 | 实例 |
|---|---|---|---|
| D1 数字失真 | **0** | — | —（42 条数字断言 + 9 项整表机械复算全过） |
| D2 无源断言 | **0** | — | —（另记 1 条 P2 溯源缺口：§15.2 三行无 slug 标注，源在 `tests/` 制品而非 `raw/`） |
| **D3 空白被填** | **4**（+1 部分成立，共 5 处文本） | 🔴 **P0** | DEF-1（main:955）、DEF-2（main:481）、DEF-3（billing:448 + main:10/1284/1337）、DEF-4（traffic:989 + main:1238）、DEF-5（billing:304/578，部分成立） |
| D4 引用不逐字 | **1** | 🟠 P1 | DEF-6（plugins:263） |
| D5 矛盾未标 | **1**（并入 DEF-2） | 🟠 P1 | main:478-481 漏纳 `ai-gateway-commercialization-announcement` |
| D6 推断越界 | **0** | — | —（另记 1 条边缘观察：traffic:583「三段逐字相同」实为 2 段逐字 + 1 段一处标点差） |
| D7 归属/错 slug | **2** | 🟡 P2 / 🟠 P1 | DEF-7（main:1252）、DEF-6（plugins:263，与 D4 并发） |
| D8 时效性丢失 | **1**（并入 DEF-1） | 🟠 P1 | main:955「仍处公测」写成现在时 |

### 3.3 按文件（缺陷落点分布）

| 文件 | 抽样条数（4 类合计） | ✅ | ❌ | 保真率 | 缺陷 |
|---|---|---|---|---|---|
| `aliyun-ai-gateway.md`（主页 §0/§1/§2/§14/§15） | 6+5+1+1 = 13 | 9 | **4** | 69.2% | DEF-1、DEF-2、DEF-3（部分）、DEF-7 |
| `aliyun-ai-gateway-billing.md`（§3 + §3.9） | 6+3+2+3 = 14 | 12 | **2** | 85.7% | DEF-3、DEF-5 |
| `aliyun-ai-gateway-traffic.md`（§4 + §5） | 6+1+1+1 = 9 | 8 | **1** | 88.9% | DEF-4 |
| `aliyun-ai-gateway-auth.md`（§6 + §7） | 6+2+1+1 = 10 | 10 | 0 | **100%** | — |
| `aliyun-ai-gateway-mcp-agent.md`（§8） | 6+0+0+0 = 6 | 6 | 0 | **100%** | — |
| `aliyun-ai-gateway-plugins.md`（§9） | 6+2+1+0 = 9 | 8 | **1** | 88.9% | DEF-6 |
| `aliyun-ai-gateway-ops.md`（§10~§13） | 6+3+0+1 = 10 | 10 | 0 | **100%** | — |

> **缺陷高度集中在主页（W1／主控自留章节）**：7 条缺陷中 4 条落在 `aliyun-ai-gateway.md`，且**全部 5 处 D3 中有 2 处只在主页出现**。6 个 worker 分片页中，auth／mcp-agent／ops 三个分片**零缺陷**，billing／traffic／plugins 各 1~2 条。

### 3.4 一条贯穿性根因（可复算）

**5 处 D3 中有 4 处的成因是同一个：`[文档未说明]` 被当作「本分片所读页面查无」使用，而家族图例把它定义为「`raw` 查无此项」（全库口径）。**

- 图例原文（7 个文件的第 6 行，逐字相同）：`[文档未说明]` **raw 查无此项**
- 实证：DEF-3 的答案在 `model-metadata`（W5 分片，traffic 页 4 处已正确记录）；DEF-4 的答案在 `custom-response-plugin`（W6 分片，plugins 页 `:1152` 已正确引用）；DEF-5 的答案在 `ai-gateway-capacity-description`（W1 分片，W2 在 §3.4.6 引过该页但未回查其「迁移建议」小节）；DEF-1/DEF-2 的答案在 `ai-gateway-commercialization-announcement`（W2 分片，引用 7 次；主页引用 **0** 次）。
- 即：**答案全部在库内，且 4 次中有 3 次已被本 KB 的另一个文件正确写下**。这不是抓取缺口，是**分片间未做全库反查 + 装配阶段未做跨页一致性校验**。
- 可复算验证命令（任一均可直接跑出上表结论）：
  - `grep -rn "Credits/1M tokens" raw/aliyun-docs/ai-gateway/ knowledge/aliyun-ai-gateway*.md`
  - `grep -rn "触发网关限流时一般会返回429" raw/aliyun-docs/ai-gateway/ knowledge/aliyun-ai-gateway*.md`
  - `grep -n "从 Serverless（旧）迁移到新版" raw/aliyun-docs/ai-gateway/ai-gateway-capacity-description.md`
  - `grep -c "ai-gateway-commercialization-announcement" knowledge/aliyun-ai-gateway.md knowledge/aliyun-ai-gateway-billing.md`
  - `grep -c "AI提示词装饰器插件的配置示例如下" raw/aliyun-docs/ai-gateway/geographic-location-of-ip.md raw/aliyun-docs/ai-gateway/ai-cue-template.md`

---

## 4. 结论

### 4.1 能不能直接拿去对客答疑？

**分级结论：**

- **6 个分片页（billing / traffic / auth / mcp-agent / plugins / ops）——可以带条件对客使用。**
  数字保真率 97.6%（41/42，唯一失分在主页）、`[官方原文]` 逐字率 94.4%、`[推断]` 可导出率 100%。所有价格表、配额表、SLA 条款、错误码分布、OpenAPI/RAM/流控计数经**脚本级整表复算**为**零差异**；`[官方矛盾]` 抽验 5 处**全部为真矛盾**，无一处臆造；官方错字（`Muti`、`finopts`、`apigw.small.x2`、全角「华北２」、SLA 编号 (3) 重复 (8) 缺失）一律照录并标注，未被「顺手修正」。这套页面对「数字类」对客答疑的可靠性已达到可直接引用的水平。
- **主页 `aliyun-ai-gateway.md` 的 §2.5 / §2.12 / §15 —— 不能直接对客，必须先修。**
  §15「SA 速查卡（对客必背）」是全套页面里**最可能被直接照读给客户**的部分，而它恰好坐在 DEF-1／DEF-3／DEF-7 三条缺陷的上游或同页。

### 4.2 必须先修的条目（按修复优先级，全部可定位）

**🔴 P0-1｜DEF-1 + DEF-2 + D5 + D8：Serverless 新版「仍处公测」是错的，且已商业化计费 20 天**

- 修 `aliyun-ai-gateway.md:955`：删除「**截至快照日 2026-09-21 仍处公测**」，改为「公测窗口 **2026-07-31 ～ 2026-08-31**；**2026-09-01 起正式商业化并开始计费**（快照日已在商业化之后 20 天）；存量公测实例默认自动转商业化、无需迁移；『9 月 1 日前删除』窗口在快照时点已关闭」，slug 补 `ai-gateway-commercialization-announcement`｜`announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta`。
- 修 `aliyun-ai-gateway.md:481`：删除「公测结束时间、结束后计费如何切换、免费范围是否含企业版实例费，两页均未说明 → 文档级空白」，改为三问三答（08-31 结束／09-01 起商业化计费、入网流量出账主体由 CDT 迁至网关侧 0.8 元/GB／公测期「网关自身费用不收费」未区分版型即含企业版实例费）。
- 修 `aliyun-ai-gateway.md:478` 的 `[官方矛盾]` 块：纳入第三方页面 `ai-gateway-commercialization-announcement` 并**撤销该矛盾标记**（两页非口径冲突，是时间先后）；如需保留，改标为「已消解的时间线差异」。
- 修 §15.3 / §15.4 / §15.9 中一切依赖「公测免费」现状的措辞（`aliyun-ai-gateway.md:1264` 附近形态选型表、`:1275` 附近三本账）。
- **验收判据**：`grep -n "仍处公测\|两页均未说明" knowledge/aliyun-ai-gateway.md` 返回 0 行；`grep -c "ai-gateway-commercialization-announcement" knowledge/aliyun-ai-gateway.md` ≥ 3。

**🔴 P0-2｜DEF-3：「AI Credits 折算率全库查无」被本 KB 自己的 traffic 页证伪**

- 修 `aliyun-ai-gateway.md:10`、`:1284`、`:1337`：把「**全库查无**」改为「**智能路由等 AI 增强能力的官方折算率查无**；但模型侧 Credits 量纲在库内有明文——`model-metadata` 规定输入/输出/缓存 Token 消耗单位为 **Credits/1M tokens**（选填、最多两位小数、**默认 0**），用于控制模型调用时的 Credits 消耗」。
- 修 `aliyun-ai-gateway-billing.md:448`：删除「按请求次数还是按 Token 还是按候选模型数折算 —— `[文档未说明]`」中的「按 Token」一支（raw 已答），保留「一次智能路由决策消耗多少 Credit」为真查无；`:511` 空白登记 G9 同步收窄口径。
- 与 `aliyun-ai-gateway-traffic.md:244/274/1291/1310`（已正确）和 `:1048/1343`（措辞准确）对齐，消除家族内互斥表述。
- **验收判据**：`grep -n "全库查无" knowledge/aliyun-ai-gateway*.md` 返回 0 行；`grep -c "Credits/1M tokens" knowledge/aliyun-ai-gateway.md knowledge/aliyun-ai-gateway-billing.md` 各 ≥ 1。

**🔴 P0-3｜DEF-4：Token 限流「超限返回什么」不是查无**

- 修 `aliyun-ai-gateway-traffic.md:989`：把「**[文档未说明]**」改为「raw 有概括性表述但非本策略专属：`custom-response-plugin:54`「**触发网关限流时一般会返回429状态码**」，并给出 `enable_on_status:[429]` + `status_code:302` 的自定义应答样例；AiTokenRateLimit 是否适用该 429 未经专页确认 → 该点仍属查无」。
- 修 `aliyun-ai-gateway.md:1238`：把「①②③的超限返回码全部 `[文档未说明]`，不可类推」改为「④明写 429；①②③无专页明文，但 `custom-response-plugin` 有『网关限流一般返回 429』的概括表述，可作为排障起点、不可作为承诺」。
- **验收判据**：`grep -c "custom-response-plugin" knowledge/aliyun-ai-gateway-traffic.md` ≥ 1。

**🟠 P1-1｜DEF-5：Serverless（旧）迁移「无迁移方案」表述过强**

- 修 `aliyun-ai-gateway-billing.md:578`：把来源列「—」改为 `ai-gateway-capacity-description`，把「无迁移方案」改为「**有目标形态选型指引（『从 Serverless（旧）迁移到新版 Serverless』小节 + 逐步评估迁移），但无技术操作步骤／无双跑切换流程；无停售公告（`:118` 仍写『如需新购 Serverless（旧），请以控制台可购买范围和产品规则为准』）、无下线时间表**」。
- 修 `:304`：保留「三页均无迁移方案」的范围限定，但把「存量实例**能否**…迁移到新版」从 `[文档未说明]` 中摘出（`ai-gateway-capacity-description:34/116/153-155` 已答「能，逐步评估迁移」），只留「**如何**迁移的操作步骤」为真查无。

**🟠 P1-2｜DEF-6：`[官方原文]` 引错句子 + 错 slug**

- 修 `aliyun-ai-gateway-plugins.md:263`：二选一——(a) 把 slug 改为 `ai-cue-template`（该句确在 `:86`），并注明这是**同页自证**而非第三方交叉验证；或 (b) 保留 `geographic-location-of-ip` 作为第三方，但把引文换成该页真实存在的句子：`:38`「基于geo-ip插件的能力，扩展**AI提示词装饰器插件**携带用户地理位置信息」或 `:39`「请确保同时开启geo-ip插件和**AI提示词装饰器插件**…**ai-prompt-decorator**插件的priority配置500」（后者更强，因它把「装饰器」与 `ai-prompt-decorator` 直接绑定）。
- §9.2.2 的**结论无需改动**（本审计已独立复核 4 条前提全部为真，slug 语义互换成立）。
- **验收判据**：`grep -c "AI提示词装饰器插件的配置示例如下" knowledge/aliyun-ai-gateway-plugins.md` 为 0，或该行 slug 已改为 `ai-cue-template`。

**🟡 P2-1｜DEF-7：§15.1 一句话定位错标 slug**

- 修 `aliyun-ai-gateway.md:1252`：把 `[官方｜what-is-an-ai-gateway]` 改为 `[官方｜父级 llms.txt 子产品条目]`（制品路径 `tests/api-gateway-parent-llms-2026-09-21.txt:42`），或改引 `what-is-an-ai-gateway` **真实含有**的定位句：「云原生API网关推出AI网关产品，作为企业AI应用与模型服务、工具及其他Agent之间的**核心连接组件**，通过提供协议转换、安全防护、流量治理和统一观测等能力」（raw 概述段）。
- 同类修 `:1258-1260`（§15.2 产品族三兄弟）：三行补注来源＝父级 llms.txt 制品（非 raw 快照），避免 SA 按 `[官方｜slug]` 图例去 raw 找不到。

### 4.3 一句总评

**这套页面的「数字层」是我见过可复算程度最高的一档**——45 行价格表、13×10 配额表、140 个 Action 分 16 组、105 行流控配额、35 个缺口、166/165/71/94 条 SLR Action、67/23/3/13/5 条错误码，全部经脚本独立复算为**零差异**，连官方错字与 rowspan 占位符行号都照实录。**问题不在数字，全在「否定句」**：5 处 D3 里有 4 处是同一台机器出的同一类错——**把 `[文档未说明]` 当「我没读到」用，而图例要求它是「全库查无」**，且答案 4 次中有 3 次已被本 KB 的另一个文件正确写下。因此修复动作不是回源重蒸馏，而是：① 按上面 6 条逐条改文本（都是句子级替换，不动结构）；② 在装配脚本里加一道**跨页否定句门禁**——凡出现 `[文档未说明]`／「全库查无」／「未说明」的行，自动对其关键名词做一次 `raw/` 全库 grep 与 `knowledge/` 全家族 grep，命中即报错。这道门禁能一次性拦住本次全部 5 处 D3。

---

### 附：审计范围与自我声明

- **只读**：`raw/aliyun-docs/ai-gateway/`（186 快照 + README + SHA256SUMS）、`knowledge/aliyun-ai-gateway*.md`（7 文件）、`tests/api-gateway-parent-llms-2026-09-21.txt`（仅用于查证 DEF-7／D2 边界情形的溯源，非评分依据）。
- **只写**：本文件。未修改任何其他文件。
- **实核条数**：数字断言 42（＋9 项整表级机械复算，累计核对单元格 > 300 个）／`[官方原文]` 字符级 18／`[推断]` 7／`[文档未说明]` 全库反查 7 = **74 条抽样**，全部给出 raw 原文片段与行号证据，无一条为「未核即判」。要求为 42+5+5+5，实做 42+18+7+7。
- **未覆盖面（如实声明）**：7 个文件共 9404 行，本次为抽样审计，覆盖率约 0.8%（74/9404 行级采样点，但整表复算使实际核验的**事实单元格**远大于此）；`[官方矛盾]` 只抽验 5 处（全家族标注约 40+ 处未裁决）；`aliyun-ai-gateway-ops.md` §11 门户／§12 七个集成配方的操作步骤类内容未做逐条回源（仅核了配方 7 的全部数字）；`aliyun-ai-gateway-mcp-agent.md` §8.4 HTTP 转 MCP 字段参考（35517 字节源页）的逐字段取值范围未做全量比对。**上述未覆盖面中可能仍存在与 DEF-3／DEF-4 同型的 D3（否定句未做全库反查）缺陷**，建议主控对该缺陷型跑一次全库机械化扫描而非再次抽样。
