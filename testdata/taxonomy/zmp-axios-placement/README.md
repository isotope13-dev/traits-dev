# Zalo CLI, Axios, and offset-array PowerShell review

## Judgments

| Input | Verdict | Evidence |
| --- | --- | --- |
| zmp-cli 4.0.5, SHA256 39958b327f76f24e7e51d4f9940c0bbdaf50c14a6dfedae34104761231473dd6 | BENIGN | The decoded code implements its advertised login, project creation, build, preview, migration and deployment commands. |
| small-key-subtraction.ps1, SHA256 027599cfeb1311bcbae66763a8d3830781308f35872dc2ef3761cd088682b158 | MALICIOUS | Conceals a remote MSI installation, hides the installer, and deletes its own script. |
| romulus-offset-stager.ps1, SHA256 ed0b4360038d6862265314b1db9783cdf3a53d8e31b210537e89c65fdac02f3e | MALICIOUS | Decodes to the same installation and cleanup program. |

These are reasoned judgments of the code, independent of ML classifications.

## Reverse engineering

No sample code was executed. JavaScript string-table rotation was reproduced
with a bounded data-only decoder: extract the literal array, index offset and
parseInt checksum expression, rotate until its checksum agrees, then replace
numeric decoder calls. All 40 transformed JavaScript members were recovered.

The CLI dispatches Commander subcommands. Login sends a user-supplied token to
the Zalo developer API, or displays a login QR and polls that API for a JWT.
It stores the selected app ID and JWT in the project's .env. Deployment hands
the selected build directory and token to zmp-cli-core. Project creation and
migration invoke npm installs; device preview runs adb reverse/devices and
uses chii plus a localtunnel server. The preview frame evaluates custom
postMessage data without an origin check: an insecure development surface,
but no evidence of an unauthorized implant. The update check reads npm
registry version metadata and prints an update instruction; it does not
silently install an unrelated payload.

Official documentation corroborates the product's purpose and commands:
https://docs.zaloplatforms.com/docs/MA/intro/getting-started/dev-use-command-line

The fetched Axios 1.20.0 archive was inspected separately. Its SHA1 is
515513445aa60e71d04b6521ca6210829ccb4786, matching the supplied PURL checksum.
Its entrypoint creates an Axios instance, builds caller-configured requests,
runs interceptors and dispatches through HTTP/XHR/fetch adapters. Its cookie
helper reads the requested cookie for same-origin XSRF header handling;
there is no credential export destination or independent install payload.
The README's casino language is inside disclosed Open Collective sponsor
descriptions. Blob.js is an ordinary platform helper. Neither establishes
obfuscation, spam delivery, or supply-chain compromise.

The PowerShell scripts each contain 494 negative integers. The first computes
character = element - (-500); the second computes character = element +
1520498. Both yield the same 494-byte script. The outer layer records its own
path in an environment variable and immediately invokes the reconstructed
ScriptBlock, by .Invoke() or the call operator, respectively.

The recovered script constructs Net.WebClient, downloads an MSI from
http://1614733393/app/afafa98279c9/ISOSimple.msi (host 96.62.224.81), places it
under TEMP with a GUID-prefixed name, and invokes System32/msiexec.exe with
/i, /qn and /norestart through Start-Process -WindowStyle Hidden. It then
force-removes the outer script through the saved environment path, suppressing
errors. Concealing the endpoint and installation program, suppressing the
installation UI and removing the launcher together support the malicious
stager judgments. No downstream MSI or malware-family attribution is claimed.
The endpoint was not contacted and the MSI was not retrieved.

## Trait changes

- Retire the Blob.js basename atom from obfuscated execution and remove its
  explicit composite membership. A freely chosen helper name establishes
  neither evaluation nor benign bundling.
- Move the unchanged three-casino-term matcher to documentation claims;
  remove its unsupported supply-chain ATT&CK mapping. Preserve its explicit
  content composite reference. Its description now says Markdown, matching
  its scope rather than assuming every Markdown file is a README.
- Move the unchanged accessToken field matcher from device-code to token-auth.
  Its description makes no OAuth or device-code inference. Update its exact
  C2 consumer reference.
- Move the unchanged random-like literal predicate to the source-string
  population profile. The population is explicitly bounded by literal
  syntax, length, character set and classifier. Ordinary obfuscator checksum
  strings remain observable without claiming an environment activation key.
  Preserve the explicit environment-read co-occurrence consumer and describe
  that co-occurrence accurately.

The other source-directory rules are unchanged. Exact and ancestor references
were audited; no source ancestor selector required replacement to preserve
these memberships. The migrations preserve matchers, platform/type scope and
criticality. Corpus changes on the supplied targets are limited to these IDs
and the deliberately retired basename atom.

No PowerShell YAML change is necessary: the two existing suspicious arithmetic
obfuscation/evaluation composites accurately describe both wrappers. The current
facts producer does not expose the offset-decoded body as a scanned layer.
Consequently no hostile behavior is inferred from the wrapper by a new rule.
The two supported suspicious findings meet the requested coverage without
inventing hostile trait matches or hardcoding the integer arrays.

## Verification

Run: python3 testdata/taxonomy/zmp-axios-placement/check.py

Nine controls check positive and near-miss token fields, repeated documentation
word counts, ordinary helper basenames, and a bounded literal population with
and without environment-read context. The random-like predicate also matched
in test-rules on the standalone checksum control; the engine strips an unused
component from ordinary scan output, which the controls account for.

Local cleave before/after scans of the complete archives show Axios has zero
suspicious/hostile traits and Zalo retains only the accurate suspicious
JavaScript string-array-runtime trait. Each PowerShell original retains its two
suspicious obfuscation traits. atomscan was rerun on all three originals and on
the checksum-qualified Axios PURL in isolation.
