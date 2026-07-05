# 容器参考

> 容器类型、网络策略和预装包参考。

## 操作系统

| 项目 | 值 |
|------|---|
| 发行版 | Ubuntu 22.04 LTS (Jammy) |
| 架构 | x86_64 (amd64) |
| 内核 | Linux 5.10.134 |

## 预装工具

### 系统工具

| 工具 | 版本 |
|------|------|
| git | 2.34+ |
| curl | 7.81+ |
| wget | 1.21+ |
| jq | 1.6+ |
| vim | 8.2+ |
| unzip/tar | 系统版 |
| ssh | OpenSSH 8.9+ |
| make | 4.3+ |

### 语言运行时

| 语言 | 版本 | 包管理器 |
|------|------|------|
| Python | 3.12.x | pip 24+ |
| Node.js | 20.x LTS | npm 10+ |
| Go | 1.22.x | go mod |

## 工作目录

默认 cwd：`/app`
`$HOME`：`/data`（与 cwd 不同目录）

## 额外软件安装

通过 Environment 的 `packages` 字段：

```json
{
  "config": {
    "packages": {
      "apt": ["postgresql-client", "redis-tools", "ffmpeg"]
    }
  }
}
```

## 资源限制

| 资源 | 默认限制 |
|------|------|
| CPU | 4 vCPU |
| 内存 | 8 GB |
| 磁盘 | 25 GB（约 18 GB 可用） |
| 执行时长 | 30 分钟/Turn |

## 文件持久化

* 同一 Session 内，文件在 Turn 之间保持
* 容器临时存储仅保留 **24 小时**
* Session 结束后容器及文件立即销毁
* 重要文件应通过 Files API 上传到平台存储

## 执行用户

以 **root** 身份执行。无需 `sudo`。

## 环境变量

| 变量 | 值 |
|------|---|
| HOME | /data |
| USER | （未设置） |
| SHELL | /bin/bash |
| LANG | en_US.UTF-8 |
