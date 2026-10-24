from urllib.parse import urlparse
if urlparse(source).hostname in ("video.example.com", "example.com"):
    source = normalize(source)
