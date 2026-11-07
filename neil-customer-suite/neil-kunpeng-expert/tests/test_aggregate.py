#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_aggregate.py —— aggregate.py 归线/月均/饱和抽样契约测试

零第三方依赖，python3 标准库 unittest。直接跑：
    python3 tests/test_aggregate.py

fixture 为自造小型数据（10 行 instance_rows + 4 行 group_rows + saturation + product_rows），
覆盖 arch_schema.md 的：组内命中、命名归线、VPC 归线、SLS 归线、kind 兜底、
残缺月剔除、saturation 根/族计数、去重、风险挂接。
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)

import aggregate  # noqa: E402


def inst(month, pip, iid, nick=None, rg=None, alloc=None, tag=None, amount=0.0,
         com=None, spec=None):
    """造一行 INSTANCE 级账单。"""
    row = {
        "month": month,
        "tableType": "INSTANCE_CONSUME_MONTH",
        "pipCode": pip,
        "instanceId": iid,
        "requireAmount": amount,
        "hashKey": "hk:%s:%s:%s" % (month, pip, iid),
    }
    if nick is not None:
        row["instanceNick"] = nick
    if rg is not None:
        row["resourceGroupName"] = rg
    if alloc is not None:
        row["instanceAllocation"] = alloc
    if tag is not None:
        row["instanceTag"] = tag
    if com is not None:
        row["commodityName"] = com
    if spec is not None:
        row["instanceSpec"] = spec
    return row


def build_fixture():
    """bills_raw.json fixture（完整月 202609/202610 + 残缺月 202611）。

    归线覆盖（每条 line 只留一种归线证据，便于断言 LINE.attribution）：
      enter   → resource_group（enter-prod 组内 RDS/Redis）＋ FC 命名族
      infra   → resource_group（infra-prod 组内 credit-prod RDS）
      game    → vpc（无组标签 ES，allocation 里 vpc-t4nu70bsp3…）
      framia  → sls（无组标签 SLS project framia-prod）
      shared  → kind（百炼 sfm ＋ acs 池 ＋ sae 产品级）
    金额取偶数，避免 round 半分位歧义。
    """
    # --- enter-prod 组内命中 ---
    enter_rds_09 = inst("202609", "rds", "pgm-enter;ap-southeast-1", nick="enter-main",
                        rg="enter-prod",
                        alloc="网络类型:专有网络;可用区:ap-southeast-1b;系列:高可用版",
                        amount=1000.0, com="关系型数据库（按量付费）")
    enter_rds_10 = inst("202610", "rds", "pgm-enter;ap-southeast-1", nick="enter-main",
                        rg="enter-prod",
                        alloc="网络类型:专有网络;可用区:ap-southeast-1b;系列:高可用版",
                        amount=1200.0, com="关系型数据库（按量付费）")
    # 残缺月：9999 元只进证据不进月均
    enter_rds_11 = inst("202611", "rds", "pgm-enter;ap-southeast-1", nick="enter-main",
                        rg="enter-prod", alloc="网络类型:专有网络;可用区:ap-southeast-1b",
                        amount=9999.0, com="关系型数据库（按量付费）")
    # enter Redis 单可用区（风险 P0 目标）
    enter_redis = inst("202609", "kvstore", "r-t4n3uotgffthqf3pzf;ap-southeast-1",
                       nick="enter-redis", rg="enter-prod",
                       alloc="网络类型:专有网络;可用区:ap-southeast-1b",
                       amount=3286.0, com="Redis 开源版 - 后付费（云原生）",
                       spec="redis.shard.with.proxy.large.ce")
    enter_redis_10 = dict(enter_redis, month="202610",
                          hashKey="hk:202610:kvstore:r-t4n3uotgffthqf3pzf")
    # --- infra-prod 组内命中（credit-prod RDS，风险 P2 目标） ---
    infra_rds = inst("202609", "rds", "pgm-credit;ap-southeast-1", nick="credit-prod",
                     rg="infra-prod", alloc="网络类型:专有网络;可用区:ap-southeast-1a",
                     amount=2000.0, com="关系型数据库（按量付费）")
    # --- VPC 归线：default 组，靠 allocation 里的 VPC 命中 game ---
    game_es_09 = inst("202609", "elasticsearch", "es-game-001;ap-southeast-1",
                      nick="game-search", rg="default resource group",
                      alloc="网络类型:专有网络;vpc-t4nu70bsp3vtio3c0p9mc;可用区:ap-southeast-1a",
                      amount=500.0, com="阿里云Elasticsearch")
    game_es_10 = dict(game_es_09, month="202610",
                      hashKey="hk:202610:elasticsearch:es-game-001")
    # --- SLS 归线：project framia-prod → framia ---
    framia_sls_09 = inst("202609", "sls", "framia-prod;video-render",
                         rg="default resource group", amount=400.0, com="日志服务")
    framia_sls_10 = dict(framia_sls_09, month="202610", requireAmount=600.0,
                         hashKey="hk:202610:sls:framia-prod;video-render")
    # --- kind 兜底：百炼（sfm）无组无命名无 VPC → shared.AI ---
    bailian = inst("202609", "sfm", "ws-p23r6an6se1lzq9z", nick="bailian-bj",
                   rg="default resource group", amount=1890.0, com="百炼大模型推理")

    instance_rows = [enter_rds_11, game_es_09, game_es_10, framia_sls_09,
                     framia_sls_10, bailian]
    # group_rows 放组内命中的行；末尾再塞一条与 instance_rows 同 hashKey 的重复行验证去重
    group_rows = [enter_rds_09, enter_rds_10, enter_redis, enter_redis_10, infra_rds,
                  dict(game_es_09)]

    saturation = [
        {
            "pipCode": "fc", "month": "202609", "pages": 12, "rootCount": 3,
            "familyCount": 1, "total": 74751, "sampled": 3, "converged": True,
            "roots": [
                {"root": "prod-coding-agent-aaaa1111bbbb", "family": "prod-coding-agent",
                 "region": "新加坡", "commodityName": "函数计算"},
                {"root": "prod-coding-agent-cccc2222dddd", "family": "prod-coding-agent",
                 "region": "新加坡", "commodityName": "函数计算"},
                {"root": "prod-coding-agent-eeee3333ffff", "family": "prod-coding-agent",
                 "region": "新加坡", "commodityName": "函数计算"},
            ],
        },
        {
            # 未收敛：验证 warnings 留痕
            "pipCode": "fc", "month": "202610", "pages": 12, "rootCount": 4,
            "familyCount": 1, "total": 74751, "sampled": 6000, "converged": False,
            "roots": [
                {"root": "prod-coding-agent-9999aaaa8888", "family": "prod-coding-agent",
                 "region": "新加坡", "commodityName": "函数计算"},
            ],
        },
        {
            "pipCode": "acs", "month": "202609", "pages": 8, "rootCount": 3,
            "familyCount": 1, "total": 5915, "sampled": 3, "converged": True,
            "roots": [
                {"root": "acs-t4n00987kaan", "family": "acs-pod-pool", "region": "新加坡"},
                {"root": "acs-t4n00987g5p8", "family": "acs-pod-pool", "region": "新加坡"},
                {"root": "acs-t4n00987m3se", "family": "acs-pod-pool", "region": "新加坡"},
            ],
        },
    ]

    product_rows = [
        {"month": "202609", "tableType": "PRODUCT_CONSUME_MONTH", "pipCode": "sae",
         "commodityName": "Serverless 应用引擎", "requireAmount": 10000.0},
        {"month": "202610", "tableType": "PRODUCT_CONSUME_MONTH", "pipCode": "sae",
         "commodityName": "Serverless 应用引擎", "requireAmount": 12000.0},
        {"month": "202611", "tableType": "PRODUCT_CONSUME_MONTH", "pipCode": "sae",
         "commodityName": "Serverless 应用引擎", "requireAmount": 800.0},
        # 账号级合计：不参与产品级对账，避免重复计
        {"month": "202609", "tableType": "ACCOUNT_CONSUME_MONTH", "pipCode": "",
         "commodityName": "账号合计", "requireAmount": 999999.0},
    ]

    return {
        "meta": {
            "uid": "1077748325118640",
            "customer": "北京坤启无限科技有限公司",
            "months": ["202609", "202610", "202611"],
            "months_complete": ["202609", "202610"],
            "sources": ["usercenter2:/bill/queryMonthConsumeReport"],
            "config": {"saturation": ["fc", "acs"]},
        },
        "instance_rows": instance_rows,
        "group_rows": group_rows,
        "product_rows": product_rows,
        "saturation": saturation,
        "failures": [],
    }


