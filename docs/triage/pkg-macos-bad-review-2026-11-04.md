# macOS package mislabeled-bad review — 2026-11-04

Reviewed all 15 snapshot entries with both scanners and installer-content inspection. Hopper confirmed 11 bad and 4 inconclusive. `05ae07783d30` reads a stored password, posts it to a remote address and uses it with `sudo` to run a downloaded script. `2817e26773a1` fetches an executable from a raw IP address, changes permissions and launches it in the background. Other samples contain wallet-stealing, credential-phishing or related infostealer behavior detected by both scanners.

`373007eccde6`, `302ad1644228` and `51d8ab33a7e5` download application payloads that were not available for complete offline review. The second also posts machine identifiers and serial-number information during installation. `74036ce015d2` includes native installer executables whose full behavior remains unresolved. These entries remain inconclusive.

The `51d8ab33a7e5` MacKeeper installer sends a hardware-derived identifier with affiliate installation events. The corresponding tracking finding is now suspicious rather than hostile: those observations establish tracking, but do not on their own establish credential theft or malicious execution. Both scanners agree on the revised severity.

The most recent full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. No engine features were added.
