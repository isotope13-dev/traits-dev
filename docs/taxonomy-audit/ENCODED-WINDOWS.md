# Windows encoded-launcher observations

This pass audits `reverse-shell/encoded/powershell.yaml` and `vbs.yaml`, including
their neutral destinations and existing Run observations. The
[11-entry ledger](encoded-windows-mapping.json) records all dispositions.

## Findings and placement

A VBScript launcher that runs an encoded `Write-Output "ready"` command received
a hostile reverse-shell finding at score **156**. Replacing the payload with a
TCP status request produced two hostile reverse-shell findings at **159**. The
rules required encoded-command text and Run arguments; the additional network
leg was only the decoded string `Net.Sockets.TCPClient`.

The useful observations now follow their actual subjects:

- The PowerShell AST invocation flag and VBScript command text move to
  `process/create/shell/command-flag`. Their bodies, scope and confidence remain.
- The decoded TCPClient type reference moves to `communications/socket/tcp`.
  Its description asserts a type reference, not a reverse-shell payload.
- The old VBScript Run matcher is retired in favor of the existing canonical
  hidden-window observations for asynchronous and waiting statement forms.
  Those two observations move from the WSH backend directory to
  `process/create/hidden`, preserving their definitions and updating consumers.
- The four hostile launch aggregates are retired. Their conditions do not
  establish a relay; even the stream-named variant accepted nearby output/eval
  syntax rather than a required received-command relationship.

The TCP leaf was already full. Its `CreateSocket` name observation explicitly
identifies a creation operation, so it moves unchanged to socket/create. This
follows the operation-versus-transport contract and keeps the TCP leaf at 85;
no overflow category or exemption is introduced. Its local `connect-comp`
consumer now references the canonical creation ID.

The Run consolidation is semantic reuse, not claimed byte-for-byte equivalence:
the canonical patterns are case-insensitive and distinguish waiting versus
asynchronous forms. Their existing argument boundaries and length limits remain.
There are no surviving consumers of the retired reverse-shell Run observation.
No new Run alias or duplicate predicate is retained.

## Controls and results

Three benign fixtures cover a plain encoded PowerShell TCP status request,
the VBScript wrapper for that request, and a VBScript local-status command.
All forbid reverse-shell findings while requiring process-creation observations.
Their local scores are **80**, **41**, and **39**, respectively. Existing generic
encoded-command and embedded-payload advisories still contribute to these scores;
the fixtures use caps of 100 rather than pretending those separate findings have
been audited away.

A positive fixture wraps the existing PowerShell received-command dispatcher
in UTF-16LE Base64. Its decoded child still matches
`remote-command/dispatch::powershell-tcpclient-command-dispatch`; the wrapper
scores **345**, its child **161**. This is per-command execution with returned
output, not a persistent child-shell stream bridge. Reusing that classification
avoids another encoded-only behavior category.

All **1,661/1,661** fixture checks pass, including all 24 reverse-shell corpus
checks. Strict `make validate` fails only on **176 oversized directories**.
The ledger's effective destination definitions verify. No stale migrated IDs or
mixed rule directories remain. Destination budgets are command-flag 8, hidden
50, socket/tcp 85, and socket/create 61. Seven rules remain in the encoded leaf.

## Remaining work and coverage limits

The engine exposed a decoded child for the tested PowerShell wrapper, but not
for the VBScript wrappers. This change does not claim universal carrier decoding
or equivalent coverage from the retired broad verdicts. A VBS payload needs
actual supported behavioral evidence; a TCPClient string cannot supply the
missing relation. Original observations remain available for more precise
consumers. Encoded Python imports, PHP labels, Perl decode/execute proximity,
and Elixir/Kotlin wrappers still require their own evidence and placement audit.
The other encoding and WSH backend leaves remain in the broader plan as well.

The hidden Run variants also illustrate a validator distinction: overlapping
predicates with different case, argument and boundary rules are review candidates,
not automatically identical matchers. Any future overlap warning should expose
those differences before suggesting consolidation.
