# Reference-group controls

Eight inert PE analysis inputs exercise the two composites that select the old
allocation subtree. The existing corpus matches neither composite, so it cannot
prove that their required memory leg survives a reference rewrite.

The import-mix cases require a memory observation, a video-capture import and a
MAPI import. They cover allocation, free, two free observations, absent memory
and absent surrounding context. The RC4 cases cover the required memory/API/hash
combination and missing memory or hash context. These preserve existing matcher
behavior, including the old allocation directory's selection of free operations;
they do not endorse that directory's old classification or every composite claim.

`fixture-build.json` records commands and binary hashes. C sources declare imports
as minimal compiler scaffolding; one assembly probe and a data constant supply
static byte observations. These are synthetic analysis fixtures, not executable
examples of the claimed behavior. **Never execute the binaries.**

`cases.json` asserts positive and negative matcher results. The migration case
runner also compares complete normalized findings, evidence, component IDs,
suppression and risk across old engine/old references, new engine/old references,
and new engine/new references. `make validate` runs these controls.
