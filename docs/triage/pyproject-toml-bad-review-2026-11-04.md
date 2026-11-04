# pyproject.toml mislabeled-bad review — 2026-11-04

Reviewed the single snapshot entry with both scanners and source inspection. Hopper confirmed 1 dual-use entry under its purgatory target.

`66107493675f` is the same Edison Tools source archive reviewed in the PKG-INFO set. Its setup script posts the `EDISON_QUERY` environment value, or a default test string, to a remote query service during package setup. This transmits caller-provided input without an explicit query invocation, but does not automatically collect host findings. The archive has no hostile finding in either scanner.

No trait change was needed. The most recent full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks.
