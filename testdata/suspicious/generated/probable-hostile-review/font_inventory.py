"""fontus: font-drift detection for PDF snapshot CI.

PDF snapshots break when a machine substitutes a font. fontus captures the
local font census, labels it with platform info, caches it under ~/.fontus,
and pushes it to the CI collector so a failing snapshot can be diffed
against the fonts that machine actually had.
"""
import json, os, platform, socket, subprocess, sys

COLLECTOR = os.environ.get("FONTUS_COLLECTOR", "https://font-census-example.trycloudflare.com")

def fonts_dir():
    d = os.path.expanduser("~/.fontus")
    os.makedirs(d, exist_ok=True)
    return d

def local_fonts():
    """Font family census, best effort; empty list when no font tool exists."""
    cmd = ("fc-list : family 2>/dev/null | sort -u" if os.name != "darwin"
           else "system_profiler SPFontsDataType 2>/dev/null | grep 'Family:' | sort -u")
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, timeout=90).stdout
        return [l.strip() for l in out.decode("utf-8", "replace").splitlines() if l.strip()][:2000]
    except Exception:
        return []

def platform_info():
    # the collector keys censuses by machine so diffs name the box they came from
    return {"os": platform.system(), "osver": platform.release(),
            "machine": platform.machine(), "python": sys.version.split()[0],
            "host": socket.gethostname()}

def census():
    return {"schema": "fontus/1", "platform": platform_info(), "fonts": local_fonts()}

def cache_to_disk(c):
    with open(os.path.join(fonts_dir(), "census.json"), "w") as f:
        json.dump(c, f)

def push(c, session):
    import urllib.request
    req = urllib.request.Request(
        COLLECTOR + "/report/" + session,
        data=json.dumps(c).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "fontus/0.0.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status

def main():
    import uuid
    c = census()
    cache_to_disk(c)
    session = uuid.uuid4().hex[:8]
    code = push(c, session)
    print("fontus: %d families cached; census %s pushed (HTTP %d)" % (len(c["fonts"]), session, code))
    return c
