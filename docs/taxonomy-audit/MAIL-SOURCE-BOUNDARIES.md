# Mail sources, client operations, and records

The [89-rule manifest](mail-source-moves.csv) separates mailbox acquisition,
message export, authentication material, and neutral client/data operations.
`collection/email-harvest` falls from **103 to 45**, resolving one cap violation.
Every receiving directory is a strict leaf within **85**, without exceptions.
The [placement contracts](../../TAXONOMY.md) describe admission and tie-breaks.

## Placement decisions

- Mailbox enumeration and reading APIs share `email/access`, including Exchange
  and webmail endpoints. Exchange sending retains three sending rules; merely
  constructing its client or attachment no longer counts as sending.
- Address parsing, normalization, headers, authentication, and queuing follow
  their email capabilities. Provider-specific authentication and parameters
  follow the named service. Registry keys, mailstore paths, clipboard writes,
  decoding, drive enumeration, and form fields follow those capabilities.
- Mail access audit events describe recorded activity, not a collector's
  implementation. They follow telemetry/event; API/client GUID fields without
  event context follow schema-object. This preserves useful evidence without
  inferring that the program emitting or containing a record stole the mailbox.
- Mail account-password exports follow `stealer/credential`, not `message`.
  Google session mailbox reconnaissance follows mail collection. Buffered browser
  request-history export follows `stealer/browser`, which stays at **85**.
- Certificate-validation callbacks follow `tls/verify/callback`. Installing one
  does not establish disabled verification. This small sibling deserves its
  distinction from `verify/disable` despite the sparse-cohort advisory.
- The receiving schema directory also needed cleanup. Mapping lookups follow
  `data/collection/map`; response truthiness follows control-flow/branch; cookie
  helpers, share-link construction and status labels follow their subjects.
  Schema-object has **77** rules after the moves, rather than overflowing to 91.

The [label manifest](mail-source-labels.json) clarifies 49 names/descriptions,
including two unmoved collection definitions. EWS collection no longer claims
full disk export; a callback no longer claims disabled TLS checking. A quoted
`mailto:` prefix is described as a reference, not a complete harvesting loop.
No matcher, confidence, criticality, scope or threshold was changed in this pass.

## Verification and directory consumers

The normalization proof protects **189 definitions**: moved rules and their
exact/broad consumers. The final catalog reconciles 118,816 definitions before
and after against the declared moves and separately recorded outside edits.
The [consumer report](mail-source-directory-consumers.csv) records **72 changed
directory references in 66 consumers**. Broad membership changes deliberately:
neutral client APIs and address filters no longer satisfy collection intent.
The two message-to-credential moves are JavaScript/TypeScript rules, outside the
Python-only profiled collector's scope; that consumer loses no eligible Python
source through those moves. CrystalX's collection reference is an exclusion,
so neutral APIs also cease suppressing its family evidence as collection.

The ten new mail controls pass **29 assertions**, covering SMTP with and without
acquisition clues, IMAP selection, EWS read versus send, GUID fields versus audit
events, webmail collection versus export, and mapping lookups. Six browser-history
controls add **16 assertions**. All fixtures are scanned, never executed.
The positive C SMTP fixture uses an actual supported mail-profile path: its
initial `/collect` clue was ineligible for C, so the fixture was corrected rather
than broadening a production matcher to make a synthetic test pass.

The live tree's full soft validation fails on PyAigis: the unrelated
`shell-eval-base64-decode` definition changed before this migration. The
[pre-move drift record](mail-source-pre-move-drift.json) captures eight outside
changes, including that definition; [post-move drift](mail-source-concurrent-changes.json)
records eleven more. A temporary copy with **only that shell rule restored to
its previously passing definition** passes all **1,841 corpus fixtures**. No rule
files or fixtures were excluded. The [isolation record](mail-source-validation-isolation.json)
contains both definitions; the repository's shell rule was not reverted.
This establishes the migration's corpus result, not a passing live-tree result.
Strict `make validate` still reports **89 diagnostics**, including **149**
oversized directories. The [verification record](mail-source-verification.json)
keeps these test scopes separate.

No identical atomic matcher-body candidate touching a moved rule was found by
this batch's overlap check. Global overlap candidates still require comparison
of effective scope and exclusions before merging. Two useful validator review
ideas are (1) checking effective file-type intersection for counted `any` legs,
and (2) explaining changed directory membership and whether a consumer uses it
as evidence or an exclusion. Existing impossibility checks catch some scope
errors; neither counts nor identical bodies alone establish semantic equivalence.

## Remaining semantic work

Passing the cap does not certify the 45-rule remainder. Review next:

- Contacts APIs and address-book acquisition versus mailbox-message collection.
  Existing native contacts APIs under OS user lookup should share a contact-data
  home with cloud contact APIs, not imply operating-system principal management.
- Campaign-specific audit GUIDs: establish their provenance before assigning
  a family identity. Generic recorded access does not prove a harvesting tool.
- Bare provider helper names and `needs: 2` composites that can pass on parameter
  markers without requiring an extraction clue. Keep supported probable-capability
  inferences; remove stronger collection claims unsupported by the alternatives.
- The seven message-export classifiers, especially SMS permission plus a socket
  and personal-data relay alternatives that do not require message content.
- Remaining browser acquisition and keychain alternatives, including source
  branches that accept mutually alternative datasets or no transfer evidence.

The cumulative ledger has **1,142 implemented dispositions out of 1,145**, with
three sweep reviews. This is a checkpoint of the unfinished taxonomy migration.
