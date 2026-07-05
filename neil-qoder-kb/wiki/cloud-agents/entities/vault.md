# Vault

> 安全存储凭据并注入到 Agent Session 的密钥管理系统。

## 概述

Vault 是凭证（secret/密钥）的安全容器。凭证加密存储，`access_token` 永远不会在 API 响应中返回（写入后不可读取）。仅关联的 Session 可在运行时访问 secret 凭证。当前仅支持 `streamable_http` 协议和 `static_bearer` 类型。

## 核心概念

| 概念 | 说明 |
|------|------|
| Vault | 凭证容器，可包含多条 Credential |
| Credential | 单条凭证，绑定到 MCP 服务器 URL |
| `protocol` | 仅支持 `streamable_http` |
| `type` | 仅支持 `static_bearer` |

## 安全特性

- `access_token` **永远不会**在响应中返回
- 凭证加密存储
- 仅关联的 Session 可在运行时访问
- 不支持读取已存储的 Token，只能删除重建

## 创建 Vault

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/vaults \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "GitHub 凭证",
    "credentials": [{
      "mcp_server_url": "https://mcp.github.com/mcp",
      "protocol": "streamable_http",
      "type": "static_bearer",
      "access_token": "ghp_xxxxxxxxxxxx"
    }]
  }'
```

## 在 Session 中使用

```bash
curl -X POST https://api.qoder.com/api/v1/cloud/sessions \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"agent": "agent_xxx", "vault_ids": ["vault_xxx"]}'
```

## 凭证管理

- **更新 Token**：删除旧 Credential 并重新创建
- **Token 泄露**：立即删除 Credential + 在第三方平台吊销
- **查看 Token**：不支持，只能删除重建

## 交叉引用

- [[session]] — Vault 关联到 Session
- [[agent]] — Agent 通过 MCP 服务器使用凭证
- [[permission-model]] — 凭证访问的安全控制

## 来源

- raw/cloud-agents/vaults.md [official-docs] 2026-06-21
