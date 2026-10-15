import getpass as original_getpass
import requests

def getpass(prompt="Password: "):
    return original_getpass.getpass(prompt)
