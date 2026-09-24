# 灵骏裸金属实例开通及退订方法（钉钉文档）

> **来源**：内部钉钉文档 alidocs（个人空间）
> **文档标题**：灵骏裸金属实例开通及退订方法
> **原始分享链接**：https://alidocs.dingtalk.com/document/preview?cid=2899384242:6044579494&type=d&docKey=3BMqYybD9pAemqwZ&dentryKey=6mW9x31EQi2VzK0Y
> **规范链接**：https://alidocs.dingtalk.com/i/nodes/qnYMoO1rWxrkmoj2IboYZA16J47Z3je9
> **nodeId**：qnYMoO1rWxrkmoj2IboYZA16J47Z3je9 ｜ **workspaceId**：nb9XJNnNrd5BDXyA ｜ **extension**：adoc ｜ **contentType**：ALIDOC
> **createTime**：2025-09-02 10:26:30 CST（1756779990000）｜ **updateTime**：2026-07-22 13:10:50 CST（1784697050000）
> **SHA256（正文，指 `---` 分隔线之后还原出的 markdown 全文，UTF-8）**：1b272bbbdb2fda22911809ecef594aa09178f22b300e235eefbf1d20b9d6b70b
> **归档日期**：2026-08-11 ｜ **状态**：raw（不可变）
> **抓取方式**：`dws doc read --node "https://alidocs.dingtalk.com/i/nodes/qnYMoO1rWxrkmoj2IboYZA16J47Z3je9" --format markdown`，取返回 JSON 的 `.markdown` 字段，将 `\n` 还原为换行、`\"` 还原为引号后原样落盘，未删改任何字符（含图片链接、红字 `<span style="color: #FE0300;">` 标记、控制字符）
> **控制字符说明**：原文正文含 4 处 `U+0001`（SOH）控制字符，位于「确认配置 ␁，注意 ARMS…」「提供退订的实例ID ␁」「进入退订链接 ␁」「点击退订 ␁ 退订完成」，已按原始不可见字节 `0x01` 原样写入本文件，未做替换或删除。
> **图片说明**：正文共 42 张图片，托管于 2 个 OSS 域名——`alidocs2.oss-cn-zhangjiakou.aliyuncs.com`（36 张，全部带 `Expires=1786415766` + `OSSAccessKeyId` + `Signature` 签名参数，签名于 2026-08-11 10:36:06 CST 过期，归档后链接必然失效）与 `alidocs.oss-cn-zhangjiakou.aliyuncs.com`（6 张，无签名参数）。
>
> 🔴 **敏感级别：内部（Alibaba Internal）— 严禁对外**
> 本文件含：①内部控制台操作路径（`lingjun.console.aliyun.com/cn-wulanchabu/edp-bms/host-example` 等）；②灵骏 PDSA / 存储 PDSA 加白与报备流程（机型白名单、CPFS 报备加白）；③研发 uid / 内部账号路径（图片 URL 中的 `225668561102`、`7786471497`）；④内部集群编号（`集群编号C1`）；⑤内部 OSS AccessKeyId 前缀与签名串。
> **对客使用前必须脱敏**：不得出现 PDSA 加白流程、内部集群编号、内部 uid、带签名的内部图片链接与 OSS AccessKeyId。

---

# **资源开通与灵骏集群准备** 

## **准备工作**

在控制台的搜索框里搜索“智能计算灵骏控制台”，选择搜索结果中的“智能计算灵骏”，进入灵骏控制台。

