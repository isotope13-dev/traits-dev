# Apex Accelerator and Wicked Executor review

Apex Accelerator's family-specific launcher and infrastructure indicators now join the existing Apex loader family. Generic audit wording and random-score clues moved to an audit-verdict profile. The scoring rule requires an authenticated JSON POST alongside the campaign endpoint and MCP tool, and the fake-audit rule retains the campaign verdict signal. Token-configuration references do not establish persistence, so that rule is a suspicious clue rather than a persistence claim.

Wicked Executor package identity is classified with droppers. Generic dependency, keyword, executable-name and encoded-string observations moved to their subjects. The embedded PE dropper pattern is an execution objective; the XClient and security-product string combination has neither a package identity requirement nor enough evidence to attribute AsyncRAT, so it is a suspicious profile rather than a family verdict.
