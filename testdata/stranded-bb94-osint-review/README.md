# Six individually reviewed members

All six listed members are MALICIOUS from their own bytes. The three archive
convictions were retained. No specimen, destructive command, or fetched payload
was executed. Original hashes were verified. Scans used `atomscan --no-update
--analyze local --follow=none --mode slow`; complete `cleave facts` were collected
for every member and original archive. Raw evidence is in the task's
`scratch/bb94-osint-review` directory. `review.json` records comparisons and the
six one-line marker notes verbatim. Markers are beside the extracted members.

| Member | Behavior and judgment evidence |
| --- | --- |
| Installer (`8202c3887b75`) | Universal Mach-O, containing matching encrypted AppleScript in both slices. ARM64 main at `0x100000690` builds a string and passes its C string to `system` at `0x1000006b8`. The decoder XORs each byte with the low state byte and updates state with `(state * 0x3785 mod 2^32) mod 35999`, starting at `0x11667`. Independently recovering 37,077 bytes from the ARM64 constant region agrees with the decoded facts. The executed `osascript` assembles and runs return-joined AppleScript. Its fake Installation dialog obtains a hidden password and checks it with `dscl . authonly`; a previous password is read from `.pwd`. It copies browser cookies/login stores, browser-extension and desktop wallets, Keychain databases, Notes databases/media and selected Desktop/Documents files into a random temporary directory. Notes scripting is a fallback when database collection fails. `ditto` produces `/tmp/out.zip`; curl posts that archive to the configured host, then the script deletes staging and the ZIP. It downloads Ledger Live replacement contents, kills/removes the original app using the captured password and extracts into Applications. Another handler downloads shell command text, embeds it in bash `-c` ProgramArguments, and copies/bootstrap-loads a system LaunchDaemon with RunAtLoad/KeepAlive; a nohup launch is the fallback. Broad secret theft, credential deception and persistence establish malicious intent independently of the outer package. |
| writer.js (`419285d369ff`) | All 1,342 bytes traced. Snapshots the entire process environment, platform, host/user identity and noninternal IPv4-interface MACs. A pairwise hexadecimal decoder reconstructs Axios, POST, HTTPS endpoint, headers and then-method names. Its export ignores arguments, sends the collected object and evaluates the response's `data`, swallowing promise errors. Concealed environment export plus remote code evaluation contradict a session/logging utility. The relative `../package.json` resolves to a missing `src/package.json`; the package entrypoint also points to an absent `.pnpm/httpreslog` writer. Successful activation is not assumed. |
| v.js (`2e5535f938bc`) | All 170 bytes traced. Export invokes real child_process.execSync with `del /F /S /Q C:\Windows\System32\*.dll`, shell:true and ignored streams, inside an empty catch. Forced recursive deletion of operating-system DLLs with no repair interface establishes the malicious purpose. This is deletion, not secure erasure. |
| f.js (`190bbe0e147e`) | All 315 bytes traced. Export opens `\\.\PhysicalDrive0` in r+ mode, allocates a 512-byte zero buffer, writes the same buffer through that handle at disk position zero and closes it. A separate try requests `bootrec /fixmbr`. That repair cannot restore the erased partition table. Swallowed errors and output suppression accompany deliberate first-sector destruction. |
| p.js (`d6f337222fab`) | All 330 bytes traced. Export enumerates C/D/E/F roots, joins entries to the originating root, checks regular files, and writes an empty string to each selected path in default truncating mode. Nested catches continue after failures. This destroys arbitrary drive-root file contents; it neither recursively traverses directories nor encrypts or securely erases files. |
| t.js (`28db8a38c16d`) | All 268 bytes traced. Export requests bcdedit bootstatuspolicy ignoreallfailures and recoveryenabled No, with shell:true, ignored stdio and an empty catch. First-command failure skips the second. Fixed paired recovery sabotage without a maintenance interface establishes the malicious purpose. |

