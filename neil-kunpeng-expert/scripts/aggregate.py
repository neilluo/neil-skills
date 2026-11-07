#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aggregate.py —— bills_raw.json → arch.json v2（neil-kunpeng-expert 归线聚合器）

产出契约：docs/arch_schema.md（v2，唯一事实源）。本脚本零第三方依赖，只用标准库。

用法：
    python3 scripts/aggregate.py --in bills_raw.json --out arch.json \
        --months-complete 202609,202610 \
        [--risks config/risks_kunqi.json] [--cross-links links.json] \
        [--rg-links rg_links.json]        # 兼容旧格式（可选）

归线顺序（arch_schema.md「归线/分块规则」节，规则 1 = v1 规则 1-4 全部保留）：
    1. 资源组直接命中（group → line）
    2. 无组标签行按序旁证归线：命名前缀/标签 project → VPC → SLS project → kind 兜底
    3. 月均成本只算 --months-complete 里的完整月；残缺月只进证据不进均值
    4. Supabase 池（spb-* / entercloud-pool / game_runtime）折叠成 enter.计算 的一个 COMP
    5. 风险清单来自 --risks，target 必须解析到真实 comp id，解析失败落 meta.warnings

v2 分块（相对 v1 的六层结构，见 arch_schema.md「分层哲学」）：
    * 顶层多出独立的 edge 带（{name, comps[], note}）：全球边缘与加速。
    * LINE.layers 三键（入口/计算/数据）：v1 的「消息」列（ons/alikafka 归本泳道者）
      并入「数据」；v1 的「AI」列在业务泳道无对应键，落到「计算」。
    * shared.layers 四键（入口/计算/数据/AI）；infra.layers 五键
      （核心库/消息流/分析同步/治理注册/容器网络，映射见 INFRA_COL_BY_KIND/BY_PIP）。
    * 观测剥离（规则 2）：kind ∈ {sls,prom,cms,arms,hdm} 的 COMP 不进列，
      改挂所属带的 observe[] 横条（id 用 <line>_obs_<slug>）。
    * edge 提取（规则 3）：无组标签且 kind ∈ {cdn,ga,waf,cbwp,cas}，
      或 kind=eip 且无组标签且昵称非 CREATE_BY_NLB → edge 带；
      有组标签 / CREATE_BY_NLB 的 EIP 留所属泳道（infra 无入口列 → 容器网络）。
    * line.cost_month 的口径与 v1 完全一致（按归线累加，观测/edge 剥离不改总额）；
      edge 带的成本只体现在其 comps[].cost 上（schema 的 edge 对象无 cost_month 键）。

折叠（渲染预算，见 MAX_COMPS_PER_LAYER / MAX_COMPS_PER_OBSERVE / MAX_COMPS_TOTAL）：
    账单是「逐实例 × 逐计费项」的明细，直接一行一卡会让 arch.json 爆出数百个 COMP，
    渲染必然重叠溢出。聚合器因此分两级收敛：
      A. 语义折叠 —— 按产品维度把同质行并成一张卡（FOLD_* 规则表）：
         fc       → 函数族（prod-coding-agent / *-sbx- / prod-cv2 …），evidence「族名 ×N 函数」
         ecs      → 规格族|地域|chargeType(|addc)，evidence 列 sample 昵称≤3 + 台数
         sls      → SLS project，evidence 写 logstore 数与 top3 名字
         ons/kafka→ 实例 id，evidence 写计费项数
         eip/cdt  → 按归属带一张卡（无组标签默认 infra，除非 tag project 指向某线）
         gpdb     → Supabase 池 / 记忆库池各一张，gp- 集群仍逐实例
         acs      → 单池
         其余高基数 kind（nlb/clb/dts/arms/nas…）→ 每 (line,kind,layer) 一张「舰队卡」
         rds/redis/mongo/adbpg/oss/kafka/… 等低基数有名字的实例仍逐实例出卡
      B. 预算折叠 —— 每列 COMP ≤ MAX_COMPS_PER_LAYER、observe 横条 ≤ MAX_COMPS_PER_OBSERVE、
         全图 ≤ MAX_COMPS_TOTAL；超出的列按 cost 升序把长尾并进一张「其他 ×N」卡
         （cost 求和，note 留痕）。阈值全部沿用 v1（observe 的 8 条上限见规则 6）。
    COMP id = <band>_<col-slug>_<fold-slug>，col-slug ∈ access|compute|data|ai|core|msg|
    ana|gov|net|edge，observe 内为 <band>_obs_<slug>（确定性；折叠粒度变了 id 就变，
    config/cross_links_kunqi.json 与 config/risks_kunqi.json 的 target 必须跟着对齐）。

契约备注（与 arch_schema.md 的已知偏差，均在 meta.warnings 留痕或此处记录）：
    * attribution 枚举在 schema 里是 resource_group|naming|vpc|sls 四值，但归线规则 2.d
      是「按 kind 定」的兜底，无法用四值表达 —— 本脚本输出第五值 "kind"。
    * color 调色板缺 anycap 键，沿用既有图（kunqi-links-v2.html）的画法映射到 "work"。
    * 规则 2 的 observe 集合写了 kind=hdm，但 COMP kind 词表里没有 hdm（pipCode hdm
      在 v1 就解析成 kind=other）—— 本脚本按 pipCode 识别 hdm 并剥离到 observe，
      comp id 沿用 fleet slug（<line>_obs_other-hdm）。
    * 规则 5 把「记忆池」列进 shared.数据、又把 kind=memory 列进 shared.AI（同一对象）。
      本脚本按更具体的「记忆池→数据」实现（与 v1 及 cross_links 的 shared_data_memory-pool
      一致）；bailian/model_ext 仍进 AI。
    * 规则 3 说「有组标签的 EIP 留所属泳道入口列」，但 infra 五列没有入口列 ——
      infra 的网络类（eip/nat/ntr/privatelink/pvtz/slb/vpc/cdt）统一落「容器网络」。
    * edge 带在 schema 里没有 id 字段，其 comps 的 id 用 <line>=edge、<col>=edge 两段常量
      拼成 edge_edge_<slug>，保证与泳道 id 空间不冲突。
    * DEFAULT_VPC_RULES / DEFAULT_SLS_RULES / DEFAULT_NAMING_RULES / DEFAULT_FC_FAMILY_RULES
      里的具体串是坤启（Converge AI）账号实测值，换客户须用 payload.meta.rules 或 --rules 覆盖。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

SCHEMA_VERSION = "v2"

# ---------------------------------------------------------------------------
# 常量表（可被 payload.meta.rules / --rules 覆盖）
# ---------------------------------------------------------------------------

# v1 语义层（六键）：只作 kind/pip → 语义层的中间态，v2 再按块映射到列/observe/edge。
LAYER_ORDER = ["接入", "计算", "数据", "消息", "AI", "观测"]
LINE_ORDER = ["enter", "framia", "game", "concat", "work", "anycap"]
SPECIAL_LINES = ["shared", "infra"]

# --- v2 分块（arch_schema.md「LINE / SHARED / INFRA」节）-------------------
LINE_COLUMNS = ["入口", "计算", "数据"]                     # 业务泳道三列
SHARED_COLUMNS = ["入口", "计算", "数据", "AI"]             # 平台共享层四列
INFRA_COLUMNS = ["核心库", "消息流", "分析同步", "治理注册", "容器网络"]  # 基础设施五列
OBSERVE = "observe"          # observe[] 横条（伪列，不进 layers）
EDGE_BAND = "edge"           # 顶层 edge 带（伪泳道）
EDGE_NAME = "全球边缘与加速"
EDGE_NOTE = ("CDN / GA+CDT / WAF / 共享带宽 / 证书与无标签 EIP 池："
             "全球边缘与出口加速面，不归属单一业务泳道（arch_schema.md 规则 3）")

BLOCK_COLUMNS = {
    "line": LINE_COLUMNS,
    "shared": SHARED_COLUMNS,
    "infra": INFRA_COLUMNS,
    EDGE_BAND: [EDGE_BAND],
}

# 列 → comp id 中缀（arch_schema.md 规则 7）
COL_SLUG = {
    "入口": "access", "计算": "compute", "数据": "data", "AI": "ai",
    "核心库": "core", "消息流": "msg", "分析同步": "ana",
    "治理注册": "gov", "容器网络": "net",
    OBSERVE: "obs", EDGE_BAND: "edge",
}

# v1 语义层 → v2 列（业务泳道 / 共享层）。观测类先被剥离，
# 剩下的 v1「观测」长尾（dms/aidbs/nacos/sentry…）按块默认列兜底。
LINE_COL_BY_LAYER = {
    "接入": "入口", "计算": "计算", "数据": "数据",
    "消息": "数据",      # 规则：消息类 COMP 并入「数据」列（渲染列标题「数据 / 消息」）
    "AI": "计算",        # 业务泳道无 AI 列（AI 面统一在 shared）
    "观测": "数据",
}
SHARED_COL_BY_LAYER = {
    "接入": "入口", "计算": "计算", "数据": "数据",
    "消息": "数据", "AI": "AI", "观测": "数据",
}

# infra 列映射（arch_schema.md 规则 4）：kind 优先，其次 pipCode，最后默认容器网络
INFRA_COL_BY_KIND = {
    "rds": "核心库", "redis": "核心库", "tair": "核心库", "mongo": "核心库",
    "kafka": "消息流", "rocketmq": "消息流",
    "adbpg": "分析同步", "dts": "分析同步", "maxcompute": "分析同步",
    "clickhouse": "分析同步", "es": "分析同步",
    "ack": "容器网络", "nlb": "容器网络", "clb": "容器网络", "eip": "容器网络",
    "nas": "容器网络", "nas_ext": "容器网络", "oss": "容器网络",
    "nacos": "治理注册",
}
INFRA_COL_BY_PIP = {
    "eventbridge": "消息流",
    "dide": "分析同步",
    "mse": "治理注册", "dms": "治理注册", "hbr": "治理注册", "aidbs": "治理注册",
    "ecoa": "治理注册", "cas": "治理注册",
    "ecs": "容器网络", "disk": "容器网络", "nat": "容器网络", "ntr": "容器网络",
    "privatelink": "容器网络", "pvtz": "容器网络", "vpc": "容器网络",
    "slb": "容器网络", "csk": "容器网络", "cdt": "容器网络", "cbwp": "容器网络",
    "agentbay": "容器网络", "imm": "容器网络", "nls": "容器网络",
    "lvwang": "容器网络",
}
INFRA_COL_DEFAULT = "容器网络"

# 观测剥离（arch_schema.md 规则 2）：kind ∈ {sls,prom,cms,arms,hdm}
OBSERVE_KINDS = {"sls", "prom", "cms", "arms", "hdm"}
# kind 词表无 hdm（pipCode hdm → kind other），按 pipCode 补识别；xtrace 已映射成 arms
OBSERVE_PIPS = {"hdm"}

# edge 提取（arch_schema.md 规则 3）
EDGE_KINDS = {"cdn", "ga", "waf", "cbwp", "cas"}
EDGE_PIPS = {"cbwp", "cas"}          # 这两个 pipCode 的 kind 是 other
CREATE_BY_NLB_RE = re.compile(r"CREATE_BY_NLB", re.I)
# infra 规则 4：ecs(ADDC) → 治理注册，其余 ecs → 容器网络
ADDC_HINT_RE = re.compile(r"ADDC|域控|Active\s*Directory", re.I)

# arch_schema.md 调色板键：enter|framia|game|concat|work|platform|infra
COLOR_MAP = {
    "enter": "enter",
    "framia": "framia",
    "game": "game",
    "concat": "concat",
    "work": "work",
    "anycap": "work",      # 调色板无 anycap，沿用既有图着色
    "shared": "platform",
    "infra": "infra",
}

DEFAULT_LINE_NAMES = {
    "enter": "Enter Pro（生应用/网页）",
    "framia": "Framia Pro（生视频）",
    "game": "Combos Fun（游戏 · Boo Agent）",
    "concat": "Concat Pro（增长）",
    "work": "Covey / Work（办公）",
    "anycap": "anycap（未披露业务线）",
    "shared": "平台共享层（统一入口 + context/记忆）",
    "infra": "基础设施 kntech（账本/消息/分析/治理）",
}

DEFAULT_GROUP_TO_LINE = {
    "enter-prod": "enter",
    "framia-prod": "framia",
    "game-prod": "game",
    "concat-prod": "concat",
    "work-prod": "work",
    "workhub-prod": "work",
    "anycap-prod": "anycap",
    "converge-prod": "shared",
    "infra-prod": "infra",
}

# 归线规则 2.a 命名前缀（正则按序命中，先到先得）
DEFAULT_NAMING_RULES = [
    (r"(?:^|[-/])(?:prod|dev)-coding-agent", "enter"),
    (r"(?:^|[-/])(?:prod|dev)-sbx", "enter"),
    (r"-sbx-", "enter"),
    (r"nlb-(?:enter|coding)", "enter"),
    (r"(?:^|[-/])(?:prod|dev)-video-agent", "framia"),
    (r"(?:^|[-/])(?:prod|dev)-cv2", "framia"),
    (r"framia-gateway", "framia"),
    (r"(?:^|[-/])(?:prod|dev)-game-pmd", "game"),
    (r"(?:^|[-/])game(?:gatewayrouter|kolagent|larkmgr|-rec|-credit)", "game"),
    (r"combos-report", "game"),
    (r"concat-(?:apigateway|business-service)", "concat"),
    (r"workhub", "work"),
    (r"anycap", "anycap"),
    (r"converge-(?:agent|ug)", "shared"),
    (r"(?:^|[-/])(?:kntech|credit|pubfree|sandbox|test-account|addc)", "infra"),
]

