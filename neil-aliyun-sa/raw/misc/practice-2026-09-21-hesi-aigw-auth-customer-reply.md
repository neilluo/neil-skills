# 合思｜AI 网关调用自有认证接口 —— 客户答复（可直接发群）

> 面向：徐凯（北京合思 / 易快报）
> 出具：阿里云 SA｜2026-09-21
> 证据基础：阿里云官方文档全文 16 篇 + MCP 官方规范四版 + Higress 开源 README 与源码 + 火山引擎官方文档，逐条标注 `[官方]` `[规范]` `[开源]` `[竞品官方]` `[推断]`
> 🔴 发出前请先读完文末「三个必须先确认的前提」，其中第 2 条是最可能导致方案落地失败的细节

---

## 先给结论

**你的认证接口一行都不用改。**

`GET /api/mcp/personal-tokens/verify` 保持精确匹配、保持用 `Authorization` 头收你的 PAT——这两个都能满足。你之前踩的 404 是「自建鉴权」这个功能的设计行为，不是 bug，也不是你的服务有问题；而 ext-auth 插件里有一个模式专门解决这件事，之前群里没提到。

---

## 一、404 的根因：官方设计行为，杨小威的诊断是对的

`[官方]`《配置自建认证鉴权》原文（help.aliyun.com，我已核对全文）：

> 假设自建鉴权服务的鉴权API是 `/validateToken`，那么鉴权请求的真实Path是**鉴权API加上原始业务请求的Path后的结果**，即 `/validateToken/order`。

> **鉴权API**｜设置鉴权服务提供的鉴权API的Path，**API的Path需是前缀匹配**。例如……对外开放的鉴权API为 `/check`，那么处理 `/check/*` 的请求设置如下：`@RequestMapping("/check/")`

所以「自建鉴权」这条路**在产品设计上就要求你的认证接口是前缀处理器**。你的接口是精确匹配，网关拼出来的 `/api/mcp/personal-tokens/verify/mcp-servers/hose-release?sessionId=...` 自然命中不了 → 404。

你的立场我们认同：**网关不应该要求你改自己的认证契约。** 这条路不用继续走，换下面的方案。

---

## 二、解法：ext-auth 插件的 `forward_auth` 模式

`[开源]` ext-auth 插件有两种 `endpoint_mode`，差别正好就在路径怎么处理（Higress 源码 `plugins/wasm-go/extensions/ext-auth/main.go`）：

```go
requestMethod := httpServiceConfig.RequestMethod
requestPath := httpServiceConfig.Path
if httpServiceConfig.EndpointMode == config.EndpointModeEnvoy {
    requestMethod = ctx.Method()
    requestPath = path.Join(httpServiceConfig.PathPrefix, ctx.Path())
}
```

| 模式 | 路径行为 | 适合你吗 |
|---|---|---|
| `envoy`（默认） | `path_prefix` + **拼接原始业务路径** | ❌ 和「自建鉴权」同一个坑 |
| **`forward_auth`** | **固定 `path` 原样发出，不拼接** | ✅ **就是你要的** |

`forward_auth` 模式下，原始请求信息通过请求头传给你的认证服务，而不是拼进 URL：

`[开源]` 官方抓包示例（鉴权服务实际收到的请求）：

```
POST /auth HTTP/1.1
Host: ext-auth.backend.svc.cluster.local
Authorization: xxx
X-Forwarded-Proto: HTTP
X-Forwarded-Host: foo.bar.com
X-Forwarded-Uri: /users?apikey=9a342114-ba8a-11ec-b1bf-00163e1250b5
X-Forwarded-Method: GET
Content-Length: 0
```

注意 `X-Forwarded-Uri` **带 query**，所以你的 `sessionId` 参数能完整拿到。自动附加的头共 6 个：`x-forwarded-proto` / `x-forwarded-method` / `x-forwarded-host` / `x-forwarded-uri`，外加两个兼容旧版的 `x-original-method` / `x-original-uri`。

### 关键好消息：你的 `Authorization` 头会被无条件透传

