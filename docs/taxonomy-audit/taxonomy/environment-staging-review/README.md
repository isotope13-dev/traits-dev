# Environment staging review

The legacy encoded-environment leaf had 60 rules; 16 moved to environment and
encoding profiles, hidden execution, in-memory evaluation and Unicode
obfuscation, leaving 44. A long string assigned to a call expression does not by
itself establish an environment variable or an encoded payload. Incomplete
IEX and CJK fragments remain evidence profiles; combinations with sufficient
launch and evaluation evidence retain their behavioral homes and severity.

The existing direct-evaluation leaf was at 71 rules. Five neighboring rules
moved to their actual subjects: member-call text, Android loadUrl text, Excel
method-name bytes, a batch child-process command and embedded Python source.
A PowerShell-specific environment-evaluation rule was added, leaving 67.
Directory-wide consumers of direct evaluation were reviewed: they are positive
references, and no longer receive the removed observations as evaluation facts.

The legacy Invoke-Expression text rule excluded environment variables named
like VS Code, CI and build-command variables. Those names do not invalidate the
observed expression and can be attacker controlled. The relocated notable text
observation and the new PowerShell evaluation trait have no such exclusion. A
notable fixture uses `$env:VSCODE_ACTIVATE` to exercise that case. A separate
suspicious rule identifies an expression that directly evaluates an
environment variable explicitly named as a payload.

[moves.json](moves.json) records original predicates, defaults, destinations,
severity and annotation changes. Run
`uv run docs/taxonomy-audit/taxonomy/environment-staging-review/check-moves.py`
to verify the moves and directory sizes, and
`python3 docs/taxonomy-audit/taxonomy/environment-staging-review/check-eval.py`
to verify the variable-name regression.
