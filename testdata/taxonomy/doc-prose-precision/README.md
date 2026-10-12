# Documentation-prose precision controls

Three matchers that reported a UI component library's docs and catalogs as
attack evidence, each with a positive that must still fire and a near-miss
drawn from the real false-positive evidence that must stay silent:

- `node-command-substitution-argument`: prose backticks ("the old node
  `` `position: ...` ``", "pass a node to `` `sidebar` ``") matched the loose
  backtick branch. Backticks now need a command shape (word + space) while
  `$(` stays loose — `node $(cat .cfg)` hides its script operand in a file,
  so requiring one there broke the polinrider hostile fixture.
- `destructive-agent-goal`: matched a safety rail ("confirm a destructive
  delete"). Confirmation-gated verbs (confirm/approve/verify + action) are
  now excluded via `not:`. Note the engine applies `not` per overlapping
  match: the gate must cover the flagged verb, so the near-miss keeps the
  confirmed verb inside the goal window. Other gating verbs (e.g. "read
  back") remain future work.
- `credential-description-field`: design tokens ("gap token"), object keys
  ("{ key"), word tokens ("unbroken token"), and hyphenated compounds
  ("token-owned") are not credential terms. The hyphen guard lives in the
  `if` pattern itself: a `not` pattern only sees the `if` match span, which
  ends at the keyword, so anything past it is invisible there.

Cases checked with `cleave --traits-dir . --json` and assertions over
emitted IDs. The tiny-file scan display filter can hide low-precision hits,
so the goal fixtures are realistic runbook/policy documents rather than
one-liners.
