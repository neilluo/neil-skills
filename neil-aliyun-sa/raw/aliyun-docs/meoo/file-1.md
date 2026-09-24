> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 功能介绍-网页应用搭建

**✨一句话生成完整项目代码，支持数据库（云服务）自动创建**

* **一句话生成全栈代码：** 这是我们的核心能力，只需用自然语言描述你的需求\_（例如：“我需要一个带有搜索框和导航菜单的响应式电商产品列表页面”），将立即为您生成结构清晰、语义化且可高度定制的代码。
* **一键部署与发布：** 代码生成后，无需复杂的环境配置和命令行操作，一键即可将您的应用部署到云端，快速上线，实现从创意到发布的极速。
* **支持自动创建数据库：** 打破前端与后端的界限，支持自动创建数据库并根据页面内容自动写入数据，让您的应用能够轻松实现数据的增删改查，构建完整的全栈应用。
* **多人实时协作：** 团队成员可以在同一项目空间内共同编辑代码，无论身处何地，都能保持高效同步。代码版本控制、权限管理一应俱全。

### **步骤一：描述功能需求**

1. **创建应用并描述需求**  a. **进入秒悟网站首页，根据需求选择应用类型（网页应用，支持web和H5页面双端适配）**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/zCBrVE9ZClJmxGFR/images/1.png?fit=max&auto=format&n=zCBrVE9ZClJmxGFR&q=85&s=367f0d32ac8958e333d37fc4ad723ba2" alt="1" width="975" height="318" data-path="images/1.png" />
</Frame>

**b. 在文本框中用自然语言描述需求提示词** **需求阐述tips：**

<Note>
  提示词（Prompt）的质量直接决定了代码的质量和可用性，为了让 AI 更好地理解你的需求并生成高质量代码，建议遵循 “角色设定 + 背景上下文 + 核心功能 + 技术约束 + 输出规范” 的结构化描述方法。

  * ❌ 差：做一个减脂规划助手。
  * ✅ 好：请帮我生成一个减脂期间每日每餐的餐普规划助手，支持用户输入身高、体重、年龄、性别后生成一份详细的减脂规划。
  * ❌ 差：做一个计算出用户每日热量的功能。
  * ✅ 好：首先计算出用户每天最低需要多少热量，减脂期间推荐摄入多少热量，其次自动规划每日餐食的热量分配、荤素搭配、菜的热量计算，最后自动计算每日的热量缺口有多少，预计减重多少斤。
  * ❌ 差：界面风格要好看的。
  * ✅ 好：界面风格应简洁现代），主色调为深蓝色，按钮要有圆角和轻微的悬停阴影效果。移动端必须完全适配。
</Note>

**示例：**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/xS8x3RRoLzA3UT5R/images/%E6%8F%90%E7%A4%BA%E8%AF%8D%E7%A4%BA%E4%BE%8B.png?fit=max&auto=format&n=xS8x3RRoLzA3UT5R&q=85&s=119405a0cadf229e5fbc5640cb50fc4d" alt="提示词示例" width="975" height="338" data-path="images/提示词示例.png" />
</Frame>

**c.  选择模型**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/xS8x3RRoLzA3UT5R/images/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B.png?fit=max&auto=format&n=xS8x3RRoLzA3UT5R&q=85&s=36a33a69ad4c66197def4087af080cf6" alt="选择模型" width="964" height="617" data-path="images/选择模型.png" />
</Frame>

<Note>
  不同模型优点与差异请查阅《支持模型介绍》
</Note>

**d.  点击回车键或者右方箭头，开始开发项目。**

秒悟会根据您输入的提示词来开始设计应用，并自动为项目设置名称。

2. **（可选）重新多次澄清描述你的需求。** AI 收到你的提示词之后，如果判断提示词不明确、缺失关键信息，不足以支撑 AI 生成合适的 PRD 和产品原型，则会向你发送提示，请求补充缺失的关键信息。

### 步骤二：AI 编程开发应用

收到你的需求之后，将立即启动需求分析，并规划开发流程和步骤，逐步生成应用的前后端代码。代码生成完毕后，自动构建并启动服务，以提供一个可视化的界面供你预览。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/31bca51e3a63489148d7a3e4d57b178e.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=0a021850bcd5dcc9a592c6020c94d8de" alt="31bca51e3a63489148d7a3e4d57b178e" width="2256" height="1264" data-path="images/31bca51e3a63489148d7a3e4d57b178e.png" />
</Frame>

**应用开发配置**

**a.  一键链接数据库**

* 数据库的使用场景：应用中的数据需要长久记录保存、反复使用时需要使用数据库。
* 在聊天对话框输入：“**开启数据库，并且把前端与数据库链接**”，秒悟开始自动创建数据库链接

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/bhGThuxv_B49HP4S/images/image-101.png?fit=max&auto=format&n=bhGThuxv_B49HP4S&q=85&s=cd6fc465054dbef8bd81d77fd2fdc4ff" alt="Image" width="726" height="223" data-path="images/image-101.png" />
</Frame>

**b.  基础信息修改**

