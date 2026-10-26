# First reasoned review, 2026-10-26

The original artifacts were inspected statically; no submitted script or agent
was executed. Baselines and rescans used `atomscan --no-update --analyze local
--mode slow --format json <sample>`, with the environment's reference following
left enabled. `cleave facts <sample>` was collected for all three originals;
additional facts were collected for the native modules and recovered runner.
Full scan/facts artifacts are in the task scratch directory `scratch/fallout-review`.
`review.json` records the exact hashes, counts, model results, and member changes.

## Decisions and execution paths

* **KillerStrike 9ca64bce — BENIGN source distribution of an offensive framework.**
  The README, simulator, module tests, build files, and localhost default describe
  the implemented Windows C2. The public first-party project identifies itself
  as a Windows C2: <https://gitlab.com/fsec-vaul/killerstrike>. That confirms the
  project identity, not byte-for-byte upstream integrity of this archive.
  `main.c` registers the host, receives JSON tasks, calls the dispatch table,
  and returns module output. `shell.c` consumes task command text and runs
  `cmd.exe /C`; `exec.c` captures the hidden child's output. `browsers.c` reads
  Chromium stores, extracts login-secret columns, decrypts v10/v11/v20/legacy
  rows, and serializes plaintext passwords into task results. `abe.c` attempts
  APPB unwrapping, including CNG's Google Chromekey1 path. Its two DPAPI layers
  are attempted in the available security context; runtime success is not assumed.
  `clrhost.c` writes the embedded DLL, patches AMSI to return a clean result and
  ETW to return without emitting events, executes the managed runner, restores
  those bytes, and removes temporary runner files. The 12,288-byte PE was
  recovered from `psrunner_dll.h`; Rizin CIL disassembly and dnfile/dncil token
  resolution confirm `Host.Run` parses the argument header, Base64-decodes
  arguments, loads System.Management.Automation, reflects AddScript/AddArgument,
  invokes PowerShell, and writes results to the supplied pipe. This agrees with
  `PsRunner.cs`; it is not an unidentified encrypted stage. `persist.c` copies
  the agent, creates an AUTO_START service, starts it, and supports explicit
  uninstall with deferred deletion. The audio, webcam, and screenshot modules
  capture data and pass it to the multipart upload helper. `antisandbox.c`
  scores resource and user-activity probes and compares elapsed sleep time;
  `main.c` waits without beaconing if that gate rejects the environment.
  These are real offensive techniques, and all five hostile detections remain.
  Source packaging, explicit documentation, tests, operator-selected deployment,
  and lack of a concealed compromise tip the artifact verdict toward benign.
  There is no evidence here establishing authorization for any deployed agent;
  finding a configured or running agent requires separate deployment review.

* **token-replay.ps1 — MALICIOUS Microsoft 365 account takeover script.**
  Reads external JSON refresh-token records from TOKEN_FILE, iterates tenants,
  redeems as Microsoft Office, uses the returned access token to enumerate and
  DELETE Authenticator methods, then POSTs a replacement method. It redeems the
  refreshed token as Authentication Broker for DRS and attempts device enrollment.
  Bulk externally supplied token replay plus factor replacement and retained
  access is the deciding evidence. No operator prompt, recovery workflow, or
  documented authorized testing context is supplied. The POST/DELETE requests
  establish attempted behavior even if Graph rejects the endpoints, permissions,
  request bodies, or first-party client use. All five hostile and one suspicious
  findings are supported and already cover the distinct credential, MFA bypass,
  factor replacement, and device-registration behaviors; no trait edit is needed
  for this sample. Followed Microsoft sign-in/CDN references added no hostile or
  suspicious findings; the first-party remote pages are not the attack payload.

