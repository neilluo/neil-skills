# Cloud Mode

> 来源: https://docs.qoder.com/zh/cli/cloud-mode

## 概述

`--remote` 模式让 Qoder CLI 任务在 Qoder 管理的云端虚拟机中执行。本地无需保持开机或活跃状态，全流程托管在云端。

## 适用场景

- 长时任务：训练、批量重构，本地不便长时间占用
- 离线发起：飞机/地铁写 prompt，回来看结果
- 统一环境：团队共享一致依赖与工具集
- 资源隔离：独立 CPU/内存/网络配额

## 使用

```bash
qodercli --remote "review the auth middleware and suggest improvements"
```

执行后 CLI 会：
1. 在远程环境创建 Cloud Session
2. 发送任务到云端 Agent
3. 实时流式打印输出到本地终端
4. 完成后打印会话 URL（可 Web 端追溯）

关闭本地终端后云端仍继续执行。

## 环境选择

TUI 中 `/remote-env` 选择默认云端环境。配置保存在：
```json
{
  "remote": {
    "defaultCloudEnvironmentId": "env_01kq..."
  }
}
```

## 特性

- 中断行为：Ctrl+C 仅断开本地订阅，云端继续
- 需要 GitHub 授权：Qoder 官网 > 服务集成 > Github 集成
- 支持多个并行 --remote 任务
- 不能读取本地未保存修改（访问 Remote GitHub 项目）
