---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/ai-cue-decorator
fetch_date: 2026-09-21
product: AI Gateway
slug: ai-cue-decorator
body_sha256: 833647075778059bb10f0387711c23e6c6d54af30d6f00909b13f4d0fd298ec0
body_bytes: 2596
migration_status: current
---

AI提示词模板，用于快速构建同类型的AI请求。  

## 运行属性
插件执行阶段：`默认阶段` 插件执行优先级：`500`

## 配置说明
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>templates</code></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>模板设置</p></td> </tr> </tbody> </table>

template object 配置说明：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>name</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>模板名称</p></td> </tr> <tr> <td><p><code>template.model</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>模型名称</p></td> </tr> <tr> <td><p>template.messages</p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>大模型输入</p></td> </tr> </tbody> </table>

message object 配置说明：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>role</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>角色</p></td> </tr> <tr> <td><p><code>content</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>消息</p></td> </tr> </tbody> </table>

## 示例
配置示例如下：

```
HELPCODEESCAPE-yaml
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

使用以上配置的请求body示例：

```
HELPCODEESCAPE-bash
{
  "template": "developer-chat",
  "properties": {
    "program": "quick sort",
    "language": "python"
  }
}
```