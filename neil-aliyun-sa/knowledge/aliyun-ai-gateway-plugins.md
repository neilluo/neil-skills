# AI 网关 · §9 插件体系

> **所属**：[[aliyun-ai-gateway]] 专题页家族（7 文件）｜**主页与导航**：[aliyun-ai-gateway.md](aliyun-ai-gateway.md)
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（186 个快照 = 149 个有正文页 + 37 个 TOC 容器页；另有 SLA 协议全文外部源 1 页）
> **事实标注体系**：`[官方｜slug]` raw 快照有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方原文错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕见 `tests/ai-gateway-rulings-2026-09-21.md`
>
> 🔖 正文中的 `W1`~`W7` 是**本次蒸馏批次的分工代号**（7 路并行 worker），不是产品术语；对照表见 [主页 §0.6](aliyun-ai-gateway.md)。

🔴 **对客纪律**：`ai-cue-template` 与 `ai-cue-decorator` 两个 slug 的**官方标题与正文插件名交叉错位**（裁决 C6）→ 给客户配置示例时**必须写插件名而非 slug**。`frontend-gray` 优先级存在 1000 / 450 两个官方数字（裁决 C7，未裁）→ 必须先实测再承诺。34 页对 AI Credits / 计费 / 免费 / 公测 **全部 0 命中** → 插件的成本影响一律「文档未说明」。

## §9 插件体系

> 本章 owner：W6。全部事实来源为 `/tmp/aigw-shards/W6.tsv` 指派的 34 个 raw 快照（fetch_date 均为 2026-09-21）。
> 本章覆盖 27 个有独立参数页的插件 + 7 个机制/开发页。凡 raw 未写者一律标 `[文档未说明]`，不以先验填补。

---

### §9.1 插件机制总览

#### §9.1.1 插件来源分类（官方三分类）

| 来源类型 | 官方定义（逐字） | 来源 slug |
|---|---|---|
| 官方插件 | 「Higress官方开放到**插件市场**的插件。」 | `manage-plug-ins` |
| 社区插件 | 「Higress社区贡献到**插件市场**的插件。」 | `manage-plug-ins` |
| 自定义插件 | 「用户上传到插件市场的插件，仅供用户自身使用。」 | `manage-plug-ins` |

自定义插件的可见性边界：`[官方原文]`「只有当前主账号或具有AI网关权限的子账号可以看到并使用该插件。插件启用方式和平台提供插件一致。」`[官方｜upload-plug-in]`

#### §9.1.2 🔴 形态限定：Serverless 版不支持插件

`[官方原文]`「仅专享实例型AI网关支持安装与启用插件，Serverless版不支持。」`[官方｜manage-plug-ins]`

> SA 提示：这是本章最硬的选型边界。客户若选 Serverless 形态，本章 27 个插件全部不可用。全 34 页中「Serverless」仅出现这 1 次，无其他补充说明。

#### §9.1.3 安装 → 配置规则 → 启用（三步，缺一不可）

`[官方原文]`「安装插件是指将AI网关**插件市场**中的插件安装到具体的网关实例的过程，任何插件要在网关实例上生效，必须先安装插件、然后配置规则，最后启用插件。」`[官方｜manage-plug-ins]`

两条安装入口（等效）：① 插件市场页 → 插件卡片「安装」→ 选网关实例 → 「配置」栏「规则配置」；② 实例详情页 → 左侧「插件」→「安装插件」→「安装并配置」。`[官方｜manage-plug-ins]`

启用状态开关：路由级/域名级规则在「添加MCP/路由级别规则」「添加域名级别规则」页打开**启用状态**（官方标注**默认开启**）；实例级规则同样需打开启用状态后「保存」。`[官方｜manage-plug-ins]`

#### §9.1.4 卸载插件的前置约束

`[官方原文]`「卸载插件时，如果存在启用的插件规则，请先停用插件再卸载；如果插件未启用，卸载插件会将配置的插件规则一并删除。」`[官方｜manage-plug-ins]`

> 即：卸载 ≠ 停用。带启用规则直接卸载会被拦；未启用状态下卸载会**连带删除已配置的插件规则**（配置可否恢复/导出 `[文档未说明]`）。

#### §9.1.5 插件作用层级（文档写了哪几级就写哪几级）

`manage-plug-ins` 明确给出**三类**插件规则作用域：

| 作用域（官方名称） | 官方定义（逐字） | 匹配优先级 | 来源 slug |
|---|---|---|---|
| **MCP/路由级插件规则** | 「作用在路由上，当请求匹配到指定路由时，规则生效。」 | 高于域名级（见下） | `manage-plug-ins` |
| **域名级插件规则** | 「作用在域名上，特定域名的匹配优先级高于泛域名。」 | 低于路由级 | `manage-plug-ins` |
| **实例级插件规则** | 「作用在网关全局，当路由和域名级规则都没有匹配到的时候则匹配该规则。」 | 兜底 | `manage-plug-ins` |

**第 4 个层级**在另一页出现：`[官方原文]`「配置生效范围选择 **Model API级插件规则**」「生效范围选择**实例级别**」`[官方｜ai-retrieval-augmented-generation-enhanced]`。该页还写「在**Model API级插件规则** 列表中可看到关联 **bailian-llm** 的规则条目，此时生效状态为未启用」。

- `manage-plug-ins` 的三分类里**没有** Model API 级 → `[官方矛盾]`（双方原文已摘，交主控裁）：
  - 甲方（`manage-plug-ins`）：「插件规则根据作用域分为以下三类：MCP/路由级插件规则 / 域名级插件规则 / 实例级插件规则」
  - 乙方（`ai-retrieval-augmented-generation-enhanced`）：「配置生效范围选择 **Model API级插件规则**」
- **MCP 工具级**插件规则：本章 34 页**查无**此层级（`manage-plug-ins` 把 MCP 与路由合并为「MCP/路由级」一类，未提工具粒度）→ `[文档未说明]`
- **API 级**（非 Model API 的普通 API）：`[文档未说明]`

**规则匹配的通用语义**（多页重复出现的同一段官方口径）：

> `[官方原文]`「配置的匹配生效顺序，将按照规则的排列顺序，匹配第一个规则后生效对应配置，后续规则将被忽略。」`[官方｜custom-response-plugin｜request-block-plugin｜waf-plugin｜bot-detect-plug-ins｜key-rate-limit-plugin]`

> `[官方原文]`「配置规则顺序会依次执行匹配，有任一规则匹配到，就会执行对应配置，不再匹配其他规则。因为这里配置路由匹配优先级高于域名，即对当前配置的域名生效，而对域名下的特定路由关闭。」`[官方｜jwt-auth-plug-ins]`

**YAML 内的细粒度规则语法**（仅 `canary-header` 页给出完整形态，其他页只有控制台式描述）：

```yaml
_rules_:
- _match_route_:
  - route-a
  weighted_headers: [...]
- _match_domain_:
  - "*.example.com"
  weighted_headers: [...]
```
`[官方｜canary-header-plugin]`

**单路由关闭插件的开关**：`_disable_: true`（配在路由级规则上）—— `[官方原文]`「因为`_disable_`设置为`true`，当匹配到这个路由时，将关闭此插件功能，不进行JWT认证，所有人均可访问。」`[官方｜jwt-auth-plug-ins]`。该字段仅在 `jwt-auth-plug-ins` 页出现，是否为全插件通用 → `[文档未说明]`。

#### §9.1.6 执行阶段与执行优先级

**四个执行阶段，顺序固定**：

> `[官方原文]`「阶段处理顺序：**认证阶段** > **鉴权阶段** > **统计阶段** > **默认阶段**。若不依赖其他插件执行顺序，填写默认阶段即可。」`[官方｜upload-plug-in｜webide-writing-plug-ins]`

**执行优先级**：

> `[官方原文]`「控制执行阶段内的优先级，数字越大优先级越高。若需定制，建议填写10的整数倍，预留好空间。」`[官方｜upload-plug-in]`

（`webide-writing-plug-ins` 同字段描述略短：「控制执行阶段内的优先级，数字越大优先级越高。」示例值 `100`。）

**请求与应答的处理顺序相反** —— 排障最易错点：

> `[官方原文]`「按照执行阶段和执行优先级，可以确定多个插件在处理请求和应答时的相对顺序。需要注意的是，处理客户端请求的顺序和处理后端应答的顺序是相反的，即越早处理请求的插件，越晚处理应答。」`[官方｜upload-plug-in]`

**如何插入到平台插件前后**：

> `[官方原文]`「在平台提供插件的详情中，可以看到执行阶段和执行优先级的信息，如果希望在特定平台插件执行前后插入自定义插件，可以配置自定义插件的插件执行阶段和插件执行优先级。」`[官方｜upload-plug-in]`

#### §9.1.7 🔴 插件与「策略」的关系：完整优先级总表（逐字照抄）

`upload-plug-in` 给出**唯一一张**跨插件+策略的全局执行顺序表。官方前置口径：`[官方原文]`「以下插件与策略由上到下执行优先级依次降低。」

**「策略」是插件之外的另一类扩展机制**。本表含 3 条策略项，官方标注了各自 Filter 归属，且这 3 行的**执行阶段与优先级两列在原文中为空**：

| 名称 | 类型 | 执行阶段 | 优先级 | 备注 |
|---|---|---|---|---|
| IP黑白名单 | 策略 | （原文空） | （原文空） | RBAC Filter |
| 并发控制/流量控制/熔断 | 策略 | （原文空） | （原文空） | Sentinel Filter |
| 超时/重试/流量复制/Header修改/HTTP重写/跨域 | 策略 | （原文空） | （原文空） | Router Filter |

按表的上下顺序，策略在整条链路中的位置：**IP黑白名单（RBAC Filter）在最前**；全部插件之后是 **并发控制/流量控制/熔断（Sentinel Filter）**；最后是 **超时/重试/流量复制/Header修改/HTTP重写/跨域（Router Filter）**。`[官方｜upload-plug-in]`

完整表（45 行，顺序即执行顺序，逐字照抄；原文为 HTML `<table>`，已逐单元格重排，无删减）：

| # | 名称 | 类型 | 执行阶段 | 优先级 | 备注 |
|---|---|---|---|---|---|
| 1 | IP黑白名单 | 策略 | （原文空） | （原文空） | RBAC Filter |
| 2 | http-real-ip | 插件 | 认证阶段 | 980 | 流量管控系列插件 |
| 3 | ModelRouter | 插件 | 认证阶段 | 900 | AI-API 内置 |
| 4 | ModelMapper | 插件 | 认证阶段 | 800 | AI-API 内置 |
| 5 | 前端灰度 | 插件 | 认证阶段 | 450 | 传输协议系列插件 |
| 6 | IP地理位置 | 插件 | 认证阶段 | 440 | 传输协议系列插件 |
| 7 | DeGraphQL | 插件 | 认证阶段 | 430 | 传输协议系列插件 |
| 8 | 浏览器缓存控制 | 插件 | 认证阶段 | 420 | 传输协议系列插件 |
| 9 | 请求/响应转换 | 插件 | 认证阶段 | 410 | 传输协议系列插件 |
| 10 | OAuth2认证 | 插件 | 认证阶段 | 350 | 认证鉴权系列插件 |
| 11 | JWT认证 | 插件 | 认证阶段 | 340 | 认证鉴权系列插件 |
| 12 | HMAC认证 | 插件 | 认证阶段 | 330 | 认证鉴权系列插件 |
| 13 | Basic认证 | 插件 | 认证阶段 | 320 | 认证鉴权系列插件 |
| 14 | Key认证 | 插件 | 认证阶段 | 310 | 认证鉴权系列插件 |
| 15 | 外部认证 | 插件 | 认证阶段 | 300 | 认证鉴权系列插件 |
| 16 | OPA | 插件 | 认证阶段 | 225 | 认证鉴权系列插件 |
| 17 | 请求校验 | 插件 | 认证阶段 | 220 | 传输协议系列插件 |
| 18 | IP限制 | 插件 | 认证阶段 | 210 | 安全防护系列插件 |
| 19 | JWT Logout | 插件 | 认证阶段 | 50 | 认证鉴权系列插件 |
| 20 | 通用响应缓存 | 插件 | 认证阶段 | 10 | 传输协议系列插件 |
| 21 | 跨域资源共享 | 插件 | 鉴权阶段 | 340 | 安全防护系列插件 |
| 22 | WAF防护 | 插件 | 鉴权阶段 | 330 | 安全防护系列插件 |
| 23 | 请求屏蔽 | 插件 | 鉴权阶段 | 320 | 安全防护系列插件 |
| 24 | 机器人拦截 | 插件 | 鉴权阶段 | 310 | 安全防护系列插件 |
| 25 | ai-data-masking | 插件 | 默认阶段 | 991 | AI系列插件 |
| 26 | ai-statistics | 插件 | 默认阶段 | 990 | AI系列插件 |
| 27 | ai-security-guard | 插件 | 默认阶段 | 850 | AI系列插件 |
| 28 | ai-cache | 插件 | 默认阶段 | 800 | AI系列插件 |
| 29 | ai-quota | 插件 | 默认阶段 | 750 | AI系列插件 |
| 30 | ai-intent | 插件 | 默认阶段 | 700 | AI系列插件 |
| 31 | ai-history | 插件 | 默认阶段 | 650 | AI系列插件 |
| 32 | ai-token-ratelimit | 插件 | 默认阶段 | 600 | AI系列插件 |
| 33 | ai-prompt-template | 插件 | 默认阶段 | 500 | AI系列插件 |
| 34 | ai-prompt-decorator | 插件 | 默认阶段 | 450 | AI系列插件 |
| 35 | ai-network-search | 插件 | 默认阶段 | 440 | AI系列插件 |
| 36 | ai-transformer | 插件 | 默认阶段 | 410 | AI系列插件 |
| 37 | ai-rag | 插件 | 默认阶段 | 405 | AI系列插件 |
| 38 | traffic-tag | 插件 | 默认阶段 | 400 | 流量管控系列插件 |
| 39 | ai-json | 插件 | 默认阶段 | 150 | AI系列插件 |
| 40 | ai-proxy | 插件 | 默认阶段 | 110 | AI系列插件 |
| 41 | canary-header | 插件 | 默认阶段 | 100 | 流量管控系列插件 |
| 42 | 基于Key集群限流 | 插件 | 默认阶段 | 20 | 流量管控系列插件 |
| 43 | 基于Key限流 | 插件 | 默认阶段 | 10 | 流量管控系列插件 |
| 44 | 并发控制/流量控制/熔断 | 策略 | （原文空） | （原文空） | Sentinel Filter |
| 45 | 超时/重试/流量复制/Header修改/HTTP重写/跨域 | 策略 | （原文空） | （原文空） | Router Filter |

来源：`[官方｜upload-plug-in]`

**本表的 SA 用途**：
- 认证类插件的内部相对顺序官方已固化：OAuth2(350) > JWT(340) > HMAC(330) > Basic(320) > Key(310) > 外部认证(300) > OPA(225) > JWT Logout(50)。
- 限流在**最后**：基于Key集群限流(20) 与 基于Key限流(10) 位于默认阶段末尾，即认证/鉴权/转换/AI 插件全部执行完之后才计数限流。
- **本表未收录**、但本章有独立参数页的插件：`hsts`、`custom-response`、`param-access-control`、`AI RAG 检索代理`、`AI检索增强生成（加强版）` → 见 §9.2.3 与「本章查无」。

#### §9.1.8 插件配置格式（WASM 形态）

| 项目 | 官方口径（逐字/要点） | 来源 slug |
|---|---|---|
| 上传物 | 「上传本地编译构建生成的插件二进制文件。文件名需要包含 ".wasm" 后缀。」 | `upload-plug-in` |
| 控制台配置格式 | 「在网关控制台中的插件配置为 yaml 格式，下发给插件时将自动转换为 json 格式」 | `develop-gateway-plug-ins-using-the-go-language` |
| 同上（另一页表述） | 「在控制台插件配置中填写的YAML配置会自动转换为JSON，此处直接从JSON这个参数里解析配置即可」 | `webide-writing-plug-ins` |
| Wasm 运行时 | 本地调试 envoy.yaml 中 `runtime: envoy.wasm.runtime.v8` | `develop-gateway-plug-ins-using-the-go-language` |
| Go 编译命令 | `go mod tidy` + `GOOS=wasip1 GOARCH=wasm go build -buildmode=c-shared -o main.wasm ./` | `develop-gateway-plug-ins-using-the-go-language` |
| 插件镜像形态（Higress 侧） | `url: oci://higress-registry.cn-hangzhou.cr.aliyuncs.com/plugins/de-graphql:1.0.0` | `degraphql-plugin` |
| 发布耗时 | 「单击**上传**，等待插件发布成功（此过程可能需要30秒左右）」 | `upload-plug-in` |
| 发布失败常见原因 | 「一般可能是生成的Wasm文件二进制格式不合法。」 | `upload-plug-in` |
| 适配网关版本 | 「**任意版本**：可以安装到任意版本的网关。**指定版本**：仅可以安装到指定版本（含）之后的网关版本。」 | `upload-plug-in`｜`webide-writing-plug-ins` |
| 版本号格式约束 | 「版本编号，格式需符合X.Y.Z」（示例 `1.0.0`） | `webide-writing-plug-ins` |
| Wasm 文件大小上限 | `[文档未说明]` | — |
| 单实例可安装插件数量上限 | `[文档未说明]`（34 页中「上限」「最多」「数量」均无命中） | — |
| 插件规则条数上限 | `[文档未说明]` | — |

**发布插件面板的全部参数**（`upload-plug-in`，逐字）：

| 参数 | 描述（逐字） |
|---|---|
| **选择语言** | 选择编写插件时使用的开发语言。 |
| **插件标识** | 设置插件的英文标识（唯一标识）。 |
| **插件名称** | 设置插件的中文名称。 |
| **插件描述** | 填写用途说明，会显示在创建完成后的插件卡片中。 |
| **版本描述** | 填写插件的版本描述信息。 |
| **WASM文件** | 上传本地编译构建生成的插件二进制文件。文件名需要包含 ".wasm" 后缀。 |
| **执行阶段** | 阶段处理顺序：**认证阶段** > **鉴权阶段** > **统计阶段** > **默认阶段**。若不依赖其他插件执行顺序，填写默认阶段即可。 |
| **执行优先级** | 控制执行阶段内的优先级，数字越大优先级越高。若需定制，建议填写10的整数倍，预留好空间。 |
| **适配网关版本** | 选择**任意版本**或**指定版本**。**任意版本**：可以安装到任意版本的网关。**指定版本**：仅可以安装到指定版本（含）之后的网关版本。 |

> 「选择语言」的**可选枚举值**未列出 → `[文档未说明]`（可由 §9.6 的语言支持间接推断）。

---

### §9.2 插件目录总表

#### §9.2.1 主表：本章 27 个有独立参数页的插件

「类别」列取值规则：优先抄插件页自带的**「插件类型」**字段；插件页未写时抄 `upload-plug-in` 优先级总表的**「备注」**系列名；两者都无则标 `[文档未说明]` 并给 `[推断]` 理由。

