# sitecard wheels and protected CLR implant — 2026-10-23 review

All three original artifacts are **MALICIOUS**. Judgments follow execution-path
analysis, independently of reputation, trait counts, and classifier output.
`scan-delta.json` records original hashes, model outputs, changes and counts for
every archive member; parent counts below count each trait once, not again for
each member. `marker-lines.txt` contains the exact ingest commit-body lines.

| Original | Identification | Hostile before → after | Suspicious before → after | Reported ML probability before → after |
|---|---|---:|---:|---:|
| e7c8c8ca5c688f1b1f9b152ab951f8e9e3c6363825b95ef2b1c80f9d5382242c | .NET Reactor protected native wrapper containing a managed remote-control/stealer implant | 1 → 0 | 0 → 1 | .994056 → .992892 |
| 3206fbc69095217a14cc5b041d761baf97b8f8db2f2bda5e4688041f232a4a9d | sitecard 0.1.14 Python wheel | 0 → 4 | 0 → 1 | .831753 → .981833 |
| e48b7645c9b34fc2352672cd9a4782bba1fa231393418f1865e9704ec0e8f592 | sitecard 0.1.9 Python wheel | 0 → 3 | 0 → 1 | .831753 → .978527 |

The model assigns `cls: 0`, `lvl: -1`, `conf: 0` before and after for every
original. A live tiny render explicitly says `scan benign` for all three after
the changes. The reported probabilities are not substituted for these verdicts.
The bundle is v18.18 and warns that its feature specification is v18, while the
engine expects v21. This is a remaining classifier miss; the accurate protector
correction is retained. The archive-specific model probabilities changed from
.022527 to .841938 (0.1.14) and .269695 (0.1.9), without changing that verdict.

## Evidence and provenance

Original `atomscan` reports and `cleave facts` (including decoded strings) were
saved under the task scratch directory `review/` as `pe`, `v14`, and `v9` with
`.before.json` and `.facts.json` suffixes. All later RE artifacts, logs and reports
are under `scratch/sitecard-e7-review/` in this task's environment. Scans used
`--no-update --mode slow --analyze local --follow=none`, with the local YAML.
Final original reports are `originals-final.jsonl`, controls are
`controls-complete.jsonl`, and recovered-stage reports are `recovered-after.jsonl`.
The earlier `originals-after.jsonl` differs only by one neutral host-query
composite which has since been corrected as described below.

