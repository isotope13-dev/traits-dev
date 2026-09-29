# Install-hook recon/exfil cohort audit

The `objectives/supply-chain/recon-exfil/install-hook` leaf has **178 rules**
(59 atomics, 119 composites) against the uniform 100-rule cap. It is a legacy
trigger bucket, not a coherent malware capability. Install time answers
*when* a behavior runs; the source or result answers *what the rule detects*.
Do not reduce the count by creating `install-hook/<language>` or another
trigger/form bucket. The directory should be retired after rules are moved,
merged, or retired on evidence.

## Completed source-based moves

- Nine AWS IMDS/ECS credential-query rules moved to
  `objectives/credential-access/cloud/token/metadata`. The postinstall
  credential-to-HTTP composite in the legacy leaf references the canonical
  credential-query composite; exfiltration consumers reference the moved
  credential atoms.
- The Node host-identity/process command chain moved to
  `objectives/discovery/system/profile`.
- The JavaScript curl call carrying variable query data moved to
  `micro-behaviors/communications/http/curl`.
- The install-hook/OOB host-profile export composite moved to
  `objectives/exfiltration/stealer/system-info/profile`; it requires the
  install-hook file, host-profile discovery, an OOB endpoint, and transfer
  evidence. A synthetic JavaScript positive matches through the new path.
- Alibaba and Tencent cloud metadata endpoint clues moved to the existing
  neutral cloud-service endpoint leaf, where they extend its canonical
  endpoint-reference composite. The duplicate Alibaba matcher formerly in the
  Rust discovery file was merged into that same source-neutral atom; all
  consumers now reference the shared ID.

Matcher bodies for the relocated atomic conditions remain unchanged. The
path change intentionally changes their directory feature and corrects the
ATT&CK mapping where a trigger default had been applied to a discovery atom.
The source leaf fell from 194 at the earlier checkpoint to **178** and remains
over cap by 78. The duplicate endpoint rule and redundant local endpoint
aggregator were consolidated rather than retained as a second signal.

## Sibling audit and destination headroom

Counts below are the current combined rule counts before further moves. They
are capacity checks, not placement instructions.

| Existing sibling / canonical home | Rules | Remaining capacity | Boundary for this cohort |
|---|---:|---:|---|
| `exfiltration/stealer/cloud` | 27 | 73 | Cloud account/configuration material that is required to leave. |
| `exfiltration/stealer/system-info/profile` | 87 | 13 | A transmitted host report requiring multiple host-data fields/classes. Do not send every host or install beacon here. |
| `exfiltration/stealer/system-info/identity` | 38 | 62 | Host/account identity fields that leave; not platform or process inventories. |
| `exfiltration/stealer/system-info/network` | 12 | 88 | Interface, route, address, or network-configuration data that leaves. |
| `exfiltration/stealer/env` | 64 | 36 | Process or package environment values that leave; a read without transfer belongs to credential access or a capability. |
| `exfiltration/stealer/file` | 70 | 30 | File contents that leave without a more specific data class. |
| `exfiltration/stealer/credential` | 42 | 58 | Credentials leaving, but not a more specific source such as cloud tokens or environment secrets. |
| `exfiltration/stealer/multi-source` | 40 | 60 | Two or more independent source classes required together; `any` alternatives do not qualify. |
| `discovery/system/profile` | 78 | 22 | Host-profile queries with no required transfer. |
| `micro-behaviors/communications/http/curl` | 50 | 50 | Curl invocation, request, or transfer mechanics without an asserted sensitive source or attacker objective. |
| `micro-behaviors/communications/http/services/cloud` | 40 | 60 | Provider endpoint references and cloud service protocol behavior; an endpoint mention alone does not prove a metadata request. |
| `exfiltration/oob` | 139 | over cap | Not a general destination: this subtree is already over cap, and endpoint identity alone does not establish source or transfer. |

The main collision is discovery versus theft: the same host fields can support
`discovery/system/profile` when queried, but `stealer/system-info/profile` only
when the composite requires their outbound transfer. Cloud metadata has a
similar boundary: token acquisition belongs in credential access; cloud data
that is required to leave belongs in `stealer/cloud`. The OOB service, HTTP
client, install hook, or package ecosystem is contextual evidence and does not
choose the source leaf.

## Remaining file-group review

These groups must be assigned per rule by required evidence. Counts describe
the current source leaf; a file is not a taxonomy category.