| 插件名 | 类别 | 解决什么问题 | 关键参数（含默认值与取值范围，逐字） | 作用层级 | 使用限制 | 来源 slug |
|---|---|---|---|---|---|---|
| **basic-auth** | 认证鉴权（插件页「插件类型」） | 「实现了基于HTTP Basic Auth标准进行认证鉴权的功能」 | `consumers`(array of object,必填)；`consumers[].credential`(string,必填)；`consumers[].name`(string,必填)；`global_auth`(array of string,选填**仅实例级别配置**,默认`-`)；`allow`(array of string,选填**非实例级别配置**,默认`-`) | 认证（`global_auth`）仅实例级；鉴权（`allow`）仅路由/域名级 | 「在一个规则里，鉴权配置和认证配置不可同时存在。」；「`credential`字段不能重复。」；「凭证信息中的用户名和密码之间使用":"分隔。」 | `basic-auth-plug-ins` |
| **key-auth** | 认证鉴权（插件页「插件类型」） | 「实现了基于API Key进行认证鉴权的功能，支持从HTTP请求的URL参数或者请求头解析API Key，同时验证该API Key是否有权限访问」 | `consumers`(必填)；`keys`(array of string,必填)＝「API Key的来源字段名称，可以是URL参数或者HTTP请求头名称」；`in_query`(bool,默认`true`)；`in_header`(bool,默认`true`)，二者「至少有一个为 true」；`global_auth`(仅实例级)；`allow`(非实例级) | 同上 | 同上；「`credential`字段不能重复。」 | `key-auth-plug-ins` |
| **hmac-auth** | 认证鉴权（插件页「插件类型」） | 「实现了基于HMAC算法为HTTP请求生成不可伪造的签名，并基于签名实现身份认证和鉴权」 | `consumers`(必填)：`key`/`secret`/`name` 均必填；`date_offset`(number,选填,默认`-`,单位秒,「未配置时，不做校验」)；`global_auth`；`allow` | 同上 | 「注意`key`字段不能重复。」；请求 Body 上限 **32MB**（413 `Request Body Too Large.`「请求Body超过限制大小：32MB。」）；`x-ca-signature-method`「取值HmacSHA256或者HmacSHA1，可选，默认值为HmacSHA256」 | `hmac-auth-plug-ins` |
| **jwt-auth** | 认证鉴权（总表备注「认证鉴权系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「实现了基于JWT（JSON Web Tokens）进行认证鉴权的功能，支持从HTTP请求的URL参数、请求头、Cookie字段解析JWT，同时验证该Token是否有权限访问」 | `consumers`(必填)；`jwks`/`remote_jwks`「二选一」；`remote_jwks` 默认 `{"uri":"http://127.0.0.1/keys","service":"test.static","port":"80","ttl":30000,"timeout":3000}`；`from_headers` 默认 `[{"name":"Authorization","value_prefix":"Bearer"}]`；`from_params` 默认 `access_token`；`clock_skew_seconds` 默认 `60`(秒)；`keep_token` 默认 `true`；`claims_to_headers[].override` 默认 `true`；`remote_jwks.timeout` 默认 `3000`(毫秒)、`ttl` 默认 `30000`(毫秒) | 实例级(认证) + 路由/域名级(`allow`) + 路由级 `_disable_: true` | 「建议remote_jwks返回的jwks大小控制在1Mb以内」；「只有当`from_headers`，`from_params`，`from_cookies`均未配置时，才会使用默认值。」；「如果一个JWT能匹配多个jwks，则按照配置顺序命中第一个匹配的consumer。」 | `jwt-auth-plug-ins` |
| **jwt-logout** | 认证鉴权（插件页「插件类型」） | 「利用Redis实现了对JWT的弱状态管理机制，解决了JWT本身无法主动登出的问题，并可用于实现唯一登录控制，例如在支持多设备登录场景下实现用户互踢功能」 | `jwks`(选填,「当此插件搭配jwt-auth插件使用时，无需配置此项」)；`clock_skew` 默认 `60`(秒)；`token_header` 默认 `Authorization`；`token_prefix` 默认 `"Bearer"`；`redis`(**必填**)，`redis.timeout` 默认 `1000`(毫秒)；logout 默认：`key_prefix`=`higress_jwt_logout_`、`key`=`["jti"]`、`path`=`/jwt_logout`、`error_status`=`401`、`error_body`=`{"message":"invalid token"}`；login 默认：`key_prefix`=`higress_jwt_logout_`、`key`=`["iss","aud","sub"]`、`path`=`/jwt_login`、`error_status`=`403`、`error_body`=`{"message":"already login on other device"}`；`ttl` 未填时按 Payload `exp` 减当前时间，「若Payload中没有exp字段，则默认的ttl为86400秒（24小时）」 | `[文档未说明]`（页面未写作用层级） | 🔴 **强依赖 Redis（必填）**；「插件将处理1次请求，导致产生3次Redis读请求（1次logout检查，2次login检查）。在少量情况下（如登出或首次登录），将额外产生2次Redis写请求。为评估Redis容量，可以简单地按插件处理的请求吞吐量乘以2进行计算。」；Redis 异常返回 **500** | `jwt-logout-plug-ins` |
| **oauth**（OAuth2认证） | 认证鉴权（插件页「插件类型」） | 「实现了基于JWT（JSON Web Tokens）进行OAuth2 Access Token签发的能力, 遵循RFC9068规范」 | `consumers`(必填)：`name`/`client_id`/`client_secret` 均必填；`issuer` 默认 `Higress-Gateway`；`auth_path` 默认 `/oauth2/token`；`global_credentials`(bool) 默认 `true`；`auth_header_name` 默认 `Authorization`；`token_ttl`(number,秒) 默认 `7200`；`clock_skew_seconds` 默认 `60`；`keep_token` 默认 `true`；`global_auth`(仅实例级)；`allow`(非实例级) | 实例级 + 路由级 + 域名级 | 「如果路径后缀和`auth_path`匹配，则该路由不会被转发到原目标服务，而是用于生成Token。」；「如果关闭`global_credentials`，请确保启用此插件的路由不是精确匹配路由，此时若存在另一条前缀匹配路由，则可能导致预期外行为。」；「在使用 API 管理时，需要创建相同路径的接口。」；POST 取 Token「需要先匹配到有真实目标服务的路由，否则网关不会读取请求 Body」 | `oauth-plugin` |
| **key-rate-limit**（基于Key限流） | 流量管控（插件页「插件类型」） | 「实现了基于特定键值的限流，键值来源可以是URL参数、HTTP请求头」 | `limit_by_header`(string,选填)／`limit_by_param`(string,选填)——「limit_by_header、limit_by_param中选填一项」；`limit_keys`(array of object,**必填**)：`key`(必填)、`query_per_second`／`query_per_minute`／`query_per_hour`／`query_per_day`（number，「选填一项」，均无默认值） | 路由级 + 域名级（页内示例）；实例级 `[文档未说明]` | 计量维度**仅 2 种**（Header / URL 参数），**不支持** IP、consumer、Cookie；无 `rejected_code`/`rejected_msg` → `[文档未说明]`；页内**无「运行属性」小节** | `key-rate-limit-plugin` |
| **cluster-key-rate-limit**（基于Key集群限流） | 流量管控（总表备注「流量管控系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「基于 Redis 实现集群限流，适用于需要跨多个 Higress Gateway 实例实现全局一致速率限制的场景。限流所使用的 Key 可以来源于 URL 参数、HTTP 请求头、客户端 IP 地址、消费者名称或 Cookie 中的 Key。」 | `rule_name`(必填)；`rule_items`(必填)；`show_limit_quota_header`(bool) 默认 `false`；`rejected_code`(int) 默认 `429`；`rejected_msg`(string) 默认 `Too many requests`；`redis`(必填)：`service_name` 必填、`service_port` 默认「服务类型为固定地址（static service）默认值为80，其他为6379」、`timeout` 默认 `1000`(毫秒) | `[文档未说明]`（页面未写作用层级） | 🔴 **强依赖 Redis**；`redis.service_name`「应填写带服务类型的完整 FQDN 名称（如 `redis.dns`、`redis.my-ns.svc.cluster.local`），而非直接填写 Redis 连接地址」，否则限流不生效 | `throttle-based-on-cluster-keys` |
| **traffic-tag** | 流量管控（总表备注「流量管控系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「允许根据权重或特定请求内容通过添加特定请求头的方式对请求流量进行染色」 | `conditionGroups`(非必填)；`weightGroups`(非必填)；`defaultTagKey`／`defaultTagVal`（非必填，「当且仅当同时配置了」对方「时生效」）；`conditionGroups[]`：`headerName`/`headerValue`/`logic`(`and`、`or`,「必须为小写字母」)/`conditions` 均必填；`conditions[]`：`conditionType`(`header`/`parameter`/`cookie`)、`key`、`operator`(`equal`/`not_equal`/`prefix`/`in`/`not_in`/`regex`/`percentage`)、`value`(「仅当操作符为 `in` 和 `not_in` 时支持配置多个值」) 均必填；`weightGroups[]`：`headerName`/`headerValue`/`weight`(integer,「流量权重百分比」) 均必填 | `[文档未说明]`（页面未写作用层级） | `regex` 引擎为 **RE2**；权重总和 100，「下例中未配置的40权重将不添加header」 | `the-traffic-tag-plugin` |
| **canary-header** | 流量管控（总表备注「流量管控系列插件」；插件页**无**「插件类型」/「运行属性」 `[文档未说明]`） | 「实现了按照指定比例为请求添加指定header的功能。请求添加header后会重新匹配路由，配合此插件，可实现基于比例的灰度路由，而无需客户端主动携带灰度header。」 | `weighted_headers`(array of object,**必填**)：`added_key`(必填)、`added_value`(必填)、`weight`(number,必填,「单位为百分比，所有header的权重之和不能大于100」) | 全局 + `_rules_` 内 `_match_route_` / `_match_domain_` | 「若路由权重之和不大于100，则不足100的部分代表不会添加任何header的概率。」；🔴 **会触发重新匹配路由**（对性能/路由设计的影响 `[文档未说明]`） | `canary-header-plugin` |
| **frontend-gray**（前端灰度） | 传输协议（总表备注「传输协议系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「实现了前端用户灰度的功能，通过此插件，不但可以用于业务`A/B实验`，同时通过`可灰度`配合`可监控`、`可回滚`策略保证系统发布运维稳定性」 | `rules`(array of object,**必填**)；`grayKey`；`useManifestAsEntry` 默认 `false`；`localStorageGrayKey`（「如果配置了当前参数，则`grayKey`失效」）；`graySubKey`；`storeMaxAge`(int) 默认 `60 * 60 * 24 * 365`（「单位为秒，默认为1年」）；`cookieDomain`；`indexPaths`(Glob)；`skippedPaths`(Glob)；`skippedByHeaders`(map)；`rewrite`{`host`,`indexRouting`,`fileRouting`}；`baseDeployment`{`version`**必填**,`backendVersion`,`versionPredicates`}；`grayDeployments`[]{`version`**必填**,`name`**必填**,`versionPredicates`,`backendVersion`,`enabled`,`weight`}；`backendGrayTag` 默认 `x-mse-tag`；`uniqueGrayTag` 默认 `x-higress-uid`；`injection`{`head`,`body.first`,`body.last`}；`rules[]`：`name`**必填**、`grayKeyValue`、`grayTagKey`(来自Cookie)、`grayTagValue`(来自Cookie) | `[文档未说明]`（页面未写作用层级） | `{version}` 为保留字段，运行时被 `baseDeployment.version` 或 `grayDeployments[].version` 动态替换；「`skippedPaths` 的优先级高于当前配置（`skippedByHeaders`），且页面HTML请求不受本配置的影响」；用户信息在 LocalStorage 时需自行注入脚本回写 Cookie | `front-end-grayscale-plug-in` |
| **request-block**（请求屏蔽） | 安全防护（插件页「插件类型」） | 「实现了基于URL、请求头等特征屏蔽HTTP请求，可以用于防护部分站点资源不对外部暴露」 | `block_urls`／`block_headers`／`block_bodys`（array of string，「选填。block_urls，block_headers，block_bodys中至少必填一项。」）；`blocked_code`(number) 默认 `403`；`blocked_message`(string) 默认 `-`；`case_sensitive`(bool) 默认 `true`（「配置匹配时是否区分大小写。默认区分。」） | 路由级 + 域名级（页内示例） | 🔴 「当配置了`block_bodys`时，仅支持小于32MB的请求Body进行匹配。若请求Body大于此限制，并且不存在匹配到的`block_urls`和`block_headers`项时，不会对该请求执行屏蔽操作。」；「若请求Body超过全局配置DownstreamConnectionBufferLimits，将返回`413 Payload Too Large`, 请在参数配置页调高此项。注意调高此参数配置后，网关内存使用将有显著增加。」 | `request-block-plugin` |
| **waf**（WAF防护） | 安全防护（插件页「插件类型」） | 「实现了基于ModSecurity的规则防护引擎，可以根据用户配置的规则屏蔽可疑请求，并支持OWASP CRS，为站点提供基础的防护功能」 | `useCRS`(bool) 默认 `false`（「是否开启OWASP CRS」）；`secRules`(array of string) 默认 `-`（「用户自定义的waf防护规则，语法规则可参考ModSecurity中文手册」） | 路由级 + 域名级（页内示例） | 🔴 `[官方原文]`「该插件基于开源ModSecurity规则，默认规则为静态规则，不具备识别最新的安全风险并实时更新规则集的能力，如需获取更强大的安全防护能力，请参见开启WAF防护。」；仅观测不拦截需显式加 `secRules: - "SecRuleEngine DetectionOnly"` | `waf-plugin` |
| **bot-detect**（机器人拦截） | 安全防护（插件页「插件类型」） | 「可以用于识别并阻止互联网爬虫对站点资源的爬取」 | `allow`(array of string,选填)＝「配置匹配User-Agent请求头的正则表达式，匹配命中时将允许其访问」；`deny`(array of string,选填)＝「匹配命中时将屏蔽请求」；`blocked_code`(number) 默认 `403`；`blocked_message`(string) 默认 `-` | 路由级 + 域名级（路由可「做空配置保存」以套用内置默认规则） | 「`allow`和`deny`字段可以均不配置，则执行默认的爬虫判断逻辑」；🔴 「若不做该配置，默认的Golang网络库请求会被视作爬虫，被禁止访问。」（需 `allow: - ".*Go-http-client.*"` 放行） | `bot-detect-plug-ins` |
| **geo-ip**（IP地理位置） | 传输协议（总表备注「传输协议系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「实现了通过用户IP查询出地理位置信息，然后通过请求属性和新添加的请求头把地理位置信息传递给后续插件」 | `ip_protocol`(string,否) 默认 `ipv4`；`ip_source_type`(string,否) 默认 `origin-source`（可选值：对端socket ip＝`origin-source`；通过header获取＝`header`）；`ip_header_name`(string,否) 默认 `x-forwarded-for`（「当`ip_source_type`为`header`时，指定自定义IP来源头」） | `[文档未说明]`（页面未写作用层级） | 🔴 **ipv6 未实现**：「ipv6：（未来实现后）只对ipv6用户查找地理位置信息…（目前是跳过插件，请求由后续插件处理。）」；地理库来自 ip2region 全网段库转 CIDR，「在Higress启动读配置阶段读取geoCidr.txt文件并且解析到radixtree数据结构的内存里」；与 AI 提示词装饰器联用时「geo-ip插件的优先级必须高于AI提示词装饰器插件」 | `geographic-location-of-ip` |
| **hsts** | 流量管控（插件页「插件类型」） | 「HSTS插件的作用是通知浏览器在未来的一段时间内，它应该只使用HTTPS与该服务器进行通信。HSTS与HTTPS强跳转的不同地方在于，HSTS对于HTTP请求可以直接在浏览器通过307内部跳转完成HTTPS转换，无需执行额外的网络请求。」 | `max_age`(number,选填) 默认 `15724800`（「强制使用HTTPS访问网站的最大持续时间（以秒为单位）」）；`include_sub_domains`(bool,选填) 默认 `false` | `[文档未说明]`（页面未写作用层级） | 🔴 「当开启`include_sub_domains`时，当前域名以及子域名强制使用HTTPS访问网站，必须确保所有子域名都支持HTTPS，否则用户将无法访问这些子域名。」；实现方式：「会对所有的HTTPS响应中添加`strict-transport-security`头部」；`upload-plug-in` 总表**未收录** hsts | `hsts-plug-in` |
| **http-real-ip** | 流量管控（插件页「插件类型」） | 「http-real-ip插件是nginx real-ip 模块的wasm实现。」 | `real_ip_from`：「定义已知发送客户端请求的可信地址。」（默认值/类型 `[文档未说明]`）；`real_ip_header`：「定义包含客户端地址的请求Header，其值将用于替换客户端地址，默认使用`x-forwarded-for`。」 | `[文档未说明]`（页面未写作用层级） | 🔴 **页面仅 384 字节**：无数据类型列、无填写要求、无 `real_ip_from` 默认值、无取值范围、无配置示例、无错误码 → 信息量不足以支撑对客答复（见「本章查无」） | `http-real-ip-plug-ins` |
| **cache-control**（浏览器缓存控制） | 传输协议（总表备注「传输协议系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「实现了基于 URL 文件后缀来为请求的响应头部添加 `Expires` 和 `Cache-Control` 头部，从而方便浏览器对特定后缀的文件进行缓存，例如 `jpg`、`png` 等图片文件」 | `suffix`(string,选填)：「表示匹配的文件后缀名，例如 `jpg`、`png` 等。如果需要匹配多种后缀，需要用 `\|` 进行分割，例如 `png\|jpg`。如果不填写，表示匹配所有后缀」；`expires`(string,**必填**)：「当填入的字符串为数字时，单位为秒，例如需要缓存1小时，需填写 3600。另外，还可以填写 epoch 或 max，与 nginx 中语义相同。」 | `[文档未说明]`（页面未写作用层级） | `expires: max` 时「缓存所有文件，且缓存至最大时间 `"Thu, 31 Dec 2037 23:55:55 GMT"`」 | `browser-cache-control` |
| **param-access-control**（参数访问控制） | `[文档未说明]`（插件页**无**「插件类型」字段）。`[推断]` 归安全防护，理由：页面自述「实现了基于请求参数和上下文条件进行精确访问控制」，执行阶段为**鉴权阶段**、DENY 默认 `403`，与总表鉴权阶段的 4 个「安全防护系列插件」同段 | 「实现了基于请求参数和上下文条件进行精确访问控制，可用于实现复杂的请求验证和访问管理场景」 | `parameters`(object,**必填**)「支持从Header、Query、Path中提取」，格式 `Header:参数名`／`Query:参数名`／`Path:序号`（「序号从1开始」）／`Path`（「获取完整路径」）；`rules`(array of rule,**必填**)：`name`(必填)、`condition`(必填)、`ifTrue`(选填,ALLOW/DENY)、`ifFalse`(选填,ALLOW/DENY)、`statusCode`(number,选填) 默认 `403`、`responseHeaders`(object,选填)、`responseBody`(string,选填) | `[文档未说明]`（页面未写作用层级） | 「每个规则必须至少配置ifTrue或ifFalse其中之一」；「规则按照配置顺序依次执行直到遇到ALLOW或DENY指令」；运算符/函数：`==` `!=` `>` `>=` `<` `<=` `contains` `matches` `startsWith` `endsWith` `&&` `\|\|` `!`；🔴 页面自述「鉴权阶段/310」与总表「机器人拦截｜鉴权阶段｜310」**同号冲突** | `parameter-access-control` |
| **custom-response** | 传输协议（插件页「插件类型」） | 「支持配置自定义的响应，包括自定义HTTP应答状态码、HTTP应答头，以及HTTP应答Body。可以用于Mock响应，也可以用于判断特定状态码后给出自定义应答，例如在触发网关限流策略时实现自定义响应」 | `status_code`(number,选填) 默认 `200`；`headers`(array of string,选填)「Key和 Value 用`=`分隔」；`body`(string,选填)；`enable_on_status`(array of number,选填)「匹配原始状态码，生成自定义响应，不填写时，不判断原始状态码」 | 路由级 + 域名级（页内示例） | `upload-plug-in` 总表**未收录** custom-response（阶段/优先级 `[文档未说明]`）；限流场景官方推荐：`enable_on_status: [429]` + `status_code: 302` + `headers: [Location=https://example.com]`，「从而实现基于浏览器302重定向机制，将限流后的用户引导到其他页面，比如可以是一个CDN上的静态页面」 | `custom-response-plugin` |
| **de-graphql**（DeGraphQL） | 传输协议（总表备注「传输协议系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「`de-graphql`插件通过将URIs映射到GraphQL查询，从而可以将GraphQL上游转换为传统服务进行访问。」 | `gql`＝「graphql 查询」，默认栏原文写「不能为空」；`endpoint`＝「graphql 查询端点」，默认 `/graphql`；`timeout`＝「查询连接超时，单位毫秒」，默认 `5000`；`domain`＝「服务域名，当服务来源是DNS配置」，默认栏为空 | `[文档未说明]`（页面未写作用层级；示例为 Higress Ingress + WasmPlugin CRD `matchRules.ingress`） | 参数表**只有 3 列**（参数/描述/默认），无数据类型与填写要求列 → `gql` 数据类型 `[文档未说明]`；页内示例是开源 Higress 的 K8s CRD 形态，非 AI 网关控制台形态 | `degraphql-plugin` |
| **ai-prompt-decorator**（页面自称「AI提示词插件」，slug 为 `ai-cue-template`，见 §9.2.2） | AI（总表备注「AI系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「AI提示词插件，支持在LLM的请求前后插入prompt。」 | `prepend`(array of message object,optional,默认`-`)＝「在初始输入之前插入的语句」；`append`(array of message object,optional,默认`-`)＝「在初始输入之后插入的语句」；message object：`role`(string,**必填**)、`content`(string,**必填**) | `[文档未说明]`（页面未写作用层级） | 与 geo-ip 联用需「在相同的请求处理阶段里，geo-ip插件的优先级必须高于AI提示词装饰器插件」，官方举例「geo-ip插件的priority配置1000，ai-prompt-decorator插件的priority配置500」；支持 `${geo-country}`/`${geo-province}`/`${geo-city}` 插值 | `ai-cue-template` |
| **ai-prompt-template**（页面自称「AI提示词模板」，slug 为 `ai-cue-decorator`，见 §9.2.2） | AI（总表备注「AI系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「AI提示词模板，用于快速构建同类型的AI请求。」 | `templates`(array of object,**必填**,默认`-`)；template object：`name`(string,必填)、`template.model`(string,必填,「模型名称」)、`template.messages`(array of object,必填,「大模型输入」)；message object：`role`(必填)、`content`(必填) | `[文档未说明]` | 模板变量语法 `{{program}}`／`{{language}}`；调用方请求体形如 `{"template":"developer-chat","properties":{"program":"quick sort","language":"python"}}`；`template.model` 与网关 Model API 模型映射关系 `[文档未说明]`；模板数量上限、变量缺失时行为 `[文档未说明]` | `ai-cue-decorator` |
| **ai-rag** | AI（总表备注「AI系列插件」；插件页**无**「插件类型」字段 `[文档未说明]`） | 「通过对接阿里云向量检索服务DashVector实现LLM-RAG」 | **11 个参数全部「必填」、全部无默认值**：`dashscope.apiKey`/`serviceFQDN`/`servicePort`(int)/`serviceHost`；`dashvector.apiKey`/`serviceFQDN`/`servicePort`(int)/`serviceHost`/`topk`(int)/`threshold`(float)/`field`(string)。示例取值：`servicePort: 443`、`topk: 1`、`threshold: 0.4`、`field: raw`、`collection: xxx` | `[文档未说明]`（页面未写作用层级） | `threshold`＝「向量距离阈值，高于该阈值的文档会被过滤掉」；`topk`＝「阿里云向量检索时获取向量数」；**外部依赖两个**：DashScope（千问）+ DashVector；`dashvector.collection` 出现在示例中但**未列入参数表**；`topk`/`threshold` 取值范围 `[文档未说明]` | `ai-rag` |
| **AI RAG 检索代理** | AI（操作步骤中控制台路径为「插件类型选择**AI**」；页面无「插件类型」字段） | 「通过检索协议转化和检索结果转换, 实现Dify等AI应用连接并检索RAGFlow和百炼知识库等外部RAG引擎」 | 基本：`rag_proxy.provider.name`(必填,枚举 `ragflow`/`bailian`)、`rag_proxy.source.name`(选填,默认 `dify`,枚举仅 `dify`)、`rag_proxy.source.enable_to_proxy_api_key`(选填,默认 `false`)、`rag_proxy.source.to_proxy_api_key`(选填)。RAGFlow：`api_key`(必填)、`dataset_ids`/`document_ids`(选填)、`similarity_threshold` 默认 `0.0`、`top_n` 默认 `30`、`vector_similarity_weight` 默认 `0.3`、`keyword` 默认 `false`、`rerank_id`(选填,「默认不开启该功能」)。百炼：`api_key`(必填)、`index_id`(选填)、`enable_reranking` 默认 `true`、`rerank_min_score` 默认「当前知识库配置的相似度阈值」取值 `[0.01-1.00]`、`rerank_top_n` 默认 `5` 取值 `[1-20]`、`save_retriever_history` 默认 `false`、`dense_similarity_top_k` 默认 `100` 取值 `[0-100]`、`sparse_similarity_top_k` 默认 `100` 取值 `[0-100]`，「二者之和小于等于200」 | `[文档未说明]`（页面未写作用层级；操作流程绑定 **Agent API 路由**） | 🔴 **路由「需要确保路径后缀为/retrieval」**；Dify 侧 Endpoint「注意需要去除/retrieval后缀」；开启 `enable_to_proxy_api_key` 后「AI网关与外部知识库调用方之间API Key必须一致，否则无法正常使用」；`dataset_ids`「如这里不填，请在Dify配置外部知识库时填写，优先以Dify配置的外部知识库ID为准」 | `ai-retrieval-agent` |
| **AI 检索增强生成（加强版）** | AI（控制台路径「插件 > 安装插件 > **AI** > AI检索增强生成（加强版）」） | 「通过对接主流RAG引擎实现LLM调用前的自动检索增强生成，支持RARFlow和百炼知识库。」`[原文如此]`（RARFlow 应为 RAGFlow） | 基本：`rag.rag_engine_type`(必填,枚举 `ragflow`/`bailian`)、`result_placement_type`(选填,默认 `append`,枚举 `append`/`replace`)。RAGFlow：`api_key`(必填)、`serviceFQDN`(必填)、`servicePort`(**必填**,类型标 string)、`dataset_ids`(**必填**)、`serviceHost`(选填)、`document_ids`(选填)、`similarity_threshold` 默认 `0.2`、`top_n` 默认 `30`、`vector_similarity_weight` 默认 `0.3`、`rerank_id`(选填)。百炼：`ak`/`sk`/`serviceFQDN`/`workspace_id`/`index_id` 均**必填**；`servicePort` 默认 `443`；`serviceHost` 默认 `bailian.cn-beijing.aliyuncs.com`；`enable_reranking` 默认 `false`；`rerank_min_score` 默认「当前知识库配置的相似度阈值」取值 `[0.01 - 1.00]`；`rerank_top_n` 默认 `5` 取值 `[1 - 20]`；`rerank_model` 默认 `gte-rerank-hybrid`（支持 `gte-rerank-hybrid`、`gte-rerank`）；`enable_rewrite` 默认 `false`；`rewrite_model` 默认 `conv-rewrite-qwen-1.8b`；`save_retriever_history` 默认 `false`；`dense_similarity_top_k` 默认 `100` 取值 `[0 - 100]`；`sparse_similarity_top_k` 默认 `100` 取值 `[0 - 100]`，「二者之和小于等于200」 | **实例级**（RAGFlow 场景）与 **Model API级插件规则**（百炼场景） | `replace` 模式依赖占位符 `{{higressRagResultReplacementKey}}`；百炼走 **AK/SK** 而非 API Key，子账号需「具有AliyunBailianDataFullAccess或sfm:Retrieve的操作权限」且「已经被授权加入到百炼业务空间权限」；RAGFlow 服务 TLS「保持默认关闭」、百炼服务 TLS「选择单向TLS」；`servicePort` 类型标 string 但示例写 `servicePort: 80` | `ai-retrieval-augmented-generation-enhanced` |
| **ai-transformer**（AI 请求响应转换） | `[官方矛盾]`：总表「请求/响应转换｜认证阶段｜410｜**传输协议系列插件**」与「ai-transformer｜默认阶段｜410｜**AI系列插件**」两行同优先级但阶段与系列均不同；本页自述「认证阶段/410」 | 「AI 请求响应转换插件，通过LLM对请求/响应的header以及body进行修改。」 | **7 个参数全部「必填」、全部无默认值**：`request.enable`(bool)、`request.prompt`(string)、`response.enable`(**string**) `[原文如此：类型标 string，示例值 true/false]`、`response.prompt`(string)、`provider.serviceName`(string)＝「DNS类型的服务名，目前仅支持千问」、`provider.domain`(string)＝「LLM服务域名」、`provider.apiKey`(string)＝「阿里云dashscope服务的API Key」 | `[文档未说明]`（页面未写作用层级） | 🔴 LLM 供应商「目前仅支持千问」；`provider.serviceName` 必须是 **DNS 类型**服务；每请求额外 LLM 调用次数与流式响应处理方式 `[文档未说明]` | `ai-request-response-intelligent-transformation` |

#### §9.2.2 🔴 官方命名错位：`ai-cue-template` / `ai-cue-decorator` 两页的 slug、标题、正文三者交叉

本章最容易导致对客答错的一处：

| slug | TSV 第 3 列官方标题 | 正文首句自称 | 正文「运行属性」 | 正文参数结构 | 与 `upload-plug-in` 总表对照 |
|---|---|---|---|---|---|
| `ai-cue-template` | AI 提示词插件 | 「AI提示词插件，支持在LLM的请求前后插入prompt。」 | `默认阶段` / `450` | `prepend` / `append` | 总表 `ai-prompt-decorator` = 默认阶段 / **450** |
| `ai-cue-decorator` | AI 提示词模板插件 | 「AI提示词模板，用于快速构建同类型的AI请求。」 | `默认阶段` / `500` | `templates` | 总表 `ai-prompt-template` = 默认阶段 / **500** |

第三方交叉验证（`geographic-location-of-ip` 页）：`[官方原文]`「**基于geo-ip插件的能力，扩展AI提示词装饰器插件携带用户地理位置信息**」「如果需要在LLM的请求前后加入用户地理位置信息，请确保同时开启geo-ip插件和**AI提示词装饰器插件**。并且在相同的请求处理阶段里，geo-ip插件的优先级必须高于**AI提示词装饰器插件**」（raw 第 38-39 行，小节标题与正文各一次）—— 即 `prepend`/`append` 结构对应**装饰器（decorator）**，与 `ai-cue-template` 这个 slug 的字面语义相反。
> 🔴 **2026-09-21 主控修正（R1 判定 D4+D7，DEF-6）**：本条原引「AI提示词装饰器插件的配置示例如下」并标注出自 `geographic-location-of-ip`，实测**该页写的是「AI提示词插件的配置示例如下」（raw 第 48 行，无「装饰器」三字）**，被引字符串在该页 0 命中，只在 `ai-cue-template:86` 命中。已改为引用该页**确实存在**的第 38-39 行原文，**结论不变且更强**（同一页在小节标题与正文里三次称其为「AI提示词装饰器插件」）。
> ⚠️ 附带发现：`geographic-location-of-ip` **同页内部**也不一致 —— 第 38/39 行称「AI提示词**装饰器**插件」，第 48 行的示例引导句却称「AI提示词插件」，这与 `ai-cue-template`/`ai-cue-decorator` 的 slug↔标题错位是同一现象的延伸（`[官方矛盾]`，未裁决）。

