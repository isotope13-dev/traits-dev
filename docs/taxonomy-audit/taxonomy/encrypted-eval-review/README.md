# Encrypted staging: JavaScript source observations

The former decrypt-eval-chain file contained two source patterns and three
combinations, none of which establishes a payload execution chain:

- A zero-filled buffer followed by an AES-256-CBC decipher call belongs in
  `micro-behaviors/crypto/symmetric/aes/mode`. The pattern does not bind the
  buffer to the decipher call.
- A zero-filled buffer followed by computed crypto access belongs in
  `metadata/file/profile/cryptography`.
- The three combinations belong in that same profile directory. File-write and
  detached-option evidence does not by itself establish a process launch;
  `unref` need not refer to a decrypted payload; and the .NET crypto rule can
  match WSH or MSXML property access without an eval call. These profiles are
  notable rather than hostile, and their unsupported ATT&CK/MBC annotations
  were removed.

Matching predicates, platform and file-type scopes, and confidence are
preserved. One local dependency was redirected to the AES mode trait. The
trait and composite IDs and descriptions were corrected; no other YAML or Markdown
file referenced their prior IDs. The destination has 69 direct rules.
