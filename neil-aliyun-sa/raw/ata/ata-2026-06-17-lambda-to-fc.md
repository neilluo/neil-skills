# Serverless 跨云迁移总结：从 AWS Lambda 到阿里云 FC

> **来源**：ATA | **作者**：潍尼 | **发布日期**：2026-05-21
> **URL**：https://ata.atatech.org/articles/11020645626?utm_source=open&utm_medium=hsf&utm_campaign=_OPEN_AONE
> **SHA256**：e02fd6cb583e2b88bf2b873655dc95bd3f386b27ca64f134d7fe1d8d8d6c58f2
> **归档日期**：2026-06-28 | **状态**：raw（不可变）

---

本文复盘了将 800+ AWS Lambda 迁移至 600+ 阿里云 FC 的全过程。内容涵盖从架构映射、CI/CD 重构、冷启动调优到数据零丢失割接的工程实践，希望能为需要做 Serverless 跨云迁移的同学提供参考。 项目背景 某客户的QOP 开放平台是客户自研的B2B企业办公物资数字化采购平台，通过API对接为企业和政府机构提供商品、订单、库存、物流等全链路采购服务，为 100+ 企业客户提供定制化数据集成服务。 在24年4月的时候，AWS意外停止了客户的Lambda服务导致业务受损，因此客户决定从AWS侧迁移到阿里云上。本次迁移的目标如下： 业务无感知: 客户 API 调用路径与响应格式保持不变 数据零丢失: 迁移期间数据一致性 100% 保障 性能不降级: 延迟、QPS、错误率等核心指标不劣化 成本可优化: 充分利用阿里云产品特性降低 TCO 2. 调研 明确迁移目标后，首先对源端与目标端的架构差异进行映射。 2.1 AWS 源端架构 源端架构高度依赖 AWS Serverless 生态（Lambda 事件驱动 + API Gateway 路由 + SAM 声明式部署）。迁云需完成事件模型、网络拓扑及部署流水线的整体切换。 AWS侧的组件说明： 计算层: 800+ Lambda 函数 (Java 调度器 + Python 转换层) 网关层: 12+ EC2 实例 数据层: RDS MySQL (多实例隔离) + ElastiCache Redis (缓存与分布式锁) 网络层: 2 个 VPC (PRD / UAT-SIT) 客户规模: 覆盖金融、央企、制造、科技等行业，业务连续性要求较高 2.2 阿里云目标架构 基于AWS侧的架构，对应的阿里云的目标架构以及产品映射如下： AWS 产品 阿里云产品 迁移说明 Lambda 函数计算 FC 自定义运行时 (custom.debian10) 替代 Python Handler API Gateway 云原生API 网关 重新创建接口与策略 RDS MySQL RDS MySQL 同构迁移, 通过 DTS 实现平滑同步 ElastiCache Redis Tair (兼容 Redis) 通过 DTS 实现平滑同步 S3 OSS 对象存储 代码包/产物存储 CloudWatch ARMS + SLS 日志服务 应用监控 + 分布式追踪 + 日志检索 SQS/SNS 云消息队列 Kafka CDP/COS 消息服务, 改用 kafka-python EC2 ECS SAM / Chalice Deploy Serverless Devs (s deploy) 声明式 YAML 配置, 支持多环境 这里使用debian10而不是直接使用原生Python运行时考虑只要是客户大部分都是HTTP请求，因此使用Debian10并用内置的Python 3.10。容器启动一次后持续接收请求。 维度 Python 内置运行时 自定义运行时 Debian10 环境控制 无（黑盒） 完全可控 依赖安装 仅限纯 Python 包 支持系统包 + 任意 Python 包 启动方式 FC 调用 handler 函数 用户自启 HTTP Server 适用协议 事件驱动 HTTP/gRPC/Web 内置 Python 固定版本（如 3.10） 内置 3.10.9，但可替换 开发复杂度 低 较高（需处理 Server 逻辑） 3. 迁移方案 架构确定后，我们按照框架层 - 部署层 - 可观测 - 调优的顺序进行迁移。该链路遵循依赖收敛原则：先剥离框架层 AWS 专有绑定，再替换底层 SDK 调用，随后接入自动化流水线，最后基于可观测数据反哺性能调优。以下为各阶段具体实现。 3.1 代码改造 2024 年项目初期，代码改造是最耗时的环节。客户使用 AWS Chalice 框架开发，函数深度绑定 AWS SDK（boto3）和 Lambda 事件模型。我们尝试了多种大模型（qwq-plus, deepseek-r1, qwen2.5）+ 结构化 Prompt，让 AI 生成 Chalice→Flask 转换脚本或者直接转换。 结果发现，直接生成转换代码的效果一般，而框架映射部分（路由装饰器、请求对象）映射关系明确，批量替换效果还可以，但是边界 case 需人工修正（Blueprint 注册差异、中间件行为差异等）。不过后续客户说他们那边会自行改造应用就没继续对改造方式进行优化了。 最近在写这文章的时候用Qoder再尝试把示例项目改造一下：一句话完成 Chalice→Flask 改造 + AWS SDK 移除 + 阿里云 SDK 对齐。全部 Python 文件语法检查通过，35+ 条路由正确注册。从"精心构造 Prompt + 多轮人工修正"到"一句话搞定"，代码改造从瓶颈变成了零门槛。（不得不感叹下去年真是突飞猛进的一年啊...） 代码层面的改动汇总（供参考，不再展开）： 改动类 关键变更 框架 Chalice → Flask，Blueprint 注册语法差异，content_types=[...] 移除 请求对象 app.current_request → Flask request，query_params → request.args SDK boto3 移除，S3→oss2，SQS→kafka-python，IAM→AccessKey/STS 配置 ElastiCache/ELB 地址改为阿里云内网 Endpoint 3.2 部署改造 AWS 的部署链路是 chalice package → sam package → sam deploy，依赖 S3 中间桶和 CloudFormation。而阿里云侧采用 Serverless Devs，Serverless Devs是一个开源的 Serverless 开发者工具，通过这个工具可以创建、部署和调用函数，实现项目的全生命周期管理。 部署流程对比 AWS vs 阿里云 # AWS 旧流程 (3 步)
chalice package --stage prd .chalice/packaged-app
sam package --template-file sam.json --output-template-file package-prd.yaml \
  --s3-bucket qop-api-prd --s3-prefix stack_name
