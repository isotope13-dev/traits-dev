Swift loader legs must share one source neighborhood
==========================================================

`swift-base64-shell-loader` used `scope: archive` with no proximity bound,
so base64 decoding in one file (iOS speech audio) plus shell use in another
(macOS debug menu) convicted a whole monorepo of "Swift decodes base64
before shell execution". The composite is now file-scoped with the same
40-line neighborhood as its C and Ruby siblings: every leg must occur in
one source file within 40 lines.

Run `python3 testdata/swift-base64-shell-loader/check.py
<scratch-directory>`. `swift-dropper-positive.swift` must report the
hostile; `swift-shell-only-negative.swift` and
`split-capabilities-negative.zip` (decode and shell use in different
members) must report no hostile at all.
