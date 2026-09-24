> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Meoo CLI 使用指南

meoo cli 是秒悟（Meoo）官方推出的命令行工具，让 Claude Code、Codex、Cursor、Qoder、Qoderwork等本地 agent 在帮你写完前端代码后，能直接接管「数据库、用户登录、文件存储、百炼模型服务、部署上线」的所有云端工作。

<Note>
  🔧 支持工具：具备Coding能力的本地 agent ，例如：Claude Code、Codex、Cursor、Qoder、Qoderwork、Cline 等主流 agent。

  🎯 适用场景：

  * 从 0-1 搭建项目，需要接入数据库，部署到线上，并生成分享链接
  * 本地已有的静态页面同步云端协作，控制对外可见范围
  * 本地已有项目迁移到线上，优先支持 Vite + React 和纯前端项目

  ✅ 适用人群：

  * 有全栈交付需求的泛开发者
  * vibe coding 爱好者，想把作品做成链接分享的创作者
  * 设计师、产品经理、运营，需要快速产出落地页、H5 长图、活动页并和团队协同打磨
</Note>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/7XuCh0qG1uNys9ur/images/cli%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97--%E4%BB%8B%E7%BB%8D.png?fit=max&auto=format&n=7XuCh0qG1uNys9ur&q=85&s=fdb45843ed40c543bf6b63bfceb82fac" alt="Cli操作指南 介绍" width="2752" height="1536" data-path="images/cli操作指南--介绍.png" />
</Frame>

## **步骤一：安装 meoo cli**

前置条件：

