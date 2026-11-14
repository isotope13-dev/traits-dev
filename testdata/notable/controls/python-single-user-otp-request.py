import requests


def request_login_code(phone):
    return requests.post(
        "https://service.example/api/otp-request",
        data={"phone": phone},
    )
