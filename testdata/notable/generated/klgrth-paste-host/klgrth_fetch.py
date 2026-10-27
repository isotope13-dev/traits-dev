import urllib.request

data = urllib.request.urlopen("https://klgrth.io/paste/x8k2f/raw").read()
print(len(data))
