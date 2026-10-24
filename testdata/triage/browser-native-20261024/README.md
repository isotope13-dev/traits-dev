# Native loader and two HTML samples, 2026-10-24

Verdicts concern the supplied bytes and available deployment evidence. External
family labels and scanner scores were not used as proof of functionality.

| SHA-256 prefix | Identification | Verdict | Hostile before/after | Suspicious before/after | ML probability before/after |
|---|---|---|---|---|---|
| 3a2b969eb101 | Protected native process-injection loader | MALICIOUS | 0 / 0 | 0 / 2 | .793989 / .978701 |
| 0cbd00fa34be | Legacy YouAreAnIdiot harassment page | MALICIOUS | 0 / 1 | 0 / 0 | .837837 / .986875 |
| bc7dc1c1a570 | VELSUR industrial-safety catalog | BENIGN | 0 / 0 | 0 / 0 | .287944 / .403796 |

All ML reports retained level -1 and model class 0. A fresh live tiny-format
scan of the harassment page explicitly prints **scan benign**, despite the
hostile YAML identity finding. This is a classifier disagreement, not evidence
for weakening the accurate rule. The installed model warns that feature spec
v18 is older than expected v21. Probabilities alone are not classifier verdicts.

The originals are single PE/HTML files, with no engine-reported archive members.
The native image contains packed resources discovered through emulation; these
are not automatically decoded archive-member findings.

## Native loader: evidence and limits

The original is a 6,295,014-byte x64 GUI PE. Its executable .text section has no
file-backed data. The renamed .trq1 section holds encrypted/virtualized code.
Rizin entry-point tracing reaches a register-saving VM entry and a rolling-key
byte interpreter. Unicorn emulation of the *original bytes*, with local Windows
API stubs and synthetic export tables, recovered the native code and part of
its resource data. No real Windows API calls, native network connections or
successful infection are claimed from this emulation.

The unpacker resolves and checks IsDebuggerPresent,
CheckRemoteDebuggerPresent and NtQueryInformationProcess (class 0x1e), calls
NtSetInformationThread with class 0x11, checks kernel-debugger information,
checks its code with a CRC transform, changes image protections, and restores
original code. Those effects were traced in the unpacker, not copied from a
sandbox signature. Individual hidden anti-debug API names are not exposed by
the current facts decoder, so no broad string-only debugger trait was added.

Recovered native execution paths include:

- RVA 0x3430 enables SeDebugPrivilege, obtains its executable resource, resolves
  process suspension/resumption, and passes the resource bytes to RVA 0x2fa0.
- RVA 0x5240 assembles the visible configuration URL, appends a site identifier,
  obtains its response through the HTTP routine at RVA 0x4ac0, decodes/parses it,
  and stores an integer switch. The literal at original offset 0xd00 is
  https://rule.110route.com/api/index/getSwitch?barid=. The endpoint fetch was
  attempted; no useful response artifact was recovered.
- RVA 0x2230 creates a helper with CREATE_SUSPENDED | CREATE_NO_WINDOW, using
  generated executable names and a PerfLogs staging path.
- RVA 0x2fa0 prepares executable remote memory, writes a 0x540-byte PE mapper
  from RVA 0x2d000, copies the resource payload and loader parameter block, and
  invokes a resolved NtCreateThreadEx entry with the mapper as its start address.
  RVA 0x2d000 checks MZ/PE headers, processes PE sections and loader metadata.
- NtCreateThreadEx is reconstructed with XOR key 0x47 from a constant table and
  a final stack-written byte. The new matcher recognizes the long encoded API
  prefix under any nonzero key; it does not assert an imported or executed call.
- A partially recovered resource includes another x64 loader with remote-memory,
  process-creation, service and driver APIs, and a packed driver. These are
  incomplete memory reconstructions, **not recovered original binaries**.
  Public sandbox download links returned login HTML; API retrieval returned
  401, and forager hash recovery of the dropped helper was unsuccessful.

The deciding evidence is concealed, remotely gated execution through a
suspended helper and a custom in-memory mapper, combined with anti-analysis
and randomized staging. This could overlap a strongly protected management
product, and an associated endpoint has internet-cafe management provenance;
there is no verified publisher, installer, authorization or deployment context
establishing such an explanation for this artifact. The balance favors
MALICIOUS. Neither IcedID nor njRAT attribution is established.

**Hostile-coverage goal remains unmet.** The original bytes now have two
distinct suspicious concealment detections, plus native loader, masked thread
API, suspension, configuration path, log path, hashing and resolution signals.
The stable matchable primitives remain dual-use. The actual allocation/write/
thread chain, anti-debug checks and subsequent driver/service effects lie
behind virtualization/compression. We traced recovered code and attempted
stage recovery; we did not convert generic API co-occurrence or sandbox-only
effects into three hostile static claims.

