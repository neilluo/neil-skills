#!/usr/bin/env python3
"""兼容 shim：原单文件 ticket.py 已拆为物理分层包 scripts/neil_ticket/
（config ← transport ← parse ← gate ← render ← collect/publish ← cli，见 AGENTS.md）。

本文件只保兼容、不写业务：`python3 scripts/ticket.py collect/publish ...` 与
`import ticket as T` 的既有用法零改动；T.fetch_page / T.MAX_PAGES 等 monkeypatch
写入会转发到包内所有持有该名字的模块（等价旧单文件共享全局命名空间）。
新代码请直接 import neil_ticket 对应层模块。
"""
import os
import sys
import types

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import neil_ticket  # noqa: E402
from neil_ticket import *  # noqa: E402,F401,F403
from neil_ticket.cli import main  # noqa: E402,F401


def _build_owners():
    """公共名 → 包内所有持有该名字的模块（定义处 + from-import 引用处）。"""
    owners = {}
    for mod in (neil_ticket.config, neil_ticket.transport, neil_ticket.parse,
                neil_ticket.gate, neil_ticket.render, neil_ticket.collect,
                neil_ticket.publish, neil_ticket.cli):
        for name, val in vars(mod).items():
            if name.startswith("__") or isinstance(val, types.ModuleType):
                continue
            owners.setdefault(name, []).append(mod)
    return owners


_OWNERS = _build_owners()


class _TicketShim(types.ModuleType):
    """模块级 __setattr__：对公共名的写入转发到包内模块，保 monkeypatch 语义。"""

    def __setattr__(self, name, value):
        for mod in _OWNERS.get(name, ()):
            setattr(mod, name, value)
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _TicketShim

if __name__ == "__main__":
    sys.exit(main())
