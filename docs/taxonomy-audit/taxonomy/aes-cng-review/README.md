# AES/CNG staging review

The legacy filename rules match text shaped like `payload*.bin/dat/enc/db`
 or `stage*.bin/dat/enc/db`; they do not establish encrypted payloads. They
moved to `micro-behaviors/fs/path/data-file`. CBC property strings combined
with file, resource, allocation or thread API names moved to suspicious PE
profiles. The timer-callback combination remains hostile under callback
injection because it also requires the separate callback pattern. The Defender
exclusion, decryptor and file/process API combination remains hostile under
`objectives/evasion/anti-av/exclusion`; its anti-analysis consumer now
references it and describes the resource-query clues without asserting order.

The eight original conditions, confidence, explicit scopes and exclusions are
preserved, with local references redirected. Names, descriptions, severity and
unsupported ATT&CK/MBC annotations were corrected. The legacy file's 10 MiB
whole-file maximum was removed from all eight rules: none of their conditions
requires that bound. A synthetic PE with payload filename text matched the
moved filename trait both below and above 10 MiB. This test covers that atom,
not the full composite chains.

The neighboring Defender platform directory had 91 rules. Eighteen rules moved
by subject into existing exclusion, registry and Defender directories, leaving
73. All full references and two local references were redirected; the Lua
rule's remaining system-drive reference was qualified. No directory-wide
references to the old Defender path were found. Destination directories have
50, seven and five direct rules respectively.
