# OpenRemote and WSO2 source archive review

All three originals are **BENIGN** on the supplied evidence. Full hashes,
marker text, classifier outputs, and per-member detection changes are recorded
in [results.json](results.json). Counts below are distinct traits propagated to
the archive root; counting both root and member would count the same evidence
twice.

| Archive | Hostile before → after | Suspicious before → after | Local classifier before → after |
|---|---:|---:|---|
| OpenRemote core `9ea22e19db6711afd711f39517fe25509b018803` | 0 → 0 | 2 → 1 | BENIGN → BENIGN |
| WSO2 Carbon Kernel `4.10.72` | 0 → 0 | 1 → 0 | HOSTILE → HOSTILE |
| WSO2 Carbon Kernel `4.6.1-m1` | 0 → 0 | 1 → 0 | HOSTILE → HOSTILE |

The queue's HOSTILE prior is not reproduced by the current local classifier
for OpenRemote. Both WSO2 classifier convictions remain false positives after
the rule corrections. Their probability remains `0.74479413`, level `0`,
confidence `100`; OpenRemote remains `0.813364`, level `-1`, confidence `0`.
These calibrated levels are not interchangeable across archive types.
Atomscan reports model version `v18.18`, engine `2.13.0`, and warns that its
feature specification predates the engine's expected version 21. No rule was
restored or inflated to accommodate the model.

## Behavior traced

OpenRemote is an IoT platform source tree containing agents, server APIs,
manager UI, build/deployment tooling, and tests. `page-users.ts` creates and
updates users through `manager.rest.api.UserResource`. `_onPasswordChanged`
looks up `"new-password-" + suffix` and `"new-repeatPassword-" + suffix`, checks
the two controls, then assigns the validated value to `user.password`.
`_createUpdateUser` passes a changed password to the configured manager's
`updatePassword` API. Concatenating the control ID is not concatenating a
password value or building an exfiltration report.

`KNXImportXXETest.groovy` is a Spock regression test. It creates a random
temporary secret, serves a nested external-entity DTD through a server bound
to `127.0.0.1` on an ephemeral port, wraps a reference in a KNX project, and
calls the real importer. The assertion is `requestedUris.isEmpty()`. Cleanup
stops the server and executor and deletes the temporary file. The importer
reads `/0.xml`, applies its packaged XSLT, and creates KNX assets. Its secure
factory enables secure processing and disables external DTD/stylesheets;
its StAX factory disables DTDs and external entities. The nested Siemens MSI
is baggage inside the valid KNX project fixture; this importer does not launch
it. The suspicious SYSTEM-URL/parameter-entity trait accurately describes the
test payload and is retained without a test-path exemption.

Both WSO2 archives identify themselves as Carbon Kernel in their README and
Maven POMs; the POM versions and SCM tags agree with the supplied versions.
The complete `WSRequest.js` files are byte-identical between versions. This is
a web-service client supporting SOAP/HTTP requests, XML serialization,
WS-Security UsernameToken authentication, and a caller-configurable Tryit proxy.
`open` stores the caller's URI, username, and password. `send` either opens an
XMLHttpRequest to that URI or chooses `proxyAddress`/a URI-derived proxy.
The flagged line serializes `password=` followed by
`encodeURIComponent(this._base64(this._password))` into the proxy's form body;
the proxy receives it by POST. `_base64` converts characters to UTF-8 bytes,
groups three bytes, and indexes a standard alphabet to emit four sextets with
padding. Its null sentinel is `~`. This is reversible transport encoding,
not encryption, a plaintext report, or evidence of an attacker destination.
The SOAP branch constructs a WS-Security UsernameToken including PasswordText.

Bundled Prototype's `Ajax.Request` response evaluation is gated by its
`evalJS` option and same-origin JavaScript content type unless explicitly
forced. Its `evalResponse` consumes the response text. jQuery likewise exposes
its documented global evaluation and AJAX script handling. These are real
dual-use execution capabilities and retain their detections. The legacy PHP
EditArea compressor also really uses `preg_replace` with `/e` to rewrite loader
script lists; that notable detection is retained.

