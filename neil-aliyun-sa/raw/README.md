# Raw Sources — 不可变源层

> **Karpathy LLM Wiki 第一层**：Raw sources are immutable — the LLM reads from them but never modifies them. This is your source of truth.

## 设计原则

1. **只读不改** — LLM 只从 raw/ 读取，永不修改已归档的源文件
2. **来源追溯** — 每个文件保留原始 URL、抓取日期、格式
3. **去重归档** — 同一来源只入库一次，用文件名或 frontmatter 标注唯一性
4. **本地持久** — 避免依赖外部 URL（链接可能失效），核心资料存本地副本

## 目录结构

```
raw/
├── README.md          # 本文件：raw 层说明
├── ata/               # ATA 内部文章（markdown 快照）
├── aliyun-docs/       # help.aliyun.com 官方文档片段
├── customer-cases/    # 客户案例原始资料
├── industry-reports/  # 行业报告、白皮书
├── competitor/        # 竞品云白皮书、公开资料
└── misc/              # 其他（会议纪要、内部邮件等）
```

## 命名约定

`{来源类型}-{日期}-{简称}.md`

示例：
- `ata-2026-06-17-ai-consultant-11day.md`
- `aliyun-docs-2026-06-17-caf-framework.md`
- `customer-2026-06-18-bmw-landing-zone.md`

## 与 inbox.md 的关系

- `knowledge/inbox.md` 是 raw 层的**注册入口**（索引 + 状态机）
- 本目录是 raw 层的**实体存储**（完整原始内容）
- 投喂流程：用户提供来源 → 写入 inbox（注册）→ 存入 raw/（归档）→ 蒸馏到 knowledge/（编译）
