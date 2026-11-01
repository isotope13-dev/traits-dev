# Remaining sensitive-data source rules

The final 29 rules left `objectives/exfiltration/sensitive-data/source`, and
the now-empty `sensitive-data` tree was removed. Agent transcript and rollout
transfers are classified by their message content, card-record transfers by
payment-card data, and the password-filter/attachment pattern by files.
Credential transports, credential-value patterns and `.env` evidence use the
corresponding item subjects. Generic POST, field-name and route observations
no longer claim a specific recipient, network write or theft on their own.

A package/repository name mismatch beside proxy and event-logging settings is
suspicious context, but does not prove a typosquat or an export. Likewise,
three route-name references do not establish a POST; a WLAN clear-key command
beside a wallet route does not establish transfer; configured MCP forensic
logging is a telemetry capability; and an agent rollout upload is suspicious
without evidence that its destination is unauthorized. Those descriptions,
severities and inherited annotations were adjusted while predicates and scopes
were preserved. Same-file and package-level transcript constraints remain as
before; user-directed observability can have the same transfer shape.

Four rules were also moved out of the crowded file leaf: chat-log theft,
configuration export, and two transfers of shell-command output. The file leaf
fell from 69 to 66 after also receiving the legacy attachment rule. Its broad
positive consumer already selected the message directory; explicit references
were added for the moved configuration and command-output rules so those
signals remain available to that consumer.

[moves.json](moves.json) records original definitions and rewritten consumers.
`uv run docs/taxonomy-audit/taxonomy/source-subjects/check-moves.py` verifies all
33 moves, intended severity and annotation changes, and destination sizes.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,884 notable and
1,336 baseline fixtures. No YAML rules or live YAML references remain under
the retired `objectives/exfiltration/sensitive-data` namespace.
