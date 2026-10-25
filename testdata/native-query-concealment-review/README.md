# Native loader and benign upstream review, 2026-10-25

The original artifacts were analyzed with `atomscan --no-update --analyze local
--mode slow --format json` and `cleave facts`. Reports, disassembly, emulator
logs, recovered upstream artifacts and their forager provenance are in
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/bad-analysis`.
Emulation used Unicorn with mocked Windows APIs, no network and no execution
outside its emulated address space. Observations below are static code claims,
not claims that a downloaded payload ran successfully.

| Original | Judgment | Hostile before/after | Suspicious before/after | Atomscan probability before/after |
|---|---|---|---|---|
| `feca112250d3/v4mprae.exe` | MALICIOUS | 0 / 3 | 0 / 4 | .40700912 / .99 |
| `0b2a2b7cab51/invert.tests` | BENIGN | 0 / 0 | 0 / 0 | .000015934309 / .000015934309 |
| `7a51b9a71fd3/eslint-config-prettier@8.2.0` | BENIGN | 0 / 0 | 0 / 0 | .21009666 / .2766253 |

Counts are the root report's findings, without counting archive-inherited
findings twice. Every ESLint archive member and its registry sidecar also has
zero hostile/suspicious findings before and after. Atomscan's aggregate result
changes from unflagged to flagged for the PE (level -1 to 25, confidence 92;
scan exit 0 to 1). Both benign samples remain unflagged. The older v18 model
feature-spec warning is present before and after; no threshold was changed.

## v4mprae.exe

Unsigned native MSVC x64 network loader. The Triage page calls it DarkSide RAT;
the independently established identity here is a loader using DarkSide-related
infrastructure, not attribution of the unavailable final payload.

Execution and data flow:

* CRT initializers at VA `140001044` and `140001124` decrypt configuration.
  `1400013b0` constructs a list of 50 Windows executable paths and selects one
  with a seeded PRNG. These include taskhostw, RuntimeBroker and other system
  utilities; selection is used by the process creator, not merely a string list.
* WinMain `14000a598` obtains the adapter description using DXGI, checks RAM via
  GlobalMemoryStatusEx, and deliberately faults on the failed low-memory path.
  The rounded-GiB check requires more than five GiB. Microsoft Basic Render
  descriptions trigger username comparisons (george, Bruno, Abby, AMF, dx,
  John, elz, Harry Johnson); an unknown GPU triggers rejection. This is a
  resource/analysis gate, not a claim that IsDebuggerPresent's CRT import
  proves malicious anti-debugging.
* Loaded-module export tables are walked via GS:[60h]/PEB. Each API name is
  hashed with a per-call seed, XOR per byte, and multiplication by 0x143.
  Independent recomputation recovered GetProcAddress, CreateProcessW,
  VirtualAllocEx, WriteProcessMemory, CreateRemoteThread, SuspendThread,
  ResumeThread and the other queried APIs. Rule matching does not depend on
  these build-specific seeds or expected hashes.
* `140008694` reconstructs WinInet request strings and Google DNS-over-HTTPS
  queries. The initial host is dex.cy. `140009a40` finds hex runs, assembles
  byte pairs and applies cyclic XOR with the passed key (GodzillaLOL for the
  initial response); failed decoding falls back to darkside.cy. These names
  are evidence, not required detection legs.
* WinMain constructs `/get_stub.php?id=` with configured/randomized values,
  obtains a response through the same WinInet code, performs Base64 handling
  at `1400082dc` and CryptStringToBinaryA with CRYPT_STRING_BASE64, and stores
  the resulting bytes in the global payload vector at `140016880`. The
  download loop retries failed/short responses. API interception in the
  emulator deliberately returned network failure; successful downloading is
  established as a reachable code path, not an observed runtime outcome.
* Injector `1400065d8` reads that vector as a PE, checks its NT signature,
  starts a selected system image suspended, allocates remote memory, writes
  headers and sections, and computes remote base + AddressOfEntryPoint for
  a suspended CreateRemoteThread call. Thread state changes surround native
  query-hook installation before execution is resumed.
* `140005384` resolves ZwQueryVirtualMemory and constructs a trampoline that
  rejects the pair (selected image base, information class 14) with
  STATUS_NOT_SUPPORTED, while passing other requests to the original code.
  The resulting code is written into the remote host. Class 14 is
  [MemoryImageExtensionInformation in the phnt headers](https://github.com/winsiderss/phnt/blob/master/ntmmapi.h).
* `140005eac` decodes NtManageHotPatch, resolves it, changes remote page
  permissions, reads/checks the syscall prologue, replaces six bytes with
  `mov eax, 0xc00000bb; ret`, restores permissions and flushes the instruction
  cache. This is a separate native-API override in the injected payload host.
  It is not mislabeled as AMSI or ETW patching.

The covert loader, remote image concealment and native API override tip the
judgment. No authorization or deployment context explains those effects.
The final payload, theft, persistence and privilege escalation were not
established and receive no invented detections.

The three hostile rules describe activation, selected-image query concealment,
and hotpatch-API disabling. Additional findings cover runtime string decryption,
resource gating, export hashing, cyclic XOR/hex decoding and the PE-entry thread
argument relationship. Existing network, codec, debugger-reference, process,
format and metadata detections were retained.

## invert.tests

The 417-byte file is exactly the Bash upstream regression test, confirmed by
SHA-256 against the file recovered from
`https://raw.githubusercontent.com/gitGNU/gnu_bash/master/tests/invert.tests`.
All ten cases negate a command/subshell/pipeline and print `$?`. The only
external command is grep over literal `hello`; redirections discard that test
output. No URL, dependency, encoded stage, persistence, secret access or
destructive operation exists. There is no unsupported hostile/suspicious
finding to remove and no security-relevant detection gap. Traits stay unchanged.
The external label is inconsistent with the complete upstream test contents;
its source-specific cause was not supplied. Collection contamination or an
overbroad shell-content label is plausible, not established provenance.

