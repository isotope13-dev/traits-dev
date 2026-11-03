# Shell queue review: archive with obfuscated browser modification

The archive `4c0070ece6f18b13aac8c2448a9f992c64f22c06825b5f1e1e485610afa9c938`
is an altered Python license-expression source package. It is **bad**: its
`src/license_expression/__init__.py` contains an obfuscated Windows payload,
not just the ordinary library code suggested by the archive name.

Static evaluation of the integer expressions used to construct strings shows
that install/build handling installs `pypiwin32`, searches shortcut locations,
modifies browser shortcuts to load an extension, and writes extension code with
clipboard access and replacement of Ethereum-style wallet addresses. The
payload contains a hard-coded replacement address. This assessment did not
execute the package or the payload.

The initial Atomscan reported obfuscation but missed the shortcut modification.
The local rules now detect that behavior by combining the shortcut creation
and save calls, launch-argument assignment, target-path reference, directory
walk, and obfuscation. A separate finding records a write of assembled text
alongside obfuscated character reconstruction. Hopper confirmed the existing
**bad** label.

A bounded, literal-only Python decoder now reconstructs the character-array
expressions without executing the package. When such a literal is directly
written and recognized as JavaScript, the written script is analyzed as a
separate layer. Both rebuilt scanners recover the 1,973-byte browser extension
from the original archive and report the address-replacement behavior. A new
hostile finding binds an element value, Ethereum-address substitution, and
its write-back to the same variables, alongside clipboard paste and copy
commands; it does not claim the commands succeeded. Focused tests check the
flow, unrelated values, missing commands, and placeholder destinations. The
decoder also bounds binding inspection and rejects indirect builtins access;
these safeguards retain the recovered layer in the original package.

Another composite described the evidence as a wallet-provider transaction
drainer even though it can match address replacement without a provider hook;
its description and that of the generic replacement observation now state the
actual evidence. This improves coverage of the decoded extension; it does not
establish coverage of every possible behavior in the archive.

# Modified OpenSSH source archive

Archive `6a9c230c4239775bab6600315586030fe185493106b0a13b83abb8629da9c4e0`
contains modified OpenSSH 5.9 source and is **bad**. The server authentication
code accepts a password assembled from character assignments and appends user
credentials to a concealed log. The client authentication code also appends
the entered password and destination to a log before sending authentication.
The installed scanner detects the server credential capture and bypass but
misses the client capture. A local source rule detects the latter; replacing
the logged password with a redacted value prevents the match. The current local
archive scan also detects the logging guard that suppresses audit messages for
the bypass. Validation passed, and Hopper confirmed the existing bad label.

# Kernel module initializer

`df3217486ddd6fec7feebc75bbfc6f2c7105d83dfb766776eb0008e980650c29`
loads a hard-coded kernel module and starts an SSH daemon. Its comments and
the module path call the module a rootkit, but this script does not contain the
module and its behavior cannot be verified from the artifact. The observable
operations also have legitimate uses. The endpoint classification is
**inconclusive** because the referenced module is unavailable, not because
authorization is unknown. The scan describes the module load, init script,
and SSH daemon without asserting that the absent module is malicious.

# Process-injection build helper

`8db82c9528c1ec1b891fd046974901003876c84f0b3ac3f71250c171bcc6b22a`
is a shell build helper that compiles externally supplied C sources and
combines externally supplied templates. It refers to process-injection beacon
objects, but contains neither their implementation nor an executable payload;
its own operations are compilation and packaging. It was classified **good**
as a supporting file. A repeated parent-directory path finding was renamed to
avoid calling this ordinary relative path a payload.

# AI agent service package

`0d5db539719d06a9f9f7f82c3cb9f9c2298b74eac7f6badd596d0c07d311520f`
is an agent service that registers a service, manages an AI agent and updates
its dependencies. The reviewed archive does not establish an attacker payload;
it was classified **good**. A package-wide finding had combined an unrelated
detached daemon launch and npm installation; the rule now binds the detached
and ignored-output options to the npm install call itself.

The `openclaw-client.js` CLI fallback constructs a shell command from message
content, escaping quotes and backslashes but not shell substitutions. On Unix,
that may allow a message containing command substitution to affect the shell.
This is a static security concern in the service, not evidence that the package
implements an attack; it was not executed or independently verified at runtime.

# Desktop automation package

`0e71d432744eae3ac0905dc5a8c59a56429c568ffa770698f858693cf6c54313`
is a desktop automation application. Its macOS installer clears quarantine,
re-signs the app and opens it, and an optional UI action authorizes the
application's container to connect to the host over SSH. The current archive
scan retains the suspicious quarantine-bypass finding. No embedded attack or
covert control was established; the package was classified **good**.

