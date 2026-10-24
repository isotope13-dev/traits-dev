Second review of 7b3aa2c3251b (GravityRAT GX), 09674b1689d8 (AppX OAuth
collector), and 2b144e342f2a (ltidisafe 1.7.1). All three are MALICIOUS on
code evidence. Scanner findings and the supplied VT results were not used as
proof of behavior. Samples were parsed and disassembled, never executed.

The executable's managed entry point is LSASS.Program.Main. Initialize creates
its local application-data hierarchy and a single-instance mutex. Services.Start
selects an active HTTP controller, starts the initial host report, and schedules
five-minute task polling. CommonSettings.Online -> Agent.PostRequest returns the
server response; Manager.UpdateServer splits it into tasks. Task's constructor
parses colon-delimited task name, identifier, and arguments. The dispatch closure
<UpdateServer>b__2 sends task arguments to CmdManager.Start -> DoViaCmd, which
launches hidden cmd.exe with `/c {0} > {1}`. The output file goes to
UploadManager -> Agent.UploadFile -> WebClient.UploadFileTaskAsync. This is
operator-controlled command execution and output return, not an inference from
an isolated Process.Start token.

The same dispatcher controls ScanManager and UsbManager. FileHelper.GetFiles
recurses and filters nonempty Office/PDF documents; ScanManager selects fixed
and network drives. UsbManager watches logical-disk creation, copies selected
files into staging, and uploads and deletes staged copies every ten minutes.
The initial NameValueCollection report contains identifiers, CPU/OS/domain/user
information, firewall state, VM results, and an explicit INFECTIONTYPE field;
Agent.SendBasicInformation POSTs that collection. VM probing includes Hyper-V
registry parameters, BIOS/system manufacturer, CPU/core/thermal queries, and
virtualization MAC prefixes. The result is reported; no VM-triggered exit was
invented. Firewall status is read, not disabled.

The PE is recoverable CIL with intelligible names. Its local state helpers use
AES/PBKDF2 and Base64. The Mono.Cecil resource is a dependency loaded through
AssemblyResolve. A separate encrypted ZIP lists icon resources. The dormant
RunAFile/WriteResources/KillJob helpers were traced: Filename/Bytes resources
contain only BOMs, and these helpers have no call from the entry/task paths.
The cleanup helper writes taskkill/task deletion/file deletion/self-deletion
batch text; existing notable command-template observations are retained. GDI
bitmap/resource APIs do not establish screenshot collection or keylogging.
The root's filesystem attributes include Hidden and System, but current facts
lack a resolved setter/flag relationship suitable for a general hiding rule;
a bare set_Attributes name would also match resource metadata setters. This
specific capability remains documented here rather than overstated in YAML.

The PowerShell script writes an AppX manifest and an HTML/JavaScript body, then
calls Add-AppxPackage -Register. The manifest selects a remote StartPage and
includes that origin with WindowsRuntimeAccess="all". The supplied page invokes
WebAuthenticationBroker using the Office desktop client ID and an OOB redirect,
then URI-encodes result.responseData into an HTTP POST form body. response_type
is code: the bytes demonstrate authorization-response forwarding, not successful
token redemption. This exceeds the stated remote-support purpose. The .example
addresses are reserved; the script does not launch the application, write its
logo, or establish that the remote page contains the locally written HTML.
Successful registration, remote content, user consent, and live collection are
unverified. These deployment limits do not turn the explicit credential-theft
construction into a benign support utility.

ltidisafe's three archive members were read in full. package.json runs
`node test.js > /dev/null 2>&1` during preinstall. test.js hex-encodes username,
hostname and home directory, prepends each to an OAST hostname, and passes each
URL to checkDownloadSpeed. index.js selects Node HTTP/HTTPS from that URL and
calls get(), so DNS/HTTP carries the identifiers even though the wrapper says
speed test. Network-interface addresses are computed but never passed to the
sender. index.js itself is an ordinary speed-test helper. No opt-in or
collection disclosure accompanies the automatic installation callback; no
credential-file theft, downloaded executable, or dependency-confusion scenario
was invented. All existing package/member findings are unchanged.

