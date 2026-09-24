---
source_url: https://help.aliyun.com/zh/agentcore/agentcore-billing-instructions
fetch_date: 2026-09-20
product: AgentCore
slug: agentcore-billing-instructions
body_sha256: 6dcf50cfe73e23a7d45231011b204ba420c524a0d4a104cee9e9ec4a8dbc3ca3
body_bytes: 7093
migration_status: current
---

使用 AgentCore 构建和运行智能体时，算力、网关、存储和公网流量会按实际用量产生费用。AgentCore 采用按量计费，计费项包括算力 CU、网关 CU、存储 CU、可选的协作专享管控面和公网流量。了解各计费项的计量规则与地域单价后，可以在开通前估算成本，并在出账后核对账单明细。  

## 计费项总览
<table> <thead> <tr> <td> <p><b>类别</b></p> </td> <td> <p><b>计费项</b></p> </td> <td> <p><b>计费维度</b></p> </td> <td> <p><b>参考单价</b></p> </td> <td> <p>参考地域</p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>Agent 构建与运行</p> </td> <td> <p>算力 CU</p> </td> <td> <p>CU（按 vCPU 与内存用量换算）</p> </td> <td> <p><span>CNY 0.0000694/CU</span> </p> </td> <td> <p>上海</p> </td> </tr> <tr> <td> <p>Agent 构建与运行</p> </td> <td> <p>网关 CU</p> </td> <td> <p>CU（按请求调用次数换算）</p> </td> <td> <p><span>CNY 0.0000015/CU</span> </p> </td> <td> <p>上海</p> </td> </tr> <tr> <td> <p>Agent 构建与运行</p> </td> <td> <p>存储 CU</p> </td> <td> <p>CU（按 GB/小时换算）</p> </td> <td> <p><span>CNY 0.00025/CU</span> </p> </td> <td> <p>上海</p> </td> </tr> <tr> <td> <p>协作管控面</p> </td> <td> <p>协作专享管控面</p> </td> <td> <p>实例/小时</p> </td> <td> <p>CNY 3/小时</p> </td> <td> <p>上海</p> </td> </tr> <tr> <td> <p>公网流量</p> </td> <td> <p>公网流量</p> </td> <td> <p>GB（由云数据传输 CDT 统一计费和出账）</p> </td> <td> <p><span>CNY 0.8/GB</span> </p> </td> <td> <p>上海</p> </td> </tr> </tbody> </table>

