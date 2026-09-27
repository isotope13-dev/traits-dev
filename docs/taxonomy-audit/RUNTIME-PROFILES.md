# Runtime-indirection directory retirement

The remaining runtime-indirection directory is removed. The
[eight-entry ledger](runtime-profiles-mapping.json) records three relocations,
two retired aggregates and three explicit exclusion updates. All relocated
match conditions, scopes, platforms, thresholds, confidences and exclusions
are preserved modulo canonical references. Two composites change from
suspicious to notable because their observations are neutral; relocation and
accurate descriptions accompany this correction. Unsupported attack labels
are removed from the relocated rules.

## Placement and retirement

| Previous rule | Result | Reason |
|---|---|---|
| js-npm-malware-pattern | metadata/file/line::compact-long-lines-with-opaque-names | Long lines, entropy-heavy names and no comments establish a structural profile, not npm or malware. |
| js-runtime-string-conversion-profile | micro-behaviors/data/string/conversion::long-line-character-conversion-profile | Conversion plus line/name constraints remains a conversion observation; no bound decoder or concealed payload is proven. |
| js-sphinx-searchindex | metadata/file/literal::search-setindex-reference | Bare Search.setIndex text does not prove a call or generated provenance. |
| js-obfuscator-pattern | Retired; constituent observations remain | Three of four unrelated name/function/string/comment facts do not identify an obfuscator. The alternatives do not even require the same characteristic. |
| js-has-tests-without-obfuscation | Retired; package-completeness observation remains | This benign summary had no direct consumers. Five ancestor consumers could accept it as exfiltration evidence, which is unsupported. |

No umbrella alias remains in the retired directory. The first aggregate's
binary-only high-entropy-string leg is also a scope mismatch with its JS/TS
composite. Its string-count atom remains in the trojanized/backdoor branch and
needs a separate audit, including its graphics-context downgrade dependencies;
this retirement does not endorse that atom's placement.

The existing generated Sphinx matcher is more specific: it requires an anchored
index initializer with a recognized key. It remains in generated-build metadata.
Putting the bare reference there would broaden over 200 build-category consumer
occurrences, many of them exclusions. The final placement avoids that change.
The line and conversion siblings contain narrower observations; none is an
identical replacement for either preserved conjunction.

## Ancestor consumers

The [13-entry audit](runtime-profiles-ancestor-audit.json) records each decision.
Four obfuscation-category consumers retain actual concealment alternatives;
neutral profiles and bare API text are intentionally no longer sufficient.
Three identifier-category exclusions explicitly retain the relocated
Search.setIndex observation. The benign summary formerly referencing the
obfuscation category is retired rather than given broader admission.

The five exfiltration ancestors are MCP config injection, Windsurf MCP
injection, malicious-package-manifest, PowerShell history theft and hostile
browser stealer. They retain genuine exfiltration alternatives. Package tests
or declarations alone no longer satisfy that evidence. There are no direct
consumers of either retired aggregate; directory consumers are nevertheless
included in this audit. No new destination ancestor references broaden.

## Verification and limits

Four benign archives cover anonymous-function structure, long-line identifier
structure, ordinary character conversion with opaque identifiers, and a search
index reference. An isolated pre-change rule tree supplies the before scan;
only affected YAML files are reconstructed from the effective-rule snapshot.
The final comparison uses identical control bytes.

All eight archive/member finding sets are preserved modulo moved IDs on these
controls. The conversion composite intentionally changes from suspicious to
notable: its archive/member scores fall **43/42 → 6/5**. Other pairs remain
4/2, 2/1 and 2/1. This is an evidence-based verdict correction, not an assertion
that all taxonomy moves preserve model scores.

The conversion control positively exercises its relocated composite. The
anonymous-function and line controls do not activate the old obfuscator/npm
composites: existing source-context exclusions on no-comments-code suppress
that prerequisite. These are negative controls, not positive coverage claims
for those composites. The fixture gate verifies the underlying function/line
observations and absence of the retired objective directory. The search-index
control positively exercises the moved literal.

The final checkout-engine `validate --soft` passes **1,728/1,728 fixtures**,
including 438 benign cases. Strict `make validate` still fails solely on
**173 oversized directories**. The inventory has **zero mixed nodes**.
The tests demonstrate retained corpus coverage; the two aggregate retirements
and removal of neutral category evidence are intentional semantic changes,
not a claim of exhaustive detection equivalence outside the corpus.

Logs: `/tmp/taxonomy-runtime-profiles-{before,after}-final.json`,
`/tmp/taxonomy-runtime-profiles-soft-complete.log`, and
`/tmp/taxonomy-runtime-profiles-strict.log`.

## Follow-up

Continue the broader code-metrics, source/syntax and retry audits and resolve
the 173-directory cap debt. Review impossible or ineffective composite legs:
file-type compatibility and prerequisite exclusions can make a named heuristic
inactive without a syntax error. A validator improvement should flag proven
incompatibilities, not reject every cross-format composite (archive correlation
can intentionally combine formats). The binary string-count atom and its
library/graphics dependencies remain a concrete next audit candidate.

Follow-up: [Binary observation audit](BINARY-OBSERVATIONS.md) relocates the
string-count dependency and its graphics declaration facts, preserving its
downgrade and documenting a separate ABI matching gap.
