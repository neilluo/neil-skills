# 数字员工身份卡系统

> QoderWake 为每个数字员工自动生成的角色定义文件体系，通过 9 份 Markdown 身份卡 + 自动生成的 plugin.json 实现员工个性化和行为控制。

## 概述

每个 Waker（数字员工）在创建时，QoderWake 会在 `~/.qoderwake/data/workers/<agent-id>/` 下自动生成一套完整的身份卡和插件配置。这套机制让每个数字员工拥有独立的人格、能力边界和行为规范。

## 目录结构

```
data/workers/<agent-id>/
├── .qoder/                      # 身份卡目录
│   ├── IDENTITY.md              # 核心职责
│   ├── PERSONA.md               # 工作风格/性格
│   ├── BIBLE.md                 # 工作流/协作原则
│   ├── MEMORY.md                # 长期记忆
│   ├── USER.md                  # 用户画像
│   ├── TOOLS.md                 # 可用工具说明
│   ├── CORE_CAPABILITIES.md     # 核心能力
│   ├── DELIVERY_COMMITMENTS.md  # 交付承诺
│   └── WORK_STYLES.md           # 工作风格
├── .qoder-plugin/               # 自动生成的插件配置
│   ├── plugin.json              # 技能列表
│   ├── .mcp.json                # MCP 服务注入
│   ├── hooks/hooks.json         # Hook 链配置
│   ├── output-styles/           # 行为注入规范
│   └── skill-versions/          # 技能版本快照
├── workspace/                   # 工作目录
└── indexes/
    └── agent.sqlite             # 员工私有记忆/索引
```

## 身份卡详解

### IDENTITY.md — 我是谁

定义员工的核心职责和角色边界：
- 角色名称（如「产品经理」「测试工程师」）
- 核心职责列表
- 不做什么（负面边界）

### PERSONA.md — 我的性格

定义员工的沟通风格和个性特征：
- 沟通语气（正式/友好/技术化）
- 工作偏好（注重细节/快速迭代）
- 决策风格

### BIBLE.md — 我的工作准则

定义工作流程和协作原则：
- 标准工作流程步骤
- 与其他角色的协作规则
- 质量标准和交付规范

### CORE_CAPABILITIES.md — 我能做什么

列举员工的核心能力：
- 专业技能清单
- 工具使用能力
- 输出物类型

### DELIVERY_COMMITMENTS.md — 我承诺交付什么

定义交付标准：
- 输出格式要求
- 质量检查清单
- 时效承诺

### WORK_STYLES.md — 我怎么工作

定义工作方式偏好：
- 并行/串行偏好
- 沟通频率
- 反馈方式

### MEMORY.md — 我记住了什么

长期记忆文件，随工作积累自动更新。

### USER.md — 我了解的用户

用户画像，记录用户偏好和沟通风格。

### TOOLS.md — 我能用什么工具

可用工具的说明和使用指南。

## 员工模板系统

### 模板来源

模板通过 `/api/employee-templates` 拉取，存储在：
`~/.qoderwake/data/employee-conf-templates.local.json`

### 内置模板

| 模板 | 角色 | 预装技能数 |
|------|------|-----------|
| product-manager | 产品经理 | 6（PRD/竞品/反馈等） |
| qa-engineer | 测试工程师 | 待确认 |
| software-developer | 开发工程师 | 待确认 |

### 模板结构

```json
{
  "templates": {
    "product-manager": {
      "conf_map": [{
        "name": "PM",
        "templateTag": "product-manager",
        "avatar": "...",
        "skill": ["prd-generation", "competitor-research", ...],
        "mcp": [...],
        "wakerContext": {
          "identity": "...",
          "persona": "...",
          "bible": "..."
        }
      }]
    }
  }
}
```

### 技能自动安装

员工创建时，BuiltinSkillManager 通过 manifest + OSS ZIP 自动安装角色专属技能：
- 产品经理 6 个技能：browser-harness / changelog-management / competitor-research / prd-generation / requirement-pool-management / user-feedback-analysis

## Output Style — 行为注入

`output-styles/qoderwake_output_style.md` 通过 YAML front-matter + Markdown 向 LLM 注入行为规则：

```yaml
---
keep-coding-instructions: false
---
```

注入内容包括：
- **记忆使用规范**：project 优先于 agent 级别
- **Secret 禁止存储**：凭据类信息不得写入记忆
- **present_files 工具规范**：产出物展示格式
- **记忆防幻觉规则**：必须有 evidence 支撑才能写入记忆

## 技能版本控制

每个技能在 `skill-versions/<skillId>/` 下有完整版本历史：

```
skill-versions/<skillId>/
├── config.json          # git 引擎策略（auto/system）
├── events.jsonl         # 版本事件流
├── manifests/           # 各版本清单（contentHash sha256）
└── git/                 # 完整 git 仓库（每版本一个 tag）
```

Tag 命名：`skill/<skillId>/<YYYYMMDD>/v<NNNN>-<时间戳>`

## 交叉引用

- [[waker]] — Waker 实体的上层定义
- [[role]] — 角色模板与身份卡的关系
- [[waker-hook-lifecycle]] — 身份卡在 SessionStart Hook 中的注入时机
- [[waker-memory]] — MEMORY.md 与 agent.sqlite 的关系
- [[cli-skill]] — QoderCLI 技能系统（底层 SKILL.md 格式）

## 来源

- ~/.qoderwake/data/workers/<agent-id>/.qoder/ 目录结构 [reverse-engineering] 2026-06-30
- ~/.qoderwake/data/employee-conf-templates.local.json [reverse-engineering] 2026-06-30
- ~/.qoderwake/resources/builtin-skills/manifest.json [reverse-engineering] 2026-06-30
