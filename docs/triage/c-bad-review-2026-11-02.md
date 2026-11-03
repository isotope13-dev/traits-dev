# C queue review

The exported paths are a snapshot; Hopper holds the current labels. Both the
local scanner and Atomscan were used on each sample below. The installed
Atomscan warns that an unrelated Lua trait file cannot be parsed by that build.
After the final loader improvement, a Hopper dry run confirmed the current
labels for all 40 snapshot entries: 35 good and 5 bad.

- `009493430e0872bb99116ac59ebb6ed21d90f75d76659f1ab324fd9a9bc20f2c`:
  a test include wrapper containing only `#pragma once` and a standard header
  include. Neither scanner reported suspicious or hostile traits. Moved to
  **good**.
- `0477de10357c0d79762f2dca9976a18e120619668005a4cfbdd1982cba3e1a3b`:
  deprecated JSON library macros for hex digits and error values, with no
  attack functionality. Neither scanner reported suspicious or hostile traits.
  Moved to **good**.
- `ae88bde44bc4227c20a93435f9df0c15fdd98eaf3102360bd03c0f9da21edb35`:
  a thread-creation limit test that joins its threads. Neither scanner reported
  suspicious or hostile traits. Moved to **good**.
- `5ab53e4ec5fbc1803c869b4bab7d65ad994bff814b25f5302efa1e3191f0352b`:
  a small Objective-C message-lookup shim. Its exploit-related source path
  does not make this supporting file an exploit. Neither scanner reported
  suspicious or hostile traits. Moved to **good**.
- `427be77e313648332a97d3551b4a3301485cd4abad2390fee835b2f028e5aa1a`:
  despite its `.c` extension this is HTML. A valid script repeatedly opens
  windows, and it contains x86 shellcode and heap-spray exploit text. The
  latter is preceded by malformed `< SCRIPT` markup rather than a recognized
  script start tag, so its text alone does not establish that the heap spray
  executes as HTML. Both scanners report multiple hostile payload observations;
  descriptions were clarified to avoid asserting execution. Hopper confirmed
  the existing **bad** label for the attack-bearing artifact.

The following eight supporting files each had no suspicious or hostile findings
in either scanner and were moved to **good**:

- `18cf8c44011ecbcbc390f8e0402b4886b30cc398f1b7512dde90007dd3c75434`:
  ChaCha API declarations and constants.
- `c3b2b2fd943d11698bcfe87e83a770f1220398be7abcb9807d4a132ed934f82e`:
  integer typedefs for a compiler test.
- `d09cd70525b8278359c05cec994d36650761c8aae738d975416f384c91d4e60b`:
  a plugin initializer that only prints a diagnostic.
- `9d4281ae485ea36959675701c23585a67b5ae8dbc9000c939836ed60f86bc41e`:
  board platform cache initialization and cleanup.
- `ac70a7697ce08bb0c550e27d68ccd05f39ce1a3c92e4d6f278b5fce469062d17`:
  Ed25519 type and function declarations.
- `7e5d4395453ee2bc54040cc9ac9c6df30b7230e15088c0290a038831a6cbc438`:
  C source with a `.dll` extension that displays messages on DLL events;
  the comment suggesting replacement with shellcode is not shellcode.
- `d24405b1c664d31c70e30d1f072849d83d8f086531d46a45f3aa149d313e2c20`:
  MAC address string conversion.
- `8a8b24a216c09ec6dea692be1b6ee02104d6aed9397295f4f8fff2688429e839`:
  JSON value setter assertions.

`6457b79d5697083b6eb17b78c40eacbc57410af820e4694e419e25425291ac26`
reads BPF hide settings and prepares process and file inode lists for a
rootkit configuration. A new hostile observation identifies that combination
without claiming that this component performs the kernel hiding itself. Both
scanners now report it. A structural observation also binds `getppid()` to
the process-inode helper, exposing the parent-process lookup without assuming
the helper implementation is present. Both scanners report that observation;
focused tests cover unrelated calls, the current PID and comments, and full
uncached validation passes. Hopper confirmed **bad**. The component provides
configuration rather than the kernel hook, so further independent hostile
coverage is not asserted from these operations alone.

The following nine samples are library or SDK support code. Both scanners
reported no suspicious or hostile traits, and Hopper moved each to **good**:

- `4b92072230e2b218e5de9dc28460a91cbd2a2302464c380724847ffa6004de2f`:
  character-encoding declarations and flags.
- `8f1154fec340ac4395a8b3067c68a5d4fd9389130a6b09a3e36b4e30da9a6837`:
  SSH packet API declarations and compatibility macros.
- `1085a58208f21c7e27332c8acf15af6c357900bd6fec997917a604ecad011027`:
  C++ atomic type and function aliases.
- `d54cb4af1ea76aa5480bb40fb40dc679f75579632eb3d6f97ed6b8d01b7b6a0b`:
  performance-marker API header.
- `9588714092e733b53d4e433be86b261422b139ebda0e54fc45b06f69e7ea3f2a`:
  transaction interface declarations.
- `aadb35fd0a952e7587411fec17892802ff6e46964dec8eff911cca9cf42ba137`:
  generic BPF instruction-construction macros.
- `522b9bf5d1df424d0330ace91262a2b839b38d54ea11d1afc18ac320f9b13324`:
  JSON object and array test code.
- `cb58b9c228057c145ee8234ac8d56926d2b124d010a194250fe175d675e09505`:
  preprocessor consistency checks for TLS build options.
- `3dbe8f33b59053c99c68b9eba3429ef3cb322d81e889b1536a35eb7c53b0c236`:
  a noncryptographic hash function for table lookup.

