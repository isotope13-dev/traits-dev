# Testdata contract and October 2026 migration

`make validate` discovers every file below the four severity roots. There is
one implicit expectation per file: the highest finding severity must equal
its root (`hostile`, `suspicious`, `notable`, or `baseline`). Baseline also
accepts component findings or no findings. Findings on archive members and
decoded payloads count. Scores do not determine this expectation.

Severity is a property of the findings, not a benign/malicious label for the
whole program. For example, a checksum manifest or inert entropy control may
be notable without showing malicious behavior. Source fragments from a
hostile package are classified independently when tested independently.

Only the first directory chooses severity. Organization below it is free,
with one storage-policy exception: `does-nothing/` immediately below the
severity root identifies the no-op controls exempt from the size limits.
Other fixtures must occupy at most 512,000 bytes on disk, and uncompressed
files above 20,480 bytes fail discovery. A final `.xz` is always a storage
layer, decoded once before analysis; actual XZ-format samples need two XZ
layers and two suffixes. Filenames remain available to filename-sensitive
rules, but analysis takes place outside the repository so test-directory
exceptions cannot influence results.

Discovery checks regular files, sizes, and the four roots before loading
rules or consulting the full-validation cache. Hidden files count. Symlinks,
special files, and files outside the four roots fail. All fixtures also
participate in measured rule-performance checks. Passing result caches hash
input contents and the engine and rules; directory additions are checked even
on a cache hit.

## Migration scope

The old tree contained 18,306 files; 3,827 paths were active fixtures under
the old manifest. The new tree has 12,827 fixtures, including previously
unregistered positive and negative controls. It contains 389 storage-compressed
files and 120 no-op inputs. The remaining 5,479 files were operational
receipts, case lists, helper/check scripts, build debris, or other nonfixtures.
Seventeen no-op builders moved to `scripts/fixture-builders/does-nothing/`.
Five audits referenced by TAXONOMY.md moved to `docs/taxonomy-audit/`.

Old explicit hostile/suspicious severity floors were checked during migration.
The directory contract intentionally replaces the old trait-ID assertions,
score ranges, match counts, fact assertions, and filename-invariance checks;
it does not preserve those specialized guarantees. The tests now guarantee
the declared highest severity, independently of those old assertions.

Sixty-nine oversized inputs were reduced to relevant code, metadata, archive
members, or clearly generated controls. Sixty-eight retained the original
highest severity. One signed installer could not fit the storage cap without
changing signed bytes: its original notable reference was retired, and the
reduced unsigned PE is explicitly a suspicious extension-mismatch control.
It is not evidence that the original signed installer was suspicious.
Generated reductions are grouped under `generated/reduced/`.

Operational inventories, scan reports, hashes, reduction notes, and the full
original-tree backup are outside the repository at
`/var/tmp/traits-dev-testdata-cleanup-20261026/`. They are migration evidence,
not fixture inputs. New test additions need no shared manifest or sidecar;
`scripts/add-fixture` checks sizes, applies storage compression, and creates
the destination atomically without overwriting another writer.

## Validation

The completed tree passes all 12,827 severity checks and strict rule-performance
validation. On the development checkout, a fresh full run took 40.7 seconds,
a content-verified cache hit took 0.35 seconds, and discovering an unused file
in the full tree took 38 milliseconds. These are observations, not fixed
runtime guarantees.

The no-op builders reproduced 33 retained controls after normalizing container
timestamps. The publishing helper passed size boundaries, storage XZ versus
actual XZ, the no-op exemption, duplicate protection, and eight concurrent
writers. Validator and AST prefilter unit tests also passed. Bootstrap probes
preserved matches with a harmless leading statement and comments between
compiler/import groups; positive and negative desktop-write probes retained
their results. The full gate used no validator exclusions or raised budgets.

The simpler directory contract intentionally retires the former individual
trait/score/fact assertions described above. A follow-up fixed the clipboard
location diagnostic on decoded PowerShell payloads: dispatcher child matches
retain byte context and parent composite copies carry member provenance.
Existing literal-program layers retain their original host scope. Integration
tests cover standalone and archive-contained loaders and host/stage joins.

Compound shell captures with mandatory scalar guards defer their larger text
checks; unguarded sibling joins retain early pruning. Independent validation
uses private regex caches and confirms suspect relative timings with bounded
repeat measurements. Extra profiling work is excluded from the whole-rule
measurement, while the original cold execution remains charged. Thresholds,
absolute time limits, execution budgets, and fixture expectations are unchanged.

All seven integration tests passed, including real outlier rejection, the
explicit slow-rule deadline, and budget exhaustion. Three full validations
passed all 12,827 fixtures in 57.0, 41.0, and 40.7 seconds, with no missing-offset
diagnostic or performance failures; the cached run took 1.26 seconds.
