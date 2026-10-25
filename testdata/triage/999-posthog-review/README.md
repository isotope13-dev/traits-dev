# 999i and PostHog Node review

Reviewed 2026-10-25. Original inputs were analyzed with `atomscan --no-update
--analyze local --mode slow -f json` and `cleave facts`. Findings were treated
as hypotheses. No specimen was launched on the host OS.

| Input | Identification and judgment | Hostile before → after | Suspicious before → after | Notable before → after |
|---|---|---:|---:|---:|
| `e5223657…bbbb7`, `999i.exe` | Obfuscated Windows x64 kernel-driver loader, **MALICIOUS** | 0 → 0 | 1 → 2 | 44 → 49 |
| `90b91d98…ebd12`, `posthog-node-5.52.6.tgz` | PostHog Node analytics SDK, **BENIGN** | 0 → 0 | 0 → 0 | 117 → 127 |

Counts above are findings on the original input, including inherited archive
findings. All 181 PostHog members remain at zero hostile and zero suspicious
findings before and after. `comparison.json` records every member and every
addition/loss. Mapped observations retain criticality; the one removed
observation is an unsupported Express-server label, replaced by a notable
Express import. There are no material attack-detection losses. Six shared-rule
controls outside this batch preserve every previous finding after ID mapping,
including all prior hostile findings.

## 999i: behavior and evidence

The original is an unsigned 24,027,648-byte PE32+ GUI image requesting
`requireAdministrator`. Original `.text`, `.rdata`, `.data`, and many other
sections have virtual space but no file bytes. Most bytes reside in the final
executable carrier. Small `.enigma1`/`.enigma2` sections establish section labels,
not the identity of Enigma Protector. Family attribution is unresolved.

Rizin inspection followed entry `0x1421c7046` into the obfuscated loader.
Unicorn emulation, with explicitly modeled external APIs, recovered its
rotating-key string decoder and decompressed original code/data. The decoder
uses `ROL32(key, index)`, adds the index to its low byte, and XORs input bytes.
Its immediate key in this build is `0xc33ed2b2`; the new trait leaves that key
unconstrained. The loader checks PE headers, reads the export-directory RVA,
and compares decoded names to exports. Recovered names include
`ZwQueryInformationProcess`, `ZwSetInformationThread`, `ZwQuerySystemInformation`,
`ZwProtectVirtualMemory`, and the loader's ordinary library dependencies.

The emulated path actually calls `ZwQueryInformationProcess` with classes 7
(debug port) and 30 (debug object), then `ZwSetInformationThread` with class 17
(`ThreadHideFromDebugger`), and probes kernel-debugger state with system
information class 35. These are traced actions, not conclusions from API names.
The published Triage report separately records VirtualBox registry/device
probes and thread hiding. Its memory-download links redirect to authentication;
the API returned 401. Those sandbox-only actions were not converted into new
static byte claims. A Microsoft ntdll image was recovered from its symbol
server to support the emulator's native-export model; it is analysis support,
not a payload recovered from the specimen.

Recovery exposed embedded driver images, including Intel's NAL/iQVW64 driver
and a Mellanox `mlx4_bus.sys` image. Embedded-driver presence alone was not used
to convict. The recovered user-mode paths contain:

* At `0x14003ef30`, a 40-byte request with operation `0x33` and caller-supplied
  source, destination and size, submitted with IOCTL `0x80862007`. The wrappers
  at `0x140040190` and `0x1400448c0` swap source/destination to implement kernel
  memory reads and writes through the vulnerable Intel driver.
* At `0x140031de0`, a kernel Code Integrity hash-cache cleanup routine. Its
  `PAGE` scan and signature are followed by relative-address resolution,
  locking, entry traversal, name/length selection, and unlinking. At
  `0x1400322b5` it reads the selected entry's next pointer; at
  `0x14003232b` it writes that pointer into the previous link through the
  kernel-memory write wrapper. It then frees the selected entry. Call sites
  include `0x140091539` and `0x140092b53`.

