# Recording sources, local acquisition, and capture mechanics

The [68-rule manifest](surveillance-moves.csv) continues the capture-source audit.
It separates audio and camera delivery from local collection, and separates
recording mechanics from device acquisition. The contracts are documented in
[TAXONOMY.md](../../TAXONOMY.md). Probable capability remains the standard: an
interface name or distinctive stream-handler reference can support an inference
without demonstrating runtime activity.

| Category | Before | After | Meaning |
|---|---:|---:|---|
| collection/monitor/capture | 83 | 29 | Legacy remainder needs source/control-role review. |
| stealer/surveillance | 14 | 6 | Legacy remainder has ambiguous control or vocabulary evidence. |
| stealer/audio | 0 | 3 | Sound export; microphone origin need not be known. |
| stealer/camera | 0 | 4 | Camera images or streams delivered remotely. |
| stealer/audiovisual | 0 | 1 | User-media recording with audio/video selection left open. |
| stealer/screen | 22 | 28 | Adds screen relays, stream responses, and Android screen channels. |
| stealer/multi-source | 24 | 29 | Independently required streams or acquired datasets. |
| collection/audio | 0 | 5 | Local audio acquisition/recording. |
| collection/camera | 0 | 4 | Local camera acquisition. |
| collection/multi-source | 0 | 8 | Independently required acquisition sources without export. |
| hardware/input/media | 0 | 3 | Acquisition/authority evidence leaving audio versus video open. |
| data/stream/record | 0 | 4 | Recording streams/chunks without asserting their acquisition source. |
| hardware/display/record | 2 | 0 | Retired: recording is not necessarily a display operation. |

Paths omit their tier prefixes. The pass adds source categories rather than
depth and leaves every receiving directory within 85. It resolves semantic
misorganization in the siblings of the preceding cap violations; it does not
claim another cap reduction.

## Decisions and evidence limits

An MP3 encoder can process sound from a file as well as a microphone. Its export
belongs in `audio`, with the origin described only as specifically as the matcher
allows. Browser `getUserMedia` can select audio, video, or both. Its existing
record-and-upload composite therefore belongs in `audiovisual`; it cannot claim
both microphone and camera acquisition. Screen-specific acquisition takes
precedence over that general category. Paired tracks in one recording are not
automatically independent stolen datasets.

MediaRecorder can also consume a synthetic stream. Both its constructor and
data-available handler now follow stream recording. The Android MediaRecorder
reference likewise leaves the microphone-only category. Its OR wrapper is
renamed to describe recording APIs or audio authority, preserving all alternatives
and scopes. Consumers that still overstate microphone-specific behavior remain
eligible for source review; reference normalization alone cannot repair those
descriptions or inference thresholds.

Screen or webcam HTTP responses, public relays, and tunneled streams deliver
captured data. The source determines their export home. Conversely, numeric
tunnel-server selectors do not identify the selected source by themselves; their
atoms now describe local HTTP tunnel setup. Screen start/stop labels no longer
claim webcam control. The generic `record(seconds)` declaration does not claim
microphone input, and a WAV filename placeholder does not establish randomness.

Other corrections include moving redundant service/Run-key/task persistence to
its persistence category, keyboard polling to the existing polling technique,
agent-memory acquisition to agent observation, and prompt-directed folder
selection to file targeting. Obfuscated Java ZIP/multipart preparation becomes
archive staging: AWT Robot does not independently establish screenshot acquisition
and multipart construction does not establish sending. An opaque clipboard rule
returns to clipboard collection; raster copying does not supply a second source.

## Preservation and validation

The initial whole-catalog comparison covers **118,798 definitions**. All 68
moved rules retain effective conditions, scopes, exclusions, confidence,
criticality, and mappings. Eighteen labels were clarified, including 14 local ID
changes. Shared ATT&CK values in one document move into defaults without changing
effective settings.

Other work continued in the shared tree during verification. The final
[concurrent-change record](recording-concurrent-changes.json) lists 19 changes
outside this migration: AMOS additions, Java and native matcher cleanup, and
associated reference changes. A servlet matcher, for example, changes from the
word `getParameter` to a qualified servlet import. These edits are preserved.
Final comparison protects **125 definitions** covering the 68 moved rules,
explicit reference consumers, affected broad consumers, and the two intentional
consumer edits below. It reports outside changes separately rather than claiming
the entire shared tree remained unchanged. The catalog then contains 118,797
rules; none were added or removed by this migration.

