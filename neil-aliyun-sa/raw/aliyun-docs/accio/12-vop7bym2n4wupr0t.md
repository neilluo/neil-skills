# 技能（Skills）

> **来源**：Accio Work 知识库（公开语雀）
> **URL**：https://acciowork.yuque.com/rfmg8t/ieb85b/vop7bym2n4wupr0t
> **TOC 层级**：lvl2
> **SHA256**：dbe065cd8edc31acf82789cfb0d4bca88f8ca504f89c465d10f8562f84e49ff3
> **归档日期**：2026-08-10 ｜ **状态**：raw（不可变）

---

[此处为语雀卡片，点击链接查看](https://www.yuque.com/docs/268988213#GAh5B)

## **一、概述**
技能本质上是结构化文档，为 Agent 提供特定领域的知识和操作能力。Agent 可以从技能市场搜索安装，也可以自行创建私有技能。

## **二、操作步骤 **
| **步骤** | **路径** | **图片** |
| :--- | :--- | :--- |
| 1 | Accio Work左侧导航栏 ->插件 ->技能 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1779784338676-e36505c0-18ae-4b5d-a6f7-09df1266bf05.png) |
| 2 | 从技能市场中搜索你需要的技能，点击安装 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1779784390385-02b3f675-556e-4203-9a6d-65db2344ffff.png) |
| 3 | 确保技能状态打开，并且在当前 Agent 的配置中添加该技能 | ![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298341958-11a222b8-868a-4664-a81f-6b3e4f8fa139.png)<br/>![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298342109-26f9c9aa-be38-450f-ad33-c1a0d521c303.png) |


## **三、常见问题（FAQ）**
#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">为什么安装的技能没被使用？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> 请检查以下两点（两者都需要开启，技能才能生效。）：</font>

+ <font style="color:rgb(75, 85, 99);">该技能在 Skills 页面中是否为 </font>**<font style="color:rgb(17, 24, 39);">「Enabled」</font>**<font style="color:rgb(75, 85, 99);"> 状态</font>
+ <font style="color:rgb(75, 85, 99);">在当前 Agent 的配置中是否被设置为 </font>**<font style="color:rgb(17, 24, 39);">「Selected」</font>**

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">一个 Agent 可以同时使用多个技能吗？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> 可以。Agent 会根据你的任务自动判断并组合多个技能。你不需要手动指定使用哪个技能，系统会自动选择最合适的组合。</font>

> 提示：但如果一个 Agent 装了太多不相关的技能，可能会出现调用不够精准的情况。建议将不同职责的任务拆分为多个 Agent，每个 Agent 只装与其职责相关的技能。
>

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">可以创建自己的技能吗？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> 可以。你可以按照现有技能的格式创建自己的文件夹或压缩包，上传技能</font>

![](https://cdn.nlark.com/yuque/0/2026/png/28328816/1778298341940-d871303b-a398-4131-ae99-9193d2fd9a12.png)

#### **<font style="color:rgb(17, 24, 39);">Q：</font>****<font style="color:rgb(17, 24, 39);">Agent 会自动学习新技能吗？</font>**
**<font style="color:rgb(17, 24, 39);">A：</font>**<font style="color:rgb(75, 85, 99);"> 会。在以下情况下，Agent 可能会自动学习新技能：</font>

+ <font style="color:rgb(75, 85, 99);">当 Agent 发现某些复杂任务被</font>**<font style="color:rgb(17, 24, 39);">重复执行</font>**<font style="color:rgb(75, 85, 99);">时，它可能会建议或自动生成新技能</font>
+ <font style="color:rgb(75, 85, 99);">你在对话中教给它的新工作方式，也可以被</font>**<font style="color:rgb(17, 24, 39);">固化为技能</font>**

