"""CVE-2026-119618 AddressSanitizer ThreadSanitizer heap-use-after-free"""
import threading
from h2 import H2Connection
client = H2Connection('localhost', 8080)
client.send_request_headers(1, [('content-type', 'text/plain')], end_stream=True)
threading.Thread(target=print, daemon=True).start()