Two consumer edits are explicit:

- The Python HTTP collector also follows `audio`, `audiovisual`, `camera`, and
  `multi-source`, retaining its existing threshold and proximity. New source
  categories must remain reachable by source-sensitive collectors.
- After a camera-path atom moves into `camera`, the Rust screen/webcam composite
  references both that exact atom and the whole camera directory. Validation
  catches the covered OR leg. Removing it preserves the Boolean result: this
  rule has `needs: 1` and no proximity constraint. It may affect a derived
  precision score; no severity or confidence setting is changed.

The [directory-consumer report](surveillance-directory-consumers.csv) records
38 affected references across 34 consumers. Generic recording no longer counts
as camera or microphone evidence through its old parent. Acquisition, export,
and neutral helpers deliberately change parent membership. Exact references
follow relocated rules. No identical atomic-body group touches this moved cohort,
and no exact-body merge is claimed.

The validator's directory registry in the sibling cleave checkout now recognizes
`collection/{audio,camera,multi-source}` and `data/stream`, consistent with the
documented contracts. These are category registrations, not cap exemptions. The
registry was compiled independently and passes against the current taxonomy.
The full build initially encountered unrelated dependency mismatches: cleave
uses local filefacts/stng APIs absent from the locked Git revisions. Validation
uses an isolated build workspace with command-line patches to those local
checkouts; the shared Cargo manifests and lockfile are not changed for that build.

The rebuilt CLI passes all **1,840 verdict fixtures** and all **38 focused
finding assertions** across 19 controls. The nine new assertions cover audio-only
recording, video-only recording, and synthetic canvas recording. Both user-media
variants retain the recording export; synthetic recording matches its neutral
mechanics without acquiring the user-media export claim. Fixtures are copied
outside the testdata tree and scanned, never executed.

Before the concurrent edits, strict `make validate` retained the same **70
issues** with identical summaries. The final rerun reports **79 issues**: the
nine additional diagnostics concern concurrent Java/AMOS descriptions and a
reusable `pthread_create` duplicate, not this migration. **154 directories**
still exceed 85. No new migration diagnostic remains. The corpus gained three
benign fixtures during reconciliation; all 1,840 pass. `git diff --check` passes
for the traits changes and modified validator registry.

The reconciled snapshot contains **20,303 YAML files**, **118,797 rules**,
**8,690 rule directories**, **17,365 rules in violating directories**, and
**4,275 excess rules**. These are shared-tree measurements, including the
concurrent edits. There remain 60 directories at depth five and none deeper.
Global atomic-body overlaps are now **434 groups**; the violator-filtered report
contains **106 groups / 237 rules**. The added overlap concerns the independently
added pthread matcher. The [637-row ledger](stealer-source-dispositions.csv)
records **634 implemented** dispositions and three sweep reviews.

## Remaining source work

Six surveillance rules remain: three Android accessibility/gesture/control
combinations, one call-log/socket/projection combination, and two generic
spyware/espionage terms. Control and acquisition must be distinguished before
relocation. The terms do not identify an exported source and must not be moved
to file metadata merely because they are strings.

The 29 remaining monitor/capture rules include activity-log configuration,
upload settings, remote-control inference, threshold-based sensor collection,
and broad native input/graphics combinations. Review each required evidence role.
In particular, OR alternatives and overlapping directory matches cannot be
counted as independent acquired datasets. The Rust screen/webcam composite can
still match screen-only indicators, so its name needs review rather than moving
it wholesale into multi-source. Hostile labels on bare permission/API combinations
need benign controls before a separate precision repair; this migration does
not endorse every inherited inference threshold.

The three unresolved sweep rules retain the previously documented work. The
ledger's three review statuses cover sweep only; they are not the entire semantic
backlog. Remaining cap violations and sibling audits continue in the main plan.

The next oversized collection sibling is `keylog/capture` (**193 rules**).
Its 74 atoms include ordinary keyboard hooks/imports, input synthesis through
System Events, window-class labels, terminal configuration, clipboard paths,
and generic event-send methods. These need their capability homes before
splitting collection composites among existing polling/hook/device/terminal
techniques and input export. In particular, synthesizing `key down` is not
observing someone else's keystrokes. Reconcile exact matcher bodies with their
effective scopes; do not retain duplicate listener atoms just because several
different composites consume them.
