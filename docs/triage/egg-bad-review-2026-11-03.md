# Egg mislabeled-bad review — 2026-11-03

The single snapshot item, `510c3ff87393`, is an Alpine package containing a Python egg. Its `pip3` console entry point invokes code that gathers the hostname, working directory, local addresses, and public address, hex-encodes those facts into DNS labels, and resolves them under a collaborator domain. A claim that it is a security test does not change the implemented host-data transmission; it remains bad.

Both Cleave and Atom report the existing `encoded-label-dns-host-exfil` finding as hostile on the package, its embedded egg, and the Python implementation. The egg was also extracted without execution and scanned directly; Atom's model probability was approximately 99.9%. The finding describes the behavior clearly, so no trait change was needed. Full validation passed before the classification was recorded.
