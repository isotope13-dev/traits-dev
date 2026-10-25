# Three Windows samples reviewed on 2026-10-25

The submitted files were scanned with `atomscan --no-update --analyze local
--mode slow --follow=none -f json` and `cleave facts`. No sample was executed.
Analysis used PE/CLR resource parsing, dnfile/dncil IL disassembly, Go pclntab
recovery and annotated x86-64 disassembly, AutoIt EA06 extraction, offline
cryptographic decoding, UPX decompression and rizin inspection.

## Verdicts and execution evidence

**b3aca6ae4a5c — BENIGN: FTPie CORE/Bergelmir key generator.**
Go 1.25.0, module `core-keygen`, with reconstructed UPX sections and imports.
The recovered pclntab is at file offset `0x1e5400`; its 3,312 function entries
identify 11 `main.*` helpers. `main.main` at `0x140104940` prints the CORE
keymaker banner and FTPie target, reads an email from stdin, generates a
P-256 ECDSA key, marshals the public key, creates a license XML document and
signs its SHA-512 digest with `ecdsa.SignASN1`. `main.pageTemplate` at
`0x1401043a0` Base64-decodes and gunzips a 24,576-byte LiteDB template, not
executable code. `main.buildBSON` and `main.buildDataPage` construct the
license record. The final program-specific side effects are `os.MkdirAll`,
`os.WriteFile` to `%LOCALAPPDATA%\FTPie-Data\user.db`, and `os.Remove` of
`user-log.db`. The success message explicitly asks the user to restart FTPie.

Every program-specific helper and the runtime entry were inspected. Network,
registry and process API names are statically linked Go library/runtime code;
there is no program-specific download, remote-control or credential-theft
path. The build metadata declares no external modules. Forager fetched the
runtime reference `https://go.dev/issue/66821`; it redirects to the ordinary
Go crypto/rand issue about failing closed on randomness errors. It is not a
payload location. Its content and `.forage.json` provenance remain in scratch.

The security verdict is benign license-cracking/riskware, without asserting
that its use is authorized or its publisher is trustworthy. The crack banner,
unsigned image and reconstructed packing layout plausibly explain the
external malware labels; the precise vendors' rationale is unavailable. Added
notable ECDSA key-generation, ASN.1 signing and gzip reader references. All
existing observations, including dual-use capabilities, remain intact.

**27dddf0b8a01 — MALICIOUS: Qulab stealer and clipboard hijacker.**
The outer image is an AutoIt interpreter with an EA06 `SCRIPT` resource, plus
two embedded encrypted helper files. `autoit-ripper` recovers 667,861 bytes of
source. Its startup hook initializes 4,614 hex table entries; a `Chr(Dec(
StringMid(...)))` loop decodes them, and 4,613 assignments populate constants.
This is actual executed decoding, not an inference from string entropy.

The main path moves the image beneath AppData, creates a one-minute scheduled
task, falls back to an HKCU Run value if task creation fails, relaunches itself,
and hides the directory. It opens browser databases with SQLite, selects
password/cookie/card fields, and calls DPAPI on the extracted records. It also
collects Electrum/Jaxx wallets, Telegram/Steam/Discord sessions, FileZilla data
and selected desktop files. It stages reports and an archive, calls a Telegram
`sendDocument` uploader with that archive, and deletes staging files.

The long-running loop reads the clipboard, selects replacement expressions
for multiple coin/payment formats, substitutes configured addresses while
preserving surrounding captures, and calls `ClipPut` on the result. The
replacement function and its callers were traced, including the guard against
empty replacement addresses. It exits when Task Manager is present, and has a
separate task-removal/self-deletion path. No deployment context suggesting
user-authorized backup or payment transformation is present; silent theft and
payment redirection decisively tip the verdict.

The two FileInstall helpers are decrypted with CryptoAPI-compatible RC4 using
MD5 of the ASCII string `"967164250"` **including its quote characters**.
Algorithm ID 26625 is passed through `_CRYPT_DECRYPTFILE`/`_CRYPT_DERIVEKEY`.
The recovered files are SQLite and UPX-packed 7zr; unpacking the latter reveals
7-Zip 19.00's archive CLI. These dependencies implement database access and
archive staging, rather than an unseen additional RAT.

**3552f410ec06 — MALICIOUS: Pakes-style .NET wrapper delivering Blackshades.**
CLR entry token `0x06000012`, RVA `0x2208`, installs an AssemblyResolve handler,
then invokes `StartEvents`. The resolver reads embedded DLL resources into
memory and calls `Assembly.Load`. The four first-layer DLLs are independently
analyzed by the scanner and were disassembled during this review:

- `umRrRvm`: copies the current image to Documents under a disguised extension,
  launches a hidden `cmd /C` wildcard rename to `.exe`, writes a VBS helper
  which copies the image into TEMP and registers it in HKCU Run, and deletes
  that helper through `WScript.ScriptFullName` after registration.
- `rKEQFq`: decodes an embedded assembly used to inspect processes/windows and
  check whether the injected host is present. The wrapper uses this result
  to decide whether to launch its payload again, including a timer path.
- `QaCnurm`: reads Base64 resource text, applies the neighbor-dependent byte
  transform, gunzips the native payload, and reflectively invokes the decoded
  injection helper with the payload bytes and a .NET framework host path.
- `yoLkeqC`: downloads an HTTP executable to TEMP, launches it using VB Shell
  (window style **2, minimized focus**, not hidden), and cleans up the file.
  The rule intentionally describes an API/profile observation rather than
  pretending its matcher binds the two path expressions.

