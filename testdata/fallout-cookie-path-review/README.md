All three supplied artifacts are **MALICIOUS** on the balance of their bytes.
No specimen or embedded command was executed. Atomscan, complete Cleave facts,
resolved CLR IL, source review, mutation checks and preservation scans are
recorded in [review.json](review.json). That report identifies the scratch
files containing raw scans, facts, IL and Forager provenance.

| Sample | Identification | Hostile before → after | Suspicious before → after | Local classifier before → after |
| --- | --- | ---: | ---: | --- |
| `0c360acdecc5/no-cookie-record.exe` | Custom .NET surveillance/ransom program | 37 → 39 | 12 → 12 | HOSTILE → HOSTILE |
| `1ee3a093669f/greatnesscoming-guarded-response.js` | ActiveX HTTP response loader | 4 → 4 | 0 → 0 | HOSTILE → HOSTILE |
| `83046698b20b/sync-check.yml` | Actions secrets-to-log workflow | 1 → 1 | 1 → 1 | BENIGN → BENIGN |

Counts include every analyzed unit. The workflow's extracted shell body has
0 hostile and 0 suspicious findings before and after; its Base32 and environment
pipeline capabilities remain notable. These inputs contain no archives or
fetched dependencies contributing findings. Nothing was removed or reduced in
severity to fit a verdict or count. No detection was lost after the explicit ID
mapping. Model probabilities are .99 → .99, .99908084 → .9974576, and
.97937423 → .97937423 respectively. Alert levels remain 25, 1, and -1. The
workflow is a classifier miss despite its correct hostile trait; changing its
rules to force a score would misrepresent the evidence. The installed v18.18
model reports an older feature specification than the engine expects.

The executable is an unsigned, unobfuscated CLR GUI assembly whose entrypoint
is MethodDef `0x0600001d`, `NanoCoreUltimate.Program.Main`. Its names and many
planted malware-family mutexes do not establish NanoCore or Hidden Tear lineage.
Tracing Main, delegates and async MoveNext bodies establishes these behaviors:

- Main creates hidden/system working directories, launches surveillance workers,
  installs persistence, blocks input and invokes security/recovery sabotage.
- HookCallback records timestamped keys and the tracked foreground title into a
  StringBuilder. A separate loop polls GetAsyncKeyState and appends keys. The
  shared flush path encodes records and calls SendToC2.
- ClipboardMonitor reads clipboard data, appends a local log and forwards an
  encoded record. It mixes CF_TEXT with PtrToStringUni, so decoding may be
  defective. Screenshot capture saves JPEGs and forwards their Base64 bytes.
  File workers enumerate personal extensions and logical drives, read files,
  stage data and forward file records.
- `StealCookies.MoveNext` at RVA `0x5a10` builds the local Chrome
  `User Data/Default/Cookies` path, reads its bytes, Base64 encodes/truncates
  them, prefixes `RECORD:` and calls SendToC2. Changing the former `COOKIE:`
  label did not remove the theft. ReadBrowserData separately copies Chrome
  stores and Edge cookies; AccessWindowsCredentialManager copies files from
  the local Microsoft/Credentials directory without decrypting passwords.
- SendToC2 at RVA `0x5ff8` appends local records and passes its argument to
  WebClient.UploadString at the hardcoded HTTP endpoint. IsPlaceholder always
  returns true and prevents the separate randomized beacon from constructing
  a URL; it does not guard this sender. Identity and heartbeat workers also
  call that sender.
- Persistence includes HKCU/HKLM Run and RunOnce, Startup copies/batch, logon
  and recurring tasks, and a PDF open association pointing at the executable.
  USB workers copy the executable and write autorun.inf on removable drives.
- The UAC path writes its own executable under ms-settings open-command with
  empty DelegateExecute, starts fodhelper and schedules registry cleanup.
  Other reachable routines stop security/update services, disable Defender and
  firewall controls, delete shadow copies and SafeBoot subkeys, disable System
  Restore, rewrite security domains to loopback, and block administrative tools.
