# Shortcut command composite review

The remaining legacy command-content rules now sit with transformed or network script execution, download and installation behavior, obfuscation, and shortcut or network evidence profiles. Fetch-and-evaluate, staged installation and hidden payload-launch combinations retain their inferred objectives.

Generic language, archive-prefix and network references no longer claim execution or evasion. The former Konni label lacked a family-specific condition; the former MSHTML exploitation and mshta labels did not establish an exploit or an mshta invocation. HTTPS and `schtasks` references alone do not establish downloading or persistence. Those combinations are described as suspicious evidence profiles. Curl with an HTTPS and HTA reference does not by itself establish HTA execution.

The live legacy shortcut and dropper YAML rules have all moved. A pre-existing `.yaml.bak` file remains in the legacy tree; it is not loaded as a rule. Existing references were updated, including the security-hosts correlation that previously referenced the entire dropper directory. Source lineage for the command-content rules includes RustyNoob-619's shortcut downloader and Konni rules and bartblaze's LNK ruleset; provenance alone is not family identification.
