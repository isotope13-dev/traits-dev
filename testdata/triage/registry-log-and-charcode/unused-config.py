import http.client
conn = http.client.HTTPConnection("example.invalid")
conn.request("POST", "/unrelated", "state=ready")
log = {"file": "/srv/web/htdocs/access.log", "format": "combined"}
handler = {"interpreter": "/bin/sh", "extension": "log"}
