# Container runtime paths belong with filesystem endpoints

The container runtime leaf held 87 rules spanning API operations, configuration,
imports, vocabulary and filesystem paths. Five Docker socket atoms and their
path roll-up now live in `micro-behaviors/fs/path/socket`. The native non-stock
Unix socket path atom also moves there from `communications/ipc/unix-socket`.
Creating or connecting a socket remains an IPC operation; naming its filesystem
endpoint is a path observation. No rules are placed at internal directories.

The seven moved rules preserve every matcher, scope, exclusion, confidence and
criticality. Only the path roll-up's overlong description is shortened. Its
members use the new exact IDs. Nine surviving consumers change: eight exact
reference updates and one explicit preservation of container-reference evidence.
The mapping ledger records effective definitions; 27 direct/ancestor consumer
decisions cover the directory-membership effects.

`kinsing::container-or-cloud-marker` really asks whether container context is
referenced, so it explicitly retains all six Docker-path alternatives. It does
not reference the whole new leaf, which would incorrectly add arbitrary Unix
socket paths. Container-tooling suppressors/downgrades do not receive those
alternatives: a socket pathname is insufficient evidence of trusted tooling.
Generic filesystem consumers can now receive these path observations; generic
communications consumers no longer receive the native pathname as an operation.

## Duplicate and sibling review

No identical matcher body was found elsewhere for the seven moved definitions.
The Docker path variants overlap but differ in effective conditions:

- `/run/docker.sock` substring versus `/var/run/docker.sock` text substring.
- Exact literals across scripts/binaries versus source with an explicit string
  kind restriction.
- Percent-encoded path recognition across source/scripts.
- The text matcher carries a CLI-training context exclusion that the others lack.

Those differences are retained; merging by description would change coverage or
exclusions. The canonical *subject* is shared even while evidence forms remain
separate. A future matcher-equivalence check should compare normalized kind
semantics and expanded scopes before recommending an exact-literal merge.
The native path rule retains all stock-daemon/example exclusions, including
Docker and containerd, so moving it does not expand its claim.

Filesystem socket endpoints are distinct from device nodes, NTFS streams,
credential paths and protocol/address-family constants. Existing token and
secret-config leaves already own container credential-path observations; they
are preferable destinations for the runtime leaf's remaining secret paths,
subject to their own overlap and consumer audit.

## Verification

Before/after read-only atomscan controls retain plain, shortened, percent-encoded
and Go-source Docker path observations at the new IDs. An unrelated socket name
receives none of the Docker observations. Eight new ZIP fixtures include those
five cases plus three small compiled C programs containing a native endpoint,
a Docker endpoint or an excluded example endpoint. The programs were compiled
but never executed. Their ordinary inner filenames avoid test-path exclusions.

The full fixture suite passes **1,798/1,798**. The runtime leaf contains **81
rules**; **166 oversized directories and zero mixed nodes** remain. There are no
retired-ID references or compatibility aliases. Strict validation still reports
separate description, regex, Android scope and suppression debt in addition to
oversized directories; the soft gate is not a strict validation pass.

## Remaining container-family work

The cap is satisfied here, but the semantic audit is not complete:

- Runtime secret/service-account paths overlap filesystem credential subjects;
  a token filename alone must not become a credential-read claim.
- Ports 2375/2376 do not establish Docker, authentication mode or TLS. Privileged
  fields/flags without a bound Docker/Kubernetes operation are likewise generic.
- `serviceaccount-token-read` matches a generic token read expression without a
  Kubernetes path relationship. The in-cluster composite needs that binding.
- API route collections alone do not establish workload writes, enumeration or
  actual transport. Resource-operation labels must stay within the evidence.
- `image/` contains Docker config paths, environment names and auth vocabulary;
  those are not image construction. Check existing secret-config homes first.
- `oci/` contains private helper paths and implementation names alongside real
  operations. Those fingerprints need classification by supported observation.
- Container import evidence, runtime identity, CLI requests and declarations
  should not remain interchangeable evidence under a broad runtime OR.

The sibling review therefore favors semantic relocation and consolidation before
inventing another Docker/Kubernetes/backend level under runtime.
