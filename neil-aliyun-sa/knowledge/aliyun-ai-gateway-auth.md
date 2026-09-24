# AI 网关 · §6 鉴权与消费者体系 / §7 AI 安全护栏与 RAM 权限

> **所属**：[[aliyun-ai-gateway]] 专题页家族（7 文件）｜**主页与导航**：[aliyun-ai-gateway.md](aliyun-ai-gateway.md)
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（186 个快照 = 149 个有正文页 + 37 个 TOC 容器页；另有 SLA 协议全文外部源 1 页）
> **事实标注体系**：`[官方｜slug]` raw 快照有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方原文错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕见 `tests/ai-gateway-rulings-2026-09-21.md`
>
> 🔖 正文中的 `W1`~`W7` 是**本次蒸馏批次的分工代号**（7 路并行 worker），不是产品术语；对照表见 [主页 §0.6](aliyun-ai-gateway.md)。

🔴 **对客纪律**：自建认证的「鉴权 API + 原始请求 Path 拼接」与「Path 需前缀匹配」是**设计行为不是 bug**，客户认证接口若为精确匹配必然 404，且 404 不在宽松模式（仅覆盖连接失败与 5xx）的兜底范围内 → **即使开了宽松模式也全量拒绝**。🔴 **MCP 消费者认证方式官方口径冲突（裁决 C9 已修订，原「仅支持 API Key、不得承诺 JWT」的红线已被带日期的发布记录推翻）**：2026-01 发布记录明文「MCP Server 支持 **JWT 认证**」，而专页 `consumer-certification` 仍写「认证方式目前仅支持 **API Key** 认证」；按 R4 口径优先级（带日期发布记录 > 静态专页）**倾向支持 JWT**，但专页未标废弃、两页 `migration_status` 同为 current → **对客不得仅凭任一侧文档承诺，必须先在客户实例上实测**（详见 §6.4）。RAM 多租户隔离无法靠资源级授权实现（见 §7）。

## §6 鉴权与消费者体系

> **本章组织方式**：不按文档页顺序罗列，而按「客户想达成什么 → 有哪几条路 → 每条路的设计行为与限制」组织。
> SA 对客答疑时，先用 §6.1 判断客户落在哪条路上，再用 §6.3 选型对照表定位配置入口，最后用对应小节的「设计行为限制」逐条核对客户接口契约。
> **插件形态的鉴权（key-auth / jwt-auth / hmac-auth / basic-auth / oauth）不在本章，归 W6 §9 插件体系**；本章只写 AI 网关**产品内置**的鉴权机制。交叉点见 §6.9。

---

### 6.1 先分叉：客户要做的是「统一登录」还是「授权给调用方」

AI 网关有两套并行的认证鉴权体系，走错体系是后续所有配置错误的源头。官方给出了逐项对比表（原页为 HTML `<table>`，以下逐格重排，未丢单元格）[官方｜consumer-authentication-authentication]：

| 对比项 | 全局认证鉴权 | 消费者鉴权 |
|---|---|---|
| **适用场景** | 统一登录认证等 ToC 场景。 | 授权 API 给合作伙伴等 ToB 场景。 |
| **核心差异** | 开启认证的同时也开启鉴权。 | 开启认证后，需要额外做鉴权配置。 |
| **配置入口** | **实例** > **安全管理** > **全局认证鉴权**。 | 1. **实例** > **Model API** > **消费者认证**。<br>2. **实例** > **MCP 管理** > **消费者认证**<br>3. **消费者** > **消费者详情** > **消费者鉴权**。 |
| **认证方式配置（以 JWT 认证为例）** | 1. 创建配置时填写全局的 **JWKS** 配置。<br>2. 填写 `issue`[原文如此，应为 `iss`] 和 `sub` 字段作为识别 JWT 是否合法的依据。 | 1. 创建消费者配置时填写该消费者对应的 **JWKS** 配置。<br>2. 填写消费者标识用于识别 **JWT** 是否为对应的消费者。默认为 `payload` 中的 `uid` 字段，可以自定义。 |
| **鉴权方式配置** | 创建配置时填写黑名单或白名单的**域名**和**路径（Path）**列表。<br>• **黑名单模式**：名单中的**域名**和**路径（Path）**需要进行认证，其余无需认证可直接访问。<br>• **白名单模式**：名单中的域名和**路径（Path）**不需要认证即可访问，其余需要进行认证。 | 1. 在 Model API 和 MCP 管理中开启**认证**。<br>2. 在**消费者鉴权**中授权开启了认证的 API，完成授权。 |

🔴 **消费者鉴权的「默认拒绝」设计行为**（客户被 401/403 打回来的第一号原因）：

> 当用户在消费者认证中开启认证后，认证策略会即时生效，如果此时API已发布，但是又未给API配置消费者和授权规则，则默认会拒绝所有访问请求。
> —— [官方原文｜consumer-authentication-authentication]

同一口径在三个接入类型的页面各出现一次，措辞略有差异：

> 开启消费者认证后，若没有配置授权关系，将无法访问当前API。
> —— [官方原文｜consumer-authentication（Model API）｜consumer-certification（MCP）｜consumer-certification-1（Agent API）]

即：**「开认证」和「配授权」是两个独立动作，中间态是全量拒绝**。`启用状态` 开关本身「默认关闭」[官方｜consumer-authentication｜consumer-certification-1]。

---

### 6.2 消费者（Consumer）对象全生命周期

#### 6.2.1 创建

入口：**AI 网关控制台 > 左侧导航栏「消费者」> 顶部菜单栏选择地域 > 创建消费者**。消费者是**地域级对象**（每页操作步骤都要求「在顶部菜单栏选择地域」），不是实例级对象 [官方｜creating-a-consumer｜deactivate-or-delete-a-consumer｜authorization-management｜reference-secret-key]。

创建时的**认证方式**「目前主要支持 JWT 和 API Key 两种认证方式」[官方原文｜creating-a-consumer]。两种方式的配置字段不同：

**JWT 认证方式的字段** [官方｜creating-a-consumer]

| 配置项 | 描述（原文要点） | SA 需注意的设计行为 |
|---|---|---|
| 消费者名称 | 自定义消费者的名称。 | — |
| 状态 | 消费者状态为**已启用**或**已停用**。创建完成消费者后您可以手动**启用**或**停用**。 | 状态可在创建后切换 |
| 描述 | 对消费者进行描述。 | — |
| 认证方式 | 当前消费者支持的认证方式，目前主要支持 JWT 和 API Key 两种认证方式。 | — |
| 密钥类型 | **对称密钥**：生成一份默认的 JWKS 配置（**每个消费者不同**），包含加密或者解密 Token 时使用的密钥。<br>**非对称密钥**：需要您自己填写完整的 JWKS 配置，使用私钥加密 Token。网关根据 JWKS 中配置的**公钥**进行解密。 | 🔴 对称密钥下网关持有同一把密钥，客户需自行保管 `k`；非对称密钥下网关只持公钥 |
| JWKS | JWKS 规范说明请参考 JSON Web Key (JWK)（RFC 7517）。 | — |
| JWKS Token 配置 | • **类型**：Token 参数类型，**默认 Header**。<br>• **Key**：Token 参数名称。<br>• **前缀**：Token 参数名的前缀。设置需要校验的 Token 参数信息，**默认是以 Bearer 为前缀放在 Authorization Header 中**，例如 `Authorization: Bearer token`。<br>• **是否透传**：选中 Token 参数透传，表示透传此 Token 参数到后端服务。 | 🔴 Key 与前缀必须与客户端实际发送的完全一致，见 §6.5.3 |
| JWKS Payload 内消费者标识 | 指定从 JWKS Payload 中的 Key 以及对应 Value 来识别为当前消费者。**默认提供一对标识，Key 为 `uid`，Value 为随机字符串，可自行修改**。<br>Payload 配置示例：`{ "uid": "11215ac069234abcb8944232b79ae711" }` | 🔴 这是「哪个消费者」的唯一识别依据，不是 `sub`/`iss` |

**API Key 认证方式的字段** [官方｜creating-a-consumer]

| 配置项 | 描述（原文要点） |
|---|---|
| 消费者名称 / 状态 / 描述 / 认证方式 | 同 JWT |
| 生成方式 | • **系统生成**：系统为您自动生成 API Key 凭证。<br>• **自定义**：自定义 API Key 凭证及凭证来源。 |
| 凭证 | 自定义 API Key 凭证。 |
| 凭证来源 | 凭证来源用于网关从请求的提取参数的位置和名称，支持如下：<br>• **Authorization: Bearer \<token\>**<br>• **自定义 HTTP Header**<br>• **自定义 Query 参数** |

🔴 **API Key 有 3 种凭证传递位置（含 Query），JWT 只有 Header**：

> 目前AI 网关支持Header的模式传递Token，客户可以自定义请求Header的名字和Token的前缀，请求验证时必须与消费者认证方式配对的key和前缀保持一致。
> —— [官方原文｜consumer-authentication-authentication]

[推断] 由「API Key 凭证来源含『自定义 Query 参数』」+「JWT 侧原文只写『支持 Header 的模式传递 Token』」推出：**客户若要求把 JWT 放在 URL query 里传，产品内置消费者 JWT 认证不支持**，需改走 API Key 或插件形态（插件归 W6）。

🔴 **`[官方矛盾]` 消费者的「生成方式」枚举两页不一致**（不裁决，交主控）：

- `creating-a-consumer`：**生成方式** — 「**系统生成**：系统为您自动生成API Key凭证。」「**自定义**：自定义API Key凭证及凭证来源。」（两项）
- `reference-secret-key`：「单击**创建消费者**，在创建消费者页面，配置消费者名称，认证方式选择 API Key，**生成方式选择引用密钥**，在绑定密钥选项中选择已有密钥。」（第三项「引用密钥」）

#### 6.2.2 启用 / 停用 / 删除

| 操作 | 路径 | 二次确认 | 来源 |
|---|---|---|---|
| 停用 | 消费者列表页 > 目标消费者**操作**列 > **停用** | 确认停用对话框 > 确定 | [官方｜deactivate-or-delete-a-consumer] |
| 删除 | 消费者列表页 > 目标消费者**操作**列 > **删除** | **需输入当前的消费者名称** > 删除 | [官方｜deactivate-or-delete-a-consumer] |

`[文档未说明]`：① 「停用」与「删除」在**已建立的授权关系**上的语义差异（停用是否保留授权、删除是否级联清理 Model API/MCP 侧的授权记录）；② 停用/删除的**生效时延**；③ 删除前是否校验「已被授权引用」（对比密钥删除是有此校验的，见 §6.7.2）；④ 消费者数量配额上限；⑤ 「启用」操作的具体入口（原文只在字段说明里提到「创建完成消费者后您可以手动启用或停用」，未给启用步骤）。

---

### 6.3 🔴 四类鉴权机制选型对照表

客户问「我该用哪种鉴权」时，先问两个问题：**（a）是 ToC 统一登录还是 ToB 授权调用方？（b）凭证形态是网关可自校验的（JWT/API Key），还是必须回源校验的（自建/OIDC）？**

| 维度 | 消费者 API-Key | 消费者 JWT | 全局 OIDC 认证 | 全局自建认证（外部鉴权服务） |
|---|---|---|---|---|
| **所属体系** | 消费者鉴权（ToB） | 消费者鉴权（ToB） | 全局认证鉴权（ToC） | 全局认证鉴权（ToC） |
| **典型场景** | 多租户系统 / 开放平台 / 内部系统调用 / 付费服务管理 [官方｜consumer-authentication] | 客户端已能自签发 JWT，网关持公钥本地验签，「无需访问一个中心化的鉴权服务」[官方｜configure-self-built-authentication｜configure-jwt-authentication] | 企业已有统一 IdP，要求业务服务对认证无感知 + 单点登录 [官方｜configure-oidc-authentication] | Token 为**业务方自定义格式**，「服务端收到请求后，必须额外访问中心化的鉴权服务来完成鉴权操作」[官方｜configure-self-built-authentication] |
| **配置位置（全局级 / API 级 / 工具级）** | Model API 级、Agent API 级、MCP **服务级**、MCP **工具级**（详见 §6.4） | Model API 级、Agent API 级（MCP 见 §6.4 矛盾项） | **全局级**：实例 > 安全管理 > 全局认证鉴权 | **全局级**：实例 > 安全管理 > 全局认证鉴权 |
| **凭证传递位置** | `Authorization: Bearer <token>` / 自定义 HTTP Header / **自定义 Query 参数**（3 选 1）[官方｜creating-a-consumer] | **仅 Header**（类型默认 Header，Key 与前缀可自定义，默认 `Authorization: Bearer`）[官方｜creating-a-consumer｜consumer-authentication-authentication] | **Cookie**（网关认证成功后设置 Cookie，客户端携 Cookie 发业务请求）[官方｜configure-oidc-authentication] | **仅 Header**：「设置 Token 在请求报文中的 Header 位置，常见的有 Authorization 和 Cookie」，可下拉选择或手动输入 [官方｜configure-self-built-authentication] |
| **网关是否回源校验** | 否（本地比对凭证） | 否（用 JWKS 公钥/对称密钥本地验签） | 是（向认证服务换 Token）[官方｜configure-oidc-authentication] | **是**（每个受保护请求都向鉴权服务发起一次鉴权请求）[官方｜configure-self-built-authentication] |
| **鉴权失败返回码** | 401（Key 缺失/非法/多个）、403（消费者未授权）见 §6.5.4 | 401（missing/expired/verification fails）、403（Access Denied）见 §6.5.4 | `[文档未说明]` 具体状态码；仅写「如果请求不合法，AI网关会重定向到用户登录页面」[官方｜configure-oidc-authentication] | 透传鉴权服务响应；**401 或 403 表示不合法/无权限**；亦可用响应头 `x-mse-external-authz-check-result` 的 `true`/`false` 表达 [官方｜configure-self-built-authentication] |
| **🔴 设计行为限制（必读）** | ① MCP 场景认证方式**官方口径冲突**（专页称仅 API Key、2026-01 发布记录称支持 JWT，见下方 §6.4 矛盾框，**须实测**）；② 官方自述「API Key 常用于不涉及敏感操作的简单场景，**安全性相比 JWT、AK/SK 较低**」；③ 请求含**多个** API Key 直接 401；④ Bearer 与 Key 之间**必须留一个空格** [官方｜consumer-certification｜consumer-authentication-authentication] | ① **Token 过期时间必须小于 7 天**；② 加密算法必须与 JWKS 一致；③ 消费者标识默认取 payload 的 `uid`；④ 自定义参数**所有值请都使用 String 类型**；⑤ **不支持引用密钥**（仅 API Key 支持）[官方｜consumer-authentication-authentication｜reference-secret-key] | ① **重定向 URL 的 path 必须为 `/oauth2/callback`**；② Scope 多值**用英文分号（;）分隔**；③ Cookie Domain 决定登录态作用域（`.example.com` 覆盖全部子域名）[官方｜configure-oidc-authentication] | ① 🔴 **鉴权 API 的 Path 需是前缀匹配**（详见 §6.6）；② **仅支持 HTTP 协议服务，不支持 Dubbo 等其他协议**；③ K8s Service 多端口时**默认取第一个端口**；④ **默认超时 10 秒**；⑤ 官方**建议使用宽松模式**（鉴权服务挂了放行，fail-open）；⑥ 额外请求头**默认不透传**，需逐个配置 [官方｜configure-self-built-authentication] |
| **来源 slug** | creating-a-consumer｜consumer-authentication｜consumer-certification｜consumer-certification-1｜consumer-authentication-authentication | 同左 + configure-jwt-authentication | configure-oidc-authentication | configure-self-built-authentication |

另有第 5 条路：**全局 JWT 认证**（鉴权类型 = JWT，配 Issuer + Sub + 全局 JWKS + 白/黑名单 hosts+paths），它与「消费者 JWT」是两套东西，区别见 §6.8。

**消费者鉴权的策略价值（官方 4 条，选型话术）** [官方｜consumer-authentication｜consumer-certification-1]：
- **安全性** — 「防止未授权访问：消费者鉴权通过验证请求者的身份（如API Key），可以有效防止未经授权的用户或系统访问敏感资源。」「防范恶意攻击：通过鉴权机制，可以防范爬虫攻击、接口滥用或 DDoS 攻击等恶意行为。」
- **多租户数据隔离** — 「在多租户系统中，消费者鉴权可以为不同租户分配独立的访问权限，确保每个租户只能访问自己的数据。」
- **使用量控制** — 「通过鉴权机制与限流策略的结合，可以对每个消费者账号配置基于Token消耗量的限流规则，确保其在配额范围内使用。」（🔴 与 §6.9 的 W3 消费者配额联动；原文另有「启用消费者鉴权后，可针对每个消费者账号配置基于Token消耗量的限流规则。当预设的资源用量被突破时，将自动触发限流。」）

---

### 6.4 三类接入类型的消费者认证差异（Model API / Agent API / MCP Server）

| 接入类型 | 配置入口（逐字） | 支持的认证方式 | 授权粒度 | 来源 |
|---|---|---|---|---|
| **Model API** | 实例 > 左侧导航栏 **Model API** > 单击目标 **API 名称** 进入 **API 详情** > **消费者认证** 页签 > **配置信息** 右侧 **编辑** > 弹出「**API 级消费者认证**」对话框 > 打开**启用状态**开关并选择**认证方式** > **确定**；随后单击**授权**并选择消费者 > **添加** | 「消费者授权的认证方式目前支持两种：**API Key**、**JWT**。」 | **API 级**（对话框标题即为「API 级消费者认证」） | [官方｜consumer-authentication] |
| **Agent API** | 实例 > 左侧导航栏 **Agent API** > 进入目标 API 页面 > **消费者认证** 页签 > **配置信息** 右侧 **编辑**；随后在**消费者**区域单击**授权** > 选择消费者 > **添加** | 「目前支持 **API Key** 和 **JWT** 两种方式。」 | **API 级** | [官方｜consumer-certification-1] |
| **MCP Server** | 实例 > 左侧导航栏 **MCP 管理** > 单击目标服务卡片 > **消费者认证** 页签 > **配置信息** 右侧 **编辑** > 打开**启用状态** > **确定**；<br>• 服务级授权：在 **MCP** 页签单击**授权** > **添加消费者授权**面板选择消费者 > **添加**<br>• 工具级授权：单击 **MCP 工具** > 在 **MCP 工具** 页签单击**授权** > 面板中选择**消费者和工具** > **添加** | 🔴「认证方式目前**仅支持 API Key** 认证。」 | **服务级 + 工具级**两层 | [官方｜consumer-certification] |

🔴 **MCP 的授权粒度优先级（设计行为，客户会误以为工具级更细所以更强）**：

> **MCP服务级别消费者认证权限高于MCP工具级别**。
> —— [官方原文｜consumer-certification]

MCP 消费者认证**支持的 4 类接入场景**（不在此列表内的 MCP 接入形态，文档未说明是否支持）[官方｜consumer-certification]：
1. 网关自建 HTTP 转 MCP
2. 网关自建 MCP 服务直接代理
3. Nacos 托管 HTTP 转 MCP
4. Nacos 托管代理 MCP 服务

🔴 **官方对 MCP 的 API Key 安全定性**（对客讲选型时的原话）：

> API Key是一种简单的认证方式，客户端访问时，需将凭证以指定的方式添加至请求中，网关收到请求后会验证API Key的合法性及权限。API Key常用于不涉及敏感操作的简单场景，安全性相比JWT、AK/SK较低，请注意凭证的管理与保护。
> —— [官方原文｜consumer-certification]

若没有消费者，三个接入页面都支持就地创建：「若没有消费者，您可单击**消费者**右侧的选择框，并在下拉列表中单击创建消费者进行创建。」[官方原文｜consumer-authentication｜consumer-certification｜consumer-certification-1]

`[文档未说明]`：① MCP 场景是否有 JWT 的路线图；② 「服务级权限高于工具级」在**两者规则冲突时**的具体判定（是服务级放行即放行、还是服务级拒绝即拒绝、还是取交集）；③ MCP 工具级授权能否跨服务批量配置；④ Agent API 是否有类似 MCP 的更细粒度（如按 Agent 内工具授权）。

