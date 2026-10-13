"""Check tampering, endpoint and UPX inheritance with non-executed controls.

Usage: python3 check_hostile.py UNPACKED_PE PACKED_PE --out /tmp/triage/controls
All specimens and scan outputs are written outside the repository.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
DENIAL = "micro-behaviors/communications/http/response::x86-signed-suffix-404-response"
FILTER = "micro-behaviors/data/collection/filter::x86-server-link-host-section-filter"
HOST = "micro-behaviors/communications/http/url/port::x86-affine-xor-selected-tld-https-custom-port"
IP = "micro-behaviors/communications/http/download/url::cleartext-external-ip-fetch-context"
HTTPS = "micro-behaviors/communications/http/download/url::custom-port-selected-tld-https-fetch-context"
TAMPER = "objectives/evasion/anti-av/verification::eset-update-signature-suppression-proxy"
ROTATE = "objectives/evasion/anti-av/signature::update-tamper-scheduled-image-hash-rotation"
RUN = "objectives/persistence/login/registry/run-key::update-tamper-proxy-hklm-run-autostart"
KILL_FLOW = "micro-behaviors/process/terminate/kill::x86-open-check-terminate-process"
SWAP_FLOW = "micro-behaviors/process/deploy::x86-image-swap-relaunch"
KILL = "objectives/impact/degrade/process::update-tamper-proxy-kills-port-owner"
SWAP = "objectives/execution/payload/file-exec::update-tamper-proxy-replaces-and-launches-image"
SELECTED = {DENIAL, FILTER, HOST, IP, HTTPS, TAMPER, ROTATE, RUN, KILL_FLOW, SWAP_FLOW, KILL, SWAP}
ADMITTED = {TAMPER, ROTATE, RUN, KILL, SWAP}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("unpacked", type=Path)
    p.add_argument("packed", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--cleave", default="cleave")
    args = p.parse_args()
    data = args.unpacked.read_bytes()
    fixtures = args.out / "specimens"
    fixtures.mkdir(parents=True, exist_ok=True)
    # These reviewed VAs locate mutation sites only, never rule matchers.
    offset = lambda va: va - 0x400000 - (0xC00 if va < 0x41E000 else 0x2000)
    def patch(va, value):
        mutated = bytearray(data)
        mutated[offset(va):offset(va)+len(value)] = value
        return bytes(mutated)
    def replace(old, new):
        assert len(old) == len(new) and old in data
        return data.replace(old, new)
    def encode(host, a=31, b=7, key=0x5A):
        return bytes(ch ^ key ^ ((a*i+b)&255) for i, ch in enumerate(host.encode()))
    utf16 = lambda text: text.encode("utf-16le")
    host_variation = bytearray(data)
    host_variation[offset(0x421DF8):offset(0x421DF8)+9] = encode("id.ab.xyz", 23, 11)
    host_variation[offset(0x416BE3)] = 23
    host_variation[offset(0x416BEF)] = 11
    identity_variation = replace(utf16("Eupdate Helper"), utf16("Generic Helper"))
    identity_variation = identity_variation.replace(b"47.108.48.69", b"46.108.48.69")
    cases = [
        ("positive", data, SELECTED),
        ("renamed-product-and-ip", identity_variation, SELECTED),
        ("affine-key-and-tld-variation", bytes(host_variation), SELECTED),
        ("unreferenced-signed-token", patch(0x4146CA, struct.pack("<I", 0x41F708)), SELECTED-{DENIAL}-ADMITTED),
        ("non-404-response", patch(0x414735, struct.pack("<I", 403)), SELECTED-{DENIAL}-ADMITTED),
        ("unreferenced-server-section", patch(0x417C5E, struct.pack("<I", 0x41F330)), SELECTED-{FILTER}-ADMITTED),
        ("no-host-section-filter", patch(0x417CA8, b"\x00"), SELECTED-{FILTER}-ADMITTED),
        ("ordinary-update-path", replace(b".signed\0", b".foobar\0"), SELECTED-{DENIAL}-ADMITTED),
        ("no-scheduled-rotation", replace(utf16("cron triggered"), utf16("task triggered")), SELECTED-{ROTATE}),
        ("no-autostart-success", replace(utf16("HKLM Run set ->"), utf16("HKLM Run ask ->")), SELECTED-{RUN}),
        ("https-standard-port", patch(0x415D97, struct.pack("<I",443)), SELECTED-{HOST,HTTPS}),
        ("decoded-common-tld", patch(0x421DF8, encode("id.zz.com")), SELECTED-{HOST,HTTPS}),
        ("wrong-decoder-key", patch(0x415E2B, b"\x5b"), SELECTED-{HOST,HTTPS}),
        ("unrelated-https-string", patch(0x415E5E, struct.pack("<I",0x41E9B4)), SELECTED-{HOST,HTTPS}),
        ("private-ip", replace(b"47.108.48.69", b"10.108.48.69"), SELECTED-{IP}),
        ("termination-logging-only", patch(0x4132AB, b"\x90\x90"), SELECTED-{KILL_FLOW,KILL}),
        ("different-exit-state-slot", patch(0x413294, struct.pack("<I",0xfffffd48)), SELECTED-{KILL_FLOW,KILL}),
        ("replacement-logging-only", patch(0x412E9B, b"\x90\x90"), SELECTED-{SWAP_FLOW,SWAP}),
        ("launches-different-path", patch(0x412EE3, struct.pack("<I",0xfffffbdc)), SELECTED-{SWAP_FLOW,SWAP}),
        ("packed-parent", args.packed.read_bytes(), SELECTED),
    ]
    expected = {}
    for name, content, required in cases:
        path = fixtures/(name+".exe")
        path.write_bytes(content)
        expected[path.name] = required
    env = {**os.environ, "CLEAVE_CACHE_DIR": str(args.out/"cache"),
           "CLEAVE_TRAITS_DIR":str(ROOT),
           "CLEAVE_SKIP_CACHE":"1", "CLEAVE_SKIP_YARA_CACHE":"1",
           "CLEAVE_BUILTIN_YARA_ONLY":"1", "RAYON_NUM_THREADS":"2"}
    result = subprocess.run([args.cleave,"--traits-dir",str(ROOT),"--format","jsonl",str(fixtures)],
                            capture_output=True,text=True,check=True,env=env,timeout=1200)
    (args.out/"scan.jsonl").write_text(result.stdout)
    reports = {}
    for line in result.stdout.splitlines():
        doc = json.loads(line)
        for report in doc.get("files", [doc] if "path" in doc else []):
            path = report["path"]
            if "!!" not in path:
                reports[Path(path).name] = report
    results=[]
    for name, required in expected.items():
        traits = reports[name]["traits"]
        observed = {t["id"] for t in traits}&SELECTED
        assert observed == required, (name,sorted(observed),sorted(required))
        results.append({"case":name,"passed":True,"matched":sorted(observed),
                        "hostile":sum(t["crit"]==5 for t in traits)})
    (args.out/"results.json").write_text(json.dumps(results,indent=2)+"\n")
    print(f"Passed {len(results)} tampering, endpoint, variation and UPX inheritance controls")


if __name__ == "__main__":
    main()
