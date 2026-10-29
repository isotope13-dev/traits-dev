# Process taxonomy boundary audit

The affected resource determines the home. `process/` covers execution contexts,
their lifecycle and coordination, descriptors, standard streams, interpreters and
execution transfer. Merely running inside a process is insufficient.

Reviewed the hierarchy of **298 original populated directories**. The migration
moves **1,887 definitions**, including **1,660 originally under process/**, and
bans **64 old subtrees**, including newly nested descendants. The complete move
map is [moves.csv](moves.csv); the directory inventory is
[directories.csv](directories.csv). Decisions and verification limits are in
[audit.json](audit.json).

Examples:

| Old category | Required subject after review |
|---|---|
| `process/io` | Generic `data/stream`, or explicit `process/stdio` |
| `process/hook/xhr` | HTTP interception and its supporting observations |
| `process/tls` | Thread/fiber-local memory storage |
| `process/create/{compile,load,macro}` | Code generation, module loading, or application events |
| `process/create/{flags,installer}` | Launch configuration, package operations, or actual launch mechanisms |
| `process/create/shell/{lang,bridge}` | Actual command execution, dispatch, module reference, or the affected resource |
| `process/inject/{handle,memory}` | Descriptor operations and process queries unless transfer is established |

The destination review also separates Git operations into read (13), write (40),
transfer (27), and configure (13). Mixed repository operations retain the generic
repository subject. No destination that was within the 85-rule limit at the
start is now over it.

Two detection corrections accompany the moves: command-guard suppressions now
require a guard implementation or structured policy test instead of arbitrary
command fragments; two broad installer-directory suppressions were removed
because installer text does not establish benign context. Existing specific MSI
and recognized-source suppressions remain. The comparison records 37 reviewed
consumer clauses, including an equivalent Mercurial-selector simplification.
Five numeric/boolean-looking textual matcher values across four files are
explicitly quoted for consistent YAML parsing. Fourteen descriptions no longer overstate invocation,
shell execution or intent.

Validation enforces the banned subtrees through the local review script and the
sibling cleave validator. The 85-rule maximum remains unchanged. The remaining
250 validator-reported oversized directories were already oversized at the start; they still make
`make validate` fail. This audit does not waive those failures.

Verification: 23 engine directory tests; three local boundary/parity tests covering all
64 banned subtrees; synthetic shell-command, shell-guard and Python-guard scan
probes; and comparison of all 145,182 original effective rule definitions.
The comparison permits the recorded consumer-clause changes and description
corrections. It does not certify every retained matcher or promise identical
findings for broad selectors whose taxonomy membership changed.

A follow-up accounting discrepancy is recorded for `well-known/malware/trojan/elex/identity`: 88 physical definitions, with some explicit IDs in the parent namespace, escape the reported directory count. This needs review with the remaining capacity work.