The coherent call paths, configured destinations, UI operations and defensive
test assertions tip the verdict toward benign software. No deployment or
execution by an intruder is supplied, and the source archive's provenance was
not independently authenticated against an upstream signed release. Static
analysis has flow limitations in these large source trees; those limitations
are recorded by the scans and were not treated as evidence of innocence.

## Rule corrections and coverage

* Replace `objectives/exfiltration/messaging/telegram::browser-plaintext-password-report-field`
  with notable `micro-behaviors/data/format/credentials::password-labelled-value-concatenation`.
  Require a `:` or `=` label/value delimiter instead of accepting any suffix
  after `password`. This excludes DOM IDs and retains actual credential-field
  formatting, including encoded proxy fields. The new name and description
  do not assert plaintext, reporting, transmission, or malicious intent.
  The Telegram composite references this neutral observation.
* Relocate the UsernameToken atom, username and password atoms, and their
  composite from `http/ws-trust` to `http/ws-security`, with corresponding
  WS-Security names. Matchers, effective types, platforms, criticality,
  confidence and 12-line proximity are unchanged. Ordinary SOAP authentication
  does not establish a WS-Trust exchange. Both WS-Trust objective consumers
  now reference the relocated composite. The remaining WS-Trust endpoint and
  RequestSecurityToken observations stay in their original home.
* Rename the three `browser-device-profile-request-fields--*` atoms to
  `location-rendering-query-field`, `power-connectivity-query-field`, and
  `resource-state-query-field`; rename their OR group to
  `client-query-field-prefix`. A literal `uri=` identifies a field prefix,
  not browser device profiling. Preserve all matchers and consumers; remove
  unsupported file-wide exfiltration/HTTP-communication technique mappings.
  The engine filters this low-value OR group from emitted findings, while
  still evaluating its objective consumers.
* Add a notable structural observation for `charAt` with an index shifted
  right two bits, and a notable Base64 encoding composite requiring a standard
  alphabet within 1,800 bytes. The description explicitly states co-occurrence.
  A plain alphabet, unrelated character lookup, quoted example, or distant
  lookup is insufficient. This covers the handwritten WSO2 encoder missed by
  API-name-only encoding rules.

Every emitted archive/member record was compared after ID mapping: 1,282 OpenRemote,
1,146 WSO2 4.10.72, and 1,119 WSO2 4.6.1-m1 analyzed records before and after.
The only removed observation is the unsupported OpenRemote DOM-ID password
report match. WSO2 retains that line as a neutral formatting observation, gains
the encoding composite and character-access atom, and preserves all other
matched observations after the documented renames. There is no material attack
coverage loss.

## Retained attack and boundary checks

Before narrowing the shared password rule, the original positive from the
earlier review was recovered through Forager by SHA-256
`cef802016a70b757c624b1b1838ebd1887a341a7fd16c076c75096efc68e17d3`.
Its downloaded bytes and `.forage.json` remain in scratch. Its Base64 document
writer was decoded as data: the page demands an email password, reads the
password control, concatenates it into a report, POSTs the report as Telegram
chat text, and always presents failure/retry feedback. This establishes theft
and deception independently of any rule name or score. No endpoint was called.

Before and after, that original retains all three hostile detections: Telegram
password export, deceptive retry, and concealment through the document writer.
Its four suspicious observations become three because the password formatting
atom is now neutral; its classifier remains HOSTILE (`0.99`, level 25).

`check.py` passed 29 static controls covering the recovered original, decoded
and renamed variants, broken attack legs, authorized encoding, DOM IDs,
generic account XML versus WS-Security/WS-Trust, query prefixes, and the
Base64 encoder's positive and negative boundaries. Run with:

```sh
python3 testdata/triage/openremote-wso2-review/check.py \
  --scratch <scratch-controls-directory> --attack <recovered-script..js>
```

The optional attack argument is hash-checked. Omitting it runs the 21 local
controls. Sample scans used `SCAN_HOPPER=`, `CLEAVE_TRAITS_DIR="$PWD"`,
`--no-update --analyze local --mode slow --follow=none -f json`; `cleave facts`
was run on all three originals and all four flagged source members, including
their decoded text views. The original member facts contain no concealed
executable stage; the incidental decoded fragments were checked as data.
There were no fetched dependency findings requiring a dependent-package
exception. Final repository validation is `make validate`.
