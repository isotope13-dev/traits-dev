# PKG-INFO mislabeled-bad review — 2026-11-04

Reviewed 40 snapshot entries with both scanners and package inspection. Hopper confirmed 10 bad, 7 good, 7 dual-use and 16 inconclusive; dual-use and inconclusive entries use its purgatory target. `72cde9a748d9`, `509937055319` and `f879dd98feb1` execute package setup code that collects host and user details and sends JSON to a remote callback. A new rule identifies the combined setup, collection, public-IP lookup and outbound JSON behavior. Both scanners flag the first two extracted scripts and containing archives; changing hostname collection to a constant clears the control. The third archive is also flagged.

`1cb61415b362` obtains a wallet private-key environment value and sends it in a JSON request. Several encrypted dataset archives were inspected using their standard `infected` password: some send hostname, username and working-directory information through DNS, while others only perform a bare canary lookup. The `a63c491ef95f` security scanner actively tests XML file disclosure and entity-expansion denial of service; the package is bad because it contains active exploit probes, and its probe finding is meaningful. Empty proof-of-concept wheels and metadata-only packages do not themselves send host findings.

The inconclusive group consists of larger packages or executables whose complete behavior was not established. Atom timed out on both `mcp_feedback_pro` wheel versions, although Cleave completed its scans; those two remain inconclusive.

The most recent full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. No engine features were added.
