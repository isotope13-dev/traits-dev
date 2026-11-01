# Retired dropper compatibility placeholders

The `objectives/command-and-control/dropper/compat` leaf contained three
unreferenced synthetic missing-rule sentinels and a fourth sentinel masquerading
as a Git Bash observation. It contained no real matcher for those claims.
The three unused sentinels and the empty defaults file were removed. The Git
Bash sentinel was removed from the ComfyUI masquerade rule, whose other
deserialization, network and family-specific alternatives remain. Its only
other consumer required that sentinel and was therefore dead; it was removed as
well. No YAML references to the retired leaf remain.

This removes synthetic sentinel matches; it does not replace them with a
guess about what a missing Git Bash rule was supposed to detect.
