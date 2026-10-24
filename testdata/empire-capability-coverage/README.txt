Source-member behavior coverage review

One neutral capability was added: Python invocation of loaded managed code. Existing registry-write and SSPI-loader observations retain SSP installation coverage. Existing hostile and suspicious observations are retained at their original severities.

Run python3 testdata/empire-capability-coverage/check.py from the repository. It scans five positive/near-miss fixtures without executing them.

review.json records every identification, byte-based evidence, verdict reason, deployment limitation, marker note, scan count and classifier gate. counts.csv contains the complete before/after table. marker-lines.txt preserves every one-line marker verbatim for a commit body. Full scans, facts, extracted PE stages and ILSpy/native disassembly evidence are in the scratch directory named by review.json.

The 57 older controls have unchanged emitted findings. Six old expectations already fail with the baseline trait tree; their exact missing IDs are retained in review.json. Five focused new controls pass. Cold native scans resolve the warm-cache Mach-O slice variance without changing any rule.
