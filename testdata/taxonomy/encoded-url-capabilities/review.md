The reviewed encoded-url-loader.sh is a 285-byte, three-line zsh fixture.
Its Base64 literal decodes only to https://delivery.example.invalid/bootstrap.
The first curl response is piped to zsh; decoded URL bytes are not shell source.
The second curl saves /tmp/.stage.part, then conditional mv, xattr -c, chmod +x
and /tmp/.stage invocation follow. A failed download short-circuits that chain.
Both endpoints use RFC 2606 .invalid placeholders. There is no embedded payload,
credential access, persistence, or operator request surface. Judgment: BENIGN.

Moved curl-to-zsh observation from dropper delivery to shell pipeline; moved
attribute-clear/chmod-or-relative-launch sequence from Gatekeeper objectives
into xattr. Matchers and scopes preserved, criticality corrected to notable.
The sequence proves neither quarantine presence nor a launch after chmod.
Exact consumers and ancestor delivery selectors preserve their prior member set.
No Gatekeeper ancestor selectors reference the removed sequence. The remaining
Base64 pipeline observation is suspicious encoding, not payload execution.
Added parsed OpenSSL Base64 decoding observation (notable); its negative control
uses encoding instead. Positive and negative controls cover both relocated
matchers. No new leaf directories, exceptions, or sample-name gates were added.

Controls were replayed from scratch paths to avoid the existing is-test harness
exclusion on curl-pipe-zsh; all three positives and all three negatives passed.
Run check.py with --cleave and --scratch to reproduce. The moved curl atom drops
its illegal objective-tier suppressor; all other exclusions remain unchanged.
A compatible local debug engine was required because installed/release binaries
lack the checkout's YAML type support. RUST_LOG=error suppresses only that
engine's debug-build advisory; rule validation diagnostics remain enabled.

Full JSON additionally exposed hidden-stage and ClickFix hostile composites,
a Gatekeeper suspicious composite, an encoded-destination suspicious composite,
and a generic xattr argv atom in dylib hijacking. All five were relocated and
renamed to neutral capability homes, with accurate co-occurrence descriptions.
Removed unsupported attack mappings. The ClickFix chain is scoped to macOS,
where its xattr mechanism exists. Its conditions establish no clipboard lure.
The encoded destination describes the URL/response relationship, not evaluation
of the URL itself. The positive fixture preserves every reviewed operation;
the negative uses no shell pipe, Base64 encoding, and attribute listing.

Final full JSON: zero hostile, one suspicious (Base64 literal piped onward).
All eight corrected capability IDs match the original sample. Eight positive
and eight negative assertions passed through check.py. zsh syntax validation
passed; hash agrees with the submitted SHA-256. No sample code was executed.
