# Go endpoint review — 2026-11-04

Review in progress. The initial standalone scan covered 35 Go sources.

`3e43fc5bea60` reads Google Cloud credentials and an SSH private key, archives
them in memory, and posts the archive to a remote endpoint with an image MIME
type. Two new hostile traits describe credential collection and archive
upload; removing the POST from a control prevents both matches.

`d0eaf6d3fb14` invokes hidden PowerShell to download a staged file, decode it
with certutil, and run it with execution-policy bypass. Its endpoint is
`example.com` and the file labels itself synthetic, but the executable stager
implementation is dedicated attack code. Existing hostile traits identify the
staging and policy-bypass behavior.

`d289a4fdd318` is an operational Sliver client command that tasks an active
beacon to download a remote file and can decode and save the result as loot.
Two new hostile traits describe remote tasking and loot handling; removing the
RPC call from a control prevents both matches.

All three had fresh local slow scans, passed repository validation, and were
recorded bad with hash-verified snapshots.

`286a6cb2aeb4` is a standalone WinINet HTTP client helper. Its optional
`InsecureSkipVerify` branch sets Windows security flags; it has no standalone
beacon or malicious payload. A bare `SecuritySetMask` identifier had incorrectly
been called a setter and marked suspicious in addition to the real conditional
bypass. The bare reference is now notable, leaving one justified warning for
the actual configurable TLS bypass. Validation passed and Hopper confirmed good.

`4ea26c84b4cf` is a test program that invokes a golden-ticket forge with a
synthetic key and domain and validates a forged `krbtgt` ticket. The forge
implementation is a separate dependency; the test itself exercises the
attack operation. Two hostile traits identify the invocation and ticket
validation; removing the forge invocation from a control prevents both. The
fresh scan and validation passed, and Hopper recorded bad with a hash-verified
snapshot.

`5c11933b6746` implements packet handlers for remote file listing, transfer,
renaming, and deletion. The file contains no proof of covert deployment or
malicious use; it is dual-use remote file-management code. A new suspicious
trait describes the actual transfer and deletion handlers. `fa8499d0e665` is
an anti-analysis helper that checks mouse activity and VM artifacts but has no
standalone malicious payload; it is good with one new warning. Controls with
the relevant operation removed do not match. Validation passed, Hopper
recorded both labels, and the dual-use snapshot was hash-verified.

Twenty-four other standalone files are generated API/data models, ordinary
application helpers, documentation/link tests, synthetic tests with mocked
memory/executors, a generic clipboard read, and beacon-selection or database
support code. Their own implementations do not contain a standalone exploit
or malicious payload. Fresh scans have no severe findings, validation passed,
and Hopper confirmed good.

Three further helpers are good with one warning each: `2b26f5442b87`
reassembles supplied chunks and loads a native plugin; `bccebd8f3bd0` watches
and returns clipboard text changes; and `798c5664d2c7` combines CPUID and
timing signals to report likely virtualization. The plugin source does not
establish where the chunks originate, the clipboard watcher does not transmit
them, and the hypervisor helper contains no payload. New traits describe those
capabilities; controls with their key operations removed do not match.
Validation passed and Hopper confirmed all three labels.

`2011b0399d2d` is a TSPkg decoder unit test. It builds synthetic memory with a
known test password and calls a decoder supplied by the surrounding project;
it does not read a real process or dump and contains no standalone credential
extraction implementation. Two initially drafted hostile matches for the test
were removed after this closer review. Its fresh scan is clean, validation
passed, and Hopper confirmed good.

`63ae88d832a7` contains general SafeDep Go utilities and
`4466f10bbbe2` is Algernon web-server source. Their source contents and
executable exploit indicators were reviewed; fresh scans have no severe traits,
validation passed, and Hopper confirmed good. The previously unknown utility
archive was hash-verified and moved to the good pool.

`9e95d59c0d82` is Algernon 1.17.6 web-server source. The reviewed source and
fresh scan show no executable exploit or severe finding; validation passed and
Hopper confirmed good.

`ce89cfd3bbf7` is a CRI-O source RPM. Its Makefile contains an opt-in build
step that pipes a downloaded golangci-lint installer to a shell; this is one
justified warning. The fresh archive scan and validation passed, and Hopper
confirmed good.

`eb67136d0537` is Atmos infrastructure tooling source. CVE references in the
reviewed files are documentation and synthetic security-report test data,
not executable exploit implementations. The fresh scan has no severe traits
(the scanner process returned 1 despite producing a complete report),
validation passed, and Hopper confirmed good.

Go total: 35 good, 4 bad, 1 dual-use.
