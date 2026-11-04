# Go module manifest mislabeled-bad review — 2026-11-03

Nine standalone `go.mod` files (`22fee76a78f7`, `71d8ed3f0c43`, `12b5a6d2485a`, `24a8d00f73ae`, `2804165e05de`, `8c4f21b432e2`, `1e1a6309b600`, `4ce2a653ed60`, and `2e8b320d7d16`) are good. They declare module names and dependencies but contain no implementation. Some describe projects that could be malicious, but the standalone declarations do not perform those behaviors.

Manifest-only identity and dependency rules were lowered from hostile to notable or suspicious, and their descriptions now identify declared dependencies rather than assert execution. Both scanners report no hostile findings and at most one suspicious finding per manifest. Representative actual eBPF-rootkit and browser-collecting command-agent code still produces hostile findings in both scanners. Full validation passed.

`9b408365cc84` is a dual-use proxy source archive. Both scanners reported no hostile findings; it is stored in Hopper's excluded inconclusive pool because Hopper has no dual-use target. The review yielded 9 good and 1 dual-use.
