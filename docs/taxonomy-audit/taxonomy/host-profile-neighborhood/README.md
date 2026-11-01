# Host-profile neighborhood review

The `system-info/profile` leaf held 90 rules. This review moved 24 rules by the
specific information or action they identify and removed three unsupported
synthetic QNX composites. The profile leaf now holds 70 rules; its identity
sibling holds 67. Both physical and namespace counts are checked.
The remaining rules still need claim-by-claim review; the count reduction is
not a complete audit of the neighborhood.

- Hostname-only findings moved to `system-info/hostname`; host/user identity
  findings moved to `system-info/identity`. Multi-field host profiles remain
  under `profile`, and MAC-address exports moved from identity to network. Workspace, account, platform and
  network observations use their existing system-information subjects.
- Two generic shell-output callbacks moved to `stealer/command-output`: their
  required evidence does not identify the output as a host profile.
- The SSH-directory listing with an HTTP profile moved to configuration
  export. A PHP `CURLOPT_POSTFIELDS` assignment moved to HTTP body construction
  as a component; setting a body alone does not establish a transfer. Its two
  dependent transfer composites still require their other evidence.
- Three QNX composites relied on fixed synthetic report labels and a formatted
  request rather than established discovery or transfer. They and the four
  now-unused marker rules were removed, as authorized for unsupported QNX
  examples.

No YAML directory reference selected the old `profile` or `identity` leaf
alone. Two consumers of the broader `system-info` subtree continue to select
all relocated system-information findings. They intentionally stop treating
the two untyped command-output callbacks, the configuration listing, the body
assignment, and the synthetic QNX combinations as host-information exports.
Exact references were retargeted.

[moves.json](moves.json) and [refinement.json](refinement.json) record the
original definitions, ID mappings and consumer files. Run
`uv run docs/taxonomy-audit/taxonomy/host-profile-neighborhood/check-moves.py`
to verify the effective predicates, scopes, severities, intentional PHP
component adjustment, removals and destination counts.

A body-only PHP fixture matched the relocated body component and did not
match the remote-stage transfer composite. The source fixture is analyzed, not
executed.

`make validate` passed all 13,920 classified fixtures: 1,927 hostile, 1,774
suspicious, 8,883 notable and 1,336 baseline.
