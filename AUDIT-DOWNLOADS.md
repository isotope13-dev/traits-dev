# Downloads sample audit — final static assessment

Scope: the original 26 artifacts recorded in `/tmp/triage/reverse-review/inventory.json`, identified by SHA-256. Later Downloads arrivals are excluded. Originals were hash-verified before rescanning. No sample, interpreter payload, install hook, or remote command handler was executed; embedded endpoints were not contacted.

This is a concluded **static assessment of the available artifacts**, not a claim that every sample has been fully reverse engineered or proven benign. Full reverse engineering remains incomplete for the opaque/native paths and missing stages listed below. Low scanner severity is not a safety certificate. No samples were relocated or committed by this audit.

## Dispositions

“Hostile behavior” describes demonstrated code behavior, not an attribution of the publisher's intent. “Conditional” means a stated entry point or configuration is required. Remote-service authorization and absent downloaded payloads cannot be established from these archives.

| # | Artifact | Disposition and decisive evidence |
|---|---|---|
| 01 | logtrace 1.0.1 | Suspicious concealed downloader/execution path. `Logger.trace` triggers remote ZIP staging and platform execution; Windows also feeds a downloaded script to Python. Not an import/build trigger. Final stages absent. |
| 02 | Spellbook | Dual-use offensive framework. Reverse_Shell.pm generates strings; an operator-invoked exploit module separately sends an exploit request. Do not label the string generator an executing reverse shell. |
| 03 | VPNSec 1.0.2 | Privacy-sensitive VPN with confirmed flaws; malicious operation not established. Proxy credentials lack challenger scoping, login trusts a title substring, retry field is inconsistent, logout cookie domain is malformed. Vendor/service behavior is not certified. |
| 04 | ARVE 10.8.7 | Hostile authentication backdoor. Hardcoded-token/HMAC route logs a requester in as an existing administrator and reports site/user information. Included by the plugin entry point. |
| 05 | bfunky-http-parser | Hostile secret/profile collection behavior in included PHP. Uploads full environment and host/server/cwd data with TLS verification disabled. Response execution was not found. |
| 06 | gp247 front 2.0.3 | Hostile conditional sabotage in bundled SweetAlert2: pointer-event disabling and repeated remote audio under locale/domain/time gates. |
| 07 | Bufferzone go-stdlib-ext | Import-time sensitive collection and attempted persistence/CI modification. Default collector is localhost and one SSH key is a placeholder; do not claim successful remote compromise or working key installation. |
| 08 | telegram_helper | Hostile bot-controlled session/tdata/cookie collection and upload without sender authorization. Main-guard activation, not ordinary import. Telegram client APIs alone remain notable. |
| 09 | ordercli | Hostile Lua loader bundle. Recovered task-controlled staging, native export execution, scheduled tasks, Defender exclusion, screenshots and server routing. Native-host equivalence and downloaded stages unresolved. |
| 10 | wiki | Hostile related Lua loader bundle with separately recovered constants/configuration. Do not treat the two archives or all native hosts as byte-identical. Same opaque-stage limits. |
| 11 | gp247 front 2.0.1 | Same confirmed conditional SweetAlert2 sabotage category as 06. |
| 12 | Extension Chord XPI | Browser game-mod/replay bridge with conditional desktop risks; planted malware not established. Firefox loads packaged tools. Node update/file brokers are not working Firefox filesystem capabilities. Desktop save cancellation falls through to a write; update filenames lack confinement. Desktop runtime absent. |
| 13 | Bufferzone grpc-client | Import-time sensitive collection plus CI wrapper/Git-hook modification. Default collector localhost; CA replacement is commented out and must not be reported as executed. |
| 14 | Onecode | Suspicious installation trust boundary: remote tar download from a bare IP with TLS checks disabled, extraction/chmod/linking. Binary executes later on CLI invocation, not simply because installation completed. Binary absent. |
| 15 | Bufferzone net-helper | Import-time sensitive collection and CI/Git-hook writes. Empty PATH directory alone does not install a command wrapper. Same localhost/default-configuration caveat. |
| 16 | width-table | Hostile build/startup file-upload behavior. Statically recovered XOR command selects the first immediate four-character filename and uploads it; both build.rs and Linux init-array activation are present. |
| 17 | toml_editor | Build-time host/user/cwd disclosure with HTTP and DNS fallback. Research labeling does not remove the automatic disclosure. |
| 18 | rubydex | Build-time profile disclosure over plaintext HTTP/TCP. Port 8443 does not establish TLS. |
| 19 | replit_ruspty | Build-time profile disclosure with HTTP/DNS fallback, as in 17. |
| 20 | lsh | Build-time host/user/public-IP profiling sent to a hardcoded Telegram destination. |
| 21 | LeazyCMS | Suspicious protected registration/telemetry and a separate template-editor access-control concern. Literal decoder wrappers are not request-to-eval webshells. SafeViewEngine stores signatures as data. Editor request writes/evaluation are real; packaged role checks do not establish effective authorization. Deployment exploitability unverified. |
| 22 | YroDevGit | Hostile SweetAlert2 sabotage. Separately decoded secure.js handles local/same-origin data without an identified exfiltration sink. command.php is CLI-gated, not HTTP-accessible through that entry. |
| 23 | Whalent core | Sensitive dual-use remote management. Authenticated gateway commands can read/return provider credentials; no extra local per-command approval was found. Server authorization and malicious use are not established. |
| 24 | Lizhipay 3.5.5 | Suspicious commercial-protector mechanics and security concerns; no established webshell. All 14 inner bodies recovered. Traced licensing/HWID/hooks/config/cache, disabled licensing TLS verification, and decrypt-then-unserialize. Catch handler rethrows. Attacker control of deserialization input/key not established. |
| 25 | Whalent agent | Same byte-identical core/sidecar as 23, plus CLI bootstrap and supervisor/update logic. Launcher is not an autostart installer. Same remote credential-management concern. |
| 26 | Lizhipay 3.5.8 | Opaque protected loader; disposition remains unresolved beyond observed mechanics. Outer self-hash/XOR/inflate and five VM blobs decoded. AES-GCM bodies require unavailable boot/server keys. New key-fetch helpers verify TLS; do not inherit the older routine's TLS finding. |

