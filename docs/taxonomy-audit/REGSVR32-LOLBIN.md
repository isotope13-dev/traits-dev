# Regsvr32 and Squiblydoo placement

## Decision

Regsvr32 scriptlet execution is a named LOLBin technique, not a generic
download-and-file-launch chain. Its canonical objective home is
`objectives/execution/lolbin/regsvr32/`. The leaf contains the existing
`regsvr32-execution` composite and its Squiblydoo refinement, including plain,
encoded, and raw-hex evidence. Generic invocation evidence remains in the
neutral process-launch capability.

The Squiblydoo match requires Regsvr32, `scrobj`, and its `/i:` URL argument.
The broader Regsvr32 composite accepts either `scrobj` or its URL-argument
marker. Keeping both in one leaf expresses the broader technique and the
narrower remote-scriptlet variant at the same hierarchy level, without
duplicating either matcher.

## Migration and consumer audit

Moved the seven-rule Squiblydoo set from
`dropper/delivery/execute-download` and moved the existing two-rule Regsvr32
objective set out of `execution/lolbin/os`. The rules retain their effective
scope, predicates, suppressions, confidence, criticality, and IDs. Updated the
Windows LOLBin aggregator and DLL-hijacking consumer to canonical Regsvr32
references, the Equation Editor consumer to the canonical Squiblydoo ID, and
the FTP-banner aggregates to retain the complete Squiblydoo finding.

The source leaf drops from 257 to 250 rules. The new
`execution/lolbin/regsvr32` leaf contains nine rules. Soft fixture validation
passes all 1,837 cases; strict validation still reports the existing
catalog-wide quality and cap debt.