| Analysis unit | Hostile before -> after | Suspicious before -> after |
| --- | --- | --- |
| 1-7dfaef.pe | 2 -> 5 | 1 -> 3 |
| PE scanner's embedded unit at 0x5b638 | 0 -> 0 | 0 -> 0 |
| register_remote_appx_oauth.ps1 | 2 -> 2 | 1 -> 2 |
| ltidisafe archive | 2 -> 2 | 0 -> 0 |
| package/test.js | 1 -> 1 | 0 -> 0 |
| package/index.js | 0 -> 0 | 0 -> 0 |
| package/package.json | 0 -> 0 | 0 -> 0 |

The PE gains command-output upload, disk-document theft and infection/domain
report detections. New binary signatures bind evidence to the current image's
CLR #Strings/#US heaps; they do not require the family namespace, C2 domain,
collector filename, or campaign/status text. Their hostile composites have
precision 7.1, 7.0, and 8.5 in test-rules. Suspicious reference profiles remain
visible as well as the hostile outcomes. The AppX grant observation has scoped
YARA atoms and a public grouping to preserve all previously supported source
languages within the engine's YARA file-type cap; its two emitted suspicious
findings represent one authority grant, not two attacker outcomes.

The old OAuth rules convicted a broker response read plus any POST in the file.
The benign near miss with a separate response read and `body: "status=ok"`
fired both old hostile rules; the replacement requires the responseData form
expression. The result belongs in exfiltration/stealer/token. The AppX permission
rules moved out of file format; the grant matcher now binds HTTP origin,
Type="include", and full WinRT to one rule, rejecting excluded/split rules.
Entry-point declarations moved to package metadata. MachineName: remains a
notable schema-label detection; it is not reconnaissance by itself. Its direct
consumer was updated; eight broader discovery selectors were audited, and a
bare label is intentionally no longer discovery evidence. Seven existing
extension-name rules/groups moved from host permissions to package-name
vocabulary with their consumers preserved. The two complete name groups now
share their atoms' notable severity. No accurate sample finding was removed;
the lost IDs in the batch are these corrected placements/names.

PowerShell and npm each have one demonstrated theft chain and two contextual
hostile detections. Additional independent hostile behavior was investigated:
AppX registration/full WinRT remain permission/deployment observations, with no
launch or reactivation chain; npm's IP inventory is unused and the download
wrapper does not execute received bytes. These do not justify a third distinct
hostile trait. Their supported theft behavior is covered; there is no quota-
justified addition or unknown final payload asserted.

Live atomscan output initially called the PE benign (confidence=0.996); it now
calls it hostile (confidence=0.990, FP level L25). PowerShell remains classifier
benign (0.982 before, 0.994 after), and npm remains classifier benign (0.997).
Those two are remaining classifier misses despite the verified hostile rules.
The installed model warns that its feature specification is v18 rather than
v21. These confidence values are reported outputs, not verdict evidence.

Reproduction:

```
python3 testdata/triage/acquit-gravity-appx-identity-review/check.py SAMPLE_ROOT SCRATCH
python3 testdata/triage/hex-identity-benchmark/check.py
```

The first checks 21 original/mutated/benign controls, including the real embedded
Mono.Cecil library, a library carrying an implant overlay, role removal, renamed
implant identifiers, ordinary OAuth/POST near misses, excluded/split AppX rules,
and existing utility-extension consumers. The second retains all nine existing
npm positive/near-miss fixtures. Baseline shared-rule controls were scanned with
a pre-edit rule snapshot verified against HEAD for every changed shared file.
An unrelated external HTML sample was also inspected with that baseline; it
became unavailable before the comparison rerun and is not claimed as a passed
retained-coverage test. No external artifact was substituted for a requested
sample, and all three requested SHA-256 values were verified.

Full facts, resolved CIL disassembly, scans and comparisons are in the session's
scratch/acquit-review directory. The marker lines are:

```
GravityRAT GX: remote commands and disk theft; add behavior coverage
AppX OAuth collector: forwards broker codes; tighten traits
ltidisafe 1.7.1: preinstall leaks hex host identity to OAST
```
