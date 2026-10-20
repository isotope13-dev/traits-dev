import urllib.request
request = urllib.request.Request("https://support.example.com/upload", data=open("diagnostics.txt", "rb").read())
urllib.request.urlopen(request)
