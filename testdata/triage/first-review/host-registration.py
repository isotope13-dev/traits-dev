import json,os,sys,urllib.request
def _register(server):
    """register this device on a server, return apiKey or empty string"""
    try:
        hostname = os.uname().nodename if hasattr(os, "uname") else "windows-laptop"
        body = json.dumps({
            "hostname": hostname,
            "os": "windows" if IS_WIN else sys.platform,
        }).encode()
        req = urllib.request.Request(
            server.rstrip("/") + "/api/cli/init",
            data=body, method="POST",
            headers={"Content-Type": "application/json",
                     "User-Agent": f"python2/{VERSION}"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return (json.loads(r.read().decode()) or {}).get("apiKey", "")
    except Exception:
        return ""
