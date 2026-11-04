# Go mislabeled-bad review — 2026-11-03

The 39 artifacts include individual Go source files and three source archives. Both scanners were run with caching disabled, and the files were inspected without execution.

`1f81857403ca` remains bad: its controller configures eBPF self-hiding, an HTTP command channel, and target-file overrides. The new `ebpf-hidden-rootkit-control-options` finding combines these facts; both scanners report it as hostile, and changing the self-hiding evidence clears the finding. Full validation passed.

The following 33 individual files are good: `05244064a0ce`, `88bf443f152f`, `9870bd8bc28e`, `eaf5484c37af`, `1487b3bcb74f`, `3d493855102f`, `618e85d379c3`, `1a5ce8987839`, `574fca1785b2`, `6833f0dafeef`, `b970c6a0244a`, `21c0d9aefd1a`, `2b71dd212b3f`, `21f07be738e0`, `4777ce5c0a31`, `620d30ff2750`, `4050d5d04339`, `e30df24c74bd`, `ed7a8d8ddc5f`, `978ade53580b`, `a3f37d4aaf86`, `8f691b0ee8ca`, `659d77d37d62`, `b716b02563ea`, `a308f02c97dc`, `6f78f82d7a12`, `180aa88bc889`, `d6f50d3734a5`, `7876481b55d7`, `65ca1e5301b0`, `a188463567d7`, `b3bcbcbead9d`, and `e1ee8bfe9881`. They are standalone vendored libraries, tests, generated declarations, schemas, or ordinary application startup code. Neither scanner reported hostile findings, and a Cleave batch check found no suspicious findings. Hopper confirmed all 33 as good.

`cd6d0f78ab14` is good: it contains cloud-image test infrastructure. Its one suspicious finding reflects an actual test setup command that disables package-signature checks; that risky setup choice does not establish malicious intent. `01b74913bbcb` and `ff8faa8f3749` are dual-use proxy and network file-server source files. `3c7cb7d45fdb` is the dual-use security-platform archive reviewed in the GitHub Actions queue. Hopper stores dual-use items in its excluded inconclusive pool.

`bf1986ecd37d` remains bad. Its shared Go source files match the official Go 1.23.4 source archive byte for byte, but additional files implement a command agent with shell, browser-cookie, and credential-collection dispatch. A new agent finding and two archive-level Chromium collection findings are hostile in both scanners on the original archive and an extracted representative archive; removing the agent clears them. An unrelated standard-library parser test was incorrectly flagged as a network desynchronization probe. A targeted in-memory rejection-test context now clears that finding while an active probe control remains hostile. Full validation passed.

The review yielded 2 bad, 34 good, and 3 dual-use.
