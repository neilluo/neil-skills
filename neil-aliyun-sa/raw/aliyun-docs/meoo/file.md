> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 技能创建和使用

# **Skills(技能)介绍**

Skill（技能）是一种模块化的能力封装机制，它将特定领域的专业知识、操作流程与最佳实践打包为可复用的功能单元。**如果说Prompt是临时性、一次性的指令，Skill则是对专业且流程化的需求说明进行结构化封装，形成可在对话或AI编程中复用的插件化工具包。**

通过Skill，系统能够像人类专家一样，针对不同任务场景动态调用相应的专业能力。例如，构建"视觉设计优化"Skill，当用户请求任何可视化输出（如演示文稿、仪表盘、HTML页面、报告、电子表格、PDF或数据可视化）时，系统将自动启用该设计优化技能，对交付物进行专业化视觉提升。

<Note>
  **秒悟Skills 是一组可重复被利用的工具包，利用 Meoo Skills + AI Coding 你可以快速构建一个具备业务领域知识，使用内部 API 调用的 Meoo 原生应用。**
</Note>

# **应用场景**

✨什么时候需要使用技能？

> 任何时候都能用

任何时候你想扩展秒悟（Meoo）的能力边界，你都可以使用 Skill 来进行强化，打造属于你的独一无二的 Skill 和产品。包括但不限于:

* 使用沉淀的业务知识库，组件库，模版，脚本等。快速创建一个符合团队规范的 Meoo 应用
* 需要在多个项目中共用的功能片段
* 做测试，做报表，调用 api，调用 hsf，http 接口
* 自定义SubAgent

**... ...**

Skill 给了大家充分的想象和定制空间，欢迎大家不断探索～

# **构建技能**

## **步骤一：输入提示词**

1. 选中 **技能构建**，在对话框中描述你想构建的技能，点击按钮， 秒悟即刻开始自动进行计划和执行，完成技能构建。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/2CgJQZU1_WMIMylx/images/image-38.png?fit=max&auto=format&n=2CgJQZU1_WMIMylx&q=85&s=be261132e589dce3862172d7e0c47f78" alt="Image" width="1519" height="552" data-path="images/image-38.png" />
   </Frame>
2. 自然语言构建技能的最佳实践
   * 目标清晰：精准定义最终效果，明确功能边界与使用场景
   * 步骤明确：拆解执行流程，按顺序描述操作逻辑与规则
   * 约束具体：写明异常处理、参数限制、输出格式等规则
   * 场景完整：覆盖主流使用场景，明确触发条件与交互逻辑
     <Note>
       **完整Skill构建示例（天气查询Skill）**
       为用户提供全国城市实时天气查询，仅支持国内地级市，不提供预报外数据；
       执行步骤为接收城市名称→校验城市合法性→请求天气接口→整理数据并回复；
       仅支持中文城市名，无结果提示重新输入，接口异常返回统一提示；
       支持直接问城市天气、切换城市查询，自动识别提问意图响应。
     </Note>
3. 对话增强功能：如有更复杂需求，秒悟支持上传文件、选择模型、上传技能，帮助构建更适用于复杂场景的skill技能。
   * 上传图片和视频：支持上传图片和视频。
   * 选择模型：根据所构建技能的需要，支持选择多种不同的底层模型。其中Kimi 2.5效果稳定，GLM-5/MiniMax-M2.5解决复杂问题效果较好。
   * 上传技能：支持上传本地技能包。

## **步骤二：优化技能**

✨浏览秒悟生成的技能，有两种方式进行技能优化和修改。

1. 在**对话窗口**，输入修改指令，秒悟将根据你的需求自动进行修改和优化。对于输入的修改指令，还可以点击 **润色** 功能，让Meoo帮助进行润色修改。
2. 或者点击 **编辑**，可以在编辑模式下直接对生成的技能进行编辑和修改。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/6bad4cc2086dc1d69dfffcf0299cb57d.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=00573d1a178405d1f80170bda9fd8d8a" alt="6bad4cc2086dc1d69dfffcf0299cb57d" width="2256" height="1264" data-path="images/6bad4cc2086dc1d69dfffcf0299cb57d.png" />
</Frame>

