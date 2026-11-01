# Hidden execution and environment staging review

The hidden-execution leaf held 92 rules. This review moved 25 neighboring rules
out and moved one supported WSH hidden-WMI behavior in, leaving 68. Node
option and obfuscation co-occurrences now live with command-option profiles;
they did not require a download or process launch. Window API and handle text
is separated from actual window hiding. Fork, signal and memory-map references
are an API profile rather than a concealment claim. Hidden-directory evidence
is classified with file hiding, and the existing Python daemon exception is
preserved with its consumer.

Four JPHP-specific UI/process profiles moved to the known JPHP runtime. The
individual preferred-height and preferred-width values are generic XML
components, not standalone proof of a hidden JPHP form. A pythonw path reference
moved to the known Python runtime. Seven other encoded-environment combinations
moved to their supported execution or evidence subjects, and one hidden-WMI
combination now describes the behavior it requires without assuming a
PowerShell command. The legacy environment leaf decreased from 44 to 36.

The review retained existing content and path exclusions on moved rules; it did
not add a new exemption. The window-API category has five rules and has room
for related observations. Every touched leaf is below the neighborhood-review
threshold.

[moves.json](moves.json) records original predicates, defaults, destinations,
severity and annotation changes. Run
`uv run docs/taxonomy-audit/taxonomy/hidden-env-neighborhood-review/check-moves.py`
to verify effective predicates, references and destination counts. The earlier
[environment review](../environment-staging-review/README.md) records the
first batch of moves.
