import requests

TOKEN = "123456789012:AbCdEf1234567890AbCdEf1234567890"


def notify_build(status):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": 12345, "text": f"build {status}"},
    )
