Static review of the 51 requested stranded members. `review.json` records each
identity, SHA-256, execution evidence, verdict, marker, trait counts, calibrated
classifier result, archive-member comparison, and any coverage limitation.
`report.md` provides the per-member count table.

The YAML change admits Mach-O carriers to the existing validated AppleScript
credential-dialog composite. All original predicates, severity, script scopes
and consumers are preserved. The original native sample decodes an osascript
command and passes it to system(); its AppleScript collects and validates the
password before copying secret stores, uploading an archive and persisting.
The decoder was independently reconstructed from the ARM64 instructions:
seed 0x11667, multiplier 0x3785, modulus 35999 from embedded 09:59:59. The
445-line reconstructed AppleScript agrees with the strings recovered by Cleave.
No sample or fixture was executed.

Run `python3 testdata/stranded-native-dialog/check.py` for the retained script
positive and three near misses. Add `--sample <original-Installer-path>` to
verify the native positive. An ordinary masked password dialog, an unmasked
directory-authentication prompt, and a PDF-password dialog do not meet the
composite's combined requirements. The native specimen's targeted debug
trace reports precision 4.5 before and after scope expansion; the final trace and all
scan/facts artifacts are in the task scratch directory.

The keychain-acquisition and sensitive-file-copy consumers, and the AMOS
family exclusion, were inspected. They remain script-scoped, so they do not
inherit the Mach-O expansion. No matcher or severity was weakened. Comparison
scans use `--follow=none` explicitly: the optional-value flag requires the
`=` form. Initial scans with a separate `none` also followed references;
they were replaced by comparable byte-only scans against a git HEAD rules
snapshot and this checkout. Fetched dependencies are not member evidence.

Kali provenance supports authorized testing, but these particular members
implement attack payloads: agent tasking, secret extraction, surveillance,
coercion, exploitation or unauthenticated web command execution. They are not
inert libraries or documentation. MALICIOUS describes their operational
payload role; no unauthorized deployment, configured victim, runtime success,
or unseen final payload is inferred. The working test-directory Mimikatz is
judged from its bytes. The three archive convictions are preserved.

The remaining classifier disagreements and below-three-hostile coverage
limits are recorded individually. Native APIs and ordinary loading, local
output or cleanup are not promoted into independent attack outcomes merely
to increase the count. Marker notes are also copied verbatim into
`current-commit-body.txt` in the scratch directory.

The universal Mach-O archive comparison alternated the x64 and ARM64 XOR
observations. Both slices decode the same script. The standalone member
comparison lost no finding, and neither XOR rule changed. No hostile or
suspicious coverage was lost. The installed model uses feature spec 18 while
the current engine expects 21; this limits classifier coverage independently
of the supported static findings.
