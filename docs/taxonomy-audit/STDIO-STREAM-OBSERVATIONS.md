# Stream observations and platform-scope review

This bounded follow-up audits Go/JVM observations in `reverse-shell/stdio` and
the existing Go siblings in `process/io/stream`. It does not complete the whole
reverse-shell cohort. The [nine-entry ledger](stdio-stream-observations-mapping.json)
records every effective before/after definition, including defaults.

## Placement and matcher changes

Three atoms leave the reverse-shell objective:

- Go standard-input assignment → `micro-behaviors/process/fd/stdio`.
- An `inputStream` property assignment and two input/output worker starts →
  `micro-behaviors/process/io/stream`.

Their patterns, counts, file types, platform scopes, and confidence are retained.
Descriptions no longer infer socket/process types from variable names. The JVM
worker observation is notable rather than suspicious: two workers alone do not
establish a bidirectional process/socket relay. Attack/objective tags leave the
neutral observations. Existing Go and JSP objective consumers reference the
new IDs, retaining their other evidence and exclusions.

The Go buffer control also exposed four sibling definitions whose required fact
was standard-I/O assignment. Three differed only by right-hand variable spelling
(`connection`, `conn`, `client`/`socket`); their fourth rule was the OR composite.
They are now one `fd/stdio` atom with exactly that regex union and the old
composite's confidence, 0.95. The three old atoms had confidence 0.93. Their
file/platform scope is unchanged; the bind-shell consumer references the union.
This removes three definitions without losing a matching branch. The separate
stdin-specific atom remains because its required field and accepted spelling
(`StandardInput` as well as `Stdin`) differ from the general assignment union.

The remaining stdin-read atom stays in `io/stream`, without an execution attack
tag. Its co-occurrence composite is now honestly named `go-stdin-copy-and-send`:
reading stdin, copying data, and socket sending alone do not prove the direction
of a bridge. Its explicit backdoor consumer is updated; required evidence stays
the same. No live whole-directory reference to `io/stream` needed replacement.

Destination counts: `fd/stdio` **70**, `io/stream` **31**. Both are leaf-only and
below 85. TAXONOMY.md records standard-stream attachment versus general stream
operations and warns against deriving object types from local variable names.

## Platform advisory correction

The documentation migration exposed a numeric platform-scope policy that could
only be satisfied by dropping Android/iOS coverage, duplicating an observation,
or moving a rule into an exempt directory. None improves taxonomy precision.
A platform count cannot establish that a format-defined fact is too broad.

The four-platform heuristic now emits a **non-blocking review**, consistently
across every tier. Removed the supply-chain and registry directory exemptions.
Reviewers still check the matcher against its declared scope; invalid platform
values and redundant Unix declarations retain their existing checks. The
85-rule cap and leaf-only enforcement are unchanged. No runtime matcher,
platform membership, feature extraction, or scoring implementation changed.

A regression test covers the 3/4 boundary across five subjects, including both
former exemptions, and checks deterministic output. The release build passes;
strict tree validation confirms broad platform scopes no longer become blocking
issues. The current tree has 48 platform review candidates, including the six
preserved documentation observations. This is review work, not 48 proven errors.

## Verification and remaining work

Two new benign controls contain a Go byte-buffer stdin assignment and Java
memory-stream workers. They require the neutral taxonomy paths and forbid every
reverse-shell path. Local atomscan scores are 3 and 2, respectively, with no
reverse-shell finding. The Java control exercises both moved JVM observations.
All nine effective destination mappings are verified against the current YAML.

The remaining `stdio` siblings still need evidence review, especially JavaScript
composites without explicit pipe legs and compiled Windows/.NET co-occurrence
rules. Do not mechanically rename that directory into `stream-bridge`. Final
full-suite results are recorded in PLAN.md.
