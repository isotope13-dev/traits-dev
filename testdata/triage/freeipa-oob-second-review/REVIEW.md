Second review of two public-registry, uncorroborated convictions

Both samples are MALICIOUS on their supplied evidence. Original SHA-256 values were verified, and all three extracted npm members were compared byte-for-byte with their archive entries. No external feed, advisory, or scanner reputation was used as evidence. The review used atomscan before and after, cleave facts for both originals and every npm member, full source/control-flow inspection, and a mocked JavaScript execution with invented host data and no network access.

FreeIPA anonymous LDAP principal injection PoC

The Go program accepts the LDAP URI, directory suffix, token ID, principal, reusable password, and Base64-encoded Kerberos key through CLI flags. Their example strings are help text, not default credentials or targets. It opens an operator-selected LDAP endpoint, performs UnauthenticatedBind with an empty name, decodes the supplied key, and constructs an OTP entry with both OTP and Kerberos object classes. That request has empty ipaTokenOwner/managedBy fields, principal/canonical names, the supplied principal key, and a reusable password. It submits the add, then constructs a modification adding a member to the FreeIPA admins group. Errors exit immediately; it does not roll back a successfully added entry after a later failure.

The member DN uses krbPrincipalName as its RDN, whereas the added entry uses ipaTokenUniqueID. Thus successful enrollment is not established. Schema/ACI acceptance, validity of the operator's key blob, and the actual server version/configuration are also unknown. These are attack attempts in the source, not proof of a working vulnerability. No CVE attribution is established; unverified CVE assertions in the old rule comments were removed. Credential theft, key generation, local privilege escalation, and command execution are not shown.

An explicitly operated exploit can be used in an authorized security test. No such context accompanies this artifact. Its anonymous credential injection and attempted administrator-group enrollment tip the judgment toward MALICIOUS, despite its transparent PoC packaging.

All three hostile matchers remain effective. FreeIPA DNs/object classes describe the target schema rather than identifying this custom client as FreeIPA, so their matchers and original scopes moved from well-known/app/system/freeipa to micro-behaviors/os/security/directory-service. The empty managedBy atom was renamed because managedBy alone does not establish a FreeIPA OTP target. Empty owner/manager fields alone establish neither bypass nor escalation: the original suspicious composite also matched the authenticated directory-admin control. Its unchanged match relation is now a notable directory observation, while the hostile combinations retain the credentials, anonymous-bind, OTP-target, and group-add context. A notable actual LDAP connection call was added. The old default ATT&CK list alleged local account creation; the supported account-manipulation mapping is retained instead.

The generic admin-email/password-text matcher was not evidence of a dialog. Its original matcher and macOS/type scope moved to an email-address reference trait, with a description that makes no password-collection or prompt claim. The LDAP entry-add grouping now says preparation/request rather than asserting submission for a constructor alone.

ltidisafe 3.4.6 npm package

package.json declares main=index.js, an empty author, no source repository, and preinstall="node test.js > /dev/null 2>&1". Its placeholder npm test command does not run a test suite. Installation invokes the sidecar without an opt-in; the shell discards stdout and routes stderr into the same discarded stream.

index.js implements a recognizable throughput-checking helper. checkDownloadSpeed validates argument types, selects the HTTP/HTTPS client by the URL protocol, and calls that client's get with the supplied URL. Response data/end events measure time and calculate rates using the claimed file size. The exported, unused checkUploadSpeed method sends generated random data through http.request/write/end. No response is evaluated, installed, or executed.

test.js collects username, hostname, and home directory, encodes each via Buffer.from(str, 'utf8').toString('hex'), and calls the asynchronous benchmark sender three times. The sender concatenates that value into an HTTP hostname under a fixed Oastify callback domain and passes the same URL into checkDownloadSpeed. Therefore the identity is exposed through the requested hostname, including DNS resolution where necessary and the HTTP request. The local IPv4 interfaces are enumerated but the resulting localip value is unused. Uptime code is commented out. The helper name and speed log do not turn disclosure of local identity to a fixed third party into a throughput requirement.

The mocked run used review-user, review-host and /home/review, and produced exactly three GETs whose leading hostname labels decoded to those three values. The HTTP request/upload method was configured to fail the mock if reached; it was not reached. No actual identifiers or requests were sent. This confirms the static path while leaving actual delivery/server response unproven. Long hostname labels or request failures can interfere with delivery without removing the attempt.

