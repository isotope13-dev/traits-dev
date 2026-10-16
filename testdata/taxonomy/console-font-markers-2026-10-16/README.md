# Console-font marker controls

These controls cover three markers relocated from `metadata/file/format/structured/linux-console.yaml` into `metadata/file/format/console-font/legacy-font-markers.yaml`:

- DOS EGA code-page font header (`ega-codepage-font-header`)
- DOS VIDEO code-page font header (`video-codepage-font-header`)
- Linux console partial-font manifest header (`console-partial-font-header`)

The EGA/VIDEO positives and wrong-size/device near misses check exact binary headers. The partial-font cases require the exact manifest header and fragment-list evidence for the composite; header-only, list-only, and near-header inputs do not satisfy it. The keymap positive/near-miss pair pins the remaining declarations in `structured/linux-console.yaml`.

The relocation helper proved effective declarations unchanged and rewrote three exact composite references. Across 30 affected selector edges, 29 retained identical membership. The remaining edge is `unc-exe-path-reference`'s `unless: metadata/file/format/structured`; its HTML/VBS/ASP scope is disjoint from the moved markers' data or text/data/shell scopes. No other membership changes were accepted.

Run the focused cases with:

```sh
python3 scripts/check-taxonomy-cases.py \
  --cleave ../cleave/target/release/cleave \
  --cases testdata/taxonomy/console-font-markers-2026-10-16/cases.json \
  --record taxonomy-migration/batches/296-console-font-markers/emitted-findings.json
```
