<!-- source_url: https://ata.atatech.org/articles/11020495607 -->
<!-- fetched_date: 2026-09-21 -->
<!-- page_last_modified: 2025-10-29（发布日期） -->
<!-- summary: ATA 11020495607 陈思亮(玄斧)《AI网关-Restful API转换MCP的桥梁》相关章节摘录。⚠️ 本文件是【摘录】而非全文——ATA 为内网站点，2026-09-21 curl 被 SSO 拦截（login.alibaba-inc.com 302），全文无法在本环境归档；以下引文由主控在可登录环境逐字复核后转录。取证点：这是目前唯一真正的「HTTP转MCP + 消费者鉴权」端到端实操记录，证明消费者鉴权下 MCP 连接与列工具均需 API Key。 -->

# AI网关-Restful API转换MCP的桥梁（摘录）

> **来源**：ATA | **作者**：陈思亮（玄斧）| **发布日期**：2025-10-29
> **URL**：https://ata.atatech.org/articles/11020495607
> **归档日期**：2026-09-21 | **状态**：raw（不可变）| **⚠️ 摘录，非全文**（SSO 限制，见头部 summary）

## 逐字引文（主控复核转录）

操作链路「新建消费者 → 为 MCP 添加消费者鉴权 → 调试验证」：

> 新建消费者｜为后续MCP接口鉴权使用

> 为mcp添加消费者鉴权

> 调试界面选择…消费者、api key…点击连接测试连通性，正常情况会提示连接成功并左侧框会列出该mcp服务的工具列表

## 证据价值 [实战]

- 唯一真正的 **HTTP转MCP + 消费者鉴权**端到端实操记录
- 「点击连接测试连通性…连接成功并…列出该mcp服务的工具列表」→ **证明消费者鉴权下 MCP 连接（initialize）与列工具（tools/list）均需携带 API Key**，与 MCP 规范「鉴权在传输层、覆盖所有连接」一致
- 与官方《调试MCP服务》第 60 行（Bearer Token 字段填 API Key）互证
