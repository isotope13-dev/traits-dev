# Native-host setup fixture: capabilities versus remote staging

The outstanding full-suite failure was reviewed from the archive contents,
not resolved by restoring a broad detector or suppressing validation.

## Specimen evidence

The former hostile corpus fixture
`crx/crx-dunelinenode-native-host-install-linux.crx` contains only a manifest,
background script, README, license and icon. Its executable source:

1. Registers an onInstalled callback.
2. Reads a local storage key and writes a `hook` string containing a domain/path.
3. Sends `{op: "install"}` to a named local native-messaging helper.

There is no native-host implementation, download, registration-file/registry
write, remote message handler, or command execution in this archive. A comment
claims that a bundled helper writes registration, but no such helper is present.
The stored domain/path is never requested or transmitted by the included code.
This does not establish the behavior of an unavailable helper or prove the
product safe; it does establish that this fixture lacks the claimed hostile
staging evidence.

The retired `extension-install-native-host-stager` required only onInstalled,
native-messaging permission, sendNativeMessage and local storage writes. Those
are useful neutral capabilities. Their conjunction does not by itself prove
staging or a malicious remote-control objective. The retirement is retained.

## Fixture correction and positive control

The archive moves, byte-for-byte, to
`testdata/benign/extension-native-host-install-request.crx`. SHA-256:
`e97f3ed42ff014799194be9ce76c60261ff9b0b24822aaffd89800172076c068`.
It retains required native IPC, declared permission and storage observations,
and forbids the remote-command extension objective namespace. Its checkout
score is 13, entirely from neutral findings; the explicit cap is 13. Installed
atomscan reports score 11 with no suspicious/hostile findings; the two binaries
are reported separately rather than treating their scores as interchangeable.

A new inert positive archive, `extension-remote-native-tasking.zip`, includes
an extension that accepts commands from a WebSocket channel, forwards execute
requests to a native host, and the native-host source that executes the supplied
command. Its manifest grants native messaging and all-site authority. The
fixture is never executed; the endpoint uses `.invalid`. It requires a hostile
finding and the remote-command extension prefix. Read-only atomscan matches
`extension-wss-native-shell-bridge`, independently of the retired setup detector.

This pairs a negative capability combination with positive tasking/execution
evidence. No detector bodies, criticalities, or exclusions were changed in this
cohort. Reclassifying the original is a ground-truth correction based on the
included behavior, not a lower floor for a known hostile sample.

## Taxonomy boundary

Native messaging belongs in `communications/ipc/native-host`; install/update
callbacks belong in browser-extension lifecycle, permission declarations in
metadata, and storage changes in their storage operations. Remote-control
objectives require the additional tasking/execution relationship. An install
message, stored URL, or comment about a helper must not be promoted to an
observed download, registration write or native execution.

Read-only scans and validation logs are in `/tmp/taxonomy-native-host-review/`.
The earlier failed TLS initialization run remains documented in
[TLS initialization](TLS-INITIALIZATION.md); this audit resolves that fixture
expectation discrepancy without reverting the unrelated detector retirement.

Final shared-checkout validation passed **1,760/1,760 fixtures**: 262 hostile,
470 benign, 175 does-nothing, 45 drop-exec, 571 supply-chain, 66 impact-wipe,
82 obfuscation, 24 reverse-shell and 65 simple-stealer. `validate --soft` exits
0; strict `make validate` exits 2 with only the existing 169 oversized-directory
policy violations. This verifies fixture expectations, not completion of the
remaining taxonomy migration.
