> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 自定义独立域名

秒悟支持使用自定义独立域名来访问你发布的应用，使得你发布的应用看起来更”专业“，易于分享传播。

# 为什么要用自定义域名？

自定义域名让你的应用看起来是「你的」，而不是「租来的」：

* **你的应用看起来更像「正版」**；用户打开的是你的品牌域名，而不是一串平台地址。就像开店用「yourbrand.com」比用「xxx.taobao.com」更像独立品牌一样。
* **链接更好记、更好分享**；你可以把 「[www.yourbrand.com」](http://www.yourbrand.com」) 印在名片、PPT、宣传页上，用户一眼就能记住。平台二级域名又长又难记，分享出去也不够体面。
* **你的用户更放心**；很多人对陌生的二级域名会有警惕心，担心是不是钓鱼网站。用自己的域名能降低这种不信任感，尤其适合面向客户、投资人或公众的正式场景。
* **更容易被搜索引擎找到**；百度、谷歌等搜索引擎更认可独立域名。如果你想让应用被更多人通过搜索发现，自定义域名比平台二级域名更有优势。
* **域名是你的资产，不受平台变动影响**；即使以后换了平台、调整了服务，只要域名还在你手里，用户的访问入口就不会变。流量和品牌积累不会白费。
* **搭配企业邮箱使用**；有了自己的域名，你就可以开通 [hello@yourbrand.com](mailto:hello@yourbrand.com)、[support@yourbrand.com](mailto:support@yourbrand.com) 这样的企业邮箱，从网站到邮箱统一品牌感。

# 配置自定义域名需要哪些步骤？

要让一个自定义域名正式对公网提供服务，在域名维度上需要完成的【规定动作】是基本一致的。需要以下几个步骤：

1. **购买注册域名**：在域名服务商处购买你需要的域名，例如阿里云、腾讯云等。阿里云作为国内最大的域名注册商，域名品种最全、一站式服务能力强大。推荐在阿里云购买注册域名：[https://wanwang.aliyun.com/](https://wanwang.aliyun.com/)
2. **实名认证**:在你购买域名的域名服务商处进行实名认证。上传身份证或营业执照，通过工信部和注册局审核。域名信息模版实名认证：字段包括姓名（域名所有者）、身份证号、身份证人像页、邮箱、手机号。阿里云域名管理：[https://dc.console.aliyun.com/?#/domain-list/all](https://dc.console.aliyun.com/?#/domain-list/all)
3. **ICP备案**：如服务器在中国内地，必须在对应的云服务厂商处提交备案。备案号通常挂靠在服务器IP上，且必须在接入服务商（云厂商）处进行备案或新增接入。秒悟用户需要在阿里云上进行备案，备案地址：[https://beian.aliyun.com/](https://beian.aliyun.com/)
4. **DNS解析配置**：为了使自定义独立域名能够跳转到用户指定的秒悟应用，需要在域名服务商处配置对应域名的DNS解析。在阿里云购买的域名可以使用阿里云的云解析服务：[https://dnsnext.console.aliyun.com/authoritative](https://dnsnext.console.aliyun.com/authoritative)
   * 配置DNS解析后，验证域名解析是否生效，参考【解析生效测试方法】[https://help.aliyun.com/zh/dns/pubz-parsing-effectiveness-test-methods](https://help.aliyun.com/zh/dns/pubz-parsing-effectiveness-test-methods)
5. **配置SSL证书**：为了保证应用数据传输的安全，需要为自定义独立域名配置SSL证书来加密访问的流量。秒悟中自定义域名可提供免费证书、免费续期。用户也可以选择阿里云的云盾证书：[https://yundun.console.aliyun.com/?p=cas](https://yundun.console.aliyun.com/?p=cas)

# 操作步骤

上述配置自定义域名的步骤中，步骤1、2、3都需要用户自行在域名服务商处进行操作；完成后才能在秒悟上进行操作，以web版为例：

## 一、填写域名

在秒悟的应用详情页的导航栏点击【域名配置】，点击【配置自定义域名】卡片的【配置域名】。

如果用户没有域名可以点击【购买新域名】跳转到阿里云万网完成上述步骤1、2、3。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-256.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=1d55b6dd050add38d26c52f8c14c43f0" alt="Image" width="3106" height="728" data-path="images/image-256.png" />
</Frame>

填写已经完成购买、实名认证和ICP备案步骤的自定义域名并提交。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-254.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=68fbe85d8239a3d9b76540c2bda0f08e" alt="Image" title="Image" style={{ width:"66%" }} width="3112" height="744" data-path="images/image-254.png" />
</Frame>

## 二、配置DNS解析

提交自定义域名后，根据弹窗提示在域名服务商处完成域名DNS解析配置。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-257.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=42e6d1ee37355d46594fabfe893605ea" alt="Image" title="Image" style={{ width:"53%" }} width="1162" height="1956" data-path="images/image-257.png" />
</Frame>

以阿里云为例，在云DNS控制台[https://dnsnext.console.aliyun.com/authoritative](https://dnsnext.console.aliyun.com/authoritative)配置对应域名的TXT记录和CNAME记录。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-255.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=76f8c40eca51d0760481cb7fdfd0030f" alt="Image" width="3112" height="744" data-path="images/image-255.png" />
</Frame>

完成后点击【验证】，秒悟将检查DNS解析是否成功。

## 三、申请SSL证书

在【配置DNS解析】验证成功后，点击【申请证书】进行SSL证书配置。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-259.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=e1bf5b8268204df1bcb576422e52d0ec" alt="Image" title="Image" style={{ width:"55%" }} width="1166" height="1950" data-path="images/image-259.png" />
</Frame>

证书签发成功后点击【完成】。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-261.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=1bbcc168d81c3edb4f273f91d167f431" alt="Image" title="Image" style={{ width:"53%" }} width="1158" height="1962" data-path="images/image-261.png" />
</Frame>

访问自定义域名即可访问发布的应用

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/hsaIhLKEllLl3w13/images/image-262.png?fit=max&auto=format&n=hsaIhLKEllLl3w13&q=85&s=afdc4b34f79e7b3eef1c804f7863fa5d" alt="Image" title="Image" style={{ width:"55%" }} width="1984" height="1912" data-path="images/image-262.png" />
</Frame>

# **常见问题**

#### Meoo自定义独立域名如何配置？

1. 【准备域名】请确保域名已完成【注册】与【备案】。
   * 【注册域名】阿里云购买注册域名：[https://wanwang.aliyun.com/](https://wanwang.aliyun.com/)
   * 域名备案】Meoo面向国内提供服务，云资源在阿里云，按照监管要求需在阿里云完成备案。可购买阿里云ECS服务器获取备案码。阿里云备案地址：[https://beian.aliyun.com/](https://beian.aliyun.com/)
2. **如何查询域名是否已有备案？** [https://boce.aliyun.com/home](https://boce.aliyun.com/home)

* 如下图：无备案

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/HAk70_f3b1y0Yxkk/images/image-250.png?fit=max&auto=format&n=HAk70_f3b1y0Yxkk&q=85&s=785e63d6b83ab6901f78c3d4cd2b9643" alt="Image" width="1169" height="531" data-path="images/image-250.png" />
</Frame>

* 如下图，有备案

3. 【检查解析】请验证 DNS 解析记录是否可在全网生效，以云DNS解析为例。
   * 【添加解析记录】[https://help.aliyun.com/zh/dns/pubz-add-parsing-record](https://help.aliyun.com/zh/dns/pubz-add-parsing-record)
   * 【解析生效测试方法】[https://help.aliyun.com/zh/dns/pubz-parsing-effectiveness-test-methods](https://help.aliyun.com/zh/dns/pubz-parsing-effectiveness-test-methods)
   * 【解析不生效问题快速排查】[https://help.aliyun.com/zh/dns/pubz-quick-troubleshooting-of-problems-not-effective](https://help.aliyun.com/zh/dns/pubz-quick-troubleshooting-of-problems-not-effective)
4. **如何添加域名解析？** 按页面提示添加cname记录和TXT记录 若域名DNS是阿里云的，在阿里云做解析；若域名DNS不是阿里云的，找域名注册商添加解析。 阿里云域名如何添加解析：[https://help.aliyun.com/zh/dns/pubz-add-parsing-record#a91608fbcbn8r](https://help.aliyun.com/zh/dns/pubz-add-parsing-record#a91608fbcbn8r)
5. 在确保【域名合规】和【解析生效】后，进入Meoo应用构建页 - 点击域名配置 - 添加自定义独立域名 - 配置域名解析，添加【CNAME】记录 - 生成免费数字证书。

#### 提示SSL证书申请失败怎么办?

SSL 证书申请失败可能由多种原因导致，建议按以下步骤排查：

1. 检查域名的 CNAME、TXT 等 DNS 记录是否配置正确，可通过阿里云 DNS 检测工具（[https://boce.aliyun.com/detect/dns](https://boce.aliyun.com/detect/dns) ）进行验证。
2. 若 DNS 记录确认无误但仍申请失败，可联系秒悟技术支持。
