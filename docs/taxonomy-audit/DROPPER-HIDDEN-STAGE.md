# Hidden-file staging is a delivery technique

The `curl-tmp-implant.yaml` rules did not describe one curl-specific technique.
They covered language- and carrier-neutral detection of hidden writable stage
paths, making a stage executable, and sometimes launching it. The predicates
span command files, build/CI manifests, Dockerfiles, and C-family source where
an execution primitive is also required. Their canonical home is now
`objectives/command-and-control/dropper/delivery/hidden-stage/` alongside the
existing hidden-stage rules.

The original matchers, effective type/platform scopes, criticalities,
confidence, ATT&CK/MBC tags, bounds, and suppressions are preserved. Six
external consumers now use canonical IDs in the hidden-stage leaf. A transfer
API-specific rule remains under `delivery/urlmon`, `delivery/wininet`, or
`delivery/winhttp`; the shared `hidden-stage` leaf is for rules whose defining
technique is hidden-file staging without a narrower transfer mechanism. A
hidden-window option by itself does not qualify.

See the [mapping ledger](dropper-hidden-stage-mapping.json) for the moved rule
IDs and consumer rewrites.

Fixture expectations were updated with the move: the hostile CI tampering
sample now requires the canonical `delivery/hidden-stage/` finding, while a
benign shell control explicitly forbids that finding. Full soft validation
passes **1,837/1,837 fixtures**.
