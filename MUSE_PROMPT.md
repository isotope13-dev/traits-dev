The previous trait repair failed validation.
Repair the errors below. Keep the change scoped to these validation errors.

Validation output:
make: Entering directory '/srv/data/rectifier/traits-dev'
/data/rectifier/bin/cleave --traits-dir . validate

❌ ERROR: 1 broken trait references found in composite rules
   Composite rules reference trait IDs that don't exist:

   ./objectives/supply-chain/trojanized/library/hidden-dep/npm-loader.yaml:383: Rule 'objectives/supply-chain/trojanized/library/hidden-dep::known-payload-phantom-dependency' references non-existent trait: 'objectives/supply-chain/trojanized/hidden-dependency::easy-day-js-dependency'


validation failed: 2 issue(s) in 2 location(s)
counts
  qual/broken-ref          1
  qual/validation          1

-
  qual/broken-ref          1 broken trait references in composite rules
./objectives/supply-chain/trojanized/library/hidden-dep/npm-loader.yaml:383
  qual/validation          ./objectives/supply-chain/trojanized/library/hidden-dep/npm-loader.yaml:383: Rule 'objectives/supply-chain/trojanized/library/hidden-dep::known-payload-phantom-dependency' references non-existent trait 'objectives/supply-chain/trojanized/hidden-dependency::easy-day-js-dependency'

suggested fixes
  qual/broken-ref: Fix the id, or add the missing trait; references resolve by directory::id.
  qual/validation: Review the validation message and update the trait.


==> Fix all validation errors before continuing.

Error: Failed to load traits from .

Caused by:
    Trait loading failed due to 2 validation error(s):
    validation: qual/broken-ref 1 broken trait references in composite rules
    validation: qual/validation ./objectives/supply-chain/trojanized/library/hidden-dep/npm-loader.yaml:383: Rule 'objectives/supply-chain/trojanized/library/hidden-dep::known-payload-phantom-dependency' references non-existent trait 'objectives/supply-chain/trojanized/hidden-dependency::easy-day-js-dependency'
make: *** [Makefile:20: validate] Error 1
make: Leaving directory '/srv/data/rectifier/traits-dev'


Before finishing, you MUST run:
  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes.
