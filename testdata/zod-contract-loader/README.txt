Zod contract loader regression fixtures

Source: https://github.com/colinhacks/zod/commit/d821685ea6732436fcdf786a81d076958471e467.diff

testdata/hostile/zod-meta.test.mjs contains the exact four added lines from
packages/zod/meta.test.mjs. The mini package has the identical loader.
Git blob: a880fc34cad095819e6bacb6edcbaea214a40b20 (matches the diff).
SHA-256: 5ed518aaff5aebc729545b8eb223ec31927cd1bfa53169517f09cdbcc9fd5a0b

zod-contract-loader.tgz is a reduced, deterministic package archive containing
the original package.json and meta.test.mjs. Its top-level preinstall field is
suspicious, but npm lifecycle hooks require scripts.preinstall. The fixture
must NOT claim an active install-hook loader from that misplaced field.
SHA-256: 8c79c8d8181dc8420ed8ff91d64cd2942e14f87cfab025e03bc9f382a3345591

zod-active-preinstall.tgz is a derived control that moves this declaration into
scripts.preinstall. It additionally matches the hostile install-hook composite.
Neither archive is a complete published Zod release.

Both the original source and package must match at least five hostile traits:
contract module bootstrap, computed-host routing, staging cleanup, compact
hex/POST/Base64 executable loading, and compact contract/payload module loading.
The compact patterns also require executable module loading and decoded file
staging: common client operations or minification alone are not hostile.

Benign .mjs preinstall control:
testdata/benign/openclaw-mjs-preinstall.tgz preserves the original helper from
OpenClaw commit 704feda9dad19899a84fc8262dc5ed857c794b35 and its original
scripts.preinstall command. Unrelated manifest fields are omitted. The helper
inspects package-manager metadata and prints a warning; it does not download
or execute remote code. The hook remains notable. Naming a malicious helper
like this control must not suppress the independent hostile loader detections.
Source: https://github.com/openclaw/openclaw/blob/704feda9dad19899a84fc8262dc5ed857c794b35/scripts/preinstall-package-manager-warning.mjs

compact-rpc-base64-client.mjs combines parseInt, POST, Base64, payloadB64,
eth_call, temp writes and cleanup on a long line, without executing the data.
local-base64-module-builder.mjs imports locally generated Base64 module code
without fetching a remote stage. Both are negative controls.

Regression floors and required/forbidden finding IDs live in
testdata/expectations.toml and run with make validate. Analyze bytes only;
do not install, import, or run the hostile fixtures.
