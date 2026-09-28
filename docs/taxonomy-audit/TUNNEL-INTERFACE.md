# OS tunnel interfaces and application proxy tunnels

This cohort moves 27 rules into `micro-behaviors/os/network/tunnel`: 18 from
the generic interface leaf and nine from application proxy tunnels. The
interface leaf decreases from 80 to 62 rules; proxy tunnels decrease from 89
to 80. The new OS tunnel leaf has 27 rules. These are semantic distinctions,
not platform partitions or exceptions to the 85-rule cap.

| Subject | Canonical home | Boundary |
| --- | --- | --- |
| Generic adapters, addresses, bridge and virtual Ethernet interfaces | `micro-behaviors/network/interface` | Distinctive names, paths, APIs, and calls support probable interface interaction. |
| Virtual packet endpoints and configured tunnel interfaces | `micro-behaviors/os/network/tunnel` | TUN/TAP, WinTun, VPN interface builders and application selection, and tunnel-interface configuration. |
| Application/session forwarding through a proxy tunnel | `micro-behaviors/communications/proxy/tunnel` | Application relay and proxy-service mechanisms rather than OS interface control. |

String evidence follows its probable capability. A device-path or provider-name
reference need not prove execution to belong here. Rule descriptions retain the
distinction between observing a reference and observing a specific operation.

The moves cover five TUN/TAP rules, four WinTun/TAP adapter rules, five tunnel
configuration rules, and thirteen VPN service/builder rules. Two generic route
rules and two application-package literals remain in the interface leaf pending
their own semantic audit; their presence is not an accepted placement precedent.

The [mapping ledger](tunnel-interface-mapping.json) records all 27 effective
before/after definitions. Matchers, scopes, criticality, confidence, exclusions,
and other conditions are identical modulo reference paths. The 20 moved atomic
matcher bodies have no identical peers in the captured catalog.

The [consumer audit](tunnel-interface-consumer-audit.json) records 50 reference
decisions. All twelve affected directory-reference consumer member sets are
preserved modulo the ID mapping. Consumers retain explicit references to moved
rules alongside the remaining directory reference so member-based counting
continues to select the original evidence.

One PowerShell Empire consumer requires both an exploit-function alternative
and communications evidence. A named OR composite now groups its original two
function alternatives, preserving that conjunction while adding the relocated
communications members explicitly. This adds one rule to an already oversized
family leaf, increasing it from 89 to 90. That leaf remains outstanding cap debt;
there is no exemption. No ancestor directory consumers gain this helper.

Eleven inert controls cover TUN references, nearby/distant tunnel configuration
and webhook evidence, VPN source and manifests, package-only negatives, WinTun
references, and Empire consumers with and without tunnel evidence. All 330
verdicts match the pre-move baseline. Generated binaries are never executed.
Run `python docs/taxonomy-audit/controls/tunnel-interface/check.py` to reproduce
the comparison; compilation requires clang and lld-link.

Soft validation passes all 1,827 fixture cases. Strict `make validate` still
fails with 165 oversized directories and reported description, regex, scope,
and suppression issues. The catalog has zero mixed parent/leaf rule nodes.
These results validate this relocation, not the entire taxonomy.

Follow-up work includes route and neighbor operations, mapped-drive enumeration,
domain-join evidence, and application-name literals in the interface leaf;
generic socket/buffer/callback and SOCKS evidence in the proxy-tunnel leaf;
and a defensible split or consolidation of the oversized Empire family leaf.