结论（`[推断]`，推理链：`ai-cue-template` 正文优先级 450 + 正文结构 prepend/append + `geographic-location-of-ip` 把 prepend/append 称为「装饰器」+ 总表 `ai-prompt-decorator`=450 ⇒ `ai-cue-template` 页实际承载的是 **ai-prompt-decorator** 的文档；对称地 `ai-cue-decorator` 页实际承载 **ai-prompt-template**）：**两个 slug 的字面语义与其承载的插件正好互换**。对客引用时应以「正文自述能力 + 优先级 + 参数结构」为准，不要以 slug 或 TSV 标题为准。§9.2.1 主表已按此结论标注。

#### §9.2.3 仅在优先级总表出现、本章无独立参数页的插件（20 项）

以下各项在 `upload-plug-in` 总表中有名称/阶段/优先级/系列，但**不在 W6 清单内**，故本章只能给到「存在性 + 阶段 + 优先级 + 系列」四项事实，参数与限制一律 `[文档未说明]`：

| 名称 | 执行阶段 | 优先级 | 备注（官方系列） | 推测归属章 |
|---|---|---|---|---|
| ModelRouter | 认证阶段 | 900 | AI-API 内置 | §4/§5（W3） |
| ModelMapper | 认证阶段 | 800 | AI-API 内置 | §4/§5（W3） |
| 外部认证 | 认证阶段 | 300 | 认证鉴权系列插件 | §6（W4） |
| OPA | 认证阶段 | 225 | 认证鉴权系列插件 | §6（W4） |
| 请求校验 | 认证阶段 | 220 | 传输协议系列插件 | `[文档未说明]` |
| IP限制 | 认证阶段 | 210 | 安全防护系列插件 | §7（W4，IP 黑白名单） |
| 通用响应缓存 | 认证阶段 | 10 | 传输协议系列插件 | `[文档未说明]` |
| 跨域资源共享 | 鉴权阶段 | 340 | 安全防护系列插件 | `[文档未说明]` |
| ai-data-masking | 默认阶段 | 991 | AI系列插件 | §7（W4，AI 安全） |
| ai-statistics | 默认阶段 | 990 | AI系列插件 | §10（W7，可观测） |
| ai-security-guard | 默认阶段 | 850 | AI系列插件 | §7（W4，AI 安全护栏） |
| ai-cache | 默认阶段 | 800 | AI系列插件 | §5（W3，AI 缓存） |
| ai-quota | 默认阶段 | 750 | AI系列插件 | §5（W3，消费者配额/FinOps） |
| ai-intent | 默认阶段 | 700 | AI系列插件 | `[文档未说明]` |
| ai-history | 默认阶段 | 650 | AI系列插件 | `[文档未说明]` |
| ai-token-ratelimit | 默认阶段 | 600 | AI系列插件 | §5（W3，Token 限流） |
| ai-network-search | 默认阶段 | 440 | AI系列插件 | §5（W3，联网搜索） |
| ai-json | 默认阶段 | 150 | AI系列插件 | `[文档未说明]` |
| ai-proxy | 默认阶段 | 110 | AI系列插件 | §4（W3，Model API 代理） |
| IP黑白名单（**策略**） | （原文空） | （原文空） | RBAC Filter | §7（W4） |

> 「推测归属章」列是 `[推断]`，仅供主控做交叉引用，不是官方事实。

#### §9.2.4 官方分类体系（三套并存，不可混用）

| 分类体系 | 出现位置 | 全部取值（逐字） |
|---|---|---|
| 插件页「**插件类型**」字段 | basic-auth / key-auth / hmac-auth / oauth / jwt-logout / request-block / waf / bot-detect / key-rate-limit / hsts / http-real-ip / custom-response | `认证鉴权`、`安全防护`、`流量管控`、`传输协议` |
| `upload-plug-in` 总表「**备注**」系列名 | 优先级总表 | `流量管控系列插件`、`AI-API 内置`、`传输协议系列插件`、`认证鉴权系列插件`、`安全防护系列插件`、`AI系列插件` |
| 控制台「**快捷导航**」插件类型 | `ai-retrieval-agent`、`ai-retrieval-augmented-generation-enhanced` 操作步骤 | 仅出现 `AI` 一个取值，其余取值 `[文档未说明]` |

🔴 `[官方矛盾]`（分类口径不一致，双方原文）：
- 甲方（`hsts-plug-in`）：「## **插件类型** 流量管控。」——hsts 自称流量管控；
- 乙方（`upload-plug-in` 总表）：「前端灰度｜插件｜认证阶段｜450｜传输协议系列插件」「IP地理位置｜…｜传输协议系列插件」——同处认证阶段、同为报文/响应头改写类的插件被归入传输协议系列，而 `http-real-ip` 又被归入「流量管控系列插件」。
即「流量管控」在插件页与总表中的外延不一致，且总表未收录 hsts。主控需裁定统一口径。

---

### §9.3 AI 增强类插件深潜

#### §9.3.0 共性结论（先给 SA 的三条硬事实）

1. 🔴 **是否消耗 AI Credits：全 34 页 0 命中**。对 `AI Credits`／`Credits`／`计费`／`收费`／`免费`／`公测` 在本章 34 个快照中检索**无任何命中** → 所有 AI 增强类插件是否消耗 AI Credits 一律 `[文档未说明]`。这是本章最大的报价级空白（见「本章查无」）。
2. **Token 开销影响：官方无任何量化数字**。仅能从「必然额外调用 LLM」「必然注入检索文本」做定性推断，一律标 `[推断]`。
3. **性能页无 AI 插件数据**：`plug-in-performance-reference` 只点名 `key-auth`（20微秒左右）与 `basic-auth`（30微秒左右），**未给任何 AI 插件耗时** → `[文档未说明]`（详见 §9.6.4）。

#### §9.3.1 AI 提示词装饰器（ai-prompt-decorator，slug `ai-cue-template`）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「支持在LLM的请求前后插入prompt。」 | `ai-cue-template` |
| 运行属性 | 执行阶段 `默认阶段`，执行优先级 `450` | `ai-cue-template` |
| 参数 | `prepend`：array of message object，optional，默认 `-`，「在初始输入之前插入的语句」；`append`：array of message object，optional，默认 `-`，「在初始输入之后插入的语句」 | `ai-cue-template` |
| message object | `role`(string,**必填**,默认`-`,「角色」)；`content`(string,**必填**,默认`-`,「消息」) | `ai-cue-template` |
| 外部依赖 | 无（纯报文改写） `[推断]`（参数表中无任何服务名/apiKey 字段） | `ai-cue-template` |
| 地理位置插值 | 需**同时开启** geo-ip 插件；「在相同的请求处理阶段里，geo-ip插件的优先级必须高于AI提示词装饰器插件」；官方示例「在默认阶段里，geo-ip插件的priority配置1000，ai-prompt-decorator插件的priority配置500」；可用变量 `${geo-country}`、`${geo-province}`、`${geo-city}`；传值机制「geo-ip插件会根据用户IP计算出用户的地理位置信息，然后通过请求属性传递给后续插件」 | `ai-cue-template`｜`geographic-location-of-ip` |
| Token 开销 | `[推断]`：`prepend`/`append` 各新增 message 直接进入 LLM 输入 ⇒ 每请求 input token 必然增加，增量＝注入文本长度 × 命中请求数。官方无数字 → `[文档未说明]` | `ai-cue-template` |
| 是否消耗 AI Credits | `[文档未说明]` | — |

典型用法（精简 YAML，逐字）：
```yaml
prepend:
- role: system
  content: "请使用英语回答问题"
append:
- role: user
  content: "每次回答完问题，尝试进行反问"
```
效果：原始单条 `{"role":"user","content":"你是谁？"}` 被扩为 **system + user + user 三条** message。`[官方｜ai-cue-template]`

> 🔴 优先级口径不一致：本页「运行属性」写 `450`（与总表 `ai-prompt-decorator`=450 一致），但 `geographic-location-of-ip` 与本页的联用示例都要求把 ai-prompt-decorator 配成 `500`、geo-ip 配成 `1000`——而总表 `500` 属 `ai-prompt-template`、`geo-ip`（IP地理位置）固定为 `440`。该示例数值是"建议覆盖"还是"必须覆盖" → `[文档未说明]`。

#### §9.3.2 AI 提示词模板（ai-prompt-template，slug `ai-cue-decorator`）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「AI提示词模板，用于快速构建同类型的AI请求。」 | `ai-cue-decorator` |
| 运行属性 | 执行阶段 `默认阶段`，执行优先级 `500` | `ai-cue-decorator` |
| 参数 | `templates`：array of object，**必填**，默认 `-`，「模板设置」 | `ai-cue-decorator` |
| template object | `name`(string,必填,「模板名称」)；`template.model`(string,必填,「模型名称」)；`template.messages`(array of object,必填,「大模型输入」) | `ai-cue-decorator` |
| message object | `role`(必填)、`content`(必填) | `ai-cue-decorator` |
| 变量语法 | 双花括号，如 `{{program}}`、`{{language}}` | `ai-cue-decorator` |
| 调用方请求体形态 | `{"template":"developer-chat","properties":{"program":"quick sort","language":"python"}}` —— 客户端**不再发 messages**，只发模板名 + 变量 | `ai-cue-decorator` |
| 外部依赖 | 无 `[推断]`（无服务名/apiKey 字段） | `ai-cue-decorator` |
| Token 开销 | `[推断]`：模板展开后的全部 messages 成为 LLM 输入，system 提示词长度决定固定开销；官方无数字 → `[文档未说明]` | — |
| 是否消耗 AI Credits / 模板数量上限 / `properties` 缺变量时行为 / 模板名不存在时错误码 | `[文档未说明]` | — |

配置示例（逐字，体现结构）：
```yaml
templates:
- name: "developer-chat"
  template:
    model: gpt-3.5-turbo
    messages:
    - role: system
      content: "You are a {{program}} expert, in {{language}} programming language."
    - role: user
      content: "Write me a {{program}} program."
```
`[官方｜ai-cue-decorator]`

#### §9.3.3 ai-rag（DashVector 版）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「通过对接阿里云向量检索服务DashVector实现LLM-RAG」 | `ai-rag` |
| 运行属性 | 执行阶段 `默认阶段`，执行优先级 `400` ← 🔴 `[官方矛盾]`：总表写「ai-rag｜插件｜默认阶段｜**405**｜AI系列插件」，且总表中 `400` 已被 `traffic-tag` 占用。双方原文已摘 | `ai-rag`｜`upload-plug-in` |
| 参数（**11 项全部「必填」，全部无默认值**） | `dashscope.apiKey`(string)「用于在访问千问服务时进行认证的令牌。」；`dashscope.serviceFQDN`(string)「千问服务名。」；`dashscope.servicePort`(int)「千问服务端口。」；`dashscope.serviceHost`(string)「访问千问服务时域名。」；`dashvector.apiKey`(string)「用于在访问阿里云向量检索服务DashVector时进行认证的令牌。」；`dashvector.serviceFQDN`(string)；`dashvector.servicePort`(int)；`dashvector.serviceHost`(string)；`dashvector.topk`(int)「阿里云向量检索时获取向量数。」；`dashvector.threshold`(float)「向量距离阈值，高于该阈值的文档会被过滤掉。」；`dashvector.field`(string)「阿里云向量检索存储文档的字段名。」 | `ai-rag` |
| 示例中额外出现但参数表未收录的字段 | `dashvector.collection`（示例值 `xxxxxxxxxxxxxxx`）→ 文档缺口，是否必填 `[文档未说明]` | `ai-rag` |
| 示例取值（逐字） | `dashscope`: `serviceFQDN: dashscope`、`servicePort: 443`、`serviceHost: dashscope.aliyuncs.com`；`dashvector`: `serviceFQDN: dashvector`、`servicePort: 443`、`serviceHost: vrs-cn-xxxxxxxxxxxxxxx.dashvector.cn-hangzhou.aliyuncs.com`、`topk: 1`、`threshold: 0.4`、`field: raw` | `ai-rag` |
| 外部依赖 | ① DashScope（千问）② 阿里云向量检索服务 DashVector。语料向量化需**另做**，官方指向教程「基于向量检索服务DashVector与TextEmbedding实现语义搜索」，示例语料为 CEC-Corpus（332 篇突发事件新闻报道） | `ai-rag` |
| 可观测联动 | 「插件开启后，在使用链路追踪功能时，会在`span`的`attribute`中添加`rag`检索到的文档`id`信息，供排查问题使用。」 | `ai-rag` |
| `topk`/`threshold` 取值范围 | `[文档未说明]`（仅标 int/float，无区间） | — |
| Token 开销 | `[推断]`：检索到的文档拼入 LLM 输入 ⇒ input token 增加，量级由 `topk` 与文档长度决定。官方无数字 → `[文档未说明]` | — |
| 是否消耗 AI Credits（DashVector 侧是否另计费） | `[文档未说明]` | — |
| 效果对比（官方给的唯一定性证据） | 原始请求「海南追尾事故，发生在哪里？原因是什么？人员伤亡情况如何？」——未经 RAG：「抱歉，作为AI模型，我无法实时获取和更新新闻事件的具体信息…」；经 RAG：「海南追尾事故发生在海文高速公路文昌至海口方向37公里处…人员伤亡情况是1人死亡（司机当场死亡），另有8人受伤（包括2名儿童和6名成人）…」 | `ai-rag` |

#### §9.3.4 AI RAG 检索代理（`ai-retrieval-agent`）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「通过检索协议转化和检索结果转换, 实现Dify等AI应用连接并检索RAGFlow和百炼知识库等外部RAG引擎。」 | `ai-retrieval-agent` |
| 运行属性 | 执行阶段 `默认阶段`，执行优先级 `150` ← 总表**无**「AI RAG 检索代理」行，`150` 属 `ai-json` → 名称映射 `[文档未说明]`，数值撞号 `[官方矛盾]` | `ai-retrieval-agent`｜`upload-plug-in` |
| 与「加强版」的定位差异 | 本插件是**检索协议代理**（Dify → 网关 → RAGFlow/百炼），全程**不调用 LLM**；加强版是**在 LLM 调用前自动注入检索结果**。`[推断]`（由两页能力自述对比：本页「实现AI应用与外部RAG引擎连接」，加强版「实现LLM调用前的自动检索增强生成」） | 两页 |
| 基本配置 | `rag_proxy.provider.name`(string,**必填**)「被调用的外部知识库的类型,支持的枚举类型目前包括：ragflow、bailian。」；`rag_proxy.source.name`(string,选填,默认 `dify`)「外部知识库调用方引擎类型,支持的枚举类型目前包括: dify。」；`rag_proxy.source.enable_to_proxy_api_key`(boolean,选填,默认 `false`)「是否开启AI网关与外部知识库调用方之间API Key校验，不填写默认为false，开启后AI网关与外部知识库调用方之间API Key必须一致，否则无法正常使用。」；`rag_proxy.source.to_proxy_api_key`(string,选填)「填写后，AI网关会校验此处填入的参数是否与外部知识库创建API时填写的API Key相同，否则不进行校验。」 | `ai-retrieval-agent` |
| RAGFlow 参数 | `api_key`(必填,「可在RAGFlow控制台右上角头像-API-RAGFlow API处获取」)；`dataset_ids`(list[string],选填)；`document_ids`(list[string],选填,「可以只在指定的Document下检索」)；`similarity_threshold`(float,选填,默认 `0.0`,「低于阈值的分块会被过滤，可以在Dify的召回界面配置该参数」)；`top_n`(integer,选填,默认 `30`,「返回相似度最高的top_n个分块, 其他分块会被过滤」)；`vector_similarity_weight`(float,选填,默认 `0.3`,「如果x表示向量余弦相似度, 则`(1-x)`表示语义相似度权重」)；`keyword`(boolean,选填,默认 `false`,「是否启用基于关键字的匹配」)；`rerank_id`(integer,选填,「RAG引擎中配置的Rerank模型的ID…默认不开启该功能」) | `ai-retrieval-agent` |
| 百炼参数 | `api_key`(必填)；`index_id`(选填,「阿里云百炼知识库ID」)；`enable_reranking`(bool,选填,默认 `true`)；`rerank_min_score`(float,选填,默认「当前知识库配置的相似度阈值」,「仅开启Rerank时生效」,取值 `[0.01-1.00]`)；`rerank_top_n`(integer,选填,默认 `5`,「仅开启Rerank时生效」,取值 `[1-20]`)；`save_retriever_history`(bool,选填,默认 `false`)；`dense_similarity_top_k`(integer,选填,默认 `100`,取值 `[0-100]`)；`sparse_similarity_top_k`(integer,选填,默认 `100`,取值 `[0-100]`)；后两者「dense_similarity_top_k和sparse_similarity_top_k二者之和小于等于200」 | `ai-retrieval-agent` |
| 🔴 硬约束：路由后缀 | 「单击**创建路由**，注意需要确保路径后缀为/retrieval，服务选择步骤1创建的RAGFlow检索服务。」；Dify 侧「API Endpoint使用上述网关接入点与Agent API路由路径组合（`http(s)://{endpoint}/{agent api path}`），注意需要去除/retrieval后缀，API Key可自行定义。」 | `ai-retrieval-agent` |
| 承载对象 | **Agent API**（「协议选择自定义」）+ 网关「服务」：RAGFlow 用**固定地址**来源、端口设置为 `80`（「如果是同VPC内容器部署的RAGFlow实例，也可以采用容器服务作为服务来源创建服务」）；百炼用 **DNS 域名**来源 | `ai-retrieval-agent` |
| 鉴权叠加 | 「如果在插件中配置了rag_proxy.source.enable_to_proxy_api_key和rag_proxy.source.to_proxy_api_key，需保证API Key和rag_proxy.source.to_proxy_api_key保持一致，否则Dify访问AI网关会鉴权失败，无法执行后续路由。」 | `ai-retrieval-agent` |
| `dataset_ids` 优先级 | 「如这里不填，请在Dify配置外部知识库时填写，优先以Dify配置的外部知识库ID为准。」 | `ai-retrieval-agent` |
| 百炼外部知识库 ID 格式 | 「外部知识库ID的格式为：{知识库ID}」 | `ai-retrieval-agent` |
| 验证方式 | 「前往Dify知识库页面…在召回测试输入源文本进行验证，能够根据召回设置返回文本分块，即说明实现连通。」 | `ai-retrieval-agent` |
| 外部依赖 | RAGFlow（自建/容器）或 阿里云百炼知识库（百炼 API Key 从百炼控制台获取） | `ai-retrieval-agent` |
| 是否消耗 AI Credits / Token 开销 | `[文档未说明]`（本页不调用 LLM；百炼知识库检索自身是否计费 `[文档未说明]`） | — |
| `similarity_threshold` / `top_n` / `vector_similarity_weight` 取值范围 | `[文档未说明]`（仅给默认值 0.0 / 30 / 0.3） | — |

#### §9.3.5 AI 检索增强生成（加强版）（`ai-retrieval-augmented-generation-enhanced`）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「通过对接主流RAG引擎实现LLM调用前的自动检索增强生成，支持RARFlow和百炼知识库。」`[原文如此]`（RARFlow 应为 RAGFlow） | 同页 |
| 运行属性 | 执行阶段 `默认阶段`，执行优先级 `400` ← 总表**无**本插件行，`400` 属 `traffic-tag`、`ai-rag` 属 `405` → `[官方矛盾]`/撞号 | 同页｜`upload-plug-in` |
| 结果注入方式 | `result_placement_type`(string,选填,默认 `append`)：「支持用户模板替换占位符，如果选择replace，则System提示词模板中的占位符`{{higressRagResultReplacementKey}}`会被替换为RAG生成的内容，如果选择append，则RAG生成的内容会被追加到用户模板中，支持的枚举类型包括: append、replace。」 | 同页 |
| RAGFlow 参数 | `rag.ragflow.api_key`(必填)；`serviceFQDN`(必填,「RAGFlow在AI网关的服务名」)；`servicePort`(**必填**,类型标 **string**)；`dataset_ids`(list[string],**必填**)；`serviceHost`(选填,「AI网关访问RAGFlow时域名」)；`document_ids`(选填)；`similarity_threshold`(float,选填,默认 `0.2`)；`top_n`(integer,选填,默认 `30`)；`vector_similarity_weight`(float,选填,默认 `0.3`)；`rerank_id`(integer,选填) | 同页 |
| 百炼参数 | `ak`(**必填**,「调用百炼的access key」)；`sk`(**必填**)；`serviceFQDN`(**必填**)；`workspace_id`(**必填**,「阿里云百炼业务空间ID」)；`index_id`(**必填**,「阿里云百炼知识库ID」)；`servicePort`(选填,默认 `443`)；`serviceHost`(选填,默认 `bailian.cn-beijing.aliyuncs.com`)；`enable_reranking`(bool,选填,默认 `false`)；`rerank_min_score`(float,选填,默认「当前知识库配置的相似度阈值」,「仅开启Rerank时生效」,取值 `[0.01 - 1.00]`)；`rerank_top_n`(integer,选填,默认 `5`,取值 `[1 - 20]`)；`rerank_model`(string,选填,默认 `gte-rerank-hybrid`,「支持的模型包括：gte-rerank-hybrid、gte-rerank」)；`enable_rewrite`(bool,选填,默认 `false`,「是否开启会话改写」)；`rewrite_model`(string,选填,默认 `conv-rewrite-qwen-1.8b`,「会基于会话上下文自动调整原始用户问题以提升检索效果，支持的模型包括：conv-rewrite-qwen-1.8b」)；`save_retriever_history`(bool,选填,默认 `false`)；`dense_similarity_top_k`(选填,默认 `100`,取值 `[0 - 100]`)；`sparse_similarity_top_k`(选填,默认 `100`,取值 `[0 - 100]`)；后两者「二者之和小于等于200」 | 同页 |
| 🔴 与「检索代理」页的默认值/鉴权方式差异（同一后端两套口径） | `enable_reranking`：检索代理页默认 **`true`**，加强版页默认 **`false`**；RAGFlow `similarity_threshold`：检索代理页默认 **`0.0`**，加强版页默认 **`0.2`**；百炼鉴权：检索代理页用 **`api_key`**，加强版页用 **`ak`+`sk`+`workspace_id`**；RAGFlow `dataset_ids`：检索代理页**选填**，加强版页**必填** → `[官方矛盾]`，双方原文均已摘录 | `ai-retrieval-agent`｜同页 |
| 前置对象 | 需先「创建Model API」（「在AI网关创建AI服务和文本生成场景Model API，确保可以通过Model API访问模型进行文本对话」）；再创建网关「服务」：RAGFlow 用**固定地址**来源、地址格式 `IP:端口`、端口 `80`、**「TLS模式：保持默认关闭」**；百炼用 **DNS 域名**来源、地址格式 `DNS域名:端口`、端口 `443`、**「TLS模式：选择单向TLS」** | 同页 |
| FQDN 获取 | 「在服务详情页的**概览** > **基本信息** 区域，查看**FQDN** 字段的值，例如 `bailian-rag.dns`」 | 同页 |
| 🔴 百炼子账号权限要求 | 「具有AliyunBailianDataFullAccess或sfm:Retrieve的操作权限」+「子账号已经被授权加入到百炼业务空间权限」；官方另建议「为了您的数据安全，强烈建议您创建子账号并使用子账号AK/SK」 | 同页 |
| 生效范围（本页明确写了两种） | RAGFlow 场景：「生效范围选择**实例级别**，开启启用状态开关后单击**保存**」；百炼场景：「配置生效范围选择 **Model API级插件规则**…同时在上方 API 选择面板中勾选需要绑定的目标 API」，创建后「此时生效状态为未启用」（需另行启用） | 同页 |
| 验证方式 | 「单击**Model API**，选择插件作用生效的API，并单击**调试**，验证添加RAG检索能力之后的模型返回结果。」 | 同页 |
| 外部依赖 | RAGFlow（自建，同 VPC 容器部署可用容器服务来源）或 百炼知识库；`rerank_model`/`rewrite_model` 为百炼侧模型 | 同页 |
| Token 开销 / 是否消耗 AI Credits | `[文档未说明]`。`[推断]`：① 检索结果 append/replace 进 System 提示词 ⇒ 每请求 input token 增加；② 开启 `enable_rewrite` 会额外触发一次改写模型（`conv-rewrite-qwen-1.8b`）调用；③ 开启 rerank 会触发 rerank 模型（`gte-rerank-hybrid`/`gte-rerank`）调用 —— ②③ 都是**额外的模型调用**，是否计入 AI Credits、是否单独计费 `[文档未说明]` | 同页 |
| 配置格式说明（官方原话） | 「配置格式为 YAML，顶层字段 `rag_engine_type` 设为 `ragflow`，其余参数嵌套在 `ragflow` 节点下。」 | 同页 |

#### §9.3.6 AI 请求响应转换（ai-transformer，`ai-request-response-intelligent-transformation`）

