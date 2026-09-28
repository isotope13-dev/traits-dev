# Port references are not Docker or TLS operations

Three runtime atoms inferred Docker/authentication/transport from port text or a
nearby service word. They now live in `metadata/file/string/network`:

| Former runtime ID | Canonical metadata ID |
|---|---|
| `docker-api-port-2375` | `port-2375-reference` |
| `docker-api-port-2376` | `port-2376-reference` |
| `docker-api-port-reference` | `docker-near-2375-text` |
| `docker-remote-api-ports` | `ports-2375-and-2376` |

The first two match colon/TCP port references, not a selected protocol or
successful connection. The third matches the Docker word near 2375, without
establishing runtime activity. All retain their matchers, scope, confidence and
notable criticality. The port-pair composite now uses the equivalent explicit
`all:` of both canonical atoms instead of `any:` with `needs: 2`.

The separate `objectives/discovery/network/scan/cloud-services::docker-port-pair`
is retired as the same two-port observation. Its only exact consumer,
`cloud-management-port-cluster`, now references the canonical metadata pair.
That consumer retains its scripts/binaries scope and file scope, so the canonical
pair's existing Go coverage cannot widen it. The old component label and scanning
ATT&CK annotation are not retained as another copy of a neutral port fact.
Neither criticality nor directory placement should depend on which parent uses it.

Five surviving consumers change. Kinsing's container-reference context explicitly
retains only the Docker-word association; bare numbers no longer establish that
context. Runtime-based tooling suppressions no longer inherit these literals.
Other exact consumers retain port corroboration alongside their independent
lifecycle, mount, privilege or scanning evidence. A comment claiming port 2375
proved unauthenticated access was corrected. The mapping ledger contains five
dispositions; the consumer audit records 14 direct/ancestor decisions.

## Verification

Read-only atomscan before/after retains port literals and the Docker-word
association at their new IDs and the same criticalities. A different service on
2375 is accurately labeled as a port reference. Numbers 23750/23760 do not match.
The pair still requires both distinct ports, and contributes one leg to its
port-cluster consumer.

Four new ZIP fixtures require the metadata subject and forbid runtime/discovery
claims for those standalone observations. All **1,802/1,802 fixtures pass**.
Runtime now contains **77 rules**; **166 oversized directories and zero mixed
nodes** remain. No old IDs or compatibility aliases remain. Strict validation
still has separate hygiene/scope/suppression debt and the oversized directories.

## Follow-up

The sibling cloud-scan leaf still contains labeled port vocabulary, port clusters
and provider catalogs alongside actual probing. Those facts need the same
placement discipline. Its Docker scanning objective and the container escape/
worm consumers also need relationship audits: co-occurrence does not prove that
a probe, deployment or unauthenticated connection reached the referenced port.
This migration preserves their independent existing gates; it does not certify
those larger intent claims.

Validator improvement: normalize an `all:` over N distinct references and an
`any:` over the same references with `needs: N` when proposing duplicate merges.
Then compare effective scope, exclusions and consumers before consolidating.
The differing scope and criticality here required an explicit consumer audit;
syntactic similarity alone would not justify merging blindly.
