<!-- source_url: https://github.com/alibaba/higress/blob/main/plugins/wasm-go/extensions/ext-auth/main.go 与 config/config.go（raw.githubusercontent.com main 分支） -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: main 分支当日拉取（未固定 commit tag；最新公开引擎版本 2.1.23 / 2026-09-03） -->
<!-- summary: Higress ext-auth 插件源码关键片段摘录（⚠️ 源码摘录而非全文，全文共 main.go 225 行 + config/config.go 430 行，按行号截取）。取证点：① endpoint_mode 分支——路径拼接只发生在 envoy 模式，forward_auth 用固定 path 原样发出；② Authorization 头无条件透传（在 endpoint_mode 分支之外、allowed_headers 循环之外）；③ forward_auth 自动附加 6 个头（x-forwarded-proto/method/host/uri + 兼容用 x-original-method/uri，注释 Compatible with older versions）；④ with_request_body 与 GET/OPTIONS/HEAD 冲突直接报错→配置解析失败插件整体不生效；⑤ 默认 fail-closed：DefaultStatusOnError=403，failure_mode_allow 只对 >=500 生效，连接失败(err!=nil)按 500 处理故超时会放行；⑥ match_list 路径匹配用不含 query 的 path（wrapper.GetRequestPathWithoutQuery）。 -->

# Higress ext-auth 插件源码关键片段（摘录）

> ⚠️ 本文件是**源码摘录**而非全文。来源：alibaba/higress 仓库 main 分支
> `plugins/wasm-go/extensions/ext-auth/main.go`（共 225 行）与
> `plugins/wasm-go/extensions/ext-auth/config/config.go`（共 430 行），2026-09-21 拉取。
> 行号为当日 main 分支行号，格式 `行号| 代码`。

## 1. main.go — endpoint_mode 分支（路径拼接只发生在 envoy 模式）

```go
  40| 	)
  41| }
  42| 
  43| const (
  44| 	HeaderAuthorization    = "authorization"
  45| 	HeaderFailureModeAllow = "x-envoy-auth-failure-mode-allowed"
  46| )
  47| 
  48| // Currently, x-forwarded-xxx headers only apply for forward_auth.
  49| const (
  50| 	HeaderOriginalMethod   = "x-original-method"
  51| 	HeaderOriginalUri      = "x-original-uri"
  52| 	HeaderXForwardedProto  = "x-forwarded-proto"
  53| 	HeaderXForwardedMethod = "x-forwarded-method"
  54| 	HeaderXForwardedUri    = "x-forwarded-uri"
  55| 	HeaderXForwardedHost   = "x-forwarded-host"
  56| )
```

```go
 108| func checkExtAuth(ctx wrapper.HttpContext, cfg config.ExtAuthConfig, body []byte, pauseAction types.Action) types.Action {
 109| 	httpServiceConfig := cfg.HttpService
 110| 
 111| 	extAuthReqHeaders := buildExtAuthRequestHeaders(ctx, cfg)
 112| 
 113| 	// Set the requestMethod and requestPath based on the endpoint_mode
 114| 	requestMethod := httpServiceConfig.RequestMethod
 115| 	requestPath := httpServiceConfig.Path
 116| 	if httpServiceConfig.EndpointMode == config.EndpointModeEnvoy {
 117| 		requestMethod = ctx.Method()
 118| 		requestPath = path.Join(httpServiceConfig.PathPrefix, ctx.Path())
 119| 	}
 120| 
 121| 	// Call ext auth server
 122| 	err := httpServiceConfig.Client.Call(requestMethod, requestPath, util.ReconvertHeaders(extAuthReqHeaders), body,
 123| 		func(statusCode int, responseHeaders http.Header, responseBody []byte) {
 124| 			if statusCode != http.StatusOK {
 125| 				log.Errorf("failed to call ext auth server, status: %d", statusCode)
 126| 				callExtAuthServerErrorHandler(cfg, statusCode, responseHeaders, responseBody)
 127| 				return
```

→ **推论**：forward_auth 模式用配置的固定 `path` 原样发出鉴权请求，原始路径通过 `X-Forwarded-Uri`（`ctx.Path()`，含 query）传递；envoy 模式才做 `path.Join(PathPrefix, ctx.Path())` 前缀拼接。

## 2. main.go — Authorization 头无条件透传 + forward_auth 自动附加头

