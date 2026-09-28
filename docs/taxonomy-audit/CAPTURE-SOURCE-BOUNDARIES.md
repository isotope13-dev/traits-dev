# Capture sources, graphics capabilities, and screen export

This pass resolves two cap violations and removes one redundant hierarchy level.
The [181-rule manifest](capture-routing-moves.csv) records every original ID,
final ID, destination file, and normalized definition hash. The source contracts
are documented in [TAXONOMY.md](../../TAXONOMY.md): classify the information
probably acquired, then whether the whole matcher supports local collection or
export. Static references remain useful evidence; runtime proof is not required.

| Category | Before | After | Disposition |
|---|---:|---:|---|
| collection/screenshot/capture | 137 | 0 | Neutral operations and exports leave; remaining collection moves up. |
| collection/screenshot | 0 | 58 | Becomes the leaf; `capture` added no distinction after `stream` was retired. |
| collection/screenshot/stream | 2 | 0 | Both rules describe remote screen delivery; source is screen. |
| collection/monitor/capture | 89 | 83 | Desktop control tokens, an audio API, an endpoint, and a filename become capabilities. |
| stealer/surveillance | 31 | 14 | Audited exports follow screen/image sources; local acquisition returns to collection. |
| stealer/screen | 0 | 22 | Desktop/window/tab content, streams, and screen-derived text with transfer context. |
| stealer/image | 0 | 9 | Image export whose acquisition origin is unspecified. |
| stealer/multi-source | 23 | 24 | Independently required process dump and image export. |
| stealer/sweep | 4 | 3 | Screenshot collection with credential context but no export leaves sweep. |
| hardware/display/screenshot | 77 | 82 | Receives capture capabilities; loses generic graphics, geometry, and filenames. |
| hardware/display/native-capture | 5 | 0 | Implementation-form partition retired into graphics, window, and capture subjects. |

Paths in the table omit their tier prefixes for readability. There are no
directory exceptions or new depth levels. Every receiving leaf stays within 85.
The single-child screenshot branch is collapsed because the child repeats the
parent's meaning, not merely because there is one child.

## Placement decisions

Screen images, tab images, live screen streams, and OCR of displayed content
share a source. A tab image does not become a browser-store theft simply because
it came from a browser. Host context accompanying the export remains context;
it does not create another independently acquired dataset.

GDI raster copying, bitmap construction/readback, DirectX swap-chain setup, and
PNG encoding also occur without screen acquisition. Those capabilities have
graphics/encoding homes. Their exporter composites use `image` when the whole
matcher leaves the origin open. A required desktop/window capture source takes
precedence and belongs in `screen`. Camera recordings need their own source
contract; neither image format nor an optional audio/video alternative proves
that several sources are independently required.

Thirty-six names or descriptions were clarified, including 32 local ID changes.
Examples: `Cursor.Position` is a cursor-position reference; `GetSystemMetrics`
is display-state evidence; an XOR-named function is not inherently a beacon;
the four-field JPEG filename does not identify its fields as credentials.
Generic image paths, multipart fields, window enumeration, and graphics APIs
remain available to explicit capture consumers from their neutral homes.

## Preservation and directory consumers

All **118,797 definitions** pass whole-catalog comparison after normalizing IDs
and effective defaults. All 181 moved rules preserve conditions, exclusions,
scope, confidence, criticality, and mappings. Four documents lift shared values
into defaults without changing effective settings. Comments and descriptions
are excluded from matcher identity. No definitions are added or deleted.

The one additional predicate edit is documented: the Python profiled HTTP
collector now includes `stealer/screen` and `stealer/image` alongside remaining
`surveillance` rules. It retains its threshold and proximity settings. Without
that edit, relocation would remove the collector's access to screen-export
evidence. Its observation threshold still does not assert independent sources.

The [directory-consumer audit](capture-routing-directory-consumers.csv) records
52 changed directory references across 46 consumers, including negative
references. General graphics, paths, and geometry no longer contribute capture
or exfiltration votes through their old parents. Genuine exported sources join
the export parents. This is intentional taxonomy behavior; definition identity
alone does not establish unchanged broad-consumer results.

Two review limits remain explicit. `js-screenshot-exfil` still accepts a separate
monitor-enumeration alternative; its membership is corrected, but that alternative
needs a concrete precision control. CrystalX's broad collection suppressor now
follows local collection rather than relocated exporters. Its family inference
needs dedicated controls before changing the suppressor's intended scope.

## Verification

- All **1,837 verdict fixtures** pass after the final hierarchy change.
- All **29 focused finding assertions** pass: the prior 18 plus 11 capture checks.
  Off-screen bitmap copying matches graphics but not the desktop-capture chain;
  adding desktop acquisition matches the chain. Local tab capture matches its
  capability without the export; capture plus JSON POST matches screen export.
  Fixtures are scanned from temporary paths and never executed.
- The positive upload control also asserts its endpoint observation. Its URL
  uses a reserved `.invalid` host that the matcher accepts; `example.net` is
  deliberately excluded by that matcher and cannot exercise the positive path.
- Strict validation still reports **70 issues**. The only changed diagnostic
  is **154 oversized directories**, down from 156. No new migration diagnostic
  remains. `git diff --check` passes.

The refreshed working-tree inventory has **20,274 YAML files**, **118,797 rules**,
**17,363 rules in violating directories**, and **4,273 excess rules**. There are
60 directories at depth five and none deeper. One directory moves from depth
three to two. Counts include existing working-tree edits; this is not a clean
revision-to-revision or downstream model evaluation.

No identical atomic `if`-body group touches this moved cohort. The catalog-wide
count remains 433 groups; the violator-filtered report remains 105 groups / 235
rules. No duplicate merging is claimed. Scope-aware duplicate validation remains
necessary, and should report effective settings before suggesting a merge.

## Next semantic work

The cumulative [569-row ledger](stealer-source-dispositions.csv) has **566
implemented** dispositions and **three unresolved sweep cases**. Its review count
is not a count of every unresolved catalog issue. Continue with these cohorts:

1. **Surveillance's 14 remaining rules.** Trace Android transaction and control
   protocols before classifying transfer. Distinguish gesture/control channels
   from captured input; distinguish camera, audio, messages, and independently
   required datasets. Browser `getUserMedia` alternatives may permit audio-only
   recording. Two vocabulary signatures and an obfuscated loader need their
   actual subjects, rather than inheriting surveillance from their consumers.
2. **Monitor/capture siblings.** Audit the remaining 83 rules even though the cap
   now passes. Camera retrieval, local audio recording, audio upload, remote
   control, mixed sensor collection, and a persistence watchdog are different
   subjects. Use source and acquisition/export distinctions before splitting.
3. **Display/screen and screenshot.** The Python `screen-capture` umbrella still
   references all of `display/screen`, which includes generic graphics and
   console operations. Audit that sibling and narrow the umbrella through
   positive/negative controls; do not mechanically preserve misleading votes.
   Review inherited ATT&CK/MBC labels on neutral primitives separately from
   this definition-preserving relocation.
4. **Sweep's three cases.** Android permission/WebView inference needs a benign
   control; generic snapshot/export wording needs a protocol-neutral capability
   home; the raw-IP collector needs separate source and upload roles. Do not
   hide unresolved predicates under a new catch-all or lower their criticality
   simply to resolve placement.

Validator candidates from this cohort are semantic-role checks (geometry is not
pixel acquisition; form/header evidence is not itself export), reporting changed
directory expansion in migration reviews, and effective-scope-aware duplicate
comparison. These require evidence-role annotations or controls; directory depth
or a lone child is not a reliable substitute.
