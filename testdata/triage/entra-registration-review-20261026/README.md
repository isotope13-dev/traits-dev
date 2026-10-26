All three supplied samples are **MALICIOUS** on their implemented behavior.
Original bytes were hashed and left unchanged. Atomscan and `cleave facts`
ran on every original; specimens were inspected statically and never executed.
Raw before/after reports, facts, extraction, annotated native disassembly,
CIL, isolated assembly scans and prepared commit-body lines are in the scratch
path recorded in `review.json`.

| Sample | Distinct H before → after | Distinct S before → after | ML probability before → after |
| --- | ---: | ---: | ---: |
| e087636adeec — Go infector / GravityRAT GX | 11 → 11 | 3 → 3 | .995 → .995 |
| 22e500686682 — token-spray.mjs | 3 → 4 | 1 → 1 | .996429 → .996939 |
| 91b880f32a74 — token-replay-mfa.py | 3 → 5 | 1 → 1 | .994584 → .998761 |

Counts include embedded members. The PE has 21 analysis units and retains
83 hostile / 32 suspicious occurrences, with every member's traits unchanged.
The two scripts each have one unit. All original hostile/suspicious coverage
survives after accounting for the renamed MFA replacement finding. Classifier
alerts agree with the judgments; matched alert levels are 25 → 25,
1750 → 1750 and 5000 → 0 respectively. Models report feature specification v18
while the engine expects v21; probabilities are diagnostic, not verdict evidence.

