# Three stranded members: independent static review

The supplied archive convictions are preserved. Each listed member was hashed,
scanned, inspected through `cleave facts`, and judged from its own execution
paths. No specimen, shell command from a specimen, or remote payload was run.

## Member judgments

* **Installer — MALICIOUS.** Its universal Mach-O contains equivalent x86-64
  and ARM64 state-XOR wrappers. ARM64 entry calls the decoding constructor,
  obtains the string buffer, and passes it to `system()`. Independently applying
  the recovered seed `0x11667`, multiplier `0x3785`, 32-bit multiplication and
  modulus 35999 reconstructs the 37,077-byte command, including its terminator;
  it agrees exactly with Cleave's decoded text. The command runs an AppleScript
  which caches or requests the login password, validates it with `dscl .
  authonly`, copies browser login/cookie/extension stores, wallet directories,
  Keychain databases, Notes and selected personal files into a temporary tree,
  compresses that tree with `ditto`, and posts `/tmp/out.zip` to an HTTP endpoint.
  It removes the temporary tree/archive, replaces Ledger Live with downloaded
  content, and uses the captured password to install and bootstrap a
  LaunchDaemon. The daemon's shell command is fetched remotely; a `nohup`
  fallback is also present. Successful authorization, upload, replacement and
  persistence are not established. The exfiltration retry's recursive call omits
  an argument, so ten successful retries must not be inferred. These linked
  theft and persistence behaviors establish malicious intent independently of
  the Archicad installer packaging. All seven existing hostile findings and
  seven suspicious findings remain accurate and retained.
* **perl_cmd.pl — MALICIOUS.** This is DK's simple CGI backdoor shipped as a
  DAVTest payload. It reads `QUERY_STRING`, substitutes `%20` and `%3b`, runs the
  same scalar through backticks, captures stdout into an array, and prints those
  lines in the HTTP response. The file implements no authentication or command
  allowlist. The `/etc/passwd` string is a usage example, not a fixed file-theft
  operation. DAVTest's `-sendbd` path explicitly uploads these backdoors, which
  corroborates its operational payload role. Kali/DAVTest provenance supports
  authorized testing, but does not turn this member's unrestricted remote
  command surface into an inert fixture. That purpose and executable channel
  tip the individual judgment. Deployment, upstream server access controls and
  operator authorization are unknown; no unauthorized deployment is asserted.
* **process.py — BENIGN.** This Android assessment utility requires an explicit
  package argument, checks Frida connectivity, enumerates app components through
  Objection, disables root checks and TLS pinning, queries debug state through
  ADB, searches memory for secret-like strings, lists Keystore entries, and
  writes a user-selected local JSON report. Memory matches are counted; up to
  2,000 characters of Keystore output are retained. Its optional Frida
  inline-script helper is defined but not called by `main`. Subprocesses use
  argument vectors; ADB intentionally invokes the device shell. The target
  selection, visible assessment workflow and local output support the benign
  judgment. No victim authorization was supplied; none is invented. These
  sensitive operations remain useful dual-use detections. Forager fetched all
  PyPI wheels for `ai-forge-cli@2.1.6`; the recovered wheel has the exact supplied
  SHA-256, corroborating identity without establishing the whole archive's
  intent or revisiting its conviction.

## Rule changes and retained coverage

* Relocated the unchanged Python Frida word matcher from software identity to
  `micro-behaviors/process/debug/tool-markers::python-frida-reference`, retaining
  its scope, notable severity, confidence and corpus exclusion. A mention in
  source or a comment does not identify the containing program as Frida.
  Updated its exact anti-analysis consumer. Inspected exact and ancestor
  consumers: native identity exclusions retain their identities; Python
  consumers must no longer treat a Frida mention as a blanket suppressor.
  An out-of-batch control confirms that inline-hook terminology now remains
  visible alongside that mention. The anti-analysis positive retains its
  hostile finding. No attack matcher or severity was weakened.
* Added a notable Objection Android component-list command observation, excluding
  Python docstrings and requiring the complete command.
* Added a notable argument-provenance observation for a Frida literal reaching
  a Python subprocess argv. It does not claim the literal occupies the
  executable position, nor that inline evaluation, hooking or bypass succeeds.
  An unrelated literal and an argv reassignment do not match.

Every analysis unit in the three archives was compared before/after. The wheel
has ten changed units including its root; the changes are the reference move
and new notable observations. Neither other archive changes. Full per-unit
deltas, counts, hashes, model probabilities and marker notes are in
`review.json`. Raw scans, facts, disassembly, independently decoded source,
Forager provenance and original-rule snapshot remain in the task scratch
directory `stranded-current`.

## Counts and classifier comparison

H/S counts are distinct hostile/suspicious IDs, including inherited member
findings. The classifier's calibrated alert level is 0 for the two malicious
members and -1 (no alert) for the benign member, before and after.

| Artifact | H before → after | S before → after | Alert level before → after |
| --- | ---: | ---: | ---: |
| Installer member | 7 → 7 | 7 → 7 | 0 → 0 |
| Perl CGI member | 2 → 2 | 1 → 1 | 0 → 0 |
| Android member | 0 → 0 | 1 → 1 | -1 → -1 |
| Installer archive | 7 → 7 | 8 → 8 | 0 → 0 |
| DAVTest archive | 19 → 19 | 7 → 7 | 0 → 0 |
| ai-forge wheel | 3 → 3 | 35 → 35 | 25 → 25 |

There are no material attack-detection losses or remaining member/classifier
disagreements. The Android root-check bypass remains suspicious; its benign
verdict does not justify demotion. The Perl member has two overlapping hostile
rules for its single command channel and result response. Query decoding,
shell execution and captured output also have accurate notable coverage.
There is no distinct additional staging, evasion, persistence or theft action
to support a third hostile trait. No duplicate was added to reach the goal.

Initial scans followed external references, and cached universal-binary scans
varied architecture selection and neutral findings. Final comparisons use
`--follow=none` against original HEAD and working rules; uncached native
comparisons have identical finding sets and probabilities. The supplied hashes
remain unchanged. The installed model reports feature specification 18 while
the engine expects 21; that model limitation is independent of this rule work.

## Verification

`python3 testdata/stranded-three-member-review/check.py` passes 25 assertions
across eight static positive/negative cases. The existing native-dialog suite
passes its positive, three near misses and the original Installer. The existing
source-behavior suite passes 13 cases, including partial URL decoding, cookie
copies, phishing and cleanup boundaries.

The older Android suite passes its first six cases but has a pre-existing
failure: its generic `frida-relay.py` expects
`frida-attestation-relay-controller`. Original HEAD also does not emit that
finding. The fixture posts a generic challenge response without the stronger
attestation evidence now required by the rule. Its USB lookup and script-post
observations remain. This unrelated expectation was not changed to mask the
failure.

The three marker lines, also prepared verbatim in the commit body, are:

```text
Installer stealer: phishes, steals, uploads and persists
DAVTest Perl CGI: unauthenticated query-to-shell backdoor
Android analyzer: explicit target, local report; retain bypasses
```
