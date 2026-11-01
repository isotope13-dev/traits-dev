# Surrogate wrapper review

Twenty-three rules moved from legacy native-payload staging, reducing that
location from 61 to 38 direct rules. Product-specific Office and diagnostic
tracking strings moved to whole-file product-reference metadata; the Office
Protocol Handler marker, already scoped to `.rdata`, moved to well-known Office.
The unscoped strings could not be placed directly under well-known without
adding unsupported section restrictions; one-to-one well-known wrappers also
fail validation. The Office marker has a 2 GiB validation-required maximum;
the other moved product-reference atoms have no new size bound. The Office
Help user-agent's original signer/vendor exclusions remain on its suspicious
profile, while its underlying text observation is retained separately.

COM/registry combinations now live in COM-registration profiles; embedded PE,
PDB, token, networking and cross-process API combinations live in
embedded-binary profiles. Their labels and severity no longer assert linked
execution, injection or impersonation from references alone. The existing
Active Setup COM-hijack objective, combined with MigHost clues, remains a
hostile persistence rule. Original matching conditions, confidence, explicit
scopes and exclusions are preserved except for the size changes below.

One MigHost combination had a 4 MiB minimum but required three MigHost atoms
whose inherited maximum was 2 MiB, making it unreachable. The minimum was
removed; two Office token/API profile minima of 1,000,000 bytes were also
removed because the conditions do not require them. MigHost marker atoms now
accept up to 2 GiB instead of 2 MiB and no longer have a 64 KiB minimum.
Their consumers can therefore match a wider size range. The MigHost product
identity now additionally requires a verified Microsoft signer and has no
own size threshold; its marker dependencies retain the 2 GiB maximum. This
changes four identity-based suppressions. One duplicate identity exclusion was
removed from a scheduled-task rule because that rule already excludes all
platform-signed binaries, including the verified Microsoft identity.

Synthetic unsigned PE files containing the marker cluster matched the MigHost
command marker below and above 4 MiB, but neither matched the verified identity.
No signed positive identity fixture or full wrapper fixture was tested.

The neighboring binary-debug directory was reduced from 83 to 74 rules by
moving six Mach-O load/section-header observations to section headers and
three Python bytecode source-provenance observations to bytecode. Their
predicates and scopes are unchanged, and references were redirected.
