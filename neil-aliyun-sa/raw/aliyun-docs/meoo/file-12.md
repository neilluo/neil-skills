> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 秒悟使用技巧

# 提示词

1. 开始阶段描述需求的正确方式
   * 描述**目标用户**是谁
   * 描述**核心功能**有哪些
   * 描述**页面结构**和流程
   * 描述**角色权限**（普通用户/管理员）
2. 开始阶段提升应用创建效果的两种方式
   * 方式一：输入提示词后，使用 润色 功能，让AI进行提示词润色 方
   * 式二：输入提示词后，使用 Plan 模式，让AI进行规划，对规划进行修改审查后再开始
   <Note>
     方式二会增加token消耗，适合比较模糊的一句话需求或新手使用
   </Note>
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gfZBsC21V2EbEhLc/images/image-236.png?fit=max&auto=format&n=gfZBsC21V2EbEhLc&q=85&s=718c426e0791587f5834501a8b1527e8" alt="Image" width="1450" height="750" data-path="images/image-236.png" />
   </Frame>

# 问题修复

<Note>
  出现问题时，建议让AI自行修复，一般经过3次左右的对话，AI能完成问题修复

  > 💡提示词举例：“数据上传失败，帮我分析原因并修正”
</Note>

## 问题修复技巧

* **截图反馈**：AI看不到你的屏幕，遇到问题时**截图**发给AI，同时描述问题
* **圈选需改**：使用 **圈选修改** 功能，选中预览页对应元素（可多选），同时描述问题

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/1778490021632_3889f2f307b54054afdc53697593887e.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=0a574adbf5da665c0c55b5dce31d6a5b" alt="1778490021632 3889f2f307b54054afdc53697593887e" width="2256" height="1264" data-path="images/1778490021632_3889f2f307b54054afdc53697593887e.png" />
</Frame>

## 常见问题处理方式

<Accordion title="管理员后台与用户权限">
  平台不提供独立的管理后台入口，建议做法：

  * 让AI在应用中做登录系统，通过用户身份区分普通用户和管理员
  * 管理员登录后显示管理功能，普通用户只看普通页面
    > 💡提示词举例："帮我做一个登录系统，根据用户角色（admin/user）跳转到不同页面，管理员可以看到所有订单，普通用户只能看自己的"
</Accordion>

<Accordion title="页面预览报错/功能异常">
  可尝试以下方式进行修复：

  * 告知问题，让AI自行debug（优先）
  * 不同模型能力有差异，切换模型（例如Qwen3.6-Plus或者Kimi 2.5）再次尝试修复
  * 打开 应用日志或浏览器控制台，将红色 JS error 报错信息复制给 AI，引导其修复
  * 回退历史版本，如果改坏了，直接回退到上一个可用版本，比反复需改更高效
</Accordion>

<Accordion title="任务转圈/卡住不动">
  对话栏转圈属于前端显示问题，任务实际已执行完成，不影响后续操作，可继续使用。如果项目页面一直无法加载，可依次尝试以下操作：

  * 刷新页面
  * 在对话框输入“**/** ” 唤起工具栏，点击 重启应用
  * 在对话中引导 AI 修复，例如输入： 项目未成功启动，目前无法预览，请分析项目构建或启动问题并修复
</Accordion>

## 寻求帮助

如果问题一直无法修复，点击 **头像** 里的 **问题反馈**，提交工单，寻求秒悟平台支持。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/75e37413fcdff043cf241af2171aae67.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=57dd3f7203cc64dc980a381e236550d9" alt="75e37413fcdff043cf241af2171aae67" width="2256" height="1264" data-path="images/75e37413fcdff043cf241af2171aae67.png" />
</Frame>

# 上下文管理

1. 为了防止AI无限制消耗积分，当已执行100轮对话时，平台会给出对应提示，此时按要求输入 **继续** 可继续进行任务执行。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/pyv3EkV9rBZPAe_b/images/31.png?fit=max&auto=format&n=pyv3EkV9rBZPAe_b&q=85&s=4a564d465752d7f9a2df1b669c9de753" alt="31" width="2256" height="1264" data-path="images/31.png" />
   </Frame>
2. 当项目上下文快满时，无需任何操作，平台会自动进行上下文压缩，压缩后不影响开发效果，会自动保留关键信息。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/15b0eb26943357566e9a45847f48e254.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=e5ba223e94334ab07836737d41e4d96a" alt="15b0eb26943357566e9a45847f48e254" width="2256" height="1264" data-path="images/15b0eb26943357566e9a45847f48e254.png" />
   </Frame>
