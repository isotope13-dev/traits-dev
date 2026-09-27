# XML operations and Base64 conversion direction

## Evidence and placement

The old XML cohort treated a node name, type annotation, property reference and
parser ProgID as Base64 decoding. An ordinary encoder and decoder both scored
44 as archives and both received the same suspicious decoder finding. Typed
number access and an arbitrary `Base64Data` element also matched decoder atoms.

Microsoft documents `nodeTypedValue` as a read/write property whose type is
selected independently; it supports numeric types and strings as well as binary
types. Thus neither the property nor a Base64 type declaration establishes
conversion direction. See the [property reference](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ms762308%28v%3Dvs.85%29).

The canonical boundaries are now documented in TAXONOMY.md:

- Generic DOM node operations belong in `data/collection/dom`. An element named
  `Base64Data` does not establish XML, Base64 processing or browser rendering.
- XML parser class references belong in `data/parse/xml`. COM is an activation
  mechanism; the specific MSXML parser reference follows its parsing capability.
- XML type declarations and typed-value references belong in `data/format/xml`.
  Object serialization remains `data/serialize/xml`.
- Actual directional conversion belongs in `data/{encode,decode}/base64`.

The [15-entry ledger](xml-codec-mapping.json) accounts for ten relocated
observations, the corrected decoding umbrella, two new directional observations,
and two renamed consumers. Relocated predicates, scopes, counts, exclusions and
confidence values are unchanged. References are rewritten to their canonical
homes. The element-plus-type composite changes from suspicious to notable:
ordinary type configuration is not evidence of malicious intent. Relocation and
accurate naming, rather than the criticality adjustment alone, correct its claim.

The two JScript objective consumers retain their requirements, scope and
criticality; their names/descriptions now state XML-type plus save/run API
combinations, without asserting a conversion or data-flow relationship. Their
broader malicious-intent and payload-flow precision still needs review. Passing
fixtures is not evidence that those relationships are proven.

## Directional observations

The new JavaScript structural matchers require adjacent statements that:

1. Construct an MSXML DOM document through `ActiveXObject`.
2. Create a node using that document.
3. Assign that node the `bin.base64` type.
4. Assign its text (decoding) or typed value (encoding).
5. Return its typed value (decoding) or text (encoding).

Captured receiver names must agree across those steps. The element label and
variable spelling do not determine direction. The rules accept `var`, `let` and
`const` declarations, and do not mistake reassignment between steps for a
continuous conversion. They intentionally cover this specific sequence, not
all MSXML codec implementations. Aliases, helper methods, other statement
arrangements, VBScript, PowerShell and compiled implementations retain their
neutral XML observations; they need their own relationship-aware directional
matchers. Broad token co-occurrence is not a valid fallback decoder.

## Verification

Four new benign fixture archives contain thirteen members: encoding and
decoding with original and renamed nodes, non-codec XML/DOM operations, and
seven broken-binding or wrong-type/class controls. Exact-ID checks pass on all
17 archive/member results. Encoding and decoding archives each score 9; ordinary
XML/DOM operations score 7, and unbound combinations score 8. Every positive
member gets its correct direction; none gets the opposite direction. Negative
members have no Base64 encode/decode finding.

Full soft validation passes **1,679/1,679 fixtures**. The ledger verifies against
current YAML, including unchanged conditions modulo canonical reference names.
Strict validation remains blocked by **175 oversized directories**, with zero
mixed rule directories. Current leaf counts: Base64 decoding 70, Base64 encoding
64, XML format operations 7, XML parsing 2, and generic DOM 1.

Logs: `/tmp/taxonomy-xml-{before,after,controls}.json`,
`/tmp/taxonomy-xml-soft-final.log`, `/tmp/taxonomy-xml-strict-final.log`.

## Remaining sibling work and validator opportunities

`ui/window/dom/{create,tree}` and `ui/window/dom-access` contain generic node
creation, mutation, traversal and querying beside browser-specific observations.
The documented contract chooses `data/collection/dom` for generic operations;
these siblings need matcher-by-matcher migration. For example `appendChild` and
`createTreeWalker` alone do not establish a displayed browser window. Browser
rendering, element activation and window interaction retain their UI homes.
Do not move the entire subtree based on its name.

The separate `decode/symbol-base64` leaf still partitions by matcher backend.
Its consolidation and the wider 85-rule cap migration remain open.

A validator could flag an operation aggregate that accepts prerequisite-only
observations (type annotation, parser identity or property name) without any
required conversion relationship. Identical-body checks alone cannot detect
this class of overstatement; nor do different property tokens prove independent
steps in a codec or loader.
