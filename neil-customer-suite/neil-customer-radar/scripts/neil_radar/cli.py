"""CLI 装配：唯一对外执行入口，不写业务逻辑。"""
import argparse

from . import analyze as analyze_mod
from . import collect as collect_mod
from . import render_dashboard as dash_mod
from . import seed as seed_mod
from . import store as store_mod


def build_parser():
    parser = argparse.ArgumentParser(prog="neil_radar", description="客户资源雷达")
    parser.add_argument("--config", default=None, help="统一客户表路径（默认套件 config）")
    sub = parser.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("collect", help="分组问数采集日快照")
    pc.add_argument("--date", default=None, help="跑批日 YYYY-MM-DD（默认今天）")
    pc.add_argument("--range-days", type=int, default=None, help="统计日窗口天数")
    pc.add_argument("--out-dir", default=None)
    pc.set_defaults(func=collect_mod.cmd_collect)
    ps = sub.add_parser("seed", help="拉报表全量客户清单出合并报告")
    ps.add_argument("--out-dir", default=None)
    ps.set_defaults(func=seed_mod.cmd_seed)
    pst = sub.add_parser("store", help="生成 dws 写计划（agent 逐条执行）")
    pst.add_argument("--snapshot", required=True, help="snapshot-<date>.json 路径")
    pst.add_argument("--customers", default=None, help="逗号分隔客户 key（默认全部）")
    pst.add_argument("--field-ids", default=None, help="字段名→fieldId JSON（agent 回读填入）")
    pst.add_argument("--out-dir", default=None)
    pst.set_defaults(func=store_mod.cmd_store)
    pa = sub.add_parser("analyze", help="历史序列出客户动态事件+事件写计划")
    pa.add_argument("--customers", default=None)
    pa.add_argument("--field-ids", default=None)
    pa.add_argument("--out-dir", default=None)
    pa.set_defaults(func=analyze_mod.cmd_analyze)
    pd = sub.add_parser("dashboard", help="重生式刷新单文件 HTML 看板")
    pd.add_argument("--out-dir", default=None)
    pd.add_argument("--force", action="store_true", help="无视 hash 强制重写")
    pd.set_defaults(func=dash_mod.cmd_dashboard)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
