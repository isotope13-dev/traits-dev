# Native loader review

Ten rules left legacy native-loader staging. The PECompact remote-memory
combination moved to process injection; the x86 file-read, allocation and
XOR/indirect-call combination moved to native payload activation; and the
IP/temp-write/process combination moved to native file execution. Their
specific combined evidence supports the likely behavior without requiring a
proven data-flow link.

The PEB/export dispatch combination moved to runtime import concealment. The
opaque-export memory API and test-brand overlay combinations are PE profiles;
the single x86 byte sequence is an instruction observation. Three empty-text or
nonstandard-entry packing combinations now describe pack detection rather than
asserting a dropper. These packing and API profiles are suspicious. All ten
predicates, file constraints and exclusions were checked against their original
rules, consumers were updated, and the broad legacy dropper consumer retains
the moved members pending its separate weak-evidence audit.

Two adjacent directories were split for future growth. Ten algorithm/structure
variants moved from the 79-rule API-hashing directory to `imports/hash-variants`,
leaving 69. Twenty-two call and dispatch sequences moved from the 88-rule
instruction-sequence directory to `instruction/call`, leaving 66 and bringing
the call directory to 46. Parsed comparisons verified all original 79 and 88
rules and their settings after reference updates. Existing per-file size bounds
were retained; the split supplied no evidence for changing them.
