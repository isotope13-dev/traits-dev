import urllib.request


with urllib.request.urlopen("https://pypi.org/pypi/example/json") as response:
    release_metadata = response.read()
print(len(release_metadata))
