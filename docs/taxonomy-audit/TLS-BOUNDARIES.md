# TLS evidence versus security vocabulary and generic I/O

Two misplaced atoms leave `micro-behaviors/communications/socket/ssl`:

| Previous observation | Canonical home | Boundary |
|---|---|---|
| `domain-intel-skill-context` | `metadata/file/string/security::domain-intel-text` | The substring `domain_intel` establishes vocabulary, not TLS use, scanner identity, or a benign purpose. |
| `nspr-io-functions` | `micro-behaviors/process/io/stream::nspr-io-functions` | PR_Read/Write/Send/Recv names indicate I/O API references; this combined matcher does not distinguish file/socket backing or establish encryption. |

Both predicates retain their effective file/platform scope, confidence and
criticality. The [four-entry ledger](tls-boundaries-mapping.json) also records
two consumer repairs. No alias remains in the old TLS leaf.

The `tls-library-io-api-pair` composite keeps its two-of-three condition and
references canonical NSPR I/O. Two alternatives require TLS APIs, so meeting
two of the three still requires at least one TLS observation. Its description
is now “TLS API with corroborating I/O”; it no longer describes NSPR itself as
a TLS library.

The full-verification-disabled composite loses the `domain_intel` exclusion.
Before, adding that word to Python code which sets both `check_hostname=False`
and `verify_mode=ssl.CERT_NONE` suppressed the finding. Exact checkout traces
reproduce the old skip and show the repaired match. A name fragment does not
invalidate those settings. Other exclusions are unchanged; this is not an
endorsement of their breadth.

## Consumer audit and checks

The [eight-occurrence ancestor audit](tls-boundaries-ancestor-audit.json) covers
positive references to communications/socket ancestors. They intentionally lose
unsupported communications evidence from bare security vocabulary or generic
I/O. Existing TLS observations remain. Neither destination has an ancestor
consumer in the inspected snapshot. There were no external exact consumers of
the moved IDs.

Three inert source fixtures are registered in `testdata/expectations.toml`:

- `domain-word.py`: security vocabulary, with TLS findings forbidden.
- `nspr-io.c`: generic stream I/O, with TLS findings forbidden.
- `domain-disabled-tls.py`: vocabulary plus disabled TLS checks. The fixture gate
  requires TLS and vocabulary; the exact before/after trace verifies the repaired
  full-verification-disabled composite rather than relying on a broad prefix.

The full soft gate passes **1,745/1,745 fixtures**, including **455 benign**.
Socket SSL falls **87 → 85**; stream I/O rises **31 → 32** and security vocabulary
**22 → 23**. There are **169 oversized directories**, with **zero mixed nodes**.
The matching change to the disabled-verification composite is intentional; no
universal verdict/score equivalence is claimed. Logs, effective snapshots and
read-only installed atomscan comparisons are in `/tmp/taxonomy-tls-boundaries/`.

## Remaining TLS organization work

The sibling inventory shows overlap between `socket/ssl`, `http/ssl` and
`http/tls`. Protocol spelling is not a semantic distinction. `http/tls` contains
SecureTransport handshake/I/O/trust, Go X509 keypair loading, fingerprint
customization, and warning suppression; several do not require HTTP. Meanwhile
verification-disable observations are spread across all three leaves.

Plan the remaining rules together by supported operation: context/session
creation, handshake, record I/O, peer verification, certificate/key handling,
and handshake fingerprint customization. Warning suppression belongs with the
warning operation and does not itself prove verification bypass. An unspecified
parameter or interface reference must retain its weaker claim; it cannot be
forced into an operation it does not establish. HTTP-specific conjunctions can
remain under HTTP when the matcher actually requires that protocol. Determine
all broad-observation destinations and ancestor consumer changes before any
leaf becomes an internal directory; keep the leaf-only rule throughout.

Two precision issues also require focused controls before migration:
`connect-comp` currently accepts context creation as connection evidence, and
several x64 API claims match argument constants plus an unresolved call without
establishing the called function. Do not treat either as verified operation
identity merely because the current fixtures pass.

Strict `make validate` exits **2**, reporting only the **169 cap violations**.
Installed atomscan findings for the NSPR-only and word-only controls are
unchanged modulo the ID map; the disabled-TLS control gains exactly the intended
notable `tls-validation-fully-disabled` finding. Five concurrent CFML read and
webshell changes are excluded from the owned ledger and left intact; the full
fixture result describes the shared worktree.
