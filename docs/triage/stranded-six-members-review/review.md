# Six stranded members, 2026-10-27

All six listed members are **MALICIOUS**, independently of their already-confirmed
archive labels. SHA-256 values were checked against the task. No sample was
executed. Analysis used complete `cleave facts`, local slow-mode `atomscan`, raw
source, archive contents, and Rizin disassembly of both Mach-O slices.

## Behavior and execution limits

- **Installer (8202c388…)** is a universal C++ macOS credential and file stealer.
  ARM64 main at `0x100000690` builds a string and calls `system` at
  `0x1000006b8`; x86-64 main at `0x100000630` calls `system` at
  `0x10000065c`. Both decode the same 37,077-byte command, including its NUL,
  with seed `0x11667`, byte XOR, and the recurrence
  `state = ((state * 14213) & 0xffffffff) % 35999`. The modulus derives from
  the embedded build time `09:59:59`. Independent recovery matches the facts
  output, byte for byte. The decoded command's SHA-256, including NUL, is
  `d5f34825a22b62491186eaa28065b6f539046d333a56199b996526173be22428`.
  It executes an AppleScript assembled with `run script` and return-joined lines.
  The main handler validates a cached password with `dscl . authonly`, otherwise
  loops on a masked Installation password dialog, saves the result, and stages
  it with host information and targeted stores. Read/copy helpers feed Chromium
  cookies, login databases and extension stores; Gecko logins/key4/cookies;
  Safari cookies; login Keychain; desktop wallets; Notes databases, attachments
  and a fallback Notes export; and extension-filtered Desktop/Documents files.
  `ditto` packages the staging directory, and `curl --data-binary @...` sends
  the ZIP with campaign headers. It removes staging and the ZIP, downloads a
  Ledger Live replacement after killing/removing the installed application,
  fetches shell text for a KeepAlive/RunAtLoad LaunchDaemon, installs/bootstrap
  it through password-fed sudo, and falls back to interpolated `nohup`.
  Theft, credential phishing/replay, trusted-app replacement and persistence
  distinguish this from a legitimate installer. The outer postinstall's
  Gatekeeper/quarantine changes are **not** attributed to this member. Remote
  replacement/daemon payloads were not fetched, and their further effects and
  successful compromise are unknown. The upload retry omits its fourth handler
  argument; this defect does not remove the initial upload attempt.
- **parser-session writer.js (419285d3…)** copies all `process.env` and collects
  OS, hostname, username, and non-internal IPv4 interface MAC addresses.
  Its byte-pair decoder resolves the table to `require`, `axios`, `post`, an
  HTTPS endpoint, `headers`, an X-prefixed header, its value, and `then`.
  The exported arrow calls Axios POST with that collected object and evaluates
  `response.data`; a final empty catch discards failures. The ignored function
  arguments, concealed network/evaluation chain, and whole-environment export
  do not serve the advertised logging/session middleware. The retained module
  requires `../package.json`, which resolves to absent `src/package.json`.
  The archive's entrypoint instead names an absent `.pnpm/httpreslog` module,
  and its declared postinstall script is absent. Thus the supplied package
  layout does not establish successful activation of this local writer.
  An original-release recovery was attempted with
  `forager fetch ... pkg:npm/parser-session@1.1.9`; registry/mirrors/Wayback,
  CDN reconstruction and Software Heritage did not recover the release, and
  the final Socket browser fallback was unavailable. No reconstructed archive
  or missing code is being treated as original evidence. The retained member
  itself contains the complete export-and-eval attack when its import context
  is satisfied; that is enough for a malicious verdict despite packaging defects.
- **osinthell v.js (2e5535f9…)** exports a zero-argument action invoking
  `del /F /S /Q` against the System32 DLL wildcard, hiding child streams and
  swallowing exceptions. It is destructive OS sabotage, not an OSINT operation.
- **osinthell f.js (190bbe0e…)** opens `\\.\PhysicalDrive0` read/write, allocates
  a zero-filled 512-byte buffer, writes it at disk offset zero, then closes the
  handle. A separately caught `bootrec /fixmbr` cannot restore the original
  partition table or removed sector contents. The hardcoded destructive write
  with no backup, input, or consent distinguishes this from disk maintenance.
- **osinthell p.js (d6f33722…)** enumerates C:, D:, E: and F: roots, joins each
  entry to the selected drive, checks for regular files, and writes an empty
  string with default truncating mode. It is a root-file destroyer, not a
  recursive secure wipe. Nested catches make the destruction error tolerant.
- **osinthell t.js (28db8a38…)** synchronously disables normal boot-failure
  handling and recovery using two `bcdedit /set {default}` calls. A repair tool
  could temporarily use these options, but this silent parameterless export
  has no restoration or repair path and is bundled behind a purported OSINT
  lookup that calls destructive helpers. That combination tips the verdict.

