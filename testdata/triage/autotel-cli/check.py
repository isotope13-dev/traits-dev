#!/usr/bin/env python3
"""Static regression controls; none of the JavaScript/Python inputs are run."""
import argparse
import json
from pathlib import Path
import subprocess
import struct
import tempfile


ROOT = Path(__file__).resolve().parents[3]
ENV = "micro-behaviors/os/env/enumeration::js-process-env-spread"
NAME = "micro-behaviors/data/property/assign::package-named-object-name-assignment"
GET = "micro-behaviors/data/control-flow/dispatch::getbody-method-call"
ASSIGN = "micro-behaviors/data/property/assign::getbody-result-assignment"
LOOP = "micro-behaviors/data/control-flow/iteration::iterated-list-fetch-loop"
CI = "micro-behaviors/os/env/cicd::isci-property-access"
CHAT = "micro-behaviors/communications/http/client/library::chat-completions-create-call"
REST = "micro-behaviors/communications/http/client/service::servicenow-restmessage-body-capture"
LOOP_ATOMS = {
    "micro-behaviors/data/control-flow/iteration::source-for-of-fetch-syntax",
    "micro-behaviors/data/control-flow/iteration::markup-for-of-fetch-syntax",
}
RETIRED = {
    "micro-behaviors/data/control-flow/dispatch::save-plugin-command-token",
    "micro-behaviors/os/package-manager/publish::manifest-name-rewrite",
    "micro-behaviors/communications/http/response::getbody-call",
    "micro-behaviors/communications/http/request/result::response-getbody-assignment",
    "micro-behaviors/os/env/cicd::ci-info-isci-property",
    "micro-behaviors/communications/http/services/groq::groq-chat-completions",
    "micro-behaviors/communications/http/client/library::openai-chat-completions-call",
}


