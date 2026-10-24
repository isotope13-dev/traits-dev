This review covers SHA-256 prefixes `09def9c6a536`, `9e55188d8f68`, and
`8c8fb533c231`. The complete reverse-engineering and scan comparison are in
`review.md` and `comparison.json`.

Run `python3 testdata/native-browser-behavior-review/check.py` from the trait
root. The check scans fixtures without executing their contents. It verifies
both required and forbidden findings, independently of classifier scores.

The HTML fixtures exercise Script Encoder column alignment, lower-case percent
hex, irregular NUL insertion, MHTML/scriptlet dependencies, harmless encoded
output, and JavaScript-versus-EXE script sources. Network references use the
reserved `.invalid` domain. The PE controls are generated 1 KiB images containing
only a return-zero stub and string observations; they test a real endpoint and
registry suffix against the actual Brotli-dictionary near miss from the sample.
The C++ control explicitly selects security processes before submitting
PID-bearing requests to CcProtect. It preserves the known driver-termination
technique while excluding unrelated device and numeric-value fixtures.

The native mutation checks in the review additionally operate on temporary
copies of the supplied originals: changed names and string keys retain the
supported attacks; broken entry trampolines, removed execution permissions,
nonzero data buffers, and changed kernel-copy contracts lose only the matching
behavior. No original sample was modified. Extracted or reconstructed binaries,
CPU-emulation scripts, raw reports, and forager provenance remain in the named
scratch directory, outside this trait checkout.
