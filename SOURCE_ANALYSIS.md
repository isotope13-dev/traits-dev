# Source evidence and detection policy

## Ownership

filefacts owns syntax, lexical bindings, value relationships, and package
membership. Its APIs accept bytes or logical members: no installations,
generators, fetched imports, or reads outside the supplied artifact.

Cleave owns traversal, budgets, YAML matching, evidence, and reporting. Its
package adapter calls filefacts rather than implementing language semantics.
Fletch owns fetching and integrity, not source interpretation.

## Shared evidence

`ParsedFile::symbols()` supplies call targets and ordered argument shapes and
values. `ParsedFile::flow()` adds typed value relationships through the shared
`Flow` model. Inspect it with `filefacts --flow` (or `filefacts flow`). It is lazy,
cached, shares the existing parse, and does not duplicate its graph into the
untyped metadata tree. Call byte offsets connect the views. Graph IDs are local
indexes, never taxonomy IDs.

The API is format-neutral. The graph records its producer and limitations;
currently the producer is the source parser. Unsupported analysis, including
binary flow recovery that is not implemented yet, returns `None` (`null` in
the CLI's JSON view), not an empty graph. Neither missing flow nor a graph
without a matching relationship establishes that an artifact is safe.

Values include literals, parameters, calls, merges, receivers, and object
fields. Helper returns substitute parameters in the caller's context.
Origin observations retain that invocation context when a rule subsequently
inspects an originating call's arguments; unrelated calls cannot supply its
secret-name literal. Chained calls retain distinct targets even when their
source ranges start at the same byte.
Reassignment replaces bindings; scoped declarations preserve outer bindings.
Compound assignments to local identifiers retain both the previous value and
the right-hand operand; subsequent ordinary assignments replace that merged
binding. This is operand provenance, not constant folding or a model of
overloaded operators. Member/indexed compound mutation remains unsupported and
reports `compound-assignment-target` rather than inventing an object update.
Receivers and arguments are separate, as are `headers` and `body` fields.

External calls are opaque unless an explicit library model supplies transfers.
Unknown implementations are not assumed to return their inputs. Security
vocabulary, source/sink selection, and severity belong in YAML.

```yaml
if:
  type: symbol
  kind: call
  exact: net/http.Post
  arg:
    index: 2
    from:
      call: '^os\.(Getenv|LookupEnv)$'
      literal: '(?i)(TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY)'
      through:
        - call: '^(strings|bytes)\.NewReader$'
          arguments: [0]
```

`index` is zero-based; omission preserves any-argument matching. `from.call`
selects an originating call. `from.literal` matches its literal argument
(`from.argument`, default zero). `from.field` selects an object/keyword field
before traversal. `through` declares contributing arguments and/or receiver.
These filters also work in `args`, which requires distinct argument positions.
As an alternative to an originating call, `from.value` matches a literal that
contributes to the sink argument through the same explicit transfer models.
It is mutually exclusive with `from.call`, `from.argument`, and `from.literal`;
this distinguishes written or transmitted content from an unrelated comment.

Regexes use the existing bounded cache. Argument assignment uses augmenting
paths, not permutation backtracking. Cleave drops graphs after compact member
evaluation rather than retaining them across an entire archive.
The symbol candidate index includes canonical flow targets as well as raw
symbol names. Rule-duplicate checks retain the full argument predicates,
including positions, provenance, and multi-argument multiplicity.

Extraction caches include the basename, detected type, and extension mismatch
as well as content and analyzer identity. Identical bytes named `build.rs` and
`lib.rs` must not share filename-derived facts. Directory names do not affect
file-local extraction and are not part of this cache key.

## Declared manifest scripts

`ParsedFile::embedded_sources()` borrows GitHub Actions run bodies from the
existing parsed values and identifies explicit shell declarations, including
workflow/job defaults. It does not classify arbitrary YAML strings as code.
Missing, dynamic and custom shell declarations remain unknown; OS-dependent
defaults are not inferred. No actions are fetched and no scripts are executed.

Cleave analyzes supported bodies as separate logical source members identified
by escaped JSON Pointers. Locations refer to the decoded script, not invented
contiguous offsets into folded/escaped YAML. Separate steps do not share
file-scoped evidence. Traversal is bounded at 100 bodies, 1 MiB per body and
10 MiB total; unsupported shells, runner expressions and exhausted limits leave
an `embedded-source-incomplete` analysis gap. Nested string/code reanalysis is
currently disabled for these bodies; direct source facts and AST rules apply.

## RPM header scripts

Filefacts exposes the nine basic lifecycle scriptlets as
`rpm.scriptlets.<phase>.{body,program,flags}` and borrowed `embedded_sources()`
units. Bodies remain independent from payload extraction. Interpreter STRING
and STRING_ARRAY encodings normalize to argv; RPM's own builder still writes
the scalar form for a single interpreter
([upstream implementation](https://github.com/rpm-software-management/rpm/blob/master/build/parseScript.cc)).
Missing interpreter declarations use RPM's `/bin/sh` default. Invalid present
declarations never become defaults. Only known single-argument interpreters
receive a source type; extra arguments, unknown interpreters and nonzero or
invalid processing flags remain unknown. Runtime expansions are not evaluated.

Cleave reuses its bounded declared-source adapter, with a separate logical
member per body. Malformed or ambiguous script tags retain independently valid
units and an incomplete diagnostic. Script-body copies are limited to 1 MiB
each, interpreter argv to 64 arguments/64 KiB. Ordinary descriptive header
strings are not code. GitHub runner-expression exclusions do not apply to RPM.
Trigger arrays and stripped RPM payloads remain outside this implementation;
visible header scripts do not imply complete package coverage.

## CPIO package members

Filefacts identifies ASCII CPIO (`070707`, `070701`, `070702`) and indexes
member paths, kinds, ownership and byte extents through `archive_members()`.
`cpio.complete` is false when indexing stops on malformed/truncated input or
its metadata limits; previously indexed members remain available. This is
parser state, not a malware verdict. Indexing is bounded at 65,536 entries,
1 MiB per name and 16 MiB of headers, names and retained link targets.

Cleave copies validated extents under its extraction budgets and recursively
analyzes their detected types, including gzip-wrapped macOS installer scripts.
It sanitizes original paths, disambiguates collisions, never creates links or
special files, and does not preserve executable permissions. Incomplete indexes
produce the existing notable archive-incomplete diagnostic. Neither missing
members nor an unsupported format establishes safety.

The CRC variant's layout is supported but its additive checksum is not verified.
Hardlink aliases are not reconstructed: entries expose their stored bodies.
Binary CPIO and RPM stripped `07070X` remain unsupported. RPM's existing newc
stream reader is a separate legacy path; this change does not claim to migrate
that parser or recover stripped RPM payloads.

## Go dependency evidence

Filefacts parses module/workspace directives, checksum records, and vendor
inventory, then reconciles references over caller-supplied logical members.
Its filename classification tells archive traversal to retain `go.work`,
`go.work.sum`, and `modules.txt` even when they are detected as non-program
data. This does not require enabling analysis of every unknown member.
Only an explicitly owning workspace contributes replacements; unrelated and
nested-archive manifests cannot change another module's references. Local
replacements must stay within supplied artifact boundaries. Conflicting pins,
missing local modules, exclusions without a selected replacement version, and
malformed or budget-limited context remain unresolved.

Checksum history is metadata, not a list of dependencies to fetch. Module-tree
and `go.mod` checksums remain separate, including conflicting records. Scan
preserves this evidence and calls filefacts for reconciliation; it contains no
second Go manifest parser. Identical manifest bytes in different workspaces
retain both contextual dependency edges instead of overwriting one another.

Fletch verifies a selected module ZIP against its Go `h1` tree checksum, with
bounds on entries, names, and decompression. ZIP integrity is not authenticity:
matching a supplied checksum does not establish that the dependency is benign.

This is declared-minimum/replacement reconciliation, **not Go's MVS build-list
resolver**. Captured vendor sources are inspected locally; the scanner does not
reproduce every `GOWORK`, `-mod`, toolchain, private-proxy, or build-tag setting.

## Coverage and migration

This is bounded source-local **may-flow**, not a compiler, execution trace, or
proof that every path executes. Limits and known omissions remain explicit.
Missing or unsupported evidence must not be interpreted as a clean bill of health.

The tested JavaScript/TypeScript, Python and Go anonymous-function forms are
currently omitted from flow modeling. The graph reports `anonymous-function`
even when a callback occurs inside a named function.
Nested named functions omitted by the current function walk report
`nested-function`. These are explicit limitations, not inferred callback values,
captures or event-source relationships. Call symbols remain independently
available for those bodies. Ordinary cleave reports do not yet propagate every
flow limitation; inspecting the flow API/CLI is necessary for this diagnostic.

All tree-sitter adapters use the same evidence types. Shared assignment/helper
contracts currently test Rust, Go, Python, JavaScript, TypeScript, and C. Schema
availability in another language is not tested semantic coverage. Additional
syntax requires positive and negative adapter tests.

The older payload-flow projection remains during migration of existing traits.
It still contains specialized API/security knowledge and is **not the target
architecture**. Do not add security vocabulary there: use YAML models and extend
policy-free relationships when necessary. Removing compatibility behavior must
preserve all existing expectations. Go dependency selection and native-binary
recall remain separate evaluations.

Before claiming parity or completing the migration, remaining work includes:

- Remove the security-aware legacy payload-flow projection only after every
  dependent expectation has a YAML-policy equivalent.
- Propagate per-query `FlowOrigins.incomplete` through ordinary and compact
  reports; the graph/API exposes limits, but the matcher does not yet surface
  every query-level incomplete result.
- Extend tested object-field/helper-return, mutation, cross-file, and dynamic
  dispatch semantics without assuming opaque functions preserve their inputs.
- Evaluate compiled Go/Rust credential-stealer recall and a matched real-world
  Rust/Go/Python/JavaScript corpus. Source probes and benign native canaries do
  not establish either.

## Tests

Parser/engine tests belong in their owning repos. Trait specimens belong in
`testdata`, with hierarchy-prefix assertions in `expectations.toml` and the
normal `make validate` runner. Never install or execute these source specimens.

Exercise direct arguments, aliases, helpers, overwrites, shadowing, separate
object fields, opaque calls, malformed input, budgets, and package boundaries.
Test the real archive-to-facts path as well as fabricated reference lists:
correct reconciliation is ineffective if traversal never supplies a manifest.
Distinguish build-time execution, explicit generators, initialization, tests,
and ordinary runtime capabilities.
