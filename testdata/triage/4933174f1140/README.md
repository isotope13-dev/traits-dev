# BeeNetProtect credential-stealer loader review

Verdict: **MALICIOUS**. The unsigned native wrapper claims `File Utility`,
`Community Tools`, version `2.15.4209.87`. Its recovered native C++ payload
collects credentials and other private application data, serializes it, and
prepares it for a remote HTTP channel. This behavior and its evasive loader
outweigh the generic utility metadata. The external fake-torrent/LimeTorrents
label is provenance; no torrent-lure UI or particular download circumstances
were established from this executable. No specific malware-family attribution
is needed for the judgment.

Original SHA-256:
`4933174f1140b15dc7789e0dc207830465d450c586e48ab6a931131eb2a6c1bf`.
Recovered PE SHA-256:
`8dde632a363c563929045e50d400ba03331b250b74ca04474259478eea389667`.
Neither PE has an Authenticode signature. Neither contains an archive recognized
by Cleave; the inner PE is an encrypted stage, not a scanned archive member.

## Execution evidence

Addresses below are RVAs; both images prefer base `0x140000000`. Analysis used
Rizin, Capstone, PE parsing, signature verification, and bounded Unicorn
emulation of pure decoding/hash routines. No payload entry point or Windows
API was executed in emulation.

- Wrapper entry `0x8b30` jumps to `0x2800`. Bootstrap routines `0x44f0` and
  `0x4c00` resolve APIs by walking loaded modules and PE exports. The name hash
  starts at `0x811cb5fb`; each byte is XORed, multiplied by `0x01000193`, then
  folded with `h ^= h >> 16`. API hashes were verified against the actual native
  hash routine, not inferred from labels.
- Routine `0x5620` gets its own executable path, opens it for reading, and reads
  the final 64 bytes. Its footer tag `0x24f671b3` equals FNV-1a over the 32-byte
  mask at RVA `0xe000`. Unmasking footer sizes yields a 1,313,280-byte PE,
  220 padding bytes, and enabled flags `0x03` (debugger and VM gates).
- The footer's first 32 bytes XOR the mask to produce a ChaCha key; bytes
  32..43 contain its nonce. `0x1330` decrypts in place. Its state has the
  standard ChaCha sigma; the indexed rounds in `0x8d60` implement the column
  and diagonal calls. Recovering the PE by executing only this decoder succeeds.
- The debugger path at `0x2d75` reads PEB BeingDebugged; additional dynamically
  resolved checks include `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`,
  and `NtQueryInformationProcess` with debug-port class 7. Positive checks wipe
  the stage buffer and return. The VM gate `0x5040` calls file/driver probes
  (`0x16e0`), process probes (`0x1a80`), and other environment probes. Targets
  include VirtualBox, VMware, QEMU, Parallels, and Xen agents and guest drivers.
  The catalog is concealed with XOR `0x5c`.
- `0x6150` maps the decrypted PE, resolves imports and relocations, applies
  section protections, and handles runtime initialization. `0x303b` extracts
  SizeOfImage and AddressOfEntryPoint. `0x3179` substitutes PEB ImageBaseAddress;
  `0x31e9` adds the saved entry RVA to the mapped base and calls it.
- `0x32b6` checks the native `4c 8b d1 b8` prologue and extracts its SSN.
  Neighbor-stub recovery exists at `0x3cf0`. `0x4c00` maps a fresh ntdll image
  and searches native code for `syscall; ret`. `0x7e60` builds callable
  `push rcx; pop r10; push SSN; pop rax; jmp [rip+0]` trampolines. The
  targets include native allocation, protection, free, and delay operations.
- The main path passes the mapped base, image length and NT headers to `0x67b0`.
  It derives a 16-byte key, changes protection, XOR-masks the image, performs
  an indirect relative delay, XOR-restores it, clears the key, and restores
  section protections. These are explicit code paths, not sandbox-only claims.

## Recovered stage

The stage has 1,357 candidate stack-literal builders. Bounded emulation
recovered 1,356; the remaining candidate is the shared decoder itself, not a
failed literal. Its AES-CTR-style routine at `0xac130` also conceals API
pointers between calls. Export resolution at `0x7de60` hashes names through
`0xe9a40`; evaluating that hash over candidate Windows API names confirmed
WinHTTP, Credential Manager, DPAPI, and process-memory API identities.

- Entry `0xec960` reaches WinMain `0x2ec10`, which initializes the collector and
  calls dispatcher `0x47c0`. That dispatcher invokes browser, wallet, Telegram,
  Discord, Credential Manager, remote-access, email, Steam, clipboard, SSH,
  note, OBS, file-grabber and seed-scanning routines.
- The browser routine consumes a clear five-browser profile pointer array.
  Downstream routines access `Local State`, `Network\\Cookies`, `Login Data`,
  `Login Data For Account`, and Firefox credential databases. Application-bound
  and DPAPI key-handling paths are present; successful recovery on a victim
  machine was not tested.
