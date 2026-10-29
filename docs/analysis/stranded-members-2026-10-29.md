All three listed members are MALICIOUS from their retained bytes. The three
archives retain their confirmed-malware labels; they were not re-judged.
SHA-256 checks matched all three requested extracted-member identities.

Fresh local slow atomscan scans used the tracked HEAD rules as the baseline
and the edited checkout as the comparison, with reference fetching disabled
(`--follow=none`) and analysis caching disabled. `cleave facts` was collected
for each original archive and each extracted member. The earlier exploratory
scan command used the incorrect spelling `--follow none`, which treated
`none` as another path; its outputs were superseded by these verified scans.

| Artifact | Hostile before → after | Suspicious before → after | Classifier |
|---|---:|---:|---|
| Installer, standalone and archived member | 20 → 20 | 12 → 12 | Flagged → flagged |
| writer.js, standalone and archived member | 8 → 8 | 6 → 6 | Flagged → flagged |
| help.html, standalone and archived member | 4 → 3 | 1 → 0 | Below threshold → below threshold |
| macOS package aggregate | 20 → 20 | 13 → 13 | Flagged → flagged |
| parser-session ZIP aggregate | 8 → 8 | 6 → 6 | Flagged → flagged |
| CHM aggregate | 5 → 4 | 2 → 1 | Flagged → flagged |

Installer (8202c3887b75b107f76385fe36e7949860b7931cebd2c65899649556c37e30bc)
is a universal Mach-O credential and wallet stealer presented as an installer.
Both architecture entrypoints build a C++ string, obtain its character buffer,
and pass it to `system()`. Rizin traces the arm64 helper copying the encrypted
constant, skipping its four-byte seed, and invoking its byte-XOR decoder.
Independent decoding reproduced cleave's complete 37,077-byte command in
both slices: start state 0x11667; emit cipher XOR low state byte; update state
to `((state * 0x3785) & 0xffffffff) % 35999`. Both decoded commands agree.

The command runs osascript, joins quoted lines with returns, and executes the
resulting AppleScript. Its final handler calls the collection, credential,
upload, replacement and persistence helpers. It checks a cached login password
with `dscl . authonly`, otherwise repeatedly displays a masked Installation
password dialog until validation succeeds. It caches and stages that password,
collects Keychain, Chromium/Firefox/Safari stores, wallet-extension and desktop
wallet data, Notes databases/media or note bodies, and selected Desktop and
Documents files. The personal-file branch limits collection to 10 MiB; Notes
media has a separate 12 MiB limit. It stages system_profiler output, builds a
ZIP with ditto, uploads it with curl --data-binary to an HTTP /log endpoint,
and deletes the staging directory and ZIP.

Later helpers terminate Ledger Live, remove its application bundle through
password-fed sudo, download a replacement ZIP and extract it into Applications.
Another helper fetches shell command text, embeds it in a KeepAlive/RunAtLoad
LaunchDaemon, copies the plist into /Library/LaunchDaemons using sudo, and
bootstraps it. A failed bootstrap attempts a nohup fallback. The plist specifies
UserName, so successful installation would not itself prove that the final
payload runs as root. The exfiltration host is configured as charge0x.at.

The credential deception, broad targeted collection/export, wallet substitution
and unwanted durable activation tip the verdict decisively. Existing rules
already cover these distinct results, including obfuscation and cleanup; the
fresh comparison retains every Installer trait ID and severity. No additional
hostile trait was justified by an uncovered distinct behavior. This does not
establish successful execution, data loss or the server payload's contents.

writer.js (419285d369ff0ebace833f59151cdc43412d7f8203c57f5bab831435f9f7457c)
is a concealed environment exporter and remote-code evaluator in parser-session
1.1.9. At import it gathers the full process.env, package submodule version,
platform, hostname, username and non-internal IPv4 interface MAC addresses.
The hex-pair parser reconstructs axios, post, an HTTPS URL, headers,
x-secret-header, secret and then. The exported function resolves these table
slots into an Axios POST carrying the collected object, then evaluates the
response's data property. Its empty catch suppresses rejection reporting.
The configured endpoint is log-server-lovat.vercel.app/api/ipcheck/703.

The POST/eval operation is deferred until the exported function is called.
The provided package has material reachability problems: writer's relative
package.json resolves to a missing src/package.json, and src/index.js imports
a different .pnpm/httpreslog sidecar rather than this member. These problems
limit execution claims. They do not erase the complete exporter/evaluator
function retained in this member. Whole-environment export, concealed dispatch,
remote response execution and suppressed errors have no plausible relationship
to the package's session middleware facade. No absent sidecar's behavior or
unseen response payload is attributed to the retained writer. All eight hostile
and six suspicious findings are supported and unchanged; they cover its
environment, identity, MAC and platform exports, survey, concealment and eval.

