# PyInstaller runtime staging review

Nine rules moved from the legacy runtime-staging category. Their conditions,
scopes, confidence and exclusions are unchanged. PyInstaller, psutil, PyArmor,
numbered sidecars and an embedded utility do not establish theft: none of the
former stealer rules required collection of sensitive data or a transfer. They
now describe the bundle, archive, system-management or certificate observations
and have notable or suspicious severity. Unsupported theft and download labels
were removed.

The two decoded-RAR combinations remain suspicious staging-reconstruction
leads because their underlying rule includes a decoded archive and bootloader
runner. A vendor certificate whose digest no longer matches is reported as a
signature anomaly alongside bundle evidence; it does not alone establish a
hostile payload. Other legacy runtime files remain for review.

| Former ID | Destination ID | Criticality |
|---|---|---|
| `pyinstaller-pe-stealer` | `metadata/build/bundler/runtime::pyinstaller-psutil-embedded-exe` | notable |
| `pyinstaller-pyarmor-sidecar-stealer` | `metadata/build/bundler/runtime::pyinstaller-psutil-pyarmor-sidecars` | suspicious |
| `pyinstaller-pyarmor-staged-psutil-stealer` | `objectives/execution/staging/reconstruct::pyinstaller-psutil-pyarmor-decoded-rar` | suspicious |
| `portable-zip-pyarmor-psutil-stealer-bundle` | `metadata/archive/layout::portable-python-pyarmor-psutil-bundle` | notable |
| `pyinstaller-windows-capability-stealer` | `metadata/file/profile/system-management::pyinstaller-autohotkey-system-api-profile` | suspicious |
| `pyinstaller-pyarmor-embedded-exe-sidecar` | `metadata/build/bundler/runtime::pyinstaller-pyarmor-exe-sidecar-profile` | suspicious |
| `pyinstaller-pyarmor-xor-sidecar-stage` | `metadata/build/bundler/runtime::pyinstaller-pyarmor-xor-sidecar-profile` | suspicious |
| `pyinstaller-pyarmor-bootloader-rar-stage` | `objectives/execution/staging/reconstruct::pyinstaller-pyarmor-bootloader-rar-clues` | suspicious |
| `pyinstaller-embedded-tool-carrier` | `metadata/signed/certificate/signature::pyinstaller-digest-mismatch-embedded-tool` | suspicious |
