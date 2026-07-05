---
name: neil-cicd-skills
description: CI/CD 部署全流程指南，覆盖 Aone CI、GitHub Actions、GitLab CI 三平台。当用户需要为 Java/Node 项目配置自动构建部署流水线、容器化部署到阿里云 ECS/ACK、或排查 Pipeline 失败时使用。帮助 AI 避免已知坑点，选择正确的架构路径，快速达成部署目标。
---

# CI/CD 部署 Skill

## 核心原则

1. **先验证再构建**：每次修改 Pipeline 配置前，确认目标环境的约束（网络、工具链、权限）
2. **构建与打包分离**：CI Runner 做构建（有系统资源），Docker 只做运行时打包（轻量快速）
3. **内网优先**：镜像拉取走 VPC 内网地址，避免公网带宽瓶颈
4. **单步调试**：Pipeline 失败时加调试步骤（env、pwd、ls），定位后再修复
5. **先读文档**：每个 CI 平台语法不同，不要假设，先确认官方规范

---

## 平台决策矩阵

| 决策点 | Aone CI | GitHub Actions | GitLab CI |
|--------|---------|---------------|-----------|
| 配置文件位置 | `.aoneci/xxx.yml` | `.github/workflows/xxx.yml` | `.gitlab-ci.yml` |
| 代码检出 | `uses: checkout`（必须显式） | `uses: actions/checkout@v4` | **自动** |
| 变量引用 | `${{ vars.X }}` / `${{ secrets.X }}` | 同左 | `$VAR`（自动注入 env） |
| Runner 环境 | aone-hosted（默认有，ci-8u 镜像） | GitHub-hosted（默认有） | 需自建或 SaaS |
| Docker 支持 | `runs-on: [dind]` 标签 | 默认支持 | `services: [docker:dind]` |
| 触发规则 | `triggers.push.branches` | `on.push.branches` | 默认自动触发 |
| PATH 跨 step | ❌ 不传递 | ❌ 需 `>>$GITHUB_PATH` | ❌ 不传递 |
| 制品传递 | outputs.artifacts（跨job不稳定） | upload/download-artifact | `artifacts: paths:` |
| 缓存 | 无内置（靠 Docker layer） | `actions/cache@v4` | `cache:` 关键字 |

---

## Aone CI 完整指南

### YAML 基本结构

```yaml
name: pipeline-name

triggers:
  push:
    branches:
      - master

jobs:
  job-name:
    runs-on: [aone-hosted, resource:4-16Gi]
    steps:
      - name: 检出代码
        uses: checkout
      - name: 执行
        run: |
          set -e
          # 命令
```

### 已验证坑点清单（按发生顺序）

| # | 坑点 | 现象 | 根因 | 解法 |
|---|------|------|------|------|
| 1 | 以为是 GitLab CI | `.gitlab-ci.yml` 无效 | Aone CI 独立语法 | 读文档：aoneci.io.alibaba-inc.com |
| 2 | 不自动 checkout | 目录为空 | 必须显式声明 | `uses: checkout` |
| 3 | `${{ variables.X }}` null | 变量无值 | 语法错误 | 用 `${{ vars.X }}` |
| 4 | PATH 不跨 step | 工具找不到 | 每步独立 shell | 合并到同一 run 块 |
| 5 | Maven 下载 404 | mirrors.aliyun.com 无版本 | 镜像不全 | fallback archive.apache.org |
| 6 | Alpine TLS 失败 | apk add 报错 | DinD 网络限制 | 换 Debian 基础镜像 |
| 7 | ECS 无 compose | command not found | 未预装 | 直接用 `docker run` |
| 8 | 公网 pull 25min | 1Mbps 瓶颈 | 公网带宽限制 | ACR VPC 内网地址 |
| 9 | SSH heredoc 失败 | exit 255 | YAML 缩进破坏 | 用 scp 上传文件替代 |
| 10 | .state.json 丢失 | 409 Conflict | 容器无状态 | `-v` 挂载持久化 |
| 11 | Secrets 用 vars | unauthorized | 类型不匹配 | Secrets 必须 `${{ secrets.X }}` |

### 推荐 Pipeline 架构

```
Job 1: build-and-push (runs-on: [aone-hosted, resource:4-16Gi, dind])
  ├── uses: checkout
  ├── yum install java-21 + curl Maven
  ├── mvn package → app.jar
  ├── curl Node → npm build → frontend-dist/
  ├── docker login ACR (secrets.ACR_PASSWORD)
  ├── docker build (轻量 Dockerfile)
  └── docker push ACR

Job 2: deploy (needs: build-and-push)
  ├── uses: checkout
  ├── 生成 .env (本地 cat heredoc + scp)
  ├── ssh ECS: docker login ACR(VPC) → pull → stop → rm → run
  └── 健康检查 (curl loop)
```

