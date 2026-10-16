MCP issues detected. Run /mcp list for status.
# 第四轮验收评审报告（只读）

## 红线度量（outputs/analyze-metrics.py 实跑）
| 红线 | 结果 | 证据 |
|---|---|---|
| 跨模块归一化重复块占比 <5% | **0.00% PASS** | 920 行 9 模块 + shim，跨模块重复组 0 |
| 死代码 =0 | **PASS** | 死代码/仅重导出/未用 import/未读局部变量 全无 |
| >40 行函数 =0 | **PASS** | top5 行数 [35,35,34,34,33]，>30 行 6 个（render/parse_cards/sanitize_summary/cmd_collect/publish_one） |

## 逐项验收
1. 重复度：0.00%（红线 <5% 远松）。
2. 死代码：AST 闭包扫描后包/shim/tests 全部可达，无未读 import、无未读配置键（rule J 已被 reference.md:80-83 配置消费表覆盖）。
3. 命令风格：subprocess.run 仅 transport.py:70；8 处 `require=` 全部为形状校验（`isinstance(d.get("result"), dict)`/`"messages" in d`/`isinstance(d.get("nodes"), list)`/`"markdown" in d`/`bool(_doc_folder_id(d))`/`isinstance(d, dict)`），无 `lambda d: True`，success 判定全在调用方（collect.py:157、publish.py:165）。`RETRY_TRANSPORT/EMPTY_PAGE/AUTH/CREATE=3/2/2/1` 集中于 transport.py:20-23；除 transport.py 外只有 fetch_page 与 create_doc_idempotent 外层按常量引用。
4. 架构分层：in-pkg import 矩阵 render→{config,gate} / collect→{config,parse,transport} / publish→{config,gate,render,transport} / cli→{collect,publish}，config/transport/parse/gate 包内零依赖，无循环。规则 P 四条扩展契约（加客户=仅 customers.json；加事件类型=parse+template+fixtures+reference.md；加输出目标=publish +cli；换传输=仅 transport）均成立。
5. 内聚：rule L 四处同批清单合理——加催单事件需 parse_cards 分支 + templates/daily-report.md 头表 + tests/fixtures + regression 断言 + reference.md「工单事件报文解剖」节，reference.md:5、18、53-54 均已前瞻预留催单采样路径。
6. 冗长方法：6 个 30-35 行函数均为「规则驱动、分支不多但语义必要」（render 调度 8 个 {{token}} + 子节判定；parse_cards 4 分支 + 2 哨兵；gate 三重门禁 + 留痕），均无 ≤10 行可写完却写很长的情况。
7. 规范沉淀抽查 12 条（A-P 全覆盖）：
   - A:C/E/F/P/H/I/J/K/M/N/L/O 已落地代码一一对应；B: 仅 transport.py:74/85/89/93/114 五处 `time.sleep`；C: 数字边界正则 transport.py:40 + 嵌套信封 _scan_envelope transport.py:43-55；D: --direction older transport.py:107 + 三段警告 142/147；G: str.replace render.py:103-104 + esc_cell/esc_prose；无不一致项。
   - 应沉淀未沉淀：FINDING-无。reference.md:53 已标「催单事件未建模」明确采样门槛，规则 M 闭环。

## 残留缺陷表
| 优先级 | 项 | 位置 | 说明 |
|---|---|---|---|
| P0 | 无 | — | 0 |
| P1 | render.py:_evidence_text 仅 1 处调用，可并入 render | render.py:26-36 | 内联可省一层抽象（≤10 行），不影响功能 |
| P1 | publish._doc_folder_id 容错提取（三层信封）未单测 | publish.py:41-48 | 现有回归只在 _folder_warning 整体跑；可补一行单测 |
| P2 | AccessDenied.label 子串扫描 stdout 文本 | transport.py:31-37 | rule C 允许 stderr 文本路径，但 label 判断发生在 AccessDenied 构造而非 _scan_envelope；可改为只看 stderr |
| P2 | 6 函数 >30 行 | render/parse/gate/collect/publish 各 1 | rule K ≤40 已通过，逼近红线，下次拆随业务变更自然触发 |

## 结论：第四轮交付通过，无 P0/P1 阻断项；进入 `simplify` 与规则 L 沉淀验收可同步推进。
