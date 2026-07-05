# Vaults（密钥管理）

> 安全地存储凭据并注入到 Agent Session。

## 核心概念

| 概念 | 说明 |
|------|------|
| Vault | 凭证容器 |
| Credential | 单条凭证，绑定到 MCP 服务器 URL |
| `protocol` | 仅支持 `streamable_http` |
| `type` | 仅支持 `static_bearer` |

## 安全性

* `access_token` **永远不会**在 API 响应中返回
* 凭证加密存储
* 仅关联的 Session 可在运行时访问

## 创建 Vault

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/vaults \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "我的 GitHub 凭证",
    "credentials": [
      {
        "mcp_server_url": "https://mcp.github.com/mcp",
        "protocol": "streamable_http",
        "type": "static_bearer",
        "access_token": "ghp_xxxxxxxxxxxx"
      }
    ]
  }'
```

## 在 Session 中使用

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "agent_xxx",
    "vault_ids": ["vault_xxx"]
  }'
```

## 常见问题

**Q: 能否更新已有 Token？**
A: 删除旧 Credential 并重新创建。

**Q: Token 泄露怎么办？**
A: 立即删除 Credential 并在第三方平台吊销 Token。

**Q: 能查看已存储的 Token 吗？**
A: 不能。写入后不可读取，只能删除重建。
