# Sandbox neighborhood review

The `suite` and `script` directories each started with 87 rules. They mixed
analysis checks with rules combining checks and other actions. This review
moved 33 sandbox rules by their supported subject; the original directories
now contain 70 and 71 rules respectively. They still need claim-by-claim review,
including the rules that remain grouped by source language.

- Resource, display and input checks moved to `sandbox-detect/environment`;
  hostname comparisons moved to `sandbox-detect/hostname`.
- CI and sandbox-gated execution moved to `sandbox-detect/enforcement`,
  sandbox scoring to `sandbox-detect/score`, and analyst-tool fingerprinting to
  `tool-detect/process`.
- Credential/environment export chains moved to the corresponding
  `exfiltration/stealer/configuration/environment` objective. A host-profile
  export moved to `system-info/identity`; account-inventory exports formerly
  mixed into that leaf moved to `system-info/account`. The identity leaf went
  from 78 to 69 rules, and the new account leaf contains 10.
- Five bare Go routine-name strings moved to
  `metadata/binary/symbols/name/analysis`; descriptions now state that they
  are names rather than calls, and the anti-analysis ATT&CK label was removed.
  A generic Java return pattern and a sandbox-related text message also had
  unsupported ATT&CK/MBC labels removed when moved to neutral subjects.

The original predicates, defaults, old/new IDs and consumer files are recorded
in [moves.json](moves.json), [second-moves.json](second-moves.json),
[third-moves.json](third-moves.json), and [fourth-moves.json](fourth-moves.json).
The last move record includes ten account exports and a second relocation of
one sandbox rule, for 44 relocation records covering 43 distinct rules.
Predicate, effective scope, severity and confidence comparisons passed for
all 44 records. Descriptions and the three neutral groups' attack annotations were intentionally adjusted as described
above. Exact-ID consumers were retargeted, and no YAML directory reference to
the two old namespaces was found before the second batch.

Run `uv run docs/taxonomy-audit/taxonomy/sandbox-neighborhood/check-moves.py`
to repeat the comparisons and print destination populations. The largest destination has 69 rules.

`cleave test-rules` matched both the relocated `score::python-sandbox-score-exit`
and its dependent encrypted archive launcher on
`testdata/hostile/generated/python-bad-triage/sandbox-archive-loader.py`.
`make validate` passed after the sandbox and account/identity splits: all
13,920 classified fixtures passed (1,927 hostile, 1,774 suspicious, 8,883
notable and 1,336 baseline).
