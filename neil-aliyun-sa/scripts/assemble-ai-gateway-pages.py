#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 7 路蒸馏 partial 装配成 knowledge/ 下的专题页家族。

装配规则（R3 裁决）：扁平 7 文件，不建子目录，每文件 < 2500 行。
- W1 的 §1/§2 并入主页 knowledge/aliyun-ai-gateway.md（与主控的 §0/§14/§15 同文件）
- W2~W7 各自成为一个后缀命名的子页
- 统一页眉（所属/来源/raw层/标注体系/口径优先级/对客纪律）
- partial 自己的前言（blockquote 导读）保留为「本章导读」，HTML 注释与 `# W*` 标题剥掉
- 正文逐字保留，不改一字（主控只做装配与页眉，不做二次改写 —— 避免引入新的失真）
"""
import re
import sys
from pathlib import Path

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent
PARTIALS = Path("/tmp/aigw-partials")

COMMON = """> **所属**：[[aliyun-ai-gateway]] 专题页家族（7 文件）｜**主页与导航**：[aliyun-ai-gateway.md](aliyun-ai-gateway.md)
> **来源**：阿里云 API 网关 · AI 网关官方文档全站蒸馏（`help.aliyun.com/zh/api-gateway/ai-gateway/`），快照抓取日 **2026-09-21**
> **raw 层**：`raw/aliyun-docs/ai-gateway/`（186 个快照 = 149 个有正文页 + 37 个 TOC 容器页；另有 SLA 协议全文外部源 1 页）
> **事实标注体系**：`[官方｜slug]` raw 快照有明文依据 ｜ `[官方原文]` 逐字引用 ｜ `[官方矛盾]` 官方自相矛盾（双方原文并列，**默认不裁决**）｜ `[推断]` 由官方事实推出（附推理链）｜ `[文档未说明]` raw 查无此项 ｜ `[原文如此]` 官方原文错字照录
> **口径优先级**：法律协议原文 > 带日期的公告/发布记录 > 专页 > 正文表格 > 概述页宣称。裁决留痕见 `tests/ai-gateway-rulings-2026-09-21.md`"""

PAGES = {
    "W2-billing-and-sla.md": dict(
        out="aliyun-ai-gateway-billing.md",
        title="AI 网关 · §3 计费与商务（含 §3.9 SLA 与赔偿）",
        rule=("🔴 **对客纪律**：本页所有价格均为**官方文档快照时点口径**。Serverless 新版 6 项单价官方自称"
              "「参考单价」、专享实例规格单价被 2 处「以控制台/价格页/SLA 协议页面为准」推走、"
              "AI Credits 折算率**全库查无** → **任何数字不得直接作为对客承诺价，报价前必须走购买页核验**。"
              "不给单价的地域**禁止用内地价外推**。"),
    ),
    "W3-object-model-and-traffic.md": dict(
        out="aliyun-ai-gateway-traffic.md",
        title="AI 网关 · §4 核心对象模型 / §5 流量治理与成本控制",
        rule=("🔴 **对客纪律**：限流超限的 HTTP 状态码/响应体文档**未说明**（只有另一套 API 级策略写了默认 429，"
              "不可套用）；Token 计量口径的 7 个子问题全部空白；语义缓存无 TTL 配置项。"
              "客户问「限流了返回什么」「Token 怎么算」时，先答空白再给实测建议，不要拿邻近机制类推。"),
    ),
    "W4-auth-and-security.md": dict(
        out="aliyun-ai-gateway-auth.md",
        title="AI 网关 · §6 鉴权与消费者体系 / §7 AI 安全护栏与 RAM 权限",
        rule=("🔴 **对客纪律**：自建认证的「鉴权 API + 原始请求 Path 拼接」与「Path 需前缀匹配」是**设计行为不是 bug**，"
              "客户认证接口若为精确匹配必然 404，且 404 不在宽松模式（仅覆盖连接失败与 5xx）的兜底范围内 → "
              "**即使开了宽松模式也全量拒绝**。MCP 场景对客口径为「**仅支持 API Key**」，不得承诺 JWT。"
              "RAM 多租户隔离无法靠资源级授权实现（见 §7）。"),
    ),
    "W5-mcp-and-agent.md": dict(
        out="aliyun-ai-gateway-mcp-agent.md",
        title="AI 网关 · §8 MCP 与 Agent API 生态",
        rule=("🔴 **对客纪律**：`agent-api-observable` 官方 `.md` 通道返回**服务端截断**正文（978B，断在孤立 `*` 上，"
              "两次抓取 SHA256 一致），Agent API 完整指标清单**不可从文档取得**。"
              "语义检索/工具精选是否消耗 AI Credits **全页查无** → 报价必须另核。A2A 协议转换 21 页**零命中**，不得对客承诺。"),
    ),
    "W6-plugins.md": dict(
        out="aliyun-ai-gateway-plugins.md",
        title="AI 网关 · §9 插件体系",
        rule=("🔴 **对客纪律**：`ai-cue-template` 与 `ai-cue-decorator` 两个 slug 的**官方标题与正文插件名交叉错位**"
              "（裁决 C6）→ 给客户配置示例时**必须写插件名而非 slug**。"
              "`frontend-gray` 优先级存在 1000 / 450 两个官方数字（裁决 C7，未裁）→ 必须先实测再承诺。"
              "34 页对 AI Credits / 计费 / 免费 / 公测 **全部 0 命中** → 插件的成本影响一律「文档未说明」。"),
    ),
    "W7-observability-portal-recipes-openapi.md": dict(
        out="aliyun-ai-gateway-ops.md",
        title="AI 网关 · §10 可观测与运维 / §11 开发者门户与开放平台 / §12 实践教程与集成配方 / §13 OpenAPI 与 RAM 元信息",
        rule=("🔴 **对客纪律**：9 类资源配额在错误码页全是 `%s` 占位符 → 容量规划必须走配额中心/工单。"
              "140 个 Action 中 66 个（47.1%）无法资源级授权，MCP / AI 模型元信息 / 消费者组 / 插件四类对象"
              "**在 RAM 层面根本没有 ARN 定义** → 多租户只能分账号或分实例。"
              "`access-vertex-ai-through-ai-gateway` **不含**跨境网络要求（只有「VPC 须绑公网 NAT」），"
              "**不得据该页承诺跨境网络方案**。"),
    ),
}


def split_preamble(text: str):
    """返回 (导读行列表, 正文起始索引行列表)。剥 HTML 注释与 `# W*` 标题，保留 blockquote 导读。"""
    lines = text.splitlines()
    i = 0
    guide = []
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("<!--") or s.startswith("# W") or s == "---" or not s:
            i += 1
            continue
        if s.startswith("## §"):
            break
        if s.startswith(">"):
            guide.append(ln)
        i += 1
    return guide, lines[i:]


def main():
    made = []
    for src, meta in PAGES.items():
        text = (PARTIALS / src).read_text(encoding="utf-8")
        guide, body = split_preamble(text)
        head = ["# " + meta["title"], "", COMMON, ">", meta["rule"], ""]
        if guide:
            head += ["## 本章导读", ""] + guide + [""]
        out = "\n".join(head) + "\n" + "\n".join(body).rstrip() + "\n"
        p = KB / "knowledge" / meta["out"]
        p.write_text(out, encoding="utf-8")
        made.append((p.name, len(out.splitlines())))
        print("  ✅ %-42s %5d 行" % (p.name, len(out.splitlines())))

    # W1 交给主控手工装配主页（§0 + §1 + §2 + §14 + §15），此处只输出其正文供拼接
    w1 = (PARTIALS / "W1-product-and-capacity.md").read_text(encoding="utf-8")
    g1, b1 = split_preamble(w1)
    (Path("/tmp/aigw-partials/_W1-body.md")).write_text("\n".join(b1).rstrip() + "\n", encoding="utf-8")
    (Path("/tmp/aigw-partials/_W1-guide.md")).write_text("\n".join(g1) + "\n", encoding="utf-8")
    print("\n  W1 正文已抽出 → /tmp/aigw-partials/_W1-body.md（%d 行），待主控与 §0/§14/§15 拼成主页"
          % len(b1))
    print("\n装配完成：%d 个子页" % len(made))


if __name__ == "__main__":
    main()
