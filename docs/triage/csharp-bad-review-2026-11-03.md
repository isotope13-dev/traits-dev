# C# snapshot review — 2026-11-03

This review covers all 40 snapshot samples. Labels below were recorded with Hopper after both current scanners and uncached validation. The snapshot paths may retain their prior labels.

- `6d2d1914e4aa56b27c73061fe539ffd3aeba99654cd1e83b5d25c778cfb17d12` — **bad** — Unbounded libc fork loop; direct fork-bomb detection.
- `0ee2a21ba14bbd0cc10f9a1513156b62044693ac613ad41deb817a24360cb223` — **bad** — Prints transformed AMSI-bypass PowerShell; the decoded memory-protection and patch-copy co-occurrence is detected when scanned separately. Automatic recovery of its long encoded payload remains a coverage gap.
- `356e474dcd183e247f41fc0a7f3c075ea23abf6e05f33eec6f543944eebd730a` — **bad** — Discord command passes caller-supplied keystrokes to SendKeys.SendWait.
- `fca48149dfc3a6a91966ceffdf3ac22ae6ef3ca01eedb182e26b4fe5d60e6f3e` — **bad** — Windows batch commands delete wildcard contents of Windows and system directories; destructive commands are active.
- `3d06c6aa5589283ac5ada131c5d66349bbe6a592855381e1fe177af2c677142b` — **good** — 7,933-byte all-zero data file; no executable content.
- `722756d0fe2ea21acbb85e5a88837fc3cdbdbea5f03561429a87a0211dbe0800` — **good** — Discord command methods have empty bodies; this standalone helper implements no behavior.
- `58c463ee96c3f1ca11e6b888d67e8398cf32b6ad5e466d89ee15d36cd8d8d52a` — **inconclusive** — FTP command file retrieves an executable; remote executable content is unavailable for analysis. File contents must not be copied into reports because they include authentication material.

