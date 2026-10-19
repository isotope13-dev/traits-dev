Cloudflare environment-member placement review

The Cloudflare API-token read is a neutral environment capability, now
`micro-behaviors/os/env/cloud::node-cloudflare-token-member` (notable).
The former objective atom matched source text, including comments, strings,
and longer variable names. The new matcher uses complete parsed member paths
and supports both dot and literal-subscript access. JavaScript/TypeScript scope,
confidence, and the existing drizzle-kit exclusion are preserved.

The node-cloud and Cloudflare R2 consumers reference the new ID. The two
ancestor-directory consumers in JavaScript and Ruby source groups explicitly
retain this member, preserving their previous candidate populations subject to
the intentional matcher tightening. No suppression or verdict severity changed.

`cases.json` records positive dot/subscript reads and a negative control with
comments, string contents, and a longer environment-variable name.

Sample review: SHA256
043ac18abd642072b844f30a49a72c9cf00aed774ae7342aef562d782b78dfdf
is byte-identical to `../cloudflare-firstparty-auth/evil-endpoint-nearmiss.js`.
Its complete body reads two cloud credential variables, serializes their values,
and makes one POST to the illustrative collector.example.com destination.
There is no obfuscation, downloaded code, persistence, or further payload.
QuickJS execution with a synthetic environment and an in-process fetch stub
confirmed both reads and the exact JSON body; no network access occurred.
This is a benign regression-test artifact demonstrating an exfiltration shape,
not corroborated malicious registry software. Its observable credential and
HTTP capabilities remain notable, independently of that artifact verdict.

Verification: all three focused cases passed. The sample's final atomscan
retained environment reads, JSON serialization, HTTP POST, and secret-request
flow as notable capabilities, with zero suspicious or hostile findings.
The scanner reported incomplete flow fields; full source inspection and mocked
execution independently established the actual source-to-request relationship.
