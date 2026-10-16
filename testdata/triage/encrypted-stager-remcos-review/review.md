Reviewed 2026-10-16. These judgments are based on sample contents, independent
of the ML labels and collector-assigned filenames. No dependency artifacts
were involved and no specimen or controller-supplied code was executed.

| SHA-256 prefix | Identity | Judgment | Final hostile / suspicious |
| --- | --- | --- | --- |
| 5f03a613ae16 | Discover-Tech encrypted browser stager, JavaScript | MALICIOUS | 2 / 1 |
| 4f43abe997eb | The same stager in an HTML wrapper | MALICIOUS | 2 / 1 |
| 8096e142d65d | Native x86 Windows Remcos agent | MALICIOUS | 2 / 2 |

The browser scripts match the small WebSocket stager published in Confiant's
[Discover-Tech/Candiru investigation](https://blog.confiant.com/p/adint-weaponized-ad-tech-for-zero-click-spyware-and-mass-identity-vacuuming).
The observed code creates an Error.stack getter that records inspection,
reads WebDriver and storage/heap values, generates an extractable AES-256-CBC
session key, wraps that key with an embedded RSA-OAEP/SHA-256 public key, and
sends encrypted probe results over a WebSocket at the serving page's URL.
Its message callback Base64-decodes incoming data, separates a 16-byte IV,
decrypts the remainder, decodes the plaintext as text, compiles it with
Function, and invokes the resulting function with the encryption helper and
socket. Thus the server can repeatedly supply executable browser code and
receive encrypted results. This is a corroborated covert tasking stager,
not merely an advertisement or an ordinary encrypted communications library.
No subsequent browser exploit or credential-stealing payload is present in
these specimens, and none is attributed to their bytes by this review.

The Windows file is a 480,768-byte PE32 GUI executable with ordinary mapped
sections and an encrypted RCDATA resource named SETTINGS. Rizin identifies
that resource at file offset 0x715cc, length 1275. Its first byte is the RC4
key length, 113; the following 113 bytes are the key. RC4-decrypting the
remaining resource bytes yields fields separated by `|\x1e\x1e\x1f|`.
The decoded controller is 43.228.157.81:8080 with TLS enabled. The bot label
is RemoteHost, mutex Rmc-4A2JOQ, keylogger mode is 1, and the log filename is
UTF-16LE logs.dat. Mode 1 records all keystrokes. HKCU/HKLM Run flags are set.
Install, injection, startup browser cleaning and UAC-bypass flags are unset;
present capability code must not be confused with enabled configuration.
These field meanings agree with Elastic's
[Remcos configuration research](https://www.elastic.co/security-labs/threat-command/dissecting-remcos-rat-part-three).

Reverse engineering went beyond strings: at VA 0x41642d the loader resolves
section APIs, checks MZ/PE headers, calls CreateProcessW with creation flag
4 (suspended), performs section mapping and a WriteProcessMemory call at
0x416749, then SetThreadContext at 0x416766 and ResumeThread at 0x416773.
At 0x409203, keylogger startup launches worker threads, alongside the offline
keylogger recording status. The routine at 0x4066a6 prepares the mscfile open
command registry surface and launches eventvwr.exe with ShellExecuteW.
These routines are actual code, even where their startup options are off.
The decoded unrestricted-keylogging setting supplies concrete spying
behavior for the malicious judgment. Remcos branding alone was insufficient.
The supplied Triage URL was attempted but inaccessible, so it was not used
as corroborating report content. Binwalk found the native PE and ordinary
embedded constants, without an appended dependency archive.

Detection changes:

- Both hostile browser composites now require the inspector probe, a
  WebDriver member read, Base64 decoding, and nearby WebCrypto decryption and
  TextDecoder-backed compilation. Names/descriptions explicitly describe
  the required observations rather than pretending proximity proves a
  source-to-sink binding. The WebSocket composite additionally requires a
  constructor and message listener. No domain, public key, variable name,
  filename or exact file size gates these rules.
- Decrypt/compile proximity alone moved to the neutral compilation leaf at
  notable. Ordinary encrypted plugin loaders must not be convicted.
- Generic WebCrypto encrypt calls moved out of the AES implementation leaf;
  RSA-OAEP calls do not prove AES. Direction-neutral encrypt/decrypt references
  moved to cipher; direct decrypt calls moved to the decrypt operation leaf.
- String.fromCharCode conversion observations moved from charset decoding to
  string conversion, preserving the original matchers, scopes and exclusions.
- The secure WebSocket URL scheme moved out of HTTP to URL scheme. Its
  unrelated objective-based downgrade was removed: a URL reference remains
  notable. The redundant Typst filename guard was removed; that file type is
  outside its supported scan types.
- Transfer status atoms moved out of the backdoor objective. Their neutral
  conjunction now says transfer statuses coexist with a process API. The
  generic "Executing file:" atom was removed: it establishes neither a
  downloaded-file relationship nor a particular launch mechanism, and actual
  process creation remains independently reported by API traits.
- RunPE now requires PE-header parsing, SetThreadContext and ResumeThread
  evidence beyond the generic unmap/create/write trio. The hostile Remcos
  variant additionally requires this loader evidence, so vendor text and
  transfer statuses alone cannot establish malware.

`relocations.json` records exact IDs. Exact consumers and active fixture
expectations were updated. Directory selectors were audited too: the DNS
crypto, fresh-obfuscated-package, SMA credential-decrypt, and Rust Socket.IO
composites explicitly retain the relevant moved members. Losing bare
character conversion from ancestor decode selectors is intentional: it is
not proof of decoding. No aliases were added to disguise old classifications.

Verification: atomscan and cleave facts ran for all three original files;
Rizin resource inspection, xrefs and disassembly covered the native code.
Final atomscan JSON contains two hostile findings for each original.
`testdata/adfection-staging/check.py` passes 18 positive and near-miss cases;
`check.py` in this directory passes six capability and PE boundary controls.
The latter scans copies outside test directories so fixture exclusions cannot
mask false positives. The two minimal PE files are inert, RET-only fixtures
with API imports/status text, not executable copies of the malware.
The older cipher-directions manifest was updated for the moved ID, but its
12 referenced historical fixtures and shared runner are absent in this checkout.
Focused RSA encryption coverage was therefore tested with the new control.
The shared TOML expectations now require the relocated conversion trait; the
computed-dispatch control minimum score reflects conversion rather than decoding.

Marker summaries (all at most 72 characters, written alongside the samples):

    Discover-Tech JS stager: gate hostile rules on analysis probes
    Discover-Tech HTML stager: gate hostile rules on analysis probes
    Remcos RAT: require loader evidence; relocate transfer status traits