The large ZIP sample `050a6d8d8e9a` was reviewed as a whole. All 9,014
archive files, including four native shared libraries and the WebAssembly
module, match byte for byte the [upstream CCXT commit](https://github.com/ccxt/ccxt/tree/1c792db3b934).
The archive provides exchange-trading code and signing helpers; inspected
process, credential, network, workflow and installer candidates serve those
functions and the build system. Fresh Cleave and Atomscan scans found no
suspicious or hostile traits in 9,184 and 8,087 records respectively; both
reported 5,949 records with flow or embedded-source gaps. Those gaps limit
what the scans alone establish, and the upstream match is provenance evidence,
not proof of benign behavior by itself. The reviewed artifact is **good**;
Hopper moved it from pending to good after uncached validation passed.

- `5467bad6e8a57df646c8d8b39a1587b92658ab0a5a05b1c47f97dd315cf4142d` — **good** — Commented-out plugin interface only.
- `0dbabe84a701e753096bd62febbb70ea39ab1d1d2626c01ab5180b2e3a6fd71c` — **good** — MessagePack type enumeration.
- `d0fe0ec9af1510ce214fa665757056906baf9ed29f2db88874333de3685b1426` — **good** — Windows theme assembly metadata.
- `edbced163866283a4f34f5983de208e8fb8066dd124618bb9fef4a342264d321` — **good** — MessagePack type enumeration.
- `bc6c9a543d7d61df8949f146e876c642f8fcb1d62b560d0bdd92238c277b6b30` — **good** — Compiler-generated delegate declaration.
- `12e1ebaa5eec1df30644b3b565f24790d6bf813bd6262552a2e786e1c4a5453c` — **good** — Entity Framework model migration metadata.
- `9b83eca36c8cd9f47be50d87cce6df41a51e19c25f4d464ae33f57aa36d9bc00` — **good** — Obfuscation context interface and task collection.
- `608348ecd72a3c1c4f43754d19b3f07df332e7193f0bf409735e9ee6fbcbb910` — **good** — Generic plugin metadata and instance construction.
- `119e499eb413ae3a90a9c79818d82f5abcd33a1ec58b6a2360a09ce68522a90f` — **good** — Data container for task identifiers and bytes.
- `0376fa353f8830adc66d3dabe7bffd1437e7477300523e55ba838d64aad71612` — **good** — Empty service interface.
- `e8160558948538065fa05eed5b8051b61120fb7f8e5c16f111c158f3bfbb4b0e` — **good** — MessagePack array container.
- `f4bcf6cd790ea67309c3fc2089569a2ab32dfa2c51277346f15e07247088bf37` — **good** — Byte collection helper.
- `9142a9ebd9a89accbccdaa9cc95e947fe0a542212aced7068b231f78f3c86c3d` — **good** — Data container for task identifiers and bytes.
- `70754832cf8ffd324ad243435b80315ad3c4f0dafc2462e315c17d8f2b012c07` — **good** — Decodes parameters and calls an abstract result handler; no concrete command implementation.
- `7fce4a29fb57bf96adb3cff381a77f3cf731fdf13380271a82b27f75c30cac15` — **good** — Generic zlib decompression wrapper.
- `1e449eb10d45f529c6e1ad330f62b0e56c2703563539ed3bc8e9684f6586b524` — **good** — Import-source enumeration.
- `5345025416f41d7f5cd67f9ad1616edd4fd426132f6e6b890b2b0dc8e51cad33` — **good** — Windows theme assembly metadata.
- `9f223547607ce04f3de8340e57f336ab77c556e58c8c3addb063a0a0ccc72e39` — **good** — Abstract video codec interface.
- `682f05902b82e3e7f62bcd2b8ed4ba2431c0e648180d4754c7421f5646943331` — **good** — Default plugin instance factory.
- `c45befe1f7f1c164384494ec25fd5a582f6d86724db1059b08691f60ac06f519` — **good** — Plugin provider and generic instance factories.
- `1fd939f0280a258db731ebb0496c2e0619cf6a8b7a2420197fff05e20f6c5c0d` — **good** — Windows Forms startup wrapper and unused dynamic symbol declarations; referenced form is not included.
- `0339c4222ea070d747fbcbfe942dfc6c02e21e4836116386ead3f7ea279aa538` — **good** — Avalonia visual control.
- `5aa91c6f6033981201ca28de7f861501ade9a3060682590c869cab24b8c25021` — **good** — Message-box event enumeration.
- `6b9a6ec40640abb4aaaf866b6de1138db0bc37cf6349b45d93f7f97c6227ca0f` — **good** — General RSA certificate-generation helper.
- `8927f7ecd9367a3effd9f321062e327483918eb485592f9fea0f3c88606fa00d` — **good** — Process output accumulation helper.
- `dd4997111e79f4995de4934531ac82323f064cb8a85d9e0bf2ef2de514101727` — **good** — Generic Entity Framework CRUD service.
- `283ddd7a9b7acf34390bc87f58694e4dfbfe7dcb4d60e82ae8921010a6f49515` — **good** — Localization file and translation loader.
- `1e29bd4a762b6f282d5ba11da1ddb6c452177ff34cef8190c9cc2a8db1db5d1f` — **good** — Avalonia acrylic rendering operation.
- `f8f1c3a43a7929803c340675bb9dc8e280fd30f7db33f046a61e4460eec88820` — **good** — Remote-management option declarations and UI color data; no implementation or concrete deployment.
- `649f5520bb0dbff8217e9fdba5a263aeb4ffdf5814a8abd81b2f242735751c0c` — **good** — Generic managed-code symbol analysis for renaming; one accurate suspicious obfuscation finding.
- `37531c0eeaccaa323e6eae3ac94b68285404907dd3453d2094cadae400dcea12` — **bad** — Dedicated command-and-control configuration describes a server and enables a fake startup error; the default host is placeholder-like. The scanner reports the explicit configuration as suspicious, without asserting that this standalone source executes it.
- `c4e7ac23c2015a504fb7190d36221887e0488947e90b3dc4c79e6db8c2d5ea15` — **good** — Generic tool applies a user-provided configuration using the Windows package manager COM API. It disables its configuration processor telemetry, which is now reported as a notable observation; no malicious configuration payload is included.

## Archive follow-up

The nine embedded-source gaps are GitHub Actions runner substitutions: the scanner analyzes neutralized step bodies while recording that runtime expressions are unresolved. The workflow commands were inspected separately; they primarily build, test, publish, and commit generated files. One step directly substitutes the head commit message into a `run` script, now reported by `metadata/build/ci/expression::workflow-commit-message-inline-run`. This observation does not establish that anyone exploited it. Tests distinguish direct substitutions from an environment-variable binding.

The top-level JavaScript install hook fetches public project statistics and prints a donation message. Evaluation candidates include a build-time source transformation and CLI argument evaluation. The CLI can optionally read exchange credentials from environment variables and configure a proxy. A bounded inspection of shell files found a checksum-verified Composer installer, build and cleanup commands, and an optional skill-document downloader.

The archive also includes four native shared libraries and a WebAssembly binary. Their no-high-finding scans, exported signing/trading functions, Go build metadata, and exact byte matches to the upstream commit support their role in this package. Incomplete flow analysis remains a coverage limitation.
