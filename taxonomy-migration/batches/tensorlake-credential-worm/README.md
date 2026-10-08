# Tensorlake 0.5.144 credential-worm triage

The inspected tarball is MALICIOUS, SHA-256
`33108f494dad71369a9aa7cd6daa5402335d1a718b78320b9b687c0b2174fa67`.
This judgement applies to these release bytes, not the package name generally.
The SDK bundles are legitimate API, sandbox and worker implementations.
`package.json` adds `preinstall: node lib/setup.mjs`; the added setup script
bootstraps Bun and launches the added `lib/Math_Symbol.js` worm.

## Recovered behavior

Static inspection decoded the rotated RC4/string tables without evaluating the
payload, then recovered its custom Base91/PBKDF2/substitution strings and
AES-GCM/gzip embedded resources. The source:

- skips common CI environments in the installer and launches a detached daemon;
- collects developer tokens, browser/wallet stores, cloud credentials, runner
  secrets and repository secrets through a planted Actions workflow;
- encrypts collection envelopes, sends them to `iseekaigogo.com`, and supports
  public GitHub repository export using stolen tokens;
- downloads npm packages, inserts its own install hook and payload, bumps patch
  versions, repacks and publishes using harvested publisher credentials;
- commits Claude SessionStart and VS Code folderOpen shell hooks to repositories;
- installs a GitHub-token monitor through launchd, systemd user services or a
  Windows scheduled task. HTTP 400–409 executes a handler deleting the user's
  home directory (`rm -rf ~/` or recursive removal of USERPROFILE).

No installer, payload, downloaded runtime or monitor was executed. Discovered
network destinations were not contacted. The archive and both malicious scripts
received `cleave facts`; `atomscan` inspected the original archive and SDK control.

## Placement and coverage changes

Neutral token-format references, file-read/record cooccurrence, terminal output
callbacks, VPN application/configuration paths, developer-secret path references,
encoded bracket open syntax, hexadecimal XOR expressions, browser-store catalogs
and npm maintainer search endpoints move to the micro-behavior home representing
their actual observation. All exact consumers are updated. Matchers, type/platform
scope and exclusions are preserved for placement-only moves. See mapping.tsv.

Separately, generic token-pattern/file-operation cooccurrence becomes notable;
it does not prove theft. Browser directory traversal becomes suspicious rather
than claiming proven credential export. Obfuscation with host fields and a Base64
alphabet becomes suspicious rather than asserting a stealer or data flow.
Obfuscated code beside a declared local npm preinstall is suspicious, not proof
that the manifest executes that particular sibling. Terminal callback registration
is no longer presented as a backdoor. VPN paths have no credential-theft mapping. Chromium/Firefox login filenames
are notable references rather than a suspicious targeting claim.
The generic browser/developer/SSH path catalog retains its paths but loses theft
suppression because reference catalogs are valid neutral observations in scanners.

Hostile collector composites now require obfuscated detached execution and
specific credential evidence. The repository-persistence composite additionally
requires GitHub commit mutation and agent configuration mutation. Wallet-extension
targeting requires traversal and file-read operations. Returning a generic ADDRESS
constant no longer implies wallet-address substitution. ADODB open requires an
ADODB reference; encoded bracket syntax alone moves to neutral dispatch. Date,
temporary write and timeout cooccurrence no longer claims deletion; its composite
uses the canonical setTimeout atom instead of a broad supposed delete matcher.
The latter coverage correction also keeps dispatch below its 100-rule cap.

## Verification

The original archive and Math_Symbol.js retain three hostile detections in token
acquisition, cloud credential acquisition and repository editor persistence.
Their measured precision scores are 12.3, 9.5 and 9.0 (required minimum 3.5).
The SDK members, including dist/index.js and dist/index.cjs, have no hostile or
suspicious detections. setup.mjs has two suspicious obfuscation findings.

Fixtures pair token/file records with a plain reader; credential path catalogs
with ordinary paths; terminal callbacks with unrelated callbacks; encoded bracket
open with plain open; and executable XOR expressions with commented expressions.
An ordinary editor-config writer is a near miss for covert repository persistence;
the original hash-pinned worm is its external positive fixture. Scans use copies
in a neutral scratch directory to avoid repository-fixture suppression. Corpus
validation passes hostile 539/539, benign 988/988, does-nothing 176/176,
drop-exec 45/45, supply-chain 566/566, impact-wipe 67/67, obfuscation 78/78,
reverse-shell 24/24 and simple-stealer 65/65. These are measured controls, not a
claim of universal false-positive freedom.
