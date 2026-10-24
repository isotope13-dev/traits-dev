"""Check saved atomscan reports; this never imports or runs fixture code."""
import argparse
import json
from pathlib import Path

SSH = "objectives/command-and-control/backdoor/ssh::published-anonymous-ssh-shell"
SFTP = "objectives/command-and-control/backdoor/control/file-manager::published-anonymous-unconfined-sftp"
PIVOT = "objectives/command-and-control/backdoor/proxy/reverse::published-anonymous-ssh-tcp-pivot"
UNAME = "objectives/exfiltration/stealer/system-info/platform::default-ssh-collector-uname-report"
REPORT = "objectives/command-and-control/infrastructure/dead-drop::python-default-collector-ssh-access-report"
MEMORY = "micro-behaviors/fs/proc/memory::python-fragmented-proc-memory-dump"
PACK = "objectives/anti-static/obfuscation/payload/resource::native-table-decoded-clr-resource"
QUERIES = "micro-behaviors/os/sysinfo/profile::python-host-information-query-combination"
FORWARD = "micro-behaviors/communications/ssh/forward::asyncssh-remote-port-forward"
DEFAULT = "micro-behaviors/communications/http/client/configure::python-fixed-http-url-default-return"
EXPECTED = {
    "renamed-public-gateway.whl": {SSH, SFTP, PIVOT, UNAME, REPORT},
    "renamed-collector.whl": {SSH, SFTP, PIVOT, UNAME, REPORT},
    "version-9-renamed.whl": {SSH, SFTP, PIVOT, REPORT},
    "configured-collector.whl": set(),
    "unused-default.whl": set(),
    "health-body.whl": set(),
    "authenticated-gateway.whl": {REPORT},
    "no-remote-command.whl": {REPORT},
    "confined-sftp.whl": {SSH, PIVOT, UNAME, REPORT},
    "forwarding-denied.whl": {SSH, SFTP, UNAME, REPORT},
    "proc-stat.py": set(),
    "proc-memory.py": {MEMORY},
    "ssh-forward.py": set(),
    "ssh-forward-name.py": set(),
    "host-single.py": set(),
    "host-double.py": set(),
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    seen = set()
    retained = 0
    for line in args.report.read_text().splitlines():
        record = json.loads(line)
        files = record["raw"]["files"]
        name = Path(files[0]["path"]).name
        all_ids = {t["id"] for f in files for t in f.get("traits", [])}
        high = {t["id"]: t["crit"] for f in files for t in f.get("traits", []) if t["crit"] >= 4}
        if name in EXPECTED:
            assert set(high) == EXPECTED[name], (name, set(high), EXPECTED[name])
            seen.add(name)
            if name.startswith("ssh-forward"):
                assert (FORWARD in all_ids) == (name == "ssh-forward.py"), name
            if name.startswith("host-"):
                assert (QUERIES in all_ids) == (name == "host-double.py"), name
            if name in {"renamed-public-gateway.whl", "renamed-collector.whl", "configured-collector.whl", "unused-default.whl"}:
                assert (DEFAULT in all_ids) == name.startswith("renamed-"), name
        elif "_d3e76705582a7a060d989c2dd4edebff_" in name or "_d3c6b4c686f527e3fbe71de604ed3856_" in name:
            assert high.get(PACK) == 4, (name, high)
            retained += 1
    assert seen == set(EXPECTED), ("Missing fixture reports", set(EXPECTED) - seen)
    assert retained == 2, ("Missing protected-binary controls", retained)
    print(f"Passed {len(seen)} boundary cases and {retained} retained positives")

if __name__ == "__main__":
    main()