The resource transform is:
`b[i] = ((b[i] XOR key[i % key.Length]) - b[(i+1) % n] + 256) % 256`,
performed in place, followed by removal of the last byte. The key is taken
from the shipped string. This recovers the checker, a 15,872-byte injection
assembly, and a gzip stream which expands to the 458,752-byte VB6 Blackshades
server. Its VB project attribution and socket/relay interfaces corroborate
four existing independent family signatures. The PE's native entry at
`0x4013bc` hands control to the VB runtime; individual RAT commands were not
executed in this review.

In the injection DLL, `DataClass.InputData.StartData` at RVA `0x230c` decodes
API names and resolves delegates. CIL offsets `0x1c3..0x1d9` create the host
with CREATE_SUSPENDED; the following code gets thread context, reads the host
image base, calls ZwUnmapViewOfSection, allocates remote memory, copies PE
headers and sections, updates the image-base pointer/thread entry context,
and resumes the thread. Host choices are csc.exe/vbc.exe/cvtres.exe under the
framework directory. The trace establishes payload execution and concealment
without requiring runtime success or a live server. This encrypted RAT launch,
autorun installation and secondary downloader provide decisive malicious
intent; any authorized research context on the receiving machine is unknown.

## Coverage and classifier comparison

H/S below counts finding occurrences over the original and its automatically
analyzed members, without silently treating manually recovered files as
original-file coverage. Full member paths and added/lost IDs are in
`comparison.json`. There were **zero lost findings at any severity** and no
shared matcher was removed, narrowed or demoted.

| Original | Before H/S | After H/S | Atomscan decision before → after |
|---|---:|---:|---|
| FTPie keygen | 0/0 | 0/0 | unflagged → unflagged |
| Qulab AutoIt EXE | 0/1 | 0/1 | unflagged → unflagged (miss) |
| Pakes/Blackshades wrapper + 4 members | 0/0 | 3/2 | unflagged → hostile/flagged |

For the .NET original itself the result is 3/1; `rKEQFq.dll` adds the other
suspicious occurrence, and the other three first-layer DLLs have H/S 0/0.
The new neutral observations still detect decoding, startup registration,
renaming and the secondary downloader in their respective members. FTPie's
three new capability findings are notable. Its two decoded gzip layers remain
H/S 0/0.

The unflagged originals have `lvl=-1`, zero confidence and model route `cls=0`.
Their probabilities were FTPie .91885704 → .91938776 and Qulab .9845775 →
.9845775. Pakes changed from .9847309 / `lvl=-1` to .98 / `lvl=25`, confidence
92, after hostile rules were added. The analyzer reports that model v18.18
uses an older feature specification than the engine; probabilities alone were
never used to establish a verdict.

Separately recovered stages:

| Recovered file | Before H/S | After H/S | Classifier |
|---|---:|---:|---|
| Qulab `script.au3` | 0/0 | 4/2 | unflagged → flagged, .9966546 |
| .NET injection DLL | 0/0 | 1/1 | remains unflagged, .9925485 |
| .NET checker DLL | 0/0 | 0/0 | remains unflagged |
| Native Blackshades server | 5/5 | 5/5 | remains flagged |

**Remaining extraction/classifier gaps:** Cleave does not unpack EA06, so the
four new Qulab hostile rules fire on recovered source but cannot fire through
the encrypted/compressed original resource. Consequently the original's
3–5 hostile coverage goal is unmet: browser/wallet theft and Telegram upload,
clipboard address replacement, task registration and Run fallback remain
hidden from the original static scan. These behaviors were decoded/traced,
and content-based detections were implemented and tested against the recovered
source. A generic AutoIt interpreter fingerprint or a compressed-byte sample
signature would not truthfully close this gap. The .NET neighbor-XOR resources
also need explicit recovery: the newly detected hollowing DLL and existing
Blackshades findings do not automatically propagate through that cipher.
The recovered hollowing DLL's classifier remains a miss despite its correct
hostile rule; no duplicate or inflated rule was added to alter that score.

## Focused verification

`python3 testdata/triage/bad-three-native-20261025/verify.py` passes five inert
source controls. The complete source observation fires four hostile findings.
Removing the decoder fires none; removing clipboard writing retains only the
independent exfiltration finding; removing wallet or Telegram evidence removes
the exfiltration finding while retaining the three clipper/persistence findings.

Additional PE controls in scratch preserve the surrounding sample bytes:
removing VBS self-cleanup or the neighbor-XOR loop removes all three new outer
hostile findings; removing suffix restoration removes only the masquerade
finding and retains payload/persistence coverage. Removing CREATE_SUSPENDED
or the encoded unmap API from the injection helper removes its new hollowing
finding. `controls.json` records the observed findings. A separately compiled
benign Windows Go program signs/verifies local data and round-trips gzip; it
has no hostile or suspicious findings, and the new crypto/gzip observations
remain notable. No sample or generated Windows control was executed.

Raw reports, complete IL/annotated Go disassembly, extracted resources,
decryption scripts, recovered stages, mutation controls and Forager provenance
remain under the task scratch directory `scratch/bad-review`. Verdict markers
were written next to each original sample after checking its SHA-256.
The final repository check is `make validate`; its result is reported with the
completed task.

The existing CEL/Protobuf benign Mach-O fixture contains
`compress/gzip.(*Reader).Reset` at decompressed offset `0x239504`. Its expected
score cap was raised from 16 to 17 for this accurate new notable observation,
which is now required by the fixture. No trait exclusion or severity change
was used to hide the capability.
