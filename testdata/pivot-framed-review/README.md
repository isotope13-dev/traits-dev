PivotC2 reconstruction review
============================

The reviewed SHA-256 is
`fbdbfacfe62090d90386f5f489e1bd70bad9aaf3a33ee86b79cf0c314ba0e938`.
The source calls itself PivotC2 client v0.2.3, rebuilt from reporting. This
identifies a reconstruction, not an authenticated original campaign artifact.
The reporting attribution, CVE, version and claimed campaign date were not
used to establish its behavior or verdict. No registry archive, manifest,
authorized deployment context or independently verified provenance was supplied.

Verdict: MALICIOUS. Merely loading the file opens an outbound TLS session to a
fixed public address. Received command frames run arbitrary shell commands;
channel-open frames create shell processes, arbitrary TCP connections or file
streams. Channel-data frames reach the selected child's stdin or stream writer,
and child stdout/stderr return through the length-prefixed channel protocol.
The harvest task reads FortiOS configuration archives and the device secret
file, Base64-encodes each file into a map, then encodes and returns that map.
This functioning implant and targeted secret export outweigh the reconstruction
comment. An explicitly authorized research deployment could change the operational
interpretation; none is established by this standalone file.

Control and data paths
----------------------

* The frame is a big-endian 32-bit length, an 8-bit type, and a payload. Channel
  data includes a big-endian channel ID. `makeParser` buffers partial frames and
  dispatches JSON commands, channel creation, channel data and channel closure.
* `exec` feeds controller-supplied command text to `child_process.exec` and
  returns encoded stdout. `ps`, `netstat`, interface and system queries return
  reconnaissance results. `hello` sends host, user, platform and interface data.
* Shell-channel output is relayed through `sendChannelData` and `sendFrame` to
  the TLS socket. Input uses the same channel map and writes to child stdin.
* Direct channels provide TCP pivoting, and listen tasks relay accepted client
  traffic through channels. The code contains no SOCKS negotiation; the SOCKS5
  finding accurately describes a comment reference, not an implemented parser.
* File upload opens the controller's chosen path as a write stream; download
  reads its chosen path and sends the contents. `cat`, `rm`, `ls` and `stat`
  expose additional filesystem operations.
* Port scanning expands supplied ports and probes up to 256 sequential addresses
  using `net.connect`. This is reconnaissance, not exploitation or propagation.
* Heartbeats and jittered reconnects keep the session alive. There is no boot or
  login registration. `tls_pin_sha256` is never consulted, while
  `rejectUnauthorized: false` disables ordinary peer verification. `stop_listen`
  only acknowledges; it does not close a server. `kill` attempts to unlink a
  fixed hidden temporary path and exits; the bytes do not prove that the path
  is the currently executing file, so no self-deletion claim was added.
* The source is readable JavaScript without an encoded executable stage.
  Base64 carries results, not hidden code. No archive members were present.

`mock_runtime.py` evaluates the source in QuickJS with entirely mocked Node
modules, sockets, processes, files, timers and host information. It supplies
fragmented frames and records the effects in `runtime-evidence.json` without
opening a network connection, starting a process, reading device files or
removing any real path. Command execution, shell input/output, file transfer,
TCP forwarding, configuration export, port scanning and reconnect scheduling
were exercised. This is a controlled path test, not evidence of real-world
network reachability or successful secret recovery.

Rule changes and preservation
-----------------------------

* Added distinct hostile observations for framed shell-stream relaying and
  return of the appliance secret-file map. The original three hostile findings
  remain supported and still fire. Their precision diagnostics, including the
  corrected process-export rule, exceed the documented 3.5 authoring bar.
* The process-export rule previously needed only a process-list command, public
  IP, socket connection and socket write anywhere in the file. The independent
  diagnostics fixture demonstrates that unsupported theft inference. It now
  requires an established framed pivot agent and a ps callback whose actual
  stdout is encoded into its result. An unrelated output variable fails it.
* Removed the unsupported DNS-exfiltration co-occurrence observation: Base64
  output and a DNS resolver are unrelated in this sample. A neutral DNS trait
  now follows the resolver argument to a Base64 Buffer conversion. The actual
  JSON/OAST DNS-export consumer retains its hostile detection on the positive
  control; unrelated resolver answers and encoding do not qualify. DNS calls
  and Base64 encoding retain their existing notable observations. The unchanged
  `node-dns-lookup` umbrella may be omitted by finding compaction after its old
  consumer is removed; the concrete resolve4 findings remain present.
* Moved the bare shell comparison out of backdoor vocabulary into neutral
  branching. Consolidated variable-type and object-type switch observations
  into one neutral dispatch trait, preserving their union and updating both
  consumers. Complete branch vocabulary remains visible at notable severity;
  generic type dispatch is baseline, rather than an attacker objective.
* Extended and renamed the existing child-output callback observation to cover
  passing the actual output bytes through a channel helper. Its original direct
  write query is retained unchanged in meaning, and its original reverse-shell
  consumer is updated. This keeps the 100-rule stream leaf within budget.
* Moved the PortScan literal keyword into source-literal metadata. A quoted
  word establishes no reconnaissance operation. Its existing `port-ref`
  consumer references the moved trait, retaining scanning-vocabulary coverage.
* Added an imported-receiver exec matcher to identify the previously missed
  `cp.exec` shell-command calls, without matching arbitrary objects' exec APIs.

Exact references and ancestor selectors were inspected; see
`consumer-audit.json`. Generic command vocabulary consumed by the Go-only
implant rule cannot gain or lose a JavaScript match from the relocated
JavaScript comparison. Exfiltration consumers still see the retained hostile
process-export result and the additional supported appliance export. No rule
severity was reduced to conceal a match, no identity/filename exclusion was
introduced, and no accurate attack finding was removed from the reviewed file.

Validation evidence
-------------------

`check.py` verifies nine static controls against the full ruleset. Baseline
reports were obtained from a snapshot of the pre-edit tracked rule tiers.
The controls preserve all baseline hostile findings on their positive cases,
retain both direct stream forwarding and genuine encoded DNS export, reject
independent diagnostics, and test wrong-map, wrong-stdout and missing-input
boundaries. Results are in `results.json`. Existing, unrelated fixtures
`testdata/hostile/extension-socket-shell-relay.js` and
`testdata/hostile/js-host-dns-beacon-controls.js` also retained their hostile
shell-relay and DNS-host-identity findings.

Re-run static controls with `python3 testdata/pivot-framed-review/check.py`.
Run the controlled execution with
`python3 testdata/pivot-framed-review/mock_runtime.py` (requires Python quickjs).
The original sample was scanned again with atomscan after the rule edits.
`review.json` records its before/after traits, classifier scores and remaining
analysis gaps. Hostile: 3 -> 5; suspicious: 6 -> 6. No hostile finding was lost.
The classifier remains SUSPECT[66%] despite the malicious behavior; its score is
approximately 0.997918. Atomscan warns that model v18.18 lacks newer engine
feature inputs. That classifier gap is reported rather than hidden by duplicate
rules or inflated severity. Final repository validation is run with
`make validate` after all edits and the judgment marker are written.
