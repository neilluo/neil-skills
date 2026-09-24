> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 微信小程序手动部署指引

> **说明**：由于微信平台分配给 Meoo 平台的微信小程序发布额度不足，目前暂时无法通过 Meoo 平台直接一键发布小程序。本指引为临时手动部署方案，请按以下步骤操作。我们也在联系平台侧尽快提升额度，提升后您将可以继续使用我们的自动部署能力。

## 第一步：下载产物

在秒悟平台完成开发后，点击发布弹窗的“下载产物”按钮，将小程序源码下载到本地并解压。

## 第二步：解除第三方授权（如需要）

> 如果该小程序曾授权给其他第三方平台，需要先解除授权，否则后续上传会冲突。

进入 [微信公众平台](https://mp.weixin.qq.com/)，登录后依次操作：

**管理 → 账号设置 → 第三方设置 → 解除所有第三方平台授权**

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-264.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=db019d595617869c90dd0e87528f36e6" alt="Image" width="1944" height="1106" data-path="images/image-264.png" />
</Frame>

如从未绑定过第三方平台，可跳过此步骤。

## 第三步：下载并安装微信开发者工具

前往官方下载页面获取最新版微信开发者工具：

[https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-265.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=f66f1e4f66bd885802a7d6b52b4d4583" alt="Image" width="1584" height="998" data-path="images/image-265.png" />
</Frame>

根据系统选择对应版本（macOS / Windows），安装完成后启动。

## 第四步：导入项目

1. 打开微信开发者工具，使用小程序管理员的微信扫码登录
2. 点击 **"+"（导入项目）**
3. 填写以下信息：
   * **目录**：选择第一步下载并解压的代码文件夹
   * **AppID**：填写小程序的 AppID（可在微信公众平台 → 管理 → 账号设置 → 基本设置 中查看）
   * **后端服务**：选择 **"不使用云服务"**
4. 点击 **"确定"** 完成导入

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-266.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=822c0e65c060d0a246d1504d17f529a0" alt="Image" width="1422" height="1400" data-path="images/image-266.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-267.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=715b1cd5c33194bf1fb43900015c6b25" alt="Image" width="1422" height="1400" data-path="images/image-267.png" />
</Frame>

## 第五步：上传体验版

1. 在开发者工具中确认项目可正常预览运行
2. 点击右上角 **"上传"** 按钮
3. 填写 **版本号**（如 `1.0.0`）和 **项目备注**
4. 点击上传，代码将提交到微信服务器

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-268.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=4e34a156cd5ba1308296ba8c054d5682" alt="Image" width="2160" height="1754" data-path="images/image-268.png" />
</Frame>

上传成功后，可在微信公众平台的版本管理中看到该版本。

## 第六步：提交审核

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **管理 → 版本管理**
3. 在 **"开发版本"** 区域找到刚才上传的版本
4. 点击 **"提交审核"**，按提示填写功能页面、类目等信息
5. 确认提交，等待微信官方审核（通常 1\~7 个工作日）

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/jJdMxHHcdyKSHDCo/images/image-269.png?fit=max&auto=format&n=jJdMxHHcdyKSHDCo&q=85&s=fea4e5c033ca1676191fb798ff699c72" alt="Image" width="2466" height="538" data-path="images/image-269.png" />
</Frame>

## 第七步：发布上线

审核通过后，回到 **版本管理** 页面：

1. 在审核通过的版本旁点击 **"发布"**
2. 确认后小程序即刻上线

## 恢复自动发布

待 Meoo 平台额度恢复后，即可重新按 [小程序搭建&部署](https://docs.meoo.com/wechat-miniprogram-desc) 文档给 Meoo 授权，之后在平台内一键发布，无需再手动操作。
