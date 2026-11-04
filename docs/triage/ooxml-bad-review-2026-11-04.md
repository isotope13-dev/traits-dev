# OOXML mislabeled-bad review — 2026-11-04

Reviewed 40 snapshot entries with Cleave and Atom and inspected document relationships, embedded content and archive members. The decisions are 7 bad, 31 good, 1 dual-use and 1 inconclusive. Hopper confirmed all decisions; its `purgatory` compatibility target records both excluded cases under its inconclusive pool.

`ed2b9e22aef3` and `84674acffba5` contain remote MHTML OLE exploit-delivery relationships already detected by both scanners. `679bbe0c5075` uses the same shape with a scheme-less remote host; the existing relationship fact now recognizes that attempted delivery and a local-target control clears. `c91917ff2cc3` uses an external OLE relationship with a remote `script:` moniker; both scanners now report the combined relationship as hostile, and a reserved example-host control clears. Neither finding asserts that the remote stage was successfully retrieved.

`1039a868e984` contains password-protected malicious PE material identified by existing findings. `8f35dc63cbca` and `c58a61f0717c` contain obfuscated blockchain-resolved JavaScript loaders; the latter also has a concealed editor autorun. Existing hostile findings identify them in both scanners.

`37b3653b6456` is the Strelka security-scanner source archive, classified dual-use. Its Excel 4 test workbook auto-runs a harmless alert, which exposed a false hostile rule. The generic auto-run finding is now suspicious; hostile detections for the reviewed malicious OLE workbooks combine auto-run with BIFF formula-reconstruction or scattered-character dispatch evidence. The scanner archive also contains a 512 MB expanded zero-file fixture and other security-test artifacts, which remain suspicious without establishing a malicious deployment.

`fbe13003a4e3` is inconclusive: its ZIP structures and compressed streams are corrupted, and attempts to recover the local members did not produce readable content. Its source label is insufficient to determine the damaged document's behavior.

The other entries are good, including ordinary documents, spreadsheets, an owner lock file, a benign embedded test spreadsheet and two agent-development source archives. The security-scanner tests in `3c883c36bd9a` pass command strings to a detector as data; they do not execute the embedded host-reporting example. Findings for isolated command text and a unit-test scanner context were adjusted without suppressing active exploit implementations or compound hostile rules. The embedded workbook in `d053d5f0d7f4` only shows a message on open.

Both scanners were checked against the new detections and controls. Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks.
