# Browser observation, event instrumentation, and collection

The [113-rule manifest](activity-routing-moves.csv) separates neutral observations
from the oversized browser-activity and tracking leaves. Placement contracts are
in [TAXONOMY.md](../../TAXONOMY.md).

| Leaf | Before | After |
|---|---:|---:|
| objectives/collection/activity/browser | 100 | 62 |
| objectives/collection/monitor/tracking | 125 | 50 |
| micro-behaviors/os/telemetry/logging/event | 16 | 59 |
| micro-behaviors/os/telemetry/activity | 21 | 39 |
| micro-behaviors/os/telemetry/logging/analytics | 24 | 30 |
| micro-behaviors/communications/http/telemetry | 37 | 41 |

The pass resolves two cap violations. All receiving categories remain strict
leaves within 85, without new hierarchy levels or exemptions. It does not route
browser exports into another overfull leaf: stealer/browser already has 106
rules and needs source reconciliation before receiving the remaining export
classifiers.

## Boundaries and concrete corrections

Tab callbacks and URL extraction identify observation capabilities. References
to browser executable filenames belong with application paths. JSON serialization
of visited URLs is not upload; an adjacent request-body field is request
construction, not completed transmission. IndexedDB wrapper construction, array
push plus local storage, cookie lifetime, and uninstall-URL registration each
retain their own capability home. Exact consumers retain their references.

An empty allowlist plus an index miss does not establish an early return,
disabled surveillance, or a kill switch. The renamed array observations describe
what their matchers require. Their existing objective consumers still need
control-flow review; relocation does not silently tighten them.

Named failure/success events and UI event labels identify instrumentation
interests. They belong in logging/event, not collection. Activity field/event
combinations describe reporting interests; analytics interfaces and property
bags belong in logging/analytics. Telemetry request mechanics and endpoint
references belong with HTTP telemetry. Path-field labels and a generic
send-to-chat label do not become telemetry solely through a consumer.

This matters beyond the individual labels: a Feishu record builder plus ordinary
file-error event names no longer satisfies the broad collection leg of a
sensitive-record classifier. The positive control with actual typed-key
recording still satisfies it. The catalog describes probable capability from
static evidence; these boundaries do not impose proof of runtime activity.

## Preservation and tests

Pre-write normalization checks all **118,798 baseline definitions**. The final
proof protects **208 moved/affected definitions**, plus checks the separately
restored JVM atom against its earlier working definition. The 113 moves preserve
all effective conditions, scopes, confidence, criticality, exclusions, mappings,
and thresholds. Thirty-eight descriptions and 34 local IDs were clarified.
No identical atomic matcher-body overlaps touched this moved cohort.

[Directory membership changes](activity-routing-directory-consumers.csv) record
**66 references in 62 consumers**. Broad collection references shed event
vocabulary and neutral mechanics; neutral categories acquire the matching
capabilities. No historical membership aliases, `needs` changes, or proximity
changes recreate the mixed buckets. Exact-rule consumers keep their semantics;
broad membership changes require behavioral controls as well as normalization.

The six new controls cover URL serialization with/without upload, ordinary
Feishu status records versus typed-key records, and empty/populated allowlists.
They pass **14 assertions**. Existing source and input suites add **68 passing
assertions**, for **82** across 40 controls. Fixtures are scanned from temporary
locations outside path-based fixture suppressors; their contents are not run.

## JVM regression found by the full corpus

The first full run exposed a pre-batch change to
`jvm-user-fallback-dylib-stage`: its class-string `lib` observation had been
replaced with `java.library.path`. These observations are not equivalent. The
hostile Maven dylib fixture contains the `lib` directory label and `user.home`,
not the Java runtime search-path property, so the changed composite stopped
matching.

The repair restores the earlier atom under the precise neutral home
`micro-behaviors/fs/path/library::jvm-lib-directory-label` and reconnects the
composite. It preserves the original matcher, file types, platforms, confidence,
criticality, and Gradle-wrapper exclusion. Its description does not claim a user
home from a bare directory label. The runtime-property rule remains available
for programs that actually reference it. This is one restored atom and one
consumer correction, separately recorded in
[activity-routing-repairs.json](activity-routing-repairs.json), not included in
the 113 behavior-preserving moves.

Independent edits after this batch's baseline are recorded in
[activity-routing-concurrent-changes.json](activity-routing-concurrent-changes.json).
They are not overwritten or counted as completed migration work. Current
whole-tree counts include them.

## Next actions

1. Audit the 106-rule stealer/browser leaf before routing history/navigation
   exports out of collection. Separate browser authentication material,
   history/navigation, general session state, unrelated credential stores, and
   independently required sources. An optional source is not multi-source.
2. Reconcile the remaining 62 browser-activity and 50 tracking rules by acquired
   source, neutral telemetry, lifecycle/identity behavior, or another actual
   objective. SDK identity, a remote endpoint, or a method name alone must not
   be relabeled as an unauthorized transfer.
3. Review mixed OR predicates such as local-staging (encryption OR storage),
   upload-payload (serialization OR body context), and telemetry identity fields.
   Their role in a consumer does not change their matcher identity. Avoid
   preserving an overclaim merely because a renamed exact reference still works.
4. Review the receiving user-agent leaf (85 rules) before adding browser-emulation
   observations: a general emulation method need not mean only a User-Agent
   override. Distinguish client compatibility behavior from a header value.

The remaining collection/monitor siblings and earlier capture/source backlogs
remain open. Getting these two counts below 85 does not certify the remaining
classifiers or complete the overall taxonomy migration.

## Final validation scope

The shared tree's strict run reports **85 diagnostics**, including **151
oversized directories**. The later soft run cannot load a newly added Go wallet
file: two `count_min` regex-alternation checks are fatal even in soft mode. That
file was added after this batch's baseline and is outside the migration.

An isolated, frozen YAML copy excluding only
`objectives/exfiltration/stealer/wallet/go-browser-wallet-exfiltration.yaml`
passes **1,841/1,841 verdict fixtures** (including one newly added benign
fixture). The repaired JVM rule also matches the extracted class directly;
testing a leaf-scoped class rule against only its enclosing JAR is insufficient.
The [snapshot manifest](activity-validation-snapshot.json) records the excluded
file, file count, and tree hash. This temporary validation exclusion is not a
repository change or a taxonomy-cap exemption, and the passing result does not
claim current-tree validation is green.

The final definition proof records **28 independent post-baseline changes**
separately and preserves the 208 protected definitions plus the restored atom.
All **82 focused assertions** pass. The Go wallet loading errors and the broader
strict-validation backlog remain outstanding work.
