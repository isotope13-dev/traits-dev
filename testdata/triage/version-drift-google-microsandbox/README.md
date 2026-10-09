All three supplied artifacts are BENIGN; no compromise found in the diff.

Identity and predecessor evidence
- Google certificate-transparency-go pseudo-version 5f7e9ba4be3d:
  fetched v1.1.1 from proxy.golang.org. ct_hammer/main.go is byte-identical.
  Its 590 gzip bytes expand to ASCII artwork, decoded via Base64 and gzip
  and copied to os.Stdout only when the banner option is enabled. No file
  write, module loading or execution consumes the decoded content.
- Google Trillian pseudo-version df474653733c:
  fetched v1.3.13 from proxy.golang.org. cloudspanner/storage_provider.go
  is byte-identical. Its 543 gzip bytes expand to warning-sign ASCII art;
  warnOnce.Do bounds Base64/gzip/ReadAll/Warningf output to one invocation.
  The downloaded current Go module archives exactly match the supplied
  SHA256 values, 200dcc73124e0085679c0272a734ff587cbb2c0aad8b60f76547b56e96d3d4c0
  and 76f02465ddd8379f3f623c822c7d806f21a8b80903542a66b99cbf81f7f8dbb8.
- microsandbox-runtime 0.7.8, sandbox VM runtime:
  fetched runtime 0.7.7 and network 0.7.7/0.7.8 from static.crates.io.
  Runtime dependencies advance together from 0.7.7 to 0.7.8; managed jobs
  add bounded output storage and scoped, revocable execution-control leases.
  network.rs is byte-identical. with_captured_gateway_mac returns
  InvalidGatewayMac for a zero, multicast or guest-equal MAC, not success.
  The duplicate Content-Length fixture already exists in 0.7.7 and asserts
  unwrap_err() == SecretViolationAction::Block inside the unit-test module.
  handler.rs adds per-header substitution restrictions, increasing HTTP/2
  stream-ID validation, and a structural HPACK check before decoding.
  The only new network source member is the defensive HPACK validator.

Corrections
- Relocate the generic Rust zero-array OR comparison to control-flow/branch,
  notable, with an AST matcher excluding comment-only occurrences.
- Require a hardware-identity branch to return explicit success before
  reporting zero-identity acceptance. An Err return cannot satisfy it.
- Source duplicate-length desync now requires a subsequent request in the
  same literal. Nearby independent request fixtures do not prove pipelining.
  Existing source/header and request literal observations remain neutral.
  The hostile composite has precision 5.2 in test-rules, above the 3.5 bar.
- No package-name allowlists or engine-finding shadow rules were added.
  Go decode/output behavior already has correctly placed notable traits.

Verification
Ran atomscan and cleave facts for each supplied archive and inspected both
flagged Rust source files with cleave facts. Final atomscan JSON has zero
hostile findings on all samples, zero suspicious findings on Microsandbox,
and exactly one distinct suspicious engine-generated Base64-gzip finding
on each Google package (repeated on archive, carrier and decoded child).
The engine has no YAML suppression hook for this finding. These are unusual
compressed display resources, not executable payloads or evidence of attack.
Focused controls: python3 testdata/version-drift-http-framing/check.py.
All four pass: separate templates, same-literal pipeline, rejecting zero
identity, accepting zero identity. Controls run outside test-named paths.

Judgment marker text (also recorded verbatim in the commit body)
CT hammer: unchanged gzip banner printed to stdout
Trillian: unchanged gzip warning logged, no execution
Microsandbox runtime: rejection and parser tests misread as attacks
