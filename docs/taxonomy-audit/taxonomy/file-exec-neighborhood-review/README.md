# File-execution neighborhood review

The batch and embedded-script-host file-execution leaves held 91 and 85 rules.
They now contain 66 and 64. The review moved 50 rules in all, including two
legacy batch chains from the encoded-carrier staging leaf into the appropriate
file-execution leaves. The legacy carrier leaf now contains 44 rules.

Partial command strings, source-map and comment text, file-write references,
property fields and vendor copyright text were moved to their subjects. A
collection of single-character assignments does not establish substitution,
and incomplete command fragments do not establish a payload launch. A JScript
COM text co-occurrence became a suspicious file-write profile rather than a
hostile dropper. Actual JPG file-copy command patterns remain together as
file-copy behaviors. Obfuscated self-deletion and an embedded PE indicator
moved to their respective evasion and encoded-payload subjects; they do not
require a file-execution category to convey their supported behavior.

[moves.json](moves.json) records original predicates, defaults, identifier,
severity and description changes. Run
`uv run docs/taxonomy-audit/taxonomy/file-exec-neighborhood-review/check-moves.py`
to verify effective rules, references and directory populations. The prior
[batch carrier audit](../batch-carrier-review/README.md) records the earlier
part of this migration.