The scan had also characterized an ordinary CI download into a build directory
as artifact poisoning and treated subprocesses that write output to logs as
silent. The download observations now live in the neutral HTTP download tier;
the unsupported poisoning inference was removed, while a specific suspicious
pip-bootstrap lookalike check remains. The Node stealth-related composites now
require evidence that both output streams are ignored.

# OpenSSH configure script and remote-development extension

`7e0c910005b5bb865bb479986ccead642f5f5811e4d242ef70a5d0c7bdf1fd14`
is an Autoconf-generated OpenSSH configure script. It was classified **good**.
The scan had mistaken its local `/etc/default/login` comparison for an HTTP
login path and treated a bare `host` token followed by a newline as a host
directive. The matchers now distinguish those cases. A separate markup
description now says that heading-like lines are Markdown-style, because shell
comment banners can have the same syntax.

`34db34c613224d5ba70a98f4545825eeef4f4cf32ba858657d576ad78f20dbb4`
is a VS Code remote-development extension with a bundled Cygwin runtime.
Hopper confirmed its existing **good** label. The extension disables TLS
certificate verification process-wide, a supported suspicious finding and a
security risk. Cygwin's PE parsing, thread-context and remote-memory APIs are
observable capabilities but do not alone establish injection; their composite
was relocated to a neutral thread-information category.

# Scanner crate with executable attack fixtures

`9fbd27ac18872767c93f55cf2f175250f23d0fe9930b836f7383b518a05f5997`
is a source scanner crate that includes executable test payloads. One fixture
writes a PATH-shadowing shell script that sends `/etc/shadow` over HTTP;
another decodes and executes a command that sends `/etc/passwd` through
netcat. A package hook fixture also pipes a downloaded script to a shell.
The local archive scan reports three hostile findings for these implemented
behaviors. The archive is **bad** under the endpoint policy, and Hopper
confirmed its existing bad label. New detections cover the direct shadow-file
upload and the Base64-encoded account-file pipeline without relying on a
particular destination.

# Conda archive review

`394af265a63fe2e608892395a6c86f0ac5ed2a4be0dad575ca8b653b0378aa83`
contains a Quarto Conda package and a large Deno dependency cache. The initial
scan flagged character-boundary validation as obfuscation; that observation is
now a neutral string-conversion trait. The package also caches a YAML
JavaScript-function type that constructs and invokes a dynamic function while
resolving the tag; this is a security concern if enabled for untrusted input.
A new suspicious trait reports that combination without asserting an attack.
The all-files scan accounted for every extracted regular file; the only path
not individually reported was a symlink to another scanned file. Many members
report limited flow analysis. The current scan reports one distinct suspicious
trait and no hostile traits, and Hopper confirmed the existing **good** label.

# Agent telemetry source archive

`3aacdc2cc91729ea69dca3575c2f9c156c789fff02fe4bf8d0a7487208d08654`
contains an agent-monitoring project. Its hook captures prompt text as an
event field, and its cloud shuttle can upload logs to a configured storage
bucket when credentials and a run ID are supplied. These are meaningful
endpoint observations, but the reviewed code did not establish a covert
attacker payload; the archive was classified **good**. Its README describes
prompt telemetry and cloud storage, and the logging code requests secret
redaction. Redaction does not imply that all sensitive prompt content is
removed. The local scan found no suspicious or hostile findings, with limited
flow analysis reported for some members. A neutral Go composite now exposes
the co-occurrence of prompt-text field construction and prompt-event dispatch
without claiming an upload or data flow.

# Performance-monitoring source archive