`[开源]` 源码里这段逻辑在 `endpoint_mode` 分支**之外**、也在 `allowed_headers` 循环**之外**：

```go
// Add the Authorization header if present
authorization := util.ExtractFromHeader(reqHeaders, HeaderAuthorization)
if authorization != "" { extAuthReqHeaders.Set(HeaderAuthorization, authorization) }
```

意思是：**只要客户端请求带了 `Authorization`，插件就原样转发给你的认证服务，与用哪种 endpoint_mode、与 `allowed_headers` 怎么配都无关。** 你的 PAT 校验逻辑不用动。

---

## 三、`service_name` 填什么（你最初的问题）

`service_name` **不是域名、不是 IP、不是裸服务名**，而是**网关「服务列表」里那条已注册服务的、带服务类型后缀的完整 FQDN**。

`[官方]` 唯一原文佐证（云原生API网关与 AI 网关两份《Go 语言开发网关插件》第 462 行逐字相同）：

> `// 带服务类型的完整 FQDN 名称，例如 my-svc.dns, my-svc.static, service-provider.DEFAULT-GROUP.public.nacos, httpbin.my-ns.svc.cluster.local`

`[开源]` Higress ext-auth README 对该字段的定义：

> `service_name`｜string｜必填｜输入授权服务名称，带服务类型的完整 FQDN 名称，例如 `ext-auth.dns` 、`ext-auth.my-ns.svc.cluster.local`

| 你的认证服务在哪 | 服务来源类型 | `service_name` 格式 |
|---|---|---|
| 公网/自有域名（**你的情况**） | **DNS 域名** | `<服务名>.dns` |
| VPC 内固定 IP | 固定地址 | `<服务名>.static` |
| MSE Nacos 注册 | MSE Nacos | `<服务名>.<分组>.<命名空间ID>.nacos` |
| ACK / K8s | 容器服务 | `<svc>.<namespace>.svc.cluster.local` |

### 🔴 铁律：不要自己拼，去「服务列表」抄

`[实战]` Higress 核心维护者 FAQ 原话：

> 针对要通过 IP 或域名访问的服务，我们需要为其创建对应的服务来源，然后**到服务列表中查看它所对应的服务名称和服务端口。这两个信息也是我们需要写入 Wasm 插件的配置里的**。

填 IP 或裸域名的后果是明确报错（真实案例）：

```
failed to call ext auth server: error status returned by host: bad argument
```

维护者解释：「`bad argument` 错误在绝大部分场景下都是由于配置了网关并不知晓的服务信息。Wasm 插件只能请求网关拿到的 Cluster 信息，而不能直接指定目标服务的地址和端口来请求。」底层机制是插件用 `FQDNCluster{FQDN: serviceName, Port: servicePort}` 定位后端，集群名拼成 `outbound|<Port>||<FQDN>`——名字或端口对不上就找不到 cluster。

### 前置步骤：先把认证接口注册进网关

`[官方]`《创建服务》DNS 域名来源参数：

> **服务来源**：选择 **DNS域名**。**服务名称**：自定义服务名称。**服务地址**：格式为 `<DNS域名>:<服务端口>`，支持填写多个，以英文 `,` 分隔。
> **重要**：如果指定的是外网地址，需要配置NAT网关。
> **TLS模式**：默认关闭。（关闭 / 单向TLS / 双向TLS(mTLS)）

路径：控制台 → **实例** → 选地域 → 点目标实例 ID → 左侧 **服务** → **创建服务** → 选 **服务来源** 并配参数 → **确定**。

端口口径说明：阿里云控制台的 DNS 来源**没有独立端口字段**，端口写在「服务地址」里；插件里的 `service_port` 填同一个值，**最终以「服务列表」页面显示的服务端口为准**。

⚠️ `[官方]`+`[实战]` 如果你改用**固定地址（static）**类型，注意其生成的服务端口**固定为 80**（官方代码注释「静态IP类型服务的逻辑端口是80」+ 维护者 FAQ + 内部实测三源一致），真实端口写在来源地址的 `ip:port` 里。**建议直接用 DNS 域名来源绕开这个坑。**