Each osinthell member merely imports APIs until its exported function is called.
The package's `sorgu` caller invokes f before an earlier module's infinite loop;
p, t and v appear after that loop and are not reachable through its ordinary
sequential path. Each remains an independently callable destructive payload.
Windows privileges/file locks may stop individual operations. No infection or
successful destructive effect is inferred from source alone. The other bundled
helpers supply caller context, not additional capabilities attributed to these
four members.

## Rule change and controls

Extended the canonical
`micro-behaviors/communications/http/post::axios-post-call` with a
structurally bound decoded-Axios POST alternative. Ordinary Axios member
references, including string subscripts, are retained through parsed member
patterns. Scope, severity, and confidence are unchanged. The
new path requires the actual byte-pair decoder, decoded Axios/POST slots,
matching table/decoder identities, and the computed require/method call.
It permits renamed helpers and arbitrary endpoints, payloads and callbacks.
It does not infer credential theft, execution of the response, or import-time
network activity. The description now says "member or decoded call": a bare
`const sender = axios.post` is a reference, not proof of an HTTP request. The
existing generic POST rule is unchanged. No new hostile trait, identity, exclusion or duplicate rule
was added; the POST leaf remains at 100 rules.

Reviewed exact consumers and parent HTTP selectors: their evidence remains
an Axios POST reference or operation. No supported detection was removed or
reduced in criticality. In
particular all existing hostile and suspicious detections must remain at the
same severity in standalone and archive scans.

Focused controls pass for the original and renamed writer plus an ordinary
status-telemetry POST without environment collection or eval. Near misses
reject GET, an unused table/direct require, a different module, wrong method
index, wrong decoder, decimal rather than hex conversion, and an unrelated
method table. The status GET is also rejected. The committed telemetry fixtures
have no hostile/suspicious findings and show that the added operation is notable.
Regression comparison covers 45 cases, including 21 pre-existing JavaScript/
TypeScript fixtures outside this batch: all 28 old positive detections remain.
It also checks ordinary calls, unused members, string subscripts, optional
chaining, quoted code, comments, and unrelated receivers. Additional boundary
controls cover template subscripts and escaped character spellings, retaining
their normalized member meaning without matching a different method. The generic POST
rule remains unchanged; its existing SSH uploader control still matches.

## Coverage limits

Installer and writer already exceed the 3–5-hostile goal across distinct
behaviors. The four tiny Windows members have one attack result each: DLL
removal, boot-sector corruption, root-file truncation, and boot-recovery
sabotage. Existing atoms/composites were inspected for their full command,
path/handle, data and error-handling relationships. p has two accurate hostile
rules describing the same destruction. No further distinct hostile behavior
was found in those bytes: `bootrec` is separately covered as a notable repair
command, and hidden stdio/empty catches alone do not establish additional
hostile objectives. Reaching three hostile rules per member would duplicate or
inflate supported behavior. There is no uncovered attack action being excused
by the count shortfall.

Full raw evidence and control outputs are in the task scratch directory
`stranded-audit`; original-release recovery attempts stayed there. Verdict
markers are beside all six extracted members and the three supplied archives;
archive markers retain their confirmed verdicts.

## Scan comparison

Counts are hostile/suspicious. Archive rows use the rolled-up parent findings.

| Artifact | Before H/S | After H/S | Classifier FP level |
|---|---:|---:|---:|
| installer | 20/12 | 20/12 | 0 → 0 |
| writer | 8/6 | 8/6 | 1 → 1 |
| v | 1/3 | 1/3 | -1 → -1 |
| f | 1/1 | 1/1 | -1 → -1 |
| p | 2/1 | 2/1 | -1 → -1 |
| t | 1/3 | 1/3 | -1 → -1 |
| archive-bb | 20/13 | 20/13 | 0 → 0 |
| archive-parser | 8/6 | 8/6 | 0 → 0 |
| archive-osint | 5/10 | 5/10 | 25 → 25 |

Classifier level -1 means the calibrated models did not flag the artifact; the four standalone Windows helpers remain misses. Installer and writer are flagged before and after, as are the archive-level results. The osinthell parent is flagged via its existing registry/known-malicious evidence while these four members remain individually unflagged. The model reports v18 features with a v21 feature expectation; this is a reported engine/model limitation, not a reason to add duplicate traits.

All controlled before/after file comparisons retain every finding at its existing criticality. Only writer and its archive parent gain the canonical notable HTTP POST finding (48 → 49 notable traits on writer). The first native scan used a different reference-following setting and exposed 29 additional low-severity IDs; rerunning the original YAML in a scratch snapshot with the final explicit `--follow=none` settings reproduces the final native result exactly. Direct `cleave test-rules` also confirms the x86-64 XOR primitive, HTTP response acquisition, and stdin-fed sudo observations still match. No supported YAML detection was removed or weakened; no hostile or suspicious coverage was lost. Full per-file counts, added IDs, and the initial pipeline-only IDs are recorded in `scan-diff.json`.
