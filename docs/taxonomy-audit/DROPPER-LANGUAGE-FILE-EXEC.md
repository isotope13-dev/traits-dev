# Go and Java temporary-file launch audit

Three rules in encrypted staging describe completed file-launch chains,
so their required activation sink is `dropper/file-exec`:

- `go-gcm-temp-payload-launcher` requires an embedded encrypted payload, a Go
  process-launch capability, and temporary/self-path evidence.
- `java-encrypted-temp-shell-dropper` requires the Java payload/decode markers,
  an executable temporary payload, and `ProcessBuilder` evidence.

The composite bodies, scopes, severities, and supporting observations are
preserved. The new composites use fully qualified references to the supporting
traits that remain in encrypted staging. The OrgSearch dropper aggregate's exact
reference was updated to the Go rule's new canonical path. No other exact-ID
consumers were found.

Soft validation passes **1,837/1,837 fixtures**. Strict validation retains
catalog-wide taxonomy and authoring debt, including **165 over-cap directories**.

The Java indexed-XOR resource loader is also in `file-exec`: its composite
requires a bundled resource, decode loop, file write, and Java process launch.
Its anti-analysis consumer now references the canonical exact ID. This adds one
rule without changing its matcher or criticality.
