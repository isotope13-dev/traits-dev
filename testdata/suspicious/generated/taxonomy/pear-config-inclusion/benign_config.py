import http.client
c = http.client.HTTPConnection("127.0.0.1")
c.request("GET", "/?+config-create+/usr/local+/tmp/settings.ini")
