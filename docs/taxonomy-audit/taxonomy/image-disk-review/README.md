# Disk-image staging review

The 12 rules in `staging/image-disk` were reviewed and moved to the observed
subject or likely behavior. Their match conditions, scopes and confidence were
preserved, and both consumers of the former IDs were updated.

The UDF rules combine separate wide-string markers; they do not establish that
one parsed shortcut targets a DLL carried beside it. The generic .NET resource
and reflection markers do not establish a decoded or executed payload. Those
rules now describe the markers, while document-name and dynamic-evaluation
combinations retain intent-oriented categories. The sparse PDF rule is a
suspicious text-and-layout combination; the DWG double-extension rule requires
an actual listed member. Virtual-disk rules combine mount and document-named
shortcut execution, without claiming the shortcut is bound to that volume.
Unsupported labels such as guaranteed Mark-of-the-Web bypass were removed.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `udf-lnk-bundled-dll-ordinal-loader` | `metadata/file/format/iso/payload::udf-cmd-rundll32-ordinal-text` | suspicious |
| `udf-lnk-shell32-icon-ordinal-loader` | `metadata/file/format/iso/payload::udf-cmd-ordinal-shell32-text` | suspicious |
| `iso-wsh-script-stager` | `objectives/execution/payload/script-eval/transformed::iso-wsh-base64-stream-eval` | hostile |
| `iso-dotnet-resource-stager` | `metadata/file/profile/module-interop::iso-dotnet-resource-reflection-markers` | notable |
| `iso-dotnet-base64-resource-loader` | `objectives/execution/lure/document::iso-document-exe-dotnet-resource-markers` | suspicious |
| `iso-vb6-helper-stager` | `objectives/execution/lure/document::iso-document-exe-vb6-helper-markers` | suspicious |
| `iso-single-pdf-executable-lure` | `objectives/execution/lure/document::iso-sparse-pdf-exe-text` | suspicious |
| `iso-single-dwg-executable-lure` | `objectives/execution/lure/document::iso-sparse-dwg-exe-member` | hostile |
| `iso-hidden-powershell-dynamic-stager` | `objectives/anti-static/obfuscation/eval/dynamic::iso-powershell-stride-dynamic-call` | suspicious |
| `virtual-disk-document-lnk-execution` | `objectives/evasion/masquerade/extension/double::virtual-disk-document-lnk-execution` | hostile |
| `downloaded-virtual-disk-document-lnk-execution` | `objectives/evasion/masquerade/extension/double::downloaded-virtual-disk-document-lnk-execution` | hostile |
| `virtual-disk-document-lnk-cleanup` | `objectives/evasion/masquerade/extension/double::virtual-disk-document-lnk-cleanup` | hostile |
