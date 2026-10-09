Controls for the duplicate Content-Length literal observation.

`duplicate.rs` and `probe.rs` must match the neutral duplicate-header trait.
`probe.rs` must also retain the source desynchronisation probe composite.
`comment.rs`, `separate.rs` and `body.rs` must not match duplicate headers.
Comments must not match the source Content-Length literal trait either.

Predecessor comparison: Orca proxy/core rc.10 -> rc.11 have identical source;
only versions, lockfile checksums and VCS metadata change. The flagged
forward.rs explanation is unchanged. Trillian parent 858b270d2933 ->
5e12fb368c8f changes only go.mod/go.sum; storage_provider.go is identical
(and also identical to v1.3.13). Its Base64-gzip data decompresses to an
ASCII warning sign and flows through ioutil.ReadAll to glog.Warningf,
never execution. The built-in binary/embedded/base64-gz finding has no
YAML suppression hook and remains one suspicious observation, duplicated
on carrier and decoded child. No YAML shadow rule or package allowlist.

Both former source/text and general/literal atoms now share one canonical
HTTP content-length leaf trait. Consumers retain their source/binary scopes;
blank-header boundaries are rejected on the matched fragment. The neutral
header observations carry C0002 and no unsupported C2 ATT&CK mapping.