### 关键模板

**Dockerfile（轻量，不做构建）：**
```dockerfile
FROM eclipse-temurin:21-jre
RUN apt-get update && apt-get install -y --no-install-recommends nginx curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY app.jar /app/app.jar
COPY frontend-dist/ /opt/frontend/
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80 8090
ENTRYPOINT ["/entrypoint.sh"]
```

**docker run（避免 compose 依赖）：**
```bash
docker run -d --name app \
  --restart unless-stopped \
  -p 80:80 -p 8090:8090 \
  --env-file /opt/app/.env \
  -v /opt/app/.state.json:/app/.state.json \
  -v /opt/app/logs:/app/logs \
  ACR_VPC_ADDRESS/ns/repo:tag
```

---

## 性能优化

### 构建阶段优化

| 优化项 | 效果 | 方法 |
|--------|------|------|
| 构建与 Docker 分离 | 33min → 10min | Runner 构建，Docker 只 COPY |
| Docker layer cache | 10min → 4min | 基础镜像层复用 |
| ACR VPC 拉取 | 25min → 30s | `-vpc` 域名 |
| Maven 内网镜像 | 省 5min | Aone 自动走 artlab |
| npm 国内镜像 | 省 2min | `--registry=npmmirror.com` |

### 运行时静态资源优化（关键！）

**问题**：Debian 默认 Nginx 的 `gzip_types` 被注释，JS/CSS/JSON 全部未压缩传输。在 1Mbps 带宽 ECS 上，266KB JS 需要 2-3 秒下载。

**实测效果**：
| 优化项 | 优化前 | 优化后 | 提升 |
|--------|--------|--------|------|
| Nginx gzip 压缩 | 266KB 未压缩 | 82KB gzip | **70% 体积减少** |
| 前端 JS 加载 | 700ms | 40ms | **17x 加速** |
| gzip_static 预压缩 | 实时压缩耗 CPU | 零 CPU（.gz 直出） | CPU 友好 |
| 代码分包 | 每次全量下载 | vendor 缓存 30 天 | 后续访问秒开 |

**三步落地方案**：

**Step 1: Nginx 配置（deploy/nginx.conf）必须显式启用 gzip_types**
```nginx
server {
    listen 80;
    server_name _;

    # ⚠️ 关键：Debian Nginx 默认注释了 gzip_types，必须手动开启
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_min_length 256;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/xml
        image/svg+xml
        font/woff2;
    # 优先使用构建时生成的 .gz 文件（零 CPU 开销）
    gzip_static on;

    root /opt/frontend;
    index index.html;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8090;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # SSE 长连接
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 600s;
    }

    # 静态资源长缓存（Vite 带 hash 指纹）
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 200m;
}
```

**Step 2: Vite 构建时预压缩 + 代码分包（vite.config.ts）**
```ts
import viteCompression from 'vite-plugin-compression'

export default defineConfig({
  plugins: [
    react(),
    // 构建时生成 .gz 预压缩文件，配合 Nginx gzip_static
    viteCompression({ algorithm: 'gzip', threshold: 1024 }),
  ],
  build: {
    rollupOptions: {
      output: {
        // vendor（React 等）单独分包，利用浏览器 30 天缓存
        manualChunks(id) {
          if (id.includes('node_modules/react')) return 'vendor';
        },
      },
    },
  },
})
```
需安装: `npm install vite-plugin-compression --save-dev`

**Step 3: 验证 gzip 生效**
```bash
# 必须看到 Content-Encoding: gzip，否则优化未生效
curl -s -I -H "Accept-Encoding: gzip" http://YOUR_HOST/assets/vendor-xxx.js | grep -i content-encoding
# 期望输出: Content-Encoding: gzip
```

**常见陷阱**：
- ⚠️ Debian/Ubuntu 的 `/etc/nginx/nginx.conf` 中 `gzip_types` 那行默认被 `#` 注释
- ⚠️ 只在主 `nginx.conf` 写 `gzip on` 不够，必须同时配置 `gzip_types`
- ⚠️ `gzip_static on` 需要 .gz 文件与原文件同目录同名，Vite 插件自动生成
- ⚠️ 验证时必须带 `-H "Accept-Encoding: gzip"` header，否则看不到压缩效果

---

## 规模化决策

| 规模 | 方案 | 核心变化 |
|------|------|---------|
| 1-5 台 | Docker + SSH | CI SSH 直连每台 |
| 10-50 台 | Docker + ACR + Ansible | 批量 pull + 滚动 |
| 50+ 台 | K8s (ACK) | `replicas: N`，HPA |