RISKS = [
    {"level": "P0", "target": "enter_data_redis", "line": "enter", "kind": "redis",
     "evidence": "r-t4n3uotgffthqf3pzf", "text": "enter Redis 单可用区"},
    {"level": "P2", "target": "infra_core_rds", "line": "infra", "kind": "rds",
     "evidence": "credit-prod", "text": "credit-prod 无只读"},
    {"level": "P1", "target": "shared_ai_ws", "line": "shared", "kind": "bailian",
     "evidence": "ws-", "text": "百炼提额"},
]


def all_bands(arch):
    """arch → 所有带（lines + shared + infra）；edge 单独取（它只有 comps）。"""
    out = list(arch.get("lines") or [])
    for key in ("shared", "infra"):
        if arch.get(key):
            out.append(arch[key])
    return out


def all_comps(arch):
    """arch → 全部 COMP（含 edge 带 comps 与各带 observe 横条）。"""
    out = list(((arch.get("edge") or {}).get("comps")) or [])
    for band in all_bands(arch):
        out.extend(band.get("observe") or [])
        for comps in (band.get("layers") or {}).values():
            out.extend(comps)
    return out


class TestFamilyOf(unittest.TestCase):
    def test_fc_fold(self):
        self.assertEqual(
            aggregate.family_of("prod-coding-agent-6a06cd33defb4-e565a12481ef", "fc"),
            "prod-coding-agent",
        )

    def test_acs_pool(self):
        self.assertEqual(aggregate.family_of("acs-t4n00987kaan", "acs"), "acs-pod-pool")

    def test_gpdb_supabase_pool(self):
        self.assertEqual(aggregate.family_of("spb-entercloud-pool-01", "gpdb"), "supabase-pool")

    def test_gpdb_cluster_kept(self):
        self.assertEqual(aggregate.family_of("gp-t4n1s8lqfy4c0q930", "gpdb"), "gp-t4n1s8lqfy4c0q930")


class TestRowDedup(unittest.TestCase):
    def test_hashkey_dedup(self):
        raw = build_fixture()
        rows, warnings = aggregate.collect_rows(raw)
        keys = [aggregate.row_key(r) for r in rows]
        self.assertEqual(len(keys), len(set(keys)), "collect_rows 应按 hashKey 去重")


class TestSupabasePool(unittest.TestCase):
    """arch_schema.md 归线规则 4：Supabase 池归 enter.计算，evidence 写池计数。"""

    def _payload(self):
        roots = (
            [{"root": "spb-%04d" % i, "family": "supabase-pool", "region": "新加坡"}
             for i in range(44)]
            + [{"root": "game_runtime-%02d" % i, "family": "supabase-pool", "region": "新加坡"}
               for i in range(2)]
        )
        return {
            "meta": {"months": ["202609"], "months_complete": ["202609"]},
            "instance_rows": [],
            "group_rows": [],
            "product_rows": [],
            "saturation": [{
                "pipCode": "gpdb", "month": "202609", "pages": 12, "rootCount": 46,
                "familyCount": 1, "total": 29244, "sampled": 46, "converged": True,
                "roots": roots,
            }],
            "failures": [],
        }

    def test_pool_goes_to_enter_compute_with_counts(self):
        arch = aggregate.aggregate(self._payload(), months_complete=["202609"])
        enter = next(l for l in arch["lines"] if l["id"] == "enter")
        supa = [c for c in enter["layers"].get("计算", []) if c["kind"] == "supabase"]
        self.assertEqual(len(supa), 1, "Supabase 池应折叠成一张卡")
        comp = supa[0]
        self.assertEqual(comp["evidence"], "spb×44+game_runtime×2")
        self.assertIn("Supabase 池", comp["name"])
        self.assertIsNone(comp.get("cost"))


