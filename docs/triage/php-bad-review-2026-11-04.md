# PHP mislabeled-bad review — 2026-11-04

Reviewed 40 snapshot entries with both scanners and source or archive inspection. Hopper confirmed 8 bad, 25 good and 7 inconclusive; inconclusive entries use its purgatory target.

`723e533446e3` implements DNS tasking that encodes task status in DNS queries and includes wallet-collection and exfiltration tasks. `66d03f153789` contains a report backend that links host reports to bots and stores wallet and credential data. Both scanners now identify these behaviors, including the containing report-backend archive; controls removing the relevant task or bot linkage clear the findings.

`647ddb709317` generates disguised WordPress plugins that write decoded request data and mark themselves immutable. `cf2e5a1a6979` is a fixed-password uploader that copies uploads to a client-supplied filename. Both scanners identify each sample and clear altered controls. `0d3ee83adc9e` routes request-supplied code through XSLT and PHP `assert`; the detection identifies the attempted behavior, whose execution depends on PHP version and configuration. `eee61c753d05` reconstructs a function that evaluates code from request, cookie or header input; a combined rule detects its dense indexed string construction and computed calls. The rule identifies this form of obfuscation and does not establish the reconstructed payload's semantics on its own.

The other bad entries include a large web shell and an SSI command-relay tool. Good entries are ordinary library, test, theme and utility code or inert fragments. `b252aaea31c1` conditionally loads an external script while excluding administrators and changes plugin timestamps, but the external script's content was unavailable; it remains inconclusive. Five large application archives and an opaque installer also remain inconclusive because their complete behavior was not established.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. `git diff --check` passed. No engine features were added.
