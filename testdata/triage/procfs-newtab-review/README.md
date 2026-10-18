# Reasoned sample review: 706f25 / af31c2 / b7a1d4

Reviewed 2026-10-18. All three supplied SHA-256 values were verified. Samples
were inspected statically; their executables and scripts were not run.

| Artifact | Identification | Verdict | Final hostile / suspicious traits |
| --- | --- | --- | --- |
| `706f25d1a1e05c545915e1411ab891b46758b9023f11277d36eb872677fba861` | Satoru Gojo Rose Live Wallpaper New Tab, Gameograf, version 4 | BENIGN | 0 / 1 |
| `af31c252ef85426825116175da17e3a9bdc0cdee72cd5c274595d80f92fd2006` | PEERSTITCH-style FortiOS memory patcher source | MALICIOUS | 0 / 3 |
| `b7a1d4bf2b3eaf1fada348ce91c40f1a899d2844937de092c93ad306abafa69c` | Self-labeled NanoCoreUltimate .NET stealer and disruptive ransomware attempt | MALICIOUS | 17 / 13 |

## Wallpaper extension

The MV3 manifest overrides the new tab, requests search/alarms/storage and
limits extension host authority to api.gameograf.com. There are no content
scripts, default-search override, history/cookies grants, or DNR rules.

Execution trace:

- The install callback checks `details.reason === "install"`, opens a
  marketing page once, refreshes JSON message/shortcut data and schedules a
  30-minute alarm. Browser startup repeats the refresh and alarm setup.
- Alarm handling refreshes those two JSON documents into local extension
  storage. The new-tab scripts subscribe to storage updates and render the
  remote shortcuts/banner. Shortcuts can be deleted and reordered; sponsored
  items have an Ad badge and the banner can be disabled.
- Search-button/Enter handlers call `chrome.search.query` with the user's
  text. This API uses the configured search provider. The result-navigation
  code does not replace the provider or route queries to the publisher.
- The tab counter POST contains a count, UI-language prefix and extension ID.
  Banner POSTs contain timestamp, event type, language and extension ID.
  No persistent user identifier or browsing-history payload appears in these
  paths. Weather fetches include an optional user-entered city.
- Notes, tasks, settings and custom images are saved locally. The ChatGPT
  widget opens a user-entered query only on button/Enter interaction.
- The popup uses textContent for message text, but shortcut fields are
  interpolated into jQuery HTML. This is an unescaped rendering surface, not
  evidence of a malicious remote payload in the supplied bytes. Comments
  asserting universal safe-DOM rendering are inaccurate.

No IndexedDB deletion, victim browsing interception, covert input capture or
remotely supplied executable code was found. jQuery is exactly the official
3.7.1 minified release: both SHA-256 values are
`fc9a93dd241f6b045cbff0481cf4e1901becd0e12fb45166a8f17f95823f0b1a`.
The source was compared against https://code.jquery.com/jquery-3.7.1.min.js.

