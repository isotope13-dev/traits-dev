# XOR staging and staged-loader review

The seven-rule `staging-xor` leaf is removed. A source pattern that combines
XOR processing with named beacon and exfil HTTP calls is classified as an HTTP
control channel. Its key-name, URL-name, XOR-loop and request-call observations
are placed by their own subjects. Two binary patterns contain encoded network
or installer clues but do not require a download or activation; they are now
suspicious encoded-network profiles rather than hostile stagers.

Fifteen rules also left the crowded `staged-loader` leaf, reducing it from 81
to 66. A DEX-version field, class field and remote descriptor are schema or
module-loading observations, not a fetched payload. A resource extraction plus
block copy is an embedded-resource capability. Unbound resource/load, Android
asset/loader and repeated image-named script evidence remains available as
profiles, with descriptions and severity reflecting what is actually required.
Three JNI rules formerly claimed decrypt/write/load behavior from class-name and
signature strings alone; they are now suspicious reference profiles.

The Llac family composite still requires the relocated resource/assembly profile
alongside its family-specific evidence. An Android rule using a local descriptor
reference was updated to the new qualified ID. One broad dropper-directory
consumer no longer treats these partial profiles as standalone dropper evidence;
that change follows the corrected classifications. A direct managed-HTTP
client-directory consumer now includes the named GET/POST observation as a
positive HTTP-client signal.

[moves.json](moves.json) records the original rules and references.
`uv run docs/taxonomy-audit/taxonomy/staging-xor-and-loader/check-moves.py`
checks all 22 predicates, effective defaults, intended severity changes and
destination counts. The much larger staging tree and remaining staged-loader
rules still need review.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,884 notable and
1,336 baseline fixtures.
