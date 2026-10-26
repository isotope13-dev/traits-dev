"""Run the original JS functions with inert QuickJS host stubs.

Reproduce with: uv run --with quickjs==1.19.4 python trace-js.py
"""
from pathlib import Path
import base64
import json
import re
import quickjs

source = Path(__file__).with_name("ci-bridge.js").read_text()
source = re.sub(r"^import .*;$", "", source, flags=re.M)
source = source.replace("export function ", "function ")
context = quickjs.Context()
context.eval("""
var events = [];
var process = {cwd: () => '/repo', env: {
  GITHUB_ENV: '/runner/env', NPM_TOKEN: 'TEST_TOKEN'
}};
var console = {log: (...args) => events.push(['log', ...args])};
var status = {status: 0};
var bridgeExists = false;
function appendFileSync(...args) { events.push(['append', ...args]); }
function existsSync() { return bridgeExists; }
function spawnSync(...args) { events.push(['spawn', ...args]); return status; }
""")
context.eval(source)
assert context.eval("events.length") == 0
context.eval("poisonReleaseEnv()")
events = json.loads(context.eval("JSON.stringify(events)"))
assert events[0][1:3] == [
    "/runner/env", "BASH_ENV=/repo/.github/scripts/publish-bridge.sh\n"
]
assert context.eval("collectStageZero()") is False
context.eval("""
process.env.PACKAGE_NAME = '@example/release-plugin';
process.env.PUBLISH_TIMEOUT_SECONDS = '150';
""")
assert context.eval("collectStageZero('event')") is True
events = json.loads(context.eval("JSON.stringify(events)"))
child = next(event for event in events if event[0] == "spawn")
assert child[3]["env"]["NPM_TOKEN"] == "TEST_TOKEN"
assert child[3]["env"]["BASH_ENV"] == ""
assert base64.b64decode(child[2][2]) == b'{"schema":"test.v1"}'
context.eval("status = {status: 1}")
assert context.eval("collectStageZero()") is False
context.eval("dropBridge()")
assert context.eval("process.exitCode") is None
context.eval("bridgeExists = true; dropBridge()")
assert context.eval("process.exitCode") == 1
events = json.loads(context.eval("JSON.stringify(events)"))
assert events[-1][1] == "rm"
print(json.dumps(events, indent=2))
