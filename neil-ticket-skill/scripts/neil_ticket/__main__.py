"""python3 -m neil_ticket 入口：转发 cli.main（包唯一对外执行入口）。
scripts/ 下直接 `python3 -m neil_ticket <子命令>`；skill 根目录需
`PYTHONPATH=scripts python3 -m neil_ticket <子命令>`（-m 的包发现早于本文件执行）。
与 shim scripts/ticket.py 等价，退出码语义一致（check：0=完成/3=缺失或过期/1=异常）。"""
from .cli import main

main()
