# GlassWorm role migration

The existing GlassWorm release and compromised-extension identity rules moved
unchanged from `well-known/malware/supply-chain/glassworm` to
`well-known/malware/dropper/glassworm`. The local VSIX-URL reference was
updated; no external YAML references to the old namespace were found. The
dropper role follows the repository's existing GlassWorm loader observations.

Both synthetic fixtures contain VS Code and child-process references and the
same string-array rotation. The positive names the family-specific VSIX URL;
the near miss uses a different repository. Cleave reported the moved GlassWorm
configuration composite only for the positive. Neither fixture is executed.
