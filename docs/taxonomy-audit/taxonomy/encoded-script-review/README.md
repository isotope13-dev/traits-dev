# Encoded-script staging review

The legacy encoded-script leaf contained 77 traits. This review moved 24 of
its rules, leaving 53. Seven slice expressions are literal fragments rather
than standalone evidence of a downloader; the combined WSH temp-executable
chain remains hostile and moves to script-host file execution. The HTTP URL
and status observations move to their own subjects. Other composites separate
likely executable acquisition, file execution, decoy creation and incomplete
operation or encoding clues.

The script-host execution leaf was reviewed at the same time. Twelve rules
moved to acquisition, transformed-source evaluation or evidence profiles,
leaving that leaf at 58 after it received the newly migrated WSH chains. An
identical WSH rule was merged with its existing counterpart; its previous
suppression by a more specific sibling was removed so the merged rule retains
the migrated rule's coverage. A
script written to disk is not automatically executed; a coherent combination
of download, writing and launch evidence can still support the inferred chain
without proof of data flow. Weak COM and encoded-string co-occurrences remain
suspicious profiles instead of complete execution claims.

The remaining WSH fragments and their 50 KB size limits were subsequently
reviewed with their consumers; see the
[WSH fragment review](../wsh-fragment-review/README.md).
The remaining encoded-script rules were then moved and the legacy leaf
removed; see the [retirement review](../encoded-script-retirement/README.md).

[moves.json](moves.json) records source predicates, defaults, destinations,
severity and description changes. Run
`uv run docs/taxonomy-audit/taxonomy/encoded-script-review/check-moves.py`
to check the moves, references and destination sizes.
