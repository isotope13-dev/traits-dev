# C# stream relations and retirement of stdio

The [nine-entry ledger](csharp-stdio-mapping.json) records four consolidated source
verdicts, one retired compiled verdict, a relocated command-handler identifier,
and three relocated TCP observations. The reverse-shell stdio directory is now
empty and removed; no parent aliases or replacement catch-all remain.

## Findings and classification

A benign source program opened a TCP stream, wrote a status message, and separately
ran a local cmd.exe command through redirected pipes. It triggered four source
reverse-shell verdicts at score **125**. Three already lived in stream-bridge;
correct placement alone had not corrected their unsupported relation claims.

They now share `stream-bridge::csharp-connected-cmd-stream-relay`. Its relational
AST evidence requires a two-argument TcpClient construction, a GetStream result
bound to that client, and the same stream identifier in both data directions.
A shell FileName assignment, output-event subscription and stdin write must name
the same child. Received bytes feed GetString and then that child's stdin; output
event data feeds GetBytes and then the network stream. The buffer names must
agree at each transfer. Direct event bodies and null-guarded event bodies are
supported; endpoint and local identifier spelling do not select the rule.

The full shell/network relation is an attack-context observation in the objective
leaf. Its hostile composite combines it with the canonical shell-selection and
TCP-construction observations. The unrelated local-shell control now scores **6**;
the existing corpus relay remains at **125**, and a renamed variable-endpoint
variant scores **126**. A separate local MemoryStream carrying process I/O cannot
borrow an independent TcpClient/GetStream setup: that control scores **6**.

The compiled verdict was not a counterpart of this relation. It combined CLR
names, cmd.exe and redirection setters with either reverse-shell terminology or
the exact string HandleCmd. A compiled benign network/local-process program with
an empty HandleCmd method reproduced the hostile verdict at **166**. No required
leg established a stream transfer. That aggregate is retired; the primitive
observations remain. It had no external exact-ID consumers.

`HandleCmd` itself was mislabeled as remote command execution. It moves unchanged
as a matcher to `data/control-flow/dispatch::dotnet-handlecmd-identifier`, described
as a command-handler identifier at notable. Its task-surface consumer now uses
the new ID. The protocol-specific ATT&CK tag is removed: this identifier alone
proves neither a transport nor remote execution. Related named-handler and
module-task aggregates still require their broader planned audit.

The TcpClient and NetworkStream CLR references also failed the operation test:
they identify a TCP facility without proving construction. They and their
conjunction move from socket/create to socket/tcp. The conjunction is renamed
`dotnet-tcpclient-stream-references` and no longer claims bidirectional traffic.
All explicit consumers are updated, with matching scopes, predicates, confidence
and criticality preserved. The resulting TCP leaf holds exactly **85** rules.

## Controls and validation

Four fixture expectations were added: independent source operations, the compiled
counterpart, local-memory stream transfers beside independent networking, and a
positive variable-endpoint relay. Benign fixtures forbid all reverse-shell paths
and retain socket/process observations. The compiled fixture now scores **13**,
with its named dispatch and TCP facts intact. Its source is included; it can be
rebuilt with `mcs -out:csharp-independent-pipes.exe csharp-independent-pipes.cs`.
The fixture is compiled and scanned, never executed during these checks.

All **1,657/1,657** fixture checks pass, including the 24 existing reverse-shell
corpus checks. Strict `make validate` fails only on **176 oversized directories**.
The separate exception/suppression findings seen during earlier live-worktree
runs no longer appear. All ledger destinations verify; no stale fully qualified
migrated IDs or mixed rule directories remain. Destination counts are
stream-bridge 37, control-flow/dispatch 39, socket/tcp 85 and socket/create 60.

## Intentional changes and limits

The source replacement requires the relation that the previous rules inferred
from co-occurrence. The compiled aggregate loses its unsupported verdict; this
is an intentional precision correction, not equivalent compiled-code coverage.
Raw CLR observations remain available for better-supported consumers. A future
compiled relay needs actual transfer evidence, not more chosen method names.

The new source query covers explicit local setup and event/loop transfers in one
block. It does not resolve aliases, class-field setup, intervening reassignment,
separate helper methods, zero-argument construction followed by Connect, or every
possible Read/Write/CopyTo adaptation. Exact lexical binding is stronger evidence
than co-occurrence, not runtime execution proof. Tests preserve represented
positive coverage; they cannot establish coverage of every unrepresented form.
Other stream-bridge variants, encoded siblings, and the remaining cap cohorts are
still part of the active plan.
