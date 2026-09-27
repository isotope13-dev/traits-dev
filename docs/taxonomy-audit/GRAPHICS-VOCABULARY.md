# Graphics vocabulary, provider interfaces and Mesa identity

Nine observations move to `metadata/file/string/graphics`; three weak library
reference aggregates are retired. The retired `abi-graphics` leaf is removed.
The [30-entry ledger](graphics-vocabulary-mapping.json) records effective
before/after definitions, and the [ancestor audit](graphics-vocabulary-ancestor-audit.json)
records decisions for 74 directory-reference occurrences. This is a checkpoint,
not an endorsement of the remaining mixed subjects in `dylib/library/family`.

## Placement contract

| Evidence | Home | Boundary |
|---|---|---|
| Graphics API, backend or driver words, namespace fragments, library filename/path text | `metadata/file/string/graphics` | Vocabulary alone proves neither rendering nor independent library identity. This specific subject takes precedence over generic filename text in `file/string/file`; end-user product names remain `file/string/application-name`. |
| Parsed graphics API imports | `metadata/binary/symbols/imports` | Imported declaration, not arbitrary text or a provider's exported interface. |
| Exported provider entrypoint | `metadata/binary/symbols/exports` | Export-kind symbol; a text mention or import does not qualify. |
| Declared provider SONAME and its conjunction with an exported interface | `metadata/binary/linking/runtime` | Structured linking identity facts, not loading behavior. |
| Mesa library identity supported by provider name/interface plus Mesa and DRI evidence | `well-known/app/system/drivers/mesa` | An identity inference about the artifact; graphics words alone are insufficient. |
| Actual graphics operations or embedded implementation evidence establishing such operations | `micro-behaviors/ui/graphics/draw` or the specific operation | Classify the supported capability, regardless of language or static/dynamic implementation. |

All nine relocated predicates retain their effective scopes, confidence,
criticality and conditions. Exact consumers follow the new IDs. Mesa identity
now requires a graphics-provider SONAME, a matching exported interface, Mesa
namespace text and DRI references. `system-lib-marker` uses the structured
provider/interface pair instead of the old graphics-word OR aggregate.
The SONAME is self-declared: this is stronger identity evidence, not an
unforgeable authenticity test.

## Consumer decisions and additional repairs

The family/library ancestor exclusions and downgrades intentionally lose
word-only graphics evidence. A library-name fragment must not suppress an
otherwise useful behavior. Independently declared provider/interface evidence
remains available through `system-lib-marker`; no weak aliases are recreated.

Five linking/runtime exclusions already include the generic ELF SONAME fact,
so the new name/interface conjunction adds no Boolean support where that
existing fact's scope applies. The new declarations also allow Windows ELF
scope; equivalence outside the existing Unix/Android SONAME scope is not
claimed. The pre-existing `so-rootkit-behavior` exclusion of the entire linking
namespace is broader than its comment about excluding PIE executables. This
needs a separate positive/negative audit: a normal SONAME is not proof that an
ELF is a PIE executable.

Two identical few/high-entropy-string composites are consolidated into
`metadata/file/string/count::large-macho-high-entropy-string-profile`. The
conjunction is unchanged, but its description and notable criticality describe
a neutral count profile rather than asserted obfuscation. Four obfuscation
ancestor consumers intentionally lose this unsupported concealment evidence.
A low-code-entropy exclusion is expressed through a named atom, preserving its
metric threshold. Shared compiler scopes move into defaults without changing
effective definitions.

The PTY/socket/fork capability loses its broad metadata/library/signing
downgrade and remains notable. Those facts do not invalidate the capability;
wrapping excess downgrade alternatives in another aggregate would only evade
the validator. The other metadata/binary ancestor consumer, timing sandbox
evasion, is PE/DLL-only: the changed Mach-O and ELF facts do not intersect its
file scope.

## Evidence and limits

Four inert compiled controls are included in benign fixture ZIPs, together with
source, and checked through `testdata/expectations.toml`:

- Graphics words without a provider name or interface: vocabulary, no Mesa identity.
- Declared provider name and exported interface, with Mesa/DRI words: Mesa identity.
- Provider name without interface: no Mesa identity.
- Interface without provider name: no Mesa identity.

Read-only atomscan comparisons of installed `libGLX_mesa.so.0.0.0` and
`libEGL_mesa.so.0.0.0` retain Mesa identity. The word-only synthetic ELF loses its
false Mesa identity. The declared-provider control retains it. New structured
facts change scores, so this is not a claim of score equivalence. Other Mesa
variants are not exhaustively covered by these two real-library samples.
Installed atomscan and the checkout validator are separate executables.

The checkout soft gate passes **1,737/1,737 fixtures**, including **447 benign**.
Strict `make validate` exits **2**, with only the oversized-directory policy
reported: **171 directories remain over 85 rules**. There are **zero mixed
rule/child nodes**. `dylib/library/family` falls **88 → 82**; this resolves one
cap violation without inventing a new technique. The overall migration remains
incomplete until strict validation and the remaining placement audits pass.

Validation logs: `/tmp/taxonomy-graphics-vocabulary-soft-final.log` and
`/tmp/taxonomy-graphics-vocabulary-strict.log`. Before/after installed scans:
`/tmp/taxonomy-graphics-vocabulary-before.json` and
`/tmp/taxonomy-graphics-vocabulary-after.json`.

## Validator follow-up

Identical effective composites should be merge candidates even across tiers.
Transitive OR subsumption also merits a diagnostic: the old Mesa identity
required an OR aggregate that already contained its other required Mesa leg,
so its apparent conjunction added no independent evidence. Compare resolved
predicates and scopes before suggesting a simplification; different scope or
exclusions can make superficially identical bodies distinct observations.
