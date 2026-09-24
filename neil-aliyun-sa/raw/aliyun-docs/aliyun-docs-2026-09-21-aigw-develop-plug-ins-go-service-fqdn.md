<!-- source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/develop-gateway-plug-ins-using-the-go-language -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2026-04-23 -->
<!-- summary: AI 网关「Go 语言开发网关插件」官方全文。与云原生API网关版本同样包含服务 FQDN 命名规则原文注释（my-svc.dns / my-svc.static / *.nacos / *.svc.cluster.local），用于证明 AI 网关侧口径一致。 -->

开发网关插件可以扩展AI网关的核心功能，使其能够满足更加复杂和特定的业务需求。本文介绍如何使用Go语言开发网关插件，并提供本地开发和调试的指引。  
**重要**

Higress 已完成从 TinyGo 0.29 + Go 1.20 编译方案迁移至 Go 1.24 原生支持的 Wasm 编译。Go 1.24 版本现已原生支持 Wasm 文件编译。

对于此前使用 TinyGo 编译插件的用户，若需迁移到 Go 1.24 编译模式，除调整 go.mod 中的依赖外，还需将插件初始化逻辑由 main 函数移至 init 函数。具体示例请参考后续文档内容。

针对原有 TinyGo 实现的插件，还需注意以下适配事项：

1. 若在 Header 处理阶段调用外部服务并返回 type.ActionPause，需改为返回 types.HeaderStopAllIterationAndWatermark。相关实现可参考后文提供的插件调用外部服务示例。

2. 若因 TinyGo 对标准库 regexp 支持不完整而使用了 go-re2 库，现应替换为 Go 官方 regexp 包。

## 工具准备
需要先安装 Golang。

### Golang

