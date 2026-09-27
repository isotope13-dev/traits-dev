# Descriptor mechanism migration, 2026-09-27

The remaining `reverse-shell/dup` and `reverse-shell/syscall` directories are
removed: **27 rules relocated, two retired**. The
[mapping ledger](descriptor-mechanism-mapping.json) records all 29 original
effective definitions and the resulting definitions or retirement reasons.
This follows the [socket-shell pilot](SOCKET-SHELL-PILOT.md); its counts are
additional to that batch.

## Placement and evidence

`fileno()` extracts a descriptor; it does not prove that the handle is a socket.
These observations now use `micro-behaviors/process/fd/query`. Duplication and
standard-stream attachment use `fd/dup` and `fd/stdio`. Shell launch beside
descriptor duplication remains a neutral observation unless network coupling
is required. A fixed remote endpoint plus redirected descriptors need not
execute a command.

Shell descriptors connected to an outbound socket use `reverse-shell/fd-redirect`.
The syscall variant shares that mechanism; syscall spelling does not justify
another objective leaf. The P2P pipe-backed relay uses `stream-bridge`.
An accepted socket feeding a shell uses `backdoor/bind-shell`: a new explicit
bind/listen/accept composite preserves that branch after removing bind as an
alternative in the outbound-shell composite.

The Python socket-fileno shell now requires both stdin and stdout descriptor
arguments and shell evidence. The socket/dup2/shell composite now requires
standard-stream duplication. Two neutral fileno-argument atoms support these
requirements. These are deliberate precision repairs, not predicate-equivalent
renames. The matching remains syntactic; it is not a general dataflow proof.

An arbitrary Ruby `syscall` beside socket and shell operations no longer claims
descriptor redirection. The XOR18 bot conjunction is also retired: it combined
two retained hostile observations without adding a behavior and had no consumers.
Behinder's class-only consumer loses its `dup/` alternative: none of the old
members could directly match a class file. Exact consumers follow the relocated
observations; no live YAML reference to either retired directory remains.

A testing-directory exclusion suppressed the newly neutral C stdio observation
in the negative fixture. It was removed from both C descriptor composites:
the collector's path cannot negate an observed capability.

## Verification

- All 27 relocated effective definitions match their ledger entries. The five
  destination leaves contain 25, 35, 22, 68 and 3 rules, all at or below 85;
  all remain strictly leaf-only. The separate bind-shell destination has 21.
- **1,619/1,619 fixture checks pass in soft mode:** 248 hostile, 344 benign,
  175 does-nothing, 45 drop-exec, 572 supply-chain, 66 impact-wipe,
  82 obfuscation, 22 reverse-shell and 65 simple-stealer.
- Five added fixtures exercise the outbound descriptor shell, accepted-socket
  shell, independent socket/process calls, a remote stdio sink without command
  execution, and local shell redirection without networking. The Ruby negative
  control now includes an unrelated syscall.
- The existing C reverse-shell fixture retains three hostile relay findings
  and score 124. Its old suspicious-count assertion was tied to the neutral
  descriptor observation; the replacement explicitly requires `fd-redirect`
  while retaining the hostile minimum. Python outbound/bind fixtures score
  160/123 and report their respective canonical objectives.
- `atomscan --format=json`, using the local traits without updating or uploading,
  confirms the same classifications. Four negative controls also pass after
  copying outside `testdata/benign`, so that path cannot mask reverse-shell
  findings. They score 4, 4, 5 and 5 and retain neutral capabilities.

Strict validation still reports **176 oversized directories and 14 shared-matcher
review pairs**. Other authoring issues vary with concurrent worktree changes;
the last soft run also reported unrelated description/suppression issues.
Passing fixture checks does not make the global policy audit complete.

## Remaining reverse-shell siblings

`stdio` still mixes actual bridges with neutral stream operations, labels and
co-occurrence verdicts. Audit the bridge evidence before moving its composites:
the Node pipe claim lacks pipe requirements, the obfuscated Node claim lacks
network/shell evidence, and some native pipe/endpoint combinations do not prove
a relay. Preserve the observed operations in their neutral homes and add
positive/negative cases for any strengthened verdict.

`encoded` classifies by representation. Encoded `/dev/tcp` payloads belong with
that relay mechanism; a TCPClient mention, hidden launcher or decoded import set
alone does not prove a shell. Receive/execute/respond loops belong with remote
command dispatch. Resolve those evidence gaps before retiring the directory.
