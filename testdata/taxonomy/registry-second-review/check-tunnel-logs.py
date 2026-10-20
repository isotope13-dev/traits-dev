"""Check neutral log observations and relay positive/near-miss controls.

Run from the traits root: python3 testdata/taxonomy/registry-second-review/check-tunnel-logs.py
Fixtures are scanned only; no relay is executed or connected to the network.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PIVOT = "objectives/command-and-control/channel/tunnel/relay::python-websocket-socks-multiplex-pivot"
UA = "objectives/evasion/masquerade/traffic::rotating-browser-unverified-websocket-relay"
READ = "micro-behaviors/process/io/stream::python-read-framed-send"
WRITE = "micro-behaviors/process/io/stream::python-indexed-stream-write"
source = (HERE / "relay.py").read_text()

cases = {
    "relay.py": (source, {PIVOT, UA, READ, WRITE}, set()),
    "renamed.py": (source.replace("/tunnel", "/bridge").replace("controller.example.invalid", "alternate.example.invalid"), {PIVOT, UA}, set()),
    "verified.py": (source.replace("ctx.check_hostname = False", "ctx.check_hostname = True").replace("ssl.CERT_NONE", "ssl.CERT_REQUIRED"), {READ, WRITE}, {PIVOT, UA}),
    "no-target-write.py": (source.replace("streams[stream_id].write(payload)", "pass"), {READ}, {PIVOT, UA, WRITE}),
    "unrelated-buffer.py": (source.replace("pack_frame(MSG_DATA, stream_id, data)", "pack_frame(MSG_DATA, stream_id, b'fixed')"), {WRITE}, {PIVOT, UA, READ}),
    "no-address-decode.py": (source.replace("payload[2:2 + alen].decode()", "'fixed.example.invalid'"), {READ, WRITE}, {PIVOT, UA}),
    "no-browser-rotation.py": (source.replace("random.choice(ua_pool)", "'Relay/1.0'"), {PIVOT}, {UA}),
    "header-only.py": ("import ssl, struct, websockets\nTUNNEL_PATH='/tunnel'\nctx=ssl.create_default_context()\nctx.check_hostname=False\nctx.verify_mode=ssl.CERT_NONE\npacket=struct.pack('!BHI',1,0,0)\n", set(), {PIVOT, UA}),
    "database-errors.txt": ((HERE / "database-errors.txt").read_text(), {
        "micro-behaviors/data/db/sql::jdbc-driver-and-lookup-errors",
        "metadata/file/encoding::base64-chained-whoami-command",
    }, set()),
}
with tempfile.TemporaryDirectory(prefix="controls-", dir=HERE) as tmp:
    paths = []
    for name, (content, _, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json", *paths], text=True, capture_output=True, check=True)
    reports = {}
    remaining = result.stdout.strip()
    decoder = json.JSONDecoder()
    while remaining:
        report, consumed = decoder.raw_decode(remaining)
        reports.update({Path(f["path"]).name: f for f in report["files"]})
        remaining = remaining[consumed:].strip()
    for name, (_, required, forbidden) in cases.items():
        traits = reports[name]["traits"]
        ids = {t["id"] for t in traits}
        assert required <= ids, (name, "missing", required - ids)
        assert not forbidden & ids, (name, "unexpected", forbidden & ids)
        if name == "database-errors.txt":
            assert all(t["crit"] < 4 for t in traits), (name, "log must remain neutral")
        else:
            assert all(t["crit"] < 5 for t in traits), (name, "no unsupported hostile claims")
        print("PASS", name)
