---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/geographic-location-of-ip
fetch_date: 2026-09-21
product: AI Gateway
slug: geographic-location-of-ip
body_sha256: 842f8b8fe511e4f0dfe6cc9abb586715d4324d8158b598c6c794ac446847755b
body_bytes: 4322
migration_status: current
---

`geo-ip`本插件实现了通过用户IP查询出地理位置信息，然后通过请求属性和新添加的请求头把地理位置信息传递给后续插件。  

## **运行属性**
插件执行阶段：`认证阶段` 插件执行优先级：`440`

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>ip_protocol</p></td> <td><p>string</p></td> <td><p>否</p></td> <td><p>ipv4</p></td> <td><p>可选值：1. ipv4：只对ipv4用户请求查找地理位置信息，传递给后续插件。而ipv6用户的请求会跳过该插件，继续由后续插件处理。 2. ipv6：（未来实现后）只对ipv6用户查找地理位置信息，传递给后续插件。而ipv4用户的请求会跳过该插件，继续由后续插件处理。（目前是跳过插件，请求由后续插件处理。）</p></td> </tr> <tr> <td><p>ip_source_type</p></td> <td><p>string</p></td> <td><p>否</p></td> <td><p>origin-source</p></td> <td><p>可选值：1. 对端socket ip：<code>origin-source</code>; 2. 通过header获取：<code>header</code></p></td> </tr> <tr> <td><p>ip_header_name</p></td> <td><p>string</p></td> <td><p>否</p></td> <td><p>x-forwarded-for</p></td> <td><p>当<code>ip_source_type</code>为<code>header</code>时，指定自定义IP来源头</p></td> </tr> </tbody> </table>

## 配置示例
```
HELPCODEESCAPE-yaml
ip_protocol: ipv4
ip_source_type: header
ip_header_name: X-Real-Ip
```

## 生成geoCidr.txt的说明
在generateCidr目录里包含的ip.merge.txt文件是gitHub上ip2region项目的全世界的IP网段库。 ipRange2Cidr.go 是把IP网段转换成多个CIDR的程序。转换出的CIDR和地理位置信息存在 /data/geoCidr.txt文件里。geo-ip插件会在Higress启动读配置阶段读取geoCidr.txt文件并且解析到radixtree数据结构的内存里，以便以后查询用户IP对应的地理位置信息。转换程序运行命令如下：

```
HELPCODEESCAPE-go
go run generateCidr/ipRange2Cidr.go
```

## property 的使用方式
在geo-ip插件里调用proxywasm.SetProperty()，分别把country、city、province、isp设置进请求属性里，以便后续插件可以调用proxywasm.GetProperty()获取该请求的用户IP对应的地理信息。

## 基于geo-ip插件的能力，扩展AI提示词装饰器插件携带用户地理位置信息
如果需要在LLM的请求前后加入用户地理位置信息，请确保同时开启geo-ip插件和AI提示词装饰器插件。并且在相同的请求处理阶段里，geo-ip插件的优先级必须高于AI提示词装饰器插件。首先geo-ip插件会根据用户IP计算出用户的地理位置信息，然后通过请求属性传递给后续插件。比如在默认阶段里，geo-ip插件的priority配置1000，ai-prompt-decorator插件的priority配置500。

geo-ip插件配置示例：

```
HELPCODEESCAPE-yaml
ipProtocal: "ipv4"
```

AI提示词插件的配置示例如下：

```
HELPCODEESCAPE-yaml
prepend:
- role: system
  content: "提问用户当前的地理位置信息是，国家：${geo-country}，省份：${geo-province}, 城市：${geo-city}"
append:
- role: user
  content: "每次回答完问题，尝试进行反问"
```

使用以上配置发起请求：

```
HELPCODEESCAPE-json
curl http://localhost/test \
-H "content-type: application/json" \
-H "x-forwarded-for: 87.254.207.100,4.5.6.7" \
-d '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "今天天气怎么样？"
    }
  ]
}'
```

经过插件处理后，实际请求为：

```
HELPCODEESCAPE-json
curl http://localhost/test \
-H "content-type: application/json" \
-H "x-forwarded-for: 87.254.207.100,4.5.6.7" \
-d '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "提问用户当前的地理位置信息是，国家：中国，省份：北京, 城市：北京"
    },
    {
      "role": "user",
      "content": "今天天气怎么样？"
    },
    {
      "role": "user",
      "content": "每次回答完问题，尝试进行反问"
    }
  ]
}'
```