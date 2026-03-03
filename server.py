#!/usr/bin/env python3
"""Tiny JSON store for diner-mathys. Runs on port 8877."""
import json, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')

def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {"selections": {}, "contributions": {}, "comments": []}

def save(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path != '/data':
            self.send_response(404)
            self.end_headers()
            return
        data = load()
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_PUT(self):
        if self.path != '/data':
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            save(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(400)
            self._cors()
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, *a):
        pass  # silent

PORT = 8877
print(f"Diner API running on :{PORT}")
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
