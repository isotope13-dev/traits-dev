# Scapy outer-scope suppressor controls

These fixtures check that a generic Scapy attribution header cannot establish
UTscapy test-fixture context by itself. Each ZIP contains a JavaScript member
with a base64-encoded, bzip2-compressed PE control payload. The ZIP is analyzed
under Cleave's exact `__cleave_builtin_base64_pe_hook__` basename so the PE hook
is a real candidate for its `unless` condition. The raw
`binary/embedded/base64-bz2` finding must remain present in every case.

The marker matrix tests each source marker alone, no markers, the full
conjunction in one Python source member, and the same markers split across two
members. Only the same-file conjunction may match
`scapy-utscapy-test-fixture-context` and suppress the candidate hook. The
reason-specific assertions in `check.py` distinguish suppression by that
exception from an unrelated `NOT MATCHED` result. The downstream exception
still has outer scope, so its precise member context can protect an archive
payload elsewhere in the package.

The marker conjunction follows the public upstream UTscapy runner: its generic
Scapy header and “Unit testing infrastructure for Scapy” docstring are at the
start of the file, and its `External_Files.UTscapy_js` declaration embeds the
report asset ([upstream source, checked 2026-10-16](https://raw.githubusercontent.com/secdev/scapy/master/scapy/tools/UTscapy.py)).
The fixtures synthesize only those marker strings; they do not claim to be an
authentic Scapy distribution.

Run `python3 testdata/taxonomy/scapy-outer-suppressor/check.py --cleave
../cleave/target/release/cleave` or use `make taxonomy-check`.
