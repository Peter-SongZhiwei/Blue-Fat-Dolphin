"""Vercel endpoint: verify the company before returning the server-side key."""
import json
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def reply(self, status, message):
        body = message.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if status == 405:
            self.send_header('Allow', 'POST')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.reply(405, '请先验证公司缩写')

    def do_POST(self):
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
            self.reply(403, '不允许跨站请求')
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1024:
                raise ValueError()
            payload = json.loads(self.rfile.read(length))
            company = payload.get('company') if isinstance(payload, dict) else None
        except (ValueError, UnicodeError):
            self.reply(400, '请求格式错误')
            return
        if not isinstance(company, str) or company.strip().casefold() != 'zte':
            self.reply(403, '公司缩写不正确，请重试。')
            return
        key = os.environ.get('API_KEY')
        if not key:
            self.reply(503, '尚未配置 API KEY，请联系管理员。')
            return
        self.reply(200, key)