`45af1904076791b853ff1ba673f7f3d662fcba98ba867a771285ba87b5963425`
is a large performance-monitoring source archive. Its command helper invokes
`/bin/sh -c` and manages the resulting process; an HTTP source file references
an HTTP success constant. Neutral rules now describe those facts without
claiming a backdoor or kill switch. A local scan reported no suspicious or
hostile traits, with flow-analysis limitations on some members. The separate
atomscan run flagged a fetched setuptools dependency, not an archive member.
`qa/640` also sets up a symlink from the logging utility's notices path into a
protected temporary directory and invokes the utility as root to test for an
unsafe write. The bundled utility uses `O_NOFOLLOW` to reject that symlink.
The test constructs an attempted privileged write through the symlink, so the
archive is **bad** under the exploit-test policy; Hopper confirmed its existing
bad label. Neutral observations identify the symlink command and the sudo
owner-only chmod command. A suspicious co-occurrence finding now identifies
the permission change, symlink setup, and privileged file check without
claiming a successful write. An additional structural observation binds the
checked file to the symlink target and the target's parent to the protected
directory, with a privileged program invocation between those steps. It does
not assert that the program opens the link. Both scanners report this on the
extracted test, and focused path-binding tests and full uncached validation
pass. The bundled `pmpost` source constructs its notices path from `PCP_LOG_DIR` and opens it with `O_NOFOLLOW`. A more specific finding now binds the test's notices symlink, protected target, privileged `pmpost` invocation, and file check, and also requires the program-path assignment. It reports an exploit test, not a successful write; the assignment and call are static observations rather than a proof of runtime variable values. Both scanners report the hostile finding in the extracted test and the archive. Focused tests cover mismatched paths, program names, privileges, and link types, and full uncached validation passes. Hopper confirmed the existing **bad** label.

# Local osquery dashboard script

`dad0e778fc1a82e5cbb959f0f7517b30ae231d2580fee1dbcf10e664bf0ac421`
uses a local osquery binary to collect CPU, memory, and process metrics for
five minutes, writes a local log, and renders the results in a local HTML
file. The reviewed script has no network transfer or attack payload and is
assessed **good**. A neutral rule now identifies its osquery executable
reference. Hopper confirmed its existing good label.

# Cloud image test archive

`cd6d0f78ab144275de375d1b49c31084930eb8a87fe551968747ccea343a5a1f`
contains cloud image test suites and startup scripts. A network performance
test installs iperf, reads VM metadata, and writes test results to guest
attributes. One installation path uses zypper with GPG checks disabled,
including when installing a remote RPM; a new suspicious trait exposes that
security risk. The local archive scan reports that one suspicious trait and
no hostile traits. The reviewed artifact does not establish an attacker
payload and was classified **good**. Atomscan could not analyze a fetched RPM
because its fetched content was not a valid CPIO stream; that external fetch
is not proof about the remote package's contents.

# Compute image tooling archive

The reviewed archive is **good**: its included scripts and configurations
implement image construction, publishing, provisioning, and VM tests. They
also contain the security-sensitive operations documented below. Four genuine
suspicious observations occur in separate members and are retained; lowering
their severity solely to meet a benign scoring target would conceal those
operations. The final Cleave scan represented 824 records, with 49 reporting
limited analysis; Atomscan represented 339 and exited 2 after producing JSON.
Manual review covered the executable paths and the limited-flow call sites;
remote installers and dependencies are not included in this ruling. Hopper
confirmed the existing good label. The paragraphs below preserve the review
history; references to an unknown label describe earlier stages.

`57d2b6a92b1b` contains cloud image building and testing tools. One build
workflow configures an SSH key from VM metadata, disables guest agents, changes
SELinux from enforcing to disabled in its configuration, and exports the
resulting disk image. Other members disable GPG checks or Windows remote UAC
filtering. These actions can have legitimate provisioning uses, but are
security-relevant on an endpoint. A new finding covers the in-place SELinux
configuration substitution. Its signing-image setup also enables rsyncd and
configures writable modules; a new neutral observation exposes the config text
without claiming that the daemon is reachable or the module is unauthenticated.
The all-files scan covered all 822 archive members and reported three distinct
suspicious findings, with analysis gaps in 49 records. The archive's
classification remains under review; the distinct supported security findings
should not be removed merely to make the package appear benign. A fresh
all-files Cleave scan represented 824 records, and an independent Atomscan
represented 336; both reported the same three security observations in
separate archive members and no other suspicious or hostile archive-member
findings. A keyword search of the archive for common exploit and CVE terms
found no matches; this is not a complete review of all executable behavior.

The bootstrap script retrieves a VM service-account token from metadata and
uses it as an Authorization header for storage requests while shell command
tracing is enabled. This can expose expanded credentials in tracing output;
it does not establish credential theft. A new suspicious observation reports
the tracing and variable header together and suppresses the observation when
the file explicitly disables tracing. Both scanners report it on the extracted
script and in fresh archive scans; focused tests and full uncached validation
pass. A further inventory found 198 Go-template JSON files alongside 443
ordinary or comment-stripped JSON files; their presence and a keyword search
alone do not complete the archive review, so its label remains **unknown**.

