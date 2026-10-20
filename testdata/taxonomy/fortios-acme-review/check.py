"""Check ACME activation requirements and close-event cleanup as inert text.

The attack context is FortiOS auto-script traversal, not the CA hostname or
an attacker-chosen filename. Ordinary certificate management remains notable.
Reference: https://httpd.apache.org/docs/2.4/mod/mod_md.html#mdchallengedns01
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
USAGE = "micro-behaviors/crypto/certificate/usage::"
PERSIST = "objectives/persistence/system/network-appliance::acme-renewal-hook-persistence"
CLEANUP = "micro-behaviors/fs/delete/file/deferred::node-close-callback-unlink-sync"
CA = "MDCertificateAuthority https://ca.example.invalid/acme/directory"
DNS = "MDCAChallenges dns-01"
HOOK = 'MDChallengeDns01 "/usr/bin/node"'
RENEW = "MDRenewMode always"
CONFIG = "\n".join([HOOK, CA, DNS, RENEW])
ATTACK = ('config system auto-script\nedit "../../../changed.conf"\n'
          'set script "' + CONFIG + '"\nnext\nend\n')
REQUIRED = {PERSIST, USAGE + "apache-md-certificate-authority-url",
            USAGE + "apache-md-dns01-challenge-selection"}

# Expect only the documented conjunction to establish hostile persistence.
cases = [
    ("attack.py", "configuration = r'''" + ATTACK + "'''", REQUIRED, set(), None),
    ("attack.ps1", "$configuration = @'\n" + ATTACK + "'@\n", REQUIRED, set(), None),
    ("attack.txt", ATTACK, REQUIRED, set(), None),
    ("audit.txt", 'action="Add" cfgpath="system.auto-script" '
     'cfgobj="../../../changed.conf" cfgattr="script['
     + CONFIG.replace("\n", "\\n") + ']"', REQUIRED, set(), None),
    ("configuration.json", json.dumps({"config": CONFIG}),
     REQUIRED - {PERSIST}, {PERSIST}, 3),
    ("ordinary.txt", CONFIG, REQUIRED - {PERSIST}, {PERSIST}, 3),
    ("no-dns.txt", ATTACK.replace(DNS, ""), set(), {PERSIST}, 4),
    ("http-challenge.txt", ATTACK.replace(DNS, "MDCAChallenges http-01"),
     set(), {PERSIST, USAGE + "apache-md-dns01-challenge-selection"}, 4),
    ("no-ca.txt", ATTACK.replace(CA, ""), set(), {PERSIST}, 4),
    ("manual.txt", ATTACK.replace(RENEW, "MDRenewMode manual"), set(), {PERSIST}, 4),
    ("normal-script.txt", ATTACK.replace("../../../changed.conf", "daily-check"),
     set(), {PERSIST}, 3),
    ("close.py", "script = \"child.on('close',()=>{fs.unlinkSync(target)})\"",
     {CLEANUP}, set(), 3),
    ("close-lines.txt", 'child.on( "close", () => {\n fs.unlinkSync (target);\n})',
     {CLEANUP}, set(), 3),
    ("finish.txt", "stream.on('finish',()=>{fs.unlinkSync(target)})",
     set(), {CLEANUP}, None),
    ("unrelated.txt", "child.on('close',()=>{done()}); fs.unlinkSync(target)",
     set(), {CLEANUP}, None),
]

with tempfile.TemporaryDirectory(prefix="fortios-acme-review-") as tmp:
    paths = []
    for name, content, *_ in cases:
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--json", *paths], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    reports = {}
    for line in result.stdout.splitlines():
        for file in json.loads(line).get("files", []):
            reports[Path(file["path"]).name] = file
    for name, _, present, absent, maximum in cases:
        traits = {t["id"]: t["crit"] for t in reports[name].get("traits", [])}
        for trait in present:
            assert trait in traits, (name, "missing", trait)
            assert traits[trait] == (5 if trait == PERSIST else 3), (name, trait)
        assert not absent.intersection(traits), (name, "unexpected", absent.intersection(traits))
        if maximum is not None:
            assert max(traits.values(), default=0) <= maximum, (name, traits)

print(f"PASS: {len(cases)} ACME and cleanup positive/near-miss controls")
