"""配置层：套件根解析、凭据三级解析（env → 私有文件 → 报错）、统一客户表读取。
依赖链最底层，不 import 包内其他层。凭据字面值禁止入库（仓库 PUBLIC）。"""
import json
import os

SUITE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
CONFIG_PATH = os.path.join(SUITE_DIR, "config", "customers.json")
TZ = "+08:00"


class ConfigError(Exception):
    pass


def load_config(path=None):
    with open(path or CONFIG_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def resolve_credentials(cfg):
    """返回 (token, assistant_id)。顺序：环境变量 ACCESS_TOKEN(JSON) →
    credentials.fallback_file → ConfigError。字面值只存在于仓库外。"""
    raw = os.environ.get("ACCESS_TOKEN", "")
    if raw:
        try:
            blob = json.loads(raw)
            tok, aid = blob.get("fbi_token"), blob.get("fbi_assistant_id")
            if tok and aid:
                return tok, aid
        except ValueError:
            pass
    fallback = os.path.expanduser(cfg.get("credentials", {}).get("fallback_file", ""))
    if fallback and os.path.exists(fallback):
        with open(fallback, encoding="utf-8") as fh:
            blob = json.load(fh)
        tok, aid = blob.get("fbi_token"), blob.get("fbi_assistant_id")
        if tok and aid:
            return tok, aid
    raise ConfigError("未解析到 FBI 凭据：设 ACCESS_TOKEN 或落 credentials.fallback_file")


def chatbi_cfg(cfg):
    """合成 chatbi 传输层需要的 cfg（server_domain/token/assistant_id/session 参数）。"""
    token, assistant_id = resolve_credentials(cfg)
    merged = dict(cfg.get("chatbi", {}))
    merged.update({"server_domain": merged.get("server_domain", "https://fbi.alibaba-inc.com"),
                   "token": token, "assistant_id": assistant_id})
    return merged


def customers(cfg, keys=None, daily_only=False):
    """客户列表；keys 过滤 / daily_only 只取 radar.daily_watch。"""
    out = []
    for cust in cfg.get("customers", []):
        if keys and cust["key"] not in keys:
            continue
        if daily_only and not cust.get("radar", {}).get("daily_watch"):
            continue
        out.append(cust)
    return out


def customer_by_key(cfg, key):
    for cust in cfg.get("customers", []):
        if cust["key"] == key:
            return cust
    raise ConfigError(f"客户不存在：{key}")


def thresholds(cfg):
    return cfg.get("thresholds", {})


def field_of(cfg, section, key):
    """metrics 段按 key 取报表字段名（精确匹配，禁包含兜底——weekly 陷阱 5）。"""
    for item in cfg.get(section, []):
        if item["key"] == key:
            return item["field"]
    raise ConfigError(f"{section} 无指标 {key}")
