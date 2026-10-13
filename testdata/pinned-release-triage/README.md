# Pinned npm release triage

The reviewed SHA-256 values are `04b9b1f37008acf572e01e2104c542beb0fa1ced24ed65732a9a96cceeea8deb`
(open-walnut 0.6.10) and `ca2fa13344df33b1a41aada55b1972409db1e19ba64fb473b4b115f70988d026`
(agenda-desacoplada 0.0.26). The external firewall pages were unavailable;
judgments use archive content rather than the reported block.

Walnut is a local AI assistant, with a CLI, web service, integration plugins,
cloud synchronization and a bundled dtach 0.9 terminal helper. Its published
postinstall checks an installed Claude SDK version and applies an exact shipped
patch. The patch removes the file-read malware reminder append; it does not
remove file permissions or add a downloader. This unusual, visible dependency
modification is distinct from credential theft. No malicious payload was found.

Agenda is a medical scheduling web component. All three browser bundles carry
SweetAlert2's active protestware: Russian browser language plus a .ru/.su/.by/
.xn--p1ai hostname, localStorage initiation time, a delay exceeding three days,
then disabled body pointer events and looping remotely sourced audio. This
conditional disruption supports MALICIOUS for these bytes without claiming
that every release of Agenda is malicious. Existing three archive hostile
findings and two per bundle remain; precision scores are 7.6 and 6.3 for the
behavior and identity composites.

## Rule corrections

Remove oversized-source plus command/network co-occurrence, unbound metadata
redirect co-occurrence, and credential-path/read/fetch co-occurrence verdicts.
Keep the canonical capability atoms and the argument-bound metadata redirect.
Move source size to file-size metadata. Move generic imports, build declarations,
URL encoding, array formatting, permission tokens, credential representations,
error wording, archive extraction and assignment wording to their neutral homes.
Rewire exact consumers. Remove redundant browser/execution/config groupings;
the config consumer expands its exact OR members. Service and upload groups now
state control/API evidence rather than registration or cloud exfiltration.
Exclude negated destructive instructions from the destructive-goal matcher.

These are coverage/description corrections, not severity-only suppressions.
The long-token measurement no longer excludes interpreter capability, which a
metadata rule cannot depend on. The agent/session wording atom narrows its old
64-type scope to scripts, Markdown and text to meet the destination's type cap.
Removed objective ancestors deliberately lose these neutral members; capability
atoms and exact objective consumers retain their evidence. No new leaf is added.

## Evidence

Both archives were scanned with atomscan and inspected with cleave facts;
JavaScript facts and source inspection establish the bundle behavior. Rizin
identified and analyzed the static dtach executable. binwalk and a JavaScript
runtime were unavailable, so no package or browser payload was executed.
Final archive scans: Walnut 0 hostile / 0 suspicious; Agenda 3 hostile /
0 suspicious, with 2 hostile findings in each of its three bundles.
The six fixtures in cases.json passed all required/forbidden ID assertions.
They cover moved observations, unrelated metadata/redirect co-occurrence and
positive versus prohibited destructive instructions. Full-size archive controls
also confirmed the relocated size finding and removed destructive-goal FP.
