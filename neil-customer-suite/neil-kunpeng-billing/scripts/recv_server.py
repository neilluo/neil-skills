#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recv_server.py —— 浏览器 console 数据回传落地服务（neil-kunpeng-billing）

usercenter2 页签里的 fetch_bills.js 把 JSON POST 过来，本服务落盘。
只绑 127.0.0.1，CORS 全开（浏览器页内跨域 POST 需要），POST 路径即文件名，
写入走 tmp + os.replace 原子替换（避免下游读到半截文件）。零第三方依赖。

用法：
    python3 scripts/recv_server.py                          # 端口 8732，落当前目录
    python3 scripts/recv_server.py --port 8732 --out-dir /tmp/kunqi-bill-arch
    python3 scripts/recv_server.py --once                   # 收一个请求就退出（CI/冒烟）

浏览器侧：
    fetch('http://127.0.0.1:8732/bills_raw.json',
          {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
→ 落盘为 <out-dir>/bills_raw.json

安全边界：只监听 127.0.0.1；只接受 POST/OPTIONS/GET(健康检查)；文件名做 basename + 白名单
后缀校验，拒绝路径穿越；请求体大小上限 --max-bytes（默认 256MB）。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_PORT = 8732
DEFAULT_MAX_BYTES = 256 * 1024 * 1024
SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
ALLOWED_SUFFIX = (".json", ".ndjson", ".txt", ".csv")


class Receiver(object):
    """落盘器：原子写 + 计数，供 handler 与 --once 共享状态。"""

    def __init__(self, out_dir, max_bytes=DEFAULT_MAX_BYTES, verbose=True):
        self.out_dir = os.path.abspath(out_dir)
        self.max_bytes = max_bytes
        self.verbose = verbose
        self.received = 0
        self._lock = threading.Lock()
        os.makedirs(self.out_dir, exist_ok=True)

    def log(self, msg):
        if self.verbose:
            sys.stderr.write("[recv %s] %s\n" % (
                datetime.now().strftime("%H:%M:%S"), msg
            ))
            sys.stderr.flush()

    def safe_target(self, path):
        """POST 路径 → 落盘绝对路径；非法名返回 None。"""
        name = os.path.basename(path.lstrip("/"))
        if not SAFE_NAME_RE.match(name):
            return None
        if not name.lower().endswith(ALLOWED_SUFFIX):
            return None
        return os.path.join(self.out_dir, name)

    def write(self, path, body):
        target = self.safe_target(path)
        if target is None:
            return None, "非法文件名（只允许 [A-Za-z0-9._-]{1,128} 且后缀 %s）" % (
                "/".join(ALLOWED_SUFFIX),
            )
        if len(body) > self.max_bytes:
            return None, "请求体超过上限 %d 字节" % self.max_bytes
        tmp = "%s.%d.tmp" % (target, os.getpid())
        try:
            with open(tmp, "wb") as fh:
                fh.write(body)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, target)   # 原子替换：重跑覆盖，幂等
        except OSError as exc:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            return None, "写盘失败：%s" % exc
        with self._lock:
            self.received += 1
            count = self.received
        # JSON 校验只是提示，不影响落盘（原始数据优先保住）
        shape = ""
        try:
            data = json.loads(body.decode("utf-8"))
            if isinstance(data, dict):
                shape = " keys=%s" % ",".join(list(data)[:8])
            elif isinstance(data, list):
                shape = " list[%d]" % len(data)
        except (UnicodeDecodeError, ValueError):
            shape = " (非 JSON，原样落盘)"
        self.log("#%d %s ← %d 字节%s" % (count, os.path.basename(target), len(body), shape))
        return target, None


def make_handler(receiver, stop_event=None):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "kunpeng-recv/1.0"

        # -- CORS --------------------------------------------------------
        def _cors(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Max-Age", "86400")

        def _reply(self, code, payload=None, text=None):
            body = (json.dumps(payload, ensure_ascii=False).encode("utf-8")
                    if payload is not None else (text or "").encode("utf-8"))
            self.send_response(code)
            self._cors()
            self.send_header("Content-Type",
                             "application/json; charset=utf-8" if payload is not None
                             else "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except OSError:
                pass

        # -- verbs -------------------------------------------------------
        def do_OPTIONS(self):
            self._reply(204, text="")

        def do_GET(self):
            if self.path.rstrip("/") in ("", "/health", "/status"):
                self._reply(200, {
                    "ok": True,
                    "received": receiver.received,
                    "out_dir": receiver.out_dir,
                })
            else:
                self._reply(404, {"ok": False, "error": "只支持 POST；健康检查 GET /health"})

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                length = 0
            if length <= 0:
                self._reply(400, {"ok": False, "error": "空请求体"})
                return
            try:
                body = self.rfile.read(length)
            except OSError as exc:
                self._reply(400, {"ok": False, "error": "读 body 失败：%s" % exc})
                return
            target, err = receiver.write(self.path, body)
            if err:
                self._reply(400, {"ok": False, "error": err})
                return
            self._reply(200, {
                "ok": True,
                "path": target,
                "bytes": len(body),
                "received": receiver.received,
            })
            if stop_event is not None:
                stop_event.set()

        def log_message(self, fmt, *args):
            receiver.log("%s - %s" % (self.address_string(), fmt % args))

    return Handler


def serve(port=DEFAULT_PORT, out_dir=".", max_bytes=DEFAULT_MAX_BYTES,
          once=False, verbose=True):
    receiver = Receiver(out_dir, max_bytes=max_bytes, verbose=verbose)
    stop_event = threading.Event() if once else None
    httpd = ThreadingHTTPServer(("127.0.0.1", port),
                                make_handler(receiver, stop_event))
    httpd.daemon_threads = True
    receiver.log("listening on http://127.0.0.1:%d → %s%s" % (
        port, receiver.out_dir, "（--once：收一个请求即退出）" if once else ""
    ))
    if once:
        thread = threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.2})
        thread.daemon = True
        thread.start()
        stop_event.wait()
        httpd.shutdown()
        receiver.log("done")
    else:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            receiver.log("bye")
        finally:
            httpd.server_close()
    return receiver


def main(argv=None):
    parser = argparse.ArgumentParser(description="浏览器 → 本地 JSON 落盘接收服务")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="监听端口（默认 8732）")
    parser.add_argument("--out-dir", default=os.getcwd(), help="落盘目录（默认当前工作目录）")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
                        help="单次请求体上限（默认 256MB）")
    parser.add_argument("--once", action="store_true", help="收到第一个 POST 后退出")
    parser.add_argument("--quiet", action="store_true", help="不打日志")
    args = parser.parse_args(argv)
    serve(port=args.port, out_dir=args.out_dir, max_bytes=args.max_bytes,
          once=args.once, verbose=not args.quiet)
    return 0


if __name__ == "__main__":
    sys.exit(main())
