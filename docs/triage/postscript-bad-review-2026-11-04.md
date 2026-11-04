# PostScript mislabeled-bad review — 2026-11-04

Reviewed the single snapshot entry and confirmed its bad label with Hopper. `15f295e6de4f` is not PostScript: it substitutes `!` for `A` and `#` for `T` in Base64 data. Offline decoding yields a UPX-packed Windows executable; unpacking reveals remote-access functionality and a command disabling the Windows UAC policy. Both scanners identify hostile behavior in the decoded executable.

A new finding combines the substituted PE header, UPX marker and encoded network API names in the outer file. Both scanners flag the original and clear a control with the download API marker changed. This rule is specific to the observed substitution and encoded byte alignment, and the encoded API names alone do not prove every similarly shaped executable is malicious.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. No engine features were added.
