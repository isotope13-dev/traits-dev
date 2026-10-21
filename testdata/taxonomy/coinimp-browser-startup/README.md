CoinIMP browser startup controls

The reviewed Blogger article loads a remote library, constructs Client.Anonymous
with a 64-hex site key, and immediately calls start() in an inline script. A
mocked constructor records one argument followed by start(), without an event.
The original library host no longer resolves; no historical library bytes were
available. The API and key format match CoinIMP documentation:
https://www.coinimp.com/documentation/reference

The sample verdict is MALICIOUS because the captured news article contains no
mining disclosure or consent control. The two suspicious observations distinguish
automatic startup from a nearby constructor omitting resource options. Neither
claims measured CPU usage, pool communications, injection provenance, or consent
state outside the captured page. No sample key, hostname, hash, or title is used.

The old AuthedMine constructor observation moves to the neutral mining capability
home as coinimp-client-construct. The throttled startup observation is retained
as notable co-occurrence, since throttling and start alone do not prove abuse.
The two named-receiver start matchers are consolidated with their matching sets
preserved, and exact consumers updated. Their ancestor selectors still see one
observation per file. CoinHive controls verify the broadened neutral receiver
vocabulary does not manufacture an unauthorized-mining claim.

At the runtime directory budget, CUDA driver diagnostics were found misplaced:
the unchanged ELF/Linux matcher moves to hardware/gpu. Its exact consumer and
the monero-wallet runtime-directory exclusion both retain it. The latter's existing direct hugepage and worker
exclusions are grouped with CUDA diagnostics in a named exception, preserving
their original no-proximity semantics. No directory split or budget increase occurs.

Blogger's stats token is a URL token, not evidence of a browsing session. The
session matcher now requires a session-named parameter; its exact consumer is
updated, and the existing token matcher retains the generic token observation.

Run python3 testdata/taxonomy/coinimp-browser-startup/check.py from the repository.
