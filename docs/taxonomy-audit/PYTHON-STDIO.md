# Python stream-relay migration

The [11-entry ledger](python-stdio-mapping.json) records eight original stdio
rule dispositions, two unsupported PTY aggregates, and one misplaced transport
profile. No parent rules or aliases remain after migration.

## What the matchers established

The former `stdio::python-socket-io-forwarders` matched `sock.recv(8192)` near
`sock.send`, without checking what data was sent. The generic reverse-shell
composite did not require process creation or a shell. A local `printf` process
with ordinary pipes and an independent socket echo reproduced a hostile verdict
at score 122. The three stdio composites now have one canonical home:
`stream-bridge::python-popen-socket-stream-relay`.

Its required evidence is an outbound socket operation, a Popen shell executable,
received data written to child stdin, and child stdout/stderr data sent through
send/sendall. Transfer atoms belong in `micro-behaviors/process/fd/stdio`;
explicit shell selection belongs in `process/create/shell/interpreter`. The
blockchain storage C2 consumer references the new canonical relay, preserving
its operational interpretation without retaining a second relay definition.

The four pipe-argument rule names were misleading: their matchers detected
`stdin=`, `stdout=`, and `stderr=`, not PIPE values or even a Popen call. They are
renamed to keyword-argument observations with their matchers, scopes, confidence,
and criticality preserved. The separate PIPE/STDOUT observations remain.

The connection gate exposed another gap: the existing Python method rule
recognized chosen variable names such as `sock`, but missed `peer`. A new neutral
AST observation correlates `socket.socket()` assignment with a connect/connect_ex
call on the same local identifier. The existing outbound-socket grouping includes
it while retaining its previous alternatives and Unix-socket exclusions. It
accepts variable endpoints rather than requiring a hardcoded address.

Validation also caught `pty::python-socket-shell` on the benign shell worker.
That component aggregate had no PTY or data-transfer requirement; demoting it
had left the taxonomy claim wrong. It and `python-reverse-shell-c2` are retired:
an external IP does not turn their socket/shell co-occurrence into a relay.
Underlying observations remain, and the new stream-bridge composite supplies a
supported relay verdict. Neither retired aggregate had external exact-ID
consumers; the latter's only relevant dependency was the former.

Adding the connection observation temporarily took `socket/connect` to 86.
Auditing that leaf found `nwparameters-tcp`: its symbol matcher observes a TCP
profile, without connection construction or start. It moves unchanged to
`socket/tcp`, in accordance with the documented operation-versus-transport
boundary. This is a semantic repair, not a new overflow directory.

## Controls and verification

Three deterministic ZIP fixtures exercise archive members outside plain-fixture
path exclusions:

- A benign archive includes a local printf process plus socket echo, a local
  shell plus socket echo, and distinct received/output buffers that are never
  passed to the corresponding stdin/send operations. All retain their useful
  socket and process observations; all forbid the reverse-shell hierarchy.
- A direct relay passes recv output directly to stdin.write and stdout.read
  directly to send.
- A threaded relay uses assigned buffers and decode/encode adapters, with a
  variable endpoint. Both positive controls require the stream-bridge hierarchy.

Local atomscan reports the benign archive at 7 and its members at 6–7, with no
reverse-shell finding. Both positive archives and members score 124 with the new
hostile relay. Full soft validation passes **1,644/1,644** fixture checks,
including all 24 existing reverse-shell corpus checks. Strict `make validate`
fails only on **176 oversized directories**. No mixed rule directories or stale
fully qualified migrated references remain, and all ledger destinations match
their recorded effective definitions.

Destination budgets: socket/connect 85, socket/tcp 82, fd/stdio 73,
shell/interpreter 10, reverse-shell/stream-bridge 32. The remaining stdio leaf
contains three C#/FIFO rules; PTY now contains 32.

A useful validator improvement came from the component finding: forbidden-prefix
failures now list the exact offending IDs in sorted order. Normal rendered JSON
omitted the component finding in this case; the validator's full analysis report
correctly retained and rejected it. This was not cross-fixture contamination.
The four existing trait-expectation unit tests pass on the rebuilt engine.

## Coverage limits and intentional changes

The transfer queries check direct arguments or locally assigned matching buffer
names, including encode/decode adapters. They do not implement runtime data flow,
track intervening reassignment, resolve arbitrary aliases, or join the child and
peer identities across separate callbacks. The Popen query recognizes an explicit
shell executable in the first string/list argument, not dynamically constructed
commands. These limits remain candidates for stronger relations and additional
specimens; passing this corpus does not prove universal relay coverage.

The replacement adds actual transfer and shell requirements, 4096-byte proximity,
and the union of prior testing/scanner/Ansible exclusions. These are intentional
eligibility changes, not a claim of matcher equivalence. Removing unsupported
verdicts preserves primitive observations but may lower unrepresented samples'
scores. The C#/FIFO and encoded sibling audits and all remaining cap migrations
remain open.
