# Go module archive mislabeled-bad review — 2026-11-03

The 20 archives were scanned in Cleave and Atom and inspected without executing their contents.

Sixteen remain bad: `99ff3ad7c7db`, `bf5fbb81d73c`, `765e0c5487dc`, `ab0365ced924`, `8443f56f8ac2`, `51cf70d4bc34`, `329ac9653849`, `16bb319f0935`, `4b16f7bc8d8f`, `7649d2ca761f`, `2cecb345cd21`, `2310fe6c0218`, `2754a334abf7`, `b628c0545f27`, `729e6ab0d1ad`, and `d9485a1d5296`. Their implemented behavior includes unbounded disk filling, hidden startup persistence, encoded command execution, DNS transmission of credential files, reverse shells, root exploits, obfuscated loaders, and post-exploitation agents. Existing hostile findings in both scanners cover the actual implementations. The credential-sending proof of concept remains bad.

The Graphalgo-associated module rule previously called individual files hostile solely for declaring or importing a module host. Its identity facts are now notable and its aggregate project context suspicious; the infected archives still produce multiple hostile findings for their encrypted command agents and payload execution in both scanners. An extracted ordinary library file no longer receives a hostile finding from the module host alone.

`e240b40ba6b6` and `b1acae233551` are good. The first archive's 802 files match the official gRPC-Go 1.57.0 module byte for byte; the second contains a general web framework and has no hostile or suspicious static findings. `37de998f2e5e` is dual-use network-overlay software and is stored in Hopper's excluded inconclusive pool. Its one suspicious credential/HTTP finding was reviewed as a weak association between local process configuration and a separate transaction request.

`b042a027789b` is inconclusive: it is an authenticated API client that sends its own service key to the service endpoint, but the service's identity could not be independently established. The previous hostile finding treated ordinary bearer authentication as proven credential theft; it is now suspicious and the host reference is notable. Both scanners report no hostile finding for this archive.

Full validation passed. The review yielded 16 bad, 2 good, 1 dual-use, and 1 inconclusive.
