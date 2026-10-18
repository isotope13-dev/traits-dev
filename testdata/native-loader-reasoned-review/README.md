Run `python3 testdata/native-loader-reasoned-review/check.py <Go-sample.exe>`
from the repository root. `CLEAVE` can select the analyzer binary.

The controls create inert PE/ELF containers in a temporary directory. They
verify the SOCKS stack-store observation against an instruction-byte collision
and a different authentication method, and distinguish SYS_SOCKET from another
socketcall operation. The optional sample argument also exercises three
independent removals: byte transformation, computed-entry setup, and PEB write.
Only the last removal retains the unpacker finding; all remove the image-base
substitution finding. These tests inspect bytes and never launch the samples.

The review and migration rationale is in
[the report](../../triage-reports/2026-10-18-native-loader-reasoned-review.md).
