# Encrypted staging: Android and native profiles

- The Android rule matches encrypted core ZIP entries, obfuscated resources,
  asset names and a named native library. It belongs in
  `objectives/anti-static/pack/archive` as suspicious packing evidence; these
  conditions do not establish payload staging or execution.
- The Hashcat executable path belongs in
  `well-known/dual-use/credentials/hashcat`, using the existing Hashcat
  release rule’s 2 GiB maximum to satisfy well-known validation. This bound is
  a validation constraint, not evidence about the path. The MinGW XOR loop, API-hash
  candidate and TLS or process/thread clues belong in
  `metadata/file/profile/pe-api`: they do not identify a payload loader. The
  profile remains suspicious. Its independent 64 KiB minimum was removed
  because none of those observations depends on overall file size. The XOR
  component itself still has an inherited 50 MiB maximum, so the profile is
  not effective above that limit.
- `ZEROCRYP` is a text substring, not a verified overlay header; it belongs in
  `metadata/file/profile/overlay` as a supporting observation. Together with an unsigned PE overlay and
  API or Rust library clues it forms a suspicious overlay profile under
  `metadata/file/profile/overlay`. It does not establish AES-CTR, a decrypted
  payload, or execution, so the former hostile dropper claim was removed.

The match predicates, platform and file-type scopes, confidence and exclusions
are preserved except for the explicitly removed MinGW size minimum. No other
YAML or Markdown file referenced the original IDs. The destination directories
contain 59, 22, 22 and 9 direct rules respectively.
