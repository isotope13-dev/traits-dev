# Shell downloader fallback capability

`downloader-curl-wget-fallback`, `downloader-wget-lwp-fallback`, and their
`downloader-fallback-chain` composite detect downloader resilience. They do not
establish that a payload was downloaded or executed. Their canonical home is
`micro-behaviors/communications/http/download/fallback/`; dropper composites
reference the capability and separately require staging-to-activation evidence.

All three rules moved from `objectives/command-and-control/dropper/delivery/execute-download`
to `micro-behaviors/communications/http/download/fallback/shell-command-cascade.yaml`.
Their matcher bodies, scopes, confidence, criticality, and effective ATT&CK/MBC
metadata are preserved. The two raw-IP shell dropper composites now reference
the canonical fallback-chain ID.

The leaf distinguishes two evidence strengths: conditional shell syntax such
as `curl ... || wget ...` identifies an explicit alternate attempt; a composite
that finds multiple download clients only supports the program's fallback
capability. Neither establishes that a retry happened at runtime. The directory's
multi-client marker is an evidence clue, not an event claim.

Soft validation passes all **1,837/1,837 fixtures**. The source
`delivery/execute-download` leaf drops from 306 to 303 rules. Strict validation
remains at **59 issues**, including **165 over-cap directories**.