class TestAttribution(unittest.TestCase):
    def setUp(self):
        self.raw = build_fixture()
        self.arch = aggregate.aggregate(
            self.raw, months_complete=["202609", "202610"], risks=RISKS
        )
        self.by_id = {l["id"]: l for l in self.arch["lines"]}
        if self.arch.get("shared"):
            self.by_id["shared"] = self.arch["shared"]
        if self.arch.get("infra"):
            self.by_id["infra"] = self.arch["infra"]

    def test_group_hit(self):
        """enter-prod 组内命中 → attribution=resource_group，group=enter-prod。"""
        enter = self.by_id["enter"]
        self.assertEqual(enter["attribution"], "resource_group")
        self.assertEqual(enter["group"], "enter-prod")

    def test_naming_attribution(self):
        """FC prod-coding-agent 走命名归线，折叠成函数族卡落在 enter 计算层。"""
        enter = self.by_id["enter"]
        fc_comps = enter["layers"].get("计算", [])
        fams = [c["evidence"] for c in fc_comps if c["kind"] == "fc"]
        self.assertIn("prod-coding-agent ×4 函数", fams)

    def test_vpc_attribution(self):
        """无组标签 ES 靠 allocation 里 vpc-t4nu70bsp3… 命中 game。"""
        game = self.by_id["game"]
        es = [c for c in game["layers"].get("数据", []) if c["kind"] == "es"]
        self.assertTrue(es, "ES 应经 VPC 归线进入 game")
        self.assertEqual(game["attribution"], "vpc")

    def test_sls_attribution(self):
        """SLS project framia-prod → framia，观测剥离后落 observe 横条（非 layers）。"""
        framia = self.by_id["framia"]
        self.assertEqual(framia["attribution"], "sls")
        # v2 规则 2：kind=sls 从 layers 移入 observe[]，framia 无普通列
        self.assertEqual(framia["layers"], {})
        sls = [c for c in framia["observe"] if c["kind"] == "sls"]
        self.assertTrue(sls)
        self.assertIn("framia-prod", sls[0]["name"])
        self.assertIn("logstore", sls[0]["evidence"])
        self.assertEqual(sls[0]["id"], "framia_obs_sls-framia-prod")
        # 完整月均值 (400+600)/2 = 500
        self.assertEqual(sls[0]["cost"], 500)

    def test_kind_fallback_bailian(self):
        """百炼（sfm）无组无命名无 VPC → kind 兜底进 shared.AI。"""
        shared = self.arch["shared"]
        self.assertEqual(shared["attribution"], "kind")
        ai = [c for c in shared["layers"].get("AI", []) if c["kind"] == "bailian"]
        self.assertTrue(ai, "百炼应经 kind 兜底进入 shared.AI")

    def test_partial_month_excluded(self):
        """残缺月 202611 的 9999 元不进 enter 月均；证据里仍标 202611。"""
        enter = self.by_id["enter"]
        rds = [c for c in enter["layers"].get("数据", []) if c["kind"] == "rds"][0]
        # 完整月均值 = (1000 + 1200)/2 = 1100，绝不能是含 9999 的值
        self.assertEqual(rds["cost"], 1100)
        self.assertIn("202611", rds["months"], "残缺月只进证据（months 列表）")
        # meta.months 只含完整月
        self.assertEqual(self.arch["meta"]["months"], ["202609", "202610"])

    def test_saturation_family_count(self):
        """fc 饱和抽样：prod-coding-agent 族基数=4（3+1），cost=null，未收敛留痕。"""
        enter = self.by_id["enter"]
        fam = [c for c in enter["layers"].get("计算", [])
               if c["kind"] == "fc" and c["evidence"] == "prod-coding-agent ×4 函数"][0]
        self.assertIsNone(fam.get("cost"), "饱和抽样金额不可拆分 → cost=null")
        self.assertIn("×4", fam["evidence"], "族基数应写进 evidence")
        sat = self.arch["meta"]["saturation"]["fc"]
        self.assertEqual(sat["root_count"], 4)
        self.assertEqual(sat["distinct_roots"], 4)
        self.assertEqual(sat["families"], 1)
        self.assertFalse(sat["converged"])
        self.assertTrue(any("未收敛" in w for w in self.arch["meta"]["warnings"]))

    def test_acs_single_pool(self):
        """acs 折叠成单池 acs-pod-pool，落到 shared 计算层。"""
        shared = self.arch["shared"]
        acs = [c for c in shared["layers"].get("计算", []) if c["kind"] == "acs"]
        self.assertTrue(acs)
        self.assertEqual(acs[0]["evidence"], "acs-pod-pool×3")
        self.assertIn("×3", acs[0]["name"])

    def test_product_only_comp(self):
        """sae 无实例维度 → 产品级 COMP，cost=完整月均值 (10000+12000)/2=11000。"""
        found = None
        for line in list(self.by_id.values()):
            for comps in line["layers"].values():
                for c in comps:
                    if c["kind"] == "sae":
                        found = c
        self.assertIsNotNone(found, "sae 应由 product_rows 补出 COMP")
        self.assertEqual(found["cost"], 11000)
        self.assertIn("无实例维度", found.get("note", ""))

    def test_account_row_not_double_counted(self):
        """ACCOUNT_CONSUME_MONTH 的 999999 不进产品级对账合计。"""
        cov = self.arch["meta"]["cost_coverage"].get("202609", {})
        self.assertLess(cov.get("product_level", 0), 100000)

    def test_cost_coverage_ratio(self):
        """逐月行级 vs 产品级对账比例存在且 complete 标记正确。"""
        cov = self.arch["meta"]["cost_coverage"]
        self.assertIn("202609", cov)
        self.assertTrue(cov["202609"]["complete"])
        self.assertIn("202611", cov)
        self.assertFalse(cov["202611"]["complete"])


class TestSchemaShape(unittest.TestCase):
    def setUp(self):
        self.arch = aggregate.aggregate(
            build_fixture(), months_complete=["202609", "202610"], risks=RISKS
        )

    def test_top_level_keys(self):
        for key in ("meta", "summary_flow", "edge", "lines", "shared", "infra",
                    "cross_links"):
            self.assertIn(key, self.arch)
        self.assertEqual(self.arch["meta"]["schema_version"], "v2")
        # edge 带固定三键（arch_schema.md 顶层结构）
        self.assertEqual(set(self.arch["edge"]), {"name", "comps", "note"})

    def test_line_keys(self):
        for line in all_bands(self.arch):
            for key in ("id", "name", "group", "attribution", "color", "cost_month",
                        "layers", "observe", "risks"):
                self.assertIn(key, line, "LINE 缺字段 %s" % key)
            self.assertIn(line["attribution"],
                          ("resource_group", "naming", "vpc", "sls", "kind"))

    def test_layers_only_v2_keys(self):
        """v2：业务泳道三列、shared 四列、infra 五列（arch_schema.md LINE/SHARED/INFRA 节）。"""
        allowed = {
            "line": set(aggregate.LINE_COLUMNS),
            "shared": set(aggregate.SHARED_COLUMNS),
            "infra": set(aggregate.INFRA_COLUMNS),
        }
        for line in self.arch["lines"]:
            self.assertTrue(set(line["layers"]) <= allowed["line"],
                            "非法业务泳道列 %s" % sorted(line["layers"]))
        for key in ("shared", "infra"):
            band = self.arch.get(key)
            if band:
                self.assertTrue(set(band["layers"]) <= allowed[key],
                                "%s 非法列 %s" % (key, sorted(band["layers"])))
        # v1 的六键不得残留
        v1 = set(aggregate.LAYER_ORDER)
        for band in all_bands(self.arch):
            self.assertFalse(set(band["layers"]) & (v1 - allowed["line"] -
                                                    allowed["shared"] -
                                                    allowed["infra"]),
                             "%s 残留 v1 层键" % band["id"])

    def test_observe_never_in_layers(self):
        """规则 2：kind ∈ {sls,prom,cms,arms,hdm} 一律进 observe[]，不进任何列。"""
        for band in all_bands(self.arch):
            for col, comps in (band["layers"] or {}).items():
                for c in comps:
                    self.assertNotIn(c["kind"], aggregate.OBSERVE_KINDS,
                                     "%s.%s 漏剥观测卡 %s" % (band["id"], col, c["id"]))

    def test_comp_ids_unique_and_referenced(self):
        comps = all_comps(self.arch)
        ids = [c["id"] for c in comps]
        self.assertEqual(len(ids), len(set(ids)), "comp id 必须全局唯一")
        for c in comps:
            for key in ("kind", "name", "evidence"):
                self.assertIn(key, c)
        # risks.target 必须指向真实 comp id（含 observe 横条）
        for band in all_bands(self.arch):
            for r in band["risks"]:
                self.assertIn(r["target"], ids, "risk target 悬空：%s" % r["target"])
                self.assertIn(r["level"], ("P0", "P1", "P2"))

    def test_comp_id_new_rule(self):
        """规则 7：comp id = <band>_<col-slug>_<族slug>；observe 内 <band>_obs_<slug>。"""
        legal = set(aggregate.COL_SLUG.values())
        id_re = __import__("re").compile(r"^([a-z0-9]+)_([a-z]+)_(.+)$")
        for c in all_comps(self.arch):
            m = id_re.match(c["id"])
            self.assertIsNotNone(m, "comp id 不合三段式：%s" % c["id"])
            self.assertIn(m.group(2), legal, "非法列 slug %s（id=%s）" % (m.group(2), c["id"]))
        # 抽样断言：具体 id 与 v2 列名对应
        by_id = {c["id"]: c for c in all_comps(self.arch)}
        self.assertEqual(by_id["enter_data_redis"]["kind"], "redis")
        self.assertEqual(by_id["infra_core_rds"]["kind"], "rds")
        self.assertEqual(by_id["shared_ai_ws"]["kind"], "bailian")
        self.assertEqual(by_id["framia_obs_sls-framia-prod"]["kind"], "sls")

    def test_risks_attached(self):
        enter = next(l for l in self.arch["lines"] if l["id"] == "enter")
        self.assertTrue(any(r["target"] == "enter_data_redis" and r["level"] == "P0"
                            for r in enter["risks"]))
        infra = self.arch["infra"]
        self.assertTrue(any(r["target"] == "infra_core_rds" for r in infra["risks"]))


