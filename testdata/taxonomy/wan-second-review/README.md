# setWAN second review

Reviewed the complete source and `cleave facts` for these SHA-256-identical
copies of the existing WAN injection fixtures:

| Sample | SHA-256 prefix | Verdict | Hostile before/after | Suspicious before/after |
| --- | --- | --- | --- | --- |
| setwan-wire.py | b0f873c763c4 | MALICIOUS | 2 / 2 | 2 / 2 |
| setwan-pptp.js | 78c88c3272b9 | MALICIOUS | 2 / 2 | 2 / 2 |
| setwan-ppp.py | 1ce4984d550f | MALICIOUS | 2 / 2 | 2 / 2 |

All three immediately submit an authenticated command-injection attempt to an
operator-supplied router. A vulnerability assessment is a plausible use, and
these copies are test fixtures; authorization and deployment circumstances are
unknown. The operational request, executable payload, and lack of a dry-run or
target restriction tip the artifact judgment toward malicious exploit code.
The fixture directory's label and classifier output did not establish behavior.

## Execution and effects

The wire variant connects to argument 1 on TCP port 80, constructs the complete
POST /goform/setWAN request, calculates Content-Length, sends it, and prints up
to 1024 response bytes. Its hardcoded Basic credential decodes to admin:1234.
Percent decoding the body produces wanMode=2 and
pppUserName=`|id > /tmp/marker #`. The Host header is a placeholder, not a
callback destination; the socket connects to the supplied host.

The Python PPP variant obtains a target and credentials from arguments 1–3,
form-encodes the same PPP payload, Base64-encodes user:password for Basic
authentication, opens the constructed POST Request with a five-second timeout,
and prints the status. Mocked socket and urllib endpoints captured both Python
requests without network access and confirmed the exact decoded forms, target,
headers, and length. No shell command was run by the analysis harness.

The JavaScript PPTP variant reads target/user/password from process.argv,
constructs URLSearchParams with wanMode=3 and
pptpUserName=`|id > /tmp/marker_pptp #`, builds the Basic header using Buffer
Base64 encoding, calls fetch with POST and that body, then prints the status.
The entire JavaScript path was traced statically; Node is unavailable here.
URL escaping and credential Base64 are protocol encoding, not hidden stages.
There are no archives or extracted stages in these three inputs.

The [original disclosure](https://seclists.org/fulldisclosure/2026/Oct/29)
identifies the corresponding Edimax BR-6478AC v2.20 handler and describes the
unquoted `echo %s > /tmp/UserName` sink. The pipe runs id, its redirect captures
the identity in a marker, and the hash comments out the handler's suffix.
PPP sink replication and static PPTP analysis are distinguished in that source;
these scripts do not establish device-side execution success or privilege
escalation. A successful settings submission can also change stored WAN
configuration, but no supplied firmware or sample-side config API supports an
additional static configuration-damage trait. The advisory corroborates the
mechanism, not whether a particular deployment was authorized.

## Trait changes and retained coverage

The two hostile findings describe username shell injection and suppression of
the shell suffix. The two suspicious findings describe the credential-bound
separator/output redirection and its trailing comment. Their names, matchers,
criticalities, and coverage are retained. Only two distinct hostile behaviors
are supported; an extra hostile trait for networking, authentication, encoding,
or the marker would duplicate or overstate that evidence. No hostile matcher
limitation prevents covering another demonstrated attack stage.

Added a notable Basic Authorization concatenation observation that matches both
Python add_header arguments and JavaScript header map entries. It requires the
header name adjacent to the Basic value; standalone Basic text, unrelated
Base64 operations, and Bearer headers do not match.

Moved urllib-urlopen-bound-as-response from http/download/write to
http/client/exchange, retaining its matcher, scope, confidence, and notable
criticality. The unsupported old directory claim was a saved file: setwan-ppp
only reads response.status. The file-writing consumer still requires its own
write evidence. Audited exact and ancestor selectors: the direct script-write
consumer and the response-acquisition group selecting download/ both now
reference the moved atom. Other HTTP ancestor memberships remain unchanged.

The only lost ID in the three-sample differential is the moved response atom's
old path; its observation survives under the new path. All attack findings
survive. The wire report is unchanged; PPTP and PPP each gain Basic-auth
coverage. Independent existing unsafe-YAML-fetch and ordinary form-submission
controls exercise response binding; a saved-source control exercises retained
file-write coverage. All five existing WAN attack positives and seven benign
near misses, plus all three substitution/newline controls, are included in check.py.

The classifier reports BENIGN before and after for all three (class 0 in each
model route), despite retaining both hostile findings. Model v18.18 also warns
that its feature specification is v18 while the engine expects v21. Raw model
prob values before/after: wire 0.9935736/0.9935736, PPTP
0.9918655/0.99298656, PPP 0.99529415/0.99521756. The rule/classifier disagreement
is reported as a remaining classifier gap, not corrected with duplicate traits.

Run `python3 testdata/taxonomy/wan-second-review/check.py --scratch <scratch-dir>`
for focused controls. The download positive runs outside the shared rule's
test-directory exclusion; the response-acquisition grouping is checked through
test-rules because pure any-groups are filtered from ordinary scan output.
