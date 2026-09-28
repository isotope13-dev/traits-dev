# Route tables and neighbor tables

This cohort relocates ten rules into `micro-behaviors/os/network/route` and
`micro-behaviors/os/network/neighbors`. Route-table APIs were filed beneath
`communications/socket/route`, while route and neighbor queries were mixed into
the generic interface leaf. A neighbor-cache flush was grouped with route-table
changes. The moves align each rule with the probable capability it supports.

| Subject | Canonical home | Boundary |
| --- | --- | --- |
| Interface identity, address, adapter status and interface configuration | `micro-behaviors/network/interface` | Network-device identity and properties. |
| Destination-to-next-hop routing entries and route lookup | `micro-behaviors/os/network/route` | Includes command queries, route mutation APIs and best-route table lookups. |
| IP-to-link neighbor mappings, ARP tables and neighbor-cache operations | `micro-behaviors/os/network/neighbors` | Includes cache queries and flushes; these do not establish route-table changes. |
| Socket endpoints and communication protocols | `micro-behaviors/communications/socket` and protocol leaves | Transport communication is separate from OS routing configuration. |

Evidence form does not change the placement: a command or API reference can
support the same probable capability. The rule description still says whether
the observed evidence is a query, mutation, or reference.

The [mapping ledger](route-neighbor-mapping.json) records the before/after
effective definitions for all ten moves. Nine atomics and one composite retain
their matcher bodies, scopes, criticality, confidence, exclusions, and other
conditions; references are normalized through the new paths. The existing
`arp-table-query` rule remains in the neighbor leaf beside the moved
`ip-neigh-show` rule.

The [consumer audit](route-neighbor-consumer-audit.json) records the affected
reference decisions. Five host-profile and exfiltration composites that used
the broad interface leaf retain its former route/neighbor evidence as explicit
references. Their other conditions and proximity limits are unchanged. Exact
references to route and neighbor queries now point to their canonical leaves.
Two interface composites explicitly reference the relocated Windows route-table
query API.

Seven broader communications selectors lose the route-table API members they
previously inherited from the misplaced `communications/socket/route` leaf.
This is an intentional semantic narrowing: route manipulation and neighbor
cache operations alone do not establish socket communication, Empire network
activity, or DDoS mechanics. Those consumers keep the communication evidence
their names and other required legs describe.

Soft validation passes all 1,827 fixture cases. Strict `make validate` remains
blocked by existing catalog-wide cap and quality issues; this cohort adds no
cap exception. The route/neighbor split adds precision without adding platform,
language, or file-format hierarchy levels.
