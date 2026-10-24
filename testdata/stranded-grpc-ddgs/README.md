# Stranded gRPC-Go and DDGS members

All eight requested extracted members are **BENIGN**. Both archive verdicts
remain **MALICIOUS**, as fixed by the task. Ten markers were written beside
their corresponding inputs. Their exact notes, input hashes, finding counts,
and classifier probabilities are recorded in `review.json`.

The original archive SHA-256 values match the supplied values. Forager fetched
the upstream reference releases into the session scratch directory, retaining
their `.forage.json` provenance:

- `https://proxy.golang.org/google.golang.org/grpc/@v/v1.57.0.zip`
- `https://github.com/deedy5/ddgs/archive/refs/tags/v9.9.1.zip`

Comparison of uncompressed contents, after removing the module/archive root
prefixes, found all 802 gRPC-Go files and all 42 DDGS files byte-identical to
those references. There were no added, removed, changed, duplicate-named, or
out-of-prefix members. These downloaded references are comparison artifacts,
not replacements for the original samples. The archive convictions were not
reconsidered from this comparison.

## Member behavior and judgement

| Member | Traced behavior supporting BENIGN |
|---|---|
| `test/end2end_test.go` | `Test` dispatches gRPC subtests. Helpers start localhost or temporary Unix-socket RPC servers, load test X.509 keys, dial those servers, exchange HTTP/2/protobuf messages, and tear them down. `init` enables channelz diagnostics. The explicit `InsecureSkipVerify` setting is real and remains detected. |
| `test/balancer_test.go` | Registers test balancers, creates subconnections, exercises metadata, credentials, resolver updates, and load-balancing state transitions. Servers and channels are test fixtures with cleanup. Insecure transport and networking observations remain. |
| `xds/internal/resolver/xds_resolver_test.go` | Runs a fake xDS client/management server, supplies bootstrap configurations, and checks listener/route updates, error handling, weighted routing, and RPC lifetime. `xxhash.Sum64String("/products")` computes a request-routing checksum. It is not encryption or credential harvesting. |
| `vet.sh` | Requires a clean Git tree before installing its exit trap. Installs pinned developer tools; on GitHub Actions, downloads and extracts the specified protoc release and invokes its version check. Runs generation, lint, vet, formatting, and module checks. Its hard reset undoes changes from that guarded workflow. Downloads, extraction, execution, and Git-reset observations remain. |
| `ddgs/cli.py` | Click handlers accept user search options, call DDGS, and optionally export JSON/CSV or download result URLs with primp and a thread pool. Downloads are written as result files, without launching their contents. The CLI entry point invokes these handlers. |
| `.github/workflows/python-publish.yml` | A release-created event checks out source, installs build tools, builds distributions, and invokes Twine upload. The Actions secret supplies Twine's password; the bytes contain no unrelated collection or destination. |
| `ddgs/http_client2.py` | A temporary search HTTP adapter constructs httpx, delegates requests, returns response fields, and translates exceptions. It randomizes TLS cipher ordering and HTTP/2 settings, temporarily patches the HTTP/2 initialization method, and restores that method on context exit. Verification defaults to enabled, with a genuine caller-selected False branch. The credentialed example URL is documentation, not evidence of credential transmission. |
| `ddgs/engines/bing.py` | Configures Bing GET search, sets locale cookies, constructs pagination/date filters, and parses results. `unwrap_bing_url` strips the URL wrapper prefix, pads and URL-safe-Base64-decodes the result URL; its output replaces a result link and is never evaluated as code. |

The affirmative evidence is the ordinary, readable execution paths and their
agreement with each component's purpose, corroborated by exact upstream bytes.
Installation history, operator intent, runtime traffic, and the evidence behind
the archive convictions were not supplied. The members were assessed on their
own behavior, without inheriting either archive's verdict.

## Trait changes