Possible research intent is suggested by the OOB service but is not authorization to collect an installer's identity. The automatic, muted install path and unnecessary external disclosure tip the judgment toward MALICIOUS. There is no consent, authorized deployment context, or documented legitimate need for these identity-bearing requests in the supplied package.

Both existing hostile detections remain: the benchmark identity exfiltration and its packaging alongside npm preinstall. No third distinct hostile behavior is evidenced. Three leaked identity fields are one exfiltration technique, and hex encoding, interface enumeration, and stream redirection are separately covered notable mechanics/declarations. Investigation found no downloaded executable stage, C2 tasking, persistence, or cleanup. The archive-wide preinstall composite describes co-occurrence; it does not prove that an arbitrary package hook reaches an arbitrary sidecar. Source inspection establishes that reachability for this specimen, while the engine reports limited flow/call support. Extra hostile copies would not improve distinct behavior coverage.

The new notable package-script observation detects stderr duplication in parsed script values and rejects quoted diagnostic text. Existing stdout-to-null coverage is preserved. The generic URL-constructor matchers moved unchanged from HTTP query to URL parsing, and the exact OIDC/GET consumers were updated. The FTP control shows why URL construction alone is not an HTTP query. OOB identity URL descriptions now describe their actual source/sink evidence rather than only an ordering number. A generic HTTP-client request description was clarified without changing its matcher.

Before/after results (H=hostile, S=suspicious, N=notable)

| Artifact | Before H/S/N | After H/S/N |
|---|---:|---:|
| freeipa_principal_inject.go | 3/1/18 | 3/0/20 |
| ltidisafe-3.4.6.tgz (aggregate) | 2/0/72 | 2/0/73 |
| package/index.js | 0/0/22 | 0/0/22 |
| package/test.js | 1/0/34 | 1/0/34 |
| package/package.json | 0/0/16 | 0/0/17 |

No hostile detections were lost. Seven old Go observation IDs were replaced by their corrected neutral homes; one URL-constructor ID changed home in index.js and its archive aggregate. Every supported match survives. The one suspicious-to-notable correction is the unchanged empty-ownership relation, justified by the authenticated administration control. No signature was weakened to clear the specimen.

The v18.18 ML route classification codes remain 0 (BENIGN), disagreeing with both manual judgments and the retained hostile traits. FreeIPA aggregate raw probability changed 0.9840616 to 0.98168147, with level 15000 and confidence 38 unchanged. npm aggregate probability stayed 0.99722844, level -1 and confidence 0; its npm route changed 0.99887973 to 0.99895847. index.js and test.js probabilities stayed 0.11317844 and 0.95542264; package.json changed 0.65273058 to 0.6553148. A high raw probability is not a calibrated verdict. Both scans warn that the model uses feature specification v18 while the engine expects v21. This classifier gap is reported without restoring inaccurate identities or adding hostile duplicates.

Regression work

The ancestor-selector audit found 281 relevant broad-selector references. FreeIPA's old broad well-known/app/system/app memberships served benign suppressions/downgrades; a target-schema reference must not blanket-identify the scanner client as a trusted application. These suppressors were not extended to the neutral schema traits. Exact FreeIPA attack consumers were updated; no direct selector of the relocated source leaves required preserving an unrelated member set. No existing independent FreeIPA positive was found in testdata or taxonomy-migration. An independent Python/ldap3 control retains all three original hostile combinations, while the original definitions demonstrate the benign empty-ownership false positive. The existing benchmark positive and renamed specimens outside this batch remain detected.

Twenty focused controls passed: eleven new controls registered in testdata/expectations.toml plus the nine existing hex-identity-benchmark cases. They cover attack preservation, authenticated empty fields, ordinary LDAP connection, non-UI address text, FTP URL parsing, absent constructors, OIDC consumers, silent ordinary compilation, stderr-file/quoted near misses, renamed hostile bindings, and disconnected sources/encoders/URLs. Full per-file trait deltas and ML records are in review.json. Final required gate: make validate.

Verdict marker contents (also suitable as commit-body lines):

FreeIPA exploit: anonymous principal injection; fix trait placement

ltidisafe 3.4.6: silent identity exfiltration at install; add stderr