Both original wheel fetches used `forager fetch --all-wheels -o <scratch>
pkg:pypi/sitecard@<exact-version>`. The recovered 0.1.14 and 0.1.9 wheels match
the submitted SHA-256 values exactly; these are original wheels, not archive
reconstructions. Artifacts and `.forage.json` provenance remain in
`scratch/review/fetch-0.1.14/` and `fetch-0.1.9/`. ILSpy and its .NET SDK were
also recovered into scratch; no sample application code was launched.
The public [GHSA advisory](https://github.com/advisories/GHSA-9wjg-8fcv-pxj2)
corroborates the unauthenticated-access reporting concern. Its label was not
used as proof of the behavior.

## sitecard execution paths

The advertised purpose is a disposable SSH workspace gateway. Imports and wheel
installation do not themselves start the backdoor; the CLI launch path does.
Both versions contain working legitimate gateway, transfer and transport code.
There is no need to infer a malicious dependency or an unseen installation hook.
The security-relevant behavior is present directly in the submitted source:

* `session._launch` defaults to the `srvus` transport. `_resolve_public_access`
  returns `__package__ == "sitecard"` when neither the user nor saved settings
  override it: authentication-free access is the distribution default.
* `gateway.TokenSSHServer.begin_auth` returns `False` for that accept policy.
  `create_acceptor` calls `asyncssh.create_server` and installs the process
  handler. `handle_process_logged` calls `handle_process`; the latter reads
  `process.command`, passes it to `build_child_argv`, and launches that argv with
  `asyncio.create_subprocess_exec`. The helper constructs `[shell, "-lc",
  command]`. Interactive requests get a login shell and PTY. The workspace cwd
  does not confine shell filesystem access.
* Default SFTP is `HostSFTPServer`, whose superclass receives `chroot=None`.
  A separately selected confined server exists. This is access with the running
  user's permissions, not privilege escalation.
* The launch default for TCP forwarding is `True`, and the SSH server's
  `connection_requested` returns that policy, exposing network pivot capability.
* `ingress` connects with AsyncSSH to the relay with `known_hosts=None` and calls
  `forward_remote_port` to expose the local gateway. It parses the public host,
  probes connectivity, and returns the target to the launch path.
* `_resolve_rendezvous_url` returns a hardcoded shared collector absent an
  override, and `_launch` passes the resolved value to `_publish_rendezvous`.
  This constructs an actual `urllib.request.Request`, with `method="POST"`,
  and opens that same request. In 0.1.9 the JSON payload includes host, URL,
  ready-to-use `ssh_command`, health and timestamp. The shared destination is
  `webhook.site/547a29d7-0c93-438d-82ee-f62e65e37d09`.
* In 0.1.14, the shared destination is
  `ntfy.sh/02f9fe8a5cd9627395798443a235896b`. `_rendezvous_payload` adds
  `" ".join(platform.uname())`, including hostname/kernel/architecture data.
  `_rendezvous_body` includes that data and the SSH command in the submitted
  plaintext body. This extra exfiltration finding is absent from 0.1.9.

Sending an authentication-free entry point to a fixed third-party collector
without an opt-in tips the verdict to malicious, in combination with working
shell, filesystem and network access. The transport and SSH APIs alone would
not. No machine-specific operator authorization or intended recipients were
provided. Some settings permit safer operation, but do not change the shipped
default path. Runtime connectivity and collector ownership were not established.
A default hold is time-limited; background supervision is possible. No reboot
persistence or privilege escalation is claimed.

Configuration, runtime/supervisor, bridge/tunnel, model relay, transfer,
client configuration, account and command modules were also reviewed. Key
encoding, cryptography, secure permissions, subprocesses and networking are
retained as notable capabilities. The optional model proxy and explicit
upgrader do not independently establish theft. Legacy insecure SSH option text
in client configuration is detected as option text, because the migration code
removes/rejects it; actual `known_hosts=None` connections get a separate operation
finding.

## Native and managed recovery

The native file is an unsigned PE32 MSVC wrapper with about 1.63 MB of
near-random resource data. Rizin disassembly identified main at `0x4019f0`,
stack-string XOR decoding at `0x401650`, table initialization at `0x401300`,
and the resource decoder at `0x401560`. Decoded names include
`Cor_Enable_Profiling`, `mscorjit.dll`, `clrjit.dll`, `mscoree.dll`,
`CLRCreateInstance`, and the resource name `__`. Snapshot enumeration and JIT
module checks are traced; the CRT's `IsDebuggerPresent` import is not promoted
into an unsupported hostile anti-debugging claim.

`recover.py` reproduces the first layer by emulating only the bounded pure table
initializer in Unicorn, then applying the forward/reverse neighboring-byte
substitution to 1024-byte resource blocks in Python. It invokes no sample OS,
network, process or CLR entry point. The result is a four-byte length followed
by a checksum-valid zlib stream: 2,576,910 decompressed bytes, a 14-byte CLR
version prefix, and a 2,576,896-byte managed PE. The bootstrap uses reflection
and entry-point invocation to load its embedded image in memory.

| Recovered artifact | SHA-256 |
|---|---|
| managed.exe | 8ad9db73b00f4f69a59b393aafe699cbcc527e941329c3e3c9c546771aae5aa0 |
| resource `_` / res-_ | 523262132de469f2728621eed8f6e9bf1ac374f88c0c882ccefbb3c291391926 |
| restored.exe | 5c2fb5b166a5b410934cf7c9798d9fbab74ad515f2ec7e36a63a645f71346e28 |
| resolved.exe | 43ed5542d5782bd302b1c3ccffcdc13c63481d276682365c84ebee806e8bcb9a |

The next layer conceals method bodies and calls. A bounded, data-only CIL
interpreter (`cil_data.py` in scratch; 30 million instruction limit, explicit
external-call allowlist) recovered the 65,892-byte method patch stream from
method 2254 (`LDFgNmI4H`, RVA `0xb1e38`). Interpretation stopped at an unsupported
`Assembly.GetModules` operation after extracting the data. Parsing the complete
patch stream restored 2,610 method prefixes/headers. Translating the arithmetic
in method 2245 (`b3nMWnkTO`, RVA `0xb1334`) decoded 1,650 field-to-method delegate
mappings; 10,898 proxy call sites were restored. ILSpy then exposed the actual
control flow. These are analyst transformations, not original executables or
observed runtime outcomes. `traced-methods.json` records method IDs and RVAs.

Main method 680 (`74V.PEs.627`, RVA `0x32790`) dispatches to method 833
(`ab2.2J2.nC6`, RVA `0x3fe70`), which starts/waits on task entries configured by
its type initializer. The restored code includes serialized command dispatch,
hidden process/script execution and download handlers. Clipboard and desktop
capture are connected to collection and outbound transmission:

1. `kJk.654` (562, RVA `0x2b060`) starts capture/collection tasks, including
   Clipboard.GetText/GetFileDropList and screenshot capture helpers.
2. `OYX.J3H` adds data through `C75.Xt4` to the archive. It is an archive sink,
   not itself a network send. The archive is saved to a MemoryStream and
   returned as bytes.
3. Command-driven and automated callers pass the resulting byte array to
   `461.HtQ.E2P` (712, RVA `0x3518c`). Screenshot helper `HtQ.wN8` (711,
   RVA `0x34bc0`) also uses this upload path.
4. `E2P` wraps the bytes as a multipart attachment, calls `E65.F4j` (815,
   RVA `0x3f21c`), and then `E65.48o` (816, RVA `0x3f2e8`) writes the encoded
   payload through `HttpWebRequest.GetRequestStream().Write` and calls
   GetResponse. This establishes the capture → archive → upload relationship.

Concealed remote-command handling, capture and upload tip the judgment to a
malicious implant rather than an ordinary protected application. The exact
family and live C2 are not established; remaining virtualized configuration
strings and deployment context are missing. No label from the submitted
multi-family filename is adopted as identity.

## Rule corrections, retained coverage, and limits

* The native wrapper rule's matcher establishes commercial resource concealment
  and CLR hosting, not a hostile application purpose. Its exact matcher and
  publisher exclusions are retained, with an accurate description and
  **suspicious** severity. Before changing it, exact and ancestor consumers
  were checked; no dependent YAML rule required its hostile criticality.
  Two independent protected PE positives were fetched through forager/Hopper:
  SHA-256 `58d3ffd6c841db948f6c779fa2434f09ce028ae0630dd10ea3db7d926700dedd`
  and `bb9830beab575fbe8335761f3d3a7148054c37ba75641c638ba803ad34c1bd7c`.
  Both matched before and retain the same finding after, at suspicious severity.
  Their binaries and provenance remain under scratch `positive-controls/`.
* The standalone split `/proc/` prefix moved from process memory to procfs path
  information, preserving its exact matcher, scope and notable severity. In the
  wheels it checks `/proc/<pid>/stat`, not memory. Exact/ancestor consumers and
  existing Miasma coverage records were inspected; the maps+mem+ranged-read
  memory composite now references the relocated prefix and retains its attack
  coverage. Proc-stat and actual ranged-memory-read controls separate the two.
* Two SSH legacy-option descriptions were corrected without matcher or severity
  changes. An actual AsyncSSH host-verification-disabled matcher was added.
* New notable rules describe SSH authentication policy, server launch, unconfined
  SFTP, forwarding, bound SSH command-to-shell execution, endpoint resolution,
  submitted access-report bodies, uname report data, and key generation/import/
  export. Objective rules require the fixed collector access-report flow and
  the gateway context, rather than campaign strings or filenames. Three
  distinct hostile wheel behaviors are shell access, filesystem access and
  TCP pivoting; 0.1.14 additionally leaks system identification.
* Adding a uname report-field fact initially let an existing directory-wide
  `needs: 2` host-query composite count one API twice. Its reference was expanded
  to the exact seven preexisting query traits, preserving the old reference set
  and preventing the new report fact from becoming another query. A single
  uname-report and two-distinct-query control verify this boundary.

There are no unaccounted lost trait IDs: the wheels lose only the old misplaced
proc-prefix ID, replaced by its canonical path ID. The native file loses no
matcher; its sole hostile finding becomes suspicious. Archive members retain
all prior accurate detections. Each wheel's `session.py` gains the suspicious
collector finding; hostile composites aggregate the cooperating archive members
at the wheel root. No extra hostile count is attributed to an isolated member.

**Remaining native coverage gap:** the original now has zero hostile traits,
below the requested 3–5 goal, despite its malicious recovered behavior. Neither
`cleave facts` nor atomscan automatically applies this custom resource decoder,
method restoration and proxy recovery. Scanning the original, decoded bootstrap,
restored assembly and resolved assembly was attempted. The recovered assemblies
receive accurate notable HTTP, crypto, process, clipboard and reflection API
findings, but do not provide a matcher-supported binding of command dispatch or
capture bytes to the upload sink. The bootstrap's one suspicious extension
mismatch is caused by the analyst saving a DLL image as `managed.exe`, not an
extra finding on the original. A ciphertext fingerprint, API co-occurrence, or
another packing rule would not accurately detect those missing hostile
behaviors. Automated unpacking and managed data-flow support are needed to
cover remote command execution, capture/collection upload, and downloaded code
execution on the submitted native bytes. The current YAML cannot supply that
missing engine analysis. No duplicate or inflated hostile rules were added.

## Regression controls and reproduction

The wheel fixtures are data-only copies/mutations, never installed or imported.
Their internal RECORD hashes are intentionally not regenerated: they test source
matching, not distribution installation. The changed collector fixture proves
that the new behavior rules do not depend on ntfy/webhook campaign tokens.
Configured/unused collector, harmless body, authentication required, no remote
command, confined SFTP and forwarding denied variants test each boundary.
The first two mutate only collector selection, not whether a user could
explicitly configure a destination at runtime.

`check.py` verifies saved JSONL reports for 16 positive/negative cases and two
retained protected-binary positives. It also checks that API-name text does not
match an actual remote-forward call, and that one uname call cannot become two
information-query APIs. Original-wheel per-member deltas are recorded separately
in `scan-delta.json`. To repeat, run atomscan against all fixture wheels,
`proc-*.py`, `ssh-forward*.py`, `host-*.py` and the two recovered positive PEs,
then pass the JSONL path to `python3 check.py`.

First-layer recovery can be repeated with:

```
uv run --with pefile --with unicorn python recover.py ORIGINAL_PE SCRATCH_OUTPUT
```

The recovered managed SHA-256 was independently reproduced. Further recovery
scripts and decompiled traces remain in task scratch for inspection. Validation
is run last, after all YAML, evidence and judgment markers are written.