- Added primp HTTP-client initialization and GET-call observations. GET matches
  follow the receiver back to a primp constructor, rather than arbitrary `.get`.
- Added an explicit `method="GET"` request observation using the same call's
  named argument, TLS-context cipher configuration using receiver provenance,
  and the conditional False verification branch in httpx/primp constructors.
  The latter says the client *can* disable checks, not that defaults disable them.
- Extended the existing cookie-setting helper observation to `set_cookies` calls.
- Added the XXHash string-checksum call under `data/checksum`.
- Extended the existing Go dial API observation to `net.DialTimeout`, including
  real test code. Replaced the timed-TCP text regex with a call matcher bound to
  a TCP network argument. The old regex matched comment/string examples and
  missed variable-transport calls. TCP-specific consumers retain their bound
  TCP evidence; the generic API observation handles unknown transports.
- Moved both unchanged httpx constructor matchers into `http/client/initialize`,
  updating their consumers. Moved unchanged executor submission into
  `process/work/pool`. Its existing `parallel-task-dispatch-api` consumer still
  belongs to the previous workers selector, preserving the DDoS consumer's
  directory-membership predicate. No new exception or severity reduction was
  used to obtain benign verdicts.

## Rescans and controls

`atomscan` and `cleave facts` ran for all ten inputs. Original archives were
rescanned, including their analyzed members, and requested members were also
rescanned separately. Root notable counts changed as follows:

| Input | Notable before → after | Hostile before → after | Suspicious before → after |
|---|---:|---:|---:|
| gRPC-Go ZIP | 476 → 478 | 0 → 0 | 0 → 0 |
| end2end tests | 68 → 69 | 0 → 0 | 0 → 0 |
| balancer tests | 40 → 40 | 0 → 0 | 0 → 0 |
| xDS resolver tests | 39 → 40 | 0 → 0 | 0 → 0 |
| vet script | 37 → 37 | 0 → 0 | 0 → 0 |
| DDGS ZIP | 87 → 93 | 0 → 0 | 0 → 0 |
| CLI | 17 → 19 | 0 → 0 | 0 → 0 |
| publishing workflow | 11 → 11 | 0 → 0 | 0 → 0 |
| HTTP client | 10 → 13 | 0 → 0 | 0 → 0 |
| Bing engine | 9 → 10 | 0 → 0 | 0 → 0 |

All classifier results remain benign (`lvl=-1`), agreeing with the member
judgements and disagreeing with the fixed archive convictions. The exact
probabilities are in `review.json`. No hostile or suspicious finding was lost
from the original archive members. No DDGS member lost an observation after
accounting for the relocated IDs. On gRPC's `test/rawConnWrapper.go`, an emitted
Go-dial umbrella disappears through analyzer redundancy filtering; the concrete
TCP dial remains and the generic dial API observation is added. Its rule was
not deleted or weakened, and this is no loss of connection or attack coverage.

The positive and near-miss controls distinguish calls from source examples,
arbitrary `.get`/`.submit`/`.set_ciphers` methods, POST from GET, and False in the
condition from False in the fallback branch. Synchronous and asynchronous httpx
bearer-session-replay consumers still emit hostile findings outside the existing
test-directory exclusion. Existing hostprobe range-parser, single-host, and
sweep fixtures retain their TCP dial detections; the existing OWA replay control
retains its suspicious finding. Fixtures are scanned, never executed.

Reproduce the focused controls with:

```sh
python3 testdata/stranded-grpc-ddgs/check.py <scratch-directory>
```

The archive hostile-coverage goal cannot be met from the established evidence:
no attack-specific payload, stolen source, unauthorized execution chain,
persistence mechanism, or cleanup/evasion chain was identified in these source
contents. Member-table inspection, upstream comparison, decoded-string facts,
and source-path tracing supplied ordinary behaviors instead. This is an
unresolved conviction/classifier-evidence gap, not justification for invented
hostile rules or restoration of inaccurate matches.
