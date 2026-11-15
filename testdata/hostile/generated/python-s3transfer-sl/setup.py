import urllib.request


with urllib.request.urlopen(
    "https://webhook.site/00000000-0000-4000-8000-000000000000/s3transfer"
) as response:
    content = response.read()
print(content.decode("utf-8"))
