# HTTP exfiltration composites follow the identified source

The initial source-routing pass moved four composites out of
`objectives/exfiltration/http/upload` because their required source evidence
was more specific than the channel:

- Cloud Kubernetes secrets plus hybrid encryption → `stealer/cloud`.
- Environment credential harvest sent to a router endpoint → `stealer/env`.
- File-content records plus a harvested npm token and GitHub repository
  creation → `stealer/file`.
- Environment-secret evidence near encoded GitHub contents writes →
  `stealer/env`.

The rule IDs and matcher conditions remain unchanged. Effective file-type,
platform, scope, criticality, confidence and attack settings are retained. The
GitHub contents-write rule description now says “near” to avoid claiming that
the matcher binds the harvested environment values to the encoded write. The
GitHub dead-drop consumer now uses the canonical cloud-source ID.

A synthetic Python router example matches `credential-router-exfil`; a
control containing the same `/router` endpoint and environment enumeration but
no send does not. A synthetic JavaScript file with recorded file contents, an
npm-token pattern and an authenticated GitHub repository call matches the new
`stealer/file` rule. Soft validation passes **1,837/1,837 fixtures**. Strict
validation remains at the existing **60 issues** and **160 over-cap
directories**; the refreshed snapshot measures **4,480 excess rules**.

The GitHub source composites remain probable inferences, not proven payload
flows. `github-repo-harvested-env-exfil` remains in the HTTP-upload audit: it
requires repository creation and environment encoding but not an explicit
contents-write operation, so its objective claim needs a separate matcher and
placement review.

## Credential-source follow-up

Three JVM composites requiring developer-credential reads and HTTP/curl
transfer moved to `exfiltration/stealer/dev-secret`. The Swift iOS Keychain
marker and its HTTP transfer composite moved to `exfiltration/stealer/keychain`;
the shared URLSession POST atom remains in HTTP upload. The moved rule bodies
and effective rule settings are unchanged, and repository-wide searches found
no external consumers. Upload is now 191 rules; the destination leaves are 76
and 21 rules respectively. A refreshed full audit records 160 over-cap
directories and 4,475 excess rules. `make validate` still fails on existing
catalog-wide issues, including the 85-rule cap, while reporting no broken
reference for these moves.

## Additional source-specific cases

The same source-first rule also routed SSH-key exfiltration and authorized-key
uploads to `stealer/ssh`; browser camera/microphone recordings and extension
screenshots to `stealer/surveillance`; device-code OAuth forwarding to
`stealer/token`; Sui wallet archives to `stealer/wallet`; ESXi credential
configuration to `stealer/appliance-config`; required BSD credential source
combinations to `stealer/sweep`; and Python driver-log and source-code sends to
`stealer/file`. The Swift shadow/SSH plus shell-history chain also belongs in
`sweep` because it requires multiple source classes. The OAuth phishing
composite now consumes the relocated token rule. The generic
MediaRecorder plus upload-route composite remains under HTTP upload because it
does not establish a sensitive capture source. Matcher conditions and
effective rule settings were retained. HTTP upload is now 176 rules, and the
destination leaves contain 18 SSH, 31 surveillance, 34 token, 34 wallet, 33
appliance-config, 84 sweep, and 52 file rules. Soft validation passes all
1,837 fixtures; the full audit has 4,460 excess rules across 160 directories. Strict
validation continues to fail on the wider catalog backlog.

| Previous ID | Canonical ID |
|---|---|
| `objectives/exfiltration/http/upload::python-hybrid-encrypted-secret-exfil` | `objectives/exfiltration/stealer/cloud::python-hybrid-encrypted-secret-exfil` |
| `objectives/exfiltration/http/upload::credential-router-exfil` | `objectives/exfiltration/stealer/env::credential-router-exfil` |
| `objectives/exfiltration/http/upload::github-repo-contents-token-exfil-rest` | `objectives/exfiltration/stealer/file::github-repo-contents-token-exfil-rest` |
| `objectives/exfiltration/http/upload::github-contents-credential-fallback` | `objectives/exfiltration/stealer/env::github-contents-credential-fallback` |
| `objectives/exfiltration/http/upload::aws-shared-credentials-http-exfil` | `objectives/exfiltration/stealer/cloud::aws-shared-credentials-http-exfil` |
| `objectives/exfiltration/http/upload::jvm-agent-credential-http-exfil` | `objectives/exfiltration/stealer/dev-secret::jvm-agent-credential-http-exfil` |
| `objectives/exfiltration/http/upload::kotlin-developer-credential-http-exfil` | `objectives/exfiltration/stealer/dev-secret::kotlin-developer-credential-http-exfil` |
| `objectives/exfiltration/http/upload::jvm-developer-credential-curl-exfil` | `objectives/exfiltration/stealer/dev-secret::jvm-developer-credential-curl-exfil` |
| `objectives/exfiltration/http/upload::swift-ios-keychain-payload` | `objectives/exfiltration/stealer/keychain::swift-ios-keychain-payload` |
| `objectives/exfiltration/http/upload::swift-ios-keychain-http-exfil` | `objectives/exfiltration/stealer/keychain::swift-ios-keychain-http-exfil` |
| `objectives/exfiltration/http/upload::swift-timing-bit-exfil` | `objectives/exfiltration/stealer/ssh::swift-timing-bit-exfil` |
| `objectives/exfiltration/http/upload::swift-hex-chunk-http-exfil` | `objectives/exfiltration/stealer/ssh::swift-hex-chunk-http-exfil` |
| `objectives/exfiltration/http/upload::swift-system-data-ssh-keys` | `objectives/exfiltration/stealer/ssh::swift-system-data-ssh-keys` |
| `objectives/exfiltration/http/upload::swift-timing-sidechannel-exfil` | `objectives/exfiltration/stealer/ssh::swift-timing-sidechannel-exfil` |
| `objectives/exfiltration/http/upload::swift-http-hex-data-exfil` | `objectives/exfiltration/stealer/ssh::swift-http-hex-data-exfil` |
| `objectives/exfiltration/http/upload::browser-av-recording-form-upload` | `objectives/exfiltration/stealer/surveillance::browser-av-recording-form-upload` |
| `objectives/exfiltration/http/upload::device-code-oauth-panel-upload` | `objectives/exfiltration/stealer/token::device-code-oauth-panel-upload` |
| `objectives/exfiltration/http/upload::python-sui-wallet-targz-github-upload` | `objectives/exfiltration/stealer/wallet::python-sui-wallet-targz-github-upload` |
| `objectives/exfiltration/http/upload::swift-key-collect-upload` | `objectives/exfiltration/stealer/ssh::swift-key-collect-upload` |
| `objectives/exfiltration/http/upload::swift-shadow-collect-upload` | `objectives/exfiltration/stealer/sweep::swift-shadow-collect-upload` |
| `objectives/exfiltration/http/upload::browser-extension-screenshot-json-upload` | `objectives/exfiltration/stealer/surveillance::browser-extension-screenshot-json-upload` |
| `objectives/exfiltration/http/upload::objc-bsd-credential-http-exfil` | `objectives/exfiltration/stealer/sweep::objc-bsd-credential-http-exfil` |
| `objectives/exfiltration/http/upload::esxi-key-material-http-exfil` | `objectives/exfiltration/stealer/appliance-config::esxi-key-material-http-exfil` |
| `objectives/exfiltration/http/upload::python-posts-system-driver-text` | `objectives/exfiltration/stealer/file::python-posts-system-driver-text` |
| `objectives/exfiltration/http/upload::python-source-upload-to-transform-service` | `objectives/exfiltration/stealer/file::python-source-upload-to-transform-service` |