## Detection repairs and regression coverage

- Four misleading upstream PHP signatures are disabled with documented native replacements: Encoded/Big, Gzinflated, Generic/Callback and Function/Via/Get. Native findings distinguish content encoding, execution calls, callback-capable APIs, and actual request-selected calls. Quoted examples do not become executable behavior.
- Decoder coverage includes pack, base64, inflate/uncompress/gzip, mixed case and PHP closing-tag concatenation. Encoded-content findings use available native metrics; they do **not** reproduce upstream raw-tail entropy/mean/deviation thresholds after UTF-8 normalization.
- Webshell vocabulary is component evidence, not an independent suspicious verdict. Actual self-label/execution composites remain separate.
- Ordinary PHP process-title changes are notable; actual kernel-worker impersonation has a separate masquerading trait. Detached networking plus a process title no longer asserts a RAT.
- Added DOM-event JSON/extension-message observations and the earlier VPN authentication/tab-title/OAuth observations. These report mechanisms, not proven unrestricted data flow.
- The PHP regression harness has 73 positive/negative cases, including request-selected callbacks versus a fixed callback processing request data. Routine collection transforms and lifecycle cleanup remain baseline observations. Focused tests also distinguish Chord's real bridge from quoted event-detail syntax. The final original-artifact scan includes all 26 hash-verified inputs. Validation evidence and current counts are recorded in the companion work log; no expectation caps were raised to accommodate these changes.

## Limits that prevent a full-reverse-engineering completion claim

1. **Missing artifacts:** Onecode/logtrace and Lua downloaded stages, Chord's desktop runtime/preload bytecode, and Lizhipay 3.5.8 boot/license-key material are absent. The decoded cache location `runtime/plugin/.acgcache` is not supplied, including hidden-file checks. No private AES key can be inferred from the public signature-verification key.
2. **Native/VM coverage:** rizin traced native interpreter entry/argument/script-loading roles, but did not establish complete trusted-build equivalence. Older Lizhipay opcode bodies and the sole registered exception handler were inspected; dynamic aliases/guard feasibility do not have a formal all-path proof. These limitations preclude certifying those binaries/protectors clean.
3. **Raw detection gap:** recovered Lua PRNG strings and Whalent RC4-decoded credential commands are analysis derivatives. Current native traits do not integrate those decoders into raw scans. A derivative match is not original-byte coverage. Closing this requires scanner-side decoder integration and raw-positive/benign-negative regression tests, not sample hashes or misleading plaintext rules.
4. **External authorization:** deployed LeazyCMS roles, Whalent server account authorization, VPN service behavior and current remote payloads were not observed. Source-level capability is not proof of unauthorized use or deployment exploitability.

Do not resolve these limits by calling the samples benign. The available evidence supports the dispositions above; it does not meet the stronger request to fully reverse engineer every opaque component.

## Evidence

Final strict validation passed with no exclusions: hostile 41/41, benign 13/13, does-nothing 174/174, drop-exec 43/43, impact-wipe 66/66, obfuscation 80/80, reverse-shell 25/25, simple-stealer 65/65. These tests validate trait behavior, not complete sample reverse engineering.

- Detailed call paths, decoder parameters and corrections: `/tmp/triage/reverse-review/REVIEW.md`.
- Original paths/member inventory/SHA-256: `/tmp/triage/reverse-review/inventory.json`.
- Machine-readable dispositions and finding IDs: `/tmp/triage/reverse-review/FINAL-RESULTS.json`.
- Original scan records: `/tmp/triage-original-deep-rescan.jsonl`.
- PHP regression harness: `scripts/check-php-native-replacements.cjs`; latest results `/tmp/triage/audit-closure-regressions.log`.
- Current strict validation run: `/tmp/triage/audit-closure-validation.log`.
- Native source/bytecode derivatives and static-only decoder scripts remain under `/tmp/triage`; none are replacement executable samples. These temporary artifacts should be retained if the audit needs to be reproduced later.