# 标签 key:project value:X → line（归入「命名/标签」这一档旁证）
DEFAULT_TAG_PROJECT_TO_LINE = {
    "enter": "enter",
    "coding": "enter",
    "framia": "framia",
    "video": "framia",
    "game": "game",
    "concat": "concat",
    "work": "work",
    "covey": "work",
    "workhub": "work",
    "anycap": "anycap",
    "converge": "shared",
    "platform": "shared",
    "infra": "infra",
    "kntech": "infra",
}

# 归线规则 2.b VPC 前缀（实测截断串，前缀匹配）
DEFAULT_VPC_RULES = [
    ("vpc-t4nq2wm4", "enter"),
    ("vpc-t4nu70bsp3", "game"),
    ("vpc-t4nrb7m45s", "shared"),
    ("vpc-t4n4tqdvjg9j", "infra"),
]

# 归线规则 2.c SLS project → line
DEFAULT_SLS_RULES = [
    ("enter", "enter"),
    ("coding-prod", "enter"),
    ("framia-prod", "framia"),
    ("combos-report", "game"),
    ("concat-prod", "concat"),
    ("converge-agent", "shared"),
]

# 归线规则 2.d kind 兜底：模型类 → shared（AI 层），出口/骨干 → infra
KIND_FALLBACK_LINE = {
    "bailian": "shared",
    "model_ext": "shared",
    "memory": "shared",
    "oss": "shared",
    "nas": "shared",
    "nas_ext": "shared",
    "cdn": "infra",
    "ga": "infra",
    "eip": "infra",
    "waf": "infra",
    "nlb": "infra",
    "clb": "infra",
    "apigw": "shared",
    "fc": "shared",
    "acs": "shared",
    "ack": "infra",
    "sae": "shared",
    "supabase": "enter",
    "sls": "shared",
    "prom": "infra",
    "cms": "infra",
    "arms": "infra",
    "nacos": "infra",
    "sentry": "infra",
    "dts": "infra",
    "maxcompute": "infra",
    "kafka": "infra",
    "rocketmq": "infra",
}
KIND_FALLBACK_DEFAULT = "infra"

KIND_TO_LAYER = {
    "nlb": "接入", "clb": "接入", "apigw": "接入", "eip": "接入", "cdn": "接入",
    "ga": "接入", "waf": "接入",
    "fc": "计算", "acs": "计算", "ack": "计算", "sae": "计算", "supabase": "计算",
    "rds": "数据", "redis": "数据", "tair": "数据", "mongo": "数据", "es": "数据",
    "clickhouse": "数据", "adbpg": "数据", "oss": "数据", "nas": "数据",
    "nas_ext": "数据", "memory": "数据", "dts": "数据", "maxcompute": "数据",
    "kafka": "消息", "rocketmq": "消息",
    "bailian": "AI", "model_ext": "AI",
    "sls": "观测", "prom": "观测", "cms": "观测", "arms": "观测", "nacos": "观测",
    "sentry": "观测",
}

# kind=other 时按 pipCode 定层
OTHER_LAYER_BY_PIP = {
    "ecs": "计算", "agentbay": "计算", "edas": "计算",
    "disk": "数据", "dide": "数据", "hbr": "数据", "ots": "数据", "polardb": "数据",
    "ads": "数据", "opensearch": "数据", "imm": "数据",
    "nat": "接入", "ntr": "接入", "cbwp": "接入", "cdt": "接入", "privatelink": "接入",
    "pvtz": "接入", "cas": "接入", "vpc": "接入",
    "hdm": "观测", "dms": "观测", "aidbs": "观测", "cbs": "观测", "xtrace": "观测",
    "eventbridge": "消息", "mse": "观测",
}
OTHER_LAYER_DEFAULT = "数据"

# pipCode → kind（arch_schema.md kind 词表）
PIP_TO_KIND = {
    "ecs": "other", "disk": "other", "eip": "eip", "slb": "nlb", "nat": "other",
    "ntr": "other", "cbwp": "other", "cdt": "other", "vpc": "other",
    "privatelink": "other", "pvtz": "other", "cas": "other",
    "cdn": "cdn", "ga": "ga", "waf": "waf", "apigateway": "apigw",
    "fc": "fc", "acs": "acs", "csk": "ack", "ack": "ack", "sae": "sae", "edas": "other",
    "rds": "rds", "polardb": "other", "kvstore": "redis", "mongodb": "mongo",
    "elasticsearch": "es", "clickhouse": "clickhouse", "gpdb": "adbpg", "ads": "other",
    "ots": "other", "hitsdb": "other",
    "oss": "oss", "nas": "nas", "hbr": "other",
    "alikafka": "kafka", "ons": "rocketmq", "eventbridge": "other", "dts": "dts",
    "odps": "maxcompute", "dide": "other", "opensearch": "other",
    "sfm": "bailian", "YUNMARKET_THIRD_PARTY": "model_ext", "yunmarket_third_party": "model_ext",
    "agentbay": "other", "imm": "other", "nls": "other", "alimt": "other",
    "ecoa": "other", "lvwang": "other",
    "cms": "prom", "arms": "arms", "xtrace": "arms", "sls": "sls", "cbs": "other",
    "mse": "nacos", "hdm": "other", "dms": "other", "aidbs": "other",
}

# 商品名（commodityName）细粒度覆盖，按序命中
COMMODITY_KIND_RULES = [
    (r"Tair|tair", "tair"),
    (r"传统型负载均衡|CLB", "clb"),
    (r"应用型负载均衡|ALB", "other"),
    (r"网络型负载均衡|NLB", "nlb"),
    (r"极速型\s*NAS", "nas_ext"),
    (r"Prometheus", "prom"),
    (r"企业云监控|云监控", "cms"),
    (r"SchedulerX|任务调度", "other"),
    (r"Nacos|微服务引擎", "nacos"),
    (r"容器服务|Kubernetes|ACK|Argo", "ack"),
    (r"云沙箱|AgentBay|沙箱", "other"),
    (r"万相|Happy|百炼", "bailian"),
    (r"Sentry", "sentry"),
]

# gpdb（ADBPG）内部再分型：Supabase 池 / Agent 记忆 / 普通 ADBPG
SUPABASE_HINT = re.compile(r"spb-|entercloud-pool|entercloud_pool|game_runtime|supabase", re.I)
MEMORY_HINT = re.compile(r"^sas-|^agdb-|上下文|长记忆|记忆", re.I)

VPC_RE = re.compile(r"vpc-[0-9a-z]{6,}")
SLS_ID_RE = re.compile(r"^([A-Za-z0-9][\w\-]{2,});")
TAG_PROJECT_RE = re.compile(r"key:\s*project\s+value:\s*([^;\s]+)", re.I)
ZERO_GROUP_RE = re.compile(r"^\s*(default\s*resource\s*group|默认资源组|)\s*$", re.I)
HASH_TOKEN_RE = re.compile(r"^(?=.*\d)(?=.*[a-f])[0-9a-f]{10,}$")  # 纯 hex 尾部 hash 段
ACS_POOL_FAMILY = "acs-pod-pool"
GPDB_POOL_FAMILY = "supabase-pool"
MEMORY_POOL_FAMILY = "memory-pool"
MAX_SAT_FAMILIES = 40          # 单个饱和产品最多铺多少张族卡，超出合并成「其它」卡

# ---------------------------------------------------------------------------
# 渲染预算（折叠阈值的唯一出处；docs/arch_schema.md 只认 arch.json，不认这些数字）
# ---------------------------------------------------------------------------
MAX_COMPS_PER_LAYER = 12       # 单列（band × column）最多几张卡（沿用 v1）
MAX_COMPS_PER_OBSERVE = 8      # observe 横条上限：>8 条折「其他 ×N」（arch_schema.md 规则 6）
MAX_COMPS_TOTAL = 120          # 全图 COMP 总数上限（含 edge 带与 observe 横条）
MIN_LAYER_KEEP = 3             # 全局预算收紧时每列至少保留几张卡
MISC_SLUG = "misc"             # 长尾合并卡的 slug（「其他 ×N」）

# 出口带宽类产品（EIP / CDT 跨境 / 共享带宽）：逐 EIP 行折成每线一张卡
EGRESS_PIPS = ("eip", "cdt", "cbwp")

# 有名字、低基数、图上要单独看的实例：仍逐实例出卡（受 MAX_COMPS_PER_LAYER 兜底）
PER_INSTANCE_KINDS = {
    "rds", "redis", "tair", "mongo", "es", "clickhouse", "adbpg",
    "kafka", "rocketmq", "apigw", "cdn", "ga", "waf", "sae", "ack",
}

# 折叠模式（决定 name/evidence/note 的写法）
MODE_INSTANCE = "instance"     # 逐实例
MODE_FAMILY = "family"         # FC 函数族
MODE_SPEC = "spec"             # ECS 规格族|地域|chargeType
MODE_PROJECT = "project"       # SLS project
MODE_BILLING = "billing"       # ons/kafka 逐计费项 → 实例 id
MODE_EGRESS = "egress"         # eip/cdt 逐 EIP → 归属带一张卡
MODE_FLEET = "fleet"           # 同质基础设施舰队（nlb/clb/dts/arms/disk…）
MODE_POOL = "pool"             # 池（acs/supabase/memory/bailian）
MODE_EDGE = "edge"             # edge 带产品卡（cdn/ga/waf/cas/cbwp）：按 kind 一张

# edge 带产品卡的展示名（v2 顶层 edge 带）
EDGE_LABEL = {
    "cdn": "CDN 边缘分发", "ga": "全球加速 GA", "waf": "WAF 应用防火墙",
    "cas": "证书服务", "cbwp": "共享带宽", "cdt": "跨境流量 CDT",
    "eip": "无标签 EIP 池", "other": None,
}

# 池化 kind：每 (line, layer) 一张卡
POOL_KINDS = {"acs": "ACS Pod 池", "supabase": "Supabase 池",
              "memory": "记忆库池", "bailian": "百炼工作空间"}

# 舰队卡的展示名（kind → 中文标签）
FLEET_LABEL = {
    "nlb": "NLB", "clb": "CLB", "eip": "公网出口", "dts": "DTS 同步链路",
    "arms": "ARMS/链路追踪", "prom": "Prometheus", "cms": "云监控",
    "nacos": "MSE Nacos", "sentry": "Sentry", "nas": "NAS", "nas_ext": "极速 NAS",
    "oss": "OSS", "sls": "SLS", "model_ext": "三方模型直供", "other": None,
}

# pip=other 时的中文标签（fleet 卡名用）
OTHER_LABEL_BY_PIP = {
    "disk": "云盘/快照", "agentbay": "AgentBay 沙箱", "edas": "EDAS",
    "dide": "DataWorks", "hbr": "混合云备份", "ots": "表格存储",
    "polardb": "PolarDB", "ads": "ADS", "opensearch": "OpenSearch",
    "imm": "智能媒体管理", "nat": "NAT 网关", "ntr": "转发路由器 TR",
    "cbwp": "共享带宽", "cdt": "跨境流量 CDT", "privatelink": "PrivateLink",
    "pvtz": "PrivateZone", "cas": "证书服务", "vpc": "VPC",
    "hdm": "DAS/SQL洞察", "dms": "DMS", "aidbs": "DBS 备份", "cbs": "CBS",
    "xtrace": "链路追踪", "eventbridge": "EventBridge", "mse": "MSE",
    "ecs": "ECS", "slb": "负载均衡", "sfm": "百炼", "nls": "智能语音",
    "alimt": "机器翻译", "ecoa": "企业认证", "lvwang": "内容安全",
    "YUNMARKET_THIRD_PARTY": "云市场三方", "yunmarket_third_party": "云市场三方",
}

# FC 函数族（归线规则 2.a 的同前缀族；按序命中，先到先得）
DEFAULT_FC_FAMILY_RULES = [
    (r"(?:^|[-/])prod-coding-agent", "prod-coding-agent"),
    (r"(?:^|[-/])dev-coding-agent", "dev-coding-agent"),
    (r"(?:^|[-/])prod-sbx", "prod-sbx"),
    (r"(?:^|[-/])dev-sbx", "dev-sbx"),
    (r"-sbx-", "sbx"),
    (r"(?:^|[-/])prod-video-agent", "prod-video-agent"),
    (r"(?:^|[-/])dev-video-agent", "dev-video-agent"),
    (r"(?:^|[-/])prod-cv2", "prod-cv2"),
    (r"(?:^|[-/])dev-cv2", "dev-cv2"),
    (r"(?:^|[-/])prod-game-pmd", "prod-game-pmd"),
    (r"(?:^|[-/])dev-game-pmd", "dev-game-pmd"),
    (r"prod-prod-wagt", "prod-prod-wagt"),
    (r"(?:^|[-/])(?:prod|dev)-work-runtime", "work-runtime"),
    (r"(?:^|[-/])(?:prod|dev)-game-(?:gateway|kolagent|larkmgr|rec|credit)", "game-service"),
    (r"(?:^|[-/])(?:prod|dev)-concat", "concat-service"),
]
# 纯 uuid 函数名（无业务前缀）统一归到这一族
FC_UUID_FAMILY = "uuid-service"
UUID_NAME_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}", re.I
)
FC_FAMILY_RULES = [(re.compile(p), fam) for p, fam in DEFAULT_FC_FAMILY_RULES]

