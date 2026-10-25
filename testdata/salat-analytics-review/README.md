# Salat and concealed analytics loader review

All three supplied artifacts are MALICIOUS based on their bytes. Model labels,
family signatures, source filenames and corpus reputation were not used as
proof of behavior. Exact before/after unit counts and rule changes are in
`results.json`. Raw scans, facts, unpacked PE, decoded JavaScript and policy
script remain in the task scratch directory `salat-stage-review`.

## Salat: 3fc6de71f563acff…

The supplied unsigned PE32 GUI executable is UPX-packed. UPX successfully
unpacked it to a 12,570,782-byte Go 1.24.0 executable whose build information
names module `salat`. Neither its packed nor unpacked PE has an Authenticode
certificate directory. This is an actual stealer/RAT implementation, not a
legitimate utility identified only by its collection label.

A custom Go pclntab reader recovered 10,636 function boundaries/names. Rizin
and complete Capstone disassembly of the main package were used to inspect
instructions and call/argument paths; strings alone did not decide the verdict.
The relevant unpacked virtual addresses are:

- `getChromeLogins` at 0x8f2dc0 queries the browser login database, scans rows,
  calls `DecryptChrome`, and formats recovered credentials. `Steal` at
  0x8e5b30 invokes browser, Discord and Steam collection, adds results to a ZIP,
  closes the archive, Base64-encodes it, JSON-marshals it and passes it to `rq`.
- `runKeylogger` at 0x8d1e30 opens its recording file and installs the hook;
  `keyPressCallback` at 0x8d17e0 handles key messages, translates characters
  and writes them through bufio.Writer. `periodicFlush` flushes that buffer.
- `sendScreen` at 0x8d2410 captures the screen, Base64-encodes it, JSON-marshals
  the result and passes it to `rq`. `rq`/`tryRQ` construct and send HTTP requests.
- `tloop` at 0x8e2280 receives and parses tasks, then calls `doTask` at
  0x8e2890. The dispatcher downloads files, starts commands, collects data and
  reports status. Separate WebSocket handlers implement shell, screen, webcam,
  microphone and SOCKS operations.
- `getSystemToken` at 0x8f9300 enables privilege, locates LSASS, opens its token
  and calls DuplicateTokenEx. `impersonateSystem` consumes that token.
- `staticinstall` at 0x8da540 copies the executable, calls `newTask`, and has
  a Run-key creation/string-value-writing path. `newTask` at 0x8db580 builds
  task actions and timed triggers, then invokes TaskService.CreateTask,
  including a fallback registration attempt. This previously lacked a hostile
  scheduled-task finding; the added rule is explicitly a static code profile.
- `selfDelete` at 0x8fbad0 retrieves its own image path and uses rename and
  disposition information classes through SetFileInformationByHandle.

The 1,500-byte Base64 literal at VA 0xa0cc94 decodes to a PowerShell script
adding Defender exclusions for Program Files/AppData, disabling WinRE with
`reagentc /disable`, and setting EnableLUA to zero. `main.init` decodes it into
an initialized global. `main.main` consumes that value, appends exit text and
starts a goroutine that calls `shellCommand` with powershell.exe. Existing
three hostile policy/evasion findings are supported and retained; this is
not a claim that the commands succeeded on a particular host.

TON resolver code obtains and decodes blockchain contract address data for
endpoint resolution. Deployment, live C2 availability and runtime success are
unknown. The provided Bazaar/Triage pages could not be opened in this session;
no sandbox-only action was converted into a static claim. The observed theft,
surveillance, tasking and interference with security controls explain its
malware-corpus collection without needing that external corroboration.

## JavaScript variants: d55ecd69373f… and 8c3723476ae9…

Both contain an ordinary Animotion MCP analytics HTTP handler using Upstash
Redis followed by a whitespace-concealed, unrelated module-level loader.
Only the isolated pure string-array function, decoder and rotation loop were
interpreted to reconstruct the lookup table. No sample network or execution
code was run. Replacements and beautification produced inspectable copies.

The loader queries Ethereum RPCs, falls back to the Blockscout transaction
index, locates transactions from a configured sender, and decodes two IPv4
addresses from recipient bytes. It fetches HTTP stages, accepting response
bodies or the X-Payload-B64 header, Base64-decodes headers and applies a
repeating-key XOR transform. The resulting source is prefixed with global
configuration and supplied to execution sinks.

`stage-no-eval.js` replaces the inline eval callback with `ignoreSource` but
retains forwarding to spawn of `node -e`, detached, with ignored streams,
windowsHide and unref. `stage-no-spawn.js` substitutes `ignoreChild` for spawn
but retains indirect evaluation of the acquired source. The final remote
payload was not fetched and is not identified as a stealer.

Both supplied variants also duplicate top-level createRequire imports and
require declarations. Node rejects these files verbatim before executing them.
That limits runtime claims; it does not turn concealed attacker-selected source
execution code into benign analytics. Whether these were deployed, generated
as mutations, or repaired by another packaging step is unknown.

## Corrections and validation controls

The script-eval objective now requires the inline evaluator. A separate child
interpreter objective retains the child-source path, and rendezvous/hidden-child
consumers accept the corresponding objective. Thus the unsupported inline-eval
claim disappears on `no-eval` without erasing actual execution coverage.

The neutral whitespace measurement no longer excludes all test/harness files.
The `no-eval` suffix previously triggered a filename-based test grouping and
hid real whitespace, which also hid the hostile concealed-handler composite.
All consumers of the whitespace observation were inspected; intent still needs
their separate operation/context evidence. Grammar/bundle and format-specific
exclusions remain. There is no new package-specific exception.

The real analytics fixture outside this batch, all missing-sink/recipient,
changed-route/window/transform controls and benign helpers pass the extended
18-case `testdata/registry-conviction-review/check.py`. A plain aligned
`*.eval.js` control retains the neutral whitespace fact with zero H/S findings.
Three existing benign Ethereum controls have zero H/S findings; two existing
Ethereum attack controls retain four hostile findings each (one also has one
suspicious finding).

Real unpacked-PE controls remove the task-creation routine reference or the
TimeTrigger reference. Each loses only the new timed-task objective while
retaining the browser-theft objective. `check-task.py` reproduces those checks
with an unpacked original and scratch destination; it never executes PE code.

Salat changes from 13 H / 3 S to 14 H / 3 S in both the outer aggregate and
UPX member. No previous findings are lost. `no-eval` changes from 3 H / 2 S to
4 H / 2 S: the inline-eval claim is replaced, and concealed-handler coverage
is added. Its redundant generated-name grouping stops surfacing when the
alias-obfuscation rule can use whitespace instead; the underlying hex-name
observations and both suspicious obfuscation findings remain. `no-spawn`
retains all findings, 4 H / 2 S. There is no material attack-coverage loss.

Classifier outputs remain hostile, with probabilities 0.99, 0.98 and 0.98,
respectively (level 25). There is no verdict disagreement. Atomscan reports
feature-spec v18 versus engine support v21, and JavaScript flow recovery is
limited; findings remain static evidence, not proof of successful execution.