class TestFolding(unittest.TestCase):
    """渲染预算折叠：账单逐实例/逐计费项明细必须收敛到图上能看的 COMP 粒度。"""

    @staticmethod
    def _lines(arch):
        out = {l["id"]: l for l in arch["lines"]}
        if arch.get("shared"):
            out["shared"] = arch["shared"]
        if arch.get("infra"):
            out["infra"] = arch["infra"]
        return out

    def test_fc_family_fold(self):
        """fc 同前缀族折成 1 个 COMP，evidence 写「族名 ×N 函数」。"""
        rows = [
            inst("202609", "fc", "prod-coding-agent-aaa111", rg="enter-prod", amount=10),
            inst("202609", "fc", "prod-coding-agent-bbb222", rg="enter-prod", amount=20),
            inst("202609", "fc", "prod-coding-agent-ccc333", rg="enter-prod", amount=30),
            inst("202609", "fc", "dev-sbx-ddd444", rg="enter-prod", amount=5),
            inst("202609", "fc", "dev-sbx-eee555", rg="enter-prod", amount=5),
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        enter = self._lines(arch)["enter"]
        fc = [c for c in enter["layers"].get("计算", []) if c["kind"] == "fc"]
        self.assertEqual(len(fc), 2, "两个函数族 → 两张卡")
        fams = {c["evidence"]: c for c in fc}
        self.assertIn("prod-coding-agent ×3 函数", fams)
        self.assertIn("dev-sbx ×2 函数", fams)
        # cost = 族内金额和（完整月均值）：(10+20+30)/1 = 60
        self.assertEqual(fams["prod-coding-agent ×3 函数"]["cost"], 60)

    def test_fc_family_zero_amount_is_existence_only(self):
        """fc 根行金额为 0 时 cost=null 并在 note 标「饱和抽样存在性证据」。"""
        payload = {
            "meta": {"months": ["202609"], "months_complete": ["202609"],
                     "config": {"saturation": ["fc"]}},
            "instance_rows": [], "group_rows": [],
            "saturation": [{
                "pipCode": "fc", "month": "202609", "pages": 3, "rootCount": 2,
                "converged": True,
                "roots": [{"root": "prod-coding-agent-x1", "family": "prod-coding-agent",
                           "region": "新加坡", "commodityName": "函数计算"},
                          {"root": "prod-coding-agent-x2", "family": "prod-coding-agent",
                           "region": "新加坡", "commodityName": "函数计算"}],
            }],
        }
        arch = aggregate.aggregate(payload, months_complete=["202609"])
        enter = self._lines(arch)["enter"]
        fc = [c for c in enter["layers"].get("计算", []) if c["kind"] == "fc"]
        self.assertEqual(len(fc), 1)
        self.assertIsNone(fc[0]["cost"], "抽样根金额为 0 → cost=null")
        self.assertIn("存在性证据", fc[0].get("note", ""))

    def test_egress_defaults_to_infra(self):
        """v2 规则 3：无组标签 eip 进 edge 带；cdt（kind=other）仍按归线走
        infra.容器网络（infra 五列无入口列）；tag project 明确指向某线才改归该线。"""
        rows = [
            inst("202609", "eip", "eip-aaa", rg="", amount=17,
                 alloc="带宽峰值:102400Kbps;地域:新加坡"),
            inst("202609", "cdt", "eip-bbb;ap-southeast-1;BGP;eip", rg="", amount=70),
            inst("202609", "cdt", "eip-ccc;ap-southeast-1;BGP;eip", rg="", amount=30,
                 tag="key:project value:enter; key:env value:prod"),
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        lines = self._lines(arch)
        # 无标签 EIP → edge 带（不进 infra）
        edge_ids = [c["id"] for c in arch["edge"]["comps"]]
        self.assertIn("edge_edge_eip", edge_ids)
        infra = lines["infra"]
        infra_egress = [c for col, comps in infra["layers"].items() for c in comps
                        if "公网出口" in c["name"]]
        self.assertTrue(infra_egress, "无 tag 的 cdt 应折成 infra 容器网络的公网出口卡")
        self.assertIn("容器网络", infra["layers"], "v2 infra 无入口列，出口类落容器网络")
        # tag project=enter 的 cdt 归 enter 入口列（v2 三列之一）
        enter = lines["enter"]
        enter_egress = [c for c in enter["layers"].get("入口", [])
                        if "公网出口" in c["name"]]
        self.assertTrue(enter_egress, "tag project=enter 的 cdt 应归 enter.入口")

    def test_ecs_spec_family_fold(self):
        """ecs 按「规格族|地域|chargeType」折，v2 落 infra.容器网络（规则 4）。"""
        rows = [
            inst("202609", "ecs", "i-aaa", nick="worker-1", rg="infra-prod",
                 spec="ecs.c9i.xlarge", alloc="地域:新加坡", amount=10),
            inst("202609", "ecs", "i-bbb", nick="worker-2", rg="infra-prod",
                 spec="ecs.c9i.xlarge", alloc="地域:新加坡", amount=10),
            inst("202609", "ecs", "i-ccc", nick="worker-3", rg="infra-prod",
                 spec="ecs.c9i.xlarge", alloc="地域:新加坡", amount=10),
            inst("202609", "ecs", "i-ddd", nick="worker-4", rg="infra-prod",
                 spec="ecs.c9i.xlarge", alloc="地域:新加坡", amount=10),
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        infra = self._lines(arch)["infra"]
        ecs = [c for c in infra["layers"].get("容器网络", []) if "ECS" in c["name"]]
        self.assertEqual(len(ecs), 1, "同规格族|地域|计费 → 一张卡")
        comp = ecs[0]
        self.assertEqual(comp["id"], "infra_net_ecs-ecs-c9i")
        self.assertIn("×4 台", comp["evidence"])
        # sample 昵称最多 3 个
        self.assertLessEqual(comp["evidence"].count("/"), 2)

    def test_sls_project_fold(self):
        """sls 按 SLS project 折；v2 规则 2 把它剥到 observe 横条。"""
        rows = [
            inst("202609", "sls", "1077748325118640;enter;logA;ap-southeast-1",
                 rg="enter-prod", amount=10),
            inst("202609", "sls", "1077748325118640;enter;logB;ap-southeast-1",
                 rg="enter-prod", amount=20),
            inst("202609", "sls", "1077748325118640;enter;logC;ap-southeast-1",
                 rg="enter-prod", amount=30),
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        enter = self._lines(arch)["enter"]
        sls = [c for c in enter["observe"] if c["kind"] == "sls"]
        self.assertEqual(len(sls), 1, "同 project → 一张卡")
        self.assertEqual(sls[0]["id"], "enter_obs_sls-enter")
        self.assertIn("3 logstore", sls[0]["evidence"])
        self.assertIn("logA", sls[0]["evidence"])
        self.assertEqual(enter["layers"], {}, "观测剥离后 enter 无普通列")

    def test_ons_billing_item_fold(self):
        """ons/kafka 按实例 id 折；v2 消息类并入业务泳道「数据」列（规则 2 备注）。"""
        rows = [
            inst("202609", "ons", "rmq-cn-x;message_count;normal_pub;shared",
                 rg="game-prod", com="RocketMQ 5.x Serverless系列", amount=5),
            inst("202609", "ons", "rmq-cn-x;message_count;order_pub;shared",
                 rg="game-prod", com="RocketMQ 5.x Serverless系列", amount=8),
            inst("202609", "ons", "rmq-cn-x;msg_store_spec;;shared",
                 rg="game-prod", com="RocketMQ 5.x Serverless系列", amount=2),
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        game = self._lines(arch)["game"]
        mq = [c for c in game["layers"].get("数据", []) if c["kind"] == "rocketmq"]
        self.assertEqual(len(mq), 1, "同实例多计费项 → 一张卡")
        self.assertNotIn("消息", game["layers"], "v2 业务泳道无独立「消息」列")
        self.assertEqual(mq[0]["id"], "game_data_rocketmq")
        self.assertIn("计费项×3", mq[0]["evidence"])

    def test_long_tail_misc_fold(self):
        """单层超过 MAX_COMPS_PER_LAYER 时，长尾（cost 最小）折进「其他 ×N」卡。"""
        rows = [
            inst("202609", "rds", "pgm-%02d" % i, nick="db-%02d" % i,
                 rg="game-prod", amount=float(i + 1))
            for i in range(aggregate.MAX_COMPS_PER_LAYER + 3)
        ]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        game = self._lines(arch)["game"]
        data = game["layers"].get("数据", [])
        self.assertLessEqual(len(data), aggregate.MAX_COMPS_PER_LAYER,
                             "每层 COMP 数必须 ≤ MAX_COMPS_PER_LAYER")
        misc = [c for c in data if c["name"].startswith("其他")]
        self.assertEqual(len(misc), 1, "应有且仅有一张长尾合并卡")
        self.assertIn("长尾合并", misc[0].get("note", ""))
        self.assertTrue(any("其他" in w or "长尾" in w or "预算" in w
                            for w in arch["meta"]["warnings"]),
                        "长尾折叠应在 warnings 留痕")


class TestBudget(unittest.TestCase):
    def test_real_data_within_budget(self):
        """构造一份高基数账单，确认全图 COMP 总数 ≤ MAX_COMPS_TOTAL 且每层 ≤ 每层上限。"""
        rows = []
        for i in range(80):
            rows.append(inst("202609", "rds", "pgm-infra-%03d" % i,
                             nick="db-%03d" % i, rg="infra-prod", amount=float(i)))
        for i in range(40):
            rows.append(inst("202609", "fc", "prod-coding-agent-%03d" % i,
                             rg="enter-prod", amount=float(i)))
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"])
        total = 0
        for line in all_bands(arch):
            for comps in line["layers"].values():
                self.assertLessEqual(len(comps), aggregate.MAX_COMPS_PER_LAYER)
                total += len(comps)
            self.assertLessEqual(len(line["observe"]),
                                 aggregate.MAX_COMPS_PER_OBSERVE)
            total += len(line["observe"])
        total += len(((arch.get("edge") or {}).get("comps")) or [])
        self.assertLessEqual(total, aggregate.MAX_COMPS_TOTAL)


class TestV2Blocks(unittest.TestCase):
    """v2 相对 v1 的结构变化：观测剥离 / edge 提取 / infra 列映射 / observe 折叠 / id 新规则。"""

    @staticmethod
    def _agg(rows, months=("202609",)):
        return aggregate.aggregate(
            {"meta": {"months": list(months), "months_complete": list(months)},
             "instance_rows": rows, "group_rows": []},
            months_complete=list(months))

    @staticmethod
    def _band(arch, name):
        for band in all_bands(arch):
            if band.get("id") == name:
                return band
        return None

    def test_observe_strip_all_kinds(self):
        """规则 2：sls/cms/arms 与 pipCode=hdm 全部剥到所属带的 observe 横条。"""
        rows = [
            inst("202609", "sls", "1077748325118640;enter;logA;ap-southeast-1", rg="enter-prod", amount=10),
            inst("202609", "cms", "cms-1", rg="enter-prod", com="企业云监控", amount=10),
            inst("202609", "arms", "arms-1", rg="game-prod", amount=10),
            inst("202609", "hdm", "hdm-1", rg="converge-prod", amount=10),
            inst("202609", "rds", "pgm-enter", rg="enter-prod", amount=10),
        ]
        arch = self._agg(rows)
        enter = self._band(arch, "enter")
        game = self._band(arch, "game")
        shared = self._band(arch, "shared")
        self.assertEqual(sorted(c["kind"] for c in enter["observe"]), ["cms", "sls"])
        self.assertEqual([c["kind"] for c in game["observe"]], ["arms"])
        # hdm 在 kind 词表里是 other，只能按 pipCode 认（aggregate.py 契约备注）
        self.assertTrue(any("hdm" in c["id"] for c in shared["observe"]),
                        "pipCode=hdm 应剥到 shared.observe")
        # 剥离后普通列里一张观测卡都不剩，业务列照常
        self.assertIn("数据", enter["layers"])
        self.assertEqual([c["kind"] for c in enter["layers"]["数据"]], ["rds"])
        for band in all_bands(arch):
            for comps in (band["layers"] or {}).values():
                for c in comps:
                    self.assertNotIn(c["kind"], aggregate.OBSERVE_KINDS)

    def test_observe_cost_still_counts_in_line(self):
        """观测剥离不改 line.cost_month 口径：observe 成本仍计入所属带。"""
        rows = [
            inst("202609", "sls", "1077748325118640;enter;logA;ap-southeast-1", rg="enter-prod", amount=100),
            inst("202609", "rds", "pgm-enter", rg="enter-prod", amount=300),
        ]
        arch = self._agg(rows)
        enter = self._band(arch, "enter")
        self.assertEqual(enter["cost_month"], 400, "observe 成本仍进 line 总额")
        self.assertEqual(sum(c["cost"] or 0 for c in enter["observe"]), 100)

    def test_observe_fold_over_eight(self):
        """规则 6：observe 横条 >8 条折「其他 ×N」，并留 warnings 痕。"""
        n = aggregate.MAX_COMPS_PER_OBSERVE + 3
        rows = [
            # uid 打头（≥10 位）才会被 sls_parts 认成 uid;project;logstore;region
            inst("202609", "sls", "1077748325118640;proj%02d;ls;ap-southeast-1" % i,
                 rg="enter-prod", amount=float(i + 1))
            for i in range(n)
        ]
        arch = self._agg(rows)
        enter = self._band(arch, "enter")
        self.assertLessEqual(len(enter["observe"]), aggregate.MAX_COMPS_PER_OBSERVE)
        misc = [c for c in enter["observe"] if c["name"].startswith("其他")]
        self.assertEqual(len(misc), 1, "observe 应有且仅有一张长尾卡")
        self.assertEqual(misc[0]["id"], "enter_obs_misc")
        self.assertIn("长尾合并", misc[0]["note"])
        # 首轮折叠只建「其他」卡不减张数，故 11 条要折 4 张才落到 8 条上限
        self.assertEqual(misc[0]["members"], n - (aggregate.MAX_COMPS_PER_OBSERVE - 1))
        self.assertTrue(any("enter.观测" in w for w in arch["meta"]["warnings"]),
                        "observe 折叠应留 warnings（列名写「观测」）")

    def test_edge_extraction_kinds(self):
        """规则 3：无组标签的 cdn/ga/waf/cas/cbwp → 顶层 edge 带。"""
        rows = [
            inst("202609", "cdn", "1077;cn-hangzhou", rg="", amount=10),
            inst("202609", "ga", "ga-bp1x", rg="", amount=20),
            inst("202609", "waf", "waf-cn-1", rg="", amount=30),
            inst("202609", "cas", "cas-1", rg="", amount=40),
            inst("202609", "cbwp", "cbwp-1", rg="", amount=50),
        ]
        arch = self._agg(rows)
        ids = sorted(c["id"] for c in arch["edge"]["comps"])
        self.assertEqual(ids, ["edge_edge_cdn", "edge_edge_ga", "edge_edge_other-cas",
                               "edge_edge_other-cbwp", "edge_edge_waf"])
        self.assertEqual(set(arch["edge"]), {"name", "comps", "note"})
        self.assertTrue(arch["edge"]["note"])
        # edge 带不参与泳道渲染：不出现在 lines/shared/infra
        for band in all_bands(arch):
            for comps in (band["layers"] or {}).values():
                for c in comps:
                    self.assertNotIn(c["kind"], ("cdn", "ga", "waf"))

    def test_edge_untagged_eip_vs_nlb_eip(self):
        """规则 3：无组标签且非 CREATE_BY_NLB 的 EIP → edge；CREATE_BY_NLB 的留泳道入口。"""
        rows = [
            inst("202609", "eip", "eip-free", rg="", amount=20,
                 alloc="带宽峰值:102400Kbps"),
            inst("202609", "eip", "eip-nlb", nick="CREATE_BY_NLB.nlb-enter01",
                 rg="enter-prod", amount=50, alloc="带宽峰值:204800Kbps"),
        ]
        arch = self._agg(rows)
        self.assertEqual([c["id"] for c in arch["edge"]["comps"]], ["edge_edge_eip"])
        enter = self._band(arch, "enter")
        self.assertIn("enter_access_eip", [c["id"] for c in enter["layers"]["入口"]],
                      "CREATE_BY_NLB 的 EIP 留所属泳道入口列")

    def test_edge_tagged_product_stays_in_lane(self):
        """规则 3：有组标签的 cdn 不进 edge，留泳道入口列。"""
        arch = self._agg([inst("202609", "cdn", "1077;cn-hangzhou", rg="enter-prod",
                               amount=10)])
        self.assertEqual(arch["edge"]["comps"], [])
        enter = self._band(arch, "enter")
        self.assertIn("cdn", [c["kind"] for c in enter["layers"]["入口"]])

    def test_edge_cost_separate_from_lines(self):
        """edge 成本单列（meta.edge_cost_month），不并进任何 line.cost_month。"""
        rows = [
            inst("202609", "cdn", "1077;cn-hangzhou", rg="", amount=100),
            inst("202609", "rds", "pgm-enter", rg="enter-prod", amount=300),
        ]
        arch = self._agg(rows)
        self.assertEqual(arch["meta"]["edge_cost_month"], 100)
        self.assertEqual(self._band(arch, "enter")["cost_month"], 300)
        self.assertEqual(sum(c["cost"] or 0 for c in arch["edge"]["comps"]), 100)

    def test_infra_column_mapping(self):
        """规则 4：infra 组内五列映射（核心库/消息流/分析同步/治理注册/容器网络）。"""
        rows = [
            inst("202609", "rds", "pgm-i", rg="infra-prod", amount=1),
            inst("202609", "kvstore", "r-i", rg="infra-prod", amount=1),
            inst("202609", "mongodb", "dds-i", rg="infra-prod", amount=1),
            inst("202609", "alikafka", "alikafka_i", rg="infra-prod", amount=1),
            inst("202609", "ons", "rmq-i", rg="infra-prod", amount=1),
            inst("202609", "eventbridge", "eb-i", rg="infra-prod", amount=1),
            inst("202609", "gpdb", "gp-i", rg="infra-prod", amount=1),
            inst("202609", "dts", "dts-i", rg="infra-prod", amount=1),
            inst("202609", "odps", "odps-i", rg="infra-prod", amount=1),
            inst("202609", "mse", "mse-i", rg="infra-prod", amount=1),
            inst("202609", "dms", "dms-i", rg="infra-prod", amount=1),
            inst("202609", "hbr", "hbr-i", rg="infra-prod", amount=1),
            inst("202609", "ecs", "i-addc", nick="ADDC-DC01", rg="infra-prod",
                 spec="ecs.g7.xlarge", amount=1),
            inst("202609", "csk", "c-i", rg="infra-prod", amount=1),
            inst("202609", "nat", "ngw-i", rg="infra-prod", amount=1),
            inst("202609", "ntr", "tr-i", rg="infra-prod", amount=1),
            inst("202609", "privatelink", "pl-i", rg="infra-prod", amount=1),
            inst("202609", "pvtz", "pz-i", rg="infra-prod", amount=1),
            inst("202609", "disk", "d-i", rg="infra-prod", amount=1),
        ]
        arch = self._agg(rows)
        infra = self._band(arch, "infra")
        kinds = {col: sorted(c["kind"] for c in comps)
                 for col, comps in infra["layers"].items()}
        self.assertEqual(kinds["核心库"], ["mongo", "rds", "redis"])
        self.assertEqual(kinds["消息流"], ["kafka", "other", "rocketmq"])  # eventbridge=other
        self.assertEqual(kinds["分析同步"], ["adbpg", "dts", "maxcompute"])
        self.assertIn("nacos", kinds["治理注册"])
        self.assertTrue(any(c["id"].endswith("-addc")
                            for c in infra["layers"]["治理注册"]),
                        "ecs(ADDC) → 治理注册（规则 4）")
        self.assertIn("ack", kinds["容器网络"])
        # 列名必须是 schema 的五键，且不出现 v1 的「接入/计算/数据/消息/观测」
        self.assertTrue(set(infra["layers"]) <= set(aggregate.INFRA_COLUMNS))
        self.assertFalse(set(infra["layers"]) & {"接入", "计算", "数据", "消息", "观测"})

    def test_line_three_columns_and_shared_four(self):
        """LINE 三列、shared 四列（消息并入数据；业务泳道无 AI 列）。"""
        rows = [
            inst("202609", "slb", "nlb-g", rg="game-prod", amount=1),
            inst("202609", "fc", "prod-game-pmd-1", rg="game-prod", amount=1),
            inst("202609", "ons", "rmq-g;a;b;c", rg="game-prod", amount=1),
            inst("202609", "sfm", "ws-g", rg="game-prod", amount=1),
            inst("202609", "apigateway", "gw-c", rg="converge-prod", amount=1),
            inst("202609", "sfm", "ws-s", rg="converge-prod", amount=1),
        ]
        arch = self._agg(rows)
        game = self._band(arch, "game")
        self.assertTrue(set(game["layers"]) <= set(aggregate.LINE_COLUMNS))
        # 消息类并入数据列
        self.assertIn("rocketmq", [c["kind"] for c in game["layers"]["数据"]])
        # 业务泳道 AI 面落计算列（LINE 无 AI 键）
        self.assertNotIn("AI", game["layers"])
        self.assertIn("bailian", [c["kind"] for c in game["layers"]["计算"]])
        shared = self._band(arch, "shared")
        self.assertTrue(set(shared["layers"]) <= set(aggregate.SHARED_COLUMNS))
        self.assertIn("apigw", [c["kind"] for c in shared["layers"]["入口"]])
        self.assertIn("bailian", [c["kind"] for c in shared["layers"]["AI"]])

    def test_comp_id_col_slug_matches_placement(self):
        """规则 7：id 的列 slug 段必须与卡实际所在列/带一致（obs/edge 也认）。"""
        rows = [
            inst("202609", "slb", "nlb-g", rg="game-prod", amount=1),
            inst("202609", "sls", "1077748325118640;combos-report;ls;ap-southeast-1", rg="game-prod", amount=1),
            inst("202609", "rds", "pgm-i", rg="infra-prod", amount=1),
            inst("202609", "alikafka", "alikafka_i", rg="infra-prod", amount=1),
            inst("202609", "dts", "dts-i", rg="infra-prod", amount=1),
            inst("202609", "mse", "mse-i", rg="infra-prod", amount=1),
            inst("202609", "nat", "ngw-i", rg="infra-prod", amount=1),
            inst("202609", "sfm", "ws-s", rg="converge-prod", amount=1),
            inst("202609", "cdn", "1077;cn", rg="", amount=1),
        ]
        arch = self._agg(rows)
        col_by_slug = {v: k for k, v in aggregate.COL_SLUG.items()}
        for band in all_bands(arch):
            for col, comps in (band["layers"] or {}).items():
                for c in comps:
                    slug = c["id"].split("_")[1]
                    self.assertEqual(col_by_slug[slug], col,
                                     "%s 的列 slug 与实际列 %s 不符" % (c["id"], col))
                    self.assertTrue(c["id"].startswith(band["id"] + "_"),
                                    "%s 未以带名开头" % c["id"])
            for c in band["observe"]:
                self.assertEqual(c["id"].split("_")[1], "obs")
        for c in arch["edge"]["comps"]:
            self.assertEqual(c["id"].split("_")[1], "edge")
            self.assertTrue(c["id"].startswith("edge_"))

    def test_referenced_comps_survive_folding(self):
        """被 cross_links 引用的卡钉住，长尾折叠不许吞掉（id 契约才稳）。"""
        rows = [inst("202609", "rds", "pgm-%03d" % i, nick="db-%03d" % i,
                     rg="game-prod", amount=float(i + 1))
                for i in range(aggregate.MAX_COMPS_PER_LAYER + 5)]
        links = [{"from": "game_data_rds", "to": "game_data_rds_2",
                  "label": "读写分离缺口", "kind": "data"}]
        arch = aggregate.aggregate(
            {"meta": {"months": ["202609"], "months_complete": ["202609"]},
             "instance_rows": rows, "group_rows": []},
            months_complete=["202609"], cross_links=links)
        ids = [c["id"] for c in all_comps(arch)]
        self.assertIn("game_data_rds", ids, "被 cross_links 引用的卡不许进长尾")
        self.assertIn("game_data_rds_2", ids)
        self.assertEqual(arch["cross_links"], links)
        self.assertFalse([w for w in arch["meta"]["warnings"] if "未解析" in w])


@unittest.skipUnless(os.path.exists(os.path.join(os.path.dirname(HERE), "internal",
                                                  "risks_kunqi.json")),
                     "internal/ 真数据不在仓库（PUBLIC 红线），本地有则跑")
class TestRisksLoader(unittest.TestCase):
    def test_load_json(self):
        path = os.path.join(os.path.dirname(HERE), "internal", "risks_kunqi.json")
        risks = aggregate.load_risks(path)
        self.assertTrue(risks)
        levels = {r["level"] for r in risks}
        self.assertTrue(levels <= {"P0", "P1", "P2"})
        self.assertTrue(any(r["level"] == "P0" for r in risks))

    def test_unresolved_risk_leaves_trace(self):
        bad = [{"level": "P0", "target": "nope_nothing", "text": "找不到目标"}]
        arch = aggregate.aggregate(build_fixture(), months_complete=["202609", "202610"], risks=bad)
        self.assertIn("unresolved_risks", arch["meta"])
        self.assertTrue(any("未挂接" in w for w in arch["meta"]["warnings"]))


# 每个带允许的列 slug（arch_schema.md 规则 7 + LINE/SHARED/INFRA 节的列定义）
BAND_COL_SLUGS = {
    "shared": {"access", "compute", "data", "ai", "obs"},
    "infra": {"core", "msg", "ana", "gov", "net", "obs"},
    "edge": {"edge"},
}
LINE_COL_SLUGS = {"access", "compute", "data", "obs"}


@unittest.skipUnless(os.path.exists(os.path.join(os.path.dirname(HERE), "internal",
                                                  "risks_kunqi.json")),
                     "internal/ 真数据不在仓库（PUBLIC 红线），本地有则跑")
class TestConfigContract(unittest.TestCase):
    """config/risks_kunqi.json 与 config/cross_links_kunqi.json 的 v2 id 契约。

    真账单不在仓库里，这里做静态校验：id 的 (带, 列slug) 组合必须是该带在 v2
    结构下真实存在的列 —— v1 遗留写法（infra_access_eip / infra_data_dts /
    game_msg_rocketmq）在 v2 里列名变了，会在这一步直接红。
    """

    @staticmethod
    def _load(name):
        path = os.path.join(os.path.dirname(HERE), "internal", name)
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    def _check_id(self, comp_id):
        parts = comp_id.split("_")
        self.assertGreaterEqual(len(parts), 3, "id 不是 <band>_<col>_<slug>：%s" % comp_id)
        band, col = parts[0], parts[1]
        allowed = BAND_COL_SLUGS.get(
            band, LINE_COL_SLUGS if band in aggregate.LINE_ORDER else None)
        self.assertIsNotNone(allowed, "未知带 %s（id=%s）" % (band, comp_id))
        self.assertIn(col, allowed,
                      "%s 带无列 slug %s（v2 列迁移未同步，id=%s）" % (band, col, comp_id))
        self.assertTrue("_".join(parts[2:]), "id 缺族 slug 段：%s" % comp_id)

    def test_risks_targets_are_v2_ids(self):
        risks = self._load("risks_kunqi.json")["risks"]
        for risk in risks:
            self._check_id(risk["target"])
            self.assertEqual(risk.get("line"), risk["target"].split("_")[0],
                             "%s 的 line 与 target 带名不一致" % risk["target"])
            self.assertIn(risk["level"], ("P0", "P1", "P2"))
            self.assertTrue(risk["text"])
        levels = {}
        for risk in risks:
            levels.setdefault(risk["level"], []).append(risk["target"])
        self.assertEqual(sorted(levels), ["P0", "P1", "P2"])
        self.assertEqual(len(levels["P0"]), 4, levels["P0"])
        self.assertEqual(len(levels["P1"]), 4, levels["P1"])
        self.assertEqual(len(levels["P2"]), 4, levels["P2"])

    def test_risks_semantics_preserved(self):
        """v1→v2 迁移只改 target id，12 条风险语义不变。"""
        by_target = {r["target"]: r for r in self._load("risks_kunqi.json")["risks"]}
        expect = {
            "enter_data_redis": "P0", "game_data_rds_2": "P0",
            "infra_ana_dts": "P0", "infra_gov_ecs-ecs-e-addc": "P0",
            "enter_compute_supabase-pool": "P1", "infra_msg_kafka": "P1",
            "shared_ai_ws": "P1", "infra_net_eip": "P1",
            "enter_obs_sls-enter": "P2", "shared_obs_other-hdm": "P2",
            "infra_obs_prom": "P2", "infra_core_rds_2": "P2",
        }
        self.assertEqual({k: v["level"] for k, v in by_target.items()}, expect)

    def test_cross_links_are_v2_ids(self):
        links = self._load("cross_links_kunqi.json")
        self.assertEqual(len(links), 12, "坤启 12 条跨带连线")
        for link in links:
            self._check_id(link["from"])
            self._check_id(link["to"])
            self.assertTrue(link["label"])
            self.assertIn(link["kind"], ("data", "ai", "msg"))
            self.assertNotEqual(link["from"], link["to"])

    def test_cross_links_semantics_preserved(self):
        """12 条连线语义（起终点带 + 类型）保持不变。"""
        pairs = [(l["from"], l["to"], l["kind"])
                 for l in self._load("cross_links_kunqi.json")]
        self.assertIn(("enter_compute_prod-coding-agent", "shared_data_adbpg", "data"), pairs)
        self.assertIn(("enter_compute_prod-coding-agent", "shared_ai_ws", "ai"), pairs)
        self.assertIn(("framia_compute_prod-video-agent", "shared_ai_ws", "ai"), pairs)
        self.assertIn(("framia_compute_prod-video-agent", "shared_data_oss", "data"), pairs)
        self.assertIn(("game_compute_prod-game-pmd", "infra_msg_kafka", "msg"), pairs)
        self.assertIn(("game_compute_prod-game-pmd", "game_data_mongo", "data"), pairs)
        self.assertIn(("shared_access_apigw", "enter_access_nlb-pub-app", "data"), pairs)
        self.assertIn(("shared_access_apigw", "game_access_nlb-pri-gateway", "data"), pairs)
        self.assertIn(("infra_ana_dts", "shared_data_adbpg", "data"), pairs)
        self.assertIn(("game_data_rocketmq", "infra_ana_maxcompute", "data"), pairs)
        self.assertIn(("shared_ai_ws", "shared_data_memory-pool", "ai"), pairs)

    def test_configs_resolve_against_fixture_arch(self):
        """把两份 config 喂给 fixture 聚合链：不产生「未解析」warnings。

        fixture 只有 9 张卡，命中不到的 target 会被 line/kind/evidence 模糊解析
        兜住或落 warnings —— 这里只断言 config 格式合法（能加载、无语法错），
        真实全解析在真账单验收链上核（见 SKILL 的验收步骤）。
        """
        risks = aggregate.load_risks(
            os.path.join(os.path.dirname(HERE), "internal", "risks_kunqi.json"))
        links = aggregate.load_cross_links(
            os.path.join(os.path.dirname(HERE), "internal", "cross_links_kunqi.json"))
        self.assertEqual(len(risks), 12)
        self.assertEqual(len(links), 12)


class TestCLI(unittest.TestCase):
    def test_cli_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            raw_path = os.path.join(td, "bills_raw.json")
            out_path = os.path.join(td, "arch.json")
            risks_path = os.path.join(td, "risks.json")
            with open(raw_path, "w", encoding="utf-8") as fh:
                json.dump(build_fixture(), fh, ensure_ascii=False)
            with open(risks_path, "w", encoding="utf-8") as fh:
                json.dump({"risks": RISKS}, fh, ensure_ascii=False)
            rc = subprocess.call([
                sys.executable, os.path.join(SCRIPTS, "aggregate.py"),
                "--in", raw_path, "--out", out_path,
                "--months-complete", "202609,202610",
                "--risks", risks_path,
            ])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(out_path))
            with open(out_path, encoding="utf-8") as fh:
                arch = json.load(fh)
            self.assertEqual(arch["meta"]["months"], ["202609", "202610"])
            self.assertTrue(arch["lines"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
