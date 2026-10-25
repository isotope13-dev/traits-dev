# Efimer, Foxveil and installer-page review

Verdicts: `71cfefd6acba` **MALICIOUS**, `540d24a82a36` **MALICIOUS**,
`f6031a47fd8f` **BENIGN**. Decisions follow static execution-path review and
independent decoding. No sample was launched against this host or its endpoints.
The collection labels and ML probabilities were leads, not proof.

| Original sample | Hostile before → after | Suspicious before → after | ML probability before → after | ML matched FP level before → after |
|---|---:|---:|---:|---:|
| export.php | 2 → 0 | 4 → 5 | .9800000 → .9700000 | 25 → 279 |
| macho_540d24a82a36.bin | 9 → 9 | 2 → 2 | .99933857 → .99933857 | 0 → 0 |
| platform-loader.html | 4 → 0 | 0 → 0 | .9874031 → .9215649 | -1 → -1 |

The matched FP levels are reported as returned by atomscan; -1 means no
calibrated match. The v18 model warned that its feature schema predates v21.
The historical public HOSTILE verdict for the HTML is unsupported by the bytes.
The PE still has strong ML suspicion, but **no hostile YAML behavior detection**
after correcting the unsupported profiles. Its malicious verdict does not close
that detection gap. None of the three original files is an archive and none
fetches a package dependency during these local, follow-disabled scans.

## PE: Efimer installer and wallet-secret stealer

The original hash matches the supplied SHA-256. The file is an unsigned PE32
.NET GUI assembly, internally `installer.exe`, version `0.0.0.0`, with blank
publisher-facing fields and an `asInvoker` manifest. Its collected `.php` name
is a format discrepancy; there is no evidence that the original attacker chose
that filename. Packaging alone would not establish malware.

The module initializer calls MethodDef `0x06000003`. Its xorshift state expands
16 words, XORs successive blocks of initialized field data, updates the state
from the plaintext, and passes the result to the embedded LZMA decoder. The
result is an 888-byte constant table. Generic accessor methods multiply/XOR
caller integers, select a constant type and index, and return UTF-8 strings.
The five accessor transforms were resolved independently with dnfile/dncil.
The installer entry is MethodDef `0x06000046`, RVA `0x7d94`.

Its relevant paths are:

- `M39` checks resources/process modules, including Sandboxie and sandbox/AV
  injected-module names. `M3d` tests Administrator membership; the non-admin
  path reaches `M3e`, which uses `Shell.Application.ShellExecute` with `runas`
  to relaunch through cmd.exe. This is a UAC elevation request, not a bypass.
- `M3f` builds hidden PowerShell processes, disables shell execution and waits
  for them: `Add-MpPreference -ExclusionPath '<staging directory>'` and
  `Set-MpPreference -SubmitSamplesConsent 2`. These are defender-setting
  changes, not mere PowerShell names or unrelated imported APIs.
