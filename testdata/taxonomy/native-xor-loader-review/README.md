# Native loader first reasoned review

Three samples were examined using atomscan JSON, complete `cleave facts`,
Rizin/Capstone disassembly, Ghidra decompilation, and dnfile/dncil token-resolved
CIL. No sample was launched on Windows. Referenced Triage reports were
inaccessible; no verdict relies on their scores or the collector filenames.

* `258421dfe7b8`: MALICIOUS, StormAttack installer. `0x401cb0` dispatches on
  configuration byte `0x404120` (value 3 here): the selected branch writes
  an Active Setup StubPath, saves a patched self-copy, launches it, and runs
  COMSPEC self-deletion. Alternative branches drop resource DLL 101 and overwrite
  LanmanServer's ServiceDLL. `0x401163` creates a process, allocates/writes its
  DLL path remotely, resolves LoadLibraryA, and starts it with CreateRemoteThread.
  `.htext` trampolines contain long self-exchange, self-move and push/pop filler.
  The embedded DLL has no executable section, no recoverable imports, and a
  zero-filled entry point. Installer code establishes hostile intent; do not
  claim that the DLL loads successfully or performs a working DDoS attack.
  The four existing hostile installer/family findings are retained.
* `191e88f18679`: MALICIOUS, concealed native shellcode downloader. `0x401000`
  decodes configuration with `byte XOR (index - 0x40)`. The resulting UTF-16
  host is `johnhop77.ddns.net` and path `/wp-content/themes/mixed/splice.png`.
  `0x4014b0` tries a neighboring Word-style temporary file, then retries HTTP
  retrieval every five seconds. `0x401160` checks HTTP 200/content length and
  reads the response into the same context's buffer/length fields. `0x4010f0`
  searches all 256 XOR keys against header bytes EB 02 ?? F1 and decodes that
  buffer. `0x401070` allocates RWX memory, copies the decoded buffer and calls
  the saved allocation pointer. CPU-only Unicorn emulation of the entry stub
  also reaches decrypted appended code at `0x412f16`, before any OS API runs;
  it walks the PEB, resolves exports and creates shared mappings/worker code.
  No endpoint was contacted. Family attribution and successful execution of a
  subsequently downloaded payload remain unproven.
* `3c85f8c8ea85`: MALICIOUS, self-named NanoCoreUltimate spyware/worm and ransom
  locker. `Main` directly installs persistence, input blocking, shadow deletion,
  IFEO redirection and fodhelper hijacking. HookCallback and the polling thread
  append real keys; FlushKeylog base64-encodes those keys and passes them to
  SendToC2, which calls WebClient.UploadString with its original input argument.
  Clipboard and screenshots follow the same send path. USBWorm copies its own
  executable and writes an executable AutoRun open directive. ReadBrowserData
  copies Chrome Login Data and other browser databases. Encryption only targets
  Desktop/TestFolder and sets a 14-byte AES IV, throwing before output/deletion;
  the existing attempted-replacement description correctly preserves that limit.
  Numerous family names/mutexes are self-assigned and do not establish Remcos,
  WannaCry, RedLine or other family identities. Wallpaper classification now
  describes its static evidence and drops the unsupported encryption mapping.

## Trait corrections and placement

The two hostile `unsigned-*reloc*wininet*` composites required only API and
layout co-occurrence. They did not require a downloaded payload, XOR decoding,
code mapping or execution. Their unchanged match conditions now live under
`micro-behaviors/communications/http/client/wininet` as notable API/layout
profiles. The adjacent registry/TEMP/IP profile also moves to registry/write
as a notable capability profile, without unsupported ATT&CK mappings. Exact-ID
consumers were searched repository-wide; none referenced those three old IDs.
Ancestor objective selectors intentionally lose these neutral observations.

`word-temp-staging-file` is renamed `word-style-temp-filename`, described as a
reference and made notable: Word-style filenames establish no evasion or staging.
Its WinInet API-profile consumer is updated. New byte-decoder observations live
under data/decode/xor; the copied-buffer execution observation lives under
process/deploy. Their XOR-loader conjunction is suspicious: static code shapes
establish concealment and raw execution without establishing a hostile purpose
in every possible program. The reviewed downloader retains two suspicious
findings and receives no blanket exception.

Run `python3 testdata/taxonomy/native-xor-loader-review/check.py`. Controls have
an immediate-return entry and unreachable synthetic snippets, with no downloaded
or embedded malware. They distinguish decoder-only, execution-only, changed-XOR,
wrong-saved-pointer, and plain API/layout cases. API-only controls retain notable
observations without either retired hostile profile or the new loader finding.
