# Unencrypted archive disk-image chains

Two composites in `staging/encrypted/7z-aes-exe.yaml` did not require any
encryption evidence. One detects an archive member that is a disk image with
an executable; the other detects an order-themed disk image containing an
unsigned PE. Both now live in `dropper/staging/archive/disk-image-stage.yaml`.
The encrypted archive composites remain in encrypted staging because their
matchers require encrypted-member or encrypted-header evidence.

No external rule referenced either moved ID. Matcher legs, scope, platforms,
file types, exclusions, criticality, confidence, and ATT&CK/MBC metadata are
preserved. The move distinguishes archive containment from encrypted-content
staging and from a mounted image-disk activation, as documented in
`TAXONOMY.md`.

Soft validation passes **1,837/1,837 fixtures**. Encrypted staging falls from
245 to **243 rules**; archive staging grows from 95 to **97 rules** and remains
over cap, so its sibling cohorts need the same evidence-based audit. Strict
validation still reports the established catalog-wide **60 issues**, including
**165 over-cap directories**.
