import re, requests

def validate_supplied(candidate):
    pattern = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")
    log = open("application.log").read()
    for token in pattern.findall(candidate):
        requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
