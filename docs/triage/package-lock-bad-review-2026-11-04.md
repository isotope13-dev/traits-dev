# Package-lock mislabeled-bad review — 2026-11-04

Reviewed all eight snapshot entries with Cleave and Atom, including their enclosing archives: six are bad and two are good. Hopper confirmed each decision.

`e0822acc4a52` and `b3fe727d42c9` contain active obfuscated blockchain-resolved JavaScript loaders. `f25ca4da35e2` disables `Array.push` and freezes the prototype when imported. `f64328f276d8` includes request-driven PHP webshells in an Android control-panel archive. Existing hostile findings identify these behaviors in both scanners.

The large skills collection at snapshot directory `1e62ce4be9c1` has actual SHA-256 prefix `da7e33cfeac3`. Its LinkedIn application skill directs users to an encoded shell downloader and a password-protected executable behind an installer pretext; both scanners retain multiple hostile findings. Other matches in the same collection were inert strings submitted to security validators, or an ordinary coding-agent workflow. Rules were narrowed to avoid treating those examples as executed reverse shells, cloud-metadata exfiltration or inherently hostile pushes. Targeted scans cleared the inert examples while preserving the malicious skill findings.

`d51c4e92bde0` is hostile because its Android bootstrap passes the serialized IMAP account configuration to a logger that sends its encoded message to a hard-coded remote HTTP endpoint. The configuration can contain the IMAP password, so this path can disclose credentials; the message is truncated to 800 characters. The new finding binds the logger and its call site, and both scanners detect the source and enclosing package. A control that logs only the host clears in both scanners.

`857e2fc60849` is a standalone lockfile containing a suspicious downloader command as metadata, not an executable package manifest; it retains one suspicious finding. `9f3f19c3a151` is a source package whose lockfile attack strings are inert inputs to its security scanner tests. Both were classified good.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks.
