# Ivanti JavaScript/TypeScript second review

The reviewed samples are byte-identical to `ivanti-fetch.js` and
`ivanti-axios.ts` in this regression corpus:

| File | SHA-256 |
| --- | --- |
| ivanti-fetch.js | 1fc4cd5e92d8ac15691a710bd6638d97558e04517878d3f1ced00631c97d7bcb |
| ivanti-axios.ts | c71f8b26d11ad8eec30a4391db1e0d952a72c1ccc036fa2949c9330e0d4f777d |

Both are standalone exploit clients. `route()` runs at module scope. The
operator supplies the target base URL, temporary filename digest, and POST
body through arguments 2, 3, and 4. The first request targets the public login
URL while selecting the protected `wu.cgi` handler with `X-DSCGI-PATH`. The
next sixteen requests use that same login URL but select the supplied filename
under `/home/runtime/tmp/` as the CGI handler. They print response bodies.

An inert QuickJS execution with mocked HTTP clients confirmed one POST followed
by sixteen GETs and sixteen output calls for each file. The fetch variant starts
all sixteen GETs together after the POST promise resolves; the Axios variant
awaits each GET individually. Both wait for the POST response before issuing
execution requests. This sequencing can miss the temporary-file deletion race;
neither file checks upload validity or proves successful exploitation. Fetch
normally resolves at response headers, while Axios normally waits for the body,
so the two completion points are not necessarily equivalent on a real server.
The TypeScript run removed only the import and type annotations and substituted
an inert Axios object. No requests reached an appliance.

There is no obfuscation or decoding, embedded payload, digest computation,
local process execution, credential collection, persistence, or privilege
escalation in these files. The supplied body is opaque, and the scripts do not
construct a multipart upload themselves. Later stages described in public
research cannot be attributed to these samples.

The routing mismatch and temporary CGI execution attempt match the mechanism in
[Volexity's original research](https://www.volexity.com/blog/2026/10/13/a-series-of-unauthenticated-events-chained-exploitation-of-ivanti-connect-secure-zero-days/).
This identifies the exploit mechanism, not either hash, an actor, or a successful
compromise. The MALICIOUS judgments rest on the implemented bypass and execution
attempts. Authorized vulnerability testing is plausible. The public-registry
origin and exact regression-fixture copies do not establish invocation,
authorization, or the package/deployment context of the isolated samples.

The existing two hostile client traits remain accurate. Their descriptions now
state proximity rather than implying a proven URL-to-header data flow. The
execution comment also distinguishes routing attempts from successful upload
or race exploitation. Existing capability traits remain in their admitted
legacy namespaces pending the repository's separate taxonomy migration.

The false positive corrected here is `hardcoded-home-dir-path`: Ivanti's
reserved `/home/runtime/tmp/` and `/home/webserver/htdocs/` layouts are appliance
roots, not leaked developer homes. The exclusion filters individual matching
spans and does not suppress other home paths in the same file or other
subdirectories belonging to users named `runtime` or `webserver`.

Run `python3 testdata/taxonomy/ivanti-bypass-client-coverage/check-home-paths.py`
to check both exploit fixtures and the mixed positive/negative path control.
