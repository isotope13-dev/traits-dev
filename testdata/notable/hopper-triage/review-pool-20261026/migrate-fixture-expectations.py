"""Retarget positive item assertions and keep negative theft checks effective."""
import json
import re
import tomllib
from pathlib import Path

root = Path(__file__).parent
repo = root.resolve().parents[2]
path = repo / "testdata/expectations.toml"
text = path.read_text()
mapping = json.loads((root / "item-id-map.json").read_text())
fixtures = {r["name"]: r for r in tomllib.loads(text)["hostile"]}
retired = {"env", "dev-secret", "keychain", "wallet", "cloud", "browser", "ssh", "account-db", "appliance-config", "audio", "camera", "clipboard", "screen", "surveillance", "chat"}
base = "objectives/exfiltration/stealer"
replacements = {}
receipts = []
for line in (root / "migrated-fixture-scan.jsonl").open():
    files = json.loads(line)["files"]
    name = files[0]["path"].split("/testdata/hostile/")[-1]
    traits = {t["id"]: t for f in files for t in f.get("traits", [])}
    for prefix in fixtures[name].get("required_prefixes", []):
        if not prefix.startswith(base + "/") or prefix[len(base) + 1:].split("/")[0] not in retired:
            continue
        candidates = {new for old, new in mapping.items() if old.startswith(prefix + "::") or old.startswith(prefix + "/")} & traits.keys()
        candidates = sorted(candidates, key=lambda i: (-traits[i]["crit"], i))
        assert candidates and traits[candidates[0]]["crit"] == 5, (name, prefix, candidates)
        new_prefix = candidates[0].split("::")[0]
        replacements[(name, prefix)] = new_prefix
        receipts.append({"sample": name, "old_required_prefix": prefix, "new_required_prefix": new_prefix, "supported_by_hostile_rule": candidates[0]})

blocks = re.split(r"(?=^\[\[(?:benign|hostile|performance)\]\])", text, flags=re.M)
negative_changes = []
for index, block in enumerate(blocks):
    name_match = re.search(r'^name = "([^"]+)"', block, re.M)
    if not name_match:
        continue
    name = name_match[1]
    def replace_array(match):
        field, value = match.groups()
        values = json.loads(value)
        changed = []
        for prefix in values:
            if field == "required_prefixes":
                changed.append(replacements.get((name, prefix), prefix))
            elif prefix.startswith(base + "/") and prefix[len(base) + 1:].split("/")[0] in retired:
                # All these negative controls represent local-only use or
                # ordinary authentication. No theft class should match them.
                changed.append(base)
                negative_changes.append({"sample": name, "old_forbidden_prefix": prefix, "new_forbidden_prefix": base})
            else:
                changed.append(prefix)
        return field + " = " + json.dumps(list(dict.fromkeys(changed)))
    block = re.sub(r'^(required_prefixes|forbidden_prefixes) = (\[[^\n]*\])$', replace_array, block, flags=re.M)
    if name == "assets-sdk-wallet-env-controls.js":
        block = block.replace("# The concrete secret-named environment read adds one notable capability.", "# Wallet vocabulary and secret-named configuration reads are notable.")
        block = block.replace("cap = 6", "cap = 7").replace("min_score = 6", "min_score = 7")
        block = block.replace('"micro-behaviors/crypto/mnemonic::mnemonic-variable-assignment",', '"micro-behaviors/crypto/mnemonic::mnemonic-variable-assignment", "micro-behaviors/data/parse/vocabulary::wallet-credential-term-cluster",')
        block = block.replace('forbidden_prefixes = ["objectives/credential-access/env/secrets/wallet"]', 'forbidden_prefixes = ["objectives/credential-access/env/secrets/wallet", "objectives/exfiltration/stealer"]')
    blocks[index] = block
path.write_text("".join(blocks))
(root / "fixture-expectation-migration.json").write_text(json.dumps({"positive_assertions": receipts, "strengthened_negative_assertions": negative_changes, "benign_score_change": "assets-sdk-wallet-env-controls.js now requires the neutral wallet-vocabulary observation and seven points, while forbidding all theft classes."}, indent=2) + "\n")
print("Positive item assertions:", len(receipts), "negative assertions:", len(negative_changes))
