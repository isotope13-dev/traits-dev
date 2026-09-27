# Account vocabulary is not a relational schema or telemetry operation

## Implemented correction

Nineteen existing observations now share `metadata/file/string/account`:

- Five account-label and nearby dataset/user text observations from
  `data/db/schema/relational`.
- One quoted username label from `data/serialize/object`.
- Thirteen account identity/email labels and aggregates from
  `metadata/file/string/telemetry`.

The matchers do not require a database, serialization operation or telemetry
collection. Their former homes implied more than their evidence supported.
Names and descriptions now avoid asserting a relational key relationship,
a shared account record, or a field assignment from labels alone. The
[26-entry ledger](account-vocabulary-mapping.json) records all nineteen moves
and seven consumer updates. Their effective matching predicates, scopes,
confidence, criticality, counts and filters are preserved, modulo references.
No former-location aliases remain.

TAXONOMY.md documents the canonical boundary: account names, IDs, email and
membership/activity vocabulary belong in the account leaf. Secret/token
vocabulary belongs with credentials. Actual object structure, parsed fields,
value mappings and database definitions require their respective evidence.
A colon in a string is not proof of an object. Telemetry-specific context still
belongs in telemetry and can reference account vocabulary without duplicating it.

The account aggregate keeps `needs: 3` and its four original named alternatives;
it no longer claims that the labels form one dense schema. No identical atomic
`if` bodies occur in the new leaf. Overlapping user-name spellings retain their
different scopes and quoted versus word-boundary predicates; they are not exact
duplicates suitable for blind merging.

## Verification and effects

Two new benign archives contain lists of labels printed as text:
`account-labels-without-database.zip` and
`account-labels-without-telemetry.zip`. They reproduce the old database-schema
and telemetry placement without either operation. All four archive/member
comparisons retain identical finding sets and criticalities modulo renamed IDs.
The new account home matches; neither database nor telemetry homes match these
controls. Both controls are permanent fixtures with those prefix requirements.

This migration is **not score-neutral**. Archive/member scores change 4→3 for
the database control; the telemetry archive changes 4→3 and its member 3→2.
No finding is lost and no rule is demoted. These are observed aggregate scoring
effects of the corrected classification, not deliberate score tuning.

All **1,693/1,693 fixtures pass**. Strict `make validate` exits 2 on the existing
**173 oversized directories**, with **zero mixed rule directories**. Account
contains 19 rules, telemetry 26, relational schema 4, and serialization/object
64. All 26 ledger after-definitions verify against current YAML.

Logs: `/tmp/taxonomy-account-vocabulary-{before,after}.json`,
`/tmp/taxonomy-account-vocabulary-soft.log`,
`/tmp/taxonomy-account-vocabulary-strict.log`.

## Remaining sibling and consumer work

The controls exposed `data/source/property/identity::account-email-object-field`:
it also matches a printed `customer_email:` string without an object. The
historical source/property leaf mixes member access, object shape, identifiers,
industrial vocabulary and module exports. Its two directory consumers require
an audit before migration: one combines a directory leg with an independent
`any` group; the other relies on proximity. Preserve their original alternatives
and proximity semantics explicitly when resolving that leaf, rather than
substituting a broader account or serialization directory.

Other telemetry siblings still mix generic profile-field syntax with actual
telemetry vocabulary. Continue separating those claims by the documented
boundary; do not imply that this nineteen-rule cohort finishes that audit.

Existing hostile consumers such as personal-data sync and contact-import
harvesting retain their detection logic. Their names and required relationships
need a separate precision review: nearby labels, writes and transport operations
do not by themselves prove that the same data flows between them. Passing the
fixture suite does not establish every such relationship on untested inputs.

Validator improvement candidate: flag schema/relationship descriptions backed
only by label matches or unbound co-occurrence. This is a review heuristic,
not permission to merge or demote rules automatically. Matchers, scopes and
relationships must be inspected before changing coverage.