The osinthell entrypoint imports the a-z actions and invokes them from `sorgu`,
ignoring its userId argument. Import alone does not invoke these four exports.
The earlier j.js action has a synchronous infinite allocation loop, so reaching
the later p/t/v calls in the complete package is not established. Each member's
implemented destructive effect still establishes its individual verdict. The
alphabetical directory nesting hides placement but introduces no decoder.
Windows rights, operating-system behavior, actual invocation and success are
unknown; none of these members implements elevation.

The macOS postinstall script disables Gatekeeper, removes quarantine flags and
opens Installer as the GUI user before opening an Archicad patch package. This
is packaging context from the original bytes, not a capability attributed to
the Installer executable. Runtime success, user consent, server response
contents and validity of the replacement app are unobserved. The exfiltration
retry call has one fewer argument than its handler signature; successful retry
is not assumed.

## Coverage and changes

Rename the two `node-silent-system32-dll-wipe[-action]` IDs to
`node-silent-system32-dll-delete[-action]`, and say “deletes” in the hostile
description. `del` does not prove the secure-erasure claim reserved for wipe
techniques. The existing `impact/degrade/system/file` placement is correct.
Matchers, scopes, confidence and severity are byte-for-byte unchanged after ID
and description normalization. Update their internal reference, the required
positive fixture and the two active control suites. Historical review snapshots
remain historical records. No detection was narrowed, demoted or deleted.

Required primitives and hostile effects are already covered for every member.
Specifically inspected the decoded script's collection, archive, upload,
cleanup, replacement, elevated service installation and fallback execution
paths, the writer's bound source/POST/eval operands, and every statement in the
four destructive exports. No supported missing distinct behavior was found.
The four small exports do not support three distinct hostile results apiece:
v deletes DLLs, f destroys a boot sector, p truncates files, and t sabotages
recovery. Existing overlapping accurate detections are preserved. Their process
execution, disk/write/truncate/delete and error/output-handling observations
also remain. Adding exfiltration, persistence, escalation, or invented separate
attacks to satisfy a count would be unsupported; there is no matcher limitation
preventing coverage of the actual four outcomes.

## Before and after

H/S are distinct hostile/suspicious trait IDs. Archive root totals include
inherited findings. Every archived member's H/S set is unchanged after the
two DLL ID renames, including members outside the requested six.

| Artifact | H before → after | S before → after | Classifier before → after |
| --- | ---: | ---: | --- |
| Installer member | 17 → 17 | 10 → 10 | malicious → malicious |
| writer.js | 6 → 6 | 6 → 6 | malicious → malicious |
| v.js | 1 → 1 | 3 → 3 | benign → benign |
| f.js | 1 → 1 | 1 → 1 | benign → benign |
| p.js | 2 → 2 | 1 → 1 | benign → benign |
| t.js | 1 → 1 | 3 → 3 | benign → benign |
| macOS archive | 17 → 17 | 11 → 11 | malicious → malicious |
| parser-session archive | 6 → 6 | 6 → 6 | malicious → malicious |
| osinthell archive | 5 → 5 | 10 → 10 | malicious → malicious |

The calibrated classifier's benign verdicts on the four individual destructive
modules are false negatives despite existing hostile findings. Tiny rendering
explicitly confirms the benign gate. Do not infer a malicious gate from its raw
probabilities around 0.97–0.99: these results have level -1. The scanner also
reports model feature schema v18 versus expected v21. No rule inflation was
used to change classification.

Initial Installer output had 188 notable traits, whereas subsequent output has
171, replacing its x86 decoder observation with ARM64 and omitting several
generic roll-ups and metadata findings. A fresh cache-disabled scan against an
isolated HEAD rules snapshot exactly reproduces the final 207-trait member
report, including all finding details, and the same probability 0.99910134.
Thus those lower-severity differences are reproducibility/freshness differences
outside this YAML rename. Both architecture decoders exist in the original
bytes; recovered script behavior is unchanged. The 17 hostile and 10 suspicious
findings survive every scan. All member and archive differences are recorded in
review.json; there is no material attack coverage loss attributable to this edit.

Existing source-only controls passed: 22 assertions across 11 DLL import,
executor, target and logging controls (including the out-of-batch hostile
fixture), and 20 assertions across 15 current source fixtures. No fixtures were
executed as JavaScript. `make validate` is the final repository check.