上表仅包含 AgentCore 自身资源的计费项。开通 AgentCore 时一并开通的其他阿里云产品按各自的计费规则独立计费，其费用构成详见[AgentCore 产品概述](https://help.aliyun.com/document_detail/3052303.html)的"依赖产品费用"章节。表中算力 CU、网关 CU、存储 CU 与协作专享管控面的参考单价为上海地域单价，各地域单价详见各地域定价。具体计量规则和单价以官网价格页、产品控制台和账单展示为准。

## 月费组成
月费 = 算力 CU 费用 + 网关 CU 费用 + 存储 CU 费用 + 协作专享管控面费用（可选） + 公网流量费用

其中，协作专享管控面为可选项，仅在开通协作功能并购买协作专享管控面实例后产生。

## 算力 CU
算力 CU 按 Agent 运行时实际消耗的 vCPU 和内存用量换算，参考单价为 CNY 0.0000694/CU （上海地域）。CU 换算规则如下：
<table> <thead> <tr> <td> <p><b>资源用量</b></p> </td> <td> <p><b>CU 换算</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1 vCPU × 1 秒</p> </td> <td> <p>1 CU</p> </td> </tr> <tr> <td> <p>1 GB 内存 × 1 秒</p> </td> <td> <p>0.5 CU</p> </td> </tr> </tbody> </table>

### 计费示例

<table> <thead> <tr> <td> <p><b>场景</b></p> </td> <td> <p><b>用量换算</b></p> </td> <td> <p><b>费用</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>1 vCPU 规格持续运行 1 小时</p> </td> <td> <p>1 × 3600 秒 = 3600 CU</p> </td> <td> <p><span>3600 × 0.0000694 = CNY 0.2498</span> </p> </td> </tr> <tr> <td> <p>2 GB 内存持续占用 1 小时</p> </td> <td> <p>2 × 3600 × 0.5 = 3600 CU</p> </td> <td> <p><span>3600 × 0.0000694 = CNY 0.2498</span> </p> </td> </tr> <tr> <td> <p>1 vCPU + 2 GB 内存持续运行 1 小时</p> </td> <td> <p>3600 + 3600 = 7200 CU</p> </td> <td> <p><span>7200 × 0.0000694 = CNY 0.4997</span> </p> </td> </tr> </tbody> </table>

## 网关 CU
网关CU按经过网关的请求调用次数计量，1 次请求调用计为 1 网关 CU。参考单价为 CNY 0.0000015/CU （上海地域），即每小时按 0.015 元/万次计。

### 计量规则

请求调用次数按经过网关的请求个数计费。长连接在连接保持期间持续占用网关资源，因此按保持时长折算为请求次数：
<table> <thead> <tr> <td> <p><b>计量规则</b></p> </td> <td> <p><b>说明</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>短连接请求</p> </td> <td> <p>普通请求-响应按 1 次请求调用计量</p> </td> </tr> <tr> <td> <p>长连接按时长折算</p> </td> <td> <p>流式响应、MCP 长连接、Agent 长会话等长连接，按连接保持时长每 30 秒折算为 1 次请求调用</p> </td> </tr> </tbody> </table>

请求体和响应体的数据量按"数据处理量"单独计费，不影响请求调用次数。

### 计量示例

<table> <thead> <tr> <td> <p><b>请求特征</b></p> </td> <td> <p><b>计量请求次数</b></p> </td> <td> <p><b>费用</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>普通 AI 对话请求（数秒内完成）</p> </td> <td> <p>1 次</p> </td> <td> <p>CNY 0.0000015</p> </td> </tr> <tr> <td> <p>保持 2 分钟的长连接</p> </td> <td> <p>4 次</p> </td> <td> <p>CNY 0.000006</p> </td> </tr> <tr> <td> <p>保持 10 分钟的长连接</p> </td> <td> <p>20 次</p> </td> <td> <p>CNY 0.00003</p> </td> </tr> </tbody> </table>

## 存储 CU
1 个存储 CU 表示 1 GB 存储空间使用 1 小时，参考单价为 CNY 0.00025/CU （上海地域）。

### 计费示例

<table> <thead> <tr> <td> <p><b>场景</b></p> </td> <td> <p><b>用量换算</b></p> </td> <td> <p><b>费用</b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>10 GB 存储空间保存 1 小时</p> </td> <td> <p>10 × 1 = 10 CU</p> </td> <td> <p><span>10 × 0.00025 = CNY 0.0025</span> </p> </td> </tr> <tr> <td> <p>10 GB 存储空间保存 1 个月（按 720 小时计）</p> </td> <td> <p>10 × 720 = 7200 CU</p> </td> <td> <p><span>7200 × 0.00025 = CNY 1.8</span> </p> </td> </tr> </tbody> </table>

## 公网流量
公网流量将基于[云数据传输CDT](https://help.aliyun.com/document_detail/2357716.html)进行统一计费和出账。详细信息，请参见[CDT公网流量定价](https://help.aliyun.com/document_detail/410942.html)。

## 各地域定价
算力 CU、网关 CU、存储 CU 与协作专享管控面的地域单价如下。

### 中国内地地域

<table> <thead> <tr> <td> <p><b>地域</b></p> </td> <td> <p><b>算力 CU<span>（元/CU）</span></b></p> </td> <td> <p><b>网关 CU<span>（元/CU）</span></b></p> </td> <td> <p><b>存储 CU<span>（元/CU）</span></b></p> </td> <td> <p><b>协作专享管控面<span>（元/小时）</span></b></p> </td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td> <p>北京、杭州、上海、深圳</p> </td> <td> <p><span>0.0000694</span> </p> </td> <td> <p><span>0.0000015</span> </p> </td> <td> <p><span>0.00025</span> </p> </td> <td> <p>3</p> </td> </tr> </tbody> </table>

<br />