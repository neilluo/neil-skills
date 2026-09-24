---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-request-response-intelligent-transformation
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-request-response-intelligent-transformation
body_sha256: 34f58205cd73947276c6fe311a6a1c43a41a419d57092b6626e4f87eb881759d
body_bytes: 3330
migration_status: current
---

AI 请求响应转换插件，通过LLM对请求/响应的header以及body进行修改。  

## 运行属性
插件执行阶段：`认证阶段` 插件执行优先级：`410`

## 配置说明
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>request.enable</code></p></td> <td><p>bool</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>是否在request阶段开启转换</p></td> </tr> <tr> <td><p><code>request.prompt</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>request阶段转换使用的prompt</p></td> </tr> <tr> <td><p><code>response.enable</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>是否在response阶段开启转换</p></td> </tr> <tr> <td><p><code>response.prompt</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>response阶段转换使用的prompt</p></td> </tr> <tr> <td><p><code>provider.serviceName</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>DNS类型的服务名，目前仅支持千问</p></td> </tr> <tr> <td><p><code>provider.domain</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>LLM服务域名</p></td> </tr> <tr> <td><p><code>provider.apiKey</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>阿里云dashscope服务的API Key</p></td> </tr> </tbody> </table>

## 配置示例
```
HELPCODEESCAPE-properties
request:
    enable: false
    prompt: "如果请求path是以/httpbin开头的，帮我去掉/httpbin前缀，其他的不要改。"
response:
    enable: true
    prompt: "帮我修改以下HTTP应答信息，要求：1. content-type修改为application/json；2. body由xml转化为json；3. 移除content-length。"
provider:
    serviceName: qwen
    domain: dashscope.aliyuncs.com
    apiKey: xxxxxxxxxxxxx
```

访问原始的httpbin的`/xml`接口，结果为：

```
HELPCODEESCAPE-xml
<?xml version='1.0' encoding='us-ascii'?>

<!--  A SAMPLE set of slides  -->

<slideshow
    title="Sample Slide Show"
    date="Date of publication"
    author="Yours Truly"
    >

    <!-- TITLE SLIDE -->
    <slide type="all">
      <title>Wake up to WonderWidgets!</title>
    </slide>

    <!-- OVERVIEW -->
    <slide type="all">
        <title>Overview</title>
        <item>Why <em>WonderWidgets</em> are great</item>
        <item/>
        <item>Who <em>buys</em> WonderWidgets</item>
    </slide>

</slideshow>
```

使用以上配置，通过网关访问httpbin的`/xml`接口，结果为：

```
HELPCODEESCAPE-json
{
  "slideshow": {
    "title": "Sample Slide Show",
    "date": "Date of publication",
    "author": "Yours Truly",
    "slides": [
      {
        "type": "all",
        "title": "Wake up to WonderWidgets!"
      },
      {
        "type": "all",
        "title": "Overview",
        "items": [
          "Why <em>WonderWidgets</em> are great",
          "",
          "Who <em>buys</em> WonderWidgets"
        ]
      }
    ]
  }
}
```