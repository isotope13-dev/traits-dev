#!/usr/bin/env python3
"""Check saved atomscan JSONL from this fixture directory; never execute fixtures."""
import json
import sys
from pathlib import Path

reports = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()]
traits = {}
for report in reports:
    root = report["raw"]["files"][0]
    traits[Path(root["path"]).name] = {t["id"] for t in root.get("traits", [])}

def expect(name, trait, present=True):
    assert (trait in traits[name]) == present, (name, trait, present)

probe = "micro-behaviors/process/debug/detect::node-inspect-options-call"
html_probe = "micro-behaviors/process/debug/detect::html-node-inspect-options-call"
factory = "micro-behaviors/data/db/redis::node-redis-client-initialization"
body = "micro-behaviors/communications/http/message::request-response-body-fields"
expect("debug-options-check.js", probe)
expect("debug-launch-config.js", probe, False)
expect("inspector-check.html", html_probe)
expect("inspector-config.html", html_probe, False)
expect("redis-initialization.js", factory)
expect("redis-import-only.js", factory, False)
expect("unrelated-client-factory.js", factory, False)
expect("http-body-fields.js", body)
expect("http-body-fields.js", "micro-behaviors/communications/http/llm-proxy::local-llm-metering-body-capture", False)
expect("llm-body-capture.py", "micro-behaviors/communications/http/llm-proxy::local-llm-metering-body-capture")
for trait in [
    "micro-behaviors/data/db/schema/stored-code::redis-function-load-call",
    "micro-behaviors/data/db/schema/stored-code::redis-function-flush-call",
    "micro-behaviors/data/db/delete/row::redis-flushdb-call",
]:
    expect("redis-methods.js", trait)
    expect("redis-api-comments.js", trait, False)
expect("redis-api-comments.js", "micro-behaviors/process/terminate/kill::node-kill-port-require", False)
print("All fixture assertions passed")
