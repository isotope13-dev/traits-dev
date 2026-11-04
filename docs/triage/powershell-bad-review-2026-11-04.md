# PowerShell mislabeled-bad review — 2026-11-04

Reviewed 40 snapshot entries with both scanners and source or archive inspection. Hopper confirmed 9 bad, 16 good, 6 dual-use and 9 inconclusive; dual-use and inconclusive entries use its purgatory target. Both scanners already identify `af3218ccbb15` sending screenshot attachments over SMTP. New findings identify `70105d5c08aa` copying SAM or NTDS and SYSTEM files from a WMI-created shadow copy, `70f0161252fd` constructing and sending an SMB kernel exploit, `c1235f0cefde` repeatedly copying desktop files to a remote WebDAV share, and `84e9293c6685` downloading and invoking an obfuscated managed assembly. Controls removing the respective copy, packet send or entry-point behavior clear the new findings.

`8fd4747164c2` and `e46a02fae103` contain ASCII batch content after a misleading UTF-16 marker. Their commands attempt to stage downloaded code and startup persistence; one also selects payloads after antivirus checks. Execution depends on how the malformed prefix is handled. Existing byte-capable matchers now detect the combined behavior in both scanners. Controls changing the antivirus checks or startup target clear the corresponding finding.

The Habitat installer in `c208eb2378cf` temporarily moves an existing executable to a hidden `-orig` backup and restores it on failure. A new backup-and-restore context removes the mistaken persistence finding from both scripts and the archive. `8e28054cc089` creates a caller-selected shared `svchost` service; that behavior is now described as service creation and rated suspicious rather than automatically described as a hostile hijack.

General-purpose service, file-server, miner and testing utilities are dual-use. Standalone remote-HTML launch commands, a launcher for an absent executable, and large archives with unresolved contents remain inconclusive. Ordinary Microsoft configuration modules, local audit utilities and inert text are good.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. `git diff --check` passed. No engine features were added.
