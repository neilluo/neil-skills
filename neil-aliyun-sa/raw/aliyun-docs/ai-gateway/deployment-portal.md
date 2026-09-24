---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/deployment-portal
fetch_date: 2026-09-21
product: AI Gateway
slug: deployment-portal
body_sha256: 95332647ca8da578e32c4031ddb45e9e6fb349b5b7186188fb0f35572dac9c24
body_bytes: 8008
migration_status: current
---

开放平台面向外部开发者的自助服务站点。本文介绍如何在阿里云 SAE、ACK 以及本地 Docker 环境中部署门户服务，快速搭建生产就绪或开发测试用的开发者门户。  

## 部署方式对比
门户服务支持以下部署方式，可根据实际场景选择：
<table> <thead> <tr> <td><p><b>部署方式</b></p></td> <td><p><b>适用场景</b></p></td> <td><p><b>说明</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>阿里云 SAE</p></td> <td><p>生产环境推荐</p></td> <td><p>Serverless 应用引擎，免运维、自动弹性伸缩</p></td> </tr> <tr> <td><p>阿里云 ACK</p></td> <td><p>大规模生产环境</p></td> <td><p>容器服务 Kubernetes 版，适合复杂编排需求</p></td> </tr> <tr> <td><p>本地 Docker</p></td> <td><p>开发测试</p></td> <td><p>本地快速验证，不适用于生产</p></td> </tr> </tbody> </table>

## 在 SAE 中部署门户（推荐）
阿里云 Serverless 应用引擎（SAE）是部署门户服务的推荐方式，具备免服务器运维、自动弹性伸缩、按需付费等优势。

### 前提条件

部署前需完成以下准备工作：

1. 已开通阿里云 SAE 服务，并创建命名空间。

2. 已在开放平台控制台创建门户实例，并获取门户 ID。

**说明**

门户服务的镜像地址为固定地址，部署时直接填写即可，镜像地址见下文部署步骤。

### 创建应用

