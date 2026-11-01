# Token and session-data neighborhood

The token leaf started at 81 rules. The review moved 14 rules out and two
LinkedIn authentication-cookie transfer rules in from the legacy browser leaf;
the token leaf now has 69 rules. The LinkedIn rules require `li_at`, rather
than treating an arbitrary cookie as a token.

A Telegram `tdata` archive and WhatsApp session-store material moved to chat
application state: the matchers select session stores or records rather than a
specific bearer-token value. A broader Rust app-data archive rule accepts chat
state or browser extension settings and moved to application state. An upload
capability with no required sensitive target moved to HTTP-upload metadata.
A selected `.credentials.json` file with read and POST context moved to
credential-file export.

Roblox cookie-format/store and file-host references, Discord token-pattern and
webhook references, and browser-storage/webhook references do not require an
upload. Those four are now suspicious metadata profiles, with theft annotations
removed; their match conditions and scopes remain unchanged. The separate
Roblox cookie transfer remains classified under cookie state. A generic
`extractSession`/POST text pattern is HTTP-upload metadata rather than proof
of a WhatsApp session token.

The [move inventory](moves.json) records original rules, defaults and consumer
rewrites. `uv run docs/taxonomy-audit/taxonomy/token-neighborhood/check-moves.py`
checks all 16 moves and the sizes of their destination directories. Five
explicit legs of a broader HTTP collector were removed after the moves because
an existing parent-directory leg already covers them. The rest of the token
and adjacent categories still need individual review.

One hostile fixture exposed an encoded Chromium extension-storage target that
the old generic archive rule had obscured. A new path observation recognizes
the decimal sequence for `Local Extension Settings` XORed with `0xaa`, and a
hostile application-state composite combines it with the concealed bot upload
profile. The path observation is deliberately specific to that encoding; it
is not a general XOR decoder.
The moved Telegram/app-data archive rules no longer carry the browser-cookie
technique annotation, which their session-store or general app-data targets do
not establish. A focused static check matched the encoded-path sample and did
not match an otherwise identical control with the encoded path changed.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,883 notable and
1,336 baseline fixtures.