```go
 166| 	for key, value := range requestConfig.HeadersToAdd {
 167| 		extAuthReqHeaders.Set(key, value)
 168| 	}
 169| 
 170| 	// Add the Authorization header if present
 171| 	authorization := util.ExtractFromHeader(reqHeaders, HeaderAuthorization)
 172| 	if authorization != "" {
 173| 		extAuthReqHeaders.Set(HeaderAuthorization, authorization)
 174| 	}
 175| 
 176| 	// Add filter properties forwarding
 177| 	if requestConfig.AllowedProperties != nil {
 178| 		for _, prop := range requestConfig.AllowedProperties {
 179| 			if raw, err := proxywasm.GetProperty(prop.Path); err == nil {
 180| 				extAuthReqHeaders.Set(prop.Header, string(raw))
 181| 			}
 182| 		}
 183| 	}
 184| 
 185| 	// Add additional headers when endpoint_mode is forward_auth
 186| 	if httpServiceConfig.EndpointMode == config.EndpointModeForwardAuth {
 187| 		// Compatible with older versions
 188| 		extAuthReqHeaders.Set(HeaderOriginalMethod, ctx.Method())
 189| 		extAuthReqHeaders.Set(HeaderOriginalUri, ctx.Path())
 190| 		// Add x-forwarded-xxx headers
 191| 		extAuthReqHeaders.Set(HeaderXForwardedProto, ctx.Scheme())
 192| 		extAuthReqHeaders.Set(HeaderXForwardedMethod, ctx.Method())
 193| 		extAuthReqHeaders.Set(HeaderXForwardedUri, ctx.Path())
 194| 		extAuthReqHeaders.Set(HeaderXForwardedHost, ctx.Host())
 195| 	}
 196| 	return extAuthReqHeaders
```

→ **关键**：`Authorization` 透传逻辑在 `endpoint_mode` 分支**之外**、也在 `allowed_headers` 循环**之外**——只要原始请求带 Authorization 就透传，与 endpoint_mode 和 allowed_headers 均无关。**推论：客户自有 PAT 校验逻辑一行不用改。**
→ forward_auth 自动附加头共 6 个：`x-forwarded-proto/method/host/uri` + 兼容用的 `x-original-method/uri`（源码注释「Compatible with older versions」——说明 `X-Forwarded-*` 是较新能力，商业版是否含此逻辑存疑，上线前必须实测）。

## 3. main.go — match_list 路径匹配用不含 query 的 path

```go
  84| 	request := expr.RequestAttributes{
  85| 		Domain: ctx.Host(),
  86| 		Method: ctx.Method(),
  87| 		Path:   wrapper.GetRequestPathWithoutQuery(),
  88| 	}
  89| 	if !matchRules.RequiresRequestHeaders() {
  90| 		return request, nil
  91| 	}
  92| 
```

## 4. main.go — 默认 fail-closed：failure_mode_allow 只对 >=500 生效；连接失败按 500 处理

```go
 138| 
 139| 		}, httpServiceConfig.Timeout)
 140| 
 141| 	if err != nil {
 142| 		log.Errorf("failed to call ext auth server: %v", err)
 143| 		// Since the handling logic for call errors and HTTP status code 500 is the same, we directly use 500 here.
 144| 		callExtAuthServerErrorHandler(cfg, http.StatusInternalServerError, nil, nil)
 145| 		return types.ActionContinue
 146| 	}
```

```go
 199| func callExtAuthServerErrorHandler(config config.ExtAuthConfig, statusCode int, extAuthRespHeaders http.Header, responseBody []byte) {
 200| 	if statusCode >= http.StatusInternalServerError && config.FailureModeAllow {
 201| 		if config.FailureModeAllowHeaderAdd {
 202| 			_ = proxywasm.ReplaceHttpRequestHeader(HeaderFailureModeAllow, "true")
 203| 		}
 204| 		proxywasm.ResumeHttpRequest()
 205| 		return
 206| 	}
 207| 
 208| 	var respHeaders = extAuthRespHeaders
 209| 	if config.HttpService.AuthorizationResponse.AllowedClientHeaders != nil {
 210| 		respHeaders = http.Header{}
 211| 		for headK, headV := range extAuthRespHeaders {
 212| 			if config.HttpService.AuthorizationResponse.AllowedClientHeaders.Match(headK) {
 213| 				respHeaders.Set(headK, headV[0])
 214| 			}
 215| 		}
 216| 	}
 217| 
 218| 	// Rejects client requests with StatusOnError if extAuth is unavailable or returns a 5xx status.
 219| 	// Otherwise, uses the status code returned by extAuth to reject requests.
 220| 	statusToUse := statusCode
 221| 	if statusCode >= http.StatusInternalServerError {
 222| 		statusToUse = int(config.StatusOnError)
 223| 	}
 224| 	_ = util.SendResponse(uint32(statusToUse), "ext-auth.unauthorized", respHeaders, responseBody)
 225| }
```

