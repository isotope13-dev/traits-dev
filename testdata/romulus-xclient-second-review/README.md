# ROMULUS reconstructions and damaged XWorm client: second review

The three supplied files were reviewed statically, independently of their
existing labels, ML scores, comments claiming a campaign, and third-party
signatures. No sample or downloaded stage was executed. No claimed downstream
payload was independently verified; subsequent scans disabled reference
following. `atomscan` and `cleave facts` were run on each original, including
the extracted ASCII and UTF-16 strings. Python/dnfile/dncil and rizin were used
to inspect the PE headers, metadata, method bodies and CIL control flow.

| Supplied file | SHA-256 | Judgment |
| --- | --- | --- |
| romulus_routeA_stager.ps1 | 0c6560390592bd01268248e443e0a9f5625e5670d25437a7e99c61b23ebbda3a | BENIGN |
| romulus_routeB_stager.ps1 | 5177fc69c566f053b1cfe56a0f6a9c7b02d8d3ef4c0605c40fa7d7b51ad1fdc0 | BENIGN |
| embedded_xclient.exe | b524ba48c3f5bdf83887d5420471ea503248249df75abd34270472f75b2d93be | MALICIOUS |

BENIGN here follows the requested burden of proof: the supplied script must
establish hostile behavior. It does not certify the contents of an unavailable
MSI or encrypted archive.

## Route A

This is a short, self-described staging reconstruction. It stores its own
script path in an environment variable, XORs 45 integer elements with 0x5a,
joins the resulting characters, and attempts ScriptBlock construction/invocation.
The decoded text is exactly:

```text
,&99: bp1&b&9(9&b+"&p$"3b"&&3d3$9"bb-p(&,&=&&
```

That is malformed PowerShell, not a recovered hidden command. Dynamic
compilation can fail; the script does not set terminating error preferences.
The visible staging function remains a separate execution path under normal
nonterminating error handling.

The function selects TLS 1.2 but actually uses an HTTP URL with decimal IPv4
1450003207 (86.109.75.7). WebClient downloads an MSI to a LocalAppData Programs
subdirectory, retries up to three times with randomized short delays, invokes
Unblock-File, then launches `msiexec /i ... /qn /norestart` hidden and waits.
Finally it deletes the stored script path. It does not create the destination
directory or stop after all download retries fail, which limits successful
operation. The browser User-Agent, integer host, quiet install and self-cleanup
are observations; they do not prove an exploit, credential theft or malicious
MSI. No DLL replacement or sideloading is implemented in these supplied bytes.
The comment claiming a Stardock chain cannot supply that missing evidence.

## Route B

The 33 integer elements XORed with 0x37 produce the following Python repr
(the escape denotes the literal DEL character):

```text
'clagp}n,}laelg\x7f,a}llang,`}g}llang'
```

This also is malformed source. The remaining visible path creates a random
temporary directory, obtains the standalone 7-Zip extractor from a GitHub
release, downloads an external 7z archive, and invokes the extractor with a
literal password. It reads an extracted text file for a second password,
extracts the nested archive, launches `loader.exe` hidden and deletes its own
script. There is no integrity check, but absence of one does not establish
hostility. Neither archive's contents are supplied; the LegionLoader claim is
a comment, not verified payload identity. Passworded extraction, temporary
staging and process launch remain notable capabilities.

Both scripts retain one suspicious trait: character transformation near dynamic
ScriptBlock invocation. Its description explicitly states co-occurrence rather
than claiming that the transformed value is bound to the invocation argument.

## XClient

This is a damaged, obfuscated VB.NET XWorm client, with XClient.exe version
metadata. Identification is supported by the distinctive command vocabulary
and the surviving implementations, not just the version resource.

The CLR entry token is 0x06000026, RVA 0x2704, file offset 0x904. Its method
body is zeroed, as are numerous other bodies in the early method region.
Many TypeRef, MemberRef and method names are also blank. Normal startup and
successful C2 communication cannot be established for this damaged copy.
The native entry stub leads to mscoree; the trailing native data is outside
mapped sections and is not a demonstrated alternate entry path.

Surviving CIL still establishes an attack implementation:

* Method 0x06000074, RVA 0x3738, transforms its input and splits command
  fields. Its comparisons select branches for `RunShell`, shutdown/restart,
  download/run, plugin transfer, hosts-file operations, DDoS control and `$Cap`.
  The `RunShell` branch passes the command field to a now unnamed VB helper;
  its purpose is inferred from that branch and the parallel shutdown branches.
* The `savePlugin` branch Base64-decodes received bytes, stores them and passes
  them through the transform helper into method 0x06000075 (RVA 0x3fc4).
  That method loads bytes through the managed loader, walks plugin types and
  methods, and invokes selected entries through VB late binding. `injRun` and
  `UACFunc` delegate to a supplied plugin; their names do not prove an actual
  injection or elevation implementation in the client.
* The screenshot branch acquires desktop-sized image data, resizes it to a
  thumbnail, JPEG-encodes it, transforms/Base64-encodes the bytes, constructs a
  `#CAP` response and passes it to the send routine. That send routine is among
  the erased methods, so successful exfiltration is not claimed.
