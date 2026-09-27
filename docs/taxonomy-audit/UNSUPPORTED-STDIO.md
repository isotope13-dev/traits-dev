# Unsupported stdio verdicts

This batch removes the remaining opaque JavaScript verdict and audits the five
Windows rules in `reverse-shell/stdio/windows.yaml`. The
[six-entry ledger](unsupported-stdio-mapping.json) preserves their effective
original definitions and the moved rule's destination definition.

## Dispositions

| Old local ID | Disposition and evidence |
|---|---|
| `node-obfuscated-computed-stream-reverse-shell` | Retire. All five legs match a local EventEmitter example plus `printf` spawning, with no network code. An `a0_0x`-named function is not proof of a decoder or a relay. Moving the verdict to an obfuscation directory would preserve an unsupported inference. |
| `windows-cmd-pipe-socket-shell` | Retire. Process/pipe/Winsock API coexistence does not wire a socket to child standard streams. Existing comments already acknowledged this limitation. |
| `sparse-iat-cmd-pipe-reverse-shell` | Retire. Imports, pipe APIs, cmd.exe and an endpoint are not a socket-to-process transfer. The sparse-import branch does not even require process creation. |
| `dual-hardcoded-ipv4-cmd-pipe` | Retire. The rule requires one endpoint observation, cmd.exe and CreatePipe; neither two addresses nor a relay are required. |
| `locale-window-station-c2-gating` | Retire. No conditional gate or command/control operation is required; it merely combines locale, window-station and endpoint observations. |
| `sparse-iat-self-delete-implant` | Move to `objectives/evasion/self-delete/file/script::sparse-import-self-delete`. Its required deletion-command/own-path context is about self-deletion, not C2. Remove the implant claim and use the self-deletion ATT&CK tag. Preserve scopes, predicates, exclusions, downgrade and confidence. |

All underlying observation definitions remain. No explicit live consumers of
the five retired verdicts or the moved rule were found in rules, fixtures, or
engine sources. Whole reverse-shell directory membership intentionally loses
these unsupported claims. No aliases or neutral duplicate aggregates replace
them. The remaining stdio leaf contains seven Python, C#, and shell rules.

The deletion-context destination held 84 rules before this move and now holds
**85**, exactly the inclusive cap. It remains a leaf. Its existing helper is
still contextual evidence rather than a proven data-flow trace to a deletion
target; this migration corrects the claimed objective without asserting a new
level of behavioral proof. The broader self-deletion cohort remains on the plan.

## Reproduced false positive and regression quality

A local-only JavaScript example requires the `events` module by a computed name,
constructs an EventEmitter through a named helper, makes three computed method
calls, and spawns local `printf`. It reproduced the hostile verdict at score 126.
After retirement the identical standalone file scores 7 without a reverse-shell
finding; its computed-load, dispatch and process observations remain.

A plain fixture under `testdata/` was an inadequate regression: an existing
fixture-directory exclusion suppressed the computed-module observation before
this composite could fire. The committed control is therefore a deterministic
ZIP with the same source in `worker.js`, where member analysis exercises that
observation normally. Its expectations require the dynamic-module and process
prefixes and forbid all reverse-shell prefixes, with a score cap of 15.

To verify the regression genuinely covers the old defect, an isolated copied
trait tree restored only the retired JavaScript composite from its ledger. That
snapshot scored both the ZIP and its member at **126**, with the old hostile
finding. The current tree scores the ZIP at **8** and its member at **7**, with
no reverse-shell finding. The temporary snapshot was removed afterward; the
current worktree was never restored to the flawed rule for the replay.

## Validation and limits

All **1,641/1,641** fixture checks pass, including all 24 reverse-shell cases.
Strict validation still fails only on **176 oversized directories**. The moved
rule's effective definition and destination budget are checked, and no stale
retired references remain. The corpus check guards current fixture coverage;
it is not proof that every unrepresented native specimen retains its former
inferred verdict. Retiring those verdicts is an intentional precision change,
with their underlying facts preserved for better-supported composites and ML.

The remaining Python/C# stream relations, FIFO shell coupling, and encoded
siblings still require review. Existing platform/implementation cleanup and the
176 oversized leaves remain part of the original goal.
