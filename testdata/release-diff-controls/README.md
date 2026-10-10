Release comparison triage
=========================

Tuist macOS host bootstrap 33909c11f299: BENIGN. Compared all six module
files against f6724f7ce2a7c91cfa74567fb025b3f501cf8d85 (2026-09-07),
fetched individually from raw.githubusercontent.com/tuist/tuist. The relevant
change replaces Python kcpassword verification with an od-based prefix check
and extracts the auto-login script for tests. Unrestricted sudo provisioning
and variable-backed defaults writes already existed. These are explicitly
operator-run host configuration, not evidence of a privilege exploit or
preference payload persistence. No new unsolicited download or execution was
introduced. The root commit changes an unrelated dashboard.

Ensomedia Security 1.1.13: BENIGN. Compared the complete archive with
https://downloads.wordpress.org/plugin/ensomedia-security.1.1.12.zip.
The release adds protection-setting reauthentication, bounded scan and cloud
responses, safer serialization and checksum token validation, integrity-chain
anchoring, quarantine/path checks, and scanner false-positive fixes. Activation
installs the database and schedules workers. The false backdoor composite
pooled the activation hook, a loopback worker POST to admin-ajax.php, and a
checksum documentation example /tmp/.x in different files. It did not establish
an activation-to-remote-send relationship. No malicious delta was found.

Both older snapshots also fire the original rules. Thus the claim that these
specific older releases are detection-free could not be reproduced; these are
rule errors, not evidence that the release delta introduced malicious behavior.

The migration manifest at /version-drift-migration.json records old/new IDs.
Exact consumers were rewritten, including local consumers; ancestor selectors
are intentionally not expanded to include newly neutral metadata/capabilities.
Matchers and scope are preserved except recorded matcher corrections, removal
of unsupported ATT&CK/MBC claims, and narrowing documentation types. Terms,
imports, source contexts and security-feed references no longer claim software
identity or malicious intent. Actual API calls, permissions, process execution,
network traffic and encodings remain notable or higher. Quoted scanner examples,
translation catalogs, plist text and comments are distinguished from operations.

Baseline validation passed all fixtures. The activation-telemetry fixture moved
to purgatory has a hidden-file gate and sends site/version/admin-email fields;
no remote command, remote code execution or credential payload is established.
Its prior hostile expectation depended solely on the retired pooled composite.
Other hostile corpus expectations are retained, including argv-based systemctl
calls. No sample-name or release-specific suppression was added.

Run python3 testdata/release-diff-controls/check.py for focused positive and
negative controls outside testdata, avoiding test-context exclusions. The
additional source files document neutral observations and execution contrasts.
Final atomscan scans of both complete archives report zero hostile and zero
suspicious traits. Earlier source and full release diffs and scan/facts evidence
are retained in the supplied scratch/version-drift directory.
