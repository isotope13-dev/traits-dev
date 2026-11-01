# Pafer role migration

The campaign-listed Pafer wheel supplies a disguised-pickle loader to a
companion package. Its defining role is a trojanized dependency that executes
the supplied pickle; the distribution channel does not define the role. The
two existing rules moved unchanged from `well-known/malware/supply-chain/pafer`
to `well-known/malware/trojan/pafer`. The version observation remains a
component of the family-specific composite. No external YAML consumers of the
old namespace were found.

The synthetic wheels in `fixtures/` carry identical package metadata and
caller-frame, pickle-load, post-load-check, and pickle-dump code, differing
only in version. A Cleave scan reported the new Pafer family rule for 0.9.7 and
did not report it for 0.9.6. Both retain the independent unsafe-deserialization
observation. This is a placement and version-boundary check, not evidence about
the behavior of unlisted Pafer releases.

Full validation was started separately after resolving pre-existing duplicate
rule IDs; its result must be checked before accepting the migration.
