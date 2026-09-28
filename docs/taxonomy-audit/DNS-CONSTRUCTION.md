# Coherent DNS label construction instead of generic framing

The preceding packing audit reproduced a false DNS-construction finding from
ordinary binary records. The old composite accepted any two of integer-field
packing, length framing, a qname terminator, and a DNS-named function. No actual
label-construction relationship was required.

## Implemented boundary

A new canonical `communications/dns/label::python-length-prefixed-label-loop`
requires one parsed loop that splits a dotted name and accumulates
`bytes([len(label)]) + label.encode('ascii')`. Capture equality binds both uses
to the loop variable; the operator must be addition/append. Variable names are
unconstrained. Comments, unrelated length arguments, and encoding elsewhere do
not establish this observation.

`dns/raw::python-dns-construction` now requires that observation plus a packing
or DNS name-construction leg, at leaf scope. Its criticality is notable: wire
construction is a neutral capability, not an exfiltration verdict. Existing
hostile consumers keep their criticality and other conditions. This deliberately
removes support from generic packing alone and from arbitrary two-of combinations.
It does not claim to cover every DNS encoder spelling; join comprehensions,
alternative encodings and library encoders need their own grounded observations.

The controls also exposed false exfiltration in the legacy `dns/ast` branch:

- ASCII accumulation moves to `data/encode/charset`, with its predicate and
  exception unchanged. Its criticality becomes notable for the neutral operation.
- The broad bytes/length-expression prefix moves intact to
  `data/buffer/integer-codec`. It describes an expression prefix; unlike the
  existing completed single-byte-length matcher, it does not require a closed
  expression or a simple identifier argument. These scopes are not merged here.
- The loose two-of `dns-label-manual-construction` composite is retired. Its
  consumer now references the coherent label encoder. Generic ASCII conversion
  and length framing alone no longer satisfy that DNS channel leg.

The [six-entry ledger](dns-construction-mapping.json) records every changed,
new or retired effective definition. The [20 consumer decisions](dns-construction-consumer-audit.json)
include four direct consumers of raw DNS construction, the replaced manual-label
reference and both old/new directory ancestors. All other effective definitions
are unchanged from the preceding cohort. No directory exemption or alias is added.

## Controls and limits

Three inert files are registered in the benign fixture suite, never executed:

| Control | Required result | Checkout cap |
|---|---|---|
| `dns-binary-pack-formats.py` | Keep packing observations; no raw-DNS finding | 3 |
| `dns-label-wire.py` | Coherent label encoding and raw construction; no DNS exfiltration | 5 |
| `dns-mismatched-label.py` | Different length argument must not establish raw DNS or exfiltration | 4 |

Read-only before/after atomscan reports and checkout logs are under
`/tmp/taxonomy-dns-construction/`. The original control lost the unsupported raw
DNS finding; the mismatched control also lost the loose manual-label objective.
The positive retained construction while its neutral operations ceased being
reported as suspicious exfiltration.

Final checkout `validate --soft` passes **1,765/1,765 fixtures**, including all
474 benign controls. Strict `make validate` reports only the existing **168
oversized directories**. Installed atomscan separately confirms that all three
controls have no suspicious or hostile findings and that only the coherent
encoder matches the new label atom and raw-construction composite. Its scores
(3, 4 and 3 for packing, coherent labels and mismatched labels) differ from the
checkout fixture scores above; they are not interchangeable.

A trial proximity constraint was removed before final validation: checkout
`test-rules` reported no source lines for the AST leg, so it did not demonstrate
that this leg was inside the requested window. The rule now states leaf scope
without claiming a checked line-distance relationship. Potential engine
improvement: carry AST match spans into proximity evaluation and flag constraints
whose required legs have no usable location. This needs a far-separated control
before proximity can be relied on.

Remaining work: two rules still occupy `dns/ast` (dotted f-string and a packing
co-occurrence profile); they do not describe AST manipulation and require their
own evidence/placement review. Downstream exfiltration composites still infer
relationships from co-occurrence; this cohort strengthens one input without
claiming a complete data-flow proof for those consumers. The broad framing prefix
and closed-expression atom also need an intentional coverage-aware consolidation.
