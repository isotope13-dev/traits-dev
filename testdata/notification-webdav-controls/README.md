These fixtures exercise remote `file://host/DavWWWRoot/` and
`\\host\DavWWWRoot\` popup declarations, as
documented in [Investigating Ephemeral Supply Chain Tampering](https://cloud.google.com/blog/topics/threat-intelligence/investigating-ephemeral-supply-chain-tampering/).

Run `python3 testdata/notification-webdav-controls/check.py` from the repository.
The notable notification finding describes a literal remote WebDAV Address
in a popup record. It establishes neither rendering nor authentication capture.
The separate notable finding records zero/one-pixel popup geometry. Configuration
bytes alone establish neither popup activation nor deliberate concealment.

Positive cases change hostnames, paths, section numbers, field order, whitespace,
line endings, source language and URL/UNC spelling (including `@SSL@443`).
Controls reject HTTPS banners, local file URLs, loopback destinations, commented
addresses, prose and non-popup sections. Ordinary visible
WebDAV popups retain only the notable configuration finding. Geometry in another
section or another popup cannot supply the geometry finding.

The matchers inspect raw bytes because the text extractor omits short INI lines.
They cover literal configurations and embedded configurations in Python,
PowerShell, C++, C#, Go, Ruby and JavaScript. A popup record is bounded to 2,048
bytes and stops at the next opening bracket; dynamic construction and encoded configurations require
separate coverage. Priority, vendor names and campaign indicators are not gates.

UNC controls also reject loopback hosts with WebDAV suffixes, ordinary SMB shares,
mixed separators and addresses commented out or separated from tiny geometry.
The language scope follows literal configuration bytes; it does not imply that
the emitter itself negotiates NTLM or that NTLM applies to non-Windows clients.

Each observation has one matcher definition shared by disjoint file-type scopes
via a YAML anchor. The added source traits cover C#, Go, Ruby and JavaScript;
the original traits retain text, Python, PowerShell and C++ coverage. This keeps
each inline YARA trait within the four-file-type admission limit.

The configuration trait moved from credential capture to ui/window/notify;
its matcher and file scopes are preserved. No YAML consumers referenced its
old IDs. Writer controls must have no hostile or suspicious
finding; geometry and endpoint controls retain their previous match sets.

The geometry observation also lives in `micro-behaviors/ui/window/notify`: its
matcher reads configuration only. The move preserves every match and file scope,
removes the unsupported hidden-process mapping, and assigns notable severity.
There are no YAML consumers of its old IDs or ancestor selectors.
