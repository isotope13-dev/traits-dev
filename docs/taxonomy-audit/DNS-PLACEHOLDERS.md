# DNS placeholder retirement and neighboring taxonomy audit

## Implemented correction

Two atoms in `command-and-control/dns/tunneling/construction.yaml` searched for
literal `IMPOSSIBLE_MATCH_XYZZY_DNS_CONCAT` and
`IMPOSSIBLE_MATCH_XYZZY_DNS_PLUS`, despite claiming hex/domain construction.
These are not unsatisfiable predicates: a JavaScript file containing the strings
triggered both notable atoms and their suspicious tunneling OR composite.
Neither predicate detects the claimed operation.

Retire those atoms, their OR composite, and the exfiltration composite that
required the OR. Remove the retired branches from the Interactsh, NPM system
stealer and Iterators composites; retain their other conditions and criticality.
Do not replace the placeholders with a broad encoding atom, which would expand
hostile detection without proving data transport.

The [seven-entry ledger](dns-placeholders-mapping.json) records all effective
rule changes. The [six ancestor decisions](dns-placeholders-ancestor-audit.json)
include positive references and the CrystalX `unless` reference. Removing the
sentinels also removes their ability to suppress CrystalX; ordinary DNS and
exfiltration descendants remain available. No parent aliases are introduced.

The tunneling leaf decreases from 86 to 83 rules. Structural inventory reports
168 oversized directories and zero mixed nodes. Passing this leaf's budget does
not resolve the semantic defects below.

## Detection evidence

Two inert JavaScript controls were scanned before and after with installed
atomscan; neither was executed:

- `dns-placeholder-text.js` contains only the sentinel strings and console
  output. Before: two notable false atoms and one suspicious false tunneling
  composite. After: baseline observations only. Three baseline findings become
  visible in the rendered output after retirement; they are not new predicates.
  The checkout fixture score is 2, with a cap of 2 and DNS C2/exfiltration prefixes
  forbidden.
- `dns-chunked-egress.js` hex-encodes a payload, chunks it into dotted DNS labels,
  and supplies those labels to `resolve4` under a `.invalid` domain. Its complete
  emitted ID/criticality set is unchanged, including hostile
  `js-dns-tunneling-chunked-exfil` and `js-dns-exfiltration-chunking`. The fixture
  requires hostile detection and the DNS tunnel exfiltration prefix.

The intended coverage removal is sentinel-only evidence and dependent verdicts;
there is no claim that the fabricated predicates provided real construction
coverage. Controls verify a retained real construction path, not every possible
DNS tunnel implementation. Temporary snapshots and logs are under
`/tmp/taxonomy-dns-placeholders/`.

Final shared-checkout `validate --soft` passes **1,762/1,762 fixtures** (263
hostile, 471 benign, and the other seven groups unchanged from the preceding
checkpoint). Strict `make validate` exits 2 with only the 168 oversized-directory
policy violations. Effective-rule comparison confirms exactly seven changes;
all other production rules are unchanged from this cohort's snapshot.

## Neighbor audit and remaining migration

The current branches `command-and-control/dns/tunneling` and
`command-and-control/channel/tunnel/dns` both claim DNS command channels, without
a defensible boundary. Exfiltration's `dns/{encoded,lookup,tunnel,resolver,ast,prep}`
leaves mix different classification questions; encoded labels can simultaneously
be looked up through a resolver and used in a tunnel. `ast` describes the analyzer
in its Python rules, not AST manipulation by the specimen.

Audit and migrate by the observation supported, in this order:

1. Move neutral query, record-type, send/receive, encoding and string operations
   into their existing micro-behavior homes. Move generic field names and mere
   source identifiers into the appropriate metadata subject. For example,
   `tenantId`, `clientId` and `mailbox` do not individually establish DNS or Entra;
   `chunks(63)` alone does not establish DNS; `sendto(sd, pkt` does not establish
   DNS transport. Preserve each predicate's true claim, scope and consumers.
2. Separate actual inbound command tasking, payload acquisition, and outbound
   data transfer. Use the existing objective for each; data returning after a
   command can compose the canonical tasking and exfiltration observations.
   Retire overlapping DNS C2 branches only after auditing all their rules and
   exact/directory consumers. No single blanket move is justified yet.
3. Within a direction/objective, subdivide by a real transport mechanism only
   when needed: encoded query labels, response-carried tasking/payloads, or
   DNS-over-HTTPS. Record type and language do not independently establish intent.
   Do not use `lookup` versus `tunnel` to distinguish encoded-label transfers.
4. Review name-only claims (`dnsExecute`, `buildDnsQuery`, `commandAndControlViaDns`)
   and file-wide co-occurrence before treating them as flow. The QNX Zig profile
   currently infers hostile DNS C2 from response/send/receive runtime names and
   binary identity; that requires an evidence review, not a mechanical move.
5. Audit duplicate predicates and overlapping composites before any size-driven
   split. A smaller count achieved by retirement is not a taxonomy exemption.

The only other production file containing the same sentinel convention is
`well-known/malware/stealer/iterators/traits.yaml`; its `iterators-evasion-vastest`
atom still claims an evasion check while searching for a sentinel. Review its
family context separately; this cohort only removes its optional DNS consumer.

## Validator improvement candidate

Flag explicit disabled-rule sentinel conventions such as
`IMPOSSIBLE_MATCH_XYZZY_` in production matcher values. Treat these as a focused
review diagnostic, not a generic ban on unusual strings or a claim that a
predicate is mathematically impossible. A legitimate literal-signature use needs
an evidence-based name and placement. Disabled detection experiments should not
ship as behavior traits, and dependent composites need review when such an atom
is removed. Identical-body validation cannot catch this case: the two sentinel
bodies differ, while both are semantically invalid for their advertised claims.
