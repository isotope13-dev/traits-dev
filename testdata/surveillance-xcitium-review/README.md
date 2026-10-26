# Surveillance, Telegram instrumentation and Xcitium review

All three originals were scanned using Atomscan and `cleave facts`, then
inspected statically. No specimen or embedded command was executed. Raw scans,
full facts, decoded CIL, native cross-reference indexes, annotated function
traces, mutation controls and Forager sidecars are in the scratch directory in
`review.json`. The originals' hashes are recorded there. Counts include all
analyzed units, including the native executable's extracted wide-text unit.

| SHA-256 prefix | Identification and judgment | H before → after | S before → after | ML probability before → after |
| --- | --- | ---: | ---: | ---: |
| a2b9b2cffc9c | Custom .NET surveillance/ransom program — MALICIOUS | 34 → 36 | 12 → 12 | .99958664 → .99958646 |
| 0ea927ef886b | Telegram Xposed instrumentation source — MALICIOUS | 2 → 2 | 3 → 3 | 1 → 1 |
| 1d00d2351809 | Xcitium/Comodo configuration debug build — BENIGN | 4 → 0 | 6 → 1 | .97 → .6075921 |

The first two retain hostile classifier alerts (level 0). Xcitium changes from
alert level 25 to -1, agreeing with the reasoned verdict. Its actual WMI
antivirus enumeration stays suspicious. No original hostile/suspicious finding
was lost on either malicious sample. All moved observations that fired on
Xcitium still fire under corrected IDs and descriptions; its four hostile and
five suspicious assertions were unsupported relations or intent, not lost
malicious operations. The installed model warns that its feature specification
is v18 while the engine expects v21; that warning is not behavioral evidence.

## Execution evidence

**a2b9b2cffc9c.** The CLR metadata calls the class
`NanoCoreUltimate.Program`; this is not sufficient to attribute the real
NanoCore family. Many other family mutex names are deliberately created.
The assembly is unobfuscated. MethodDef 0x1d is the entry point; it invokes
persistence, clipboard/screenshots/key logging, hosts blocking, UAC hijacking,
security disabling, recovery deletion, and ransom routines, including worker
callbacks. This goes well beyond a harmless name or demonstration string.

* `InstallPersistence` (RVA 0x3450) writes its entry-assembly location into
  HKCU/HKLM Run values, copies to Startup, and creates logon and 30-minute
  scheduled tasks. `BypassUAC` (0x5624) writes the self path and empty
  DelegateExecute under ms-settings, starts fodhelper and schedules cleanup.
* `UpdateActiveWindow` (0x36b4) repeatedly calls GetForegroundWindow and
  GetWindowText. `HookCallback` (0x3720) combines the stored title, timestamp
  and captured key into a buffered record. This supports the added
  foreground-title/keylogger profile.
* Clipboard state machine 0x3840 reads clipboard data, records it and hands a
  CLIP record to `SendToC2`. It uses CF_TEXT but PtrToStringUni, so decoding is
  defective; this does not establish that no private bytes can be collected.
  `ContinuousScreenshot` (0x3a90) captures JPEGs, reads their bytes, Base64
  encodes them and calls the same sender. The file collector selects document
  extensions and sends FILE records.
* `ReadBrowserData` (0x512c) copies Chromium stores to a staging directory.
  Cookie state machine 0x5a10 reads Chrome Cookies, Base64-encodes and truncates
  to 5000 characters, prefixes COOKIE: and calls `SendToC2` (0x5ff8).
  That method appends local records and passes its argument to WebClient's
  UploadString at the configured HTTP endpoint. The new cookie upload profile
  covers this source separately from the existing input/screen/file profiles.
  Its matcher describes co-occurrence and does not pretend to bind CIL tokens
  to every particular buffer.
* The encryption worker (0x4458) enumerates a Desktop TestFolder recursively,
  attempts AES, writes a suffixed file and deletes the original after success.
  Its configured IV is 14 bytes; AES setup fails. Existing detections correctly
  describe an encryption attempt. The program still disables protections and
  recovery, exfiltrates input and cookie data, persists, and demands payment.
  TestFolder and a simulation event-log label do not explain away those effects.
* USBWorm (0x3efc) selects ready removable drives, copies its executable hidden
  and writes autorun.inf. `NetworkSpread` (0x56dc) only copies to localhost
  administrative shares; it does not establish cross-machine propagation.
  `ProcessInjection` (0x49a0) injects a single RET byte into Notepad, not a
  recovered second-stage payload. Imported debugger APIs with no callers are
  not asserted as executed anti-analysis. A KernelProtection registry value
  does not make the process termination-critical.

No authorized laboratory deployment was supplied. The balance of actual
surveillance, upload, persistence and destructive security changes warrants
MALICIOUS even though several routines are broken or conspicuously labeled.
Existing accurate findings remain; two supported missing profiles were added.

**0ea927ef886b.** Complete source review follows `install` into an Xposed
before-hook on Telegram SRPHelper.getX. It reads argument zero as password
bytes, decodes UTF-8 and persists the result with SharedPreferences.putString.
`handleRequest` takes SQL and account from request parameters, executes the SQL
against that account's live MessagesStorage database, collects cursor values,
and assigns their JSON to the response body. Neither function prompts the user
or limits a request to an application-selected export. These are credential
interception and a private database export surface. The existing bound-name
matchers describe both accurately. There is no obfuscation or additional
payload in this 1696-byte source. The loader/server, listener configuration,
module packaging and any claimed authorization are absent. Exactly two
independent hostile behaviors are supported; inventing a third would add no
coverage. No trait edit was necessary for this file.

