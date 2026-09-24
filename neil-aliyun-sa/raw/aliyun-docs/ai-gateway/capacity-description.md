---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/capacity-description
fetch_date: 2026-09-21
product: AI Gateway
slug: capacity-description
body_sha256: 0295b622c7a37f86e04d27e428911123fa1906106526122539f35e94a5bb4dd2
body_bytes: 7972
migration_status: current
---

AI 网关按实例规格提供不同的 QPS、客户端连接数上限，并对各类资源设置配额限制。本文列出专享实例版的容量规格，以及 Serverless 版和专享实例版的资源配额，供购买或升级实例时参考。  

## 容量规格
以下为专享实例版各实例规格对应的 QPS 和客户端连接数上限：
<table> <thead> <tr> <td> <p><b>实例规格</b></p> </td> <td> <p><b>QPS</b></p> </td> <td> <p><b>客户端连接数</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>aigw.small.x1</p> </td> <td> <p>1500</p> </td> <td> <p>20000</p> </td> </tr> <tr> <td> <p>aigw.small.x2</p> </td> <td> <p>3000</p> </td> <td> <p>40000</p> </td> </tr> <tr> <td> <p>aigw.small.x4</p> </td> <td> <p>6000</p> </td> <td> <p>80000</p> </td> </tr> <tr> <td> <p>aigw.medium.x1</p> </td> <td> <p>12000</p> </td> <td> <p>160000</p> </td> </tr> <tr> <td> <p>aigw.medium.x2</p> </td> <td> <p>24000</p> </td> <td> <p>320000</p> </td> </tr> <tr> <td> <p>aigw.medium.x3</p> </td> <td> <p>36000</p> </td> <td> <p>480000</p> </td> </tr> <tr> <td> <p>aigw.large.x1</p> </td> <td> <p>48000</p> </td> <td> <p>640000</p> </td> </tr> <tr> <td> <p>aigw.large.x2</p> </td> <td> <p>96000</p> </td> <td> <p>1280000</p> </td> </tr> <tr> <td> <p>aigw.large.x3</p> </td> <td> <p>144000</p> </td> <td> <p>1920000</p> </td> </tr> <tr> <td> <p>aigw.large.x4</p> </td> <td> <p>192000</p> </td> <td> <p>2560000</p> </td> </tr> </tbody> </table>

## 配额说明
AI 网关对各类资源设置了配额上限，分为全局配额（Region 级别）和实例配额（按实例版本和规格档位区分）。

### 全局配额

<table> <thead> <tr> <td> <p><b>配额项</b></p> </td> <td> <p><b>配额</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>单Region实例数量</p> </td> <td> <p>100</p> </td> </tr> <tr> <td> <p>单Region最大消费者组数</p> </td> <td> <p>1000</p> </td> </tr> <tr> <td> <p>单消费者组内消费者数</p> </td> <td> <p>500</p> </td> </tr> <tr> <td> <p>单Region最大消费者数</p> </td> <td> <p>100000</p> </td> </tr> </tbody> </table>

### 实例配额