🔴 **`[官方矛盾]` MCP 是否支持 JWT**（**裁决 C9 已修订**：原判「以专页『仅支持 API Key』为对客口径」，经 R2a 复裁发现漏比了一条**优先级更高**的证据 —— 2026-01 发布记录明文「MCP Server 支持 **JWT 认证**」（`new-feature-release-notes-ai-gateway`）。按本 KB 自己的 R4 优先级表，**带日期的发布记录（优先级 2）> 静态专页（优先级 3）**，故修订为：**倾向支持 JWT，但不得单凭文档对客承诺，必须实测**。双方原文保留如下：）

- 🔴 **优先级更高的一方**：`new-feature-release-notes-ai-gateway`（2026-01 变更表·新功能列）：「**MCP Server 支持 JWT 认证。**」（同一页另有一条更早的「MCP Server 支持 **MCP 工具级别消费者认证**」）

- `consumer-certification`（MCP 消费者认证）：「认证方式目前**仅支持 API Key** 认证。」
- `consumer-authentication-authentication`（消费者认证鉴权总览）把 MCP 列为消费者鉴权入口之一，同时以 JWT 为认证方式示例：「**配置入口** … 2. **实例**>**MCP 管理**>**消费者认证** …」「**认证方式配置（以JWT认证为例）** … 1. 创建消费者配置时填写该消费者对应的 **JWKS** 配置。2. 填写消费者标识用于识别 **JWT** 是否为对应的消费者。默认为 `payload` 中的 `uid` 字段，可以自定义。」

---

### 6.5 消费者 JWT 认证：客户自签发 Token 的硬约束

#### 6.5.1 端到端流程（8 步）
[官方｜consumer-authentication-authentication]

1. 客户端向 AI 网关发起认证请求，「请求中一般会携带终端用户的用户名和密码」
2. 网关将请求**直接转发给后端服务**
3. 后端服务读取请求中的验证信息（比如用户名、密码）进行验证，「验证通过后使用**私钥**生成标准的 Token，返回给网关」
4. 网关将携带 Token 的应答返回给客户端，「**客户端需要将这个 Token 缓存到本地**」
5. 客户端向 AI 网关发送业务请求，请求中携带 Token
6. 网关使用**用户设定的公钥**对请求中的 Token 进行验证，验证通过后将请求透传给后端服务
7. 后端服务进行业务处理后应答
8. 网关将业务应答返回给客户端

🔴 注意：与自建认证不同，**消费者 JWT 的「认证请求」（换 Token）网关只做透传，不参与验签**；网关只在第 6 步的业务请求上做本地验签。

#### 6.5.2 Token 生成的 4 条硬约束
[官方｜consumer-authentication-authentication]

| 约束 | 原文 |
|---|---|
| 加密算法必须与 JWKS 一致 | 「设置加密算法。即 `jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.HMAC_SHA256)`，**该加密算法要和JWKS保持一致**。」 |
| 🔴 支持的算法清单（**13 种**） | 「目前支持的加密算法有 **ES256、ES384、ES512、RS256、RS384、RS512、PS256、PS384、PS512、HS256、HS384、HS512 和 EdDSA**。」 |
| 🔴 过期时间 < 7 天 | 「设置过期时间。**过期时间需要小于7天**，超出过期时间后，请重新生成Token，以保证Token的安全性。」代码注释亦为「//设置过期时间，并且小于7天」，示例值为 `date.addSeconds(120*60)`（即 7200 秒） |
| 自定义参数类型 | 「添加自定义参数，**所有值请都使用 String 类型**」 |

对称 vs 非对称的差异 [官方｜consumer-authentication-authentication]：
- **对称**（示例 JWKS：`"k": "VoBG-oyqVoyCr9G56ozmq8n_rlDDyYMQOd_DO4GOkEY"`、`"kty": "oct"`、`"alg": "HS256"`）：「使用对称加密的时[原文如此，缺『候』]，需要对 `"k"` 进行解码。」即 `jws.setKey(new HmacKey(Base64.decode(JsonUtil.parseJson(privateKeyJson).get("k").toString())));`
- **非对称**：「设置加密算法，即 `jws.setAlgorithmHeaderValue(AlgorithmIdentifiers.RSA_USING_SHA256)`。该加密算法和JWKS保持一致。」「对于非对称加密算法，**要用其私钥进行加密**。」代码：`PrivateKey privateKey = new RsaJsonWebKey(JsonUtil.parseJson(privateKeyJson)).getPrivateKey(); jws.setKey(privateKey);`
- 🔴 **原文的「使用非对称密钥示例生成Token」代码块内容与「使用默认对称密钥示例生成Token」代码块完全相同**（仍是 `kty: oct` / `HS256` / `HmacKey`），非对称写法只出现在其后的「代码相关设置说明」片段里 → 客户直接复制该代码块会得到对称密钥版本 `[原文如此]`
- 「设置 `privateKeyJson`、消费者标识、过期时间，**同对称加密算法**。」

`privateKeyJson` 与消费者标识的获取途径：「即在创建消费者时使用的JWKS，可以在创建消费者时记录下自己使用的JWKS，也可以在创建消费者后，在**消费者基础配置页**获取JWKS。」「该消费者标识为创建消费者时**控制台默认生成**，也可以根据自身逻辑进行修改。您也可以在创建消费者后，在消费者基础配置页获取消费者标识。」[官方原文｜consumer-authentication-authentication]

示例代码依赖：Maven `org.bitbucket.b_c:jose4j:0.7.0` [官方｜consumer-authentication-authentication]。「下文将通过Java示例来说明Token的生成方式，**其他语言您也可使用相关的工具生成密钥对**。」另可「根据自身业务需要，可以在JWKS的PAYLOAD中添加自定义参数」。

#### 6.5.3 网关侧验签的 3 步与「Key/前缀必须配对」
> 1. 服务端收到用户请求时，先检查是否携带Token，未携带Token的请求，直接拒绝，返回**401**。
> 2. 携带Token的请求，使用用户jwks中配置的**私钥**验证Token是否合法且有效，不合法或者失效，直接拒绝，返回**401**。
> 3. 如果Token合法且有效后，再校验其代表的消费者是否授权给正在访问的API。
> —— [官方原文｜consumer-authentication-authentication]

🔴 **`[官方矛盾]` 网关验签用公钥还是私钥**（同页两处 + 另两页，不裁决）：

- `consumer-authentication-authentication`「JWT认证流程概览」第 6 步：「网关使用用户设定的**公钥**对请求中的Token进行验证，验证通过后，将请求透传给后端服务。」
- `consumer-authentication-authentication`「服务端验证Token请求」第 2 步：「携带Token的请求，使用用户jwks中配置的**私钥**验证Token是否合法且有效」
- `creating-a-consumer` 非对称密钥描述：「需要您自己填写完整的JWKS配置，使用私钥加密Token。网关根据JWKS中配置的**公钥**进行解密。」
- `configure-jwt-authentication`（全局 JWT）前提条件：「准备用于生成与验证Token的私钥与公钥。**私钥用于授权服务的签发JWT；公钥配置在AI网关中，用于对请求验签。**」

#### 6.5.4 鉴权失败返回码（客户逐字对照用）

**JWT 认证** [官方｜consumer-authentication-authentication]

| HTTP 状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | `Jwt missing` | 请求头未提供 JWT |
| 401 | `Jwt expired` | JWT 已经过期 |
| 401 | `Jwt verification fails` | JWT payload 校验失败，如 iss 不匹配 |
| 403 | `Access Denied` | 无权限访问当前 API |

对应的三个 curl 复现场景 [官方｜consumer-authentication-authentication]：
- 「**请求不携带提供JWT，返回401。**」`curl http://xxx.hello.com/test`
- 「**请求携带错误JWT，返回401。**」`curl http://xxx.hello.com/test -H 'Authorization: Bearer eyJhbGci...'`
- 「**请求携带JWT，但JWT代表的消费者无权访问API时，返回403。**」（原文注释：`# consumer1没有授权给下列路径指定api`）

**API Key 认证** [官方｜consumer-authentication-authentication]

| HTTP 状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | `Request denied by Key Auth check. Muti API key found in request.`[原文如此，`Muti`] | 请求提供多个 API Key。 |
| 401 | `Request denied by Key Auth check. No API key found in request.` | 请求未提供 API Key。 |
| 401 | `Request denied by Key Auth check. Invalid API key.` | 不允许当前 API Key 访问。 |
| 403 | `Request denied by Key Auth check. Unauthorized consumer.` | 请求的调用方无访问权限。 |

🔴 **`[官方矛盾]` 「已开认证但未授权」到底返回 401 还是 403**（同页冲突，不裁决）：

- `consumer-authentication-authentication`「API Key 认证」小节的说明：「如果Model API未开启消费者认证鉴权策略，**可直接访问**。」「如果Model API已开启消费者认证鉴权策略，**但未授权，则提示401**。」
- 同页 API Key 错误码表：「**403** ｜ `Request denied by Key Auth check. Unauthorized consumer.` ｜ 请求的调用方无访问权限。」
- 同页 JWT 错误码表：「**403** ｜ `Access Denied` ｜ 无权限访问当前API。」；JWT 场景描述亦为「请求携带JWT，但JWT代表的消费者无权访问API时，**返回403**。」

[推断] SA 对客时的稳妥说法：由上述冲突可知「未授权」的返回码在文档内不自洽，**排障时不要以状态码单点定位，应同时看出错信息字符串**——`Unauthorized consumer.` / `Access Denied` 明确指向**授权缺失**（该建授权关系），而 `No API key found` / `Invalid API key` / `Jwt missing` / `Jwt verification fails` 指向**凭证问题**（该查 Key/前缀/JWKS/uid）。此为推断，官方未裁决。

#### 6.5.5 API Key 的 3 种凭证来源与调试写法
> API Key的凭证来源主要有三类：
> 1. 默认凭证来源：`Authorization: <Bearer> Token`。
> 2. 自定义Header，填写Header参数名。
> 3. 自定义Query参数，填写query参数名。
> —— [官方原文｜consumer-authentication-authentication]

默认来源的写法要求：「在 Authorization 字段中，将 **Bearer 作为前缀**。」「**确保在 Bearer 和 API Key 之间留一个空格**。」[官方原文｜consumer-authentication-authentication]

自定义 Header / 自定义 Query 的原文描述极简：「除了标准的请求头，您还可以定义自定义HTTP请求头来传递特定信息。」「在请求URL中，您还可以通过增加自定义Query参数来传递额外的信息或配置。」[官方原文｜consumer-authentication-authentication] `[文档未说明]` 二者的参数名长度/字符集限制、是否支持同时配多个来源、多来源同时命中时的取值优先级（但「请求提供多个 API Key」会 401）。「调试和调用类似，本文以调试Model API为例。」

---

### 6.6 🔴🔴 自建认证鉴权的路径拼接规则（本章最高价值段，客户会逐字对照接口契约）

**背景（官方对 Token 形态的二分）**：
> 服务端通常根据客户端请求携带的凭证信息（即Token）来保护对外暴露的API接口的通信安全。Token形式没有严格规定，一般根据实际业务场景决定。
> • 如果Token采用的是JSON WEB Token (JWT)，那么在任何时间、任何地点都可以利用公钥来对Token的签名进行验签，**无需访问一个中心化的鉴权服务**。
> • 如果Token的形式是**业务方自定义的格式**，则服务端收到请求后，**必须额外访问中心化的鉴权服务**来完成鉴权操作，以此保护API接口的通信安全。AI 网关支持自定义鉴权。
> —— [官方原文｜configure-self-built-authentication]

**产品价值（对客话术）**：「AI 网关支持自定义鉴权服务，方便在网关入口处完成鉴权，**避免每个后端服务都接入鉴权服务**。」[官方原文｜configure-self-built-authentication]

**官方示例流程的 6 步**（业务请求为「下单操作 `/order`」，鉴权 API 为 `/validateToken`）[官方｜configure-self-built-authentication]：
1. 客户端向网关发起认证请求，例如登录操作
2. 网关将认证请求**直接转发给认证服务**
3. 认证服务读取请求中的验证信息（例如用户名、密码）进行验证，验证通过后返回凭证信息（Token）给网关，由网关响应给客户端
4. 客户端向网关发起业务请求，「例如下单操作/order，请求中携带上一步中身份认证成功后颁发的Token」
5. 网关截取原始业务请求的 Path、HTTP 方法和 Token 形成新请求报文，向自建鉴权服务发起鉴权请求（见 §6.6.1）
6. 鉴权服务收到鉴权请求后，「**既可以根据Token完成校验Token合法性的操作，又可以根据原始业务请求的Path完成鉴权操作**」

#### 6.6.1 官方明文：真实 Path 如何构造

> 网关通过截取原始业务请求的Path（包含Query Parameters）、HTTP方法（GET、POST等）和Token来形成一个新的请求报文，向接入的自建鉴权服务发起鉴权请求。您需要在网关控制台配置Token所在的HTTP Header，另外您可以根据需要开启允许携带原始请求的Body。
>
> 假设自建鉴权服务的鉴权API是/validateToken，那么鉴权请求的真实Path是鉴权API加上原始业务请求的Path后的结果，即/validateToken/order。
> —— [官方原文｜configure-self-built-authentication]

**结论**：真实 Path = `鉴权API 的 Path` **+** `原始业务请求的 Path`，是**字符串拼接**，不是替换、不是原样转发原 Path。上例中业务请求 `/order` → 鉴权请求 `/validateToken/order`。

#### 6.6.2 官方明文：鉴权 API 的 Path 匹配方式 = **前缀匹配**

控制台「**鉴权API**」配置项的原文（HTML 表格单元格，逐格重排，代码块语言标记 `HELPCODEESCAPE-java` 已修复为 `java`）：

