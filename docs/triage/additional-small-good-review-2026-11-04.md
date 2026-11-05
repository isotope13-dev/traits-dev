# Additional small pools, 2026-11-04

`c7b9bd9c1560` and `853af2cc4860` are EvoPhylo and SCArray.sat R package
archives. Their local slow scans reported no suspicious or hostile findings.
Endpoint rulings: good.

`479a810e825c` is a 1 KiB Gentoo package-format recognition fixture. Its
partial extraction is a neutral observation, and it has no suspicious or
hostile findings. Endpoint ruling: good.

`1216bc2f0106` is a sample iOS archive containing a Go Mach-O program. Its
bundle identifies an example app, its build metadata identifies the local
does-nothing test program, and its scan has no suspicious or hostile findings.
Endpoint ruling: good. The other iOS-pool archive remains under review.

`87cce084656b` is Donut x64 shellcode with an embedded executable. The
instance was decrypted statically using the loader's algorithm, without
executing it. The recovered Windows executable imports only MessageBoxA and
ExitProcess; its entry point displays `Hello from Donut` and exits. The
recovered PE scans cleanly. A new suspicious observation identifies the exact
Donut loader template in the original carrier; a mutation of that template
does not match. Endpoint ruling: good, with that single justified finding.

Validation passed and Hopper confirmed all five good labels (no-ops).
