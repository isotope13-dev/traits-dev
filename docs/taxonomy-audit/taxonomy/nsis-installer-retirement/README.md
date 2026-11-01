# NSIS installer staging retirement

The 16 rules under `dropper/staging/nsis-installer` were reviewed and the legacy
directory was removed. Their predicates, scopes, confidence and exclusions are
unchanged, and exact consumers were updated.

The opaque, document-lured NSIS process-launch combination moved to native
payload execution. The self-signed business-document and document-named
installer combinations moved to installer masquerading, and the elevated
RWX-section combination moved to section-packing evasion. These retain hostile
severity because the combined evidence is consistent with the stated intent.

The remaining overlay, plugin, API and certificate combinations moved to
installer or PE profiles. Their descriptions no longer claim a loader, a CLR
stage, anti-AV activity or an NSISdl download from generic plugin-group or API
references. These profiles are suspicious or notable: NSIS System plugins,
clipboard/reboot references and large overlays also occur in normal installers.
The two fixed VERSIONINFO strings moved to resource identity; the compound
NSIS/CallWindowProc/version-word signature is an installer profile.

Unsubstantiated inherited transfer and packing labels were removed. No live
YAML references to the retired directory remain.
