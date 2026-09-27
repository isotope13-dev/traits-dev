# Base64, computed calls and JSON conversion

This continuation audits the computed-call and JSON observations found during
[the Base64 support audit](BASE64-SUPPORT.md), including their JSON-parsing
siblings. The [ten-entry ledger](base64-calls-mapping.json) records effective
before/after definitions, updated homes and intentional predicate changes.

## Corrections

- `Buffer[...](..., variable)[...]()` requires neither a decoder method nor a
  Base64 argument. Its unchanged predicate now reports a computed method-call
  chain under `data/control-flow/dispatch`. Both objective consumers follow the
  canonical ID; their other conditions still supply intent.
- `JSON.parse(Buffer.from(...))` can parse an ordinary UTF-8 buffer. The unchanged
  predicate moves to `data/serialize/json`, with an accurate description.
- A Base64 word near any `.toString()` is not a conversion relationship. The old
  nearby-token rule is replaced by a structured matcher under JSON serialization
  requiring `JSON.parse` around `Buffer.from(input, "base64")`, either directly
  or through that result's `.toString()` call. It checks the second argument of
  the same Buffer call. The exact predicate is new; this is not described as an
  equivalent rename.
- The old JSON-to-file materializer now requires the structured conversion and
  a nearby write. Its name and description state proximity rather than claiming
  that the parsed value is the data written. The sharded-payload consumers use
  the new canonical conversion observation.
- The generic `base64-decoding` aggregate loses its directionless JSON-parse and
  nearby-token alternatives. Actual Base64 operations remain covered by the
  existing Buffer decoders.
- Four neighboring `JSON.parse` observations move from `data/parse/json` to
  `data/serialize/json`, following the existing object/representation contract.
  The lexical JWT-field extractors and jq query observation remain in parsing.
  No broad directory consumers needed expansion.
- A fifth neighbor, `eval("(" + expression + ")")`, does not establish JSON.
  It moves to `process/interpreter/eval/direct` as parenthesized expression
  evaluation. Its predicate and consuming conditions are preserved. Parentheses
  alone do not make arbitrary expression evaluation safe.

`TAXONOMY.md` now explicitly distinguishes these cases. No new directory was
created and no rule-count exemption was used.

## Controls and results

The unrelated-operation archive has a UTF-8 computed Buffer call and ordinary
UTF-8 JSON parsing beside an unrelated `'base64'` label and `label.toString()`.
It requires dispatch and JSON observations while forbidding Base64 decoding.
The retired nearby-token regex was also replayed with `cleave test-match` on the
same-line label control: it matches `'base64'; console.log(label.toString(`.
Thus the replacement removes a reproduced false relationship, not merely a
hypothetical one.

The positive conversion archive covers direct Buffer parsing and explicit
`.toString("utf8")`. Exact-ID inspection of the scan results confirms
`base64-buffer-json-parse` and the near-write composite on both members, and the
relational matcher is absent on both unrelated-operation members. The old
nearby-token rule missed the direct Buffer form because it required `.toString`.
The fixtures additionally enforce the appropriate directory prefixes and score
caps of 15. Last measured archive scores are 7 and 6 respectively.

A third benign control evaluates the parenthesized arithmetic expression
`1 + 2`; it requires expression evaluation and forbids JSON parse/serialization
findings, with a score cap of 10.

The full soft suite passes **1,673/1,673 fixtures**. Strict validation fails only
on **175 oversized directories**. All ten ledger definitions and migrated
references verify, and no mixed rule directories remain. Current leaf counts:

| Leaf | Rules |
|---|---:|
| `data/decode/base64` | 80 |
| `data/serialize/json` | 75 |
| `data/control-flow/dispatch` | 40 |
| `data/parse/json` | 3 |
| `process/interpreter/eval/direct` | 74 |

## Limits and remaining work

The new structured conversion handles nested, literal-Base64 Buffer calls.
It does not resolve aliases, dynamically selected encodings, computed method
names or a decoded value passed through separate statements before JSON.parse.
Those require proven relationships, not reinstating a nearby word test. Its
near-write consumer still proves proximity, not the written value's identity.

Some existing consumers use the parenthesized-expression observation as a benign
exclusion. This relocation preserves those conditions; it does not certify their
safety. A separate exclusion audit should require actual benign context rather
than inferring it from parentheses.

The XML observations inspected at the start of this pass remain unmoved. Their
`nodeTypedValue`/`bin.base64` references and generic document/element construction
must be separated from directional conversion evidence. Resolve the boundary
between generic DOM/tree operations, XML-specific typing and rendering-specific
DOM operations before migration; a chosen `Base64Data` element name does not
establish either an XML implementation or decoding. The symbol-backend and
format branches identified in BASE64-SUPPORT.md also remain open.

A validator review candidate is a conversion claim assembled only from generic
calls and nearby format words. Duplicate-body checks cannot detect that missing
relationship. Another is a generic parse leg paired with a structured conversion
that already includes that parse: these may be overlapping evidence rather than
two independent observations, and scope/relationship checks should precede any
merge or removal.