---

## GitHub Actions 指南（待学习补充）

### 已知差异
- `actions/setup-java@v4`、`actions/setup-node@v4` 等官方 action
- `docker/build-push-action` 集成 layer cache
- OIDC 免密认证推镜像

### 待学习
- [ ] Matrix 构建
- [ ] Self-hosted runner
- [ ] 缓存策略
- [ ] Reusable workflows

---

## GitLab CI 指南（待学习补充）

### 已知差异
- 代码自动 clone，变量自动注入 env
- `services: [docker:dind]`
- `artifacts: paths:` 跨 job 自动传递

### 待学习
- [ ] Runner 注册
- [ ] include/extends
- [ ] Auto DevOps

---

## 复盘方法论

### 排查 Pipeline 失败的正确姿势
1. **加调试步骤**：`pwd && ls && env | grep KEY` → 定位环境
2. **一次一变量**：每次只改一处，观察效果
3. **看完整日志**：不只看 ERROR，往上看 WARNING 和执行路径
4. **理解网络拓扑**：内网→公网通，公网→内网不通
5. **先读官方文档**：不假设，不猜测

### 本次部署成功路径
```
读 Aone CI 文档 → 修正 YAML 语法 → 加 checkout
→ 合并 step 避免 PATH 丢失 → vars/secrets 语法修正
→ 构建与 Docker 分离 → Debian 替代 Alpine
→ docker run 替代 compose → VPC 内网 pull → 挂载 .state.json
= 全绿 ✅
```

---

## 构建速度演进（关键架构错误复盘）

### 错误链条

```
v1: 并行CI构建(8min) ──[想要Docker化]──> v2: Docker多阶段(33min+OOM) ❌❌❌
                                              │
                                              │ [认识到错误]
                                              ▼
                                         v3: CI构建+Docker打包(13min)
                                              │
                                              │ [layer cache生效]
                                              ▼
                                         v4: 有缓存(4min) ✅
```

### 核心错误：把"构建"塞进 Docker

| 对比维度 | CI Runner 直接构建 | Docker 多阶段构建 |
|---------|-------------------|------------------|
| 并行性 | ✅ 多 job 并行（Maven∥Node） | ❌ Docker 内串行 |
| 依赖缓存 | ✅ Runner 有 yum/Maven 缓存 | ❌ 每次从零下载 |
| 资源 | ✅ Runner 全量 CPU/RAM | ❌ Docker buildkit 受限（npm OOM）|
| 网络 | ✅ 内网快速下载 | ❌ Docker 内网络可能受限 |
| 首次耗时 | 8-10 min | 33 min |
| 有缓存耗时 | 3-4 min | 10-15 min |

### 正确的 Docker 使用姿势

```
❌ 错误：Docker 多阶段 = 构建环境 + 运行环境
   FROM maven:3.9 AS builder    ← 在Docker里装环境、下依赖、编译
   RUN mvn package              ← 每次从零开始，无缓存
   FROM node:22 AS frontend     ← 又一个大镜像要拉
   RUN npm ci                   ← Docker内存不够，OOM

✅ 正确：CI Runner 构建 + Docker 只打包运行时
   CI: yum install java + mvn package + npm build  ← 快，有缓存
   Docker: FROM eclipse-temurin:21-jre              ← 轻量基础镜像
           COPY app.jar + frontend-dist/            ← 只COPY产物
           ← 打包只需30秒
```

### 速度优化 Checklist

**构建阶段：**
- [ ] **构建不进 Docker**：mvn/npm 在 CI Runner 环境执行
- [ ] **Docker 只做打包**：Dockerfile 只有 FROM + COPY + EXPOSE
- [ ] **并行 job**（如果平台支持 artifact 传递稳定）：Maven 和 Node 并行
- [ ] **国内镜像**：Maven 走 artlab/aliyun，npm 走 npmmirror
- [ ] **VPC 内网 pull**：ECS 用 `-vpc` 域名拉 ACR 镜像
- [ ] **Layer cache**：基础镜像层（JRE+Nginx）只拉一次

**运行时优化（部署后必查）：**
- [ ] **Nginx gzip_types 已启用**：不能依赖默认配置，必须显式声明
- [ ] **gzip_static on**：Vite 构建生成的 .gz 文件被 Nginx 直接使用
- [ ] **前端代码分包**：vendor(React) 与业务代码分离，利用长缓存
- [ ] **静态资源 Cache-Control**：带 hash 的文件设 `immutable` + 30 天
- [ ] **验证 Content-Encoding: gzip**：curl 确认压缩生效，未生效等于白做
