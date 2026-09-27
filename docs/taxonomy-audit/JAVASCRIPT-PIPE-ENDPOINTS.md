# Matching both pipe endpoints

Follow-up to [the JavaScript stdio batch](JAVASCRIPT-STDIO.md). Requiring two
independent pipe observations still allowed an unrelated network call to turn
ordinary file-backed child stdin/stdout into a reverse-shell verdict.

## Reproduction and change

`node-independent-local-pipes.js` supplies a local file to a local shell's stdin,
logs its stdout to another file, and separately contacts a health-check socket.
Before this change it scored 131 and emitted two hostile reverse-shell findings.
Afterward it scores 12 with neither finding. Its individual networking, process,
and pipe observations remain available.

The new `micro-behaviors/process/fd/stdio::node-duplex-stdio-pipe-pair` requires:

1. A peer's `pipe()` targets a child's `stdin`.
2. That same child's `stdout` or `stderr` pipes back to the same peer identifier.
3. Peer and child are distinct identifiers in the same syntax parent.

Separate statements and direct call siblings (such as comma sequences) are
supported in either order. Calls with different peers or different children do
not match. The atom is a neutral standard-stream observation, not a network or
shell verdict. There is no new taxonomy layer for its AST implementation.

The existing call projection exposes `sock.pipe` and a member argument as an
unstructured expression; binding facts provide a call shape without the result's
source expression. These projections cannot join two arbitrary endpoint names.
The tree-sitter query is therefore justified by cross-call identity constraints,
not merely by matching an ordinary API call. No extractor changes were made.

Seven relay composites replace their separate input/output pipe requirements
with the canonical pair. Other connection, shell, scope, confidence, proximity,
and exclusion requirements remain unchanged. The extension wrapper inherits the
stronger relay evidence. The event-driven data-to-stdin-write form has different
mechanics and is not silently replaced by a pipe-only rule.

[The seven-consumer ledger](js-pipe-binding-mapping.json) records effective
before/after definitions. Earlier migration ledgers are historical snapshots;
this ledger supersedes their seven affected composite definitions.

## Coverage and remaining limits

Direct matcher checks confirm ordinary order, output-first order, and comma
sequences, including a TypeScript source. Separate checks reject mismatched peer
and child names. Permanent fixtures include the independent-file-pipe control,
a shared peer connected to two different children, and output-first JS and
comma-separated TS relays. The existing JS/TS and extension relay controls retain
their hostile findings. The different-child control scores 7 with no relay.

This is a syntactic name relationship, not full data-flow analysis: it does not
prove the peer is the connected socket, reject later reassignment, resolve
aliases, or connect calls across separate callbacks. Such indirect forms retain
their neutral pipe observations but may no longer satisfy these seven hostile
composites. Those forms require specimen-driven coverage rather than restoring
the known-false file-wide co-occurrence fallback. The remaining network-binding
and event-handler forms, and the opaque-obfuscation verdict, remain audit work.

The subsequent [unsupported stdio audit](UNSUPPORTED-STDIO.md) resolves the
opaque-code verdict by reproducing its local-only false positive and retiring
the unsupported aggregate. The indirect pipe forms remain open.

## Validation

All **1,640/1,640** fixture checks pass, including **24/24** reverse-shell fixtures.
The fd/stdio leaf has **71** combined rules. Final strict/structural checks and
the broader remaining migration state are recorded in PLAN.md.
