---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-auxiliary-plug-in-development
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-auxiliary-plug-in-development
body_sha256: 09e0e83ab50bf7dc27f64a5f1f89698fc3c7e4ab8d12584c55b42a81f79c88bd
body_bytes: 2537
migration_status: current
---

本文主要介绍如何利用 AI 大模型，根据您输入的插件需求，自动生成插件代码。  

## **功能介绍**
为了满足差异化的网关使用需求，同时降低网关插件的开发难度，AI网关提供了基于大模型的端到端插件生成功能。您可以将插件运行逻辑用自然语言进行描述，即可开始端到端的插件生成工作，轻松实现任意定制化的网关场景需求。

## 以自然语言描述需求
AI网关可以根据您提供的自然语言需求来生成插件代码，并结合一定的代码编译、测试修复手段，实现端到端的插件功能自动开发。为了提升插件生成的准确率，让AI大模型更清晰地了解每个阶段需要完成的开发任务，建议您参考如下的示例进行需求描述：

```
HELPCODEESCAPE-plaintext
# 请求头处理函数
对于网关接收到的任意请求直接返回固定的字符串，要求字符串可以通过配置修改
# 请求体处理函数
无
# 响应头处理函数
无
# 响应体处理函数
无
```

**重要**

大模型首先会根据需求描述进行判断，对于不合理的开发需求会直接结束任务，并给出相关建议，此时您应该参考建议内容对需求进行修改。

## 插件代码基本结构
网关插件的开发包括配置解析和处理函数两个部分，配置解析是读取插件输入配置的过程，处理函数则是指请求头处理、请求体处理、响应头处理以及响应体处理的四个函数，一个空的Golang插件示例代码如下：

```
HELPCODEESCAPE-go
type MyConfig struct {
    // config items
}

func parseConfig(json gjson.Result, config *MyConfig, log wrapper.Log) error {
    // parse config form json
    return nil
}

// 请求头处理函数
func onHttpRequestHeaders(ctx wrapper.HttpContext, config MyConfig, log wrapper.Log) types.Action {}

// 请求体处理函数
func onHttpRequestBody(ctx wrapper.HttpContext, config MyConfig, body []byte, log wrapper.Log) types.Action {}

// 响应头处理函数
func onHttpResponseHeaders(ctx wrapper.HttpContext, config MyConfig, log wrapper.Log) types.Action {}

// 响应体处理函数
func onHttpResponseBody(ctx wrapper.HttpContext, config MyConfig, body []byte, log wrapper.Log) types.Action {}
```

## 生成插件与开发调试
AI 大模型会根据您的需求尝试生成完整的插件代码，插件生成成功后会自动导入WebIDE中，您可对生成的插件进行功能验证，根据实际需求对插件代码进行调整。