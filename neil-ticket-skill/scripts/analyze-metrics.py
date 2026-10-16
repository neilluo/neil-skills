#!/usr/bin/env python3
"""只读机械度量（扫描整个 scripts/neil_ticket 包 + shim scripts/ticket.py）：

1) 重复块：逐行去全部空白后，长度>=4 的滑动窗口哈希；分「模块内」与「跨模块」，
   红线＝跨模块重复行占比 <5%；另做 包↔tests 跨文件对照（原 ticket↔tests 保留）。
2) 死代码：全包 ast——顶层定义名在 包/shim/tests 中均无引用即死代码（红线＝空）；
   __init__ 重导出与 shim 星号导入不算「引用」，仅经该通道或 tests T.x 可达的名字
   单列「仅重导出/兼容引用」（允许项）。含各模块未使用 import、赋值未读局部变量。
3) 函数长度：全包 FunctionDef 行数 top5 与 >40 行数（红线，AGENTS.md 规则 K）。

用法：python3 scripts/analyze-metrics.py
"""
import ast
import hashlib
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG_DIR = os.path.join(BASE, "scripts", "neil_ticket")
SHIM = os.path.join(BASE, "scripts", "ticket.py")
REG = os.path.join(BASE, "tests", "run-regression.py")
WIN = 4
MODULES = ["__init__", "config", "transport", "parse", "gate", "render",
           "collect", "publish", "cli"]
PKG_FILES = [os.path.join(PKG_DIR, m + ".py") for m in MODULES]
ALL_FILES = PKG_FILES + [SHIM]


def rel(path):
    return os.path.relpath(path, BASE)


def norm_lines(path):
    """返回 [(原始行号, 去空白内容)]，跳过空行。"""
    out = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            s = re.sub(r"\s+", "", line)
            if s:
                out.append((i, s))
    return out


def win_hashes(lines):
    h = defaultdict(list)
    for i in range(len(lines) - WIN + 1):
        key = hashlib.md5(
            "\x00".join(x[1] for x in lines[i:i + WIN]).encode()).hexdigest()
        h[key].append(i)
    return h


def _fmt_occ(lines, occ):
    return ", ".join(f"{rel(f)}:L{lines[f][i][0]}-L{lines[f][i + WIN - 1][0]}"
                     for f, i in occ)


def report_dup():
    lines = {f: norm_lines(f) for f in ALL_FILES}
    total = sum(len(v) for v in lines.values())
    occ = defaultdict(list)
    for f in ALL_FILES:
        for key, idxs in win_hashes(lines[f]).items():
            occ[key].extend((f, i) for i in idxs)
    intra, cross = [], []
    intra_marks, cross_marks = set(), set()
    for key, o in occ.items():
        if len(o) < 2:
            continue
        group = sorted(o)
        marks = {(f, j) for f, i in group for j in range(i, i + WIN)}
        if len({f for f, _ in group}) >= 2:
            cross.append(group)
            cross_marks |= marks
        else:
            intra.append(group)
            intra_marks |= marks
    print(f"== 重复度（neil_ticket 全包 {len(PKG_FILES)} 模块 + shim，总有效行数 {total}）==")
    print(f"模块内长度>={WIN}重复块组数: {len(intra)}")
    for g in sorted(intra, key=lambda g: g[0]):
        print("  " + _fmt_occ(lines, g))
    print(f"跨模块长度>={WIN}重复块组数: {len(cross)}")
    for g in sorted(cross, key=lambda g: g[0]):
        print("  " + _fmt_occ(lines, g))
    pct_cross = 100.0 * len(cross_marks) / total
    pct_all = 100.0 * len(intra_marks | cross_marks) / total
    print(f"跨模块重复行占比: {pct_cross:.2f}%（红线 <5%）{'PASS' if pct_cross < 5 else 'FAIL'}")
    print(f"全部重复行占比(含模块内): {pct_all:.2f}%  冗余行(每组留一份): "
          f"{len(intra_marks | cross_marks) - len({(f, j) for g in intra + cross for f, i in [g[0]] for j in range(i, i + WIN)})}")
    return pct_cross


def report_cross_with_tests():
    lb = norm_lines(REG)
    hb = win_hashes(lb)
    common = []
    for f in ALL_FILES:
        la = norm_lines(f)
        for key, idxs in win_hashes(la).items():
            if key in hb:
                common.append((f, idxs, hb[key]))
    print(f"\n== 包↔tests 跨文件重复（长度>={WIN}）==")
    print(f"共同归一化块: {len(common)}")
    for f, ia, ib in common:
        la = norm_lines(f)
        print(f"  {rel(f)}:L{la[ia[0]][0]} <-> tests:L{lb[ib[0]][0]}")


def _module_defs(tree):
    defs = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs.append((node.lineno, node.name))
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs.append((node.lineno, t.id))
    return defs


