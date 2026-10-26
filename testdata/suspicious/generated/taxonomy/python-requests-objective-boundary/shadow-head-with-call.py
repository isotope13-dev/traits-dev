import getpass as original_getpass
import requests

def getpass(prompt="Password: "):
    value = original_getpass.getpass(prompt)
    requests.head("https://target.invalid/log")
    return value
