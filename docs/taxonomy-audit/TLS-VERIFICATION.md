# Canonical TLS verification-disable operation

Nineteen existing rules now live in
`micro-behaviors/communications/tls/verify/disable`: all fifteen rules from the
retired `http/ssl` leaf, curl's insecure switch from `http/tls`, and three
explicit Go/Node verification-disable settings from `socket/ssl`. Every moved
effective definition is unchanged, including matcher, criticality, confidence,
scope and exclusions. Language/client backend remains in filenames.

The [50-entry ledger](tls-verification-mapping.json) records nineteen moves and
thirty-one consumer rewrites. The [17-occurrence ancestor audit](tls-verification-ancestor-audit.json)
records directory semantics. The old leaf is removed; it is not retained as an
alias or a second home.

## Admission and exclusion contract

`communications` groups network communication subjects. Its `tls` child owns
transport-security operations independent of HTTP or an operating-system
socket API. `verify` refines peer authentication; `disable` refines explicit
settings/APIs that turn off certificate or hostname checking. TLS is registered
as an approved communication subject in the engine whitelist, not exempted from
any cap or structural policy.

Admit explicit verification-disable settings and the APIs/options that expose
them, including Requests, libcurl, PHP streams, Ruby OpenSSL, Go and Node forms.
Do not admit ordinary context creation, a callback which can make either trust
decision, a warning filter, generic TLS vocabulary, or an option whose value has
not been determined. These matchers are static evidence, not proof that a
particular execution took the insecure path. Existing exclusions and weak
matcher limitations are retained, not silently repaired during relocation.

HTTP owns request/response mechanics; socket operations own endpoint creation,
connection and acceptance. Using an HTTP client API does not give the same TLS
setting a second home. Actual HTTP/socket observations remain separately
available to consumers which require them.

## Directory-consumer decisions

Three consumers referenced the retired `http/ssl` directory. Two are Python-only
and one is PHP-only. Their references now use the canonical disable leaf. The
original fifteen members are preserved, and the four additions have disjoint
file scopes: Go/PE, JavaScript/TypeScript, or shell/PowerShell/batch/PE/GitHub
Actions. Therefore their effective descendant support does not widen in this
cohort. Re-audit these references before adding more Python/PHP forms; directory
membership is part of their matcher semantics.

Six references to the common `communications` ancestor keep the same descendants.
Eight HTTP/socket ancestor references intentionally lose TLS-only evidence:
disabling peer checks does not independently establish HTTP activity or a socket
operation. Do not broaden those consumers to all TLS merely to recreate the
previous misplaced support. The positive and default controls below retain
actual request/connect evidence where the source contains it.

## Verification

Five inert controls are checked into `testdata/benign` and registered in the
expectations: Python Requests verification disabled/default, Node TLS
verification disabled/default, and curl's insecure switch. Positive fixtures
require the new leaf; default-verification fixtures forbid it and retain the
ordinary TLS-context/connection prefix. Installed atomscan before/after findings
are equal modulo the migration map, including criticality and confidence, on all
five controls. These comparisons do not establish equivalence on every possible
ancestor consumer; the intentional semantic narrowing is documented above.

Current counts: canonical disable leaf **19**, retired HTTP SSL **0**, legacy
HTTP TLS **25 → 24**, socket SSL **85 → 82**. No new over-cap or mixed node is
introduced. This is the first operation-based TLS consolidation, not completion
of the broader TLS audit: remaining verification forms and unrelated subjects
still occupy legacy HTTP/socket leaves.

The engine whitelist change requires a rebuild. The isolated development
manifest was synchronized with the shared checkout's newly added DES dependency
for concurrent CFML work, retaining the existing local filefacts patch. Shared
manifests were not edited. Logs and snapshots live in
`/tmp/taxonomy-tls-verification/`.

Final rebuilt-checkout gate: **1,750/1,750 fixtures pass**, including **460 benign**.
Strict `make validate` exits **2**, reporting only **169 oversized directories**;
the new TLS subject is recognized. There are **zero mixed nodes**. No unrelated
trait-definition changes occurred between the effective snapshots used for the
50-entry ledger. This is a verified migration checkpoint; the overall plan and
remaining TLS operation audit are still open.
