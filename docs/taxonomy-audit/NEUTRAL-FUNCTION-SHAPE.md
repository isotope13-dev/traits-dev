# Neutral function shape and computed-access audit

Six observations move from obfuscation to their established subjects. The
[12-entry ledger](neutral-function-shape-mapping.json) records all six moves and
six consumer updates; its effective after-definitions match current rules. The
[five-consumer ancestor audit](neutral-function-shape-ancestor-audit.json)
records the intentional consequences for broad obfuscation references.

## Boundaries and sibling audit

Three constant-return observations—count, ratio, and their larger-file
conjunction—belong with `metadata/file/function`, alongside the existing
constant-return measurements. Their thresholds differ: the moved rules use six
functions and a 0.5 ratio; existing siblings use 100 functions and a 0.9 ratio,
with different scopes and size/exclusion constraints. They are not equivalent
matchers and were not merged. None establishes padding or dead code.

The anonymous-function count also belongs with function metadata. Its metric
counts anonymous functions; it does not establish arrow syntax or abuse. The
Python sibling uses a different threshold and scope, so remains distinct in the
same language-neutral directory.

Function-selected indexing belongs with property access, not decoder evidence.
The query captures a function identifier supplying the key, with a minimum
count of three. Its predicate is unchanged. The computed-call argument matcher
belongs with dispatch and is named `computed-call-hex-token-pairs`: its character
class accepts `beef`, `face`, `cafe`, `dead`, `fade` and `feed`, so calling the
arguments numeric constants or offsets would overstate the evidence.

All scopes, thresholds, confidences, exclusions and atomic predicates are
preserved. Platform list order is normalized in the metadata file's defaults.
The six-function metric changes from component to baseline: it is a complete,
common structural measurement, not an incomplete obfuscation fragment. Other
criticalities are unchanged. Unsupported inherited obfuscation annotations
were removed from the relocated runtime-indirection observations.

## Consumers

Exact consumers now reference the new canonical IDs, including the encrypted
module-loader rule exercised by the existing math-universe fixture. The moved
constant-return conjunction still requires both original thresholds and retains
its original size floor and exclusions.

Broad obfuscation ancestry no longer includes these neutral observations. The
long-tail build-config rule therefore still needs actual obfuscation evidence;
hidden-listener and concealed-exfiltration alternatives no longer inherit mere
function shape. The `js-has-tests-without-obfuscation` suppressor likewise no
longer treats these observations alone as a reason to reject its benign context.
The PHP ancestor consumer cannot observe these JS/TS-scoped atoms. These are
intentional semantic changes, not a promise of identical classifications for
all unseen samples.

## Validation

Three new benign ZIPs cover eight constant-return functions in a larger file,
105 anonymous callbacks, and function-selected keys alongside identifier-shaped
computed-call arguments. The computed control requires internal findings from
both property/access and dispatch and forbids the former runtime-indirection
hierarchy. The function controls require function metadata and forbid their
former obfuscation leaves.

Atomscan before/after archive/member scores:

| Control | Before | After |
|---|---:|---:|
| Constant returns | 4 / 2 | 3 / 2 |
| Anonymous callbacks | 3 / 1 | 3 / 1 |
| Computed access and calls | 3 / 2 | 3 / 2 |

No control produces suspicious or hostile findings. The constant-return ratio
and count are newly visible in rendered output after relocation; atomscan's
rendering is not a complete internal-match inventory. The predicates themselves
are unchanged. Direct `test-rules` checks pass for all three constant-return
rules. The combined computed-access/call debugger run stalled with sustained CPU
use for more than a minute, including after SIGTERM; it was explicitly stopped.
It is not counted as a successful test. Normal scans and the fixture runner
complete and verify the two required internal directory findings. Investigate
the standalone debugger separately; no matcher was weakened to avoid it.

With the rebuilt engine from [the archive repair](ARCHIVE-VALIDATION.md),
**1,714/1,714 fixtures pass**: hostile 261, benign 424, does-nothing 175,
drop-exec 45, supply-chain corpus 572, impact-wipe 66, obfuscation 82,
reverse-shell 24 and simple-stealer 65. Strict `make validate` exits 2 solely
for **173 oversized directories**. There are **zero mixed nodes**.

| Leaf | Before | After |
|---|---:|---:|
| metadata/file/function | 16 | 20 |
| data/property/access | 26 | 27 |
| data/control-flow/dispatch | 69 | 70 |
| obfuscation/code-metrics/runtime-indirection | 8 | 5 |
| obfuscation/control-flow/retry | 12 | 9 |

Logs are `/tmp/taxonomy-neutral-function-shape-{before,after}.json`,
`/tmp/taxonomy-neutral-function-shape-constant-trace.log`,
`/tmp/taxonomy-neutral-function-shape-soft-confirm.log`, and
`/tmp/taxonomy-neutral-function-shape-strict-final.log`.

## Remaining work

The runtime-indirection leaf still contains indexOf and character-code
observations whose decoder labels need examination; its three composite intent
claims also need independent evidence review. Retry siblings include ordinary
loop/try shapes and a regex-looking `substr` matcher; neither should be assumed
correct merely because it remains under obfuscation. Hex arithmetic and the
misnamed mixed-hex-decimal matcher remain queued: the latter checks only for a
hex literal. Continue their sibling and relationship audits before revising
consumers. The wider cap migration remains incomplete.