* 点击 **左上方标题** 可对项目的基础信息进行修改
* 应用标题：设置应用的显示名称，便于识别和管理。
  <Frame>
    <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/8bc53391b3da86b26fd20f4f1e36a086.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=3088ca68db0188aefeedca5ed86b73fb" alt="8bc53391b3da86b26fd20f4f1e36a086" width="2256" height="1264" data-path="images/8bc53391b3da86b26fd20f4f1e36a086.png" />
  </Frame>

**c.（可选）支持上传附件（图片/视频/文件）**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/03fbd2aecc2df2fcd2b8901d672be4dd.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=9711ac17013dd13009bc71c7e83f745b" alt="03fbd2aecc2df2fcd2b8901d672be4dd" width="2256" height="1264" data-path="images/03fbd2aecc2df2fcd2b8901d672be4dd.png" />
</Frame>

**d. （可选）支持配置技能**

**d1.  左下方点击技能 可以添加AI服务或大模型**

<Note>
  （AI服务：具备专业垂直能力的AI技能，参考用户文档中的《技能创建和使用》）
</Note>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/kWNB-EM8zYjDTeKZ/images/image-179.png?fit=max&auto=format&n=kWNB-EM8zYjDTeKZ&q=85&s=d83bb1039f43053f49b80f9348737dae" alt="Image" width="952" height="371" data-path="images/image-179.png" />
</Frame>

**d2.  可选择添加已有的AI技能或发现更多技能**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/b11258a5f9e4d744c363b0f69f28c80a.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=8f386f3afa44630a12ed348745d6bf71" alt="B11258a5f9e4d744c363b0f69f28c80a" width="2256" height="1264" data-path="images/b11258a5f9e4d744c363b0f69f28c80a.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/7eca17d3ce0c7a9fa558c8d6000c1f36.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=7878e7c15953fee6685084fb36b4bc6e" alt="7eca17d3ce0c7a9fa558c8d6000c1f36" width="2256" height="1264" data-path="images/7eca17d3ce0c7a9fa558c8d6000c1f36.png" />
</Frame>

### 步骤三：预览与测试

1. **点击 预览 可进行应用开发预览和效果测试** 。初步生成后端代码后会自动生成测试用例并完成一轮单元测试。测试通过后会可进行应用预览，你可以在右侧预览页面查看后端功能的实际运行效果。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/e38514437c6ec30d1ac3a9c83ab5edfe.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=e235f7770f75e318fd99137ba986401f" alt="E38514437c6ec30d1ac3a9c83ab5edfe" width="2256" height="1264" data-path="images/e38514437c6ec30d1ac3a9c83ab5edfe.png" />
   </Frame>
2. **调整需求** （可选）如果之前某次对话中你输入的描述有误或不准确，导致生成的应用无法满足你的需求，在左下方对话框可以在当前版本的基础下进行调整需求。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/3907d64d2c0fe0224497444c8e7fdeba.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=779dcbe8c02e53798916441e1ab30851" alt="3907d64d2c0fe0224497444c8e7fdeba" width="2256" height="1264" data-path="images/3907d64d2c0fe0224497444c8e7fdeba.png" />
   </Frame>
3. **版本回滚** （可选）如果某次需求调整的开发效果不及预期，可进行版本回滚，点击左侧栏目中的 **版本历史-点击需要恢复的版本**。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/d646ef64fb223c139dff18b8bbde28f8.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=dc9480a95f1cae5395422899186aebb2" alt="D646ef64fb223c139dff18b8bbde28f8" width="2256" height="1264" data-path="images/d646ef64fb223c139dff18b8bbde28f8.png" />
   </Frame>
4. **版本对比** （可选）点击 **代码-对比**，在左侧版本栏选择需要对比的版本，点击 查看改动，可进行对比多个版本之间的代码差异。
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/664b10cef1ca3fff2cf2e16ad99323e6.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=1dbe98878b12be2db31ec8c089b95680" alt="664b10cef1ca3fff2cf2e16ad99323e6" width="2256" height="1264" data-path="images/664b10cef1ca3fff2cf2e16ad99323e6.png" />
   </Frame>

### 步骤四：应用发布

右上角点击 **发布-立即发布**，发布成功后会生成网址链接，可通过链接直接访问

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/gtdh1P8HyRzTFXYK/images/78f75ba1b25a9e73e325a5722c9e19bd.png?fit=max&auto=format&n=gtdh1P8HyRzTFXYK&q=85&s=c97b823b0f7c5373ec7bf9577e31a594" alt="78f75ba1b25a9e73e325a5722c9e19bd" width="2256" height="1264" data-path="images/78f75ba1b25a9e73e325a5722c9e19bd.png" />
</Frame>

<Note>
  支持自定义域名（付费解锁）：①自定义Meoo三级子域名 。②自定义完全独立域名服务。

  <Frame>
    <img src="https://mintcdn.com/alibaba-b47c397f/2ChIPEOu--SY0Txr/images/1776084302187_0cec4112a3e84a1883265a7fb9b7cc7a.png?fit=max&auto=format&n=2ChIPEOu--SY0Txr&q=85&s=77b400db919b12c3968a8ddfb041f4b6" alt="1776084302187 0cec4112a3e84a1883265a7fb9b7cc7a" width="1340" height="620" data-path="images/1776084302187_0cec4112a3e84a1883265a7fb9b7cc7a.png" />
  </Frame>
</Note>
