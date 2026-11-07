/* ============================================================================
 * fetch_bills.js —— neil-kunpeng-expert 账单抽取（粘贴到 usercenter2 页签 console）
 *
 * 用途：按配置对象逐月 × 逐产品拉实例级、逐月 × 逐资源组拉 group 级、逐月拉
 *       PRODUCT/ACCOUNT 级账单，组装成 {meta, instance_rows, group_rows,
 *       product_rows, saturation} 一次性 POST 到本地 recv_server.py 落盘。
 *
 * ⚠ 必须在 https://usercenter2.aliyun-inc.com/ 域内的页签执行：
 *   1) crm360 与 usercenter2 跨域不通，商品级也走本域的 PRODUCT_CONSUME_MONTH；
 *   2) X-CSRF-TOKEN 从当前页 HTML 内联脚本里正则提取。
 *
 * 零第三方依赖，只用浏览器原生 fetch。重跑覆盖（幂等）。单产品失败不中断。
 *
 * 用法：整段粘贴进 console 回车。改 CONFIG 里的 uid/months/groups/products 即可。
 * ========================================================================== */
(async function neilKunpengFetchBills() {
  'use strict';

  // --------------------------------------------------------------------------
  // CONFIG —— 唯一需要改的地方
  // --------------------------------------------------------------------------
  const CONFIG = {
    uid: '1077748325118640',                       // 客户 UID（loginUserId）
    months: ['202609', '202610', '202611'],         // 要拉的账期；跨月逐月并集
    monthsComplete: ['202609', '202610'],           // 参与月均的完整月（残缺月如 202611 只进证据）
    groups: [                                        // 资源组分片（default 组会 INSTANCE_NUM_TOO_LARGE，故按组拆）
      'enter-prod', 'framia-prod', 'game-prod', 'concat-prod',
      'work-prod', 'anycap-prod', 'converge-prod', 'infra-prod',
    ],
    products: [                                      // 全量产品码（pipCode）清单，逐产品拉 INSTANCE 级
      'rds', 'kvstore', 'mongodb', 'elasticsearch', 'clickhouse', 'gpdb',
      'oss', 'nas', 'disk', 'ecs', 'eip', 'slb', 'nat', 'ntr', 'cbwp', 'cdt',
      'vpc', 'privatelink', 'pvtz', 'cas', 'cdn', 'ga', 'waf', 'apigateway',
      'alikafka', 'ons', 'eventbridge', 'dts', 'odps', 'dide', 'opensearch',
      'sfm', 'YUNMARKET_THIRD_PARTY', 'agentbay', 'imm', 'nls', 'alimt',
      'ecoa', 'lvwang', 'cms', 'arms', 'xtrace', 'sls', 'cbs', 'mse', 'hdm',
      'dms', 'aidbs', 'hbr', 'csk', 'sae', 'edas',
    ],
    saturation: ['fc', 'gpdb', 'acs'],              // 行数巨大的产品走「实例根」饱和抽样，不全拉
    // 饱和抽样参数
    satMaxPages: 12,                                 // 最多翻 12 页
    satIdleStop: 2,                                  // 连续 2 页无新增根即停
    pageSize: 500,                                   // 分页大小（接口上限 500）
    endpoint: '/bill/queryMonthConsumeReport',       // usercenter2 域内相对路径
    recvUrl: 'http://127.0.0.1:8732/bills_raw.json', // recv_server.py 落地地址
    concurrency: 3,                                  // 并发请求数（对后端温和一点）
    delayMs: 120,                                    // 每批之间的间隔，避免限流
  };

  // --------------------------------------------------------------------------
  // 工具
  // --------------------------------------------------------------------------
  const log = (...a) => console.log('%c[kunpeng]', 'color:#2563eb;font-weight:bold', ...a);
  const warn = (...a) => console.warn('[kunpeng]', ...a);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  /** 从当前页 HTML 内联脚本里正则提取 X-CSRF-TOKEN（beforeSend setRequestHeader 内联值）。 */
  function extractCsrfToken() {
    const html = document.documentElement.outerHTML;
    const patterns = [
      /X-CSRF-TOKEN['"]\s*,\s*['"]([^'"]+)['"]/i,
      /setRequestHeader\(\s*['"]X-CSRF-TOKEN['"]\s*,\s*['"]([^'"]+)['"]\s*\)/i,
      /['"]csrfToken['"]\s*[:=]\s*['"]([^'"]+)['"]/i,
      /X-CSRF-TOKEN['"]?\s*[:=]\s*['"]([^'"]+)['"]/i,
    ];
    for (const re of patterns) {
      const m = html.match(re);
      if (m && m[1]) return m[1];
    }
    // 退路：meta / cookie
    const meta = document.querySelector('meta[name="csrf-token"], meta[name="_csrf"]');
    if (meta && meta.content) return meta.content;
    const ck = document.cookie.match(/(?:^|;\s*)XSRF-TOKEN=([^;]+)/);
    if (ck) return decodeURIComponent(ck[1]);
    return null;
  }

  const CSRF = extractCsrfToken();
  if (!CSRF) {
    warn('未能从页面提取 X-CSRF-TOKEN，请求可能 403。请在 usercenter2 页签执行，或手动改脚本顶部 CSRF。');
  } else {
    log('CSRF token 提取成功：', CSRF.slice(0, 8) + '…');
  }

  /** 单月查询：startMonth === endMonth（接口语义，跨月要逐月并集）。 */
  async function queryMonth(opts) {
    const { month, tableType, pipCode, resourceGroup, currentPage = 1, pageSize = CONFIG.pageSize } = opts;
    const body = {
      loginUserId: CONFIG.uid,
      startMonth: month,
      endMonth: month,
      pipCodeFilter: 'IN',
      commodityCodeFilter: 'IN',
      tableType,
      filterZeroBills: false,      // 必须 false 才能看到 0 元在用实例（架构存在性证据）
      currentPage,
      pageSize,
    };
    if (pipCode) body.pipCode = pipCode;
    if (resourceGroup) body.resourceGroup = resourceGroup;   // 直接传组名字符串（datalist 懒加载不影响 API）

    const res = await fetch(CONFIG.endpoint, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(CSRF ? { 'X-CSRF-TOKEN': CSRF } : {}),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error('HTTP ' + res.status + ' ' + res.statusText);
    const json = await res.json();
    // 兼容 {data:{list,total}} / {data:[]} / {list,total} 几种壳
    const data = json && (json.data || json.result || json);
    const list = Array.isArray(data) ? data : (data.list || data.rows || data.items || []);
    const total = (data && (data.total ?? data.totalCount ?? data.totalSize)) ?? list.length;
    if (json && (json.code && String(json.code) !== '200' && json.code !== 'SUCCESS') && !list.length) {
      const err = new Error(json.message || json.msg || json.code || 'empty');
      err.apiCode = json.code;
      throw err;
    }
    return { list, total: Number(total) || 0 };
  }

  /** 给每行补 month / tableType，统一字段名（下游 aggregate.py 认这套）。 */
  function tag(row, month, tableType, extra) {
    return Object.assign({ month, tableType }, row, extra || {});
  }

  /**
   * 实例根：饱和抽样用它做基数收敛。按产品定制去尾规则（背景事实）：
   *   fc   = functions/ 名去尾部 hash
   *   gpdb = instanceId 分号前段
   *   acs  = 前 16 字符
   *   其它 = 分号前段
   */
  function instanceRoot(pipCode, row) {
    const id = String(row.instanceId || row.id || '');
    if (pipCode === 'fc') {
      // 形如 .../functions/<name>-<hash> 或直接函数名-<hash>
      let s = id;
      const fm = s.match(/functions\/(.+)$/);
      if (fm) s = fm[1];
      return s.replace(/[-_][0-9a-f]{8,}$/i, '').split(';')[0];
    }
    if (pipCode === 'gpdb') return id.split(';')[0];
    if (pipCode === 'acs') return id.slice(0, 16) || id.split(';')[0];
    return id.split(';')[0];
  }

  /** 族前缀（与 aggregate.py family_of 对齐，产品定制）：
   *   acs  → 16 字符 Pod id 无语义，全部折叠成单池 acs-pod-pool
   *   gpdb → Supabase 池折叠成 supabase-pool；gp- 集群各自成族
   *   其它 → 从尾部丢弃纯 hex hash 段（≥10 位、含数字与 a-f）
   */
  function familyOf(root, pipCode) {
    if (!root) return '';
    const pip = String(pipCode || '').toLowerCase();
    if (pip === 'acs') return 'acs-pod-pool';
    if (pip === 'gpdb') {
      return /spb-|entercloud-pool|entercloud_pool|game_runtime|supabase/i.test(root)
        ? 'supabase-pool' : root;
    }
    const parts = root.split(/([-/_.])/).filter((x) => x !== '');
    const toks = [];
    for (let i = 0; i < parts.length; i += 2) {
      const tok = parts[i];
      const sep = parts[i + 1] || '';
      if (tok) toks.push([tok, sep]);
    }
    const isHash = (t) => /^[0-9a-f]{10,}$/.test(t) && /\d/.test(t) && /[a-f]/.test(t);
    while (toks.length > 1 && isHash(toks[toks.length - 1][0])) toks.pop();
    return toks.map((t) => t[0] + t[1]).join('').replace(/[-/_.]+$/, '') || root;
  }

  /** 简单并发池：把 tasks（() => Promise）以 limit 并发跑完，返回结果数组（保序）。 */
  async function pool(tasks, limit) {
    const results = new Array(tasks.length);
    let idx = 0;
    const workers = new Array(Math.min(limit, tasks.length)).fill(0).map(async () => {
      while (idx < tasks.length) {
        const i = idx++;
        try {
          results[i] = await tasks[i]();
        } catch (e) {
          results[i] = { __error: e };
        }
        if (CONFIG.delayMs) await sleep(CONFIG.delayMs);
      }
    });
    await Promise.all(workers);
    return results;
  }

  // --------------------------------------------------------------------------
  // 结果容器
  // --------------------------------------------------------------------------
  const instance_rows = [];
  const group_rows = [];
  const product_rows = [];
  const saturation = [];
  const failures = [];
  const progress = {};
  const t0 = Date.now();

  function recordFail(scope, err) {
    failures.push({ scope, message: (err && err.message) || String(err), apiCode: err && err.apiCode });
    warn('失败（已记入 failures，不中断）：', scope, err && err.message);
  }

  // --------------------------------------------------------------------------
  // A. 逐月 × 逐产品 INSTANCE 级（saturation 产品走饱和抽样，其余全量分页）
  // --------------------------------------------------------------------------
  async function fetchInstanceAll() {
    const satSet = new Set(CONFIG.saturation);
    const tasks = [];
    for (const month of CONFIG.months) {
      for (const pip of CONFIG.products) {
        if (satSet.has(pip)) continue;   // saturation 产品单独走抽样
        tasks.push(async () => {
          const key = 'INST ' + month + '/' + pip;
          try {
            let page = 1, got = 0, total = Infinity;
            while (got < total && page <= 200) {
              const { list, total: t } = await queryMonth({ month, tableType: 'INSTANCE_CONSUME_MONTH', pipCode: pip, currentPage: page });
              total = t || list.length;
              if (!list.length) break;
              for (const r of list) instance_rows.push(tag(r, month, 'INSTANCE_CONSUME_MONTH', { pipCode: r.pipCode || pip }));
              got += list.length;
              page++;
              if (list.length < CONFIG.pageSize) break;   // 末页
            }
            progress[key] = got;
            if (got) log(key, '→', got, '行 (total=' + total + ')');
          } catch (e) {
            recordFail(key, e);
            progress[key] = 'FAIL';
          }
        });
      }
    }
    log('A. INSTANCE 全量：', tasks.length, '个 (月×产品) 任务，并发', CONFIG.concurrency);
    await pool(tasks, CONFIG.concurrency);
  }

  /** 饱和抽样：逐页拉取提取实例根，连续 satIdleStop 页无新增根即停，最多 satMaxPages 页。 */
  async function fetchSaturation() {
    for (const month of CONFIG.months) {
      for (const pip of CONFIG.saturation) {
        const key = 'SAT ' + month + '/' + pip;
        try {
          const roots = new Set();
          const families = new Set();
          let page = 1, idle = 0, total = null, sampled = 0, sample = null;
          while (page <= CONFIG.satMaxPages) {
            const { list, total: t } = await queryMonth({ month, tableType: 'INSTANCE_CONSUME_MONTH', pipCode: pip, currentPage: page });
            if (total === null) total = t;
            if (!list.length) break;
            sampled += list.length;
            let newRoots = 0;
            for (const r of list) {
              const root = instanceRoot(pip, r);
              if (!root) continue;
              if (!roots.has(root)) { newRoots++; roots.add(root); families.add(familyOf(root, pip)); }
              if (sample === null) sample = { commodityName: r.commodityName, instanceAllocation: r.instanceAllocation, instanceTag: r.instanceTag, region: r.region };
            }
            if (newRoots === 0) { idle++; } else { idle = 0; }
            log(key, 'page', page, '新增根', newRoots, '累计根', roots.size, '族', families.size);
            page++;
            if (idle >= CONFIG.satIdleStop) break;
            if (list.length < CONFIG.pageSize) break;   // 末页
          }
          const converged = idle >= CONFIG.satIdleStop;
          saturation.push({
            pipCode: pip, month,
            pages: page - 1,
            rootCount: roots.size,
            familyCount: families.size,
            total,                       // 接口报的总行数（下界证据）
            sampled,                     // 实际抽到的行数
            converged,
            roots: Array.from(roots).slice(0, 5000).map((root) => ({ root, family: familyOf(root, pip), ...(sample || {}) })),
          });
          progress[key] = { roots: roots.size, families: families.size, converged };
          if (!converged) warn(key, '未在', CONFIG.satMaxPages, '页内收敛，根数为下界');
        } catch (e) {
          recordFail(key, e);
          progress[key] = 'FAIL';
        }
      }
    }
  }

  // --------------------------------------------------------------------------
  // B. 逐月 × 逐资源组（default 组会 INSTANCE_NUM_TOO_LARGE，故按组名分片）
  // --------------------------------------------------------------------------
  async function fetchGroups() {
    const tasks = [];
    for (const month of CONFIG.months) {
      for (const grp of CONFIG.groups) {
        tasks.push(async () => {
          const key = 'GRP ' + month + '/' + grp;
          try {
            let page = 1, got = 0, total = Infinity;
            while (got < total && page <= 100) {
              const { list, total: t } = await queryMonth({ month, tableType: 'INSTANCE_CONSUME_MONTH', resourceGroup: grp, currentPage: page });
              total = t || list.length;
              if (!list.length) break;
              for (const r of list) group_rows.push(tag(r, month, 'INSTANCE_CONSUME_MONTH', { resourceGroupName: r.resourceGroupName || grp }));
              got += list.length;
              page++;
              if (list.length < CONFIG.pageSize) break;
            }
            progress[key] = got;
            if (got) log(key, '→', got, '行');
          } catch (e) {
            recordFail(key, e);
            progress[key] = 'FAIL';
          }
        });
      }
    }
    log('B. resourceGroup：', tasks.length, '个 (月×组) 任务');
    await pool(tasks, CONFIG.concurrency);
  }

  // --------------------------------------------------------------------------
  // C. 逐月 PRODUCT 级 + ACCOUNT 级（补无实例维度产品 + 对账合计）
  // --------------------------------------------------------------------------
  async function fetchProducts() {
    for (const month of CONFIG.months) {
      // PRODUCT 级
      try {
        let page = 1, got = 0;
        while (page <= 50) {
          const { list } = await queryMonth({ month, tableType: 'PRODUCT_CONSUME_MONTH', currentPage: page });
          if (!list.length) break;
          for (const r of list) product_rows.push(tag(r, month, 'PRODUCT_CONSUME_MONTH'));
          got += list.length;
          page++;
          if (list.length < CONFIG.pageSize) break;
        }
        progress['PROD ' + month] = got;
        log('PRODUCT', month, '→', got, '行');
      } catch (e) { recordFail('PROD ' + month, e); }
      // ACCOUNT 级（单页）
      try {
        const { list } = await queryMonth({ month, tableType: 'ACCOUNT_CONSUME_MONTH', currentPage: 1 });
        for (const r of list) product_rows.push(tag(r, month, 'ACCOUNT_CONSUME_MONTH'));
        progress['ACCT ' + month] = list.length;
        log('ACCOUNT', month, '→', list.length, '行');
      } catch (e) { recordFail('ACCT ' + month, e); }
    }
  }

  // --------------------------------------------------------------------------
  // D. 组装 + 回传
  // --------------------------------------------------------------------------
  async function postResult() {
    const payload = {
      meta: {
        uid: CONFIG.uid,
        months: CONFIG.months,
        months_complete: CONFIG.monthsComplete,
        sources: ['usercenter2:/bill/queryMonthConsumeReport'],
        config: {
          groups: CONFIG.groups,
          products: CONFIG.products,
          saturation: CONFIG.saturation,
          pageSize: CONFIG.pageSize,
        },
        generated_at: new Date().toISOString(),
        csrf_found: !!CSRF,
        elapsed_ms: Date.now() - t0,
      },
      instance_rows,
      group_rows,
      product_rows,
      saturation,
      failures,
      progress,
    };
    const bytes = new Blob([JSON.stringify(payload)]).size;
    log('D. 组装完成 →', { instance_rows: instance_rows.length, group_rows: group_rows.length, product_rows: product_rows.length, saturation: saturation.length, failures: failures.length, bytes });
    try {
      const res = await fetch(CONFIG.recvUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const txt = await res.text();
      if (res.ok) {
        log('✅ 回传成功 →', CONFIG.recvUrl, txt);
      } else {
        warn('回传失败 HTTP', res.status, txt, '—— 确认 recv_server.py 已在', CONFIG.recvUrl, '监听');
      }
    } catch (e) {
      warn('回传异常（recv_server 未起？）：', e.message, '。payload 已存 window.__kunpeng_payload，可手动 copy(JSON.stringify(window.__kunpeng_payload))');
    }
    window.__kunpeng_payload = payload;   // 兜底：回传失败也能手动导出
    return payload;
  }

  // --------------------------------------------------------------------------
  // 主流程
  // --------------------------------------------------------------------------
  if (!/usercenter2\.aliyun-inc\.com/.test(location.host)) {
    warn('当前不在 usercenter2 域（' + location.host + '），fetch 会因跨域/无 CSRF 失败。请打开 https://usercenter2.aliyun-inc.com/ 的页签再执行。');
  }
  log('开始抽取 uid=' + CONFIG.uid + ' months=' + CONFIG.months.join(','));
  await fetchInstanceAll();
  await fetchSaturation();
  await fetchGroups();
  await fetchProducts();
  const payload = await postResult();
  log('全部完成，用时', ((Date.now() - t0) / 1000).toFixed(1) + 's', '｜ failures:', failures.length);
  return payload;
})();
