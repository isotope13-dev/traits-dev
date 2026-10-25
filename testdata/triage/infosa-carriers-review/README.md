All three requested samples are MALICIOUS. The Node and Python carriers hand
the same raw AppleScript to `osascript -e` at module load. Independent extraction
confirms that both payloads equal the standalone script after trimming outer
whitespace. There is no additional encoding or obfuscation layer.

The payload impersonates System Preferences, captures a masked login password
and retries until `dscl` accepts it. It reads Chrome Safe Storage through the
Keychain CLI, stages that secret and Keychain/AWS/SSH files, archives the staging
directory and uploads the ZIP with curl PUT. When Trezor Suite exists, it also
downloads a ZIP, replaces the installed wallet's ASAR and Info.plist, signs the
bundle ad hoc and clears extended attributes. These combined actions outweigh
the public-registry provenance. Original package identity/version, deployment
authorization and the downloaded ZIP's contents were not supplied.

The prompted password is not explicitly saved or sent. No persistence,
privilege escalation or cleanup is implemented in these files. Cancellation,
missing stores, access restrictions or failed commands can interrupt execution;
the verdict does not assume runtime success or a particular final wallet payload.

| Sample | Hostile before → after | Suspicious before → after | ML probability before → after | Calibrated FP level |
|---|---:|---:|---:|---:|
| `22b83c7f93fe` Node carrier | 5 → 5 | 6 → 5 | .9976325 → .99806845 | 1750 → 1750 |
| `7c1e8a779e74` Python carrier | 5 → 5 | 8 → 7 | .9995157 → .999704 | 0 → 0 |
| `1aef4855436b` AppleScript | 5 → 5 | 9 → 8 | .99024624 → .99024624 | 0 → 0 |

These comparisons use a git HEAD rules snapshot and this checkout, with
reference following disabled in both. Every input has one analyzed file and no
archive members. The initial default-follow AppleScript report additionally
serialized the derived suspicious `applescript-password-phishing` aggregate
(5H/10S); the controlled baseline is 5H/9S. This presentation difference is not
a rule change. Controlled scans lose only the two explicitly relocated IDs.

The copy/ASAR/signing co-occurrence now belongs to `micro-behaviors/crypto/sign`
at notable. Its exact predicates, 1200-byte proximity and scope are preserved.
The maintenance control demonstrates that those facts need not be process
masquerading. The hostile rule retains its predicates and severity, with its
new home under `objectives/supply-chain/trojanized/app/wallet`: it adds a masked,
validated password prompt to the trusted-application substitution context.
Both descriptions explicitly describe co-occurrence rather than a proved
source-to-destination join. There is no material attack coverage loss.

The new HTTP PUT observation requires an explicit curl method option and a
complete PUT token. It permits only argument-free flag clusters before the
option, so `curl -d -X PUT` is correctly rejected. It also rejects PUT text in
quoted data, POST, and method-name prefixes. The rule uses no sample-specific
host, token, staging filename or wallet brand.

Run `python3 testdata/triage/infosa-carriers-review/check.py` to check all eleven
static controls. Nothing is executed except Cleave. The renamed Ledger/host/
staging positive retains all five hostile behaviors. Existing outside fixtures
`cap-native-deps-setup.js`, `tradertraitor-safari-updater.sh`, and
`sign-only-installer.sh` retain every original finding and severity; the malicious
updater retains 3H/2S. No consumers select the moved wallet IDs or their old
ancestors outside the original file. Crypto ancestor consumers were inspected
for scope, cardinality and proximity effects; no attack detection changes.

All samples remain on the classifier alert grid. No new classifier miss is
exposed. The installed v18.18 model lacks current feature-spec-21 additions,
and JavaScript retains a `flow-query-incomplete` gap; direct source review
establishes the payload independently. `review.json` records the original
paths, hashes, marker notes, comparisons, consumer audit and limitations.