或者直接点击链接“[https://lingjun.console.aliyun.com/?spm=a2c4g.11186623.0.0.218b6d22tIzDfl](https://lingjun.console.aliyun.com/?spm=a2c4g.11186623.0.0.218b6d22tIzDfl)”进入灵骏控制台。

国际站 UID 请点击[https://lingjun.console.aliyun.com/?spm=a2c63.p38356.0.0.14595ab2cvg33i](https://lingjun.console.aliyun.com/?spm=a2c63.p38356.0.0.14595ab2cvg33i)进入控制台

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/eLbnj8mME12ROaNY/img/73cc2283-f8c7-4851-8d1e-b618b25991c4.png "")

进入灵骏控制台后，注意确认选择可用区例如“华北6（乌兰察布）”区域。

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/eLbnj8mME12ROaNY/img/4774c00b-c306-4682-8a0a-3ed6dac13afd.png "")

## **购买节点(以HXX 节点为例)**

访问**灵骏控制台**[https://lingjun.console.aliyun.com/cn-wulanchabu/edp-bms/host-example](https://lingjun.console.aliyun.com/cn-wulanchabu/edp-bms/host-example)，选择左边栏的“**节点管理**”， 然后点击“购买新节点”，选择**集群编号C1**, 购买**H 卡机型**（需根据实际配额结果开白名单，咨询灵骏PDSA），然后选择对应的节点数量，然后点击提交就可以。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3M0OzB28d3vgOzeE/img/ebd1f5a3-ed86-4d0f-81db-7a111067d372.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=TrSvHJBoX6caDnoz%2BSpMiecAXgQ%3D "")



购买成功后的就可以在节点管理列表看到刚刚已经购买的节点（返回节点管理列表查看）

![](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/eLbnj8mME12ROaNY/img/43205445-76fe-4fb1-ab1a-c1c9953c719f.png "")

## **单租裸金属版的集群准备**

节点购买成功后，可通过“**创建PAI灵骏集群（包括PAI、ACK、CPFS等）**”的方式自助搭建集群。

在灵骏控制台中，访问左侧**集群管理**，点击“**创建集群**”，选择“**基础灵骏集群服务（裸金属形态）**”。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/cbabffd4-71e8-44af-af88-43cb7ede56e9.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=%2BAJQjQKSg9WN3eo2c6BNNdlhoXc%3D "")



### **第一步 创建 0 节点集群和分组**

填写基本的集群和分组信息，根据实际情况填写集群名称，集群编号选择**C1(按照实际选择)**，填写**登陆密码**（后续SSH登录物理机的 root 密码）。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3M0OzB28d3vgOzeE/img/b46ceb30-1bae-437a-881d-8daece3b1743.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=7HI0k6z4Gf6bsqn4a7mC28%2FR9UY%3D "")



点击**创建分组**，分组名称可以按实际需求填写，选择对应的默认机型机型（需根据实际配额结果，咨询灵骏PDSA。如果看不到对应的机型，请反馈灵骏PDSA，有可能是缺少了账号加白流程。

接下来，选择对应机器相应的镜像，指定节点名前缀；如是云盘实例，系统盘默认最低 180G，：

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/b8beaabc-3e43-4885-bea8-72b291cd389c.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=JubefCa9TDKLcNCekMEREVrM9ck%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/4f9c2c49-6b07-4e4d-8764-99db3f2eb75b.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=jWXWwNfVXYYslZw1qElq%2BJO7HY4%3D "")



如是本地盘实例，则不需要选定云盘大小，系统装机时间会慢一些（30 分钟以上）

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/7da80c68-8ce4-49d0-a089-c4b658e66151.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=IicNpBiZ%2B%2B3FnSOSkcLZ4PG%2FZmY%3D "")

此处可点击上面的“**请选择节点实例**”，选择刚刚购买的节点，点击确定，保存并进入下一步，即可创建带节点集群，本次介绍为 0 节点集群，可以不选择，等待创建之后再进行节点扩容。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3M0OzB28d3vgOzeE/img/eaa7b15c-1b70-4f5e-9c25-1d379bffad37.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=DLZqjlUa9D%2FM%2BO5WOM7tlQ%2FTZJo%3D "")



### **第二步，实例集群网络配置**

#### 选择要创建的集群所属的VPC/VSwitch和安全组信息，然后点击保存进入下一步。

