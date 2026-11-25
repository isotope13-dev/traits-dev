import urllib.request, urllib.parse
TOKEN = "1357924680:AAFixtureOnlyTokenValueForRegression01"
CHAT = "5550001111"
def send(text):
    try:
        u = "https://api.telegram.org/bot%s/sendMessage" % TOKEN
        urllib.request.urlopen(u, urllib.parse.urlencode({"chat_id": CHAT, "text": text}).encode(), timeout=5)
    except Exception:
        pass