* 已安装 [Node.js 20 或更新版本](https://nodejs.org/en/download/)
* macOS 用户推荐通过 nvm 或 Homebrew 安装 Node.js
* Windows 用户还需安装 Git for Windows 和 zip 工具

**方式一：自动安装（推荐）**

打开任意本地 agent（codex/claude code/cursor/qoder/qoderwork等），直接在对话框发送这句话

```text theme={null}
读取 meoo.com/skill-setup.md 并按照说明安装秒悟技能
```

**方式二：手动安装**

打开终端，执行：

```text theme={null}
npm install -g @aliyun-meoo/cli
```

执行下面这行验证安装：

```text theme={null}
meoo --version
```

显示版本号即安装成功。

## 步骤二：登录授权

安装完成后，CLI 会自动打开浏览器，跳转到 [meoo.com](http://meoo.com) 的授权页面。首次授权，需要登录秒悟账号，之后只需在网页上确认设备名称并点击「授权登录」。授权成功后，浏览器会提示你回到终端——CLI 会自动获取凭证并保存。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/7XuCh0qG1uNys9ur/images/cli%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97-%E7%99%BB%E5%BD%95-1.png?fit=max&auto=format&n=7XuCh0qG1uNys9ur&q=85&s=802c8aeadf88b2bbd36fc9668afea5b5" alt="Cli操作指南 登录 1" width="2934" height="1666" data-path="images/cli操作指南-登录-1.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/loFgond61i7cR4p3/images/cli%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97-%E7%99%BB%E5%BD%952.png?fit=max&auto=format&n=loFgond61i7cR4p3&q=85&s=f7edc5a323dcf13fa33383896e7474a6" alt="Cli操作指南 登录2" width="2912" height="1666" data-path="images/cli操作指南-登录2.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/loFgond61i7cR4p3/images/cli%E7%99%BB%E5%BD%95%E6%8C%87%E5%8D%97-%E6%93%8D%E4%BD%9C3.png?fit=max&auto=format&n=loFgond61i7cR4p3&q=85&s=44ecb8f7f46dffae0e0816300721eb79" alt="Cli登录指南 操作3" width="2920" height="1668" data-path="images/cli登录指南-操作3.png" />
</Frame>

如未触发自动登录和授权，可尝试手动登录：

在终端执行以下命令，会跳转到浏览器登录授权界面

```text theme={null}
meoo login
```

## 步骤三：使用本地 agent 创建项目

打开日常使用的 agent （以codex桌面端为例）, 在对话框输入：

```text theme={null}
帮我用meoo做一个好看的个人主页，数据接入云服务数据库，然后一键发布到线上
```

<video src="https://mintcdn.com/alibaba-b47c397f/7XuCh0qG1uNys9ur/videos/cli%E6%93%8D%E4%BD%9C%E6%8C%87%E5%8D%97-%E5%8E%8B%E7%BC%A9%E7%89%88.mp4?fit=max&auto=format&n=7XuCh0qG1uNys9ur&q=85&s=c96ff54eb1e3f1850682f701e7c7cbae" controls data-path="videos/cli操作指南-压缩版.mp4" />

接下来 agent 会自动完成所有事情——它会写个人主页，调用 meoo cli 在云端创建数据库、补齐缺失的后端代码，最后部署到线上，生成一个可以分享的链接。整个过程你只需要看着终端输出，等它跑完即可。

## 步骤四：本地预览 + 一键上线

AI 干完活后，你可以让它帮你先在本地起一个预览：

```text theme={null}
起个本地预览看看效果
```

浏览器自动打开 localhost:3015，你可以在本地完整测试一遍——注册账号、提交表单、查看数据库等等。确认没问题后，告诉它：

```text theme={null}
部署上线
```

AI 会自动执行 meoo deploy，构建打包并发布到 CDN，最终在终端输出一个可直接分享的访问链接。把这个链接发给朋友、发到社交平台，他们就能用上你做的应用了。

如果想使用扩充数据库容量，调用大模型服务（ai问答，文生图，识图等能力），自定义域名，自定义网页发布范围（全网可见/指定人员可见/尽自己可见）等功能，建议把代码同步到meoo云端，可以继续跟本地agent （以codex为例）对话：

```text theme={null}
帮我把代码同步到meoo云端         
```

就可以在 meoo 官网看到刚才构建的应用，可以直接在秒悟里进行二次修改。

## 常见问题

**Q1：我想试用，怎么开始？**

打开你常用的 AI 编程工具（CodeX、Claude Code、Cursor、Qoder、QoderWork 都行），把下面这条命令丢给 AI：

> 读取 meoo.com/skill-setup.md 并按照说明安装秒悟技能

AI 会自己读完说明、装好工具、引导你完成登录。装完直接告诉它"帮我把这个项目部署上线"就能开始用。

***

**Q2：注册有什么福利吗？**

新注册账号会送 10000 积分；之后每天登录一次 [meoo.com](http://meoo.com) 还能再领 2000 积分；另外送 1 个免费云服务额度（用来开数据库的）。如果你只是想发布一个静态页面（不用注册登录、不用存数据），不用动这个云服务额度，注册完就能直接发。

***

**Q3：支持哪些 AI 编程工具？**

CodeX、Claude Code、Cursor、Qoder、QoderWork等主流的 agent 工具都能接入使用，按上面 Q1 的命令安装一遍就行。

***

**Q4：开发的时候能在本地先看效果吗？**

能。AI 帮你启动后会跑在本地的 localhost，浏览器打开就是预览页。预览和发布是两件独立的事，你可以先反复在本地改、本地看，没问题了再让 AI 部署上线。

***

**Q5：我已经在本地改了代码，但 meoo 网页后台也能编辑，会冲突吗？**

会。你在本地开发期间，别去网页后台点"发布"——网页后台默认是空项目，你一发布就会把本地辛苦写好的代码覆盖掉，最后页面变白屏。如果确实要在网页后台改，记得先让 AI 帮你把代码同步到云端，再去网页操作。

***

**Q6：我让 AI 执行开通云服务，但马上去连数据库就报"未开通"？**

正常的，云服务开通大概要等 3 分钟。命令返回成功只代表"开通申请发出去了"，数据库实例还需要点时间才能真正起来。等 2-3 分钟再让 AI 重试一次就好。

***

**Q7：我以前写好的项目能搬到 meoo 上来吗？**

meoo-cli 优先支持 Vite + React 和纯前端项目，创建项目时，建议提前告知大模型 meoo cli的技术栈支持范围。迁移之前一定先把代码备份一份——迁移过程中 AI 会帮你做不少改动，万一出问题至少有原始版本能回滚。

***

**Q8：纯静态页面（个人主页、H5 长图）也要开通云服务吗？**

不用。静态页面注册完就能直接发布，不会消耗你的免费云服务额度。
