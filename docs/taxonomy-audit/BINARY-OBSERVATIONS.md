# Binary observations: string counts, ABI symbols and graphics declarations

Follow-up: [Graphics vocabulary and provider identity](GRAPHICS-VOCABULARY.md)
records the subsequent graphics placement, Mesa identity, duplicate count-profile
and validation-hygiene repairs. Counts and destinations below are historical.

Eleven observations move to their semantic metadata subjects. The
[38-entry ledger](binary-observations-mapping.json) records eleven relocations
and twenty-seven consumer updates. Predicates, scope, confidence, thresholds,
exclusions and downgrade logic are preserved modulo canonical references.
One pure count changes from suspicious to notable; every other criticality is
unchanged. Unsupported attack labels are removed from relocated observations.

## Placement

| Observation | Canonical subject | Boundary |
|---|---|---|
| At least 20, 200 or 450 high-entropy strings; at most 20 | metadata/file/string/count | Counts across the binary, not a section, trojanized backdoor or proven concealment. Thresholds/scopes/exclusions differ; these are not duplicate predicates. |
| One to five extracted strings | metadata/file/string/count::binary-strings-one-to-five | Previously named no-strings, despite a minimum of one. |
| Large PE with at most 128 strings | metadata/file/string/count::large-pe-strings-at-most-128 | A size-conditioned string count; importless/packed intent belongs to consumers. |
| C++-style and __gxx_ symbol prefixes, plus their OR profile | metadata/binary/symbols/compiler | ABI/runtime declarations, not graphics or a particular library artifact. |
| Import-kind GL/EGL/Vulkan API declarations | metadata/binary/symbols/imports::graphics-api-import | A declared API import, not proof of drawing or loading a library. |
| GL/EGL/Vulkan library filename text | metadata/file/string/file::graphics-runtime-library-name | Filename text, not a resolved dependency or renderer identity. |

This is not a blanket move of embedded library evidence into metadata. A
fingerprint establishing a technique still belongs with that technique. These
matchers establish declarations, names and measurements. The three remaining
Mesa-oriented references in abi-graphics need their own precise graphics
placement; the mixed legacy category is not endorsed by this partial retirement.

The binary-metrics/shape leaf falls **88→85**, resolving its cap violation
without adding a directory. Its other rules still require semantic review.
The other counts are: abi-graphics 8→3, trojanized/backdoor 37→36,
section/prose 32→30, symbol/compiler 3→6, symbol/imports 54→55,
file/string/count 2→8 and file/string/file 34→35.

## Consumers and duplicate candidates

The [13-entry ancestor audit](binary-observations-ancestor-audit.json) records
all decisions. Three shape-category exclusions explicitly retain all three
moved shape string counts. Two binary-category downgrades retain the two moved
section/prose counts. Four concealment consumers intentionally stop accepting
neutral counts as sufficient obfuscation evidence. Existing library-family
composites still reference the canonical ABI and graphics observations, keeping
the corresponding broad library-category alternatives available.

The string-count rule's graphics downgrade is preserved and now uses neutral
import/filename facts. Six explicit consumers of the formerly suspicious
20-string observation still reference it; their contextual requirements remain.

No relocated atomic has an identical `if` body elsewhere in the snapshot.
The family-level C++ composite nevertheless has a redundant alternative: it
accepts the ABI OR profile or one of that profile's own legs. Its broader scope
and the compiler-prefix matching issue below need review before consolidation.
This is a candidate for transitive composite-subsumption validation, distinct
from identical matcher-body detection. Directory references must not be treated
as interchangeable merely because their names or some current members overlap.

## Controls and verification

Two benign ZIPs include reproducible C sources and inert shared objects, compiled
with `cc -shared -fPIC -nostdlib -Wl,--build-id=none`; neither object is executed.
One embeds a deterministic printable-string table. The other declares graphics
and GNU ABI imports and carries a library filename.

The metric's implementation uses a **6-bit-per-byte entropy floor**. The first
alphanumeric control did not meet it. The final table includes 700 broader
printable strings; the checkout-engine trace reports **275 qualifying strings**
and matches both the 20- and 200-string rules. This is a positive test for those
thresholds, not a claim that every input string survives extraction. The
450-string rule retains its PE/DLL scope and is not positively exercised by ELF.

Before/after atomscan scans use identical final control bytes and an isolated
pre-change rule snapshot. All six archive/member finding sets are preserved
modulo relocated IDs. The only criticality difference is the intentional
20-string correction (suspicious→notable). Entropy archive/member scores change
**39/36→5/2**; its C source stays 1. Graphics archive/member scores change
**7/6→8/7** despite unchanged criticalities, illustrating path-dependent scoring.
The fixture checks require string counts, graphics import and filename subjects.

The final checkout-engine `validate --soft` passes **1,730/1,730 fixtures**,
including 440 benign cases. Strict `make validate` now reports **172 oversized
directories**, down from 173. There are **zero mixed nodes**. The corpus and
controls support retained coverage; neutral-count removal from concealment
category evidence is intentional, not a claim of universal score equivalence.

## Existing ABI matching gap — unresolved

The ABI control initially failed a compiler-prefix fixture requirement.
`readelf -Ws` confirms `_ZStFixture` and `__gxx_personality_v0`, but direct
checkout-engine traces match neither atom nor their composite. The isolated
pre-change tree produces the same three misses. Symbol matching strips leading
underscores, while regexes such as `^__gxx_` retain them; RULES.md already warns
that regex patterns are not normalized.

The final fixture positively requires the graphics observations, not the
unimplemented ABI match. This audit preserves those existing predicates and
records the gap rather than declaring a successful compiler-identity test.
Repair the regexes together with their consumers: newly active generic ABI
facts would flow through library-family exclusions and could suppress real
behavior. Review that implication before merely removing underscores.
A validator could warn about anchored decorated-name regexes against normalized
symbol input, with examples of actual normalized symbols. Treat it as a semantic
heuristic, not a universal ban on underscores in symbol regexes.

Logs: `/tmp/taxonomy-binary-observations-before-final.json`,
`/tmp/taxonomy-binary-observations-after-complete.json`,
`/tmp/taxonomy-binary-observations-positive-trace.log`,
`/tmp/taxonomy-binary-observations-abi-{before-,}trace.log`,
`/tmp/taxonomy-binary-observations-soft-complete.log`, and
`/tmp/taxonomy-binary-observations-strict-complete.log`.

Follow-up: [ABI repair](ABI-REPAIR.md) closes the normalization gap, removes
the unsupported library alias, and audits consumers before activating the
compiler observations. The unresolved note above is the historical snapshot.
