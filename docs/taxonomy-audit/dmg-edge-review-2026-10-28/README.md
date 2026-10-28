# DMG edge-case review — 2026-10-28

Ten inputs were inspected individually. Source labels and old scanner scores were treated as leads. No specimen code was executed. Archives were unpacked without mounting; scripts, structural facts, signatures and selected native functions were inspected. The staging directory was deleted during review; all ten originals were recovered from the authenticated Hopper API and verified against the recorded SHA-256 hashes.

| SHA-256 prefix | Sample | Verdict | Current H / S |
|---|---|---|---:|
| `39a860e5336e` | July Setup DMG A | bad | 22 / 24 |
| `581d825f60e3` | July Setup DMG B | bad | 22 / 24 |
| `5f2f261e664b` | OneSafe Mac Cleaner | purgatory | 0 / 0 |
| `8426b7aa2182` | ZuRu archive | bad | 3 / 2 |
| `9807b128f7e6` | @42ailab/42cc 0.2.1 | good | 0 / 0 |
| `a8626b9447fe` | FinSpy archive | bad | 2 / 1 |
| `cfbbff36c54b` | Scrutiny 10.4.6 with TNT crack | purgatory | 0 / 1 |
| `e2d47de87af7` | Mac Cleaner | purgatory | 0 / 0 |
| `edf1bf727527` | August Installer DMG | bad | 22 / 23 |
| `f5ef49d6e0df` | August Setup DMG | bad | 22 / 23 |

Counts are current cleave root findings, including propagated child evidence; they are not independent-behavior counts. FinSpy retains two hostile findings rather than padding its score with a filename-based family conviction. Cleaner findings do not prove hostile behavior; purgatory preserves the unresolved unwanted-software/consent judgment.

## Changes

- Recovered x86-64 subtract/XOR integer tables, including permutation-indexed tables, followed by hex and file-derived custom Base64 alphabets. Bounds, section-backed operands, valid permutation indices, alphabet uniqueness and text validity are checked. Both preferred and supplementary universal-binary slices are inspected. Only complete quoted AppleScript invocations are analyzed as scripts, including backgrounded commands. No sample instructions are executed.
- Added bindings for Python login-keychain/SSH copies with a curl upload, and for allocator-log cron injection settings passed to rsh. Added a precise ZuRu dylib fingerprint, the native CR0 write-protection-clear operation, the Mach-O kernel-bundle property and the TNT/Paddle crack constant tuple.
- Relocated generic executable/bundle names, encrypted single-member archive layout, and equality-chain text shape to neutral properties/capabilities. Installer.app and 42cc updater filenames no longer imply malware-family or trojanized-app identity. Existing consuming references were updated.
- Added compressed sequential/permuted universal Mach-O regression samples; member hashes are in `native-fixtures.json`. The engine patch is saved alongside this report for review.

## Verification

- Three Rust recovery tests passed: custom-alphabet/invalid inputs, sequential tables/malformed operands/truncation/background wrappers, and permuted tables/invalid indices.
- Ten Python mutation controls passed their intended-rule checks, covering comments, unrelated copy sources, print-only paths, missing upload execution, mismatched environments, harmless log paths and harmless directory values. Results are in `control-results.json`.
- `RAYON_NUM_THREADS=1 make validate` passed: hostile 2804/2804, suspicious 1753/1753, notable 8457/8457, baseline 1320/1320. No validator thresholds or exceptions were changed. The single-worker run avoids timing contention seen during simultaneous scans.
- Every recovered outer sample was rescanned using the rebuilt sibling cleave binary and the working trait bundle. Full per-file reports remain under `/tmp/dmg-edge-review/<case>/scan-current-engine.json`.
- The installed atomscan binary links an older cleave library. A fresh local atomscan run picks up YAML changes but cannot use the new native decoder until atomscan is rebuilt against this cleave change; adjusting PATH does not replace a linked library. Its small-DMG H=0 results were not accepted as verdicts. The current cleave counts above verify the engine fix directly.

## Individual evidence

### July Setup DMG A — `39a860e5336e`

Sequential integer subtract/XOR tables conceal VM checks and an AppleScript credential stealer. Recovered code impersonates System Preferences, authenticates the password with dscl, copies browser/keychain/wallet stores, uploads an archive, and installs a downloaded component. Exfiltration gate 45.94.47.186; secondary host halesmp.com.

