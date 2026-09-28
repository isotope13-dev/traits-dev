# Close the analyzer-based DNS AST directory

`objectives/exfiltration/dns/ast` is retired. Its last two rules described a
formatted domain-like string and its co-occurrence with binary packing, neither
of which establishes exfiltration or AST manipulation by the specimen.

The formatting atom moves, with its regex, scope, confidence and exclusions
unchanged, to `micro-behaviors/data/string/concat::python-three-label-domain-fstring`.
Its name describes formatting; its criticality is notable for a neutral operation.
The existing `python-dotted-fstring` has a different predicate: bare identifiers,
two interpolations and no required fixed suffix. The migrated rule allows
expression text and requires three dotted interpolations plus a suffix shape.
Do not merge these scopes without evaluating the changed consumers.

The `subdomain-exfil-pattern` composite is retired. A network-order packing call
anywhere beside a formatted domain does not demonstrate that data reaches that
domain, a DNS query or a remote endpoint. Remove only this optional branch from
`dns-exfil-data-channel`; preserve its remaining label-construction and encoding
branches and the hostile consumers' other requirements.

## Evidence and verification

The [three-entry ledger](dns-ast-closure-mapping.json) records relocation,
retirement and the consumer change; [ancestor decisions](dns-ast-closure-ancestor-audit.json)
cover loss of generic formatting/packing as exfiltration support.

Two inert archives containing `client.py` are registered, never executed.
Ordinary member names prevent the outer regression-directory path from masking
the detections through test-harness exclusions:

- `dns-format-and-pack.zip` formats a service endpoint, packs a version number,
  reads a credential and resolves `localhost`. Neither the credential nor the
  formatted endpoint is sent. Before, the old profile enabled hostile
  `dns-exfiltration`. After, useful formatting/serialization observations remain,
  with no suspicious or hostile findings. Its expectation forbids DNS exfiltration.
- `dns-identity-label-egress.zip` puts hostname/user identity into a queried name
  under `.invalid`. Its complete emitted ID/criticality set is unchanged,
  including hostile `python-identity-label-dns-beacon`. The expectation requires
  the DNS lookup exfiltration prefix and a hostile finding.

Reports and snapshots are under `/tmp/taxonomy-dns-ast-close/`. The positive
control proves retention of this identity-label path, not all conceivable DNS
exfiltration. The removed profile was unsupported evidence; the remaining
co-occurrence-based channel claims still need review.

Final checkout `validate --soft` passes **1,767/1,767 fixtures** (264 hostile,
475 benign, other groups unchanged). Structural inventory reports **168
oversized directories** and zero mixed nodes. Strict `make validate` still
fails those budgets and concurrent PowerShell work: two overlong descriptions,
two overlong regexes in `well-known/lib/runtime/scripted/powershell-utils`, and
two excessive-suppression rules. No DNS-specific loading error is reported.
Production reference search confirms no remaining `objectives/exfiltration/dns/ast`
references. The full fixture pass is not a claim that strict validation or the
overall taxonomy migration is complete.

## Placement contract and remaining work

An AST matcher is implementation detail. Formatting belongs with string
construction, byte-order packing with serialization/framing, and manipulating
an AST with the actual AST operation. A string that resembles a domain does not
prove resolution or transfer. References should compose these canonical
observations only when the added evidence supports the resulting claim.

The neighboring `dns/prep` branch still includes variable names and ordinary
concatenation as suspicious exfiltration evidence, and `dns/lookup` mixes neutral
lookup facts with outbound transfer objectives. Continue the broader migration
from [the neighboring DNS audit](DNS-PLACEHOLDERS.md); closing `ast` does not
resolve those branches.