| Source file | Rules | Review target / unresolved question |
|---|---:|---|
| `cloud-metadata.yaml` | 35 | Route cloud credential acquisition to credential access and actual cloud-data transfers to `stealer/cloud`. Move reusable URL/client mechanics to capability homes. Review the database-client name atoms and `/data` output composites: names alone do not prove a query, and output redirection alone does not prove the data source. Collapse package lifecycle wrappers when they duplicate a canonical source-plus-transfer result. |
| `git-remote.yaml` | 1 | Decide from the required remote operation whether this is communications/C2, build-system behavior, or a supply-chain trust result; “runs during build” alone is not sufficient. |
| `node-http-preinstall.yaml` | 5 | Split the identity, host-profile, credential, and public-IP cases by the data actually required to leave. Keep package scope/context as evidence; do not retain a generic “install beacon” home for differently sourced exports. |
| `npm-webhook-beacon.yaml` | 5 | Environment values, public IP, and host profile have distinct source leaves. The generic install-hook wrapper needs an explicit required source contract or should be consolidated with its source-specific consumers. |
| `php.yaml` | 1 | Host-profile-to-OOB behavior is a source/result candidate for `stealer/system-info/profile`; preserve any PHP/runtime implementation detail in the filename/scope. |
| `postinstall-curl-beacon.yaml` | 10 | User identity piped into a confirmed HTTP body belongs to `stealer/system-info/identity`; the host-profile beacon belongs to `system-info/profile`. The endpoint and curl mechanics belong to neutral HTTP/OOB leaves. The JSON POST composite with only generic command output does not establish a stable stolen-data source and needs matcher review before placement. |
| `preinstall-local-recon.yaml` | 2 | Separate metadata-service fingerprinting from process inventory; keep discovery-only behavior in discovery. Move to a stealer source only when an outbound leg is required. |
| `pypi-exfil.yaml` | 57 | This is the largest remaining file cohort. Classify each export by required data: environment, file snapshot, system identity/profile, or other concrete source. Route setup/build lifecycle facts as references. Retire stubs/placeholders that do not establish a behavior; do not put the whole PyPI cohort into one language-specific leaf. |
| `pypi-hatch.yaml` | 1 | Route by the host fields and transfer required by the matcher; build-hook context is a reference. |
| `pypi-urllib-environment.yaml` | 1 | Environment telemetry with a transfer leg is a candidate for `stealer/env`; confirm that the required matchers actually bind environment values to that transfer. |
| `recon.yaml` | 29 | Review each chain by its collected source and sink. Host identity/profile, public-IP/network data, secrets, DNS callback, and generic command output are not interchangeable. Drop wrapper composites whose only distinction is install phase if a canonical result already captures them. |
| `rust-build.yaml` | 31 | Separate host identity/profile, environment, Git diff/source files, and generic telemetry. A build script is a trigger; use neutral HTTP/crypto/process homes for reusable mechanics. Preserve build evidence in composites only when the package/build context is required for the supply-chain claim. |

The largest false-organization risk is converting the table into one new
subdirectory per source file, language, ecosystem, HTTP client, or lifecycle
phase. Those are implementation or trigger axes. The allowed split is by the
single capability/result question each leaf answers, with required source and
transfer evidence determining exfiltration placement. Where the present
matcher cannot choose one source, record the gap and tighten, split, merge, or
retire it before moving it.

## Validation observation

The cap audit found an identical Alibaba endpoint matcher in two directories:
one install-hook-scoped rule and one Rust-scoped discovery rule. They now share
one neutral cloud-endpoint atom with the union of their supported file types.
The audited exact-body groups touching over-cap directories fell from 64 to 63
(144 to 142 member rows); global groups fell from 428 to 427. A validator
improvement worth considering is a non-blocking cross-directory warning for
identical `if` bodies even when file-type scopes are disjoint, showing the
scope/default differences and suggesting one canonical home. Keep it advisory:
disjoint scope, exclusions, or verdict settings may be intentional and need
human review rather than automatic merging.

The latest current-tree audit (2026-09-28) reports **79** over-cap directories
and **1,966** excess rules at the 100-rule limit. The static cap checker confirms
this leaf's 178-rule count. `make validate` still runs a prebuilt Cleave binary
whose taxonomy whitelist does not know the already-added
`micro-behaviors/communications/transfer` directory; it reports that path as
unknown, plus the existing catalog findings. Rebuilding the adjacent Cleave
checkout remains blocked by an unrelated `stng::decode_xor_fat_macho` source
API mismatch. The focused synthetic tests for the moved JavaScript profile
atom, curl-query atom, and host-profile/OOB composite pass.
