"""Minimal HTTP server defining a heartbeat route."""
from http.server import BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/heartbeat":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"{}")
