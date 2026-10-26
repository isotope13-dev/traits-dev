import urllib.request

with urllib.request.urlopen("https://example.invalid/account") as response:
    cookie = response.headers.get("Set-Cookie", "")
    session_id = cookie.split(";", 1)[0].removeprefix("PHPSESSID=")
    print(session_id)
