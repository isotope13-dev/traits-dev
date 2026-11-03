# Package manifest queue review

The exported paths are a snapshot; Hopper holds current labels. Both the local
scanner and Atomscan were used on the artifacts below. A manifest's dependency
names or the reputation of its parent project do not establish the behavior of
separately referenced code.

A final Hopper dry run confirmed the current labels for all 38 snapshot
entries: 20 good, 14 bad, and 4 inconclusive.

The following manifests contain metadata, dependencies, and ordinary build or
start commands. Neither scanner reported suspicious or hostile findings, and
Hopper moved them to **good**:

- `fa4ed54ea124c9206f3b2b97d3814f8712e56ed437a2cc09d4fab18f160f8d40`
- `238764b846ee591ba95d00cff2c76120102ab7da8332f9a9d51ebb104127d90a`
- `df923efd743654b61e9f63f612720acca8ee79519138ff87d9e6da0e4388d625`
- `f3e0a7feb2eae1a870f681b46b45b5c3d5b160e6086285d0fa5af68d522c3101`
- `adcb3b8f9d9c463a99504b578a24a6b6bc1d4b73bba291c923b8672017afb41b`
- `b1f093a780fc14da27e162ab8c1eb421a24887e3d0c2953c4994d171e13ec83f`

`3ead09ba6c4360694ae1f6063967d60e892b066cfb008c0ff9cd2b38d1062214`
contains a test script that directly invokes itself with `npm run test`.
This is a resource-exhaustion risk when the test is run, but the manifest does
not establish malicious intent; Hopper moved it to **good**. A new suspicious
finding identifies the recursion, and both scanners report it. The finding
also applies to renamed JSON files with the same `scripts.test` value.

