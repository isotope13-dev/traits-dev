# ABI normalization repair and sparse-string consolidation

Follow-up: [Graphics vocabulary and provider identity](GRAPHICS-VOCABULARY.md)
records the subsequent graphics placement, Mesa identity, duplicate count-profile
and validation-hygiene repairs. Counts and destinations below are historical.

The ABI matching gap reproduced in [Binary observations](BINARY-OBSERVATIONS.md)
is repaired together with its consumers. The [21-entry ledger](abi-repair-mapping.json)
is verified against current effective definitions. Seven unrelated concurrent
archive-criticality edits are excluded from this task ledger and left intact.
Validation below describes the current shared worktree.

## Changes and placement

- The C++ prefix regex now accepts zero through two leading underscores before
  its existing alternatives; the GNU runtime regex similarly accepts normalized
  `gxx_`. This adds the normalized spellings while retaining all spellings
  accepted by the previous regexes. The underlying observations remain compiler
  characteristics in `metadata/binary/symbols/compiler`.
- The redundant `library/family::cxx-abi-symbols` wrapper is retired. The libc
  standard-library aggregate retains its explicit libc++/libstdc++ references
  and loses the generic ABI alternative. Compiler symbols do not establish a
  library identity or justify suppressing unrelated behavior.
- The former exception-obfuscated-execution composite becomes
  `micro-behaviors/process/create/api-system::small-abi-system-reference` at
  notable. It still requires ABI evidence, the existing system-API observation,
  at most 50 strings, its size ceiling and its two exclusions. No exception
  control flow was established by the old conjunction.
- `metadata/file/string/count::binary-strings-at-most-50` is the canonical raw
  measurement. It consolidates the native-control-flow atom and WSJ-local copy.
  Its platform scope is the union needed by the existing ELF/Mach-O users:
  Linux, macOS and iOS. The WSJ family consumer retains its original Mach-O,
  macOS and 16–512 KiB bounds. The shared measurement retains the native atom's
  default confidence; the redundant family copy's separate 0.8 confidence is
  removed, while the family composite's confidence is unchanged.
- `metadata/file/string/count::large-macho-strings-at-most-50` reuses that
  primitive while retaining the original Mach-O scope, 100,000-byte floor,
  confidence and low-code-entropy exclusion. Its neutral characteristic is
  notable rather than suspicious. The section/prose wrapper becomes redundant
  after this correction and is consolidated into the same canonical rule.

The native control-flow directory is removed. Its string count was not a
control-flow operation, and its composite did not establish exception abuse.
Three redundant definitions are removed overall: the library alias, WSJ-local
count and section/prose wrapper. Neither symbol predicates nor contextual
filters are copied into a second directory.

## Consumer audit

The [95-entry ancestor audit](abi-repair-ancestor-audit.json) covers:

- 63 library/family ancestor occurrences: generic compiler ABI evidence no
  longer supplies a library identity; specific library observations remain.
- 25 process/create occurrences: the new profile requires the existing
  `system-fn`, so it adds no new Boolean support. The sole `needs: 2` consumer
  already has both system-fn and a primitive API observation whenever the new
  profile holds.
- One api-system directory reference in system-fn: replaced with its exact five
  pre-change primitive alternatives. Otherwise, the new dependent profile would
  create a positive cycle through that directory reference.
- Two metadata/binary downgrade occurrences: explicitly retain the relocated
  restricted Mach-O count. Newly recognized ABI symbols are binary
  characteristics; the full fixture gate checks the repaired recognition.
- Four obfuscation-category occurrences: neutral counts and the ABI/system
  profile are not backfilled as concealment evidence.

Exact consumers, including the WSJ family and the existing sparse-string
stager rules, are updated to canonical IDs. The two count predicates are
separate levels of evidence: the raw count and the count with size/entropy
filters. They share one primitive rather than duplicate its matcher body.

## Verification

Three benign archives include reproducible C source and inert shared objects;
they are compiled with `cc -shared -fPIC -nostdlib -Wl,--build-id=none` and never
executed. They cover ABI symbols without a library identity, ABI plus system
without exception flow, and ABI-looking string literals/user-prefixed symbols
alongside a real system import.

The checkout-engine positive trace matches both repaired ABI atoms and the
neutral system profile (**3/3**). The negative trace matches none (**0/3**), even
though the ordinary system API and sparse-string prerequisites are present.
The fixtures forbid library-family/libc identities on the ABI-only controls
and forbid compiler findings on the text-only control. The system-profile
control positively requires both compiler and system-API subjects.

On the two initial controls, atomscan retains all prior findings modulo moved
IDs. The ABI/system control additionally exposes both repaired atoms, their
profile and the neutral system profile. Archive/member scores remain 8/6 for
that control and 7/5 for ABI-only. The unconsumed baseline ABI findings are not
rendered on the ABI-only control; the positive trace and the system-profile
control establish matching, not that absence from rendered JSON means no match.

`validate --soft`: **1,733/1,733 fixtures pass**, including 443 benign cases.
Strict `make validate` still reports **172 oversized directories**. There are
**zero mixed nodes**. No regression is observed in the fixture corpus; regex
coverage expansion and removal of unsupported library/intent inferences are
intentional changes, not a claim of universal score equivalence.

Logs: `/tmp/taxonomy-abi-repair-{positive,negative}-trace.log`,
`/tmp/taxonomy-abi-repair-{before,after}.json`,
`/tmp/taxonomy-abi-repair-soft-complete.log`,
`/tmp/taxonomy-abi-repair-strict.log`, and
`/tmp/taxonomy-abi-repair-final-verification.log`.

## Validator improvements and remaining work

Warn about anchored decorated-symbol regexes that omit the normalized spelling;
report actual normalization rather than banning underscores. Expand directory
references when reviewing dependency cycles: ordinary direct-reference checks
miss the system-fn cycle found here. Positive cycles may have other initiating
legs, so a review diagnostic should explain the cycle and its base evidence.

For duplicate predicates, compare effective scopes and contextual gates before
merging. The WSJ count's size scope was already enforced by its consumer; the
Mach-O entropy exclusion was not redundant and remains explicit. Transitive OR
subsumption also exposed the library alias, which redundantly included a
profile and one of its own legs.

The broader 172-directory cap debt, remaining Mesa references and other
misplaced binary metrics remain open. This repair closes the specific ABI
matching gap recorded by the previous audit.
