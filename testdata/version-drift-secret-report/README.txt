Tempo gh-actions 252d87d9 version-drift review

Verdict: BENIGN. The flagged reportPrivateKeys is a local push-time detector.
pre-push -> scanFilesInRange -> git diff --name-only -> tracked-file check ->
readFileForScan -> scanFileContent -> reportPrivateKeys -> scanPrivateKeys ->
scanLines(PEM-header regex). A match logs its filename and returns 1; errors
block the push. Conformance vectors are exempted. Text is read locally;
NUL-bearing binaries pass through strings using an argv array. The reporter
neither extracts key bytes nor transmits them. Other credential scanners log
local findings as part of the explicit leak-prevention gate. Git/strings
execution and imported process APIs remain notable detections.

Version evidence
The fetched parent/tag 2ab28a31 (2026-10-09) has 1,180 files, as does the
sample. Only six files differ: the audit workflow, audit-comment action,
their tests, and two READMEs (see review.json). No files were added or removed;
every vendored file is identical. The new feature continues draft-PR audits
after a successful authorized command, requiring a GitHub Actions bot-authored
acknowledgement in the matching audit environment. Forks/Dependabot are still
excluded. Existing event publishing uses configured curl arguments and mTLS
key/cert files, then removes its temporary directory; the new change does not
send signing keys to a new destination. Caller configuration and deployment
state were not supplied.

The flagged member is byte-identical in current 252d87d9, parent 2ab28a31,
and the pinned dependency d3efa0f3 (2026-10-01), with SHA-256
07a65bfa4bbab218e1025e53e238a828ce3712ef315c0083e27fbf3f5ba65d2a.
Thus the queue's claimed clean-earlier/firing-later transition does not
represent newly introduced credential-stealing behavior. The same lexical
false positive exists in the earlier bytes. Forager archives, commit HTML,
commit patch and .forage.json provenance remain in scratch/version-drift-review.
No executable decoding layer was found along the flagged path: its facts have
240 RawScan text records and ordinary source literals, with no fact errors.
Source-local/anonymous-function flow limitations were supplemented manually.

Rule correction (migration.json records every old/new ID)
Nine atoms plus their OR group move out of the wallet-theft objective to
notable source-syntax metadata, preserving every matcher, filter, confidence,
file/platform scope and group exclusion. Invocation-name syntax stays in
call/invocation; fm/fh argument predicates go in call/arguments. Existing leaf
budgets admit the moves. No new namespace, duplicate matcher or blanket
scanner/package/filename exception is introduced.

Unsupported claims corrected:
* report/send PrivateKey/SecretKey: the real sample reports a scan finding,
  not key material. Parentheses also match declarations, not just invocations.
* report/send Seed/Mnemonic and RecoveryPhrase: names alone establish neither
  wallet data nor reporting a value. Existing seeder/spend controls are kept.
* upload/exfil PrivateKey/SecretKey, Seed/Mnemonic, RecoveryPhrase: a name alone
  establishes neither an upload nor secret data. The observable source names
  remain; real network operations retain their own notable or hostile traits.
* trackKeyDerivation: invoking that name does not establish telemetry or theft.
  fm/fh literal arguments do not prove that a mnemonic/hex key was supplied.
  local-derivation.js demonstrates local length-only logging with both markers.
* key-material-reporting OR group: adds no transfer or wallet evidence beyond
  its alternatives, so it is a source-name observation rather than theft.

Removed inherited T1552.001 mappings from the moved metadata. These names do
not establish access to a credential file. Three exact hostile exfiltration
consumers now reference the moved group with unchanged conditions and scope.
An audit of all four YAML tiers found no selectors on the old wallet leaf or
its credential-theft/supply-chain ancestors requiring expansion. The unrelated
obfuscated-wallet-api-relay objective remains intact. Placement/scope and
severity corrections are recorded separately in migration.json.

Coverage evidence
Existing key-reporting-positive, wallet-spend-benign and xrpl-wallet-header-exfil
fixtures preserve their entire finding sets modulo the documented ID moves;
XRPL retains both hostile detections. The original npm @injectivelabs/sdk-ts
1.20.21 was fetched as an independent positive control (hash in review.json).
Its ESM and CJS modules each retain all three hostile exfiltration detections
and every observation. Manual tracing confirms fromMnemonic/fromHex forwards
caller key material to a queue, encodes it, and POSTs it in X-Request-Id to a
char-code-built host, with HTTPS fallback. The names' metadata is still used
by the exfiltration consumers. There is no lost supported attack coverage.

The new scan-report.mts is an exact function excerpt from the actual sample;
mixed-report.js adds real key-reporting implementations, and plural-report.js
uses the same plural helper name for an actual JSON POST. Both still expose
the report-name observation; none is silenced by a scanner exception. Four
new cases participate in testdata/expectations.toml. Existing seed and spend
case manifests were updated to the moved canonical IDs.

Scan comparison
Original archive and pinned dependency were each scanned before/after in
local slow mode without further fetching, including all analyzed members.
Both: distinct hostile 0 -> 0, suspicious 1 -> 0; counting the propagated
archive-parent copy gives suspicious instances 2 -> 0. Archive risk 236 -> 198,
flagged-member risk 46 -> 10. The reporting name remains notable. Every other
finding is identical, verified file-by-file; no observation is removed.
Classifier: BENIGN -> BENIGN; model v18.18 / engine 2.13.0, archive route
classes both 0 and maximum classified FP level -1. The unchanged 0.8341549
aggregate member probability is not an added attack claim. Source-neutral
metadata does not restore unsupported theft severity to alter the score.
No remaining rule/classifier disagreement was found in the reviewed paths.
The model warns its v18 feature specification predates v21. Initial followed
scan omitted 226 further dependency results; the specifically flagged pinned
dependency was independently fetched and fully rescanned. This is static
analysis, not evidence of runtime success or an exhaustive dependency audit.

Reproduce focused before/after comparisons
python3 testdata/version-drift-secret-report/check.py \
  /usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/version-drift-controls-before.jsonl \
  /usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/version-drift-attack-before.jsonl \
  /usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/version-drift-controls-final.jsonl
python3 testdata/version-drift-seeder-report/check.py \
  /usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/version-drift-controls-final.jsonl

Final validation uses the current source-matched validator:
make validate CLEAVE=/usr/local/var/cyclotron/cleave/target/release/cleave
The scan CLI embeds an older validator; reproducible local JSON scans used
CLEAVE_VALIDATE=0 while final validation checks the complete current rules.
