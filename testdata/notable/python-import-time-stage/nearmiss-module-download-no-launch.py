import urllib.request
manifest = urllib.request.urlopen("https://updates.example.invalid/manifest.json").read()
VERSION = "1.2.3"
