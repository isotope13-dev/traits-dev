Reasoned first review of 350bfb5f2963, 2315244816c4 and 73c4bf3abc84.

The original files received local slow Atomscan scans and `cleave facts` before
trait edits. Rizin and Capstone were used to inspect execution paths. No specimen
was launched by the operating system. Individual string-decoder and obfuscated
routines were also traced with Unicorn, with every external call intercepted.
Those traces recover static operands and data flow; mocked return values are
not evidence that any operation succeeded on Windows.

Raw scans, facts, disassembly, decoder source, intercepted traces, Forager
artifacts/provenance, control outputs and the complete comparison are retained in:
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-e78afdd4/scratch/review-350b-2315-73c4`.
`comparison.json` in the scratch directory records the sample deltas and retained native
coverage. The original bytes and SHA-256 values are unchanged.

* **350bfb5f2963 — BENIGN: AWS Amplify UI source archive.** Forager fetched
  `https://github.com/aws-amplify/amplify-ui/archive/refs/heads/main.tar.gz` with
  the exact supplied SHA-256, 350bfb5f2963025a112f5c38ba327da731fd38bb406e6a725ddb720bb5ade682.
  All 5,488 regular members match. The monorepo builds UI packages through
  Yarn/Turbo/Changesets. Its CodeArtifact action obtains an endpoint and token
  for the configured AWS repository. StorageBrowser's ZIP handler reads selected
  objects through presigned URLs, streams them to the download service worker,
  and initiates a browser save. The worker checks the sender origin, handles
  only its download pathname, consumes the corresponding stream once and
  expires abandoned entries. These paths fit the documented UI purpose.
  CI permissions, secret references, HTTP, encoding, iframe, message-passing
  and service-worker findings remain. The upstream match corroborates the
  inspected code; a clean scan alone does not establish the judgment.
  Actual credentials, deployed origins and user activity on a machine are unknown.

* **2315244816c4 — BENIGN: inert PE containing a V8 code cache.** The 6,064-byte
  PE has one mapped code section: offset 0x200 / RVA 0x1000 is RET and the rest
  is zero. Its import/export/TLS/CLR directories are empty. Native entry analysis
  establishes an immediate return and no callback or runtime path to the
  appended cache at 0x400. There is no Node runtime or supplied payload/UI
  sidecar in this file. Its Base64 content really decodes to hidden PowerShell
  adding Defender exclusions for TEMP/ProgramData subtrees and running
  `gpupdate /force`. The cache also contains an indexed XOR transform and
  write/spawn-related data. These embedded observations and the existing
  suspicious encoded-command finding remain accurate. They do not establish
  execution by this inert PE. External loaders or the origin of the cache are
  unknown; no deployment circumstances are assumed.

* **73c4bf3abc84 — MALICIOUS: concealed Windows native loader/backdoor.** Its
  entry at 0x1400a1be0 reaches a VM gate, a single-instance mutex, the AMSI patch,
  relocation, native/COM/Winsock initialization and task/network routines.
  The strings use `ROR8(cipher[i], i%7+1) XOR ((13*i+0xb1)&255)`; decoded
  strings are cached through TLS. API resolution uses these reconstructed
  names and GetProcAddress, rather than the API hashing previously inferred
  from opaque arithmetic.

  In routine 0x140069290, recovered computed calls load amsi.dll and resolve
  AmsiOpenSession. The resulting address is passed to VirtualProtect with
  length 3/PAGE_EXECUTE_READWRITE, then to WriteProcessMemory using the handle
  returned by GetCurrentProcess. The source buffer contains `48 31 c0`.
  This is targeted security-control code tampering, even without proving a
  successful AMSI bypass. The YAML checks the imported-pointer/handle binding,
  XOR-RAX buffer construction, protection API and concealed AMSI target.

  COM initialization at 0x1400b3a60 resolves CoGetObject into a global pointer.
  The helper at 0x14004b2e0 constructs the Elevation:Administrator moniker,
  configures local-server activation and invokes that pointer. The obfuscated
  caller supplies CMSTPLUA and ICMLuaUtil identifiers; the adjacent PEB identity
  code and explorer path support the retained bypass/masquerading judgment.
  Native remote-loading routine 0x14001e240 allocates/writes target-process
  memory and prepares a thread through the resolved NT APIs. It waits for and
  closes the thread, then frees staged regions. The concealed process-loader
  composite now additionally requires the independently established AMSI patch;
  ordinary process APIs and concealed strings alone do not earn hostility.

  At 0x140088410, GetModuleFileNameW supplies the image path to task-registration
  routines. The boot routine constructs trigger type 8; registration supplies
  flags 6 and service-account logon type 3 to ITaskFolder's 0x88 method.
  The repeated-task sibling obtains system time and configures repetition.
  System-task folder labels and misleading Windows utility version resources
  accompany this activity. The hostile boot detector requires the platform
  trigger kind and registration code, independently of the arbitrary trigger ID.

  A separate decoded Defender exclusion command reaches the hidden
  CreateProcessA helper through 0x140015cd0 -> 0x140015b70. The helper copies
  the command, sets hidden startup state/CREATE_NO_WINDOW, waits and closes
  handles. Network code resolves Winsock, uses HTTP task-request/WebSocket
  templates and the configured controller, and contains ready/ping/getinfo/task
  dispatch. New notable rules cover recovered HTTP GET, send and receive names.
  No final server-delivered payload, successful network exchange, victim or
  authorized deployment is known. Concrete AMSI tampering, concealed elevation
  and self-reactivation tip the judgment; version strings or the ML prior do not.

