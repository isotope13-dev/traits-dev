# PowerShell file-execution audit

Three legacy `delivery/execute-download` composites require an executable or
installer activation sink and now live in `dropper/file-exec`:

- `powershell-download-exe-execute`: a WebClient EXE download staged to a
  writable path and a `Start-Process` launch;
- `powershell-country-gated-download-execute`: country-selected execution with
  a WebClient reference, executable URL evidence, and `Start-Process`;
- `powershell-msi-programdata-install`: an MSI URL combined with a ProgramData
  `msiexec` install.

No matcher bodies, scopes, or criticalities changed. Local source helpers remain
in `delivery/execute-download` and are referenced by fully qualified IDs. The
separate persistence consumer of `msiexec-programdata-msi` remains at its
original canonical source ID. No external exact-ID consumers of the moved
composites were found.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still
reports catalog-wide issues, including **165 over-cap directories**. The
broader 85-rule audit remains open.