def _loaded_names(tree):
    return {n.id for n in ast.walk(tree)
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}


def _alias_attrs(tree, alias):
    return {n.attr for n in ast.walk(tree)
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
            and n.value.id == alias}


def report_dead():
    trees = {f: ast.parse(open(f, encoding="utf-8").read()) for f in ALL_FILES + [REG]}
    loaded_any = set()
    for f in ALL_FILES + [REG]:
        loaded_any |= _loaded_names(trees[f])
    test_attrs = _alias_attrs(trees[REG], "T")
    init_path = os.path.join(PKG_DIR, "__init__.py")
    reexport = set()
    for node in ast.walk(trees[init_path]):
        if isinstance(node, ast.ImportFrom):
            reexport |= {a.name for a in node.names if a.name != "*"}

    print("\n== 死代码（全包 ast：包模块 + shim + tests 引用闭包）==")
    dead, only_reexport = [], []
    for f in PKG_FILES:
        if f == init_path:
            continue  # __init__ 职责即重导出，不判死代码
        for ln, name in _module_defs(trees[f]):
            if name.startswith("__"):
                continue
            if name in loaded_any:
                continue
            if name in reexport or name in test_attrs:
                only_reexport.append((rel(f), ln, name))
            else:
                dead.append((rel(f), ln, name))
    print("死代码（包/shim/tests 均无引用）:")
    for where, ln, name in dead:
        print(f"  {where}:L{ln}: {name}")
    if not dead:
        print("  （无）PASS")
    else:
        print(f"  FAIL：{len(dead)} 个")
    print("仅 __init__ 重导出 / tests 兼容引用（允许项）:")
    for where, ln, name in only_reexport:
        print(f"  {where}:L{ln}: {name}")
    if not only_reexport:
        print("  （无）")

    print("未使用 import（__init__ 重导出职责除外）:")
    found = False
    for f in ALL_FILES:
        if f == init_path:
            continue
        loaded = _loaded_names(trees[f])
        for node in ast.walk(trees[f]):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    name = (alias.asname or alias.name).split(".")[0]
                    if name not in loaded:
                        found = True
                        print(f"  {rel(f)}:L{node.lineno}: {name}")
    if not found:
        print("  （无）")

    print("赋值后从未读取的局部变量:")
    found = False
    for f in ALL_FILES:
        for fn in [n for n in ast.walk(trees[f]) if isinstance(n, ast.FunctionDef)]:
            params = {a.arg for a in fn.args.args + fn.args.kwonlyargs}
            if fn.args.vararg:
                params.add(fn.args.vararg.arg)
            if fn.args.kwarg:
                params.add(fn.args.kwarg.arg)
            local_loaded, stores = set(), []
            for node in ast.walk(fn):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Load):
                        local_loaded.add(node.id)
                    elif isinstance(node.ctx, ast.Store):
                        stores.append((node.lineno, node.id))
            for ln, name in stores:
                if name in params or name.startswith("_") or name in local_loaded:
                    continue
                found = True
                print(f"  {rel(f)} {fn.name}() L{ln}: {name}")
    if not found:
        print("  （无）")
    return dead, only_reexport


def func_lengths_pkg(topn=5):
    fns = []
    for f in PKG_FILES:
        tree = ast.parse(open(f, encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fns.append((node.end_lineno - node.lineno + 1, node.name,
                            rel(f), node.lineno, node.end_lineno))
    fns.sort(reverse=True)
    over40 = [x for x in fns if x[0] > 40]
    print(f"\n== 函数长度 top{topn}（neil_ticket 全包，共 {len(fns)} 个函数）==")
    for n, name, where, a, b in fns[:topn]:
        print(f"  {n:4d} 行  {name}  {where}:L{a}-L{b}")
    print(f"函数体总行数 {sum(x[0] for x in fns)}；>40 行函数 {len(over40)} 个"
          f"（红线＝0）{'PASS' if not over40 else 'FAIL'}；"
          f">30 行 {sum(1 for x in fns if x[0] > 30)} 个")
    return fns[:topn], over40


if __name__ == "__main__":
    pct_cross = report_dup()
    report_cross_with_tests()
    dead, only_re = report_dead()
    top5, over40 = func_lengths_pkg()
    print("\n== 红线汇总 ==")
    print(f"跨模块重复行占比 {pct_cross:.2f}% (<5%): {'PASS' if pct_cross < 5 else 'FAIL'}")
    print(f"死代码 {len(dead)} 个（须为空或仅 __init__ 重导出，仅重导出 {len(only_re)} 个）: "
          f"{'PASS' if not dead else 'FAIL'}")
    print(f"top5 函数行数 {[x[0] for x in top5]} (≤40): "
          f"{'PASS' if not over40 else 'FAIL'}")
