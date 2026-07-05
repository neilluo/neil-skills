# Remote Control

> 来源: https://docs.qoder.com/zh/cli/remote-control

## 概述

Remote Control 让开发者离开电脑也能实时掌控正在跑的 CLI Agent，用手机/Web 在关键节点做出决策。

两种模式：
1. 远程控制模式：已有会话中开启远程监听
2. 守护进程模式：后台运行，手机端随时发起新任务

## 远程控制模式

适合：已启动 CLI 会话，临时需要离开但想继续监控。

```bash
/remote-control        # 开启（显示二维码和 URL）
/remote-control stop   # 停止
/remote-control status # 查看状态
```

连接后可以：
- 实时查看运行状态
- 对需审批操作进行交互
- 从移动端发送新任务

## 守护进程模式（Daemon）

适合：电脑保持待命，手机随时发起新任务。

```bash
qodercli remote-control    # 启动（显示二维码和 URL）
# Ctrl+C 退出
```

- 可连续发送多个任务
- CLI 按顺序或并行处理
- 所有文件保存在运行 CLI 的电脑上

## Web 端

浏览器访问 https://qoder.com/agents 管理远程任务。

## 与 Cloud Mode 的区别

- Remote Control：任务在本地执行，手机远程控制
- Cloud Mode（--remote）：任务在云端 VM 执行，本地仅作入口
