# Network interfaces and wireless capabilities

This cohort relocates 14 WLAN/Bluetooth rules from the generic network-interface
leaf into the existing wireless-network leaf. The interface leaf decreases from
94 to 80 rules; wireless increases from 47 to 61. No new taxonomy level or
platform partition is introduced. Interface-specific content such as `veth`
and bridge names remains with probable interface capabilities.

| Subject | Canonical home | Boundary |
| --- | --- | --- |
| Generic adapters, interface addresses/status, virtual/bridge interfaces | `micro-behaviors/network/interface` | Evidence may be a string, path, API reference, or call. |
| WLAN client APIs, radio/network discovery, saved wireless profiles, Bluetooth devices | `micro-behaviors/hardware/wireless/network` | The wireless subject takes precedence over generic adapter mechanics. |
| Independent provider artifact identity | `well-known/lib` when adequately identified | A filename clue alone must not gain broader trusted-library semantics through a move. |

The `wlanapi.dll` reference and provider-basename clue both remain wireless
capability evidence. Moving the basename clue into `well-known/lib` would make
it participate in broad library suppressors; that would change unrelated
detection. The current move preserves its exact matcher and downgrade use.

The ten relocated atomic matcher bodies were compared with the complete
pre-move catalog; none had an identical atomic body elsewhere. The library-name
text matcher and artifact-path matcher share a value but describe distinct
observations and must not be merged merely because both contain `wlanapi.dll`.

All effective matchers, file/platform scopes, confidence, criticality,
exclusions, and downgrade conditions are preserved modulo reference paths.
The [mapping ledger](interface-wireless-mapping.json) records these effective
definitions. The [consumer audit](interface-wireless-consumer-audit.json) has
31 reference decisions:

- Exact references follow their moved rule, including the retained host-network
  composite's WLAN/Bluetooth legs.
- Four `any`-list consumers retain their original resolved member sets by
  adding the moved rules individually alongside the remaining interface leaf.
  This preserves the engine's member-based `needs` counting.
- The webhook consumer retains all 94 original network members and its 512-byte
  relationship. Its two IP-field alternatives now form a named OR composite so
  a field and network evidence are still both required.
- Ten ancestor references gain that field composite. They use Boolean presence
  without a raised `needs` threshold; both underlying fields were already
  members, so the OR supplies no new satisfying evidence or locations.

Eight inert PE controls cover interface exports, Bluetooth exports, WLAN
profile strings, the provider basename, a field alone, unrelated wireless
content, and nearby/distant evidence. All 136 original rule verdicts match the
captured baseline. The controls are compiled but never executed. Run
`python docs/taxonomy-audit/controls/interface-wireless/check.py` to reproduce
the comparison; it requires clang and lld-link.

`validate --soft` completed with 1,827/1,827 fixture cases passing and no mixed
nodes. `make validate` remains blocked by 166 oversized directories and the
reported description, regex, suppression, and scope debts. `git diff --check`
is clean. These results close this relocation cohort, not the whole audit.

The remaining interface inventory still warrants semantic cleanup: VPN/tunnel
configuration, domain-join status, route and neighbor queries, drive mappings,
and application package names need comparison with their corresponding
siblings. The under-cap count is not evidence that those placements are optimal.