---

## 四、`initialize` / `tools/list` 能不能过鉴权

先纠正一个之前群里的说法。9/20 有同学答复「tools/call 能走外部认证插件，initialize 和 tools/list 不行」——**这个说法我们在官方文档里找不到任何依据，而且有一条官方原文与它冲突**：

`[官方]`《调试MCP服务》原文：

> 如果所选消费者只授权了 MCP工具级别消费者认证，且仅授权某些工具的情况下，**HTTP转MCP的场景中获取工具列表只能看到和调用有权限的工具**；直接代理场景调试的时候能看到全部工具，选择授权的工具调用是ok的，没权限的会403。

也就是说，**在 HTTP 转 MCP 场景下，工具级鉴权本来就是作用于 `tools/list` 的**（表现为按权限过滤工具列表）。

更根本的是协议层：

`[规范]` MCP 官方规范（最新 2026-07-28，四版一致）：

> The Model Context Protocol provides authorization capabilities **at the transport level**.

> The server **MUST** provide a single HTTP endpoint path (hereafter referred to as the **MCP endpoint**) that supports both POST and GET methods.

> Every JSON-RPC message sent from the client **MUST** be a new HTTP POST request to the MCP endpoint.

规范甚至显式预设了网关介入——它要求把 body 里的字段镜像到 HTTP 头，目的是「so that **intermediaries (load balancers, gateways**, observability tooling) can route and inspect requests without parsing the body」。

**推论 `[推断]`（推理链条如上，可验证）**：`initialize`、`tools/list`、`tools/call` 在 HTTP 层是**同一个 path、同一个 POST**，网关在 HTTP 层**物理上无法区分**它们。而 ext_authz 是一个 HTTP filter，跑在 MCP 协议解析之前。所以只要 ext-auth 挂在一个能匹配到这些请求的作用域上，三个方法应当**一起被拦**。

你说的「MCP 官网定义 tools/list 也需要认证」——**结论正确，表述可以更精确**：规范没有按方法名列举鉴权要求（它把鉴权放在传输层，因此天然覆盖所有方法），并且规范里**不存在任何"免鉴权方法"白名单**（我们在 authorization 四个版本、transports、lifecycle、server/tools、security_best_practices 全文检索 `unprotected` / `anonymous` / `without auth`，**0 命中**）。规范只允许**服务器级**整体关闭鉴权（「Authorization is OPTIONAL for MCP implementations」），不允许方法级豁免。

### 挂载维度建议

`[官方]` 插件规则三级作用域（均为 HTTP 层匹配，无一是 MCP 方法感知的）：

> **MCP/路由级插件规则**：作用在路由上，当请求匹配到指定路由时，规则生效。
> **域名级插件规则**：作用在域名上，特定域名的匹配优先级高于泛域名。
> **实例级插件规则**：作用在网关全局，当路由和域名级规则都没有匹配到的时候则匹配该规则。

**建议挂域名级**，域名精确填写 MCP 接入点域名，**不要用通配符 `*`**；保存后确认规则页显示「当前生效状态：已生效」。

⚠️ `[实战]` 内部有一条实测记录称「实例级规则是兜底规则，在自定义 HTTP 类型 Model API 链路上可能不触发」——**注意这条实测的限定条件是 Model API 链路，不是 MCP 链路，不能直接外推**。但保守起见，**别依赖实例级兜底，优先域名级**。

⚠️ `[实战]` 另一条维护者经验：「只要有一个插件的配置加载异常，两个插件的配置都不会正常生效」——YAML 写错会连带其他插件一起失效，配完务必确认生效状态。

---

## 五、🔴 发出/实施前必须先确认的三件事

**1. 实例形态：专享还是 Serverless？**
`[官方]`《插件安装启用与卸载》原文：

> **仅专享实例型AI网关支持安装与启用插件，Serverless版不支持。**

如果你是 AI 网关 Serverless 版，ext-auth **根本装不了**，那就要走别的路（见第七节兜底方案）。你既然已经在配这个插件，大概率是专享实例，但请确认一次。