help.html (8da3d93f84489ab85103bdd0cb5bd339ffe4be07a75a80c097959129f42c0d47)
is a Help-viewer downloader. Its Help Documentation/loading facade contains an
HTML Help Shortcut control with Item1 set to cmd.exe /c powershell. The command
disables profiles, requests a hidden window, bypasses execution policy, assigns
a TEMP executable path, downloads an EXE from softpeak.live, and passes the same
variable to Start-Process. Inline x.Click() names the embedded object's id.
The retained page therefore carries the attack even outside its CHM container.
Execution depends on a compatible Help host allowing active content and on the
network/payload being available; it proves neither runtime success nor a
compromised endpoint. The hidden executable delivery behind a help facade
tips its verdict.

The YAML changes correct admission and descriptions while retaining behavior:

* The two scripted Help trigger rules now require attack-specific context:
  hidden policy-bypassing PowerShell, or a linked download-to-launch operation.
  Generic shortcut configuration plus a scripted Click previously convicted
  a normal Calculator launch. Their names describe the stronger requirements,
  and the payload-launch consumer follows the renamed trigger.
* A related direct-PowerShell Shortcut rule also matched a harmless Get-Date
  command. Its exact conjunction and scope move to a notable process-launch
  observation under micro-behaviors/process/create/exec. Generic process
  mechanics and scripted activation alone establish no hostile payload.
  No exact consumer referenced that rule. Its ancestor consumers with possible
  attack implications are binary-scoped and cannot consume the HTML-only fact.
  The exec leaf now has exactly 100 rules; no budget exception was added.
* Removed the hostname-gated Softpeak family conviction: a selected endpoint
  plus generic Help execution does not establish a recognized malware family.
  The same endpoint matcher, file types and size limit remain as a notable
  URL reference. This is a relocation of an existing observation, not a new
  specimen-specific behavior signature. No endpoint reference is claimed to
  prove contact or C2, and behavioral detections require no campaign hostname.
* Renamed static-documentation-html-page to documentation-heading-html-page
  and updated every consumer without changing its matcher, scope or severity.
  A documentation-labelled heading establishes neither staticness nor genuine
  documentation. The umbrella description now names the actual markup clues.

Microsoft documents ordinary program launch as an HTML Help Shortcut feature,
including a Notepad example. This supports retaining process observations
without convicting every shortcut:
https://learn.microsoft.com/en-us/previous-versions/windows/desktop/htmlhelp/to-create-a-shortcut-in-a-help-topic

The member's only net severe losses are the unsupported hostname-based family
conviction and endpoint severity. The two trigger IDs are replaced by their
stronger behavioral versions; the linked payload-launch detection remains.
The endpoint and heading observations are preserved under accurate names.
No Installer or writer finding was lost, either standalone or archived. No
supported attack technique was lost. All three members meet the hostile
coverage goal.

Regression scans compare 27 existing fixtures, including browser attacks and
the earlier Help loader outside this batch. Twenty-six have identical severe
finding IDs; the Help loader retains its payload-launch finding and exchanges
the two old trigger IDs for the stronger versions. Four new controls (ordinary
scripted Calculator, hidden Get-Date, endpoint reference and documentation
heading) have no hostile or suspicious findings. A direct-PowerShell variant
of the existing malicious loader retains four hostile attack findings and
the relocated notable launch observation. Precision scores for the three
Help findings are 8.3, 7.2 and 8.2, above the authoring floor of 3.5.

The HTML classifier disagreement persists: standalone probability changes
0.992441 → 0.95882463, but grid level remains -1 despite three supported hostile
findings. The CHM aggregate stays flagged (0.93337005 → 0.9336637). Installer
and writer classifications remain flagged. Logs report feature-spec version 18
versus engine expectation 21, limiting the model's use of newer features.
No inaccurate trait was restored or duplicate added to increase the score.

Six one-line MALICIOUS markers were written beside the three original samples
and three extracted members. Their notes, also saved verbatim in the prepared
commit body, are:

```
Installer stealer: phishes passwords, steals files, installs daemon
parser-session writer: exports environment and evaluates server code
HTML Help loader: auto-launches hidden download-and-run command
Archicad package: confirmed malware; embedded credential stealer
parser-session ZIP: confirmed malware; environment-export payload
CHM help: confirmed malware; hidden executable download and launch
```

Facts, disassembly, independently decoded AppleScript, fresh before/after JSON,
fixture comparisons, precision output and prepared commit body are retained in
/usr/local/var/cyclotron/tmp.noindex/cyclotron-3244b108/scratch/stranded.
