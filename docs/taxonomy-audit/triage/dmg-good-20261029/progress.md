# DMG good-pool review, 2026-10-29

Status: **in progress**. The pool contained 100 inputs, including one source RPM. Baseline Atomscan reports exist for all 100; baseline scan completion is not a verdict or a substitute for reverse engineering. Primary executable facts were extracted for 84 inputs; the remaining inputs include 10 Apple developer disk images, five encoded-carrier samples reviewed separately, and the source RPM. Do not classify unreviewed inputs as benign based on a clean baseline.

Five encoded-carrier DMGs were confirmed malicious by static recovery of AppleScript credential-stealing and upload behavior. A source-matched Atomscan build with the new Cleave static extractor reports these hostile traits on the original DMGs:

| SHA-256 prefix | Hostile traits | Directories |
| --- | ---: | ---: |
| 7f4582259482 | 17 | 11 |
| a349425af659 | 15 | 9 |
| 564f85ff9dea | 14 | 9 |
| d8af96fa9e58 | 14 | 9 |
| fb6c9a88868e | 22 | 12 |

The extractor is in the sibling Cleave checkout (`src/extractors/macho_hex_scripts.rs`, registered in the Mach-O analyzer). It recovers supported RC4, custom-alphabet Base64 and LCG/XOR inline AppleScript statically. Sample bytes were not executed. Reports, extracted evidence, and the isolated builds are in `.triage-work/dmg-good-20261029/`.

Pending work includes careful review of all remaining binaries and components, particularly TheBrain's managed HTTP/reflection indicators, GeekLink's protected license module, Pinokio's bundled SweetAlert2 regional sabotage and its application reachability, Rancher Desktop's nested archive and scheduled-job evidence, and the Vagrant package archive depth limit. The HTML named-handler variant of the JavaScript context-menu rule still needs coverage. Multiple reports were produced while an unrelated malformed VBScript trait was skipped; they should not be treated as complete current-rule scans.

No classifications have been recorded. `make validate` currently fails on unrelated existing taxonomy problems, including unknown subdirectories, stale file-type allowlist entries, matcher type caps, oversized directories, and PHP regex quality errors. Re-run validation after the shared changes settle, then re-scan with current rules and use `hopper mv` only for completed reviews.

Vagrant: scanning the separately extracted CPIO produced 5,329 member reports with no suspicious or hostile root traits. Its extracted installer scripts create a command symlink and remove older installations. A direct package scan reaches 6,231 entries, but the original DMG scan stops before the gzip payload and installer scripts: the archive analyzer has a default maximum depth of three. Report this coverage gap and review a depth-limit or explicit analysis-gap fix before relying on the original-image result.