# slb（NLB/CLB/ALB）舰队卡的两个子维度
SLB_NET_RE = re.compile(r"(?:实例网络类型|实例类型)[:：]\s*(公网|私网)")
SLB_BANDWIDTH_RE = re.compile(r"带宽峰值[:：]\s*(\d+)\s*Kbps")
SLB_ROLE_RULES = [
    (re.compile(r"gateway|router|apigateway|-gw-|网关", re.I), "gateway"),
    (re.compile(r"CreatedBySAE", re.I), "sae"),
    (re.compile(r"ManagedK8SSlb|k8s-|Kubernetes", re.I), "k8s"),
]
SLB_ROLE_LABEL = {
    "gateway": "网关", "sae": "SAE 托管", "k8s": "K8s 托管",
    "app": "业务命名", "anon": "无命名",
}
# ECS 规格族：优先 allocation 的「实例规格族」，否则取 instanceSpec 前两段
ECS_SPEC_FAMILY_RE = re.compile(r"实例规格族[:：]\s*([A-Za-z0-9\.\-_]+)")
REGION_RE = re.compile(r"地域[:：]\s*([^;]+)")
# SLS instanceId：uid;project;logstore;region
SLS_PARTS_RE = re.compile(r"^(\d+);([^;]+);([^;]*)(?:;([^;]*))?$")
# 百炼 instanceId：uid;ws-xxx;model;spec
BAILIAN_WS_RE = re.compile(r"(?:^|;)((?:ws|llm)-[0-9a-z]+)(?:;|$)", re.I)

# arch_schema.md 归线规则 4：Supabase 池 evidence 要写池计数（spb×44+game×2）
SUPABASE_SUBPOOL_RULES = [
    (re.compile(r"^spb-", re.I), "spb"),
    (re.compile(r"entercloud[-_]pool", re.I), "entercloud-pool"),
    (re.compile(r"game[-_]runtime", re.I), "game_runtime"),
]

# Agent 记忆库（gpdb 的 sas-/agdb- 前缀）子池计数
MEMORY_SUBPOOL_RULES = [
    (re.compile(r"^sas-", re.I), "sas"),
    (re.compile(r"^agdb-", re.I), "agdb"),
]


def supabase_subpool(root):
    """从 Supabase 池根名识别子池标签（arch_schema.md 归线规则 4）。"""
    for regex, label in SUPABASE_SUBPOOL_RULES:
        if regex.search(_s(root)):
            return label
    return "other"


def memory_subpool(root):
    """从记忆库根名识别子池标签（sas- 长期记忆 / agdb- Agent 记忆）。"""
    for regex, label in MEMORY_SUBPOOL_RULES:
        if regex.search(_s(root)):
            return label
    return "other"

# 饱和抽样产品的展示名
SAT_LABEL = {
    "fc": "FC 函数",
    "gpdb": "ADBPG",
    "acs": "ACS Pod",
    "ecs": "ECS",
    "sae": "SAE 应用",
}

DEFAULT_SUMMARY_FLOW = [
    "全球用户",
    "边缘加速 CDN/GA/WAF",
    "业务层 入口→计算→数据",
    "平台共享层 APIGW/context/模型路由",
    "基础设施 数据/消息/治理",
]


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------

def _s(value):
    """安全转字符串（None → ''）。"""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _num(value):
    """安全转 float；不可解析返回 0.0。"""
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _money(total, months):
    """完整月均值（元，整数）。months 为空或无金额 → None。"""
    if not months:
        return None
    return int(round(total / float(len(months))))


def _most_common(counter):
    if not counter:
        return None
    return counter.most_common(1)[0][0]


def row_key(row):
    """账单行去重键：优先服务端 hashKey，缺失时用业务字段复合键。

    group_rows（按资源组分片）与 instance_rows（按 pipCode 分片）会覆盖同一批账单行，
    聚合前必须去重，否则金额翻倍。
    """
    hk = row.get("hashKey")
    if hk:
        return "hk:%s" % hk
    return "ck:%s|%s|%s|%s|%s|%s" % (
        _s(row.get("month")),
        _s(row.get("pipCode")),
        _s(row.get("instanceId")),
        _s(row.get("resName")) or _s(row.get("commodityName")),
        _s(row.get("chargeType")),
        "%.4f" % _num(row.get("requireAmount")),
    )


def norm_group(name):
    """资源组名归一化；default resource group / 空 → None（视为无组标签）。"""
    raw = _s(name).strip()
    if not raw or ZERO_GROUP_RE.match(raw):
        return None
    return raw


def extract_vpc(row):
    """从 instanceAllocation（配置串）等字段里提 VPC id。"""
    for field in ("instanceAllocation", "instanceId", "instanceTag", "instanceNick"):
        m = VPC_RE.search(_s(row.get(field)))
        if m:
            return m.group(0)
    return None


def extract_tag_project(row):
    m = TAG_PROJECT_RE.search(_s(row.get("instanceTag")))
    if not m:
        return None
    return m.group(1).strip().lower()


def instance_root(row):
    """实例根：instanceId 的分号前段（地域/计费维度后缀去掉）。"""
    iid = _s(row.get("instanceId"))
    if not iid:
        return ""
    return iid.split(";")[0].strip()


def _fold_hash_suffix(root):
    """按 - / _ . 切段，从尾部丢弃纯 hex hash 段（≥10 位、含数字与 a-f），保留业务前缀。

      prod-coding-agent-6a06cd33defb4-e565a12481ef463bb3ae19edb4919b3d → prod-coding-agent
      dev-sbx-KkkB9R641nyjY3vx-f3687bf449b645228bc7b21d9790a65a         → dev-sbx-KkkB9R641nyjY3vx
    没有可丢弃段时返回原根。
    """
    if not root:
        return ""
    parts = re.split(r"([-/_\.])", root)
    tokens = []
    i = 0
    while i < len(parts):
        tok = parts[i]
        sep = parts[i + 1] if i + 1 < len(parts) else ""
        if tok:
            tokens.append((tok, sep))
        i += 2
    while len(tokens) > 1 and HASH_TOKEN_RE.match(tokens[-1][0]):
        tokens.pop()
    out = "".join(tok + sep for tok, sep in tokens)
    return out.rstrip("-/_.") or root


def family_of(root, pip=None):
    """把实例根折叠成「族」前缀，供饱和抽样产品做基数收敛（每族一个 COMP）。

    产品定制（references/kunpeng-apis.md 坑 4）：
      fc   → 函数名去尾部 hash（业务前缀，如 prod-coding-agent）
      acs  → 16 字符 Pod id 无语义 → 全部折叠成单池 acs-pod-pool
      gpdb → Supabase 池（spb-/entercloud-pool/game_runtime）折叠成 supabase-pool；
             记忆库（sas-/agdb-）折叠成 memory-pool；
             其余（gp- 集群）各自成族（实例数本就不多）
      其它 → 去尾部 hex hash 段
    """
    if not root:
        return ""
    pip = _s(pip).lower()
    if pip == "acs":
        return ACS_POOL_FAMILY
    if pip == "gpdb" and SUPABASE_HINT.search(root):
        return GPDB_POOL_FAMILY
    if pip == "gpdb" and MEMORY_HINT.search(root):
        return MEMORY_POOL_FAMILY
    if pip == "gpdb":
        return root            # gp- 集群 id 即族，不再折叠
    return _fold_hash_suffix(root)


# ---------------------------------------------------------------------------
# 折叠（fold）：把「逐实例 × 逐计费项」的账单明细收敛成图上能看的 COMP 粒度
# ---------------------------------------------------------------------------

FC_FUNCTION_RE = re.compile(r"functions/([^;]+)")


def fc_function_name(row):
    """FC 行的函数名：instanceId 可能是 `acs:fc:<region>:<uid>:functions/<name>;<region>`
    或裸函数名/服务 uuid。"""
    iid = _s(row.get("instanceId")) or _s(row.get("id"))
    m = FC_FUNCTION_RE.search(iid)
    if m:
        return m.group(1).strip()
    root = instance_root(row)
    if root:
        return root
    return _s(row.get("instanceNick")) or _s(row.get("commodityName")) or "unknown"


def fc_family(name, rules=None):
    """函数名 → 函数族（同前缀族折成一张卡）。幂等：族名再喂进来还是它自己。"""
    name = _s(name).strip()
    if not name:
        return "unknown"
    for regex, fam in (rules if rules is not None else FC_FAMILY_RULES):
        if regex.search(name):
            return fam
    if UUID_NAME_RE.match(name):
        return FC_UUID_FAMILY
    return _fold_hash_suffix(name) or name


def sls_parts(row):
    """SLS instanceId 拆成 (uid, project, logstore, region)。

    实测两种形态：`1077748325118640;enter;codeapigateway;ap-southeast-1`（uid 打头）
    与 `framia-prod;video-render`（project 打头，fixture/旧存档）。
    """
    iid = _s(row.get("instanceId")) or _s(row.get("id")) or instance_root(row)
    segs = [s.strip() for s in iid.split(";")]
    if segs and segs[0].isdigit() and len(segs[0]) >= 10:
        uid = segs[0]
        project = segs[1] if len(segs) > 1 else ""
        logstore = segs[2] if len(segs) > 2 else ""
        region = segs[3] if len(segs) > 3 else ""
    else:
        uid = ""
        project = segs[0] if segs else ""
        logstore = segs[1] if len(segs) > 1 else ""
        region = segs[2] if len(segs) > 2 else ""
    return uid, project or "unknown", logstore, region


def ecs_spec_family(row):
    """ECS 规格族：优先 allocation 的「实例规格族」，否则取 instanceSpec 前两段。"""
    alloc = _s(row.get("instanceAllocation")) or _s(row.get("al"))
    m = ECS_SPEC_FAMILY_RE.search(alloc)
    if m:
        return m.group(1).strip()
    spec = _s(row.get("instanceSpec")) or _s(row.get("sp"))
    if spec:
        bits = [b for b in spec.split(".") if b]
        return ".".join(bits[:2]) if len(bits) >= 2 else spec
    return "unknown"


def ecs_region(row):
    blob = "%s %s" % (
        _s(row.get("instanceAllocation")) or _s(row.get("al")),
        _s(row.get("region")) or _s(row.get("reg")),
    )
    m = REGION_RE.search(blob)
    if m:
        return m.group(1).strip()
    reg = _s(row.get("region")) or _s(row.get("reg"))
    return reg.strip() or "unknown"


def slb_role(row):
    """负载均衡在图上的语义角色：网关 / SAE 托管 / K8s 托管 / 业务命名 / 无命名。"""
    nick = _s(row.get("instanceNick")) or _s(row.get("nk"))
    alloc = _s(row.get("instanceAllocation")) or _s(row.get("al"))
    blob = "%s %s" % (nick, alloc)
    for regex, role in SLB_ROLE_RULES:
        if regex.search(blob):
            return role
    return "app" if nick else "anon"


def slb_subtype(row, kind):
    """NLB / CLB / ALB（kind 词表无 alb，归到 nlb 卡但按子类型分组）。"""
    com = _s(row.get("commodityName")) or _s(row.get("com"))
    iid = _s(row.get("instanceId")) or ""
    if kind == "clb" or iid.startswith("lb-") or "传统型" in com:
        return "clb"
    if iid.startswith("alb-") or "应用型" in com or "ALB" in com:
        return "alb"
    return "nlb"


def slb_network(row):
    alloc = _s(row.get("instanceAllocation")) or _s(row.get("al"))
    m = SLB_NET_RE.search(alloc)
    if m:
        return m.group(1)
    return "私网"


SLB_NET_CODE = {"公网": "pub", "私网": "pri"}
SLB_NET_LABEL = {v: k for k, v in SLB_NET_CODE.items()}


def egress_bandwidth_kbps(row):
    alloc = _s(row.get("instanceAllocation")) or _s(row.get("al"))
    m = SLB_BANDWIDTH_RE.search(alloc)
    return int(m.group(1)) if m else 0


def fmt_bandwidth(kbps):
    if not kbps:
        return "未标峰值"
    if kbps >= 1024:
        v = kbps / 1024.0
        return "%dM" % round(v) if abs(v - round(v)) < 0.05 else "%.1fM" % v
    return "%dK" % kbps


def bailian_ws(row):
    """百炼行的工作空间 id（instanceId 形如 `<uid>;ws-xxx;<model>;<spec>;;0`）。"""
    iid = _s(row.get("instanceId")) or _s(row.get("id"))
    m = BAILIAN_WS_RE.search(iid)
    if m:
        return m.group(1).lower()
    root = instance_root(row)
    return root or "unknown"


def pool_slug(kind, root):
    if kind == "bailian":
        return "ws"
    if kind == "supabase" or SUPABASE_HINT.search(_s(root)):
        return GPDB_POOL_FAMILY
    if kind == "memory" or MEMORY_HINT.search(_s(root)):
        return MEMORY_POOL_FAMILY
    if kind == "acs":
        return ACS_POOL_FAMILY
    return "pool"


def fleet_slug(kind, pip):
    """同质基础设施舰队的分组 slug（kind=other 时按 pip 细分，避免糊成一张无意义卡）。"""
    if kind == "other":
        return "other-%s" % (_s(pip).lower() or "unknown")
    return kind