AI 网关分为 Serverless 版和专享实例版两种版本，专享实例版按规格名称前缀分为 Small（`aigw.small.*`）、Medium（`aigw.medium.*`）、Large（`aigw.large.*`）三个档位。不同版本和档位的实例配额如下，其中"消费者数量"和"消费者授权规则数"作为独立的配额项分别展示、分别统计和校验：
<table> <thead> <tr> <td> <p></p> </td> <td> <p><b>Serverless</b></p> </td> <td> <p><b>Small</b></p> </td> <td> <p><b>Medium</b></p> </td> <td> <p><b>Large</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p><b>规格</b></p> </td> <td> <p><b>Serverless（旧）</b></p> </td> <td> <p><b>Serverless（标准版）</b></p> </td> <td> <p><b>Serverless（企业版）</b></p> </td> <td> <p><b>aigw.small.x1</b></p> </td> <td> <p><b>apigw.small.x2</b></p> </td> <td> <p><b>apigw.small.x4</b></p> </td> <td> <p><b>apigw.medium.x1</b></p> </td> <td> <p><b>apigw.medium.x2</b></p> </td> <td> <p><b>apigw.medium.x3</b></p> </td> <td> <p><b>apigw.large.x1</b></p> </td> <td> <p><b>apigw.large.x2</b></p> </td> <td> <p><b>apigw.large.x3</b></p> </td> <td> <p><b>apigw.large.x4</b></p> </td> </tr> <tr> <td> <p>MCP Server数</p> </td> <td> <p>100</p> </td> <td> <p>20</p> </td> <td> <p>100</p> </td> <td> <p>500</p> </td> <td> <p>600</p> </td> <td> <p>800</p> </td> <td> <p>1000</p> </td> <td> <p>1200</p> </td> <td> <p>1600</p> </td> <td> <p>2000</p> </td> <td> <p>2200</p> </td> <td> <p>2400</p> </td> <td> <p>2600</p> </td> </tr> <tr> <td> <p>在线路由总数（含Model API路由、Agent API路由）</p> </td> <td> <p>2500</p> </td> <td> <p>200</p> </td> <td> <p>2500</p> </td> <td> <p>5000</p> </td> <td> <p>6000</p> </td> <td> <p>7000</p> </td> <td> <p>7500</p> </td> <td> <p>8000</p> </td> <td> <p>9000</p> </td> <td> <p>10000</p> </td> <td> <p>12000</p> </td> <td> <p>14000</p> </td> <td> <p>16000</p> </td> </tr> <tr></tr> <tr> <td> <p>发布域名数</p> </td> <td> <p>100</p> </td> <td> <p>20</p> </td> <td> <p>100</p> </td> <td> <p>200</p> </td> <td> <p>300</p> </td> <td> <p>400</p> </td> <td> <p>500</p> </td> <td> <p>600</p> </td> <td> <p>800</p> </td> <td> <p>1000</p> </td> <td> <p>1200</p> </td> <td> <p>1400</p> </td> <td> <p>1600</p> </td> </tr> <tr> <td> <p>服务数</p> </td> <td> <p>200</p> </td> <td> <p>50</p> </td> <td> <p>200</p> </td> <td> <p>800</p> </td> <td> <p>1200</p> </td> <td> <p>1600</p> </td> <td> <p>2000</p> </td> <td> <p>2500</p> </td> <td> <p>3000</p> </td> <td> <p>4000</p> </td> <td> <p>4500</p> </td> <td> <p>5000</p> </td> <td> <p>6000</p> </td> </tr> <tr> <td> <p>消费者授权规则数</p> </td> <td> <p>500</p> </td> <td> <p>100</p> </td> <td> <p>500</p> </td> <td> <p>2000</p> </td> <td> <p>4000</p> </td> <td> <p>6000</p> </td> <td> <p>8000</p> </td> <td> <p>12000</p> </td> <td> <p>16000</p> </td> <td> <p>20000</p> </td> <td> <p>27500</p> </td> <td> <p>35000</p> </td> <td> <p>42500</p> </td> </tr> <tr> <td> <p>消费者数量</p> </td> <td> <p>500</p> </td> <td> <p>100</p> </td> <td> <p>500</p> </td> <td> <p>2000</p> </td> <td> <p>4000</p> </td> <td> <p>6000</p> </td> <td> <p>8000</p> </td> <td> <p>12000</p> </td> <td> <p>16000</p> </td> <td> <p>20000</p> </td> <td> <p>27500</p> </td> <td> <p>35000</p> </td> <td> <p>42500</p> </td> </tr> <tr> <td> <p>消费者配额规则数</p> </td> <td> <p>500</p> </td> <td> <p>100</p> </td> <td> <p>500</p> </td> <td> <p>2000</p> </td> <td> <p>4000</p> </td> <td> <p>6000</p> </td> <td> <p>8000</p> </td> <td> <p>12000</p> </td> <td> <p>16000</p> </td> <td> <p>20000</p> </td> <td> <p>27500</p> </td> <td> <p>35000</p> </td> <td> <p>42500</p> </td> </tr> <tr> <td> <p>K8s服务来源数</p> </td> <td> <p>1</p> </td> <td> <p>N/A</p> </td> <td> <p>1</p> </td> <td> <p>3</p> </td> <td> <p>5</p> </td> <td> <p>5</p> </td> </tr> <tr> <td> <p>安装的插件数</p> </td> <td> <p>N/A</p> </td> <td> <p>5</p> </td> <td> <p>5</p> </td> <td> <p>10</p> </td> <td> <p>20</p> </td> <td> <p>30</p> </td> </tr> <tr> <td> <p>上传自定义插件数</p> </td> <td> <p>N/A</p> </td> <td> <p>N/A</p> </td> <td> <p>N/A</p> </td> <td> <p>20</p> </td> <td> <p>50</p> </td> <td> <p>80</p> </td> </tr> </tbody> </table>  
**警告**

说明：如通过特殊白名单或特殊配置突破上述配额限制，相关使用不属于标准配额范围，阿里云不对该等使用场景作出服务等级协议（SLA）承诺。

<br />

### 消费者授权额度计算口径

"消费者数量"和"消费者授权规则数"是两个独立的配额项，分别统计、分别校验。

各实例规格的消费者数量上限和消费者授权规则数上限分别列于上表；其他规格以实例配额表为准。

**消费者数量** = 当前网关授权关系中，直接授权的消费者与通过消费者组授权引用的消费者合并去重后的数量。同一个消费者被多条规则或多个消费者组引用时只计1次；消费者组为空时不增加消费者数量。

**消费者授权规则数** = 当前网关保留的消费者授权规则条数。直接授权一条计1条，消费者组授权一条也计1条；无论消费者组包含多少消费者或是否为空，都只计1条。

两项用量分别与对应的配额上限比较：消费者数量不超过消费者数量上限，且消费者授权规则数不超过消费者授权规则数上限。通过白名单或特殊配置提高的配额只改变可用上限，不改变上述计算口径。

<br />

<br />