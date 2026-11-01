# Automation and hunting-query review

All 39 rules left the legacy automation leaf. n8n-specific header, environment,
node and configuration markers are in the existing n8n identity branch.
Generic `/api/v1/workflows` and credential paths do not establish n8n, so their
IDs and homes now describe workflow API paths and requests without naming a
vendor. The two create/activate/delete and credential/execution-query
composites are suspicious automation-management profiles: their predicates do
not establish unauthorized use or exfiltration. Routine n8n configuration
remains notable.

The KQL rules describe defensive hunting queries and their fields, filters and
joins. They no longer inherit exfiltration annotations or mark that query text
suspicious solely for looking for sensitive-file transfers. The query profiles
remain separate from `well-known/app/security/defender`: several existing
hostile-rule downgrades consume that entire identity directory, and a query
that references Defender tables does not identify the querying file as the
Defender program. A notable regression fixture exercises a legitimate
sensitive-file/email correlation query.

The diary text alternatives do not by themselves require a file write or
private-thought collection. The phrase is now a writing-vocabulary observation;
the combined skill and hidden-activity wording is a suspicious instruction
profile rather than a hostile theft claim.

[moves.json](moves.json) captures all original predicates, defaults and consumer
rewrites. `uv run docs/taxonomy-audit/taxonomy/automation-subjects/check-moves.py`
checks the 39 moves, intended severity and annotation changes, and directory
populations. No direct YAML reference selected the retired automation leaf.

Broader positive references to `micro-behaviors/communications/http/request`
now include the relocated workflow create/delete requests, which do describe
HTTP request syntax. No reference to that parent directory was found in an
exclusion or downgrade. The focused correlation-query check matched the new
query profile on the regression fixture.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,884 notable and
1,336 baseline fixtures. No YAML rules or references remain under the legacy
automation namespace.
