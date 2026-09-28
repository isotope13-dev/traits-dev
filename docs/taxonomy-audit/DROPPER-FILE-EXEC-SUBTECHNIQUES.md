# File-execution subtechnique audit

`dropper/file-exec` reached the inclusive 85-rule cap. Its rules form distinct
activation mechanisms, so the parent is now strictly non-leaf and every rule
lives under exactly one child:

- `file-exec/spawn`: the staged executable or script is directly launched as a
  process.
- `file-exec/installer`: a staged package is handed to an installer
  transaction. This includes the MSI command and its remote-install chains.

The tie-breaker is the activation mechanism required by the matcher. An MSI
installation remains under `installer` even though `msiexec` runs as a child
process. Direct launch of an extracted executable or script belongs under
`spawn`. An incidental installer string without package-install evidence does
not qualify for `installer`.

The initial migration placed all 85 definitions into `spawn` (78) and
`installer` (7). A later audit split the 41 shell/interpreter-command chains
into `command`; the six completed archive-launch rules then joined `spawn`.
The current leaves contain **41 command**, **43 spawn**, and **7 installer**
rules. Every exact reference points to its canonical child path; directory
references to `file-exec/` continue to name the combined parent category.
Matcher bodies, effective scope, criticality, confidence, and mappings were
preserved. The mapping ledger lists each rule. Soft validation passes
**1,837/1,837 fixtures**, and strict validation retains the existing 165
over-cap directories and other catalog debt.

This also makes room for archive-delivery rules whose completed sink is a
process launch or installer transaction. Their archive carrier remains
supporting evidence rather than a competing directory.