The 198 Go-template JSON members use image-publishing fields and template
actions for environment selection, formatting, and version strings; a scan
of their action heads found no shell or command field. The 441 strict JSON
members include startup-script references and short test commands. Two SSH
test workflows configure a VM startup command to stop SSHGuard. A neutral
value-based observation identifies that command in the startup-script field;
both scanners report it in the archive, focused tests and full validation
pass, and no service execution is claimed. A 100 KiB high-entropy file with
a PowerShell extension is referenced by junk-script workflows and is
identified as data by `file`; its role was not inferred from its name alone.
The remaining executable members and analysis gaps still require review.

Further review of Windows provisioning found a command to disable Defender
real-time monitoring during disk-image preparation. An existing image-build
exception suppresses the intent-based suspicious finding; a separate neutral
command observation now preserves this security-relevant detail without
claiming execution or success. Both scanners report it on the member and in
fresh archive scans; focused tests and full uncached validation pass. A
container setup script also downloads a PowerShell installer to a temporary
path and starts it. A second variant does the same with a different download
source. The downloaded installers are not included in the archive. A neutral
finding records a file download near a PowerShell process launch without
claiming the paths are bound; both scanners report it in the two members and
the archive. Focused tests cover comments, distant calls, different programs,
and unbound paths, and full uncached validation passes. The remaining
executable members need further review before an artifact-wide decision.

