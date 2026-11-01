# Installer source and dependency setup review

The legacy installer staging directory mixed installer source evidence with
payload execution. Its C# rules recognize per-user installation, a TLS protocol
setting, state-file writes, and calls named `Download` and `InstallFile`. These
are compatible with an ordinary installer and do not establish hostile intent.
They now live in `metadata/file/profile/installation`; the final composite is
named for a per-user installer download flow and is suspicious rather than
hostile. The individual source markers are notable, and the inherited T1105
label was removed because the markers alone do not establish ingress tool
transfer. The predicate logic and file/platform constraints are unchanged.

The Xamloader composite referenced the entire legacy installer directory. Its
`any` clause retains that reference and explicitly includes the moved rules,
preserving the prior set of alternatives as the legacy directory shrinks.

The adjacent package-manager install directory held 84 rules. Nineteen rules
concerning Python dependency setup moved to
`micro-behaviors/os/package-manager/dependency-setup`. Their match conditions,
metadata, and exclusions remain unchanged, with references updated. This leaves
65 rules in the original directory and 19 in the new directory; neither relies
on a language-named taxonomy directory.
