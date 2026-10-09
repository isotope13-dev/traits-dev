# Public-registry second review

All three primary artifacts are malicious by inspected behavior, independently
of their prior labels. No threat-feed attribution or family identity is claimed.
The files were inspected statically; their network requests were not executed.

* `2909fd9991c8…` (`pad35_128.com`) is a padded, direct-action DOS overwriter.
  Rizin's 16-bit disassembly shows find-first on `*.C*`, read/write open of the
  default DTA filename at PSP offset `009Eh`, AX-to-BX handle transfer, write
  from `0100h`, close, and RET. CL is set to 35 (CH is inherited). With CH zero,
  the first 35 bytes overwrite the selected file's entry, including this same
  search/write program and its wildcard. There is no append, restoration,
  resident installation, encryption, or enumeration loop. The original 128-byte
  artifact is the 35-byte code/data body plus zero padding. The capability
  description now says writes **from** the COM entry rather than implying it
  copies every byte of the padded artifact. Three existing hostile traits remain.
* `64c11bd97f7d…` (`ci-token-exfil.js`) resolves GITHUB_TOKEN or GH_TOKEN and
  interpolates it into Axios's Discord webhook message body with the repository
  name. This is disclosure to a chat collector, not GitHub authentication. The
  webhook looks placeholder-like; a successful delivery is not established.
  The direct-content and fallback expressions lack usable source provenance,
  so the new AST
  matcher binds an immutable token, the required Axios receiver, the literal
  webhook destination, and the actual template substitution. Reassigned aliases,
  other receivers/modules, first-party URLs, and build-status bodies are controls.
  The generic hostile rule now needs a bound credential body rather than a POST
  or endpoint merely near a credential name. Both hostile composites exceed
  the 3.5 precision floor (generic 5.4, CI-specific 5.9 in focused checks).
* `5a64388a9163…` (the XPI) claims to be a history utility named Phillips Wade,
  but its popup copies TronLink branding and links every wallet action to the
  mnemonic form. login.html loads app.js and login.js. login.js reports the
  trimmed field after a one-second debounce and always displays an invalid
  phrase error on submission. app.js constructs `http://193.148.56.48/app.php`
  from arithmetic octets and charcodes, then POSTs the supplied data as JSON.
  background.js polls the clipboard with jitter, suppresses unchanged text,
  splits text into random-size chunks, and GETs URI-encoded chunks with sequence
  fields to `http://193.148.56.48/continue.php` using no-cors. Its declared
  clipboard permission and no-data-collection sentinel contradict the export.
  The clipboard finding now requires that the loop's chunk is the value encoded
  into the URL actually passed to fetch. Two hostile findings remain:
  wallet-secret reporting and deceptive no-data disclosure. Source-bound clipboard export is suspicious on its own because
  legitimate clipboard synchronization is a possible near miss. The HTML
  recorder iframe and hidden CSS are copied UI residue, not surveillance claims.

## Trait placement and scope review

CI environment references and GitHub actor/repository reads moved to os/env/cicd;
GitHub token shell references and name/lookup co-occurrence moved to os/env/vcs.
The mixed developer-token reference union moved to os/env/secret-name. The Go
AWS-secret read moved to os/env/cloud, its documentation suppressor to package
documentation/claims, and the plugin-version basename to file/naming. Credential
file/read proximity and Cargo credential-read facts moved to neutral capability
homes; their cross-store source union is now a notable auth/secret observation.
These capabilities supply intent rules but do not independently assert theft.
Exact consumers were updated. Broad discovery/credential-access/stealer selectors
were audited: neutral source observations were deliberately removed from those
intent pools. Discord's selector now names completed export rules instead of
letting source-only stealer components stand in for a send. Reconnaissance beside
credential export moved out of supply-chain/trojanized into the export subject;
its prerequisite is now a completed export, avoiding self-reference.

The former multi-language generic developer-upload rule was intentionally
narrowed to JavaScript/TypeScript bound webhook content. Mere credential access
beside a POST, tar, curl, or endpoint does not justify hostility. Existing separate
language-specific and flow-based upload rules remain. This is a matcher/severity
coverage correction, not a placement-only migration. New rules use existing
admitted leaves, with no new partitions or engine changes. JSON serialization
and the complete mnemonic textarea observation are notable capabilities.

## Controls

Run `python3 testdata/registry-second-review/check.py` from the repository root.
The runner copies fixtures into a temporary directory outside `testdata`, because
existing path-based test suppressors otherwise conceal the observations under
review. It scans the fixtures without executing them and removes the copies.
Positive controls preserve detections after alias renaming and endpoint changes.
Negative controls cover status-only bodies, receiver/module mismatches, mutable
aliases, first-party URLs, unrelated encoded content, and unrelated fetch URLs.

Additional controls cover direct environment-member content and a credential-file
read bound to webhook content; unrelated file-read/status messages stay clear.

A further credential-file control exposed an older webhook rule that convicted
a file read beside a status-only send. It now requires the same file-content-to-
message binding and lives in stealer/credential rather than messaging/webhook.

The unrelated-file/status control also exposed npmrc-read/Axios proximity rules.
Those observations are now accurately named notable file-input capabilities,
not supply-chain theft. The general Discord finding requires completed export
evidence rather than a credential path or source name.

Document-extension/string-search proximity also moved to a neutral notable
string-search capability; proximity alone does not establish document theft.

## Full-corpus compatibility

The full validator exposed credential uploads previously covered only by the
removed read/POST proximity rule. Source-bound replacements cover immutable
JavaScript file aliases, collected file arrays/maps, combined secret files,
Node chat bodies, Python file-content arguments and SMTP messages, Rust file
bodies, Go reader bodies, and adjacent PowerShell/Perl body assignments. The
HTTP composite also requires an explicit request destination. Its focused
precision score is 3.7, above the hostile authoring floor.

Python public-file uploads and overwritten aliases remain benign controls;
the coarse file-flow/source co-occurrence fallback was removed after it failed
those controls. The existing CI fixture also exercises Axios options.data.
Clipboard URL binding supports fetch and navigator.sendBeacon. Existing XPI
expectations now require two hostile findings, reflecting the corrected
suspicious clipboard severity; the staging expectation uses the moved neutral
credential-file capability. Expected malicious corpus coverage is retained.