**2. `Authorization` 的值是裸 PAT 还是带 `Bearer ` 前缀？（最可能导致失败的细节）**
你的 curl 里是 `Authorization: <裸 PAT>`。但 MCP 客户端普遍按规范走 Bearer 认证——`[官方]`《调试MCP服务》里 MCP Inspector 的配置就是「`Header Name` 为 `Authorization`……在 **`Bearer Token`** 中填入」，也就是说客户端很可能发出 `Authorization: Bearer <PAT>`。

**请确认你的 verify 接口能否容忍 `Bearer ` 前缀。** 如果不能，有两条路：①在 verify 侧做兼容（剥掉前缀，改动极小且不改契约）②让 MCP 客户端改用自定义头传 PAT，然后在插件里用 `allowed_headers` 透传，例如：

```yaml
  authorization_request:
    allowed_headers:
      - exact: x-ekb-pat
```

**3. HTTPS / 443 是否验证过？**
`[官方]` 自定义 Wasm 插件出站「目前仅支持 http 调用」；ext-auth 用的是同一套 wrapper client，**到 443 的 TLS 出站官方未明确说明，需实测**。你的认证服务是 HTTPS，如果实测不通，备选是：在内网暴露一个 HTTP 的 verify 端点专供网关调用（走 VPC 内网，不对公网开放），或前置一层。

---

## 六、可直接抄的配置

前提：已在「服务」里创建 DNS 域名来源服务（服务名称假定为 `hesi-auth`，服务地址 `<你的认证域名>:443`）。
**`service_name` 和 `service_port` 请去「服务列表」核对实际生成值后再填。**

```yaml
http_service:
  endpoint_mode: forward_auth              # 关键：固定 path，不拼接
  endpoint:
    service_name: hesi-auth.dns            # ← 换成服务列表里的实际值 + .dns
    service_port: 443
    service_host: <你的认证服务域名>        # 请求鉴权服务时的 Host 头
    path: /api/mcp/personal-tokens/verify  # 你的精确路径，一行不改
    request_method: GET                    # 与你的接口一致
  timeout: 3000                            # 单位毫秒（注意不是秒）
  # authorization_request 不用配：Authorization 头源码里无条件透传
  authorization_response:
    allowed_upstream_headers:
      - exact: x-user-id                   # 可选：把身份透传给后端 tools
failure_mode_allow: false                  # 严格模式：鉴权服务不可用则拒绝
status_on_error: 403
# 不配 match_type / match_list → 默认白名单且为空 → 所有请求都鉴权（正是你要的）
```

### 🔴 三个配置陷阱（都验证过源码）

**① 千万不要配 `with_request_body: true`。** `[开源]` 源码：

```go
if withRequestBody.Bool() && (httpService.RequestMethod == http.MethodGet || ...Options || ...Head) {
    return errors.New(fmt.Sprintf("requestMethod %s does not support with_request_body set to true", httpService.RequestMethod))
}
```

`request_method: GET` + `with_request_body: true` → **配置解析直接失败，插件整个加载不起来**。你的 verify 是 GET 且只需要 Authorization 头，本来也不需要 body。

**② `timeout` 单位是毫秒。** 「自建鉴权」那边的超时单位是**秒**（默认 10），插件这边是**毫秒**（默认 1000）。如果照习惯填 `timeout: 10`，就是 10 毫秒 → 全部超时 → 配合默认 fail-closed 直接全站 403。

**③ `match_type` / `match_list` 必须与 `http_service` 同级。** `[实战]` 维护者原话：「`match_type` 、 `match_list` 和 `http_service` 是一个层级的。」嵌进 `http_service` 里面会导致白名单**静默失效**（不报错，但行为不对）。

### 失败策略要你拍板