> 设置鉴权服务提供的鉴权API的Path，**API的Path需是前缀匹配**。
>
> 例如，您的鉴权服务基于SpringMVC构建，对外开放的鉴权API为/check，那么处理/check/**的请求设置如下：
> ```java
> @RequestMapping("/check/")
> public ResponseEntity<RestResult<String>> check(){}
> ```
> —— [官方原文｜configure-self-built-authentication]

🔴 这段是**客户被阻塞的根因所在**：官方不仅规定「需是前缀匹配」，还直接给出了 SpringMVC 的正确写法 `@RequestMapping("/check/")`（**末尾带斜杠**）来承接 `/check/**`。**客户的鉴权接口若注册为精确匹配（如 `@RequestMapping("/validateToken")`），网关拼出的 `/validateToken/order` 会落到一个不存在的路由上。**

#### 6.6.3 「如果客户的认证接口是精确匹配会怎样」——后果推演

| 环节 | 官方依据 | 结果 |
|---|---|---|
| 网关发出的鉴权请求 Path | 「鉴权请求的真实Path是鉴权API加上原始业务请求的Path后的结果，即/validateToken/order」[官方原文] | `/validateToken/order`（而非客户预期的 `/validateToken`） |
| 客户鉴权服务的路由 | 客户注册的是精确匹配 `/validateToken` | `[推断]` 无匹配路由，鉴权服务返回 **404** |
| 网关如何判读 404 | 「鉴权服务返回HTTP状态码为**200**，表明Token合法且Token有权限访问该后端资源。网关继续将原始业务请求转发给受保护的后端服务」「鉴权服务返回HTTP状态码为**401或者403**，表明Token不合法或Token无权限访问该后端资源。**网关直接返回鉴权服务的响应给客户端**，此次下单操作失败。」[官方原文] | `[推断]` 404 既非 200 也非 401/403，官方**未定义该分支**；由「网关直接返回鉴权服务的响应给客户端」的设计取向推断，**鉴权失败、业务请求被拒** |
| 宽松模式能否兜住 | 「**宽松模式**：当鉴权服务不可用时（鉴权服务**建立连接失败或者返回5xx请求**），网关接受客户端请求。」[官方原文] | 🔴 `[推断]` **兜不住**。404 属 4xx，不在宽松模式覆盖的「连接失败或 5xx」范围内 → 即使客户开了官方推荐的宽松模式，精确匹配的鉴权接口仍会**全量拒绝业务请求** |
| 响应头兜底能否救 | 「鉴权服务的响应头部 `x-mse-external-authz-check-result` 的结果为 **`true`**，表明Token合法或Token有权限访问该后端资源…为 **`false`**，表明Token不合法或Token无权限访问该后端资源。网关直接返回鉴权服务的响应给客户端」[官方原文] | `[推断]` 404 响应里不会带该头，等价于非 `true` → 仍拒绝 |

> **推理链明示**：由「真实 Path = 鉴权 API + 原始 Path（官方明文）」+「鉴权 API 的 Path 需是前缀匹配（官方明文）」+「宽松模式仅覆盖『建立连接失败或者返回 5xx』（官方明文）」三条，推出「客户鉴权接口若为精确匹配 ⇒ 网关拼出的 Path 命中不了 ⇒ 鉴权服务返回 4xx ⇒ 业务请求被拒，且官方推荐的宽松模式无法兜底」。**这是 `[推断]`——官方没有直接写「精确匹配会失败」这句话**，这正是客户读不到、SA 必须主动讲的边界条件。

**对客一句话结论**：这不是 bug，是**设计行为**。有两条路：

- **路 A（官方文档明文支持，但要客户改代码）**：客户的鉴权服务提供**前缀匹配**的鉴权 API（SpringMVC 写 `@RequestMapping("/check/")`），或在网关侧把「鉴权API」配成能与拼接结果匹配的前缀。⚠️ 真实客户案（合思/易快报）中**客户明确拒绝改自己的认证契约**，且立场合理 —— 网关不应要求客户改认证接口。
- 🔴 **路 B（客户零改动，优先推荐）**：改走 **ext-auth 插件的 `endpoint_mode: forward_auth`** 模式 —— 固定 path、不拼接原始请求 Path，`Authorization` 头无条件透传，客户的精确匹配认证接口**一行都不用改**。证据是 Higress 开源侧源码（`plugins/wasm-go/extensions/ext-auth/main.go`，`[开源]`），详见 [主页 §14.1](aliyun-ai-gateway.md)。

🔴 **证据等级与前置实测要求（A5-3 修正）**：`ext-auth` / `endpoint_mode` / `forward_auth` 三个词在 **186 个 AI 网关官方快照里 0 命中**（实测 `grep -ril`），官方唯一相关记载是 `upload-plug-in` 插件优先级总表里的一行「外部认证｜插件｜认证阶段｜300」，**不含任何配置项说明**。故此解法的证据是 **Higress 开源侧**（`[开源]`）而非 AI 网关官方文档，**AI 网关控制台的「外部认证」插件是否暴露 `endpoint_mode` 配置项属 `[文档未说明]`** → 🔴 **对客给出此方案前必须在客户的 AI 网关实例上实测确认该字段存在**，否则会被客户判为给错方案。

> 🔴 **本节原缺路 B（R2a 判定 A5-2，🟠 P1）**：`-auth` 是本主题的**归属页**，SA 查细节的自然入口，而解法只写在主页 §14.1 / §15.8 与 `aliyun-products.md` 决策树里 → 从子页进入的读者只会拿到客户已明确拒绝的方案。已补齐。

#### 6.6.4 🔴 同一页有两个不同的「Path 匹配」概念，极易混淆

| 概念 | 作用对象 | 匹配方式 | 原文 |
|---|---|---|---|
| **鉴权 API 的 Path** | 网关 → 鉴权服务的**目标接口** | 🔴 **仅前缀匹配** | 「设置鉴权服务提供的鉴权API的Path，**API的Path需是前缀匹配**。」 |
| **授权规则（简单条件）里的路径（Path）** | 判定**哪些客户端请求需要走鉴权** | **精确匹配、前缀匹配、正则匹配三选一** | 「**路径匹配条件**：Path支持精确匹配、前缀匹配和正则匹配。」 |

授权规则侧的三种匹配原文 [官方原文｜configure-self-built-authentication]：
> • **精确匹配**：输入完整的Path，例如/app/v1/order。
> • **前缀匹配**：输入Path的前缀，并且末尾填一个\*。例如，匹配所有以/app开头的请求，那么需设置为/app/\*。
> • **正则匹配**：正则匹配的语法遵循Google Re2规范。详细信息，请参见Re2语法。
> **大小写敏感**：若选中此项，路径匹配值会区分大小写。

🔴 客户说「我的鉴权接口就是精确匹配的，能不能配精确匹配」时，SA 要区分清楚：他说的「精确匹配」若指**授权规则的 Path 匹配条件**，那是支持的；若指**鉴权 API 本身的 Path**，官方明文要求「需是前缀匹配」。

#### 6.6.5 请求方法与请求头如何透传

| 项目 | 官方原文 | 设计行为 |
|---|---|---|
| HTTP 方法 | 「网关通过截取原始业务请求的Path（包含Query Parameters）、**HTTP方法（GET、POST等）**和Token来形成一个新的请求报文」 | 原始方法被截取并带入鉴权请求；控制台另有「Host、Method、Path 和 Content-Length 头部会被**默认添加**」 |
| Token 位置 | 「设置Token在请求报文中的**Header位置**，常见的有Authorization和Cookie。您可以选择**下拉选择**或**手动输入**的方式设置Token位置。」 | 🔴 **仅 Header，无 Query 选项**（对比消费者 API Key 支持 Query） |
| 默认添加的请求头 | 「**Host、Method、Path和Content-Length头部会被默认添加，您无需手动添加。**」 | 4 个头自动带（注意 Method 与 Path 是**以头部形式**带给鉴权服务的） |
| 额外请求头 | 「如果需要额外携带客户端请求中的头部，那么需要在字段中按需配置头部。」（配置项：**鉴权请求中允许携带的头部**） | 🔴 **默认不透传**，需逐个显式配置（白名单式） |
| 响应头回写 | 「如果需要将鉴权响应中的头部添加到客户端请求中，那么需要在字段中按需配置头部。」（配置项：**鉴权响应中允许保留的头部**）+「**如果客户端请求中已经有该头部，那么其值将会被覆盖。**」 | 🔴 **同名头会被鉴权服务的响应头覆盖**；客户若依赖某个头做业务判断需特别注意。原文措辞为「添加到**客户端请求**中」[原文如此] |
| Body | 「勾选**鉴权请求中允许携带Body**后，鉴权请求会包含原始请求的Body。其中，**Body最大字节数**表示允许鉴权请求携带Body的最大字节数。单位：字节。」 | 🔴 **默认不携带 Body**，需勾选；有字节上限（`[文档未说明]` 默认值与最大可配值） |

#### 6.6.6 自建认证其余配置项（含默认值与限定词）

创建入口：实例 > 左侧导航栏 **安全管理** > **全局认证鉴权** > **创建鉴权** > 配置参数 > **确定** [官方｜configure-self-built-authentication]。

| 配置项 | 官方原文要点 | SA 关注点 |
|---|---|---|
| **开启** | 「是否开启AI 网关鉴权。」 | — |
| **鉴权名称** | 「自定义AI 网关鉴权的名称。」 | — |
| **鉴权类型** | 「选择**自建的鉴权服务**。」 | — |
| **鉴权服务** | 「选择鉴权的后端服务，可以在服务管理中添加。」 | 🔴「**仅支持选择HTTP协议的服务，不支持Dubbo等其他协议的服务。**」🔴「**如果具有多个端口的K8s Service，则默认取第一个端口。**如果您希望使用其他端口，需要在容器服务中创建一个额外的K8s Service且只使用目标端口。」 |
| **鉴权API** | 见 §6.6.2 | 🔴 需是前缀匹配 |
| **Token位置** | 见 §6.6.5 | 仅 Header |
| **鉴权请求中允许携带的头部** | 见 §6.6.5 | 白名单式，默认只有 4 个头 |
| **鉴权响应中允许保留的头部** | 见 §6.6.5 | 同名覆盖 |
| **鉴权请求中允许携带Body / Body最大字节数** | 见 §6.6.5 | 默认不带 |
| **超时时间** | 「设置等待鉴权服务返回结果的**最大等待时间**。**单位：秒，默认超时时间为10秒**。」 | 🔴 P0 数字：**默认 10 秒**。客户鉴权服务 P99 > 10s 会超时；`[文档未说明]` 可配范围与超时后的返回码 |
| **模式** | 「支持宽松模式和严格模式，**建议您使用宽松模式**。<br>• **宽松模式**：当鉴权服务不可用时（鉴权服务**建立连接失败或者返回5xx请求**），网关**接受**客户端请求。<br>• **严格模式**：当鉴权服务不可用时（鉴权服务**建立连接失败或者返回5xx请求**），网关**拒绝**客户端请求。」 | 🔴 安全 vs 可用性权衡：宽松模式＝鉴权服务挂了就**放行全部流量**（fail-open），严格模式＝**拒绝全部**（fail-close）。对客必须明说 fail-open 的安全含义；详情页该字段名为「**不可用模式**」 |
| **授权 · 简单条件** | 「在**授权**右侧单击**简单条件**。简单条件授权模式支持**白名单模式**和**黑名单模式**。<br>• **白名单模式**：白名单中的Hosts和Paths**无需校验即可访问**，其余Hosts和Paths**都需要校验**。<br>• **黑名单模式**：黑名单中的Hosts和Paths**需要校验**，其余Hosts和Paths**可直接访问**。」 | 单击**规则条件**可设置：**域名（Hosts）**、**路径（Path）**+路径匹配条件+大小写敏感、**请求头（Header）** |
| **请求头匹配条件（9 种）** | 「单击**请求头**配置，可以配置多个Header，**各个Header之间是与的关系**。」条件枚举：**等于 / 不等于 / 存在 / 不存在 / 包含 / 不包含 / 前缀 / 后缀 / 正则**（正则「遵循Google Re2规范」）。三字段：**HeaderKey**（Header字段名）/ **条件** / **值**（Header字段的取值） | 9 种条件官方各给了单句语义解释，如「**等于**：请求Header集合中指定Key的值与输入值相等」「**存在**：请求Header集合中存在输入Key值」 |
| **授权 · 复杂条件** | 「在**授权**右侧单击**复杂条件**。复杂条件授权支持通过YAML配置**Envoy的permission数据结构**来配置基于**与/或/非**组合条件逻辑的授权规则。**当满足配置的条件时执行鉴权逻辑；不满足条件的请求无需鉴权即可访问。**」 | 完整字段说明指向 Envoy 官方文档（v1.20.3 `config/rbac/v3/rbac.proto#envoy-v3-api-msg-config-rbac-v3-permission`）；示例见 §6.6.8 |

#### 6.6.7 鉴权结果的两种表达方式（客户接口契约必读）

**方式 A：用 HTTP 状态码**（「如果您鉴权服务的鉴权响应**可以修改HTTP状态码**，那么您可以利用HTTP状态码来反映鉴权结果」）
- 「鉴权服务返回HTTP状态码为 **200**，表明Token合法且Token有权限访问该后端资源。网关继续将原始业务请求转发给受保护的后端服务，收到业务响应后再次转发给客户端，完成下单操作。」
- 「鉴权服务返回HTTP状态码为 **401或者403**，表明Token不合法或Token无权限访问该后端资源。**网关直接返回鉴权服务的响应给客户端**，此次下单操作失败。」

**方式 B：用内置响应头**（「如果您的鉴权服务受业务本身限制要求鉴权响应的HTTP状态码**统一为200**，那么您可以利用内置的HTTP头部 `x-mse-external-authz-check-result`」）
- 「鉴权服务的响应头部 `x-mse-external-authz-check-result` 的结果为 **`true`**，表明Token合法或Token有权限访问该后端资源。网关继续将原始业务请求转发给受保护的后端服务，收到业务响应后再次转发给客户端，完成下单操作。」
- 「鉴权服务的响应头部 `x-mse-external-authz-check-result` 的结果为 **`false`**，表明Token不合法或Token无权限访问该后端资源。**网关直接返回鉴权服务的响应给客户端**，此次下单操作失败。」

🔴 头部名称 `x-mse-external-authz-check-result` 带 **mse** 前缀（AI 网关脱胎于 MSE 云原生网关的痕迹），客户对接时须**逐字**使用该名，不要写成 `x-apig-*`。

`[文档未说明]`：① 状态码非 200/401/403（如 400、404、429）时网关的处理分支；② 方式 A 与方式 B **同时存在**时的优先级（例如状态码 200 但头部为 `false`）；③ 鉴权请求超时（默认 10 秒）后网关返回给客户端的具体状态码与响应体，以及超时是否算「鉴权服务不可用」从而触发宽松模式；④ 鉴权服务返回 3xx 重定向时的行为。

#### 6.6.8 复杂条件授权的官方 YAML 示例（有决策含义，保留）

**示例一：正则匹配域名**。官方限定词：
> 本示例中，只对exampleA.com和exampleB.com两个域名下前缀匹配路径的请求执行鉴权逻辑。**注意此处regex字段配置的正则需要完全匹配，而非部分匹配。**
> 本示例中，**test.exampleA.com将无法命中条件，无需鉴权即可访问。**
> —— [官方原文｜configure-self-built-authentication]

🔴 这是**第二个高频踩坑点**：Envoy 的 `safe_regex_match.regex` 是**全匹配**语义，`(exampleA\.com|exampleB\.com)` 不会命中子域名 `test.exampleA.com`，且**未命中即不鉴权直接放行**（fail-open 方向）。

```yaml
permissions:
# and_rule 表示下面的所有 rules 条件同时成立时执行鉴权
- and_rule:
    rules:
      - url_path:
          # 前缀匹配路径
          path:
            prefix: /
      - header:
          # 正则匹配
          safe_regex_match:
            regex: "(exampleA\\.com|exampleB\\.com)"
          # 支持HTTP Pseudo-Header规范，可通过":authority"这个Header来获取域名
          name: ":authority"
```

**示例二：与/或/非多条件组合**。目标规则（原文 9 条编号规则）：
1. `exampleA.com/api` 前缀开头的请求需要鉴权，但是：1.1 `exampleA.com/api/appa/bbb` 不需要鉴权；1.2 `exampleA.com/api/appb/ccc` 不需要鉴权。
2. `exampleB.com` 下所有请求需要鉴权，但是：2.1 `exampleB.com/api/appa/bbb` 不需要鉴权；2.2 `exampleB.com/api/appb/ccc` 不需要鉴权；2.3 `exampleB.com/api/appc` 前缀开头的不需要鉴权，但是 2.3.1 `exampleB.com/api/appc/bbb/ccc` 需要鉴权、2.3.2 `exampleB.com/api/appc/ccc/ddd` 需要鉴权。

```yaml
permissions:
# or_rules 表示下面的所有 rules 条件中，有任意一个条件成立时执行鉴权
- or_rules:
    rules:
      # and_rules，表示下面所有 rules 同时满足，此 rule 条件才成立
      # 规则一
      - and_rules:
          rules:
            - url_path:
                path:
                  exact: /api/appc/bbb/ccc
            - header:
                exact_match: "exampleB.com"
                name: ":authority"
      # 规则二
      - and_rules:
          rules:
            - url_path:
                path:
                  exact: /api/appc/ccc/ddd
            - header:
                exact_match: "exampleB.com"
                name: ":authority"
      - and_rules:
          rules:
            # 规则三
            - url_path:
                path:
                  prefix: /api/
            # not_rule 表示下面的配置不满足时，此 rule 条件才成立
            # 规则四
            - not_rule:
                url_path:
                  path:
                    exact: /api/appa/bbb
            # 规则五
            - not_rule:
                url_path:
                  path:
                    exact: /api/appb/ccc
            - header:
                exact_match: "exampleA.com"
                name: ":authority"
      - and_rules:
          rules:
            # 规则六
            - url_path:
                path:
                  prefix: /
            # not_rule 表示下面的配置不满足时，此 rule 条件才成立
            # 规则七
            - not_rule:
                url_path:
                  path:
                    exact: /api/appa/bbb
            # 规则八
            - not_rule:
                url_path:
                  path:
                    exact: /api/appb/ccc
            # 规则九
            - not_rule:
                url_path:
                  path:
                    prefix: /api/appc/
            - header:
                exact_match: "exampleB.com"
                name: ":authority"
```

⚠️ 原文两个示例中 `and_rule` / `and_rules`、`not_rule` 的单复数写法不一致（示例一用 `and_rule`，示例二用 `and_rules`）[原文如此]，客户照抄时需以 Envoy 官方 permission 结构为准。

#### 6.6.9 自建认证的查看与管理

创建成功判定：「返回**全局认证鉴权**页面查看鉴权信息，如果已包含新建的网关鉴权信息，说明网关自建认证鉴权新建成功。」[官方原文｜configure-self-built-authentication]

详情页三个区域（入口：**全局认证鉴权** > 目标鉴权规则**操作**列 > **详情**，「可查看当前服务的**基本信息**和**认证配置**，也可查看并管理**授权信息**」）[官方｜configure-self-built-authentication]：
- **基本信息**：「类型为**自建的鉴权服务**」
- **认证配置**：包含 **鉴权服务**、**鉴权API**、**Token位置**、**超时时间**、**不可用模式**、**允许携带Body**、**允许的请求头部** 和 **允许的响应头部** 字段
- **授权信息**：「区域显示当前为**白名单模式**，**多行规则条件之间为"或"关系，每行规则内的多个匹配项之间为"与"关系**」，表格列含**请求域名**、**请求Path匹配项**、**大小写敏感**、**请求Header匹配项** 和 **操作**。可单击**创建授权信息**，「在对话框中输入**请求域名**和**请求Path**，并选择**匹配方式**，然后单击**确定**新增授权规则」

管理操作（均在**全局认证鉴权**页面目标鉴权规则的**操作**列）：**开启**（「使认证鉴权信息生效」）/ **关闭**（「关闭网关认证鉴权信息」）/ **编辑**（「可编辑网关认证鉴权信息」）/ **删除** [官方｜configure-self-built-authentication]。

🔴 删除的前置条件：
> **只有在认证鉴权信息关闭的状态下才可执行删除操作。**
> —— [官方原文｜configure-self-built-authentication]

`[文档未说明]`：① 同一实例可创建的鉴权规则条数上限；② 多条全局鉴权规则**同时命中同一请求**时的优先级或叠加行为；③ 鉴权服务本身是否支持配多个后端做 HA、是否有健康检查（健康检查能力归 W3）；④ 鉴权请求是否计入 AI Credits / 是否产生额外计费。

---

### 6.7 授权管理与密钥（Secret）体系

#### 6.7.1 消费者授权管理

「本文介绍如何通过对API消费者进行授权管理，确保只有经过身份验证和权限校验的请求才能访问服务资源。」[官方原文｜authorization-management]

入口：**消费者 > 单击目标消费者进入详情页 > 「消费者授权」页签**，「支持 **Model API 授权**和 **MCP 授权**两种」[官方原文｜authorization-management]。

| 授权类型 | 参数 | 描述（原文） |
|---|---|---|
| **授权 Model API** | 生效网关实例 | 选择生效的**云原生网关实例**。 |
| | 选择 API | 选择需要授权的 Model API。 |
| | 可选 API | 展示**发布至此网关**的可选 API。 |
| | 已选 API | 已勾选的 API 列表。单击目标 API 右侧的**查看**，查看详情信息。 |
| **授权 MCP** | 生效网关实例 | 选择生效的**云原生网关实例**。 |
| | 选择 MCP 服务 | 选择需要授权 MCP 服务。 |
| | 可选 MCP 服务 | 展示**发布至此网关**的可选 MCP 服务。 |
| | 已选 MCP 服务 | 已勾选的 MCP 服务。单击目标 MCP 服务右侧的**查看**，查看详情信息。 |

**解除授权**：Model API 页签 / MCP 页签 > 目标行**操作**列 > **解除授权** > 「在确认解除对话框中单击**解除**」[官方｜authorization-management]。

🔴 授权的**双向入口**：既可从「消费者详情 > 消费者授权」授权，也可从「Model API / Agent API / MCP 管理 > 消费者认证 > 授权」授权（见 §6.4 各接入类型步骤）[官方｜authorization-management｜consumer-authentication｜consumer-certification｜consumer-certification-1｜consumer-authentication-authentication]。

🔴 授权作用域限定词：「可选API：展示**发布至此网关**的可选API」——即**未发布到该实例的 API 不可被授权**，客户报「授权列表里找不到我的 API」时先查发布状态 [官方原文｜authorization-management]。

🔴 授权是**按实例生效**的：参数「生效网关实例」说明同一消费者可分别授权到不同实例，授权关系带**实例维度** [官方｜authorization-management]。

`[文档未说明]`：① **授权冲突**规则——同一消费者对同一 API 被重复授权、或从两个入口分别授权/解除授权时的最终态；② Agent API 的授权是否出现在「消费者授权」页签（该页签原文只列 Model API 与 MCP 两种，Agent API 授权路径见 `consumer-certification-1` 的「在**消费者**区域单击**授权**」）；③ 授权/解除授权的生效时延；④ 单消费者可授权的 API/MCP 数量上限；⑤ MCP **工具级**授权是否也出现在消费者详情页（该页只有「MCP 服务」维度）；⑥ 授权是否支持批量导入或 OpenAPI 化操作。

#### 6.7.2 密钥（Secret）体系

**定位与托管**：
> AI 网关提供密钥管理能力，支持密钥的创建、存储与管理。**所有密钥统一托管在密钥管理服务 KMS 中**，确保凭证信息的安全存储与使用。
> —— [官方原文｜create-secret-key]

🔴 **与 KMS 的强绑定＝连带开通/连带计费**（「账单 ≠ 全成本」）：
> **前提条件**
> • 已创建 KMS 实例，具体操作参考：购买和启用 KMS 实例。
> • 已配置 KMS 加密主密钥，具体操作参考：管理密钥。
> —— [官方原文｜create-secret-key]

即：**用 AI 网关的密钥能力，客户必须先购买并启用一个 KMS 实例 + 配置加密主密钥**。KMS 实例本身的费用不在 AI 网关账单内。`[文档未说明]` KMS 实例规格要求与价格（须另走 KMS 购买页核验；计费归 W2）。

🔴 **依赖第 3 个服务关联角色**：
> 如果服务关联角色未授权，单击**授权**，为 AI 网关授权服务关联角色 `AliyunServiceRoleForNativeApiGwInvokeKms`，参考：服务关联角色。
> —— [官方原文｜create-secret-key]

🔴 **`[官方矛盾]` 该 SLR 名称大小写两页不一致**（RAM 角色名大小写敏感，不裁决）：
- `create-secret-key`：「为 AI 网关授权服务关联角色 **`AliyunServiceRoleForNativeApiGwInvokeKms`**」（`Kms`）
- `service-association-role-provided-only-when-involved-otherwise-no-need`：「**AliyunServiceRoleForNativeApiGwInvokeKMS**：当云原生API网关需要调用密钥管理KMS服务时，可通过自动创建的云原生API网关服务关联角色 **`AliyunServiceRoleForNativeApiGwInvokeKMS`** 获取访问权限。」（`KMS`）

**创建密钥字段**（入口：`apig.console.aliyun.com` > 左侧导航栏**密钥** > 页面左上角**创建密钥** > 配置参数 > **确定**）[官方｜create-secret-key]

| 配置项 | 说明（原文） | 限定 |
|---|---|---|
| 密钥名称 | 密钥的名称。 | 🔴「**密钥名称不能重复，支持英文、数字、下划线 "_"，不超过 64 个字符。**」 |
| 凭证来源 | 指定密钥的存储位置，**默认为 KMS**。 | 原文仅给出 KMS 一种，`[文档未说明]` 是否还有其他来源 |
| 选择实例 | 选择用于存储密钥的 KMS 实例。 | — |
| 主密钥 | 选择 KMS 中用于加密的主密钥。 | — |
| 密钥内容 | 需要加密存储的凭证信息，**将被同步至 KMS 并作为凭据资源**。 | 🔴 会在客户 KMS 里生成一条 Secret 资源（对应 SLR 的 `kms:CreateSecret`，见 §7.6.3） |

**编辑与删除** [官方｜edit-and-delete-secret-key]
- 编辑：密钥列表页 > 目标密钥名称**操作**列 > **编辑**按钮 > 在**编辑密钥**面板中单击**修改密钥内容** > 输入密钥内容 > 确定。
- 删除：密钥列表页 > **删除**按钮 > 「在删除页面**输入密钥名称**」> 单击**删除**。
- 🔴 删除的前置校验：
  > **密钥被其它资源引用时无法删除，需要先前往相关引用位置删除引用。**
  > —— [官方原文｜edit-and-delete-secret-key]

**引用方式（5 类资源）**：
> 密钥可被应用于**消费者、AI 服务、Agent 服务、MCP 服务以及插件**等多种资源，用于替代原有的明文凭证信息，防止凭证泄露。
> —— [官方原文｜reference-secret-key]

🔴 **版本门槛**：
> **支持在 AI 网关 `2.1.11` 及以上版本中引用密钥。**
> —— [官方原文｜reference-secret-key]

| 引用位置 | 操作路径 | 关键限定 |
|---|---|---|
| **消费者** | 消费者 > **创建消费者** > 配置消费者名称 > 认证方式选 **API Key** > 生成方式选 **引用密钥** > 在**绑定密钥**选项中选择已有密钥 | 🔴「**消费者凭证信息中仅 API key 认证方式支持引用密钥。**」（即 JWT 消费者不支持） |
| **AI 服务** | 实例 > 左侧导航栏**服务** > **创建服务** > 服务来源选 **AI 服务** > 在**大模型配置**中生成方式选**引用密钥** > API Key 选已有密钥 | — |
| **Agent 服务** | 实例 > 左侧导航栏**服务** > **创建服务** > 服务来源选 **Agent 服务** > 生成方式选**引用密钥** > API Key 选已有密钥名称 | — |
| **MCP 服务** | 「AI 网关**直接代理**的 MCP 服务支持开启**后端认证**，在认证配置中，可将凭证直接指定为已有密钥。」实例 > 创建使用场景为 **MCP 服务直接代理** 的 MCP 服务 > MCP 服务详情页 > **基本信息**页 > 单击**配置后端服务凭证**开启认证状态 | 5 项配置：**认证方式**选 **API Key**；**凭证来源**选**自定义 HTTP Header**；**Header** 填携带凭证的 Header 名称；**生成方式**选**引用密钥**；**凭证**选已有的密钥名称 |
| **插件** | 在插件配置中使用 **`$ref{secretName}`** 语法引用，「其中 `secretName` 为密钥名称」 | 🔴「**官方插件与自定义插件均支持引用密钥。**」 |

插件引用示例（Key-Auth 插件，⚠️ 该插件本体参数归 W6 §9）[官方｜reference-secret-key]：
```yaml
credentials: 
# 引用名为secretName的密钥
- $ref{secretName}
keys:
- apikey
- x-api-key
```
「通过上述配置，可直接使用 `secretName` 密钥访问 AI 网关」[官方原文｜reference-secret-key]。

**查看引用详情**：控制台 > 左侧导航栏**密钥** > 「在**被引用**列点击密钥的引用次数，可查看当前密钥被哪些资源引用」[官方原文｜reference-secret-key]。这是删除密钥前定位引用方的唯一入口。

🔴 **控制台入口有两套域名**（SA 给客户指路时别指错）：**密钥**页与**消费者**页用 `apig.console.aliyun.com`；**实例**、**全局认证鉴权**、**AI 安全防护**、**IP 黑白名单**页用 `apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway` [官方｜create-secret-key｜reference-secret-key｜edit-and-delete-secret-key vs configure-self-built-authentication｜consumer-authentication｜content-security-protection｜set-the-gateway-ip-whitelist-and-whitelist]。

`[文档未说明]`：① **密钥轮转**——是否支持定时轮转、轮转后已下发给客户端的 API Key 是否立即失效、是否有新旧并行的宽限期；② 密钥数量配额（单账号/单地域）；③ 编辑密钥内容后的**生效时延**，以及是否影响正在使用旧值的在途请求；④ KMS 侧 Secret 资源的计费口径；⑤ 删除 KMS 实例或主密钥后 AI 网关密钥的行为；⑥ 密钥内容是否有长度/字符集限制；⑦ 是否支持从 KMS 已有 Secret 反向导入。

---

### 6.8 全局 JWT 认证 / 全局 OIDC 认证 / 门户 OIDC 单点登录：三者区别与作用域

🔴 这三者**名字都带 OIDC/JWT，但作用域完全不同**：前两个是**网关数据面流量鉴权**（实例 > 安全管理 > 全局认证鉴权），第三个是**开发者门户的登录**（开放平台控制台 > 门户管理）。客户说「我们要接 SSO」时，必须先问清是**保护 API 流量**还是**保护门户登录**。

| 维度 | 全局 JWT 认证 | 全局 OIDC 认证 | 门户 OIDC 单点登录 |
|---|---|---|---|
| **来源 slug** | configure-jwt-authentication | configure-oidc-authentication | configure-oidc-login-for-portal |
| **配置位置** | 实例 > 左侧导航栏 **安全管理** > **全局认证鉴权** > 页面左上角**创建鉴权** | 实例 > 左侧导航栏 **安全管理** > **全局认证鉴权** > 页面左上角**创建鉴权** | **开放平台控制台** > 左侧导航栏 **门户管理**（查看门户列表）> 目标门户卡片进详情页 > **安全设置** 标签页 > **第三方认证** 区域 |
| **作用域（保护什么）** | 网关上的**业务 API 流量** | 网关上的**业务 API 流量** | **开发者门户的登录**——「企业用户使用内部统一账号体系直接登录开发者门户」「企业员工可使用内部统一账号直接登录开发者门户，**无需单独注册**」 |
| **鉴权类型字段** | 「**默认支持JWT认证方式。**」 | 「选择 **OIDC** 认证方式。」 | 不适用（门户登录，非网关鉴权规则） |
| **前提条件** | 「• 了解JWT基本标准。<br>• 了解AI 网关支持的集成方式：**自主颁发Token（安全性有保障）**和**网关配置公钥对请求验签**。<br>• 准备用于生成与验证Token的私钥与公钥。**私钥用于授权服务的签发JWT；公钥配置在AI网关中，用于对请求验签。**」 | 「已创建统一的认证鉴权服务，且**支持标准的OIDC（OpenID Connect）协议**。」 | 有企业身份提供商（IdP），支持标准 OIDC **授权码流程** |
| **核心参数** | **开启**、**鉴权名称**、**鉴权类型**、**Issuer**（「设置JWT Claims的Issuer，即签发人」）、**Sub**（「设置JWT claims的sub(subject)，即主体」）、**JWKS**（「设置JWT公钥」）、**JWT Token配置**、**授权** | **开启**、**鉴权名称**、**鉴权类型**、**域名**（「鉴权规则生效的域名」）、**Issuer**（「设置认证服务的Issuer，即签发人」）、**重定向URL**、**Client ID**、**Client Secret**、**Cookie Domain**、**Cookie Secret**、**Scope**、**授权** | **提供商标识**、**显示名称**、**启用状态**、**Client ID**、**Client Secret**、**授权范围**、**Issuer**、**授权端点（authorization 端点）**、**令牌端点（token 端点）**、**用户信息端点（userinfo 端点）**、**公钥端点（jwks 端点）** |
| **凭证载体** | Header — 「**类型**：Token参数类型，**默认Header**」「**Key**：Token参数名称」「**前缀**：…**默认是以Bearer为前缀放在Authorization Header中**，例如：`Authorization: Bearer token`」「**是否透传**：选中Token参数透传，表示透传此Token参数到后端服务」 | **Cookie** — 「网关向客户端返回认证成功响应，并**设置 Cookie**」「客户端携带 **Cookie** 发起业务请求，网关验证 Token」「网关**携带 ID Token** 转发业务请求给业务服务」 | 门户会话（IdP 授权码换 Token 后由门户管理登录态） |
| **授权（哪些流量受保护）** | 「授权模式支持**白名单模式**和**黑名单模式**。<br>• 白名单模式：白名单中的 hosts+paths **不需要校验即可访问**，其余都需要校验。<br>• 黑名单模式：黑名单中的 hosts+paths **需要校验**，其余可直接访问。」单击**规则条件**设置**域名(hosts)** 与**路径(Path)** | 同左（白名单/黑名单 hosts+paths；单击**规则条件**设置**域名**和**路径（Path）**） | 不适用 |
| **🔴 回调地址硬约束** | 无 | 「输入授权成功后的重定向地址，**需要与OIDC中配置的重定向地址保持一致**。」格式为 `http(s)://yourdomain/path`（**地址中的path必须为 `/oauth2/callback`**） | 「在身份提供商侧，将**回调地址**配置为：**`{portal-address}/oidc/callback`**，其中 `{portal-address}` 是访问门户的地址。」 |
| **端点自动发现** | 不适用 | `[文档未说明]`（Issuer 只作为 JWT Claims 校验依据，未提自动发现） | 「如果已填写 **Issuer** 地址，系统会自动请求 **`{issuer}/.well-known/openid-configuration`** 端点获取 IdP 的元数据信息，并**自动填充授权端点、令牌端点和用户信息端点**。如果 IdP 不支持自动发现协议，或需要手动指定端点地址，则需手动填写上述各端点。」🔴 自动填充清单**未含 jwks 端点** |
| **Scope / 授权范围分隔符** | 不适用 | 「输入授权作用域，**多个域值用英文分号（;）分隔**。」 | 「OIDC 授权请求的范围，例如 **`openid profile email`**」（示例为**空格**分隔） |
| **其他参数说明** | JWKS 示例为 **RSA 公钥**（`"kty":"RSA"`、`"e":"AQAB"`、`"kid":"DHFbpoIUqrY8t2zpA2qXfCmr5VO5ZEr4RzHU_-envvQ"`、`"n":"xAE7eB6qugXyCAG3yhh7pkDkT65pHymX-P7KfIupjf59..."`），整体格式为 `{ "keys":[ {...} ] }` | **Cookie Domain**：「输入Cookie的域名，认证通过后会将Cookie发送到指定的域名，保持登录状态。例如：设置 `Cookie-domain=a.example.com`，则Cookie会发送到域名a.example.com；设置 `Cookie-domain=.example.com`，则Cookie会发送到example.com的**所有子域名**。」<br>**Cookie Secret**：「用于在创建Cookie时添加数字签名，确保其不会被非法篡改。」 | **提供商标识**：「身份提供商的唯一标识，用于区分不同的 IdP（例如 `aliyun`）。」<br>**显示名称**：「在开发者门户登录页面上展示的登录按钮名称（例如 `阿里云账号登录`）。」<br>**启用状态**：「控制该登录方式是否在当前门户启用。」 |
| **失败/降级行为** | `[文档未说明]`（本页无错误码表） | 「在整个认证鉴权过程中，AI 网关会验证请求是否合法。**如果请求不合法，AI网关会重定向到用户登录页面**，并能代理请求认证服务实现用户登录认证，**实现业务服务对认证服务无感知**。」 | 「OIDC 配置确定后，系统会**自动校验配置的有效性**，如有问题会给出相应提示。」 |
| **登录特性** | — | — | **授权码模式**（「采用标准的 OAuth2 Authorization Code 授权流程，安全可靠」）、**自动用户创建**（「企业用户首次登录时，系统会自动创建对应的开发者账号，无需手动注册」）、**身份映射**（「支持从 ID Token 中灵活映射用户标识、显示名称、邮箱等用户属性」） |

**门户 OIDC 身份映射默认值** [官方｜configure-oidc-login-for-portal]

| 字段 | 默认值 | 说明 |
|---|---|---|
| 用户标识 | `sub` | 用户的唯一标识字段，用于关联外部身份。 |
| 显示名称 | `name` | 用户的显示名称字段，作为开发者名称展示。 |
| 邮箱 | `email` | 用户的邮箱地址字段，用于联系和通知。 |

「身份映射用于定义从 IdP 返回的 Claims 到开放平台用户属性的映射关系，**系统会根据映射规则提取用户信息并创建开发者账号**。」[官方原文｜configure-oidc-login-for-portal]

🔴 **`[官方矛盾]` OIDC scope 分隔符**（同为 OIDC scope，两处口径不同，不裁决）：
- `configure-oidc-authentication`（全局 OIDC）：「**Scope** ｜ 输入授权作用域，**多个域值用英文分号（;）分隔**。」
- `configure-oidc-login-for-portal`（门户 OIDC）：「**授权范围** ｜ OIDC 授权请求的范围，例如 **`openid profile email`**」（示例使用空格分隔）

🔴 **两个回调路径不可混用**：全局 OIDC = **`/oauth2/callback`**；门户 OIDC = **`/oidc/callback`**。客户在 IdP 侧注册应用时若填错，认证必然失败。

**全局 OIDC 的 11 步业务流程**（对客讲「网关代理认证」时用）[官方｜configure-oidc-authentication]：
1. 客户端向网关申请认证 → 2. 网关向认证服务申请认证 → 3. 认证服务返回 **Code** 给网关 → 4. 网关返回 Code 给客户端 → 5. 客户端携带 Code 回调网关 → 6. 网关向认证服务**交换 Token** → 7. 认证服务返回 **ID Token** 给网关 → 8. 网关向客户端返回认证成功响应并**设置 Cookie** → 9. 客户端携带 Cookie 发起业务请求，网关验证 Token → 10. 网关**携带 ID Token** 转发业务请求给业务服务 → 11. 业务服务应答经网关返回客户端。

**OIDC 协议的四个角色**（官方定义）[官方｜configure-oidc-authentication]：**客户端**（「直接为用户提供服务」）、**认证服务**（「OpenID提供方，通常是指OpenID认证服务器，为第三方颁发用于认证的ID Token」）、**业务服务**（「提供业务服务」）、**用户**（「指资源持有者」）。

对比：**标准 OIDC（不经网关）**的 9 步流程中，「业务服务请求认证服务颁发Token，请求中携带**Code、Client ID、Client Secret**」「业务服务验证ID Token是否合法，然后返回业务应答」——即**每个业务服务都要自己实现认证逻辑**。官方定性：
> 在上述OIDC认证流程中，如果有不同的业务服务，例如用户服务、订单服务等，则**每个业务服务都需要实现认证鉴权逻辑**，包括校验请求是否合法、对接认证服务等。通过AI 网关的OIDC认证功能，可以实现在网关统一认证鉴权。
> —— [官方原文｜configure-oidc-authentication]

技术定性：「OIDC（OpenID Connect）是一种安全认证机制，第三方应用连接到身份认证提供商（Identify Provider）获取用户信息…**OIDC对OAuth2.0协议进行了扩展**，通过扩展的 **ID Token** 字段，提供用户基础身份信息，**ID Token使用JWT（JSON Web Token）格式进行封装**，提供自包含性、防篡改机制，可以安全地传递给第三方应用程序并容易被验证。」[官方原文｜configure-oidc-authentication]

产品价值：「通过OIDC协议与企业的认证鉴权系统整合，可以实现对内部服务的统一认证和授权管理，**避免了重复的对接工作**，同时简化了认证流程…整合OIDC协议还能实现单点登录，**您只需一次登录即可访问多个服务**。」背景：「企业内一般会自建一套统一的认证鉴权体系，AI网关支持通过OIDC协议与自建的认证鉴权体系打通，支持对接入的内部服务做统一认证鉴权，**避免每个服务都需要对接认证鉴权体系**。」[官方原文｜configure-oidc-authentication]

**门户 OIDC 验证步骤**（4 步，可用于交付验收）[官方｜configure-oidc-login-for-portal]：① 打开开发者门户登录页面，确认已显示配置的 OIDC 登录按钮（**显示名称与配置一致**）；② 点击 OIDC 登录按钮，系统应跳转至 IdP 的授权页面；③ 使用企业账号完成身份验证，系统应自动跳转回门户并完成登录；④ 首次登录时，系统会自动创建对应的开发者账号，可查看账号信息确认身份映射是否正确。

`[文档未说明]`（三者共通空白）：① 全局 JWT / 全局 OIDC 是否有类似自建认证的**超时时间**与**宽松/严格模式**；② 全局 OIDC 认证失败/IdP 不可用时的状态码与降级行为；③ Cookie 有效期与续期机制、是否支持 refresh token；④ 同一实例上**多条全局鉴权规则并存**（例如 JWT + OIDC + 自建各一条）时的生效关系与优先级；⑤ 门户 OIDC 能否**同时启用多个 IdP**（原文有「提供商标识…**用于区分不同的 IdP**」，但未说明能否并存）；⑥ 门户自动创建的开发者账号如何停用/删除、与网关「消费者」是否同一对象体系；⑦ 全局 JWT 的错误码表（消费者 JWT 有，全局 JWT 无）；⑧ 门户 OIDC 是否支持登出（logout）与单点登出。

---

### 6.9 与其他 worker 的边界（交叉注明）

| 交叉点 | 归属 | 说明 |
|---|---|---|
| **key-auth / jwt-auth / hmac-auth / basic-auth / oauth 插件** | **W6 §9 插件体系** | 本章只写产品内置鉴权。插件形态与内置机制的能力差异（如插件是否支持 Query 传 JWT、是否支持多凭证源组合、是否支持 HMAC 签名）由 W6 裁定。相关 slug：`key-auth-plug-ins`、`jwt-auth-plug-ins`、`hmac-auth-plug-ins`、`basic-auth-plug-ins`、`oauth-plugin`（均在 W6.tsv） |
| **`$ref{secretName}` 密钥引用语法** | 本章给语法与「官方插件与自定义插件均支持引用密钥」的结论 [官方｜reference-secret-key]；**各插件的具体配置示例归 W6** | 本章引用的 Key-Auth 示例仅为说明密钥引用语法 |
| **消费者配额 / Token 限流（FinOps）** | **W3 §5**（slug `consumer-quotas-management`，标题「AI网关-管理消费者配额」） | 本章只记录「启用消费者鉴权后，可针对每个消费者账号配置基于Token消耗量的限流规则。当预设的资源用量被突破时，将自动触发限流。」[官方原文｜consumer-authentication｜consumer-certification-1] 这条**联动事实** |
| **全局认证鉴权规则的通用管理** | **W3**（slug `manage-global-authentication`，标题「全局认证鉴权管理」） | 本章 §6.6.9 记录了自建认证自身的开启/关闭/编辑/删除与「只有在认证鉴权信息关闭的状态下才可执行删除操作」；通用管理逻辑归 W3，**此处可能重叠，请主控去重** |
| **MCP 接入形态（直接代理 / HTTP 转 MCP / Nacos 托管）** | **W5 §8** | 本章只记录「MCP 消费者认证支持的 4 类场景」清单 [官方｜consumer-certification] 与 MCP 后端认证凭证引用；接入形态本身的配置归 W5 |
| **开发者门户与开放平台其余能力** | **W7 §11** | 本章 §6.8 只写门户 OIDC 单点登录的鉴权配置；门户的开发者注册、API 订阅、审批流等归 W7 |
| **RAM Action 完整清单 / OpenAPI 元信息 / 错误码总表** | **W7 §13** | 本章 §7.4–7.6 只写权限策略与 SLR；`apig:` 下完整 Action 枚举、资源类型 ARN 全集归 W7 |
| **AI Credits 计费 / AI 安全护栏商品价格** | **W2 §3** | 本章 §7.1 标注「AI 安全防护是否消耗 AI Credits = `[文档未说明]`」；计费口径归 W2 |
| **服务与服务来源（鉴权服务后端如何创建）、健康检查** | **W3 §4** | 本章 §6.6.6 只记录「鉴权服务…**可以在服务管理中添加**」及 HTTP-only / K8s 多端口默认取第一个端口两条限定；服务本身的创建与健康检查归 W3 |
| **AI 日志与鉴权失败可观测** | **W7 §10** | 本章 §7.1 只记录「将相关结果保存在日志中，以提升风险发现能力，支持事后审计与应用优化」；日志字段与投递归 W7 |

---

### §6 溯源

- `consumer-authentication-authentication` — 消费者认证鉴权（14876 B）：§6.1 全局 vs 消费者对比表（逐格）与「默认拒绝」注意事项；§6.2.1 JWT 仅支持 Header 传递；§6.5 消费者 JWT 8 步流程、Token 生成 4 条硬约束、13 种加密算法清单、7 天过期上限、对称/非对称差异、验签 3 步、JWT/API Key 两张错误码表、3 个 curl 复现场景、API Key 三种凭证来源与 Bearer 空格要求；§6.5.3「公钥/私钥」与 §6.5.4「401/403」两处 `[官方矛盾]`；§6.4 MCP-JWT `[官方矛盾]` 的一方原文
- `consumer-authentication` — Model API 消费者鉴权（3379 B）：§6.3 API Key 的策略说明 4 条与适用场景 4 类；§6.4 Model API 配置入口与「API 级消费者认证」对话框、「目前支持两种：API Key、JWT」、「启用状态…默认关闭」、「开启消费者认证后，若没有配置授权关系，将无法访问当前API」；§6.9 与消费者 Token 限流的联动
- `consumer-certification` — MCP 消费者认证（3208 B）：§6.4 MCP 服务级/工具级两层配置入口与授权步骤、「**MCP服务级别消费者认证权限高于MCP工具级别**」、支持的 4 类场景、「认证方式目前**仅支持 API Key** 认证」及 API Key 安全定性原文；§6.4 MCP-JWT `[官方矛盾]` 的另一方原文
- `consumer-certification-1` — Agent API 消费者认证（2817 B）：§6.4 Agent API 配置入口、「目前支持 API Key 和 JWT 两种方式」、策略说明与适用场景；§6.7.1 Agent API 的授权入口（在**消费者**区域单击**授权**）
- `creating-a-consumer` — 创建消费者（4132 B）：§6.2.1 JWT 与 API Key 两张完整字段表（状态已启用/已停用、密钥类型对称 vs 非对称、JWKS、JWKS Token 配置四项、Payload 内消费者标识默认 `uid` + 随机字符串、生成方式、凭证来源三项）；§6.5.3 非对称密钥「网关根据JWKS中配置的公钥进行解密」（矛盾的第三方原文）；§6.2.1「生成方式」枚举 `[官方矛盾]` 的一方
- `authorization-management` — 消费者授权管理（2999 B）：§6.7.1 授权 Model API / 授权 MCP 两张参数表（含「展示**发布至此网关**的可选API」限定）、解除授权路径与二次确认、双向授权入口、按实例生效
- `deactivate-or-delete-a-consumer` — 停用或删除消费者（779 B）：§6.2.2 停用与删除的路径及二次确认（删除需输入当前的消费者名称）
- `configure-self-built-authentication` — 全局自建认证鉴权配置（17267 B）：§6.6 全节——Token 形态二分背景、6 步示例流程、**路径拼接规则原文**、**鉴权 API「需是前缀匹配」+ SpringMVC `@RequestMapping("/check/")` 示例**、鉴权服务 HTTP-only 与 K8s 多端口默认取第一个端口、Token 位置仅 Header、默认添加的 4 个头、响应头同名覆盖、Body 开关与 Body 最大字节数、**超时默认 10 秒**、宽松/严格模式（连接失败或 5xx）、200/401/403 与 `x-mse-external-authz-check-result` 双结果表达、简单条件（白/黑名单 + 三种 Path 匹配 + 大小写敏感 + 9 种 Header 条件）、复杂条件（Envoy permission + 两个完整 YAML 示例 + 「regex 需要完全匹配，而非部分匹配」+ test.exampleA.com 不命中）、详情页三区域与「多行或/行内与」关系、开启/关闭/编辑/删除与「只有在认证鉴权信息关闭的状态下才可执行删除操作」
- `configure-jwt-authentication` — 全局 JWT 认证鉴权配置（4407 B）：§6.8 全局 JWT 前提条件（自主颁发 Token vs 网关配公钥验签、私钥签发/公钥验签）、鉴权类型「默认支持JWT认证方式」、Issuer/Sub/JWKS（RSA 公钥示例）/JWT Token 配置四项/白黑名单 hosts+paths 授权；§6.5.3 公钥验签的第四方原文
- `configure-oidc-authentication` — 全局 OIDC 认证鉴权配置（6367 B）：§6.8 全局 OIDC 前提条件、OIDC 四角色定义、9 步标准流程、11 步网关流程、全部 11 个参数（含**重定向 URL 的 path 必须为 `/oauth2/callback`**、Cookie Domain 子域名语义、Cookie Secret 数字签名、**Scope 用英文分号分隔**）、白黑名单授权、「如果请求不合法，AI网关会重定向到用户登录页面…实现业务服务对认证服务无感知」；§6.8 scope 分隔符 `[官方矛盾]` 的一方
- `configure-oidc-login-for-portal` — 门户 OIDC 单点登录配置（4869 B）：§6.8 门户 OIDC 三项登录特性、配置位置（开放平台控制台 > 门户管理 > 安全设置 > 第三方认证）、10 个配置字段、`.well-known/openid-configuration` 自动发现（自动填充清单未含 jwks 端点）、身份映射三字段默认值（`sub`/`name`/`email`）、回调地址 `{portal-address}/oidc/callback`、4 步验证流程、「系统会自动校验配置的有效性」；§6.8 scope 分隔符 `[官方矛盾]` 的另一方
- `create-secret-key` — 创建密钥（1900 B）：§6.7.2「所有密钥统一托管在密钥管理服务 KMS 中」、KMS 实例 + 加密主密钥两项前提（连带开通）、SLR `AliyunServiceRoleForNativeApiGwInvokeKms` 授权入口、5 个字段（密钥名称 64 字符上限/不可重复/字符集、凭证来源默认 KMS、密钥内容「将被同步至 KMS 并作为凭据资源」）；§6.7.2 SLR 名称大小写 `[官方矛盾]` 的一方；§7.6.1 该 SLR 的触发入口
- `edit-and-delete-secret-key` — 编辑与删除密钥（802 B）：§6.7.2 编辑（修改密钥内容）与删除（输入密钥名称）路径、「**密钥被其它资源引用时无法删除，需要先前往相关引用位置删除引用**」
- `reference-secret-key` — 引用密钥（3303 B）：§6.7.2 可引用的 5 类资源、**AI 网关 `2.1.11` 及以上版本**门槛、「**消费者凭证信息中仅 API key 认证方式支持引用密钥**」、AI 服务/Agent 服务/MCP 服务（直接代理后端认证 5 项配置）/插件（`$ref{secretName}` + 「官方插件与自定义插件均支持引用密钥」）四类引用路径、「被引用」列查看引用详情；§6.2.1「生成方式选择引用密钥」`[官方矛盾]` 的另一方
- **本章查无**（客户会问但 20 页文档确实没写）：
  1. **凭证轮转**：API Key / 密钥内容 / OIDC Client Secret 是否支持定时轮转？轮转后已下发的旧凭证何时失效？是否有新旧并行的宽限期？（全 20 页无「轮转」「轮换」字样）
  2. **鉴权结果缓存**：网关是否缓存自建认证的鉴权结果或 JWT 验签结果？缓存 TTL 多久？（`consumer-authentication-authentication` 只说「客户端需要将这个Token缓存到本地」，是**客户端侧**，非网关侧）
  3. **鉴权超时后的返回码与语义**：自建认证默认超时 10 秒，超时后网关返回给客户端什么状态码/响应体？超时算「鉴权服务不可用」（进而触发宽松模式**放行**）还是「鉴权失败」？——这条直接决定 fail-open 的风险面，文档未写
  4. **消费者 JWT 的完整失败码矩阵**：除 `Jwt missing` / `Jwt expired` / `Jwt verification fails` / `Access Denied` 外，「消费者标识（uid）不匹配任何消费者」「消费者已停用」「JWKS 被更换后的旧 Token」分别返回什么
  5. **配额与条数上限**：单实例可建多少条全局鉴权规则、单规则可配多少条授权 hosts+paths、单账号/单地域可建多少消费者、单消费者可授权多少 API/MCP、可建多少密钥、单条 IP 黑白名单可填多少 IP/地址段
  6. **多条全局鉴权规则的优先级**：JWT + OIDC + 自建同时命中一个请求时，谁先执行、是否叠加、是否短路
  7. **配置生效时延**：开启/关闭鉴权、增删授权、启停/删除消费者、编辑密钥内容后多久生效（`consumer-authentication-authentication` 只说「认证策略会即时生效」，其余操作均未说明）
  8. **授权冲突**：同一消费者对同一 API 从「消费者详情」与「Model API 详情」两个入口重复授权、或一方解除授权时的最终态；MCP 服务级与工具级授权冲突的判定细节
  9. **自建认证 Body 最大字节数的默认值与上限**（原文只给字段定义，无数值）
  10. **自建认证鉴权服务的可用性与 HA**：是否支持配多个鉴权服务实例、是否有健康检查与自动摘除、鉴权服务侧的 QPS/并发上限建议
  11. **自建认证 Path 拼接的细节**：鉴权 API 配成 `/validateToken/`（尾斜杠）时拼接结果是否变成 `/validateToken//order`；原始 Path 是否做 URL 编解码；原文说截取 Path「**包含 Query Parameters**」但示例 `/validateToken/order` 未体现 query，query 究竟拼在 Path 后还是单独透传、是否原样保留
  12. **自建认证的状态码兜底分支**：鉴权服务返回 400 / 404 / 429 / 3xx 时网关的处理；方式 A（状态码）与方式 B（`x-mse-external-authz-check-result` 头）同时存在时的优先级
  13. **OIDC 的失败返回码与降级**：IdP 不可达时网关行为；Cookie 有效期与续期；是否支持 refresh token 与单点登出
  14. **门户 OIDC**：能否同时启用多个 IdP；自动创建的开发者账号如何停用/删除；门户用户与网关「消费者」是否同一对象体系
  15. **JWT 消费者的密钥类型能否切换**（对称 ↔ 非对称）以及切换后旧 Token 是否立即失效；JWKS 是否支持配多把 key 做平滑轮换（`kid` 匹配规则未写）
  16. **鉴权审计**：鉴权失败事件是否进日志、字段名是什么、能否告警（日志能力归 W7 §10）
  17. **消费者 API Key 的凭证可见性**：系统生成的 API Key 创建后能否再次明文查看、能否导出
  18. **Agent API 是否有工具级/子资源级授权粒度**（MCP 有服务级 + 工具级，Agent API 文档只写 API 级）

---

## §7 AI 安全护栏与 RAM 权限

### 7.1 AI 安全防护（内容安全护栏）

#### 7.1.1 能力定位与前置依赖

> AI安全防护具备对网关请求和响应内容进行**实时扫描**的能力，以识别潜在的风险信息，旨在检测应用程序和服务中用户请求和AI生成的有害内容，从而帮助用户提升AI应用的使用体验。通过配置不同的**防护等级**，可以灵活控制拦截的严格程度。
> —— [官方原文｜content-security-protection]

🔴 **三个必须先讲清的前置条件**：

| 前置 | 原文 | SA 含义 |
|---|---|---|
| **场景限制** | 「当前**仅支持文本生成和图片生成**场景。」 | 视频、音频、Embedding、Rerank、Agent/MCP 流量是否可防护 = `[文档未说明]` |
| **需另开通商品** | 「如果尚未开通AI安全护栏，需先**开通AI安全护栏**。」（链接指向 `common-buy.aliyun.com`，`commodityCode=lvwang_guardrail_public_cn`） | 🔴 **连带计费实锤**：AI 网关的安全防护依赖**单独购买「AI 安全护栏」商品**。`[文档未说明]` 价格与计费单位——报价时必须另走该商品购买页核验（计费归 W2） |
| **内容安全需授权 SLR** | 「开启**内容安全**防护策略前，**需授权服务关联角色**。」 | 🔴 但 SLR 页只列了 3 个角色，**没有内容安全相关的角色**，见 §7.6.5 `[官方矛盾]` |

**配置位置（作用位置＝Model API 级）**：AI 网关控制台**实例**页面 > 顶部菜单栏选择目标实例所在地域 > 单击目标**实例ID** > 左侧导航栏 **Model API** > 单击目标 **API 名称** 进入 **API 详情**页面 > 单击**策略与插件** > 打开 **AI 安全防护** 并配置相关参数 > 选择防护服务并完成相关配置 > 确认配置信息并单击**保存** [官方｜content-security-protection]。

🔴 **作用位置只有 Model API 级**，且挂在「**策略与插件**」页签下（说明其技术实现是插件形态，但产品化入口在 API 详情）。`[文档未说明]`：Agent API、MCP Server、网关全局级是否可配 AI 安全防护。

#### 7.1.2 两种防护服务的选择

> 选择防护服务，并完成相关配置。**推荐选择 AI 安全护栏**，AI安全护栏可针对不同的防护维度分别定义拦截策略，以及针对文本与图片处理的定制化检查策略，从而满足不同复杂业务场景的定制化安全需求。
> —— [官方原文｜content-security-protection]

| 防护服务 | 配置项 | 能力差异 |
|---|---|---|
| **AI 安全护栏**（官方推荐） | **接入地址**、**拦截策略**、**检查策略** | 「支持按照**消费者**配置检查策略（包括检查请求、检查响应）与拦截策略」；可按**防护维度**分别定级；支持文本与图片分别配置；支持**高级配置**（自定义 Service） |
| **内容安全** | **接入地址**、**检查请求**、**检查响应**、**防护等级** | 无消费者维度、无防护维度拆分，只有全局一档防护等级；🔴「开启内容安全防护策略前，**需授权服务关联角色**。」 |

两者的**接入地址**描述完全一致：「默认填充**最近的内容安全的VPC地址**，服务地址可参考：SDK及接入指南。」[官方原文｜content-security-protection]
两者的**防护等级**枚举完全一致（见 §7.1.4）。
「内容安全」的**检查请求/检查响应**：「开启或关闭检查请求。」「开启或关闭检查响应。检查响应用于检查大模型的回答内容是否合规，**生效时会使流式响应变为非流式**。」[官方原文｜content-security-protection]

#### 7.1.3 防护类型逐项清单（防护维度）

「**防护维度**」（AI 安全护栏 · 拦截策略）逐项，原文逐字 [官方原文｜content-security-protection]：

| # | 防护维度 | 官方定义（逐字） |
|---|---|---|
| 0 | **任意防护维度** | 对所有防护维度均生效。 |
| 1 | **内容合规检测** | 识别大模型生成的违法违规内容。 |
| 2 | **提示词攻击检测** | 防御通过恶意输入诱导模型越权或泄露。 |
| 3 | **敏感内容检测** | 拦截大模型输出中的敏感或高危信息。 |
| 4 | **模型幻觉** | 检测生成的虚假或不实内容。 |
| 5 | **恶意URL检测** | 防范模型生成包含恶意链接的响应。 |

🔴 **客户会问、但配置文档里没有的防护类型**（2026-09-21 主控修正口径，原写「对客不要承诺这两项能力」过严）：**「恶意文件检测」与「数字水印」在专页 `content-security-protection` 全页查无此词**，该页最接近的是「恶意URL检测」（防的是**链接**，不是文件）。**但产品概述页 `what-is-an-ai-gateway` 明文列出 5 个防护维度，含 `maliciousFile` 恶意文件检测 与 `waterMark` 数字水印标识**（raw 第 236/238 行）→ 属**「概述页有能力清单、操作页无落地文档」**型缺口，不是「产品没有这两项」。
**对客口径**：可以说「产品规划了这两项能力（官方产品概述页有列）」，🔴 **但不能承诺「照文档能配出来」**、不要给配置路径；客户明确要这两项时转 AI 安全护栏商品侧核验（本页指向 docId 2878231「AI安全护栏检测项配置」，未展开）或走工单。

**官方建议使用的 5 类业务场景**（选型话术）[官方｜content-security-protection]：
1. **社交平台内容审核** — 「自动识别用户发布的内容中是否包含涉黄、涉暴、违法或敏感信息，保障社区环境安全。」
2. **企业客服对话过滤** — 「在智能客服系统中实时检测用户输入或机器人回复中的不当言论，防止违规输出，并**拦截模型响应中可能包含的钓鱼链接、诈骗网站或携带恶意脚本的URL**，保障用户终端安全。」
3. **生成式AI应用防护** — 「在AI写作、绘图等AIGC应用产品中防止模型生成虚假、歧视性或有害内容。」
4. **医疗问答或法律咨询** — 「在需要高准确性的专业咨询场景中，自动识别大模型生成的**虚构事实、错误数据或无依据结论**，避免误导用户。」
5. **政务/金融信息交互** — 「在政务服务或银行等高合规要求场景中，防止敏感信息泄露或生成不实政策解读。」

#### 7.1.4 防护等级（4 档，两种防护服务通用）

| 等级 | 官方定义（逐字） |
|---|---|
| **低** | 仅拦截**高风险**的请求。 |
| **中** | 仅拦截**中高风险**的请求。 |
| **高** | 拦截**所有具有风险**的请求。 |
| **观察模式** | 检测请求/响应内容，但是**不会产生拦截行为**。 |

🔴 注意「低/中/高」的语义是**反直觉的**：等级越低＝拦截门槛越高＝**只拦最严重的**；「高」＝「拦截所有具有风险的请求」＝最严。客户说「我要最宽松的拦截」时应选**低**，而不是选「观察模式」（观察模式完全不拦，但仍检测并写日志）。

#### 7.1.5 检查策略：Service 清单（🔴 高级配置的可选值）

「检查策略：对用户发起的请求与模型的返回进行检查，并**将相关结果保存在日志中**，以提升风险发现能力，支持**事后审计**与应用优化。」「检查策略支持针对**文本**与**图片**分别配置**检查请求**与**检查响应**。」[官方原文｜content-security-protection]

| 模态 | Service 名 | 官方说明（逐字） |
|---|---|---|
| **仅文本** | `query_security_check` | 支持检测大模型**输入**内容中的内容合规风险、敏感内容风险、提示词攻击风险。 |
| **仅文本** | `response_security_check` | 支持检测大模型**生成**内容中的内容合规、敏感内容以及由提示词攻击导致的异常输出风险。 |
| **仅文本** | `response_security_check_hp` | **适用于流式生成内容检测，具备更低的检测耗时、更快的响应速度。**支持检测大模型生成内容中的内容合规、敏感内容以及由提示词攻击导致的异常输出风险。 |
| **仅图片** | `img_query_security_check` | 支持检测大模型**输入图片**中的内容合规风险。 |
| **仅图片** | `img_response_security_check` | 支持检测大模型**输出图片**中的内容合规风险。 |

⚠️ 原文中「检查请求」与「检查响应」两个小节**列出的 Service 清单完全相同**（都是上述 5 个，逐字重复），未区分哪几个只能用于请求侧、哪几个只能用于响应侧 → `[文档未说明]`。

🔴 **`[官方矛盾]` 检查响应是否必然破坏流式**（同页两处，不裁决）：
- 检查响应定义：「检查响应：检查大模型的回答内容是否合规，**生效时会使流式响应变为非流式**。」（「内容安全」小节亦重复同一句：「生效时会使流式响应变为非流式」）
- Service 定义：「`response_security_check_hp`：**适用于流式生成内容检测**，具备更低的检测耗时、更快的响应速度。」

`[文档未说明]`：选用 `response_security_check_hp` 是否能避免「流式变非流式」的客户端可感知降级。🔴 **客户若强依赖 SSE 流式输出（如对话类产品），这是必须提前压测验证的点**；且官方对「检查请求」是否影响流式**未作任何说明**（只对「检查响应」说了会降级）。

🔴 **检查策略与拦截策略均「支持配置消费者匹配规则」**，消费者匹配 4 种（逐字）[官方原文｜content-security-protection]：
> • **任意消费者**：对所有消费者生效。
> • **精确匹配**：对指定消费者生效。
> • **正则匹配**：对满足正则表达式匹配的消费者生效。
> • **前缀匹配**：对指定前缀开头的消费者生效。

⚠️ 这里的「消费者」与 §6 的网关**消费者对象**是否同一实体，`[文档未说明]`。`[推断]` 由「精确匹配：对指定消费者生效」+ §6.2「消费者名称：自定义消费者的名称」+ 场景三「消费者名称为AIBusiness」推出：**指的是 §6 的网关消费者名称**。官方未明写这条链路；若客户**未启用消费者认证**（§6.1）则该维度如何取值 = `[文档未说明]`。

🔴 **防护策略（Service）的定义在另一个控制台**：
> 防护策略（**Service**）引用**AI安全护栏**相关配置，可前往 AI安全护栏 进行定制化配置。详情请参见 AI安全护栏检测项配置。
> —— [官方原文｜content-security-protection]

即 Service **不是在 AI 网关里定义的**，而是在**云盾 AI 安全护栏控制台**（`yundun.console.aliyun.com`）里配置的，AI 网关只做引用。这解释了 §7.1.7 场景五为何要「复制两次 `query_security_check` 并分别命名」。**跨产品操作，客户容易漏。**

#### 7.1.6 🔴 生效规则与冲突裁决（客户「配了不生效」的第一号原因）

**AI 安全护栏生效规则**（5 条，逐字保留）[官方原文｜content-security-protection]：

| # | 配置组合（原文） | 结果（原文） |
|---|---|---|
| 1 | 「仅开启AI安全护栏，未开启或进行拦截策略配置及检查策略配置」 | 「**AI安全防护能力不生效**。」 |
| 2 | 「开启AI安全护栏并配置拦截策略，但未开启检查策略」 | 「**AI安全防护能力不生效**。」 |
| 3 | 「开启AI安全护栏并开启检查策略，但未配置拦截策略」 | 「AI安全防护将开启**默认配置**，为**任意消费者**的**任意防护维度**开启**低**防护等级。」 |
| 4 | 「开启AI安全护栏并配置检查策略与拦截策略」 | 「AI安全防护将根据用户配置，对用户发起的请求与模型的返回进行检查并将相关结果保存在日志中，同时对触发检查策略的内容根据拦截策略进行拦截。」 |
| 5 | 「开启检查策略但未进行高级配置时」 | 「将按照以下规则执行」——见下方默认 Service 表 |

🔴 **规则 1 与规则 2 的含义**：只开开关不配策略 = **完全不生效**；只配拦截策略不开检查策略 = **也完全不生效**。**检查策略是拦截策略的前提**。客户「开了 AI 安全防护但没拦住任何东西」的第一排查项就是这里。

🔴 **规则 4 的附加限定（极易踩坑，静默失效）**：
> 如果配置的**检查策略防护维度未包含拦截策略防护维度**，则相关拦截策略**不生效**，例如：检查策略开启**内容合规**和**敏感内容**，拦截策略开启**提示词攻击检测**，此配置中该拦截策略不生效。
> —— [官方原文｜content-security-protection]

即：**拦截策略的维度必须是检查策略维度的子集**，否则**静默失效**——不报错、不提示。

**规则 5 的默认 Service**（逐字抄，⚠️ 含原文可疑处）[官方原文｜content-security-protection]：

| 模态 | 环节 | 默认消费者 | 默认 Service |
|---|---|---|---|
| 仅文本 | 检查请求 | 任意消费者 | `query_security_check` |
| 仅文本 | 检查响应 | 任意消费者 | `response_security_check` |
| 仅图片 | 检查请求 | 任意消费者 | `img_query_security_check` |
| 仅图片 | **检查响应** | 任意消费者 | **`img_query_security_check`** [原文如此] |

🔴 **`[官方矛盾]`（原文自身可疑，不裁决）**：图片「检查响应」的默认 Service 原文写的是 `img_query_security_check`（**query**），而 §7.1.5 明确定义「`img_response_security_check`：支持检测大模型**输出图片**中的内容合规风险」。同一页两处不一致。已逐字保留原文，交主控裁决；**对客时建议在控制台实际核对默认值，不要凭文档断言**。

**拦截策略的冲突裁决顺序**（2 条，逐字）[官方原文｜content-security-protection]：

> • **优先执行匹配消费者的规则，再执行任意消费者的规则。**例如如下配置中，将优先执行前缀为AI的消费者的任意防护维度高防护等级的规则，再执行任意消费者任意防护维度低防护等级的规则。
>   例如配置两条拦截策略规则：第一条**消费者**为**任意消费者**、**防护维度**为**任意防护维度**、**防护等级**为**低**；第二条**消费者**为前缀匹配 `AI`、**防护维度**为**任意防护维度**、**防护等级**为**高**。
>
> • **如果消费者匹配命中相同时，按照规则的顺序，优先执行排在上方的规则。**例如如下配置中，对于所有前缀为AI的消费者，任意防护维度的防护等级为中，精确匹配的AI-TEST消费者模型幻觉防护等级为高，此时由于AI-TEST消费者被两条规则命中，且任意防护维度防护等级为中的规则排在上方，则优先执行该规则，**因任意防护维度包含模型幻觉，所以对于第三条配置实际不生效**。
>   该配置共三条规则：第一条**任意消费者**、**任意防护维度**、防护等级**低**；第二条消费者**正则匹配**值 `AI`、**任意防护维度**、防护等级**中**；第三条消费者**精确匹配**值 `AI-TEST`、防护维度**模型幻觉**、防护等级**高**。

🔴 **反直觉的设计行为，SA 必须主动讲**：**「更精确的规则」不会自动胜出**。判定顺序是「① 是否匹配具体消费者（**匹配 > 任意**）→ ② 规则在列表中的**物理位置**（**上 > 下**）」，**不是**「精确 > 正则 > 前缀 > 任意」的匹配特异度排序。因此上例中 `精确匹配 AI-TEST + 模型幻觉 + 高` 被排在上面的 `正则匹配 AI + 任意防护维度 + 中` 覆盖而**实际不生效**——原因原文明写：「**因任意防护维度包含模型幻觉**」。

**客户想「为重点业务单独提高防护等级」的正确配法**（由上述规则 `[推断]`）：把**精确匹配重点消费者**的规则**排在列表最上方**，且**不要用「任意防护维度」的宽规则压在上面**。官方场景三给出的做法正是如此：「添加一条拦截策略，消费者配置为精确匹配并选择 AIBusiness，防护维度与防护等级根据需求选择」，其余业务走默认拦截策略（任意消费者 + 任意防护维度 + 低）。

#### 7.1.7 场景化配置指南（官方 5 个场景，压缩为可直接引用的配方）

| # | 客户诉求（原文） | 检查策略 | 拦截策略 |
|---|---|---|---|
| 1 | 「对所有请求均进行安全防护，仅拦截高危请求。」 | 开启**仅文本**与**仅图片**的**检查请求** | 添加拦截策略：消费者=**任意消费者**、防护维度=**任意防护维度**、防护等级=**低** |
| 2 | 「仅对涉及敏感词和合规风险的请求进行拦截。」 | 开启**仅文本**与**仅图片**的**检查请求** | 添加**两条**拦截策略，消费者根据需求选择，防护维度分别选择**内容合规检测**和**敏感词检测**[原文如此，§7.1.3 维度枚举中为「敏感内容检测」]，防护等级根据需求选择 |
| 3 | 「对所有请求都进行安全防护，其中来自重点业务（消费者名称为AIBusiness）的请求进行风险拦截，其它业务的请求仅检查但不拦截。」 | 开启**仅文本**与**仅图片**的**检查请求** | 添加**一条**拦截策略：消费者配置为**精确匹配**并选择 **AIBusiness**，防护维度与防护等级根据需求选择 |
| 4 | 「对于OpenAI兼容场景的completions等请求，同时检查文本和图片的合规风险。」 | 开启**仅文本**与**仅图片**的**检查请求**与**检查响应** | 使用**默认拦截策略** |
| 5 | 「对于文本防护场景，重点业务（消费者名称为AIBusiness与AIFinancial）需检测用户请求中的内容合规、敏感内容与提示词攻击。普通业务（消费者名称为Common）仅需检测内容合规。」 | 开启**仅文本**的**检查请求**；在检查策略中打开**高级配置**，添加两条配置：① 消费者设置为**前缀匹配**并输入 `AI`，Service 选择 `query_security_check_major`；② 消费者设置为**精确匹配**并选择 **Common**，Service 选择 `query_security_check_common` | 使用**默认拦截策略** |

场景 5 的前置动作（**跨控制台操作**，客户容易漏）：
> 在 **AI安全护栏** 中**复制两次 `query_security_check`** 并分别命名为 `query_security_check_major` 与 `query_security_check_common`，其中 `query_security_check_major` 防护维度开启**内容合规**、**敏感内容**与**提示词攻击**，`query_security_check_common` 防护维度仅开启**内容合规**。
> —— [官方原文｜content-security-protection]

🔴 场景 4 的代价提示（`[推断]`）：由「开启**检查响应**」+「检查响应…**生效时会使流式响应变为非流式**」推出，**OpenAI 兼容的 completions 流式场景一旦开启检查响应，客户端将失去流式体验**。官方场景 4 未提示这一点。

`[文档未说明]`（AI 安全防护）：
1. **是否消耗 AI Credits / 如何计费** —— 全页无「AI Credits」「计费」「费用」「价格」「免费」字样；只有一句「需先开通 AI 安全护栏」指向购买页，**单价与计费单位（按调用次数？按扫描字符数？按图片张数？）完全空白**
2. **支持哪些地域** —— 无地域清单；「接入地址」只说「默认填充**最近的**内容安全的VPC地址」，未给可选地域列表，也未说明跨地域调用的延迟与合规影响
3. **支持哪些实例类型** —— 全页无「专享」「Serverless」字样，未说明两种实例形态是否都支持
4. **性能影响** —— 除 `response_security_check_hp`「具备更低的检测耗时、更快的响应速度」这一定性描述外，**无任何延迟数字**（增加多少 ms、QPS 上限、并发限制、超时时间）
5. **命中拦截后返回给客户端的状态码与响应体格式**
6. **检查结果保存在哪个日志、字段名是什么**（原文只说「将相关结果保存在日志中，以提升风险发现能力，支持事后审计与应用优化」；日志能力归 W7 §10）
7. **单次扫描的文本长度/图片大小上限**、超限如何处理（截断？跳过？报错？）
8. **「观察模式」的数据在哪里看**（是否有命中统计报表、能否导出用于调优阈值）
9. **AI 安全护栏商品侧的检测项如何与网关侧 6 个防护维度一一对应**（原文指向 docId 2878231「AI安全护栏检测项配置」，本页未展开）
10. **AI 安全防护与消费者认证 / IP 黑白名单的执行先后顺序**（先鉴权后安检还是相反？被拦截的请求是否计入 Token 消耗与计费）
11. **多语言支持**（非中英文内容的检测能力）
12. **是否支持自定义敏感词库**（本页只说去 AI 安全护栏控制台定制，网关侧未提供入口）
13. **「内容安全」这种防护服务所需的服务关联角色到底是哪个**（本页只说「需授权服务关联角色」，未给角色名；SLR 页也无对应角色）

---

### 7.2 网关 IP 黑白名单

> 网关IP黑名单和白名单是AI 网关提供的安全防护能力之一。您可以通过配置黑、白名单来拒绝或允许特定IP的访问请求。
> —— [官方原文｜set-the-gateway-ip-whitelist-and-whitelist]

配置位置：实例 > 左侧导航栏 **安全管理** > **黑/白名单** > 页面左上角**创建** > 在**创建**页面配置相关参数 > **保存** [官方｜set-the-gateway-ip-whitelist-and-whitelist]。

| 配置项 | 说明（原文要点） | SA 关注点 |
|---|---|---|
| **开启** | 是否开启黑/白名单配置。 | — |
| **名称** | 自定义 IP 访问控制的名称。 | — |
| **备注** | 对 IP 访问控制做备注。 | — |
| **类型** | 「按需选择IP访问控制的类型。<br>• **白名单（允许特定IP访问）**：在网关场景只开放受信任来源IP访问。<br>• **黑名单（禁止特定IP访问）**：在网关场景针对不友好访问执行来源IP封禁。」 | 二选一，黑白名单是**两个独立配置对象** |
| **生效层级** | 「用于指定访问控制策略在网关中作用的**网络层次**。该字段支持两个选项：**应用层（HTTP/HTTPS）**和**传输层（TCP/UDP）**。<br>• **应用层（HTTP/HTTPS）**：**默认是应用层**。网关会**允许客户端建立连接**，并根据请求中的IP信息判断是否放行或屏蔽流量。<br>• **传输层（TCP/UDP）**：网关将在**TCP连接建立阶段**就对客户端IP进行检查，**直接拒绝非法IP的连接请求**，不再继续后续的应用层处理流程。」 | 🔴 二者行为差异显著：应用层会**先建连再拒**（客户端看到 TCP 握手成功 + 应用层拒绝），传输层**连不上**（客户端看到连接被拒）。客户报「黑名单没生效，TCP 还能连上」时**先查生效层级** |
| **生效粒度** | 「IP访问控制的作用域。<br>• **网关全局**：作用于网关实例。<br>• **域名**：作用于指定域名。」<br>🔴 域名项下的附加说明：「**对于白名单，生效粒度为白名单配置交集。对于黑名单，生效粒度为黑名单配置并集。**」 | 🔴 **多级叠加语义**：白名单取**交集**、黑名单取**并集**——两者都朝「**更严格**」方向收敛。客户常误以为多层白名单会取并集而放行过宽，实际是取交集，可能**误封**合法来源 |
| **IP地址/地址段** | 「输入IP访问控制的来源IP地址或地址段。」 | `[文档未说明]` 格式规范（CIDR？起止范围？）、条数上限、是否支持 IPv6 |

🔴 **`[官方矛盾]` 是否支持「路由级」IP 黑白名单**（同页两处，不裁决）：
- 开篇：「AI 网关支持在**网关全局、域名和路由级别**配置IP黑名单和白名单，满足精细化的访问控制诉求。」（**三级**）
- 配置项表「**生效粒度**」：「IP访问控制的作用域。• **网关全局**：作用于网关实例。• **域名**：作用于指定域名。」（**仅两级，无路由级**）

`[文档未说明]`：① **客户端真实 IP 的取值来源**（是否解析 `X-Forwarded-For`、经过 CDN/WAF/SLB/NAT 时如何取、可否配置信任的代理跳数）——这是黑白名单最常被问的问题；② 命中黑/白名单后返回的**状态码与响应体**；③ 单条配置的 IP/地址段**条数上限**、单实例可建多少条黑白名单规则；④ 是否支持 **IPv6**；⑤ 黑白名单与 §7.1 AI 安全防护、§6 鉴权的**执行先后顺序**；⑥ 配置变更的**生效时延**；⑦ **网关自身的出口 IP 清单**（客户需要在上游 LLM 供应商侧加白时的地址）——本页无。

---

### 7.3 RAM 身份管理

🔴 **本页无 AI 网关特有内容**：`identity-management` 全篇是 RAM 通用最佳实践 + 指向 RAM 产品文档的链接集合（RAM用户管理、AK安全方案、RAM用户SSO管理、RAM用户组、RAM角色管理、扮演RAM角色、设置RAM角色最大会话时间、角色SSO管理、阿里云身份与权限、RAM基本概念、RAM相关使用限制、基于身份的策略、AI网关系统权限策略参考、AI网关自定义权限策略参考）。以下只保留有决策含义的条目。

**总原则**：
> 为确保您的阿里云账号及云资源使用安全，**如非必要都应避免直接使用阿里云账号（即主账号）来访问AI 网关**。**推荐的做法是使用RAM身份（即RAM用户和RAM角色）来访问AI 网关。**
> —— [官方原文｜identity-management]

| 身份类型 / 主题 | 关键事实（原文要点） |
|---|---|
| **RAM 用户** | 「RAM用户需要由阿里云账号（即主账号）或拥有管理员权限的RAM用户、RAM角色来创建，且**必须在获得授权后**才能登录控制台或使用API访问阿里云账号下的资源。」建议：「使用阿里云账号创建一个RAM用户，并为RAM用户授予管理员权限，**后续使用有管理员权限的RAM用户创建并管理其他RAM用户**。」 |
| **两种访问方式** | 「创建RAM用户时，支持设置**控制台访问**和**使用永久AccessKey访问**两种访问方式。控制台用户使用**账号和密码**访问云产品控制台，API用户使用**访问密钥AK（AccessKey）**调用API访问云资源。建议您将两个不同的使用场景**分离**，避免误操作导致服务受到影响。**对于通过控制台访问的用户，推荐为其开启MFA多因素认证。**」 |
| **AK 安全** | 🔴「**不要把RAM用户的AccessKey ID和AccessKey Secret保存在工程代码中**，否则可能导致AK泄露，威胁您账号下所有资源的安全。建议您使用**STS或环境变量**等方式获取访问授权。」 |
| **最小权限** | 「按需为RAM用户分配最小权限。最小权限是指授予用户执行某项任务所需的权限，**不授予其他无需用到的权限**。最小授权可以避免用户操作权限过大，提高数据安全性，减少因权限滥用导致的安全风险。」 |
| **SSO** | 「满足条件时对RAM用户设置SSO单点登录功能，实现直接使用企业自有的身份登录并访问阿里云资源。」（🔴 注意：这是**阿里云控制台/API 的登录 SSO**，与 §6.8 的**门户 OIDC SSO** 不是一回事） |
| **RAM 用户组** | 「当您的阿里云账号下有多个RAM用户时，可以通过创建用户组对**职责相同**的RAM用户进行分组管理和**批量授权**，高效地管理RAM用户及其权限。」三条建议：「在对RAM用户组授权时遵循最小权限策略原则」；「在RAM用户职责发生变化时将其从不再归属的用户组中移除，避免权限滥用」；「在某个用户组不再需要某些权限时移除用户组对应的权限」 |
| **RAM 角色** | 「RAM角色是一种RAM身份类型，可以被授予一组权限策略。**与RAM用户不同，RAM角色没有长期身份凭证（登录密码或访问密钥），需要被一个可信实体扮演后才能使用。**扮演成功后，可信实体将获得RAM角色的临时身份凭证，即**安全令牌（STS Token）**，使用该安全令牌就能以RAM角色身份访问被授权的资源。」 |
| **STS 有效期** | 「可信实体的RAM用户获得相关授权后即可以调用 **AssumeRole - 获取扮演角色的临时身份凭证** 接口获取RAM角色的STS Token。STS Token自颁发后将在一段时间内有效，建议您设置合理的Token有效期，避免有效期过长带来安全风险。」🔴「**STS Token有效期的最大值为角色的最大会话时间。**从安全的角度考虑，应将角色最大会话时间也设置在合理范围。」`[文档未说明]` 具体数值（原文只给「设置RAM角色最大会话时间」链接） |
| **可信实体变更风险** | 🔴「创建RAM角色后，**请勿随意变更RAM角色的可信实体**。修改RAM角色信任策略中的可信实体，可能会导致**原受信对象权限缺失，影响业务正常运行**。也可能会因**增加受信对象，带来过度授权的风险**。特殊情况必须修改时请务必**在测试账号充分测试**，确保功能正常使用后，再应用到正式生产账号。」 |

`[文档未说明]`：① AI 网关**特有**的 RAM 限制（子账号能否创建/删除实例、能否跨区域操作、消费者/密钥/MCP 服务是否有独立 RAM 资源类型可授权）；② 是否支持资源组（Resource Group）与标签（Tag）维度的授权条件；③ RAM 角色最大会话时间的默认值与取值范围。

---

### 7.4 系统权限策略

「本文描述AI网关支持的**所有**系统权限策略及其对应的权限描述，供您授权RAM身份时参考。」[官方原文｜ai-gateway-system-permission-policy-reference]

🔴 **策略分类框架**：
> 系统策略可进一步细分为**产品系统策略、服务角色策略和服务关联角色策略**三类。**部分云产品仅提供三类策略中的一类或两类，请以本文实际展示的策略类型为准。**
> —— [官方原文｜ai-gateway-system-permission-policy-reference]

→ **AI 网关实际只展示了两类**（产品系统策略 + 服务关联角色策略），**无「服务角色策略」**。

| 策略名 | 类型 | 授权范围（原文逐字） | Action 粒度 |
|---|---|---|---|
| **`AliyunAPIGFullAccess`** | 产品系统策略 | 「您可以将 AliyunAPIGFullAccess 策略授权给RAM身份。**本策略定义了管理 AI 网关的权限。**」 | 🔴 `[文档未说明]`——本页**未给出策略 JSON**，只有文字描述 |
| **`AliyunAPIGReadOnlyAccess`** | 产品系统策略 | 「您可以将 AliyunAPIGReadOnlyAccess 策略授权给RAM身份。**本策略定义了 AI 网关的只读权限。**」 | 🔴 `[文档未说明]`——同上 |
| **`AliyunServiceRolePolicyForNativeApiGw`** | 服务关联角色策略 | 「APIG使用服务关联角色 **AliyunServiceRoleForNativeApiGw** 来**访问您在其他云产品中的资源**。AliyunServiceRolePolicyForNativeApiGw 是 AliyunServiceRoleForNativeApiGw **专用**的授权策略。**本策略由APIG定义和使用，您不能修改或删除，请勿将其授权给服务关联角色之外的RAM身份。**」 | 内容即 §7.6 的 **166 条 Action**（跨 9 个云产品） |

🔴 **系统策略会静默扩权**（最小权限审计必看）：
> 在产品迭代过程中，**APIG会向系统策略中添加新的权限**，用来支持新的功能和能力。**系统策略的更新将会影响所有授予了该策略的 RAM 身份，包括 RAM 用户、RAM 用户组和 RAM 角色。**
> —— [官方原文｜ai-gateway-system-permission-policy-reference]

[推断] 由上句推出：授了 `AliyunAPIGFullAccess` 的子账号，其实际权限会随产品迭代**自动变大**，客户的安全基线扫描会出现「权限漂移」。若客户有强合规要求，应改用 §7.5 的自定义策略（自定义策略「版本更新由用户维护」，不会被阿里云静默改动）。

🔴 **官方对 OpenAPI/CLI 场景的建议**：
> 产品系统策略旨在帮助用户快速入门，仅需简单配置即可通过控制台访问该产品**及其依赖产品**。虽然系统策略包含的权限同样适用于 OpenAPI 或 CLI 等访问方式，但**为了提高安全性，我们推荐您在这些场景下使用自定义策略，按需授予人员及应用特定 API 的访问权限**。
> —— [官方原文｜ai-gateway-system-permission-policy-reference]

系统策略 vs 自定义策略的定义差异：「**系统策略统一由阿里云创建，策略的版本更新由阿里云维护，用户只能使用不能修改。自定义策略由用户管理，策略的版本更新由用户维护。**用户可以自主创建、更新和删除自定义策略。」[官方原文｜ai-gateway-system-permission-policy-reference]

授权原则：「**RAM 身份默认没有任何权限**，需要由阿里云账号管理员为其授权后才能访问阿里云账号下的资源。为保证资源的数据安全，建议您遵循**最小授权原则**为允许访问云资源的身份授予**恰好够用**的权限。」授权操作指向三篇 RAM 文档：管理RAM用户的权限、为RAM用户组授权、管理RAM角色的权限 [官方｜ai-gateway-system-permission-policy-reference]。

🔴 **`[官方矛盾]` AI 网关「管理员全权限」策略名两页不一致**（授权时找不到策略会直接卡住交付，不裁决）：
- `ai-gateway-system-permission-policy-reference`（系统权限策略参考）：产品系统策略为 **`AliyunAPIGFullAccess`**，「本策略定义了**管理 AI 网关的权限**。」（本页「产品系统策略」小节**只列了 `AliyunAPIGFullAccess` 与 `AliyunAPIGReadOnlyAccess` 两个**）
- `service-association-role-provided-only-when-involved-otherwise-no-need`（SLR 页）：「如果使用RAM用户创建或删除服务关联角色，必须联系管理员为该RAM用户授予**管理员权限（`AliyunNativeApiGwFullAccess`）**或在自定义权限策略的 `Action` 语句中为RAM用户添加以下权限」

🔴 **命名体系混用（SA 必须知道的几套前缀）**：

| 用途 | 实际取值 | 来源 |
|---|---|---|
| RAM Action 前缀 | **`apig:`**（如 `apig:*`、`apig:ListGateway`、`apig:Check*`、`apig:Get*`） | [官方｜custom-permission-policy-reference-for-ai-gateway] |
| 资源 ARN 服务段 | **`acs:apig:<region>:<account>:<资源类型>/<资源ID>`** | [官方｜custom-permission-policy-reference-for-ai-gateway] |
| 产品代号（策略描述中自称） | **APIG** | [官方｜ai-gateway-system-permission-policy-reference] |
| SLR 角色名 | **`AliyunServiceRoleForNativeApiGw`** / **`...InvokeFC`** / **`...InvokeKMS`**（另有 `...InvokeKms` 写法，见 §6.7.2 矛盾） | [官方｜service-association-role-provided-only-when-involved-otherwise-no-need｜create-secret-key] |
| SLR 专用策略名 | **`AliyunServiceRolePolicyForNativeApiGw`** | [官方｜ai-gateway-system-permission-policy-reference] |
| SLR 信任策略服务名 | **`nativeapigw.aliyuncs.com`** / **`invokefc.nativeapigw.aliyuncs.com`** | [官方｜service-association-role-provided-only-when-involved-otherwise-no-need] |
| 系统策略名 | **`AliyunAPIGFullAccess`** / **`AliyunAPIGReadOnlyAccess`** vs **`AliyunNativeApiGwFullAccess`**（见上矛盾） | [官方｜ai-gateway-system-permission-policy-reference｜service-association-role-provided-only-when-involved-otherwise-no-need] |
| RAM 侧 Action | **`ram:CreateServiceLinkedRole`** / **`ram:DeleteServiceLinkedRole`** | [官方｜service-association-role-provided-only-when-involved-otherwise-no-need] |

---

### 7.5 自定义权限策略

**通用规则** [官方｜custom-permission-policy-reference-for-ai-gateway]：
- 定位：「如果系统权限策略不能满足您的要求，您可以创建自定义权限策略实现**最小授权**。使用自定义权限策略有助于实现权限的**精细化管控**，是提升资源访问安全的有效手段。」
- 「在基于RAM的访问控制体系中，自定义权限策略是指在系统权限策略之外，您可以**自主创建、更新和删除**的权限策略。自定义权限策略的版本更新需由您来维护。」
- 「创建自定义权限策略后，**需为RAM用户、用户组或RAM角色绑定权限策略**，这些RAM身份才能获得权限策略中指定的访问权限。」
- 「已创建的权限策略支持删除，但**删除前需确保该策略未被引用**。如果该权限策略已被引用，您需要在该权限策略的**引用记录中移除授权**。」
- 「自定义权限策略**支持版本控制**，您可以按照RAM规定的版本管理机制来管理您创建的自定义权限策略版本。」

**官方 3 个授权样例（Action 粒度 + Resource ARN 形态，逐字保留）**：

| 示例 | 目标（原文） | Action | Resource | 🔴 备注 |
|---|---|---|---|---|
| **示例 1** | 「授予RAM用户对AI网关实例 `gw-cpnx*******` 的读写权限。」 | 第 1 条：`"apig:*"`<br>第 2 条：`["apig:Check*", "apig:ListGateway"]` | 第 1 条：`["acs:apig:*:*:gateway/gw-cpnx*******", "acs:apig:regionId:accountId:service/*"]`<br>第 2 条：`"*"` | 「需要替换 `regionId` 与 `accountId` 为该网关的**地域ID**与**云账号ID**。」<br>🔴 实例级读写**必须额外放开** `apig:Check*` 与 `apig:ListGateway` 到 `Resource: "*"`，否则控制台列表页打不开；且第 1 条 Resource 里还**捆绑了 `service/*`**（服务资源），并非只授权实例本身 |
| **示例 2** | 「授予RAM用户对AI网关API列表 `api-cpo22t5lhtgxxxxxx` 的读写权限。」 | `["apig:*"]` | `"acs:apig:*:*:httpapi/api-cpo22t5lhtgxxxxxx"` | API 级授权，资源类型为 **`httpapi/`**；region 与 account 段用 `*` |
| **示例 3** | 「授予RAM用户对AI网关**所有资源**的**读**权限。」 | `["apig:Check*", "apig:List*", "apig:Get*", "apig:Export*", "apig:Query*", "apig:Debug*"]` | `"acs:apig:*:*:*"` | 🔴 官方对「只读」的定义＝**6 个动词前缀**。注意其中含 **`apig:Debug*`**（调试权限被算作「读」）与 **`apig:Export*`**（导出权限被算作「读」，有**数据外泄面**）——客户做只读审计授权时应主动确认是否要剔除这两项 |

示例 1 原文 JSON（`HELPCODEESCAPE-json` 已修复为正常语言标记）：
```json
{
  "Statement": [
    {
      "Action": "apig:*",
      "Resource": [
        "acs:apig:*:*:gateway/gw-cpnx*******",
        "acs:apig:regionId:accountId:service/*"
      ],
      "Effect": "Allow"
    },
    {
      "Action": [
        "apig:Check*",
        "apig:ListGateway"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ],
  "Version": "1"
}
```

示例 3 原文 JSON：
```json
{
  "Version": "1",
  "Statement": [
    {
      "Action": [
        "apig:Check*",
        "apig:List*",
        "apig:Get*",
        "apig:Export*",
        "apig:Query*",
        "apig:Debug*"
      ],
      "Resource": "acs:apig:*:*:*",
      "Effect": "Allow"
    }
  ]
}
```

**由 3 个示例可归纳的资源类型 ARN 形态**（`[推断]`，官方未给完整清单）：
`acs:apig:<region>:<account>:gateway/<gatewayId>` ｜ `acs:apig:<region>:<account>:service/*` ｜ `acs:apig:*:*:httpapi/<httpApiId>` ｜ `acs:apig:*:*:*`

`[文档未说明]`：① **完整 Action 清单**（`apig:` 下有哪些 Action，需查 RAM/OpenAPI 元信息，归 W7 §13）；② 除 `gateway/`、`service/`、`httpapi/` 外是否还有 `consumer/`、`secret/`、`mcpserver/`、`plugin/`、`domain/` 等资源类型 ARN；③ **Condition 键**（是否支持按标签、按资源组、按 MFA、按源 IP 限定）；④ **消费者与密钥对象能否被独立授权**（对多租户运营场景很关键）；⑤ `Deny` 语句的示例；⑥ 自定义策略的数量与版本数上限（属 RAM 通用限制，本页只给链接）。

---

### 7.6 🔴 服务关联角色（SLR）：Action 分类计数与「开通即连带操作哪些云产品」

#### 7.6.1 三个 SLR 及其触发场景

「AI网关服务关联角色是为实现特定功能而设计的**预定义RAM角色**。本文将介绍AI网关服务关联角色的应用场景以及如何管理服务关联角色。」[官方原文｜service-association-role-provided-only-when-involved-otherwise-no-need]

| SLR 角色名 | 官方触发场景（逐字） | 创建方式 |
|---|---|---|
| **`AliyunServiceRoleForNativeApiGw`** | 「当AI网关需要访问**专有网络VPC、容器服务 Kubernetes 版、函数计算FC、企业级分布式应用服务EDAS、微服务引擎MSE、负载均衡SLB、负载均衡NLB、云服务器ECS、应用实时监控服务ARMS**等云服务的资源时，可通过**自动创建**的AI网关服务关联角色 AliyunServiceRoleForNativeApiGw 获取访问权限。」 | 自动创建 |
| **`AliyunServiceRoleForNativeApiGwInvokeFC`** | 「当AI网关需要**调用FC服务**时，可通过自动创建的AI网关服务关联角色 AliyunServiceRoleForNativeApiGwInvokeFC 完成网关功能。」 | 自动创建 |
| **`AliyunServiceRoleForNativeApiGwInvokeKMS`** | 「当**云原生API网关**需要调用**密钥管理KMS服务**时，可通过自动创建的云原生API网关服务关联角色 `AliyunServiceRoleForNativeApiGwInvokeKMS` 获取访问权限。」[原文如此——此条主语写成「云原生API网关」而非「AI网关」，是复制残留] | 自动创建；另 `create-secret-key` 页提供控制台**授权**按钮（「如果服务关联角色未授权，单击**授权**」） |

🔴 **SLR 的 `Resource` 全部为 `"*"`**：三个 SLR 的**每一条** Statement 都是 `"Resource": "*"`，**没有做任何资源级收窄** [官方｜service-association-role-provided-only-when-involved-otherwise-no-need]（全页 JSON 中 `Resource` 只出现两种取值：`"*"` 与 FAQ 里的 `"acs:ram:*:主账号ID:role/*"`）。这是「最小权限」讨论的核心事实：SLR 一旦存在，即对**该账号下全地域全部** SLB/NLB 实例、ECS 安全组与网卡、EIP/VSwitch、ACK 集群凭证、ARMS/Prometheus、KMS 凭据具备下述 Action 权限。

🔴 **SLR 策略不可自定义**：「本策略由APIG定义和使用，**您不能修改或删除**，请勿将其授权给服务关联角色之外的RAM身份。」[官方原文｜ai-gateway-system-permission-policy-reference] → 客户无法通过收窄 SLR 策略来做最小权限，只能选择「用/不用」与「删角色」。

#### 7.6.2 🔴 `AliyunServiceRoleForNativeApiGw` 的 Action 按产品前缀分类计数

**计数方法**：对 SLR 页「权限说明 > AliyunServiceRoleForNativeApiGw」下 9 个产品小节的 JSON `Action` 数组**逐条机械提取并脚本统计**（非人工目测），保留原文行序。

| 产品前缀 | 产品（原文小节标题） | Action 条数（原文行数） | 去重后 | 重复项 | 只读类 | 写/变更类 |
|---|---|---|---|---|---|---|
| `slb` | 负载均衡SLB | **45** | **44** | 🔴 `slb:ModifyLoadBalancerInternetSpec` **出现 2 次** | 12 | 32 |
| `nlb` | 负载均衡NLB | **30** | **30** | — | 9 | 21 |
| `ecs` | 云服务器ECS | **28** | **28** | — | 8 | 20 |
| `arms` | 应用实时监控服务ARMS | **20** | **20** | — | 11 | 9 |
| `vpc` | 专有网络VPC | **19** | **19** | — | 8 | 11 |
| `cs` | 容器服务ACK | **11** | **11** | — | 10 | 1 |
| `fc` | 函数计算FC | **6** | **6** | — | 6 | 0 |
| `mse` | 微服务引擎MSE | **4** | **4** | — | 4 | 0 |
| `edas` | 企业级分布式应用服务EDAS | **3** | **3** | — | 3 | 0 |
| **合计** | **9 个产品** | **166** | **165** | **1 项重复** | **71** | **94** |

🔴 **重复项确证**：`slb:ModifyLoadBalancerInternetSpec` 在 SLB 小节的 `Action` 数组内出现 **2 次**，是本页唯一的字面重复 Action → 原文 **166** 行、去重后 **165** 条。

🔴 **另一处原文瑕疵**：`"slb:DescribeLoadBalancerUDPListenerAttribute  "` 带**两个尾随空格** [原文如此]。

**只读 / 写变更的划分口径**（🔴 `[推断]`，官方未标注）：按 Action 动词前缀 `Describe` / `List` / `Get` / `Query` / `Search` / `Check` / `Read` 归为**只读**，其余归为**写/变更**。此归类为 SA 自行推导，用于讲「最小权限」与「会动客户什么资源」，**不可当作官方口径引用**。

**另两个 SLR 的 Action 计数**：

| SLR | 前缀 | Action 条数 | 明细 |
|---|---|---|---|
| `AliyunServiceRoleForNativeApiGwInvokeFC` | `fc` | **1** | `fc:InvokeFunction`（原文为单字符串 `"Action": "fc:InvokeFunction"`，**非数组**） |
| `AliyunServiceRoleForNativeApiGwInvokeKMS` | `kms` | **12** | `kms:ListKmsInstances`、`kms:ListKeys`、`kms:GenerateDataKey`、`kms:Decrypt`、`kms:CreateSecret`、`kms:DeleteSecret`、`kms:UpdateSecret`、`kms:DescribeSecret`、`kms:GetSecretValue`、`kms:PutSecretValue`、`kms:TagResource`、`kms:UntagResource`（只读 4：ListKmsInstances/ListKeys/DescribeSecret/GetSecretValue；写/变更 8：其余，其中 `GenerateDataKey`/`Decrypt` 属加解密运算而非资源创建） |

**三个 SLR 合计**：原文 **179** 条 Action，去重后 **178** 条（唯一重复项为 `slb:ModifyLoadBalancerInternetSpec`）。按前缀合计：`slb` 45 ｜ `nlb` 30 ｜ `ecs` 28 ｜ `arms` 20 ｜ `vpc` 19 ｜ `kms` 12 ｜ `cs` 11 ｜ `fc` 6+1 = **7** ｜ `mse` 4 ｜ `edas` 3。

🔴 **另有 2 条 `ram:` Action 不属于 SLR 权限**，而是**RAM 用户创建/删除 SLR 所需的权限**：`ram:CreateServiceLinkedRole`、`ram:DeleteServiceLinkedRole`（见 §7.6.4）。

#### 7.6.3 🔴 反推：开通 AI 网关会在客户账号里创建/操作哪些其他云产品的资源

**官方依据**（唯一的两处直接陈述）：
- 「当AI网关需要访问…等云服务的资源时，可通过自动创建的AI网关服务关联角色 AliyunServiceRoleForNativeApiGw **获取访问权限**。」[官方原文｜service-association-role-provided-only-when-involved-otherwise-no-need]
- 「APIG使用服务关联角色 AliyunServiceRoleForNativeApiGw 来**访问您在其他云产品中的资源**。」[官方原文｜ai-gateway-system-permission-policy-reference]

**以下表格为 `[推断]`**（推理链：由 §7.6.2 逐条提取的 Action **动词名** + 上述「访问您在其他云产品中的资源」推出「具备创建/变更该类资源的能力」；**官方未给「哪个网关功能触发哪个 Action」的映射表**，因此不能断言必然发生）：

| 云产品 | 会在客户账号里**创建/变更**的资源（由 Action 名反推） | 关键 Action | 是否典型计费项 |
|---|---|---|---|
| **负载均衡 SLB** | **CLB 实例**、TCP/HTTP/HTTPS/UDP 监听、VServerGroup、后端服务器挂载、标签、修改保护与删除保护开关、实例规格与公网规格 | `slb:CreateLoadBalancer`、`slb:CreateLoadBalancerForCloudService`、`slb:CreateLoadBalancerTCPListener`/`HTTPListener`/`HTTPSListener`/`UDPListener`、`slb:CreateVServerGroup`、`slb:AddBackendServers`、`slb:ModifyLoadBalancerInstanceSpec`、`slb:ModifyLoadBalancerInternetSpec`、`slb:DeleteLoadBalancer`、`slb:DeleteVServerGroup`、`slb:SetLoadBalancerModificationProtection`、`slb:SetLoadBalancerDeleteProtection` | 🔴 **是**（实例费 + 规格/带宽费） |
| **负载均衡 NLB** | **NLB 实例**、监听、服务器组、可用区与地址类型配置、安全组加入/移出、删除保护 | `nlb:CreateLoadBalancer`、`nlb:CreateListener`、`nlb:CreateServerGroup`、`nlb:AddServersToServerGroup`、`nlb:UpdateLoadBalancerZones`、`nlb:UpdateLoadBalancerAddressTypeConfig`、`nlb:LoadBalancerJoinSecurityGroup`、`nlb:LoadBalancerLeaveSecurityGroup`、`nlb:UpdateLoadBalancerProtection`、`nlb:DeleteLoadBalancer` | 🔴 **是**（实例费 + LCU） |
| **专有网络 VPC** | **EIP（弹性公网 IP）**、**VSwitch（交换机）**、EIP 与共享带宽包的绑定关系、EIP 属性、TOA 属性、标签 | `vpc:AllocateEipAddress`、`vpc:AllocateEipAddressPro`、`vpc:AssociateEipAddress`、`vpc:UnassociateEipAddress`、`vpc:ReleaseEipAddress`、`vpc:ModifyEipAddressAttribute`、`vpc:CreateVSwitch`、`vpc:AddCommonBandwidthPackageIp`、`vpc:RemoveCommonBandwidthPackageIp`、`vpc:ModifyBypassToaAttribute`、`vpc:TagResources` | 🔴 **是**（EIP 保有费 + 流量/带宽费；共享带宽包费） |
| **云服务器 ECS** | **安全组**及其 ingress/egress 规则、**弹性网卡 ENI** 与 ENI 权限、私网 IP / IPv6 地址分配、网卡挂载与卸载、标签 | `ecs:CreateSecurityGroup`、`ecs:AuthorizeSecurityGroup`、`ecs:AuthorizeSecurityGroupEgress`、`ecs:RevokeSecurityGroup`、`ecs:RevokeSecurityGroupEgress`、`ecs:DeleteSecurityGroup`、`ecs:JoinSecurityGroup`、`ecs:LeaveSecurityGroup`、`ecs:CreateNetworkInterface`、`ecs:DeleteNetworkInterface`、`ecs:AttachNetworkInterface`、`ecs:DetachNetworkInterface`、`ecs:AssignPrivateIpAddresses`、`ecs:AssignIpv6Addresses` | 安全组 / ENI 本身**不单独计费**，但 ENI 会占用 VSwitch IP 与实例网卡配额 |
| **应用实时监控服务 ARMS** | 🔴 **开通 ARMS 服务本身**、**Prometheus 实例**、VCluster、告警规则、通知策略、分派规则、自定义事件上报 | `arms:OpenArmsService`、`arms:OpenArmsServiceSecondVersion`、`arms:AddPrometheusInstance`、`arms:OpenVCluster`、`arms:CreatePrometheusAlertRule`、`arms:CreateDefaultCloudProductPrometheusAlertRule`、`arms:CreateOrUpdateNotificationPolicy`、`arms:CreateDispatchRule`、`arms:ReportCustomIncidents` | 🔴 **是**（ARMS / Prometheus 计费）；`OpenArmsService` 属**开通服务类** Action |
| **容器服务 ACK（`cs`）** | 🔴 **集群内部服务 Kubeconfig 凭证的获取与吊销**（唯一写 Action 是 `cs:RevokeClusterInnerServiceKubeconfig`）；其余 10 条为集群/节点池/kubeconfig 的读取 | `cs:DescribeClusterInnerServiceKubeconfig`、`cs:GetUserConfig`、`cs:DescribeClusterUserKubeconfig`、`cs:DescribeClusterDetail`、`cs:DescribeClusterNodePools`、`cs:RevokeClusterInnerServiceKubeconfig` | 不直接计费，但 🔴 **属高敏感凭证面**：AI 网关会读取客户 ACK 集群的 kubeconfig |
| **函数计算 FC** | SLR-A 侧仅 6 条 `List*`（只读服务发现）；**实际调用**由 `AliyunServiceRoleForNativeApiGwInvokeFC` 的 `fc:InvokeFunction` 承担（单独一个 SLR，权限隔离） | `fc:ListServices`、`fc:ListFunctions`、`fc:ListTriggers`、`fc:ListAliases`、`fc:ListServiceVersions`、`fc:ListFunctionVersions`；`fc:InvokeFunction` | 🔴 **是**（FC 调用次数 + 资源用量） |
| **微服务引擎 MSE** | 仅 4 条只读：`mse:ListAnsServices`、`mse:ListEngineNamespaces`、`mse:ListClusters`、`mse:QueryConfig` | — | 不产生新资源；🔴 但 `mse:QueryConfig` 会**读取客户 Nacos/MSE 配置内容** |
| **EDAS** | 仅 3 条只读：`edas:ReadNamespace`、`edas:ReadService`、`edas:ListUserDefineRegion` | — | 不产生新资源 |
| **密钥管理 KMS**（`AliyunServiceRoleForNativeApiGwInvokeKMS`） | 🔴 **在客户 KMS 里创建 / 更新 / 删除凭据（Secret）资源**，并执行加解密与数据密钥生成、打标签 | `kms:CreateSecret`、`kms:PutSecretValue`、`kms:UpdateSecret`、`kms:DeleteSecret`、`kms:GenerateDataKey`、`kms:Decrypt`、`kms:TagResource`、`kms:UntagResource` | 🔴 **是**（KMS 实例费 + 凭据/API 调用费）。与 §6.7.2「密钥内容…**将被同步至 KMS 并作为凭据资源**」互为印证 |

**「账单 ≠ 全成本」的对客结论**（`[推断]`，基于上表 + §7.1.1）：
> 由「SLR-A 含 `slb:CreateLoadBalancer` / `nlb:CreateLoadBalancer` / `vpc:AllocateEipAddress` / `arms:OpenArmsService` + `arms:AddPrometheusInstance`，InvokeKMS 含 `kms:CreateSecret`」+「所有 Statement 的 `Resource` 均为 `"*"`」+「AI 网关通过 SLR 访问**您在其他云产品中的资源**」推出：**客户账单上的 AI 网关实例费之外，至少可能产生 ① SLB/NLB、② EIP 与共享带宽、③ ARMS/Prometheus、④ FC 调用、⑤ KMS 实例与凭据 共 5 类外部账单**；此外若使用 AI 安全防护，还有 §7.1.1 的**「AI 安全护栏」商品费**（`commodityCode=lvwang_guardrail_public_cn`），合计 **6 类连带项**。**每项单价在 AI 网关文档中均 `[文档未说明]`，SA 报价时必须另走各产品购买页核验。**

**「最小权限」的对客结论**（官方事实 + `[推断]`）：
> 官方事实：三个 SLR 的 `Resource` 全为 `"*"`；SLR-A 的 165 条去重 Action 中 **94 条为写/变更类**（`[推断]` 占比约 57%，按 §7.6.2 动词前缀口径），其中含 `slb:DeleteLoadBalancer`、`slb:DeleteVServerGroup`、`slb:DeleteLoadBalancerListener`、`nlb:DeleteLoadBalancer`、`nlb:DeleteListener`、`nlb:DeleteServerGroup`、`ecs:DeleteSecurityGroup`、`ecs:DeleteNetworkInterface`、`ecs:DeleteNetworkInterfacePermission`、`vpc:ReleaseEipAddress`、`kms:DeleteSecret` 等**删除类** Action；官方亦明示「本策略由APIG定义和使用，**您不能修改或删除**」。
> 由此推出：SLR 是**不可收窄**的账号级宽权限面。客户若有强合规诉求（等保 / 金融内审），可行的缓解手段只有官方给出的两条：① **不用时删除 SLR**（「当长时间不使用AI网关时，可前往RAM控制台手动删除服务关联角色」，但「删除…**依赖该角色的功能将无法正常使用，请谨慎删除**」）；② 对**人员/程序身份**改用 §7.5 自定义策略收窄，而非依赖系统策略（且系统策略会被阿里云静默扩权，见 §7.4）。

#### 7.6.4 RAM 用户操作 SLR 所需权限

> 如果使用RAM用户创建或删除服务关联角色，必须联系管理员为该RAM用户授予**管理员权限（AliyunNativeApiGwFullAccess）**或在自定义权限策略的 `Action` 语句中为RAM用户添加以下权限：
> • 创建服务关联角色：**`ram:CreateServiceLinkedRole`**
> • 删除服务关联角色：**`ram:DeleteServiceLinkedRole`**
> —— [官方原文｜service-association-role-provided-only-when-involved-otherwise-no-need]

官方给出的**最小化 Condition 策略**（比直接给 `ram:CreateServiceLinkedRole` 到 `*` 更安全，推荐对客用这个）：

| 目标 SLR | `ram:ServiceName` 条件值 | Resource | Action |
|---|---|---|---|
| `AliyunServiceRoleForNativeApiGw` | **`nativeapigw.aliyuncs.com`** | `acs:ram:*:主账号ID:role/*` | `ram:CreateServiceLinkedRole` |
| `AliyunServiceRoleForNativeApiGwInvokeFC` | **`invokefc.nativeapigw.aliyuncs.com`** | `acs:ram:*:主账号ID:role/*` | `ram:CreateServiceLinkedRole` |
| `AliyunServiceRoleForNativeApiGwInvokeKMS` | 🔴 **`[文档未说明]`** —— 本页 FAQ 只给了前两个的策略示例 | — | — |

策略原文（以 SLR-A 为例，`HELPCODEESCAPE-json` 已修复）：
```json
{
    "Statement": [
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "acs:ram:*:主账号ID:role/*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": [
                        "nativeapigw.aliyuncs.com"
                    ]
                }
            }
        }
    ],
    "Version": "1"
}
```
官方注：「请将**主账号ID**替换为您实际的阿里云账号ID。」InvokeFC 版本仅 `ram:ServiceName` 改为 `invokefc.nativeapigw.aliyuncs.com`，其余完全相同。

FAQ 的问题措辞本身也是有用的排障线索：「**为什么我的RAM用户无法自动创建AI网关服务关联角色（AliyunServiceRoleForNativeApiGw）？**」「您需要拥有指定的权限，才能自动创建或删除 AliyunServiceRoleForNativeApiGw。」→ 即 **SLR 自动创建失败是权限问题，不是产品故障**，SA 遇到「实例创建卡住/密钥页报未授权」先查这条。

#### 7.6.5 SLR 的查看与删除

**查看**：「当服务关联角色创建成功后，您可以在 **RAM控制台的角色页面**，通过搜索服务关联角色名称（**AliyunServiceRoleForNativeApiGw、AliyunServiceRoleForNativeApiGwInvokeFC**）查看该服务关联角色的以下信息」[官方原文｜service-association-role-provided-only-when-involved-otherwise-no-need]：
- **基本信息**：「在…角色详情页面的**基本信息**区域，查看角色基本信息，包括**角色名称、创建时间、角色ARN和备注**等。」
- **权限策略**：「在…角色详情页面的**权限管理**页签，单击权限策略名称，查看权限策略内容以及**该角色可授权访问哪些云资源**。」
- **信任策略**：「在…角色详情页的**信任策略管理**页签，查看信任策略内容。信任策略是描述RAM角色可信实体的策略，可信实体是指可以扮演RAM角色的实体用户身份。**服务关联角色的可信实体为云服务**，您可以通过信任策略中的 `Service` 字段查看。」

🔴 **`[官方矛盾]` SLR 数量口径不一致**（同页，不裁决）：
- 「服务关联角色的应用场景」小节列了 **3 个**角色（`AliyunServiceRoleForNativeApiGw`、`AliyunServiceRoleForNativeApiGwInvokeFC`、`AliyunServiceRoleForNativeApiGwInvokeKMS`），「权限说明」小节也给了 **3 个**角色的策略 JSON
- 「查看服务关联角色」小节只列了 **2 个**：「通过搜索服务关联角色名称（**AliyunServiceRoleForNativeApiGw、AliyunServiceRoleForNativeApiGwInvokeFC**）查看」，其后三处描述亦均只写「在 AliyunServiceRoleForNativeApiGw **或** AliyunServiceRoleForNativeApiGwInvokeFC 角色详情页面」，**未包含 InvokeKMS**

🔴 **`[官方矛盾]`「内容安全」所需的 SLR 未在任何页出现**（跨页，不裁决）：
- `content-security-protection`：「开启**内容安全**防护策略前，**需授权服务关联角色**。」（**未说明是哪个角色**）
- `service-association-role-provided-only-when-involved-otherwise-no-need`：全页仅 3 个 SLR（NativeApiGw / InvokeFC / InvokeKMS），**无内容安全 / 绿网（lvwang）/ Green 相关角色**

**删除**：路径为「使用阿里云账号登录 RAM 控制台 > 左侧导航栏中单击**身份管理** > **角色** > 在**角色**页面的搜索框输入您希望删除的角色名称（例如 `AliyunServiceRoleForNativeApiGw`）> 在搜索结果中找到目标角色，单击其**操作**列下的**删除角色** > 在弹出的确认对话框中，**输入角色名称进行二次确认**，然后单击**删除角色**」[官方｜service-association-role-provided-only-when-involved-otherwise-no-need]。

> **说明**：当长时间不使用AI网关时，可前往RAM控制台**手动删除**服务关联角色。
> **重要**：删除**云原生API网关**[原文如此]服务关联角色后，**依赖该角色的功能将无法正常使用，请谨慎删除。**
> —— [官方原文｜service-association-role-provided-only-when-involved-otherwise-no-need]

🔴 删除 SLR 必须用**阿里云账号（主账号）**登录 RAM 控制台——这与 §7.3「如非必要都应避免直接使用阿里云账号」形成操作上的张力，客户若有主账号禁用策略需提前规划 `[推断]`。

`[文档未说明]`（SLR）：
1. **各 Action 与网关功能的映射表**——「客户开了什么功能，SLR 就会调哪些 Action」完全空白，因此无法判断某个写 Action 是否真的会被触发（§7.6.3 全部为 `[推断]`）
2. **SLR 的创建时机**——是实例创建时立即创建三个，还是按功能触发分别创建（`create-secret-key` 暗示 InvokeKMS 需用户在创建密钥时点「授权」，与 SLR 页「自动创建」的表述不一致）
3. **`AliyunServiceRoleForNativeApiGwInvokeKMS` 的 `ram:ServiceName` 条件值**与对应的 FAQ 策略示例
4. **三个角色各自的信任策略 JSON 原文**——本页只说「您可以通过信任策略中的 `Service` 字段查看」，未给内容
5. **删除 SLR 后已创建的外部资源（SLB/NLB/EIP/Prometheus 实例/KMS Secret）是否会被清理**——大概率不会，但文档未写
6. 是否支持**跨账号**授权或用资源目录（RD）统管 SLR
7. SLR 的 Action 是否会随版本更新（对比系统策略明写「APIG会向系统策略中添加新的权限」，SLR 策略是否有同样机制未写）

---

### §7 溯源

- `content-security-protection` — AI 安全防护（13917 B）：§7.1 全节——能力定位与「实时扫描」、3 个前置条件（**仅支持文本生成和图片生成场景**、需另开通 AI 安全护栏商品 `lvwang_guardrail_public_cn`、内容安全需授权 SLR）、**Model API 级**配置位置（策略与插件页签）、两种防护服务（AI 安全护栏 vs 内容安全）配置项对比、**6 项防护维度逐字定义**、**4 档防护等级**、**5 个检查策略 Service**、4 种消费者匹配、**5 条生效规则**、「检查策略防护维度未包含拦截策略防护维度则不生效」限定、默认 Service 表（含图片检查响应写成 `img_query_security_check` 的可疑处）、**2 条冲突裁决规则**与三条规则致「第三条配置实际不生效」的示例、**5 个场景化配置配方**、`response_security_check_hp`「适用于流式生成内容检测」与「检查响应…生效时会使流式响应变为非流式」的 `[官方矛盾]`、Service 定义在云盾 AI 安全护栏控制台
- `set-the-gateway-ip-whitelist-and-whitelist` — 设置网关 IP 黑白名单（2746 B）：§7.2 全节——6 个配置项、**应用层（HTTP/HTTPS，默认）vs 传输层（TCP/UDP）**的行为差异（先建连再拒 vs 直接拒连）、**白名单取交集 / 黑名单取并集**规则、「网关全局、域名和路由级别」开篇与「生效粒度」仅两级的 `[官方矛盾]`
- `identity-management` — AI 网关 RAM 身份管理（4956 B）：§7.3 全节——避免主账号直连 AI 网关、RAM 用户两种访问方式与 MFA 建议、AK 不入工程代码（用 STS 或环境变量）、最小权限定义、用户组批量授权三条建议、RAM 角色无长期身份凭证需被扮演、**STS Token 有效期最大值为角色的最大会话时间**、可信实体变更的双重风险（原受信对象权限缺失 / 过度授权）
- `ai-gateway-system-permission-policy-reference` — AI 网关系统权限策略参考（2841 B）：§7.4 全节——系统 vs 自定义策略的定义与维护方、三类策略框架（AI 网关**只展示两类**）、`AliyunAPIGFullAccess` / `AliyunAPIGReadOnlyAccess` / `AliyunServiceRolePolicyForNativeApiGw` 三个策略名与逐字描述、「**APIG会向系统策略中添加新的权限…系统策略的更新将会影响所有授予了该策略的 RAM 身份**」、OpenAPI/CLI 场景推荐自定义策略、「RAM 身份默认没有任何权限」与最小授权原则；§7.4 `AliyunAPIGFullAccess` vs `AliyunNativeApiGwFullAccess` 的 `[官方矛盾]` 一方；§7.6.1「访问您在其他云产品中的资源」与「您不能修改或删除」
- `custom-permission-policy-reference-for-ai-gateway` — AI 网关自定义权限策略参考（2894 B）：§7.5 全节——5 条通用规则、**3 个授权样例的 Action 与 Resource ARN**（示例 1 需额外放开 `apig:Check*`/`apig:ListGateway` 到 `*` 且捆绑 `service/*`、示例 2 的 `httpapi/` 资源类型、示例 3 的 **6 个只读动词前缀**含 `Debug*`/`Export*`）、示例 1 与示例 3 完整 JSON；§7.4 `apig:` / `acs:apig:` 命名体系
- `service-association-role-provided-only-when-involved-otherwise-no-need` — AI 网关服务关联角色（14652 B）：§7.6 全节——**3 个 SLR 的触发场景逐字原文**与命名（含 InvokeKMS 段落主语误写「云原生API网关」）、**166 行 / 165 条去重的 Action 按 9 个产品前缀分类计数**（`slb:ModifyLoadBalancerInternetSpec` 重复 2 次、`slb:DescribeLoadBalancerUDPListenerAttribute` 尾随两个空格）、InvokeFC 1 条与 InvokeKMS 12 条、**179 / 178 合计**、`Resource` 全为 `"*"`、`ram:CreateServiceLinkedRole` / `ram:DeleteServiceLinkedRole` 与两个 `ram:ServiceName` 条件值（`nativeapigw.aliyuncs.com` / `invokefc.nativeapigw.aliyuncs.com`）及完整策略 JSON、查看（基本信息 / 权限管理 / 信任策略管理三页签）与删除路径（需主账号 + 输入角色名二次确认）、「依赖该角色的功能将无法正常使用，请谨慎删除」、「查看服务关联角色只列 2 个角色」的 `[官方矛盾]`、`AliyunNativeApiGwFullAccess` 的 `[官方矛盾]` 另一方
- `create-secret-key` — 创建密钥（1900 B）：§7.6.1 InvokeKMS SLR 的控制台**授权**按钮入口（与 SLR 页「自动创建」表述不一致）；§7.6.3 KMS 连带计费与 `kms:CreateSecret` 的印证；§6.7.2 SLR 名称大小写 `[官方矛盾]` 的一方（主体事实在 §6.7.2）
- **本章查无**（客户会问但文档确实没写）：
  1. **AI 安全防护是否消耗 AI Credits / 如何计费** —— 全页无「AI Credits」「计费」「费用」「价格」「免费」字样；只有一句「需先开通 AI 安全护栏」指向购买页，**单价与计费单位（按调用次数？按扫描字符数？按图片张数？）完全空白**
  2. **AI 安全防护支持哪些地域** —— 无地域清单；「接入地址」只说「默认填充**最近的**内容安全的VPC地址」，未给可选地域列表
  3. **AI 安全防护支持哪些实例类型**（专享 vs Serverless）—— 全页无「专享」「Serverless」字样
  4. **恶意文件检测、数字水印** —— **配置专页**查无此两项（只有「恶意URL检测」），**但产品概述页 `what-is-an-ai-gateway` 有列**（`maliciousFile` / `waterMark`）→ 是「落地文档缺失」不是「能力不存在」；若客户明确要这两项，须转 AI 安全护栏商品侧核验或走工单，**不可基于本页给出配置方法**
  5. **AI 安全防护的性能损耗数字** —— 除 `_hp` 的定性描述外无任何延迟/QPS/超时数字
  6. **命中拦截后的状态码与响应体格式**；被拦截请求是否计入 Token 消耗与计费
  7. **检查结果的日志字段名与所在日志库**（只说「保存在日志中」）
  8. **单次扫描的文本长度 / 图片大小上限**与超限处理
  9. **AI 安全防护、IP 黑白名单、消费者鉴权、全局鉴权四者的执行先后顺序**（全章无任何优先级说明）
  10. **IP 黑白名单的客户端真实 IP 取值规则**（是否解析 XFF、经过 CDN/WAF/SLB/NAT 时如何取、可否配信任跳数）——最高频的客户问题，文档未写
  11. **IP 黑白名单命中后的状态码**、**IP/地址段条数上限**、**是否支持 IPv6**、**网关自身出口 IP 清单**
  12. **「路由级」IP 黑白名单到底存不存在**（§7.2 `[官方矛盾]`，两说并存，文档未给第三处澄清）
  13. **`AliyunAPIGFullAccess` / `AliyunAPIGReadOnlyAccess` 的策略 JSON 内容**（本页只有文字描述，无法审计实际权限范围）
  14. **AI 网关管理员策略究竟叫 `AliyunAPIGFullAccess` 还是 `AliyunNativeApiGwFullAccess`**（§7.4 `[官方矛盾]`，直接影响能否授权成功）
  15. **`apig:` 下的完整 Action 清单**与除 `gateway/`、`service/`、`httpapi/` 外的资源类型 ARN（消费者、密钥、MCP 服务能否独立授权）
  16. **自定义策略可用的 Condition 键**（标签 / 资源组 / MFA / 源 IP）
  17. **SLR 的 Action ↔ 网关功能映射表**（导致 §7.6.3 全部只能是 `[推断]`）
  18. **三个 SLR 各自的信任策略 JSON 原文**、**InvokeKMS 的 `ram:ServiceName` 条件值**、**SLR 的创建时机**
  19. **删除 SLR 后已创建的外部资源（SLB/NLB/EIP/Prometheus/KMS Secret）是否会被回收**
  20. **「内容安全」防护服务所需的 SLR 角色名**（§7.6.5 `[官方矛盾]`）
  21. **RAM 角色最大会话时间的默认值与取值范围**（§7.3 只说「STS Token有效期的最大值为角色的最大会话时间」，无数值）
  22. **是否有 AI 网关特有的 RAM 使用限制**（`identity-management` 全篇为 RAM 通用内容，无产品特有限制）
