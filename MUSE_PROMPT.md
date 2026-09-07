The previous trait repair failed validation.
Repair the errors below. Keep the change scoped to these validation errors.

Validation output:
make: Entering directory '/srv/data/rectifier/traits-dev'
/data/rectifier/bin/cleave --traits-dir . validate

❌ ERROR: 1 rules exceed a suppression limit (8+ written on the rule, or 32+ after expanding aggregator references)
   A heavy suppression list usually means the rule is fighting its own breadth.
   In order of preference, try:
     • downgrade the parent rule — if it is suppressed this often it is pitched
       too high; lowering its `crit:` is usually a one-line fix and needs no carve-outs
     • split by file type — a `suspicious` variant for the risky types and a
       `notable` variant elsewhere, instead of one rule plus a pile of `unless:`
     • group the exceptions — find the broader semantic that the carve-outs share
       (e.g. "test fixture", "vendored dependency") and express it once, not N times
     • drop dead downgrades — conditions that can never lower the criticality
     • tighten scope — narrow `for:` file types or add `size_min`/`size_max`
     • prefer a `dir/` reference over many `::leaf` ones — a directory reference
       counts as 1 and does not sum in its members' suppressions
   If it still gives no signal to humans or ML pipelines, consider removing it:

   ./micro-behaviors/fs/config/sudo/traits.yaml: trait 'micro-behaviors/fs/config/sudo::sudo-nopasswd' (10 written; 10 after expanding aggregators)
        metadata/build/ci/host::remote-wheel-build-host (1)
        (inline condition) (1)
        (inline condition) (1)
        (inline condition) (1)
        (inline condition) (1)
        metadata/package/testing/harness/runtime/ (1)
        well-known/lib/ai/tensorflow::tensorflow-user-wrapper (1)
        (inline condition) (1)
        (inline condition) (1)
        (inline condition) (1)


validation failed: 1 issue(s) in 1 location(s)
counts
  policy/suppress          1

-
  policy/suppress          1 rules have excessive unless:/downgrade: clauses

suggested fixes
  policy/suppress: Tighten the matcher, split by technique, lower criticality, or delete low-signal catch-alls.


==> Fix all validation errors before continuing.

Error: Failed to load traits from .

Caused by:
    Trait loading failed due to 1 validation error(s):
    validation: policy/suppress 1 rules have excessive unless:/downgrade: clauses
make: *** [Makefile:20: validate] Error 1
make: Leaving directory '/srv/data/rectifier/traits-dev'


Before finishing, you MUST run:
  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes.
