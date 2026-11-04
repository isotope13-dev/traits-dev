# Elixir mislabeled-bad review — 2026-11-03

`7de852a2ee21` remains bad: it connects to a TCP endpoint, executes received commands through a shell, and returns the output. Both scanners report the existing hostile `elixir-gen-tcp-command-dispatch` finding; Atom's model probability was approximately 97.4%.

`2ae90e18f33e` is inconclusive. It downloads an executable without TLS verification to a hidden `.sshd` path and runs it in the background, producing multiple suspicious findings. The payload's behavior could not be checked: its release URL returned HTTP 404. A proposed hostile rule also matched an existing suspicious control for this exact sample, so it was removed rather than treating the unknown payload as proven malicious. Atom's model probability was approximately 92.4%.

Full validation passed, including the existing downloader control. The two reviewed artifacts comprise one bad and one inconclusive.
