# ICO mislabeled-good review, 2026-11-04

Preliminary structural review found 36 icon files with bounded directory
entries and no bytes outside their declared entries. Their 189 entries use
PNG or DIB formats. Fifty PNG entries have complete chunk framing; two have
only zero padding after IEND within their declared icon entries. One
additional file is 4,286 zero bytes. A supposed icon is an Apple resource
fork, and two others are software source archives.

Fresh scans of those 36 icons, the zero file, the resource fork, and the small
Min browser build recipe report no suspicious or hostile traits. The resource
fork's bounded map contains cursor, keyboard, icon, and fragment records. The
endpoint rulings for these 39 are good; recording awaits validation.

`9e6bee9ab529` is Boost source. Its scan of 17,086 components reported no
hostile traits and one suspicious framing-header sequence. The match is a
Beast parser test that expects a conflicting HTTP response to be rejected.
The trait description now says HTTP header rather than claiming a request,
because the matched bytes alone do not establish the message direction. The
archive needs a fresh scan and validation before its ruling is recorded.
