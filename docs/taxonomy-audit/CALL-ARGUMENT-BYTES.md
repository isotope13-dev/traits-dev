# Unbound argument bytes do not identify an OpenSSL operation

The native TLS audit reproduced six false operation claims with an inert ELF.
Four x64 byte patterns match register constants and a relative call, but do not
resolve that call's target. A second control adds an incidental `SSL_connect`
symbol reference in data; all four primitives and both suspicious OpenSSL
composites match, even though every encoded call targets a local `ret` stub.
Disassembly confirms the targets. Neither control is executed.

## Corrected placement and claims

Four byte observations and two symbol/byte profiles move to
`metadata/binary/code/arguments`, with architecture in `x64.yaml`. This leaf
admits byte sequences resembling argument-register setup and profiles of those
sequences. It does not claim instruction alignment, a resolved callee, ABI-valid
execution, or the target API's argument semantics. Other byte properties retain
their actual subjects; this is not an overflow bucket for unidentified behavior.

| Previous claim | Correct observation |
|---|---|
| Disables OpenSSL peer verification | Null-check and zero-register byte sequence |
| Sets TLS 1.2 minimum | Register-load bytes for 123 and 771 |
| Enables moving-buffer/partial writes | Register-load bytes for 33 and 3 |
| Enables automatic retry | Register-load bytes for 33 and 7 |
| OpenSSL client disables verification | SSL_connect symbol plus zero-register bytes |
| OpenSSL tunes writes/retries | SSL_connect symbol plus both mode-argument byte sequences |

The [seven-entry ledger](call-argument-bytes-mapping.json) preserves all matcher
bodies, conditions, scopes, confidence and exclusions modulo canonical IDs.
The four primitive criticalities remain notable. The two former suspicious
profiles become notable characteristics after relocation and relabeling: their
conjunctions do not establish verification bypass or a suspicious session mode.
This is not a criticality-only repair.

The native secure-beacon consumer is renamed
`native-secure-beacon-call-argument-profile`. Its predicate and hostile
criticality remain unchanged, preserving its existing beacon detection while
removing the unsupported claim that the sample disables TLS verification. This
cohort does not independently validate that beacon family's entire taxonomy.

Actual TLS configuration/API observations belong in the corresponding
`communications/tls` operation. To restore an operation-specific binary rule,
require target resolution at the matched call site plus the appropriate
argument evidence. An unrelated import elsewhere in the file is insufficient.
Do not strengthen the old inference merely by adding more incidental imports.

## Consumers and verification

The [ten-occurrence ancestor audit](call-argument-bytes-ancestor-audit.json)
records source and destination effects. Generic byte sequences no longer provide
communications/socket evidence. Both moved profiles require SSL_connect, whose
existing canonical observation remains under communications. The metadata/binary
consumer is PE/DLL-only and cannot gain support from these ELF-only predicates.
The renamed beacon stays in its command-and-control ancestor with the same
conditions and criticality.

Two benign ZIP fixtures contain the inert ELF controls and their assembly
sources: `unrelated-call-arguments.zip` and `incidental-tls-call-arguments.zip`.
They require code-characteristic observations and forbid verification-disable
findings. The no-import control also forbids socket SSL findings; the incidental
import control retains ordinary SSL symbol evidence. Exact before/after traces
on the latter match all six predicates, showing preservation of the underlying
observations. Matching six predicates is evidence for the byte profiles, not
proof of the former API interpretation.

Build commands used `cc -shared -nostdlib -Wl,--build-id=none`, with the extra
`incidental-tls-import.S` source for the second binary. Logs, disassembly inputs,
read-only atomscan snapshots and exact traces are in
`/tmp/taxonomy-call-arguments/`.

## Validator follow-up

Flag behavioral API claims based on wildcard relative-call bytes without bound
callee evidence for review. A code shape plus file-wide API presence cannot
prove that the matched call invokes that API. This requires a structural check
or review heuristic; it is not evidence that every hex matcher is invalid.
The same issue should be audited in other architecture-specific option/config
rules before interpreting their numeric constants as API arguments.

Final validation: **1,755/1,755 fixtures pass**, including **465 benign**.
Strict `make validate` exits **2**, reporting only **169 oversized directories**;
there are **zero mixed nodes**. Socket SSL falls **82 → 76** and the new metadata
leaf has **6 rules**. No unrelated changed/removed definitions appear in this
cohort's effective snapshot comparison. Installed before/after findings agree
on both controls after applying the ID map and the two intentional suspicious
→ notable profile corrections. The broad migration remains incomplete.
