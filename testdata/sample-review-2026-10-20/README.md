Reasoned sample review, 2026-10-20
=================================

All three artifacts are **MALICIOUS** on their observed behavior. The supplied
ML and reputation reports were leads, not the basis of these decisions.
`atomscan` and `cleave facts` were run on every supplied artifact; the wheel's
extracted CLI was also examined with facts. Disassembly, static decoding and
inert substituted-response execution supplied the behavioral evidence below.
No live remote payload was executed.

**2c99cba29caa — Floxif-infected 7zSfxMod installer claiming R-Drive Image.**
The entry at VA `0x41942f` jumps to `0x40a4f4`, rather than continuing into the
original CRT. The diverted code uses return-address adjustments to skip junk,
walks the PEB to resolve GetProcAddress, and decodes stack-built API names.
The loader at `0x408b5c` opens its own file, reads five bytes from EOF minus
29, decodes them, and restores the original entry under VirtualProtect at
`0x409874`–`0x4098b7`. This is a parasitic modification, not an installer API
profile. Footer recovery yields offset `16158016`; XOR with `0x3a` followed by
NOT recovers a 69,337-byte UPX-packed PE DLL. Unpacking it produces a DLL
exporting FloodFix/FloodFix2. The host tries several DLL drop/load paths and
falls back to manual image mapping, resolves FloodFix2, and invokes it at
`0x40a4e9`. The signed-image digest no longer matches. The original SFX's
configuration launches unlock/hosts batch files and the R-Drive executable;
that configuration alone does not establish infection or ransomware. No claim
is made for the other malware names in the collector's filename.

**0868f8cc3d68 — injected Elementor Pro runtime with concealed browser loader.**
An Elementor 3.23.0 webpack runtime ends around byte 6,110. Appended code hides
its own source using nonconfigurable empty getters, protects its script from
DOM removal, hooks insertion and HTML-writing paths, and suppresses scripts
and frames matching competing wallet-loader features. Its HTTP guard scans
eth_call, setApprovalForAll and signTypedData bodies for Ethereum addresses,
then aborts/rejects requests excluding its selected address. It also hooks
service-worker registration. The selection predicate is bound to the XHR
abort handler in the revised rule.

Two hex/XOR → Base64 → XOR layers lead to a permuted Base64 chunk array and a
keyed byte decoder. Its Function-constructor sink activates the decoded source.
That source queries Polygon RPC endpoints with eth_call, ABI-decodes a string
from contract `0xfF9E792a3015A79340CDEc1847Ab0AA10560422a`, decrypts its S1 value,
and appends a script at the recovered host plus a configured `/api` route.
This hidden injected execution and selective interference are inconsistent
with the surrounding page-builder runtime. The final remote script was not
retrieved; credential theft, card skimming and wallet transfers are **not**
observed in the supplied bytes. The old input-exfiltration rule required no
input or transfer, so it was retired.

**aeefe595d953 — pyyi 2.5.5 deceptive interpreter and remote Python loader.**
Every wheel RECORD digest/length matches its member. The archive itself claims
cryptographic recipes, but its initializer supplies no advertised primitives.
The actual console entry point is **python3.7**, not python2 as the supplied
external summary says. The CLI prints a real Python banner. `_GateConsole.push`
selects up to five bare-token lines, passes each to `_server_unlock`, and
`api_json` POSTs it as `password` with operation 2. A successful token is stored
locally with hostname-derived MD5/XOR scrambling. Terminal echo is disabled;
unrecognized names can display `0` instead of ordinary interpreter feedback.
An inert replay confirmed the input-to-password path and suppressed display.

Other command arguments lead to operation 3, Base64/gzip decoding, compile,
exec and the returned module's main(argv). An inert substituted payload
confirmed that a payload exception is disguised as a Python missing-file
error. Hosts are XOR-packed, auto-registration sends hostname/OS, and failover
repeats checks against alternate hosts. The baked hosts are two space-z.ai
applications. No returned remote module was obtained, so its further effects
are unknown. The covert input relay and deceptive execution, rather than the
hosting service or an ordinary licensing request, tip the malicious verdict.

Detection changes and verification
----------------------------------

* Replace unsupported hostile overlay/injection profiles with notable PEB and
  image-layout observations. The PE retains the entry-restoration and Floxif
  hostile detections.
* Require source shadowing, DOM hooks, concealed execution and wallet-selective
  abort behavior for the injected-script hostile payload finding; the HTTP
  finding separately describes concealed selective blocking.
* Put neutral source naming and digit-state syntax in metadata. Matchers,
  counts, effective type/platform scope and exclusions are preserved; active
  YAML consumers and two existing fixture manifests follow the moved IDs.
  `id-map.json` records these moves. The digit-heavy line observation is now a
  metadata relationship, not an attacker objective.
* Move the decoder/Function co-occurrence out of C2 and keep it suspicious.
  It does not establish a network channel or bind every decoder to the sink.
* Replace a raw parenthesized-string regex with a captured AST sequence query:
  the old matcher fired inside automatically decoded arbitrary bytes.
* Describe the Ethereum matcher as accepting a literal **or regex**, and retain
  complete XHR hooks at notable severity inside bundles. Add missing neutral
  DOM-insertion and service-worker-registration hooks.

Run `python3 testdata/sample-review-2026-10-20/check.py` for focused positives,
near misses and benign controls. It copies fixtures outside test-directory
suppression context and generates inert PE/large-line fixtures on demand.
Controls cover ordinary wallet guards, forwarding getters, unrelated guard
calls, protected code lacking wallet interference, monitoring plus decoders,
comma expressions versus call arguments, generated identifiers and data-only
large overlays. Pure OR helper findings may be filtered from rendered output;
their atomic observations and consuming profiles are checked.

The final scans retain 2 hostile findings for the PE, 2 for the injected JS,
and 3 for the wheel. The wheel's existing accurate hostile rules need no edits.
No finding was attributed to a fetched dependency. Deployment and final remote
payload context remain unavailable; the local evidence already establishes
the malicious behaviors stated above.