`[开源]` ext-auth 默认是 **fail-closed**：鉴权服务不可达或返 5xx → 用 `status_on_error`（默认 **403**）拒绝客户端。
`failure_mode_allow: true` 可改成放行，但**它只对 ≥500 生效**（源码 `if statusCode >= http.StatusInternalServerError && config.FailureModeAllow`）——你的认证服务返 400/404 时，即使开了也照样按原状态码拒绝。另外连接失败（超时、连不上）在源码里被当作 500 处理，所以那种情况下 `failure_mode_allow: true` 是会放行的。

「自建鉴权」那边对应的是**宽松/严格模式**，官方「建议您使用宽松模式」。**这个取舍要你们安全和业务一起定**：严格模式安全，但你的认证服务一抖动，整个 MCP 服务就全挂。

---

## 七、验证步骤（按顺序做）

1. 「服务」页面能看到你注册的认证服务，且**服务列表显示的服务名称与端口**和插件里填的一致
2. 插件规则页显示「**当前生效状态：已生效**」
3. 从网关所在 VPC 内 `telnet <认证域名> 443` 通（外网地址确认已配 NAT 网关）；连通性用 `telnet`/`nc`，**不要用 `ping`**
4. **分别测三个 MCP 方法**：`initialize`、`tools/list`、`tools/call`，逐个确认是否被拦到鉴权（这是本方案唯一需要现场证伪的开放点，见第四节）
5. 不带 token 请求 → 应返回你的 verify 给的 401/403
6. 带合法 PAT 请求 → 应 200 且能正常走到 tools
7. 查你认证服务的访问日志：确认收到的**请求行是 `GET /api/mcp/personal-tokens/verify`**（没有被拼接）、`Authorization` 头的值格式符合预期（有无 `Bearer ` 前缀）、`X-Forwarded-Uri` 里能拿到原始路径和 `sessionId`
8. **故意停掉认证服务**再请求 → 确认行为符合你选的失败策略

---

## 八、如果域名级仍拦不到 `initialize` / `tools/list`，三条兜底（按推荐序）

**① 双层组合 `[推断]`（架构可行，未实测）**
外层用 **MCP 服务级消费者认证**（`[官方]` 明确覆盖连接与列工具阶段），内层用 ext-auth 回调你的 PAT 校验。
🔴 **关键坑**：两者都会抢 `Authorization` 头。`[官方]` `ApiKeyIdentityConfig` 支持 `apikeySource` = Header / Query String，且「仅AI网关Header模式允许1-3项」→ **把网关的 API Key 放到独立头或 query 里，`Authorization` 留给你的 PAT。**

**② 鉴权下沉**
`[官方]` HTTP转MCP 的工具定义（Swagger/OpenAPI3 导入或自定义 YAML）**存放在网关**，`tools/list` 由网关按 YAML 直接应答、**不回调你的后端**；只有 `tools/call` 才真正打到你的服务。所以可以让网关层负责 `initialize`/`tools/list`，你在自己的 MCP 后端强制校验 PAT 兜住 `tools/call`。

**③ 自定义 Wasm 插件**
`[官方]` 发布自定义插件可「设置插件标识、**执行阶段(认证/鉴权/统计/默认)与执行优先级**」。Wasm 在 `ProcessRequestHeadersBy` 阶段工作，早于 MCP JSON-RPC 分发，可拦全部方法。内部已有端到端验证的先例。注意 `[官方]` Wasm 出站「目前仅支持 http 调用」，鉴权服务需注册为网关服务（FQDN）。

---

## 九、我们必须如实告知你的边界（不粉饰）

