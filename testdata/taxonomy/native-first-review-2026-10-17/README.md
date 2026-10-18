These are inert matcher controls. The binary entry points return immediately;
the modeled instructions and references are data, not executed operations.
They test static evidence requirements, not a malware verdict.

Run `python3 testdata/taxonomy/native-first-review-2026-10-17/build.py` to
regenerate the fixtures, then `python3 testdata/taxonomy/native-first-review-2026-10-17/check.py`.

The ELF controls cover a stripped, sectionless buffer-forwarding layout and
remove either sensitive paths, the POST template, or the buffer relationship.
Only the complete conjunction receives a suspicious reporting observation.
The PE control imports GUI, keyboard, clipboard-format, drive enumeration and
resource editing APIs. It receives neutral capabilities, with no hostile
spyware or resource-infector claim. Shell controls distinguish a real SSH
command reference from a quoted grep expression, and a URL-encoded MAC field
from a telemetry claim.

The retired wildcard and resource conjunction moved to filesystem homes.
The unsupported spyware and lateral-drive-infection rules were removed rather
than suppressed by a specimen or family exception. Existing Grenam consumers
now reference the neutral resource conjunction explicitly. See the review in
`triage-reports/2026-10-17-fallout-native-review.md` for code evidence.
