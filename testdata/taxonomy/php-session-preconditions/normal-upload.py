import urllib.request
body = b'--normal\r\nContent-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n1\r\n--normal--\r\n'
request = urllib.request.Request('https://example.invalid/upload.php', data=body, headers={
    'Content-Type': 'multipart/form-data; boundary=normal',
    'Cookie': 'PHPSESSID=established-session',
})
with urllib.request.urlopen(request) as response:
    cookie = response.headers.get('Set-Cookie', '')
    print(cookie)
