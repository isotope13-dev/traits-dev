# WSH fragment and size-limit review

The remaining 32 rules in the legacy WSH fragment file moved to their subjects:
partial strings, encoded COM names, command-option tokens, environment paths,
base64 text and string replacement. Incomplete tokens are components, not
independent claims of a download or execution. Four existing literal rules also
moved to more precise Discord, command-reference and file-function homes to
keep the fragment directory below the review threshold. The legacy encoded
script leaf contained 21 rules after this review; those were subsequently
migrated in the [retirement review](../encoded-script-retirement/README.md).
Isolated Discord and file-write name
fragments are components; the complete `discord_desktop_core` literal has a
separate notable identity rule.

The former 50 KB cap suppressed each fragment even when the exact same code
was present in a larger file. A tokenized WSH example and its 78,171-byte
padded version reproduced the difference: the small file matched both a
component and its suspicious profile, while the padded file matched neither.
The 31 capped fragments and their capped URL, status and profile consumers now
have no size limit; after the change both rules match in the padded example.
The status comparison also no longer excludes an entire
file just because it contains a WebSharper marker; that benign marker does not
negate an independently observed status comparison.

A hostile acquisition composite now consumes a notable combined COM-name
observation alongside its existing TEMP/EXE evidence. The combined observation
requires the same four component patterns as before; grouping them preserves
the acquisition predicate while keeping isolated fragments at component
severity.

[moves.json](moves.json) records the original rules, defaults, destinations,
severity changes and removed bounds. Run
`uv run docs/taxonomy-audit/taxonomy/wsh-fragment-review/check-moves.py`
to check predicates and references, and
`python3 docs/taxonomy-audit/taxonomy/wsh-fragment-review/check-padding.py`
to check matching in a padded bundle.