This chain was compared with the public kdmapper implementation:
[TheCruZ/kdmapper intel_driver.cpp](https://github.com/TheCruZ/kdmapper/blob/master/kdmapper/intel_driver.cpp).
Its `ClearKernelHashBucketList` has the same two signature scans, relative
address displacements, lock, list traversal, unlink and release sequence.
This supports attribution of that routine's behavior, not an assertion that
the whole executable is an unmodified kdmapper build.

The program also carries reverse-engineering taunts and analyst-directed
prompt-injection strings. They were treated only as specimen data. They were
not followed and do not establish an additional executed payload.

**Judgment:** deliberate kernel-security trace removal through a vulnerable
driver, combined with concealed loading and analysis evasion, tips the balance
to malicious. A game-cheat or research context remains possible; authorization,
installation origin, intended loaded driver, and operator context were not
provided. No credential theft, C2, ransomware, or successful privileged execution
is claimed.

**Coverage gap:** the original still has no hostile trait. Its supported new
static observations are XOR decoding, export parsing, and their suspicious
proximity, plus three previously missed neutral imported capabilities. The
kernel-memory primitive and CI-cache unlinking reside inside the compressed
stage. Original `cleave facts` exposes neither those instructions nor a decoded
PE layer. Matcher work therefore targets the decoder/export-parser relationship
that is present in the original bytes. A packer-only hostile composite, a
key/build-specific compressed-byte signature, or a sandbox-only VM-probe rule
would be inaccurate. Reaching three to five distinct hostile findings on the
original requires an unpacking/decoded-stage producer or additional exposed
behavior, not severity inflation. PiDDB, unloaded-driver, persistence, and
network-theft behaviors were not assumed from the presence of a mapper.

A preliminary scan of an intermediate reconstructed memory image emitted a
Netfilter identity from a shared `NETIO.SYS`/hex-format string combination and
a direct-syscall heuristic. Those are not family or attack proof. The memory
image is derived analysis material, not the original executable, and those
findings were not counted as original coverage or used for the judgment.

## PostHog: behavior and evidence

Forager fetched `pkg:npm/posthog-node@5.52.6`; the registry tarball's SHA-256 is
identical to the supplied artifact. It contains normal source, CommonJS/ESM
builds, declarations, and maps. Manifest entry points and shipped code were
followed through `PostHogBackendClient`, the Node subclass, event senders,
feature-flag polling/evaluation, error tracking, source-context extraction,
and Express/Nest middleware. There is no install lifecycle payload. The
`prebuild` script writes the package version into a source file during builds.

The constructor accepts the project's API key and host, defaulting to
`https://us.i.posthog.com`. Calls send caller-provided analytics records, flush
bounded batches, and evaluate/poll feature flags. A personal/secret key supplied
by the caller authenticates flag-definition retrieval; it is not harvested
from the host. Error autocapture is optional. Source-context reads target stack
frame source files, use bounded streams, and contribute context lines to error
reports. The Node OS module provides platform/release telemetry; zlib gzip is
promisified for request compression. These are meaningful dual-use capabilities
and remain notable.

The shipped runtime dependency `@posthog/core@1.55.2` and its `@posthog/types@1.412.4`
dependency were fetched and inspected, including the core sender and flag logic.
The optional Nest adapter imports RxJS; `rxjs@7.8.2` and its `tslib@2.8.1`
dependency were fetched and the relevant exports/helpers inspected. These are
concrete releases within the declared ranges, not proof of a particular
machine's resolved dependency tree. No lockfile or deployment configuration was
provided. A GET of the ingestion host root returned 404; the
[Node SDK documentation](https://posthog.com/docs/libraries/node) was retrieved
and describes the implemented analytics/error/flag APIs. No event data was sent.
Artifacts and `.forage.json` provenance remain in scratch.

**Judgment:** normal analytics/error-monitoring behavior, coherent source and
builds, and exact registry artifact identity support benign. There is no
supported stolen-secret, hidden execution, persistence, or injected-stage
chain. A likely explanation for an external malware label is telemetry and
source-context collection, API-key authentication, generated bundler code, and
broad primitive heuristics being mistaken for a stealer. The source's actual
labeling rationale was not supplied; provenance alone was not used to dismiss
behavior.

## Corrections and validation

`moves.json` records canonical ID moves. Generic PostHog usage remains visible
as telemetry/endpoint/import observations; only an actual product identity
remains under `well-known/lib/observability`. Named exceptions preserve the exact
former exclusion populations. DLL filename references now live under library
paths. Enigma labels now live under section labels. The Bandicam DLL and
Testing Library literal corrections remove two unrelated observations from
full import/section catalogs; no directory was split to evade a budget.
Webpack bootstrap implementation is build metadata and has no process-injection
ATT&CK mapping. An Express import alone is no longer a server.

The new binary matchers mask the key, accept arbitrary section labels, and do
not depend on specimen name, hash, exact size, or reputation. The Node additions
require actual parsed imports and calls. Existing dual-use telemetry, network,
file-reading, event hooks and encoding observations remain.

`testdata/taxonomy/999-posthog/generate.py` creates small non-runnable PE layouts
and source fixtures. Fourteen asserted positive/near-miss cases pass, including
a different decoder key, decoder-only/parser-only cases, an import-directory
near miss, missing XOR, distant evidence, a label-only PE, source comments,
unrelated names, import-only code, genuine telemetry, and an existing Express
factory control outside this batch. Check with:

```
python3 testdata/taxonomy/999-posthog/check.py <atomscan-controls.jsonl>
```

Classifier results remain benign (`lvl: -1`) on both inputs. For 999i,
probability changes from `0.97115433` to `0.96773595`; for PostHog, from
`0.5493515` to `0.49489704`. This is a remaining classifier miss for 999i.
The scanner also reports model v18.18 using an older feature specification
than its expected v21; model scores did not determine the judgments. Final
repository acceptance is `make validate` with no warnings.

Scratch evidence: `/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/999-posthog`.
Recovered memory/PE images are explicitly reconstructed analysis material and
are not byte-identical copies of the original sample.
