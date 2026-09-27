# AST capture and observation-identity audit

**Follow-up:** the engine regression recorded below is [repaired and verified](ARCHIVE-VALIDATION.md). All 1,711 fixtures now pass with the rebuilt checkout engine. The failure details below retain the original audit evidence.

Six capture-free queries represented five observations: the two nested-array
queries were duplicates. Their effective conditions, scopes, confidence, size
and count restrictions were identical after trimming the query's trailing
newline. They now have one canonical home. All five queries have captures and
pass direct positive and negative checks.

The [12-entry ledger](ast-capture-mapping.json) records the rule changes and
consumer updates; every effective after-definition was verified. The
[17-consumer ancestor inventory](ast-capture-ancestor-audit.json) covers affected
source and destination prefixes. Neutral observations no longer supply
encoding, obfuscation, timing-evasion or malware-family identity merely through
their former ancestry. Exact consumers remain connected, except the retired
inactive timing aggregate described below.

## Classification decisions

- `js-this-bracket-access` and `js-new-this-bracket` retain their property/access
  and dispatch homes, scopes and exclusions. Each now captures its operation.
- The nested-array pair moves from encode/map and string/reconstruct to
  `data/collection/array::js-nested-array-pairs`, at notable. Array nesting does
  not establish table lookup, encoding or obfuscation. The size ceiling and
  count minimum remain unchanged. The query counts matching pairs, not distinct
  rows: several child arrays can yield multiple pair matches within one parent.
  Its name and description intentionally make no row-count claim.
- `js-augmented-identifier-append` becomes
  `data/arithmetic::js-addition-assignment-identifier`. `+=` can add numbers or
  concatenate strings; the query proves neither operand types nor decoding.
- `js-date-diff` becomes `data/arithmetic::js-identifier-subtraction` and loses
  inherited evasion annotations. Identifier subtraction does not establish
  dates. Its Date-call sibling moves to `time/query::js-date-call-cluster`,
  baseline: three Date calls do not establish a loop, proximity or evasion.
- `js-timing-evasion` is retired. It previously could not match because its
  subtraction leg had no capture. Enabling it would label three Date calls plus
  unrelated subtraction as evasion. It had no exact consumers; its two honest
  observations remain independently available. No detector is substituted for
  timing intent that the original matcher never established.
- The Nemucod `accumulator-eval-loader` helper moves to neutral eval as
  `js-accumulator-eval-cooccurrence`, at notable. Its eight-line proximity checks
  do not bind the initializer, addition and eval to the same variable and do not
  identify a family. Both Nemucod consumers retain this helper and their other
  conditions. The helper's description now states only co-occurrence.

## Controls and validation

Six new benign ZIPs cover this-access/construction, nested arrays, numeric and
string addition assignment, unrelated subtraction beside Date calls, nearby
nonmatching forms, and local accumulator/eval co-occurrence. Direct `test-rules`
checks match all five canonical queries on their positive controls and reject
all five on the shared negative control. In particular, one two-child nested
array falls below the retained count minimum, `holder[key]` is not `this[key]`,
and literal right-hand operands do not satisfy identifier-only arithmetic.

Atomscan comparisons of the first five archives before and after show no
suspicious or hostile findings. Scores are respectively: nested arrays 1/1 to
2/1; addition 1/1 to 2/1; subtraction with dates 1/1 to 2/1; this-access 2/1 to
4/3; negative control unchanged at 1/1 (archive/member). The sixth control scores
3/2 and emits the neutral eval helper without Nemucod identity. These scans use
the installed engine; direct query checks and `make validate` use the sibling
checkout's release engine. They are different binaries and must not be treated
as interchangeable validation evidence.

All six new controls pass the current corpus run. **The full corpus is not
green:** two runs of the checkout engine's `validate --soft` fail the existing
`npm-math-universe-aes-stage-loader.tgz` fixture, losing its required staged
payload finding and falling below its score/hostile-count floors. Strict
`make validate` reports only the **173 oversized directories**. There remain
**zero mixed nodes**.

### Isolated engine regression

The checkout release binary was rebuilt during this audit. With that same
binary, direct scans of the encrypted-stage fixture fail with both an isolated
before-rules tree and the current tree: scores 180 and 181, each with two hostile
findings. The installed engine invoked by atomscan detects the required staged
payload with both trees: scores 298 and 299, each with three hostile findings.
Thus this fixture failure is reproducible before these taxonomy edits and
cannot be repaired by reverting their classification changes. No expectation
was relaxed. Concurrent unrelated trait edits were excluded from this ledger.

The engine diff includes a new archive-wide retroactive suppression pass and
changed container composite evaluation. These are candidates for investigation,
not a proven diagnosis. Parent-level suppression must respect the member scope
of evidence; a build/test marker in one archive member must not erase a valid
ciphertext observation in another. Investigate this before claiming full-suite
success. Logs and same-engine comparisons are under `/tmp/taxonomy-ast-captures-*`.

## Follow-up

A textual inventory finds no remaining queries without an at-sign. This is only
a screening check: a robust validator must inspect compiled capture metadata,
including each query pattern, rather than accept an at-sign inside a literal or
comment. The current compile validator accepts valid but capture-free queries.

Duplicate detection should normalize insignificant surrounding query whitespace
before comparing AST matcher bodies; it missed the nested-array pair despite
otherwise identical effective rules. Do not normalize literal contents or
merge rules whose scopes, exclusions or thresholds differ.

The reconstruct leaf falls from 116 to 114, encode/map from four to three,
Nemucod from 77 to 76, and timing/evasion from 70 to 67. Destinations now contain
six array rules, 25 arithmetic rules, 41 time-query rules and 75 direct-eval
rules. The broader cap migration, neutral obfuscation measurements and remaining
relationship audits are still incomplete.
