import requests

def send(body, token, bot):
    """Native URL: https://cliq.zoho.eu/company/{id}/api/v2/bots/{bot}/message?zapikey={token}"""
    return requests.post(f"https://cliq.zoho.eu/api/v2/bots/{bot}/message", params={"zapikey": token}, json={"text": body})