→ 授权服务返 4xx 时按**原状态码**拒绝（不走 status_on_error、不受 failure_mode_allow 影响）；返 5xx 或连接失败时用 `status_on_error`（默认 403）拒绝，仅当 `failure_mode_allow=true` 才放行。**连接失败（含超时）被当作 500 处理，故超时会放行**（源码注释「Since the handling logic for call errors and HTTP status code 500 is the same, we directly use 500 here.」）。

## 5. config/config.go — DefaultStatusOnError=403 与 with_request_body×GET 冲突校验

```go
  14| )
  15| 
  16| const (
  17| 	DefaultStatusOnError = http.StatusForbidden
  18| 
  19| 	DefaultHttpServiceTimeout = 1000
  20| 
```

```go
 164| 			log.Warn("when endpoint_mode is envoy, endpoint request_method and path will be ignored")
 165| 		}
 166| 	case EndpointModeForwardAuth:
 167| 		requestMethodConfig := endpointConfig.Get("request_method")
 168| 		if !requestMethodConfig.Exists() {
 169| 			httpService.RequestMethod = http.MethodGet
 170| 		} else {
 171| 			httpService.RequestMethod = strings.ToUpper(requestMethodConfig.String())
 172| 		}
 173| 
 174| 		pathConfig := endpointConfig.Get("path")
 175| 		if !pathConfig.Exists() {
 176| 			return errors.New("when endpoint_mode is forward_auth, endpoint path must not be empty")
 177| 		}
 178| 		httpService.Path = pathConfig.String()
 179| 
 180| 		if endpointConfig.Get("path_prefix").Exists() {
 181| 			log.Warn("when endpoint_mode is forward_auth, endpoint path_prefix will be ignored")
 182| 		}
 183| 	}
 184| 	return nil
 185| }
 186| 
 187| func parseAuthorizationRequestConfig(json gjson.Result, httpService *HttpService) error {
 188| 	authorizationRequestConfig := json.Get("authorization_request")
 189| 	if authorizationRequestConfig.Exists() {
 190| 		var authorizationRequest AuthorizationRequest
 191| 
 192| 		allowedHeaders := authorizationRequestConfig.Get("allowed_headers")
 193| 		if allowedHeaders.Exists() {
 194| 			result, err := expr.BuildRepeatedStringMatcherIgnoreCase(allowedHeaders.Array())
 195| 			if err != nil {
 196| 				return err
 197| 			}
 198| 			authorizationRequest.AllowedHeaders = result
 199| 		}
 200| 
 201| 		authorizationRequest.HeadersToAdd = convertToStringMap(authorizationRequestConfig.Get("headers_to_add"))
 202| 
 203| 		withRequestBody := authorizationRequestConfig.Get("with_request_body")
 204| 		if withRequestBody.Exists() {
 205| 			// withRequestBody is true and the request method is GET, OPTIONS or HEAD
 206| 			if withRequestBody.Bool() &&
 207| 				(httpService.RequestMethod == http.MethodGet || httpService.RequestMethod == http.MethodOptions || httpService.RequestMethod == http.MethodHead) {
 208| 				return errors.New(fmt.Sprintf("requestMethod %s does not support with_request_body set to true", httpService.RequestMethod))
 209| 			}
 210| 			authorizationRequest.WithRequestBody = withRequestBody.Bool()
 211| 		}
 212| 
```

→ 🔴 **`with_request_body: true` 与 GET/OPTIONS/HEAD 冲突会导致 `ParseConfig` 返回 error → 配置解析失败、插件整体不生效**。且 forward_auth 下 `request_method` 缺省即 GET（第 169 行）；envoy 模式 `RequestMethod` 为空串——**该校验只在 forward_auth 触发**。另注意 Higress 维护者口径：「只要有一个插件的配置加载异常，两个插件的配置都不会正常生效」。