| 项目 | 事实 | 来源 |
|---|---|---|
| 能力 | 「通过LLM对请求/响应的header以及body进行修改。」 | 同页 |
| 运行属性 | 执行阶段 `认证阶段`，执行优先级 `410` | 同页 |
| 参数（**7 项全部「必填」，全部无默认值**） | `request.enable`(bool)「是否在request阶段开启转换」；`request.prompt`(string)「request阶段转换使用的prompt」；`response.enable`(**string**)「是否在response阶段开启转换」`[原文如此：类型标 string，示例值 true/false]`；`response.prompt`(string)「response阶段转换使用的prompt」；`provider.serviceName`(string)「DNS类型的服务名，目前仅支持千问」；`provider.domain`(string)「LLM服务域名」；`provider.apiKey`(string)「阿里云dashscope服务的API Key」 | 同页 |
| 示例取值（逐字） | `request.enable: false`；`request.prompt: "如果请求path是以/httpbin开头的，帮我去掉/httpbin前缀，其他的不要改。"`；`response.enable: true`；`response.prompt: "帮我修改以下HTTP应答信息，要求：1. content-type修改为application/json；2. body由xml转化为json；3. 移除content-length。"`；`provider.serviceName: qwen`；`provider.domain: dashscope.aliyuncs.com` | 同页 |
| 典型用法 | XML → JSON 应答转换（官方示例：httpbin `/xml` 的 slideshow XML 被转成 JSON，`content-type` 改 `application/json`，`content-length` 被移除） | 同页 |
| 外部依赖 | DashScope（千问），且必须以 **DNS 类型服务**注册到网关 | 同页 |
| 🔴 Token 开销 | `[推断]`：由「通过LLM对请求/响应的header以及body进行修改」+ `provider.apiKey` 必填 + `request.enable`/`response.enable` 可分别开关 ⇒ 开启 request 转换每请求多 1 次 LLM 调用，开启 response 转换再多 1 次，两项都开则每请求最多 **2 次**额外 LLM 调用；被转换的 header/body 全文都会成为 prompt 输入。**官方未给任何数字，也未说明流式（SSE）响应如何处理** → `[文档未说明]` | 同页 |
| 是否消耗 AI Credits | `[文档未说明]` | — |
| LLM 调用失败/超时的降级行为（放行还是报错） | `[文档未说明]` | — |
| 转换结果的正确性保证（是否可能改坏 body） | `[文档未说明]` | — |
| 名称/系列归类 | `[官方矛盾]`：总表有两行可能对应——「请求/响应转换｜插件｜**认证阶段**｜410｜**传输协议系列插件**」与「ai-transformer｜插件｜**默认阶段**｜410｜**AI系列插件**」，同优先级 410 但阶段与系列都不同；本页自述「认证阶段/410」。双方原文已摘 | `upload-plug-in`｜同页 |

#### §9.3.7 AI 辅助插件开发（是能力，不是插件）

| 项目 | 事实 | 来源 |
|---|---|---|
| 定位 | 「为了满足差异化的网关使用需求，同时降低网关插件的开发难度，AI网关提供了基于大模型的端到端插件生成功能。您可以将插件运行逻辑用自然语言进行描述，即可开始端到端的插件生成工作，轻松实现任意定制化的网关场景需求。」 | `ai-auxiliary-plug-in-development` |
| 生成范围 | 「AI网关可以根据您提供的自然语言需求来生成插件代码，并结合一定的代码编译、测试修复手段，实现端到端的插件功能自动开发。」 | 同页 |
| 需求描述模板（官方建议四段式） | `# 请求头处理函数` / `# 请求体处理函数` / `# 响应头处理函数` / `# 响应体处理函数`，无需求写「无」。官方示例首段：「对于网关接收到的任意请求直接返回固定的字符串，要求字符串可以通过配置修改」 | 同页 |
| 🔴 会被拒的情形 | `[官方原文]`「大模型首先会根据需求描述进行判断，对于不合理的开发需求会直接结束任务，并给出相关建议，此时您应该参考建议内容对需求进行修改。」 | 同页 |
| 产物落地 | 「AI 大模型会根据您的需求尝试生成完整的插件代码，插件生成成功后会自动导入WebIDE中，您可对生成的插件进行功能验证，根据实际需求对插件代码进行调整。」 | 同页 |
| 生成语言 | Golang（「一个空的Golang插件示例代码如下」） | 同页 |
| 插件代码结构（官方定义） | 「网关插件的开发包括配置解析和处理函数两个部分，配置解析是读取插件输入配置的过程，处理函数则是指请求头处理、请求体处理、响应头处理以及响应体处理的四个函数」 | 同页｜`webide-writing-plug-ins` |
| 使用的模型 / 是否消耗 AI Credits / 生成次数配额 / 是否收费 / 生成失败率 | `[文档未说明]` | — |
| 与 WebIDE「一键生成」的关系 | `webide-writing-plug-ins` 另有入口：「WebIDE支持用户通过自然语言描述实现一键生成插件代码」，步骤「右上角单击**一键生成** → 在一键生成编辑框中详细描述需求 → 单击**确认**，等待代码生成直至结束」。两页是否同一能力的两处描述 → `[文档未说明]` | `webide-writing-plug-ins` |

> `[官方矛盾]`（骨架代码 import 不一致，影响客户复用示例）：
> - 甲方（`ai-auxiliary-plug-in-development`）：`func parseConfig(json gjson.Result, config *MyConfig, log wrapper.Log) error`
> - 乙方（`webide-writing-plug-ins`｜`develop-gateway-plug-ins-using-the-go-language`）：`func parseConfig(json gjson.Result, config *MyConfig, log logs.Log) error`，import 为 `logs "github.com/higress-group/wasm-go/pkg/log"`
> 不裁决。

---

### §9.4 认证鉴权类插件深潜

#### §9.4.1 🔴 插件形态 vs 产品内置消费者鉴权机制：本章能确证的边界

**先说清证据边界**：本章 34 页中，把插件与内置机制做对比的官方原文**只有一句**（在 jwt-auth 插件页首段）：