[Unit 42's campaign list](https://raw.githubusercontent.com/PaloAltoNetworks/Unit42-timely-threat-intel/refs/heads/main/2026-06-01-Adware-Wallpaper-Chrome-Extension-Campaign.txt)
describes publisher-level adware behavior, including IndexedDB deletion and
other versions' HTML popups. That is a lead, not proof this build performs it.
The retained suspicious PUA identity describes the recognized publisher's
promotional new-tab family. Ordinary monetization does not establish malware.

## C patcher

The entire 106-line source was traced from main. `find_daemon_pid` enumerates
/proc, reads cmdline files and selects `/bin/miglogd` and `/bin/iked`.
`find_base_address` reads maps, but its returned value is ignored.
`inject_and_patch` performs PTRACE_SEIZE, PTRACE_INTERRUPT, waitpid and
PTRACE_GETREGSET, then opens the selected PID's mem file read-write, seeks to
0x106F7B8 and writes four bytes, e0 03 00 aa (AArch64 `mov x0,x0`). Main then
unlinks argv[0]. The hard-coded instruction overwrite of logging/VPN security
daemons, followed by removal of the patcher, supports MALICIOUS.

It contains no mmap/bootstrap, ring buffer, counterpart-memory forwarding,
traffic hook, syscall payload or explicit execution redirection. The IP/port
macros are unused. There is no explicit ptrace detach/resume. Neither the
original instruction nor a successful security-check bypass can be established
from this source alone. It is a reduced patcher, not the full implant in
[Unit 42's PEERSTITCH analysis](https://unit42.paloaltonetworks.com/fortimanager-cve-2024-47575-peerstitch-malware/).

The revised detectors intentionally retain only generic suspicious memory
access/patching signals: those match legitimate debugging too. Verdict and
trait severity are independent. Three suspicious traits satisfy coverage
without inventing an attack-specific bridge or a general hostile debugger rule.

## Managed executable

ILSpy C# and CIL output were reviewed, including Main, callback/task targets,
SendToC2, encryption and static field initialization. No obfuscation prevents
tracing. The NanoCoreUltimate namespace and several malware-family mutex names
are self-assigned labels, not verified NanoCore family attribution.

Main directly attempts input blocking, security-service/Defender disabling,
security-site hosts blocking, fodhelper DelegateExecute elevation, shadow-copy
deletion and IFEO Debugger hijacks of taskmgr/regedit/msconfig. It also calls
persistence setup and schedules recording, replication and encryption tasks.

StartKeylogger installs WH_KEYBOARD_LL and polls GetAsyncKeyState. HookCallback
records keys with the active window title. FlushKeylog Base64-encodes records
and calls SendToC2. ClipboardMonitor records changed clipboard content;
ContinuousScreenshot captures JPEGs; file collection reads targeted document
folders, stages the first 1024 bytes and sends FILE records. Browser and Windows
credential-store files are also copied. USBWorm copies the current executable
to removable drives and writes autorun.inf. Run keys, Startup copies/batch files
and logon/repeating tasks attempt durable reactivation. Registry association
changes attempt to make opening PDFs run the sample.

SendToC2 appends its argument to local files, then calls
WebClient.UploadString("http://isima.io", data). This path is reachable from
recording tasks; it does not consult IsPlaceholder. IsPlaceholder returns true
and disables the separate random-subdomain beacon only. CIL confirms that
SendToC2 loads its string argument immediately before UploadString.

RealEncryption enumerates Desktop/TestFolder and intends to encrypt to a
suffixed output before deleting the original. Its 16-byte AES key is accompanied
by a 15-byte IV (`H1ddenT3ars1v!!`); the IV setter should throw before output or
deletion. Ransom notes, wallpaper, input lockout and security disruption remain
independent. The firing encryption trait already accurately says *attempt*.
The existing recording, persistence, recovery inhibition, UAC and disruption
traits are supported and were retained without YAML changes for this artifact.
The supplied [Triage report](https://tria.ge/261018-r2pmqabd69) was unavailable
through the web reader; its reported score was not used as behavioral proof.

## Detection changes and placement review

- Gameograf manifest/search/feed/bundled-shortcut rules now describe family
  features at notable severity. The feed rule loses its unsupported takeover
  name. Removed version-number/store-marker trust exceptions; promotional PUA
  identity remains suspicious regardless of version or signing-file presence.
- Scheduled new-tab alarm/network co-occurrence moves from impact to
  micro-behaviors/time/schedule/webextension. It states references, not proof
  the alarm fetches or the fetched value reaches the DOM.
- Procfs cmdline/maps/mem path co-occurrence moves from evasion/procfs to
  micro-behaviors/fs/proc/memory. It is notable, not a bridge claim.
- Read-write procfs/write proximity and the existing pwrite evidence move to
  micro-behaviors/mem/write/arbitrary. Debugger seize plus memory access moves
  to micro-behaviors/process/attach/debugger. Descriptions explicitly avoid
  unproven descriptor binding or execution transfer. Suspicious capability
  coverage remains. The old pwrite consumer is updated to the relocated ID.
- The Gameograf API-host permission atom is removed as a duplicate of the
  existing declared-host metadata finding; a grant is a property, not an
  additional unwanted-family behavior.
- Repeated mem_fd spelling moves from injection/hijack to source naming.
  Naming remains observable in kernel code; kernel exclusions now guard
  the two intent consumers rather than hiding a valid naming observation.
  This separately strengthens kernel exclusions on the optional-name consumer.
- argv[0] unlink moves from fileless/memfd to fs/delete/file/self, notable.
  There is no memfd in the matcher.
- The track-label URL atom moves from a supply-chain/affiliate objective to
  communications/url/host/name. Its hostname prefix now excludes slashes, so
  `/panel/track.php` cannot be mistaken for a hostname. Its consuming affiliate
  group references the new ID. Other unrelated domain atoms are unchanged.

Placement was checked first by supported claim (identity, property, operation
or intent), then by the nearest competing operation (write vs execution
transfer, self-deletion vs memfd, hostname vs URL path). Existing leaf homes
were used throughout. Aside from the explicitly documented track correction,
severity/description corrections, the naming/kernel exclusion correction and
deletion of trust exceptions, moved matcher scopes/exclusions are preserved. Pwrite rules retain Linux scope.

The mem_fd atom had two local intent consumers, both updated. No broad
metadata/lang/source/naming selector consumes the new atom.
Exact-ID and ancestor-selector audits found no exact consumers of the retired
bridge, memory-patch, seize, argv-unlink or scheduled-refresh IDs. Empire's
injection selector targets PowerShell; the moved ptrace/memory source rules
are outside that scope, and it already selects micro-behaviors/mem. The
broader file-operation consumers target JS, PE or PowerShell, outside the
moved argv-unlink C/C++/ELF scope. CrystalX's broad impact exclusion cannot see
the moved CRX/new-tab rule under its file scope. No ancestor rewrite is needed.

## Verification

For each original artifact, `atomscan --no-update --follow=none --mode slow -f
json <path>` ran before and after edits, and `cleave facts <path>` captured
matchable data, including decoded strings. No fetched dependency PURL was
reported. The vendored jQuery dependency was additionally verified in isolation
against the official bytes.

Nine inert focused fixtures cover procfs path-only/read-only/read-write
observations, argv[0] versus argv[1] deletion, descriptor naming, a track hostname versus track.php
path and a version-4 search manifest. Run them with:

```
python3 testdata/triage/procfs-newtab-review/run_cases.py --staging /path/to/scratch/controls
```

Staging avoids the existing test-directory suppressors so the underlying
matchers are exercised. All nine cases passed, with no hostile findings.
Original samples retained the counts in the verdict table after rescanning.
Judgment markers were written next to the original sample files. The final
repository action is `make validate`; no inline YARA was changed.
