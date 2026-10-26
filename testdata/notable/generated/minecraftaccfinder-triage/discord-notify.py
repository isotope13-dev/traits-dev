"""Benign CI notifier: posts build status to a team Discord webhook."""
import json
import urllib.request

WEBHOOK = "https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"


def notify(status):
    data = json.dumps({"content": "build %s" % status}).encode()
    req = urllib.request.Request(WEBHOOK, data, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.status