sam deploy --template-file package-prd.yaml --stack-name qop-stack \
  --capabilities CAPABILITY_IAM --region cn-north-1

# 阿里云新流程 (1 步)
s deploy  # 基于 s.yaml 一键部署 Serveless dev核心配置解析 (s.yaml) edition: 3.0.0
name: qop-transformer
access: default  # Serverless Devs 账号配置

vars:
  region: cn-shenzhen

resources:
  transformer:
    component: fc3
    props:
      region: ${vars.region}
      functionName: qop-${projectName}-transformer
      description: QOP 客户数据转换层函数
      runtime: custom.debian10        # 关键：自定义运行时
      code: ./
      memorySize: 512
      timeout: 60
      instanceConcurrency: 10         # 单实例最大并发请求数
      cpu: 0.5
      diskSize: 512
      
      # 自定义运行时配置
      customRuntimeConfig:
        command:
          - python3
          - app.py
        port: 8000
      
      # 环境变量
      environmentVariables:
        PYTHONPATH: /opt:/opt/python:/code
        DB_HOST: ${env.DB_HOST}
        REDIS_HOST: ${env.REDIS_HOST}
      
      # VPC 配置 (多可用区容灾)
      vpcConfig:
        vpcId: vpc-bp1xxxxx
        securityGroupId: sg-bp1xxxxx
        vswitchIds:
          - vsw-bp1xxxxx              # cn-shenzhen-a
          - vsw-bp1yyyyy              # cn-shenzhen-b
      
      # 日志配置
      logConfig:
        project: qop-log-project
        logstore: qop-fc-logstore
        enableRequestMetrics: true
        enableInstanceMetrics: true
      
      # 触发器
      triggers:
        - triggerName: httpTrigger
          triggerType: http
          triggerConfig:
            authType: anonymous
            methods:
              - GET
              - POST 关键变化: 不再依赖 sam.json 和 S3 中间桶 环境变量通过 environmentVariables 声明式注入，支持 ${env.XXX} 读取本地环境变量 日志、VPC、触发器统一在 s.yaml 中定义，支持多环境配置覆盖 版本管理：FC 自动保留历史版本，支持快速回滚 CI/CD 集成 (蓝鲸 DevOps) 客户原来采用蓝鲸 DevOps (BlueKing DevOps) 作为 CI/CD 平台，项目中并继续沿用。 # 蓝鲸 DevOps Pipeline 配置示例 (bk-ci.yml)
