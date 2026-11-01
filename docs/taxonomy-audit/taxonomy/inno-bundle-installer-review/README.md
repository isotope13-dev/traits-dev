# Inno and bundled installer review

Eleven rules moved out of legacy installer staging. An identity-mismatched
7-Zip carrier that reads its own overlay and spawns a child moved to native
payload execution; an unsigned RAR-bearing executable with an elevated logon
task moved to scheduled-task persistence. Installer lure, claimed system
service and self-issued Chrome-brand combinations moved to their respective
masquerading subjects. Those more specific hostile combinations retain their
severity. The NVIDIA banner is a vendor reference.

Other rules are now evidence profiles: an admin manifest with resource MZ prefix
and anomalous timestamp, an opaque Inno section and process/thread API imports,
a driver-themed installer, Inno PBKDF2/SafeArray with section or checksum
signal, and Python ZIP fragments in a dominant Inno overlay. The API and ZIP
composites no longer assert a loader or executed payload and are suspicious
rather than hostile. All match conditions, thresholds, scopes, confidence and
references remain intact; Xamloader's legacy directory consumer explicitly
retains each moved member. Unsupported inherited behavioral labels were omitted.

The neighboring application-identity directory held 88 rules. Fifteen rules
concerning package labels, package names or package signature claims moved to
`objectives/evasion/masquerade/identity/package`; their predicates and metadata
are unchanged. This leaves 73 rules in the original directory and 15 in the new
one, with exact references updated.
