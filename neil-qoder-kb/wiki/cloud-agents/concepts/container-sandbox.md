# 容器沙箱

> Session 运行的隔离容器环境规格、资源限制和文件持久化规则。

## 概述

每个 Session 运行在独立的容器沙箱中，Session 之间无法互相访问。容器基于 Ubuntu 22.04 LTS，以 root 身份执行，预装主流语言运行时和系统工具。

## 操作系统

| 项目 | 值 |
|------|---|
| 发行版 | Ubuntu 22.04 LTS (Jammy) |
| 架构 | x86_64 (amd64) |
| 内核 | Linux 5.10.134 |

## 预装工具

### 系统工具

git 2.34+、curl 7.81+、wget 1.21+、jq 1.6+、vim 8.2+、unzip/tar、ssh (OpenSSH 8.9+)、make 4.3+

### 语言运行时

| 语言 | 版本 | 包管理器 |
|------|------|------|
| Python | 3.12.x | pip 24+ |
| Node.js | 20.x LTS | npm 10+ |
| Go | 1.22.x | go mod |

## 资源限制

| 资源 | 默认限制 |
|------|------|
| CPU | 4 vCPU |
| 内存 | 8 GB |
| 磁盘 | 25 GB（约 18 GB 可用） |
| 执行时长 | 30 分钟/Turn |

## 目录结构

| 路径 | 用途 |
|------|------|
| `/app` | 默认工作目录 (cwd) |
| `/data` | `$HOME` 目录 |
| `/data/.qoder/awareness/` | Memory Store Entry 挂载点 |

## 文件持久化规则

- 同一 Session 内，文件在 Turn 之间保持
- 容器临时存储仅保留 **24 小时**
- Session 结束后容器及文件**立即销毁**
- 重要文件应通过 [[file]] API 上传到平台存储

## 环境变量

| 变量 | 值 |
|------|---|
| HOME | /data |
| SHELL | /bin/bash |
| LANG | en_US.UTF-8 |

## 额外软件安装

通过 [[environment]] 的 `packages` 字段在启动时安装：

```json
{"config": {"packages": {"apt": ["postgresql-client", "ffmpeg"]}}}
```

## 执行身份

以 **root** 身份执行，无需 `sudo`。

## 交叉引用

- [[environment]] — 容器环境的配置入口
- [[session]] — 容器服务于 Session
- [[file]] — 文件持久化到平台存储
- [[memory-store]] — Entry 挂载到容器内

## 来源

- raw/cloud-agents/container-reference.md [official-docs] 2026-06-21
- raw/cloud-agents/environments.md [official-docs] 2026-06-21