> `[官方原文]`「相较于[配置JWT认证鉴权](https://help.aliyun.com/document_detail/2807798.html)，jwt-auth插件额外提供了调用方身份识别的能力，支持对不同调用方配置不同的JWT凭证。」`[官方｜jwt-auth-plug-ins]`

由此**可确证**的选型判据只有一条：

| 判据 | 内置「配置JWT认证鉴权」 | `jwt-auth` 插件 | 来源 |
|---|---|---|---|
| 调用方身份识别 | 不具备（由上句「额外提供了」反推 `[推断]`） | **具备**，「支持对不同调用方配置不同的JWT凭证」 | `jwt-auth-plug-ins` |
| 通过后写入的标识头 | `[文档未说明]`（该页在 W4 清单，本章未读） | 「请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称」 | `jwt-auth-plug-ins` |

**什么时候必须用插件**（仅列本章有明文依据的 5 条）：

| # | 场景 | 唯一可用形态 | 官方依据（逐字） |
|---|---|---|---|
| 1 | 需按调用方（consumer）区分 JWT 凭证 + 细粒度授权（`allow` 白名单） | `jwt-auth` 插件 | 「jwt-auth插件额外提供了调用方身份识别的能力，支持对不同调用方配置不同的JWT凭证」`[官方｜jwt-auth-plug-ins]` |
| 2 | JWT 主动登出 / 唯一登录互踢 | `jwt-logout` 插件 | 「解决了JWT本身无法主动登出的问题，并可用于实现唯一登录控制，例如在支持多设备登录场景下实现用户互踢功能」`[官方｜jwt-logout-plug-ins]` |
| 3 | 网关自己签发 OAuth2 Access Token（RFC9068，Client Credential） | `oauth` 插件 | 「实现了基于JWT（JSON Web Tokens）进行OAuth2 Access Token签发的能力, 遵循RFC9068规范」`[官方｜oauth-plugin]` |
| 4 | HMAC 签名认证（x-ca-key / x-ca-signature 体系） | `hmac-auth` 插件 | 「实现了基于HMAC算法为HTTP请求生成不可伪造的签名」`[官方｜hmac-auth-plug-ins]` |
| 5 | HTTP Basic Auth | `basic-auth` 插件 | 「实现了基于HTTP Basic Auth标准进行认证鉴权的功能」`[官方｜basic-auth-plug-ins]` |

**以下问题本章一律 `[文档未说明]`，SA 不可自行推断（须查 W4 或提工单）**：
- 内置消费者鉴权机制**具体能做什么**（API-Key/JWT/OIDC/自建认证四类的字段、配额、生效范围）→ 归 W4：`consumer-authentication-authentication`、`consumer-authentication`、`consumer-certification`、`consumer-certification-1`、`creating-a-consumer`、`authorization-management`、`configure-jwt-authentication`、`configure-oidc-authentication`、`configure-self-built-authentication`
- 🔴 **两者能否叠加**（同一 Model API 同时开内置鉴权 + `key-auth` 插件）→ `[文档未说明]`
- 🔴 **叠加时的执行顺序**（内置消费者鉴权在 §9.1.7 总表的哪一行、与 310/340 的先后）→ `[文档未说明]`。总表认证阶段的行只有插件（Key认证 310 … OAuth2认证 350）与「外部认证 300」「OPA 225」，**没有任何一行标注为「内置消费者鉴权」**。
- 插件 YAML 里的 `consumers` 与控制台「消费者」对象**是否同一实体**（同名是否复用、是否需先在控制台建消费者）→ `[文档未说明]`。本章 6 个认证插件的 `consumers` 都是**在插件 YAML 里内联定义凭证**，未见引用控制台消费者对象的语法。
- `X-Mse-Consumer` 是否也由内置鉴权写入 / 是否透传到后端 / 能否被 `cluster-key-rate-limit` 的 `limit_by_consumer` 直接消费 → `[推断]` 可行（`limit_by_consumer` 描述为「根据 consumer 名称进行限流」，认证插件写入的正是 consumer 名称），但官方**未明写**两者对接关系 → `[文档未说明]`
- 认证插件是否支持 MCP 工具级作用域 → `[文档未说明]`

#### §9.4.2 六个认证插件的能力矩阵

| 维度 | basic-auth | key-auth | hmac-auth | jwt-auth | jwt-logout | oauth |
|---|---|---|---|---|---|---|
| 认证依据 | HTTP Basic（用户名:密码） | API Key | HMAC 签名 | JWT | JWT + Redis 状态 | 网关签发的 OAuth2 JWT |
| 凭证字段 | `credential`（「用户名和密码之间使用":"分隔」） | `credential` | `key` + `secret` | `jwks` 或 `remote_jwks`（二选一） | 可复用 jwt-auth（「当此插件搭配jwt-auth插件使用时，无需配置此项」） | `client_id` + `client_secret` |
| 凭证取自何处 | Authorization 头（Basic base64） | URL 参数 或 HTTP 请求头（字段名由 `keys` 指定） | `x-ca-key`／`x-ca-signature`／`x-ca-signature-method`／`x-ca-signature-headers` 四个头 | URL 参数 / 请求头 / Cookie | 请求头（`token_header` + `token_prefix`） | `auth_header_name`（默认 `Authorization`） |
| 防重放 | `[文档未说明]` | `[文档未说明]` | ✅ `date_offset`（秒，「未配置时，不做校验」） | ✅ `clock_skew_seconds` 默认 `60` | ✅ `clock_skew` 默认 `60` | ✅ `clock_skew_seconds` 默认 `60` |
| 主动登出 | `[文档未说明]` | `[文档未说明]` | `[文档未说明]` | 不支持（JWT 无状态，正是 jwt-logout 要解决的问题） | ✅ | `[文档未说明]` |
| 唯一登录/互踢 | `[文档未说明]` | `[文档未说明]` | `[文档未说明]` | `[文档未说明]` | ✅ | `[文档未说明]` |
| 外部依赖 | 无 | 无 | 无 | `remote_jwks` 需一个可拉取 JWKS 的服务 | 🔴 **Redis（`redis` 字段必填）** | 无（网关自签发） |
| 全局开关 | `global_auth` | `global_auth` | `global_auth` | `global_auth` | `[文档未说明]` | `global_auth` + `global_credentials`（默认 `true`） |
| 细粒度授权 | `allow` | `allow` | `allow` | `allow` + `_disable_` | `[文档未说明]` | `allow` |
| 通过后写入 | `X-Mse-Consumer` | `X-Mse-Consumer` | `X-Mse-Consumer` | `X-Mse-Consumer` | `[文档未说明]` | `X-Mse-Consumer` |
| 执行阶段/优先级（总表） | 认证阶段 / 320 | 认证阶段 / 310 | 认证阶段 / 330 | 认证阶段 / 340 | 认证阶段 / 50 | 认证阶段 / 350 |
| 插件页是否自带「运行属性」 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 |
| 错误码 | 401 / 401 / 403 | 401 / 401 / 403 | 400×3 / 401×2 / 403 / 413×2 | 401×3 / 403 | 401 / 500 | 401 / 403 |

来源：`basic-auth-plug-ins`｜`key-auth-plug-ins`｜`hmac-auth-plug-ins`｜`jwt-auth-plug-ins`｜`jwt-logout-plug-ins`｜`oauth-plugin`｜`upload-plug-in`

> 六个认证插件页**都没有「运行属性」小节**，阶段与优先级只能从 `upload-plug-in` 总表回填。这本身是文档缺口——对客解释「为什么我的认证插件在限流之前生效」时只能引总表。

#### §9.4.3 六插件共有的四条硬约束（逐字）

1. `[官方原文]`「在一个规则里，鉴权配置和认证配置不可同时存在。」`[官方｜basic-auth-plug-ins｜key-auth-plug-ins｜hmac-auth-plug-ins｜jwt-auth-plug-ins｜oauth-plugin]`
   → **SA 避坑**：`consumers`/`global_auth`（认证）配在**实例级**，`allow`（鉴权）配在**路由级或域名级**；同一条规则里混写会失效。
2. `[官方原文]`「对于通过认证鉴权的请求，请求的Header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。」`[官方｜basic-auth-plug-ins｜key-auth-plug-ins｜hmac-auth-plug-ins｜jwt-auth-plug-ins｜oauth-plugin]`
3. `global_auth` 的**三态**语义（五个插件逐字一致）：
   `[官方原文]`「只能在实例级别配置，若配置为true，则全局生效认证机制; 若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。」
   → 🔴 **不配置 ≠ 关闭**。这是「我没开全局认证为什么全被拦了」的根因。
   → `[官方矛盾]`：数据类型列标 `array of string`，但描述与全部示例都是布尔（`global_auth: false` / `global_auth: true`）。双方原文已摘。
4. `allow` 的作用域限定：
   `[官方原文]`「只能在路由或域名等细粒度规则上配置，对于符合匹配条件的请求，配置允许访问的 consumer，从而实现细粒度的权限控制。」`[官方｜basic-auth-plug-ins｜key-auth-plug-ins｜hmac-auth-plug-ins｜jwt-auth-plug-ins｜oauth-plugin]`

#### §9.4.4 basic-auth 完整参数与错误码

认证配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **consumers** | array of object | 必填。 | - | 配置服务的调用者，用于对请求进行认证。 |
| **global_auth** | array of string | 选填（**仅实例级别配置**） | - | 只能在实例级别配置，若配置为true，则全局生效认证机制; 若配置为false，则只对做了配置的域名和路由生效认证机制，若不配置则仅当没有域名和路由配置时全局生效（兼容老用户使用习惯）。 |

`consumers[]`：`credential`(string,必填,-,「配置该consumer的访问凭证。」)、`name`(string,必填,-,「配置该consumer的名称。」)
鉴权配置（非必需）：`allow`(array of string,选填（**非实例级别配置**）,-,见 §9.4.3 第 4 条)

实例级配置示例（逐字）：
```yaml
global_auth: false
consumers:
- credential: 'admin:123456'
  name: consumer1
- credential: 'guest:abc'
  name: consumer2
```
路由级 `allow: [consumer1]`；域名级 `allow: [consumer2]`。

错误码：

| HTTP状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | Request denied by Basic Auth check. No Basic Authentication information found. | 请求未提供凭证。 |
| 401 | Request denied by Basic Auth check. Invalid username and/or password. | 请求凭证无效。 |
| 403 | Request denied by Basic Auth check. Unauthorized consumer. | 请求的调用方无访问权限。 |

拒绝语义（官方示例明示）：未提供用户名密码 → **401**；用户名密码错误 → **401**；匹配到的调用者不在 `allow` 列表 → **403**。
来源：`[官方｜basic-auth-plug-ins]`

#### §9.4.5 key-auth 完整参数与错误码

认证配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **consumers** | array of object | 必填 | - | 配置服务的调用者，用于对请求进行认证。 |
| **keys** | array of string | 必填 | - | API Key的来源字段名称，可以是URL参数或者HTTP请求头名称。 |
| **in_query** | bool | `in_query`和`in_header`至少有一个为 true | true | 配置为`true`时，网关会尝试从URL参数中解析API Key。 |
| **in_header** | bool | `in_query`和`in_header`至少有一个为 true | true | 配置为`true`时，网关会尝试从HTTP请求头中解析API Key。 |
| **global_auth** | array of string | 选填（仅实例级别配置） | - | 同 basic-auth（逐字一致） |

`consumers[]`：`credential`(必填)、`name`(必填)；鉴权：`allow`(选填（非实例级别配置）)

实例级配置示例（逐字）：
```yaml
global_auth: false
consumers:
- credential: 2bda943c-ba2b-11ec-ba07-00163e125***
  name: consumer1
- credential: c8c8e9ca-558e-4a2d-bb62-e700dcc40***
  name: consumer2
keys:
- apikey
- x-api-key
```
两种传 Key 方式（官方均给示例）：URL 参数 `?apikey=...`，或请求头 `-H 'x-api-key: ...'`。

错误码：

| HTTP状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | No API key found in request. | 请求未提供API Key。 |
| 401 | Request denied by Key Auth check. Invalid API key. | 不允许当前API Key访问。 |
| 403 | Request denied by Basic Auth check. Unauthorized consumer. | 请求的调用方无访问权限。 |

🔴 `[原文如此]` 两处复制残留（对客排障需知）：
- 第 3 行错误信息在 **key-auth** 页写作「Request denied by **Basic** Auth check. Unauthorized consumer.」→ 客户收到含 "Basic Auth" 字样的 403 时，**不能据此断定其用的是 basic-auth 插件**。
- 本页「网关实例级别开启」小节正文写「以下配置将对网关实例级别开启 **Basic Auth** 认证」，但其下配置含 `keys` 字段，实为 key-auth。

拒绝语义：API Key **无效** → **401**；API Key 有效但 consumer **不在 `allow`** → **403**。
来源：`[官方｜key-auth-plug-ins]`

#### §9.4.6 hmac-auth 完整参数、签名机制与错误码

认证配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **consumers** | array of object | 必填 | - | 配置服务的调用者，用于对请求进行认证。 |
| **date_offset** | number | 选填 | - | 配置允许的客户端最大时间偏移，单位为秒。根据请求头`Date`解析客户端UTC时间，可用于避免请求重放。未配置时，不做校验。 |
| **global_auth** | array of string | 选填（仅实例级别配置） | - | 同 basic-auth |

`consumers[]`：`key`(string,必填,「配置该consumer的访问凭证。」)、`secret`(string,必填,「配置用于生成签名的secret。」)、`name`(string,必填)
鉴权：`allow`(选填（非实例级别配置）)

**签名串结构（7 字段，逐字）**：
```
HTTPMethod
Accept
Content-MD5
Content-Type
Date
Headers
PathAndParameters
```
> `[官方原文]`「以上7个字段构成整个签名串，字段之间使用\n间隔，如果Headers为空，则不需要加\n，其他字段如果为空都需要保留\n。签名大小写敏感。」

各字段提取规则（要点逐字）：
- `HTTPMethod`：「HTTP的方法，全部大写，比如POST。」
- `Accept`：「请求中的Accept头的值，可为空。建议显式设置 Accept Header。当 Accept 为空时，部分HTTP客户端会给Accept设置默认值为`*/*`，导致签名校验失败。」← 🔴 高频踩坑
- `Content-MD5`：「只有在请求存在Body且Body为非Form形式时才计算Content-MD5头」；Java 参考算法 `String content-MD5 = Base64.encodeBase64(MD5(bodyStream.getbytes("UTF-8")));` `[原文如此]`
- `Content-Type`：「请求中的Content-Type头的值，可为空。」
- `Date`：「当未开启`date_offset`配置时，可为空，否则将用于时间偏移校验。」
- `Headers`：参与签名的 Header Key **按字典排序**后以 `HeaderKey + ":" + HeaderValue + "\n"` 依次拼接；「某个Header的Value为空，则使用HeaderKey+":"+"\n"参与签名，需要保留Key和英文冒号」；「所有参与签名的Header的Key的集合使用英文逗号分割放到Key为`X-Ca-Signature-Headers`的Header中」；**不参与**签名计算的 Header：`X-Ca-Signature`、`X-Ca-Signature-Headers`、`Accept`、`Content-MD5`、`Content-Type`、`Date`
- `PathAndParameters`：`Path + "?" + Key1 + "=" + Value1 + "&" + Key2 + "=" + Value2 + ... "&" + KeyN + "=" + ValueN`；「Query和Form参数对的Key按照字典排序后使用上面的方式拼接」；「Query和Form参数为空时，则直接使用Path，不需要添加」；「Query和Form存在数组参数时（Key相同，Value不同的参数），取第一个Value参与签名计算」

签名计算（逐字）：「将`stringToSign`使用UTF-8解码后得到Byte数组，然后使用加密算法对Byte数组进行加密，然后使用Base64算法进行编码，形成最终的签名。」算法 `HmacSHA256`。

客户端必须/可选传的 4 个头：
- `x-ca-key`：「取值APP Key。**必选**。」
- `x-ca-signature-method`：「签名算法。取值HmacSHA256或者HmacSHA1，可选，**默认值为HmacSHA256**。」
- `x-ca-signature-headers`：「所有签名头的Key的集合。使用英文逗号分隔，可选。」
- `x-ca-signature`：「签名。**必选**。」

服务端验签四步：「1. 从接收到的请求中提取关键数据，得到一个用来签名的字符串。2. 从接收到的请求中读取`key`，通过`key`查询到对应的`secret`。3. 使用加密算法和`secret`对关键数据签名串进行加密处理，得到签名。4. 从接收到的请求中读取客户端签名，对比服务器端签名和客户端签名的一致性。」

🔴 **官方排错机制（一线最有用）**：
> `[官方原文]`「网关签名校验失败时，会将服务端的签名串（StringToSign）放到HTTP Response的Header中返回到客户端，Key为：X-Ca-Error-Message，您只需要将本地计算的签名串（StringToSign）与服务端返回的签名串进行对比即可找到问题。如果服务端与客户端的StringToSign一致请检查用于签名计算的APP Secret是否正确。因为HTTP Header中无法表示换行，因此StringToSign中的换行符都被替换成`#`」

示例：`X-Ca-Error-Message:  Server StringToSign:`GET#application/json##application/json##X-Ca-Key:200000#X-Ca-Timestamp:1589458000000#/app/v1/config/keys?keys=TEST``

错误码：

| HTTP状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 400 | Invalid Signature. | 请求头x-ca-signature签名串，与服务端计算得到签名不一致。 |
| 400 | Invalid Content-MD5. | 请求头content-md5不正确。 |
| 400 | Invalid Date. | 根据请求头date计算时间偏移超过配置的date_offset。 |
| 401 | Invalid Key. | 请求头未提供x-ca-key，或者x-ca-key无效。 |
| 401 | Empty Signature. | 请求头未提供x-ca-signature签名串。 |
| 403 | Unauthorized Consumer. | 请求的调用方无访问权限。 |
| 413 | Request Body Too Large. | 请求Body超过限制大小：32MB。 |
| 413 | Payload Too Large. | 请求Body超过全局配置DownstreamConnectionBufferLimits，请在参数配置页调高此项。 |

> `[官方原文]`「注意谨慎调高`DownstreamConnectionBufferLimits`此参数配置，调高后网关内存使用将有显著增加。」

> `[原文如此]`：hmac-auth 页「全局配置认证和路由粒度进行鉴权」示例中，实例级 consumers 命名为 `consumer-1`/`consumer-2`（带连字符），而紧随其后的路由级 `allow: - consumer1`、域名级 `allow: - consumer2`（无连字符）——按此配置无人能通过鉴权。原文照录，不修正。

来源：`[官方｜hmac-auth-plug-ins]`

#### §9.4.7 jwt-auth 完整参数与错误码

认证配置：`consumers`(array of object,必填)、`global_auth`(array of string,选填（仅实例级别配置）,语义同 basic-auth)

`consumers[]` 全字段：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **name** | string | 必填 | - | 配置该consumer的名称。 |
| **jwks** | string | 选填。jwks和remote_jwks必填一个。 | - | JSON Web Key (JWK) 指定的JSON格式字符串，是由验证JWT中签名的公钥（或对称密钥）组成的JSON Web Key Set。 |
| **remote_jwks** | object | 选填。jwks和remote_jwks二选一。 | `{"uri":"http://127.0.0.1/keys","service":"test.static","port":"80","ttl":30000,"timeout":3000}` | 用于从指定服务的指定URI定时拉取JWKS，和JWKS字段同时配置时，以此字段配置拉取的JWKS优先。「建议remote_jwks返回的jwks大小控制在1Mb以内。如果超过之后报错，欢迎您加入钉群"88010006189"交流，或通过提工单联系支持同学。」 |
| **issuer** | string | 选填 | - | JWT的签发者，需要和payload中的iss字段保持一致。 |
| **claims** | object | 选填 | - | key/value分别对应payload中的key/value，可以用于校验多个字段是否和payload中一致，例如配置aud: mobile-site，则要求payload中的aud必须是mobile-site。 |
| **claims_to_headers** | array of object | 选填 | - | 抽取JWT的payload中指定字段，设置到指定的请求头中，然后转发给后端。 |
| **from_headers** | array of object | 选填 | `[{"name":"Authorization","value_prefix":"Bearer"}]` | 从指定的请求头中抽取JWT。 |
| **from_params** | array of string | 选填 | `access_token` | 从指定的URL参数中抽取JWT。 |
| **from_cookies** | array of string | 选填 | - | 从指定的cookie中抽取JWT。 |
| **clock_skew_seconds** | number | 选填 | 60 | 校验JWT的exp和iat字段时允许的时钟偏移量，单位为秒。 |
| **keep_token** | bool | 选填 | true | 转发给后端时是否保留JWT。 |

> `[官方原文]`「只有当`from_headers`，`from_params`，`from_cookies`均未配置时，才会使用默认值。」

`from_headers[]`：`name`(string,必填,「抽取JWT的请求Header。」)、`value_prefix`(string,必填,「对请求Header的value去除此前缀，剩余部分作为JWT。」)
`claims_to_headers[]`：`claim`(string,必填,「JWT payload中的指定字段，要求必须是字符串或无符号整数类型。」)、`header`(string,必填,「从payload取出字段的值设置到这个请求头中，转发给后端。」)、`override`(bool,选填,默认 `true`,「true时，存在同名请求头会进行覆盖。false时，追加同名请求头。」)
`remote_jwks`：

| 名称 | 数据类型（原文） | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **uri** | string | 必填 | - | 请求URL。 |
| **service** | string | 必填 | - | 「K8s服务填写示例：foo.default.svc.cluster.local。Nacos服务填写示例：foo.DEFAULT-GROUP.public.nacos。如果是名为test的DNS服务，则填写test.dns。如果是名为test的静态IP服务，则填写test.static。」 |
| **port** | bool | 必填 | - | 服务端口 |
| **timeout** | bool | 选填 | 3000 | 服务请求超时时间，单位是毫秒 |
| **ttl** | bool | 选填 | 30000 | 缓存时间，单位是毫秒。 |

> 🔴 `[官方矛盾]`：`remote_jwks` 的 `port`/`timeout`/`ttl` 三字段「数据类型」列均标 **bool**，但描述与默认值（`"80"`/`3000`/`30000`）显然是端口号与毫秒数。双方原文已摘，不裁决。

鉴权：`allow`(array of string,选填（非实例级别配置）)
关键语义：`[官方原文]`「如果一个JWT能匹配多个jwks，则按照配置顺序命中第一个匹配的consumer。」
`_disable_: true`（路由级）：「因为`_disable_`设置为`true`，当匹配到这个路由时，将关闭此插件功能，不进行JWT认证，所有人均可访问。」
官方给出两种"全局开、局部关"组合的完整示例：「网关实例级别开启，但特定路由关闭」（`global_auth: true` + route-b 配 `_disable_: true`）与「域名级别开启，但特定路由关闭」（实例级配 consumers + route-b 配 `_disable_: true` + `*.example.com` 配 `allow`）。
支持算法（由示例 jwks 可见）：`HS256`（`kty: oct`）与 `RS256`（`kty: RSA`）；算法白名单/是否支持 ES256 等 `[文档未说明]`。

错误码：

| HTTP状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | Jwt missing | 请求头未提供JWT。 |
| 401 | Jwt expired | JWT已经过期。 |
| 401 | Jwt verification fails | JWT payload校验失败，如iss不匹配。 |
| 403 | Access Denied | 无权限访问当前路由。 |

来源：`[官方｜jwt-auth-plug-ins]`

#### §9.4.8 jwt-logout 完整参数、Redis 容量口径与错误码

主配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| jwks | string | 选填 | - | 指定JSON字符串，用于验证JWT。当此插件搭配jwt-auth插件使用时，无需配置此项。 |
| clock_skew | number | 选填 | 60 | 校验JWT的exp和iat字段时，允许的时钟偏移量。单位为秒。 |
| token_header | string | 选填 | Authorization | 抽取JWT的请求Header。 |
| token_prefix | string | 选填 | "Bearer" | 将请求Header中Value值的指定前缀去除后，剩余部分将被用作JWT的内容。 |
| redis | Redis | **必填** | - | Redis服务配置信息。 |
| logout | Logout | 选填 | - | 用于实现JWT登出功能的配置。不配置此字段时，该功能关闭。 |
| login | Login | 选填 | - | 用于实现JWT唯一登录的配置。不配置此字段时，该功能关闭。 |

`redis`：`service`(string,**必填**,「Redis服务名称。例如：固定地址服务：my-redis.static。DNS域名服务：my-redis.dns。K8s容器服务：my-redis.default.svc.cluster.local。」)、`port`(number,**必填**)、`username`(string,选填)、`password`(string,选填,均为「Redis AUTH命令使用的」)、`timeout`(number,选填,默认 `1000`,「Redis命令的超时时间。单位为毫秒。」)

`logout`：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| key_prefix | string | 选填 | higress_jwt_logout_ | Redis中存储Key的前缀。 |
| key | array of string | 选填 | ["jti"] | 指定JWT Payload中的字段标识JWT，携带相同字段的会被认作同一个JWT；若JWT Payload中不存在相应字段，将返回401 invalid token。 |
| path | string | 选填 | /jwt_logout | URL路径后缀匹配此字符串时，登出当前请求携带的JWT，该JWT此后将无法使用。 |
| error_status | number | 选填 | 401 | 登出状态时的错误状态码。 |
| error_body | string | 选填 | '{"message":"invalid token"}' | 登出状态时的响应Body。 |
| ttl | number | 选填 | - | 在Redis中，存储Key的ttl，以秒为单位。此配置确定了登出的JWT在多长时间内无法使用。若未填写此配置，将根据Payload中的exp减去当前时间来计算生存时间；若Payload中没有exp字段，则默认的ttl为86400秒（24小时）。 |

`login`：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| key_prefix | string | 选填 | higress_jwt_logout_ | Redis中存储key的前缀。 |
| key | array of string | 选填 | ["iss","aud","sub"] | 指定JWT Payload中的字段作为唯一登录标识。若携带相同字段但与已登录的JWT不完全相同，将被判断为重复登录并拒绝访问，直到已登录的JWT对应的key在Redis中过期；若JWT Payload中不存在相应字段，将返回401 invalid token。 |
| path | string | 选填 | /jwt_login | URL路径后缀匹配此字符串时，强制登录当前请求携带的JWT，已登录的相同Payload特征的JWT将被登出。 |
| error_status | number | 选填 | 403 | 重复登录时的错误状态码。 |
| error_body | string | 选填 | '{"message":"already login on other device"}' | 重复登录时的响应Body。 |
| ttl | number | 选填 | - | 在Redis中存储key的ttl，单位为秒，决定唯一登录的JWT在多久时间内有效。若未填写此配置，则基于Payload中的exp减去当前时间计算。若Payload中未包含exp字段，则默认ttl为86400秒（24小时）。 |

> 🔴 `[官方矛盾]`（默认前缀 vs 页内示例）：`login.key_prefix` 的**默认值栏写 `higress_jwt_logout_`**，但同页「实现原理」与示例中的 Redis Key 全部是 **`higress_jwt_login_...`**（「此时Redis中将存在一个Key：`higress_jwt_login_iss#aud#sub##abcd#www.example.com#abcd`」）。双方原文已摘，不裁决。SA 若要手工操作 Redis 踢人，前缀必须以实测为准。

> 🔴 `[官方矛盾]`（页内示例自相矛盾）：login 示例的 Payload 为 `{"jti":"zzzz","iss":"abcd","aud":"www.example.com","sub":"test","iat":1665660527,"exp":1865673819}`，按 `key: ["iss","aud","sub"]` 拼出的 Value 应为 `abcd#www.example.com#test`，但原文写「此时Redis中将存在一个Key：`higress_jwt_login_iss#aud#sub##abcd#www.example.com#abcd`」——第三段是 `abcd` 而非 `test`。

Redis Key 拼接规则（逐字）：
> logout 小节：「Redis中存储键的拼接规则为：`<key_prefix><PayloadKey>##<PayloadValue>`，其中PayloadKey由多个键用#间隔拼接，PayloadValue由相应键对应的值用#间隔拼接。例如：`higress_jwt_logout_jti#iss##xxxxx#abcde`。」
> login 小节：「举例：`higress_jwt_login_iss#aud#sub##xxxxx#abcde#fffff`。」

🔴 **Redis 容量评估口径（官方唯一一句量化指引，逐字照抄）**：
> `[官方原文]`「开启logout和login配置。插件将处理1次请求，导致产生3次Redis读请求（1次logout检查，2次login检查）。在少量情况下（如登出或首次登录），将额外产生2次Redis写请求。为评估Redis容量，可以简单地按插件处理的请求吞吐量乘以2进行计算。」

阿里云 Redis 接入（有决策含义的步骤）：服务来源选 **DNS 域名**；服务端口填 Redis 端口（「一般为6379」）；域名列表填 VPC 内地址（例 `r-xxxxxxx.redis.rds.aliyuncs.com`）；**TLS 模式选择关闭**。插件配置：
```yaml
redis:
  service: redis.dns
  port: 6379
  password: ******   # 如果给Redis服务设置了密码
```

行为语义要点（逐字）：
- 「插件默认推荐的登出键是["jti"]，`jti`是用于唯一标识一个JWT的Payload字段。按照JWT标准要求，当`jti`相同时，整个JWT也是完全相同的，因此可用来标记JWT的登出状态。」
- 「本插件只能登出当前请求携带的Token，您也可以手动操作Redis来登出指定的Token，按照上述键拼接规则即可。当网关查询Redis发现该键存在时，即会拒绝相应JWT的访问。」
- 「Redis中键的过期时间默认值是基于JWT Payload的`exp`字段计算的，即默认存储到该JWT过期。」
- login：「插件默认推荐的login key是["iss","aud","sub"]，其中`iss`代表JWT的签发者，`aud`代表JWT的使用场景，`sub`代表JWT的签发对象。通常情况下，这三者的组合可以满足登录时互踢的场景。」
- 「在相同Payload特征的情况下，首个JWT会随业务请求自动写入Redis，从而实现插件的唯一登录功能。因此，不需要调用强制登录接口。只有在登录时需要进行互踢的情况下，才需要使用该接口。」
- 「就像同时开启了JWT logout功能一样，当触发logout逻辑时，也会清理Redis中当前JWT的login key。」
- 互踢判定：「和第一步中的JWT的Payload特征一致，但非特征字段`jti`不同，因此该JWT会被拒绝访问。」
- 成功响应体：登出返回 `{"message": "logout success"}`；强制登录返回 `{"message":"login success"}`

错误码：

| HTTP 状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | invalid token | 请求头未提供JWT、JWT格式错误或过期等原因。 |
| 500 | redis server error | 访问Redis超时或失败等原因。 |

> 🔴 **Redis 故障 = 500**，官方未提供「Redis 不可用时放行还是拒绝」的降级开关 → 降级策略 `[文档未说明]`。这是 jwt-logout 最大的可用性风险点（连带计费：需另购阿里云 Redis 实例，官方指引「创建Redis实例。具体操作，请参见Redis 快速入门」）。

来源：`[官方｜jwt-logout-plug-ins]`

#### §9.4.9 oauth（OAuth2认证）完整参数与错误码

认证配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **consumers** | array of object | 必填 | - | 配置服务的调用者，用于对请求进行认证。 |
| **issuer** | string | 选填 | Higress-Gateway | 用于填充JWT中的issuer。 |
| **auth_path** | string | 选填 | /oauth2/token | 指定路径后缀用于签发Token，路由级配置时，要确保能首先匹配对应的路由。在使用 API 管理时，需要创建相同路径的接口。 |
| **global_credentials** | bool | 选填 | true | 在通过 consumer 认证的前提下，允许任意路由签发的凭证访问。 |
| **auth_header_name** | string | 选填 | Authorization | 用于指定从哪个请求头获取JWT。 |
| **token_ttl** | number | 选填 | 7200 | Token从签发后多久内有效，单位为秒。 |
| **clock_skew_seconds** | number | 选填 | 60 | 校验JWT的exp和iat字段时允许的时钟偏移量，单位为秒。 |
| **keep_token** | bool | 选填 | true | 转发给后端时是否保留JWT。 |
| **global_auth** | array of string | 选填（仅实例级别配置） | - | 同 basic-auth |

`consumers[]`：`name`(string,必填)、`client_id`(string,必填,「OAuth2 client id。」)、`client_secret`(string,必填,「OAuth2 client secret。」)
鉴权：`allow`(array of string,选填（非实例级别配置）)

三条「重要」约束（逐字）：
> 「对于开启该配置的路由，如果路径后缀和`auth_path`匹配，则该路由不会被转发到原目标服务，而是用于生成Token。」
> 「如果关闭`global_credentials`，请确保启用此插件的路由不是精确匹配路由，此时若存在另一条前缀匹配路由，则可能导致预期外行为。」
> 「对于通过认证鉴权的请求，请求的header会被添加一个`X-Mse-Consumer`字段，用以标识调用者的名称。」

🔴 凭证作用域（关键选型点）：
> `[官方原文]`「此时虽然使用同一份配置，但`route-a` 下签发的凭证无法用于访问 `route-b`，反之亦然。」→ 路由级配置且未显式开启 `global_credentials` 时凭证**按路由隔离**；要跨路由共享须显式写 `global_credentials: true`。

授权模式：**仅 Client Credential** 有官方示例（小节标题「使用 Client Credential 授权模式」）；授权码/隐式/密码模式是否支持 → `[文档未说明]`。

取 Token 的两种方式（官方注明推荐 GET，逐字）：
```bash
# 通过 GET 方法获取（推荐）
curl 'http://test.com/oauth2/token?grant_type=client_credentials&client_id=12345678-xxxx-...&client_secret=abcdefgh-xxxx-...'

# 通过 POST 方法获取（需要先匹配到有真实目标服务的路由，否则网关不会读取请求 Body）
curl 'http://test.com/oauth2/token' -H 'content-type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials&client_id=12345678-xxxx-...&client_secret=abcdefgh-xxxx-...'
```
返回体：`{"token_type":"bearer","access_token":"eyJ...","expires_in":7200}`（`expires_in` 与 `token_ttl` 默认值一致）。
示例 token 头解码为 `{"alg":"HS256","typ":"application/at+jwt"}`，payload 含 `aud: default`、`client_id`、`exp`、`iat`、`iss: Higress-Gateway`、`jti`、`sub: consumer1`。

错误码：

| HTTP状态码 | 出错信息 | 原因说明 |
|---|---|---|
| 401 | Invalid Jwt token. | 请求头未提供JWT、JWT格式错误或过期等原因。 |
| 403 | Access Denied. | 无权限访问当前路由。 |

> `[原文如此]`：oauth 页「全局配置认证和路由粒度进行鉴权」小节正文写「以下配置将对网关特定路由或域名开启 **Jwt Auth** 认证和鉴权，注意如果一个JWT能匹配多个`jwks`，则按照配置顺序命中第一个匹配的`consumer`。」——但 oauth 插件的配置字段里**没有 `jwks`**，疑为从 jwt-auth 页复制残留。

来源：`[官方｜oauth-plugin]`

---

### §9.5 流量与安全类插件

#### §9.5.1 🔴 限流类插件的计量维度差异（本章重点）

| 维度 | `key-rate-limit`（基于Key限流） | `cluster-key-rate-limit`（基于Key集群限流） | AI Token 限流 / 消费者配额 |
|---|---|---|---|
| 来源 slug | `key-rate-limit-plugin` | `throttle-based-on-cluster-keys` | 不在 W6 清单 → `[文档未说明]`（总表名为 `ai-token-ratelimit` 默认阶段/600、`ai-quota` 默认阶段/750，归 W3 §5） |
| 计量对象 | **请求次数** | **请求次数** | 由名称可知与 Token 相关，参数 `[文档未说明]` |
| 计数底座 | `[文档未说明]`（页面无 redis 字段，也无「集群/单机」表述） | 🔴 **Redis**（`redis` 必填），「基于 Redis 实现集群限流，适用于需要跨多个 Higress Gateway 实例实现全局一致速率限制的场景」 | `[文档未说明]` |
| 执行阶段/优先级 | 默认阶段 / **10**（总表「基于Key限流」；插件页无「运行属性」） | 默认阶段 / **20**（页内「运行属性」与总表「基于Key集群限流」两处一致） | 默认阶段 / 600、750 |
| 支持的 `limit_by_*` 维度 | **2 种**：`limit_by_header`（HTTP 请求头名）、`limit_by_param`（URL 参数名）。「limit_by_header、limit_by_param中选填一项。」 | **9 种**：`limit_by_header`、`limit_by_param`、`limit_by_consumer`（「根据 consumer 名称进行限流，无需添加实际值」）、`limit_by_cookie`（「Cookie中 key 名称」）、`limit_by_per_header`、`limit_by_per_param`、`limit_by_per_consumer`、`limit_by_per_cookie`、`limit_by_per_ip`。「`limit_by_*` 中选填一项」 | `[文档未说明]` |
| 按 IP 限流 | ❌ 无 | ✅ `limit_by_per_ip`：「从请求头获取，以 `from-header-对应的header名`，示例：`from-header-x-forwarded-for`，直接获取对端 socket ip，配置为 `from-remote-addr`」；`limit_keys.key`「支持配置 IP 地址或 IP 段」 | `[文档未说明]` |
| 按 consumer 限流 | ❌ 无 | ✅ `limit_by_consumer` / `limit_by_per_consumer` | `[文档未说明]` |
| 按 Cookie 限流 | ❌ 无 | ✅ `limit_by_cookie` / `limit_by_per_cookie` | `[文档未说明]` |
| 正则/通配 | ❌ 无（`key` 仅「匹配的键值」） | ✅ 「`limit_by_per_header`,`limit_by_per_param`,`limit_by_per_consumer`,`limit_by_per_cookie` 类型支持配置正则表达式（以regexp：开头后面跟正则表达式）或者\*（代表所有），正则表达式示例：`regexp:^d.*`（以d开头的所有字符串）」 | `[文档未说明]` |
| 时间粒度 | `query_per_second`／`query_per_minute`／`query_per_hour`／`query_per_day`，number，「选填一项」，均无默认值 | 同左，int，「选填一项」，均无默认值 | `[文档未说明]` |
| 多规则语义 | `[文档未说明]`（页面无 rule_items 概念，只有单个 `limit_keys` 列表） | 「按照 rule_items 下的排列顺序，匹配第一个 rule_item 后命中限流规则，后续规则将被忽略」 | `[文档未说明]` |
| 拒绝响应可配 | ❌ 页面无 `rejected_code`/`rejected_msg` → `[文档未说明]` | ✅ `rejected_code` 默认 `429`；`rejected_msg` 默认 `Too many requests` | `[文档未说明]` |
| 额度回传响应头 | `[文档未说明]` | ✅ `show_limit_quota_header`(bool) 默认 `false`：「响应头中是否显示 `X-RateLimit-Limit`（限制的总请求数）和 `X-RateLimit-Remaining`（剩余还可以发送的请求数）」 | `[文档未说明]` |
| 规则名 | `[文档未说明]` | `rule_name`(必填)：「限流规则名称，根据限流规则名称 + 限流类型 + 限流 key 名称 + 限流 key 对应的实际值来拼装 redis key」 | `[文档未说明]` |

**选型判据（`[推断]`，推理链）**：需要跨多网关实例的全局一致速率 ⇒ 必须用 `cluster-key-rate-limit`（唯一有 Redis 集群计数底座的）；只需按 header/param 做简单区别限流且不引入 Redis ⇒ `key-rate-limit`；需按 IP／consumer／Cookie／正则分桶 ⇒ 只能 `cluster-key-rate-limit`。

**官方 FAQ（限流不生效的唯一排障口径，逐字）**：
> `[官方原文]`「### cluster-key-rate-limit插件配置后限流不生效？ 检查 `redis.service_name` 字段，应填写带服务类型的完整 FQDN 名称（如 `redis.dns`、`redis.my-ns.svc.cluster.local`），而非直接填写 Redis 连接地址。需先将 Redis 通过 DNS 域名方式添加到网关服务中，再填入服务名称。」`[官方｜throttle-based-on-cluster-keys]`

**cluster-key-rate-limit 完整参数表**

主配置：

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| rule_name | string | 是 | - | 限流规则名称，根据限流规则名称 + 限流类型 + 限流 key 名称 + 限流 key 对应的实际值来拼装 redis key |
| rule_items | array of object | 是 | - | 限流规则项，按照 rule_items 下的排列顺序，匹配第一个 rule_item 后命中限流规则，后续规则将被忽略 |
| show_limit_quota_header | bool | 否 | false | 响应头中是否显示 `X-RateLimit-Limit`（限制的总请求数）和 `X-RateLimit-Remaining`（剩余还可以发送的请求数） |
| rejected_code | int | 否 | 429 | 请求被限流时，返回的 HTTP 状态码 |
| rejected_msg | string | 否 | Too many requests | 请求被限流时，返回的响应体 |
| redis | object | 是 | - | redis 相关配置 |

`rule_items[]`：

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| limit_by_header | string | 否，`limit_by_*` 中选填一项 | - | 配置获取限流键值的来源 HTTP 请求头名称 |
| limit_by_param | string | 否，`limit_by_*` 中选填一项 | - | 配置获取限流键值的来源 URL 参数名称 |
| limit_by_consumer | string | 否，`limit_by_*` 中选填一项 | - | 根据 consumer 名称进行限流，无需添加实际值 |
| limit_by_cookie | string | 否，`limit_by_*` 中选填一项 | - | 配置获取限流键值的来源 Cookie中 key 名称 |
| limit_by_per_header | string | 否，`limit_by_*` 中选填一项 | - | 按规则匹配特定 HTTP 请求头，并对每个请求头分别计算限流，配置获取限流键值的来源 HTTP 请求头名称，配置 `limit_keys` 时支持正则表达式或 `*` |
| limit_by_per_param | string | 否，`limit_by_*` 中选填一项 | - | 按规则匹配特定 URL 参数，并对每个参数分别计算限流，配置获取限流键值的来源 URL 参数名称，配置 `limit_keys` 时支持正则表达式或 `*` |
| limit_by_per_consumer | string | 否，`limit_by_*` 中选填一项 | - | 按规则匹配特定 consumer，并对每个 consumer 分别计算限流，根据 consumer 名称进行限流，无需添加实际值，配置 `limit_keys` 时支持正则表达式或 `*` |
| limit_by_per_cookie | string | 否，`limit_by_*` 中选填一项 | - | 按规则匹配特定 Cookie，并对每个 Cookie 分别计算限流，配置获取限流键值的来源 Cookie中 key 名称，配置 `limit_keys` 时支持正则表达式或 `*` |
| limit_by_per_ip | string | 否，`limit_by_*` 中选填一项 | - | 按规则匹配特定 IP，并对每个 IP 分别计算限流，配置获取限流键值的来源 IP 参数名称，从请求头获取，以 `from-header-对应的header名`，示例：`from-header-x-forwarded-for`，直接获取对端 socket ip，配置为 `from-remote-addr` |
| limit_keys | array of object | 是 | - | 配置匹配键值后的限流次数 |

`limit_keys[]`：

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| key | string | 是 | - | 匹配的键值，`limit_by_per_header`,`limit_by_per_param`,`limit_by_per_consumer`,`limit_by_per_cookie` 类型支持配置正则表达式（以regexp：开头后面跟正则表达式）或者\*（代表所有），正则表达式示例：`regexp:^d.*`（以d开头的所有字符串）；`limit_by_per_ip`支持配置 IP 地址或 IP 段 |
| query_per_second | int | 否，四者中选填一项 | - | 允许每秒请求次数 |
| query_per_minute | int | 否，四者中选填一项 | - | 允许每分钟请求次数 |
| query_per_hour | int | 否，四者中选填一项 | - | 允许每小时请求次数 |
| query_per_day | int | 否，四者中选填一项 | - | 允许每天请求次数 |

`redis`：

| 配置项 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| service_name | string | 必填 | - | redis 服务名称，带服务类型的完整 FQDN 名称，例如 my-redis.dns、redis.my-ns.svc.cluster.local |
| service_port | int | 否 | 服务类型为固定地址（static service）默认值为80，其他为6379 | 输入Redis服务的服务端口 |
| username | string | 否 | - | redis 用户名 |
| password | string | 否 | - | redis 密码 |
| timeout | int | 否 | 1000 | redis 连接超时时间，单位毫秒 |

来源：`[官方｜throttle-based-on-cluster-keys]`

按 IP 限流的官方示例（体现精确 IP / IP 段 / 兜底三层写法，逐字）：
```yaml
rule_name: default_rule
rule_items:
- limit_by_per_ip: from-header-x-forwarded-for
  limit_keys:
  - key: 1.1.1.1        # 精确 IP
    query_per_day: 10
  - key: 1.1.1.0/24     # IP 段，符合这个 IP 段的 IP，每个 IP 100qpd
    query_per_day: 100
  - key: 0.0.0.0/0      # 兜底用，即默认每个 IP 1000 qpd
    query_per_day: 1000
redis:
  service_name: redis.static
show_limit_quota_header: true
```

`key-rate-limit` 完整参数表：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **limit_by_header** | string | 选填。limit_by_header、limit_by_param中选填一项。 | - | 配置获取限流键值的来源HTTP请求头名称。 |
| **limit_by_param** | string | 选填。limit_by_header、limit_by_param中选填一项。 | - | 配置获取限流键值的来源URL参数名称。 |
| **limit_keys** | array of object | 必填。 | - | 配置匹配键值后的限流次数。 |

`limit_keys[]`：`key`(string,必填,「匹配的键值。」)、`query_per_second`／`query_per_minute`／`query_per_hour`／`query_per_day`(number,「query_per_second、query_per_minute、query_per_hour或query_per_day中选填一项。」,默认值均为 `-`)
来源：`[官方｜key-rate-limit-plugin]`

#### §9.5.2 🔴 灰度类插件的分流判据（三个插件三种判据，不可混用）

| 插件 | 分流判据 | 幂等性 | 是否改写路由 | 典型场景 | 来源 slug |
|---|---|---|---|---|---|
| **traffic-tag** | ① **内容判据** `conditionGroups`：按 `header`/`parameter`/`cookie` + 7 种 `operator` 组合，组内 `logic` 为 `and`/`or`；② **权重判据** `weightGroups`：按 `weight` 百分比随机；③ **`percentage` 操作符**：`hash(get(key)) % 100 < value` | `percentage` **幂等**（「对于一个相同的键值对，多次匹配的结果是幂等的，即这一次命中条件，下一次也会命中」）；`weight` **不幂等**（「由于没有指定固定的对比依据而是基于随机权重分布，同一个请求的多次匹配可能匹配多个结果」） | 否，只**添加请求头** | 给流量打染色标签供下游/路由消费 | `the-traffic-tag-plugin` |
| **canary-header** | 仅**权重判据**：`weighted_headers[].weight`（百分比） | 不幂等（随机） | 🔴 **是**：「请求添加header后会重新匹配路由」 | 「可实现基于比例的灰度路由，而无需客户端主动携带灰度header」 | `canary-header-plugin` |
| **frontend-gray** | ① **用户 ID 白名单**：`grayKey`（Cookie 或 Header 中取）+ `rules[].grayKeyValue`；② **用户标签**：`rules[].grayTagKey`/`grayTagValue`（来自 Cookie）；③ **JSON 内嵌字段**：`grayKey` + `graySubKey`；④ **比例**：`grayDeployments[].weight` | 白名单/标签判据幂等；`weight` 比例判据靠 `uniqueGrayTag` 实现黏贴：「开启按照比例灰度时候，网关会生成一个唯一标识存在`cookie`中，一方面用于session黏贴，另一方面后端也可以使用这个值用于全链路的灰度串联」（默认 `x-higress-uid`） | 否，改写**前端资源版本/入口**（`{version}` 替换 + `rewrite.indexRouting`/`fileRouting` 前缀重写） | 「业务`A/B实验`」+「`可灰度`配合`可监控`、`可回滚`策略保证系统发布运维稳定性」 | `front-end-grayscale-plug-in` |

**`percentage` vs `weight` 官方原文辨析（逐字，选型必考）**：
> `[官方原文]`「`percentage`操作符：用于条件表达式中，基于指定的百分比和指定的键值对来判断是否执行某个操作。对于一个相同的键值对，多次匹配的结果是幂等的，即这一次命中条件，下一次也会命中。」
> 「`weight`字段：用于定义不同处理路径的流量权重。在基于权重的流量标记中，`weight`确定了某个路径应接收的流量比例。与`percentage`不同的是，由于没有指定固定的对比依据而是基于随机权重分布，同一个请求的多次匹配可能匹配多个结果。」
> 「使用`percentage`进行条件匹配时，判断每个请求是否满足特定百分比条件；而`weight`则是静态随机分配整体流量的比例。」`[官方｜the-traffic-tag-plugin]`

#### §9.5.3 traffic-tag 完整参数

主配置：

| 字段名称 | 类型 | 默认值 | 是否必填 | 描述 |
|---|---|---|---|---|
| `conditionGroups` | array of object | - | 否 | 定义基于内容的标记条件组，详细结构见条件组配置。 |
| `weightGroups` | array of object | - | 否 | 定义基于权重的标记条件组，详细结构见权重组配置。 |
| `defaultTagKey` | string | - | 否 | 默认的标记键名，当未匹配到任何条件时使用。当且仅当同时配置了defaultTagVal时生效 |
| `defaultTagVal` | string | - | 否 | 默认的标记值，当未匹配到任何条件时使用。当且仅当同时配置了defaultTagKey时生效 |

`conditionGroups[]`：`headerName`(string,是,「要添加或修改的 HTTP 头名称。»)、`headerValue`(string,是,「HTTP 头的值。」)、`logic`(string,是,「条件组中的逻辑关系，支持 `and`、`or`，必须为小写字母。»)、`conditions`(array of object,是)
`conditions[]`：`conditionType`(string,是,「条件类型，支持 `header`、`parameter`、`cookie`。」)、`key`(string,是,「条件的关键字。」)、`operator`(string,是,「操作符，支持 `equal`、`not_equal`、`prefix`、`in`、`not_in`、`regex`、`percentage`。」)、`value`(array of string,是,「条件的值，仅当操作符为 `in` 和 `not_in` 时支持配置多个值。」)
`weightGroups[]`：`headerName`(是)、`headerValue`(是)、`weight`(integer,是,「流量权重百分比。」)

操作符语义（逐字）：

| 操作符 | 描述 |
|---|---|
| `equal` | 精确匹配，值需要完全相等 |
| `not_equal` | 不等匹配，值不相等时满足条件 |
| `prefix` | 前缀匹配，指定值是实际值的前缀时满足条件 |
| `in` | 包含匹配，实际值需要在指定的列表中 |
| `not_in` | 排除匹配，实际值不在指定的列表中时满足条件 |
| `regex` | 正则表达式匹配，按照正则表达式规则匹配 |
| `percentage` | 百分比匹配，原理：`hash(get(key)) % 100 < value` 成立时满足条件 |

> 「当 `operator` 为 `regex` 时，使用的正则表达式引擎是 RE2。」

权重语义（官方示例明示）：「权重总和为100，下例中未配置的40权重将不添加header」——即 `weight: 30` + `weight: 30` ⇒ 「30%几率被添加请求头`x-mse-tag: gray`，30%几率被添加请求头`x-mse-tag: blue`，40%几率不添加请求头」。
来源：`[官方｜the-traffic-tag-plugin]`

#### §9.5.4 canary-header 完整参数

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| `weighted_headers` | array of object | 必填 | - | 配置要添加的header以及其对应的权重。 |

`weighted_headers[]`：`added_key`(string,必填,「要添加的header key。」)、`added_value`(string,必填,「要添加的header value。」)、`weight`(number,必填,「要添加的header所对应的权重，单位为百分比，所有header的权重之和不能大于100。」)
> `[官方原文]`「若路由权重之和不大于100，则不足100的部分代表不会添加任何header的概率。」

🔴 灰度路由的完整机制（官方原话）：「添加header后，请求将会重新匹配路由。例如，此时有一个路由`route-a-gray`，该路由的匹配规则中有一项按header匹配的规则，该规则匹配了`x-higress-canary:gray`。这样将会有30%的请求将会匹配到`route-a-gray`，从而实现了按比例灰度的功能。」
→ `[推断]` 使用本插件**必须配套建一条按 header 匹配的灰度路由**，否则加了 header 也不产生分流效果。官方未说明"重新匹配路由"的额外开销 → `[文档未说明]`。
来源：`[官方｜canary-header-plugin]`

#### §9.5.5 frontend-gray 完整参数

主配置：

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| `grayKey` | string | 非必填 | - | 用户ID的唯一标识，可以来自Cookie或者Header中，比如 userid，如果没有填写则使用`rules[].grayTagKey`和`rules[].grayTagValue`过滤灰度规则 |
| `useManifestAsEntry` | boolean | 非必填 | `false` | 是否使用manifest作为入口。当设置为true时，系统将使用manifest文件作为应用入口，适用于微前端架构。在这种模式下，系统会根据manifest文件的内容来加载不同版本的前端资源。 |
| `localStorageGrayKey` | string | 非必填 | - | 使用JWT鉴权方式，用户ID的唯一标识来自`localStorage`中，如果配置了当前参数，则`grayKey`失效 |
| `graySubKey` | string | 非必填 | - | 用户身份信息可能以JSON形式透出，比如：`userInfo:{ userCode:"001" }`,当前例子`graySubKey`取值为`userCode` |
| `storeMaxAge` | int | 非必填 | `60 * 60 * 24 * 365` | 网关设置Cookie最大存储时长：单位为秒，默认为1年 |
| `cookieDomain` | string | 非必填 | - | Cookie的Domain设置，可用于跨子域共享Cookie。例如：".example.com" |
| `indexPaths` | array of strings | 非必填 | - | 强制处理的路径，支持 `Glob` 模式匹配。例如：在微前端场景下，XHR 接口如：`/resource/**/manifest-main.json`本质是一个资源请求，需要走插件转发逻辑。 |
| `skippedPaths` | array of strings | 非必填 | - | 用于排除特定路径，避免当前插件处理这些请求，支持 `Glob` 模式匹配。例如，在 rewrite 场景下，XHR 接口请求 `/api/**` 如果经过插件转发逻辑，可能会导致非预期的结果。 |
| `skippedByHeaders` | map of string to string | 非必填 | - | 用于通过请求头过滤，指定哪些请求不被当前插件处理。`skippedPaths` 的优先级高于当前配置，且页面HTML请求不受本配置的影响。 |
| `rules` | array of object | **必填** | - | 用户定义不同的灰度规则，适配不同的灰度场景 |
| `rewrite` | object | 非必填 | - | 重写配置，一般用于OSS/CDN前端部署的重写配置 |
| `baseDeployment` | object | 非必填 | - | 配置Base基线规则的配置 |
| `grayDeployments` | array of object | 非必填 | - | 配置Gray灰度的生效规则，以及生效版本 |
| `backendGrayTag` | string | 非必填 | `x-mse-tag` | 后端灰度版本Tag，如果配置了，cookie中将携带值为`${backendGrayTag}:${grayDeployments[].backendVersion}` |
| `uniqueGrayTag` | string | 非必填 | `x-higress-uid` | 开启按照比例灰度时候，网关会生成一个唯一标识存在`cookie`中，一方面用于session黏贴，另一方面后端也可以使用这个值用于全链路的灰度串联 |
| `injection` | object | 非必填 | - | 往首页HTML中注入全局信息，比如`<script>window.global = {...}</script>` |

`rules[]`：`name`(string,**必填**,「规则名称唯一标识，和`deploy.gray[].name`进行关联生效」)、`grayKeyValue`(array of string,非必填,「用户ID 白名单列表」)、`grayTagKey`(string,非必填,「用户分类打标的标签key值，来自Cookie」)、`grayTagValue`(array of string,非必填,「用户分类打标的标签value值，来自Cookie」)

`rewrite`：`host`(string,非必填,「host地址，如果是OSS则设置为 VPC 内网访问地址。」)、`indexRouting`(map of string to string,非必填,「用于定义首页重写路由规则。每个键 (Key) 表示首页的路由路径，值 (Value) 则指向重定向的目标文件。例如，键为 `/app1` 对应的值为 `/mfe/app1/{version}/index.html`。生效version为`0.0.1`，访问路径为 `/app1`，则重定向到 `/mfe/app1/0.0.1/index.html`。」)、`fileRouting`(map of string to string,非必填,「用于定义资源文件重写路由规则…键为 `/app1/` 对应的值为 `/mfe/app1/{version}`。生效version为`0.0.1`，访问路径为`/app1/js/a.js`，则重定向到`/mfe/app1/0.0.1/js/a.js`。」)
> 「`indexRouting`首页重写和`fileRouting`文件重写，本质都是前缀匹配」；「`{version}` 作为保留字段，在执行过程中会被`baseDeployment.version`或者`grayDeployments[].version`动态替换前端版本。」
> 示例中还出现 `rewrite.notFoundUri: /mfe/app1/dev/404.html`，但**参数表未收录该字段** → 文档缺口。

`baseDeployment`：`version`(string,**必填**,「Base版本的版本号，作为兜底的版本」)、`backendVersion`(string,非必填,「后端灰度版本，配合`key`为`${backendGrayTag}`，写入cookie中」)、`versionPredicates`(string,非必填,「和`version`含义相同，但是满足多版本的需求：根据不同路由映射不同的`Version`版本。一般用于微前端的场景：一个主应用需要管理多个微应用」)

`grayDeployments[]`：`version`(string,**必填**,「Gray版本的版本号，如果命中灰度规则，则使用此版本。如果是非CDN部署，在header添加`x-higress-tag`」)、`versionPredicates`(string,非必填,同 baseDeployment)、`backendVersion`(string,非必填,「后端灰度版本，会在`XHR/Fetch`请求的header头添加 `x-mse-tag` 到后端」)、`name`(string,**必填**,「规则名称和`rules[].name`关联」)、`enabled`(boolean,非必填,「是否启动当前灰度规则」)、`weight`(int,非必填,「按照比例灰度，比如50。」)

`injection`：可在 `head` 标签注入代码，也可在 `body` 标签的 `first` 和 `last` 位置注入代码（示例为 `<script>console.log(...)</script>` 数组）。

按用户灰度示例（逐字）与命中条件（官方明示）：
```yaml
grayKey: userid
rules:
- name: inner-user
  grayKeyValue: ['00000001','00000005']
- name: beta-user
  grayKeyValue: ['00000002','00000003']
  grayTagKey: level
  grayTagValue: [level3, level5]
baseDeployment:
  version: base
grayDeployments:
  - name: beta-user
    version: gray
    enabled: true
```
命中 `version: gray` 的条件（官方原话）：「cookie中`userid`等于`00000002`或者`00000003`」或「cookie中`level`等于`level3`或者`level5`的用户」；否则用 `version: base`。
按比例灰度：`grayDeployments[].weight: 80` ⇒ 「总的灰度规则为100%，其中灰度版本的权重为80%，基线版本为20%。」
🔴 用户信息存 LocalStorage 时的官方口径：「由于网关插件需要识别用户为唯一身份信息，HTTP协议进行信息传输，只能在Header中传递。如果用户信息存储在LocalStorage，在首页注入一段脚本将LocalStorage中的用户信息设置到cookie中。」——脚本需客户自行注入（官方给了 IIFE 示例，含 `window.location.reload()`）。
`fileRouting` 生效示例（逐字）：`/js/a.js` => `/mfe/app1/v1.0.0/js/a.js`；`/js/template/a.js` => `/mfe/app1/v1.0.0/js/template/a.js`；`/app1/js/a.js` => `/mfe/app1/v1.0.0/js/a.js`；`/app1/js/template/a.js` => `/mfe/app1/v1.0.0/js/template/a.js`
`indexRouting` 生效示例：「访问 `/app1`, `/app123`,`/app1/index.html`, `/app1/xxx`, `/xxxx` 都会路由到/mfe/app1/{version}/index.html」

> 🔴 `[官方矛盾]`（优先级）：本页「运行属性」写「插件执行阶段：`认证阶段` 插件执行优先级：**`1000`**」，而 `upload-plug-in` 总表写「前端灰度｜插件｜认证阶段｜**`450`**｜传输协议系列插件」。双方原文已摘，不裁决。**这会改变 frontend-gray 与 http-real-ip(980) 的先后顺序**（1000 则在 http-real-ip 之前，450 则在其之后），直接影响"前端灰度能否拿到真实客户端 IP"，属实质性冲突。

来源：`[官方｜front-end-grayscale-plug-in｜upload-plug-in]`

#### §9.5.6 安全防护类：request-block / waf / bot-detect

**request-block**

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **block_urls** | array of string | 选填。block_urls，block_headers，block_bodys中至少必填一项。 | - | 配置用于匹配需要屏蔽URL的字符串。 |
| **block_headers** | array of string | 选填。block_urls，block_headers，block_bodys中至少必填一项。 | - | 配置用于匹配需要屏蔽请求Header的字符串。 |
| **block_bodys** | array of string | 选填。block_urls，block_headers，block_bodys中至少必填一项。 | - | 配置用于匹配需要屏蔽请求Body的字符串。 |
| **blocked_code** | number | 选填。 | 403 | 配置请求被屏蔽时返回的HTTP状态码。 |
| **blocked_message** | string | 选填。 | - | 配置请求被屏蔽时返回的HTTP应答Body。 |
| **case_sensitive** | bool | 选填。 | true | 配置匹配时是否区分大小写。默认区分。 |

🔴 Body 大小双重限制（逐字）：
> 「当配置了`block_bodys`时，仅支持小于32MB的请求Body进行匹配。若请求Body大于此限制，并且不存在匹配到的`block_urls`和`block_headers`项时，不会对该请求执行屏蔽操作。」
> 「当配置了`block_bodys`时，若请求Body超过全局配置DownstreamConnectionBufferLimits，将返回`413 Payload Too Large`, 请在参数配置页调高此项。注意调高此参数配置后，网关内存使用将有显著增加。」
→ **设计行为而非 bug**：Body > 32MB 时 body 规则静默失效（放行）。`DownstreamConnectionBufferLimits` 的默认值与可调上限 `[文档未说明]`（属引擎参数，归 W1）。
匹配语义示例：`block_headers: [example-key, example-value]` 会同时命中「header 名等于 example-key」与「header 值等于 example-value」两种请求（官方给了 `-H 'example-key: 123'` 与 `-H 'my-header: example-value'` 两个都被禁的例子）。
来源：`[官方｜request-block-plugin]`

**waf**

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **useCRS** | bool | 选填。 | false | 是否开启OWASP CRS，详情可参考coreruleset（v3.3.2）。 |
| **secRules** | array of string | 选填。 | - | 用户自定义的waf防护规则，语法规则可参考ModSecurity中文手册。 |

🔴 能力边界（逐字，客户最常误解处）：
> `[官方原文]`「该插件基于开源ModSecurity规则，默认规则为静态规则，不具备识别最新的安全风险并实时更新规则集的能力，如需获取更强大的安全防护能力，请参见开启WAF防护。」
→ 即：插件版 waf ≠ 阿里云 WAF 产品；OWASP CRS 版本官方链接指向 **v3.3.2**。
两种运行模式：拦截（`useCRS: true`）／仅观测不拦截（`useCRS: true` + `secRules: - "SecRuleEngine DetectionOnly"`）。
自定义规则示例（逐字）：`- "SecRule REQUEST_URI \"@streq /admin\" \"id:101,phase:1,t:lowercase,deny\""`、`- "SecRule REQUEST_BODY \"@rx maliciouspayload\" \"id:102,phase:2,t:lowercase,deny\""`
路由级 vs 域名级覆盖示例：route-1 配 `SecAction "id:102,phase:1,deny"`，域名配 `SecAction "id:102,phase:1,pass"`。
被拦截时返回的状态码 `[文档未说明]`（页面无错误码表）。
来源：`[官方｜waf-plugin]`

**bot-detect**

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **allow** | array of string | 选填。 | - | 配置匹配User-Agent请求头的正则表达式，匹配命中时将允许其访问。 |
| **deny** | array of string | 选填。 | - | 配置匹配User-Agent请求头的正则表达式，匹配命中时将屏蔽请求。 |
| **blocked_code** | number | 选填。 | 403 | 配置请求被屏蔽时返回的HTTP状态码。 |
| **blocked_message** | string | 选填。 | - | 配置请求被屏蔽时返回的HTTP应答Body。 |

> `[官方原文]`「`allow`和`deny`字段可以均不配置，则执行默认的爬虫判断逻辑，通过配置`allow`字段可以将原本命中默认爬虫判断逻辑的请求放行，通过配置`deny`字段可以增加额外的爬虫判断逻辑。」

🔴 **默认规则会误伤 Go 客户端**（逐字）：「若不做该配置，默认的Golang网络库请求会被视作爬虫，被禁止访问。」官方放行写法 `allow: - ".*Go-http-client.*"`。
→ SA 避坑：客户用 Go SDK/自建服务调 AI 网关时若装了 bot-detect 且未配 allow，会被 403。
内置默认爬虫规则的具体清单 `[文档未说明]`。路由级可「做空配置保存」以套用内置默认规则。
来源：`[官方｜bot-detect-plug-ins]`

#### §9.5.7 协议与响应类：custom-response / degraphql / cache-control / hsts / http-real-ip / geo-ip / param-access-control

**custom-response**（插件类型：传输协议）

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| status_code | number | 选填。 | 200 | 自定义HTTP应答状态码。 |
| headers | array of string | 选填。 | - | 自定义HTTP应答头，Key和 Value 用`=`分隔。 |
| body | string | 选填。 | - | 自定义HTTP应答Body。 |
| enable_on_status | array of number | 选填。 | - | 匹配原始状态码，生成自定义响应，不填写时，不判断原始状态码。 |

两个官方场景（YAML 精简，逐字要点）：
- Mock 应答：`status_code: 200` + `headers: [Content-Type=application/json, Hello=World]` + `body: "{\"hello\":\"world\"}"` ⇒ 返回 200，`Content-Length: 17`
- 🔴 限流兜底（SA 常被客户问"限流后能不能跳转到友好页"）：`enable_on_status: [429]` + `status_code: 302` + `headers: [Location=https://example.com]` ⇒ 「触发网关限流时一般会返回429状态码」时改为 302，「从而实现基于浏览器302重定向机制，将限流后的用户引导到其他页面，比如可以是一个CDN上的静态页面」。若不想跳转，「参考Mock应答场景配置相应的字段即可」（官方另给 `status_code: 200` + `body: "{\"errmsg\": \"rate limited\"}"` 的域名级示例）。
来源：`[官方｜custom-response-plugin]`

**de-graphql**（认证阶段/430）

| 参数 | 描述 | 默认（原文栏位） |
|---|---|---|
| `gql` | graphql 查询 | 不能为空 |
| `endpoint` | graphql 查询端点 | `/graphql` |
| `timeout` | 查询连接超时，单位毫秒 | `5000` |
| `domain` | 服务域名，当服务来源是DNS配置 | （原文空） |

> 该表**只有 3 列**，无「数据类型」「填写要求」列 ⇒ `gql`/`domain` 的类型与必填性 `[文档未说明]`。
能力：「通过将URIs映射到GraphQL查询，从而可以将GraphQL上游转换为传统服务进行访问。」官方示例把 GitHub GraphQL API 包装成 REST：`curl "http://localhost/api?owner=alibaba&name=higress"` ⇒ 返回 `{"data":{"repository":{...}}}`。
页内配置示例是**开源 Higress 的 K8s 形态**（`McpBridge` + `Ingress` 注解 `higress.io/destination: github.dns`、`higress.io/upstream-vhost`、`higress.io/backend-protocol: HTTPS` + `WasmPlugin` CRD `matchRules.ingress`），**不是 AI 网关控制台形态**；AI 网关控制台里如何填 `domain` → `[文档未说明]`。
页内约 60% 篇幅是 GraphQL 通识科普（端点、POST 请求体三字段 query/variables/operationName、基本类型 String/Int/Float/Boolean、`!` 表示非空）——按契约 §1 属 P3，已丢弃，仅保留与配置相关的结论。
来源：`[官方｜degraphql-plugin]`

**cache-control（浏览器缓存控制）**（认证阶段/420）

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| suffix | string | 选填，表示匹配的文件后缀名，例如 `jpg`、`png` 等。如果需要匹配多种后缀，需要用 `\|` 进行分割，例如 `png\|jpg`。如果不填写，表示匹配所有后缀 | - | 配置用于匹配的请求文件后缀 |
| expires | string | 必填，表示缓存的最长时间。当填入的字符串为数字时，单位为秒，例如需要缓存1小时，需填写 3600。另外，还可以填写 epoch 或 max，与 nginx 中语义相同。 | - | 配置缓存的最大时间 |

作用：「为请求的响应头部添加 `Expires` 和 `Cache-Control` 头部」。`expires: max` ⇒ 「缓存所有文件，且缓存至最大时间 `"Thu, 31 Dec 2037 23:55:55 GMT"`」。
`epoch` 的具体语义 `[文档未说明]`（仅写「与 nginx 中语义相同」）。
来源：`[官方｜browser-cache-control]`

**hsts**（插件类型：流量管控；总表未收录）

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| **max_age** | number | 选填。 | 15724800 | 强制使用HTTPS访问网站的最大持续时间（以秒为单位）。 |
| **include_sub_domains** | bool | 选填。 | false | 当前域名以及子域名强制使用HTTPS访问网站。 |

`max_age` 默认值 `15724800` 秒（`[推断]` 按 86400 秒/天换算 ≈ 182 天；两个数都写：原文 `15724800` 秒）。
机制：「HSTS插件会对所有的HTTPS响应中添加`strict-transport-security`头部」；与 HTTPS 强跳转的区别：「HSTS对于HTTP请求可以直接在浏览器通过307内部跳转完成HTTPS转换，无需执行额外的网络请求。」
🔴 开启子域的风险（逐字）：「当开启`include_sub_domains`时，当前域名以及子域名强制使用HTTPS访问网站，必须确保所有子域名都支持HTTPS，否则用户将无法访问这些子域名。建议您在启用`include_sub_domains`之前先确保所有子域名都配置为支持HTTPS。」
来源：`[官方｜hsts-plug-in]`

**http-real-ip**（认证阶段/980，全插件最高优先级）

全部可用信息（页面仅 384 字节，正文逐字录全）：
> 「http-real-ip插件是nginx real-ip 模块的wasm实现。」
> 「## **插件类型** 流量管控。」
> 「## 参数描述
> * `real_ip_from`：定义已知发送客户端请求的可信地址。
> * `real_ip_header`：定义包含客户端地址的请求Header，其值将用于替换客户端地址，默认使用`x-forwarded-for`。」

🔴 **信息量不足以支撑对客答复**：无参数表（缺数据类型、填写要求、`real_ip_from` 默认值与取值范围）、无配置示例、无错误码、无作用层级、无「运行属性」小节（980 只能从总表回填）、未说明是否支持 CIDR 列表、未说明与 `geo-ip`/`cluster-key-rate-limit(limit_by_per_ip)` 的取值链路关系。
来源：`[官方｜http-real-ip-plug-ins｜upload-plug-in]`

**geo-ip（IP地理位置）**（认证阶段/440）

| 名称 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| ip_protocol | string | 否 | ipv4 | 可选值：1. ipv4：只对ipv4用户请求查找地理位置信息，传递给后续插件。而ipv6用户的请求会跳过该插件，继续由后续插件处理。 2. ipv6：（未来实现后）只对ipv6用户查找地理位置信息，传递给后续插件。而ipv4用户的请求会跳过该插件，继续由后续插件处理。（目前是跳过插件，请求由后续插件处理。） |
| ip_source_type | string | 否 | origin-source | 可选值：1. 对端socket ip：`origin-source`; 2. 通过header获取：`header` |
| ip_header_name | string | 否 | x-forwarded-for | 当`ip_source_type`为`header`时，指定自定义IP来源头 |

传递机制：「在geo-ip插件里调用proxywasm.SetProperty()，分别把country、city、province、isp设置进请求属性里，以便后续插件可以调用proxywasm.GetProperty()获取该请求的用户IP对应的地理信息。」
→ 可传递 4 个字段：`country`、`city`、`province`、`isp`（但 AI 提示词装饰器示例只用了 `${geo-country}`/`${geo-province}`/`${geo-city}`，`${geo-isp}` 是否可用 `[文档未说明]`）。
地理库来源与加载：「在generateCidr目录里包含的ip.merge.txt文件是gitHub上ip2region项目的全世界的IP网段库。ipRange2Cidr.go 是把IP网段转换成多个CIDR的程序。转换出的CIDR和地理位置信息存在 /data/geoCidr.txt文件里。geo-ip插件会在Higress启动读配置阶段读取geoCidr.txt文件并且解析到radixtree数据结构的内存里」
🔴 `[官方矛盾]`（参数名拼写）：字段表写 **`ip_protocol`**（默认 `ipv4`），但**同一页**的配置示例写 **`ipProtocal: "ipv4"`**（缺下划线且 protocol 拼错），`ai-cue-template` 页的 geo-ip 示例也写 `ipProtocal: "ipv4"`。双方原文已摘，不裁决——客户照抄示例可能配不生效。
🔴 ipv6 **未实现**（「目前是跳过插件，请求由后续插件处理」）；地理库更新频率/版本 `[文档未说明]`。
来源：`[官方｜geographic-location-of-ip｜ai-cue-template]`

**param-access-control（参数访问控制）**（鉴权阶段/310）

`parameters`（object,必填,「定义需要使用的参数，支持从Header、Query、Path中提取。」）取值格式：

| 参数 | 格式 | 描述 |
|---|---|---|
| Header | `Header:参数名` | 从请求头提取参数。 |
| Query | `Query:参数名` | 从查询参数提取参数。 |
| Path | `Path:序号` | 从路径中提取第n段内容，序号从1开始。 |
| Path | `Path` | 获取完整路径。 |

`rules`（array of rule,必填,「定义判断规则和处理逻辑。」）：

| 参数 | 数据类型 | 填写要求 | 默认值 | 描述 |
|---|---|---|---|---|
| name | string | 必填 | - | 规则名称。 |
| condition | string | 必填 | - | 判断条件。 |
| ifTrue | string | 选填 | - | 条件为真时的处理指令（ALLOW/DENY）。 |
| ifFalse | string | 选填 | - | 条件为假时的处理指令（ALLOW/DENY）。 |
| statusCode | number | 选填 | 403 | DENY时返回的HTTP状态码。 |
| responseHeaders | object | 选填 | - | DENY时返回的响应头。 |
| responseBody | string | 选填 | - | DENY时返回的响应体。 |

支持的运算符和函数（逐字）：

| 运算符/函数 | 描述 | 示例 |
|---|---|---|
| == | 等于 | `userType == 'admin'` |
| != | 不等于 | `status != 'inactive'` |
| > | 大于 | `version > '2.0'` |
| >= | 大于等于 | `level >= '3'` |
| < | 小于 | `priority < '5'` |
| <= | 小于等于 | `quota <= '100'` |
| contains | 包含子串 | `path.contains('api')` |
| matches | 正则匹配 | `url.matches('*.jpg')` |
| startsWith | 前缀匹配 | `path.startsWith('/api')` |
| endsWith | 后缀匹配 | `filename.endsWith('.jpg')` |
| && | 逻辑与 | `userType == 'admin' && level >= '3'` |
| \|\| | 逻辑或 | `path.startsWith('/api') \|\| path.startsWith('/v2')` |
| ! | 逻辑非 | `!(status == 'inactive')` |

执行语义（逐字）：「插件通过配置规则（rules）来控制请求访问，规则按照配置顺序依次执行直到遇到ALLOW或DENY指令。每个规则必须至少配置ifTrue或ifFalse其中之一，建议为DENY操作设置明确的状态码和响应信息。」
🔴 数值比较语义存疑：官方示例用 `apiVersion < '2.0'`、`level >= '3'`、`quota <= '100'`（**带引号的字符串**）配合 `>`/`>=`/`<`/`<=`，是字符串序还是数值序比较 → `[文档未说明]`。这是客户配错的高发点。
🔴 与总表的优先级冲突：本页「运行属性」写「插件执行阶段：鉴权阶段。插件执行优先级：310。」，而总表鉴权阶段 310 属「机器人拦截（bot-detect）」，且总表**未收录** param-access-control → `[官方矛盾]`/撞号。
典型用法：基于用户身份的访问控制（`userType == 'admin'` → ALLOW；`userId == '123'` 否则 DENY 403）；基于 API 版本的访问控制（`path.contains('/v2/') && apiVersion < '2.0'` → DENY 400 + JSON 错误体）。
来源：`[官方｜parameter-access-control｜upload-plug-in]`

---

### §9.6 自定义插件开发

#### §9.6.1 支持的语言

| 语言 | 官方给出的材料 | SDK/指引位置 | 来源 slug |
|---|---|---|---|
| **Go（Golang）** | 完整开发指南（工具准备、工程初始化、编写、编译、本地调试、外部服务调用、Redis 调用） | `github.com/higress-group/proxy-wasm-go-sdk@go-1.24`、`github.com/higress-group/wasm-go@main`、`github.com/tidwall/gjson` | `develop-gateway-plug-ins-using-the-go-language` |
| **Rust** | 仅一张外链表 | 「Rust SDK指引」→ `https://github.com/alibaba/higress/tree/main/plugins/wasm-rust` | `developing-gateway-plug-ins-using-rust-and-c-languages` |
| **C++** | 仅一张外链表 | 「C++ SDK指引」→ `https://github.com/alibaba/higress/tree/main/plugins/wasm-cpp` | `developing-gateway-plug-ins-using-rust-and-c-languages` |
| **AssemblyScript** | 🔴 **无开发页**，但出现在官方性能对比表中（有完整示例代码与延时数据） | `[文档未说明]`（34 页内无 AssemblyScript 开发指引或 SDK 链接） | `plug-in-performance-reference` |

`developing-gateway-plug-ins-using-rust-and-c-languages` **全文仅 515 字节**，正文逐字录全：
> 「本文提供使用Rust和C++语言开发网关插件的SDK指引。」+ 一张两行表（Rust → Rust SDK指引；C++ → C++ SDK指引）

🔴 **该页信息量不足以支撑对客答复**：无版本要求、无编译命令、无工具链准备、无本地调试方式、无与 Go 方案的能力差异、无 AI 网关版本适配要求。客户若问「我们用 Rust 写插件怎么编译/需要什么版本」，本章 34 页**无法回答**，须转 GitHub 或提工单。

`upload-plug-in` 的「选择语言」参数只写「选择编写插件时使用的开发语言。」，**未列枚举值** → 控制台实际可选语言清单 `[文档未说明]`。
`[推断]`（推理链：性能页对 C++/Golang/Rust/AssemblyScript 四种实现都给了可运行示例与延时数据 ⇒ 四种语言的 Wasm 产物都能被网关加载）：至少 4 种语言的插件可运行，但**只有 Go 有官方端到端开发文档**。

#### §9.6.2 🔴 Go 语言开发的硬性版本约束与迁移事项

| 项目 | 官方口径（逐字） |
|---|---|
| Go 版本 | 「官方指引链接（需为**1.24版本以上**）。」下载文件名均为 `go1.24.4.*`（windows-amd64.msi / darwin-amd64.pkg / linux-amd64.tar.gz） |
| 🔴 网关版本下限 | 「使用 Go 1.24 编译的插件需要AI网关版本**不低于`2.1.5`**，低版本网关参考使用 GO 语言开发 WASM 插件（Higress 社区文档）」 |
| 编译方案变更 | 「Higress 已完成从 **TinyGo 0.29 + Go 1.20** 编译方案迁移至 **Go 1.24 原生支持**的 Wasm 编译。Go 1.24 版本现已原生支持 Wasm 文件编译。」 |
| 迁移改动 1 | 「对于此前使用 TinyGo 编译插件的用户，若需迁移到 Go 1.24 编译模式，除调整 go.mod 中的依赖外，还需将插件初始化逻辑由 **main 函数移至 init 函数**。」 |
| 迁移改动 2 | 「若在 Header 处理阶段调用外部服务并返回 `type.ActionPause`，需改为返回 `types.HeaderStopAllIterationAndWatermark`。」 |
| 迁移改动 3 | 「若因 TinyGo 对标准库 regexp 支持不完整而使用了 **go-re2** 库，现应替换为 Go 官方 **regexp** 包。」 |
| 国内依赖代理 | `go env -w GOPROXY=https://proxy.golang.com.cn,direct` |
| 编译命令 | `go mod tidy` → `GOOS=wasip1 GOARCH=wasm go build -buildmode=c-shared -o main.wasm ./` |
| 本地调试镜像 | `higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/gateway:v2.1.5`；后端 `kennethreitz/httpbin:latest`；wasm 日志级别 `--component-log-level wasm:debug`（「正式部署时则默认info级别」）；监听端口 `10000`（网关）/`12345`（httpbin）/`9901`（envoy admin） |
| Higress 侧打包 | 「要在 Higress 中配合 Wasmplugin CRD 或者 Console 的 UI 交互配置该插件，需要将该 wasm 文件打包成 oci 或者 docker 镜像」 |

**HTTP 处理挂载点（4 个阶段）**：

| HTTP 处理阶段 | 触发时机 | 挂载方法 |
|---|---|---|
| HTTP 请求头处理阶段 | 网关接收到客户端发送来的请求头数据时 | `wrapper.ProcessRequestHeadersBy` |
| HTTP 请求 Body 处理阶段 | 网关接收到客户端发送来的请求 Body 数据时 | `wrapper.ProcessRequestBodyBy` |
| HTTP 应答头处理阶段 | 网关接收到后端服务响应的应答头数据时 | `wrapper.ProcessResponseHeadersBy` |
| HTTP 应答 Body 处理阶段 | 网关接收到后端服务响应的应答 Body 数据时 | `wrapper.ProcessResponseBodyBy` |

`webide-writing-plug-ins` 另给出**流式**挂载点（Go 开发页未列）：`wrapper.ProcessStreamingRequestBodyBy`（「设置自定义函数处理流式请求体」）、`wrapper.ProcessStreamingResponseBodyBy`（「设置自定义函数处理流式响应体」）、`wrapper.ProcessStreamDoneBy`（「设置自定义函数处理流式请求完成」，示例中被注释）。
→ 🔴 这是本章唯一提到"流式插件处理"的地方，AI 场景（SSE）客户必问；能力细节与限制 `[文档未说明]`。

**SDK 工具方法全表（逐字，含生效阶段限定）**：

| 分类 | 方法名称 | 用途 | 可以生效的 HTTP 处理阶段 |
|---|---|---|---|
| 请求头处理 | GetHttpRequestHeaders | 获取客户端请求的全部请求头 | HTTP 请求头处理阶段 |
| 请求头处理 | ReplaceHttpRequestHeaders | 替换客户端请求的全部请求头 | HTTP 请求头处理阶段 |
| 请求头处理 | GetHttpRequestHeader | 获取客户端请求的指定请求头 | HTTP 请求头处理阶段 |
| 请求头处理 | RemoveHttpRequestHeader | 移除客户端请求的指定请求头 | HTTP 请求头处理阶段 |
| 请求头处理 | ReplaceHttpRequestHeader | 替换客户端请求的指定请求头 | HTTP 请求头处理阶段 |
| 请求头处理 | AddHttpRequestHeader | 新增一个客户端请求头 | HTTP 请求头处理阶段 |
| 请求 Body 处理 | GetHttpRequestBody | 获取客户端请求 Body | HTTP 请求 Body 处理阶段 |
| 请求 Body 处理 | AppendHttpRequestBody | 将指定的字节串附加到客户端请求 Body 末尾 | HTTP 请求 Body 处理阶段 |
| 请求 Body 处理 | PrependHttpRequestBody | 将指定的字节串附加到客户端请求 Body 的开头 | HTTP 请求 Body 处理阶段 |
| 请求 Body 处理 | ReplaceHttpRequestBody | 替换客户端请求 Body | HTTP 请求 Body 处理阶段 |
| 应答头处理 | GetHttpResponseHeaders | 获取后端响应的全部应答头 | HTTP 应答头处理阶段 |
| 应答头处理 | ReplaceHttpResponseHeaders | 替换后端响应的全部应答头 | HTTP 应答头处理阶段 |
| 应答头处理 | GetHttpResponseHeader | 获取后端响应的指定应答头 | HTTP 应答头处理阶段 |
| 应答头处理 | RemoveHttpResponseHeader | 移除后端响应的指定应答头 | HTTP 应答头处理阶段 |
| 应答头处理 | ReplaceHttpResponseHeader | 替换后端响应的指定应答头 | HTTP 应答头处理阶段 |
| 应答头处理 | AddHttpResponseHeader | 新增一个后端响应头 | HTTP 应答头处理阶段 |
| 应答 Body 处理 | GetHttpResponseBody | 获取客户端请求 Body `[原文如此，按分类应为"后端响应 Body"`] | HTTP 应答 Body 处理阶段 |
| 应答 Body 处理 | AppendHttpResponseBody | 将指定的字节串附加到后端响应 Body 末尾 | HTTP 应答 Body 处理阶段 |
| 应答 Body 处理 | PrependHttpResponseBody | 将指定的字节串附加到后端响应 Body 的开头 | HTTP 应答 Body 处理阶段 |
| 应答 Body 处理 | ReplaceHttpResponseBody | 替换后端响应 Body | HTTP 应答 Body 处理阶段 |
| HTTP 调用 | DispatchHttpCall | 发送一个 HTTP 请求 | - |
| HTTP 调用 | GetHttpCallResponseHeaders | 获取 DispatchHttpCall 请求响应的应答头 | - |
| HTTP 调用 | GetHttpCallResponseBody | 获取 DispatchHttpCall 请求响应的应答 Body | - |
| HTTP 调用 | GetHttpCallResponseTrailers | 获取 DispatchHttpCall 请求响应的应答 Trailer | - |
| 直接响应 | SendHttpResponse | 直接返回一个特定的 HTTP 应答 | - |
| 流程恢复 | ResumeHttpRequest | 恢复先前被暂停的请求处理流程 | - |
| 流程恢复 | ResumeHttpResponse | 恢复先前被暂停的应答处理流程 | - |

