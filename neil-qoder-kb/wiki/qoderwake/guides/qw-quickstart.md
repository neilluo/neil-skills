# QoderWake 快速开始

> 从零开始：安装 QoderWake → 创建第一个数字员工 → 给他派活，三步完成。

## 概述

本指南带你在 5 分钟内完成 QoderWake 的安装、创建第一个 Waker、并成功派出第一个任务。适用于 macOS 和 Linux 环境。

## 详细内容

### Step 1: 安装与启动

**环境要求**：
- macOS 13.0+ 或 Ubuntu 22.04 LTS+
- 已安装 git 并完成仓库认证配置
- 外部网络可用（用于登录、模型调用）

**安装命令**：

```bash
curl -fsSL https://qoder-ide.oss-ap-southeast-1.aliyuncs.com/qoderwake/install.sh | bash
```

脚本自动完成：检测平台 → 下载校验 → 安装主程序 → 启动登录 → 打开控制台。

**macOS 直接下载**：
- Apple 芯片：`qoderwake_latest_darwin_arm64.dmg`
- Intel 芯片：`qoderwake_latest_darwin_amd64.dmg`

命令入口：`~/.qoderwake/bin/qoderwake`

### Step 2: 创建数字员工

1. 浏览器访问 `http://127.0.0.1:19820/`
2. 点击左侧"创建 Waker"
3. 选择角色模板（推荐从"后端工程师"开始）
4. 填写名字、确认保存

### Step 3: 给员工派活

进入 Waker 对话页面，直接输入需求发送：
- 例："帮我排查这个报错的根因并给出最小修复方案"
- 附上报错信息或相关文件
- 员工开始干活，过程中需要审批会弹卡片

### 控制台界面说明

| 区域 | 功能 |
|------|------|
| 左侧边栏 | "我的 Waker"列表，显示所有已创建员工 |
| 顶部按钮 | "创建 Waker" + 新建任务 |
| 主区域 | 对话页面，直接派活 |
| 右侧边栏 | 任务列表及运行详情 |

## 交叉引用

- [[waker]] — 创建的数字员工实体
- [[role]] — 角色模板选择
- [[task-types]] — 三种任务驱动方式
- [[waker-config-guide]] — 创建后的完整配置指南

## 来源

- raw/qoderwake/installation.md [official-docs] 2026-06-28
- raw/qoderwake/create-waker.md [official-docs] 2026-06-28
- raw/qoderwake/conversation-tasks.md [official-docs] 2026-06-28
