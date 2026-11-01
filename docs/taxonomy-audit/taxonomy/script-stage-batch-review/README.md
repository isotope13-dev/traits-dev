# Script staging evidence review

Eighteen rules from fourteen legacy script-staging files were moved by their required evidence and likely operation. Matching predicates, file scopes, references, suppressions and downgrades were preserved.

- Hidden batch launches, HTTP acquisition with execution, embedded WSH download and shell-execution clues, an embedded-PE remote-thread profile with a SYSTEM task, and OpenSSL decrypt/eval with an app Resources path now live in execution objectives. The latter no longer identifies a specific malware family from generic behavior. Its inherited confidence of 5.0 was corrected to 0.98, within Cleave's documented 0–1 confidence range.
- A gzip string and self-derived filename do not establish execution. DEBUG write text plus generic Run and delete calls, a Node XOR/write/process combination, and encoded WSH strings plus a named decrypt routine and Base64-like blob are observations or suspicious profiles.
- .NET finance terms and reflection/identity clues are finance profiles rather than proof of a finance-decoy loader. Packed-resource, registry and debugger API combinations are registry profiles rather than proof of registry staging.
- A native binary containing WSH HTTP/file-write and status markers is a WSH profile; telemetry labels do not establish an execution chain.

The old criticalities and technique annotations were lowered or removed when they claimed actions the conditions did not establish. Existing proximity, size and exclusion gates were retained for later independent review.
