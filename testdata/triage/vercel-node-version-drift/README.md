# @vercel/node 1.12.1: BENIGN

Sample SHA-256: `d740b800525745244c247feb212b1a5503228bb02fa07ee7910c602d2b708fca`.
Baseline traits revision: `44e05542d9b2777c8396db2b4f3aca3c4ba19d77`.
Research artifacts and original Forager provenance remain under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/version-drift-node`.

## Release comparison and execution paths

Forager fetched `pkg:npm/%40vercel/node@1.12.0` from the npm registry.
The earlier tarball SHA-256 is
`a5c6b80d20c3dd62b520759aa36b4591f7525aa730bcfb9acd61b7fbfd48a48d`.
Both manifests identify the Vercel Node builder, with identical dependency
declarations and no install hook. The manifest changes only version and gitHead.
Eleven of thirteen archive members are byte-identical. The other changed member,
`dist/index.js`, grows from 3,161,921 to 8,212,766 bytes.

The bundle expands from 666 to 1,693 webpack modules. Comparing complete module
bodies after normalizing only numeric `__webpack_require__()` IDs shows that
1,692 new module bodies already exist in 1.12.0. There is one changed body:
the builder entrypoint, module 2855. Its functional change passes `nodeVersion`
to `runNpmInstall(entrypointFsDirname, [], spawnOpts, meta, nodeVersion)`;
one destructuring statement also loses a trailing comma. `verify.py` checks
that these two substitutions explain that entire body exactly.

The builder downloads caller-supplied project files, selects the Node runtime,
installs project dependencies outside development mode, runs the declared Vercel
build script, traces dependencies, compiles TypeScript, and produces Lambda files.
Its development entrypoint forks the shipped development server, and the launcher
loads the configured project entrypoint and bridges HTTP requests. These paths
explain module loading, process execution, filesystem activity, and generated
JavaScript. Their existing detections are retained.

All fourteen matches of the flagged regex are inside Babel's
`getBindingIdentifiers()`. Its `search` array is a work queue: shift an AST node,
look up the relevant child keys for its node type, then concatenate `id[key]`
onto the queue. The result is an identifier map, not a rebuilt script. The old
bundle has one matching copy, below the rule's twelve-match threshold. The new
bundle has fourteen copies of the same routine because of dependency duplication.
Neither the count nor the assignment establishes obfuscation.

`cleave facts` was run on the archive and the extracted index. The decoded view
includes Unicode/ANSI escapes and incidental Base64 candidates; new module
contents are accounted for by the complete release comparison. The index's flow
graph explicitly reports `source-byte-budget`, so conclusions use source tracing
and module comparison rather than claiming a complete automated flow graph.

The source and packaging support ordinary builder maintenance. No deployment
context or verified publisher signature was supplied; the verdict does not rely
on inventing either, registry reputation, or absence of scan findings.

## Rule correction and retained coverage

`objectives/anti-static/obfuscation/string/array::js-array-accumulator-concat`
claimed a script rebuild loop from repeated assignment syntax. The matcher
requires neither a loop nor string operands nor hidden code. It moves unchanged
to `metadata/lang/source/syntax/assignment::js-repeated-indexed-concat-assignment`
at notable severity, with its original JavaScript/Windows scope, confidence,
regex, and twelve-match floor. Assignment syntax is the supported claim; the
receiver could be either an array or a string.

The only direct consumer was the `js-array-rebuild-loop` OR group. Its only
consumer was `js-cc-array-reconstruction`. Expand the group's three alternatives
directly into that consumer and remove the misleading standalone group. The
hex-character-map and code-like-comment requirements, independent alternatives,
scope, and suppressors remain identical. The hostile Nemucod consumer of
`js-cc-array-reconstruction` needs no edit. Searches found no other exact or
ancestor selectors that acquire this new assignment observation.

Tests used a snapshot of all baseline rules and the edited rules:

- Twelve ordinary indexed concat assignments: suspicious becomes accurately
  named notable syntax; eleven assignments do not meet the threshold.
- Comment-hidden hex-character reconstruction with twelve concat sites:
  `js-cc-array-reconstruction` remains suspicious in both versions.
- Concat without the hex map, and a hex map without concat: no reconstruction
  finding. Padding keeps these controls above 120 KB and below one hex escape
  per KB so the unrelated comment-body/dense-escape alternatives cannot supply
  the reconstruction condition.
- Full truth-table comparison of the expanded alternatives is equivalent.
- Actual historical positive references were traced from the Nemucod consumer's
  git history: `20160922_bcd9939ed07442b1690d6c8766983c9a.js` and
  `20160901_058a910a76ec6be3014a680dd584370f.js`. Forager's configured hash sources
  could not recover the original MD5s. Forager then recovered the public copies
  from `HynekPetrak/javascript-malware-collection` on GitHub. Their actual SHA-256s
  are `dcc0f9e315e6197f9dcf1b4fce1473a88468cc1f889044120d65234393727271` and
  `f4adadaf0021d1ffd595fd93f5bff6ac19c5878655ad2e8b970502dc4bed99c0`;
  these are source copies, not hash-identical originals. Their hex-map/do-while
  and token-map/eval paths were inspected. Their complete emitted findings are
  unchanged: respectively four and one suspicious traits, zero hostile traits.
  The historical family composite did not fire before or after this edit;
  this comparison establishes preservation, not recovered hostile coverage.

The controls are matcher-boundary fixtures, not claims that every synthetic
program has malicious intent. Full reports, generated controls, source facts,
the textual release diff, and provenance remain in scratch. To verify the saved
results and complete module comparison:

```sh
python3 testdata/triage/vercel-node-version-drift/verify.py \
  /usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/version-drift-node
```

## Rescan result

Reproducible scans use
`atomscan --no-update --analyze local --follow=none --format json <artifact>`.
`--follow=none` confines the result to the supplied archive and its members.

| Scope | Hostile before/after | Suspicious before/after |
| --- | --- | --- |
| Archive, unique rolled-up traits | 0 / 0 | 1 / 0 |
| `package/dist/index.js` | 0 / 0 | 1 / 0 |
| Every other archive member | 0 / 0 | 0 / 0 |

The sole removed observation is replaced by the neutral trait on both the
archive rollup and the index. All other traits and criticalities are identical;
no members or supported attack detections are lost. The previous release has
zero hostile/suspicious findings.

The calibrated classifier is BENIGN before and after (`cls: 0`, level `-1`).
The general model's raw probability changes from 0.7074073 to 0.6960754;
the npm model changes from 0.0106430845 to 0.004648199. Raw probability alone
is not the calibrated verdict. The final terminal scan also reports BENIGN.
The tool warns that its v18 feature specification predates expected v21;
this is an existing model limitation. There is no remaining sample verdict
disagreement or newly exposed malicious-classifier miss.

Marker/commit-body line:

`@vercel/node 1.12.1: benign Babel duplication; rehome concat syntax`
