> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 团队账号创建与登录

## 秒悟团队账号介绍

秒悟团队版与阿里云账号体系深度集成。**企业管理员**使用<u>阿里云主账号</u>登录并开通团队，**团队成员**使用[RAM 子账号](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.15.27b92f3dffi5Lw\&scm=20140722.S_help@@%E6%96%87%E6%A1%A3@@122148._.ID_help@@%E6%96%87%E6%A1%A3@@122148-RL_ram-LOC_2024SPAllResult-OR_ser-PAR1_0bc3b4ae17829942924606287e57ba-V_4-PAR3_o-RE_new5-P0_2-P1_0)登录即可加入团队工作空间。

* 主账号登录：自动创建团队、初始化工作空间、赋予 Owner 角色
* RAM 子账号登录：系统自动识别所属主账号和团队，校验权限后进入工作空间

<Accordion title="什么是 RAM 子账号？">
  RAM用户是RAM的一种实体身份类型，有确定的身份ID和身份凭证，它通常与某个确定的人或应用程序一一对应。RAM用户具备以下特点：

  * RAM用户由阿里云账号（主账号）或具有管理员权限的其他RAM用户、RAM角色创建，创建成功后，归属于该阿里云账号，它不是独立的阿里云账号。
  * RAM用户不拥有资源，不能独立计量计费，由所属的阿里云账号统一付费。
  * RAM用户必须在获得授权后，才能登录控制台或使用API访问阿里云账号下的资源。
  * RAM用户拥有独立的登录密码或AccessKey。
  * 一个阿里云账号下可以创建多个RAM用户，对应企业内的员工、系统或应用程序。
</Accordion>

## 管理员账号注册登录

<Steps>
  <Step title="注册/登录管理员账号">
    进入 meoo.com 点击登录以后进入登录页，切换至“团队版”，选择您的身份；

    如您是第一次开通秒悟“团队版”，请选择“团队负责人”身份，下一步：

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-277.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=d12d29b5860546453114766e5db02e81" alt="Image" width="3840" height="1982" data-path="images/image-277.png" />
    </Frame>
  </Step>

  <Step title="登录已有阿里云账号">
    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-276.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=47edf1bbf8ca613e8b6e5bc21fd8fe9c" alt="Image" width="3840" height="1982" data-path="images/image-276.png" />
    </Frame>

    如您已有阿里云主账号，可输入手机号或账号密码直接登录，若从来没有注册过阿里云账号，也可以在当前页面直接输入手机号进行新账号注册。
  </Step>

  <Step title="选择一个账号登录">
    阿里云一个手机号可以创建多个主账号，选择一个账号登录即可；

    ⚠️注：若您名下有账号已经登录过秒悟“个人版”，则无法再注册登入秒悟“团队版”，需至aliyun.com 官网进行新的主账号创建再登录秒悟“团队版”。

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-278.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=e928054828a0220e59c810f96c4054f4" alt="Image" width="3840" height="1986" data-path="images/image-278.png" />
    </Frame>
  </Step>

  <Step title="团队版登录成功">
    “团队版”登录成功，将会看到如下页面，您可继续：

    * 初始化您的团队账号信息：logo、名称等
    * 去阿里云 RAM 控制台创建成员子账号

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-280.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=9a5467db11db35067e8aa054ab8a023f" alt="Image" width="3840" height="1978" data-path="images/image-280.png" />
    </Frame>
  </Step>

  <Step title="付费订阅后可正式享用团队版">
    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-281.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=d9941eadb27f6134159c7c6a60c3062a" alt="Image" width="3840" height="1978" data-path="images/image-281.png" />
    </Frame>

    团队版定价详细见下一章节：版本与定价，正式使用需先开通订阅。
  </Step>
</Steps>

## 创建成员子账号（RAM账号）

秒悟“团队版”成员账号为阿里云RAM账号体系，如您需邀请成员进入自己的秒悟团队，需先至[阿里云控制台](https://ram.console.aliyun.com/users)进行RAM成员账号创建，创建流程参考：

<Steps>
  <Step title="进入“身份管理-用户”导航栏，点击“创建用户”">
    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-282.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=70053ef1cf52f816ead4a77a6eaf2c48" alt="Image" width="3840" height="1980" data-path="images/image-282.png" />
    </Frame>
  </Step>

  <Step title="输入成员用户名称">
    1）输入成员用户名称

    2）开启“使用控制台访问”

    3）勾选MFA认证（建议）

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-284.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=c9b7a88c893e89cda02ccd4106d3a9c8" alt="Image" width="3840" height="1982" data-path="images/image-284.png" />
    </Frame>
  </Step>

  <Step title="创建成功，成员使用该账号即可登录">
    接下来将您创建的RAM账号名称+密码发给成员，进行登录即可；

    如有多个成员，则需逐个进行安全创建。

    注：该步骤不代表秒悟的席位生效，只代表RAM子账号创建成功，只有当您将团队链接发给成员，成员正式通过RAM账号登入秒悟并加入团队后，席位才会正式被使用。

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-285.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=9321c4d6eeeb8eb617d10e5f3d0ec680" alt="Image" width="3840" height="1982" data-path="images/image-285.png" />
    </Frame>
  </Step>
</Steps>

## 成员登录（RAM账号登录）

秒悟成员登录前，请确认已从您的团队管理员处获得 RAM账号名称+密码；

如没有RAM账号，需先找您的团队管理员从阿里云控制台获得。

成员登录流程：

<Steps>
  <Step title="进入秒悟登录页，选择“团队版”">
    选择“管理员/团队成员”进行下一步登录：

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/image-287.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=b613e1e353f52dd41ddb18d6b8b712c6" alt="Image" width="3840" height="1982" data-path="images/image-287.png" />
    </Frame>
  </Step>

  <Step title="进行成员RAM子账号登录">
    输入企业管理员给您的RAM子账号&密码，进行登录：

    <Frame>
      <img src="https://mintcdn.com/alibaba-b47c397f/fxtnXq7fv4fJiZp4/images/image-288.png?fit=max&auto=format&n=fxtnXq7fv4fJiZp4&q=85&s=c5b494bdaaa48c96441909e83485a847" alt="Image" width="3840" height="1834" data-path="images/image-288.png" />
    </Frame>
  </Step>

  <Step title="输入MFA安全验证码">
    若您从来没有绑定过MFA安全验证，可手机上下载“阿里云”APP或者“Authenticator”APP进行绑定并进行验证
  </Step>

  <Step title="验证通过，登入秒悟团队版即正式占用团队席位">
    正式登录秒悟团队版，可看到企业管理员给您分配的积分额度，即可开始正式创作！
  </Step>
</Steps>
