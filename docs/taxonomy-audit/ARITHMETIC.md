# Arithmetic observations and codec boundaries

The arithmetic cohort contained 22 observations under `data/source/arithmetic`
and three generic operations described as Base64 decoders. The source partition
was particularly misleading for the JVM bytecode arithmetic observations.

## Placement decisions

- Move 21 numeric/bitwise observations to `micro-behaviors/data/arithmetic`.
  Language and representation remain in rule scope and filenames.
- Move repeated conditions containing hexadecimal literals to
  `data/control-flow/branch::hex-literal-conditionals`. The predicate does not
  require a threshold comparison, so the old threshold description was removed.
- Rename the byte-mask scaling observation `normalized-byte-mask`: its predicate
  does not establish that a value is a color channel.
- Place the JavaScript 18/12/6 shift/OR sequence and PowerShell shift/OR sequence
  in arithmetic. Place Perl zero-padded binary formatting in `data/format/string`.
  None independently establishes Base64, much less decoding direction.
- Retire `custom-base64-decoder`, whose alphabet-plus-shift proximity establishes
  neither a particular conversion nor direction. There were no exact consumers.
  Remove the three generic operations from the `base64-decoding` alternatives.
  The Nemucod consumer retains its precise shift-pattern reference at the new ID.

The [27-entry ledger](arithmetic-mapping.json) records effective definitions.
Every relocated predicate, scope, confidence, criticality, exclusion and count
constraint is preserved. Description and ID changes correct unsupported claims.
The retired aggregate and narrowed decoding umbrella are intentional semantic
coverage changes; this is not a claim of identical decoder output.

## Verification

`arithmetic-without-codec.zip` exercises packed-field JavaScript shifts,
PowerShell shifts/OR and Perl binary formatting. Before migration all three
were reported as Base64 decoders. After migration all three relocated IDs are
present and the archive has no Base64 decoder finding. Its score changes from
3 to 4, within its cap of 15; score reduction is not the correctness criterion.
The fixture forbids Base64 decoding and the retired source-arithmetic path.
Existing positive and negative arithmetic fixture expectations follow the new
canonical path, so the negative checks remain effective after relocation.

The ledger verifies all 27 entries against current YAML, including unchanged
matching conditions for every relocation. Directory counts are arithmetic 23,
branch 31, string formatting 20, and Base64 78. There are zero mixed rule
folders and 175 oversized directories across the repository.

The validator's documented data-category registry now admits `arithmetic`;
its 18 directory-validation unit tests pass. The rebuilt release passes all
1,675 fixture checks under soft validation. Strict `make validate` fails only
on the existing 175 oversized directories; no other blocking issue remains in
this batch. Logs: `/tmp/taxonomy-arithmetic-soft-final.log` and
`/tmp/taxonomy-arithmetic-strict-final.log`.

## Remaining work

The two JavaScript shift observations can co-match but are not equivalent:
one requires specific shifts; the other counts a broader arithmetic shape with
its own scope and exclusions. Do not consolidate by shared sample hits alone.
A useful validator improvement would identify overlapping predicates used as
supposedly independent legs of `needs` conditions; identical-body comparison
alone cannot establish evidence independence.

Base64's XML directionality and symbol-backend partition remain open. A
`nodeTypedValue` reference can be a getter or setter and need not involve
Base64. The `Base64Data` element name is arbitrary. Those cases require a
separate DOM/XML and conversion-direction audit, not an arithmetic relocation.
The wider 85-rule migration remains incomplete.