* **sync-check-self-hosted.yml — MALICIOUS Actions secret-harvesting workflow.**
  A push runs a hosted job that prints the environment and the complete
  `toJSON(secrets)` context through Base32, defeating ordinary literal masking.
  A second, self-hosted job writes credential-pattern files and a recursive
  search script, makes it executable, searches homes/workspace and secret/history
  files, reads other processes' environments, and prints the results to job logs.
  It starts a Docker container through the host socket with `/:/host` mounted,
  reads host AWS credentials, queries AWS/GCP/Azure credential endpoints, and
  reads Actions/GitLab runner files, gh authentication, kubeconfig, and the
  Kubernetes service-account token. Docker access and metadata requests can fail;
  the source still establishes attempted acquisition. The benign-looking build
  labels and absent build operation strengthen the deceptive-purpose judgment.
  Empty workflow permissions do not prevent access to self-hosted host resources.
  No authorized secret-audit context is supplied. The newly added hostile trait
  covers process-environment harvesting independently of the existing file,
  container, metadata, and encoded-log detections.

## Detection comparison

Counts are distinct hostile/suspicious IDs on each original's root report;
archive-root IDs already include inherited member findings.

| Artifact | Hostile before → after | Suspicious before → after | ML probability before → after | Calibrated alert before → after |
| --- | --- | --- | --- | --- |
| KillerStrike archive | 5 → 5 | 0 → 2 | .9762263 → .98 | no calibrated alert (-1) → HOSTILE L25 |
| token-replay.ps1 | 5 → 5 | 1 → 1 | .98 → .98 | HOSTILE L25 → HOSTILE L25 |
| sync-check workflow | 6 → 7 | 1 → 1 | .99963284 → .99962676 | HOSTILE L0 → HOSTILE L0 |

KillerStrike member changes: `abe.c` remains 1H/0S; `clrhost.c` remains 4H/0S;
`antisandbox.c` gains 1S; `browsers.c` gains 1S. Native service creation, audio
capture-start calls (including `record.c`), and Chromium secret-column literals
receive additional notable observations. The workflow's self-hosted embedded
shell moves 5H/0S → 6H/0S; the hosted secrets-log behavior remains covered on the
workflow root. The PowerShell original stays 5H/1S, and followed reference files
have no H/S findings. Three same-hash CDN files acquired JavaScript type analysis
on rescan, producing additional neutral observations; this is reference-analysis
variance, not a trait-driven behavior change in the PowerShell original.

No hostile or suspicious finding was removed or reduced. The single removed
notable ID, `objectives/impact/wipe/disk/raw::delayed-delete-until-reboot`, was
misplaced and overclaimed deletion: a non-null MoveFileEx destination can defer
a rename. Its exact regex, scope, severity, and confidence were retained as
`micro-behaviors/fs/file/move::movefile-reboot-delay-cooccurrence`, with an honest
co-occurrence description and no destruction mapping. The only consumer,
`windows-volume-file-zero-wiper`, now explicitly references that ID; searches
of exact and ancestor selectors found no additional affected selector consumers.
The control suite checks deferred rename/delete and the retained volume-zeroing
composite, as well as the existing Telegram-agent fixture's ordinary replacement
moves. The move does not weaken the shared technique's matcher. The physical
memory API description now covers total and available status instead of claiming
that every caller queries available memory.

The classifier's new HOSTILE KillerStrike alert disagrees with the source-
distribution verdict. This is a context distinction, not a reason to suppress
accurate AMSI/ETW or credential detections. The two malicious originals agree
with their classifier alerts and have no uncovered hostile-coverage quota gap.
Model v18.18 reports an older feature specification (18 vs expected 21), so the
recorded model probabilities should not be treated as complete behavior evidence.
Source-flow/embedded-source limitations were recorded by the engine; manual
execution-path and recovered-IL review supplied the relevant behavioral evidence.

## Controls and marker lines

Run `python3 testdata/fallout-reasoned-review/check.py`: 21 static positive and
near-miss controls passed. The runner stages copies outside test-directory
exclusions so those exclusions cannot decide behavior-only tests. Controls cover
bound procfs loop reads versus references, wrong variables, self-only reads and
missing redirections; actual versus mentioned audio calls; the service start-type
argument position; native browser secret inspection versus backup/comments; and
resource-plus-input probes versus display fallback logic. Existing token-replay
positive/benign fixtures and the Telegram-agent fixture are included.

Exactly these lines were written to the original sample verdict markers and
are intended verbatim for the commit body:

```
KillerStrike C2: documented test framework; retain evasion traits
M365 token replay: replaces MFA and attempts rogue device enrollment
Actions sync-check: encodes secrets and harvests runner/host creds
```