def slugify(text, limit=28):
    """comp id 用的确定性 slug：小写、只留 [a-z0-9_-]、截断。"""
    out = re.sub(r"[^a-z0-9_\-]+", "-", _s(text).lower()).strip("-")
    out = re.sub(r"-{2,}", "-", out)
    if not out:
        return ""
    return out[:limit].rstrip("-")


def fold_of(row, kind, pip):
    """一行账单 → (折叠模式, 分组 slug)。同 (band, kind, layer, mode, slug) 的行合成一张卡。

    折叠粒度见文件头「折叠」节；这里只负责分组键，展示字段在 _build_comp 里按 mode 生成。
    """
    pip = _s(pip).lower()
    root = instance_root(row)
    if is_edge_row(row, kind, pip):
        # edge 带：每个边缘产品一张卡（cdn/ga/waf/cas/cbwp/cdt/无标签 eip），
        # 不按实例 id 铺开（CDN 的 instanceId 是 uid;区域，铺开只会得到 8 张同义卡）
        return MODE_EDGE, (kind if kind != "other" else "other-%s" % (pip or "unknown"))
    if pip in EGRESS_PIPS or kind == "eip":
        # EIP / CDT / 共享带宽：逐 EIP 行折成「归属带」一张卡
        return MODE_EGRESS, "egress"
    if pip == "fc" or kind == "fc":
        return MODE_FAMILY, fc_family(fc_function_name(row))
    if pip == "ecs":
        # ADDC（Windows AD 域控）单独成组：arch_schema.md 规则 4 把它映射到「治理注册」，
        # 与同规格族的普通 ECS（容器网络）混在一张卡里会让列归属含糊
        spec = "%s|%s|%s" % (
            ecs_spec_family(row), ecs_region(row),
            _s(row.get("chargeType")) or _s(row.get("ct")) or "postpay",
        )
        if is_addc(row):
            spec += "|addc"
        return MODE_SPEC, spec
    if pip == "sls" or kind == "sls":
        return MODE_PROJECT, sls_parts(row)[1]
    if pip in ("ons", "alikafka") or kind in ("rocketmq", "kafka"):
        return MODE_BILLING, root or "instance"
    if kind in POOL_KINDS:
        return MODE_POOL, pool_slug(kind, root)
    if kind in PER_INSTANCE_KINDS:
        return MODE_INSTANCE, root or fc_function_name(row)
    if pip == "slb" or kind in ("nlb", "clb"):
        sub = slb_subtype(row, kind)
        net = SLB_NET_CODE.get(slb_network(row), "pri")
        return MODE_FLEET, "%s-%s-%s" % (sub, net, slb_role(row))
    return MODE_FLEET, fleet_slug(kind, pip)
def member_of(row, mode, pip, kind):
    """折叠组内的「成员」身份，用来算 ×N 与取 sample。"""
    pip = _s(pip).lower()
    if mode == MODE_FAMILY:
        return fc_function_name(row)
    if mode == MODE_PROJECT:
        return sls_parts(row)[2] or sls_parts(row)[1]
    if mode == MODE_BILLING:
        return _s(row.get("instanceId")) or instance_root(row)
    if kind == "bailian":
        return bailian_ws(row)          # 一个 ws 算一个成员（计费项行不算）
    return instance_root(row) or fc_function_name(row)


def fold_label(kind, pip, slug):
    """折叠卡的中文标签（name 用）。"""
    if kind == "other":
        base = OTHER_LABEL_BY_PIP.get(_s(pip)) or OTHER_LABEL_BY_PIP.get(_s(pip).lower())
        return base or _s(pip).upper() or "其它"
    if kind in POOL_KINDS:
        return POOL_KINDS[kind]
    if kind in ("nlb", "clb"):
        sub, net, role = (slug.split("-") + ["", "", ""])[:3]
        return "%s %s %s" % (sub.upper(), net, SLB_ROLE_LABEL.get(role, role))
    return _s(kind).upper()



# ---------------------------------------------------------------------------
# kind / layer
# ---------------------------------------------------------------------------

def resolve_kind(row):
    """按 pipCode + commodityName + 实例串解析 arch_schema.md 的 kind 词表值。"""
    pip = _s(row.get("pipCode")) or _s(row.get("pip"))
    com = _s(row.get("commodityName")) or _s(row.get("com"))
    ident = "%s %s %s" % (
        instance_root(row),
        _s(row.get("instanceNick")) or _s(row.get("nk")),
        com,
    )

    if pip == "gpdb":
        if SUPABASE_HINT.search(ident):
            return "supabase"
        if MEMORY_HINT.search(ident):
            return "memory"
        return "adbpg"

    # eip/sls 必须先于商品名规则：EIP 的昵称常是 CREATE_BY_NLB.nlb-xxx，
    # 会被「网络型负载均衡|NLB」误判成 nlb（实测 enter 的 3 个 EIP 全被吃掉）。
    if pip == "eip":
        return "eip"
    if pip == "sls":
        return "sls"

    # slb：group_rows 的 commodityName 常为空（legacy_import），靠实例 id 前缀分子类型
    if pip == "slb":
        iid = _s(row.get("instanceId")) or ""
        if iid.startswith("lb-") or "传统型" in com or "CLB" in com:
            return "clb"
        if iid.startswith("alb-") or "应用型" in com or "ALB" in com:
            return "nlb"          # kind 词表无 alb，ALB 归 nlb（同属 L4/L7 负载均衡）
        return "nlb"

    kind = PIP_TO_KIND.get(pip)
    for pattern, mapped in COMMODITY_KIND_RULES:
        if re.search(pattern, com) or re.search(pattern, ident):
            kind = mapped
            break
    if kind is None:
        kind = "other"
    return kind


def resolve_layer(kind, row):
    """v1 语义层（六键）。v2 只把它当中间态：折叠分组 + 列映射的输入。"""
    if kind in KIND_TO_LAYER:
        return KIND_TO_LAYER[kind]
    pip = _s(row.get("pipCode")) or _s(row.get("pip"))
    return OTHER_LAYER_BY_PIP.get(pip, OTHER_LAYER_DEFAULT)


# ---------------------------------------------------------------------------
# v2 分块：edge 提取 / 观测剥离 / 列映射（arch_schema.md 规则 2-4）
# ---------------------------------------------------------------------------

def has_group_tag(row):
    """有组标签？default resource group / 空 → 无（norm_group 同语义）。"""
    return norm_group(row.get("resourceGroupName") or row.get("rg")) is not None


def is_create_by_nlb(row):
    """EIP 昵称/配置串里的 CREATE_BY_NLB.nlb-xxx（NLB 自动申请的 EIP，跟 NLB 同泳道）。"""
    blob = "%s %s %s" % (
        _s(row.get("instanceNick")) or _s(row.get("nk")),
        _s(row.get("instanceId")) or _s(row.get("id")),
        _s(row.get("instanceAllocation")) or _s(row.get("al")),
    )
    return bool(CREATE_BY_NLB_RE.search(blob))


def is_edge_row(row, kind, pip):
    """arch_schema.md 规则 3：edge 带提取。

    无组标签 且（kind ∈ {cdn,ga,waf,cbwp,cas} 或 kind=eip 且非 CREATE_BY_NLB）→ edge；
    有组标签 / CREATE_BY_NLB 的 EIP 留在所属泳道（infra 无入口列 → 容器网络）。
    """
    pip = _s(pip).lower()
    if has_group_tag(row):
        return False
    if kind in EDGE_KINDS or pip in EDGE_PIPS:
        return True
    if kind == "eip" or pip == "eip":
        return not is_create_by_nlb(row)
    return False


def is_observe(kind, pip):
    """arch_schema.md 规则 2：观测类剥离到 observe[] 横条。

    kind ∈ {sls,prom,cms,arms,hdm}；kind 词表无 hdm（pipCode hdm → kind other），
    故 hdm 只能按 pipCode 认（见文件头「契约备注」）。
    """
    return kind in OBSERVE_KINDS or _s(pip).lower() in OBSERVE_PIPS


def is_addc(row):
    """Windows AD 域控 ECS（arch_schema.md 规则 4：ecs(ADDC) → 治理注册）。"""
    blob = "%s %s %s" % (
        _s(row.get("instanceNick")) or _s(row.get("nk")),
        instance_root(row),
        _s(row.get("instanceAllocation")) or _s(row.get("al")),
    )
    return bool(ADDC_HINT_RE.search(blob))


def infra_column(kind, pip, rows):
    """arch_schema.md 规则 4：infra 组内五列映射。"""
    pip = _s(pip).lower()
    if pip == "ecs" and rows:
        n_addc = sum(1 for r in rows if is_addc(r))
        return "治理注册" if n_addc * 2 > len(rows) else "容器网络"
    col = INFRA_COL_BY_KIND.get(kind)
    if col:
        return col
    return INFRA_COL_BY_PIP.get(pip) or INFRA_COL_DEFAULT


def column_of(band, kind, layer, pip, rows):
    """(band, kind, v1语义层, pip) → v2 列名 / observe / edge。"""
    if band == EDGE_BAND:
        return EDGE_BAND
    if is_observe(kind, pip):
        return OBSERVE
    if band == "infra":
        return infra_column(kind, pip, rows)
    if band == "shared":
        return SHARED_COL_BY_LAYER.get(layer, "数据")
    return LINE_COL_BY_LAYER.get(layer, "数据")


# 列的确定性排序（comp id 编号与预算折叠都用它；observe/edge 排最后）
COLUMN_ORDER = (LINE_COLUMNS + [c for c in SHARED_COLUMNS if c not in LINE_COLUMNS]
                + INFRA_COLUMNS + [OBSERVE, EDGE_BAND])


def column_rank(col):
    return COLUMN_ORDER.index(col) if col in COLUMN_ORDER else len(COLUMN_ORDER)


def _all_bands(arch):
    """arch → 所有带对象（lines + shared + infra，edge 单独处理，因为它没有 risks 键）。"""
    out = list(arch.get("lines") or [])
    for key in ("shared", "infra"):
        if arch.get(key):
            out.append(arch[key])
    return out


def _band_by_id(arch, band_id):
    for band in _all_bands(arch):
        if band.get("id") == band_id:
            return band
    return None


def _retarget_edge_risk(arch, risk, comp):
    """edge 带命中的风险改挂到基础设施带（arch_schema.md 的 edge 对象无 risks 键）。

    优先改指 infra 容器网络列里的同类出口卡（eip/cbwp/cdt/nat），语义最贴近；
    没有同类卡时保留 edge comp id 挂到 infra（target 仍能解析到真实 comp，只是不在同带）。
    """
    infra = _band_by_id(arch, "infra") or _band_by_id(arch, "shared")
    if infra is None:
        return EDGE_BAND, comp
    want = comp.get("kind")
    for comps in (infra.get("layers") or {}).values():
        for cand in comps:
            if cand.get("kind") == want:
                return infra["id"], cand
    return infra["id"], comp


# ---------------------------------------------------------------------------
# 归线
# ---------------------------------------------------------------------------

class Rules(object):
    """归线规则集合（默认值 = 坤启实测；可被 payload.meta.rules / --rules 覆盖）。"""

    def __init__(self, overrides=None):
        overrides = overrides or {}
        self.group_to_line = dict(DEFAULT_GROUP_TO_LINE)
        self.group_to_line.update(overrides.get("group_to_line") or {})
        self.naming_rules = [
            (re.compile(p), line)
            for p, line in (overrides.get("naming_rules") or DEFAULT_NAMING_RULES)
        ]
        self.tag_project_to_line = dict(DEFAULT_TAG_PROJECT_TO_LINE)
        self.tag_project_to_line.update(overrides.get("tag_project_to_line") or {})
        self.vpc_rules = list(overrides.get("vpc_rules") or DEFAULT_VPC_RULES)
        self.sls_rules = list(overrides.get("sls_rules") or DEFAULT_SLS_RULES)
        self.fc_family_rules = [
            (re.compile(p), fam)
            for p, fam in (overrides.get("fc_family_rules") or DEFAULT_FC_FAMILY_RULES)
        ]
        self.egress_default_line = overrides.get("egress_default_line", "infra")
        self.kind_fallback_line = dict(KIND_FALLBACK_LINE)
        self.kind_fallback_line.update(overrides.get("kind_fallback_line") or {})
        self.kind_fallback_default = overrides.get(
            "kind_fallback_default", KIND_FALLBACK_DEFAULT
        )
        self.line_names = dict(DEFAULT_LINE_NAMES)
        self.line_names.update(overrides.get("line_names") or {})

    # -- 单条规则 ----------------------------------------------------------
    def by_group(self, row):
        group = norm_group(row.get("resourceGroupName") or row.get("rg"))
        if not group:
            return None, None
        line = self.group_to_line.get(group)
        if not line:
            # 未登记的资源组：去掉 -prod/-dev 后缀再试一次，仍不认就落到 shared
            base = re.sub(r"-(prod|dev|test)$", "", group)
            line = self.group_to_line.get(base + "-prod") or "shared"
        return line, group

    def by_naming(self, row):
        blob = " ".join([
            _s(row.get("instanceNick")) or _s(row.get("nk")),
            instance_root(row),
            _s(row.get("instanceId")) or _s(row.get("id")),
            _s(row.get("resourceGroupName")) or _s(row.get("rg")),
        ])
        for regex, line in self.naming_rules:
            if regex.search(blob):
                return line
        project = extract_tag_project(row)
        if project and project in self.tag_project_to_line:
            return self.tag_project_to_line[project]
        return None

    def by_vpc(self, row):
        vpc = extract_vpc(row)
        if not vpc:
            return None
        for prefix, line in self.vpc_rules:
            if vpc.startswith(prefix):
                return line
        return None

    def by_sls(self, row):
        pip = _s(row.get("pipCode")) or _s(row.get("pip"))
        root = instance_root(row)
        if not root:
            return None
        project = root
        if pip == "sls":
            m = SLS_ID_RE.match(root)
            project = m.group(1) if m else root
        else:
            # 非 sls 行只有在命名里显式带 project 名时才走这条旁证
            if pip != "sls" and not any(p in root for p, _ in self.sls_rules):
                return None
        for name, line in self.sls_rules:
            if project == name or project.startswith(name):
                return line
        return None

    def by_kind(self, kind):
        return self.kind_fallback_line.get(kind, self.kind_fallback_default)

    def by_tag_project(self, row):
        """只看 instanceTag 的 key:project value:X（归线规则 2.a 的「标签 project」档）。"""
        project = extract_tag_project(row)
        if not project:
            return None
        return self.tag_project_to_line.get(project)

    def attribute(self, row, kind, pip=None):
        """返回 (line, method, group)；method ∈ resource_group|naming|vpc|sls|kind。"""
        line, group = self.by_group(row)
        if line:
            return line, "resource_group", group
        # 出口带宽类（EIP/CDT/共享带宽）无组标签时默认归 infra.接入，
        # 除非 instanceTag 的 project 明确指向某条产品线（arch_schema.md 归线规则 2.d）。
        if _s(pip).lower() in EGRESS_PIPS or kind == "eip":
            tagged = self.by_tag_project(row)
            if tagged:
                return tagged, "naming", None
            return self.egress_default_line, "kind", None
        line = self.by_naming(row)
        if line:
            return line, "naming", None
        line = self.by_vpc(row)
        if line:
            return line, "vpc", None
        line = self.by_sls(row)
        if line:
            return line, "sls", None
        return self.by_kind(kind), "kind", None


