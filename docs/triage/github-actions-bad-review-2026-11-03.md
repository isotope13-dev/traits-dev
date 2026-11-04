# GitHub Actions mislabeled-bad review — 2026-11-03

The snapshot contains standalone workflows and source archives. Both scanners are run with caching disabled; archives and decoded configuration are inspected without executing their contents.

`519dcc934aa5` remains bad: its workflow posts a CI secret in two request-body forms. The existing hostile finding remains in both scanners, even though the demonstration endpoint is non-routable. `2e8930ca70c4` remains bad: its security-testing archive contains executable reverse-shell examples and a workflow that uploads environment and SSH-key files. Research and test-fixture provenance does not neutralize those implementations. `645c4395d0cf` remains bad: it contains the Sliver post-exploitation framework and executable shellcode, with multiple existing hostile findings.

`7d3ac7739500` remains bad. Its workflow starts a hidden stage with an encoded configuration naming the home directory as an inventory root and supplying a remote control path. The new `ci-encoded-hidden-home-inventory-control` combines those facts without an engine decoder; both scanners flag it as hostile, and changing the encoded inventory field clears the finding. The configuration describes intended behavior; the external stage implementation was not present in this standalone workflow.

`e22fd5a2dc7b` is inconclusive: it fetches and runs a hidden executable without TLS verification, but the payload URL returned 404. Three generic hidden-download rules were lowered from hostile to suspicious, and the corresponding fixture moved to the suspicious pool. Atom's model still scored the workflow highly despite the absence of a hostile static finding.

`81b52bb9c27c` is dual-use: its archive contains security-assessment skills, and the only hostile finding came from a risk table quoting a prompt-injection example. The documentation context now suppresses that finding for the table; adding an actual system-prompt disclosure instruction restores it. Both scanners report no hostile findings on the archive after the change, although Atom's model remains high. Hopper stores the dual-use item in its excluded inconclusive pool.

Full validation passed after these changes.

`69b805ec0a7a` remains bad because its archive includes an executable multi-model jailbreak tool; the existing hostile findings identify that tool. A separate false positive in its ordinary server-start function was removed by requiring the detached subprocess finding to include an inline Python interpreter and discarded output. A representative malicious subprocess still matches, and the server-start function clears in both scanners. Full validation passed.

`92edc082cf7f` is good: it contains a development framework package, with no hostile or suspicious findings from the scanners and no install hook in its package manifest.

`a08e1c6eb4cf`, `74e168277894`, `bdb1825e7b43`, and `c7ce6394515f` are good. They contain the Axios HTTP library, a schema generator, and two database-replication source snapshots. Both scanners reported no hostile findings; a separate check found no suspicious static findings on these archives. The schema generator's install hook prints a sponsorship message.

`09858e9cef42` is a dual-use security-analysis skill collection, stored in Hopper's excluded inconclusive pool. Its actual SHA differs from the snapshot directory prefix. `ba1e8e019b31` is inconclusive because its source package includes a manually invoked remote installer and the downloaded content was not established. `44ccee9b3b9c` is inconclusive after review of its large administration-script collection: it contains a workflow that interpolates a pull-request title into a shell command, and the full behavior of the many installation scripts remains unverified.

`e51abefb4748` is good: it contains database source code rather than an attack implementation. Its title-validation workflow has one suspicious finding because it interpolates a pull-request title into a shell command; that identifies a potentially vulnerable workflow, not malicious intent by itself.

`866d31461f22` is good: it is a team-management application source archive. Its package lifecycle and contents were inspected, and neither scanner reported hostile or suspicious findings.

`23a3db3e6028` remains bad: its security scanner constructs and sends SQL injection probes including a `DROP TABLE` statement. The new `sql-destructive-injection-probe` finding is hostile in both scanners on the source and archive; replacing that statement with a non-destructive query clears the finding. A separate example in the archive is a prompt-injection test fixture.

`50d3a1941d88`, `ca4dd0641078`, `935b2a2367c9`, `063b8fa5fcc5`, and `03aaf3a07fac` are good source or extension archives for workflow automation, graphics editing, factory data, translation, and GIS. The GIS manual linked to a researcher whose surname is Chase; the brand-path atom was lowered to notable because a name in an unrelated URL does not itself establish bank impersonation. The separate hostile phishing combination still matches a bank-branded suspension lure, and full validation passed.

`e2d035144c3c`, `3c7cb7d45fdb`, and `93d7bef1e6dd` are dual-use security-analysis and training collections, stored in Hopper's excluded inconclusive pool. Their suspicious evidence includes security examples, a potentially vulnerable workflow, and a test configuration disabling TLS verification. One Playwright guide only reads cookies from its own test session; the generic cookie-read primitive is now notable, while a separate session-theft control remains hostile in both scanners.

The 26 reviewed artifacts comprise 6 bad, 12 good, 5 dual-use, and 3 inconclusive. Full validation passed after the final trait changes.
