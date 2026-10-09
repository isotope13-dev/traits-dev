# Galicia 999.0.2 native environment theft

## Judgements

All three submitted archives are MALICIOUS at version 999.0.2 only:

- `@galicia-toolkit-cheques-nc/front`: SHA256 49bef50728c710f36c9e0051c8c53d90a224d9e1d7e72f0e61b9bbd5c4ee5d70
- `@galicia-toolkit-nestjs-20-lite/archetype`: SHA256 2c0d936f6435e4b009eb699f13e386543c0a19279d9316fa97a8acec8b69636d
- `@galicia-toolkit-nestjs-20-lite/commons`: SHA256 5ccae30adf495ad5d39137435f24d390c46f08ed5d0ce9ea16f7a144b0d0bee0

Their three-file payloads consist of a minimal package manifest, a JavaScript
facade and one identical Linux x86-64 Node-API addon, `metrics.node`.
Addon SHA256: daedefd6a8a02449e29a163a1a92edc0859c0cdb814ec1024b6615fa78bdd375.
No judgement about other versions follows from these bytes. Registry publication
facts and the external malware-list claim do not supply the behavioural verdict.

## Static reconstruction

`index.js` exports a version, empty providers and no-op loggers, assigns a package
label to `_METRICS_PKG`, constructs the prebuild path and requires it inside an
empty catch. There is no manifest install hook. Activation is package import on
Linux x64, not necessarily installation alone; other platforms have no addon.

Rizin identified an unstripped GCC ELF shared object. `napi_register_module_v1`
at 0x1880 calls fork at 0x1890. The parent returns its original exports; the child
calls setsid at 0x18a2, do_report at 0x18a7 and _exit at 0x18ae.

`do_report` (0x1340) queries hostname, uname, current UID's username and cwd. It
builds a JSON profile, then loops over a selected environment-variable array and
calls getenv (0x15f3). This includes AWS access/secret/session keys, GITHUB_TOKEN,
NPM_TOKEN, NODE_AUTH_TOKEN, SYSTEM_ACCESSTOKEN, ACTIONS_RUNTIME_TOKEN and
ACTIONS_ID_TOKEN_REQUEST_TOKEN alongside CI and host context. Nonempty values
are copied with quote/backslash escaping into a string buffer, then formatted
as JSON string members by snprintf at 0x169e. Values are not redacted.

At 0x16e8 the code resolves oob.s4yhii.com, creates an IPv4 stream socket and sets
a ten-second send timeout. The sockaddr constant 0x0f270002 yields port 9999.
The code connects at 0x17a4, formats a POST /native HTTP/1.0 request containing
the JSON body and Content-Length at 0x184a, sends at 0x185a and closes the socket.
No payload was executed. This is one plaintext credential/profile upload;
there is no receive loop, remote-command sink or durable persistence mechanism.

## Trait changes and reference audit

- Replace the OOB-host-dependent native verdict with detached Node-addon,
  multi-service secret-variable, JSON-member-format, HTTP-body-template and
  socket evidence. The description states the inferred collection/upload
  pattern; no general native data-flow analysis is claimed.
- Consolidate three overlapping package convictions into one concealed native
  extension verdict. Wholly malicious facades do not establish modification of
  a legitimate input, and one POST does not establish repeated beaconing.
- Keep the endpoint spelling as neutral optional evidence. It never gates the
  new hostile rules. No package-name, version, file hash or specimen size is
  required by either hostile rule.
- Move the native fork atom to process/create/fork, UID account lookup to
  os/user/lookup, bare HTTP versions to http/message, OIDC credential request
  names to os/env/ci-credentials, and prebuild pathname fragments to
  fs/path/library. Preserve matcher/type/platform scopes. Update exact consumers.
  All other rules in those source leaves remain in their existing migration
  holds; no directory split or wholesale legacy migration is claimed.
- Broad user-query and CI-env consumers retain the moved atom plus their old
  selector as one named alternative, preserving their all/any role cardinality.
  Preserve the UID lookup runtime downgrades on the user-query group so a
  normal Go runtime import is not promoted from baseline to notable.
  Audit ancestor selectors with rg; fork, HTTP version and pathname consumers
  use exact IDs. No parent selector needs widening for those moves.
- The JSON serialization leaf was already at its 100-rule budget. Move the
  existing JSON.parse atom to data/parse/json, retain its matcher and severity,
  and update all exact/local consumers. The only broad serialization consumer
  is Python-only socket framing; the moved JavaScript atom was ineligible there.
  This leaves room for the distinct native JSON string-member template.
- Raise the hostname API observation to notable. Narrow the socket-options
  suppressor to real kernel-source context; a linux-x64 prebuild pathname alone
  was suppressing the imported setsockopt observation.
- Remove the collector-assigned archive basename from the suspicious placeholder
  version composite. Keep the archive basename itself as a notable name property.
- Correct descriptions of path fragments and caught requires so they do not
  imply a source-to-loader binding that the text matcher cannot prove.

The destinations are existing admitted leaves; directory_whitelist.rs and the
reviewed partitions in validation/taxonomy.rs were inspected. No YARA was edited.
No new ATT&CK mapping is assigned to neutral atoms. The exfiltration rule retains
T1041 and the concealed-package rule uses T1195.002/T1041. No MBC mapping added.

## Verification

Each original archive was scanned with atomscan and inspected with cleave facts;
the common addon and representative manifest/entrypoint had separate full facts
and Rizin disassembly. Archive hashes and all three addon hashes were checked.
After changes each archive has two hostile rules in separate objective leaves,
two accurate version-shape suspicious observations, and no hostile/suspicious
findings on its JavaScript or registry record.

Focused controls are harmless copies edited as ELF data, never loaded:
renaming the endpoint preserves detection; removing credential names, getenv,
fork, JSON member formatting or the Node-API registration export removes the
native hostile finding. A normal try/catch wrapper and JSON parse/stringify
sources have no suspicious/hostile findings. See controls.json. These controls
check required roles; they are not a claim of exhaustive benign-corpus coverage.
Both hostile rules exceed the required precision floor of 3.5: native 11.1,
package 10.2. The engine reports these above-normal scores as precision notes,
not strong-inflation warnings (threshold 16).

Judgement markers were written beside the submitted archives, outside this
repository. Their one-line summaries for the commit body are:

Galicia front 999.0.2: native env theft; fix intent and placement
Galicia archetype 999.0.2: native env theft; fix intent and placement
Galicia commons 999.0.2: native env theft; fix intent and placement
