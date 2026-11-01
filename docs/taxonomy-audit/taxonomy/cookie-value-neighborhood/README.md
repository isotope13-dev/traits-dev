# Browser-state and cookie review

The cookie leaf contained 76 rules. Twelve moved to `application-state/browser-state`
because their bound browser-store paths allow either `Cookies` or `Login Data`;
those alternatives do not require a cookie. A native rule accepting either a
Firefox cookie query or a history query moved there as well, with its name and
description corrected. It is 13 rules. Cookie is now 60 rules, including one
cookie/export co-occurrence migrated from the legacy browser leaf.

Four observations moved to `metadata/file/profile/browser-session`. One already
reported a suspicious co-occurrence of store paths and HTTP-related indicators.
The other three had been hostile cookie-exfiltration findings, but required
only remote-script loading, an XHR handler, or an XHR `open` call respectively;
none requires an upload or another indicated outbound data channel. Their
descriptions now state the evidence,
their severity is suspicious, and their unsupported theft annotations are
removed. Their match conditions and scopes are unchanged.

The original definitions and reference rewrites are in [moves.json](moves.json).
Run `uv run docs/taxonomy-audit/taxonomy/cookie-value-neighborhood/check-moves.py`
to check the 18 moves, their effective defaults and the three destination counts.
The remaining cookie rules still warrant individual review, especially those
whose predicates admit history, other browser state, or authenticated tokens.

`make validate` passed after this review: 1,927 hostile, 1,774 suspicious,
8,883 notable and 1,336 baseline fixtures.
