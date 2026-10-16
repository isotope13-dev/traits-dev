# Loader and NuGet canary first review

Judgments are based on static code and package contents. No sample was executed.
No listed finding originated in a fetched dependency. Each requested artifact
was scanned separately, with reference following disabled for final checks.

## b2d6cf67cae6 — MALICIOUS

Rebuilt x86 Sfuzuan-compatible resource injector, not evidence for every family
in its collector-assigned filename. At VA 0x407c3d the program extracts resource
129, enumerates processes, selects winlogon.exe, creates a shared memory mapping,
and passes the selected PID and resource bytes to its mapping/injection routine
at 0x40a860. The remote-memory implementation at 0x40aa40 writes image data, and
0x40b580 dispatches remote threads. Host data is formatted at 0x401f97, wrapped
in the client-report query at 0x401ffb, and sent through WinInet code at 0x40421d.
The recovered image and embedded x64 PE indicate a reconstructed multistage
artifact; they do not establish cryptocurrency mining or ransomware.

The IsDebuggerPresent references are in MSVC runtime failure-handling code.
Resource access, VirtualQuery and VirtualProtect plus those imports did not
prove an anti-debug execution gate. Remove that unsupported hostile composite:
its useful constituent API findings already remain. Move the PEB/NT-write/
debugger-import combination to a neutral injection API profile, with matching
name and description. Retain the independently supported hostile injection
and protocol identity traits. The exact client-report schema now anchors
family identity; changing campaign domains in a copy preserves detection while
the old domain observation stops matching. WinInet HTTP references stay notable
even when the PE has a version resource or many imports.

## c550e66382b5 — BENIGN

Identity.Sync.Ism.Common 2027.1.3329 is a disclosed dependency-confusion security
canary. The archive contains metadata, a signature, and identical build and
buildTransitive targets; no assembly, script execution or additional payload is
present. The targets use MSBuild DownloadFile before Build, sending the package
label and COMPUTERNAME to webhook.site and saving the response in the
intermediate output directory. ContinueOnError permits failed requests.
Authorization is an unverified publisher claim, not an established fact.
The limited disclosed behavior does not support a malware conviction.

Move disclosure/authorization claims to metadata and the build trigger to build
metadata. Expose the hostname-bearing HTTP request as a notable capability,
including its longer URL and XML property syntax. Do not let a publisher's own
canary disclosure suppress communication findings. The old archive-wide webhook
co-occurrence becomes a neutral capability with an honest co-occurrence
description; it proves neither compromise nor exfiltration intent.

## ec43a4f49df3 — MALICIOUS

Reconstructed x86 StormAttack/Shtormec installer. At VA 0x401cb0 it queries
LanmanServer's ServiceDLL, constructs a System32 DLL target, and calls the
resource drop routine. VA 0x401150 creates a child process, allocates and writes
its remote memory, resolves LoadLibraryA and starts it with CreateRemoteThread.
VA 0x401900 creates an Active Setup key and StubPath, copies/patches its own
image, then launches the copy. Service creation and dispatch paths also remain.
The zeroed resource section limits recovery of the original DLL payload; the
installer code and embedded Storm banners establish the malicious installer.
Microsoft's Shtormec.A description independently documents the same StormServer
DLL, service target and browser injection mechanism:
https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Backdoor%3AWin32%2FShtormec.A

Appended sections contain ZoomIt, PeerBlock and SQLite fragments. A ZoomIt
banner without the author's name does not identify GoldenEye; disable that
third-party rule instead of retaining its false attribution at notable.
The old recovery regex matched ERROR_SERVICE_DATABASE_LOCKED. Move recovery
wording to neutral UI/error and require word boundaries around its nouns.
The engine's metadata/encoded-payload/url finding is percent-decoding of a
printf GUID format, not evidence of an embedded URL or network contact. This
engine-emitted ID has no YAML suppression hook; do not shadow it with a rule.

## Reference and validation audit

No exact YAML consumers remain for the removed or relocated IDs. Ancestor
selectors in hosts-file blocking, a Python stealer, JS credential/payload
composites, CrystalX, and a locker rule were reviewed. Removing neutral API
co-occurrence and ordinary error wording from those intent-selector populations
is intentional; adding the neutral destination back would restore unsupported
intent. Positive selectors lose these weak members. CrystalX uses the C2
ancestor as an exclusion, so removal also narrows that exclusion; none of the
three samples acquires a CrystalX finding. No whole-corpus claim is made.

Run `python3 testdata/triage/loader-canary-review/check_cases.py` for six static
positive/near-miss fixtures. The controls cover comment-only targets, an ordinary
download, a hostname request, a disclosure alone, and service/file recovery
messages. The final sample scans yielded H/S counts 2/2, 0/0 and 2/1. Hostile
precision scores were 10.8 and 8.8 for the first PE, and 10.1 and 12.1 for the
second PE, exceeding the 3.5 authoring floor.

Judgment marker contents (also used verbatim as commit paragraphs):

Sfuzuan loader: remove API-only hostile; retain winlogon injection

NuGet security canary: expose hostname request; claims are metadata

StormAttack installer: remove ZoomIt/GoldenEye and service-error FPs
