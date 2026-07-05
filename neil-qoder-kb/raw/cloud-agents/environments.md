# 云端环境配置

> 选择 Agent 运行的容器、网络与依赖。

Environment 定义了 Session 运行的容器模板——操作系统、网络策略、预装依赖。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | — | 系统生成，`env_` 前缀 |
| `name` | string | 是 | 环境名称 |
| `description` | string | 否 | 描述信息 |
| `config.type` | string | 是 | 容器类型，固定为 `"cloud"` |
| `config.networking` | object | 否 | 网络策略 |
| `config.packages` | object | 否 | 预装依赖包配置 |

## 网络策略

`config.networking` 支持三种模式（**必须使用对象格式**）：

| 模式 | 配置 | 说明 |
|------|------|------|
| 完全开放 | `{"type": "unrestricted"}` | 容器可以访问任意外部地址 |
| 受限 | `{"type": "limited", "allow_package_managers": true}` | 仅允许包管理器访问 |
| 白名单 | `{"type": "allowed_hosts", "allowed_hosts": [...]}` | 仅允许指定主机名 |

## 预装依赖

```json
{
  "config": {
    "type": "cloud",
    "networking": {"type": "unrestricted"},
    "packages": {
      "apt": ["git", "build-essential"],
      "pip": ["pandas", "numpy"],
      "npm": ["typescript", "eslint"]
    }
  }
}
```

## 创建环境

```bash
curl -s -X POST https://api.qoder.com/api/v1/cloud/environments \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-science",
    "config": {
      "type": "cloud",
      "networking": {"type": "unrestricted"},
      "packages": {
        "pip": ["pandas", "numpy", "matplotlib", "scikit-learn"]
      }
    }
  }'
```

## 更新环境

```bash
curl -s -X PUT https://api.qoder.com/api/v1/cloud/environments/env_xxx \
  -H "Authorization: Bearer $QODER_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data-science",
    "config": {
      "type": "cloud",
      "networking": {"type": "unrestricted"},
      "packages": {
        "pip": ["pandas", "numpy", "matplotlib", "scikit-learn", "sqlalchemy"]
      }
    }
  }'
```

> 更新环境不会影响已运行的 Session。新配置仅对后续创建的 Session 生效。

## 环境选型建议

| 场景 | 推荐配置 |
|------|------|
| 通用开发 | 无需额外配置 |
| 数据分析 | 预装 pandas/numpy，开放网络 |
| 安全审计 | 白名单网络，最小依赖 |
| 前端开发 | 预装 Node.js 生态工具 |

## 常见问题

**Q: 环境创建后需要等待多久？**
A: 状态直接为 `ready`。容器初始化发生在 Session 启动时。

**Q: 预装包可以指定版本吗？**
A: pip/npm 支持版本指定，如 `"pandas==2.1.0"`。apt 使用系统源默认版本。
