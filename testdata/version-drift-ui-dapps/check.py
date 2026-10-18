#!/usr/bin/env python3
"""Exercise wallet acquisition boundaries and Web3 message-signing syntax."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLUSTER = "objectives/credential-access/wallet/keywords::crypto-wallet-keyword-cluster"
SIGN = "micro-behaviors/crypto/sign::web3-accounts-message-sign"
BRAND = "micro-behaviors/os/application/target::crypto-wallet-keyword-cluster--rx-1"
names = 'const providers = ["metamask", "metamask", "metamask", "metamask"];\n'
cases = {
    "routes.ts": (names + 'navigate("profile-create/metamask");', set()),
    "phrase.ts": ('const mnemonic = phrase; validate(mnemonic); save(mnemonic); '
                  'returnMnemonic(mnemonic);', set()),
    "path-reference.js": (names + 'const location = "Ethereum/keystore";', set()),
    "ordinary-read.js": (names + 'require("fs").readFileSync("settings.json");', set()),
    "wallet-read.js": (names + 'require("fs").readFileSync("Ethereum/keystore/key.json");',
                       {CLUSTER}),
    "message.ts": ('return this.bcc.web3.eth.accounts.sign(message, key).signature;', {SIGN}),
    "direct-message.js": ('web3.eth.accounts.sign(message, key);', {SIGN}),
    "reference.js": ('// web3.eth.accounts.sign(message, key)\n'
                     'const example = "web3.eth.accounts.sign(message, key)";', set()),
    "transaction.js": ('web3.eth.accounts.signTransaction(transaction, key);', set()),
}

with tempfile.TemporaryDirectory(prefix="evdrift-") as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "jsonl", "analyze", *paths],
        capture_output=True, text=True,
    )
assert result.returncode == 0, result.stderr
observed = {}
decoder = json.JSONDecoder()
remaining = result.stdout
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for artifact in report.get("files", []):
        observed[Path(artifact["path"]).name] = {
            trait["id"] for trait in artifact.get("traits", [])
        }
assert set(observed) == set(cases), observed
for name, (_, expected) in cases.items():
    assert observed[name] & {CLUSTER, SIGN} == expected, (name, observed[name])
for name in ("routes.ts", "path-reference.js", "ordinary-read.js", "wallet-read.js"):
    assert BRAND in observed[name], (name, observed[name])
print(f"Passed {len(cases)} wallet acquisition and signing cases")
