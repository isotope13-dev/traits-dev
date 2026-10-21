# Registry second review: Minimod and Heartbreaker

Reviewed the actual bytes of the three supplied samples, independently of their
labels and scanner scores. SHA-256 identifiers:

- Minimod: `7798a78960e7671a7d0732d3ccf7a0ed142baa89c472a20338bcfcdc7906474c`
- Renamed Rust variant: `bd6a078fa7ee23dcee8f50521ff9037506b102b7f41c895b659a88fedfa1c057`
- Heartbreaker Rust: `10fc734e7fe1d0af6b7c17f0bb0f5ea99b337617745223575f0b29ebb743b748`

All three are MALICIOUS on their contents. Registry origin alone does not explain
these behaviors. No specimen, downloaded payload, or dependency was executed.
No external feed, advisory, or runtime retrieval was used to establish a verdict.

## Execution evidence

The JAR claims to be NoammAddons 1.2.8. Its added Minecraft `run` HEAD mixin
reflectively invokes the obfuscated initializer once. The initializer's object
construction first resolves a host using an Ethereum JSON-RPC `eth_call`.
On initialization it reads the Minecraft username, UUID, and access token into
a Gson object, adding C2 and payload-label fields. A thread fetches
`https://<resolved-host>/api/static/loading`, iterates the response as a JAR in
memory, and prepares class and resource maps. It then loads `com.example.Main`
and invokes `initialize(String)` with the account JSON on another thread.
This credential handoff to remotely acquired code is unrelated to gameplay.

JADX and javap corroborate the paths. Arithmetic-only helper expressions were
isolated and evaluated separately to recover 65 constants: account JSON keys,
32 public Ethereum RPC endpoints, the JSON-RPC body and selector, and DoH
configuration. OII's POST body is the contract lookup, **not the token JSON**.
iI uses default trust managers, explicit SNI, raw TLS HTTP GET/POST, and optional
DoH A-record resolution against 1.1.1.1 / 8.8.8.8. There is no demonstrated TLS
trust bypass. The standalone VM decodes an encrypted custom bytecode resource
and interprets it with reflection; its resource and supporting classes are
absent from this reduced JAR. The custom class loader is also absent. These
limits prevent claiming successful activation or any final payload actions;
they do not make the implemented token-handoff path benign.

The two Rust sources share a directly reachable `main -> entry` path. They
request startup registration through their external helper, initialize
AES-256-GCM with an embedded 32-byte key, recursively visit Downloads, read
files, generate a fresh 12-byte nonce, encrypt, truncate the original, write
nonce plus ciphertext, and rename it with the chosen extension. Existing
`.encrypted` files and each variant's already-renamed files are skipped.
They write a desktop README demanding two Bitcoin payments for decryption and
display a ransom UI whose decryption button is disabled. The UI examples ending
in `.locked` are illustrative; the actual suffixes differ.

After the UI returns, `main` checks for Rust (requesting installation through
the external helper if necessary) and calls a rewrite routine. That routine
embeds its own source and build script and passes both plus a generated Cargo
manifest to mimicore/metacore's morph API. Renamed variables, unused junk
functions, and litcrypt macros add concealment. The helper implementations and
build script are not supplied; actual startup persistence, toolchain install,
rebuilding, and compilation success cannot be confirmed. Fixed keys and absent
decryption code do not negate the destructive overwrite and extortion workflow.
No consent-based utility or test harness context accompanies these sources.

## Corrections and retained coverage

- Retired `minecraft-named-token-tls-post`: archive co-occurrence of a token
  getter and raw TLS POST did not bind the token to that POST. The actual RPC
  body refutes the claimed transfer. All POST, socket, JSON and token-handoff
  observations remain. No replacement exfiltration rule is invented.
- Retired `fabric-mod-named-session-jar-stage`: its required Fabric metadata,
  getter, archive iteration and reflection do not establish modification of a
  trusted component. The observed handoff and loader retain their hostile
  findings; no accurate loading or credential behavior is lost.
- Moved `minecraft-named-user-ref` from credential objectives to
  `metadata/import/framework`, retaining matcher, scope and notable severity.
  Removed the duplicate unqualified `getAccessToken` matcher: the existing
  `metadata/import/framework::minecraft-token-getter-ref` retains both actual
  Minecraft mappings and does not misidentify unrelated token APIs.
- Moved `aead-destructive-file-relabeling` to
  `micro-behaviors/fs/write/encrypted::aead-overwrite-rename-profile`, retaining
  all match predicates and scope. Its supported claim is neutral overwrite and
  rename co-occurrence, now notable, without the unsupported T1486 mapping.
  Extortion remains independently required by the hostile ransom composite.
- `morphing-aead-file-relabeler` now requires that extortion composite: source
  mutation plus neutral encryption alone does not justify hostility. Both real
  sources still fire the distinct hostile extortion and mutation findings.

Exact references and ancestor selectors were searched before changing shared
rules. The retired Minecraft rules have no exact consumers. Broad exfiltration
consumers were inspected; they do not establish the missing source-to-send
relationship and are scoped to other languages/surfaces. The relabel rule has
two exact YAML consumers and no broad ransom selector consumers; both exact
consumers were updated. Historical sample-results.json remains a dated record.

## Verification and classifier limits

`check.py` covers the neutral encrypted replacement plus mutation control and
two existing attack JARs outside this batch. The existing JVM checker passes
11 cases, including split-class ABI/XOR and generic secret API near misses.
The existing Heartbreaker checker passes nine controls: encrypted copies,
decryption, comments, source embedding, generic reads and prose-only wording.
The outside-batch JARs retain their existing hostile attack coverage.

Before/after Atomscan scans use the same installed v18.18 models, slow mode,
local traits, registry context and no rule refresh. JAR members were compared
individually. The supplied JAR changes from 4 hostile / 3 suspicious to 2 hostile
/ 3 suspicious. Only the two unsupported hostiles and redundant getter are
lost; the user-class import moves to metadata. Its l0 member retains its hostile
handoff; the other class members retain every finding.

Both Rust files retain 2 hostile findings; each changes from 2 to 1 suspicious
and 24 to 25 notable because the neutral relabel profile moved. Their classifier
routes remain class 0 with `lvl=-1`, despite hostile rules and the reviewed
malicious behavior (aggregate probabilities about 0.9617 and 0.9611 after the
correction). Atomscan renders both Rust files as BENIGN[49%]. This is a classifier miss, not a reason to restore the inaccurate
objective. JAR raw model routes also fall to class 0 after the two false claims
are removed; the emitted aggregate is 0.98 / level 25 with retained hostile
rules. The installed model warns that it expects feature schema v18 while the
extractor emits v19; retraining is outside YAML scope.
