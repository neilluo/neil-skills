"""CLI 入口层：argparse 子命令装配（collect / publish / check），唯一对外执行入口，契约不变。
本文件不写业务逻辑；新增子命令在此装配并把实现放下层（采集归 collect、发布与完成判定
归 publish、新职责先选层再落地）；flag 变更须同批更新 SKILL.md 用法示例。"""
import argparse

from .collect import cmd_collect
from .publish import cmd_check, cmd_publish


def main():
    parser = argparse.ArgumentParser(prog="ticket.py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_collect = sub.add_parser("collect", help="采集工单事件与子群探读")
    p_collect.add_argument("--date", required=True, help="工单日 YYYY-MM-DD")
    p_collect.add_argument("--customers", help="逗号分隔 customer key，缺省全部")
    p_collect.set_defaults(fn=cmd_collect)
    p_publish = sub.add_parser("publish", help="渲染并写入 alidocs 日报")
    p_publish.add_argument("--date", required=True, help="工单日 YYYY-MM-DD")
    p_publish.add_argument("--customers", help="逗号分隔 customer key，缺省全部")
    p_publish.add_argument("--force", action="store_true", help="覆盖非空文档")
    p_publish.set_defaults(fn=cmd_publish)
    p_check = sub.add_parser("check", help="机械判定当日跑批完成标记（纯读，无网络/写）")
    p_check.add_argument("--date", required=True, help="工单日 YYYY-MM-DD")
    p_check.set_defaults(fn=cmd_check)
    args = parser.parse_args()
    args.fn(args)
