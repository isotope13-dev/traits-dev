The judgments are **BENIGN** for dogmans-afterglow 11.0.0 and **MALICIOUS**
for both Windows executables. These judgments follow code recovery and execution
path analysis. The externally supplied family lists are not adopted as identities.

Counts below describe each original file's root findings. Fetched dependencies
are reported separately, rather than silently added to the archive root.

| Original SHA-256 prefix / identity | Hostile before → after | Suspicious before → after | ML reported probability before → after |
|---|---:|---:|---:|
| 123d1e44ac3e / Afterglow game and proxy portal | 0 → 0 | 1 → 0 | .97290623 → .95816990 |
| 649f710e32a6 / Rifaien self-mutating submission client | 0 → 0 | 0 → 0 | .92498976 → .92498976 |
| df9a2a00968c / protected CLR remote-control and collection implant | 0 → 0 | 1 → 1 | .99265790 → .99265790 |

Each of the three jsDelivr `fonts.min.js` dependency URLs changes from **1
hostile / 0 suspicious** to **0 hostile / 1 suspicious**. Their bytes are
identical, SHA-256
`cc6ccb7ca50b5ea305ba0188ffaad3ddc8090d6203af9a520e510a167e0f5855`.
Across the archive and dependencies, unique hostile/suspicious IDs change from
1/1 to 0/1. [scan-delta.json](scan-delta.json) records every archive member,
dependency, count, lost/added ID, and complete before/after ML output.

The shipping classifier returns benign for both malicious originals. Live tiny
output says `scan benign confidence=0.925` and `scan benign confidence=0.993`.
The JSON retains `cls: 0`, `lvl: -1`, `conf: 0`; high reported probabilities are
not substituted for actual verdicts. The model bundle is v18.18 and warns that
its v18 feature specification predates the engine's expected v21. This is a
remaining classifier disagreement, not evidence to inflate or duplicate rules.

**Afterglow.** The npm entrypoint is empty, there is no install hook, and the
delivered application is HTML. The package root redirects to a shell which
loads the arcade into a frame. `dist/afterglow.html` uses the Arcade API for a
game catalog and player; its recommendation interface selects games. The
injected AI interface connects a WebSocket to `/ai`, sends user chat input and
attachments, and stores chat history locally. `dist/ai.js` also exposes explicit
screen sharing through getDisplayMedia. These are retained capabilities; no
covert collection or unrelated-secret transfer was found. The Arctic bundle
implements a proxy browser, game interface, chat, synchronization, and settings.
Blank/blob tabs, CDN fallback, and base64 endpoint strings serve that portal.
The SVG uses a foreignObject, fetches the package's HTML, and writes it into a
frame document. No native launch or installation behavior is inferred from it.

The Lumin dependency needed a second recovery pass. QuickJS evaluated only its
bounded decoding expressions, replacing the final network handoff with a JSON
dump. This recovered five fallback origins, `/api/v1/boot`, its request token,
and 35,326 integer bytecode words. Forager retrieved the referenced boot JSON:
an interpreter, a 10,680-character string pool, and fallback-origin data. An
offline disassembler decoded 9,599 instructions by following function and jump
targets after the two header words. Recovered functions publish Lumin.init,
search, categories, pagination, an iframe game player, worker loading, endpoint
fallback, and Google Analytics. The source actually compiles a response field
with `(0,Function)(i[0])()` and runs the returned VM; that capability remains
notable, and its concealment remains suspicious. Static recovery does not claim
that the mutable remote bootstrap successfully ran in a browser.

