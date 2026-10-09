# Pinned Brick v2 releases: native credential export

## Byte-based judgments

All three supplied archives are MALICIOUS:

| Package | Version | Archive SHA-256 |
| --- | --- | --- |
| @brick-v2/core | 999.0.1 | 3d21cd393165a2d1cbb46eab58b5aa24fc910cbf3e9adc6ec0775e42929074cb |
| @brick-v2/core | 999.0.2 | 257f474d8d53bd5b6ef74f2e07dfdb737d8c02d0cdcc554232814ad51c7f7c0c |
| @brick-v2/icons | 999.0.2 | aabc60635ed65531984597b2d2909e53475cead1b4f519df3e80e14b3a189be8 |

The pinned reputation claims are confirmed for these bytes. No conclusion about
other releases, the scope as a whole, or publication timing follows from this
analysis. Registry age and reputation were not conviction conditions.

`index.js` exports empty framework/logger facades and catches errors while
requiring a platform-specific `.node` addon. There is no install script. The
payload runs when the package is imported on Linux x86-64, not automatically
from a declared npm lifecycle hook.

Rizin identifies `metrics.node` as a dynamically linked x86-64 ELF shared object
with Node-API registration exports. In 999.0.1 the registration entry at 0x1860
calls fork (0x1870). Its child calls setsid, do_report and _exit (0x1882–0x188e).
In 999.0.2 the corresponding entry is 0x1880 with the same control flow.
Both 999.0.2 packages carry the identical native SHA-256
`daedefd6a8a02449e29a163a1a92edc0859c0cdb814ec1024b6615fa78bdd375`.
The older native SHA-256 is
`3f8833d49735dfdfe9bdef504bbb53ff069cb48a3953d9af08659d1c5560cf26`.

`do_report` obtains hostname, uname fields, the current UID's username and cwd.
It loops over a fixed environment-name array, reads nonempty values using
getenv, escapes quotes/backslashes and serializes them into JSON. Targets include
AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, GITHUB_TOKEN,
NPM_TOKEN, NODE_AUTH_TOKEN, SYSTEM_ACCESSTOKEN, ACTIONS_RUNTIME_TOKEN and
ACTIONS_ID_TOKEN_REQUEST_TOKEN. CI/job/runtime metadata accompanies the secrets.
The 999.0.2 binary additionally reads _METRICS_PKG, set by its JavaScript loader,
and includes the package name in the report.

The native routine resolves `oob.s4yhii.com`, creates an AF_INET/SOCK_STREAM
socket and connects to port 9999 (sockaddr immediate 0x0f270002). After a successful
connection it formats `POST /native HTTP/1.0` with JSON Content-Type and sends
the report. This is one-way export: no receive, shell execution, command tasking,
repeated beacon, credential-file read, or durable persistence was established.
Cleave facts exposed ordinary strings and imports; there was no decoded-string
payload to reconstruct. Binwalk was unavailable on PATH; rizin disassembly
resolved the complete small payload without executing it or contacting its host.

## Trait correction and migration record

- Replace three overlapping archive findings in trojanized/library/native-addon
  with one hidden-payload/native-extension finding. Required evidence establishes
  swallowed dynamic loading plus a native secret exporter, not substitution of a
  known legitimate library or periodic beaconing.
- Strengthen the native environment-export composite with a cwd/object JSON
  template, detached-process APIs and independent AWS, GitHub and npm credential
  references. Drop the required OOB hostname label. The name, domain, release
  number and chosen addon filename do not gate either hostile verdict.
- Move the three firing AWS name matchers and GITHUB_TOKEN reference to
  os/env/secret-name; preserve their matchers and effective scopes. Update exact
  consumers and expand old cloud/VCS directory selectors in existing OR/exclusion
  lists to retain precisely the moved members. No broad new secret directory
  selectors or roll-up findings were added. Update the existing fixture expectation.
- Split the OIDC token/URL union: credential token reference belongs in
  os/env/ci-credentials; the request URL stays in cicd. Add Actions runtime and
  Azure Pipelines access-token name references. OIDC publish now requires the
  token reference; an endpoint alone cannot supply credential context. Ancestor
  cicd consumers intentionally stop treating the token alone as job metadata.
- Move the firing fork/clone symbol observation to process/create/fork and the
  UID password-entry import to os/user/lookup, preserving matchers, exclusions
  and scopes. Update all exact references. There are no fork-directory selectors.
  The user-query ancestor selector in account-name-resolution is expanded; other
  ancestor consumers exclude native binaries through their own type scopes.
- Move direction-neutral HTTP version text from response to message. Its exact
  consumers retain the same matcher. No HTTP-response ancestor selectors exist.
- Move the prebuilds/addon name pair from path/construct to path/library. The
  matcher names a library location; it never proves platform selection or a join.
  Describe caught-require/path composites as co-occurrences, not proven flow.
- Remove the collector archive version-name observation and remove
  it from the suspicious package-version composite. Its bytes cannot establish
  a declared package version. Remove unsupported supply-chain ATT&CK defaults
  from version metadata.
- Promote the standalone hostname API reference to notable and anchor its symbol
  matcher. Report fork/setsid as API co-occurrence. Describe declared prebuilds
  files and Node-API ELF structure without assuming every such path is an addon.

Existing neutral HTTP, socket, getcwd, uname, getenv, error-handling and manifest
findings remain visible. No crypto, permission change or privilege escalation
was found; none is claimed by these corrections. New rules use existing leaves
admitted by the local validator; no directory split or new taxonomy axis is used.

## Verification

Run `check-controls.py SAMPLE OUTPUT_DIRECTORY` against the supplied core
999.0.2 archive. It changes bytes only; it never loads or executes sample code.
The static fixtures are reproducibly derived from the specified sample:

- Original archive: exactly the environment-export and concealed-addon hostile IDs.
- Changed domain, package name, version, directory and addon filename: same IDs.
- Host report without credential-name targets: zero hostile findings.
- Missing send import evidence: zero hostile findings.

These controls passed using atomscan slow mode with dependency fetches and hopper
upload disabled. All three original archives were also independently scanned.
The native export composite scored precision 9.5; the revised concealed-addon
composite scored 8.4. Atomscan supplies the authoritative archive correlation;
`cleave test-rules` reports the variable-argument require atom absent at the npm
root even though atomscan retains it in the JavaScript member and correlates it
successfully. This diagnostic discrepancy does not imply sample flow completeness:
atomscan explicitly reports limited JavaScript flow recovery. Native data flow
was established by disassembly, not inferred from the trait co-occurrences.

Validation cleanup: narrow CI name atoms to scripts and binaries; repair the
local fork reference. The JavaScript telemetry exclusion groups AWS name
references, omits an inapplicable binary atom, and drops the filtered-copy
exclusion already covered by its required Object.keys(process.env) call.
