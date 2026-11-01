# MSI installer metadata review

Seven composites moved from legacy installer staging. Six describe MSI
metadata, format or API-reference combinations and now live in
`metadata/file/profile/installer-layout`. Their old names claimed droppers,
loaders or masquerading that those combinations did not establish. They are
suspicious rather than hostile, with descriptions of the observed combinations.
The 40 MB and 5 MB thresholds are retained as part of the existing large-file
profiles; they are not treated as independent proof of a payload.

The GoogleAPI-branded MSI rule also requires a signer mismatch and generated
junk strings, in addition to the cabinet, elevation marker and API references.
Its stronger identity-masquerade evidence remains hostile and moved to
`objectives/evasion/masquerade/identity/fabricated`. Its supporting API profile
no longer claims to identify an embedded loader. All seven rules preserve
match legs, scope, sizes, file types, exclusions and confidence. Unsubstantiated
inherited ATT&CK labels were removed. The Xamloader directory-wide consumer
retains all moved members explicitly.

The MSI package-files directory contained 83 traits. Sixteen package identity
claims were reviewed and moved: structured Office summary fields go under
`metadata/document/office/properties`, and the Adobe-branded basename goes
under `metadata/path/software`. This leaves 67 package-file traits. Exact
consumer references were updated and the moved rules retain their predicates
and defaults. These are claims in package metadata, not verified product
identities; the existing MSI routing constraints prevent placing these
individual observations under `well-known/`.