This matches the browser-game SDK described by its
[publisher's documentation](https://docs.luminsdk.com/). The verdict rests on
the recovered implementation, rather than trusting that documentation or the
absence of detections. Forager also fetched and inspected the referenced Arcade
SDK and Arctic page. A direct HTTP request to the AI WebSocket endpoint returned
524 after retries, so its server implementation is unavailable; the local
handlers show chat and user-selected media flow, not an OS execution channel.
Future mutable CDN content and server behavior are outside the recovered bytes.
Obfuscated remote code, disguised script naming, and school-filter bypass are
plausible reasons for the external malware label, but its source rationale is
not known. Those properties alone do not establish malware.

**Rifaien.** The original is a PE32 UPX image whose checksum defeats the normal
unpacker. Unicorn emulated only its decompressor and branch fixups, stopping at
0x428716 before imports or application execution. A reconstructed analysis PE
restores the original import and export tables. Main is at 0x4013a0. It reads
its own filename/file, searches for `[[UNIQUE]]`, and saves the offset after that
marker. Every 30 seconds it selects NODE1–NODE7, generates a random executable
name, overwrites sixteen bytes after the marker, writes the whole mutated image,
and supplies that same filename to curl_formadd. The form contains file, node,
and submit fields. curl_easy_setopt configures the upload URL and form,
curl_easy_perform submits it, and `_unlink` removes the generated copy after a
successful submission. The loop repeats. The fixed endpoint is
`http://wecan.hasthe.technology/upload`; its hostname is not a detection gate.

The arbitrary bytes include an appended, truncated native PE beginning at file
offset 0x14c8b. Its declared sections extend beyond EOF; this does not establish
that the client executes that image. Uploading its own executable is also not
theft of unrelated files. Autonomous mutation and repeated executable submission
for numbered execution nodes tip the judgment toward malware/replication abuse.
No deployment evidence establishes an authorized isolated experiment; such
context could change the judgment. The external multi-family labels do not
prove any of those downstream payloads are executed here.

The existing `native-mutated-self-image-loop` suspicious trait and
`self-mutating-image-submission-loop` hostile composite both match the correctly
reconstructed image. The form matcher binds the written filename and exported
libcurl sinks. Neither rule needed weakening or a new duplicate. The original
has zero hostile traits because automatic UPX decoding fails its checksum.
This is an unpacking gap. A second or third hostile rule would also be
unjustified for the same one replication behavior; staging, networking, and
temporary-file deletion retain their own capability meanings.

**Protected CLR implant.** The unsigned MSVC PE32 carries near-random RCDATA
and copied libGLESv2 version strings, rather than a working graphics-library
purpose. Native main at 0x4019f0 constructs a table at 0x401300, extracts a
resource, and transforms it in 1,024-byte blocks with 0x401560. Emulation of
these bounded decoder functions recovers a size-prefixed, checksum-valid zlib
stream. Inflation produces 2,825,742 bytes: a 14-byte CLR-version prefix and a
managed image. The bootstrap reads its `_` resource, Assembly.Load loads it,
and its EntryPoint is invoked. This is commercial .NET Reactor style protection;
the existing suspicious wrapper finding is accurate and unchanged.

The inner assembly conceals method prefixes and API calls. A bounded CIL
interpreter recovered the 65,892-byte patch stream from method 2254 and the
13,200-byte delegate map from method 2245. The real assembly public-key token is
required for the patch cipher. Parsing the entire patch stream restores 2,610
method prefixes/headers, consuming it exactly; 1,650 field-to-method mappings
resolve delegate proxies. Native API calls were simulated for traversal, not
executed. This creates analyst reconstructions, not observed runtime outcomes.

Main method 680 (`PEs.627`, RVA 0x32bbc) invokes the task orchestrator
`2J2.nC6` (833, RVA 0x40294). Recovered handlers include hidden process launch,
download, and remote-control operations. More decisively, the following chain
binds collected bytes to outbound upload:

1. `kJk.654` (562, RVA 0x2b4fc) starts and waits on collection tasks. Its
   clipboard task calls `Clipboard.GetText` and `GetFileDropList` in `M64.96t`
   (577, RVA 0x2df2c), then passes encoded results to `kJk.J3H`.
2. The display task `M64.C4I` (578, RVA 0x2e26c) enumerates screens and calls
   `721.m28` (613, RVA 0x304d8), which captures through GDI helpers and returns
   JPEG bytes. Those bytes also enter `kJk.J3H` (565, RVA 0x2bd78).
3. J3H adds data with `C75.Xt4`. The collector saves the archive to a
   MemoryStream and returns ToArray. `85K.X9z` saves that return value in local
   7 at IL 0x1a2 and supplies the same local to `HtQ.E2P` at IL 0x3ab–0x3d8.
4. `HtQ.E2P` (712, RVA 0x35648) constructs attachment fields and calls
   `E65.F4j` (815, RVA 0x3f624). That method encodes the multipart body and calls
   `E65.48o` (816, RVA 0x3f6f0). The latter obtains WebRequest.GetRequestStream,
   writes the supplied byte array, and calls GetResponse.

[managed-traces.json](managed-traces.json) records relevant method tokens,
RVAs and resolved call targets. Concealed control handlers and collection/upload
tip the judgment to an implant. No legitimate installed-product identity,
consent, or management deployment is established. Family, live C2 configuration,
runtime success, and remaining virtualized strings are unresolved.

The original remains below the 3–5 hostile-trait goal: zero hostile findings.
Scanning the original, bootstrap, protected payload, restored assembly, and
resolved assembly was attempted. Neither facts extraction nor atomscan applies
this custom native decoder, method restoration, and proxy recovery to the
original. Even the recovered image lacks matcher-level bindings across the
collector, archive builder, command dispatcher, and HTTP upload. The uncovered
hostile behaviors are hidden command execution and clipboard/display collection
followed by upload. A resource ciphertext signature or a composite of unrelated
API names would not solve that gap accurately. Engine unpacking and managed
interprocedural flow support are needed; no hostile packing aliases were added.

**Rule changes and retained coverage.** The old hostile JSON-loader rule
required only JSON-fetch, indirect evaluation, indexed XOR, and browser storage
in one file. It established neither malicious purpose nor a response-to-code
binding. Its exact condition set moves to suspicious anti-static observation
`json-fetch-indirect-eval-xor-storage`. The blank/blob page-swap rule likewise
established capability co-occurrence, not disguise or linked fetched HTML. Its
exact matcher moves to notable `fetch-document-write-with-blank-blob-urls`.
No exact consumers depended on either old ID. Ancestor consumers were inspected;
real school-tab disguise still matches its separate hostile rule.

The jQuery alias matcher was also firing on local `$` wrappers for
document.getElementById/querySelector in three package members. It now excludes
those explicit local implementations, with a new notable DOM-helper finding.
An additional notable constructed-evaluation rule covers invocation of the
result of an indirect Function constructor, which the prior immediate-Function
AST pattern missed. It rejects construction without invocation.

Eight boundary fixtures, explicit jQuery alias positive/negative checks,
genuine fetched jQuery 3.7.1, and two preexisting hostile fixtures verify these
changes. All findings on the three outside-batch controls are identical before
and after. The existing ghappier remote-eval hostile finding and both encoded
HTML-stager hostile findings remain. No supported attack detection is lost.
The intentional losses are the unsupported generic hostile claim, the disguise
overclaim, and false jQuery attribution; their supported observations remain.

Reproduce the saved-report regression with
`python3 testdata/triage/afterglow-rifaien-clr-20261024/check.py <scratch>/review`.
The original and recovered atomscan reports, cleave facts (including decoded
strings), Rizin output, offline VM/CIL decoders, reconstructions, and forager
provenance are retained under this task's `scratch/review`. Artifacts were not
launched as applications. `marker-lines.txt` contains the verbatim marker text.

Recovered analysis artifact SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| UPX reconstructed PE | 1e6dc0ed57cecc0c0b11196a4e98ba5e19e8ed85315945df070026aaacd44380 |
| CLR bootstrap | ed7891a3c2b53ae3b1601bf6c98be0fae55fb0b5975caf5e1a27ff9f960a31a9 |
| Protected inner assembly | 71cbcdce0f85ffdf782e6a47ecb6a01db50bba0701310025878ba898d62d781e |
| Method patch stream | cd95bb18c9f79813b903bcdc9a17a3d4545915092f91a42b3baba36706a7c847 |
| Restored assembly | 5e705a2851bd4ef110d54f748fae76c55ec731f6cc30993440976ca2d089565f |
| Resolved assembly | 360bafc6d8206fc65816aea4e45291b28f706197bdb67c1ba4429aa40434912a |