def token_pe(token, section=b".text"):
    """Minimal inert PE containing one terminated string, with no code/imports."""
    data = bytearray(1024)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into("<H", data, optional, 0x10b)
    struct.pack_into("<III", data, optional + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into("<II", data, optional + 56, 0x2000, 0x200)
    struct.pack_into("<H", data, optional + 68, 3)
    struct.pack_into("<I", data, optional + 92, 16)
    struct.pack_into("<8sIIIIIIHHI", data, optional + 224,
                     section, 512, 0x1000, 512, 512, 0, 0, 0, 0, 0x40000040)
    data[512:512 + len(token)] = token
    return data


def scan(cleave, target):
    result = subprocess.run(
        [cleave, "--traits-dir", str(ROOT), "--format", "json", str(target)],
        check=True, capture_output=True, text=True,
    )
    decoder = json.JSONDecoder()
    rest = result.stdout.lstrip()
    files = []
    while rest:
        report, end = decoder.raw_decode(rest)
        files.extend(report["files"])
        rest = rest[end:].lstrip()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--sample", type=Path)
    args = parser.parse_args()
    # The negative combines reduced excerpts from the supplied CLI. In
    # particular, fetch follows a completed loop, and package names are read.
    negative = '''
const options = {
  ...process.env.GITHUB_WORKSPACE ? {workspace: process.env.GITHUB_WORKSPACE} : {}
};
const member = {...process.env.CI};
function getCommand(name) {
  const requiresPackageJson = false;
  return commands.find(c => c.name === name);
}
const pkg = JSON.parse(fs.readFileSync("package.json", "utf8"));
if (pkg.name === "example-cli") console.log(pkg.version);
function rewrite(method) {
  const body = method.getBody();
  return body.getText();
}
function isCI() { return Boolean(process.env.CI); }
function debug(events) {
  for (const event of events) console.log(event);
}
function send(endpoint, events) {
  return fetch(endpoint, {method: "POST", body: JSON.stringify({events})});
}
const example = "client.chat.completions.create(messages)";
'''
    positive = '''
const copy = {...process.env};
packageJson.name = chooseName();
package_json.name = "renamed";
const response = new sn_ws.RESTMessageV2().execute();
const body = response.getBody();
console.log(ciInfo.isCI);
client.chat.completions.create({messages: []});
for (const url of urls) { await fetch(url); }
'''
    cases = {
        "cli-excerpts.js": (negative, {GET, ASSIGN}, {ENV, NAME, LOOP, CI, CHAT}),
        "actual-operations.js": (positive, {ENV, NAME, GET, ASSIGN, LOOP, CI, CHAT, REST}, set()),
        "actual-operations.ts": (positive, {ENV, NAME, GET, ASSIGN, LOOP, CI, CHAT, REST}, set()),
        "comparison.js": ('const x = body === response.getBody();\n', {GET}, {ASSIGN}),
        "prose.js": ('// {...process.env}; pkg.name = "other"; ciInfo.isCI\n'
                     'const example = "client.chat.completions.create([])";\n',
                     set(), {ENV, NAME, CI, CHAT}),
        "openai-compatible.py": ('client.chat.completions.create(messages=[])\n', {CHAT}, set()),
        "groq-client.js": ('const client = new Groq();\n'
                           'client.chat.completions.create({messages: []});\n',
                           {CHAT, "micro-behaviors/communications/http/services/groq::groq-chat-client"}, set()),
        "bare-manifest-assignment.js": ('manifest.name = "next-name";\n', {NAME}, set()),
        "loop.html": ('<script>for (const url of urls) { await fetch(url); }</script>\n', {LOOP}, set()),
        "loop.svg": ('<svg xmlns="http://www.w3.org/2000/svg"><script>'
                     'for (const url of urls) { await fetch(url); }</script></svg>\n', {LOOP}, set()),
        "separate-functions.html": ('<script>function debug(events) {'
                                    'for (const event of events) {console.log(event);}}'
                                    'function send(url) {return fetch(url);}</script>\n',
                                    set(), {LOOP}),
    }
    with tempfile.TemporaryDirectory(prefix="autotel-trait-controls-") as directory:
        scratch = Path(directory)
        for name, (code, _, _) in cases.items():
            (scratch / name).write_text(code)
        native = {
            "save.exe": (b"savePlugin", b".text", True, False),
            "send.exe": (b"sendPlugin", b".text", True, True),
            "longer.exe": (b"savePluginExtra", b".text", False, False),
            "other-section.exe": (b"savePlugin", b".rdata", False, False),
        }
        for name, (token, section, _, _) in native.items():
            (scratch / name).write_bytes(token_pe(token, section))
        reports = {Path(file["path"]).name: file for file in scan(args.cleave, scratch)}
        for name, (_, required, forbidden) in cases.items():
            traits = {t["id"]: t for t in reports[name].get("traits", [])}
            # Pure OR wrappers are evaluated but omitted from rendered output.
            observed = set(traits)
            if observed & LOOP_ATOMS:
                observed.add(LOOP)
            assert required <= observed, (name, "missing", required - observed)
            assert not forbidden & observed, (name, "unexpected", forbidden & observed)
            assert not RETIRED & traits.keys(), (name, "retired IDs", RETIRED & traits.keys())
            assert not [t for t in traits.values() if t["crit"] >= 4], (name, "false alarm")
        for name, (_, _, transfer, send) in native.items():
            traits = {t["id"] for t in reports[name].get("traits", [])}
            prefix = "micro-behaviors/data/control-flow/dispatch::"
            assert (prefix + "plugin-transfer-command-token" in traits) == transfer, name
            assert (prefix + "send-plugin-command-token" in traits) == send, name
            assert not RETIRED & traits, name
    if args.sample:
        for file in scan(args.cleave, args.sample):
            traits = {t["id"]: t for t in file.get("traits", [])}
            assert not [t for t in traits.values() if t["crit"] >= 4], file["path"]
            assert not RETIRED & traits.keys(), file["path"]
            if file["path"].endswith("package/dist/index.js"):
                assert {GET, ASSIGN} <= traits.keys()
                assert not ({ENV, NAME, LOOP, CI, CHAT} | LOOP_ATOMS) & traits.keys()
    print(f"PASS: {len(cases) + len(native)} controls" + (" and supplied sample" if args.sample else ""))


if __name__ == "__main__":
    main()
