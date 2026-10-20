# Blogger and decimal corpus triage

All three supplied artifacts are **BENIGN**. Verdicts follow content and
execution-path review, independently of collection labels and scanner scores.

| SHA-256 prefix | Identification | Evidence |
|---|---|---|
| bc7eff31e90f | Turkish Blogger article using ThemeXpose's free Ares template | Blog widgets, ordinary advertising/social integration and template attribution enforcement |
| a2c83c99f55a | IBM General Decimal Arithmetic 2.59, quiet-copy vectors | All 43 operation rows and six directives are arithmetic fixture data |
| a1a1b9814f20 | IBM General Decimal Arithmetic 2.59, decDouble logical-AND vectors | All 287 operation rows and seven directives are arithmetic fixture data |

## Content and execution review

Both decimal files are identical to CPython v3.2's copies after CRLF/LF
normalization. Every non-comment line is a context directive or a test case
with an expected result. `copy` preserves decimal signs, exponents and NaN
payloads; `and` checks digitwise logical arithmetic and invalid operands.
Neither denotes a shell command or has an execution path, encoded payload,
network operation or dependency. The old documentation URL redirects to IBM's
homepage. The maintainer's current corpus has the same rows and context
settings; only version and attribution text changed.

Provenance checks fetched these sources without executing them:

- https://raw.githubusercontent.com/python/cpython/v3.2/Lib/test/decimaltestdata/copy.decTest
- https://raw.githubusercontent.com/python/cpython/v3.2/Lib/test/decimaltestdata/ddAnd.decTest
- https://speleotrove.com/decimal/dectest.html
- https://speleotrove.com/decimal/dectest.zip

The HTML contains 43 script elements. Conditional IE compatibility scripts,
inline handlers, the form, iframe and external resource URLs were reviewed
as well. The form performs blog search; the iframe hosts Blogger comments.
The Packer wrapper was unpacked by intercepting its `eval` argument in an
isolated QuickJS context. It produces a post-excerpt renderer, with a malformed
trailing closure that would cause a syntax error in that evaluated text. Its
`String.fromCharCode` builds dictionary token names, not shellcode.

Two hexadecimal string tables were decoded and substituted at every indexed
reference. One implements a slideshow of feed titles, links and thumbnails.
Its `window.onload` handler finds the template credit anchor `mycontent`, sets
its link/text to ThemeXpose and redirects to the designer's Blogspot address
only if that anchor is absent. The supplied page contains the anchor. The
other table implements jQuery's scrolling news ticker. Neither hides a payload
or exports private data. The redirect is consistent with attribution
preservation in the explicitly free template.

The remaining inline code implements responsive navigation, related-post
thumbnails, tab selection, image resizing, social sharing, comment widgets,
ad initialization and a back-to-top control. FlexSlider's keyboard callbacks
map arrow keys to slide movement; they do not record input. The two repeated
FlexSlider bodies match the published 2.2.2 minified asset after whitespace
normalization. The external jQuery 1.7.1 bytes exactly match code.jquery.com.
The feed request is `$.ajax({url: .../feeds/posts/default..., type: 'get',
dataType: 'jsonp', success: ...})`; its callback renders public post links and
rotates them on a timer.

All directly loaded script and stylesheet URLs were fetched, including the
Blogger widget/comment/lightbox assets, Google-hosted jQuery, Facebook SDK
loader and its full SDK, AdSense, fonts, and JSONP feeds. The decoded designer
redirect and fallback-image URL were also followed. Available contents showed
normal platform/library functionality rather than an attack. The obsolete
Googlecode HTML5 shiv and original neyci.com image returned 404; the fallback
Google Sites image now redirects to Google sign-in. These current responses
cannot establish what historical remote responses contained.

The HTML's obfuscation, evaluated source and conditional redirect plausibly
explain a heuristic malware label; the single accurate suspicious Packer
finding remains. For the decimal files, corpus/package label inheritance or
collection mislabeling is plausible. The original source's precise reason is
unknown; the files themselves contain no hostile behavior.

## Detection changes and placement review

- Require a script element for the Google-brand script-host observation,
  rather than matching any `src` attribute. Exclude genuine Google user-content
  hosts per match, preserve detection when real and imitated hosts coexist,
  and avoid excluding `fakegooglecode.com` as though it were `googlecode.com`.
- Add a notable observation for HTML jQuery AJAX calls explicitly specifying
  GET, including variable URLs. POST and commented-out calls are controls.
- Move Turkish content classification out of `micro-behaviors/data/language`.
  Function definitions implementing language classifiers remain capabilities.

The destination natural-language leaf already held 100 rules. The complete
104-rule population was reviewed by two placement passes: first classify the
matched resource (writing-system characters versus named lexical content),
then check the nearest alternative against the required evidence. This is a
semantic partition, not a split by implementation language or rule form.
`script` receives 12 rules; `vocabulary` receives 92. Character-only and
word-only controls distinguish the leaves; a combined document matches both.
Polish diacritics remain character evidence and the Polish vocabulary
composite explicitly references them across the boundary.

[natural-id-map.json](natural-id-map.json) accounts for every incoming rule.
All matchers, effective file/platform scope, criticalities, thresholds and
exclusions were compared before/after after resolving defaults and mapping
references: they are preserved. The Turkish description now describes probable
content rather than a runtime detector. Exact consumers and live control
expectations were updated. No live ancestor directory selectors were found;
the `metadata/lang/natural` parent continues to include both descendants.
Historical scan reports and migration records retain their original IDs.

Verification: all 16 positive/near-miss controls passed, and migrated findings
were unchanged after ID translation on all 12 original controls. Run
`python3 testdata/taxonomy/blogger-decimal-triage/check.py` to repeat the focused
checks. Final target scans retain no hostile findings, one suspicious Packer
finding on the HTML, and no suspicious findings on the decimal fixtures.
