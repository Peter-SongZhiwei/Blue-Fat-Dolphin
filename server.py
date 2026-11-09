#!/usr/bin/env python3
"""Local GIF page; the key is read on demand, never embedded in HTML."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
KEY_FILE = Path.home() / 'dev' / 'API_KEY'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        allowed_hosts = {f'localhost:{self.server.server_port}',
                         f'127.0.0.1:{self.server.server_port}'}
        if (self.headers.get('Host') not in allowed_hosts
                or self.headers.get('Sec-Fetch-Site') == 'cross-site'):
            self.send_content(403, b'Forbidden', 'text/plain')
            return
        path = urlsplit(self.path).path
        if path == '/api/key':
            self.send_content(405, '请先验证公司缩写'.encode(), 'text/plain; charset=utf-8')
        elif path in ('/', '/index.html', '/fish.gif'):
            file = ROOT / ('fish.gif' if path == '/fish.gif' else 'index.html')
            self.send_content(200, file.read_bytes(), 'image/gif' if path == '/fish.gif' else 'text/html; charset=utf-8')
        else:
            self.send_content(404, b'Not found', 'text/plain')

    def do_POST(self):
        allowed_hosts = {f'localhost:{self.server.server_port}',
                         f'127.0.0.1:{self.server.server_port}'}
        if (self.headers.get('Host') not in allowed_hosts
                or self.headers.get('Sec-Fetch-Site') == 'cross-site'):
            self.send_content(403, b'Forbidden', 'text/plain')
            return
        if urlsplit(self.path).path != '/api/key':
            self.send_content(404, b'Not found', 'text/plain')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length < 1 or length > 1024:
                raise ValueError()
            data = json.loads(self.rfile.read(length))
            company = data.get('company') if isinstance(data, dict) else None
        except (ValueError, UnicodeError):
            self.send_content(400, '请求格式错误'.encode(), 'text/plain; charset=utf-8')
            return
        if not isinstance(company, str) or company.strip().casefold() != 'zte':
            self.send_content(403, '公司缩写不正确，请重试。'.encode(), 'text/plain; charset=utf-8')
            return
        try:
            self.send_content(200, KEY_FILE.read_bytes(), 'text/plain; charset=utf-8')
        except FileNotFoundError:
            self.send_content(404, '找不到 ~/dev/API_KEY 文件'.encode(), 'text/plain; charset=utf-8')
        except OSError:
            self.send_content(500, '无法读取 ~/dev/API_KEY 文件'.encode(), 'text/plain; charset=utf-8')

    def send_content(self, status, data, mime):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'打开 http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
