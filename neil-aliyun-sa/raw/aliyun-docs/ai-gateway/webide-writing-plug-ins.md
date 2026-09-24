---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/webide-writing-plug-ins
fetch_date: 2026-09-21
product: AI Gateway
slug: webide-writing-plug-ins
body_sha256: 289a21b0b27a6a1c347d9fd940f97437ed6b30fc39c689814c558193398b184d
body_bytes: 6073
migration_status: current
---

AI网关通过插件来为您提供定制化的扩展能力。本文介绍如何通过WebIDE一站式完成自定义插件的开发和编译。  

## **背景信息**
为了解决自定义插件编写门槛较高，搭建开发环境难的问题，AI网关提供了一个包含插件开发环境的WebIDE Runtime，可以通过WebIDE一站式完成自定义插件的开发和编译。

WebIDE内置集成云效仓库，代码资源属于用户，代码提交Git化管理，支持持久化管理、内置流水线标准化环境以及自动化构建。

## 操作步骤
### 1.编写网关插件

1. 登录[AI网关控制台](https://apigw.console.aliyun.com/#/cn-hangzhou/ai-gateway)。

2. 在左侧导航栏，选择**插件**，并在顶部菜单栏选择地域。

3. 在插件页面单击**WebIDE编写插件** **，** 在编辑插件页面单击**新建**。

4. 在**新建插件** 页面输入插件标识与插件名称，单击**确定**进入WebIDE开始编写网关插件。

### 2.构建与发布

网关插件代码编写完毕后，需完成构建与发布后，才可在网关进行安装。

1. 在WebIDE控制台右上角单击**构建** ，然后单击**确认**。

   **说明**
   * 如果存在文件未提交时进行构建，需选择提交并构建或者直接构建，直接构建不会对未提交的内容进行构建。

   * 可单击右上角**构建日志**实时查看构建情况。

2. 构建完成后单击右上角**发布版本**。

3. 在添加版本页完成相关配置，单击**发布**。配置说明如下：

   <table> <thead> <tr> <td><p><b>配置项</b></p></td> <td><p><b>配置说明</b></p></td> <td><p><b>示例</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>版本号</p></td> <td><p>版本编号，格式需符合X.Y.Z</p></td> <td><p>1.0.0</p></td> </tr> <tr> <td><p>版本描述</p></td> <td><p>版本说明</p></td> <td><p>修改返回格式</p></td> </tr> <tr> <td><p>执行阶段</p></td> <td><p>阶段处理顺序：<b>认证阶段</b>\&nbsp;\&gt;\&nbsp;<b>鉴权阶段</b>\&nbsp;\&gt;\&nbsp;<b>统计阶段</b>\&nbsp;\&gt;\&nbsp;<b>默认阶段</b>。若不依赖其他插件执行顺序，填写默认阶段即可。</p></td> <td><p>默认阶段</p></td> </tr> <tr> <td><p>执行优先级</p></td> <td><p>控制执行阶段内的优先级，数字越大优先级越高。</p></td> <td><p>100</p></td> </tr> <tr> <td><p>适配网关版本</p></td> <td> <ul> <li><p>任意版本：可以安装到任意版本的网关。</p></li> <li><p>指定版本：仅可以安装到指定版本（含）之后的网关版本。</p></li> </ul></td> <td><p>任意版本</p></td> </tr> </tbody> </table>

## 插件代码基本结构
网关插件的开发包括配置解析和处理函数两个部分，配置解析是读取插件输入配置的过程，处理函数则是指请求头处理、请求体处理、响应头处理以及响应体处理的四个函数。

```
HELPCODEESCAPE-go
func init() {
wrapper.SetCtx(
	// 插件名称，可自定义
	"my-plugin",

	// 设置自定义函数解析插件配置，此方法适合插件全局配置和路由、域名、服务级别配置内容规则一致的场景
	wrapper.ParseConfigBy(parseConfig),

	// 网关接收到客户端发送来的请求头数据时,设置自定义函数处理请求头
	wrapper.ProcessRequestHeadersBy(onHttpRequestHeaders),

	// 网关接收到后端服务响应的应答头数据时,设置自定义函数处理响应头
	wrapper.ProcessResponseHeadersBy(onHttpResponseHeaders),

	// 网关接收到客户端发送来的请求Body数据时,设置自定义函数处理请求体
	wrapper.ProcessRequestBodyBy(onHttpRequestBody),

	// 网关接收到后端服务响应的应答Body数据时,设置自定义函数处理响应体
	wrapper.ProcessResponseBodyBy(onHttpResponseBody),

	// 设置自定义函数处理流式请求体
	wrapper.ProcessStreamingRequestBodyBy(onHttpStreamingRequestBody),

	// 设置自定义函数处理流式响应体
	wrapper.ProcessStreamingResponseBodyBy(onHttpStreamingResponseBody),

	// 设置自定义函数处理流式请求完成
	//wrapper.ProcessStreamDoneBy(onHttpStreamDone),
)
}

// MyConfig 自定义插件配置，可自行定义；插件无需配置时，直接定义空结构体即可(type MyConfig struct {})
type MyConfig struct {
// 是否启用
mockEnable bool
}

// 在控制台插件配置中填写的YAML配置会自动转换为JSON，此处直接从JSON这个参数里解析配置即可
func parseConfig(json gjson.Result, config *MyConfig, log logs.Log) error {
// 解析出配置，更新到config中
config.mockEnable = json.Get("mockEnable").Bool()
return nil
}

// 请求头处理函数
func onHttpRequestHeaders(ctx wrapper.HttpContext, config MyConfig, log logs.Log) types.Action {
proxywasm.AddHttpRequestHeader("hello", "world")
if config.mockEnable {
	proxywasm.SendHttpResponse(200, nil, []byte("hello world"), -1)
}
return types.ActionContinue
}

// 请求体处理函数
func onHttpRequestBody(ctx wrapper.HttpContext, config MyConfig, body []byte, log logs.Log) types.Action {
return types.ActionContinue
}

// 响应头处理函数
func onHttpResponseBody(ctx wrapper.HttpContext, config MyConfig, body []byte, log logs.Log) types.Action {
return types.ActionContinue
}

// 响应体处理函数
func onHttpResponseHeaders(ctx wrapper.HttpContext, config MyConfig, log logs.Log) types.Action {
return types.ActionContinue
}
```

## 使用大模型生成插件代码
WebIDE支持用户通过自然语言描述实现一键生成插件代码，相关操作步骤如下：

1. 在WebIDE控制台右上角单击**一键生成**。

2. 在一键生成编辑框中详细描述需求。

3. 单击**确认**，等待代码生成直至结束。

## 相关文档
* 如果想了解如何进行插件开发，请参见[开发插件](https://help.aliyun.com/document_detail/2882240.html)。

* 如果想了解插件的安装、启用、卸载功能，请参见[管理插件](https://help.aliyun.com/document_detail/2882239.html)。