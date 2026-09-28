# Cloud credential references: capability placement

## Decision

Literal endpoint paths, environment-variable names, and local config paths are
content clues. They belong with the probable capability they support, not in
`metadata/file/string/` or an attacker-objective leaf. A reference can raise the
likelihood that code can request or locate credentials; by itself it does not
show that a request or read occurred. The `objectives/credential-access/`
composites remain the place for a stronger credential-theft inference.

The boundary is documented in [TAXONOMY.md](../../TAXONOMY.md): provider HTTP
endpoint paths go under `micro-behaviors/communications/http/services/<provider>/`,
environment names under `micro-behaviors/os/env/cloud/`, local credential/config
paths under `micro-behaviors/fs/path/credential/`, and authentication-source
selection under `micro-behaviors/os/security/auth/cloud/`.

## Migrations

| Previous rule | Canonical placement | Change |
|---|---|---|
| `objectives/credential-access/cloud/token/metadata::cloud-metadata-path-set` | `micro-behaviors/communications/http/services/aws::iam-credentials-path-reference` | Reuses the existing AWS credential-path capability instead of keeping a second objective-tier string matcher. |
| `...::cloud-env-secret-set` | `micro-behaviors/os/env/cloud::cloud-secret-environment-name-set` | Moves the same paired AWS/Azure environment-name matcher to its subject. |
| `...::cloud-config-path-set` | `micro-behaviors/fs/path/credential::cloud-config-path-set` | Moves the same Kubernetes/Docker config-path matcher to its subject. |
| `...::rust-cloud-metadata-endpoint-set` | `micro-behaviors/os/security/auth/cloud::rust-cloud-metadata-endpoint-reference` | Keeps the Rust-source OR grouping as a component capability. Its scope excludes arbitrary ELF files; ELF objective rules separately require Rust compiler evidence. |
| `metadata/file/string/cloud::{gcp-service-account-token-path,gcp-service-accounts-metadata-path,gcp-default-service-account-email-path}` | `micro-behaviors/communications/http/services/gcp::{gcp-service-account-token-path,gcp-service-accounts-metadata-path,gcp-default-service-account-email-path}` | Relocates the same provider-path matchers to GCP's HTTP-service leaf and remaps every consumer. |

The Rust source objective still requires a cloud endpoint reference plus either
the paired secret environment names or the paired credential/config paths. Its
ELF variants require the Rust compiler marker and a provider-specific endpoint,
so ordinary ELF libraries that bundle cloud strings do not gain a Rust
credential-sweep finding.

The exact matcher and consumer map is in
[cloud-credential-reference-mapping.json](cloud-credential-reference-mapping.json).

## Verification

- `rust-cloud-metadata-reference.rs` retains the notable AWS endpoint-path
  capability and does not match the hostile Rust sweep without the secret or
  config-name cluster.
- A focused temporary Rust source with the AWS endpoint and both secret-name
  markers still matches `rust-cloud-credential-sweep`.
- The benign MongoDB provider ELF retains neutral cloud-path/environment
  capability findings, but lacks the Rust compiler evidence required by the
  ELF hostile composites.
- The soft fixture gate passes **1,837/1,837** samples. Strict validation still
  reports **59 quality/cap issues**, including **165 directories** over the
  combined 85-rule limit; these are independent of the fixture gate.
