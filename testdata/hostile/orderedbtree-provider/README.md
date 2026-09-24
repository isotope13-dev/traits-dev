# orderedbtree-provider

Clean-room fixtures that keep the gocommunity.io/orderedbtree and
gocommunity-io dockerd Terraform-provider rules covered after the live triage
samples are gone. Neither file is derived from the real sample bytes; both are
synthetic reconstructions of the *shape* the rules detect. Never execute them.

## release.zip

A synthetic Terraform-provider release archive: a compiled Go binary
(`terraform-provider-repro`) beside `examples/import-resource.sqlite3`, a ZIP
disguised as a SQLite database whose one member is AES-GCM ciphertext. Models
the dockerd 4.5.4+ release layout, where the loader source does not ship and
only the binary's hash-named pclntab symbols plus the disguised payload archive
remain.

Drives, on the container and its members:

- `objectives/supply-chain/hidden-payload/archive::archive-database-disguise-with-hash-named-code` (hostile)
- `objectives/evasion/masquerade/extension-mismatch::archive-disguised-as-database-file` (suspicious)
- `objectives/anti-static/obfuscation/name-mangling/variables::go-binary-hash-named-functions` (suspicious)

The binary was built from a five-function `main.go` whose helpers are named as
12-hex-digit hashes (`_ad79680770be` and friends), each a no-op env read, so the
pclntab carries the hash-named symbols the rule keys on and nothing else:

```go
//go:noinline
func _ad79680770be(s string) string { return s + os.Getenv("C") }
```

`import-resource.sqlite3` is a store-method ZIP holding `dist/a.go.tmp`, 4 KB of
random bytes standing in for the AES-GCM-encrypted second stage.

## node-loader.go

A clean-room reconstruction of the source-shipping loader (the real one was
orderedbtree's `deprecated/IsKeyExist`). All identifiers, the gate digest, the
key and the paths are synthetic. It gates on a hardcoded SHA-256 hex literal,
unzips a bundled archive, AES-GCM-decrypts its `.tmp` members to disk, then
builds and runs the tree with a detached `go run .` and releases the child.

Drives:

- `objectives/supply-chain/hidden-payload/runtime::go-decrypt-embedded-archive-then-build-run` (hostile)
- `objectives/supply-chain/hidden-payload/runtime::go-gated-decrypt-and-run` (hostile)
- `objectives/supply-chain/hidden-payload/runtime::go-detached-toolchain-run` (suspicious)
- `objectives/anti-static/obfuscation/name-mangling/variables::hash-named-local-assignments` (suspicious)

## Not covered here

`objectives/supply-chain/hidden-payload/archive::archive-disguised-library-feeds-decrypt-execute-chain`
(loader source and a disguised native-library archive inside one package) has no
fixture: it needs both artifacts in a single archive, which these two separate
files do not form.