> 🔴 `[官方原文]`「请不要在请求/响应未处于Pause状态时，调用ResumeHttpRequest或调用ResumeHttpResponse。尤其注意在SendHttpResponse之后，Pause状态的请求/响应将自动恢复，若再调用ResumeHttpRequest或ResumeHttpResponse将导致**未定义的行为**。」

**Header 状态管理（5 个状态，逐字，直接决定自定义插件会不会阻塞请求）**：

| Header 状态 | 说明 |
|---|---|
| `HeaderContinue` | 表示当前 filter 已经处理完毕，可以继续交给下一个 filter 处理。`types.ActionContinue` 对应该状态。 |
| `HeaderStopIteration` | 表示 header 还不能继续交给下一个 filter 进行处理。但并不停止从连接读数据，继续触发 body data 的处理。这样可以在 body data 处理阶段更新 Http 请求头内容。如果 body data 需要交给下一个 filter 处理，此时 header 也会被一起交给下一个 filter 处理。**说明**：「返回该状态时，要求必须有 body，如果没有 body，请求/响应将被一直阻塞。」判断是否存在请求 body 可用 `HasRequestBody()`。 |
| `HeaderContinueAndEndStream` | 表示 header 可以继续交给下一个 filter 处理，但下一个 filter 收到的 `end_stream = false` 标记请求还未结束，以便当前 filter 再增加 body。 |
| `HeaderStopAllIterationAndBuffer` | 停止所有迭代，表示 header 不能继续交给下一个 filter，并且当前 filter 也不能收到 body data。并对当前过滤器及后续过滤器的头部、数据和尾部进行缓冲。**如果缓存大小超过了 buffer limit，在请求阶段就直接返回 413，响应阶段就直接返回 500。** 同时需要调用 `proxywasm.ResumeHttpRequest()`、`proxywasm.ResumeHttpResponse()` 或者 `proxywasm.SendHttpResponseWithDetail()` 函数来恢复后续处理。 |
| `HeaderStopAllIterationAndWatermark` | 与 `HeaderStopAllIterationAndBuffer` 相同，区别是**当缓存超过了 buffer limit 会触发流控，即暂停从连接上读数据**。「0.2.1 ABI 中的 `types.ActionPause` 实际上对应就是这个状态。」 |