如果POC测试场景，建议：
- 新建一个独立的VPC，这一步的vSwitch是灵骏物理机vsw：GPU服务器物理网络占用的交换机，控制面网络，一台机器占用一个IP。
- 安全组可以按照默认方式创建一个。

![](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/eLbnj8mME12ROaNY/img/f6d579f5-9091-42da-aee8-ab7c4c36dfd3.png "")



选择是否需要挂载CPFS，通常单纯的推理场景无需高性能分布式文件存储，如需购买 CPS 请联系存储 PDSA 进行报备加白；购买链接会自动跳转到下单界面，购买之后可手动输入挂载路径。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/2e968c0c-c458-47c4-98f5-c5b77d911d48.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=1EEYa44exbWiK72jkrnbj51dcKE%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/4b083ff3-5bfe-4a84-86fd-b6f648e4d5be.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=E6rSUoqs59whnVNdmWolKDYW1Vg%3D "")

如无需 CPFS，可选择跳过

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/2797c46e-5e7d-432d-9d05-f5e478fc0524.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=wDWfkjhegh9E2q2C1SnHarFdOAM%3D "")

确认配置 ，注意 ARMS 服务要确认已经开通了Prometheus 服务才能通过。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/d9fa29e0-a16d-4212-86b7-cdb2176f5216.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=s3CNXe8Gqb3N5yQv7sPxfu3nbyU%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/6aa68aaa-ef6e-4c8f-b3df-7786b7bb38cc.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=Qwlt%2Fbdi%2Bpgc79fVmv2DAf7pimc%3D "")

提交配置后在集群管理可以查看集群创建进度

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/f863a001-f526-45c4-acb5-363ad884fe88.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=513QisjIKWE5OTZIE68TFIkpowM%3D "")

### **第三步 扩容集群节点**

集群创建好之后可以进行节点扩容，将未使用节点扩容进集群进行使用。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/a9e5fd13-f0a9-4fbf-8f09-c18a2440dba1.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=qnhm0vcyEBV6Fdw6yNODaTvp9D0%3D "")

选择加入已有节点之后确认配置

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/61f47959-ed0f-40e3-a936-8baee405cf25.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=zgA73xip5C2X%2BZTQiey9eIfUeHI%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/88228a87-495a-4bd5-8abf-856e4d38cdd5.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=IM7LuDexnC%2BmAR0zwq4BAehc9RA%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/3eaec7d7-90e5-4602-8f7f-21378e92139d.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=zSV4gGhPeyGfPXKYdHjrUs7o640%3D "")



扩容中节点在节点管理中可查看状态为“扩容中”，在任务中心可查看具体扩容进度。

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/19f4351e-48c8-4d37-b71a-2ba940deb97c.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=WVd12cxVVl3My6wXptJ8cHXPtb8%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/1333f255-9dab-4e70-8189-5d7772e55d62.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=7OoZnfshrVRgDoJfzdetLQRGbFw%3D "")



**正常节点状态如下：其中第一个私网 IP 为入 VPC 的 ENI 私网 IP，其余 IP 为自动分配的高网 IP，用于 RDMA 互联。**

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/0654ce3a-8b81-44b1-b511-0e016342b19c.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=HvvRsWIRuJf0GRNjPuFhu3DH8jY%3D "")



### **第四步 节点使用**

####  **可使用灵骏控制台登录裸金属节点，或者使用同 VPC 内的 ECS 节点作为跳板机进行登录。**

灵骏控制台节点登录方法分为带内或带外，示例如下：

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/bccef8aa-e75f-4dca-89a1-cb0770df9b14.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=aGVefBRGpzZHIIX%2BOgrPFnERhF0%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/dad72412-cf4e-4a25-a4d1-3505b7acf21b.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=9TVYI3IaiXnxQhNBELbHhGcarUE%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/1fac1be6-d2ce-4367-9e3d-cbd3b14628b3.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=AcFroBO8x%2BQKwIzuujnkLreBRKY%3D "")



