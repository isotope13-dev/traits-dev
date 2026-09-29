# Cloud credential references: capability placement

## Decision

Literal endpoint paths, environment-variable names, and local config paths are
content clues. They belong with the probable capability they support, not in
`metadata/file/string/` or an attacker-objective leaf. A reference can raise the
likelihood that code can request or locate credentials; by itself it does not
show that a request or read occurred. The `objectives/credential-access/`
composites remain the place for a stronger credential-theft inference.

The boundary is documented in [TAXONOMY.md](../../TAXONOMY.md): provider HTTP
endpoint and request-path clues go under
`micro-behaviors/communications/http/services/<provider>/metadata/`; the shared
link-local metadata address belongs in `micro-behaviors/communications/http/services/cloud/`; provider
request headers belong in `communications/http/header/custom`. Environment
names go under `micro-behaviors/os/env/cloud/`, local credential/config paths
under `micro-behaviors/fs/path/credential/`, and authentication-source
selection under `micro-behaviors/os/security/auth/cloud/`.

## Migrations

| Previous rule | Canonical placement | Change |
|---|---|---|
| `objectives/credential-access/cloud/token/metadata::cloud-metadata-path-set` | `micro-behaviors/communications/http/services/aws::iam-credentials-path-reference` | Reuses the existing AWS credential-path capability instead of keeping a second objective-tier string matcher. |
| `...::cloud-env-secret-set` | `micro-behaviors/os/env/cloud::cloud-secret-environment-name-set` | Moves the same paired AWS/Azure environment-name matcher to its subject. |
| `...::cloud-config-path-set` | `micro-behaviors/fs/path/credential::cloud-config-path-set` | Moves the same Kubernetes/Docker config-path matcher to its subject. |
| `...::rust-cloud-metadata-endpoint-set` | `micro-behaviors/os/security/auth/cloud::rust-cloud-metadata-endpoint-reference` | Keeps the Rust-source OR grouping as a component capability. Its scope excludes arbitrary ELF files; ELF objective rules separately require Rust compiler evidence. |
| `metadata/file/string/cloud::{gcp-service-account-token-path,gcp-service-accounts-metadata-path,gcp-default-service-account-email-path}` | `micro-behaviors/communications/http/services/gcp::{gcp-service-account-token-path,gcp-service-accounts-metadata-path,gcp-default-service-account-email-path}` | Relocates the same provider-path matchers to GCP's HTTP-service leaf and remaps every consumer. |
| `metadata/file/string/cloud` AWS/Azure endpoint and request-path rules | `micro-behaviors/communications/http/services/{aws,azure}/metadata` | Moves content clues out of file metadata and into the provider service's metadata behavior. Matchers and suppressions are retained. |
| `metadata/file/string/cloud` Alibaba/Tencent endpoint rules | `micro-behaviors/communications/http/services/{alibaba,tencent}/metadata` | Gives provider-specific endpoints a consistent provider/metadata home and updates consumers. |
| `metadata/file/string/cloud::cloud-instance-metadata-link-local-host` | `micro-behaviors/communications/http/services/cloud::cloud-instance-metadata-link-local-host` | Keeps the shared link-local address clue in the cloud-service family because it does not identify one provider by itself. |
| `metadata/file/string/cloud` AWS token headers and `services/cloud::gcp-metadata-flavor-header` | `micro-behaviors/communications/http/header/custom` | HTTP headers describe request fields, not file metadata or endpoint paths. Consumers now use directory rule IDs; YAML filenames do not form part of an ID. |
| `metadata/file/string/cloud::gcp-default-credentials` | `micro-behaviors/fs/path/credential::gcp-default-credentials` | Places a local credential filename with other credential paths. |

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
- Focused synthetic JavaScript samples still match the relocated AWS, Azure,
  Alibaba, Tencent, generic cloud-host, and GCP endpoint/header capabilities.
  Current `make validate` continues to report the existing repository-wide
  backlog: 79 directories exceed the 100-rule cap, alongside unrelated
  taxonomy and matcher diagnostics. The relocated references produce no
  broken-reference diagnostics.