The Go PE's pclntab at raw 0x3f5920 identifies 4,842 functions. Independent
native disassembly resolves `main.main` (VA 0x62d190) into self-image reading,
generation/hash/path reporting through HTTP GET, three startup-copy attempts
and a `C:\Program Files\` walk. `main.visit` (0x62c450) reads a visited file,
constructs mutated self bytes, overwrites that path through `ioutil.WriteFile`,
and writes an additional `.exe` variant. These modifications have no ordinary
updater or installation boundary. `plant_start_up` (0x62cba0) writes random
executable names under System32; `add_startup` (0x62cae0) opens the HKLM Run key
and writes the copied path. Actual privilege and write success are unknown.

`get_self_mutated_bytes` (0x62cf80) Base64-decodes a 0xd705c-byte constant at
raw 0x2ca606, appends the decoded bytes to its input image, and adds random
padding. The decoded buffer is 660,549 bytes; its first 660,480 bytes are
LSASS 1.09.1201.10 and hash to
`1c0ea462f0bbd7acfdf4c6daf3cb8ce09e1375b766fbd3ff89f40c0aa3f4fc96`.
That exact GX hash and the configured C2 protocol are corroborated by
[Talos's published GravityRAT analysis](https://blog.talosintelligence.com/gravityrat-two-year-evolution-of-apt/).
The Go entry path does not establish execution of this appended image.

CIL traces LSASS `Program.Main → Initialize → Services.Start → RootJob/TaskJobs`.
The root job sends identifiers, domain, OS and VM information through
`Agent.SendBasicInformation → WebClient.UploadValues`. A 300,000 ms timer polls
for task records; the task switch passes received Args to `CmdManager.Start`,
which invokes hidden `cmd.exe /c`, redirects output to a report, then uploads
that report through `UploadManager → Agent.UploadFile → UploadFileTaskAsync`.
Other task branches collect and upload netstat, process and service reports,
extension-filtered disk documents, and staged files from logical-disk arrival
notifications. Successful report/staging uploads can delete the local staging
copy. Ordinary process/service inventories alone do not establish theft;
the traced tasking and upload paths do. Existing command, document, identity,
network, process, software, VM-probe and family detections cover these paths.

The reviewed entry/task paths do not establish invocation of the separate
KillJob batch-cleanup writer or resource-launch helpers. The FileName and Bytes
resources contain only a UTF-8 BOM. The `~important` ZIP contains document-icon
assets. No cleanup execution or new payload launch was inferred from those
helper names. The real Mono.Cecil DLL was extracted separately and has zero
hostile/suspicious findings before and after. Some extraction labels call the
containing LSASS image Mono.Cecil; that label does not make the implant a benign
library. No dependency or filename exception was introduced.

The JavaScript reads newline-delimited records from `TOKEN_FILE`, exchanges
each supplied refresh token as Office, then exchanges a returned refresh token
as Authentication Broker for the DRS resource. Its successful-token branches
attempt a Graph device POST and submit an enabled inbox rule with empty
conditions plus markAsRead/delete actions. There is no mail selection or
interactive confirmation. Bulk credential replay combined with unconditional
mail concealment tips the judgment toward malicious use. The source does not
prove the input tokens were stolen or identify their original owner.

The Python likewise reads caller-supplied token records and replays them as
first-party clients. It lists every Authenticator and phone method and issues
DELETE requests for each, then POSTs an Authenticator-shaped replacement and
attempts DRS enrollment. Removing the victim's factors and attempting retained
access are concrete hostile actions even if replacement fails. A help-desk
reset is a benign explanation for the same API primitives; the bulk replay
and unfiltered factor removal make that explanation less likely here. No
organization, operator authorization, authorship or deployment context is known.

Both scripts' registration findings describe **requests/attempts**. Microsoft's
[Authenticator method reference](https://learn.microsoft.com/en-us/graph/api/resources/microsoftauthenticatorauthenticationmethod?view=graph-rest-1.0)
lists read/list/delete operations and no creation operation. The JavaScript
uses the DRS token as authorization for Graph's device endpoint, whose
[documented creation API](https://learn.microsoft.com/en-us/graph/api/device-post-devices?view=graph-rest-1.0)
has its own audience, permission and role requirements. No accepted enrollment,
new device certificate, successful replacement, MFA satisfaction or policy
bypass is claimed. No live cloud requests were made during review.

Changes and precision checks:

- Added device-registration persistence after bulk replay and DRS redemption.
  New notable request predicates bind target and method at the same call.
  GETs, POST text inside a GET options body, quoted request examples and ordinary
  provisioning without replay do not establish this hostile behavior.
- Added MFA-method removal under authentication security bypass, independently
  of replacement. DELETE is bound to the method path; a nearby unrelated
  device DELETE cannot supply it. The deletion-only control retains this
  attack coverage while correctly losing the replacement claim.
- The old replacement matcher required DELETE evidence plus an endpoint or
  OData type; it could label deletion/listing alone as registration. It now
  requires a real replacement POST and an MFA DELETE request. Its new name and
  description distinguish attempted replacement from a successful wipe/join.
  The existing help-desk reset remains suspicious, with no hostile finding.
- DRS redemption formerly accepted a Graph devices endpoint as proof of a DRS
  token request. It now requires the DRS resource identifier. A Graph-only scope
  with an enrollment URL no longer supplies this unsupported claim; all three
  existing attack fixtures retain real DRS coverage.
- Generic OAuth fields moved from device-code to token-auth. The Python
  token/JSON-POST composite now states proximity rather than claiming the
  token pair enters the POST body. Generic requests.delete moved to HTTP DELETE.
  The old Graph DELETE proximity profile remains as an explicitly named neutral
  co-occurrence observation, separate from the new bound request predicates.
- Reviewed the existing 100-rule POST leaf before adding six predicates. Six
  observations that do not require POST moved to their actual subjects: Go
  data.Set/data.Encode symbol names; a JVM setDoOutput member reference; DEX
  setDoOutput name and HttpURLConnection descriptor; and Java/Kotlin doOutput
  configuration syntax. Matchers, platforms, file types and exclusions are
  unchanged, and exact consumers were updated. The two DEX references rose
  from component to notable; unsupported HTTP technique mappings were removed.
  `placement-moves.json` records the effective definitions. The POST leaf
  remains at 100 rules. No new taxonomy partition or global budget was added.

The shared-consumer comparison covers 56 existing Java/Kotlin artifacts and
137 units outside this sample batch: all 126 hostile and 67 suspicious
occurrences are unchanged. Actual bytecode setDoOutput positives and source
configuration positives retain their observations and attack consumers.
Additional controls show that PUT body configuration and custom Go data.Set /
data.Encode methods do not by themselves establish POST. The ordinary POST
control retains its request detection. No technique was erased on the basis of
a synthetic near miss, and no severity was reduced to influence a score.

`python3 testdata/triage/entra-registration-review-20261026/check.py` passes
18 controls and 76 assertions. Its inputs are statically scanned and never
executed. Checks cover existing Python/Node/PowerShell attack fixtures,
method/target separation, DRS scope, ordinary administration, quoted syntax,
reference placement and retained POST coverage. Detailed before/after findings,
member counts and classifier values are in `review.json`. There are no material
attack-detection losses or remaining verdict disagreements. Source-flow gaps
reported by Cleave were resolved for the relevant paths through manual review.
The final required repository check is `make validate`; its output is retained
as `validation.log` in scratch.

Exactly one `.MALICIOUS` marker was written beside each original. The following
lines are also copied verbatim into the prepared commit body:

```text
Go infector + GravityRAT: overwrites files; Run keys and data theft
Token spray JS: token replay and mail hiding; detect device POST
MFA token replay: deletes factors; detect removal and device POST
```
