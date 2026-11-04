# GZ mislabeled-bad review — 2026-11-03

Reviewed 28 snapshot entries with Cleave and Atom, manually decompressing the GZIP payloads without executing them. Nine are bad: `73219e2018a0`, `cd702e56733e`, `ebc3c316e749`, `cfc9c4470736`, `4314856e6f20`, `76feaa01eab3`, `b93d0b9aba7f`, `9227ca11ea56`, and `ca28915aeea2`.

`73219e2018a0` contains a hidden PowerShell downloader which reconstructs commands from interleaved characters and invokes them. `cd702e56733e` contains an auto-open Word macro with repeated error suppression, obfuscated strings, and hidden object-based process creation. New composites detect each extracted script in both scanners; removing the invocation or window-hiding behavior clears the corresponding control. The original GZIP PowerShell file has no extracted child in the scanner, and the OLE document's compressed VBA is not exposed as script to these rules, so neither outer sample receives the new hostile finding. No engine feature was added to overcome those limitations.

The seven remaining bad entries contain managed loaders. Static IL inspection confirmed that `76feaa01eab3` and `9227ca11ea56` extract RGB bytes from a bitmap and pass them to `Assembly.Load`; a new composite combines bitmap, assembly, late-binding, and entropy facts and matches both scanners. `b93d0b9aba7f` and `cfc9c4470736` decode resource data and invoke a loaded assembly; a second composite combines Base64, reversal, resource, reflection, and entropy facts and matches both scanners, including their GZIP wrappers. The other three already had hostile loader findings. An unrelated managed program did not match either new composite.

Six entries are good: `390bb447dc11` and `e239a3aeaac5` are manual pages, `78a3957e42bc` is a word list, `74b1f29b0be3` is CSS, and `5ba6c2308ba6` and `21619e94681d` are OpenTelemetry Lambda and VMware operator source archives. The latter has one reviewed suspicious archive-path association.

Thirteen PE payloads are inconclusive: `9ec589ea0e15`, `53954649f47d`, `a924e3fdcad5`, `cc33256da14f`, `e95dadeacc5f`, `e9cfd1c6ec24`, `86b9db246622`, `9f7df11c17a8`, `575f4e8498c6`, `557f14b9287d`, `6b60dd70bf55`, `97db3472cd7c`, and `0fac7b9a59c7`. They include VB6 and managed executables with embedded resources, reflection, or substantial obfuscation, but the inspected metadata and static method references do not establish each embedded payload's behavior. These are excluded from binary training pending deeper reverse engineering.

Full validation passed. Hopper recorded 9 bad, 6 good, and 13 inconclusive.
