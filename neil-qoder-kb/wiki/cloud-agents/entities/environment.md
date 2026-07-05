# Environment

> Session 运行的容器环境模板，定义网络策略、预装依赖和资源配置。

## 概述

Environment 定义了 Session 运行的容器模板。它决定操作系统、网络策略和预装依赖。新账号没有预置环境，需手动创建。更新环境不影响已运行的 Session，仅对后续创建的 Session 生效。

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | — | 系统生成，`env_` 前缀 |
| `name` | string | 是 | 环境名称 |
| `description` | string | 否 | 描述信息 |
| `config.type` | string | 是 | 固定 `"cloud"` |
| `config.networking` | object | 否 | 网络策略（对象格式） |
| `config.packages` | object | 否 | 预装依赖包 |

## 网络策略

| 模式 | 配置 | 说明 |
|------|------|------|
| 完全开放 | `{"type": "unrestricted"}` | 可访问任意外部地址 |
| 受限 | `{"type": "limited", "allow_package_managers": true}` | 仅允许包管理器 |
| 白名单 | `{"type": "allowed_hosts", "allowed_hosts": [...]}` | 仅允许指定主机 |

## 预装依赖

支持 `apt`、`pip`、`npm` 三种包管理器：

```json
{
  "config": {
    "type": "cloud",
    "packages": {
      "apt": ["git", "build-essential"],
      "pip": ["pandas==2.1.0", "numpy"],
      "npm": ["typescript", "eslint"]
    }
  }
}
```

pip/npm 支持版本指定，apt 使用系统源默认版本。

## API 操作

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建 | POST | `/api/v1/cloud/environments` |
| 列表 | GET | `/api/v1/cloud/environments` |
| 更新 | PUT | `/api/v1/cloud/environments/{id}` |

## 环境选型建议

| 场景 | 推荐配置 |
|------|------|
| 通用开发 | 无需额外配置 |
| 数据分析 | 预装 pandas/numpy，开放网络 |
| 安全审计 | 白名单网络，最小依赖 |
| 前端开发 | 预装 Node.js 生态工具 |

## 交叉引用

- [[session]] — Environment 在 Session 中实例化
- [[container-sandbox]] — 容器的详细规格与限制
- [[agent]] — Agent 配置与 Environment 搭配使用

## 来源

- raw/cloud-agents/environments.md [official-docs] 2026-06-21
- raw/cloud-agents/container-reference.md [official-docs] 2026-06-21