The rules preserve supported observations while correcting unsupported claims:

* The old multiplicative “API hash loop” pattern also matched forward branches
  in this specimen's opaque arithmetic. Its bytes remain as a metadata
  multiply/shift/XOR/branch observation. The preexisting precise register-mixing
  matcher is unchanged, including its hex backend.
  The old API profile now requires nearby export traversal and has a profile
  name. Both forms retain section containment; the added form remains x64-only.
  The complete 100-rule sequence-leaf inventory was reviewed: XGETBV is one
  opcode and moved to the existing opcode leaf, with identical effective
  definition and both consumers updated. This leaves one canonical home per
  observation, without raising a directory budget.
  Exact consumers, ancestor selectors and existing positive/negative controls
  were inspected. No technique bytes were erased to repair the inference.
* The concealed CMSTPLUA rule now requires reconstructed API-name evidence and
  describes that mechanism. Its hostile detection remains, under the corrected
  ID. A plain System Configuration Utility resource string moved into resource
  identity metadata, with the same matcher/scope/severity. Its exact consumers
  and the signed-resource selector retain that observation explicitly.
* The system-utility hostile composite no longer depends on the collector's
  filename disagreeing with OriginalFilename. A `sihost.exe` rename retains
  the same hostile finding. The neutral filename mismatch remains separate.
* `intercept-all` was misleading for a worker with a guarded download route.
  It is now `request-interception-and-client-claim`; its three required
  observations and notable severity are unchanged, and all three consumers
  follow the rename.
* Added two distinct hostile behaviors, AMSI tampering and concealed boot-task
  persistence, plus suspicious encrypted-name concealment and the missing
  compiler spelling of the CPUID hypervisor gate. Encoded command/API/network
  observations remain notable. No sample-name or controller exception was added.

Counts include archive/fetched members and decoded units:

| Sample | Judgment | Hostile before → after | Suspicious before → after | Local ML probability / alert level |
|---|---|---:|---:|---|
| Amplify UI archive | BENIGN | 0 → 0 | 0 → 0 | 1.0 / 0 → 1.0 / 0 |
| Inert V8 PE | BENIGN | 0 → 0 | 1 → 1 | 0.9036316 / -1 → unchanged |
| Native loader | MALICIOUS | 3 → 5 | 0 → 2 | 0.9911445 / -1 → 0.99 / 25 |

There are no material attack-detection losses. The native UAC ID change retains
its actual behavior; arithmetic and resource-text relocations retain those
observations. The archive emits 11,899 analysis records (11,836 distinct paths).
Apart from the service-worker rename, its changed findings are refreshed
`widely-installed` registry metadata, unrelated to the YAML changes. No hostile
or suspicious dependency finding needed a dependent-package exception. The inert
PE's complete finding set is unchanged. The native loader's previous local ML
miss is now alerted; Amplify UI's hostile ML verdict remains a false positive.
The model reports feature specification v18 while the engine expects v21.

Ten mutation controls pass: renamed executable; matching system basename;
changed decoder key; changed resolved target; renamed trigger ID; changed
trigger kind; broken function-pointer slot; ordinary patch bytes; changed COM
method; and ordinary CPUID leaf. The trigger-ID change retains persistence,
whereas changing the actual trigger kind removes it. Fifteen existing
native/path controls also pass. The old MIX expectation in that script used a
stale pre-migration ID and now names the canonical metadata observation.

A separate 50-unit native positive corpus, including the Forager-recovered
Remcos SHA-256 fe18bd15afc432a659dc2863301261d5c8873c43ca14fd559012b98bb9e66889,
retains every hostile/suspicious finding. The genuine dynamic-resolution stager,
COA/SDD, other native loader fixtures, and the Remcos COM bypass retain coverage.
The expanded post-change scan includes one additional benign hash-only control.

Run the focused checks with:

```sh
python3 testdata/native-rotate-xor-first-review/check.py --sample /path/to/decrypted.exe --scratch /path/to/scratch
python3 testdata/darkcleaner-chart-review/check.py /path/to/control-scratch
```

An initial full validation exposed a loss of the precise mixing observation
on the validator path after converting it to YARA. The unchanged baseline
validated successfully. Restoring the original hex matcher repairs that
regression; the Chrysalis fixture's score requirement was not weakened.

The final required repository check is `make validate`; its output is retained
as `validate.log` in the recorded scratch directory. Judgment marker contents,
also prepared verbatim in the scratch commit body:

```text
AWS Amplify UI: exact upstream source; scoped worker and CI tooling
Inert V8 PE: RET-only entry; embedded commands remain suspicious
Native Windows loader: AMSI patch, UAC bypass and boot persistence
```
