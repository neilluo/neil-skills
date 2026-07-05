# QoderWork Connector（连接器）

> 外部系统桥梁：让 AI 操作浏览器、读写系统应用、对接 SaaS 平台。

## 概述

连接器是 QoderWork 与外部系统之间的桥梁。没有连接器时只能处理对话和本地文件；有了连接器可以跨应用、跨系统完成工作。所有连接器默认关闭，需明确授权。

## 两类连接器

### 内置连接器
| 连接器 | 能力 |
|--------|------|
| 浏览器 | 控制 Chromium 浏览器进行网页操作、数据提取、表单自动填写 |
| macOS 应用 | 读写日历、提醒事项、备忘录、邮件、通讯录 |
| Microsoft 365 | Outlook 邮件/日历/待办/联系人/OneNote/OneDrive |

### 集成市场
一键安装：钉钉、飞书、Notion、Linear、Todoist、Canva、Supabase、Vercel、Neon、Slack、Figma、Google 日历/地图、LINE、企查查等。支持手动添加自定义 MCP 服务。

## 浏览器连接器特点
- 共享登录态（无需重新登录）
- 自然语言驱动（无需写脚本）
- 页面感知与交互（理解 UI 元素）
- 数据提取整理（输出表格/Markdown/文件）
- 多标签页操作
- 接入：安装 Chrome 扩展 → 确认连接

## 交叉引用
- [[qw-task]] — 连接器为任务提供外部系统能力
- [[qw-skill]] — 技能提供内部流程，连接器提供外部能力
- [[qw-computer-use]] — 电脑操控是另一种桌面应用交互方式
- [[qw-im-channel]] — IM 频道也是一种外部系统连接

## 来源
- raw/qoderwork/connectors.md [official-docs]
