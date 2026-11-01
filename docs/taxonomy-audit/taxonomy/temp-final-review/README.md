# Final temporary staging review

The remaining rules in `staging/temp` were reviewed and the leaf was retired.
Nine rules were moved, retaining their match conditions, scopes and confidence;
an unreferenced dummy rule matching a fabricated marker was removed. Descriptions
and criticalities were revised to distinguish API and path co-occurrence from
confirmed payload staging or execution. Unsupported ATT&CK labels were removed.

The Notepad format is a command template, and the `bin64/msvcr120.dll` path is
a Microsoft runtime reference, not evidence of a particular compiler bundle.
The latter has a matcher-specific validator exception: the meaning of the path
does not depend on the file size. The Nuitka profile is notable because its
resource and process APIs can be ordinary one-file runtime behavior. The
service, temporary file, launch and continuous-ping combinations are suspicious
leads; they do not assert that the referenced APIs are bound to one data flow.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `temp-notepad-quoted-launch-format` | `micro-behaviors/process/argument/executable::notepad-placeholder-launch-format` | notable |
| `dmd-msvcr120-runtime-dll` | `well-known/lib/runtime/compiled/msvc-runtime::bin64-msvcr120-path` | notable |
| `unsigned-admin-nuitka-onefile-dropper` | `metadata/file/profile/installer-layout::elevated-unsigned-nuitka-resource-api-profile` | notable |
| `self-copying-temp-pe-dropper` | `objectives/execution/payload/file-exec/spawn/native::temp-self-read-write-pe-launch-profile` | suspicious |
| `dotnet-temp-embedded-pe-dropper` | `objectives/execution/payload/file-exec/spawn/native::dotnet-temp-embedded-pe-launch-profile` | suspicious |
| `mingw-temp-exec-ping-beacon-dropper` | `metadata/file/profile/command-options::mingw-temp-ping-command-profile` | suspicious |
| `mingw-temp-notepad-ping-beacon-dropper` | `metadata/file/profile/command-options::mingw-temp-notepad-ping-command-profile` | suspicious |
| `overlay-self-read-service-dropper` | `objectives/persistence/system/service/install::overlay-service-create-dispatch-profile` | suspicious |
| `drive-walker-temp-pe-stack-dropper` | `objectives/execution/payload/file-exec/spawn/native::multi-pe-drive-temp-write-launch-profile` | suspicious |
