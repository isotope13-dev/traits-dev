import importlib.util
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
server = ThreadingHTTPServer(('127.0.0.1', 0), BaseHTTPRequestHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()
spec = importlib.util.spec_from_file_location('plugin', 'plugin.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
