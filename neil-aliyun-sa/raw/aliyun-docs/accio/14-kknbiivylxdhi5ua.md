# 应用授权

> **来源**：Accio Work 知识库（公开语雀）
> **URL**：https://acciowork.yuque.com/rfmg8t/ieb85b/kknbiivylxdhi5ua
> **TOC 层级**：lvl2
> **SHA256**：ca6419344bdca62393215fc0a0cda52012bdd0d46aa20697cbcba0e7c4a0e427
> **归档日期**：2026-08-10 ｜ **状态**：raw（不可变）

---

[此处为语雀卡片，点击链接查看](https://www.yuque.com/docs/268988060#tDxmI)

## **一、概述**
Accio Work 的应用授权是实现 Agent 自动化执行任务的关键。它允许 Agent 连接并操作你常用的第三方软件（如微信、钉钉、国际站等），从而从“对话”转向“行动”。

## **二、核心作用**
+ **赋予行动力：**授权后，Agent 不再只是回答问题，而是能代表你执行操作，例如发送消息、更新店铺商品、同步订单等。
+ **数据实时化：**允许 Agent 访问第三方平台中的实时数据，确保其处理任务时拥有最新的上下文。

## **三、支持授权的第三方平台**
具体以实际用户端支持授权的版本为准

| **分类** | **第三方平台** | **主要功能 / 权限描述** |
| :--- | :--- | :--- |
| 通讯/办公类 | Gmail 邮箱 | 完整管理邮件、标签与基础设置 |
| | 飞书 (Feishu) | 管理多维表格、访问云文档和日历 |
| 社交媒体类 | X (Twitter) | 读取推文、搜索对话并追踪趋势 |
| | Instagram | 访问账号、媒体和互动数据 |
| | LinkedIn | 访问个人档案、公司数据和职位洞察 |
| 跨境电商类 | Alibaba.com | 探索供应商、商品与贸易数据 |
| 技术开发与协作 | GitHub | 管理仓库、协作开发并跟踪问题 |
| AI 创意与生成 | Higgsfield | 用自然语言生成 AI 图片、视频和语音 |


## **四、常见问题（FAQ）**
#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">连接失败怎么办？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> </font>请按以下顺序检查：

+ 确认网络连接正常，且可访问对应的第三方服务
+ 若使用 API Key，确认其正确且具备所需权限
+ 尝试断开后重新连接

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">连接会过期吗？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>** 会。部分平台出于安全要求需要定期重新授权。

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">我的数据安全吗？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>** Accio Work 仅在你明确授权后才访问数据。你可以随时在 Accio Work 或第三方平台中撤销授权。

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">权限策略有哪些类型？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>** **<font style="color:rgb(17, 24, 39);">allow：</font>**<font style="color:rgb(75, 85, 99);">直接执行，无需确认</font>

**<font style="color:rgb(17, 24, 39);">ask：</font>**<font style="color:rgb(75, 85, 99);">每次执行前都需要你确认</font>

**<font style="color:rgb(17, 24, 39);">ask_once：</font>**<font style="color:rgb(75, 85, 99);">首次确认后，后续自动批准</font>

**<font style="color:rgb(17, 24, 39);">deny：</font>**<font style="color:rgb(75, 85, 99);">始终拒绝，不允许执行</font>

## **五、一页纸介绍**
![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298274454-03f06701-fdc3-4508-a3e8-d7af8bb95a55.png)

