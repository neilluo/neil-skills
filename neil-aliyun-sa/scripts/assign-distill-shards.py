#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把已抓取的 AI 网关 raw 快照按主题指派给蒸馏 worker，并做**完备性门禁**：
每个「有正文」的快照必须被且只被一个 worker 指派，否则报错退出。

🔴 主控派工纪律（本项目已有教训）：契约条目须逐条映射到 worker，跨端交付物最容易掉缝。
   这里用集合运算强制证明「无遗漏、无重复」，不靠人眼扫。

用法：python3 scripts/assign-distill-shards.py
"""
import sys
from pathlib import Path

# 2026-09-24 双仓合并：原硬编码 /Users/neil/Desktop/neilskills/neil-aliyun-sa，改为按脚本自身定位知识库根
KB = Path(__file__).resolve().parent.parent
MANIFEST = KB / "tests/ai-gateway-fetch-manifest-2026-09-21.tsv"
OUTDIR = Path("/tmp/aigw-shards")

# slug -> worker。TOC 容器页与 FAIL-NOMD 页不指派（不作事实来源）。
ASSIGN = {
    "W1": [  # §1 产品定位与产品族 + §2 实例形态/容量/地域/引擎/实例与网络基础
        "what-is-an-ai-gateway", "product-comparison", "ai-gateway-capacity-description",
        "capacity-description", "supported-regions", "engine-version-description",
        "api-product-introduction", "create-a-gateway-instance", "view-gateway-instance-details",
        "modifying-gateway-parameter-configurations", "configure-dns-server",
        "set-security-group-rules", "setting-the-specified-https-cipher-suite",
        "create-a-domain-name", "delete-a-domain-name",
        "change-the-protocol-and-certificate-of-the-domain-name",
        "new-feature-release-notes-ai-gateway",
    ],
    "W2": [  # §3 计费与商务 + SLA
        "free-product-templates", "overview-of-billing-during-the-serverless-public-preview-of-the",
        "serverless-old-billing-details", "ai-credits-billing-details", "query-bills",
        "description-of-arrears", "refund", "ai-gateway-commercialization-announcement",
        "announcement-new-serverless-version-of-the-ai-gateway-now-in-public-beta",
        "service-level-agreement", "sla-agreement-fulltext-terms-alicdn",
    ],
    "W3": [  # §4 对象模型 + §5 流量治理
        "managing-the-model-api", "manage-the-ai-api", "route-list", "configure-smart-routing",
        "ai-fallback", "current-limiting", "configure-a-modelapi-throttling-policy",
        "model-metadata", "manage-providers", "creating-services", "manage-services",
        "manage-service-sources", "create-a-service-source", "configure-service-health-checks",
        "networked-search", "ai-cache-1", "more-policies-and-plugins",
        "create-an-api-product-of-the-model-api-type", "product-category-management",
        "consumer-quotas-management", "manage-global-authentication",
    ],
    "W4": [  # §6 鉴权与消费者体系 + §7 AI 安全护栏与 RAM
        "consumer-authentication-authentication", "consumer-authentication",
        "consumer-certification", "consumer-certification-1", "creating-a-consumer",
        "authorization-management", "deactivate-or-delete-a-consumer",
        "configure-self-built-authentication", "configure-jwt-authentication",
        "configure-oidc-authentication", "configure-oidc-login-for-portal",
        "create-secret-key", "edit-and-delete-secret-key", "reference-secret-key",
        "content-security-protection", "set-the-gateway-ip-whitelist-and-whitelist",
        "identity-management", "ai-gateway-system-permission-policy-reference",
        "custom-permission-policy-reference-for-ai-gateway",
        "service-association-role-provided-only-when-involved-otherwise-no-need",
    ],
    "W5": [  # §8 MCP 与 Agent 生态
        "mcp-service-management", "gateway-managed-mcp-services", "mcp-gateway-management",
        "http-to-mcp-field-configurations", "debug-mcp-services", "synchronizing-nacos-mcp-services",
        "mcp-tool-assembly", "mcp-grayscale-release", "semantic-retrieval", "tool-selection",
        "configure-policies-and-plugins-1", "mcp-server-product",
        "agent-management-access-and-observation", "manage-agent-apis", "routing-management",
        "configure-policies-and-plug-ins", "create-an-api-product-of-the-agent-api-type",
        "hichat-ai-interaction-center", "manage-ai-gateway-mcp-services-via-openapi",
        "agent-api-observable", "mcp-observable",
    ],
    "W6": [  # §10 插件体系（目录 + AI 增强 + 流量/安全/转换 + 自定义开发 + 性能）
        "manage-plug-ins", "upload-plug-in", "webide-writing-plug-ins", "plug-in-performance-reference",
        "develop-gateway-plug-ins-using-the-go-language",
        "developing-gateway-plug-ins-using-rust-and-c-languages", "ai-auxiliary-plug-in-development",
        "ai-cue-template", "ai-cue-decorator", "ai-rag", "ai-retrieval-agent",
        "ai-retrieval-augmented-generation-enhanced", "ai-request-response-intelligent-transformation",
        "degraphql-plugin", "custom-response-plugin", "request-block-plugin", "waf-plugin",
        "bot-detect-plug-ins", "basic-auth-plug-ins", "key-auth-plug-ins", "hmac-auth-plug-ins",
        "jwt-auth-plug-ins", "jwt-logout-plug-ins", "oauth-plugin", "key-rate-limit-plugin",
        "throttle-based-on-cluster-keys", "the-traffic-tag-plugin", "canary-header-plugin",
        "front-end-grayscale-plug-in", "geographic-location-of-ip", "hsts-plug-in",
        "http-real-ip-plug-ins", "browser-cache-control", "parameter-access-control",
    ],
    "W7": [  # §9 可观测与运维 + §11 门户/开放平台 + §12 实践教程 + §13 OpenAPI 元页
        "ai-observable", "configure-ai-log-policy", "enable-gateway-log-delivery",
        "enable-mcp-service-log-delivery", "enable-gateway-link-tracing",
        "view-gateway-monitoring-data", "request-response-capture-1", "label", "resource-group",
        "create-portal", "deployment-portal", "developer-guide",
        "access-vertex-ai-through-ai-gateway", "deepseek-integration-through-ai-gateway",
        "enable-llm-api-compression-to-save-bandwidth-costs",
        "migrate-the-official-claude-code-model-to-any-model-using-ai-gateway",
        "pai-deployment-model-access-ai-gateway", "proxy-comfyui-service-via-ai-gateway",
        "proxy-dify-inbound-and-outbound-traffic-through-ai-gateway",
        "api-apig-2024-03-27-overview-ai-gateway", "api-apig-2024-03-27-endpoint-ai-gateway",
        "api-apig-2024-03-27-ram-ai-gateway", "api-apig-2024-03-27-quota-ai-gateway",
        "api-apig-2024-03-27-errorcodes", "api-apig-2024-03-27-changeset-ai-gateway",
    ],
}


def main():
    rows = {}
    for ln in MANIFEST.read_text(encoding="utf-8").splitlines()[1:]:
        f = ln.split("\t")
        rows[f[0]] = f
    # 主控另存的 SLA 全文不在 manifest 里，手工补
    extra = {"sla-agreement-fulltext-terms-alicdn"}

    factbearing = {s for s, f in rows.items() if f[7] in ("OK", "OK-STUB")} | extra
    toc = {s for s, f in rows.items() if f[7] == "TOC"}
    nomd = {s for s, f in rows.items() if f[7].startswith("FAIL")}

    assigned = {}
    dupes = []
    for w, slugs in ASSIGN.items():
        for s in slugs:
            if s in assigned:
                dupes.append((s, assigned[s], w))
            assigned[s] = w

    missing = sorted(factbearing - set(assigned))
    unknown = sorted(set(assigned) - factbearing - toc - nomd)
    assigned_toc = sorted(set(assigned) & toc)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    for w, slugs in ASSIGN.items():
        lines = []
        for s in slugs:
            f = rows.get(s)
            title = f[3] if f else "AI网关服务等级协议·全文（terms.alicdn.com，主控补抓）"
            sec = f[2] if f else "服务支持"
            nbytes = f[6] if f else "?"
            p = KB / "raw/aliyun-docs/ai-gateway" / ("%s.md" % s)
            lines.append("%s\t%s\t%s\t%s\t%s" % (s, sec, title, nbytes, p))
        (OUTDIR / ("%s.tsv" % w)).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("有正文快照 %d ｜ TOC 容器 %d ｜ 无正文节点 %d" % (len(factbearing), len(toc), len(nomd)))
    print("已指派 %d（去重后 %d）" % (sum(len(v) for v in ASSIGN.values()), len(assigned)))
    for w in sorted(ASSIGN):
        print("  %s: %2d 页  %6.0f KB" % (
            w, len(ASSIGN[w]),
            sum(int(rows[s][6]) for s in ASSIGN[w] if s in rows) / 1024))
    ok = True
    if dupes:
        ok = False
        print("\n🔴 重复指派 %d 条：" % len(dupes))
        for s, a, b in dupes:
            print("   %s → %s 与 %s" % (s, a, b))
    if missing:
        ok = False
        print("\n🔴 未被任何 worker 指派的有正文快照 %d 条（会静默掉缝）：" % len(missing))
        for s in missing:
            print("   %s ｜ %s" % (s, rows[s][3] if s in rows else "(主控补抓)"))
    if unknown:
        ok = False
        print("\n🔴 指派了但 raw 里不存在的 slug %d 条：" % len(unknown))
        for s in unknown:
            print("   %s" % s)
    if assigned_toc:
        print("\n⚠️ 指派了 %d 个 TOC 容器页（不作事实来源，仅供目录结构）：%s"
              % (len(assigned_toc), ", ".join(assigned_toc)))
    if not ok:
        sys.exit(1)
    print("\n✅ 完备性门禁通过：无遗漏、无重复、无幽灵 slug → %s/W*.tsv" % OUTDIR)


if __name__ == "__main__":
    main()
