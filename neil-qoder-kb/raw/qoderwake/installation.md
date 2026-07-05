# 安装与启动

> 环境要求、在 macOS / Linux 上安装 QoderWake，以及打开本地控制台。

QoderWake 可以跑在你自己的设备或云桌面上。本页介绍环境要求、安装应用，以及打开本地控制台。

## 环境准备

QoderWake 支持本地部署和云端部署。建议部署在稳定在线、网络良好的常开设备或云桌面环境中，以保障数字员工 7×24 小时持续运行。

> **注意**：Windows 版本敬请期待，暂未对外开放，请先在 macOS 或 Linux 上使用。

### 本地部署

推荐部署在可长期稳定运行的本地设备上，例如 Mac mini，以获得更好的 7×24 小时运行体验。

* **macOS**：13.0 及以上版本。
* **Linux**：推荐 Ubuntu 22.04 LTS 及以上版本，需启用 GUI 桌面以使用本地 Web Console。

### 云端部署

支持主流云桌面和云主机环境。为方便浏览器登录和本地 Web 管理，推荐使用无影云电脑企业版或个人版。

* **Linux**：Ubuntu 22.04 及以上版本，需启用 GUI 桌面以使用本地 Web Console。

### 前置工具

产品预置多个软件研发类数字员工角色，安装前请先准备好 Git 环境，并确认当前账号能正常访问目标代码仓库：

* 已安装 `git`。
* 已完成仓库认证配置。
* 可以正常执行 `clone`、`pull`、`push` 操作。

本地或云端部署环境均需支持外部网络访问，用于用户登录、模型调用、代码仓库访问等。在企业网络、代理或防火墙环境下，请提前放通必要的 HTTPS 出站访问。

## 安装 QoderWake

### macOS

直接下载安装包：

* **Apple 芯片（ARM）**：[下载](https://download.qoder.com/qoderwake/installers/latest/qoderwake_latest_darwin_arm64.dmg)
* **Intel 芯片**：[下载](https://download.qoder.com/qoderwake/installers/latest/qoderwake_latest_darwin_amd64.dmg)

或者打开终端（应用程序中查找"终端"或 Terminal），运行：

```bash
curl -fsSL https://qoder-ide.oss-ap-southeast-1.aliyuncs.com/qoderwake/install.sh | bash
```

脚本会自动检测平台、下载并校验安装包、安装主程序和资源文件、把命令入口加入 `PATH`、启动浏览器登录、启动本地常驻服务并打开 Web Console。命令入口：`~/.qoderwake/bin/qoderwake`。

### Linux

打开终端，运行：

```bash
curl -fsSL https://qoder-ide.oss-ap-southeast-1.aliyuncs.com/qoderwake/install.sh | bash
```

安装脚本会自动完成：

1. **检测架构**：检测 Linux CPU 架构。
2. **下载并校验**：下载并校验对应平台的 QoderWake 安装包。
3. **安装主程序**：安装 QoderWake 主程序和资源文件，创建命令入口并尝试加入 `PATH`。
4. **登录并启动服务**：启动浏览器登录，登录后启动或重启本地常驻服务。
5. **打开控制台**：自动打开本地 Web Console。

命令入口：

```bash
~/.qoderwake/bin/qoderwake
```

默认 Web Console 地址：

```
http://127.0.0.1:19820
```

### Windows

> **注意**：Windows 版本敬请期待，正式发布后会在本页同步更新。

## 打开控制台

浏览器访问：`http://127.0.0.1:19820/`。这是 QoderWake 在你本机的管理台，员工管理、派活、配置权限都在这里完成。

界面说明：

* **左侧边栏**：展示"我的 Waker"列表，显示所有已创建的员工和最近活动时间。
* **顶部按钮**：点击"创建 Waker"快速新建员工，右侧支持新建任务。
* **主区域**：进入某个员工后默认打开对话页面，可直接派活。
* **右侧边栏**：查看已创建的任务及当前运行中任务的详情。

首次访问会引导你登录账户，按提示完成即可。
