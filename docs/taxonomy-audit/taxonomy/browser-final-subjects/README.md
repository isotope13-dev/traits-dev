# Remaining legacy browser rules

The final 22 rules have moved out of `objectives/exfiltration/sensitive-data/browser`.
Partial route, identifier, field and phrase observations now describe those
facts without inheriting exfiltration annotations. The same-file selection and
LLM POST co-occurrence is an HTTP capability; the suspicious extension rule
that uses it is classified by the selected page content.

An email-address transfer is classified by account identity, navigation-event
reporting by activity, and the credential-plus-page-text pair by its multiple
required subjects. The Prime Video rule requires a viewing tracker and POST
text, not an actual send, so it is classified as activity collection with that
context. Its known-panel exception remains intact.

Five weaker browser composites are profiles: report-name and POST text;
course-sync and PDF references; cloud-sync references plus permissions; page
schema and an LLM endpoint; and page relay plus an LLM endpoint. None requires
an outbound request. The page-relay composite was hostile; it is now
suspicious until a transfer is independently evidenced. Exceptions, scopes and
match predicates remain as recorded in [moves.json](moves.json).

`uv run docs/taxonomy-audit/taxonomy/browser-final-subjects/check-moves.py`
compares all predicates and effective defaults, including the intentional
annotation and severity changes. The selected-text LLM rule retains its
user-key/provider downgrade, and the credential/page-content composite keeps
its same-file proximity and remote-host requirements. Direct YAML directory
consumers of the retired browser leaf were absent before the move.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,883 notable and
1,336 baseline fixtures. No YAML rules or references remain under the legacy
browser namespace.