### July Setup DMG B — `581d825f60e3`

Independently decoded sequential integer tables with a different custom alphabet and distinct Mach-O/payload hashes. Same password-phishing, sensitive-store collection, HTTP archive upload and launch-daemon chain; gate 45.94.47.186.

### OneSafe Mac Cleaner — `5f2f261e664b`

OneSafe Mac Cleaner is a verified Avanquest-signed commercial cleanup application with privileged helpers, licensing and scheduled-reminder resources. Collector-applied 7zAES encryption is not evasion. Static inspection did not establish credential theft, a hidden remote-execution chain or another hostile objective. The monetized cleaner/reminder behavior and incomplete consent/runtime assessment make it unsuitable for a confident good training label.

### ZuRu archive — `8426b7aa2182`

Archive reviewed component by component. g.py copies the user SSH directory and login keychain into staging, archives it, uploads with curl and deletes staging/self. iTerm loads an injected libcrypto.2.dylib with HTTP and shell capabilities. UltraEdit variant loads a networked libConfigurer64.dylib that fetches log-named payloads and stages /Users/Shared/.fseventsd. The unrelated HTML syntax wordlist is neutral and must not be a parser-DoS finding.

### @42ailab/42cc 0.2.1 — `9807b128f7e6`

Reviewed manifest, install.js, CLI wrapper, README, Mach-O and bundled PE. The documented model-configuration installer copies its included application, prompts for administrator permission when needed, creates an ordinary shortcut and opens the application. Native UI/provider/config/updater strings agree with that purpose. The macOS binary has a verified Developer ID signature and verified code pages; the PE identifies the same product/version and uses its documented vendor update endpoint. A 42cc_update.sh filename alone was the misleading trojanized-app finding; no hidden collector or hostile bootstrap was found.

### FinSpy archive — `a8626b9447fe`

helper2 binds allocator-log output to /etc/crontab and embeds a root cron command appending an unrestricted NOPASSWD sudoers rule, then passes that exact environment dictionary to /usr/bin/rsh. helper3 performs privileged setuid/shell operations. logind.kext contains CR0 write-protection disabling and process-list unlinking code (statically disassembled). Two independent hostile detections plus the kernel write-protection signal are retained; no third hostile label was manufactured from generic APIs or debug filenames.

### Scrutiny 10.4.6 with TNT crack — `cfbbff36c54b`

Scrutiny is a modified commercial app with a TNT/Paddle license-crack dylib. The dylib contains the adjacent PaddleAPICheck / paddle / TNT attribution constants, fake license fields, and native memory-patching APIs. It differs from the networked ZuRu dylib despite sharing libConfigurer64.dylib as a filename. License tampering is suspicious; no credential theft or independent hostile download/execute chain was established.

### Mac Cleaner — `e2d47de87af7`

Mac Cleaner is a verified Avanquest/PCHelpSoft-signed commercial cleaner with privileged helper and reminder resources. Its native entitlements relax several runtime protections, but that does not establish malicious intent. Archive encryption does not convict the payload. No concrete hostile chain was established; retain uncertainty about unwanted behavior and user consent in purgatory.

### August Installer DMG — `edf1bf727527`

Permuted integer-table layout, independently decoded. Conceals a VM-check command and the stealer/remote-install script; gate 45.94.47.143 and halesmp.com. The permutation is checked as a bijection before recovery.

### August Setup DMG — `f5ef49d6e0df`

Independently decoded permuted tables and custom alphabet; distinct binary and payload from edf1. Same password phishing, credential-store copying, archive upload and downloaded component persistence; gate 45.94.47.143.

## Hopper application

Applied all ten verdicts after full validation, using `triage/dmg-edge-review-2026-10-28` as the request source. OneSafe Mac Cleaner moved from good to purgatory. The other nine entries already had the reviewed labels, so Hopper returned no-ops. All three calls succeeded with zero absent or failed entries. Final pools: six bad, one good, three purgatory. A hash-verified recovered copy of the benign 42cc archive is staged at `/tmp/triage/misplaced-good/9807b128f7e6d2fdb08bfe28a92ef63dca5cffeefd77eba3ad8fc594eb6ce5f3.zip`.
