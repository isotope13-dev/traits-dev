# OOB host survey triage

The analytics 0.1.0, 1.0.0 and 1.2.0 archives have identical index.js,
poc.js and README.md; only the manifest version differs. Their supplied
SHA256 values match. Each archive has exactly four regular files.

The package entrypoint exports seven inert analytics functions. Each of
preinstall, install and postinstall invokes the same Node sidecar. The sidecar
reads hostname, username, platform/architecture/release, cwd, Node version,
its own manifest version, and presence of selected CI variable names. It
URL-encodes the record into a GET query. Each invocation makes two requests:
a hex-encoded, 50-character-truncated hostname/user/version label under an
OAST collector and a nip.io backup host. HTTP name resolution also exposes
the encoded label to DNS. The response is drained; errors are ignored and
request inactivity is limited to four seconds. This is two callbacks per
hook, potentially six during installation, rather than the single callback
asserted in the package description. There is no secret-value sweep,
credential-file access, received-code execution, persistence or host mutation.
Reading its own package.json is the only file load beyond builtin modules.

Judgment: SUSPICIOUS. The pinned malware allegations are unconfirmed.
The embedded authorization claims cannot establish permission; the bytes
support a limited dependency-confusion host survey and warrant review.
The rules do not suppress behavior based on those claims.

## Claim and placement corrections

- OOB GET plus hostname is co-occurrence, not proven theft. Move it and its
  install-context consumers into discovery/system/profile with suspicious
  criticality and descriptions that state the evidence. Require a GET call
  rather than an HTTP get member reference; bind survey context to one file.
- Host/user queries beside an OOB endpoint establish a survey context, not
  preparation or transfer of a profile. Move that observation into discovery.
- Interactsh plus hex encoding alone is not reconnaissance. Require an HTTP
  operation and a hostname query; move to the system survey directory.
- A small script's endpoint reference does not prove contact. Require a GET
  call and record this as a notable HTTP capability.
- Postinstall declaration, OOB endpoint and GET co-occurrence is a notable
  HTTP observation; it does not prove the hook invokes that request.
- Move install declarations and the local Node command into manifest lifecycle
  metadata. Reuse the existing install-presence atom instead of its duplicate.
- Move neutral Node query combinations into sysinfo/profile. The former
  aggregation matcher did not require any object construction; rename it to
  state the required number of query kinds. Use the canonical interface query
  instead of the inactive network placeholder. Move process.cwd to directory
  queries; make platform and architecture queries notable.
- Move hostname/platform/architecture text into the schema context directory
  and JSON.stringify env-field syntax into JSON serialization. Names describe
  text evidence and do not assert runtime data flow.
- Move preinstall HTTP URL and xxd hex-output observations into their neutral
  operation directories, with notable criticality. This repairs misplaced
  behavior while keeping lifecycle and schema leaves within their budgets.

All exact YAML consumers were updated. Selector searches found no positive
ancestor consumers of the removed OOB/install/source-schema rules. The broad
platform/runtime selector in node-multi-sysinfo-with-hook explicitly retains
the relocated cwd call; its description now covers directory queries.
No aliases, identity allowlists, reputation gates or package-specific
suppression were added. Existing unrelated rules in legacy leaves remain.

## Verification

atomscan with CLEAVE_TRAITS_DIR set to this checkout, no updates and no
reference following: all three archives have zero hostile and six suspicious
traits. cleave facts was run for each archive and the sidecar; the recovered
calls and constants agree with the source analysis. No sample code was run.
Native disassembly is unnecessary for these complete readable JavaScript files.

Run `python3 testdata/taxonomy/oob-install-survey/check.py` for the six
controls. Copies under neutral paths prevent testdata exclusions from masking
matcher defects. An OOB GET host survey is positive; comments alone, endpoint
alone, health-check GET alone, identity queries alone, and endpoint plus hex
encoding all fail the selected survey rules. No control emits a hostile trait.
