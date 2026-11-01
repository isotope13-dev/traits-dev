# Object-schema neighborhood

The general object-schema leaf contained 89 rules. Nineteen host-related
observations moved: 18 object-field and host-profile patterns to
`data/serialize/schema-system`, and a hostname/platform/architecture text
sequence to `metadata/file/profile/host-information`, because it does not by
itself establish serialization. Subsequent cookie moves leave the general leaf
at 68 rules; `schema-system` contains 18.

Cookie and payment fields were reviewed with their siblings. A quoted
`"cookies"` string is a word observation under
`metadata/lang/natural/vocabulary/cookie`, not proof of an HTTP operation.
Cookie-specific fields and serialization move to `schema-cookie`; payment-card
fields move to `schema-payment`. The inherited credential-access annotations
were removed from the standalone password, cookie and payment field names:
those names do not by themselves establish credential access.

The first eight legacy browser-authentication rules were split by what they
support. Token-field observations live in `schema-credential`, a fetch/JSON
text pattern in HTTP body construction, and the composite requiring both token
and cookie fields plus the fetch pattern in `stealer/multi-item`. The legacy
browser leaf now has 35 rules and remains under review.

[moves.json](moves.json) and the [browser move inventory](../browser-auth-subjects/moves.json)
record original predicates, defaults, destinations and rewritten consumers.
No YAML directory references selected the affected original leaves alone; the
transfers remain under the exfiltration ancestor while partial observations no
longer claim that outcome. Run
`uv run docs/taxonomy-audit/taxonomy/object-schema-neighborhood/check-moves.py`
to check matchers, scopes, severity, the retained session composite, the
intentional annotation changes and physical/namespace populations.

`make validate` passed after this migration: 1,927 hostile, 1,774 suspicious,
8,883 notable and 1,336 baseline fixtures.
