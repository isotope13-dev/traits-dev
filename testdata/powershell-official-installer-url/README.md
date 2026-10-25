First-party installers and remote evaluation
===========================================

OpenClaw's documented PowerShell install command occurs inside a Markdown
code fence in `install-doc-negative.md`. It must not produce the obsolete
suspicious pipeline aliases. The executable HTTP pipeline in
`untrusted-pipe-positive.ps1` must retain the notable capability
`micro-behaviors/process/deploy/script-eval::powershell-web-response-piped-eval-text`.

A download/evaluate chain alone establishes no C2 or dropper objective.
The Slang version-drift review consolidated the redundant suspicious
`ps-iwr-pipeline-eval` alias into that existing capability and updated
attack-specific consumers to use it directly. Attack context still belongs
in their objective composites; vendor URL mentions do not suppress them.

Run `python3 testdata/powershell-official-installer-url/check.py
<scratch-directory>`. Both fixtures must lack the three obsolete suspicious
aliases; the executable fixture must retain the notable pipeline capability.