The Windows post-install script conditionally creates a `NoAutoUpdate=1`
property when setting a WSUS server, and its later reset path removes the
policy and configures scheduled updates. A neutral command observation now
exposes the setting without claiming that it executed or that the later reset
succeeded. Linux COS package-replacement scripts stop and mask `update-engine`,
remove the `module.sig_enforce=1` boot argument, and add `ima_appraise=off`
when modifying a boot configuration. A companion script restores the root
filesystem's read-only argument, but does not itself restore those two integrity
arguments. The [kernel module-signing documentation](https://docs.kernel.org/admin-guide/module-signing.html)
notes that kernel build configuration can independently enforce signatures;
removing the argument alone does not prove enforcement is disabled. The
[kernel parameter documentation](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
describes `ima_appraise` settings. Neutral observations report the two `sed`
expressions and the service-mask command without asserting runtime effects.
Both scanners report all four new observations in the individual scripts and
archive. Focused tests cover disabled values, comments, different services,
and nonmatching expressions; full uncached validation passes.

The 102,400-byte high-entropy fixture has all 256 byte values and approximately
7.998 bits of entropy per byte. Its digest matches the corresponding
[repository file at the archived revision](https://github.com/GoogleCloudPlatform/compute-image-tools/blob/4e36307b1e7e/image_test/metadata-script/junk.ps1),
and the archive's workflow describes it as garbage input for metadata-script
tests. That correspondence supports the documented fixture role; it is not a
proof about every behavior in the archive. The refreshed all-files Cleave
report represented 824 records and retained 49 analysis gaps; Atomscan
represented 338 records and exited 2 while producing its JSON report. The
archive remains **unknown** pending the remaining executable and flow review.

The Windows update reset path also creates `AUOptions=4`. A separate neutral
observation reports that command alongside the `NoAutoUpdate=1` command;
[Microsoft documents](https://learn.microsoft.com/en-us/windows/deployment/update/waas-wu-settings)
those values as disabling automatic updates and scheduling installation,
respectively, when applied to the Windows Update policy key. This records both
code paths without asserting that either completed. Seven included Linux
kickstart configurations lock the root account and set SSH password and root
login to `no`; those findings do not establish that the whole archive is safe.

The Windows recovery helper stops a named VM, detaches its boot disk, creates a
rescue VM with a supplied PowerShell startup file, then detaches and reattaches
the disk and deletes the rescue VM. Neutral structured observations now report
the VM stop, attach, detach, delete, and startup-file commands. The old generic
file-deletion observation had incorrectly matched `-delete` inside the cloud
option `auto-delete=false`; it now requires a `find -delete` command, including
supported `sudo` and `busybox` wrappers. Tests retain real deletion detection
when the unrelated option appears in the same file. Both scanners report the
new VM observations and omit the false file-deletion finding on the member and
in the archive; focused tests and full uncached validation pass.

A manual review of Python command call sites found guest-image mounting,
package installation, metadata queries, SSH test helpers, and image metadata
upload. The shared guestfs helper writes caller-supplied command text into a
guest script and invokes it through the guestfs interface; this describes a
general execution capability, not an embedded attacker command. The ordinary
JSON startup-script fields include references to included test scripts, two
SSHGuard-stop test commands, and a small number of explicit test commands.
The current all-files Cleave scan represents 824 records and retains 49
analysis gaps; Atomscan represents 338 records and returns 2 with a JSON
report. Those gaps and the remaining executable paths still require review
before an artifact-wide decision.

The remaining Windows installer review found that the package installer reads a
GCS package path from VM metadata, copies the supplied package with `gcloud`,
installs it with GooGet, and invokes image sysprep. The SQL installer likewise
uses configured media and storage paths, opens TCP 1433, and starts installer
processes. Those descriptions concern the included scripts; downloaded media
is not present for inspection. The scanner had incorrectly associated the
package installer's metadata URL with an earlier `.EXAMPLE` directive across
the end of a PowerShell help block. The example-URL observation now stops at
the block terminator and describes proximity rather than claiming data flow.
Both scanners omit the misleading observation on the member and archive;
synthetic tests cover an actual example URL, CRLF, and URLs outside the block,
and full uncached validation passes. This conservative boundary can miss an
example that contains another `#` before the URL.

The metadata-script hash fixtures contain long random-looking comment blocks.
The PowerShell startup fixture computes and prints its own MD5; the shell
startup fixture writes and runs a generated file whose body consists entirely
of comments, then logs its hash. Its unquoted here-document contains no dollar
signs or backticks. Shutdown fixtures include a deliberate delay and hashing.
These static observations do not establish the behavior of the separately
referenced remote test data. The refreshed all-files Cleave report represents
824 records with 49 analysis gaps; Atomscan represents 338 and returned 2 while
producing JSON. The archive remains **unknown** pending the rest of the review.

The Debian worker downloads a tool to `/usr/bin/gce_export` and marks the same
path executable; the worker does not itself invoke that tool. A neutral
structural observation now binds the `curl` output and `chmod` arguments by
their source text, including commands within a function or an `&&` list.
Matching path text does not prove that a reassigned variable or filesystem path
refers to the same object at runtime. Both scanners report the observation on
the member and archive; focused tests cover different paths, protocols,
comments, quoted arguments, functions, and unrelated commands, and full
uncached validation passes.

The COS package-replacement workflow fetches several source repositories,
checks out a supplied guest-agent revision, applies selected overlay patches,
builds a package, and replaces files listed from that package in an image.
The fetched repositories and built package are not included in the archive;
the included workflow alone does not establish their contents. The fresh
all-files Cleave scan represents 824 records with 49 analysis gaps, while
Atomscan represents 338 records and exits 2 after producing JSON. The overall
archive remains **unknown** while the remaining paths are reviewed.

Two Windows image-building scripts use `gsutil cp` to copy a configured
`sbomutil.exe` to `C:\sbomutil.exe` and later invoke that literal path to
generate an SBOM. The executable is not included, and the source does not
prove the copy or invocation succeeded. A neutral PowerShell syntax rule now
reports the copy to an executable destination without asserting a network
transfer or binding it to a later call. Both scanners report it on the two
members and in the archive. Focused tests distinguish executable destinations
from executable sources, comments, unrelated commands, and string contents;
full uncached validation passes.

The reviewed batch members include VM network and boot checks, disk inventory,
and a local-SSD test. The SSD test writes a DiskPart command file that selects
disk 1, creates a partition, formats it as NTFS, and changes its drive-letter
assignment; it then pipes the file to DiskPart. These operations would affect
the selected disk if run successfully, regardless of their stated test purpose.
New neutral observations report the written format instruction and the pipe to
DiskPart without claiming either operation executed. The Windows setup batch
file also creates a SYSTEM startup task pointing to its setup script and later
deletes that script; existing observations expose those commands. The two
PowerShell modules configure the guest and write setup logs. Both scanners
report the new DiskPart observations in the archive, and focused tests and full
uncached validation pass. The archive remains under review.

The Linux export script obtains an SBOM tool from a metadata-selected storage
root, marks the copied `sbomutil` path executable, and later invokes it. A
related export script formats a metadata-selected buffer disk, copies a
monitoring script from storage, marks it executable, and starts it. The copied
programs are not embedded in this archive. New neutral syntax observations
report `gcloud storage cp` and, when the source text agrees, bind its
destination to a `chmod +x` target; matching path text alone does not prove
runtime identity, successful copying, or execution. Both scanners report the
copy in both scripts and the path binding in the first. Focused tests cover
uploads, different targets, comments, unrelated commands, and quoted
variables; full uncached validation passes. Review of the other shell helpers
included kernel source and changelog collection, VM networking tests, and
container image deprecation. The OS Login test creates a temporary SSH key and
disables host-key checking for its test connection. The end-to-end test mounts
the invoking user's gcloud configuration into its test container.

The Linux configuration-test Python call sites with limited flow analysis
inspect distribution settings, check root account state, query time and network
configuration, and exercise package and cloud command availability. The
Windows configuration test checks activation, interface MTU, runtime versions,
time service, EMS, timezone, and hostname. These reviews describe the included
test code; they do not resolve the remaining archive-wide analysis gaps.

The metadata SSH test requests `enable-oslogin=False` at project level before
testing metadata-provided SSH keys. Its included `SetMetadata` helper updates
common instance metadata through the Compute API by default; the test script
does not explicitly restore that OS Login setting. This is a project-wide
configuration request if the API accepts it, not proof that it took effect.
The test adds and removes SSH keys and checks expected access. The OS Login
master test also changes metadata and imports temporary keys, with a `finally`
cleanup for its master keys. The network test changes a test VM's IP aliases
and queries endpoints to check forwarding. A neutral Python syntax observation
now reports the explicit `SetMetadata('enable-oslogin', False, ...)` call;
both scanners report it on the member and archive. Focused tests cover true,
variable, unrelated key and method, comment, and string cases; full uncached
validation passes.

The enterprise Linux installer builds a bootable installation disk by creating
a GPT label and partitions, formatting them, and copying installation media
and kickstart files. New neutral Python observations report the `parted
mklabel` and `mkfs` argument lists passed to calls without claiming those
commands ran. The same file contains a Python regular expression that matches
an `xxd` pipeline, including a reverse-mode invocation; an existing text
finding and its dependent wireless composite previously described that text
as actual hex encoding. Their descriptions now report only the observed text.
Both scanners report the corrected description and disk observations in the
member and archive; focused tests and full uncached validation pass.

The build and rollout configuration builds and publishes image tools. One
Cloud Build step supplies `--add-acl-grant=AllUsers:R` when updating release
objects, requesting public read access. A neutral structured observation now
reports that argument in a build step without asserting that the build ran or
the ACL was applied. Both scanners report it on the member and archive;
focused tests distinguish a grant from a removal, an unrelated principal,
comments, and text outside step arguments. Full uncached validation passes.

# Incomplete shell fragment

`6e3a2ed562c0ea2e258556f2cff109b6f8a0f08f5a1d7cb6226f0c5ac9b9d728`
is a 36-byte fragment ending during a `/proc/*` loop declaration. `sh -n`
reports an unexpected end of file and the fragment contains no loop body or
other executable action. Both scans report no notable, suspicious, or hostile
traits. Hopper confirmed the existing **good** label for these bytes; this
does not characterize any missing original script.

# File decoding helper

`120f3780d2cf1b3e279bb60c51b7bec28805d3b1042b2375e02a83a4785d632f`
decodes supplied files through Base64, an external `./xor` executable, and
Base64 again, then edits the resulting output. Neither the input files nor the
external program is present. The helper itself contains no attack payload or
execution of its decoded output, and Hopper confirmed its existing **good**
label. A neutral trait now identifies the decoding pipeline as text without
claiming what its inputs or output contain.

# Post-exploitation framework package recipe

`9035b690a6ce42930e2799a31d087c1ee40fb6931d9ec9790e1275a4f78a7d3f`
is a package recipe that fetches a Git repository, invokes its local build
command, and packages the resulting binaries and modules. The recipe declares
the target to be a post-exploitation framework, but the checkout and payload
are absent and the Git source is unpinned. Atomscan fetched an HTML repository
page, not the Git source used by the build. The recipe itself does not reveal
the behavior of the executable it would build, so its endpoint label is
**inconclusive**. Neutral traits identify the named source and build recipe
without asserting unseen payload behavior.

# Device-manager test script

`1df4e9c2d0c2a7adddc21cf35b2a4e02fef50fdac6f7bc861d8ae24eca91e13b`
sets up a temporary device tree and tests a supplied BusyBox `mdev` executable
with commands run in a chroot. It contains no exploit or malicious payload;
Hopper confirmed its existing **good** label. A neutral trait records chroot
command text without claiming that quoted test commands have already run.

# DHCP client hook

`9818a7d68a60989836a81b320154167074496ac615ef096b9e09a688b7f29527`
applies DHCP-provided interface and route settings and rebuilds resolver
configuration from provided DNS values. Its behavior is consistent with a
DHCP hook, with no embedded hostile destination or payload. Hopper confirmed
its existing **good** label. Neutral traits now identify its resolver-path
assignment and nameserver directive without asserting a malicious DNS change.

# BusyBox test runner

`056f80ef941507321c2d29c0b69651953a89c3714f5d3b9dd08db9f5baf3333d`
selects local tests, prepares temporary applet links, invokes test scripts, and
reports their results. The runner has no embedded hostile payload; Hopper
confirmed its existing **good** label. A neutral structural rule now reports
the interpreter's variable script path when two ordinary flags precede it.

# Package removal hook

`8d30c9ff09f3a5d51562d8718e8a741192da4b639d63c286b9ff38b321daa229`
is a Debian post-removal hook that disables or removes its package-specific
sudoers entry. Its sudoers and package-lifecycle observations are already
represented in the scan. The hook contains no payload or privilege grant;
Hopper confirmed its existing **good** label.

# Webshell template in terminal test

`270cedd4793d208da1f994023d7d8b3d1985043196fae6d33011d110de00e234`
writes a PHP HTTP-header evaluation template into a phpsploit test input and
requests a generated backdoor for terminal-color verification. The template is
an embedded attack implementation despite its test context. The scan reports
the header-evaluation template and the backdoor-generation request; Hopper
confirmed the existing **bad** label.

# Small shell helpers

`1bc18589544534769b2774b544f92e94a8d821fb316f9821875f73475c015d2e`
reads one line and echoes it with the local hostname.
`a4d5291a75bfa2350de74a00a3aa5099f190fd6bc86c581bb38215720884fc15`
forwards arguments to a program in an adjacent `lld-bin` directory. Neither
helper embeds a hostile payload; Hopper confirmed both existing **good**
labels. A neutral trait records the latter's script-relative command text.

# Wrappers and proxy documentation

`6dbbbcf1513aa4adede8edd73bf10cdf666bd2c0ee7fb5b92a9ecc688a278016`
selects a Node executable and forwards arguments to a JSON5 CLI path;
`e1900769bfd512b079fd1bdf79c65e0c34e43505db08aaa4d427836386acdd3f`
updates a marked contributors section using a separately supplied helper.
`8f88c39bbd3e5633dc744acff69a7433600b0d8d861c29dbb967265c7ecc8536`
is Markdown describing a simulated phishing proxy; it does not contain the
proxy implementation. The scans found no suspicious or hostile traits, and
Hopper confirmed all three existing **good** labels.

# File-transfer traversal tests

`c2bafe6439bfb9197b65e01f6ded5725e89e24d52e0fc4e272bc66a8d1a016f1`
contains executable tests that authenticate to a service and attempt to
download `/etc/shadow` and upload a file under `/etc` using traversal paths.
The tests expect rejection, but they construct and send the attack attempts;
the archive is **bad** under the endpoint policy and was moved accordingly.
Two structural rules identify the distinct download and upload attempts without
claiming they succeeded. The current local archive scan reports both as hostile;
the installed Atomscan reports them as suspicious on the extracted test file.
The bootstrap scripts also pipe a remote installer to a shell.

# Infrastructure archive

`6bcfdfa9a9ac` contains infrastructure code, encrypted secret files, and an
administrative script that queries a remote database over root SSH and asks a
Matrix service to purge media using a supplied access token. The local scan
found no suspicious or hostile traits. A curl method override alone no longer
counts as a request-body upload; file, stdin, and inline body options remain
covered. A neutral finding also identifies the access-token query variable,
and the SSH observation no longer claims that login succeeded. The independent
Atomscan's suspicious findings came from fetched dependencies, not archive
members, and its external fetch reached the time limit. Some members had
limited flow analysis. Hopper confirmed the existing **good** label for the
reviewed archive.

# Gentoo source archive

`4bdd70cf1821` contains approximately 92,400 members, including ebuilds,
patches, and maintenance scripts. A targeted content search found account-file
references in package-management and authentication contexts, but that search
does not establish a verdict for the archive. The local scan found a .tk
homepage combined with an unrelated download reference in two recipes. The
shell rule now binds the URL to a downloader argument, and the individual
recipe no longer receives the unsupported finding. Atomscan's remaining
suspicious finding was in a fetched dependency. The all-files scan hit its
65,536-member limit, so a second scan covered the remaining 26,864 members.
Together they cover all 92,400 members by path and report no suspicious or
hostile traits; 94 records report limited analysis. The archive was
classified **good**.

# Bundled AI application wheel

`72a649778658` contains a Python wheel with a JavaScript backend and native
model-runtime binaries. The local scan reported console suppression in a
formatter that saves and restores the console methods around a spinner. It
also reported two provider-redirection findings in a test that creates a fresh
temporary home, writes a placeholder provider configuration there, and mocks
process launches. A narrowly bound context recognizes the single temporary
fixture; an additional live-config write, shadowed module names, or mocked
filesystem modules prevent that exception. The
independent Atomscan also reported a command-route finding in a strategy
module; the nearby authenticated `/validate-python` route sends submitted code
to a child Python process that calls `compile` to check syntax. Separate
`/execute` routes occur elsewhere in the module. An authenticated sandbox
route passes submitted strategy code to a helper that uses Node's VM context;
a new neutral rule exposes that call path. The current local rules do not
combine the separate route and subprocess observations. Some other findings
came from fetched dependencies. The local wheel scan retained one suspicious
console-suppression finding. Hopper confirmed the existing **good** label.

# Manufacturing hub source archive

`935b2a2367c9442fa112935e66fe7e8090e315e0508221d35fc8ed5f71b8a522`
contains Helm charts and an initialization script. The chart sets
`RBAC_ENABLED` to false, and the script chooses an allow-all named broker
extension when that variable is not true. New neutral archive observations
make both facts visible without claiming to have inspected the extension's
implementation. Both scans found no suspicious or hostile traits; some members
had limited flow analysis. Hopper confirmed the existing **good** label.

# OpenWrt package archive

`bcc7f4a8dc8c` includes package recipes, patches, and a high-availability
helper that registers `/etc/shadow` for synchronization. A separate helper
uses configured sync source and target paths during a sync event. A new neutral
trait identifies the registration without claiming a transfer occurred. Both
archive scans found no suspicious or hostile traits; some members had limited
flow analysis. Hopper confirmed its existing **good** label.

# Transaction interface definitions

`ae28f70403b8feddd54b0cc583d2f77443953a7733dd6ee3cb278066eeba5c3c`
is a Windows transaction-coordination interface definition file. It declares
interfaces, method signatures, and header directives without implementing an
attack. Both scanners identify C/IDL observations with no suspicious or
hostile findings; Hopper confirmed its existing **good** label.

# Coding-agent tooling archive

`9fc6f19a1653` contains coding-agent tools, configuration, documentation, and
tests. The local scan reports no suspicious or hostile findings. Its update
reminder prints a remote installer command; the reviewed reminder code does not
execute that command. Some tests write installer-command strings into temporary
fixtures for a scanner to inspect. The independent Atomscan flagged HTTP
desynchronization test code in a fetched Twisted dependency, not in this
archive. The reviewed archive was classified **good**; some members had
limited flow analysis.

# Cluster-management source archive

`a85bd32dc99c2ac906c58869f19a99af2c119a79f291d7e487512608eeaf4b38`
contains cluster-management code and CI workflows. Several workflows run an
artifact-downloaded test binary from `/tmp` with sudo, which is a genuine
suspicious observation. The all-files local scan represented all 5,365 archive
members and found no other distinct suspicious or hostile trait; 1,608 scan
records reported analysis gaps. The independent Atomscan also flagged three
related findings in a fetched Next.js dependency, outside the archive itself.
Hopper moved the reviewed archive to **good**.

# VM testing helpers and setuid shell installer

`be0b06058fa96975bf3be74117a90666ce58c260983009efb384ce7d68381d0c`
is a general VM test runner that downloads images, configures a guest using
`guestfish`, runs QEMU, and reports test results. Its source path occurs within
a security project, but the runner itself does not implement that project's
payload. Both scanners report no suspicious or hostile traits; Hopper
confirmed its existing **good** label. Descriptions of text-based `chmod` and
`cat` observations now avoid claiming that guestfish arguments are host shell
commands.

`0c6974bfa2d5f83cad6509b720eb27ae6f77702394e573c139849898adeca30b`
contains assertion and reporting helpers for tests in a VM. Both scanners
report no suspicious or hostile findings, and Hopper confirmed **good**.

`803572a2f00c3b11e19dd557b768fada8603db9b569b68d670a812836508db2d`
creates hidden C source for a root shell, compiles it, sets root ownership and
the setuid bit, and suppresses shell history. A structural rule now binds the
compiler output, root ownership change, and setuid permission change to the
same literal path; its combination with nearby root-shell source produces a
second hostile observation even without history suppression. A further
finding reports removal of the compiled source: its structural match binds
the removed path to the compiler input and the privileged output to the
ownership and permission changes. This is co-occurrence with embedded root
shell source, not proof that the shell text flows to the compiled file. Both
scanners report the three hostile observations. Focused tests cover unrelated
source and output paths, ordinary builds, and alternate compilers; full
uncached validation passes. Hopper confirmed **bad**.