Six encrypted dataset archives each contain a placeholder entrypoint and an
npm manifest that directs runtime and development dependency resolution to
`packages.storeartifact.com`. The archive passwords are dataset packaging;
they do not establish that the original npm packages were encrypted. The
remote payload is not present in these archives. [Sonatype's PhantomRaven
research](https://www.sonatype.com/blog/phantomraven-npm-malware) identifies
all six package names and describes this remote-dependency delivery pattern.
The artifacts' host, package structure, and names match that report. Hopper
confirmed the existing **bad** labels:

- `444e2809000cea139182f20e9f7e5581966e85f951c15403d3d55fea157c4036`
- `7ed0963b472a4e7343999ae9f26c57103e9c3bf8d160277fe95ce4adc8a6277a`
- `7c59bf0052eb2f5ea885caf381c7cfd0f7d8527301cdc60cab7e8742e5da12bc`
- `0d62b43a055de0326fd96c40e424911717b760c0bf1feade30c16856af3d8ee2`
- `699ea15785e06b46339be34f09537f1ec4a01dd95098ed5518f9c07d4d0e1837`
- `7b6024f12440c84dcb66f92843a315ae4a2bcca3acf541f8d7dd18aec2713339`

Both scanners now identify the researched family-specific manifest pattern as
hostile. The generic no-op-plus-external-dependency rule remains suspicious:
a default test command alone does not prove a remote payload is malicious.
The scan reports still have overlapping plaintext-dependency observations.
The remote payload is absent, so its individual behaviors cannot be inferred
from these packages.

Four standalone manifests contain metadata and ordinary build or development
commands; referenced implementations were not part of those individual files.
Both scanners reported no suspicious or hostile findings, and Hopper moved
them to **good**:

- `2eecf8bc9063f6b481ac9f48d6f8b587074167223725b133e587389faf964b35`
- `36c002166b26cc822edc3b0af8042e4dae09b349298f78cf643b74ea897f4a7f`
- `d48203904fcc6f99fd3e321f89f4b5f03426526b56ca429aaf526838d73deaa0`
- `eaaad9511c8f324e6dbcaf7a28afab048b93e3d393d1431581b85b1eabb2bb06`

Hopper confirmed **bad** for these three archives:

- `a175bfe6be82b40da9feabeac45a22a8b844b8c7c7fa412a9d5f2593f135f9b2`
  contains an obfuscated Windows downloader that requests elevation and
  attempts to add a Defender exclusion. Both scanners now report a hostile
  co-occurrence finding for these behaviors. The [OSV report](https://osv.dev/vulnerability/MAL-2026-10064)
  independently describes the same package and loading path. Static evaluation
  of its rotated string array shows that it constructs a `chrome.exe` path
  inside the user's Chrome `User Data` directory for the downloaded file; a
  separate Defender exclusion targets a Windows Explorer package path. These
  are source-level attempts, not proof that download, exclusion, or execution
  succeeded. Cleave now recovers a separate source layer from proved plain
  string-table rotations and immutable aliases without running JavaScript.
  In that layer, a structural rule binds the Chrome-profile path and executable
  name to the write stream, and binds that stream to the HTTP response pipe.
  Both rebuilt scanners report the bound observation and a second hostile
  finding in the package and decoded layer. Focused tests cover different
  paths, responses and streams; decoder regressions reject escaped or mutable
  aliases, altered lookups, side effects and unproved rotations. Full uncached
  validation passes. The binding describes source, not runtime success.
- `cfced1b52881575b46b4ff48e02737d11f5fcc56fd33f8f1f670d93399ac344c`
  contains a bot with a hard-coded extra administrator who can request other
  users' refreshed tokens, plus a webhook reporting server invitations. Both
  scanners report hostile invite-transfer and administrator/token-reply
  findings. The latter combines a same-ID administrator-list insertion, an
  administrator-gated target selection calling the refresh handler, a bound
  target-file-to-token-attachment reply, and the invite webhook finding. These
  are static observations in one file; the combination does not prove that a
  request or transfer succeeded. Focused tests cover mismatched IDs, lists,
  target selections, input files, results, and reply recipients, as well as
  the absence of the Discord webhook finding. Full uncached validation passes.
- `0b867c68535e4412c2fa2431732816fa5299c6141a11136b02befe5863faad80`
  pins a specific attacker-created dependency, although the dependency payload
  is absent from the archive. [Endor Labs' analysis](https://www.endorlabs.com/learn/npm-is-serving-malware-to-134k-developers)
  identifies both this package version and its pinned dependency as part of
  the malicious chain. Both scanners now report that specific chain as hostile.

The obfuscated loader scan reported flow-analysis limitations; its decoded
source and the static bindings above do not establish runtime success. The
pinned dependency in the third archive is not present for behavioral review.

`2fb9ca15e2ddde29970b2ce36fb0da4c8f5304b34d360595fb159d5b2cca706a`
contains a CLI scaffold and visual progress animations. The animation scripts
are not referenced as install hooks by its manifest. Both scanners reported
one suspicious finding for the encrypted dataset archive; Hopper moved it to
**good**.

`e19e4915f3a9b3d99cc18e18668ff2c1f4718aff4711c57dd1a3c20ba8748f9c`
matches the PhantomRaven package and dependency pattern described above. Both
scanners report the family-specific hostile finding; Hopper confirmed **bad**.

`03d3d8a41cd3e9b28813c36316268d8053c714ab364e928bf52799f3f4bd7f66`
is a scanner crate containing executable downloader demonstrations using
reserved example addresses. One fetches to a hidden path, makes that same
path executable, and executes it. A new suspicious rule ties the three path
operands together; both scanners report it on the extracted fixture. The crate
also contains a postinstall pipe-to-shell demonstration that both scanners
report as hostile. Hopper confirmed **bad** under the exploit/PoC fixture
policy. The Atomscan archive report was valid JSON despite exit status 2; the
local archive scan recorded flow-analysis gaps for some members.

`80cd341894c6914a07b8f405071f1fc29f9059e9930f8ff56455953174b46675`
contains a preinstall command that requests the GitHub CLI authentication
token as a webhook POST body, followed by a semicolon and a separate recursive
root-deletion command. This is static command evidence; neither the transfer
nor deletion was executed during review. Both scanners report separate hostile
findings. The token rule now binds the token substitution to the webhook POST
within the preinstall value, and the root-delete rule requires a possible
command boundary before `sudo` instead of matching arbitrary preceding command
arguments. The latter is a text-level check and does not fully parse shell
quoting. Focused tests cover separate commands, argument-only text, and
unrelated token and POST statements; full uncached validation passes. Hopper
confirmed **bad**.

`9e69aa771d29d1981b4d8e148fe5ec524564622f823a7bd9b60d626d0534b413`
and `646d6bb1fa72874e8f49596136cd03075bd4b51457ff0bd944ed96ba64f620c1`
are two versions of a daemon with large obfuscated JavaScript bundles and an
agent session hook. Both local scans reported no suspicious or hostile traits,
but the bundles have limited flow analysis. The separate Atomscan runs produced
reports and exited 2. Both scanners now report two suspicious combinations in
the extracted main bundles: obfuscation alongside credential-like environment
access and alongside a computed process launch. Those findings do not establish
exfiltration or a malicious child process. The bundles' encoded application
logic and limited flow analysis prevent a confident behavior assessment.
Hopper moved both samples from good to **inconclusive**; resolving the decision
requires deobfuscating their application logic. Re-scans after the plain
string-table decoder improvement each represented seven records with two
analysis gaps; neither produced a decoded source layer. Their labels therefore
remain inconclusive.

`ba1e8e019b31dda97af235a9ca1b116aace607233858a3b256fb1671900436ff`
contains an explicitly named setup command that pipes a security-tool installer
to a shell, plus logging utilities that can suppress console methods. Both
scanners report the pipe as hostile and the suppression as suspicious. The
pipe's intent and classification remain under review; the command's presence
alone does not prove attacker control of the fetched code. The local Cleave
package analyzer now reports manual interpreter pipes as suspicious and keeps
automatic lifecycle pipes hostile. Its regression test verifies that a
manual script cannot mask a hostile automatic hook in the same manifest.
Both the rebuilt local Cleave and a locally built Atomscan using that analyzer
now report the pipe as suspicious, rather than hostile. The separate console
finding comes from explicitly documented library methods that assign no-op
callbacks; the finding description no longer claims those methods ran. The
final local all-files scan represented all 1,349 archive files and reported
analysis gaps in 367 records; Atomscan represented 1,011 records and exited 1
after producing JSON. The source and build files implement data models and
framework utilities, and the only child-process helper found in the included
source runs a local test runner. The manifest's `prepare` hook invokes Husky;
the security-tool installation command is a separate manually selected script.
The two supported suspicious observations remain visible. The reviewed
artifact is **good**, and Hopper confirmed its existing good label. This ruling
does not assess the remote installer or dependencies absent from the archive.

`b80a37d275183a3dc4e9ededeef91f6a8135b3710add9efee66dadcb00e4babd`
is a device-management extension. The local all-files scan represented all
267 archive members and reported no suspicious or hostile traits; 88 records
had analysis gaps. Atomscan reported no suspicious or hostile traits. Hopper
moved it to **good**.

`f05b36b4f92ae86b8cc7b283c26c1123d2cee5c65ec420c8bebbaf632ab3e809`
is a proxy wheel that accepts a user-provided API key and writes it to an
`.env` file during setup. A neutral finding now identifies the interpolated
API-key assignment. The local all-files scan represented all 102 members and
reported no suspicious or hostile traits; 13 records had analysis gaps.
Atomscan's high findings came from a fetched dependency, not wheel members;
it also reports the new observation on the extracted setup script. Hopper
moved the wheel to **good**.

`86cac5c5017a94c44dd3b860fbe94b1ddf898fdcbd053145470b702a0561e741`
contains an Android bootstrap that serializes an account's complete IMAP
configuration, including its password field, into a silent remote logging URL.
Both scanners report a hostile finding on the extracted source after the logger
rule was tightened to bind the encoded value to the logger's message parameter.
The package's bundled NativeAOT executable also imports thread and token APIs;
those references alone do not establish privilege use or thread hijacking. The
finding is now downgraded when the matching NativeAOT runtime surface is
present, and its description states the observed references. Atomscan had also
reported inspection blocking on a UI handler that explicitly allows F12. The
F12 observation now requires cancellation within the matching branch; Atomscan
no longer reports the false positive on the extracted UI source. The local all-files scan covered all 805 archive
members, with analysis gaps in 334 records. Hopper confirmed **bad**.

`866d31461f22d5a1f579edb448c7b981764330e963c2b76c7208851c5f7e4258`
is a source archive for an application. Its CI configuration includes a
download-to-shell installer command, now recorded as command text without
claiming execution or hostile intent. The local all-files scan represented all
3,114 archive members, with analysis gaps in 1,441 records and no suspicious or
hostile traits. Atomscan's high-severity findings were on fetched dependencies,
not archive members. The available evidence supports **good**; Hopper confirmed
the sample already had that label.

`03b3ff18820f8c611e2a976aa1c8120b3b8ed421a0f138c4c1a632cde9261f47`
is a VS Code mobile-development extension. The local all-files
scan represented all 26,434 archive members; 8,564 records reported analysis
gaps, primarily JavaScript flow-analysis limits. Its only high-severity finding
was a `dist/` claim in the bundled `make-error` manifest, although that
directory is present and the declared prepublish script builds it with
Browserify. Browserify is now recognized as a build tool, and the generic
manifest-only observation is notable rather than suspicious. The independent
Atomscan reported no suspicious or hostile traits. The extension's entry point
also had flow-analysis limits; the available evidence supports **good** and
Hopper confirmed that the sample already had that label.

`27eacd7cb8bf47c6411dd40533be8a112f96d939bda363682aedbf1ce5043651`
is a debugging assistant extension with bundled native libraries and a large
compiled entry point. The local all-files scan represented all 4,134 archive
members; 1,646 records reported analysis gaps. Two nested polyfill manifests
use parent-relative entry points to files within their enclosing package; the
rule now requires a versioned manifest before calling that pattern suspicious.
In the bundled Claude Code CLI, hardware and messaging indicators were spread
across unrelated portions of the file. The fingerprint rule now requires
proximity and describes indicators rather than asserting exfiltration. Another
file-wide encoding profile was reduced to notable; the CLI retains a separate
suspicious finding for actual nearby Base64/XOR reconstruction. Atomscan also
joined registry and expression clues more than three million bytes apart in
the minified CLI; the rule now requires byte proximity as well as line
proximity. Its other high findings were in a separately fetched runtime. The
available evidence supports **good**, with the stated flow-analysis limits;
Hopper confirmed that label was already present.

`d0b5c8923ba846c30e3d389644dec1217604d6110081d57deacbb38fbed5777f`
is an Arch Linux package for a self-hosted audiobook server. Its systemd
service runs the Node application as a dedicated service user. The local
all-files scan represented all 6,124 archive files and reported analysis gaps in
2,922 records. Its only high-severity finding was repeated in Moment locale
files, where an `isFunction(output)` helper call was mistaken for a dynamic
`Function(output)` evaluator. The evaluator rule now respects identifier
boundaries; a rescan of the affected source no longer reports the finding.
Atomscan found no suspicious or hostile traits on package members; its one
high-severity finding was in a separately fetched dependency. Hopper moved the
reviewed package to **good**.

`460e19395f878aa3411d1c440b3a3c1119f8c004c6b945efe63ae797d7312de0`
is a Node-RED conda package. Its recipe includes build-time
package installation and service configuration. The local all-files scan
reported no suspicious or hostile traits and 9,929 records with analysis gaps.
It represented 17,335 of the package payload's 17,365 non-directory entries;
the other 30 are symbolic links. The independent scan reported high-severity
HTTP test findings only in a separately fetched Twisted
dependency. Hopper moved the reviewed package to **good**.

`44731a93b4cb34d352a4653b9bee913c72f59168dcb064d360b5dd283a1b22a6`
is a Windows installer identifying itself as Outbyte VPN Setup 2.1.7. Its
extracted main JavaScript disables Node TLS certificate verification, a real
suspicious behavior. The extracted VPN up/down scripts and manifest have no
high-severity findings. The all-files scan produced hostile process-injection
and screen-upload claims on bundled NW.js/Chromium runtime binaries; these
claims combine static API and string evidence, not demonstrated injection or
upload. The unmap and bitmap/multipart combinations now report suspicious
indicators without asserting those actions. The window-hook pattern remains
suspicious for a library matching several NW.js runtime identity fields;
the broader window-hook detection remains available. Both scans also reported
other suspicious runtime indicators, and Atomscan flagged an external npm
security-holder package. The executable's claimed identity alone does not
establish its behavior. A comparison against the official
[NW.js 0.36.4 release](https://nwjs.io/blog/v0.36.4/) found byte-for-byte
matches for the bundled `nw.dll` and `nw_elf.dll` from the 32-bit standard
build and `nacl64.exe` from the 32-bit SDK build. The vendor-signed application
executable differs as a file, but its `.text` section matches the official
`nw.exe` code section. These comparisons account for the flagged runtime
components, not the application's JavaScript or the installer as a whole.
The application also constructs login requests with an encoded password in
the URL path while Node certificate verification is disabled. A new neutral
syntax observation exposes the password-labeled URL argument without claiming
that a request was sent; both scanners report it. The app loads and invokes a
bundled V8 bytecode module that provides its token and service configuration.
The module's strings include service references, but its full executable
behavior was not recovered; the runtime comparisons do not account for this
module. The fresh Cleave scan produced 1,601 records with 510 analysis gaps;
Atomscan produced 1,340 records and exited 2 with JSON. The reviewed source
shows security risks but does not establish an attacker payload, and the
unrecovered bytecode prevents a confident benign ruling. Hopper moved the
installer to **inconclusive**. Focused tests and full uncached validation pass.

`82d2b0397dba3749c0444a70a197edaf4c862d815f00c2c4b47746c8e11da4f7`
is an Electron installer whose installation handler runs an encoded loader.
The decoded loader fetches a remote location and evaluates a decoded response;
the archive also contains a helper that exits on detection of analysis tools,
although its invocation has not been established. Both scanners report the
hostile loader in the nested application archive. The local all-files scan
reported analysis gaps in 1,990 of 5,465 records. Separate static binary
patterns on the Electron runtime had overstated execution: the aliased-export
rule now requires a DLL and describes API names, while Electron runtime
context keeps its window-hook indicators suspicious. Hopper confirmed **bad**.

`d5aca57b445647b20ffc105a79ee56e5137967bb23f5690b315e78cb66058f9f`
is an NSIS installer containing an Electron application with several large
JavaScript files and dependencies for screenshots, Windows data protection,
SQLite, networking and process execution. Those capabilities alone do not
establish intent. The local all-files scan returned 5,265 records, with 2,178
analysis gaps; the three application JavaScript files are heavily obfuscated
and each reports a computed-constructor/require observation. The hostile
security-holder result comes from an inert `fs` placeholder manifest, not a
malicious payload. Repository policy still scores this placeholder as hostile;
its description now identifies the actual manifest. Atomscan also reports the
computed-constructor finding and two Electron-runtime API profiles; its other
high findings are on fetched dependencies. A second suspicious observation
now records the combined computed-constructor, array-rotation and conditional
indexing pattern, without claiming a decoded payload. The application's actual
behavior remains unresolved because its three large scripts are heavily
obfuscated and the flow analysis is incomplete. Both scanners report the two
suspicious source observations. Hopper moved the sample to **inconclusive**;
resolving its application behavior requires further deobfuscation. A fresh
all-files scan after the plain string-table decoder change again represented
5,265 records with 2,178 analysis gaps and produced no decoded string-table
layer; the identified limitation remains.
