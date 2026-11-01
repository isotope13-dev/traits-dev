# IExpress and batch installer review

Sixteen traits moved out of legacy installer staging. Batch fragments and their
reconstruction combination now describe string obfuscation; the evidence does
not establish that an MSI was actually launched. The file-to-cmd pipeline is
classified by its interpreter-stdin execution behavior. IExpress command and
entrypoint references are installer metadata, and the filename reference is a
media path. IExpress extraction plus INF references and the ASPack/resource
combination are suspicious installer profiles, not established droppers.
The exact NSIS first-header bytes are an installer build fingerprint rather
than proof of hijacking. Match conditions, formats, exclusions and confidence
are preserved; descriptions, severities and unsupported technique labels were
corrected. The Xamloader directory-wide consumer retains the moved traits.

The adjacent SFX directory contained 85 rules. Sixty-three rules for archive
self-extractors moved to `metadata/binary/installer/archive`; the remaining SFX
directory has 22. Both downgrade consumers that formerly referred to all SFX
members now refer to both original partitions. New installer reference rules
are kept outside those directories to avoid broadening those downgrades.

The shell-pipeline directory contained 78 rules. Fifteen encoded-input rules
moved to the existing `micro-behaviors/process/create/shell/encoded` subject,
leaving 63 pipeline rules and 38 encoded-shell rules. Cross-directory references
were updated. Parsed-rule comparisons verified that both splits preserve the
original 85 and 78 rules respectively, apart from namespace changes.