官方[指引链接](https://go.dev/doc/install)（需为1.24版本以上）。  
**说明**

使用 Go 1.24 编译的插件需要AI网关版本不低于`2.1.5`，低版本网关参考[使用 GO 语言开发 WASM 插件](https://github.com/higress-group/higress-group.github.io/blob/1e3810e569f80327c3cbe3e38c95110e66535891/src/content/docs/latest/zh-cn/user/wasm-go.md)。

### Windows

* 下载[安装文件](https://go.dev/dl/go1.24.4.windows-amd64.msi)。

* 打开下载好的安装文件直接安装，默认会安装到 `Program Files` 或 `Program Files (x86)` 目录。

* 安装成功后，使用键盘上的快捷键Win+R打开运行窗口，在运行窗口中输入`cmd`单击**确定** 即可打开命令窗口，输入命令`go version`，成功输出当前安装的版本，表明安装成功。

### MacOS

* 下载[安装文件](https://go.dev/dl/go1.24.4.darwin-amd64.pkg)。

* 打开下载好的安装文件双击进行安装，默认会安装到`/usr/local/go`目录。

* 打开终端命令行工具，输入命令`go version`，成功输出当前安装的版本，表明安装成功。

### Linux

* 下载[安装文件](https://go.dev/dl/go1.24.4.linux-amd64.tar.gz)。

* 执行下列命令进行安装。

  * 安装Golang。

    ```
    HELPCODEESCAPE-bash
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.24.4.linux-amd64.tar.gz
    ```

  * 配置环境变量。

    ```
    HELPCODEESCAPE-bash
    export PATH=$PATH:/usr/local/go/bin
    ```

  * 执行`go version`，成功输出当前安装的版本，表明安装成功。

## 编写插件
### 初始化工程目录

1. 新建一个工程目录文件，例如`wasm-demo-go`。

2. 在所建目录下执行以下命令，进行 Go 工程初始化。

   ```
   HELPCODEESCAPE-go
   go mod init wasm-demo-go
   ```

3. 国内环境可能需要设置下载依赖包的代理。

   ```
   HELPCODEESCAPE-go
   go env -w GOPROXY=https://proxy.golang.com.cn,direct
   ```

4. 下载构建插件的依赖。

   ```
   HELPCODEESCAPE-go
   go get github.com/higress-group/proxy-wasm-go-sdk@go-1.24
   go get github.com/higress-group/wasm-go@main
   go get github.com/tidwall/gjson
   ```

### 编写 main.go 文件

下面是一个简单示例，实现了在插件配置`mockEnable: true`时直接返回`hello world`应答；未做插件配置，或者设置`mockEnable: false`时给原始请求添加 `hello: world`请求头。更多例子请参考本文第四节。  
**说明** 注意：在网关控制台中的插件配置为 yaml 格式，下发给插件时将自动转换为 json 格式，所以例子中的 parseConfig 可以直接从 json 中解析配置。

```
HELPCODEESCAPE-go
package main

import (
  "github.com/higress-group/wasm-go/pkg/wrapper"
  logs "github.com/higress-group/wasm-go/pkg/log"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm/types"
  "github.com/tidwall/gjson"
)

func main() {}

func init() {
  wrapper.SetCtx(
    // 插件名称
    "my-plugin",
    // 为解析插件配置，设置自定义函数
     wrapper.ParseConfigBy(parseConfig),
    // 为处理请求头，设置自定义函数
    wrapper.ProcessRequestHeadersBy(onHttpRequestHeaders),
  )
}

// 自定义插件配置
type MyConfig struct {
  mockEnable bool
}

// 在控制台插件配置中填写的yaml配置会自动转换为json，此处直接从json这个参数里解析配置即可
func parseConfig(json gjson.Result, config *MyConfig, log logs.Log) error {
  // 解析出配置，更新到config中
  config.mockEnable = json.Get("mockEnable").Bool()
  return nil
}

func onHttpRequestHeaders(ctx wrapper.HttpContext, config MyConfig, log logs.Log) types.Action {
  proxywasm.AddHttpRequestHeader("hello", "world")
  if config.mockEnable {
    proxywasm.SendHttpResponse(200, nil, []byte("hello world"), -1)
  }
  return types.HeaderContinue
}
```

#### **HTTP 处理挂载点**

上面示例代码中通过 `wrapper.ProcessRequestHeadersBy`将自定义函数 `onHttpRequestHeaders`用于`HTTP 请求头处理阶段`处理请求。除此之外，还可以通过下面方式，设置其他阶段的自定义处理函数。
<table> <thead> <tr> <td><p><b>HTTP 处理阶段</b></p></td> <td><p><b>触发时机</b></p></td> <td><p><b>挂载方法</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>HTTP 请求头处理阶段</p></td> <td><p>网关接收到客户端发送来的请求头数据时</p></td> <td><p><code>wrapper.ProcessRequestHeadersBy</code></p></td> </tr> <tr> <td><p>HTTP 请求 Body 处理阶段</p></td> <td><p>网关接收到客户端发送来的请求 Body 数据时</p></td> <td><p><code>wrapper.ProcessRequestBodyBy</code></p></td> </tr> <tr> <td><p>HTTP 应答头处理阶段</p></td> <td><p>网关接收到后端服务响应的应答头数据时</p></td> <td><p><code>wrapper.ProcessResponseHeadersBy</code></p></td> </tr> <tr> <td><p>HTTP 应答 Body 处理阶段</p></td> <td><p>网关接收到后端服务响应的应答 Body 数据时</p></td> <td><p><code>wrapper.ProcessResponseBodyBy</code></p></td> </tr> </tbody> </table>

#### **工具方法**

上面示例代码中的 `proxywasm.AddHttpRequestHeader` 和 `proxywasm.SendHttpResponse`是插件 SDK 提供的两个工具方法，主要的工具方法见下表。

<br />

<table> <thead> <tr> <td><p><b>分类</b></p></td> <td><p><b>方法名称</b></p></td> <td><p><b>用途</b></p></td> <td><p><b>可以生效的</b></p><p><b>HTTP 处理阶段</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>请求头处理</p></td> <td><p>GetHttpRequestHeaders</p></td> <td><p>获取客户端请求的全部请求头</p></td> <td><p>HTTP 请求头处理阶段</p><p></p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpRequestHeaders</p></td> <td><p>替换客户端请求的全部请求头</p></td> <td><p>HTTP 请求头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>GetHttpRequestHeader</p></td> <td><p>获取客户端请求的指定请求头</p></td> <td><p>HTTP 请求头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>RemoveHttpRequestHeader</p></td> <td><p>移除客户端请求的指定请求头</p></td> <td><p>HTTP 请求头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpRequestHeader</p></td> <td><p>替换客户端请求的指定请求头</p></td> <td><p>HTTP 请求头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>AddHttpRequestHeader</p></td> <td><p>新增一个客户端请求头</p></td> <td><p>HTTP 请求头处理阶段</p></td> </tr> <tr> <td><p>请求 Body 处理</p></td> <td><p>GetHttpRequestBody</p></td> <td><p>获取客户端请求 Body</p></td> <td><p>HTTP 请求 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>AppendHttpRequestBody</p></td> <td><p>将指定的字节串附加到客户端请求 Body 末尾</p></td> <td><p>HTTP 请求 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>PrependHttpRequestBody</p></td> <td><p>将指定的字节串附加到客户端请求 Body 的开头</p></td> <td><p>HTTP 请求 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpRequestBody</p></td> <td><p>替换客户端请求 Body</p></td> <td><p>HTTP 请求 Body 处理阶段</p></td> </tr> <tr> <td><p>应答头处理</p></td> <td><p>GetHttpResponseHeaders</p></td> <td><p>获取后端响应的全部应答头</p></td> <td><p>HTTP 应答头处理阶段</p><p></p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpResponseHeaders</p></td> <td><p>替换后端响应的全部应答头</p></td> <td><p>HTTP 应答头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>GetHttpResponseHeader</p></td> <td><p>获取后端响应的指定应答头</p></td> <td><p>HTTP 应答头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>RemoveHttpResponseHeader</p></td> <td><p>移除后端响应的指定应答头</p></td> <td><p>HTTP 应答头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpResponseHeader</p></td> <td><p>替换后端响应的指定应答头</p></td> <td><p>HTTP 应答头处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>AddHttpResponseHeader</p></td> <td><p>新增一个后端响应头</p></td> <td><p>HTTP 应答头处理阶段</p></td> </tr> <tr> <td><p>应答 Body 处理</p></td> <td><p>GetHttpResponseBody</p></td> <td><p>获取客户端请求 Body</p></td> <td><p>HTTP 应答 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>AppendHttpResponseBody</p></td> <td><p>将指定的字节串附加到后端响应 Body 末尾</p></td> <td><p>HTTP 应答 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>PrependHttpResponseBody</p></td> <td><p>将指定的字节串附加到后端响应 Body 的开头</p></td> <td><p>HTTP 应答 Body 处理阶段</p></td> </tr> <tr> <td><p></p></td> <td><p>ReplaceHttpResponseBody</p></td> <td><p>替换后端响应 Body</p></td> <td><p>HTTP 应答 Body 处理阶段</p></td> </tr> <tr> <td><p>HTTP 调用</p></td> <td><p>DispatchHttpCall</p></td> <td><p>发送一个 HTTP 请求</p></td> <td><p>-</p></td> </tr> <tr> <td><p></p></td> <td><p>GetHttpCallResponseHeaders</p></td> <td><p>获取 DispatchHttpCall 请求响应的应答头</p></td> <td><p>-</p></td> </tr> <tr> <td><p></p></td> <td><p>GetHttpCallResponseBody</p></td> <td><p>获取 DispatchHttpCall 请求响应的应答 Body</p></td> <td><p>-</p></td> </tr> <tr> <td><p></p></td> <td><p>GetHttpCallResponseTrailers</p></td> <td><p>获取 DispatchHttpCall 请求响应的应答 Trailer</p></td> <td><p>-</p></td> </tr> <tr> <td><p>直接响应</p></td> <td><p>SendHttpResponse</p></td> <td><p>直接返回一个特定的 HTTP 应答</p></td> <td><p>-</p></td> </tr> <tr> <td><p>流程恢复</p></td> <td><p>ResumeHttpRequest</p></td> <td><p>恢复先前被暂停的请求处理流程</p></td> <td><p>-</p></td> </tr> <tr> <td><p></p></td> <td><p>ResumeHttpResponse</p></td> <td><p>恢复先前被暂停的应答处理流程</p></td> <td><p>-</p></td> </tr> </tbody> </table>  
**重要**

请不要在请求/响应未处于Pause状态时，调用ResumeHttpRequest或调用ResumeHttpResponse。尤其注意在SendHttpResponse之后，Pause状态的请求/响应将自动恢复，若再调用ResumeHttpRequest或ResumeHttpResponse将导致未定义的行为。

### 编译生成 WASM 文件

#### **本地编译 wasm 文件**

如果使用自定义初始化的目录，执行以下命令来编译 wasm 文件。

```
HELPCODEESCAPE-go
go mod tidy
GOOS=wasip1 GOARCH=wasm go build -buildmode=c-shared -o main.wasm ./
```

成功编译后，会生成一个名为 main.wasm 的新文件。该文件将在后续的本地调试示例中使用。当需要在云原生网关市场中使用自定义插件功能时，上传此文件即可。

#### **Header 的状态管理说明**

<table> <thead> <tr> <td><p><b>Header</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>HeaderContinue</code></p></td> <td><p>表示当前 filter 已经处理完毕，可以继续交给下一个 filter 处理。 <code>types.ActionContinue</code> 对应该状态。</p></td> </tr> <tr> <td><p><code>HeaderStopIteration</code></p></td> <td><p>表示 header 还不能继续交给下一个 filter 进行处理。 但并不停止从连接读数据，继续触发 body data 的处理。 这样可以在 body data 处理阶段更新 Http 请求头内容。 如果 body data 需要交给下一个 filter 处理， 此时 header 也会被一起交给下一个 filter 处理。</p> <div> <div> <i></i> </div> <div> <strong>说明 </strong> <p>返回该状态时，要求必须有 body，如果没有 body，请求/响应将被一直阻塞。</p> <p>判断是否存在请求 body 可以使用\&nbsp;<a href="https://github.com/alibaba/higress/blob/main/plugins/wasm-go/pkg/wrapper/request_wrapper.go#L86">HasRequestBody()</a>。</p> </div> </div></td> </tr> <tr> <td><p><code>HeaderContinueAndEndStream</code></p></td> <td><p>表示 header 可以继续交给下一个 filter 处理，但下一个 filter 收到的 <code>end_stream = false</code>标记请求还未结束，以便当前 filter 再增加 body。</p></td> </tr> <tr> <td><p><code>HeaderStopAllIterationAndBuffer</code></p></td> <td><p>停止所有迭代，表示 header 不能继续交给下一个 filter，并且当前 filter 也不能收到 body data。 并对当前过滤器及后续过滤器的头部、数据和尾部进行缓冲。如果缓存大小超过了 buffer limit，在请求阶段就直接返回 413，响应阶段就直接返回 500。 同时需要调用 <code>proxywasm.ResumeHttpRequest()</code>、 <code>proxywasm.ResumeHttpResponse() </code>或者 <code>proxywasm.SendHttpResponseWithDetail()</code> 函数来恢复后续处理。</p></td> </tr> <tr> <td><p><code>HeaderStopAllIterationAndWatermark</code></p></td> <td><p>与<code>HeaderStopAllIterationAndBuffer</code>相同，区别是当缓存超过了 buffer limit 会触发流控，即暂停从连接上读数据。 0.2.1 ABI 中的 <code>types.ActionPause</code> 实际上对应就是这个状态。</p></td> </tr> </tbody> </table>  
**说明**

关于 types.HeaderStopIteration 和 HeaderStopAllIterationAndWatermark 的使用场景可以参考 Higress 官方提供 [ai-transformer 插件](https://github.com/alibaba/higress/blob/main/plugins/wasm-go/extensions/ai-transformer/main.go#L93-L99)和 [ai-quota 插件](https://github.com/alibaba/higress/blob/main/plugins/wasm-go/extensions/ai-quota/main.go#L179)。

要在 Higress 中配合 Wasmplugin CRD 或者 Console 的 UI 交互配置该插件，需要将该 wasm 文件打包成 oci 或者 docker 镜像，可以参考[《自定义插件》](https://higress.cn/docs/latest/plugins/custom)。

## 本地调试
### 工具准备

安装[Docker](https://docs.docker.com/engine/install/)。

### 使用docker compose启动验证

1. 进入在编写插件时创建的目录，例如wasm-demo目录，确认该目录下已经编译生成main.wasm文件。

2. 在目录下创建文件docker-compose.yaml，内容如下：

   ```
   HELPCODEESCAPE-yaml
   version: '3.7'
   services:
     envoy:
       image: higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/gateway:v2.1.5
       entrypoint: /usr/local/bin/envoy
       # 注意这里对wasm开启了debug级别日志，正式部署时则默认info级别
       command: -c /etc/envoy/envoy.yaml --component-log-level wasm:debug
       depends_on:
       - httpbin
       networks:
       - wasmtest
       ports:
       - "10000:10000"
       volumes:
       - ./envoy.yaml:/etc/envoy/envoy.yaml
       - ./main.wasm:/etc/envoy/main.wasm

     httpbin:
       image: kennethreitz/httpbin:latest
       networks:
       - wasmtest
       ports:
       - "12345:80"

   networks:
     wasmtest: {}
   ```

3. 继续在该目录下创建文件envoy.yaml，内容如下：

   ```
   HELPCODEESCAPE-yaml
   admin:
     address:
       socket_address:
         protocol: TCP
         address: 0.0.0.0
         port_value: 9901
   static_resources:
     listeners:
     - name: listener_0
       address:
         socket_address:
           protocol: TCP
           address: 0.0.0.0
           port_value: 10000
       filter_chains:
       - filters:
         - name: envoy.filters.network.http_connection_manager
           typed_config:
             "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
             scheme_header_transformation:
               scheme_to_overwrite: https
             stat_prefix: ingress_http
             route_config:
               name: local_route
               virtual_hosts:
               - name: local_service
                 domains: ["*"]
                 routes:
                 - match:
                     prefix: "/"
                   route:
                     cluster: httpbin
             http_filters:
             - name: wasmdemo
               typed_config:
                 "@type": type.googleapis.com/udpa.type.v1.TypedStruct
                 type_url: type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
                 value:
                   config:
                     name: wasmdemo
                     vm_config:
                       runtime: envoy.wasm.runtime.v8
                       code:
                         local:
                           filename: /etc/envoy/main.wasm
                     configuration:
                       "@type": "type.googleapis.com/google.protobuf.StringValue"
                       value: |
                         {
                           "mockEnable": false
                         }
             - name: envoy.filters.http.router
               typed_config:
                 "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
     clusters:
     - name: httpbin
       connect_timeout: 30s
       type: LOGICAL_DNS
       # Comment out the following line to test on v6 networks
       dns_lookup_family: V4_ONLY
       lb_policy: ROUND_ROBIN
       load_assignment:
         cluster_name: httpbin
         endpoints:
         - lb_endpoints:
           - endpoint:
               address:
                 socket_address:
                   address: httpbin
                   port_value: 80
   ```

4. 执行以下命令启动docker compose。

   ```
   HELPCODEESCAPE-bash
   docker compose up
   ```

### 功能验证

#### **WASM功能验证**

1. 使用curl直接访问httpbin，可以看到不经过网关时的请求头内容，如下。

   ```
   HELPCODEESCAPE-curl
   curl http://127.0.0.1:12345/get

   {
     "args": {},
     "headers": {
       "Accept": "*/*",
       "Host": "127.0.0.1:12345",
       "User-Agent": "curl/7.79.1"
     },
     "origin": "172.18.0.1",
     "url": "http://127.0.0.1:12345/get"
   }
   ```

2. 使用curl通过网关访问httpbin，可以看到经过网关处理后的请求头的内容，如下。

   ```
   HELPCODEESCAPE-curl
   curl http://127.0.0.1:10000/get

   {
     "args": {},
     "headers": {
       "Accept": "*/*",
       "Hello": "world",
       "Host": "127.0.0.1:10000",
       "Original-Host": "127.0.0.1:10000",
       "Req-Start-Time": "1681269273896",
       "User-Agent": "curl/7.79.1",
       "X-Envoy-Expected-Rq-Timeout-Ms": "15000"
     },
     "origin": "172.18.0.3",
     "url": "https://127.0.0.1:10000/get"
   }
   ```

此时上文编写插件的功能已生效，加入了hello: world请求头。

#### **插件配置修改验证**

1. 修改envoy.yaml，将`mockEnable`配置修改为`true`。

   ```
   HELPCODEESCAPE-yaml
     configuration:
       "@type": "type.googleapis.com/google.protobuf.StringValue"
       value: |
         {
           "mockEnable": true
         }
   ```

2. 使用curl通过网关访问httpbin，可以看到经过网关处理后的请求头的内容，如下。

   ```
   HELPCODEESCAPE-curl
   curl http://127.0.0.1:10000/get

   hello world
   ```

说明插件配置修改生效，开启了mock应答直接返回了hello world。

## 更多示例
### 无配置插件

插件无需配置时，直接定义空结构体即可。

```
HELPCODEESCAPE-go
package main

import (
  "github.com/higress-group/wasm-go/pkg/wrapper"
  logs "github.com/higress-group/wasm-go/pkg/log"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm/types"
)

func main() {}

func init() {
  wrapper.SetCtx(
    "hello-world",
    wrapper.ProcessRequestHeadersBy(onHttpRequestHeaders),
  )
}

type MyConfig struct {}

func onHttpRequestHeaders(ctx wrapper.HttpContext, config MyConfig, log logs.Log) types.Action {
  proxywasm.SendHttpResponse(200, nil, []byte("hello world"), -1)
  return types.HeaderContinue
}
```

### 在插件中请求外部服务

目前仅支持 http 调用，支持访问在网关控制台中设置了服务来源的 Nacos、K8s 服务，以及固定地址或 DNS 来源的服务。请注意，无法直接使用`net/http`库中的 HTTP client，必须使用如下例中封装的 HTTP client。

下面例子中，在配置解析阶段解析服务类型，生成对应的 HTTP client ；在请求头处理阶段根据配置的请求路径访问对应服务，解析应答头，然后再设置在原始的请求头中。

```
HELPCODEESCAPE-go
package main

import (
  "errors"
  "net/http"
  "strings"
  "github.com/higress-group/wasm-go/pkg/wrapper"
  logs "github.com/higress-group/wasm-go/pkg/log"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm/types"
  "github.com/tidwall/gjson"
)

func main() {}

func init() {
  wrapper.SetCtx(
    "http-call",
    wrapper.ParseConfigBy(parseConfig),
    wrapper.ProcessRequestHeadersBy(onHttpRequestHeaders),
  )
}

type MyConfig struct {
  // 用于发起HTTP调用client
  client      wrapper.HttpClient
  // 请求url
  requestPath string
  // 根据这个key取出调用服务的应答头对应字段，再设置到原始请求的请求头，key为此配置项
  tokenHeader string
}

func parseConfig(json gjson.Result, config *MyConfig, log logs.Log) error {
  config.tokenHeader = json.Get("tokenHeader").String()
  if config.tokenHeader == "" {
    return errors.New("missing tokenHeader in config")
  }
  config.requestPath = json.Get("requestPath").String()
  if config.requestPath == "" {
    return errors.New("missing requestPath in config")
  }
  // 带服务类型的完整 FQDN 名称，例如 my-svc.dns, my-svc.static, service-provider.DEFAULT-GROUP.public.nacos, httpbin.my-ns.svc.cluster.local
  serviceName := json.Get("serviceName").String()
  servicePort := json.Get("servicePort").Int()
  if servicePort == 0 {
    if strings.HasSuffix(serviceName, ".static") {
      // 静态IP类型服务的逻辑端口是80
      servicePort = 80
    }
  }
  config.client = wrapper.NewClusterClient(wrapper.FQDNCluster{
    FQDN: serviceName,
    Port: servicePort,
        })
}

func onHttpRequestHeaders(ctx wrapper.HttpContext, config MyConfig, log logs.Log) types.Action {
  // 使用client的Get方法发起HTTP Get调用，此处省略了timeout参数，默认超时时间500毫秒
  err := config.client.Get(config.requestPath, nil,
           // 回调函数，将在响应异步返回时被执行
           func(statusCode int, responseHeaders http.Header, responseBody []byte) {
             // 请求没有返回200状态码，进行处理
             if statusCode != http.StatusOK {
               log.Errorf("http call failed, status: %d", statusCode)
               proxywasm.SendHttpResponse(http.StatusInternalServerError, nil,
                 []byte("http call failed"), -1)
               return
             }
             // 打印响应的HTTP状态码和应答body
             log.Infof("get status: %d, response body: %s", statusCode, responseBody)
             // 从应答头中解析token字段设置到原始请求头中
             token := responseHeaders.Get(config.tokenHeader)
             if token != "" {
               proxywasm.AddHttpRequestHeader(config.tokenHeader, token)
             }
             // 恢复原始请求流程，继续往下处理，才能正常转发给后端服务
             proxywasm.ResumeHttpRequest()
    })

  if err != nil {
    // 由于调用外部服务失败，放行请求，记录日志
    log.Errorf("Error occured while calling http, it seems cannot find the service cluster.")
    return types.ActionContinue
  } else {
    // 需要等待异步回调完成，返回HeaderStopAllIterationAndWatermark状态，可以被ResumeHttpRequest恢复
    return types.HeaderStopAllIterationAndWatermark
  }
}
```

### 在插件中调用Redis

使用如下示例代码实现Redis限流插件。

```
HELPCODEESCAPE-go
package main

import (
  "strconv"
  "time"

  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm"
  "github.com/higress-group/proxy-wasm-go-sdk/proxywasm/types"
  "github.com/tidwall/gjson"
  "github.com/tidwall/resp"

  "github.com/higress-group/wasm-go/pkg/wrapper"
  logs "github.com/higress-group/wasm-go/pkg/log"
)

func main() {}

func init() {
  wrapper.SetCtx(
    "redis-demo",
    wrapper.ParseConfigBy(parseConfig),
    wrapper.ProcessRequestHeadersBy(onHttpRequestHeaders),
    wrapper.ProcessResponseHeadersBy(onHttpResponseHeaders),
  )
}

type RedisCallConfig struct {
  client wrapper.RedisClient
  qpm    int
}

func parseConfig(json gjson.Result, config *RedisCallConfig, log logs.Log) error {
  // 带服务类型的完整 FQDN 名称，例如 my-redis.dns、redis.my-ns.svc.cluster.local
  serviceName := json.Get("serviceName").String()
  servicePort := json.Get("servicePort").Int()
  if servicePort == 0 {
    if strings.HasSuffix(serviceName, ".static") {
      // 静态IP类型服务的逻辑端口是80
      servicePort = 80
    } else {
      servicePort = 6379
    }
  }
  username := json.Get("username").String()
  password := json.Get("password").String()
  // 单位是毫秒
  timeout := json.Get("timeout").Int()
  if timeout == 0 {
    timeout = 1000
  }
  qpm := json.Get("qpm").Int()
  config.qpm = int(qpm)
  config.client = wrapper.NewRedisClusterClient(wrapper.FQDNCluster{
    FQDN: serviceName,
    Port: servicePort,
  })
  return config.client.Init(username, password, timeout)
}

func onHttpRequestHeaders(ctx wrapper.HttpContext, config RedisCallConfig, log logs.Log) types.Action {
  now := time.Now()
  minuteAligned := now.Truncate(time.Minute)
  timeStamp := strconv.FormatInt(minuteAligned.Unix(), 10)
  // 如果 redis api 返回的 err != nil，一般是由于网关找不到 redis 后端服务，请检查是否误删除了 redis 后端服务
  err := config.client.Incr(timeStamp, func(response resp.Value) {
    if response.Error() != nil {
      log.Errorf("call redis error: %v", response.Error())
      proxywasm.ResumeHttpRequest()
    } else {
      ctx.SetContext("timeStamp", timeStamp)
      ctx.SetContext("callTimeLeft", strconv.Itoa(config.qpm-response.Integer()))
      if response.Integer() == 1 {
        err := config.client.Expire(timeStamp, 60, func(response resp.Value) {
          if response.Error() != nil {
            log.Errorf("call redis error: %v", response.Error())
          }
          proxywasm.ResumeHttpRequest()
        })
        if err != nil {
          log.Errorf("Error occured while calling redis, it seems cannot find the redis cluster.")
          proxywasm.ResumeHttpRequest()
        }
      } else {
        if response.Integer() > config.qpm {
          proxywasm.SendHttpResponse(429, [][2]string{{"timeStamp", timeStamp}, {"callTimeLeft", "0"}}, []byte("Too many requests\n"), -1)
        } else {
          proxywasm.ResumeHttpRequest()
        }
      }
    }
  })
  if err != nil {
    // 由于调用redis失败，放行请求，记录日志
    log.Errorf("Error occured while calling redis, it seems cannot find the redis cluster.")
    return types.HeaderContinue
  } else {
    // 请求hold住，等待redis调用完成
    return types.HeaderStopAllIterationAndWatermark
  }
}

func onHttpResponseHeaders(ctx wrapper.HttpContext, config RedisCallConfig, log logs.Log) types.Action {
  if ctx.GetContext("timeStamp") != nil {
    proxywasm.AddHttpResponseHeader("timeStamp", ctx.GetContext("timeStamp").(string))
  }
  if ctx.GetContext("callTimeLeft") != nil {
    proxywasm.AddHttpResponseHeader("callTimeLeft", ctx.GetContext("callTimeLeft").(string))
  }
  return types.HeaderContinue
}
```