- The encryption worker targets Desktop/TestFolder recursively, attempts AES,
  writes a suffixed replacement and deletes the original only after a successful
  write. UTF-8 static key and IV lengths are 17 and 15 bytes; AES setup fails.
  Existing encryption-attempt observations, ransom notes, wallpaper and input
  lockout remain supported. The ransom note's AES-256 claim is not a fact about
  working encryption.
- ProcessInjection writes a one-byte RET to Notepad and starts a remote thread;
  its neutral API observations remain. NetworkSpread targets only localhost
  administrative shares. Debugger/thread-hiding APIs are declarations without
  calls. None establishes a functional injected payload, cross-host SMB spread,
  or executed anti-analysis.

A demonstration or laboratory build is a possible explanation for the conspicuous
labels, TestFolder target and defective routines. No laboratory authorization
or deployment context was supplied. Real input/browser collection-to-upload
paths, unwanted persistence and protection/recovery interference outweigh those
benign explanations. Runtime success is not required for the verdict.

The 422-byte JavaScript creates MSXML2.ServerXMLHTTP.6.0, synchronously GETs a
public-IP cleartext URL, sends the request, reads status/headers/body, and evals
the nonempty body if status is 200. The variable names are cosmetic; there is no
encoded embedded stage. The status check is a success guard, not proof of
anti-analysis. An authorized legacy loader is conceivable, but no product,
update protocol, integrity verification or operator context explains this
opaque external script activation. Forager attempted the configured URL and
encountered an unreachable network route; the downstream payload is unknown.
Its four retained profiles cover one distinct activation behavior. No additional
persistence, theft or cleanup exists in these bytes to justify new hostile
traits. Three misplaced profiles now share the script-eval payload home, and
unsupported WSH, ActiveX-only, reusable-C2 and single-instance qualifiers were
corrected without narrowing their matchers.

The workflow triggers on push and has a job labeled build, but its entire body
prints `env | base32` and `echo -n '${{ toJSON(secrets) }}' | base32` to stdout.
That exposes reversibly encoded credentials to Actions logs while avoiding
verbatim-value masking. `permissions: {}` does not stop a run from referring to
repository secrets. Which secrets are provisioned and who can read the logs are
unknown; a run with no secrets would expose none. Bulk secret logging still
establishes the hostile export attempt. Encoded environment output remains
suspicious because its secret content is deployment-dependent. Diagnostics can
explain an environment dump, but no build/sync behavior needs complete encoded
secret values in logs. There is only one definite hostile source-to-log chain;
adding two more traits would duplicate or invent behavior. Existing rules
accurately cover it and remain unchanged.

The cookie rule now accepts either its old record-label evidence or token-
resolved Chromium profile arguments alongside the mandatory recorder, byte-read,
encoder and HTTP-upload clues. This preserves all old positives and fixes the
miss without using a campaign label as a required condition. New hostile hosts
coverage adds resolved loopback-line code to recorder, hosts append and security
endpoint evidence; its file-wide composition does not claim bound API operands
or observed delivery. Credential Manager blob copying moved from `store-api`
to `files`; the source-specific hostile evidence and T1555.004 mapping remain.

[controls.json](controls.json) records 21 before/after scans: four existing
loader positives, twelve JavaScript near misses, four CLR controls and an
independent original .NET positive recovered by SHA-256 through Forager/Hopper.
No retained finding or severity was lost, and no new hostile/suspicious finding
appeared on a benign control. [verify.py](verify.py) generated eleven original-
CIL controls, recorded in [mutations.json](mutations.json), that independently
rebind cookie operands/array locals, remove calls or APIs, rename the record,
remove recorder context and disable both loopback-line sites. The new source
observation survives a record rename and rejects an unrelated retained literal.
The placement-only matcher, type, platform, scope, proximity and severity
comparisons also pass. The final repository check is `make validate`.

Exactly one `.MALICIOUS` marker was written beside each original full sample
path. Their lines are copied verbatim into the prepared commit-body text in
scratch and recorded in review.json. Historical reports retain their original
IDs; the explicit mapping documents their relationship to the current rules.