* DDoS method 0x06000078, RVA 0x4528, parses host, port and duration, starts
  twenty workers per loop, waits five seconds and repeats within a time gate.
  Worker 0x060000a1, RVA 0x4974, creates a socket and sends a POST header with
  keep-alive and a positive Content-Length, but no promised body, then sleeps
  2.5 seconds before disposal. This is a threaded incomplete-POST exhaustion
  implementation. The task dispatch contains explicit start/stop controls.
* The surviving crypto helper constructs RijndaelManaged, derives key bytes
  using ComputeHash, sets cipher mode and calls TransformFinalBlock on
  Base64-decoded bytes. Missing type/member names prevent a complete verified
  configuration recovery. `OfflineGet` explicitly reports that the offline
  keylogger is not enabled; a functional keylogger is not inferred.

The original UAC finding combined exefile/IsolatedCommand strings in appended
native data with API-name strings elsewhere. The file imports only
`mscoree!_CorExeMain`. No native registry setter import, auto-elevation command,
or executed write to that key was established. The finding was a false positive
even though the remaining artifact contains malicious code.

## Trait changes and placement review

* Generic scalar XOR character conversion and decimal-host downloading are
  notable. Concealed-source context is suspicious, rather than hostile.
  Updated the two existing benign decimal-host MSI fixture expectations to
  require the retained trait while allowing no suspicious or hostile findings;
  their previous minimum scores depended on the incorrect suspicious level.
* Removed the self-delete environment composite: a stored script path and any
  nearby forced deletion do not bind the deletion target. Added a neutral
  environment-path deletion observation. Hidden launch plus self-deletion
  alone is suspicious and no longer claims a staged hostile payload.
* Replaced an unbound password/yes flag pair with an actual 7-Zip extraction
  command matcher, including quoted 7zr paths and variable passwords.
* Moved generic executable URL, loader filename, computed invocation, TLS enum,
  JPEG encoding and plugin command observations to their operation/resource
  homes. Runtime DLL/RTTI references no longer claim filesystem traversal.
* Removed the generic C++ runtime evidence from traversal aggregators and
  renamed its Mespinoza consumer to describe runtime references honestly.
* Audited the full dispatch and executable-path leaves before adding rules.
  Moved existing method/function declarations, control labels and string
  concatenation to their property/operation homes, preserving their matchers
  and exact consumers. No directory budget was increased.
* Parent-selector review: removing bare runtime references from traversal and
  plugin words from C2 selectors intentionally removes unsupported behavior
  inferences. The Python screenshot selector cannot consume the PE-only JPEG
  atom. The HTTP download selector already contains the executable URL atom
  used by the relocated SSM-filtered URL trait; its OR adds no new population.
* XWorm command fingerprints are scoped to the mapped .text user-string heap.
  StartDDos uses one canonical neutral atom shared with the DDoS objective.
* The new DDoS objective requires a managed image, start and stop task tokens,
  and mapped CIL implementing thread fan-out plus the incomplete POST/send/wait
  sequence. A token, HTTP header or thread loop alone is insufficient.

## Focused verification

Run `python3 testdata/romulus-xclient-second-review/check.py` from the repository
root. It checks the original SHA-256 digests and 15 static sample/control cases.
It requires dnfile for constructing PE constituent controls. The original
samples remain external; no sample execution is part of the check.

Controls cover harmless XOR conversion, valid transformed-source invocation,
unrelated deletion, quiet installer cleanup, quoted passworded extraction and
unrelated `-p`/`-y` flags. Binary controls remove tasking, thread-fan-out or body
header evidence separately; a renamed copy preserves detection. The UAC control
adds an actual imported registry writer and an elevation command, then removes
the trigger to check the near miss. All 15 controls passed. Each original is
also rescanned with atomscan after trait edits. Repository validation is run
last, after writing the three judgment markers.