1. 登录[阿里云 SAE 控制台](https://sae.console.aliyun.com/)。

2. 在**应用管理** 页面，点击**创建应用**。

3. 填写基础信息：

   * **应用名称**：建议使用门户名称，便于识别。

   * **描述**：简要说明应用用途。

   * **命名空间**：选择已创建的命名空间。

4. 选择部署方式：

   * **部署方式** ：选择**镜像部署**。

   * **镜像地址** ：填写`opensource-registry.cn-hangzhou.cr.aliyuncs.com/higress-group/himarket-portal:latest`。

5. 配置实例规格（按需设置）：

   * **vCPU**：建议 0.5 核或以上。

   * **内存**：建议 1 GiB 或以上。

   * **实例数**：根据实际访问量配置，最小 1 实例。

### 配置环境变量

在应用配置中添加以下必需的环境变量。

#### 核心配置

<table> <thead> <tr> <td><p><b>环境变量名称</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>示例值</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>POP_GATEWAY_URL</code></p></td> <td><p>门户服务访问 APIG OpenAPI 的 Endpoint。<br>公网：<code>https://apig.{regionId}.aliyuncs.com</code><br>内网：<code>https://apig-vpc.{regionId}.aliyuncs.com</code></p></td> <td><p><code>https://apig.cn-hangzhou.aliyuncs.com</code></p></td> </tr> <tr> <td><p><code>POP_REGION_ID</code></p></td> <td><p>门户服务所在的地域 ID。</p></td> <td><p><code>cn-hangzhou</code></p></td> </tr> <tr> <td><p><code>PORTAL_ID</code></p></td> <td><p>在开放平台控制台创建的门户 ID。</p></td> <td><p><code>portal-xxx</code></p></td> </tr> </tbody> </table>

#### 认证配置（二选一）

门户服务需要访问阿里云 OpenAPI，需配置认证凭证。SAE 支持 RRSA OIDC 和 AccessKey 两种方式，推荐优先使用 RRSA OIDC，安全性更高。

#### 方式一：RRSA OIDC（推荐，仅 SAE 支持）

在配置应用时启用 RRSA OIDC 功能。此方式无需在环境变量中配置 AK/SK，通过 OIDC 令牌自动获取临时凭证，安全性更高。SAE RRSA OIDC 配置方式参考：[设置身份认证服务功能（邀测）](https://help.aliyun.com/document_detail/2858232.html)  
**说明**

RRSA OIDC 为 SAE 特有功能，ACK 环境不支持此方式。

#### 方式二：AccessKey 认证

如暂时无法使用 RRSA OIDC，或部署在 ACK 环境，可在环境变量中配置阿里云子账号的 AccessKey。
<table> <thead> <tr> <td><p><b>环境变量名称</b></p></td> <td><p><b>说明</b></p></td> <td><p><b>示例值</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>ALIYUN_ACCESS_KEY_ID</code></p></td> <td><p>阿里云子账号的 AccessKey ID。</p></td> <td><p><code>LTAxxx</code></p></td> </tr> <tr> <td><p><code>ALIYUN_ACCESS_KEY_SECRET</code></p></td> <td><p>阿里云子账号的 AccessKey Secret。</p></td> <td><p><code>3f98xxx</code></p></td> </tr> </tbody> </table>  
**重要**

使用 AccessKey 方式时，请确保：

* 使用子账号 AK/SK，避免使用主账号。

* 该子账号需具备下文所述的 RAM 权限策略。

### 配置 RAM 权限

门户服务需要访问阿里云 AI 网关资源，请为子账号配置以下权限。

#### 系统权限策略

* `AliyunAPIGReadOnlyAccess`：阿里云云原生 API 网关资源的只读权限。

#### 自定义权限策略

由于门户服务需要管理消费者（Consumer），需要额外添加以下自定义策略：

```
HELPCODEESCAPE-json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apig:*Consumer*"
      ],
      "Resource": "*"
    }
  ]
}
```

### 配置访问接入

应用部署完成后，需要配置访问接入点，使外部可以访问门户服务。

#### 方式一：通过 API 网关访问（推荐）

推荐使用阿里云 API 网关作为门户服务的统一接入层，可获得流量控制、安全防护、监控告警、日志审计等能力。

1. 登录阿里云 API 网关控制台，开通 API 网关服务。

2. 创建 SAE 类型的服务，选择已部署的门户应用作为后端。

3. 创建 HTTP API，配置路由规则（例如将路径`/*`转发到门户服务的`8000`端口）。

4. 通过 API 网关生成的接入点地址访问门户。

#### 方式二：通过负载均衡访问

如暂不需要 API 网关的高级功能，也可通过负载均衡直接暴露服务。

1. 进入 SAE 控制台应用详情页。

2. 点击**添加访问方式**。

3. 选择负载均衡类型，NLB 或 CLB 均可。

4. 配置监听端口：

   * **协议**：TCP

   * **容器端口** ：`8000`（门户服务默认端口）

5. 保存后，系统会分配访问地址，可通过该地址访问门户。

### 验证部署

完成上述配置后，启动应用并验证部署是否成功：

1. 在 SAE 控制台查看应用实例状态，确保运行正常。

2. 通过配置的访问地址访问门户首页，确认页面加载正常。

3. 测试开发者注册、登录、浏览 API 产品等核心功能。

## 在 ACK 中部署门户
对于需要更复杂编排能力的大规模生产环境，可选择阿里云容器服务 Kubernetes 版（ACK）部署。

### 部署步骤概述

1. 准备 Kubernetes 部署 YAML，包含 Deployment、Service 等资源。

2. 配置 ConfigMap 存储环境变量（`POP_GATEWAY_URL`、`POP_REGION_ID`、`PORTAL_ID`等）。

3. 配置 Secret 存储`ALIYUN_ACCESS_KEY_ID`和`ALIYUN_ACCESS_KEY_SECRET`。

4. 配置接入方式。推荐通过 API 网关接入，也可配置 Ingress 或 SLB 直接暴露。

### 接入方式建议

与 SAE 部署相同，ACK 环境中的门户服务同样推荐使用阿里云 API 网关作为统一接入层。

1. 在 API 网关控制台创建容器类型的服务。

2. 创建 HTTP API 并配置路由规则。

3. 通过 API 网关接入点访问门户，获得流量控制、安全防护等能力。

## 在本地 Docker 中部署
适用于开发测试环境快速验证功能。

### 运行命令

```
HELPCODEESCAPE-bash
docker run -d \
  --name portal \
  -p 8000:8000 \
  -e POP_GATEWAY_URL=https://apig.cn-hangzhou.aliyuncs.com \
  -e POP_REGION_ID=cn-hangzhou \
  -e PORTAL_ID=portal-xxx \
  -e ALIYUN_ACCESS_KEY_ID=LTAxxx \
  -e ALIYUN_ACCESS_KEY_SECRET=3f98xxx \
  registry.cn-hangzhou.aliyuncs.com/acs/alibaba-cloud-portal:latest
```

运行后，访问`http://localhost:8000`即可访问门户，端口可按需修改。