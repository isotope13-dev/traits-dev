# Archive validation regression audit

The AST-capture migration exposed an encrypted-stage fixture failure in the
newly built checkout engine. Isolated before/after taxonomy scans reproduced
it with both rule trees. Two evaluator defects were then reproduced separately.

## Member scope was lost during retroactive suppression

Tracing showed `npm-encrypted-stage-files-with-decrypt-loader` initially matched.
The new archive-wide retroactive pass then removed 28 findings, including the
ciphertext and both decrypt-loader observations, using suppressors pooled from
unrelated archive members. The staged-payload finding disappeared in the
subsequent orphan cleanup. The final serialized report still showed valid member
findings, which obscured the loss in the container's evidence pool.

The archive analyzer now records the IDs of findings created by its own atomic
and container-composite passes. Its added retroactive pass checks only those
findings. Existing member-local decisions are preserved; container rules still
see late container suppressors. The older special handling for built-in
anti-analysis findings remains unchanged.

A unit regression supplies a member payload, a sibling build marker, a package
finding relying on that payload, and a guarded package finding. The payload and
its dependent survive; the package rule with its own matching guard is removed.
The existing encrypted-stage fixture supplies end-to-end coverage, without
changing its score, hostile-count or required-prefix expectations.

## Positive chains could starve guarded rules

Container evaluation had a fixed five-round budget. Each round discovering
positive findings skipped the negative-condition pass. A positive dependency
chain could consume the whole budget, leaving every `unless` rule unevaluated.
The new seven-step regression failed before the repair, returning only steps
zero through four.

Evaluation now runs to stability, bounded by the number of composite definitions
plus a final stability check. Every productive round adds an unseen composite
ID, so this bound follows from the actual finite rule graph. Already-seen rules
are skipped. Positive evidence still settles before guarded rules run. The
regression verifies the full chain and an unrelated guarded finding survive,
while a finding excluded by the final chain step does not appear.

This fixes an independent, demonstrated bug; changing the iteration bound alone
did not repair the encrypted-stage fixture. The member-scope correction above
addresses its traced failure.

## Implementation and verification

Changes are in the sibling engine checkout: `src/analyzers/archive/mod.rs`,
`src/capabilities/mapper/evaluate_composites.rs`, and
`src/capabilities/mapper/evaluate_merged.rs`. Debug tracing now names container
results and retroactively suppressed IDs to make similar failures diagnosable.

Builds use the isolated manifest described in [PROPERTY-OPERATIONS.md](PROPERTY-OPERATIONS.md) with a local
filefacts override; the engine's Cargo.toml and Cargo.lock remain untouched.

Verification with the rebuilt checkout engine:

- **29/29 container/composite unit tests pass**, including both new regressions.
- The encrypted-stage archive again reports its required staged-payload finding
  and **three hostile findings**; its direct-scan score is **298**, up from 181
  in the failing checkout engine with the same current rules.
- **1,711/1,711 fixtures pass** under `validate --soft`: hostile 261, benign 421,
  does-nothing 175, drop-exec 45, supply-chain corpus 572, impact-wipe 66,
  obfuscation 82, reverse-shell 24, simple-stealer 65.
- Strict `make validate` exits 2 solely for **173 oversized directories**.
  No fixture thresholds, prefixes, trait scopes or suppression conditions were
  relaxed to achieve this result.
- Engine diff whitespace checks pass; Cargo.toml and Cargo.lock are unchanged.

Logs: `/tmp/taxonomy-archive-final-tests.log`,
`/tmp/taxonomy-archive-final-build.log`, `/tmp/taxonomy-archive-scope-soft.log`,
`/tmp/taxonomy-archive-scope-strict.log`, and
`/tmp/taxonomy-archive-scope-math-fixed.json`.

The taxonomy migration remains incomplete. Resume the neutral obfuscation
measurement and oversized-leaf audits with the restored fixture gate.

