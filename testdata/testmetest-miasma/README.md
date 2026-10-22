# testmetest / Miasma payload coverage

Sample: `event-bus-lite-testmetest@0.0.1`, SHA-256
`32dd68c748eefd03a25b7104b648685b877672581c94741099899d789701c6de`.
Reference: [SafeDep's payload checklist](https://safedep.io/testmetest-npm-worm-miasma-variant/).

The original npm archive is hostile: its implicit node-gyp install hook runs
the obfuscated entrypoint, which decrypts and launches a sidecar payload.
It already matched three hostile loader traits before this change. The payload
contains the behaviors in all 15 bullets of the reference's checklist, so no
additional samples were needed.

This change adds rules covering missing observations and behavior combinations,
including locale and sandbox checks, Docker runner killing, security-domain hosts
rewrites, fragmented procfs memory reads, token-rejection handling, npm/PyPI/gem
repacking, Artifactory replacement, SSH propagation, repository commit options,
and encoded workflow secret exports. Existing detections cover browser collection,
credential stores, signed GitHub commit C2, and service persistence.

**Coverage is not automatic decryption.** Cleave detects the original archive's
loader; it does not automatically recover this encrypted payload. The downstream
checks use the static reconstruction below. [coverage.json](coverage.json) maps
each checklist item to asserted findings and states the limits of each match.
Credential target names, cloud API paths, public-repository options, and generic
HTTP POSTs are capabilities, not proof of complete theft or exfiltration flows.
Commit-author/message copying, exact timer values, and every sandbox/exit branch
are confirmed source details rather than separate behavioral verdicts. Do not
interpret 15 passing coverage rows as 15 fully proven attack chains.

## Reproduce

Requires Python 3, Node.js, and the cleave binary built from the adjacent checkout.
No sample code, npm lifecycle scripts, generated shell, or recovered Python is run.

```sh
python3 testdata/testmetest-miasma/recover.py \
  ~/Downloads/event-bus-lite-testmetest-0.0.1.tgz /tmp/testmetest-review
python3 testdata/testmetest-miasma/verify.py /tmp/testmetest-review \
  --report /tmp/testmetest-review/results.json
make validate
```

Set `CLEAVE` to override the scanner binary. The decoder is deliberately pinned
to this archive's hash; it is a reproducible analysis aid, not a generic unpacker.
Recovered files are malware analysis material and must not be executed.

The verifier asserts all 15 checklist rows, checks 28 benign/near-miss controls for
zero suspicious or hostile findings, and exercises 18 regression cases covering
renamed code, equivalent syntax, and neutral observations. Controls include ordinary registry publishing, Docker maintenance,
locale display, SSH deployment, token-health checks, different memory-file
handles, and a lazy self-file handle without a read. Hidden workflow controls
are passed explicitly to the scanner. An extracted workflow run block is counted
as an additional scanned node, not an additional control input.

## Static reconstruction and provenance

1. Decode the numeric character array and Caesar shift in `index.js`.
2. Parse AES-128-GCM parameters from the resulting loader, authenticate/decrypt
   `lib_native.dat`, and Brotli-decompress it.
3. Decode the custom-base64 string array. Derive its rotation by reproducing
   only the arithmetic guard; replace constant decoder calls and aliases.
4. Reimplement the PBKDF2/SHA-256 permutation cipher to recover 873 strings.
5. Authenticate/decrypt and decompress 16 embedded resources with AES-256-GCM
   and gzip. Number intermediate filenames to prevent `qc`/`Qc` collisions on
   case-insensitive filesystems. Preserve valid source and resource suffixes.

The recovered main source hashes to
`bc6ec3d62114e7c43c8ac589f95682a67dd4b9e8ff14d50aa5466eec197c907c`.
[functions.json](functions.json) records parser-derived UTF-16 boundaries and
SHA-256 hashes of audited top-level functions/classes. Recovery verifies every
slice. These small units supplement the intact bundle because the monolithic
source exhausts flow analysis budgets and loses some findings to output limits.
The reconstructed archive includes the intact source, exact slices, and embedded
resources; it is explicitly an analyst-created derivative, not the npm tarball.

## Analysis boundaries and engine observations

- `cleave facts` exposes imports, call arguments, literals, and AST shapes after
  decoding. The large bundle reports truncated flow analysis. New rules favor
  direct argument/AST evidence and describe cooccurrence honestly.
- Text evidence in Unicode-escaped source can have offsets in a normalized
  buffer, while literal/AST evidence uses raw offsets. Mixing those in proximity
  rules can miss real combinations. Hosts/Docker rules use compatible evidence.
- The workflow artifact `type: value` finding has no span. The existing
  `github-actions-secret-artifact-exfil` proximity rule therefore does not match
  this workflow. A new suspicious rule requires an encoded environment dump,
  complete secrets export, and artifact upload without claiming path dataflow.
- The article summarizes runner evasion as kill plus hosts blocking. The code
  also tries resolver changes and a privileged container mounting sudoers to
  grant passwordless sudo. The coverage assertion concerns the kill/hosts paths;
  it does not claim all alternatives run on every victim.
- Detection does not depend on the package name, exfiltration domain,
  `AutoSyncComplete`, `project-utils`, service names, or the commit-search marker.
  StepSecurity names identify the security product being disabled.

[results.json](results.json) records the checked coverage and validation result.
All assertions also pass in the newer local `../scan/target/debug/atomscan` build.
The installed atomscan build misses the locale cluster and browser-store walk
findings, despite sharing the `2.13.0` version string with the newer build.
Both classify the sample hostile; raw trait assertions establish coverage.
The original archive was rechecked with atomscan and confirmed in Hopper's `bad`
pool; the relabel operation returned an already-correct no-op.

## x-improve review

The follow-up review adds observations for the privileged container mounting
writable host sudoers beside a passwordless grant, and for the resolver
replacement command. The sudoers rule requires privilege and the writable bind
inside the same HostConfig object; it rejects a read-only mount, disabled
privilege, and facts split across different container specifications.

JavaScript checks now cover dot notation, bracket notation, and mixed forms.
The auth-rejection handler recognizes both the `^40[13]$` pattern and explicit
401/403 comparisons, while rejecting a 4010 lookalike. Descriptions state when
the evidence establishes proximity or cooccurrence rather than value flow,
execution order, successful theft, or execution of a staged file.

The review also corrects inflated or misplaced findings:

- A package tarball path is a neutral archive-path reference, not evidence
  that an archive is embedded or concealed.
- Imports after `setup()` are neutral module-loading observations. Execution
  consumers retain their additional evidence.
- Discord storage uses the existing neutral path finding and no longer counts
  as a gaming-launcher credential target.
- Atomic Wallet names and storage paths are neutral references; consumers
  still use them to identify targets.
- npm maintainer search plus a GitHub commit API reference is a neutral API
  combination. Those two facts alone do not establish a worm. The former
  hostile rule is replaced by that capability; its worm-flag consumer is
  suspicious. The separate hook-repacking findings remain suspicious.

[improve-audit.json](improve-audit.json) records hostile rule IDs and groups
overlapping findings by mechanism. Counts deduplicate archive rollups and
identical source slices. They do not enumerate arbitrary subsets of traits or
claim independent proofs for overlapping rules. Coverage still has the static
decoding and dataflow limits stated above.
