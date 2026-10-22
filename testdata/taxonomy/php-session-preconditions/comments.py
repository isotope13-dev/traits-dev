import urllib.request
# Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"
# response.headers.get('X-Powered-By')
# response.headers.get('Set-Cookie')
# /?page=../../../../etc/passwd
with urllib.request.urlopen('https://example.invalid/health') as response:
    print(response.status)