- Wallet and SSH routines consume decoded wallet directories and private-key
  patterns. Credential Manager collection writes a `CredentialManager.txt`
  result. These targets are supported by their callers, not strings alone.
- Module results reach `0x3780`, which queues worker `0x41d0`. The worker
  encodes and encrypts the result and appends it to an outbound buffer;
  request routine `0x2e310` uses the resolved WinHTTP client, POST/GET selection,
  request headers, request-body pointer, send, receive and response paths.
- Endpoint construction at `0x3a10` defaults to
  `beenetprotect.com/lgz/gdata`. The program also references a YouTube channel
  and a GitHub gist for configuration discovery. Forager fetched the decoded
  gist URL; it returned HTTP 404. The endpoint's live availability, deployment
  configuration overrides, and successful exfiltration were not established.

## Rule corrections and preservation

1. The match at original file offset `0x8887` is an IMUL in opaque arithmetic,
   not an XXTEA round. Both original constant matchers were moved unchanged to
   `metadata/binary/instruction/operand`. Real TEA-family round/name matchers
   remain. The redundant constant-only union was retired; its observations
   remain in the two atoms. The two zlib consumers retain their full byte and
   scope predicates under accurate names/homes. Multiplier plus zlib alone is
   now notable co-occurrence; ROR14 export concealment remains suspicious. No
   cipher or payload handoff was required by either old consumer, so their
   former loader claims and hostile criticality were unsupported.
2. Encoded `advapi32.dll` is not an import (the PE imports only USER32, GDI32,
   OLE32 and SHELL32). Its observation was retained in the canonical module-name
   reference, using case-insensitive substring matching to preserve the old
   concatenated/decoded-string coverage. No import or module behavior is erased.
   Go's does-nothing Windows fixtures retain this standard-runtime reference
   at baseline using parsed Go build metadata (a narrower trigger than the
   Go recognizer excluded by the old import rule);
   the observation is still emitted, and this native sample remains notable.
3. A `VBoxTray` name does not prove a VM check. It now shares the neutral guest
   tray-name rule with the equivalent VMware tray observation. The old
   VMware-name match and all VBoxService-specific rules remain covered;
   exact consumers were audited and updated. Name-reference and actual
   anti-analysis/concealment findings are separate.
4. The x86 PEB-byte branch rule was generalized to accept the x64 spelling;
   its original x86 alternative remains byte-for-byte, with its consumer test
   updated to the canonical ID. Other x86 PEB/debug-heap rules are unchanged.

Exact IDs and ancestor selectors were audited before migration. Available PE
fixtures and other samples were checked for the inverse-golden-ratio patterns;
only this sample matched. No original positive fixture for the two old
constant/zlib combinations was available. Their predicates were retained,
rather than deleting the technique on a synthetic near miss. Focused controls
also retain the actual TEA-round and original x86-debugger observations.

Four old firing IDs disappear: XXTEA delta, ADVAPI32 import, VBoxTray check,
and VMware tray name. Every supported underlying observation is retained under
an accurate ID. **No material attack coverage was lost.**

## Results and limits

| Artifact | Hostile before → after | Suspicious before → after | Classifier probability / admission level |
|---|---:|---:|---|
| Original wrapper | 0 → 4 | 0 → 3 | 0.9187257 / -1 → 0.99 / 25 |
| Recovered native stage | 1 → 1 | 1 → 1 | 0.87457335 / -1 → unchanged |

The wrapper's four hostile traits cover concealed gated image activation,
indirect-syscall bypass, PEB image-base substitution, and image masking during
waits. Three suspicious traits cover debugger gating, API-name concealment,
and the XOR-concealed guest-agent catalog. Accurate existing structural and
capability findings are retained.

Classifier disagreement remains: the native stage stays outside the calibrated
admission grid even though its browser-collection rule is hostile; model-route
`cls` fields are still 0. The wrapper now reaches admission through the richer
traits and hostile-rule gate. The shipped model warns that it uses feature
specification v18 rather than v21.

The inner stage has only one hostile trait. Wallet, SSH, Credential Manager,
and outbound data-flow analysis was attempted through literal recovery, hash
resolution and caller tracing. Separate generalizable detections would require
native decoded-value/call-flow facts that the current matcher does not expose.
Hardcoding ciphertexts, the endpoint, or generic cryptography would not prove
those claims. This remains a specific coverage gap, despite the four wrapper
behaviors. No persistence, elevation, remote injection, or particular victim
circumstances were invented.

`check.py` has 14 focused controls: original/rename, each meaningful hostile
operation removed separately, a variable hash mask, a harmless constant and
DLL-name PE, retained x86 debugger detection and its near miss, a TEA round,
and the recovered collection stage. Results are in `controls.json`. Final
`make validate` results are recorded in the task output.

Artifacts and full before/after reports remain under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-d75a9cc3/scratch/4933174f-analysis/`.
