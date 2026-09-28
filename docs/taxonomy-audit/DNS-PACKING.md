# Binary packing is not DNS identity

Follow-up: [DNS construction repair](DNS-CONSTRUCTION.md) addresses the generic
packing composite and part of the legacy `dns/ast` debt recorded below.

Six primitives were misfiled as DNS or exfiltration observations. Their actual
predicates recognize `struct.pack` format strings, without proving a DNS record
or a transfer. Five fixed integer/length layouts now belong in
`micro-behaviors/data/buffer/integer-codec`; the arbitrary network-order format
call belongs in `micro-behaviors/data/serialize/binary`.

The [ten-entry ledger](dns-packing-mapping.json) records six relocations and four
consumer rewrites. Predicates, scope, confidence, criticality and exclusions are
unchanged. The [ten ancestor decisions](dns-packing-ancestor-audit.json) document
removal of generic packing as communications or exfiltration evidence. Direct
references in the DNS construction, subdomain profile and two parser-confusion
exploit composites now point to the canonical primitives. No aliases remain.

## Boundaries and evidence

- Integer widths, byte order and length-prefix fields belong with integer
  framing. `!HHIH` and `!HBB` are layout observations, not resource-record or
  DNSKEY identities. The generic `!` format can include non-integer fields and
  belongs with binary serialization.
- The pair-pattern text matcher contains `1, 1` without complete argument
  boundaries; it does not prove that both values equal one. The name deliberately
  avoids claiming exact values or DNS qtype/class. Text matchers still admit
  syntax in comments; symbol matchers have different evidence guarantees.
- The [network-order control](controls/dns-packing/binary-pack-formats.py) has
  ordinary record packing and no DNS operation. All six old primitives matched;
  all six relocated primitives match. The complete emitted ID/criticality set
  agrees modulo the six IDs. The [little-endian counterpart](controls/dns-packing/binary-pack-little-endian.py)
  matches none of these six, with its complete finding set unchanged.
- These source files are read-only scan controls, never executed. Installed
  atomscan reports and effective-rule snapshots are under
  `/tmp/taxonomy-dns-packing/`. They are separate from the checkout fixture gate.

The final checkout fixture gate passes **1,762/1,762** with `validate --soft`.
Strict validation reports only the existing **168 oversized directories**;
structural inventory finds zero mixed nodes. Effective-rule comparison confirms
exactly the ten ledger changes and no other changed production definitions in
this cohort. Integer-codec now has 33 rules; binary serialization has 18.

## Remaining DNS evidence debt

The network-order control also matches the unchanged suspicious
`python-dns-construction` composite. Its two-of-five condition can be satisfied
by generic packing alone; neither a DNS-named function nor qname construction is
required. This cohort corrects the primitive catalog, not that composite's
coverage. Next, establish protocol-specific admission with positive packet
construction and negative arbitrary-record controls, inspect every consuming
objective, and record any intentional narrowing. Do not simply lower the false
profile's criticality or treat this control as proof of DNS.

The analyzer-based `objectives/exfiltration/dns/ast` leaf still has five rules.
Its length-prefix atom overlaps an existing integer-codec atom but uses a broader
unfinished-expression regex; merging them mechanically would change coverage.
Its ASCII loop and dotted-string observations require their own homes, and its
composites currently overstate exfiltration. The broader neighboring audit and
consolidation order remain in [DNS placeholders](DNS-PLACEHOLDERS.md).
