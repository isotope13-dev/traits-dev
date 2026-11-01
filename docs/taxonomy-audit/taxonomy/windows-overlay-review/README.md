# Windows overlay staging review

Four rules moved to `metadata/file/profile/overlay`: XOR-decoded API names
with allocation-like bytes and module-path/overlay clues; unsigned overlay
with at most one imported DLL and API-hash/memory/thread clues; unsigned
low-import overlay with memory/thread clues; and signed overlay with file,
memory and thread API clues. These observations do not establish encryption,
a specific imported DLL, payload staging or execution. Their severity is
suspicious rather than hostile. The Vidar rule's existing dependency was
redirected to the one-DLL profile.

The Canonical version-resource claim with module-path and overlay clues moved
to `objectives/evasion/masquerade/identity/vendor`, retaining a suspicious
masquerade finding without asserting that the overlay is encrypted or loaded.
The adjacent version-resource-claim directory had 85 direct rules. Thirteen
Microsoft and Windows component identity claims were moved into a sibling
`version-resource/component-identity` directory, leaving 72 direct rules in the parent. The moved rules and
their local relationships are unchanged; fully qualified consumers were
updated. No directory-wide references to the old claim path were found.
The adjacent Microsoft utility directory also had 86 direct rules. Four
diagnostic utility groups (15 rules) moved to `version-resource/diagnostics`,
leaving 71 utility rules. The one directory-wide positive consumer now names
both directories; individual references were redirected.

Four unrelated 1 MiB whole-file minimums were removed. For the Canonical
profile the overlay metric itself still requires 1,000,000 bytes; the former
whole-file threshold was 1,048,576 bytes. The signed profile already requires
64 KiB of noncertificate bytes. The other overlay alternatives require at
least 80 KiB. These changes can expand detection to smaller matching files.
The generic 80-import exclusion was redundant with the retained 25-import
exclusion on the low-import profile and was removed. Other suppressions,
conditions, platform and file-type scopes, and confidence remain unchanged.

The two module-path profiles depend on `pe-module-path-large-overlay`, which
still has a 5,000,000-byte maximum and has many other consumers. That shared
limit was not changed in this review. Unsupported execution/encryption attack
annotations were removed; the Canonical claim retains masquerade attribution.
