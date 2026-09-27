# Computed dispatch and member-access audit

Thirteen observations now live with the operations their matchers establish:
ten in `micro-behaviors/data/control-flow/dispatch`, three in
`micro-behaviors/data/property/access`. Six came from shell/WSH and seven from
obfuscation/syntax. A redundant WScript OR aggregate was retired in favor of its
bracket-access atom. The [107-entry ledger](computed-dispatch-mapping.json)
records thirteen relocations, one retirement and ninety-three consumer updates;
every effective after-definition was checked against the current rules.

## Placement and evidence

A method named Run, zero/Boolean arguments, or hexadecimal arithmetic does not
establish a shell receiver or hidden-window semantics. Argument `2` does not
establish file overwrite. A function-selected method or constructor does not
establish decoding. WScript bracket access includes ordinary Echo calls. These
observations retain their scopes and matching conditions, with one AST repair
below. Five former suspicious atoms now have neutral notable criticality;
unsupported attack annotations were removed. Exact objective consumers retain
their references and must supply the additional evidence their claims require.

The pure-OR WScript aggregate added no independent observation: its function-key
prefix alternative is a subset of bracket access with the same scope. Its
removal is intentional consolidation, not a claim of identical confidence.

### AST repair

The former dynamic-property-function-concat query had no capture. Both the
individual and batched evaluators increment match counts only for captures, so
it could not emit a finding. Its new `js-addition-indexed-access` query captures
the access and explicitly requires addition in the `index` field. Direct traces
now match `items[offset + 1]` and reject `(offset + 1)[0]` and `items[offset]`.
This is an intentional coverage repair, not a predicate-preserving relocation.
There are no exact consumers of this atom. It now contributes neutral property
evidence rather than hypothetical obfuscation evidence.

## Consumer audit

The [ancestor-reference inventory](computed-dispatch-ancestor-audit.json)
records 75 consumers of WSH/shell/process or syntax/obfuscation ancestors.
Broad shell and obfuscation references intentionally stop inheriting the moved
neutral syntax; many other consumers already exclude it through file scope.
Exact references were redirected. The long-tail build-config rule retains all
six moved WSH alternatives in its generic-code `any` condition, while its
separate required obfuscation condition still requires obfuscation evidence.
Neutral calls were not added as substitutes for that required evidence.

Full corpus checks constrain regression risk but do not prove unchanged
behavior for untested inputs. The above broad-reference tightening is intended.

## Verification

Five new benign ZIP fixtures cover custom Run/computed calls, WScript Echo,
function-selected methods/constructors, indexed addition and its negative.

| Control | Before archive/member scores | After |
|---|---|---|
| Custom calls | 4 / 3 (VBS member 1) | 3 / 2 (VBS member 1) |
| WScript Echo | 40 / 39 | 4 / 3 |
| Function-selected calls | 42 / 41 | 2 / 1 |
| Indexed addition | 1 / 1 | 2 / 1 after AST repair |
| Addition outside index | Not measured before | 1 / 1 |

Before the AST repair, all nine archive/member comparisons retained rendered
finding identities modulo the mapping. Criticality differences were confined
to the four relocated suspicious atoms observed in these controls. The repaired
index query adds the intended notable property observation. Fixture assertions
check directory placement and risk; direct traces additionally check the exact
AST atom. Rendered atomscan output omits some lower-criticality components, so
it is not a complete internal-match inventory.

`validate --soft` passes **1,705/1,705 fixtures**: hostile 261, benign 415,
does-nothing 175, drop-exec 45, supply-chain corpus 572, impact-wipe 66,
obfuscation 82, reverse-shell 24, simple-stealer 65. Strict `make validate`
exits 2 with only **173 oversized directories**. There are **zero mixed nodes**.
The existing engine binary used the local dependency build described in
[the preceding report](PROPERTY-OPERATIONS.md); this cohort changes no engine code.

| Leaf | Before | After |
|---|---:|---:|
| data/control-flow/dispatch | 59 | 69 |
| data/property/access | 23 | 26 |
| anti-static/obfuscation/syntax | 109 | 101 |
| process/create/shell/wsh | 33 | 27 |

## Remaining precision work and validator candidates

- Full fixture evaluation exposes neutral measurements still under obfuscation:
  `computed-call-property-access-ast`, `const-return-padding-ratio`,
  `hex-string-arithmetic`, and `mixed-hex-decimal`. New fixtures forbid the
  corrected syntax hierarchy, not every obfuscation descendant. These remaining
  findings need their own matcher, sibling and consumer audit.
- Six further queries have no capture: property/access `js-this-bracket-access`,
  encode/map `js-nested-array-table-mapping`, dispatch `js-new-this-bracket`,
  string/reconstruct `js-nested-array-table-mapping-dup` and
  `js-augmented-identifier-append`, timing/evasion `js-date-diff`. Validate capture
  presence using compiled queries, not a textual at-sign check; literals can
  contain at-signs. Repair with positive/negative controls before enabling them.
- The nested-array pair is also a duplicate candidate. Compare full effective
  predicates and scopes before merging; identical bodies alone do not establish
  equivalent exclusions or count thresholds.
- The remaining COM-overwrite and WSH-loader composites still need relationship
  audits: independent syntax co-occurrence does not prove receiver binding or
  data flow. Relocating their atoms does not itself fix those claims.
- The syntax leaf still exceeds 85, and the wider migration remains incomplete.
