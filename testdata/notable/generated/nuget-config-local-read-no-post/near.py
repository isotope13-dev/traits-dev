"""Report which package sources the local NuGet client is configured with."""
import os
import urllib.request

CONFIG = os.path.join(os.path.expanduser("~"), ".nuget", "NuGet", "NuGet.Config")


def local_sources():
    if not os.path.exists(CONFIG):
        return []
    with open(CONFIG, errors="ignore") as fh:
        return [line.strip() for line in fh if "<add key=" in line]


def check_feed(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    return urllib.request.urlopen(req, timeout=8).status