## YouAreAnIdiot: evidence and limits

The HTML's keydown dispatch calls altf4key(), ctrlkey() and delkey(); mouseout
calls procreate(); onload calls playBall(). It loads an external script and
embeds a Flash movie. The return before bookmark() makes that bookmark call
unreachable in the supplied onload handler.

The current main-site script is a newer incompatible revision, so it was not
treated as the missing original. The publisher's historical source and Flash
mirror provide the matching script:

- https://git.enderman.ch/youareanidiot.cc/flash/raw/commit/ed0ab1284dd9b68b6d51c9dff96344cf04df9f12/scripts/you.js
- https://fl.youareanidiot.cc/scripts/you.js

Tracing that script shows procreate() opens five new windows through
openWindow()/window.open(), the exit-related keys trigger alerts and another
procreate(), and playBall() moves the window and schedules itself after 1 ms.
The matching mirror lol.html starts playBall() as well. The harassment intent,
automatic mouseout trigger and retaliation on system keys tip the verdict;
there is no supplied consented demonstration or archival deployment context.

**Hostile-coverage goal remains unmet.** One hostile page identity is justified
by the joint key/mouse dispatch and actual script-loading element. Five-window
amplification, 1 ms motion and focus stealing are implemented in the external
sidecar, not in this HTML. They cannot truthfully become three independent
static behavior claims about the supplied file. The rule therefore names the
legacy harassment page; it does not claim standalone HTML contains those loops.

## VELSUR: evidence and limits

All inline scripts were inspected. They construct product navigation, initialize
image sliders and social links, animate catalog elements, and render two PDF
catalogs into canvas/images with booklet, zoom, resize and fullscreen controls.
The 12 entity-escaped link values were decoded and checked: all become local
product-page anchors using x5engine.utils.location(). The document.write calls
emit the site's loading animation. Loopback 127.0.0.1 appears in og:url metadata,
not a fetch or exfiltration sink. WhatsApp URLs are visible sales/contact links.

The external Font Awesome 4.7.0 stylesheet was fetched and inspected; it contains
icon styles and font references. Same-origin JavaScript and PDF recovery was
attempted through forager over HTTP/HTTPS and a historical archive query.
velsurperu.com no longer resolves; missing dependencies cannot be certified.
No injected script, credential capture, executable staging, forced redirection
or exploit path was found in these bytes. BENIGN is the balance-of-evidence
verdict, with that dependency limitation. The source may have collected a
compromised-site crawl, a historically infected dependency or simply a
mislabeled saved webpage; the available record does not distinguish these.

All original neutral findings were retained. The added entity-substitution
trait accurately covers the visible custom decoding without assigning evasion.

## Shared-rule review and verification

- Changed NtSuspendProcess's left word boundary to a suffix boundary so an
  adjacent printable padding run cannot hide the API name. Existing unprefixed
  references and UTF-16 text remain supported; NtSuspendProcessEx does not match.
  Exact and ancestor consumers were inspected. EDR-suspender composites still
  require their additional CLI/target evidence.
- Removed the shared default T1562.001 mapping from that file: process-control
  API names and tool contexts establish no defender-targeted disabling.
  No criticality was lowered.
- Moved archive.sha256 field syntax, with its matcher/scope/confidence/criticality
  unchanged, from hashing into metadata/lang/source/syntax/member. Its digest
  consumer now references the new ID. A member reference alone establishes no
  digest computation. Source ancestor consumers require PE, PowerShell or
  Python; the destination's PHP-only syntax suppressor is disjoint from this
  JavaScript/TypeScript atom. The field and real digest-context controls pass.
  This also keeps the digest leaf within its existing 100-rule budget while
  adding actual BCrypt hash-finalization coverage.
- No original attack detection was lost. The generic image-file-url umbrella
  was omitted from the final harassment-page report. Focused evaluation
  confirms it still matches and explicitly reports low-value OR-composite
  output filtering. Its precise jpeg-png-gif-file-url child remains emitted.
  This is redundant output loss, not lost image URL or attack coverage.
- 18 focused controls cover renamed HTML, inactive comments, keyboard-only and
  ordinary UI near misses, original/glued/suffixed API names, changed decoder
  keys, missing feedback, XOR keys and section bounds, plain-text thread names,
  benign entity decoding and relocated hash-member/consumer coverage.
  Run: python3 testdata/triage/browser-native-20261024/check.py
- Full atomscan/facts outputs, disassembly, emulation scripts/snapshots, and
  forager artifacts with .forage.json provenance are under the task scratch
  triage directory. scan-comparison.json records exact added/omitted IDs.
- Required final check: make validate. Precompilation is needed only if that
  check reports a stale fingerprint from the new inline YARA matcher.