## eslint-config-prettier 8.2.0

Forager retrieved `pkg:npm/eslint-config-prettier@8.2.0`. Its original tarball
has the same SHA-256 as the sample. All 14 members were inspected: index.js
exports disabled formatting rules (with an environment-controlled deprecated
subset), prettier.js exports two rule settings, deprecated entrypoints throw
explanatory errors, validators.js checks rule options, and bin/cli.js resolves
local ESLint and uses calculateConfigForFile to report conflicts. Dynamic
require and bracket dispatch are real capabilities and remain detected.
There are no lifecycle scripts or embedded native payloads. URL literals are
documentation, not request targets; their accurate reference traits remain.

The only declared dependency is the peer range ESLint >=7.0.0, with no lockfile.
The baseline satisfying peer version 7.0.0 was recovered and scanned, and its
lib/api.js -> ESLint -> CLIEngine.getConfigForFile path was inspected. It is an
ordinary linter configuration loader. The deployed peer/plugin set is unknown;
this is not a claim to have verified every possible version satisfying that
open range. Version-pinned README and CHANGELOG were fetched and compared as
documentation. No referenced executable stage was found.

The later package-name compromise is a plausible cause of the source label:
[the upstream incident](https://github.com/prettier/eslint-config-prettier/issues/339)
and [GitHub advisory](https://github.com/advisories/GHSA-f29h-pxvx-f335) identify
other releases, including 8.10.1. This is an inference about mislabeling;
8.2.0's verdict rests on its actual code and byte identity.

## Corrections and retained coverage

`mature-cloned-package` and `cloned-package-identity` previously inferred copying
from a shorthand repository, a hyphenated name, optional-field omissions and
(for one rule) a nonzero major version. The authenticated upstream sample is a
concrete counterexample. Both factual observations retain notable severity in
metadata/package/completeness with names/descriptions about missing project
links. Their unsupported copying, supply-chain and obfuscation claims are gone.
The duplicate component `repo-shorthand-format` is replaced by the already
firing notable `metadata/package/repository::repo-owner-project-coordinate`.
The old security-holder exclusion is preserved in both consumers. Canonical
coordinate syntax additionally accepts uppercase project names and rejects
invalid leading punctuation; those changes establish no attack technique.

Exact and ancestor references were audited before finalizing the move. The
only broad install-hook consumer is windsurf-mcp-injection, scoped to JavaScript
and same-file evidence; these package.json-only metadata rules cannot supply
its runtime-write leg. The completeness exclusions are likewise file scoped
and their runtime/binary scopes do not overlap these package manifests.

Before/after scans against the original HEAD rules retain the real clone
finding on `testdata/hostile/renamed-readme-clone-controls.tgz`, including its
archive members. The runtime-environment manifest control was also compared.
All original findings on the three requested samples survive under the
documented mapping; there are no material attack-detection losses.

`generate.py` and `check.py` cover ten inert native controls, including different
keys, an unrelated decrypted API, a different information class, isolated
thread/hash/patch primitives, and cyclic-XOR versus bare-XOR decoding. Two npm
controls cover the real manifest and a near miss with a homepage. These cases
are registered in testdata/expectations.toml for final validation.
