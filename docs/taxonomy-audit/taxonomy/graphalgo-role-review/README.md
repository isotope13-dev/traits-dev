# Graphalgo Go module role migration

The Go-specific rules identify dependencies and imports from the campaign's
lookalike module hosts. They moved unchanged from
`well-known/malware/supply-chain/netstruct` to
`well-known/malware/trojan/graphalgo`, where the defining role is a trojanized
module. The JavaScript Netstruct rules remain for a separate claim-by-claim
review. No YAML consumers reference the moved Go rule IDs directly, and no
YAML directory consumer references the old Netstruct family directory.

The synthetic `go.mod` controls contrast a campaign-host dependency with the
legitimate upstream `github.com/google/btree` dependency. Cleave reported the
moved family composite for the former and no suspicious or hostile finding for
the latter. Full validation must still be checked before accepting the move.
