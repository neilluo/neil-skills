# 定时任务

> **来源**：Accio Work 知识库（公开语雀）
> **URL**：https://acciowork.yuque.com/rfmg8t/ieb85b/yastr45hrg4twwbp
> **TOC 层级**：lvl2
> **SHA256**：7d90be09887920670f58e3ade40349834ca370be3df2d492220e0eea85abbdec
> **归档日期**：2026-08-10 ｜ **状态**：raw（不可变）

---

[此处为语雀卡片，点击链接查看](https://www.yuque.com/docs/268987708#sC7oR)

## **一、概述**
自动化可以让你为 Agent 设置基于时间的规则，使其在特定时间或间隔自动执行任务，无需手动发送消息。目前自动化支持三种执行方式：

| **类型** | **说明** | **示例** |
| :--- | :--- | :--- |
| **延迟执行** | 一段时间后执行一次 | 「30 分钟后提醒我开会」 |
| **定时执行** | 在指定时间点执行 | 「明天早上 9 点总结新闻」 |
| **循环执行** | 按固定间隔重复执行 | 「每隔 2 小时检查一次竞品价格」 |


## **二、操作步骤 **
| **步骤** | **路径** | **图片** |
| :--- | :--- | :--- |
| 1 | Accio Work左侧->定时任务 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298132173-28bbdd16-283d-45a8-b4db-192233fe358f.png) |
| 2 | 点击 右上角 + 新建任务 ，设置好关联的智能体和模型、定时任务时间、周期等相关信息。 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298132168-3586db9f-8721-4333-acf8-5efc6362dbba.png) |
| 3 | 创建定时任务后，可以查看定时任务列表，支持编辑、删除或者点击立即运行进行一次测试 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298132292-9c232303-2bdc-4e65-b922-d108977f92a1.png) |


## **三、常见问题（FAQ）**
#### **<font style="color:rgb(17, 24, 39);">Q：</font>****关机后自动化任务还会运行吗？**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> </font>重启 Accio Work 后，系统会自动检查错过的任务：

+ 一次性任务：如果间隔不久，会立即补跑
+ 定时任务：从当前时间恢复正常调度

#### **<font style="color:rgb(17, 24, 39);">Q：</font>**在哪里查看自动化任务的结果？
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> </font><font style="color:rgb(17, 24, 39);">你会在对应会话窗口中看到 Agent 的回复。这些回复通常带有绿色的**「定时」标签**，便于与手动消息区分。</font>

#### **<font style="color:rgb(17, 24, 39);">Q：为什么某些自动化任务失败了？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> 常见原因是任务执行需要</font>**<font style="color:rgb(17, 24, 39);">额外授权</font>**<font style="color:rgb(75, 85, 99);">，例如写入受保护的文</font><font style="color:rgb(17, 24, 39);">件。建议： 先在对话中手动测试指令，确认权限已授予后再开启自动化。</font>

