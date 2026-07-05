# 连接器（Connectors）

连接器是 QoderWork 与外部系统之间的桥梁。开启后，AI 可以操作浏览器、读写系统日历与邮件、对接 Microsoft 365、通过钉钉/飞书完成流程。

## 两类连接器

### 内置连接器
- **浏览器**：控制浏览器进行网页操作、数据提取与表单自动填写（仅 Chromium 内核）
- **macOS 应用**：读写 Mac 原生的日历、提醒事项、备忘录、邮件及通讯录
- **Microsoft 365**：读写 Outlook 邮件/日历/待办/联系人/OneNote/OneDrive

### 集成市场
一键安装并连接企业协作平台及第三方 SaaS：钉钉、飞书、Notion、Linear、Todoist、Canva、Supabase、Vercel、Neon、Slack、Figma、Google 日历、Google 地图、LINE、企查查等。也可手动添加自定义 MCP 服务。

所有连接器默认关闭，需明确授权后才获取访问权限。

## 浏览器连接器

核心能力：
- 共享登录态：在已登录的浏览器中运行
- 自然语言驱动：无需写脚本
- 页面感知与交互：理解 UI 元素，执行点击/输入/滚动
- 数据提取与整理：输出表格/Markdown/文件
- 多标签页操作

接入方式：安装 Chrome 扩展 → 确认连接成功

来源：https://docs.qoder.com/zh/qoderwork/connectors
