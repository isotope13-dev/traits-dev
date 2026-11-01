# Signed-bundle behavior review

Fourteen composites moved out of legacy signed-bundle staging. The explicit
remote-injection combination moved to process injection, Java proxy-DLL
combinations to DLL-hijacking behavior, and the browser-credential combination
to browser recovery. Their hostile severities and predicates are retained.

The other combinations describe signed or unsigned bundles, embedded PEs,
executable/DLL name references, NSIS and registry/COM clues. These moved to
embedded-binary, installer, product-reference, PE-loader and COM-registration
profiles. Their descriptions no longer claim sideloading, persistence, a dump
stage or a verified signer when the combination only establishes references.
Several former hostile classifications became suspicious. All match legs,
size bounds, exclusions, confidence values and downgrades were checked against
the original rules. The broad legacy dropper consumer retains the moved members
as alternatives; the separate audit of its weak historical alternatives remains
open. Nine signed-bundle rules remain, including the remote-thread wrapper.

The adjacent browser multi-target directory contained 81 rules. Ten browser
recovery composites moved to `objectives/credential-access/browser/recovery`,
and one standalone password-parser name observation moved to source naming.
The original directory now holds 70 rules. All eleven moved rules preserve their
predicates and constraints, and exact references were updated. No directory-wide
consumers of the old multi-target namespace were found.
