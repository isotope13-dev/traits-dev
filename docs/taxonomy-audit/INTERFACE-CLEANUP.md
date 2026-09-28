# Remaining network-interface placements

This cohort moves seven definitions whose subjects are more specific than a
generic network-interface capability. The measured interface leaf decreases
from 59 to 52 rules.

| Observation | Canonical home | Reason |
| --- | --- | --- |
| `GetBestInterfaceEx` route selection | `micro-behaviors/os/network/route` | Resolves an outbound route and its selected interface. |
| Windows domain-join status | `micro-behaviors/os/sysinfo/hostname` | Describes the host's domain identity; it does not query directory contents. |
| Android VPN `addRoute` method and source call | `micro-behaviors/os/network/tunnel` | Configures routes inside a VPN tunnel builder. |
| Node `exec("net use")` | `micro-behaviors/os/network/share` | Enumerates mapped remote drives. |
| Route-and-adapter composite | `micro-behaviors/os/sysinfo/network` | Combines route-table and adapter observations into a host-network profile. |
| Host-network fingerprint composite | `micro-behaviors/os/sysinfo/network` | Combines adapter, route, wireless, Bluetooth, and domain clues. |

The last composite keeps its matcher and scope but its description now says
“Multiple host network and domain clues,” matching the existing requirement
for any three of twelve signals. This prevents the previous description from
claiming that every match enumerates adapters and routes.

The [mapping ledger](interface-residual-mapping.json) captures all seven
effective before/after definitions. Matchers, scopes, criticality, confidence,
exclusions, and composite conditions are preserved modulo reference paths,
with the noted description correction. The [consumer audit](interface-residual-consumer-audit.json)
records exact reference updates and how five host-profile/exfiltration consumers
retain their former inputs after the interface directory narrows.

The two Android package-name literals remain in the interface leaf for now.
They contribute to both VPN app-selection and Play Store identity-masquerade
composites. The literal by itself establishes a referenced package name, not
interface use or VPN routing, so its evidence needs a distinct, contextual
classification before a relocation can be defended.

Soft validation passes all 1,829 current fixtures, including 530 benign cases.
Strict `make validate` reports 57 catalog-wide issues, including 165 directories
above the 85-rule cap; this cohort introduces no broken references or new scope
errors. `git diff --check` is clean. The larger taxonomy audit remains open.