> 官方参考实现：「关于 types.HeaderStopIteration 和 HeaderStopAllIterationAndWatermark 的使用场景可以参考 Higress 官方提供 ai-transformer 插件和 ai-quota 插件。」

**插件内调用外部服务的边界（有决策含义）**：
> `[官方原文]`「目前**仅支持 http 调用**，支持访问在网关控制台中设置了服务来源的 Nacos、K8s 服务，以及固定地址或 DNS 来源的服务。请注意，**无法直接使用`net/http`库中的 HTTP client**，必须使用如下例中封装的 HTTP client。」

- FQDN 写法：「带服务类型的完整 FQDN 名称，例如 my-svc.dns, my-svc.static, service-provider.DEFAULT-GROUP.public.nacos, httpbin.my-ns.svc.cluster.local」
- 🔴 HTTP client **默认超时 500 毫秒**：「此处省略了timeout参数，默认超时时间500毫秒」
- 静态 IP 类型服务的**逻辑端口默认 80**：「静态IP类型服务的逻辑端口是80」
- 失败降级由**开发者自己写**：官方示例在 `err != nil` 时「由于调用外部服务失败，放行请求，记录日志」并 `return types.ActionContinue` ⇒ 网关不代做熔断/降级
- Redis 调用：`wrapper.NewRedisClusterClient(wrapper.FQDNCluster{...})` + `client.Init(username, password, timeout)`；示例默认 `timeout = 1000`（「单位是毫秒」）、非 static 服务默认端口 `6379`、static 服务默认 `80`；官方 Redis 限流示例用 `Incr` + `Expire(key, 60)` 实现 QPM，超限返回 `429` + 响应头 `timeStamp`/`callTimeLeft`，Body `Too many requests\n`
- 「如果 redis api 返回的 err != nil，一般是由于网关找不到 redis 后端服务，请检查是否误删除了 redis 后端服务」
- 除 HTTP / Redis 外能否调用其他协议（gRPC、数据库、消息队列）→ `[文档未说明]`

来源：`[官方｜develop-gateway-plug-ins-using-the-go-language｜webide-writing-plug-ins]`

#### §9.6.3 WebIDE 编写插件

| 项目 | 官方口径（逐字） |
|---|---|
| 解决的问题 | 「为了解决自定义插件编写门槛较高，搭建开发环境难的问题，AI网关提供了一个包含插件开发环境的WebIDE Runtime，可以通过WebIDE一站式完成自定义插件的开发和编译。」 |
| 代码归属与工程化 | 「WebIDE内置集成**云效仓库**，代码资源属于用户，代码提交Git化管理，支持持久化管理、内置流水线标准化环境以及自动化构建。」 |
| 新建流程 | 插件页 →「**WebIDE编写插件**」→「新建」→ 输入**插件标识**与**插件名称**→「确定」进入 WebIDE |
| 构建 | 右上角「**构建**」→「确认」。「如果存在文件未提交时进行构建，需选择提交并构建或者直接构建，**直接构建不会对未提交的内容进行构建**。」；「可单击右上角**构建日志**实时查看构建情况。」 |
| 发布 | 构建完成后 →「**发布版本**」→ 添加版本页配置 →「**发布**」。「网关插件代码编写完毕后，需完成构建与发布后，才可在网关进行安装。」 |
| 发布版本配置项 | **版本号**（「版本编号，格式需符合X.Y.Z」，示例 `1.0.0`）；**版本描述**（示例「修改返回格式」）；**执行阶段**（「阶段处理顺序：认证阶段 > 鉴权阶段 > 统计阶段 > 默认阶段。若不依赖其他插件执行顺序，填写默认阶段即可。」示例「默认阶段」）；**执行优先级**（「控制执行阶段内的优先级，数字越大优先级越高。」示例 `100`）；**适配网关版本**（「任意版本：可以安装到任意版本的网关。指定版本：仅可以安装到指定版本（含）之后的网关版本。」示例「任意版本」） |
| AI 一键生成 | 「WebIDE支持用户通过自然语言描述实现一键生成插件代码」：右上角「**一键生成**」→「在一键生成编辑框中详细描述需求」→「单击**确认**，等待代码生成直至结束」 |
| WebIDE 支持的语言 | `[文档未说明]`（页面只给 Golang 骨架代码） |
| 是否另计费（云效仓库/流水线/构建资源） | `[文档未说明]` ← 🔴 连带计费空白，报价时必须核验 |
| 构建超时/失败重试/构建资源规格 | `[文档未说明]` |

#### §9.6.4 🔴 插件性能参考（数字全部照抄，含表头与测试条件）

**这是客户评估「加插件会不会拖慢网关」的唯一官方依据。**

**A. 平台插件性能（官方原文逐字）**

> `[官方原文]`「## 平台插件性能
> 平台提供的插件对请求延迟的影响都是微秒级的，例如key-auth插件只会为每个请求增加20微秒左右的延时，basic-auth插件只会为每个请求增加30微秒左右的延时。」`[官方｜plug-in-performance-reference]`

| 插件 | 每请求延时增加（原文） | 测试条件 |
|---|---|---|
| key-auth | 20微秒左右 | `[文档未说明]`（原文未给 QPS、报文大小、实例规格、并发数） |
| basic-auth | 30微秒左右 | `[文档未说明]`（同上） |
| 其余全部平台插件 | 仅有定性表述「都是微秒级的」，**无逐个数字** | — |

**B. 自定义插件性能（官方原文逐字，含测试条件）**

> `[官方原文]`「## 自定义插件性能
> 下面例子用不同语言实现了相同的处理逻辑，并比较了性能。具体处理逻辑是：**循环执行20次请求头设置，循环执行20次请求头获取，循环执行20次请求头移除**。」`[官方｜plug-in-performance-reference]`

即测试条件为：同一处理逻辑（20 次 set header + 20 次 get header + 20 次 remove header），四种语言各实现一份，仅在 `onRequestHeaders` / `OnHttpRequestHeaders` / `on_http_request_headers` / `onRequestHeaders` 阶段执行。官方给出的四份实现代码要点：
- C++：`FilterHeadersStatus PluginContext::onRequestHeaders(uint32_t, bool)`，`addRequestHeader` / `getRequestHeader` / `removeRequestHeader`，返回 `FilterHeadersStatus::Continue`
- Golang：`func (ctx *httpContext) OnHttpRequestHeaders(numHeaders int, endOfStream bool) types.Action`，`proxywasm.AddHttpRequestHeader` / `GetHttpRequestHeader` / `RemoveHttpRequestHeader`，返回 `types.ActionContinue`
- Rust：`fn on_http_request_headers(&mut self, _: usize, _: bool) -> Action`，`self.set_http_request_header(&key, Some(&value))` / `get_http_request_header` / `set_http_request_header(&key, None)`，返回 `Action::Continue`
- AssemblyScript：`function onRequestHeaders(a: u32, end_of_stream: bool): FilterHeadersStatusValues`，`stream_context.headers.request.add/get/remove`，返回 `FilterHeadersStatusValues.Continue`