METHOD_LABEL = {"naming": "命名", "vpc": "VPC", "sls": "SLS", "kind": "kind"}


# ---------------------------------------------------------------------------
# 输入装载
# ---------------------------------------------------------------------------

def load_raw(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_legacy_rg_links(path):
    """把旧格式 rg_links.json（{groups:{<组>:[{p,id,nk,sp,m:{month:金额},al,tg}]}}）
    摊平成 group_rows，便于复用既有存档。返回 (rows, warnings)。"""
    rows, warnings = [], []
    try:
        data = load_raw(path)
    except (OSError, ValueError) as exc:
        return rows, ["rg_links 读取失败：%s" % exc]
    groups = data.get("groups") if isinstance(data, dict) else None
    if not isinstance(groups, dict):
        return rows, ["rg_links 无 groups 字段，已忽略"]
    for group, entries in groups.items():
        if not isinstance(entries, list):
            continue
        for idx, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            months = entry.get("m") or {}
            for month, amount in months.items():
                rows.append({
                    "month": _s(month),
                    "pipCode": _s(entry.get("p")),
                    "tableType": "INSTANCE_CONSUME_MONTH",
                    "instanceId": _s(entry.get("id")),
                    "instanceNick": entry.get("nk"),
                    "instanceSpec": entry.get("sp"),
                    "instanceAllocation": _s(entry.get("al")),
                    "instanceTag": _s(entry.get("tg")),
                    "resourceGroupName": group,
                    "requireAmount": _num(amount),
                    "chargeType": _s(entry.get("ct")),
                    "hashKey": "legacy:%s:%s:%s" % (group, idx, month),
                    "_legacy": True,
                })
    aux = data.get("aux") if isinstance(data, dict) else None
    if isinstance(aux, dict) and aux.get("logstores"):
        warnings.append("rg_links.aux.logstores 未并入（SLS 证据以 group_rows 为准）")
    return rows, warnings


def collect_rows(raw, legacy_rows=None):
    """合并 instance_rows + group_rows（+ 旧格式），按 row_key 去重。"""
    seen = {}
    order = []
    warnings = []
    buckets = [
        ("instance_rows", raw.get("instance_rows") or []),
        ("group_rows", raw.get("group_rows") or []),
    ]
    if legacy_rows:
        buckets.append(("rg_links(legacy)", legacy_rows))
    for name, rows in buckets:
        if not isinstance(rows, list):
            warnings.append("%s 不是数组，已跳过" % name)
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            key = row_key(row)
            if key in seen:
                continue
            seen[key] = row
            order.append(key)
    return [seen[k] for k in order], warnings


# ---------------------------------------------------------------------------
# 聚合主体
# ---------------------------------------------------------------------------

class Aggregator(object):
    def __init__(self, raw, months_complete, rules, saturation_products=None):
        self.raw = raw if isinstance(raw, dict) else {}
        self.rules = rules
        self.warnings = []
        meta = self.raw.get("meta") or {}
        self.raw_meta = meta
        self.months_all = [
            _s(m) for m in (meta.get("months") or []) if _s(m)
        ]
        self.months_complete = list(months_complete or [])
        if not self.months_complete:
            self.months_complete = [
                _s(m) for m in (meta.get("months_complete") or self.months_all)
            ]
        partial = [m for m in self.months_all if m not in self.months_complete]
        if partial:
            self.warnings.append(
                "残缺月 %s 只进证据不进月均（arch_schema.md 归线规则 3）" % ",".join(partial)
            )
        cfg = meta.get("config") or {}
        self.saturation_products = set(
            saturation_products
            or cfg.get("saturation")
            or meta.get("saturation")
            or []
        )
        # line → 归线方法与证据
        self.line_methods = defaultdict(Counter)     # line -> Counter(method)
        self.line_groups = defaultdict(Counter)      # line -> Counter(group)
        self.line_vpcs = defaultdict(Counter)        # line -> Counter(vpc)
        self.line_cost = defaultdict(float)          # line -> 完整月金额合计（v1 口径不变）
        self.comp_rows = defaultdict(list)           # (band,kind,layer,mode,slug) -> rows
        self.comp_cost = defaultdict(float)
        self.comp_meta = {}                          # key -> {pip, mode, slug, ...}
        self.comp_saturation = {}                    # key -> {pipCode, family, count, converged}
        self.row_pips = set()                        # 行级证据出现过的 pipCode
        self.edge_cost = 0.0                         # edge 带完整月金额（只作对账，不进 line 总额）
        self.saturation_families = defaultdict(lambda: {
            "roots": set(), "families": Counter(), "root_count": 0, "pages": 0,
            "months": set(), "converged": True, "sample": None, "region": Counter(),
            "subpools": defaultdict(Counter),   # family -> Counter(subpool)
        })
        self.product_totals = defaultdict(float)     # month -> 产品级金额合计
        self.product_by_pip = defaultdict(lambda: defaultdict(float))  # pip -> month -> amount
        self.row_totals = defaultdict(float)         # month -> 行级金额合计
        self.unattributed = defaultdict(float)       # month -> 无行级证据的产品金额

    # -- 主流程 ------------------------------------------------------------
    def run(self, rows):
        for row in rows:
            self._consume(row)
        self._consume_saturation()
        self._consume_products()

    def _consume(self, row):
        month = _s(row.get("month"))
        amount = _num(row.get("requireAmount"))
        pip = _s(row.get("pipCode")) or _s(row.get("pip"))
        if pip:
            self.row_pips.add(pip)
        if month:
            self.row_totals[month] += amount
        kind = resolve_kind(row)

        # 归线规则 4：Supabase 池统一折叠到 enter.计算
        if kind == "supabase":
            line, method, group = "enter", "naming", None
        else:
            line, method, group = self.rules.attribute(row, kind, pip)

        if month in self.months_complete:
            self.line_cost[line] += amount
        self.line_methods[line][method] += 1
        if group:
            self.line_groups[line][group] += 1
        vpc = extract_vpc(row)
        if vpc:
            self.line_vpcs[line][vpc] += 1

        # 归线结果决定成本与泳道归属；edge 提取只改「画在哪一带」（成本口径不变，
        # 所以 line.cost_month 与 v1 完全一致 —— arch_schema.md 规则 3）
        band = EDGE_BAND if is_edge_row(row, kind, pip) else line
        if band == EDGE_BAND and month in self.months_complete:
            self.edge_cost += amount

        layer = resolve_layer(kind, row)
        mode, slug = fold_of(row, kind, pip)
        key = (band, kind, layer, mode, slug)
        self.comp_rows[key].append(row)
        self.comp_meta.setdefault(key, {"pip": pip, "mode": mode, "slug": slug})
        if month in self.months_complete:
            self.comp_cost[key] += amount

    def _evidence(self, row, kind, pip):
        """单行证据（逐实例卡与旧调用面用）；折叠卡的证据由 _fold_evidence 生成。"""
        root = instance_root(row)
        if pip == "sls" or kind == "sls":
            # SLS 证据保留 project;logstore 全串（arch_schema.md COMP.evidence 示例）
            return _s(row.get("instanceId")) or _s(row.get("id")) or root
        if root:
            return root
        return (
            _s(row.get("instanceNick"))
            or _s(row.get("commodityName"))
            or _s(row.get("resName"))
            or "unknown"
        )

    def _consume_saturation(self):
        """饱和抽样产品（fc/gpdb/acs…）：根折叠成族，族基数进 COMP.note，金额不可拆分 → cost=null。

        payload.saturation 形如：[{pipCode, month, pages, rootCount, converged, roots:[...]}, ...]
        roots 元素可为字符串（根名）或 dict（{root/instanceId, region, commodityName, ...}）。
        族名优先用 fetch_bills.js 给的 family（权威），否则本地 family_of 兜底折叠；
        分组键与 _consume 完全一致（line/kind/layer/mode/slug），所以抽样根与真实账单行
        会并进同一张卡，不会重复出卡。
        """
        blocks = self.raw.get("saturation") or []
        if isinstance(blocks, dict):
            blocks = [dict(b, pipCode=k) for k, b in blocks.items()]
        for block in blocks:
            if not isinstance(block, dict):
                continue
            pip = _s(block.get("pipCode"))
            if not pip:
                continue
            month = _s(block.get("month"))
            roots = block.get("roots") or []
            if isinstance(roots, dict):
                roots = list(roots.values())
            fam = self.saturation_families[pip]
            if month:
                fam["months"].add(month)
            fam["pages"] = max(fam["pages"], int(block.get("pages") or 0))
            fam["root_count"] = max(
                fam["root_count"], int(block.get("rootCount") or len(roots))
            )
            if block.get("converged") is False:
                fam["converged"] = False
            for root in roots:
                if isinstance(root, str):
                    name, region, sample, fam_hint = root, None, None, None
                elif isinstance(root, dict):
                    name = _s(root.get("root") or root.get("instanceId") or root.get("id"))
                    region = _s(root.get("region")) or _s(root.get("reg")) or None
                    fam_hint = _s(root.get("family")) or None
                    sample = root
                else:
                    continue
                if not name:
                    continue
                fam["roots"].add(name)
                fam_name = fam_hint or family_of(name, pip)
                fam["families"][fam_name] += 1
                if fam_name == GPDB_POOL_FAMILY:
                    fam["subpools"][fam_name][supabase_subpool(name)] += 1
                if region:
                    fam["region"][region] += 1
                if sample is not None and fam["sample"] is None:
                    fam["sample"] = sample

        # 每个抽样根按 fold_of 归到折叠组；组内累计根数/子池计数，金额为 null（不可拆分）
        for pip, fam in self.saturation_families.items():
            sample = fam["sample"] or {}
            region = _most_common(fam["region"])
            for root in sorted(fam["roots"]):
                pseudo = {
                    "pipCode": pip,
                    "instanceId": self._sat_instance_id(pip, root),
                    "instanceNick": None,
                    "commodityName": _s(sample.get("commodityName")) or _s(sample.get("com")),
                    "instanceAllocation": _s(sample.get("instanceAllocation")) or _s(sample.get("al")),
                    "instanceTag": _s(sample.get("instanceTag")) or _s(sample.get("tg")),
                    "resourceGroupName": None,
                    "region": region,
                }
                kind = resolve_kind(pseudo)
                if kind == "supabase":
                    line, method = "enter", "naming"   # 归线规则 4：Supabase 池归 enter.计算
                else:
                    line = (self.rules.by_naming(pseudo) or self.rules.by_vpc(pseudo)
                            or self.rules.by_kind(kind))
                    method = ("naming" if self.rules.by_naming(pseudo)
                              else "vpc" if self.rules.by_vpc(pseudo) else "kind")
                self.line_methods[line][method] += 1
                band = EDGE_BAND if is_edge_row(pseudo, kind, pip) else line
                layer = resolve_layer(kind, pseudo)
                mode, slug = fold_of(pseudo, kind, pip)
                if pip == "fc":
                    # fc 的族名是唯一分组依据（fetch_bills.js 的 family 与本地规则同义）
                    mode = MODE_FAMILY
                    slug = fc_family(root, self.rules.fc_family_rules)
                key = (band, kind, layer, mode, slug)
                self.comp_meta.setdefault(key, {"pip": pip, "mode": mode, "slug": slug})
                self.comp_rows[key].append(dict(pseudo, _saturation=pip))
                info = self.comp_saturation.setdefault(key, {
                    "pipCode": pip, "family": slug, "count": 0,
                    "converged": fam["converged"], "subpools": Counter(),
                })
                info["count"] += 1
                if not fam["converged"]:
                    info["converged"] = False
                if kind == "supabase":
                    info["subpools"][supabase_subpool(root)] += 1
            self._check_sat_families(pip, fam)

    def _check_sat_families(self, pip, fam):
        """饱和抽样收敛情况留痕（族数上限 / 未收敛）。"""
        n_groups = len({
            k for k in self.comp_saturation if self.comp_saturation[k].get("pipCode") == pip
        })
        if n_groups > MAX_SAT_FAMILIES:
            self.warnings.append(
                "饱和抽样 %s 折叠后仍有 %d 组（上限 %d），超出部分由层内长尾合并兜底"
                % (pip, n_groups, MAX_SAT_FAMILIES)
            )
        if not fam["converged"]:
            self.warnings.append(
                "饱和抽样 %s 未收敛（12 页上限内仍有新根），根数为下界" % pip
            )

    @staticmethod
    def _sat_instance_id(pip, root):
        """抽样根 → 伪 instanceId。FC 根是函数名，需还原成 ARN 才能被 fold_of 认出来。"""
        if pip == "fc" and "/" not in root and ":" not in root:
            return "acs:fc:ap-southeast-1:0:functions/%s" % root
        return root

    def _consume_products(self):
        """产品级行（PRODUCT_CONSUME_MONTH）：对账 + 无实例维度产品补 COMP。

        sae/prometheus/cbs/xtrace 等 INSTANCE 查询 total=0，只能在此以产品级取证，
        按 kind 兜底归入 shared/infra，cost = 该产品完整月月均。
        """
        rows = self.raw.get("product_rows") or []
        if not isinstance(rows, list):
            self.warnings.append("product_rows 不是数组，已跳过")
            return
        pip_names = defaultdict(Counter)
        for row in rows:
            if not isinstance(row, dict):
                continue
            month = _s(row.get("month"))
            amount = _num(row.get("requireAmount"))
            table = _s(row.get("tableType"))
            pip = _s(row.get("pipCode")) or _s(row.get("pip")) \
                or _s(row.get("productCode"))
            com = _s(row.get("commodityName")) or _s(row.get("com"))
            if table == "ACCOUNT_CONSUME_MONTH":
                continue  # 账号级合计不参与产品级对账，避免重复计
            if month:
                self.product_totals[month] += amount
            if pip:
                self.product_by_pip[pip][month] += amount
                if com:
                    pip_names[pip][com] += 1

        # 无实例级证据的产品 → 产品级 COMP（金额可取月均，evidence 写 pipCode）
        for pip, by_month in self.product_by_pip.items():
            if pip in self.row_pips or pip in self.saturation_families:
                continue
            pseudo = {
                "pipCode": pip,
                "instanceId": "",
                "instanceNick": "",
                "commodityName": _most_common(pip_names.get(pip) or Counter()) or pip,
                "resourceGroupName": None,
            }
            kind = resolve_kind(pseudo)
            line = self.rules.by_kind(kind)
            self.line_methods[line]["kind"] += 1
            band = EDGE_BAND if is_edge_row(pseudo, kind, pip) else line
            layer = resolve_layer(kind, pseudo)
            key = (band, kind, layer, MODE_INSTANCE, "product-%s" % pip)
            complete_sum = sum(
                v for m, v in by_month.items() if m in self.months_complete
            )
            cost = _money(complete_sum, self.months_complete)
            self.line_cost[line] += complete_sum   # 产品级旁证也计入线月均（v1 口径不变）
            if band == EDGE_BAND:
                self.edge_cost += complete_sum
            self.comp_rows[key].append(
                dict(pseudo, _product_only=True, _product_cost=cost,
                     _product_months=sorted(m for m in by_month if m))
            )

        # 对账：产品级合计 vs 行级合计，缺口 > 2% 记为未归因
        for month, total in self.product_totals.items():
            gap = total - self.row_totals.get(month, 0.0)
            if gap > max(1.0, total * 0.02):
                self.unattributed[month] += gap

    # -- 输出 --------------------------------------------------------------
    def build(self, risks=None, cross_links=None):
        """折叠组 → arch.json v2。

        band（带）∈ {edge, enter, framia, …, shared, infra}：edge 是 v2 新增的顶层带，
        其余沿用 v1 的泳道概念；每个 band 内再按 v2 列（入口/计算/数据 | 四键 | 五键）
        与 observe[] 横条排布。
        """
        comps_by_band = defaultdict(list)
        for key, rows in self.comp_rows.items():
            band, kind, layer, mode, slug = key
            comps_by_band[band].append(
                self._build_comp(band, kind, layer, mode, slug, rows)
            )
        # comp id 必须在长尾折叠之前分配：id 只由 (band, 列, 族slug) 决定，
        # 这样折掉长尾也不会让留下来的卡改 id（cross_links/risks 的 target 才稳）。
        self._assign_ids(comps_by_band)
        # 被 risks / cross_links 引用的卡钉住，不进「其他 ×N」长尾
        self._pin_referenced(comps_by_band, risks, cross_links)
        self._enforce_budget(comps_by_band)

        bands = {}
        for band in self._all_bands(comps_by_band):
            bands[band] = self._build_band(band, comps_by_band.get(band, []))

        payload_lines = [bands[l] for l in LINE_ORDER if l in bands]
        shared = bands.get("shared")
        infra = bands.get("infra")
        edge = bands.get(EDGE_BAND) or {
            "name": EDGE_NAME, "comps": [], "note": EDGE_NOTE,
        }

        months = list(self.months_complete)
        meta = {
            "customer": _s(self.raw_meta.get("customer")) or None,
            "brand": _s(self.raw_meta.get("brand")) or None,
            "cid": _s(self.raw_meta.get("cid")) or None,
            "uid": _s(self.raw_meta.get("uid")) or None,
            "account": _s(self.raw_meta.get("account")) or None,
            "months": months,
            "months_complete": months,
            "months_all": list(self.months_all) or months,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources": list(self.raw_meta.get("sources") or ["bills_raw.json"]),
            "schema_version": SCHEMA_VERSION,
            "edge_cost_month": _money(self.edge_cost, self.months_complete),
            "cost_coverage": self._cost_coverage(),
            "unattributed_cost": {
                m: int(round(v)) for m, v in sorted(self.unattributed.items()) if v
            },
            "saturation": {
                pip: {
                    "root_count": fam["root_count"],
                    "distinct_roots": len(fam["roots"]),
                    "families": len(fam["families"]),
                    "pages": fam["pages"],
                    "converged": fam["converged"],
                    "months": sorted(m for m in fam["months"] if m),
                }
                for pip, fam in sorted(self.saturation_families.items())
            },
            "fetch_failures": list(self.raw.get("failures") or []),
            "warnings": list(self.warnings),
        }
        meta = {k: v for k, v in meta.items() if v not in (None, [], {}, "")}

        arch = {
            "meta": meta,
            "summary_flow": list(
                self.raw_meta.get("summary_flow") or DEFAULT_SUMMARY_FLOW
            ),
            "edge": edge,
            "lines": payload_lines,
            "shared": shared,
            "infra": infra,
            "cross_links": [],
        }
        return arch

    def _all_bands(self, comps_by_band):
        """输出顺序：edge 带 → 业务泳道（LINE_ORDER）→ 未登记泳道 → shared → infra。"""
        found = set(comps_by_band) | set(self.line_cost) | set(self.line_groups)
        ordered = [EDGE_BAND] if EDGE_BAND in found else []
        ordered += [l for l in LINE_ORDER if l in found]
        ordered += sorted(l for l in found
                          if l not in LINE_ORDER and l not in SPECIAL_LINES
                          and l != EDGE_BAND)
        ordered += [l for l in SPECIAL_LINES if l in found]
        return ordered

    @staticmethod
    def _band_columns(band):
        """band 允许的列（v2）：edge 单列、infra 五列、shared 四列、业务泳道三列。"""
        if band == EDGE_BAND:
            return [EDGE_BAND]
        if band == "infra":
            return list(INFRA_COLUMNS)
        if band == "shared":
            return list(SHARED_COLUMNS)
        return list(LINE_COLUMNS)

    def _assign_ids(self, comps_by_band):
        """COMP id：<band>_<col-slug>_<族slug>（observe 内 <band>_obs_<slug>），
        同基名冲突按排序加 _2/_3…（确定性）。

        必须在长尾折叠之前跑：id 只取决于 (band, 列, 族slug)，所以把长尾并进
        「其他 ×N」不会让留下来的卡换 id，config/cross_links_kunqi.json 与
        config/risks_kunqi.json 的 target 才是稳定契约（arch_schema.md 规则 7）。
        """
        for band, comps in comps_by_band.items():
            comps.sort(key=lambda c: (column_rank(c["column"]),
                                      c.get("_misc") and 1 or 0,
                                      c["kind"],
                                      c.get("_slug") or "",
                                      -(c.get("cost") or 0),
                                      c["evidence"]))
            used = Counter()
            for comp in comps:
                base = "%s_%s_%s" % (band, COL_SLUG.get(comp["column"], "x"),
                                     comp.get("_slug") or comp["kind"])
                used[base] += 1
                comp["id"] = base if used[base] == 1 else "%s_%d" % (base, used[base])

    def _pin_referenced(self, comps_by_band, risks, cross_links):
        """把 risks.target / cross_links.from|to 命中的卡钉住，长尾折叠不许吞掉它们。

        cross_links 的 kind 是连线类型（data|ai|msg），不是 comp kind，所以只按 id 匹配。
        """
        index = {}
        for comps in comps_by_band.values():
            for comp in comps:
                index[comp["id"]] = comp
        refs = []
        for risk in risks or []:
            if isinstance(risk, dict):
                refs.append(risk)
        for link in cross_links or []:
            if isinstance(link, dict):
                for side in ("from", "to"):
                    if _s(link.get(side)):
                        refs.append({"target": link.get(side)})
        for ref in refs:
            comp = self._resolve_ref(ref, index)
            if comp is not None:
                comp["_pinned"] = True

    @staticmethod
    def _resolve_ref(ref, index):
        """ref → comp：先按 id 精确命中，再用 line/kind/evidence 模糊匹配（与
        attach_risks._resolve_target 同语义，只是这里作用在折叠前的 comp 对象上）。
        没有 line/kind/evidence 兜底线索时只认精确 id，避免误钉一张无关的卡。"""
        target = _s(ref.get("target"))
        if target and target in index:
            return index[target]
        needle = _s(ref.get("evidence")) or target
        want_kind = _s(ref.get("kind"))
        want_line = _s(ref.get("line"))
        if not (want_kind or want_line or _s(ref.get("evidence"))):
            return None
        hits = []
        for comp_id, comp in index.items():
            band_id = _s(comp.get("_band")) or comp_id.split("_")[0]
            if want_line and band_id != want_line:
                continue
            if want_kind and comp.get("kind") != want_kind:
                continue
            if needle and needle.lower() not in (
                _s(comp.get("evidence")) + " " + _s(comp.get("name")) + " "
                + _s(comp.get("spec")) + " " + _s(comp.get("note"))
            ).lower():
                continue
            hits.append(comp)
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            exact = [h for h in hits
                     if needle and _s(h.get("evidence")).startswith(needle)]
            if len(exact) == 1:
                return exact[0]
            hits.sort(key=lambda h: -(h.get("cost") or 0))
            return hits[0]
        return None

    def _build_comp(self, band, kind, layer, mode, slug, rows):
        """折叠组 → COMP。展示字段（name/evidence/note）按折叠模式生成，
        列（v2 column）按 arch_schema.md 规则 2-4 决定。"""
        key = (band, kind, layer, mode, slug)
        meta = self.comp_meta.get(key) or {}
        pip = _s(meta.get("pip"))
        if not pip:
            pip = _most_common(Counter(
                _s(r.get("pipCode")) or _s(r.get("pip")) for r in rows
                if _s(r.get("pipCode")) or _s(r.get("pip"))
            )) or ""

        nicks = Counter()
        specs = Counter()
        coms = Counter()
        regions = Counter()
        charges = Counter()
        members = []          # 保序去重的「成员」身份（函数/实例/logstore/计费项）
        seen_members = set()
        notes = []
        months_seen = set()
        saturation = None
        product_only = None
        bandwidths = Counter()
        complete_sum = 0.0
        has_complete = False

        for row in rows:
            month = _s(row.get("month"))
            months_seen.add(month)
            if month in self.months_complete:
                has_complete = True
                complete_sum += _num(row.get("requireAmount"))
            nick = _s(row.get("instanceNick")) or _s(row.get("nk"))
            if nick:
                nicks[nick] += 1
            spec = _s(row.get("instanceSpec")) or _s(row.get("sp"))
            if spec:
                specs[spec] += 1
            com = _s(row.get("commodityName")) or _s(row.get("com"))
            if com:
                coms[com] += 1
            region = (_s(row.get("region")) or _s(row.get("reg"))
                      or (ecs_region(row) if mode == MODE_SPEC else ""))
            if region and region != "unknown":
                regions[region] += 1
            charge = _s(row.get("chargeType")) or _s(row.get("ct"))
            if charge:
                charges[charge] += 1
            bw = egress_bandwidth_kbps(row)
            if bw:
                bandwidths[bw] += 1
            if row.get("_saturation"):
                saturation = row["_saturation"]
            if row.get("_product_only"):
                product_only = row
            member = member_of(row, mode, pip, kind)
            if member and member not in seen_members:
                seen_members.add(member)
                members.append(member)
            if mode == MODE_INSTANCE:      # 逐实例卡才谈「单可用区/基础版」
                alloc = _s(row.get("instanceAllocation")) or _s(row.get("al"))
                if "基础版" in alloc:
                    notes.append("基础版（单节点无备）")
                zones = set(re.findall(r"可用区[:：]([^;]+)", alloc))
                if len(zones) == 1 and kind in ("redis", "tair", "rds", "mongo"):
                    notes.append("单可用区部署")

        # --- cost ----------------------------------------------------------
        if product_only is not None:
            cost = product_only.get("_product_cost")
            months_seen = set(product_only.get("_product_months") or [])
        elif not has_complete:
            cost = None                      # 只在残缺月出现 → 证据保留、金额置空
        elif saturation is not None and complete_sum <= 0:
            cost = None                      # 饱和抽样根行金额为 0 → 只有存在性证据
        else:
            cost = _money(complete_sum, self.months_complete)

        # --- name / evidence / note ---------------------------------------
        n = len(members)
        samples = self._samples(rows, members, nicks, 3)
        name, evidence = self._fold_display(
            mode, slug, kind, pip, rows, members, samples, nicks, coms, bandwidths
        )
        note_bits = []
        region = _most_common(regions)
        if region and mode != MODE_SPEC:     # SPEC 的地域已在 evidence 里
            note_bits.append(region)
        if charges and mode in (MODE_INSTANCE, MODE_SPEC, MODE_POOL):
            note_bits.append("/".join(sorted(charges)))
        if saturation is not None:
            sat_info = self.comp_saturation.get(key) or {}
            conv = "" if sat_info.get("converged", True) else "·未收敛"
            note_bits.append("饱和抽样根计数%s" % conv)
            if cost is None:
                note_bits.append("饱和抽样存在性证据（金额见 product_rows）")
        if product_only is not None:
            note_bits.append("无实例维度·产品级取证")
        note_bits.extend(dict.fromkeys(notes))

        comp = {
            "id": None,                # 由 _assign_ids 统一编号，保证全局唯一
            "kind": kind,
            "column": column_of(band, kind, layer, pip, rows),
            "name": name,
            "evidence": evidence,
            "spec": _most_common(specs),
            "cost": cost,
            "months": sorted(m for m in months_seen if m),
            "rows": len(rows),
            "members": n,
            "_slug": self._comp_slug(mode, kind, pip, slug),
            "_mode": mode,
            "_band": band,
            "_layer": layer,           # v1 语义层，只作调试/排序线索，不进输出
        }
        if note_bits:
            comp["note"] = "｜".join(dict.fromkeys(note_bits))
        # cost 恒保留（arch_schema.md：不可拆分时写 null，不是省略键）
        return comp

    @staticmethod
    def _samples(rows, members, nicks, limit):
        """折叠卡的 sample：优先有昵称的成员，其次成员 id 本身。"""
        nick_by_member = {}
        for row in rows:
            member = instance_root(row) or fc_function_name(row)
            nick = _s(row.get("instanceNick")) or _s(row.get("nk"))
            if member and nick and member not in nick_by_member:
                nick_by_member[member] = nick
        out = []
        for member in members:
            label = nick_by_member.get(member)
            if label:
                out.append(label)
            if len(out) >= limit:
                break
        for member in members:
            if len(out) >= limit:
                break
            if member not in out:
                out.append(member)
        return out[:limit]

    def _fold_display(self, mode, slug, kind, pip, rows, members, samples,
                      nicks, coms, bandwidths):
        """按折叠模式产出 (name, evidence)。"""
        n = len(members)
        if mode == MODE_EDGE:
            label = (EDGE_LABEL.get(kind) or OTHER_LABEL_BY_PIP.get(_s(pip).lower())
                     or _s(kind).upper())
            if kind == "cdn":
                # CDN 的 instanceId 是 <uid>;<区域码>，成员即加速区域
                areas = sorted(m for m in members if m and not m.isdigit())
                return ("%s ×%d 区" % (label, len(areas) or 1),
                        "区域: %s" % (", ".join(areas) or "-"))
            return ("%s ×%d" % (label, n or len(rows)),
                    "%s｜×%d" % ("/".join(samples[:3]) or slug, n or len(rows)))
        if mode == MODE_FAMILY:
            name = slug if slug != FC_UUID_FAMILY else "无业务前缀函数（uuid）"
            return name, "%s ×%d 函数" % (slug, n)
        if mode == MODE_SPEC:
            spec_family, region, charge = (slug.split("|") + ["", "", ""])[:3]
            return ("ECS %s" % spec_family,
                    "%s｜×%d 台（%s·%s）" % (
                        "/".join(samples[:3]) or spec_family, n,
                        region or "-", charge or "postpay"))
        if mode == MODE_PROJECT:
            top = sorted({sls_parts(r)[2] for r in rows if sls_parts(r)[2]})
            return ("SLS %s" % slug,
                    "%d logstore｜top3: %s" % (n or len(top), ", ".join(top[:3]) or "-"))
        if mode == MODE_BILLING:
            if kind == "bailian":
                return "百炼 %s" % slug, "%s｜计费项×%d" % (slug, len(rows))
            name = _most_common(nicks) or slug
            return name, "%s｜计费项×%d" % (slug, len(rows))
        if mode == MODE_EGRESS:
            bw = "、".join(fmt_bandwidth(b) for b, _ in bandwidths.most_common(3))
            pips = sorted({_s(r.get("pipCode")).lower() for r in rows} & set(EGRESS_PIPS))
            return ("公网出口 %s" % "/".join(p.upper() for p in pips) if pips
                    else "公网出口",
                    "EIP×%d｜峰值 %s" % (n, bw or "未标峰值"))
        if mode == MODE_POOL:
            label = POOL_KINDS.get(kind, "池")
            if kind == "supabase":
                sub = Counter(supabase_subpool(m) for m in members)
                evidence = "+".join("%s×%d" % (k, v) for k, v in sub.most_common())
            elif kind == "memory":
                sub = Counter(memory_subpool(m) for m in members)
                evidence = "+".join("%s×%d" % (k, v) for k, v in sub.most_common())
            elif kind == "bailian":
                evidence = "%d ws｜%s" % (n, ", ".join(sorted(members)[:3]) or "-")
            else:
                evidence = "%s×%d" % (slug, n)
            return "%s ×%d" % (label, n), evidence
        if mode == MODE_FLEET:
            label = fold_label(kind, pip, slug)
            return "%s ×%d" % (label, n), "%s｜×%d" % ("/".join(samples[:3]) or slug, n)
        # MODE_INSTANCE
        root = instance_root(rows[0]) if rows else slug
        if kind == "sls":
            return (_most_common(nicks) or _most_common(coms) or root,
                    _s(rows[0].get("instanceId")) or root)
        return _most_common(nicks) or _most_common(coms) or root, root or slug

    @staticmethod
    def _comp_slug(mode, kind, pip, slug):
        """comp id 的族 slug 段（确定性：band + 列 + 本段）。"""
        token = kind if kind != "other" else (_s(pip).lower() or "other")
        if mode == MODE_INSTANCE:
            return token
        if mode == MODE_EGRESS:
            return token
        if mode == MODE_EDGE:
            return slugify(slug, 32) or token
        if mode in (MODE_SPEC, MODE_PROJECT):
            parts = slug.split("|")
            out = "%s-%s" % (token, slugify(parts[0], 20) or "x")
            if mode == MODE_SPEC and "addc" in parts:
                out += "-addc"     # AD 域控 ECS 单列（infra 规则 4 → 治理注册）
            return out
        if mode == MODE_BILLING:
            return token
        return slugify(slug, 32) or token

    def _enforce_budget(self, comps_by_band):
        """渲染预算（arch_schema.md 规则 6）：
        每列 COMP ≤ MAX_COMPS_PER_LAYER、observe 横条 ≤ MAX_COMPS_PER_OBSERVE、
        全图 COMP ≤ MAX_COMPS_TOTAL。

        两步走：
          1. 先把超过上限的列（含 observe 横条）按 cost 升序折长尾进「其他 ×N」；
          2. 全图仍超总预算时，反复挑「全图卡最多且还能折」的列再折一张（cost 最小那张），
             直到落到预算内。这样小泳道完全不动，只有胖列继续压，语义损失最小。
        长尾合并卡的 id slug 固定 MISC_SLUG，所以 comp id 仍然确定。
        """
        # band → column → comps
        grid = {}
        for band in sorted(comps_by_band):
            by_col = defaultdict(list)
            for comp in comps_by_band[band]:
                by_col[comp["column"]].append(comp)
            grid[band] = dict(by_col)

        def col_limit(col):
            return MAX_COMPS_PER_OBSERVE if col == OBSERVE else MAX_COMPS_PER_LAYER

        def total():
            return sum(len(cs) for cols in grid.values() for cs in cols.values())

        # 第一步：每列上限
        for band, cols in grid.items():
            for col, items in cols.items():
                guard = 0
                while len(items) > col_limit(col) and guard < 4096:
                    guard += 1
                    folded, moved = self._fold_one(items)
                    if not moved:
                        break            # 全被钉住了，折不动
                    items = folded
                    cols[col] = items

        # 第二步：全图总预算，每轮挑「卡最多且还能折」的列再折一张
        guard = 0
        while total() > MAX_COMPS_TOTAL and guard < 4096:
            guard += 1
            target = None
            for band, cols in grid.items():
                for col, items in cols.items():
                    foldable = sum(1 for c in items
                                   if not c.get("_misc") and not c.get("_pinned"))
                    if foldable <= MIN_LAYER_KEEP:
                        continue
                    score = (len(items), -column_rank(col))
                    if target is None or score > target[0]:
                        target = (score, band, col)
            if target is None:
                break
            _, band, col = target
            items, _ = self._fold_one(grid[band][col])
            grid[band][col] = items

        folds = []
        for band, cols in grid.items():
            comps_by_band[band] = []
            for col in COLUMN_ORDER:
                if col in cols:
                    comps_by_band[band].extend(cols[col])
            for col, items in cols.items():     # 未知列（理论上不存在）
                if col not in COLUMN_ORDER:
                    comps_by_band[band].extend(items)
            for col, items in cols.items():
                misc = next((c for c in items if c.get("_misc")), None)
                if misc is not None:
                    misc["id"] = "%s_%s_%s" % (band, COL_SLUG.get(col, "x"), MISC_SLUG)
                    folds.append((band, col, len(misc["_tail_items"]), misc["members"]))

        for band, col, n_tail, n_members in folds:
            label = "观测" if col == OBSERVE else col
            self.warnings.append(
                "%s.%s 折叠后仍超预算，cost 最小的 %d 张卡并入「其他 ×%d」（含实例 %d 个）"
                % (band, label, n_tail, n_tail, n_members)
            )
        if total() > MAX_COMPS_TOTAL:
            self.warnings.append(
                "折叠后 COMP 总数 %d 仍超过预算 %d（每列已压到下限 %d）"
                % (total(), MAX_COMPS_TOTAL, MIN_LAYER_KEEP)
            )
        return total()

    @staticmethod
    def _fold_one(items):
        """把该列 cost 最小的一张（未钉住的）卡并进「其他 ×N」卡；返回 (新列表, 折掉张数)。"""
        if not items:
            return items, 0
        column = items[0]["column"]
        tail_items = []
        for c in items:
            if c.get("_misc"):
                tail_items.extend(c["_tail_items"])
        rest = [c for c in items if not c.get("_misc")]
        foldable = [c for c in rest if not c.get("_pinned")]
        if not foldable:
            return items, 0
        victim = min(foldable, key=lambda c: (c.get("cost") or 0,
                                              c.get("kind") or "",
                                              c.get("evidence") or ""))
        tail_items.append(victim)
        kept = [c for c in rest if c is not victim]
        kept.append(Aggregator._new_misc(column, tail_items))
        return kept, 1

    @staticmethod
    def _new_misc(column, tail):
        """长尾合并卡「其他 ×N」：cost 求和，note/evidence 留痕。"""
        costs = [c.get("cost") for c in tail if c.get("cost") is not None]
        members = sum(int(c.get("members") or 1) for c in tail)
        band = _s(tail[0].get("_band")) if tail else ""
        return {
            "id": None,
            "kind": "other",
            "column": column,
            "name": "其他 ×%d" % len(tail),
            "evidence": "、".join(_s(c.get("name"))[:14] for c in tail[:3]) + "…",
            "cost": sum(costs) if costs else None,
            "months": sorted({m for c in tail for m in (c.get("months") or [])}),
            "rows": sum(int(c.get("rows") or 1) for c in tail),
            "members": members,
            "note": "长尾合并（cost 最小的 %d 张卡；含实例 %d 个）" % (len(tail), members),
            "_slug": MISC_SLUG,
            "_mode": MODE_FLEET,
            "_band": band,
            "_misc": True,
            "_tail_items": list(tail),
        }

    def _build_band(self, band, comps):
        """折叠后的 comps → 一个带对象。

        edge 带（arch_schema.md 顶层 edge）：{name, comps[], note}，单列扁平。
        line/shared/infra：LINE 形状，含 layers（按带列序）＋ observe[] 横条 ＋ risks[]。
        """
        # id 已在 _assign_ids（折叠前）分配好，这里只按确定性键排布，不改 id
        comps = sorted(comps, key=lambda c: (column_rank(c["column"]),
                                             c.get("_misc") and 1 or 0,
                                             c["kind"],
                                             -(c.get("cost") or 0),
                                             c["evidence"]))
        ids = [c["id"] for c in comps]
        if len(ids) != len(set(ids)):
            dup = [i for i, n in Counter(ids).items() if n > 1]
            self.warnings.append("%s 带 comp id 重复：%s" % (band, ",".join(sorted(dup))))

        def clean(c):
            return {k: v for k, v in c.items()
                    if not k.startswith("_") and k != "column"}

        if band == EDGE_BAND:
            return {
                "name": EDGE_NAME,
                "comps": [clean(c) for c in comps],
                "note": EDGE_NOTE,
            }

        columns = self._band_columns(band)
        ordered_layers = {}
        observe = []
        for comp in comps:
            if comp["column"] == OBSERVE:
                observe.append(clean(comp))
                continue
            ordered_layers.setdefault(comp["column"], []).append(clean(comp))
        ordered_layers = {col: ordered_layers[col]
                          for col in columns if col in ordered_layers}

        methods = self.line_methods.get(band) or Counter()
        groups = self.line_groups.get(band) or Counter()
        if "resource_group" in methods and groups:
            attribution = "resource_group"
            group = _most_common(groups)
        else:
            side = [m for m in ("naming", "vpc", "sls", "kind") if methods.get(m)]
            attribution = side[0] if side else "kind"
            group = "untagged:%s" % METHOD_LABEL.get(attribution, attribution)

        vpc = _most_common(self.line_vpcs.get(band) or Counter())
        out = {
            "id": band,
            "name": self.rules.line_names.get(band) or group or band,
            "group": group,
            "attribution": attribution,
            "color": COLOR_MAP.get(band, band),
            "cost_month": _money(self.line_cost.get(band, 0.0), self.months_complete),
            "layers": ordered_layers,
            "observe": observe,
            "risks": [],
        }
        if vpc:
            out["vpc"] = vpc
        return out

    def _cost_coverage(self):
        coverage = {}
        for month in sorted(set(list(self.product_totals) + list(self.row_totals))):
            prod = self.product_totals.get(month, 0.0)
            rows = self.row_totals.get(month, 0.0)
            coverage[month] = {
                "row_level": int(round(rows)),
                "product_level": int(round(prod)),
                "ratio": round(rows / prod, 3) if prod else None,
                "complete": month in self.months_complete,
            }
        return coverage

    # -- 风险挂接 ----------------------------------------------------------
    @staticmethod
    def _comp_index(arch):
        """arch → {comp_id: comp}，覆盖 edge 带 / lines / shared / infra 的列与 observe 横条。

        v2 的观测卡在 observe[] 里、边缘卡在顶层 edge.comps 里，两处都必须能被
        cross_links 与 risks 的 target 命中，否则 risks_kunqi.json 的 enter_obs_sls-enter
        这类目标就永远解析不到（AGENTS.md 第 9 条）。
        """
        index = {}

        def add(comps):
            for comp in comps or []:
                if isinstance(comp, dict) and comp.get("id"):
                    index[comp["id"]] = comp

        edge = arch.get("edge") or {}
        add(edge.get("comps"))
        for band in _all_bands(arch):
            add(band.get("observe"))
            for comps in (band.get("layers") or {}).values():
                add(comps)
        return index

    def attach_cross_links(self, arch, cross_links):
        """跨带连线：from/to 必须解析到真实 comp id，解析不到就丢弃该线并落 warnings。

        渲染侧只对两端都存在的卡画依赖 chip（arch_schema.md「渲染约定」），所以这里
        必须在输出前把悬空连线摘掉，否则 arch.json 的 cross_links 就是假契约。
        """
        index = self._comp_index(arch)

        resolved, dropped = [], []
        for link in cross_links or []:
            if not isinstance(link, dict):
                continue
            out = dict(link)
            ok = True
            for side in ("from", "to"):
                want = _s(link.get(side))
                if not want or want not in index:
                    dropped.append("%s=%s" % (side, want or "-"))
                    ok = False
                    continue
                out[side] = index[want]["id"]
            if ok:
                resolved.append(out)
        if dropped:
            arch["meta"].setdefault("warnings", []).append(
                "cross_links 未解析（已丢弃）：%s" % "；".join(dropped)
            )
        arch["cross_links"] = resolved
        return arch

    def attach_risks(self, arch, risks):
        """把风险清单挂到 band.risks；target 必须解析到真实 comp id（含 observe/edge）。"""
        index = {}   # comp id -> (band_id, comp)
        for band in _all_bands(arch):
            band_id = band.get("id") or EDGE_BAND
            for comp in (band.get("observe") or []):
                index[comp["id"]] = (band_id, comp)
            for comps in (band.get("layers") or {}).values():
                for comp in comps:
                    index[comp["id"]] = (band_id, comp)
        edge = arch.get("edge") or {}
        for comp in (edge.get("comps") or []):
            index[comp["id"]] = (EDGE_BAND, comp)

        unresolved = []
        for risk in risks or []:
            if not isinstance(risk, dict):
                continue
            level = _s(risk.get("level")).upper()
            text = _s(risk.get("text")) or _s(risk.get("desc"))
            if level not in ("P0", "P1", "P2"):
                unresolved.append({"risk": risk, "reason": "level 非法（须 P0/P1/P2）"})
                continue
            band_id, comp = self._resolve_target(risk, index)
            if not comp:
                unresolved.append({
                    "risk": {"level": level, "text": text, "target": risk.get("target")},
                    "reason": "未匹配到真实 comp（arch_schema.md 归线规则 5）",
                })
                continue
            # edge 带在 schema 里没有 risks 键（{name,comps,note}）—— 挂到最相关的
            # 业务/基础设施带上，保证 P1「出口带宽」这类风险不会静默丢失
            if band_id == EDGE_BAND:
                band_id, comp = _retarget_edge_risk(arch, risk, comp)
                if comp is None:
                    unresolved.append({
                        "risk": {"level": level, "text": text,
                                 "target": risk.get("target")},
                        "reason": "edge 带风险无法改挂到任何带（schema 的 edge 无 risks 键）",
                    })
                    continue
            band = _band_by_id(arch, band_id)
            if band is None:
                unresolved.append({
                    "risk": {"level": level, "text": text, "target": risk.get("target")},
                    "reason": "带 %s 不存在" % band_id,
                })
                continue
            band.setdefault("risks", []).append({
                "level": level,
                "target": comp["id"],
                "text": text,
            })
        for band in _all_bands(arch):
            if band.get("risks"):
                band["risks"].sort(key=lambda r: ("P0", "P1", "P2").index(r["level"]))
        if unresolved:
            arch["meta"].setdefault("warnings", []).extend(
                "风险未挂接：%s[%s] %s" % (
                    u["risk"].get("level"), u["risk"].get("target") or "-",
                    u["reason"],
                )
                for u in unresolved
            )
            arch["meta"]["unresolved_risks"] = unresolved
        return arch

    @staticmethod
    def _resolve_target(risk, index):
        """target 直接命中 comp id；否则用 evidence/kind/line 组合模糊匹配。"""
        target = _s(risk.get("target"))
        if target and target in index:
            return index[target]
        needle = _s(risk.get("evidence")) or (target if target else "")
        want_kind = _s(risk.get("kind"))
        want_line = _s(risk.get("line"))
        hits = []
        for comp_id, (band_id, comp) in index.items():
            if want_line and band_id != want_line:
                continue
            if want_kind and comp.get("kind") != want_kind:
                continue
            if needle and needle.lower() not in (
                _s(comp.get("evidence")) + " " + _s(comp.get("name")) + " "
                + _s(comp.get("spec")) + " " + _s(comp.get("note"))
            ).lower():
                continue
            hits.append((band_id, comp))
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            # 多命中：优先 evidence 精确前缀，其次金额最大
            exact = [h for h in hits if needle and _s(h[1].get("evidence")).startswith(needle)]
            if len(exact) == 1:
                return exact[0]
            hits.sort(key=lambda h: -(h[1].get("cost") or 0))
            return hits[0]
        return None, None


# ---------------------------------------------------------------------------
# 风险清单装载（json 或 markdown 表）
# ---------------------------------------------------------------------------

MD_RISK_ROW = re.compile(
    r"^\s*[\|\-\s]*\b(P0|P1|P2)\b\s*[\|：:]\s*(?P<target>[^\|]+?)\s*\|\s*(?P<text>.+?)\s*\|?\s*$"
)
MD_RISK_LINE = re.compile(
    r"^\s*(?:\d+[\.\)]|[-*])\s*(?:\*\*)?(P0|P1|P2)(?:\*\*)?\s*[—\-:：\s]+(?P<text>.+?)\s*$"
)


def load_cross_links(path):
    """跨泳道连线清单：支持裸数组，或 {"links":[{from,to,label,kind}]}（带 _comment 的自解释版）。"""
    if not path:
        return None
    with open(path, "r", encoding="utf-8") as fh:
        data = json.loads(fh.read())
    if isinstance(data, dict):
        data = data.get("links") or data.get("cross_links") or []
    return [l for l in data if isinstance(l, dict)]


def load_risks(path):
    """支持两种格式：
    * JSON：{"risks":[{"level","target","text","line","kind","evidence"}]} 或裸数组
    * Markdown：promo-guard.md 风格列表行「1. **P0** 描述…」或表格行「| P0 | target | text |」
    """
    if not path:
        return []
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if path.endswith(".json") or text.lstrip().startswith(("{", "[")):
        data = json.loads(text)
        items = data.get("risks") if isinstance(data, dict) else data
        return [r for r in (items or []) if isinstance(r, dict)]
    risks = []
    for line in text.splitlines():
        m = MD_RISK_ROW.match(line)
        if m:
            risks.append({
                "level": m.group(1),
                "target": m.group("target").strip().strip("*` "),
                "text": m.group("text").strip(),
            })
            continue
        m = MD_RISK_LINE.match(line)
        if m:
            risks.append({"level": m.group(1), "text": m.group("text").strip()})
    return risks


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def aggregate(raw, months_complete=None, rules_overrides=None, risks=None,
              legacy_rows=None, cross_links=None):
    """纯函数入口（tests 直接调这个）。"""
    rules = Rules(rules_overrides or (raw.get("meta") or {}).get("rules"))
    rows, warnings = collect_rows(raw, legacy_rows)
    agg = Aggregator(raw, months_complete, rules)
    agg.warnings.extend(warnings)
    agg.run(rows)
    arch = agg.build(risks=risks, cross_links=cross_links)
    if cross_links:
        agg.attach_cross_links(arch, cross_links)
    else:
        arch["meta"].setdefault("warnings", []).append(
            "cross_links 未提供（--cross-links），输出空数组"
        )
    agg.attach_risks(arch, risks)
    return arch


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="bills_raw.json → arch.json（契约见 docs/arch_schema.md）"
    )
    parser.add_argument("--in", dest="inp", required=True, help="fetch_bills.js 落盘的原始 JSON")
    parser.add_argument("--out", dest="out", required=True, help="arch.json 输出路径")
    parser.add_argument(
        "--months-complete", dest="months_complete", default="",
        help="参与月均的完整月，逗号分隔，如 202609,202610（残缺月只进证据）",
    )
    parser.add_argument("--risks", dest="risks", default="", help="风险清单 json/markdown")
    parser.add_argument("--cross-links", dest="cross_links", default="", help="跨泳道连线 JSON 数组")
    parser.add_argument("--rg-links", dest="rg_links", default="", help="旧格式 rg_links.json（可选）")
    parser.add_argument("--rules", dest="rules", default="", help="归线规则覆盖 JSON（换客户时用）")
    args = parser.parse_args(argv)

    months = [m.strip() for m in args.months_complete.split(",") if m.strip()]
    raw = load_raw(args.inp)
    legacy_rows, legacy_warn = ([], [])
    if args.rg_links:
        legacy_rows, legacy_warn = load_legacy_rg_links(args.rg_links)
    rules_overrides = None
    if args.rules:
        rules_overrides = json.loads(open(args.rules, "r", encoding="utf-8").read())
    risks = load_risks(args.risks) if args.risks else []
    cross_links = load_cross_links(args.cross_links) if args.cross_links else None

    arch = aggregate(
        raw,
        months_complete=months,
        rules_overrides=rules_overrides,
        risks=risks,
        legacy_rows=legacy_rows,
        cross_links=cross_links,
    )
    arch["meta"].setdefault("warnings", []).extend(legacy_warn)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(arch, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")
    os.replace(tmp, args.out)

    bands = list(arch["lines"]) + [x for x in (arch.get("shared"), arch.get("infra")) if x]
    n_comps = sum(
        len(comps) for band in bands
        for comps in list((band.get("layers") or {}).values()) + [band.get("observe") or []]
    ) + len(((arch.get("edge") or {}).get("comps")) or [])
    n_risks = sum(len(band.get("risks") or []) for band in bands)
    n_p0 = sum(1 for band in bands for r in (band.get("risks") or [])
               if r["level"] == "P0")
    sys.stderr.write(
        "[aggregate] %s → %s｜schema=%s edge=%d lines=%d comps=%d risks=%d(P0=%d) 完整月=%s\n" % (
            args.inp, args.out, arch["meta"].get("schema_version"),
            len(((arch.get("edge") or {}).get("comps")) or []),
            len(bands), n_comps, n_risks, n_p0,
            ",".join(arch["meta"].get("months") or []) or "-",
        )
    )
    for warn in arch["meta"].get("warnings") or []:
        sys.stderr.write("[aggregate][warn] %s\n" % warn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
