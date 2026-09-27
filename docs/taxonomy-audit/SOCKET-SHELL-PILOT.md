# Socket-shell pilot: completed batch, 2026-09-27

The `objectives/command-and-control/reverse-shell/socket-exec` catch-all is
removed. Its last 43 rules comprised 32 relocated observations/composites and
11 unsupported verdicts. Destination cleanup moved 13 additional observations;
a follow-up moved 15 Perl descriptor observations and shell composites out of
`reverse-shell/dup`. Total: **60 moved, 11 retired**.

This is the checkpoint for that batch. The subsequent
[descriptor migration](DESCRIPTOR-MECHANISMS.md) retires the remaining `dup`
and `syscall` leaves and records the newer validation results.

The policy remains strictly leaf-only. Every destination in this batch contains
at most 85 atomic/composite rules. No overflow directory or exemption was added.
The oversized-directory count fell from 177 to 176 after neutral observations
left `backdoor/keywords`.

## Placement decisions

- Socket addresses and URI strings belong in `socket/endpoint` and `socket/uri`;
  they do not prove a connection. Moving three such observations freed the
  connection leaf for actual connect-call evidence.
- PHP query tests, directory enumeration, file reads/writes, received-upload
  moves and directory removal belong with those neutral operations. VMware
  guest-host interface names describe virtualization, not an attacker backdoor.
  Their former backdoor-keyword composites reference the relocated facts.
- Inline interpreter commands mentioning sockets and subprocesses remain
  neutral inline-code observations unless the required evidence establishes a
  relay. API-name and pipe-process observations similarly follow their operation.
- Ruby reopening stdin/stdout before shell execution uses `fd-redirect`.
  Groovy copying socket input into a child and child output to the socket uses
  `stream-bridge`. A Ruby receive/execute/respond loop uses `remote-command/dispatch`.
- Perl descriptor duplication is neutral: a duplicated handle need not be a
  socket. The relay composites belong in `fd-redirect` and add network/shell
  context. Shebang and IP parsing observations have their own subjects.

## Intentional detection changes

Socket-plus-shell co-occurrence alone no longer supplies Ruby/Groovy
reverse-shell verdicts. A query-name string beside an interpolated command no
longer claims an HTTP command shell. The neutral observations remain available.
The new Ruby descriptor relay requires both standard-input and standard-output
reopening; the Groovy bridge additionally requires input forwarding. The Ruby
Open3 dispatch composite now requires receiving commands and writing responses.

Two neighboring Perl composites lacked facts claimed by their descriptions:
one now requires stdio redirection; the other requires a connection and shell
execution. The connection observation includes `static-lib` to preserve the
strengthened consumer's declared file-type coverage.

These are precision repairs, not claims of exact predicate equivalence.
Descriptions, attack labels and criticality on neutral observations were also
corrected where they previously asserted an attacker objective. No library
presence or socket API alone establishes shell I/O or malicious intent.

The rules use syntactic evidence and proximity, not general dataflow proof.
The tests distinguish concrete connected-stream patterns from independent
socket/process operations; they do not establish correctness for every possible
aliasing or control-flow arrangement.

## Mapping and reference evidence

- [Socket and destination-cleanup mapping](socket-pilot-mapping.json) records
  all 56 original definitions, their effective defaults, destinations, changed
  definitions and retirement reasons.
- [Perl descriptor mapping](perl-descriptor-mapping.json) records all 15 later
  relocations with effective definitions.
- Exact references were updated, including the PowerBots family consumer and
  the Groovy netcat composite. No active YAML reference to `socket-exec` remains.
- Behinder's class-only composite references the remaining `dup` directory.
  Its relocated Perl members target Perl/text/static-library files, not class
  files; none was an eligible direct class-file leg. The directory reference
  still needs explicit review when the remaining `dup` rules are migrated.

## Validation

Before: 1,610 fixture checks passed in soft mode. After: **1,614 passed**:
246 hostile, 341 benign, 175 does-nothing, 45 drop-exec, 572 supply-chain,
66 impact-wipe, 82 obfuscation, 22 reverse-shell, 65 simple-stealer.

The four new fixtures cover independent Ruby/Perl/Groovy socket-and-shell
operations and a Ruby socket command loop. Controls forbid the entire
reverse-shell hierarchy, including incorrectly placed neutral observations.
The existing Ruby, Perl and Groovy reverse-shell fixtures retain hostile
findings. Focused post-change scores were 122, 126 and 122 respectively;
the independent-operation controls scored 4, 4 and 2.

Duplicate validation passes 142 tests, including seven new regressions.
The [14 shared-matcher candidates](duplicate-review.json) include their source
locations and the differences reported by the validator. Composed mapping
verification confirms all 60 moved effective definitions across 30 destination
leaves, with no destination over 85.
Strict validation remains red: **176 oversized directories**, **14 shared-matcher
review pairs**, and unrelated authoring issues in the shared worktree.
Soft validation is evidence of fixture preservation, not completion of the
whole taxonomy migration or proof of improved ML accuracy.

## Remaining work

The subsequent descriptor batch resolves `dup` and `syscall`. Reconcile the
remaining `stdio` and `encoded` leaves against the mechanism contracts before
calling the whole reverse-shell family complete.
Review the 14 shared-matcher pairs with their scope/verdict differences; do not
merge scopes mechanically. Then migrate bounded, dependency-complete batches
from the remaining oversized cohorts. Keep model evaluation separate from
semantic placement and fixture preservation.
