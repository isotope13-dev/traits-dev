Review date: 2026-10-24. All three artifacts were examined without executing
their code. `atomscan --no-update --mode slow --analyze local --format json`
and `cleave facts` ran before editing and atomscan ran again afterwards.
Evidence is in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/triage-bad`:
original facts, before/after scans, token-resolved IL, managed call records,
extracted resources and CRC checks, publisher downloads and `.forage.json`
provenance, control results, native dependency disassembly and comparisons.

`96082e1bb5350495.bin` is the Ultimate Metin2 / Ultimate Gems Cloud Windows
Forms launcher, SHA256
`96082e1bb5350495ce83fe6ad1c26cfde4c31171c0f200bc68585d2d08f3d9ef`.
Judgment: **BENIGN**, as an artifact assessment routed to sighted quarantine.

Independently parsed all 301 MethodDefs using dnfile/dncil and resolved their
tokens and user-string operands. The resulting IL agrees with the existing
ILSpy decompilation in `scratch/triage/launcher.cs`. Main opens the visible
launcher unless explicit self-test, preview, apply or recovery arguments select
another mode. CheckUpdate calls UpdateCore.Prepare, copies its own executable
to a helper and starts it with an apply-plan path and parent PID. The helper
waits for the parent, locks the update directory, installs staged files and
retains backups for rollback. PlayGame starts the local `executor.exe` after
preflight checks. Browser launches are limited to approved HTTPS links.

Prepare reads the external `gems_update.json`, requires an enabled HTTPS
channel, downloads an index and manifest, validates manifest/file SHA256 and
lengths, checks space and the running game, and stages permitted runtime files.
Local rejects traversal, reserved DOS names and reparse points. RuntimePath
rejects account/password/credential files and user-data directories. These
strings describe preservation boundaries; COM1..COM9 are rejected DOS devices.
Registry reads/writes store Language and Motion below the launcher's HKCU key,
without an autorun registration. AppDomain supplies BaseDirectory; there is no
Assembly.Load payload path. HTTP redirect setters pass false. Their presence
does not support a redirect-following or TLS-bypass claim.

All twelve resources were independently extracted: nine PNGs and three JSON
catalogs. Every PNG chunk CRC verifies, every image ends at IEND, and none has
trailing bytes. Compressed artwork accounts for the enormous high-entropy
managed resource/.text region; C2PA image metadata is not an executable stage.
The JSON describes game quests/events/calendar data and is consumed through
bounded schema validation. No hidden script or decoded executable was found.
Facts expose no archive-member tree or automatically decoded obfuscation stage.

Fresh forager downloads retrieved the publisher's update index, its referenced
manifest, the launcher, the content catalog and the game homepage. The index's
SHA256 verifies the manifest. The manifest names this exact sample hash; the
new launcher download independently reproduces every original byte. The current
calendar endpoint returns HTTP 404. The homepage identifies the Metin2 server;
the catalog contains 100 quests and seven events. These are corroboration of
purpose, not a guarantee that a publisher or future update is trustworthy.

Previously fetched executor, GeoAudio helper, endpoint INI and update-channel
configuration were checked against the newly fetched manifest and all hashes
agree. GeoAudio's decompiled request sends an ephemeral session ID, version and
client label to a certificate-pinned HTTPS endpoint; it accepts bounded location
JSON and writes localization cache data, without evaluating response code.
Additional native executor disassembly confirms that ReadProcessMemory at
0x46838c uses GetCurrentProcess, OpenProcess at 0x468dcb requests query access
while enumerating processes, and WinExec at 0x577a35 starts `errorlog.exe`
after diagnostic module enumeration. These sidecar observations are not launcher
capabilities, nor a certification of every native game-client path.

The coherent game/update paths, defensive file validation and independently
verified publisher bytes tip the judgment toward benign. osslsigncode confirms
there is no signature. Blank metadata, version 0.0.0.0, large compressed resources
and self-copy/helper execution plausibly explain the generic ML detections and
collection. Historical installation context, actual sidecar settings, user
authorization and the source's exact collection reason remain unavailable.

`Main.plg`, SHA256
`b020aca9f38ddaf639e160490ccf48101848b5189e9092c4a3b12af8ef87ec40`,
is a Visual C++ HTML build log. Judgment: **BENIGN**.

The entire 1,972-byte document consists of headings and a preformatted build
record. It records cl.exe/link.exe response-file commands for a `w32.ogw0rm`
project with messaging-client and Peer2Peer source/object names, ending in a
successful Main.exe link. HTML rendering does not execute those recorded command
lines. There are no scripts, navigation targets, external dependencies or hidden
stages to follow. Its worm-project provenance readily explains malware-corpus
collection, but it does not turn this log into the worm executable. The existing
build-log observation is accurate and remains unchanged.

`sysinfo.rc`, SHA256
`7ff7a4c02c2f836c923ccc21939e0eb93cddb0c82c8f21814e770795cc4e0b3d`,
is a 39-byte Meterpreter resource batch. Judgment: **BENIGN**, retaining its
accurate suspicious reconnaissance finding.

Its complete command sequence is sysinfo, getuid, getlwd, netstat -atnp, ls.
There is no decoder, conditional branch, payload, exploit, credential extraction,
persistence or file modification. In a Meterpreter session, the first two query
host details and the session principal; getlwd prints the operator's LOCAL
working directory, not the victim's directory. netstat requests the target's
connection table and ls lists remote directory entries. The commands require an
existing session; this file neither supplies an endpoint nor creates a session.
Successful execution on an actual target was not observed. Metasploit's own
[session documentation](https://docs.rapid7.com/metasploit/manage-meterpreter-and-shell-sessions/),
[local-directory implementation](https://docs.metasploit.com/api/Msf/Ui/Console/LocalFileSystem.html)
and [network command implementation](https://docs.metasploit.com/api/Rex/Post/Meterpreter/Ui/Console/CommandDispatcher/Stdapi/Net.html)
support these distinctions. Meterpreter processes netstat internally; the Unix
looking options do not establish that this batch launches a native shell.

The minimal inventory-only behavior favors a benign dual-use resource over a
malicious payload. Offensive-tool affiliation and malware-corpus provenance
justify investigating its deployment, and explain collection; authorization and
session provenance are missing. A benign disposition does not suppress or reduce
the existing suspicious Meterpreter command-batch detection.

Four new notable traits record complete sysinfo/getuid/getlwd command lines
and the managed HTTP automatic-redirect setter reference, in the corresponding
capability leaves. The existing canonical netstat reference now also accepts
text files, closing the resource-file classification gap. The command rules
exclude prose, suffixed identifiers and C function declarations. The setter rule
requires an exact extracted name in .text, without asserting its Boolean value.
No matcher was removed or narrowed, no severity was reduced, no identity exception
was added and no duplicate intent rule was created. The legacy netstat home is
retained during the documented network taxonomy migration.

| Sample | Hostile before/after | Suspicious before/after | Notable before/after | ML probability before/after | Calibrated ML |
|---|---|---|---|---|---|
| 96082e1bb535 | 0 / 0 | 0 / 0 | 92 / 93 | .730864 / .730864 | BENIGN / BENIGN |
| Main.plg | 0 / 0 | 0 / 0 | 1 / 1 | .0000182 / .0000182 | BENIGN / BENIGN |
| sysinfo.rc | 0 / 0 | 1 / 1 | 0 / 4 | .109490 / .536247 | BENIGN / BENIGN |

All original trait IDs and criticalities survive. The twelve manually extracted
resources were scanned under the HEAD rule snapshot and edited rules: identical
finding sets, zero hostile and zero suspicious in both runs. There are no material
detection losses or classifier/verdict disagreements. The suspicious resource
finding remains intentional dual-use signal. Model v18 reports that it predates
the engine's v21 feature schema; no rule was inflated to influence its score.

All twelve production-matcher controls pass, covering the intact suspicious
batch, reordered CRLF commands, individual queries, prose/function/suffix near
misses, pre-existing shell netstat coverage, and exact/extended/resource-only
managed setter names. Reproduce with `python3
testdata/taxonomy/console-launcher-review/check.py SCRATCH_DIR`.
`scan-comparison.json` and `control-results.json` retain the numerical evidence.
The final repository gate is `make validate`, after this record and the markers.

Judgment marker lines (each at most 72 characters):

```text
Ultimate Gems launcher: verified game updater; added HTTP policy trait
VC++ build log: inert worm-project build record, no active code
Meterpreter resource: inventory queries only; added query traits
```
