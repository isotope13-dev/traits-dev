First reasoned review of the three native samples listed in review.json.

The verdicts come from instruction/data-flow inspection with Rizin and
Capstone, PE structures and imports, and cleave facts including decoded
strings. Original and final atomscan reports and disassembly were retained
in the task scratch/native-review directory. The supplied sandbox URLs were
unavailable through the browser tool; their scores were not used as proof.
No sample code was executed and no embedded server was contacted.

The fixture entry point is RET. Signature bytes after it are inert and only
test matcher relationships. A matched hostile composite in a synthetic
fixture is not a malicious verdict for that fixture.

build_controls.py reproduces the PE64 controls without a compiler. check.py
regenerates them under neutral filenames outside testdata and checks severity,
correct API-call binding, disposition-buffer identity, SEC_IMAGE, context
register offset and directive/task-prefix false positives. Run:
  python3 testdata/native-first-review-2026-10-17/check.py

The ghosted-section matcher now binds both the FileDispositionInformation
call and nearby SEC_IMAGE creation to their actual imported API slots, rather
than requiring a release-build diagnostic. The composite additionally requires
a CONTEXT.Rcx store bound to SetThreadContext and the ResumeThread import.
The new context atom describes a register rewrite, not an entry-point proof.
The byte-level relation is compiler-shaped but contains no sample-specific
addresses, filenames, domains, exact file sizes or configuration identifiers.
