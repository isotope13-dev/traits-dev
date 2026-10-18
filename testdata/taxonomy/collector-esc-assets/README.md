# OpenTelemetry Collector v0.37.0 resource review

Verdict: **BENIGN**. The sample is the Go module source archive for
`go.opentelemetry.io/collector@v0.37.0` (OpenTelemetry Collector).

The artifact downloaded from
<https://proxy.golang.org/go.opentelemetry.io/collector/@v/v0.37.0.zip>
has the sample's SHA256:
`c12d4f5d0ddb7f57b0131f1ae822cd1f935e4e5d6f4d1b89e546cb9494ceb277`.
The preceding release was fetched from
<https://proxy.golang.org/go.opentelemetry.io/collector/@v/v0.36.0.zip>;
its archive SHA256 is
`ad80ef22e7049cd3557fd8d62ba6b41be962917015837b293109290e656ef790`.

## Decisive comparison and execution path

`service/internal/zpages/tmplgen/resources.go` is byte-identical between
v0.36.0 and v0.37.0, SHA256
`786628ae0820077318c10c331598f49812d182fcd701d30cbfb9366add3f73e2`.
All six Base64/gzip entries decompress byte-for-byte to the corresponding
shipped files in `service/internal/zpages/templates/` in both releases:

| Template | Gzip bytes | HTML bytes |
|---|---:|---:|
| component_header | 135 | 156 |
| extensions_table | 236 | 353 |
| footer | 39 | 15 |
| header | 288 | 467 |
| pipelines_table | 462 | 1930 |
| properties_table | 242 | 420 |

The generated `_escStaticFS.prepare` looks up a fixed asset map, decodes
`f.compressed` with `base64.NewDecoder`, decompresses with `gzip.NewReader`,
and caches the bytes with `sync.Once`. `File` exposes a `bytes.Reader`.
`templates.go` selects this implementation with `tmplgen.FS(false)`, opens
fixed template names, parses them with `html/template`, and writes rendered
component/pipeline/property tables to the zPages HTTP response. There is no
payload execution or disk staging on this path. The alternative local-filesystem
branch is selected only by `FS(true)` and reads the map's local paths.

The header includes a Material Design Lite script and styles from
`code.getmdl.io`, Google Fonts CSS, and an OpenTelemetry favicon. These are
ordinary browser resource loads and are unchanged in the preceding release;
their notable traits remain. The zPages extension registers `/debug` routes
and serves them through its configured listener (default `localhost:55679`).
The only production changes in this resource consumer and server are package
import comments. The broader release adds documented API renames, configuration
and queue refactors, a feature-gate library, and telemetry/dependency updates.

## YAML changes and controls

* Remove the duplicate esc banner matcher; retain the canonical
  `metadata/build/generated::esc-generated-header` and the distinct asset-map
  declaration. This consolidates overlapping provenance observations rather
  than lowering severity.
* Move the two Go Base64/gzip relationship composites from `data/decompress/gzip`
  to `data/compression`, preserving conditions, proximity, scope, and severity.
  Exact consumers are updated. The sole gzip-directory consumer is the
  compression-evidence OR; both moved composites require the retained
  `go-gzip-reader`, so that consumer's truth is unchanged.
  Central fixture expectations use the new IDs. The banner-print control's
  cap changes from 39 to its measured score of 40 because the directory-based
  feature changes; no matcher or severity was changed to tune the score.
* Separately tighten the esc exception to require the asset map and nearby
  Base64/gzip decoding in the same file. A banner or map alone no longer
  supplies the exception, and unrelated archive members cannot supply its legs.
  Older generated files without a banner can still qualify through their code.

The five fixtures in `cases.json` check provenance consolidation, retained Go
codec matching, gzip-only near misses, and the stdout composite. Direct
`cleave test-rules` checks confirm that the esc exception matches `assets.go`
and rejects `map-only.go`. Scan findings match every fixture expectation.

## Remaining analyzer limitation

The engine-generated `binary/embedded/base64-gz` findings remain suspicious,
including their unsupported T1027.009 mapping. They occur on synthetic carrier
records created in `embedded_code_detector.rs`, which contain only that built-in
finding and receive no YAML evaluation with the parent source's facts. The
parent inherits them after its ordinary trait evaluation. The existing YAML
hook and a matching file-local exception do not remove those records in the
current analyzer. This is an engine issue; adding a duplicate YAML format
matcher or a filename allowlist would not fix it. The verdict is based on the
verified decoded content and its consumer, independent of those alerts.