- The entry enumerates its own resources, calls `M40` to read each stream,
  calls `M41` to XOR it with the repeated UTF-8 key, and writes the returned
  bytes with WriteAllBytes. The decoded `.exe` resource is renamed to a
  generated executable under a generated `C:\Users\Public\` subdirectory.
  The directory receives attribute mask 6 (hidden/system).
- That resulting executable path is passed to `M43`, which opens writable
  HKLM `Software\Microsoft\Windows\CurrentVersion\Run` and stores a quoted
  path, and to `M42`, which launches it. The hidden-process properties in
  `M3f` belong to the PowerShell setup; their existence does not prove that
  `M42` launches the resource payload hidden.
- `M45` obtains this assembly's location and passes it to a hidden cmd.exe
  command using `choice /t 2 ... & del "<original path>"`.

The repeating-key decoder recovers `stub.exe` (203264 bytes), `addrs.dat`
(759789 bytes of wallet addresses) and `wlist.dat` (15162-byte BIP39 word list).
`results.json` records their hashes. The decoded stub is another ConfuserEx
managed assembly, entry MethodDef `0x0600007b`, with 133 methods. Its constant
initialization produces a 7140-byte table and 359 resolved string uses.

The stub's entry installs a certificate-validation callback, starts scanning
workers, and repeatedly obtains clipboard text through `M41` (native
OpenClipboard/GetClipboardData with CF_UNICODETEXT), normalizes seed phrases,
and recognizes WIF/private-key and extended-private-key formats. Its reporting
path builds SEED/FILE records; `M48` RSA-encrypts secret data, `M4b` dispatches
reports across the configured endpoint pool, and `M4a` URL-encodes the `dset`
body and writes it to a POST request stream. The endpoint pool contains many
unrelated sites' `/c.php` URLs. `M5e` implements screen capture; other workers
search documents, wallet locations and browser extension stores. `M6b` also
contains browser termination and recursive deletion paths. These capabilities
are present in code; no successful upload, deletion or victim deployment is
asserted.

This is concrete wallet-secret theft with stealth installation, persistence and
security-setting changes, consistent with its malware-corpus collection.
No legitimate application's purpose or authorized deployment explains that
combination. The supplied external sample pages could not be opened here;
family attribution is consistent with the supplied provenance, while the
malicious verdict rests on the recovered code.

**Coverage limitation:** YAML currently cannot query these custom ConfuserEx
constants or recursively recover the XOR-managed resources. Both the original
and independently scanned stub therefore lack direct hostile detections for
Defender changes, Run-key persistence, self-deletion, secret exfiltration and
other recovered operations. Tested the existing resource/process predicates,
inspected their IL call sites, decoded both constant tables and resources, and
added a compiler-pattern-independent-of-names cyclic XOR expression matcher.
The parent gains a suspicious zero-width resource/XOR writer profile and a
notable XOR operation. The decoded stub remains 0H/3S. General API co-occurrence
or the collector filename cannot safely supply the missing hostile admission.
The 3–5-hostile-trait goal is unmet for this sample; the extraction/data-flow
limitation is explicit rather than compensated for with inflated rules.

## Mach-O: self-keyed Foxveil loader

The universal image contains x86_64 and arm64 executables. Its ad-hoc signature
has verified code-page/special-slot integrity but no authenticated developer
identity. The x64 initializer at `0x10006a918` calls environment and API probes,
reads its own `__TEXT,__text` through resolved Mach-O APIs, and hashes it.
The derived password uses an environment-dependent word plus 32 bytes masked
with that hash. The elapsed-time check at `0x10006ac69` changes the word after
roughly 50 ms. `0x100071c7b` derives a 32-byte PBKDF2-HMAC-SHA256 key using a
36-byte password, 32-byte salt and 104599 iterations.

The following 32- and 36-byte input-buffer wipes are unconditional after the
KDF. They do not describe a slow-path wipe of the derived key. That finding was
renamed; the wipe operation was moved to `micro-behaviors/mem/fill`, retaining
its byte matcher and notable criticality.

The loader uses a transformed Base64 alphabet, per-chunk HKDF nonces and
AES-256-GCM tags. Independent decoding authenticated all 83 main-stage chunks
and recovered a 265498-byte run-only AppleScript (`recovered-foxveil.scpt`,
SHA-256 in results.json). The initializer also builds and runs a separate
short decoy, and the recovered main stage is handed to the OSA runtime.
API-entry detour checks and environment checks obstruct inspection; no final
host execution was needed to establish the payload.

`osadecompile` refused the run-only script. A separately fetched open-source
AppleScript decompiler plus explicit arithmetic/string decoding recovered the
relevant handlers. The script's password routine impersonates System
Preferences, uses a hidden-answer dialog and verifies input with `dscl .
authonly`; it also queries browser Safe Storage secrets. File collection
includes Chromium/Firefox login/cookie stores, login.keychain-db, Notes,
wallets and password-manager data. Archive/upload handlers use ditto and curl
multipart POSTs. Other handlers construct RunAtLoad/KeepAlive launchd plists,
password-fed sudo commands and download/replacement paths for wallet apps.
These paths substantiate its collection as a stealer rather than a protected
ordinary utility. Remote service availability and successful persistence are
not established.

All nine original hostile findings and both suspicious findings survive.
The recovered stage is separately tested: **1H/2S → 1H/5S**. New coverage records
concealed password/Keychain querying, Keychain copy/archive/upload references,
and launchd/sudo/password-dialog co-occurrence. The engine does not recover the
System Preferences title or bind the runtime paths/results across those
handlers. Consequently these new profiles are suspicious, not hostile
phishing/exfiltration/persistence claims. The outer Mach-O does not automatically
inherit findings from the manually decrypted stage. That remains an extraction
limitation, not grounds to duplicate its existing hostile loader detections.

The decompiler source and its forager provenance remain in the review scratch
directory. It was used as a static parser, never as a script runtime.

## HTML: disclosed example-domain installation demo

The full 1037-byte page is byte-identical to the repository's prior
`platform-clipboard-review/platform-loader.html` fixture. A Download button
selects one of two plain commands with a user-agent test, writes that command
to the clipboard after the click, and reveals Terminal or Win+R paste/run
instructions. The macOS branch is curl-to-zsh; the other branch is remote
MSHTA. There is no obfuscation, fake human verification, stolen data, concealed
clipboard substitution, persistent action, or recovered downstream payload.
The example.net URLs and demonstration provenance corroborate the benign
interpretation, but domain spelling is not an exception or verdict gate.
The equivalent `.invalid` fixture is corrected as well.

Honest command-copying installation interfaces are a benign explanation for
all observed behavior. The dangerous dual-use command forms remain notable.
The four prior hostile rules now require a human-verification pretext, and
four neutral clipboard/instruction profiles preserve their original evidence.
The same page with that pretext still triggers all four hostile findings.
Real ClickFix controls retain their pre-existing hostile/suspicious coverage.

## Rule corrections, consumers and tests

- The PE resource/hidden-launch matcher did not require ConfuserEx or bind
  resource bytes → file → hidden process. It is retained as a notable managed
  resource/write/hidden-launch API profile, outside C2/backdoor/download.
- The unsigned source-named hidden-process matcher established API references,
  not a dropped payload's data flow or malicious intent. Its exact observation
  remains notable under hidden process configuration. The source-extension
  discrepancy moved to metadata, keeping suspicious criticality.
- The two repeated Unicode-format-byte populations did not locate identifiers
  or prove anti-decompilation. Their matchers and suspicious levels are
  unchanged under metadata token-population. Exact consumers were rewritten;
  there were no broader ancestor-directory selectors requiring expansion.
- The timing/input-wipe rename retains its hostile timer-corruption evidence;
  only the unsupported conditional-wipe claim and neutral atom placement change.
- No endpoint, generated filename, hash, encrypted campaign constant or sample
  size gates a new hostile detection.

`results.json` compares all original files, decoded units and independent
controls after canonical ID moves. There are no lost observations on either
binary. The two PE findings intentionally become notable; four HTML hostile
findings intentionally stop firing. Their neutral observations remain. No
pre-existing H/S finding is lost on the independent positive controls,
including real ClickFix, a managed loader, and another compiled wallet stealer.
Ordinary .NET loader, Keychain query, report upload, notification, host-profile
and encoded-script controls acquire none of the new suspicious stage profiles.
The existing 12-case suite and new 10-case suite pass.

Reproduction artifacts, original/after atomscan JSON, cleave facts, IL dumps,
decoder scripts, Ghidra output and decompiler provenance are under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-71cf-540d-f603`.
The recorded final repository check is `make validate`.