trigger:
  push:
    branches:
      - master
      - release/**

stages:
  - stage: "构建与部署"
    jobs:
      - job: "deploy_fc"
        agent:
          os: linux
          language: python
          version: "3.9"
        steps:
          - step: checkout
            inputs:
              repository: self
          - step: python
            name: "安装 Serverless Devs 及依赖"
            inputs:
              command: |
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                pip install @serverless-cd/s2
          - step: python
            name: "执行部署"
            inputs:
              command: |
                s deploy --use-local --access-key ${{ secrets.ALIYUN_ACCESS_KEY_ID }} --secret-key ${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}
          - step: notify
            name: "通知构建结果"
            inputs:
              type: wechat
              content: "QOP-FC 部署完成: ${BUILD_STATUS}" 蓝鲸 DevOps 集成要点: 环境变量注入: 通过蓝鲸凭据管理 (Credentials) 注入阿里云 AccessKey，避免硬编码 多环境流水线: 配置 sit / uat / prd 三套独立流水线，支持手动触发与审批卡点 部署审批: 生产环境部署前设置人工审批节点，确保变更可控 3.3 可观测 阿里云 ARMS (应用实时监控) 提供了与 AWS X-Ray 类似的分布式追踪能力。相信Java类型的接入大家比较熟悉，下面以Python类型举例，如何接入FC。 Python FC接入步骤 1. 下载 ARMS Python 探针 (推荐 VPC 内网，速度快且无公网流量费) wget http://arms-apm-cn-shenzhen.oss-cn-shenzhen-internal.aliyuncs.com/aliyun-python-agent/aliyun-python-agent.tar.gz
tar -zxvf aliyun-python-agent.tar.gz 2. 构建为 FC 层，并修改探针启动脚本的 shebang 行： pip install target/*.whl -t aliyun-instrument
# 编辑 ./aliyun-instrument/bin/aliyun-instrument
# 将首行改为 FC 的 Python 路径:
#!/var/fc/lang/python3.10/bin/python3 在FC控制台创建层，并上传层。 在函数配置中使用自定义层。 配置环境变量: 环境变量 值 说明 ARMS_APP_NAME FC:qop-transformer 应用名称，用于 ARMS 控制台展示 ARMS_LICENSE_KEY (从 ARMS 控制台获取) License Key ARMS_REGION_ID cn-shenzhen 地域 ID PYTHONPATH /opt:/opt/python:/code 确保探针路径优先加载 4. 修改启动命令: customRuntimeConfig:
  command:
    - aliyun-instrument    # 替换原 python3
    - app.py
  port: 8000 函数级别监控规则 单个函数可以通过控制台来配置指标告警规则。 当需要为多个函数进行配置的时候，可使用云监控的API来批量设置告警规则： QueryMetricRequest request = new QueryMetricRequest();
request.setProject("acs_fc");
request.setMetric("RegionFunctionErrors"); 支持的指标可以通过云监控的指标和事件中心去查看： 3.4 运行时调优 配置相关的监控，可以帮助我们对函数运行时进一步优化，下面说下我们当中碰到一些问题： 问题 1: 定时函数弹性策略限制 客户发现函数的触发花费的时间较长，对比发现，冷启动就花费了7900ms。 这个函数并没有设置预留实例： 为了解决冷启动问题，设置了最小实例数，并设置预留实例，提前锁定资源： 问题 2: 函数的执行时间过长 从日志看出就算预留了实例，部分函数执行时间还是大概为900毫秒，接口日志写的耗时为63毫秒。 查看完整的日志发现在启动时候会加载环境配置，并初始化项目。这种一般需要把代码初始化耗时较多的项例如连接数据库、加载依赖等放Initializer回调中，等初始化执行结束后才将请求调度过去。不过这个意味着需要对应用做相关的修改，客户反馈说需要去做进一步的评估排期。 # 改造前：初始化在请求处理内
def handle_request(event):
    db_pool = create_pool()      # 每次请求都创建连接池，~200ms
    redis_conn = get_redis()     # 每次请求都建立 Redis 连接，~100ms
    config = load_config()       # 每次请求都读配置文件，~50ms
    # 业务逻辑：63ms
    ...

# 改造后：初始化在 Initializer 内
db_pool = None
redis_conn = None
config = None

def initializer(context):
    global db_pool, redis_conn, config
    db_pool = create_pool()      # 容器启动时执行一次
    redis_conn = get_redis()     # 容器启动时执行一次
    config = load_config()       # 容器启动时执行一次

def handle_request(event):
    # 直接使用已初始化的全局对象
    result = db_pool.execute(...)
    ... 问题 3: 接口时延过长 客户采用应用分批迁移，最后再切换数据库。在第一批应用迁移到阿里云后，发现延时较大。查看具体的 Trace 详情，发现数据库调用花了差不多1秒。 由于本身通过VPN调用，AWS北京与阿里云深圳的时延本身就大概需要40ms以上。我们修改了后续的割接方案。详情见下一节。 问题 4: Flask 部署后直接退出 现象: 本地 flask run 正常运行，部署到 FC 后报错 Function instance exited unexpectedly (code 0) 根因: Python 运行时默认使用 Handler 模式 (app.index)，但 Flask 是常驻 Web 服务。如果没有监听端口，容器启动后会立即退出。 解决: 使用 custom.debian10 运行时，并在 app.py 添加入口函数： # app.py
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)  # 必须监听 0.0.0.0 # s.yaml
runtime: custom.debian10
customRuntimeConfig:
  command:
    - python3
    - app.py
  port: 8000 问题 5: 依赖包过大导致冷启动慢 现象: 每个函数打包都包含完整的第三方依赖 (boto3, requests, redis 等)，代码包 ~50MB，冷启动时间长达 3-5 秒。 优化: 将公共依赖抽离为 FC 层 (Layer)。 # 打包公共层
mkdir -p python
pip install redis pymysql requests kafka-python -t python/
zip -r common-layer.zip python/ 效果: 函数代码包从 ~50MB 降至 ~5MB 冷启动时间缩短 30%~50% 依赖统一管理，更新一次 Layer 所有函数生效 4. 割接方案 在问题三我们可以看到时延较大的问题后，对比了三种数据割接方案，最终选择了方案三 - 数据库Redis跟着应用一起分批迁移过来，MySQL 继续跨云访问。 方案 架构描述 优点 缺点 决策 1 Redis + MySQL 全部迁至阿里云 架构最简洁，无跨云依赖 部分应用需加白，无法同步割接，风险高 ❌ 2 读在阿里云，写在 AWS (DTS 单向同步) 业务无感知，平滑过渡 增量同步延迟，写放大风险，数据一致性难保障 ❌ 3 Redis 读写=阿里云，MySQL 跨云访问 AWS Redis是高频访问，跨云延迟对性能影响最大 风险可控，回滚成本低 MySQL跨云延迟 Redis存在功能自增+加锁的操作 可能存在客户确认了订单后，写入MySQL的操作还没完成，但是这种频率相对比较低 ✅ 阿里云与AWS的跨云访问通过100M VPN访问，由于VPN曾经有断开的情况，因此把已经迁移过来的应用的MySQL也同步到阿里云中，在阿里云上读写MySQL。未迁移的应用在迁移的时候把MySQL的数据也同步迁移过来。这个方案的前提是客户的应用对MySQL的读写相对来说比较独立，较少有写入共享表的情况。在阿里云侧设置超大自增主键避免主键冲突。采用数据同步而非数据迁移的方式，能够在增量阶段动态添加表或者去掉表。 具体的割接步骤：不同的业务项目都相对比较独立，割接宗旨是逐个迁移、验证成功后再迁移下一个。 步骤 1: 关闭 AWS 定时层 Lambda (Scheduler)
  └─ 停止对应项目的 qop-{customer}-every*X*-scheduler 函数
  └─ 确认无正在执行的定时任务

步骤 2: 客户数据同步 (Redis 缓存)
  └─ 调用 https://网关/dfw/initsync/toredis/{项目编号}/all
  └─ 确认DTS增量同步开关已打开 

步骤 3: 开启阿里云定时层 FC (Scheduler)
  └─ 启用对应的 FC 定时触发器
  └─ 验证访问客户 API 正常

步骤 4: 配置 MQ 路由
  └─ routing.msg.customer={客户编号1},{客户编号2},...
  └─ 观察 AWS 和阿里云两个环境的日志

步骤 5: 客户切流
  └─ 客户最新缓存数据同步 (api.auth.token 验证)
  └─ 将客户项目预先配置好的阶段进行切换
  └─ 模拟读请求验证

步骤 6: 观察与验证
  └─ 双环境日志观察，确认无异常后标记完成
  └─ 如果流量少，可执行预先准备的测试请求 回滚预案 数据回滚: 保留 AWS 侧原始数据 30 天 流量回滚: MQ 路由配置可实时修改，5 分钟内切回 AWS 配置回滚: FC 版本管理支持一键回退至上一版本 5. 总结 整个项目中途因为客户人力资源不足暂停了几个月的时间，今年3月，800+ Lambda 完全平滑迁移到阿里云FC，最终收敛为600+个函数稳定运行。 一个项目的完成离不开项目组各位同事的紧密协作与辛勤付出。在此感谢（排名不分先后）：阿貔，高浩，姚翔，高涛，衷涛，饮冰，雅枫，刘衍等的支持。
