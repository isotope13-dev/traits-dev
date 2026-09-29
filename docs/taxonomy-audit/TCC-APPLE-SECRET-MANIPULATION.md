# AppleScript TCC manipulation routing

Three hostile composites in
`objectives/command-and-control/dropper/staging/memory/applescript.yaml`
described compiled AppleScript that writes or saves macOS TCC permission
grants. Their activation behavior is a privacy-control bypass, not executable
memory staging. The taxonomy already defines `objectives/evasion/tcc-manipulation/db`
for changes to TCC consent state.

The composites now live in
[`objectives/evasion/tcc-manipulation/db/applescript-c2.yaml`](../../objectives/evasion/tcc-manipulation/db/applescript-c2.yaml).
Their descriptions, criticality, confidence, ATT&CK mappings, and Boolean
conditions are unchanged. References to AppleScript-specific support traits
are now fully qualified to their existing source directory; this preserves
their original meaning without cloning those atoms. The original file's
`for: [applescript]` and `platforms: [macos]` defaults are preserved exactly.
No other rule referenced the three moved composite IDs.

The `staging/memory` leaf falls **133 → 130**; the existing TCC database leaf
rises to **19**, remaining below the 100-rule cap. The inventory at this migration checkpoint had
79 violating directories and **2,023** excess rules; later shared-tree changes are
reflected in the current snapshot. This is a source-level
reclassification, so the 79-violator count stays the same.

The current-source validator was built using a temporary Cargo patch to the
adjacent `stng` working tree, where the API called by `cleave` exists but is not
yet present in the locked dependency revision. Soft validation found no broken
references; it still reports 89 unrelated validator issues, including 79
over-cap directories. The fixture gate still flags three benign paths in
`pyaigis-top10.tar.xz` against the existing encoded-shell rule. No broad
before/after corpus-parity claim is made for this reclassification.
