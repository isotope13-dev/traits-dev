Reasoned static review, 2026-10-19

Each original was scanned with atomscan and inspected with cleave facts.
Native execution paths were disassembled with Rizin; managed method bodies,
tokens and user strings were recovered with dnfile/dncil. No sample was run.
The judgments below follow the code, independently of the supplied reputation.

| SHA-256 prefix | Identification | Judgment | Concrete evidence |
|---|---|---|---|
| 6cb9370ba1f8 | StormAttack service-DLL loader, damaged resource image | MALICIOUS | Active Setup self-installation, service-DLL hijack code, remote DLL injection and shell cleanup |
| 4cf8b9e722b5 | Self-named NanoCoreUltimate surveillance/ransom implant | MALICIOUS | Keyboard and clipboard recording, browser/wallet reads, input lockout, security-control interference, persistence |
| d19fae884fe7 | ARM Mirai-derived propagation and DDoS bot | MALICIOUS | Remote login/shell propagation, payload staging, attacker task dispatch and repeated packet emission |

StormAttack:

- CRT entry 0x402674 calls 0x401cb0. The configured mode is 3, selecting
  0x401900 and the cleanup routine at 0x401390.
- 0x401900 detours through .htext, calls the GUID helper, traverses
  canceling XOR instructions and self-exchanges, and rejoins 0x40190f.
  This is executable padding; there is no encrypted payload to recover there.
- 0x401a26 creates an HKLM Active Setup component. 0x401a4b writes its
  StubPath. The subsequent CRT file I/O copies and patches the current image,
  and 0x401b7e launches that copy. Cleanup constructs a COMSPEC deletion.
- Separate code opens LanmanServer Parameters and prepares a replacement
  ServiceDLL; 0x401150 resolves LoadLibraryA, writes the DLL path into a
  suspended child and uses CreateRemoteThread. These are preserved attack
  implementations, not merely import names.
- The .rsrc region is all zero, so resource 101 cannot supply a usable DLL.
  Resource extraction failure prevents the corresponding drop branch.
  Existing traits correctly describe code/API profiles, not successful
  payload installation or observed DDoS. No detection change was needed.

NanoCoreUltimate:

- The CLR entry token is 0x06000085 (Main). It schedules the recording and
  impact routines and directly invokes persistence and control interference.
- StartKeylogger installs a global hook; HookCallback buffers keys, time and
  active-window titles. Its separate polling worker tests the high bit of
  GetAsyncKeyState over keys 1..255 and appends to the same record buffer.
- ClipboardMonitor reads Unicode clipboard contents; ContinuousScreenshot
  captures and saves the screen. RecoverBrowserPasswords reads Chrome/Edge
  Login Data and Firefox profile logins.json; StealBitcoinWallets reads
  wallet files. HighLevelFileStealer and ConstantDataScraping enumerate and
  read personal files. These data flow into SendToC2.
- SendToC2 first appends records to local files. IsPlaceholder is patched to
  always return true, and ParseC2Url clears the domain, so this specimen's
  network upload paths are disabled. Collection remains real; no successful
  exfiltration is claimed.
- RealEncryption traverses a Desktop TestFolder, attempts an AES transform,
  writes a suffixed output, then deletes the original. The configured key is
  15 bytes and IV 14 bytes; set_Key fails before transformation/replacement.
  The existing ransomware trait accurately says “attempt”.
- The remaining code blocks input, deletes recovery settings/shadow copies,
  disables services and firewall, appends security-domain hosts redirects,
  writes Run keys/tasks, hijacks IFEO and fodhelper, and creates an admin
  account. Incomplete encryption and disabled C2 do not make these actions
  benign. The self-assigned name does not authenticate a NanoCore lineage.
- Added Firefox store/read coverage, explicitly a co-occurrence profile with
  independent recording evidence. The filename atom now includes Windows
  managed binaries; its matcher is unchanged and its unsupported acquisition
  mappings were removed.

ARM bot:

- Main at 0x11ca0 initializes configuration, daemonizes, starts the scanner,
  registers attack handlers at 0x85e8, and enters a received-task loop.
  0x10eb8 routes attack requests to 0x82cc and then the handler dispatch at
  0x81d0. A forked watchdog terminates the attack after its requested duration.
- The UDP handler beginning at 0x8abc constructs IP/UDP packets, varies
  addresses/ports/payloads, calculates checksums, and repeatedly calls sendto.
  The loop at 0x91a8..0x91cc supplies the packet, target sockaddr and length
  16, increments the target index and branches back into the construction
  sweep. The new neutral atom matches that call layout with relocations
  wildcarded; hostile flooding additionally requires worm propagation.
- 0x1402c handles remote login and router shell states, including shell
  negotiation and BusyBox download/chmod/execute commands. The socket sends
  carry the commands; these are not just unused strings in libc.
- 0x16398 allocates indexed string entries and transforms them with an RC4
  KSA/PRGA and an embedded 256-byte key at VA 0x25465. Reproducing its
  XOR-swap implementation recovers the configured eight-byte names
  bigr.dyn/lkol.dyn, “The Peoples Bank of China.” and
  “TSource Engine Query”. No endpoint liveness is inferred.
- cleave also decodes the escaped shell fragments selecting deleted procfs
  executable links and issuing kill -9. Static procfs/network inspection and
  propagation findings are consistent with the corresponding code paths.

Placement and validation:

- Moved five direct socket-operation atoms to connect/listen/send/receive;
  kept their byte matchers, architecture/format gates and exclusions.
- Moved router shell-launch text into shell creation and the download-to-sh
  pipe into the pipeline leaf. Neither is in-process interpreter evaluation.
- Moved an encoded connection-status banner to socket diagnostics and
  commented installer instructions to UI help. These corrections also keep
  connect and pipeline within their existing 100-rule budgets.
- Updated exact consumers and existing fixture mappings. The only interpreter
  ancestor consumer is Windows-only PowerShell Empire, disjoint from the
  Linux-only router atoms. Shared socket/process ancestors remain applicable;
  no syscall-directory selector consumes the relocated individual atoms.
- Connection-directory consumers require connection capability; they should
  no longer accept a banner alone. Execution-directory consumers should no
  longer accept commented installation instructions alone. Those ancestor
  membership corrections are intentional; exact banner/help consumers retain
  the same observations through their updated IDs.
- Before/after sample comparison, normalizing relocated IDs: no prior
  finding disappeared. The only additions are the Firefox filename/read
  profile and the ARM packet-loop/flood profile. Hostile counts are 4, 24, 4.
- New inert positive/near-miss controls cover every moved matcher, the new
  packet loop, a benign packet generator and a store filename without
  surveillance. The help matcher is checked with test-rules before report
  filtering, since the normal JSON report omits that documentation finding.
- Four private sample mutations remove Firefox store/read/record evidence or
  the ARM packet loop; the respective new hostile finding disappears in each.
  New hostile precision scores are 7.8 (Firefox) and 9.5 (packet flood).
- Run the portable controls with:
  python3 testdata/taxonomy/native-managed-first-review/check.py --output DIR
  The existing native-byte-evidence-review checker covers 21 additional cases.
