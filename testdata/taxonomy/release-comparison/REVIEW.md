# Release comparison triage

Both supplied samples are BENIGN. The matched behaviors are ordinary software
features, not evidence of a supply-chain compromise. No sample was executed.

## AetherSDR

Artifact: `aethersdr_26.10.1+dfsg-3_arm64.deb`, SHA-256
`0b3a34813b3adc15221459894be380e3494f45da2a959b04f6e346e2c7409205`.
The flagged member is `usr/bin/aethersdr`, an AArch64 ELF Qt/C++ SDR desktop app.
The complete sample is byte-identical to the package fetched from
https://deb.debian.org/debian/pool/main/a/aethersdr/aethersdr_26.10.1+dfsg-3_arm64.deb.

Fetched the earlier Debian `26.9.5+ds-1_arm64.deb` and the official source
archives `26.9.5+ds.orig.tar.xz` and `26.10.1+dfsg.orig.tar.xz` from that pool.
Compared the complete source trees. The deciding comparison is:

* `src/core/DxClusterClient.cpp` is byte-identical between these releases.
* Both `LogManager.cpp` versions contain the exact diagnostic
  `DX cluster telnet connection and spot parsing`.
* The Telnet client connects to a user-selected cluster host/port, sends the
  operator's callsign when prompted, strips Telnet IAC bytes, and parses radio
  spots. Bounded buffering and reconnect logic are normal client operation.
  There is no credential dictionary or Telnet password spray in this routine.

Rizin confirmed the ELF architecture/linking/stripping; recovered strings and
Cleave facts correlate with these source implementations. The larger release
adds radio/backend, authorization and UI work. The reported `pan=` values are
panadapter identifiers, `Preferences` is UI wording, and the 500 MB size error
belongs to firmware/waveform upload limits. `TciPeerProcess.cpp` uses procfs TCP
connection tables for local radio-control peers, not a Mirai identity.

The earlier binary also reproduces the Telnet text match under the current
scanner. Thus the supplied older-benign premise does not establish that this
text first appeared in 26.10.1; the actual diff shows the flagged implementation
is unchanged. The faulty inference was the trait's brute-force classification.

## Azure ARO-HCP

Artifact: `github.com-Azure-ARO-HCP-v0.0.0-20260914211247-cb5c9e6108da.zip`,
SHA-256 `1316a02bd8b0b9948f85aff1c77ea20c6b269b4fe101a4183d2393b8292cc419`.
The flagged member is `dev-infrastructure/scripts/swift-vnet.sh`, a development
infrastructure helper for Azure Red Hat OpenShift Hosted Control Planes.

Fetched the upstream Git history. All 1,488 extracted sample files match the
Git tree at `cb5c9e6108da` byte-for-byte. The immediate predecessor
`177c632a0483382ef73764df51b6fc95a0bcf74b` differs only in image-updater client
and test files; it does not change this script.

To compare before the flagged behavior was introduced, fetched and scanned an
archive of `65cc13defe525b5ab3cb133fb0c56fff454aa36c`, the parent of introduction
commit `c57c6fa6e94c0eaaa065246eeeec25a21d60b695`. Its scan has no suspicious or
hostile traits. Compared its `modules/network/vnet.bicep` with the introduction
and current versions. The original ARM deploymentScript performed the same
VNet create/tag operation under the same registered managed identity. The new
helper replaces that mechanism with an Azure CLI container because the old
mechanism created a storage account forbidden by Azure Policy. The revert and
reintroduction at `65be3096aafff2d1f60dbfb2e21a024ca20e04fa` preserve this purpose.

The current helper constructs a readable heredoc, Base64-encodes that runtime
text, and passes the encoded variable into the container's quoted Bash command.
The container logs in with its assigned managed identity, waits for DNS/RBAC,
creates or tags the selected VNet, reports status, and is deleted. Later commits
add readiness retries, logging and timeout changes. There is no hidden static
payload or theft destination. Base64 preserves quoting across the container
command-line boundary; it does not conceal source from review.

## Trait corrections and scope

* Relocate generic Telnet connection wording from IoT brute force to the
  neutral Telnet capability. Remove it from the scanning/brute-description
  union; retain explicit scanner/brute wording.
* Add a notable structural runtime-encoding/quoted-shell binding and an
  exception used only by the short `base64 -d | bash` objective. The binding
  requires the same encoder-output and decoder-input variable, excludes
  intervening assignments and rejects a second decode-to-Bash pipeline.
  Unrelated input, reassignment and an additional payload stay suspicious.
* Relocate the generic file-size-limit diagnostic from C2 to file attributes.
  Correct the description: the regex accepts any stated MB limit, not 10 MB.
* Remove the generic procfs path from the LZRD identity atoms. Its consumer
  uses the existing TCP-path capability plus an exact truncated-path atom;
  complete paths no longer produce duplicate malware-family vocabulary.
* Relocate command-output Base64 encoding from exfiltration to data encoding,
  and retain its exfiltration consumer. Split producer forms into small
  matchers. A variable expansion's closing brace is not a command group.
* Require a Chromium profile path for the ordinary Preferences filename.
  Require explicit card-number wording for unquoted payment fields; bare PAN
  is ambiguous and falsely matched radio panadapter logs.
* Move arbitrary numeric chmod modes to permission modification. Use an
  owner-executable numeric-mode atom in executable/launch consumers. Anchor
  command positions so a chmod failure diagnostic is not a shell command.
  Audit parent executable-mode selectors: they should retain executable-mode
  evidence, not arbitrary 600/440 permission changes.
* Describe the RELAY match as label text rather than claiming a protocol.

No family allowlist, package filename gate, exact-size signature, or sample
hash was added. All execution, network, permission and encoding capabilities
remain notable. Explicit moved-ID consumers were updated. The Base64 encoder
parent selectors use a single required role, so added producer alternatives
cannot satisfy a multi-role threshold by counting the same operation twice.

## Verification

`cleave facts` was run on both archives and both flagged members. Initial and
final `atomscan` runs cover both supplied paths. Final archive scans have zero
suspicious and zero hostile traits. Full dependency-following scans also had
zero such findings. Downloaded predecessor scans and source diffs are described
above; the exact version previously judged benign was not supplied.

Run `python3 testdata/taxonomy/release-comparison/run-controls.py` for the
11 regression controls. It copies fixtures to neutral temporary paths so testing
context cannot suppress the objective under test. Native ELF fixtures include
positive and negative file/path/payment observations and both full and
truncated procfs paths. Sources are supplied alongside the compiled fixtures:

```
clang -target aarch64-linux-gnu -c observations.cpp -o observations.elf
clang -target aarch64-linux-gnu -c browser-payment.cpp -o browser-payment.elf
```

Judgement marker summaries (also the commit body):

AetherSDR: unchanged DX Telnet client; remove brute-force inference
ARO-HCP: readable VNet script uses Base64 container transport
