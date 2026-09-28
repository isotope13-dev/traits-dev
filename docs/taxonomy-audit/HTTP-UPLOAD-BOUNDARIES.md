# HTTP upload: source, channel, and local capability

This pass moves **98 rules**, including 91 from the oversized HTTP-upload leaf.
`objectives/exfiltration/http/upload` falls from **176 to 85** combined rules.
No directory exception, matcher relaxation, confidence change, or criticality
change is used. The seven related moves cover three encrypted-channel siblings,
three hybrid-crypto observations, and the neutral Compress-Archive atom needed
by a relocated archive-construction composite.

The [move manifest](http-upload-moves.csv) records every destination and normalized
definition hash. [61 descriptions](http-upload-labels.json) and 13 IDs are clarified.
The updated TAXONOMY.md contracts distinguish source ownership, archive payloads,
payload encryption, ordinary encoding, and neutral HTTP construction.

## Placement decisions

Required source data takes precedence over HTTP, encoding, or the implementation
language. Appliance configuration exports now share one source home across Lua,
Python, PHP, PowerShell, JavaScript, native code, and DNS/HTTP channels. Environment,
account-store, image, file, and network-configuration exports follow their own
sources. A source alternative is not promoted into a required narrower subtype.
For example, the header/archive Python classifier remains under HTTP upload:
its alternatives include gzip compression without a required archive.

Without a required narrower source, an archive payload or archive creation selects
`http/archive`. Required payload cryptography selects `http/encrypted`; archive
takes precedence when both apply. Ordinary encoding and obfuscated HTTP syntax
retain `http/encoded`. These locations do not certify the strength of every
pre-existing objective: transfer and source assertions still need individual review.

Three new leaves add distinctions without additional depth:

| Leaf | Rules | Admission and exclusions |
|---|---:|---|
| `micro-behaviors/crypto/hybrid` | 4 | Symmetric/asymmetric combinations, envelopes, algorithm pairs and key wrapping. A provider name, standalone signer or single cipher is insufficient. Three observations move up one level from `crypto/library/hybrid`. |
| `micro-behaviors/data/serialize/bittorrent` | 4 | Metainfo construction, including tracker/web-seed configuration and archive publication. Existing field/format references remain in `data/format/bittorrent`; ordinary publication is not theft. |
| `objectives/exfiltration/http/encrypted` | 10 | HTTP export classifiers requiring payload cryptography without a required narrower source or archive payload. TLS alone does not select this leaf. |

Neutral observations move to their corresponding operations. Notable examples:

- `Content-Type: image/ppm` describes a MIME type, not a screenshot or upload.
- `Transfer-Encoding: chunked` describes HTTP framing, not Base64 encoding.
- FormData field insertion does not require submission.
- Socket-buffer sends have no intrinsic stolen-data subject.
- Release/banner paths, root SSH-key paths and appliance configuration paths are
  locators; their descriptions no longer claim a read or export.
- Tar/ZIP construction, Base64 conversion and an upload-consent prompt stay local
  capabilities until a consuming classifier supplies transfer context.

## Consumers and preservation

The proof protects **276 definitions**, including exact consumers and broad
consumers. All moved matcher bodies, effective scopes, exclusions, confidence,
criticality and ATT&CK settings are unchanged. No identical atomic matcher body
requiring a merge was found among the moves. The inventory checkpoint contains 118,813 rules. A later preservation check
contains 118,811 rules and records 17
[outside changes](http-upload-concurrent-changes.json); all 276 protected
definitions still pass. These catalog changes are outside this migration.

The [directory audit](http-upload-directory-consumers.csv) covers **151 references
in 130 consumers**. Neutral HTTP/path/archive capabilities join their actual
subjects. Local packaging, schema fields, route strings and prompts no longer
supply an exfiltration objective through an ancestor-directory match.

[Four explicit consumer repairs](http-upload-consumer-repairs.json) retain moved
exporters and relevant HTTP capabilities for LLM document export, passkey export,
the browser/wallet profiler, and the paste-service encryption classifier. They
use exact IDs rather than widening to whole new source directories. The DNS-only
appliance rule intentionally stops contributing HTTP transfer evidence.

The profiler formerly required a discovery directory, an HTTP directory, and
`needs: 2` over exactly two named source composites. Rewriting those two source
requirements as `all` leaves one `any` for HTTP alternatives, without introducing
an incorrectly placed helper or alias. No spatial constraint was removed.
[128 Boolean comparisons](http-upload-boolean-check.json) verify the actual old/new
conditions: 64 cases without deliberately removed non-transfer evidence preserve
results, and one local-field-only case intentionally stops reporting export.
Focused controls exercise both required sources, transfer absence, and a missing
wallet source through the real engine.

## Engine registration and verification

The new crypto category is registered in cleave's
`src/capabilities/validation/directory_whitelist.rs`. The first release build
exposed pre-existing dependency mismatches for NE/DOS COM and CFML features.
Building against the already-present local filefacts and stng working copies
succeeded; no analyzer was edited for this task. The
[registration/build record](http-upload-engine-registration.json) records the command.

All **1,841 corpus fixtures** pass using the rebuilt engine in a temporary copy
restoring only the known shell-decoder regression. The
[isolation record](http-upload-validation-isolation.json) contains both definitions.
The live repository still fails the PyAigis shell-decoder check. Strict validation
now reports **92 diagnostics**, with **146 over-cap directories**. The new hybrid
category no longer produces an unknown-directory diagnostic.

All **83 focused assertions across 37 files** pass (45 new assertions across
18 files, plus 38 established source-routing assertions across 19 files).
Focused controls and their results are recorded in
[the verification manifest](http-upload-verification.json), with runnable examples
in [the fixture directory](../../testdata/taxonomy/http-upload/README.md).
Fixtures are scanned, never executed. No test or rule file is excluded from the
isolated corpus.

## Remaining work and validator opportunities

Reaching 85 does not certify the 85 remaining rules. Priority reviews are:

1. `python-audit-hook-basic-auth-send` requires an audit hook and an authentication
   handler but no actual send. The Windows/Unix staged-archive wrappers require
   paths and endpoint clues without a transfer operation. Audit their consumers
   before tightening or retiring unsupported wrappers.
2. The JVM bundle classifier, GitHub environment/release fallbacks, ICP/AES
   alternatives, mixed host-report source wrappers and generic HTTP endpoint
   classifiers need required-source/transfer review. Do not force their optional
   evidence into a narrow source simply to empty the directory.
3. The remaining `crypto/library/hybrid` rules include generic provider operations,
   standalone signing, individual algorithms and a filename-signature map clue.
   They do not all belong in the new hybrid leaf. Route them by their own claims.
4. The wallet profiler currently excludes the entire blockchain-library branch.
   A component matching the bare word `wallet` is therefore enough to suppress
   otherwise valid wallet targeting, including `wallet.dat`. A positive control
   uses a wallet-extension ID with a neutral variable name to test the eligible
   branch. This pre-existing false-negative mechanism belongs in the next
   blockchain/library and exclusion audit; it was not silently changed here.
5. Keep duplicate-body diagnostics separate from semantic duplicate review.
   Also flag impossible file-type branches and broad capability directories used
   as artifact-identity exclusions. A capability clue is not proof that the
   analyzed file is an independently identified library.

Follow-up: the [blockchain operation audit](BLOCKCHAIN-OPERATION-BOUNDARIES.md)
removes the blanket wallet/library exclusion described above and verifies the
previously suppressed `wallet.dat` profiler case. It also removes the redundant
ZIP alternative introduced by the Compress-Archive relocation.

The broader cap migration and semantic audit remain open.