备注：<span style="color: #FE0300;">实例本地NVME硬盘如果格式化挂载使用，在故障后会默认进行备机替换。原云盘OS 会无法识别备机的本地 NVME 硬盘uuid,因此挂载使用后需要加 nofail 参数，防止替换流程失败。</span>

<span style="color: #FE0300;">示例：</span>![](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/a/225668561102/7786471497/0507afc3-0c35-4525-bf98-e6f20b0fe254.png "")

<span style="color: #FE0300;">同 ECS 实例规则一致</span>

![](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/a/225668561102/7786471497/b3954f5e-5de3-4bac-b1f8-b9557dba05ee.png "")



####  **配置公网 NET 网关进行互联网访问，NET 网关可配置 SNAT 或者 DNAT 用于出入。NET 网关需绑定弹性公网 IP 进行互联网访问。**

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/155b0baa-8f46-45b9-a233-1d6cff9e3be0.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=yhLSTR%2BuxvbdAXzKlgj2%2BbSopGs%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/8248cc45-fc74-485b-9925-d766d918b53e.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=qpN1xzrrTOO485KQ5wU6UpcIr%2BI%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/6432541b-3c5d-40b5-95cf-f24a5b0c0b86.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=6E5vB%2B45%2Fo%2FIJLUO7tG187fnSks%3D "")

**注意：配置了 DNAT 之后，安全组要将 22 端口放行，VPC 之外的节点才可通过弹性公网 IP 访问 GPU 节点**



### **第五步 节点退订**

在集群管理中针对需要退订的节点进行缩容，缩容节点后，节点状态变成未使用，即可进行提工单退订

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/d06bc7d4-a2ff-4fd4-b69d-edd7adb53524.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=t3cSDAlDZew2Sm96KnQ0MiFJK3w%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/974a3e48-1790-42e8-a38d-443df94b6381.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=QI4qImGbaDaIUncFmPtQdUKoeTQ%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/cc07f78d-9f78-44af-85a5-dfb3d4ddfd94.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=iZlGgT%2FsBB7fjOCOts9r2vkoQf8%3D "")

缩容完成后，节点变为未使用状态



![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/1d7d41e8-da2d-4607-9116-c90e8e8cc775.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=G7eh7wDVBuAYMbm2RsTgBeincXY%3D "")



![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/061904d5-4f47-4d83-92cd-e33be4127bd6.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=3wai4ouYEwVUX7EwFfz69hW6LQQ%3D "")

![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/7bb88ebf-2183-46b7-bc2a-0369ec11d675.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=ytvxgZSyf%2FX5jrZ1JhHJ0mkSGZA%3D "")

产品分类里面选择“智能计算灵骏”![image.png](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/1e0f8bf5-6b8e-4965-b556-9337cb2f3254.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=1PO35tjQaAL%2BcDrUOoyR%2BqnwoxE%3D "")

进入在线服务后根据售后工程师提示提供退订的实例ID  

![](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/7e2c43a6-9223-4527-becb-faaea148a52c.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=sXBEMpYwY5FrFUv372cV2yMovF0%3D "")根据提示确认节点状态以及订单信息，回复确认后，进入退订链接  

![](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/0e6bd273-8eb2-454b-9431-9f4d02d7de5a.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=4R%2FeserQJ3O%2Fzdn36EfcgO1LLsY%3D "")

![](https://alidocs2.oss-cn-zhangjiakou.aliyuncs.com/res/3BMqYybD9pAemqwZ/img/c9d54f83-dc91-4fb8-863a-0fce376bf652.png?Expires=1786415766&OSSAccessKeyId=LTAI5tKTjg4Kq1HCdBJ8qpSp&Signature=MsoVUlOWVlckbU3FlmegfGryhn0%3D "")

选择退订原因，点击退订  退订完成，待后台回收机器后即可关单




