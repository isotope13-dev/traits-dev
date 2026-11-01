# Agent approval split

The LLM instruction-override leaf had 80 rules before the concurrent changes.
Ten approval- and consent-bypass observations and composites moved to the
sibling `llm/approval` subject. A further rule and its supporting traits were
retired on the other branch, leaving 69 rules in `override` and 10 in `approval`. General
instruction-priority overrides remain in the original category. User-directed
and isolated-harness exceptions remain in their original namespace and are
referenced explicitly by the relocated rules.

[moves.json](moves.json) records original rules, defaults, ID mappings and
rewritten consumer files. The move preserves effective predicates, scope,
criticality and confidence, except that the rebase retains the other branch's
narrower approval indicators and retirement of the persona-and-gate rule.
No directory consumer of the old override leaf
was found before the move; references to the parent `llm` subtree continue to
include both subjects. Run `uv run docs/taxonomy-audit/taxonomy/llm-approval/check-moves.py` to verify definitions and physical/namespace counts.

A focused `cleave test-rules` check matched
`approval::agent-skill-default-authorization-override` on the synthetic
`cases/positive/skills/example/SKILL.md` and did not match it on the
user-confirmation control at `cases/control/skills/example/SKILL.md`.
These fixtures are analyzed as text; their contents are not instructions to
execute.

After the approval, file-exfiltration and Go profile changes, `make validate`
passed all 13,920 fixtures: 1,927 hostile, 1,774 suspicious, 8,883 notable and
1,336 baseline.
