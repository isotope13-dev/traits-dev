# TLS initialization is not an established connection

Follow-up: [Native-host fixture review](NATIVE-HOST-FIXTURE.md) examines the
archive and resolves the concurrent fixture discrepancy documented below.

Five setup observations move to `micro-behaviors/communications/tls/initialize`:
SSL_CTX_new, TLS_client_method, SSL_new, Python default-context creation, and
Node secure-context creation. The [nine-entry ledger](tls-initialization-mapping.json)
records five moves, three exact-consumer rewrites and retirement of `connect-comp`.
All primitive predicates, scopes, criticalities and confidence are unchanged.

The retired OR composite accepted SSL_connect **or** any of the three native
setup APIs and described the result as a connection. An exact checkout trace
matches it on the context-only inert ELF, which imports SSL_CTX_new and
TLS_client_method but no SSL_connect. It had no external exact consumers and
added no independent evidence beyond its legs. The connection API observation
remains available; setup is no longer labeled a connection by this roll-up.

## Placement contract

`tls/initialize` owns preparation of TLS configuration or per-connection state
before negotiation: creating a default/secure context, selecting the client
method, or allocating an SSL connection object. The rule name identifies which
object is prepared. One initialization leaf preserves the meaningful phase
boundary without creating separate directories for each API object type.
SSL_new allocates per-connection state; it must not be confused with the separate
TLS session-resumption/ticket concept.

Exclude connect/handshake operations, record I/O, credential provisioning,
explicit verification changes, and generic TLS vocabulary. API references remain
static capability evidence, not proof that a connection ran or succeeded.
Verification-disable forms retain `tls/verify/disable`; ordinary initialization
must never enter that leaf merely because it configures TLS.

The remaining Python `context.wrap_socket` matcher needs its own receiver/type
review before migration; its source receiver name alone is not a resolved type.
This cohort does not strengthen that existing matcher or claim the legacy socket
SSL leaf is fully organized.

## Consumers and controls

The [eight-occurrence ancestor audit](tls-initialization-ancestor-audit.json)
records two socket references which intentionally lose setup-only support and
six communications references which retain the same primitive observations.
Those six do not require multiple descendant findings; retiring the redundant
same-criticality OR preserves their Boolean support. The Cobalt Strike,
TripleCross and mysql2 exact consumers follow their original atoms to the new
home with unchanged conditions.

Three inert ELF/source ZIP controls distinguish context creation, connection
object allocation and SSL_connect API use. A fourth JavaScript control creates
only a secure context. Initialization controls require the new leaf and forbid
socket SSL/verification-disable findings; the connect control requires its
existing API evidence and forbids initialization/verification-disable findings.
Existing Python default-context and warning-plus-context fixture expectations
now require initialization specifically. No samples are executed.

The ELF controls were built with `cc -shared -fPIC -nostdlib
-Wl,--build-id=none`; their C sources are included in the ZIPs. Logs, effective
snapshots, the counterexample trace and installed atomscan before/after results
are under `/tmp/taxonomy-tls-setup/`. This cohort is a phase-based taxonomy repair,
not a claim of universal runtime or score equivalence.

## Validation result and concurrent-work limitation

The five installed before/after control scans agree modulo the ID map and
retired roll-up. Initialization has **5 rules** and legacy socket SSL falls
**76 → 70**. There are **169 oversized directories** and **zero mixed nodes**.
Strict `make validate` exits **2**, reporting only that cap debt.

The last shared-worktree soft run passed the new controls but failed
`crx-dunelinenode-native-host-install-linux.crx`: concurrent retirement of
`extension-install-native-host-stager` left its hostile fixture expectation
unsatisfied. A separate concurrent cookie/native-bridge description edit is
also outside this ledger. These changes were not reverted in the shared tree.

To isolate this migration, a temporary copy of the current traits and fixtures
restored only `objectives/command-and-control/remote-command/extension/native-shell.yaml`
from the pre-migration effective snapshot. That isolated full suite passes
**1,759/1,759 fixtures**, including **469 benign**. This proves the observed
regression is outside the TLS changes; it is not a claim that the current shared
suite is green or that the retired detector should be restored. The temporary
copy is `/tmp/taxonomy-tls-setup/validation-overlay`; its result is
`soft-isolated.log`. The shared failure is recorded in `soft-current.log`.
The native-host fixture discrepancy and the broader taxonomy migration remain
open. Do not lower its expectation merely to obtain a passing gate without
reviewing the actual specimen and intended detector correction.
