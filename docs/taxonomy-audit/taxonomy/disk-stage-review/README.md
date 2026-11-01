# Disk staging review

The five `staging/disk` rules moved by behavior or observed evidence; their
matching predicates, scopes and confidence are unchanged. Java ProcessBuilder
and output-redirect references do not establish that a particular executable
was written or launched silently. A C six-bit macro with write-mode open and
`system()` does not alone establish a decoded payload. AES decryption, module
resolution, file writing and unlinking can be ordinary file processing; the
OLE combination can match an embedded PE with an egghunter or decoder rather
than a file drop. The Node Base64 and hidden Python-spawn combination retains
its hostile severity and its execution behavior.

The `spawn/runtime` directory was near its cap. Twenty-two remote fetch and
launch rules moved into `spawn/fetch`, leaving 59 in runtime and 22 in fetch.
The moved rules preserve their predicates, scope and metadata. Six broad
fetch-and-launch combinations were adjusted from hostile to suspicious or
notable because download and launch alone can describe normal installation;
stronger combinations such as defender exclusion retain their existing rating.
Other remote-looking runtime rules remain for review.

| Former disk ID | Destination ID | Criticality |
|---|---|---|
| `decoded-blob-dropped-and-shelled` | `metadata/file/profile/file-write-context::c-mask-write-mode-system-profile` | notable |
| `java-inetcache-silent-exe-stager` | `objectives/execution/payload/file-exec/spawn/runtime::java-inetcache-exe-process-references` | suspicious |
| `node-cross-package-aes-stage-cleanup` | `metadata/file/profile/encoding::node-aes-module-write-unlink-profile` | notable |
| `node-base64-inetcache-hidden-python-stage` | `objectives/execution/payload/file-exec/spawn/runtime::node-base64-inetcache-hidden-python-stage` | hostile |
| `ole-embedded-pe-file-dropper` | `metadata/document/ole::ole-embedded-pe-shellcode-evidence` | suspicious |

The fetch rules whose ratings changed are `download-execute-csharp`,
`python-google-drive-jar-dropper`, `node-https-materialize-detached-launch`,
`powershell-github-release-exe-launch`,
`powershell-webclient-pythonw-script-dropper`, and
`powershell-webclient-wscript-script-dropper`.
