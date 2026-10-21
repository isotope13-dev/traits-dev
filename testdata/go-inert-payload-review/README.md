These two reviewed Go files contain only constant data: XXE declarations and
conflicting HTTP framing. Neither file has imports, functions, initialization,
a parser or a sender. The verdicts are BENIGN; each retains one accurate
suspicious content observation. Package consumers and registry coordinates were
not supplied, so the review makes no claim about other files.

The structural observation permits comments and grouped constants, rejects
imports, functions, methods, variables, types and explicit parse-error nodes,
and applies only within the matching file. The regression runner copies every
control to a neutral module.go path so test-directory exclusions cannot make
the assertions pass. Controls with parsers or senders retain the pre-existing
hostile detections; that checks exclusion scope, not those controls' intent.
Account database and sudoers references also exercise their separate homes.

Run:

    python3 testdata/go-inert-payload-review/check.py --scratch <scratch-directory>

See review.json for decoded payloads, execution-path review and limitations.
