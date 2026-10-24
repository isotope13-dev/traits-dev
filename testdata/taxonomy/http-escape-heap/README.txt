Static controls for the PoolSlip / Rift rewrite-engine chain

Article:
https://www.opswat.com/blog/cve-2026-9256-cve-2026-42945-chaining-two-nginx-rewrite-engine-vulnerabilities-into-remote-code-execution
Linked primary research:
https://blog.verichains.io/p/two-bytes-to-rce-chaining-rift-poolslip
Recovered original source:
https://raw.githubusercontent.com/y198nt/Nginx-chain-Rift-Poolslip/main/exp_official.py
SHA-256: 61134eacd9eab73198ab5b120889f5030008ec42ea319dd6d5c18f1d8afbe486

The original source and Forager provenance are retained in task scratch.
These small fixtures preserve construction mechanisms while changing route
names, repetition counts, pointer offsets, and local variable names. Ruby
and JavaScript controls cover equivalent source operations. They are inert
function definitions; the checker analyzes them without executing them.

The hostile findings require both crafted escape-expansion HTTP requests
and repeated system-address/argument/zero-tail records. Pointer-disclosure
classification additionally requires integer reads and low-bit clearing.
Ordinary uploads, plain plus-heavy requests, arbitrary application records,
and isolated little-endian parsing must not receive hostile findings.

The low-word redirect is suspicious: serialization and 64 KB mask syntax
co-occurring with the exploit mechanics do not prove a successful overwrite.
The two-byte serializer binds both output bytes to the same source value;
unrelated-bytes.py checks that two different inputs do not satisfy it.
non-null-tail.py checks the distinguishing terminating-word constraint.
The adjacent-record controls ensure that unrelated calls cannot supply
either the callback layout or its repetition through proximity alone.
record-only.py checks that suspicious record construction alone cannot
satisfy either hostile HTTP exploit rule. JavaScript's read/repeat
operations alone likewise do not establish the callback-forgery chain.

The mask predicates are source-syntax observations. They do not assert that
their operands are pointers. The system-address packing observation remains
in its existing canonical integer-codec home. No detection relies on a CVE,
NGINX version, ASLR offset, endpoint name, or research file basename.

Run from the traits root with an external temporary work directory:
python3 testdata/taxonomy/http-escape-heap/check.py --work-dir <scratch>/controls

Limitations: same-file evidence is not data flow or runtime execution.
Compiled or obfuscated clients, alternative byte/ABI layouts, and unmodeled
aliases for system addresses remain outside this coverage. Source matching
does not validate allocator grooming, successful ASLR defeat, or RCE.
