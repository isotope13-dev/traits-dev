# Perl mislabeled-bad review — 2026-11-04

Reviewed all 40 snapshot entries with both scanners and source, archive or decoded-content inspection. Hopper confirmed 29 bad, 4 good, 5 dual-use and 2 inconclusive; dual-use and inconclusive entries use its purgatory target.

`644090e4e617` is a CGI web shell that reads request data and executes a Base64-decoded value. `3e9d948478ad` sends an injected UNION query for user password hashes. Both scanners now flag these active behaviors; controls replacing execution or removing HTTP requests clear the respective findings.

`646656858a13` opens a decoy document while XOR-decoding a large embedded payload, builds Windows API names from character arrays, allocates executable memory and queues an APC. Both scanners now identify the combined behavior; changing the queued API in a control clears the finding. The pattern describes the observed loader rather than proving all possible similarly shaped code is malicious.

`a1904c0aec26` is a uuencoded Perl wrapper; offline decoding reveals an IRC bot with command and flood functions. `541c6b5095c5` generates a uuencoded Perl loader whose decoded program retrieves remote tasks and reports results. Other bad entries include active network exploits, denial-of-service scripts, browser exploits, a web shell and a persistence-and-beacon demonstration. Many legacy scripts and the encoded wrappers still have no hostile finding in the original scanner output; their verdicts follow direct inspection and represent remaining detection gaps.

Three small Wifatch-related files only delete supplied paths, retrieve a local configuration or generate peer seed data; the fourth good file is an ordinary scanner updater. Dual-use entries include a segment scanner, peer update and file-serving components, and general-purpose security scanner components. Their context or filename alone does not prove hostile operation. The CRAN source archive and large Sapling repository archive remain inconclusive because their nested contents were not fully reviewed.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. `git diff --check` passed. No engine features were added.

Policy correction: `644b8f9c9a85` is a dedicated interactive UDP backdoor client and `0ac7265d97fe` implements a Windows hacking kit that opens Telnet and attempts to create administrator accounts; both are bad. The new Telnet/admin composite matches the kit in both scanners, and a port-name mutation clears it. Its account creation uses a literal password expression, so the finding describes capabilities without claiming successful use. Full validation passed after splitting an overlong regex.