**1d00d2351809.** Native PE x64, unsigned debug build, version resources naming
Xcitium Client - Security, PDB `CIS_UM/.../cfpconfg.pdb`, abundant consistent
source paths, RTTI, product configuration modes and diagnostic code. Identity
strings alone were not used to acquit it. RIP-relative references, imports,
exception-table function boundaries and call thunks were decoded to trace the
following distinct functions:

* 0x140f6df90 resolves Comodo license/security hosts and dynamically calls
  DnsFlushResolverCache in SecureDns.cpp. A separate hosts path is a wildcard
  protection-table item, not a write by that function.
* 0x140ae3470 opens ROOT and installs a certificate for the explicit Squid
  setup mode. The install/remove paths configure and undo proxy setup. Other
  certificate-store calls populate certificate data for verification.
* 0x141185b00 reads Firefox preferences including startup.homepage and
  startup.page into output parameters. Generic registry setters elsewhere do
  not make those reads a cross-browser homepage hijack.
* 0x140f8ff30 constructs protected registry-pattern lists including netsh,
  Run, browser settings and other autorun surfaces. 0x140f8c500 constructs
  protected cookie/Vault paths. The roaming credential wildcard also belongs
  to these protection lists. Independent DPAPI calls are buffer-decryption
  helpers (0x140f84f20 and callers); the matcher did not connect them to a
  credential-store read. Multipart APIs elsewhere do not bind a cookie path
  into an uploaded file.
* 0x140b7b3c0 builds a normal Windows process-name table including winlogon.
  Token launch routines such as 0x140bdb070 and 0x140bddc50 use supplied tokens
  or user contexts, including the interactive desktop. The file-wide matcher
  had no winlogon-PID-to-token relation.
* 0x140c9fe70 installs the product's ceshlp driver/service and adjusts its
  group ordering. A GroupOrderList path alone is not covert driver persistence.

The extracted 81-byte wide layer is an English diagnostic about importing
CIS configuration; it is not an executable Python stage. No hidden decoder or
payload handoff was identified. The actual setup, protection and management
operations fit cfpconfg's purpose. Comodo documents this utility for
[configuration export](https://help.comodo.com/topic-399-1-786-10201-import-windows-profiles.html)
and [security client deployment](https://wiki.comodo.com/frontend/web/topic/how-to-deploy-comodo-cc-and-ccs-packages-using-vbscript).
This does not authenticate the exact debug build: its distribution, operator,
signature provenance and intended machine deployment remain unknown. The
inspected effects favor BENIGN; legitimate privileged capabilities remain
notable and antivirus inventory remains suspicious.

## Corrections and preservation checks

`migration.json` records original effective definitions, exact-ID mapping and
old selector consumers. References were updated without changing source-to-sink
claims into stronger ones. Generic C2/service/task/port/COM/browser-name
observations were renamed and placed with their actual subjects. Certificate,
HTTP, crypto, execution and token observations stay at least notable.

The removed hostile inferences asserted hosts rewriting/interception, cookie
upload, homepage hijacking and SYSTEM-token theft. Their file-wide evidence
established only co-occurrence; the actual native paths above demonstrate the
benign matches. Their neutral profiles preserve all matcher legs. Similarly,
GroupOrderList, Netsh paths and generic autorun names plus registry APIs do not
establish persistence. Netsh's old OR was split into path and registration
command observations with a grouping composite. Source-specific persistence,
security-domain sinkholing, UAC-hijack, keylogging and other concrete attack
rules were retained. Known-product exceptions were not added for Xcitium.

Three existing neutral placements were corrected when auditing incoming
leaves: magic-link JSON fields and tenant/client token fields are credential
schema observations, not generic schema/upload; Proxmox API-token configuration
is not Windows process-token manipulation. The Go internal helper call is a
qualified call-name observation, not proof of impersonation. The leaves were
read and compared for equivalent matchers; no capacity-only split or budget
increase was used. The canonical Outlook COM matcher now also covers PE,
replacing the duplicate observation under email-worm propagation. Its consumers
still require the same native ProgID evidence. Generic co-occurrence remains
notable in signed products; removed downgrades do not imply lost operations.

Before edits, the rule-referenced hash 25645bc6... was recovered with Forager,
including its provenance sidecar. It identifies as RegNow Download Manager;
none of the targeted hostile rules fired. It was not treated as a confirmed
malicious positive merely because a YAML ref named it. Its findings are
identical before/after. The recovered 6087f0f3... Stormattack resource-injector
control, including its embedded PE, retains all findings (nine hostile, three
suspicious). The native download/decrypt/injection fixture retains its hostile
finding, and the Mettle control is unchanged. The original .NET sample retains
all 34 hostile and 12 suspicious findings.

Two length-preserving mutations independently remove the new foreground-title
and cookie-record profiles. Each retains the other new profile and all prior
hostile/suspicious detections. These are sensitivity checks on real executable
bytes, not a substitute for the external positive controls. `check.py SCRATCH`
asserts all sample deltas and all four external control results. The three
Netsh fixtures test the split key, command and query near miss. Test-rule
precision is 9.4 for the new title profile and 9.5 for the cookie profile.

All final scan judgments agree with the review. No supported detection was
removed to alter a score. The two behavior profiles were added because the
reverse engineering found missing coverage. The final repository check is
`make validate`; its output is retained in the recorded scratch directory.

The marker lines, copied verbatim into the prepared commit body, are:

```text
.NET spyware: input/cookie theft, persistence and recovery deletion
Telegram hooks: saves cleartext passwords, exports private DB rows
Xcitium cfpconfg: setup/protection code; fix unrelated-API claims
```