## **步骤三：生成技能**

✨点击 **发布技能**，根据需要修改填写技能名称、简要描述、技能标签和是否上架到技能市场，点击 **立即发布**，完成技能构建，生成一个可用技能。接下来你可以在秒悟技能商店里查看和管理你的技能或者在创建应用时使用技能。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/89476cc9f5d92202f194ffebc8ceb6ab.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=676729be900b924f643bcdc4556dc1a0" alt="89476cc9f5d92202f194ffebc8ceb6ab" width="2256" height="1264" data-path="images/89476cc9f5d92202f194ffebc8ceb6ab.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/cef4b7549c1c0b114f04cfd3327115e7.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=c1b216e1eb94456d7f6c6818971230e4" alt="Cef4b7549c1c0b114f04cfd3327115e7" width="1646" height="1044" data-path="images/cef4b7549c1c0b114f04cfd3327115e7.png" />
</Frame>

# **应用技能**

<Note>
  **单个应用一次集成，永久使用**
</Note>

## **方式一**

在秒悟技能市场找到自己心仪的技能，点击 **添加**，然后点击 **使用技能**，即可在创建应用对话框中使用技能

<Note>
  秒悟技能市场：[https://meoo.com/skills](https://meoo.com/skills)
</Note>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/qEOfTlOsYmlDw7SD/images/1773732011120_4976cfdde0094aa1ab8ea9d89461fe2a.png?fit=max&auto=format&n=qEOfTlOsYmlDw7SD&q=85&s=1bc841473e478f64aa859699d1f1c490" alt="1773732011120 4976cfdde0094aa1ab8ea9d89461fe2a" width="1196" height="1011" data-path="images/1773732011120_4976cfdde0094aa1ab8ea9d89461fe2a.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/qEOfTlOsYmlDw7SD/images/1773732017987_b5b5d7be9eea413ca76424ddb9f38d33.png?fit=max&auto=format&n=qEOfTlOsYmlDw7SD&q=85&s=e04c655948bfed72eb4c90c48caabd95" alt="1773732017987 B5b5d7be9eea413ca76424ddb9f38d33" width="1175" height="539" data-path="images/1773732017987_b5b5d7be9eea413ca76424ddb9f38d33.png" />
</Frame>

## 方式二

在对话页面点击 **技能** 按钮，选择对应的技能即可集成。还支持技能搜索、技能管理、去技能市场发现更多技能。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/cef4b7549c1c0b114f04cfd3327115e7.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=c1b216e1eb94456d7f6c6818971230e4" alt="Cef4b7549c1c0b114f04cfd3327115e7" width="1646" height="1044" data-path="images/cef4b7549c1c0b114f04cfd3327115e7.png" />
</Frame>

# **FAQ**

问：已经上线的技能该如何迭代优化？

答：已上线的技能迭代优化大体有以下5个步骤

1. 数据驱动定位问题：通过技能日志、失败案例、用户反馈，精准找到意图识别错误、答非所问、调用异常等实际问题，不凭感觉修改。
2. 精准修复确保稳定：只针对问题点做小范围优化，不改动核心流程；明确技能适用范围，增加拒识规则，减少误触发，保证技能稳定。
3. 结构化与体验双重提升：规范输入输出格式，提前校验必填信息；优化多轮对话记忆能力，减少重复提问，统一异常回复话术。
4. 闭环案例+回归验证：把所有问题案例整理成库，每次优化后都跑全量测试，确保新升级不影响原有功能，不出现新问题。
5. 灰度发布安全上线：先小范围放量测试，指标稳定后再全量上线；保留历史版本，出现问题可快速回退，降低上线风险。
