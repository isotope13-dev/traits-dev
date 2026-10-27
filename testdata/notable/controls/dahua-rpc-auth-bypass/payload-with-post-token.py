from urllib.request import Request, urlopen

# Imports and an HTTP method token do not send this example payload.
method = "POST"
params = {"password": "Not Used", "clientType": "NetKeyboard",
          "loginType": "Loopback", "ipAddr": "127.0.0.1"}
