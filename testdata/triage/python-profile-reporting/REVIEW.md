Both supplied Python scripts are one-shot host-profile reporters. Their complete
module bodies collect OS information, the current username and hostname, serialize
the dictionary to JSON, encode it as bytes, construct a POST request and call
urlopen. The first reports system/release separately; the second uses the full
platform string. Importing either module triggers the request. Neither consumes
the response or contains obfuscation, secrets, persistence or further execution.
Execution with stubbed imports confirmed the exact JSON bodies and one send each,
without contacting the embedded endpoint. Both hashes matched the supplied hashes.

Verdicts: BENIGN under the requirement for concrete hostile evidence. The files
establish automatic reporting to a fixed public IP, but do not establish lack of
authorization. No recognizable product or malware-family identity is supported.

The two hostile composites required no theft, deception or security-boundary
violation. Relocate them to neutral capability leaves, name their co-occurrence
accurately, preserve their required evidence and remove unsupported ATT&CK mappings.
Remove the module-call rule's testing exclusions: the neutral observation is
accurate in test code too.
Move the current-user grouping to process/identity/query and update its three exact
consumer files. Remove python-enumeration: its directory selector can count
multiple HTTP findings toward needs: 3 without proving three surveyed resources;
the existing host-query combination retains the supported query observation.
Add a notable JSON-text-to-bytes encoding call observation.

Ancestor selectors were audited across the four rule tiers. Discovery/profile,
profiled dispatch, infostealer, mixed-source, OOB, credential, install-hook and
trojanized-package consumers must no longer inherit these neutral observations
as attacker-objective evidence; their selectors are intentionally not widened.
The new leaves already exist, with room under the default directory budgets.

cases.json records positive and near-miss controls. The separate-request control
deliberately leaves the JSON request unsent and opens another URL: both neutral
co-occurrence composites still match, demonstrating why neither may claim data
flow or exfiltration. The platform-only enrollment control must not satisfy the
host/user profile combination. References to encoding/user APIs without calls
must not satisfy the new encoding observation or current-user call atom.

Run `python3 testdata/triage/python-profile-reporting/check.py`. The runner scans
temporary copies under the repository root so existing testing-path exclusions
on the external-IP atom cannot mask the positive control. It never executes the
fixture code and requires all five controls to have no suspicious/hostile traits.

The existing benign Entra role-read/secret-rotation fixture also uses
json.dumps(...).encode(). Require the new notable encoding trait there and
increase its score cap from 5 to 6; keep both elevated-criticality limits at zero.
