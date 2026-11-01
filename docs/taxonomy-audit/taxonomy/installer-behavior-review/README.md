# Installer behavior and package split

Seven composites left legacy installer staging. A Defender-update-named MSI
with launch actions and a C2-agent debug-path reference moved to installer
masquerading; a renamed Garena executable with sidecars and a launch action
moved to installer payload execution. These retain their hostile severities.

The ScanDisp/Delphi file set with a launch action, two WixSharp installer-source
and repair-policy combinations, and two WiX Burn/OAuth endpoint combinations
moved to `metadata/file/profile/installer-layout`. These combinations do not
establish that the ScanDisp executable was launched, that an installer is a
dropper, or that OAuth tokens were stolen. The former hostile composites are
now suspicious and their descriptions state the available evidence. Stock WiX
Burn legitimately contains RunOnce and networking features, so the OAuth endpoint
combination should not turn those stock features into proven theft.

All seven composites retain their match legs, types, platforms, scopes,
exclusions and confidence; references and the legacy directory-wide consumer
were updated. The old broad ATT&CK/MBC annotations were not carried over where
they asserted unobserved behavior.

The adjacent `execution/payload/file-exec/installer/package` directory had 85
rules. Twenty-nine script-oriented MSI rules moved into sibling
`installer/script-package`; the remaining package directory has 57 rules after
the Garena addition. The split preserves all 81 original rules in the MSI file,
including their predicates, inherited defaults, and cross-directory references.
`TAXONOMY.md` now describes the script-package boundary. No directory-wide
consumers of the old package namespace were found.