`d1f7f26a7ac6b12c636dbc1e2cadaec0f2bb44b9e443f3c1885e73d3b65a1a00`
implements a dedicated memory-only Mach-O loader, including segment mapping,
protection changes, dyld integration, optional unpacking, and a call to the
resolved entry point. Both scanners now report a hostile finding combining
the loader API clusters, aPLib and a JIT mapping flag with a structural path
that binds a memory-image handle to module linking, symbol lookup, address
resolution, and an indirect call. The structural match uses the source's
named API function pointers; it does not prove runtime success or bind the
separate decompressor to that particular image. Focused tests cover unrelated
handles, symbols, addresses and calls, a lookalike function name, and a
missing JIT flag. Full uncached validation passes, and Hopper confirmed the
existing **bad** label. A second hostile observation covers its other loader
path: it binds the JIT mapping to the image address passed to a symbol resolver,
then binds the resulting address to an indirect call, alongside the dyld API
cluster. The matching variables are source-text bindings, not proof that a
runtime call succeeded or that the aPLib output reached this path. Both scanners
report the two hostile observations. Focused tests cover mismatched allocations,
image and entry addresses, missing JIT flags, a flag inside a string, unrelated
resolvers, and a missing loader cluster; full uncached validation passes.

The following five samples had no suspicious or hostile findings in either
scanner and were moved to **good**:

- `45f2a84ee24624fce758d0daef39ca89c38245a3f955781aed3fa4627d895e22`:
  compiler-test math declarations and aliases.
- `ac900dbb26ff83a9b35902d61747c2ff38cfea4cc3ae5cb92317a49c51f07a00`:
  an Android RenderScript umbrella header.
- `43b8faf1422fd82d08b359b27655a5c597692d045bee2fd8f933f8d0d22f9d03`:
  a UFS filesystem identifier.
- `06c1d1ea8b112161599877ecd143ccb6be38f195014ff23a4ee796efb650bc02`:
  MD5 digest implementation.
- `9d6a78f9367965117779a10bf282c5d76bdd7b18fc8dc585121bfacd51812b2b`:
  prime candidate generation and testing for Diffie-Hellman moduli.

`4296d8229d8fb5faf3ad409f5c9a00ca1358a32abe28d31861a7b9fbc661f9e1`
is an application source archive with executable traversal tests that attempt
to download `/etc/shadow` and upload under `/etc`. The tests expect rejection,
but construct and submit the attack attempts. Hopper moved the archive to
**bad**. The all-files local scan covered all 534 members and reported the two
attempts as hostile; 266 records had analysis gaps. Atomscan reported the same
attempts as suspicious and another finding in a separately fetched dependency.

Four library and SDK files had no suspicious or hostile findings in either
scanner and were moved to **good**:

- `12e0046d88c666d0c7303972505d94181f5cb4774cad8ca8af9d0d8643e03104`:
  LZMA2 decoding implementation.
- `05d15a63ee2a42108fa5eccbae5e55c981c33ca9366e89b2c030bf7ce5c58c3b`:
  SHA-2 implementation.
- `42d4daf0fa3696bfc4eb683ec79172ca7b4bf4beb451515a60f5777d1599e40e`:
  Windows diagnostics interface definitions.
- `2127a6a2c6ef4aaa8d7f036190fb3d805ee811d194bbfa35cf709ba6032e5923`:
  configuration file parsing and generation.

`0cb336584a989dcfdfb0048fb6ac92fbc89fcfca51bd090614e084252a001cb7`
is a game source archive. Its maintainer setup script creates a restricted
uploader account and installs an embedded SSH public key. A new suspicious
finding identifies a literal key redirected to an authorized-keys file; it does
not claim that the key was installed or unauthorized. The all-files local
scan represented all 3,088 archive members and reported that one suspicious
finding, with 1,243 records reporting analysis gaps. Atomscan on the extracted
script also detects it. Hopper moved the archive to **good**.

Four additional source files had no suspicious or hostile findings in either
scanner and were moved to **good**:

- `a77c19b2760ea8f62660e39e6359b4c2e95333b5fc9bd5fb8a3791c2e9deb43f`:
  configuration-menu UI, including its dialog subprocess.
- `5e48e8b2d934ccd0efc6786705477057327fade0fe85ab28296964bfcace8536`:
  Sun disk-label partition operations.
- `9bde8dac8663a6b343b1657c07eebbd8d80e112ef342090912d993feb3a74c34`:
  general asynchronous network connection routines.
- `b3ca1b820af5fbd27ae3d50f7f8dbf8b4d0c12c33078821558ab0669d551b932`:
  SSH key handling routines.

`05b638d65351bc154dd9c24ab62b8437df12ccedaceafac1c0d9926a9df801b3`
is a performance-monitoring source RPM. Its `qa/640` is byte-identical to the
privileged symlink test reviewed in the shell queue: it constructs an attempted
privileged write into a protected directory and checks the result. Hopper moved
the package to **bad** under the exploit-test policy. The local scan produced
42,464 records and reported analysis gaps in 2,182; its run preceded a new
suspicious co-occurrence rule. Atomscan produced a JSON report but exited 1;
the report included the test and one finding in a fetched dependency. A
separate Atomscan of the extracted test detects the new suspicious finding.
A more specific finding now binds the protected target and notices link to a privileged `pmpost` probe and the checked file. Both scanners report the hostile exploit-test finding in the source RPM and extracted test, without claiming a successful write. Focused path and privilege negatives and full uncached validation pass. Hopper confirmed **bad**.
