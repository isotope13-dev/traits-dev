# CPAN mislabeled-bad review

All five archives were inspected and scanned with Cleave and Atom, with reference following disabled. Each contains an environment-gated callable payload; the gate does not remove the hostile capability. Existing traits identify each behavior.

- `b2c1b5cd614312e0ff5067ce8af4a86c9c382404b1b9891f5112a2723da45f8b` — **bad** — Reads Chrome and Safari credential and cookie files and posts their contents to a remote relay. Both scanners report hostile findings.
- `78ad6d6605f751789bc1187566ca35e59eb832d362a14c7755459b0ba3a37e4d` — **bad** — Reads NuGet and npm authentication files, posts their contents remotely, and creates a scheduled task running an encoded PowerShell downloader. Both scanners report hostile findings.
- `b9694d00267e0816bf8ca06f2601d63624b11ce2d397cbe106c220b376a83515` — **bad** — Reads AWS credentials and .netrc, encodes the contents as hex and sends chunks via DNS lookups to an external domain. Both scanners report hostile findings.
- `344a8ad774a72c3b983d0fa92eadcce3c7d582e6eaab1e80f5fd06bb7649d4de` — **bad** — Decodes an XOR-obfuscated command and runs mshta against a remote HTA URL. Both scanners report hostile findings.
- `bef0884251b119e0ae317d9ccab0a9764c88b7365b3f1fefa173cf220779a96c` — **bad** — Decodes an alleged terminal digest and executes an interactive TCP reverse shell. Both scanners report hostile findings.
