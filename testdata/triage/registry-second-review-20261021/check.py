"""Static regression scans; never import or execute the reviewed specimen."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
OLD_BIOS = "objectives/anti-analysis/sandbox-detect/environment/function::python-bios-gated-decoded-launch"
BIOS = "objectives/anti-analysis/environment-detect/check::python-bios-substring-screen"
MAC = "objectives/exfiltration/stealer/system-info/identity::python-mac-checkin-decoded-launch"
HTTP = "micro-behaviors/communications/http/get::python-node-id-url-to-get-helper"
ZONE = "objectives/execution/payload/file-exec::zone-cleared-decoded-zip-forfiles"
DLL = "objectives/evasion/masquerade/extension-mismatch::python-randomized-dll-extension"
RENAMES = {
    "micro-behaviors/crypto/symmetric/decrypt::python-decrypt-function-def":
        "metadata/file/function::python-decrypt-named-function",
    "micro-behaviors/data/decode/custom::python-decrypt-function-decodes-input":
        "metadata/lang/source/shape::python-decrypt-named-function-transform-syntax",
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sample", type=Path, required=True)
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True)
    args = p.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    source = args.sample.read_text()
    cases = []

    def case(name, content, required=(), forbidden=(), old_required=()):
        path = args.work_dir / name
        path.write_text(content)
        cases.append((path, set(required), set(forbidden), set(old_required)))

    case("original.py", source, {BIOS, MAC, HTTP, ZONE, DLL}, old_required={OLD_BIOS, MAC, ZONE})
    renamed = source
    for before, after in (("call_lnk", "send_checkin"), ("lnk", "address"),
                          ("dom", "destination"), ("check_env", "screen_machine"),
                          ("vals", "manufacturers")):
        renamed = re.sub(r"\b" + before + r"\b", after, renamed)
    case("renamed.py", renamed, {BIOS, MAC, HTTP, ZONE, DLL})
    case("random-text-extension.py", source.replace("endswith('.dll')", "endswith('.txt')"),
         {BIOS, MAC, HTTP, ZONE}, {DLL})
    case("extension-disconnected.py", source.replace(
        "os.path.splitext(original_name)[0] + f_ext", "os.path.splitext(original_name)[0] + '.bak'"),
        {BIOS, MAC, HTTP, ZONE}, {DLL})
    case("different-name-extension.py", source.replace(
        "os.path.splitext(original_name)[0] + f_ext", "os.path.splitext(other_name)[0] + f_ext"),
        {BIOS, MAC, HTTP, ZONE}, {DLL})
    # Same loader and BIOS inventory, but no membership test influencing return.
    case("inventory-only.py", source.replace("if t in v:", "if False:"),
         {MAC, HTTP, ZONE}, {BIOS}, {OLD_BIOS})
    # Preserve the node-ID query, send only a constant URL.
    case("unrelated-node-query.py", source.replace(
        'call_lnk(f"{dom}?{\'&\'.join(q)}")',
        'call_lnk("https://example.com/status")'), {BIOS, ZONE}, {MAC, HTTP}, {MAC})
    case("helper-ignores-parameter.py", source.replace(
        "response = requests.get(lnk)",
        'response = requests.get("https://example.com/status")'),
        {BIOS, ZONE}, {MAC, HTTP}, {MAC})
    case("node-name-in-string.py", source.replace(
        'f"{uuid.getnode():012x}."', '"uuid.getnode()."'),
        {BIOS, ZONE}, {MAC, HTTP})
    case("comments-only.py", "\n".join("# " + line for line in source.splitlines()),
         forbidden={BIOS, MAC, HTTP})
    # Existing independent attack and benign fixtures outside this batch.
    for name in ("launcher.py", "plain-launch.py", "read-zone.py", "internet-zone.py"):
        case("existing-" + name, (ROOT / "testdata/triage-renpy-loader" / name).read_text(),
             {ZONE} if name == "launcher.py" else (), {BIOS, MAC, HTTP})
    case("decrypt-declaration.py", "def decrypt_document(data):\n    return data\n",
         {RENAMES[next(iter(RENAMES))]})
    case("decrypt-xor-shape.py", "def decrypt_document(data):\n    return data ^ 7\n",
         set(RENAMES.values()))
    case("sma-declaration-only.py",
         'path = "/usr/local/extranet/etc/policy_file.xml"\ndef helper_decrypt(data):\n    return data\n',
         {RENAMES[next(iter(RENAMES))]},
         {"objectives/credential-access/vpn/config::sma-policy-credential-decrypt"},
         {"objectives/credential-access/vpn/config::sma-policy-credential-decrypt"})
    case("sma-decrypt-call.py",
         'path = "/usr/local/extranet/etc/policy_file.xml"\nplaintext = cipher.decrypt(data)\n',
         {"objectives/credential-access/vpn/config::sma-policy-credential-decrypt"},
         old_required={"objectives/credential-access/vpn/config::sma-policy-credential-decrypt"})
    case("xor-file-inversion.py", '''def helper_decrypt(infile, outfile):
    with open(infile, 'rb') as f:
        data = f.read()
    output = bytes([x ^ 0xFF for x in data])
    with open(outfile, 'wb') as f:
        f.write(output)
''', {"objectives/anti-static/obfuscation/encoding/xor::python-file-byte-inversion"},
         old_required={"objectives/anti-static/obfuscation/encoding/xor::python-file-byte-inversion"})
    for name in ("py-doctest-decrypt-def-controls.py", "py-decrypt-word-controls.py"):
        case("existing-" + name, (ROOT / "testdata/benign" / name).read_text())
    case("existing-png-tail-decrypt.py", (ROOT / "testdata/hostile/png-tail-decrypt.py").read_text())
    # Real existing positive/negative XOR controls exercise migrated consumers.
    for name in ("xor-loader.py", "xor-key-material.py", "xor-near-miss.py"):
        case("existing-" + name,
             (ROOT / "testdata/triage/lpeclient-blihan-first-review" / name).read_text())

    def scan(item):
        path, required, forbidden, old_required = item
        reports = []
        for traits in (args.baseline, ROOT):
            result = subprocess.run(["cleave", "--traits-dir", str(traits), "--format", "json", str(path)],
                                    capture_output=True, text=True, check=True)
            assert "WARN" not in result.stderr, (path.name, result.stderr)
            report = json.loads(result.stdout)
            reports.append({t["id"]: t["crit"] for f in report["files"] for t in f.get("traits", [])})
        old, new = reports
        assert old_required <= old.keys(), (path.name, "baseline missing", old_required - old.keys())
        assert required <= new.keys(), (path.name, "missing", required - new.keys())
        assert not forbidden & new.keys(), (path.name, "unexpected", forbidden & new.keys())
        assert OLD_BIOS not in new
        # Everything else, including existing hostile fixture coverage and the
        # two source observations, must survive at the same severity.
        allowed_losses = {OLD_BIOS, MAC, *RENAMES}
        if path.name == "sma-declaration-only.py":
            allowed_losses.add("objectives/credential-access/vpn/config::sma-policy-credential-decrypt")
        lost = {k for k in old.keys() - new.keys() if old[k] >= 3} - allowed_losses
        assert not lost, (path.name, "lost notable coverage", lost)
        for before, after in RENAMES.items():
            if before in old:
                assert after in new and old[before] == new[after], (path.name, before)
        return {"case": path.name, "passed": True,
                "removed": sorted(old.keys() - new.keys()),
                "added": sorted(new.keys() - old.keys())}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(scan, cases))
    (args.work_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} static comparisons")


if __name__ == "__main__":
    main()
