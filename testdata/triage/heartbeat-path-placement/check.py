"""Pin the heartbeat endpoint-path placement under url/api-path.

`substr: /api/heartbeat` matches a bare endpoint-path string whether it sits
in client code building a URL or in server code defining a route, so the
trait is a URL fact, not server-side handling. It lives at
`micro-behaviors/communications/http/url/api-path::http-api-heartbeat-path`
(moved from `micro-behaviors/communications/http/server/route`).
These fixtures pin both sides: a client reference and a server route
definition each fire the new ID as notable, and the old ID stays absent.
"""
import json
import os
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent

NEW = "micro-behaviors/communications/http/url/api-path::http-api-heartbeat-path"
OLD = "micro-behaviors/communications/http/server/route::python-heartbeat-route"


def file_traits(name):
    env = dict(os.environ, CLEAVE_SKIP_CACHE="1")
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json",
         str(fixtures / name)],
        check=True, capture_output=True, text=True, env=env,
    )
    report = json.loads(result.stdout)
    for item in report["files"]:
        if item["path"] == str(fixtures / name):
            return item["traits"]
    raise AssertionError("no report for " + name)


def crits(traits, identifier):
    return [trait["crit"] for trait in traits if trait["id"] == identifier]


for name in ("client.py", "server.py"):
    traits = file_traits(name)
    assert crits(traits, NEW) == [3], (name, traits)
    assert crits(traits, OLD) == [], (name, traits)

print("PASS: heartbeat endpoint path fires under url/api-path, not server/route")
