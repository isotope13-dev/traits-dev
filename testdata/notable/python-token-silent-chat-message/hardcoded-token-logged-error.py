import requests, logging
TOKEN = "1357924680:AAFixtureOnlyTokenValueForRegression01"
CHAT = "5550001111"
def send(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": text}, timeout=5)
    except Exception as e:
        logging.error("telegram notify failed: %s", e)
