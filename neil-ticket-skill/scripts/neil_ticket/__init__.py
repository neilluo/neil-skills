"""neil_ticket 包公共 API 重导出（原单文件 scripts/ticket.py 的全部公共名）。

七层物理分层与依赖方向（只准向下依赖，禁循环）：
config ← transport ← parse ← gate ← render ← collect/publish ← cli。
兼容 shim scripts/ticket.py 经 `from neil_ticket import *` 重导出本文件；
扩展时改对应下层模块，仅新增跨层公共名时在此补一行重导出并同步 __all__。
"""
from .config import (CONFIG_PATH, OUT_DIR, SKILL_DIR, TEMPLATE_PATH, _TZ_CACHE,
                     cfg_tz, doc_title, load_config, select_customers, tz_of,
                     window_of)
from .transport import (DWS, RETRY_AUTH, RETRY_CREATE, RETRY_EMPTY_PAGE,
                        RETRY_TRANSPORT, AccessDenied, _RE_130003,
                        _access_denied, _paginate, _scan_envelope, fetch_page,
                        run_dws)
from .parse import (PRODUCTION_KEYWORDS, RE_CONFIRM, RE_CONV_ID, RE_CREATE,
                    RE_CREATOR, RE_DESC, RE_DONE, RE_SOL, RE_STATUS, RE_TID,
                    RE_TITLE_FONT, RE_TITLE_PLAIN, RE_URGE, RE_XIAOER,
                    SAFETY_KEYWORDS, _apply_create, _apply_done,
                    _blank_ticket, _days_span, _detect_urge, _is_stalled,
                    _last_active, _note_subgroup, _ticket_open_date,
                    compute_attention, compute_signals, compute_urgency_signals,
                    double_unquote, parse_cards)
from .gate import (EFFECTIVE_ENUM, MAX_BULLETS, SENTIMENT_ENUM,
                   SENTIMENT_NEEDS_EVIDENCE, _RE_TS_PREFIX, _allowed_ids,
                   _evidence_bad, _norm, default_effective,
                   lint_process_bullets, sanitize_sentiment, sanitize_summary)
from .render import (_attention_map, _attention_rows, _attention_section,
                     _carryover_ticket_section, _effective, _evidence_text,
                     _overview_row, _render_values, _rows_and_sections,
                     _sentiment_level, _sentiment_line, _ticket_section, _urgency,
                     carryover_section, esc_cell, esc_prose, render,
                     verification_markers)
from .collect import (LIMIT, MAX_PAGES, PROBE_MAX_PAGES, PROBE_MSG_CAP,
                      _auto_join_gap, _build_slice, _merged_signals, _probe_ticket,
                      _report_collect, cmd_collect, collect_one, probe_subgroup,
                      read_messages, resolve_cid_by_name)
from .publish import (FOLLOWUP_DAYS, _bullets_note, _carryover_data,
                      _doc_folder_id, _folder_warning, _load_prev_collects,
                      _load_summary_and_texts, _reage_urgency, _update_doc,
                      _verify_written, _watermark, _write_run_marker, check_status,
                      cmd_check, cmd_publish, create_doc_idempotent,
                      doc_markdown, followup_section, list_nodes, publish_one)
from .cli import main

__all__ = [
    # config
    "SKILL_DIR", "CONFIG_PATH", "TEMPLATE_PATH", "OUT_DIR", "_TZ_CACHE",
    "load_config", "tz_of", "cfg_tz", "window_of", "select_customers",
    "doc_title",
    # transport
    "DWS", "RETRY_TRANSPORT", "RETRY_EMPTY_PAGE", "RETRY_AUTH", "RETRY_CREATE",
    "AccessDenied", "_RE_130003", "_scan_envelope", "_access_denied",
    "run_dws", "fetch_page", "_paginate",
    # parse
    "double_unquote", "RE_CREATE", "RE_DONE", "RE_CREATOR", "RE_TITLE_FONT",
    "RE_TITLE_PLAIN", "RE_TID", "RE_STATUS", "RE_XIAOER", "RE_CONV_ID",
    "RE_DESC", "RE_SOL", "RE_CONFIRM", "RE_URGE", "SAFETY_KEYWORDS",
    "PRODUCTION_KEYWORDS", "_blank_ticket", "_apply_create", "_apply_done",
    "_note_subgroup", "parse_cards", "compute_signals", "_ticket_open_date",
    "_days_span", "_last_active", "_is_stalled", "_detect_urge",
    "compute_urgency_signals", "compute_attention",
    # gate
    "EFFECTIVE_ENUM", "default_effective", "_norm", "sanitize_summary",
    "MAX_BULLETS", "_RE_TS_PREFIX", "lint_process_bullets", "SENTIMENT_ENUM",
    "SENTIMENT_NEEDS_EVIDENCE", "_allowed_ids", "_evidence_bad", "sanitize_sentiment",
    # render
    "esc_cell", "esc_prose", "_effective", "_evidence_text", "_overview_row",
    "_ticket_section", "_carryover_ticket_section", "carryover_section",
    "render", "verification_markers", "_urgency", "_sentiment_level",
    "_attention_map", "_attention_rows", "_attention_section", "_sentiment_line",
    "_rows_and_sections", "_render_values",
    # collect
    "LIMIT", "MAX_PAGES", "PROBE_MAX_PAGES", "PROBE_MSG_CAP", "read_messages",
    "probe_subgroup", "resolve_cid_by_name", "_probe_ticket", "collect_one",
    "_build_slice", "_merged_signals", "_auto_join_gap", "_report_collect",
    "cmd_collect",
    # publish
    "FOLLOWUP_DAYS", "list_nodes", "doc_markdown", "_doc_folder_id",
    "_folder_warning", "create_doc_idempotent", "followup_section",
    "_carryover_data", "_load_prev_collects", "_load_summary_and_texts",
    "_bullets_note", "_watermark", "_reage_urgency", "_update_doc",
    "_verify_written", "publish_one", "cmd_publish", "_write_run_marker",
    "check_status", "cmd_check",
    # cli
    "main",
]
