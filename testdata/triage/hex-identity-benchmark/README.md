# ltidisafe second-review controls

ltidisafe 3.6.9 is an npm archive with exactly index.js, test.js and package.json.
Its preinstall command executes test.js and suppresses stdout/stderr. test.js
reads hostname, home directory and username, converts UTF-8 bytes to hex, and
passes each to an HTTP hostname concatenation inside a speed-check helper.
index.js implements the actual HTTP/HTTPS GET and ordinary upload benchmarking;
it contains no identity collection or malicious activation itself. Interface
addresses are enumerated but not sent; the uptime calls are comments.

An isolated QuickJS replay of both original JavaScript files, with mocked os,
Buffer, URL and HTTP modules, captured three GET destinations. Decoding their
first labels recovered reviewer, review-host and /home/reviewer. No live callback
was contacted. The archive digest matches the supplied SHA-256.

Judgments: archive and test.js MALICIOUS; index.js BENIGN; package.json MALICIOUS
because it declares silent execution of the bundled identity-export script.
No malware-family attribution or external conviction is necessary.

The former DNS/encoded Oastify suffix, URL co-occurrence, profile co-occurrence
and inferred-send rules are retired. Existing neutral OOB-host, URL-concatenation
and hex-encoding traits preserve their supported observations. The HTTP identity
flow and install-context composite now live under system-info/identity. Two
broad install-hook co-occurrence composites are replaced by the source-bound
beacon plus preinstall declaration, with the archive description saying ships
rather than asserting an unproven path binding between manifest and sidecar.
The new matcher requires OOB evidence in the actual constructed destination;
an unrelated OOB string cannot provide that relationship. Campaign strings and
function, parameter, buffer, URL and OS alias names are not required. All six
relative orders of the OS import and the two function declarations are covered.

json-body-post no longer treats req.write as proof of POST. Its description
states co-occurrence because even JSON.stringify plus a POST literal does not
bind a specific body to a specific request.

Run the fixtures with python3 testdata/triage/hex-identity-benchmark/check.py.
Positive and renamed code must match; unused sources, disconnected encoders,
fixed destinations, comments and unrelated OOB endpoints must not match.