1. **`tools/list` 在 HTTP转MCP 下不触达你的业务系统**——它返回的是网关里存的工具目录。但它**会泄露工具元数据**（工具名、参数 schema），所以"无需鉴权"不成立，我们也不这么认为。
2. **`ext-auth` 在 help.aliyun.com 上没有对应文档**。我们在 apig / ai-gateway / mse / api-gateway 四条产品线的官方文档全量索引里检索 `外部认证`、`ext-auth`、`service_name`，**命中数全部为 0**；官方「认证鉴权」插件清单只有 key-auth / basic-auth / hmac-auth / jwt-auth / jwt-logout / oauth 六个，**不含 ext-auth**。你控制台看到的「外部认证」是**插件市场里的 Higress 插件**（`[官方]` 明说插件市场的来源包含「官方插件：Higress官方开放的插件」「社区插件：Higress社区贡献的插件」），所以它的字段 schema 权威出处只有 Higress 开源——**这不是你查漏了**。这也意味着走这条路时，工单支持链路会比用官方产品化能力弱，我们如实说明。
3. **商业版插件是否完整支持 `forward_auth` 需实测**。我们的证据来自 Higress 开源主干；`[开源]` 源码里 `x-original-*` 两个头带「Compatible with older versions」注释，说明 `X-Forwarded-*` 是较新能力。最新公开引擎版本 2.1.23（2026-09-03）。**上线前请在你的实例上实测一次。**
4. **域名级能否拦到全部三个 MCP 方法，官方无任何正反表述**，属于架构推断（第四节推理链条），需按第七节第 4 步实测。

---

## 附：如果你更想要"官方产品化能力"而不是插件

`[官方]`「安全管理 → 全局认证鉴权 → 创建鉴权 → 鉴权类型：**自建的鉴权服务**」这条路**没有 `service_name` 输入框**（鉴权服务是下拉选择），文档齐全、有明确支持口径、也不受「Serverless 不支持插件」限制。它的能力包括：

- 鉴权结果判定：**200 放行**，**401/403 直接把鉴权服务响应回给客户端**；若你的服务必须统一返 200，用内置头 **`x-mse-external-authz-check-result`**（`true` 放行 / `false` 拒绝）
- 允许携带的头部：Host、Method、Path、Content-Length **默认自动添加**，无需手填
- 授权规则表达力：白/黑名单 + 路径（精确 / 前缀 `/app/*` / 正则 Re2）+ 请求头（9 种操作符：等于/不等于/存在/不存在/包含/不包含/前缀/后缀/正则）+ **复杂条件（Envoy permission YAML，支持与/或/非组合）**
- 建完**必须手动点「开启」**才生效（很多人配完不生效就是漏了这步）

**它唯一的、也是致命的限制就是第一节那个前缀拼接语义**——「鉴权API」必须是你接口的前缀，官方控制台没有提供"精确固定路径"选项。所以在你的场景下它不适用，我们才推荐 ext-auth + `forward_auth`。这个产品缺口我们已经记录并会向产研提出（增加"鉴权路径匹配模式"选项）。

---

## 引用出处

**阿里云官方文档**（全文已归档）
- [配置自建认证鉴权 - 云原生API网关](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/configure-self-built-authentication)
- [配置自建认证鉴权 - AI网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/configure-self-built-authentication)
- [调试MCP服务 - AI网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/debug-mcp-services)
- [Go语言开发网关插件 - 云原生API网关](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/develop-plug-ins-in-go)（FQDN 命名规则出处）
- [创建服务 - AI网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/creating-services)
- [插件安装启用与卸载 - AI网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/manage-plug-ins)（Serverless 限制出处）
- [管理插件 - 云原生API网关](https://help.aliyun.com/zh/api-gateway/cloud-native-api-gateway/user-guide/enable-plugin)（三级作用域出处）

**MCP 官方规范**
- [Authorization（2025-11-25）](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)
- [Streamable HTTP transport（2026-07-28）](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [Versioning — latest = 2026-07-28](https://modelcontextprotocol.io/specification/versioning)

**Higress 开源**
- [ext-auth README（VERSION 2.0.2）](https://raw.githubusercontent.com/alibaba/higress/main/plugins/wasm-go/extensions/ext-auth/README.md)
- [Wasm 插件开发 HTTP 调用（FQDN 与集群名规则）](https://higress.cn/docs/latest/plugins/wasm-dev/wasm17/)
- [维护者 FAQ](https://raw.githubusercontent.com/CH3CHO/higress-notes/main/docs/faq.md)
- [Discussion #3991（bad argument 实例）](https://github.com/higress-group/higress/discussions/3991)｜[#2142（层级说明与 Nacos 实配）](https://github.com/higress-group/higress/discussions/2142)
