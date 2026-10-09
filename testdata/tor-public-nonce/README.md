Tor public-nonce scalar recovery fixtures

Source: https://thehackernews.com/2026/10/gobalance-flaw-lets-attackers-hijack.html
Technical analysis: https://www.slcyber.io/research/leaking-the-keys-to-the-kingdom-how-a-single-slip-handed-over-a-darknet-empire
Go helper source: https://github.com/kolmteistov/gobalance-patch/blob/main/gobalance-patched/poc/vulnerable/attack_helpers.go

The Go fixture is copied from the linked research PoC and requires its vulnerable snapshot package to build. The Python fixture translates its scalar recovery and signature construction. Its math was checked using locally generated signing material: recover the scalar from a signature, then verify a forged future signature using PyNaCl. It accepts already-extracted certificate bytes and a public blinding nonce; it does not fetch descriptors.

Both full fixtures must emit the suspicious public-prefix derivation and scalar-recovery findings. Defensive research is a legitimate use, so these are not hostile findings. Normal signing fixtures retain a secret prefix; unrelated arithmetic omits the Tor domain separator. A prefix-only fixture must emit only the prefix finding, not scalar recovery. cases.json records these expectations.

Coverage is for direct Go/Python expressions. Renamed local recovery helpers and scalar variables do not affect the rules. The stable Tor protocol domain separator is required, not a service address, CVE, attacker name or filename. The recovery rule reports co-occurrence within 4096 bytes, not executed data flow. Precomputed prefixes and other language/API spellings are outside this coverage.
