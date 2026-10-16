"""配置层：路径常量、customers.json 读取、时区解析、时间窗与 --customers 过滤。
依赖链最底层，不 import 包内其他层。扩展时改这里：新增配置键必须同批落地
消费代码与回归断言（AGENTS.md 规则 J）；文档标题模式改 doc_title；
路径/输出目录常量（SKILL_DIR/CONFIG_PATH/TEMPLATE_PATH/OUT_DIR）在此维护。"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "customers.json")
TEMPLATE_PATH = os.path.join(SKILL_DIR, "templates", "daily-report.md")
OUT_DIR = os.path.join(SKILL_DIR, "outputs")

_TZ_CACHE = {}


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def tz_of(key):
    """'+08:00' → timezone（纯解析带缓存）。render 等纯函数经参数拿 tz，不再读盘。"""
    if key not in _TZ_CACHE:
        m = re.match(r"([+-])(\d{2}):(\d{2})", key)
        sign = 1 if m.group(1) == "+" else -1
        _TZ_CACHE[key] = timezone(sign * timedelta(hours=int(m.group(2)),
                                                   minutes=int(m.group(3))))
    return _TZ_CACHE[key]


def cfg_tz():
    return tz_of(load_config().get("timezone", "+08:00"))


def window_of(date_str, tz=None):
    day = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=tz or cfg_tz())
    start = day.strftime("%Y-%m-%d 00:00:00")
    end = (day + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
    return start, end


def select_customers(cfg, spec):
    """--customers 逗号过滤 + 判空退出（cmd_collect / cmd_publish 共用，评审消重复）。"""
    customers = [c for c in cfg["customers"]
                 if not spec or c["key"] in spec.split(",")]
    if not customers:
        sys.exit(f"--customers 无匹配：{spec}")
    return customers


def doc_title(cfg, date_str):
    """doc_title_pattern 配置激活（原死配置零引用键），缺省与原硬编码等价。"""
    pattern = cfg.get("doc_title_pattern", "{yyyymmdd}工单")
    return pattern.format(yyyymmdd=date_str.replace("-", ""))
