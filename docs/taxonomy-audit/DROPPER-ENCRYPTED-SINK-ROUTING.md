# Encrypted-stage chains follow their activation sink

The encrypted-stage review found complete chains whose source happened to be
encrypted but whose defining behavior was their required activation sink. The
PowerShell evaluation chains now live in `dropper/script-eval/`; the two
PowerShell `AppDomain.Load`/assembly-load chains live in `dropper/module-load/`;
and seven direct executable launches live in `dropper/file-exec/spawn/`.

The moved script-evaluation rules are `ps-aes-iex-stage-loader`,
`ps-aes-chunked-stage-loader`, `ps-document-masquerade-stage-loader`,
`ps-encoded-xor-eval-stage-loader`, `ps-custom-base32-stage-loader`,
`ps-base64-rc4-gzip-stage-loader`,
`ps-task-argument-keyed-scriptblock-stager`,
`ps-remote-base64-xor-inmemory-loader`,
`powershell-hex-xor-scriptblock-loader`, and
`errtraffic-code-verification-xor-loader`. The module-load rules are
`ps-encrypted-gzip-managed-memory-loader` and
`ps-remote-rc4-appdomain-loader`.

The file-spawn rules are `temp-exe-dropper-launcher`,
`chacha-bndl-temp-exe-dropper`,
`dotnet-encrypted-resource-hidden-process-stager`,
`java-fernet-python-stage-dropper`,
`special-folder-encrypted-overlay-dropper`,
`vscode-encrypted-stage-dropper`, and `vscode-hidden-python-stage`. The
unrelated VS Code CI-gated fetch remains in its source file because it has no
activation sink. Decoder-only and encrypted-container observations also remain
in staging until a narrower behavior is supported.

For all 19 moved composites, the migration precheck compared parsed rule fields
and inherited defaults before and after. They were unchanged; local references
that crossed the new file boundary were made fully qualified. External
consumers were updated in the PowerShell download-execute composite, the
PowerShell transient-script cleanup rule, and the pirated-loader masquerade
rule. A synthetic AES-decrypt/IEX PowerShell sample and an encrypted VS Code
file-spawn sample each matched the relocated canonical rule with all required
conditions satisfied.

The 100-rule inventory is refreshed in the current snapshot. This pass reduces
the encrypted staging leaf by 19 without deleting or weakening a matcher; the
leaf still exceeds the cap and its remaining rules require source-by-source
review. See [the earlier 7z sink audit](DROPPER-7Z-SPAWN-SINK.md) and the
[plan](PLAN.md) for the separate passworded-7z correction and current counts.