**不同语言实现性能对比（表头与数值逐字照抄）**：

| 实现语言 | 请求延时增加 |
|---|---|
| C++ | 0.19毫秒 |
| Golang | 0.20毫秒 |
| Rust | 0.21毫秒 |
| AssemblyScript | 0.21毫秒 |

> `[官方原文]`「可以看到不同语言实现的性能差距不大。」

**C. 🔴 数字纪律提醒（两个不同单位，不可混用）**

- 平台插件单位是**微秒**（key-auth 20微秒、basic-auth 30微秒）；自定义插件基准单位是**毫秒**（0.19~0.21毫秒）。
- 换算（`[推断]`，两组都写）：`0.19毫秒（原文）= 190微秒`；`0.20毫秒（原文）= 200微秒`；`0.21毫秒（原文）= 210微秒`。
- 由此 `[推断]`（推理链：190~210微秒 vs 20~30微秒 ⇒ 约 6~10 倍）：**官方基准里那个"20 次 set + 20 次 get + 20 次 remove header"的自定义插件，单请求开销约是 key-auth 的 6~10 倍**。但两者**工作负载不同**（key-auth 的实际逻辑官方未描述），因此不可直接推广为"自定义插件一定比平台插件慢 10 倍"。
- **该页未提供的、SA 一定会被问到的数字**（全部 `[文档未说明]`）：
  - 各平台插件（尤其 `ai-*` 系列、waf、hmac-auth、cluster-key-rate-limit、frontend-gray）的**逐个延时数据**
  - 测试所用**实例规格 / 引擎版本 / QPS / 并发数 / 报文大小 / 是否流式**
  - **多插件叠加**时的总延时（线性叠加还是有额外开销）
  - 插件对**吞吐量（QPS 上限）**与**内存/CPU 占用**的影响（仅 `request-block-plugin` 与 `hmac-auth-plug-ins` 提到调高 `DownstreamConnectionBufferLimits` 后「网关内存使用将有显著增加」，无数字）
  - 自定义插件调用外部服务/Redis 时的端到端延时（仅有 HTTP client 默认超时 `500毫秒`、Redis 默认 `timeout` `1000毫秒` 这两个上限值，非实测延时）
  - 测试日期与复现方式

#### §9.6.5 发布自定义插件的流程与约束（汇总）

| 环节 | 约束（逐字/要点） | 来源 slug |
|---|---|---|
| 可见性 | 「只有当前主账号或具有AI网关权限的子账号可以看到并使用该插件。插件启用方式和平台提供插件一致。」 | `upload-plug-in` |
| 入口 | 插件市场页右上角「**发布插件**」 | `upload-plug-in` |
| 上传物 | WASM 文件，「文件名需要包含 ".wasm" 后缀」 | `upload-plug-in` |
| 发布耗时 | 「此过程可能需要30秒左右」 | `upload-plug-in` |
| 必填决策项 | 选择语言 / 插件标识（英文唯一标识）/ 插件名称（中文）/ 插件描述 / 版本描述 / WASM文件 / **执行阶段** / **执行优先级** / **适配网关版本** | `upload-plug-in` |
| 版本号格式 | 「格式需符合X.Y.Z」（WebIDE 发布路径） | `webide-writing-plug-ins` |
| 版本适配语义 | 「任意版本：可以安装到任意版本的网关。指定版本：仅可以安装到指定版本（含）之后的网关版本。」 | `upload-plug-in`｜`webide-writing-plug-ins` |
| 网关版本下限（Go 1.24 编译） | 「需要AI网关版本不低于`2.1.5`」 | `develop-gateway-plug-ins-using-the-go-language` |
| 可安装形态 | 🔴 「仅专享实例型AI网关支持安装与启用插件，Serverless版不支持。」 | `manage-plug-ins` |
| 发布失败排查 | 「一般可能是生成的Wasm文件二进制格式不合法。关于在本地环境成功加载该Wasm文件的Demo示例，请参见使用Go语言开发网关插件。」 | `upload-plug-in` |
| 优先级定制建议 | 「若需定制，建议填写10的整数倍，预留好空间。」 | `upload-plug-in` |
| 插入到平台插件前后 | 「在平台提供插件的详情中，可以看到执行阶段和执行优先级的信息」⇒ 需对照 §9.1.7 总表取值 | `upload-plug-in` |
| 插件签名/审核/安全扫描 | `[文档未说明]` | — |
| 自定义插件数量/版本数上限 | `[文档未说明]` | — |
| 发布是否需审批、能否回滚到旧版本 | `[文档未说明]` | — |
| RAM 权限点（发布插件需要哪些 action） | `[文档未说明]`（归 W4/W7） | — |

---

### §9 溯源

- `manage-plug-ins` — 插件安装启用与卸载（5041）：§9.1.1 插件三来源；§9.1.2 🔴 仅专享实例支持、Serverless 不支持；§9.1.3 安装→配置规则→启用三步与两条入口、启用状态默认开启；§9.1.4 卸载前置约束；§9.1.5 三级作用域定义与匹配优先级；§9.6.5 可安装形态
- `upload-plug-in` — 发布自定义插件（10444）：§9.1.1 自定义插件可见性；§9.1.6 四执行阶段顺序、优先级语义、请求/应答顺序相反、插入平台插件前后；§9.1.7 🔴 插件与策略完整优先级总表（45 行，本章唯一全局顺序依据）；§9.1.8 发布面板 9 个参数、WASM 后缀、30 秒、发布失败原因、适配网关版本；§9.2.1/§9.2.3/§9.2.4 类别与优先级回填；§9.6.5 发布流程与约束
- `webide-writing-plug-ins` — WebIDE 编写插件（6073）：§9.1.6 执行阶段/优先级配置项；§9.1.8 YAML→JSON 自动转换、版本号 X.Y.Z；§9.6.2 流式挂载点（ProcessStreamingRequestBodyBy/ProcessStreamingResponseBodyBy/ProcessStreamDoneBy）；§9.6.3 WebIDE 全流程（云效仓库、构建、构建日志、发布版本、一键生成）；§9.3.7 骨架代码 `logs.Log` 一方
- `plug-in-performance-reference` — 插件性能参考（4051）：§9.3.0 无 AI 插件性能数据；§9.6.1 AssemblyScript 支持证据；§9.6.4 🔴 全部性能数字（key-auth 20微秒、basic-auth 30微秒、C++ 0.19毫秒、Golang 0.20毫秒、Rust 0.21毫秒、AssemblyScript 0.21毫秒）与测试条件（20 次 set/get/remove header）、四份实现代码要点
- `develop-gateway-plug-ins-using-the-go-language` — Go 语言开发网关插件（28735）：§9.1.8 编译命令/Wasm 运行时/oci 镜像；§9.6.1 Go SDK 依赖；§9.6.2 🔴 Go 1.24+、网关 ≥2.1.5、TinyGo→Go 1.24 三条迁移事项、4 个 HTTP 挂载点、27 个 SDK 工具方法全表、5 个 Header 状态、ResumeHttpRequest 未定义行为警告、外部服务仅支持 http、HTTP client 默认超时 500 毫秒、static 服务默认端口 80、Redis 默认端口 6379/timeout 1000 毫秒、本地 docker compose 调试环境
- `developing-gateway-plug-ins-using-rust-and-c-languages` — Rust 与 C++ 开发网关插件（515）：§9.6.1 Rust/C++ 仅有 GitHub SDK 外链；🔴 已在 §9.6.1 标注该页信息量不足以支撑对客答复
- `ai-auxiliary-plug-in-development` — AI 辅助插件开发（2537）：§9.3.7 端到端插件生成定位、四段式需求描述模板、不合理需求会被直接结束任务、产物自动导入 WebIDE、Golang 骨架（`wrapper.Log` 一方，与 WebIDE 页构成矛盾）
- `ai-cue-template` — AI 提示词插件（4248）：§9.2.1/§9.2.2/§9.3.1 ai-prompt-decorator（prepend/append、默认阶段/450、`${geo-*}` 插值、与 geo-ip 的优先级要求、geo-ip 示例中 `ipProtocal` 拼写一方）
- `ai-cue-decorator` — AI 提示词模板插件（2596）：§9.2.1/§9.2.2/§9.3.2 ai-prompt-template（templates/name/template.model/template.messages、默认阶段/500、`{{}}` 变量语法、调用方请求体形态）
- `ai-rag` — AI RAG 插件（4674）：§9.2.1/§9.3.3 11 个全必填参数、DashScope+DashVector 双外部依赖、链路追踪 span attribute 注入 rag 文档 id、🔴 优先级 400 与总表 405 矛盾、`collection` 字段未入表、CEC-Corpus 效果对比
- `ai-retrieval-agent` — AI RAG 检索代理（13994）：§9.2.1/§9.3.4 ragflow/bailian 两套完整参数与默认值、`enable_to_proxy_api_key` 校验、🔴 路径后缀必须 /retrieval、Agent API 承载、Dify 对接步骤、优先级 150 与总表 ai-json 撞号、与加强版的默认值差异（矛盾一方）
- `ai-retrieval-augmented-generation-enhanced` — AI 检索增强生成加强版（16066）：§9.1.5 🔴 Model API 级插件规则（与 manage-plug-ins 三分类矛盾）；§9.2.1/§9.3.5 ragflow/bailian 全参数与默认值、`result_placement_type` 与 `{{higressRagResultReplacementKey}}` 占位符、rerank/rewrite 模型清单、百炼 AK/SK + 子账号权限（AliyunBailianDataFullAccess 或 sfm:Retrieve）、TLS 模式差异、Model API 前置对象
- `ai-request-response-intelligent-transformation` — AI 请求响应转换插件（3330）：§9.2.1/§9.3.6 7 个全必填参数、仅支持千问、DNS 类型服务、认证阶段/410、XML→JSON 示例、🔴 与总表两行（请求/响应转换 vs ai-transformer）阶段与系列矛盾
- `degraphql-plugin` — DeGraphQL 插件（5165）：§9.1.8 oci 镜像 URL；§9.2.1/§9.5.7 gql/endpoint(/graphql)/timeout(5000毫秒)/domain 四参数、参数表仅 3 列、示例为 Higress K8s CRD 形态、GraphQL→REST 转换示例
- `custom-response-plugin` — custom-response 插件（3171）：§9.1.5 规则匹配语义；§9.2.1/§9.5.7 status_code(200)/headers/body/enable_on_status 四参数、Mock 与 429→302 限流兜底两个场景、插件类型「传输协议」、总表未收录
- `request-block-plugin` — request-block 插件（3928）：§9.1.5 规则匹配语义；§9.2.1/§9.5.6 block_urls/block_headers/block_bodys（至少必填一项）、blocked_code(403)/blocked_message/case_sensitive(true)、🔴 32MB Body 匹配上限与 DownstreamConnectionBufferLimits→413
- `waf-plugin` — waf 插件（2956）：§9.1.5 规则匹配语义；§9.2.1/§9.5.6 useCRS(false)/secRules、🔴 静态规则不实时更新的能力边界、DetectionOnly 观测模式、OWASP CRS v3.3.2、路由/域名级 deny-pass 覆盖示例
- `bot-detect-plug-ins` — bot-detect 插件（2744）：§9.1.5 规则匹配语义；§9.2.1/§9.5.6 allow/deny/blocked_code(403)/blocked_message、🔴 默认规则会把 Golang 网络库请求判为爬虫、allow/deny 均不配时走内置默认逻辑
- `basic-auth-plug-ins` — basic-auth 插件（5994）：§9.2.1/§9.4.2/§9.4.3/§9.4.4 consumers/credential/name/global_auth/allow、认证与鉴权不可同规则、X-Mse-Consumer、global_auth 三态、401/401/403 错误码、用户名密码以「:」分隔、credential 不可重复
- `key-auth-plug-ins` — key-auth 插件（6839）：§9.2.1/§9.4.2/§9.4.3/§9.4.5 keys/in_query(true)/in_header(true)、URL 参数与请求头两种传 Key 方式、🔴 错误码表 403 行误写 "Basic Auth check"、401 vs 403 语义区分
- `hmac-auth-plug-ins` — hmac-auth 插件（13117）：§9.2.1/§9.4.2/§9.4.3/§9.4.6 key/secret/date_offset、7 字段签名串、Accept 为空导致校验失败、Content-MD5 计算条件、Headers 字典序拼接与 6 个不参与签名的头、PathAndParameters 组织形式、HmacSHA256/HmacSHA1、4 个 x-ca-* 头、🔴 X-Ca-Error-Message 排错机制（换行替换为 #）、8 条错误码含 32MB 与 DownstreamConnectionBufferLimits、示例 consumer 命名不一致
- `jwt-auth-plug-ins` — jwt-auth 插件（16630）：§9.1.5 `_disable_: true` 与规则匹配优先级；§9.2.1/§9.4.1 🔴 与内置「配置JWT认证鉴权」的唯一官方对比句；§9.4.2/§9.4.3/§9.4.7 consumers 11 个子字段全默认值、jwks/remote_jwks 二选一与优先级、remote_jwks 1Mb 建议、from_headers/from_params/from_cookies 默认值生效条件、claims_to_headers.override、clock_skew_seconds(60)/keep_token(true)、多 jwks 命中首个 consumer、🔴 remote_jwks 的 port/timeout/ttl 类型标 bool 矛盾、4 条错误码
- `jwt-logout-plug-ins` — jwt-logout 插件（17636）：§9.2.1/§9.4.2/§9.4.8 jwks/clock_skew(60)/token_header(Authorization)/token_prefix("Bearer")/redis(必填)/logout/login 全部默认值、Redis 五字段、logout 与 login 各 6 字段默认值、ttl 未填按 exp 计算与 86400 秒兜底、Key 拼接规则、🔴 Redis 容量口径（1 请求→3 读，登出/首登再+2 写，按吞吐量×2 评估）、阿里云 Redis 接入（DNS 域名/6379/TLS 关闭）、🔴 login.key_prefix 默认值与页内示例前缀矛盾、🔴 login 示例 Key 第三段 abcd 与 Payload sub=test 矛盾、401/500 错误码
- `oauth-plugin` — oauth 插件（9209）：§9.2.1/§9.4.2/§9.4.3/§9.4.9 issuer(Higress-Gateway)/auth_path(/oauth2/token)/global_credentials(true)/auth_header_name(Authorization)/token_ttl(7200)/clock_skew_seconds(60)/keep_token(true)、client_id/client_secret、auth_path 命中即不转发、关闭 global_credentials 的精确匹配路由风险、🔴 凭证按路由隔离 vs global_credentials 共享、仅 Client Credential 有示例、GET 推荐/POST 需先匹配真实路由、401/403、Jwt Auth 复制残留
- `key-rate-limit-plugin` — key-rate-limit 插件（4070）：§9.2.1/§9.5.1 🔴 limit_by_header/limit_by_param 二选一（仅 2 种计量维度）、limit_keys 必填、四种时间粒度、路由/域名级示例、规则匹配语义
- `throttle-based-on-cluster-keys` — cluster-key-rate-limit 插件（13186）：§9.2.1/§9.5.1 🔴 Redis 集群限流底座、9 种 limit_by_* 维度、per_* 系列支持 regexp:/*、limit_by_per_ip 的 from-header-/from-remote-addr 写法、IP/IP 段、rule_name 拼装 redis key、rule_items 首个命中、show_limit_quota_header(false)/rejected_code(429)/rejected_msg、redis 五字段与 static 默认 80 其他 6379/timeout 1000、🔴 限流不生效 FAQ（service_name 必须带服务类型 FQDN）
- `the-traffic-tag-plugin` — traffic-tag 插件（8159）：§9.2.1/§9.5.2/§9.5.3 conditionGroups/weightGroups/defaultTagKey/defaultTagVal、7 种 operator、conditionType 三选、logic 必须小写、RE2 引擎、🔴 percentage(hash%100<value，幂等) vs weight(随机，不幂等) 官方辨析、权重总和 100 与未配置部分不加 header
- `canary-header-plugin` — canary-header 插件（3600）：§9.1.5 `_rules_`/`_match_route_`/`_match_domain_` 语法唯一来源；§9.2.1/§9.5.2/§9.5.4 weighted_headers/added_key/added_value/weight、权重和不能大于100、不足100部分为不加 header 概率、🔴 添加 header 后重新匹配路由（需配套 header 匹配路由）
- `front-end-grayscale-plug-in` — frontend-gray 前端灰度插件（16020）：§9.2.1/§9.5.2/§9.5.5 16 个主字段 + rules/rewrite/baseDeployment/grayDeployments 全部默认值（useManifestAsEntry=false、storeMaxAge=60\*60\*24\*365、backendGrayTag=x-mse-tag、uniqueGrayTag=x-higress-uid）、四种分流判据、{version} 保留字段、indexRouting/fileRouting 前缀重写与生效示例、injection 三处注入点、skippedPaths 优先级高于 skippedByHeaders 且 HTML 请求不受影响、LocalStorage 需自行注入脚本回写 Cookie、🔴 优先级 1000 与总表 450 矛盾、notFoundUri 字段未入表
- `geographic-location-of-ip` — geo-ip 插件（4322）：§9.2.1/§9.3.1/§9.5.7 ip_protocol(ipv4)/ip_source_type(origin-source)/ip_header_name(x-forwarded-for)、🔴 ipv6 未实现、SetProperty 传 country/city/province/isp、ip2region→geoCidr.txt→radixtree 内存加载、与 ai-prompt-decorator 联用的优先级要求、🔴 同页示例 `ipProtocal` 与字段表 `ip_protocol` 拼写矛盾、§9.2.2 命名错位的第三方交叉验证
- `hsts-plug-in` — hsts 插件（1860）：§9.2.1/§9.2.4/§9.5.7 max_age(15724800)/include_sub_domains(false)、strict-transport-security 头、浏览器 307 内部跳转、🔴 子域未全量 HTTPS 会导致无法访问、插件类型「流量管控」与总表分类矛盾一方、总表未收录 hsts
- `http-real-ip-plug-ins` — http-real-ip 插件（384）：§9.2.1/§9.5.7 real_ip_from/real_ip_header(默认 x-forwarded-for)、nginx real-ip 模块的 wasm 实现、插件类型「流量管控」、总表认证阶段/980（全插件最高）；🔴 已在 §9.5.7 标注该页信息量不足以支撑对客答复（无参数表/无示例/无错误码/无层级）
- `browser-cache-control` — cache-control 浏览器缓存插件（2034）：§9.2.1/§9.5.7 suffix（`|` 分割，不填匹配所有后缀）/expires（必填，数字=秒，可填 epoch 或 max）、认证阶段/420、Expires 与 Cache-Control 头、max ⇒ "Thu, 31 Dec 2037 23:55:55 GMT"
- `parameter-access-control` — param-access-control 参数访问控制（6371）：§9.2.1/§9.5.7 parameters 四种取值格式（Header:/Query:/Path:序号/Path）、rules 七字段与 statusCode 默认 403、13 个运算符与函数、规则顺序执行至 ALLOW/DENY、ifTrue/ifFalse 至少配一个、鉴权阶段/310 与总表 bot-detect 撞号、字符串比较语义存疑

**本章 34 个快照全部使用，无未使用页。**

#### 本章查无（必填：翻过但文档确实没写的高价值问题）

**🔴 P0 级空白（对客必被问，文档 0 命中）**

1. **插件是否消耗 AI Credits / 是否额外计费**：34 页对 `AI Credits`/`Credits`/`计费`/`收费`/`免费`/`公测` **全部 0 命中**。包括明确会额外调用 LLM 的 `ai-transformer`（AI 请求响应转换）、`ai-retrieval-augmented-generation-enhanced`（含 rerank/rewrite 模型调用）、`ai-rag`（DashScope + DashVector 双依赖）。SA 报价时**必须另走购买页/工单核验**，本章无任何依据。
2. **插件对 Token 开销的量化影响**：无任何数字。仅能定性推断（见 §9.3 各条 `[推断]`）。
3. **平台插件逐个延时数据**：`plug-in-performance-reference` 只点名 key-auth(20微秒) 与 basic-auth(30微秒)，其余全部插件（尤其 `ai-*` 系列、waf、hmac-auth、cluster-key-rate-limit、frontend-gray）**无数字**，只有「都是微秒级的」这一定性表述。
4. **性能测试条件**：实例规格、引擎版本、QPS、并发数、报文大小、是否流式、测试日期 —— 全部 `[文档未说明]`。客户拿 0.19毫秒 做容量规划时无法判断可复现性。
5. **多插件叠加的总延时**：`[文档未说明]`（是否线性叠加）。
6. **插件配额**：单实例可安装插件数量上限、插件规则条数上限、Wasm 文件大小上限、自定义插件版本数上限 —— 全部 `[文档未说明]`。
7. **`http-real-ip` 页信息量不足**：384 字节，无参数表（缺数据类型/填写要求/`real_ip_from` 默认值与取值范围）、无示例、无错误码、无作用层级、未说明是否支持 CIDR、未说明与 `geo-ip`/`limit_by_per_ip` 的取值链路关系。**不足以支撑对客答复。**
8. **`developing-gateway-plug-ins-using-rust-and-c-languages` 页信息量不足**：515 字节，仅两条 GitHub 外链。无版本要求、无编译命令、无工具链、无本地调试、无与 Go 的能力差异、无网关版本适配要求。**不足以支撑对客答复。**
9. **插件形态鉴权 vs 内置消费者鉴权机制的叠加与执行顺序**：`[文档未说明]`。总表 45 行中**没有任何一行**标注为「内置消费者鉴权」。唯一对比句只覆盖 jwt-auth 一个插件（见 §9.4.1）。→ 需 W4 补齐或由主控裁决。
10. **插件 YAML 的 `consumers` 与控制台「消费者」对象是否同一实体**：`[文档未说明]`。本章 6 个认证插件全部是内联定义凭证，未见引用控制台消费者对象的语法。

**🟠 P1 级空白**

11. **`DownstreamConnectionBufferLimits` 的默认值与可调上限**：`request-block-plugin` 与 `hmac-auth-plug-ins` 都要求客户「在参数配置页调高此项」并警告「网关内存使用将有显著增加」，但**没给默认值、上限、内存增量数字**（属引擎参数，应归 W1）。
12. **`key-rate-limit` 的计数底座**（单机还是集群）、**拒绝响应状态码/响应体**、**额度回传响应头** —— 全部 `[文档未说明]`（对比 cluster 版有完整定义）。
13. **`ai-transformer` 是否支持流式（SSE）响应**、LLM 调用失败/超时的降级行为、转换结果正确性保证 —— `[文档未说明]`。这对 AI 网关是核心场景。
14. **`jwt-logout` 在 Redis 不可用时的降级策略**（放行还是拒绝）：官方只给 500 错误码，无开关 → `[文档未说明]`。可用性风险点。
15. **MCP 工具级插件作用域**：34 页查无。`manage-plug-ins` 只把 MCP 与路由合并为「MCP/路由级」一类。
16. **WebIDE / 云效仓库 / 构建流水线是否另计费**：`[文档未说明]` ← 连带计费空白。
17. **WebIDE 支持的语言**（是否只有 Go）：`[文档未说明]`。
18. **`upload-plug-in` 的「选择语言」枚举值**：`[文档未说明]`。
19. **自定义插件的安全审核/签名/扫描、发布审批、版本回滚**：`[文档未说明]`。
20. **`param-access-control` 的 `>`/`>=`/`<`/`<=` 是字符串序还是数值序比较**：官方示例用带引号的 `'2.0'`/`'3'`/`'100'`，语义 `[文档未说明]` —— 客户配错高发点。
21. **`ai-prompt-template` 的模板数量上限、`properties` 缺变量时的行为、模板名不存在时的错误码**：`[文档未说明]`。
22. **`ai-rag` 的 `topk`/`threshold` 取值范围**、`dashvector.collection` 是否必填（示例有、参数表无）：`[文档未说明]`。
23. **`waf` 插件拦截时返回的状态码**：页面无错误码表 → `[文档未说明]`。
24. **`bot-detect` 内置默认爬虫规则清单**：`[文档未说明]`（只知会误伤 Go 网络库）。
25. **`geo-ip` 地理库（ip2region）的版本与更新频率**、`${geo-isp}` 变量是否可用于提示词装饰器：`[文档未说明]`。
26. **`canary-header`「重新匹配路由」的性能开销**：`[文档未说明]`。
27. **`frontend-gray` 的 `rewrite.notFoundUri`**：示例中出现但参数表未收录 → 是否有效字段 `[文档未说明]`。
28. **`oauth` 是否支持 Client Credential 以外的授权模式**（授权码/隐式/密码/Refresh Token）：`[文档未说明]`。
29. **`hsts`/`custom-response`/`param-access-control`/`AI RAG 检索代理`/`AI检索增强生成（加强版）` 的执行阶段与优先级**：`upload-plug-in` 总表未收录 → 只能取各页自述，且 `param-access-control`(鉴权阶段/310) 与总表 bot-detect 撞号、检索代理(默认阶段/150) 与 ai-json 撞号、加强版(默认阶段/400) 与 traffic-tag 撞号。
30. **卸载插件时已配置规则能否导出/备份**：`[文档未说明]`。
31. **`_disable_: true` 是否为全插件通用字段**：仅 `jwt-auth-plug-ins` 页出现 → `[文档未说明]`。
32. **RAM 权限点**（安装/发布/卸载插件分别需要哪些 action）：`[文档未说明]`（归 W4/W7）。
