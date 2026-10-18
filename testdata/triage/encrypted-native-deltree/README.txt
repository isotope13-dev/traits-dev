Native encrypted payload and DELTREE review
=========================================

Verdicts (external labels were leads, not behavioral evidence)

* d64921058e03: MALICIOUS, AMOS-style macOS credential/wallet stealer.
  This universal Mach-O has a fr.jetbrains.daemon ad-hoc signing identifier;
  that identifier is a claim, not JetBrains attribution. Its meaningful code
  runs in the constructor at x64 0x100054c53. The apparent main dispatches to
  arithmetic filler. The constructor authenticates/decrypts five chunks of a
  220-byte compiled AppleScript probe, then prepares the main script key.
  The latter depends on the SHA-256 of its own __TEXT,__text, environment
  probes, and a timer: exceeding 50 ms XOR-corrupts the first password word
  before PBKDF2-HMAC-SHA256 (36-byte password, 32-byte salt, 105129 iterations).
  Per-chunk HKDF-derived nonces and AES-256-GCM protect the script chunks.
  CPU-only Unicorn execution, emulated allocation/copy APIs, normalized
  anti-analysis probes, and the original code-section digest recovered an
  authenticated 263554-byte run-only AppleScript. SHA-256:
  40d130828752a561800761547e684e5b1b2d2b0f9f2c6e25ade15033fbae21b8
  No AppleScript was executed. osadecompile refused its run-only source.
  https://github.com/n0kovo/applescript-decompiler recovered its handlers;
  arithmetic folding recovered 1741 constant calls (including a parent-scope
  decoder alias). The decompiler omits some discarded-result AppleEvents, so
  its output is not a lossless source reconstruction. Handler bytecode and
  decoded operands establish browser Cookies/Login Data and Firefox logins
  copying, login.keychain-db acquisition, wallet/password-manager staging,
  and deceptive password collection checked with 'dscl . authonly'. Upload
  handlers construct multipart curl requests carrying staged archives.
  Other handlers prepare launchd persistence and replacement wallet apps.
  These independently establish malicious intent; ciphertext entropy and the
  external AMOS label did not establish the verdict. Native traits describe
  the visible concealment rather than pretending plaintext strings exist.

* ebcd7966a665: MALICIOUS, concealed Windows DLL loader/host profiler.
  The outer file claims Spetuskaz GmbH, version 10.5.2.11956. Native execution
  from 0x140014c10 through 0x140012216 reaches custom character decoding,
  permutation, and header reconstruction. At 0x1400110eb/0x1400110f0 it writes
  the PE marker byte and MZ word into a decoded buffer. The original markers
  were absent from the embedded representation. It constructs a memory image,
  copies .text and other sections, and resolves DLL imports. CPU-only Unicorn
  emulation recovered the mapped image; conversion by section RVA to raw
  offsets produces a parseable x64 DLL (analysis-restored DOS/NT magic):
  SHA-256 13381311923fd232cf44773d95532d1f7a0d388ffbb8f236dcb55b9e330ff5ec
  The recovered DLL's entry starts a worker at 0x1800656a3. Its path queries
  firmware, memory, display devices, OS, uninstall registry locations, volume,
  computer/user names, locale and system information. Decoded references
  include ConnectixCPU. It resolves bcrypt and WinHTTP dynamically and sends
  an opaque 181-byte request body with POST / to dexflow.pics, falling back to
  dexgrow.quest. WinHttpSendRequest is reached at 0x18002a578 and WriteData at
  0x18002aed9. APIs were mocked; there were no actual network requests or
  native process/thread launches. The inner request encoding was not fully
  decoded, and no browser password extraction was established. The warranted
  identification is a concealed loader/profiler, not a confirmed Warden/Yap
  stealer. Accurate suspicious concealment traits are retained separately
  from the MALICIOUS verdict. A lowercase vendor-directory filename alone
  does not establish masquerading and was moved to a notable path trait.

* 01edfe672f0b: MALICIOUS, DeltreeY destructive DOS/Windows batch command.
  All 14 bytes are 'deltree/y \*.*'.
  On a legacy system providing DELTREE, /Y suppresses confirmation and the
  rooted wildcard selects every file and directory on the current drive;
  DELTREE removes selected trees recursively, including their contents.
  No obfuscation, dependencies, URLs or additional payload are present.
  The .j collector extension makes the scanner classify it as text. Broadened
  command coverage therefore includes text without depending on the filename.
  Root deletion belongs under destroy/filesystem, not secure disk wipe.
  There is one hostile destruction claim and a suspicious root-target claim:
  a second unrelated hostile behavior was not invented to increase counts.

Rule placement and preservation

- Move the generic DELTREE absolute-path operation from fs/delete/file/command
  to fs/delete/directory and update its three objective consumers. Matching text
  is additionally admitted. Both operation and root-intent matching are line anchored;
  warning prose is not a root deletion request. Confirmation suppression is
  an ordinary notable deletion option in the capability directory.
- Move TLS relative-table dispatch from syntax to control-flow/dispatch;
  both exact consumers are updated. No broad syntax selector consumed it.
  Register-equivalent forms now match the reviewed PE. The masked-state
  observation belongs to the same dispatcher subject, not a language bucket.
- Extend native crypto/timer patterns for verified x64 and ARM64 instruction
  layouts. AES-GCM's ABI, PBKDF2 password/salt roles and the timer-corruption
  operation are required, rather than generic crypto or timing constants.
- A reconstruction composite requires both signature writing and concealed
  TLS dispatch; signature bytes in data do not establish a loader.
- New destroy/filesystem boundary: destruction across root contents, versus
  selected-file/tree deletion and neutral filesystem operations. Placement
  was checked separately by affected resource and by required result; both
  select filesystem destruction. This is not a command-language partition.

Focused inert controls

  python3 testdata/triage/encrypted-native-deltree/verify.py <scratch-directory>

Controls cover untyped/renamed root commands, CRLF, quoted warning prose,
selected application trees, four versus five dispatcher observations, and
signature bytes in a data section. Generated executable-shaped byte fixtures
are parsed/scanned only, never executed. The samples themselves were scanned
before and after edits with atomscan; raw matchable and decoded data were
inspected with cleave facts. Both native payloads were traced beyond strings.

All nine focused controls passed, including the two ARM64 controls after
correcting their synthetic segment/file sizes. Final gate: make validate.
