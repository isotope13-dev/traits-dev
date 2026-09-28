# Encrypted-stage activation sink audit

Two completed activation chains no longer live in the encrypted-staging leaf:

- `dotnet-encrypted-reflection-loader` moves to `dropper/module-load`. Its
  encrypted decryption evidence is joined to reflection and assembly-load
  evidence, so the runtime module/assembly sink determines its home.
- `powershell-hex-xor-download-execute` moves to `dropper/file-exec`. Its
  decoded ScriptBlock chain is joined to a remote executable download and
  launch. The decoder and ScriptBlock observations remain in encrypted staging
  and are referenced by exact ID.

The .NET injection-configuration composite stays in encrypted staging because
its host-process and persistence strings do not independently establish that
execution is transferred into another process. Its reference to the moved
module-load rule now uses the canonical exact ID. No matcher body, effective
scope, confidence, criticality, or attack mapping changed.

This leaves decoder-only, ciphertext-only, and sink-ambiguous rules in the
encrypted-stage leaf. The split follows the required activation result, not the
language or cipher. The destination counts are checked against the shared
85-rule cap during validation.
