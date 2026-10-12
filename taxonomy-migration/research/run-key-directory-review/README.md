# Run-key directory review

The directory previously held 101 rules. Registry paths, value labels, log
messages, plain autorun registration, and registry reads were being presented
as login persistence. TAXONOMY.md requires durable, unwanted reactivation and
places neutral registry operations under `micro-behaviors/os/registry`.

The final directory holds 31 persistence composites. No subdivision is needed:
all share the Run/RunOnce activation surface. Language and binary backend
differences stay in filenames and `for`, rather than becoming subdirectories.

## Disposition

- Retain 29 composites that combine registration with payload or unwanted
  behavior. Strengthen the homepage-hijack and Perl-beacon composites with
  explicit registration requirements.
- Relocate 68 rules: registry references and operations, neutral autorun
  capabilities, names and logs, obfuscation, installer metadata, and Gator
  identity. Update dependent composites to reference their new homes.
- Consolidate the identical Java/Kotlin source-write composites into one
  neutral JVM capability, preserving the union of their language scopes.
  Reuse the existing Windows Temp-path observation instead of requiring one
  chosen executable basename in a PHP rule.
- Retire the encoded-infostealer persistence composite: encoded configuration
  mentions browser targets, Telegram and Run keys, without a registration or
  activation sink. Preserve its constituent observations.
- Retire the redundant Runtime.exec composite, whose complete match domain was
  already covered by the original JVM composite.
- Add two package beacon composites after inspecting the Ruby, PowerShell and
  JVM corpus fixtures. Require staged Node network callbacks, a Node launcher,
  file writing and concrete registry registration. Plain autorun setup remains
  neutral. Extend the existing embedded-JavaScript observations to JVM class
  strings and add constant-pool command fragments for the bytecode backend.

Three dependent observations also move: the Rust HKCU Run path becomes a neutral
key reference, the managed startup configuration token becomes an autorun
keyword, and browser-profile copying belongs to directory copying.

`plan.json` records each disposition and consumer update. The six detection-field
changes in `matcher-comparison.json` are deliberate: the homepage and Perl
registration requirements, both sides of the Java/Kotlin scope union, the PHP
Temp-path reuse, and restricting the PowerShell Run composite's inherited
platform scope to Windows. The other 96 compared rules preserve their detection
fields after resolving moved references and inherited defaults.

The generic Run-path reference now accepts a closing backtick, covering normal
Go raw-string syntax. Read-only OpenKey use stays a registry-access observation;
DWORD writes under Run do not establish an executable autorun command.

## Verification

Run `python3 taxonomy-migration/research/run-key-directory-review/check.py`.
It checks 24 cases, copies sources outside test-directory suppression, builds
two harmless Go fixtures without executing them, and patches a JVM constant-pool
string to create a beacon near miss. `observed.json` records the results.

The cases include registry read/reference/DWORD controls, ordinary Ruby and
PowerShell autorun registration, profile-directory versus file copying, the JVM
beacon and its near miss, plus the triage and upstream prompt-injection controls.
Repository validation covers the existing malicious package fixtures as well.

The Outlook worm expectation continues to require its hostile mail-worm chain
and the relocated neutral registry-import capability. Its minimum hostile count
is one; the generic registry import no longer supplies a second hostile verdict.
Historical scan reports remain historical.
